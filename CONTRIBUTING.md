# Contributing

This is a public repository from the UBC FRESH Lab. Contributions should keep it public-safe,
reproducible, and aligned with the active roadmap phase.

## Development setup

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
pre-commit install
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
pre-commit install
```

## The green dashboard

The dashboard is the signal that every commit must keep green:

```bash
python scripts/dashboard.py
```

It runs lint, format, strict types, the test suite with its coverage gate, the workflow validator,
the docs build with warnings as errors, and the seed generator. The pre-commit hooks run the same
checks on each commit. Any change from green is investigated and fixed before you continue. There
are no exceptions. See [the green dashboard](docs/agents/green-dashboard.rst).

## Workflow

- Read [`AGENTS.md`](AGENTS.md) and [`ROADMAP.md`](ROADMAP.md) before non-trivial work.
- Work on the branch for the active phase, named `feature/p<n>-<slug>`.
- Start every commit message with the task ID, for example `P0.7 add the green dashboard`.
- Write every function with full type annotations and a numpy-style docstring, and add unit tests for
  it in the same change set.
- Keep `ROADMAP.md`, `CHANGE_LOG.md`, `notes/`, and the matching GitHub issues in step with the work.
- Change the docs in the same change set as the behavior they describe.
- Open pull requests against `main` with `Part of #<parent issue>` in the body. A maintainer
  merges human-authored pull requests, and CI must be green first. An agent-run phase closes out
  as described in `docs/reference/phase-closeout.rst`.

## Control characters and public safety

- Write GitHub issue and pull request bodies to files and post them with `--body-file`. Do not build
  them from escaped strings. Sequences such as `\f` and `\t` become control characters, which can
  silently corrupt a branch name or a command.
- Use LF line endings. Carriage returns are rejected.
- Run `python scripts/check_workflow.py` before you push. It rejects control characters,
  byte-order marks, personal paths, and secret-shaped strings. To check one body file, run
  `python scripts/check_workflow.py --files path/to/body.md`.
- Do not commit private data, raw transcripts, credentials, generated local outputs, or
  machine-specific paths.

## Reporting problems

Open an issue. Describe what you ran, what you expected, what happened, and the relevant output. Do
not paste credentials or private data.
