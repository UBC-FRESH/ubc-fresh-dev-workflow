"""Self-check: the planning surfaces of this repository pass the workflow validator."""

from __future__ import annotations

import subprocess
import sys
import tomllib
from pathlib import Path

import check_workflow as cw

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


GATE_WRITES: tuple[str, ...] = (
    ".coverage",
    ".hypothesis/constants/cache",
    "_build/html/index.html",
    "htmlcov/index.html",
    "runtime/dashboard.json",
    "coverage.xml",
    ".pytest_cache/v/cache/nodeids",
    ".ruff_cache/0.1/cache",
    ".mypy_cache/3.12/cache.json",
    "scripts/__pycache__/check_workflow.cpython-312.pyc",
    "tmp/dashboard-seed/README.md",
    ".venv/bin/python",
)


def test_the_repository_gitignore_covers_everything_the_gates_write() -> None:
    """Every output that the gates write is ignored, so the walk never scans it."""
    rules = cw.load_ignore_rules(ROOT)
    missed = [rel for rel in GATE_WRITES if not cw.is_ignored(rel, is_dir=False, rules=rules)]
    assert missed == []


GATE_PAGES: tuple[str, ...] = (
    "AGENTS.md",
    "docs/reference/testing-policy.rst",
    "docs/reference/quality-gates.rst",
    "templates/project/AGENTS.md.tmpl",
)


def test_the_coverage_gate_is_95_percent() -> None:
    """The pytest run enforces 95 percent branch coverage of scripts/."""
    config = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert "--cov-fail-under=95" in config["tool"]["pytest"]["ini_options"]["addopts"].split()


def test_the_pages_that_state_the_coverage_gate_say_95_percent() -> None:
    """Each page that states the coverage gate gives 95 percent, and none still gives 90."""
    for rel in GATE_PAGES:
        text = (ROOT / rel).read_text(encoding="utf-8")
        assert "95 percent" in text, rel
        assert "90 percent" not in text, rel
