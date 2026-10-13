"""Self-check: the planning surfaces of this repository pass the workflow validator."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT: Path = Path(__file__).resolve().parents[1]


def test_repository_passes_the_workflow_validator() -> None:
    """The validator finds no errors in this repository."""
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "check_workflow.py"), str(ROOT)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
