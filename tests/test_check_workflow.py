"""Tests for the workflow validator.

Bad fixtures are built at runtime, so this file never contains the patterns that
the validator checks for.
"""

from __future__ import annotations

from pathlib import Path

import check_workflow as cw

FORM_FEED = chr(12)
BOM = chr(0xFEFF)
HOME_PREFIX = "/" + "home" + "/" + "someone" + "/"
GITHUB_TOKEN = "ghp_" + "A" * 36

VALID_ROADMAP = """# Demo Roadmap

## Issue Tracker Map

| Phase | Parent issue | Branch | Status |
| --- | --- | --- | --- |
| P0 Bootstrap | TBD | `feature/p0-bootstrap` | planned |
| P1 Build | #2 | `feature/p1-build` | active |

## Phase 0: Bootstrap

Parent issue: TBD
Branch: `feature/p0-bootstrap`
Status: planned

- [ ] P0.1 First bootstrap task

## Phase 1: Build

Parent issue: #2
Branch: `feature/p1-build`
Status: active

- [ ] P1.1 First build task (#3)
  - [ ] First subtask

## Detailed Next Steps Notes

1. Start P1.1.
"""

VALID_CHANGELOG = """# Change Log

## 2026-10-12

- Earlier entry.

## 2026-10-13

- Later entry.
"""

VALID_LLMS = """# Demo

> Agent index.

- [Index](index.html): home.
"""


def write(root: Path, rel: str, text: str) -> None:
    target = root / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")


def make_repo(root: Path) -> Path:
    for rel in cw.REQUIRED_FILES:
        write(root, rel, "placeholder\n")
    write(root, "ROADMAP.md", VALID_ROADMAP)
    write(root, "CHANGE_LOG.md", VALID_CHANGELOG)
    write(root, "docs/llms.txt", VALID_LLMS)
    write(root, "docs/index.rst", "Demo\n====\n")
    write(root, "README.md", "# Demo\n")
    return root


def error_codes(root: Path) -> set[str]:
    return {diag.code for diag in cw.run(root) if diag.severity == "error"}


def test_valid_repository_has_no_errors(tmp_path):
    assert error_codes(make_repo(tmp_path)) == set()


def test_missing_required_file_is_an_error(tmp_path):
    root = make_repo(tmp_path)
    (root / "AGENTS.md").unlink()
    assert "FILE-MISSING" in error_codes(root)


def test_recommended_file_is_only_a_warning(tmp_path):
    root = make_repo(tmp_path)
    diags = cw.run(root)
    assert any(d.code == "FILE-RECOMMENDED" and d.severity == "warning" for d in diags)
    assert "FILE-MISSING" not in error_codes(root)


def test_phase_numbers_must_increase(tmp_path):
    root = make_repo(tmp_path)
    write(root, "ROADMAP.md", VALID_ROADMAP.replace("## Phase 1: Build", "## Phase 0: Build"))
    assert "ROADMAP-PHASE-ORDER" in error_codes(root)


def test_active_phase_needs_a_parent_issue(tmp_path):
    root = make_repo(tmp_path)
    write(root, "ROADMAP.md", VALID_ROADMAP.replace("Parent issue: #2", "Parent issue: TBD"))
    assert "ROADMAP-PARENT-REQUIRED" in error_codes(root)


def test_complete_phase_needs_checked_tasks(tmp_path):
    root = make_repo(tmp_path)
    text = VALID_ROADMAP.replace("Status: planned", "Status: complete")
    write(root, "ROADMAP.md", text.replace("Parent issue: TBD", "Parent issue: #1"))
    assert "ROADMAP-COMPLETE-OPEN" in error_codes(root)


def test_task_must_belong_to_its_phase(tmp_path):
    root = make_repo(tmp_path)
    text = VALID_ROADMAP.replace("- [ ] P0.1 First bootstrap task", "- [ ] P5.1 Misplaced task")
    write(root, "ROADMAP.md", text)
    assert "ROADMAP-TASK-ID" in error_codes(root)


def test_tracker_must_match_phase_sections(tmp_path):
    root = make_repo(tmp_path)
    write(root, "ROADMAP.md", VALID_ROADMAP.replace("| P1 Build | #2 |", "| P1 Build | #9 |"))
    assert "ROADMAP-TRACKER" in error_codes(root)


def test_unknown_status_is_rejected(tmp_path):
    root = make_repo(tmp_path)
    write(root, "ROADMAP.md", VALID_ROADMAP.replace("Status: active", "Status: wip"))
    assert "ROADMAP-STATUS" in error_codes(root)


def test_changelog_must_be_in_date_order(tmp_path):
    root = make_repo(tmp_path)
    text = "# Change Log\n\n## 2026-10-13\n\n- New.\n\n## 2026-10-12\n\n- Old.\n"
    write(root, "CHANGE_LOG.md", text)
    assert "CHANGELOG-ORDER" in error_codes(root)


def test_changelog_headings_must_be_dates(tmp_path):
    root = make_repo(tmp_path)
    write(root, "CHANGE_LOG.md", "# Change Log\n\n## Unreleased\n\n- Pending.\n")
    assert "CHANGELOG-DATE" in error_codes(root)


def test_broken_local_link_is_an_error(tmp_path):
    root = make_repo(tmp_path)
    write(root, "README.md", "# Demo\n\nSee [the guide](docs/missing.rst).\n")
    assert "LINK-BROKEN" in error_codes(root)


def test_external_and_anchor_links_are_ignored(tmp_path):
    root = make_repo(tmp_path)
    write(root, "README.md", "# Demo\n\n[site](https://example.org/x) and [top](#demo).\n")
    assert error_codes(root) == set()


def test_llms_index_must_point_at_existing_pages(tmp_path):
    root = make_repo(tmp_path)
    write(root, "docs/llms.txt", "# Demo\n\n- [Ghost](ghost.html): no page.\n")
    assert "LLMS-BROKEN" in error_codes(root)


def test_control_characters_are_rejected(tmp_path):
    root = make_repo(tmp_path)
    write(root, "README.md", f"# Demo\n\nBranch: eature{FORM_FEED}/p0\n")
    assert "CONTROL-CHAR" in error_codes(root)


def test_byte_order_mark_is_rejected(tmp_path):
    root = make_repo(tmp_path)
    write(root, "README.md", f"{BOM}# Demo\n")
    assert "BOM" in error_codes(root)


def test_carriage_returns_are_rejected(tmp_path):
    root = make_repo(tmp_path)
    (root / "README.md").write_bytes(b"# Demo\r\n")
    assert "CONTROL-CHAR" in error_codes(root)


def test_personal_paths_are_rejected_but_placeholders_pass(tmp_path):
    root = make_repo(tmp_path)
    write(root, "README.md", f"Clone into {HOME_PREFIX}projects/demo\n")
    assert "PATH-PERSONAL" in error_codes(root)
    write(root, "README.md", "Clone into /home/<user>/projects/demo\n")
    assert "PATH-PERSONAL" not in error_codes(root)


def test_secret_shapes_are_rejected(tmp_path):
    root = make_repo(tmp_path)
    write(root, "notes/leak.md", f"token {GITHUB_TOKEN}\n")
    assert "SECRET-SHAPED" in error_codes(root)


def test_files_mode_checks_a_single_body(tmp_path):
    body = tmp_path / "body.md"
    body.write_text(f"Branch: eature{FORM_FEED}/p0\n", encoding="utf-8")
    assert cw.main(["--files", str(body)]) == 1
    clean = tmp_path / "clean.md"
    clean.write_text("Branch: `feature/p0`\n", encoding="utf-8")
    assert cw.main(["--files", str(clean)]) == 0
