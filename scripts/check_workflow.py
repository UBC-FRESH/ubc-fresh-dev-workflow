#!/usr/bin/env python3
"""Check a repository against the UBC-FRESH dev workflow surfaces.

This script is the oracle for the planning surfaces. It parses ``ROADMAP.md``
and ``CHANGE_LOG.md``, resolves local Markdown links and the ``docs/llms.txt``
index, and scans tracked text for defects that must not reach a public
repository: control characters, byte-order marks, personal paths, and
secret-shaped strings. It uses only the standard library, so it runs in a fresh
clone before anything is installed.

Usage::

    python scripts/check_workflow.py [ROOT]
    python scripts/check_workflow.py --files PATH [PATH ...]

The exit status is 0 when no errors are found. Warnings are printed but do not
fail the run. Finding codes are stable; see docs/agents/oracles-and-evidence.rst.
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import sys
from collections.abc import Iterator
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parent.parent
SELF_RELPATH = "scripts/check_workflow.py"
SKIP_DIRS = frozenset(
    {
        ".git",
        ".venv",
        "venv",
        "_build",
        "tmp",
        "__pycache__",
        ".pytest_cache",
        ".ruff_cache",
        ".mypy_cache",
        "node_modules",
    }
)
SKIP_TOP_LEVEL = frozenset({"tests"})
MAX_SCAN_BYTES = 1_000_000
PHASE_STATUSES = ("planned", "active", "pr-open", "complete", "deferred")
OPEN_STATUSES = ("active", "pr-open", "complete")

REQUIRED_FILES = (
    "README.md",
    "AGENTS.md",
    "ROADMAP.md",
    "CHANGE_LOG.md",
    "notes/README.md",
    "docs/conf.py",
    "docs/index.rst",
    "docs/llms.txt",
    "docs/requirements.txt",
    "requirements-dev.txt",
    ".gitignore",
    "scripts/check_workflow.py",
    ".github/ISSUE_TEMPLATE/phase.md",
    ".github/ISSUE_TEMPLATE/task.md",
    ".github/workflows/ci.yml",
    ".github/workflows/docs.yml",
    "tests/test_workflow.py",
)
RECOMMENDED_FILES = ("LICENSE", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "CITATION.cff")

PHASE_RE = re.compile(r"^## Phase (\d+):\s*(.+?)\s*$")
PARENT_RE = re.compile(r"^Parent issue:\s*(#\d+|TBD)\s*$")
BRANCH_RE = re.compile(r"^Branch:\s*`([^`\s]+)`\s*$")
STATUS_RE = re.compile(r"^Status:\s*([a-z-]+)\s*$")
TASK_RE = re.compile(r"^- \[( |x|X)\] P(\d+)\.(\d+)\s+(.+?)\s*$")
SUBTASK_RE = re.compile(r"^\s{2,}- \[( |x|X)\]\s+\S")
ISSUE_REF_RE = re.compile(r"\(#(\d+)\)\s*$")
TRACKER_RE = re.compile(r"^\|\s*P(\d+)\b")
LINK_RE = re.compile(r"\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
PERSONAL_PATTERNS = (
    (re.compile(r"/home/(?![<${])[A-Za-z0-9._-]+/"), "Linux home directory path"),
    (re.compile(r"/Users/(?![<${])[A-Za-z0-9._-]+/"), "macOS home directory path"),
    (re.compile(r"[A-Za-z]:\\Users\\(?![<${])"), "Windows user profile path"),
)
SECRET_PATTERNS = (
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"), "GitHub token"),
    (re.compile(r"\bgithub_pat_[A-Za-z0-9_]{30,}"), "GitHub fine-grained token"),
    (re.compile(r"\bpypi-[A-Za-z0-9_-]{40,}"), "PyPI token"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "AWS access key id"),
    (re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----"), "private key"),
    (
        re.compile(
            r"(?i)\b(?:password|passwd|secret|api[_-]?key|token)\s*[:=]\s*"
            r"[\"']?[A-Za-z0-9/+_-]{16,}"
        ),
        "credential assignment",
    ),
)


@dataclass(frozen=True)
class Diagnostic:
    """One finding: its severity, stable code, location, and message."""

    severity: str
    code: str
    path: str
    line: int
    message: str

    def render(self) -> str:
        """Return the finding as one line of text."""
        where = f"{self.path}:{self.line}" if self.line else self.path
        return f"{self.severity:<8}{self.code:<22}{where}  {self.message}"


def error(code: str, path: str, line: int, message: str) -> Diagnostic:
    """Build an error finding."""
    return Diagnostic("error", code, path, line, message)


def warning(code: str, path: str, line: int, message: str) -> Diagnostic:
    """Build a warning finding."""
    return Diagnostic("warning", code, path, line, message)


@dataclass
class Task:
    """A task line in a phase section, with its subtask lines."""

    phase: int
    number: int
    checked: bool
    line: int
    issue: int | None
    subtasks: list[tuple[int, bool]] = field(default_factory=list)


@dataclass
class Phase:
    """A '## Phase <n>:' section, its header lines, and its tasks."""

    number: int
    line: int
    parent: str | None = None
    branch: str | None = None
    status: str | None = None
    tasks: list[Task] = field(default_factory=list)


def iter_text_files(root: Path) -> Iterator[Path]:
    """Yield tracked-looking UTF-8 text files under root, skipping ignored paths."""
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(name for name in dirnames if name not in SKIP_DIRS)
        for name in sorted(filenames):
            path = Path(dirpath) / name
            rel = path.relative_to(root)
            if rel.parts[0] in SKIP_TOP_LEVEL or rel.as_posix() == SELF_RELPATH:
                continue
            if path.is_symlink() or not path.is_file():
                continue
            if path.stat().st_size > MAX_SCAN_BYTES or not _is_utf8(path):
                continue
            yield path


def _is_utf8(path: Path) -> bool:
    try:
        path.read_bytes().decode("utf-8")
    except UnicodeDecodeError:
        return False
    return True


def _read_text(path: Path) -> str:
    return path.read_bytes().decode("utf-8", errors="replace")


def _read_lines(path: Path) -> list[str]:
    return _read_text(path).split("\n")


def _is_local_target(target: str) -> bool:
    if target.startswith(("http://", "https://", "mailto:", "#", "<")):
        return False
    return "{{" not in target and "<" not in target


def _strip_fragment(target: str) -> str:
    return target.split("#", 1)[0]


def _issue_ref(text: str) -> int | None:
    match = ISSUE_REF_RE.search(text)
    return int(match.group(1)) if match else None


def parse_roadmap(lines: list[str]) -> list[Phase]:
    """Parse the phase sections of a roadmap into Phase records."""
    phases: list[Phase] = []
    current: Phase | None = None
    task: Task | None = None
    for lineno, raw in enumerate(lines, start=1):
        line = raw.rstrip()
        if line.startswith("## "):
            match = PHASE_RE.match(line)
            current = Phase(number=int(match.group(1)), line=lineno) if match else None
            if current is not None:
                phases.append(current)
            task = None
            continue
        if current is None:
            continue
        parent = PARENT_RE.match(line)
        if parent and current.parent is None:
            current.parent = parent.group(1)
        branch = BRANCH_RE.match(line)
        if branch and current.branch is None:
            current.branch = branch.group(1)
        status = STATUS_RE.match(line)
        if status and current.status is None:
            current.status = status.group(1)
        task_match = TASK_RE.match(line)
        if task_match:
            task = Task(
                phase=int(task_match.group(2)),
                number=int(task_match.group(3)),
                checked=task_match.group(1) in ("x", "X"),
                line=lineno,
                issue=_issue_ref(task_match.group(4)),
            )
            current.tasks.append(task)
            continue
        subtask = SUBTASK_RE.match(line)
        if subtask and task is not None:
            task.subtasks.append((lineno, subtask.group(1) in ("x", "X")))
    return phases


def parse_tracker(lines: list[str]) -> list[tuple[int, list[str], int]]:
    """Return (phase number, table cells, line number) for each tracker row."""
    rows: list[tuple[int, list[str], int]] = []
    for lineno, raw in enumerate(lines, start=1):
        line = raw.strip()
        match = TRACKER_RE.match(line)
        if match is None:
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        rows.append((int(match.group(1)), cells, lineno))
    return rows


def _check_phase(path: str, phase: Phase) -> list[Diagnostic]:
    diags: list[Diagnostic] = []
    label = f"P{phase.number}"
    where = phase.line
    header = (("Parent issue", phase.parent), ("Branch", phase.branch), ("Status", phase.status))
    for name, value in header:
        if value is None:
            diags.append(error("ROADMAP-PHASE-META", path, where, f"{label} has no '{name}:' line"))
    if phase.status is not None and phase.status not in PHASE_STATUSES:
        allowed = ", ".join(PHASE_STATUSES)
        diags.append(
            error(
                "ROADMAP-STATUS",
                path,
                where,
                f"{label} status '{phase.status}' is not one of {allowed}",
            )
        )
    if phase.parent == "TBD" and phase.status in OPEN_STATUSES:
        diags.append(
            error(
                "ROADMAP-PARENT-REQUIRED",
                path,
                where,
                f"{label} is {phase.status} but has no parent issue; create it first",
            )
        )
    seen: set[int] = set()
    for task in phase.tasks:
        task_label = f"P{task.phase}.{task.number}"
        if task.phase != phase.number:
            diags.append(
                error("ROADMAP-TASK-ID", path, task.line, f"{task_label} sits under {label}")
            )
        if task.number in seen:
            diags.append(
                error("ROADMAP-TASK-ID", path, task.line, f"{task_label} repeats in {label}")
            )
        seen.add(task.number)
        if phase.status != "complete":
            continue
        if not task.checked:
            diags.append(
                error(
                    "ROADMAP-COMPLETE-OPEN",
                    path,
                    task.line,
                    f"{label} is complete but {task_label} is not checked",
                )
            )
        for sub_line, sub_checked in task.subtasks:
            if not sub_checked:
                diags.append(
                    error(
                        "ROADMAP-COMPLETE-OPEN",
                        path,
                        sub_line,
                        f"{label} is complete but a subtask of {task_label} is not checked",
                    )
                )
    if phase.status == "complete" and not phase.tasks:
        diags.append(
            error("ROADMAP-COMPLETE-OPEN", path, where, f"{label} is complete but lists no tasks")
        )
    return diags


def _check_tracker(path: str, lines: list[str], phases: list[Phase]) -> list[Diagnostic]:
    diags: list[Diagnostic] = []
    rows: dict[int, tuple[list[str], int]] = {}
    for number, cells, lineno in parse_tracker(lines):
        if number in rows:
            diags.append(error("ROADMAP-TRACKER", path, lineno, f"P{number} has two tracker rows"))
        rows[number] = (cells, lineno)
    known = {phase.number for phase in phases}
    for number, (_, lineno) in rows.items():
        if number not in known:
            diags.append(
                error("ROADMAP-TRACKER", path, lineno, f"tracker row P{number} has no phase")
            )
    for phase in phases:
        label = f"P{phase.number}"
        if phase.number not in rows:
            diags.append(error("ROADMAP-TRACKER", path, phase.line, f"{label} has no tracker row"))
            continue
        cells, lineno = rows[phase.number]
        if len(cells) < 4:
            diags.append(
                error(
                    "ROADMAP-TRACKER",
                    path,
                    lineno,
                    f"{label} row needs Phase, Parent issue, Branch, and Status cells",
                )
            )
            continue
        parent_cell, branch_cell, status_cell = cells[1], cells[2], cells[3]
        if parent_cell != (phase.parent or ""):
            diags.append(
                error(
                    "ROADMAP-TRACKER",
                    path,
                    lineno,
                    f"{label} parent issue '{parent_cell}' differs from its phase section",
                )
            )
        if branch_cell.strip("`") != (phase.branch or ""):
            diags.append(
                error(
                    "ROADMAP-TRACKER",
                    path,
                    lineno,
                    f"{label} branch '{branch_cell}' differs from its phase section",
                )
            )
        if status_cell != (phase.status or ""):
            diags.append(
                error(
                    "ROADMAP-TRACKER",
                    path,
                    lineno,
                    f"{label} status '{status_cell}' differs from its phase section",
                )
            )
    return diags


def check_roadmap(path: str, text: str) -> list[Diagnostic]:
    """Check the phase grammar, phase statuses, and tracker map of a roadmap."""
    lines = text.split("\n")
    phases = parse_roadmap(lines)
    if not phases:
        return [error("ROADMAP-NO-PHASES", path, 0, "no '## Phase <n>:' headings found")]
    diags: list[Diagnostic] = []
    previous = -1
    for phase in phases:
        if phase.number <= previous:
            diags.append(
                error(
                    "ROADMAP-PHASE-ORDER",
                    path,
                    phase.line,
                    f"P{phase.number} must be unique and come after P{previous}",
                )
            )
        previous = max(previous, phase.number)
        diags.extend(_check_phase(path, phase))
    diags.extend(_check_tracker(path, lines, phases))
    return diags


def check_changelog(path: str, text: str) -> list[Diagnostic]:
    """Check that changelog entries are dated ISO dates in ascending order."""
    diags: list[Diagnostic] = []
    previous: dt.date | None = None
    dated = 0
    for lineno, raw in enumerate(text.split("\n"), start=1):
        if not raw.startswith("## "):
            continue
        label = raw[3:].strip()
        try:
            day = dt.date.fromisoformat(label)
        except ValueError:
            diags.append(
                error("CHANGELOG-DATE", path, lineno, f"heading '{label}' is not a YYYY-MM-DD date")
            )
            continue
        dated += 1
        if previous is not None and day < previous:
            diags.append(
                error(
                    "CHANGELOG-ORDER",
                    path,
                    lineno,
                    f"{label} is older than the entry above it; newest entries go last",
                )
            )
        previous = day
    if dated == 0:
        diags.append(error("CHANGELOG-EMPTY", path, 0, "no dated '## YYYY-MM-DD' entries"))
    return diags


def check_required_files(root: Path) -> list[Diagnostic]:
    """Check that the required files exist, and warn about recommended ones."""
    diags: list[Diagnostic] = []
    for rel in REQUIRED_FILES:
        if not (root / rel).is_file():
            diags.append(error("FILE-MISSING", rel, 0, "required file is missing"))
    for rel in RECOMMENDED_FILES:
        if not (root / rel).is_file():
            diags.append(warning("FILE-RECOMMENDED", rel, 0, "recommended file is missing"))
    return diags


def check_markdown_links(root: Path) -> list[Diagnostic]:
    """Check that every local link in a Markdown file points at an existing file."""
    diags: list[Diagnostic] = []
    for path in iter_text_files(root):
        if path.suffix != ".md":
            continue
        rel = path.relative_to(root).as_posix()
        for lineno, line in enumerate(_read_lines(path), start=1):
            for match in LINK_RE.finditer(line):
                target = match.group(1)
                if not _is_local_target(target):
                    continue
                file_part = _strip_fragment(target)
                if file_part and not (path.parent / file_part).exists():
                    diags.append(
                        error(
                            "LINK-BROKEN", rel, lineno, f"link target '{file_part}' does not exist"
                        )
                    )
    return diags


def check_llms(root: Path) -> list[Diagnostic]:
    """Check that every link in docs/llms.txt names an existing docs page."""
    index = root / "docs" / "llms.txt"
    if not index.is_file():
        return []
    diags: list[Diagnostic] = []
    for lineno, line in enumerate(_read_lines(index), start=1):
        for match in LINK_RE.finditer(line):
            target = match.group(1)
            if not _is_local_target(target):
                continue
            file_part = _strip_fragment(target)
            if not file_part:
                continue
            if file_part.endswith(".html"):
                source = root / "docs" / (file_part[: -len(".html")] + ".rst")
            else:
                source = root / "docs" / file_part
            if not source.exists():
                diags.append(
                    error(
                        "LLMS-BROKEN",
                        "docs/llms.txt",
                        lineno,
                        f"'{file_part}' has no matching page under docs/",
                    )
                )
    return diags


def scan_text(rel: str, data: bytes) -> list[Diagnostic]:
    """Scan one file for control characters, byte-order marks, and unsafe strings."""
    diags: list[Diagnostic] = []
    if b"\r" in data:
        diags.append(error("CONTROL-CHAR", rel, 0, "carriage return found; use LF line endings"))
    text = data.decode("utf-8")
    for lineno, line in enumerate(text.split("\n"), start=1):
        if "\ufeff" in line:
            diags.append(error("BOM", rel, lineno, "byte-order mark (U+FEFF) found"))
        control = CONTROL_RE.search(line)
        if control is not None:
            code_point = ord(control.group())
            diags.append(
                error("CONTROL-CHAR", rel, lineno, f"control character U+{code_point:04X} found")
            )
        for pattern, label in PERSONAL_PATTERNS:
            if pattern.search(line):
                diags.append(
                    error(
                        "PATH-PERSONAL",
                        rel,
                        lineno,
                        f"{label}; use a placeholder or a relative path",
                    )
                )
                break
        for pattern, label in SECRET_PATTERNS:
            if pattern.search(line):
                diags.append(
                    error(
                        "SECRET-SHAPED",
                        rel,
                        lineno,
                        f"possible {label}; remove it, and rotate it if real",
                    )
                )
                break
    return diags


def scan_repository(root: Path) -> list[Diagnostic]:
    """Run the text checks on every tracked-looking file under root."""
    diags: list[Diagnostic] = []
    for path in iter_text_files(root):
        rel = path.relative_to(root).as_posix()
        diags.extend(scan_text(rel, path.read_bytes()))
    return diags


def check_files(paths: list[Path]) -> list[Diagnostic]:
    """Run only the text checks on the given files, such as issue body files."""
    diags: list[Diagnostic] = []
    for path in paths:
        name = str(path)
        if not path.is_file():
            diags.append(error("FILE-MISSING", name, 0, "file does not exist"))
            continue
        data = path.read_bytes()
        try:
            data.decode("utf-8")
        except UnicodeDecodeError:
            diags.append(error("ENCODING", name, 0, "file is not valid UTF-8"))
            continue
        diags.extend(scan_text(name, data))
    return diags


def run(root: Path) -> list[Diagnostic]:
    """Run every repository check against root and return all findings."""
    diags = check_required_files(root)
    roadmap = root / "ROADMAP.md"
    if roadmap.is_file():
        diags.extend(check_roadmap("ROADMAP.md", _read_text(roadmap)))
    changelog = root / "CHANGE_LOG.md"
    if changelog.is_file():
        diags.extend(check_changelog("CHANGE_LOG.md", _read_text(changelog)))
    diags.extend(check_markdown_links(root))
    diags.extend(check_llms(root))
    diags.extend(scan_repository(root))
    return diags


def main(argv: list[str] | None = None) -> int:
    """Command-line entry point. Returns the process exit status."""
    parser = argparse.ArgumentParser(description="Check the UBC-FRESH dev workflow surfaces.")
    parser.add_argument(
        "root",
        nargs="?",
        type=Path,
        default=DEFAULT_ROOT,
        help="repository root to check (default: the checkout that contains this script)",
    )
    parser.add_argument(
        "--files",
        nargs="+",
        type=Path,
        metavar="PATH",
        help="run only the text checks on these files, for example issue body files",
    )
    args = parser.parse_args(argv)
    if args.files:
        diags = check_files(args.files)
    else:
        root = args.root.resolve()
        if not root.is_dir():
            parser.error(f"not a directory: {root}")
        diags = run(root)
    for diag in diags:
        print(diag.render())
    errors = sum(1 for diag in diags if diag.severity == "error")
    print(f"{errors} error(s), {len(diags) - errors} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
