#!/usr/bin/env python3
"""Render the UBC-FRESH project seed into a new directory.

The seed lives in ``templates/project/``. Files whose names end in ``.tmpl`` are
rendered with the project tokens and written without the suffix. Every other file
is copied unchanged. The validator is copied into the new project so the project
can check its own planning surfaces, and the validator runs on the result before
the script finishes.

Usage::

    python scripts/new_project.py --name "My Project" --slug my-project --dest ../my-project

This script does not contact GitHub. Creating a repository, a parent issue, or a
branch needs maintainer approval, so the script prints the commands instead.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEED_DIR = ROOT / "templates" / "project"
VALIDATOR = ROOT / "scripts" / "check_workflow.py"
TEMPLATE_SUFFIX = ".tmpl"
NAME_RE = re.compile(r'^[^"\\\x00-\x1f]{2,80}$')
SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,62}$")
OWNER_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9-]{0,38}$")
PLACEHOLDER_RE = re.compile(r"\{\{[A-Z_]+\}\}")
DEFAULT_PURPOSE = "Describe the purpose of this project in two sentences before Phase 0 starts."
NEXT_STEPS = """
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
    """Derive a repository slug from a project name."""
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")[:63]


def validate_inputs(name: str, slug: str, owner: str) -> None:
    """Reject values that would break rendered files or GitHub names."""
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
    """Return the token-to-value map used to render the seed."""
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
    """Replace every token in text with its value."""
    for token, value in tokens.items():
        text = text.replace(token, value)
    return text


def plan_seed(seed_dir: Path) -> list[tuple[Path, Path, bool]]:
    """Return (source, destination relative path, is_template) for every seed file."""
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
    plan.append((VALIDATOR, Path("scripts") / VALIDATOR.name, False))
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
    """Render the seed into dest and return the written paths."""
    validate_inputs(name, slug, owner)
    if dest.exists() and any(dest.iterdir()) and not force:
        raise FileExistsError(f"{dest} is not empty; choose another --dest or pass --force")
    plan = plan_seed(SEED_DIR)
    targets = [dest / target for _, target, _ in plan]
    if not force:
        existing = [target for target in targets if target.exists()]
        if existing:
            raise FileExistsError(f"{existing[0]} already exists; pass --force to overwrite")
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
    """Run the validator that was copied into the new project."""
    return subprocess.run(
        [sys.executable, str(dest / "scripts" / VALIDATOR.name), str(dest)],
        capture_output=True,
        text=True,
        check=False,
    )


def main(argv: list[str] | None = None) -> int:
    """Command-line entry point. Returns the process exit status."""
    parser = argparse.ArgumentParser(description="Render the UBC-FRESH project seed.")
    parser.add_argument("--name", required=True, help="human-readable project name")
    parser.add_argument("--slug", help="repository slug (default: derived from --name)")
    parser.add_argument("--dest", required=True, type=Path, help="directory to create or fill")
    parser.add_argument("--owner", default="UBC-FRESH", help="GitHub owner for the next steps")
    parser.add_argument("--purpose", default=DEFAULT_PURPOSE, help="one or two sentences")
    parser.add_argument("--force", action="store_true", help="overwrite existing files")
    args = parser.parse_args(argv)
    slug = args.slug or slugify(args.name)
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
