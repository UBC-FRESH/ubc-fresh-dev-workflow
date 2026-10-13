# AGENTS.md

This file is the working contract for coding agents in this repository.

This repository is the UBC-FRESH dev workflow: a seed, an onboarding kit, and a worked example of the workflow it describes. It is built with that workflow, so changes here follow the same rules the seed gives every project built from it.

Keep this file short. Each rule below either checks itself or points to the page that explains it.

## Session start

Before you change anything, read in this order:

1. This file.
2. [`ROADMAP.md`](ROADMAP.md): the active phase and its "Detailed Next Steps Notes".
3. The latest entries in [`CHANGE_LOG.md`](CHANGE_LOG.md).
4. The notes your task names, in [`notes/`](notes/README.md).
5. The docs pages that govern your task. Start with [`docs/agents/session-protocol.rst`](docs/agents/session-protocol.rst).

Cite the pages you relied on in your report.

## Repository state

- `README.md`: public overview and reading paths.
- `ROADMAP.md`: phases, tasks, and the issue tracker map.
- `CHANGE_LOG.md`: append-only narrative, newest entries last.
- `docs/`: the Sphinx site, which is the RTFM surface. Published to GitHub Pages from `main`.
- `notes/`: ADRs, reference notes, and focused plans.
- `templates/project/`: the seed rendered by `scripts/new_project.py`.
- `scripts/`: the validator (`check_workflow.py`) and the initializer (`new_project.py`).
- `tests/`: pytest suite, including a self-check of this repository.
- `.github/`: CI, the docs deploy workflow, and issue templates.

Do not claim a capability, a CI job, or a release that the roadmap has not recorded as complete.

## Working principles

- **Evidence over trust.** Treat a prose report as untrusted until you have checked the state it describes. Cite command output, diffs, commit hashes, and URLs.
- **One bounded move at a time.** Stop and report after each one. See [`docs/agents/bounded-moves.rst`](docs/agents/bounded-moves.rst).
- **No oracle, no capability.** A new agent-facing capability needs a validator that can fail. See [`docs/agents/oracles-and-evidence.rst`](docs/agents/oracles-and-evidence.rst).
- **Workflow as scaffold.** Create the parent issue, branch, and roadmap entry before the work, not after.
- **Structured handoff.** Issues, roadmap entries, notes, and the changelog carry the state. A new session should not need this chat.
- **Preserve uncertainty.** Say what you did not verify, and why.
- **Scope discipline.** Stay inside the active phase and task. Record adjacent ideas; do not start them.
- **Sanitized output.** Keep raw transcripts, credentials, private data, and personal paths out of tracked files.

## Planning workflow

- One phase is one GitHub parent issue and one feature branch, `feature/p<n>-<slug>`.
- One task is one child issue, linked to the parent as a sub-issue.
- A subtask is a checklist item inside the child issue body. Three levels at most.
- Record issue numbers beside phases and tasks once they exist.
- Keep `ROADMAP.md`, `CHANGE_LOG.md`, `notes/`, issue bodies, and PR descriptions in step.

Details: [workflow model](docs/reference/workflow-model.rst) and [GitHub mapping](docs/reference/github-mapping.rst).

## Approval gates

You may, within the active phase: create and commit to its branch, push that branch, open and update its issues and pull requests, and run local checks.

You must ask, and wait for an explicit answer, before you: activate a phase; merge a pull request; close a parent issue; create a tag or a release; change visibility, settings, or the template flag; create an external account, repository, or server; touch private data or credentials; or delete anything.

Details: [approval gates](docs/reference/approval-gates.rst).

## GitHub hygiene

- Audit read-only first: `gh issue list`, `gh issue view <n>`, `gh pr list`.
- Write issue bodies and comments to files and post them with `--body-file`. Never build them from escaped strings, which can inject control characters.
- Read back every comment or edit with `gh issue view` before you report it as posted.
- Post a progress comment when a task or phase milestone completes. Post a closeout comment before you close any issue.
- If GitHub is unavailable, record the failed command, its exit status, and the error text. Keep an issue-tree manifest in the repository until access returns. Do not describe the GitHub side as current while it is not.

Details: [issue standard](docs/reference/issue-standard.rst) and [git conventions](docs/reference/git-conventions.rst).

## Formatting

- Put section labels on their own lines, such as `Phase identifier: P0` and `Status: active`.
- Use real task-list syntax, one item per line. Never write an inline pseudo-checklist.
- Wrap branch names, paths, commands, and commit hashes in backticks.
- Start commit messages with the task ID, for example `P0.5 add initializer`.

## Verification

Run these before you report a change as done:

```bash
python -m ruff check .
python -m pytest
sphinx-build -b html docs _build/html -W
python scripts/check_workflow.py
```

When you change a docs page, rebuild with `-W`. When you change the roadmap or the changelog, run the validator. Record the commands and their results in the changelog entry for the milestone.

## Documentation rules

- Update the affected docs page in the same change set as the behavior it describes.
- When you add or rename a docs page, update its toctree and [`docs/llms.txt`](docs/llms.txt).
- Keep each rule in one place. Link to the reference page instead of copying it here.

## Public safety

- No private data, credentials, raw transcripts, unpublished documents, or machine-specific paths in tracked files.
- Use placeholders, repository-relative paths, or environment variables in examples.
- Run `python scripts/check_workflow.py` before each push. It rejects personal paths, control characters, byte-order marks, and secret-shaped strings.

## Notes and decisions

- Record a decision that will matter later as an ADR in `notes/adr/`. Never rewrite an accepted ADR; supersede it with a new one.
- Keep notes living: update them in the same change set as the work they describe.

## What does not belong here

Domain rules, project-specific runbooks, and model choices stay out of this file. Projects built from the seed keep their domain rules in their own `AGENTS.md` and reference pages. Model choice is configuration; see the dev server guide.
