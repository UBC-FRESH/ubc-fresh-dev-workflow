# UBC-FRESH Dev Workflow

[![CI](https://github.com/UBC-FRESH/ubc-fresh-dev-workflow/actions/workflows/ci.yml/badge.svg)](https://github.com/UBC-FRESH/ubc-fresh-dev-workflow/actions/workflows/ci.yml)

A seed and onboarding kit for agent-assisted science and engineering projects.

It captures how the UBC FRESH Lab plans, builds, reviews, and releases software with coding agents: a phase, task, and subtask roadmap mirrored in GitHub issues; agent operating contracts; agent-friendly documentation; and a container-per-project dev server recipe.

This repository is built with the pattern it documents. Its roadmap, issues, changelog, notes, and docs show the workflow running on itself, so you can see what a project looks like after it has been through the loop.

## What this is

- **A seed.** Start a new project from it. `scripts/new_project.py` renders the planning files, the docs skeleton, the workflow validator, and CI into a new directory.
- **An onboarding kit.** New team members, collaborators, and coding agents read the docs in a fixed order and learn the workflow without a live tutor.
- **A worked example.** Phase P0 of this repository shows the full loop: a parent issue, child issues, a feature branch, a changelog entry, the validator, and a pull request for review.
- **A dev server recipe.** `docs/guides/dev-server/` describes a FRESH-style server with one container per project, a browser IDE, and an agent CLI. It is a recipe, not a requirement.

## The pattern in one picture

```text
ROADMAP.md             plan of record: phases P<n>, tasks P<n>.<m>
|
+-- GitHub parent issue, one per phase     branch feature/p<n>-<slug>
|     +-- child issues, one per task       sub-issues of the parent
|           +-- subtasks: checklist items in the child issue body
|
+-- CHANGE_LOG.md    dated narrative, newest last
+-- notes/           decisions (ADRs), reference notes, focused plans
+-- docs/            the RTFM surface, published to GitHub Pages
```

## Where to start

| If you are | Start with |
| --- | --- |
| a new team member | [Onboarding](docs/guides/onboarding.rst) |
| starting a new project | [Starting a new project](docs/guides/first-project.rst) |
| setting up a server | [FRESH-style dev server](docs/guides/dev-server/index.rst) |
| a coding agent | [`AGENTS.md`](AGENTS.md), then the [session protocol](docs/agents/session-protocol.rst) |
| a collaborator who wants the pattern | [`ROADMAP.md`](ROADMAP.md), then the [workflow model](docs/reference/workflow-model.rst) |

## Quick start

Check out the repository and run the local checks:

```bash
git clone https://github.com/UBC-FRESH/ubc-fresh-dev-workflow.git
cd ubc-fresh-dev-workflow
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
pre-commit install
python scripts/dashboard.py
```

Start a new project from the seed:

```bash
python scripts/new_project.py --name "My Project" --slug my-project --dest ../my-project
```

The initializer validates what it produced. Then follow [Starting a new project](docs/guides/first-project.rst) to create the GitHub repository and its Phase 0 parent issue.

## The green dashboard

Every commit leaves the dashboard green. `python scripts/dashboard.py` runs the lint, format, type,
test, validator, docs, and seed gates, and exits non-zero when any of them is red. Any change from
green is investigated and fixed immediately. See [the green dashboard](docs/agents/green-dashboard.rst)
and [quality gates](docs/reference/quality-gates.rst).

## Status

Phase P0, the bootstrap scaffold, is complete on the branch `feature/p0-bootstrap-scaffold`. It was
reopened to add the quality gates, the typed API reference, and the embedded capability pattern. Its
pull request, #17, is queued for approval with a close-out report, and it has not merged. The live
status of every phase is in [`ROADMAP.md`](ROADMAP.md) and in the GitHub issues.

## Repository map

| Path | Purpose |
| --- | --- |
| `AGENTS.md` | Operating contract for coding agents working in this repository |
| `ROADMAP.md` | Plan of record and issue tracker map |
| `CHANGE_LOG.md` | Dated narrative of changes |
| `docs/` | Sphinx site: guides, reference contracts, and agent protocols |
| `notes/` | ADRs, reference notes, and the pattern survey |
| `templates/project/` | The seed that `scripts/new_project.py` renders |
| `scripts/` | `check_workflow.py` (validator) and `new_project.py` (initializer) |
| `tests/` | pytest suite, including a self-check of this repository |
| `.github/` | CI, the docs deploy workflow, and issue templates |

## Lineage

The pattern comes from FRESH lab software projects, including freshforge, femic, ws3, fhops, nemora, and modelwright, and from the lab's agent tooling. [`notes/reference/pattern-survey.md`](notes/reference/pattern-survey.md) records what was borrowed, what was standardized, and what was deliberately left out.

## Public by design

This repository is public. Keep private data, credentials, raw transcripts, and machine-specific paths out of it. The validator checks the mechanical parts of that rule. The rest is on you. See [`CONTRIBUTING.md`](CONTRIBUTING.md).

## License and citation

MIT. Copyright (c) 2026 UBC FRESH Lab. See [`LICENSE`](LICENSE). Cite the repository with [`CITATION.cff`](CITATION.cff).

## Community

Contributions and questions are welcome through issues. Please follow the [code of conduct](CODE_OF_CONDUCT.md).
