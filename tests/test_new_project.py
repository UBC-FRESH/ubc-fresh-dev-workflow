"""Tests for the project initializer."""

from __future__ import annotations

import re
from pathlib import Path

import new_project as initializer
import pytest

TEXT_SUFFIXES = {".md", ".rst", ".txt", ".yml", ".py", ".cff", ".toml"}
PLACEHOLDER = re.compile(r"\{\{[A-Z_]+\}\}")


def render_demo(dest: Path, *, force: bool = False) -> list[Path]:
    return initializer.create_project(
        name="Demo Project",
        slug="demo-project",
        dest=dest,
        owner="UBC-FRESH",
        purpose="A demo project for the tests.",
        today="2026-10-13",
        force=force,
    )


def test_renders_seed_without_leftover_placeholders(tmp_path):
    dest = tmp_path / "demo"
    render_demo(dest)
    assert (dest / "AGENTS.md").is_file()
    assert (dest / "scripts" / "check_workflow.py").is_file()
    for path in dest.rglob("*"):
        if path.is_file() and path.suffix in TEXT_SUFFIXES:
            assert not PLACEHOLDER.search(path.read_text(encoding="utf-8")), path
    assert "Demo Project" in (dest / "README.md").read_text(encoding="utf-8")


def test_generated_project_passes_the_validator(tmp_path):
    dest = tmp_path / "demo"
    render_demo(dest)
    result = initializer.run_validator(dest)
    assert result.returncode == 0, result.stdout + result.stderr


def test_refuses_to_overwrite_without_force(tmp_path):
    dest = tmp_path / "demo"
    dest.mkdir()
    (dest / "AGENTS.md").write_text("mine\n", encoding="utf-8")
    with pytest.raises(FileExistsError):
        render_demo(dest)
    render_demo(dest, force=True)
    assert (dest / "AGENTS.md").read_text(encoding="utf-8") != "mine\n"


def test_rejects_an_invalid_slug(tmp_path):
    with pytest.raises(ValueError):
        initializer.create_project(
            name="Demo",
            slug="Bad Slug",
            dest=tmp_path / "demo",
            owner="UBC-FRESH",
            purpose="A demo.",
            today="2026-10-13",
            force=False,
        )


def test_slugify_produces_a_valid_slug():
    slug = initializer.slugify("My Project: Phase 1!")
    assert slug == "my-project-phase-1"
    assert initializer.SLUG_RE.match(slug)


def test_command_line_derives_the_slug_and_validates(tmp_path, capsys):
    dest = tmp_path / "demo"
    assert initializer.main(["--name", "Demo Project", "--dest", str(dest)]) == 0
    assert "demo-project" in capsys.readouterr().out
    assert (dest / "ROADMAP.md").is_file()
