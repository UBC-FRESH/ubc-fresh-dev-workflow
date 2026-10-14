"""Policy tests for the GitHub workflows: a pinned runner and actions that run on Node 24."""

from __future__ import annotations

import re
from pathlib import Path

ROOT: Path = Path(__file__).resolve().parents[1]
WORKFLOWS: tuple[Path, ...] = (
    ROOT / ".github" / "workflows" / "ci.yml",
    ROOT / ".github" / "workflows" / "docs.yml",
    ROOT / "templates" / "project" / ".github" / "workflows" / "ci.yml",
    ROOT / "templates" / "project" / ".github" / "workflows" / "docs.yml",
)
RUNNER: str = "ubuntu-24.04"
NODE24_ACTIONS: frozenset[str] = frozenset(
    {
        "actions/checkout@v5",
        "actions/setup-python@v6",
        "actions/upload-artifact@v6",
        "actions/upload-pages-artifact@v5",
        "actions/deploy-pages@v5",
    }
)


def test_every_job_runs_on_the_pinned_runner() -> None:
    """Each workflow names the pinned runner, and none names the floating ubuntu-latest label."""
    for path in WORKFLOWS:
        text = path.read_text(encoding="utf-8")
        runners = re.findall(r"runs-on:\s*(\S+)", text)
        assert runners, path
        assert set(runners) == {RUNNER}, (path, runners)


def test_every_action_is_a_version_that_runs_on_node_24() -> None:
    """Each action reference is one of the versions whose metadata declares Node 24."""
    for path in WORKFLOWS:
        text = path.read_text(encoding="utf-8")
        used = set(re.findall(r"uses:\s*(\S+)", text))
        assert used, path
        assert used <= NODE24_ACTIONS, (path, used - NODE24_ACTIONS)


def test_the_quality_job_checks_the_server_scripts() -> None:
    """The root CI runs shellcheck and bash -n on each script in server/."""
    text = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert "shellcheck server/*.sh" in text
    assert "bash -n" in text
