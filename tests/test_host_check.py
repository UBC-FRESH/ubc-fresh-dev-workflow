"""Tests for server/host-check.sh, the read-only host checks for the LXD dev server."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

ROOT: Path = Path(__file__).resolve().parents[1]
SCRIPT: Path = ROOT / "server" / "host-check.sh"
BASH: str = shutil.which("bash") or "/bin/bash"
ALLOWED_COMMANDS: frozenset[str] = frozenset(
    {
        "snap list lxd",
        "snap info lxd",
        "id -Gn",
        "lxc list",
        "lxc storage list --format csv",
    }
)
GOOD_STUBS: dict[str, str] = {
    "snap": (
        'case "$*" in\n'
        '  "list lxd") exit 0 ;;\n'
        "  \"info lxd\") printf 'tracking:     latest/stable\\n' ;;\n"
        "  *) exit 1 ;;\n"
        "esac"
    ),
    "id": "printf 'users adm lxd\\n'",
    "lxc": (
        'case "$*" in\n'
        '  "list") exit 0 ;;\n'
        "  \"storage list --format csv\") printf 'default,zfs,,1,CREATED,\\n' ;;\n"
        "  *) exit 1 ;;\n"
        "esac"
    ),
}


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


def snapshot(root: Path) -> dict[str, bytes | None]:
    """Map every path under root to its bytes, or to None for a directory."""
    return {
        path.relative_to(root).as_posix(): (path.read_bytes() if path.is_file() else None)
        for path in root.rglob("*")
    }


def test_every_check_passes_on_a_configured_host(tmp_path: Path) -> None:
    """A host with the snap, the group, the daemon, and a pool passes every check."""
    result, _ = run_script(tmp_path, GOOD_STUBS)
    assert result.returncode == 0, result.stdout + result.stderr
    assert result.stdout.splitlines() == [
        "PASS The LXD snap is installed: yes",
        "PASS The LXD snap tracks the latest/stable channel: latest/stable",
        "PASS The current shell is in the lxd group: yes",
        "PASS The LXD daemon is reachable: yes",
        "PASS A storage pool exists: 1 pool(s), driver: zfs",
    ]


def test_a_user_outside_the_lxd_group_fails_only_that_check(tmp_path: Path) -> None:
    """Group membership is checked on its own, so the other checks still pass."""
    stubs = dict(GOOD_STUBS, id="printf 'users adm\\n'")
    result, _ = run_script(tmp_path, stubs)
    assert result.returncode == 1
    assert "FAIL The current shell is in the lxd group: no" in result.stdout.splitlines()
    assert result.stdout.count("PASS") == 4


def test_a_missing_lxc_is_a_failed_check_and_not_a_crash(tmp_path: Path) -> None:
    """Without lxc, the daemon and pool checks fail with a state, and stderr stays empty."""
    stubs = {"snap": GOOD_STUBS["snap"], "id": GOOD_STUBS["id"]}
    result, commands = run_script(tmp_path, stubs)
    assert result.returncode == 1
    assert "FAIL The LXD daemon is reachable: no" in result.stdout.splitlines()
    assert "FAIL A storage pool exists: none" in result.stdout.splitlines()
    assert result.stderr == ""
    assert not [command for command in commands if command.startswith("lxc ")]


def test_every_command_the_script_runs_is_a_read(tmp_path: Path) -> None:
    """A configured host and a host without lxc both run only the allowed read commands."""
    _, configured = run_script(tmp_path / "configured", GOOD_STUBS)
    _, unconfigured = run_script(
        tmp_path / "unconfigured", {"snap": GOOD_STUBS["snap"], "id": GOOD_STUBS["id"]}
    )
    assert configured
    assert set(configured) <= ALLOWED_COMMANDS
    assert set(unconfigured) <= ALLOWED_COMMANDS


def test_the_script_changes_no_file(tmp_path: Path) -> None:
    """Running the script leaves the working and home directories exactly as they were."""
    run_dir = tmp_path / "run"
    (run_dir / "work").mkdir(parents=True)
    (run_dir / "home").mkdir()
    (run_dir / "work" / "notes.txt").write_text("keep\n", encoding="utf-8")
    before = (snapshot(run_dir / "work"), snapshot(run_dir / "home"))
    result, commands = run_script(run_dir, GOOD_STUBS)
    assert result.returncode == 0, result.stderr
    assert commands, "the script ran no command, so nothing was checked"
    after = (snapshot(run_dir / "work"), snapshot(run_dir / "home"))
    assert after == before


def test_the_output_names_no_path_from_the_machine(tmp_path: Path) -> None:
    """The output prints check names and states only, and no path or group list."""
    result, _ = run_script(tmp_path, GOOD_STUBS)
    assert result.returncode == 0, result.stderr
    assert str(tmp_path) not in result.stdout
    assert "users" not in result.stdout


def test_help_prints_usage_and_runs_no_check(tmp_path: Path) -> None:
    """The help option prints usage, exits with status 0, and runs no command."""
    result, commands = run_script(tmp_path, GOOD_STUBS, "--help")
    assert result.returncode == 0
    assert result.stdout.startswith("usage: host-check.sh")
    assert commands == []


def test_an_unknown_option_is_a_usage_error(tmp_path: Path) -> None:
    """An unknown option exits with status 2, prints usage to stderr, and runs no command."""
    result, commands = run_script(tmp_path, GOOD_STUBS, "--apply")
    assert result.returncode == 2
    assert result.stdout == ""
    assert "usage:" in result.stderr
    assert commands == []


def test_the_script_has_valid_bash_syntax() -> None:
    """The script parses as bash without running it."""
    result = subprocess.run([BASH, "-n", str(SCRIPT)], capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stderr
