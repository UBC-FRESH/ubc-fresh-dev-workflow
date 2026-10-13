#!/usr/bin/env python3
"""Render the UBC-FRESH project seed into a new directory.

The seed lives in ``templates/project/``. Files whose names end in ``.tmpl`` are
rendered with the project tokens and written without the suffix. Every other file is
copied unchanged. The validator is copied into the new project, so the project can check
its own planning surfaces, and the validator runs on the result before the script ends.

Command-line usage::

    python scripts/new_project.py --name "My Project" --slug my-project --dest ../my-project

This script does not contact GitHub. Creating a repository, a parent issue, or a branch
needs maintainer approval, so the script prints the commands instead.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT: Path = Path(__file__).resolve().parent.parent
SEED_DIR: Path = ROOT / "templates" / "project"
VALIDATOR: Path = ROOT / "scripts" / "check_workflow.py"
TEMPLATE_SUFFIX: str = ".tmpl"
NAME_RE: re.Pattern[str] = re.compile(r'^[^"\\\x00-\x1f]{2,80}$')
SLUG_RE: re.Pattern[str] = re.compile(r"^[a-z0-9][a-z0-9-]{1,62}$")
OWNER_RE: re.Pattern[str] = re.compile(r"^[A-Za-z0-9][A-Za-z0-9-]{0,38}$")
PLACEHOLDER_RE: re.Pattern[str] = re.compile(r"\{\{[A-Z_]+\}\}")
DEFAULT_PURPOSE: str = (
    "Describe the purpose of this project in two sentences before Phase 0 starts."
)
SHARED_FRAMEWORK_FILES: tuple[str, ...] = (
    "scripts/check_workflow.py",
    "scripts/dashboard.py",
    "tests/conftest.py",
    "tests/test_check_workflow.py",
    "tests/test_cli.py",
    "tests/test_dashboard.py",
    "tests/test_properties.py",
    "pyproject.toml",
    "requirements-dev.txt",
    ".pre-commit-config.yaml",
)
NEXT_STEPS: str = """
Next steps. The GitHub steps need maintainer approval first.
  cd {dest}
  git init -b main
  git add .
  git commit -m "Initial commit: project seed"
  gh repo create {owner}/{slug} --private --source=. --remote=origin --push
  Create the Phase 0 parent issue from .github/ISSUE_TEMPLATE/phase.md.
  Then set its number and the status 'active' in ROADMAP.md.
  docs/guides/first-project.rst describes the rest of the flow.
"""


def slugify(name: str) -> str:
    """Derive a repository slug from a project name.

    Parameters
    ----------
    name : str
        Human-readable project name.

    Returns
    -------
    str
        Lowercase letters, digits, and hyphens, with no leading or trailing hyphen, and at
        most 63 characters long.
    """
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")[:63]


def validate_inputs(name: str, slug: str, owner: str) -> None:
    """Reject values that would break rendered files or GitHub names.

    Parameters
    ----------
    name : str
        Human-readable project name. It is written into Python and reStructuredText.
    slug : str
        Repository slug. It becomes the repository name.
    owner : str
        GitHub owner name. It appears in the next-step commands and the Sphinx metadata.

    Raises
    ------
    ValueError
        When any value fails its pattern.
    """
    if not NAME_RE.match(name):
        raise ValueError(
            "project name must be 2 to 80 characters, without quotes, backslashes, "
            "or control characters"
        )
    if not SLUG_RE.match(slug):
        raise ValueError(
            f"slug '{slug}' must be 2 to 63 lowercase letters, digits, or hyphens, "
            "starting with a letter or digit"
        )
    if not OWNER_RE.match(owner):
        raise ValueError(f"owner '{owner}' is not a valid GitHub owner name")


def build_tokens(name: str, slug: str, owner: str, purpose: str, today: str) -> dict[str, str]:
    """Build the token-to-value map that renders the seed.

    Parameters
    ----------
    name : str
        Project name, which fills the ``{{PROJECT_NAME}}`` token.
    slug : str
        Repository slug, which fills the ``{{PROJECT_SLUG}}`` token.
    owner : str
        GitHub owner, which fills the ``{{OWNER}}`` token.
    purpose : str
        One or two sentences of purpose, which fill the ``{{PROJECT_PURPOSE}}`` token.
    today : str
        ISO date of the render, which fills the ``{{TODAY}}`` token. The first four
        characters also fill the ``{{YEAR}}`` token.

    Returns
    -------
    dict of str to str
        Each placeholder token mapped to its value. ``{{TITLE_RULE}}`` is an underline of
        ``=`` characters as long as the project name.
    """
    return {
        "{{PROJECT_NAME}}": name,
        "{{PROJECT_SLUG}}": slug,
        "{{OWNER}}": owner,
        "{{PROJECT_PURPOSE}}": purpose,
        "{{TITLE_RULE}}": "=" * len(name),
        "{{YEAR}}": today[:4],
        "{{TODAY}}": today,
    }


def render(text: str, tokens: dict[str, str]) -> str:
    """Replace every token in a text with its value.

    Parameters
    ----------
    text : str
        Template text that may contain tokens.
    tokens : dict of str to str
        Token-to-value map from :func:`build_tokens`.

    Returns
    -------
    str
        The text with every known token replaced. Unknown tokens are left in place, and
        :func:`create_project` rejects them.
    """
    for token, value in tokens.items():
        text = text.replace(token, value)
    return text


def plan_seed(seed_dir: Path) -> list[tuple[Path, Path, bool]]:
    """List every file that a new project receives, with its source and destination.

    Parameters
    ----------
    seed_dir : Path
        Directory that holds the seed templates.

    Returns
    -------
    list of tuple of (Path, Path, bool)
        For each output file: the source path, the destination path relative to the new
        project, and whether the source is a template that needs rendering. The shared
        framework files, such as the validator and the dashboard, are copied from this
        repository.

    Raises
    ------
    ValueError
        When two sources would write the same destination.
    """
    plan: list[tuple[Path, Path, bool]] = []
    for source in sorted(seed_dir.rglob("*")):
        if not source.is_file():
            continue
        relative = source.relative_to(seed_dir)
        if relative.name.endswith(TEMPLATE_SUFFIX):
            target = relative.with_name(relative.name[: -len(TEMPLATE_SUFFIX)])
            plan.append((source, target, True))
        else:
            plan.append((source, relative, False))
    for rel in SHARED_FRAMEWORK_FILES:
        plan.append((ROOT / rel, Path(rel), False))
    targets = [target for _, target, _ in plan]
    duplicates = sorted({str(t) for t in targets if targets.count(t) > 1})
    if duplicates:
        raise ValueError(f"seed writes the same destination twice: {', '.join(duplicates)}")
    return plan


def create_project(
    *,
    name: str,
    slug: str,
    dest: Path,
    owner: str,
    purpose: str,
    today: str,
    force: bool,
) -> list[Path]:
    """Render the seed into a destination directory.

    Parameters
    ----------
    name : str
        Human-readable project name.
    slug : str
        Repository slug.
    dest : Path
        Directory to create or fill.
    owner : str
        GitHub owner name.
    purpose : str
        One or two sentences of purpose.
    today : str
        ISO date of the render.
    force : bool
        When ``True``, existing files at the destination are overwritten.

    Returns
    -------
    list of Path
        Every file that was written.

    Raises
    ------
    ValueError
        When an input fails validation.
    FileExistsError
        When the destination is not empty, or a file would be overwritten without ``force``.
    RuntimeError
        When a placeholder survives rendering.
    """
    validate_inputs(name, slug, owner)
    if dest.exists() and any(dest.iterdir()) and not force:
        raise FileExistsError(f"{dest} is not empty; choose another --dest or pass --force")
    plan = plan_seed(SEED_DIR)
    targets = [dest / target for _, target, _ in plan]
    tokens = build_tokens(name, slug, owner, purpose, today)
    written: list[Path] = []
    for (source, relative, is_template), target in zip(plan, targets, strict=True):
        target.parent.mkdir(parents=True, exist_ok=True)
        if is_template:
            rendered = render(source.read_text(encoding="utf-8"), tokens)
            if PLACEHOLDER_RE.search(rendered):
                raise RuntimeError(f"a placeholder was left unrendered in {relative}")
            target.write_text(rendered, encoding="utf-8")
        else:
            shutil.copy2(source, target)
        written.append(target)
    return written


def run_validator(dest: Path) -> subprocess.CompletedProcess[str]:
    """Run the validator that was copied into a new project.

    Parameters
    ----------
    dest : Path
        Root of the new project.

    Returns
    -------
    subprocess.CompletedProcess of str
        The finished process, with its captured standard output and standard error.
    """
    return subprocess.run(
        [sys.executable, str(dest / "scripts" / VALIDATOR.name), str(dest)],
        capture_output=True,
        text=True,
        check=False,
    )


def main(argv: list[str] | None = None) -> int:
    """Run the initializer from the command line.

    Parameters
    ----------
    argv : list of str or None, optional
        Arguments to parse. ``None`` reads ``sys.argv``.

    Returns
    -------
    int
        ``0`` on success, ``1`` when the generated project fails validation, and ``2`` when
        the inputs are rejected.
    """
    parser = argparse.ArgumentParser(description="Render the UBC-FRESH project seed.")
    parser.add_argument("--name", required=True, help="human-readable project name")
    parser.add_argument("--slug", help="repository slug (default: derived from --name)")
    parser.add_argument("--dest", required=True, type=Path, help="directory to create or fill")
    parser.add_argument("--owner", default="UBC-FRESH", help="GitHub owner for the next steps")
    parser.add_argument("--purpose", default=DEFAULT_PURPOSE, help="one or two sentences")
    parser.add_argument("--force", action="store_true", help="overwrite existing files")
    args = parser.parse_args(argv)
    slug: str = args.slug or slugify(args.name)
    try:
        written = create_project(
            name=args.name,
            slug=slug,
            dest=args.dest,
            owner=args.owner,
            purpose=args.purpose,
            today=dt.date.today().isoformat(),
            force=args.force,
        )
    except (ValueError, FileExistsError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(f"Rendered {len(written)} files into {args.dest}")
    result = run_validator(args.dest)
    print(result.stdout, end="")
    if result.returncode != 0:
        print(result.stderr, end="", file=sys.stderr)
        print("error: the generated project failed validation", file=sys.stderr)
        return 1
    print(NEXT_STEPS.format(dest=args.dest, owner=args.owner, slug=slug))
    return 0


if __name__ == "__main__":
    sys.exit(main())
