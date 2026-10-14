"""Tests for server/provision-base.sh, the base container from the host and containers guide."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

ROOT: Path = Path(__file__).resolve().parents[1]
SCRIPT: Path = ROOT / "server" / "provision-base.sh"
GUIDE: Path = ROOT / "docs" / "guides" / "dev-server" / "host-and-containers.rst"
BASH: str = shutil.which("bash") or "/bin/bash"
PACKAGES: str = (
    "git git-annex python3-venv python3-pip build-essential curl ca-certificates jq shellcheck"
)
INSTALL_PACKAGES: str = f"sudo apt-get install -y {PACKAGES}"
IN_BASE: str = "lxc exec fresh-base -- sudo --login --user ubuntu bash -c"
DPKG_CHECK: str = f"{IN_BASE} dpkg -s {PACKAGES}"
UPDATE: str = f"{IN_BASE} sudo apt-get update"
INSTALL: str = f"{IN_BASE} {INSTALL_PACKAGES}"
FRESH_LXC: str = """case "$*" in
  "info fresh-base") exit 1 ;;
  "launch ubuntu:24.04 fresh-base") exit 0 ;;
  "exec fresh-base -- cloud-init status --wait") exit 0 ;;
  *"dpkg -s"*) exit 1 ;;
  *) exit 0 ;;
esac"""
PROVISIONED_LXC: str = """case "$*" in
  "info fresh-base") exit 0 ;;
  *"dpkg -s"*) exit 0 ;;
  *) exit 1 ;;
esac"""
PARTIAL_LXC: str = """case "$*" in
  "info fresh-base") exit 0 ;;
  *"dpkg -s"*) exit 1 ;;
  *) exit 0 ;;
esac"""
LAUNCH_FAILS_LXC: str = """case "$*" in
  "info fresh-base") exit 1 ;;
  *) exit 1 ;;
esac"""


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
    (tmp_path / "home").mkdir(parents=True, exist_ok=True)
    log = tmp_path / "commands.log"
    for name, body in stubs.items():
        write_stub(bin_dir, log, name, body)
    result = subprocess.run(
        [BASH, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        check=False,
        env={"PATH": str(bin_dir), "HOME": str(tmp_path / "home")},
        cwd=tmp_path / "work",
    )
    commands = log.read_text(encoding="utf-8").splitlines() if log.exists() else []
    return result, commands


def guide_base_commands() -> list[str]:
    """Return the commands in the guide's base container section, in the order the guide gives."""
    text = GUIDE.read_text(encoding="utf-8")
    section = text[
        text.index("\nCreate the base container\n") : text.index(
            "\nCreate one container per project\n"
        )
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
    return commands


def plan_commands(output: str) -> list[str]:
    """Return the command lines of a dry-run plan, without its comment lines."""
    return [
        " ".join(line.split())
        for line in output.splitlines()
        if line.strip() and not line.startswith("#")
    ]


def test_the_dry_run_prints_the_guides_base_commands_in_order(tmp_path: Path) -> None:
    """The dry-run prints the guide's base container commands, command for command and in order."""
    result, _ = run_script(tmp_path, {}, "--dry-run")
    assert result.returncode == 0, result.stderr
    expected = guide_base_commands()
    assert len(expected) == 7, expected
    assert plan_commands(result.stdout) == expected


def test_the_dry_run_runs_no_command(tmp_path: Path) -> None:
    """Printing the plan runs no lxc command, so nothing on the host changes."""
    result, commands = run_script(tmp_path, {"lxc": FRESH_LXC}, "--dry-run")
    assert result.returncode == 0, result.stderr
    assert commands == []


def test_apply_on_a_fresh_host_runs_the_steps_in_order(tmp_path: Path) -> None:
    """Without a base, --apply creates it, waits for cloud-init, and then installs the packages."""
    result, commands = run_script(tmp_path, {"lxc": FRESH_LXC}, "--apply")
    assert result.returncode == 0, result.stderr
    assert commands == [
        "lxc info fresh-base",
        "lxc launch ubuntu:24.04 fresh-base",
        "lxc exec fresh-base -- cloud-init status --wait",
        DPKG_CHECK,
        UPDATE,
        INSTALL,
    ]


def test_apply_on_a_provisioned_base_changes_nothing(tmp_path: Path) -> None:
    """A base that exists with its packages installed gets no state-changing command."""
    result, commands = run_script(tmp_path, {"lxc": PROVISIONED_LXC}, "--apply")
    assert result.returncode == 0, result.stderr
    assert "Nothing to do." in result.stdout
    assert commands == ["lxc info fresh-base", DPKG_CHECK]


def test_apply_on_a_base_missing_packages_installs_only_them(tmp_path: Path) -> None:
    """A base that exists but lacks packages is not recreated, and only the install runs."""
    result, commands = run_script(tmp_path, {"lxc": PARTIAL_LXC}, "--apply")
    assert result.returncode == 0, result.stderr
    assert commands == [
        "lxc info fresh-base",
        DPKG_CHECK,
        UPDATE,
        INSTALL,
    ]


def test_apply_stops_at_the_first_failed_step(tmp_path: Path) -> None:
    """A failed launch stops the script before any later step, and exits with status 1."""
    result, commands = run_script(tmp_path, {"lxc": LAUNCH_FAILS_LXC}, "--apply")
    assert result.returncode == 1
    assert "failed: launch the base" in result.stderr
    assert commands == ["lxc info fresh-base", "lxc launch ubuntu:24.04 fresh-base"]


def test_no_mode_or_two_modes_is_a_usage_error(tmp_path: Path) -> None:
    """Running without a mode, or with two, exits with status 2 and runs no command."""
    no_mode, no_mode_commands = run_script(tmp_path / "none", {"lxc": FRESH_LXC})
    two_modes, two_commands = run_script(
        tmp_path / "two", {"lxc": FRESH_LXC}, "--dry-run", "--apply"
    )
    assert no_mode.returncode == 2
    assert "usage:" in no_mode.stderr
    assert two_modes.returncode == 2
    assert two_modes.stdout == ""
    assert no_mode_commands == []
    assert two_commands == []


def test_help_prints_usage_and_runs_no_command(tmp_path: Path) -> None:
    """The help option prints usage, exits with status 0, and runs no command."""
    result, commands = run_script(tmp_path, {"lxc": FRESH_LXC}, "--help")
    assert result.returncode == 0
    assert result.stdout.startswith("usage: provision-base.sh")
    assert commands == []


def test_the_script_has_valid_bash_syntax() -> None:
    """The script parses as bash without running it."""
    result = subprocess.run([BASH, "-n", str(SCRIPT)], capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stderr
