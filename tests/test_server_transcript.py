"""The committed dry-run transcript of the server scripts matches what the scripts print."""

from __future__ import annotations

import shlex
import subprocess
from pathlib import Path

ROOT: Path = Path(__file__).resolve().parents[1]
TRANSCRIPT: Path = ROOT / "notes" / "reference" / "server-dry-run-transcript.md"


def transcript_blocks() -> list[tuple[str, str]]:
    """Return each (command, expected output) pair from the transcript's text blocks."""
    blocks: list[tuple[str, str]] = []
    lines = TRANSCRIPT.read_text(encoding="utf-8").splitlines()
    index = 0
    while index < len(lines):
        if lines[index] == "```text":
            end = lines.index("```", index + 1)
            body = lines[index + 1 : end]
            assert body, index
            assert body[0].startswith("$ "), body[:1]
            output = "".join(line + "\n" for line in body[1:])
            blocks.append((body[0][2:], output))
            index = end
        index += 1
    return blocks


def test_the_transcript_holds_the_two_dry_runs() -> None:
    """The transcript records the dry run of each script that has one, and nothing else."""
    blocks = transcript_blocks()
    assert [shlex.split(command)[0] for command, _ in blocks] == [
        "server/provision-base.sh",
        "server/new-project-container.sh",
    ]


def test_each_dry_run_output_matches_the_transcript() -> None:
    """Running each recorded command prints exactly the text recorded for it."""
    for command, expected in transcript_blocks():
        result = subprocess.run(
            shlex.split(command),
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
            env={"PATH": "/usr/bin:/bin"},
        )
        assert result.returncode == 0, (command, result.stderr)
        assert result.stdout == expected, command
