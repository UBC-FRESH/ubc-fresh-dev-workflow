"""Tests for the project initializer."""

from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

import pytest

import check_workflow as cw
import new_project as initializer

TEXT_SUFFIXES: frozenset[str] = frozenset({".md", ".rst", ".txt", ".yml", ".py", ".cff", ".toml"})
PLACEHOLDER: re.Pattern[str] = re.compile(r"\{\{[A-Z_]+\}\}")
GATE_OUTPUTS: tuple[str, ...] = (
    ".coverage",
    ".coverage.worker",
    "coverage.xml",
    "htmlcov/index.html",
    "runtime/dashboard.json",
    ".hypothesis/constants/cache",
)
GIT_REQUIRED = pytest.mark.skipif(shutil.which("git") is None, reason="git is not installed")


def render_demo(dest: Path, *, force: bool = False) -> list[Path]:
    """Render the seed with fixed demo inputs.

    Parameters
    ----------
    dest : Path
        Destination directory.
    force : bool, optional
        Whether existing files may be overwritten.

    Returns
    -------
    list of Path
        The files that were written.
    """
    return initializer.create_project(
        name="Demo Project",
        slug="demo-project",
        dest=dest,
        owner="UBC-FRESH",
        purpose="A demo project for the tests.",
        today="2026-10-13",
        force=force,
    )


def test_renders_seed_without_leftover_placeholders(tmp_path: Path) -> None:
    """Every rendered text file is free of placeholder tokens, and the names are filled in."""
    dest = tmp_path / "demo"
    render_demo(dest)
    assert (dest / "AGENTS.md").is_file()
    assert (dest / "scripts" / "check_workflow.py").is_file()
    for path in dest.rglob("*"):
        if path.is_file() and path.suffix in TEXT_SUFFIXES:
            assert not PLACEHOLDER.search(path.read_text(encoding="utf-8")), path
    assert "Demo Project" in (dest / "README.md").read_text(encoding="utf-8")


def test_generated_project_passes_the_validator(tmp_path: Path) -> None:
    """A generated project passes the validator that was copied into it."""
    dest = tmp_path / "demo"
    render_demo(dest)
    result = initializer.run_validator(dest)
    assert result.returncode == 0, result.stdout + result.stderr


def test_generated_phase_0_holds_only_local_tasks(tmp_path: Path) -> None:
    """Repository creation is an activation step, so the rendered Phase 0 has no GitHub task."""
    dest = tmp_path / "demo"
    render_demo(dest)
    lines = (dest / "ROADMAP.md").read_text(encoding="utf-8").splitlines()
    phase_0 = next(phase for phase in cw.parse_roadmap(lines) if phase.number == 0)
    assert [(task.phase, task.number) for task in phase_0.tasks] == [(0, 1), (0, 2)]
    start = phase_0.line - 1
    following = [index for index in range(start + 1, len(lines)) if lines[index].startswith("## ")]
    section = "\n".join(lines[start : following[0] if following else len(lines)]).lower()
    assert "github" not in section
    assert "repository" not in section


def test_generated_phase_carries_an_acceptance_criteria_block(tmp_path: Path) -> None:
    """Every phase of a rendered roadmap carries an Acceptance criteria block."""
    dest = tmp_path / "demo"
    render_demo(dest)
    lines = (dest / "ROADMAP.md").read_text(encoding="utf-8").splitlines()
    phases = cw.parse_roadmap(lines)
    assert phases
    for phase in phases:
        start = phase.line - 1
        following = [
            index for index in range(start + 1, len(lines)) if lines[index].startswith("## ")
        ]
        section = lines[start : following[0] if following else len(lines)]
        assert "Acceptance criteria:" in section, phase.number
        after = section[section.index("Acceptance criteria:") + 1 :]
        bullets = [line for line in after if line.startswith("- ")]
        assert len(bullets) == 1, phase.number
        assert bullets[0].startswith("- <"), phase.number


def test_generated_lifecycle_map_lists_the_six_stages(tmp_path: Path) -> None:
    """The rendered Lifecycle Map names the six stages of the lifecycle reference, in order."""
    dest = tmp_path / "demo"
    render_demo(dest)
    lines = (dest / "ROADMAP.md").read_text(encoding="utf-8").splitlines()
    start = lines.index("## Lifecycle Map")
    following = [index for index in range(start + 1, len(lines)) if lines[index].startswith("## ")]
    section = lines[start : following[0] if following else len(lines)]
    stages = [
        line.split("|")[1].strip()
        for line in section
        if line.startswith("| ") and line.split("|")[1].strip() not in ("Stage", "---")
    ]
    assert stages == [
        "Scope and design",
        "Build",
        "Verify",
        "Release and deploy",
        "Operate and maintain",
        "Retire",
    ]


def test_refuses_to_fill_a_non_empty_directory_without_force(tmp_path: Path) -> None:
    """A non-empty destination is kept unless the caller forces the render."""
    dest = tmp_path / "demo"
    dest.mkdir()
    (dest / "AGENTS.md").write_text("mine\n", encoding="utf-8")
    with pytest.raises(FileExistsError, match="not empty"):
        render_demo(dest)
    assert (dest / "AGENTS.md").read_text(encoding="utf-8") == "mine\n"
    render_demo(dest, force=True)
    assert (dest / "AGENTS.md").read_text(encoding="utf-8") != "mine\n"


@pytest.mark.parametrize(
    ("name", "slug", "owner", "match"),
    [
        ("D", "demo", "UBC-FRESH", "project name"),
        ('Bad "name"', "demo", "UBC-FRESH", "project name"),
        ("Demo", "Bad Slug", "UBC-FRESH", "slug"),
        ("Demo", "demo", "-bad-owner", "owner"),
    ],
)
def test_rejects_invalid_inputs(
    tmp_path: Path, name: str, slug: str, owner: str, match: str
) -> None:
    """Names, slugs, and owners that would break rendered files are rejected."""
    with pytest.raises(ValueError, match=match):
        initializer.create_project(
            name=name,
            slug=slug,
            dest=tmp_path / "demo",
            owner=owner,
            purpose="A demo.",
            today="2026-10-13",
            force=False,
        )


def test_slugify_produces_a_valid_slug() -> None:
    """A project name becomes a slug that passes the slug pattern."""
    slug = initializer.slugify("My Project: Phase 1!")
    assert slug == "my-project-phase-1"
    assert initializer.SLUG_RE.match(slug)


def test_slugify_limits_the_length() -> None:
    """A very long name is cut to the 63-character slug limit."""
    assert len(initializer.slugify("a" * 200)) == 63


def test_build_tokens_fills_the_title_rule_and_the_year() -> None:
    """The title underline matches the name length, and the year comes from the date."""
    tokens = initializer.build_tokens("Demo", "demo", "UBC-FRESH", "Purpose.", "2026-10-13")
    assert tokens["{{TITLE_RULE}}"] == "===="
    assert tokens["{{YEAR}}"] == "2026"


def test_render_leaves_unknown_tokens_in_place() -> None:
    """Known tokens are replaced, and unknown tokens are left for the caller to reject."""
    tokens = {"{{PROJECT_NAME}}": "Demo"}
    assert initializer.render("{{PROJECT_NAME}} {{OTHER}}", tokens) == "Demo {{OTHER}}"


def test_plan_seed_includes_the_validator_and_skips_directories(tmp_path: Path) -> None:
    """The plan covers every seed file, marks templates, and copies the validator."""
    (tmp_path / "nested").mkdir()
    (tmp_path / "nested" / "plain.txt").write_text("plain\n", encoding="utf-8")
    (tmp_path / "rendered.md.tmpl").write_text("{{PROJECT_NAME}}\n", encoding="utf-8")
    plan = initializer.plan_seed(tmp_path)
    destinations = {str(target): is_template for _, target, is_template in plan}
    assert destinations["rendered.md"] is True
    assert destinations[str(Path("nested") / "plain.txt")] is False
    assert destinations[str(Path("scripts") / "check_workflow.py")] is False


def test_plan_seed_rejects_two_sources_for_one_destination(tmp_path: Path) -> None:
    """Two seed files that write the same destination are rejected before rendering."""
    (tmp_path / "AGENTS.md").write_text("one\n", encoding="utf-8")
    (tmp_path / "AGENTS.md.tmpl").write_text("two\n", encoding="utf-8")
    with pytest.raises(ValueError, match="same destination"):
        initializer.plan_seed(tmp_path)


def test_unrendered_placeholder_is_a_runtime_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A template with an unknown placeholder fails the render instead of leaking it."""
    seed = tmp_path / "seed"
    seed.mkdir()
    (seed / "BROKEN.md.tmpl").write_text("{{NOT_A_TOKEN}}\n", encoding="utf-8")
    monkeypatch.setattr(initializer, "SEED_DIR", seed)
    with pytest.raises(RuntimeError, match="unrendered"):
        render_demo(tmp_path / "out")


def test_generated_project_carries_the_shared_gates(tmp_path: Path) -> None:
    """A generated project receives the validator, the dashboard, and the gate configuration."""
    dest = tmp_path / "demo"
    render_demo(dest)
    for rel in initializer.SHARED_FRAMEWORK_FILES:
        assert (dest / rel).is_file(), rel
    assert "[tool.mypy]" in (dest / "pyproject.toml").read_text(encoding="utf-8")


def test_command_line_derives_the_slug_and_validates(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The command derives the slug from the name, prints next steps, and returns 0."""
    dest = tmp_path / "demo"
    assert initializer.main(["--name", "Demo Project", "--dest", str(dest)]) == 0
    output = capsys.readouterr().out
    assert "demo-project" in output
    assert "gh repo create UBC-FRESH/demo-project" in output
    assert (dest / "ROADMAP.md").is_file()


def test_command_line_returns_two_for_rejected_inputs(tmp_path: Path) -> None:
    """A rejected input makes the command return status 2 and write nothing."""
    assert initializer.main(["--name", "x", "--dest", str(tmp_path / "demo")]) == 2
    assert not (tmp_path / "demo").exists()


def test_command_line_returns_one_when_the_generated_project_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A generated project that fails the validator makes the command return status 1."""

    def failing(dest: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(
            args=[str(dest)], returncode=1, stdout="", stderr="bad\n"
        )

    monkeypatch.setattr(initializer, "run_validator", failing)
    assert initializer.main(["--name", "Demo", "--dest", str(tmp_path / "demo")]) == 1
    assert "failed validation" in capsys.readouterr().err


@GIT_REQUIRED
def test_generated_project_ignores_the_files_its_gates_write(tmp_path: Path) -> None:
    """A new project's git repository ignores the coverage, runtime, and Hypothesis outputs."""
    dest = tmp_path / "demo"
    render_demo(dest)
    subprocess.run(["git", "-C", str(dest), "init", "-q"], check=True)
    for rel in GATE_OUTPUTS:
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("output\n", encoding="utf-8")
    for rel in GATE_OUTPUTS:
        check = subprocess.run(
            ["git", "-C", str(dest), "check-ignore", "-q", rel],
            capture_output=True,
            check=False,
        )
        assert check.returncode == 0, f"{rel} is not ignored by the generated project"
