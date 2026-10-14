"""Tests for server/new-project-container.sh, the per-project container of the guide."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

ROOT: Path = Path(__file__).resolve().parents[1]
SCRIPT: Path = ROOT / "server" / "new-project-container.sh"
GUIDE: Path = ROOT / "docs" / "guides" / "dev-server" / "host-and-containers.rst"
BASH: str = shutil.which("bash") or "/bin/bash"
NAME: str = "fresh-project-a"
PORT: str = "18080"
LIST_COMMAND: str = "lxc list -c n --format csv"
EMPTY_LXC: str = """case "$*" in
  "list -c n --format csv") exit 0 ;;
  "copy fresh-base fresh-project-a") exit 0 ;;
  "start fresh-project-a") exit 0 ;;
  "config device add fresh-project-a workspace"*) exit 0 ;;
  "config device add fresh-project-a ide"*) exit 0 ;;
  *) exit 1 ;;
esac"""
NAME_TAKEN_LXC: str = """case "$*" in
  "list -c n --format csv") printf 'fresh-project-a\\n' ;;
  *) exit 1 ;;
esac"""
PORT_TAKEN_LXC: str = """case "$*" in
  "list -c n --format csv") printf 'other\\n' ;;
  "config device show other") printf 'ide:\\n  listen: tcp:127.0.0.1:18080\\n  type: proxy\\n' ;;
  *) exit 1 ;;
esac"""
COPY_FAILS_LXC: str = """case "$*" in
  "list -c n --format csv") exit 0 ;;
  "copy fresh-base fresh-project-a") exit 1 ;;
  *) exit 0 ;;
esac"""
LIST_FAILS_LXC: str = "exit 1"


def write_stub(bin_dir: Path, log: Path, name: str, body: str) -> None:
    """Write an executable stub that logs its command line, and then runs its body."""
    stub = bin_dir / name
    stub.write_text(
        f"#!/bin/sh\nprintf '%s %s\\n' '{name}' \"$*\" >> '{log}'\n{body}\n",
        encoding="utf-8",
    )
    stub.chmod(0o755)


def run_script(
    tmp_path: Path, stubs: dict[str, str], *args: str
) -> tuple[subprocess.CompletedProcess[str], list[str]]:
    """Run the script with only the stubs on its PATH, and return its result and its commands."""
    bin_dir = tmp_path / "stubs"
    bin_dir.mkdir(parents=True, exist_ok=True)
    (tmp_path / "work").mkdir(parents=True, exist_ok=True)
    log = tmp_path / "commands.log"
    for name, body in stubs.items():
        write_stub(bin_dir, log, name, body)
    result = subprocess.run(
        [BASH, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        check=False,
        env={"PATH": str(bin_dir), "HOME": str(tmp_path)},
        cwd=tmp_path / "work",
    )
    commands = log.read_text(encoding="utf-8").splitlines() if log.exists() else []
    return result, commands


def make_workspace(tmp_path: Path) -> Path:
    """Create the project's workspace directory, which the script mounts."""
    workspace = tmp_path / "project-a"
    workspace.mkdir(parents=True, exist_ok=True)
    return workspace


def guide_container_commands() -> list[str]:
    """Return the lxc commands of the guide's per-project section, in the order the guide gives."""
    text = GUIDE.read_text(encoding="utf-8")
    section = text[
        text.index("\nCreate one container per project\n") : text.index("\nSnapshots and backups\n")
    ]
    commands: list[str] = []
    in_block = False
    joined = ""
    for raw in section.splitlines():
        if raw.strip() == ".. code-block:: bash":
            in_block = True
            continue
        if not in_block or not raw.strip():
            continue
        if not raw.startswith("   "):
            in_block = False
            continue
        line = raw.strip()
        if line.endswith("\\"):
            joined += line[:-1].rstrip() + " "
        else:
            commands.append(" ".join((joined + line).split()))
            joined = ""
    return [command for command in commands if command.startswith("lxc ")]


def plan_commands(output: str) -> list[str]:
    """Return the command lines of a dry-run plan, without its comment lines."""
    return [
        " ".join(line.split())
        for line in output.splitlines()
        if line.strip() and not line.startswith("#")
    ]


def test_the_dry_run_prints_the_guides_per_project_commands(tmp_path: Path) -> None:
    """With the guide's example values, the plan is the guide's four lxc commands, in order."""
    workspace = make_workspace(tmp_path)
    result, commands = run_script(tmp_path, {}, "--dry-run", NAME, str(workspace), PORT)
    assert result.returncode == 0, result.stderr
    expected = [
        command.replace("/srv/projects/project-a", str(workspace))
        for command in guide_container_commands()
    ]
    assert len(expected) == 4, expected
    assert plan_commands(result.stdout) == expected
    assert commands == []
    assert not (workspace / "fresh-project-a.code-workspace").exists()


def test_the_dry_run_plans_a_workspace_that_does_not_exist_yet(tmp_path: Path) -> None:
    """A dry run only plans, so the workspace need not exist. --apply still requires it."""
    missing = tmp_path / "not-yet"
    result, commands = run_script(tmp_path, {}, "--dry-run", NAME, str(missing), PORT)
    assert result.returncode == 0, result.stderr
    assert f"source={missing}" in result.stdout
    assert commands == []


def test_apply_creates_the_container_and_writes_a_valid_workspace_file(tmp_path: Path) -> None:
    """A free name and port give a copied, started container and a valid .code-workspace file."""
    workspace = make_workspace(tmp_path)
    result, commands = run_script(
        tmp_path, {"lxc": EMPTY_LXC}, "--apply", NAME, str(workspace), PORT
    )
    assert result.returncode == 0, result.stderr
    assert commands == [
        LIST_COMMAND,
        "lxc copy fresh-base fresh-project-a",
        "lxc start fresh-project-a",
        f"lxc config device add fresh-project-a workspace disk source={workspace} "
        "path=/workspace shift=true",
        "lxc config device add fresh-project-a ide proxy "
        "listen=tcp:127.0.0.1:18080 connect=tcp:127.0.0.1:8080",
    ]
    data = json.loads((workspace / "fresh-project-a.code-workspace").read_text(encoding="utf-8"))
    assert data == {"folders": [{"name": NAME, "path": "."}]}


def test_a_taken_name_stops_before_any_change(tmp_path: Path) -> None:
    """An existing container with the same name stops the script before any change."""
    workspace = make_workspace(tmp_path)
    result, commands = run_script(
        tmp_path, {"lxc": NAME_TAKEN_LXC}, "--apply", NAME, str(workspace), PORT
    )
    assert result.returncode == 1
    assert "container fresh-project-a already exists. Nothing was changed." in result.stderr
    assert commands == [LIST_COMMAND]
    assert not (workspace / "fresh-project-a.code-workspace").exists()


def test_a_taken_port_stops_before_any_change(tmp_path: Path) -> None:
    """A port that another container already forwards stops the script before any change."""
    workspace = make_workspace(tmp_path)
    result, commands = run_script(
        tmp_path, {"lxc": PORT_TAKEN_LXC}, "--apply", NAME, str(workspace), PORT
    )
    assert result.returncode == 1
    assert "port 18080 is already forwarded by other. Nothing was changed." in result.stderr
    assert commands == [LIST_COMMAND, "lxc config device show other"]
    assert not (workspace / "fresh-project-a.code-workspace").exists()


def test_an_existing_workspace_file_is_not_overwritten(tmp_path: Path) -> None:
    """A workspace file that already exists stops the script, and its content is kept."""
    workspace = make_workspace(tmp_path)
    target = workspace / "fresh-project-a.code-workspace"
    target.write_text("keep\n", encoding="utf-8")
    result, commands = run_script(
        tmp_path, {"lxc": EMPTY_LXC}, "--apply", NAME, str(workspace), PORT
    )
    assert result.returncode == 1
    assert "already exists. Nothing was changed." in result.stderr
    assert commands == [LIST_COMMAND]
    assert target.read_text(encoding="utf-8") == "keep\n"


def test_a_failed_copy_stops_the_script_and_writes_no_file(tmp_path: Path) -> None:
    """A failed copy stops the script before the later steps, and it writes no file."""
    workspace = make_workspace(tmp_path)
    result, commands = run_script(
        tmp_path, {"lxc": COPY_FAILS_LXC}, "--apply", NAME, str(workspace), PORT
    )
    assert result.returncode == 1
    assert "failed: copy the base" in result.stderr
    assert commands == [LIST_COMMAND, "lxc copy fresh-base fresh-project-a"]
    assert not (workspace / "fresh-project-a.code-workspace").exists()


def test_a_failed_listing_stops_before_any_change(tmp_path: Path) -> None:
    """If the containers cannot be listed, the script cannot check them, so it stops."""
    workspace = make_workspace(tmp_path)
    result, commands = run_script(
        tmp_path, {"lxc": LIST_FAILS_LXC}, "--apply", NAME, str(workspace), PORT
    )
    assert result.returncode == 1
    assert "could not list the containers. Nothing was changed." in result.stderr
    assert commands == [LIST_COMMAND]


def test_bad_arguments_are_usage_errors_and_run_no_command(tmp_path: Path) -> None:
    """Bad or missing arguments exit with status 2 before any lxc call."""
    workspace = make_workspace(tmp_path)
    cases: list[list[str]] = [
        [],
        ["--apply", "Fresh_Project", str(workspace), PORT],
        ["--apply", NAME, str(workspace), "80"],
        ["--apply", NAME, "project-a", PORT],
        ["--apply", NAME, str(tmp_path / "missing"), PORT],
        ["--apply-now", NAME, str(workspace), PORT],
    ]
    for index, args in enumerate(cases):
        result, commands = run_script(tmp_path / str(index), {"lxc": EMPTY_LXC}, *args)
        assert result.returncode == 2, args
        assert result.stdout == "", args
        assert "usage:" in result.stderr, args
        assert commands == [], args


def test_help_prints_usage_and_runs_no_command(tmp_path: Path) -> None:
    """The help option prints usage, exits with status 0, and runs no command."""
    result, commands = run_script(tmp_path, {"lxc": EMPTY_LXC}, "--help")
    assert result.returncode == 0
    assert result.stdout.startswith("usage: new-project-container.sh")
    assert commands == []


def test_the_script_has_valid_bash_syntax() -> None:
    """The script parses as bash without running it."""
    result = subprocess.run([BASH, "-n", str(SCRIPT)], capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stderr
