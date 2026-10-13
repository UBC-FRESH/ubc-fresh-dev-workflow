# AGENTS.md

This file is the working contract for coding agents in this repository.

This repository is the UBC-FRESH dev workflow: a seed, an onboarding kit, and a worked
example of the workflow it describes. It is built with that workflow, so changes here follow
the same rules that the seed gives every project built from it.

Keep this file short. Each rule below either checks itself or points to the page that
explains it.

## Session start

Before you change anything, read in this order:

1. This file.
2. [`ROADMAP.md`](ROADMAP.md): the active phase and its "Detailed Next Steps Notes".
3. The latest entries in [`CHANGE_LOG.md`](CHANGE_LOG.md).
4. The notes your task names, in [`notes/`](notes/README.md).
5. The docs pages that govern your task. Start with
   [`docs/agents/session-protocol.rst`](docs/agents/session-protocol.rst).

Cite the pages you relied on in your report.

## Repository state

- `README.md`: public overview and reading paths.
- `ROADMAP.md`: phases, tasks, and the issue tracker map.
- `CHANGE_LOG.md`: append-only narrative, newest entries last.
- `docs/`: the Sphinx site, which is the RTFM surface. Published to GitHub Pages from `main`.
- `notes/`: ADRs, reference notes, and focused plans.
- `templates/project/`: the seed rendered by `scripts/new_project.py`.
- `scripts/`: the validator, the dashboard, and the initializer.
- `tests/`: the test suite, in the layers that [testing policy](docs/reference/testing-policy.rst)
  describes.
- `.github/`: CI, the docs deploy workflow, and issue templates.

Do not claim a capability, a CI job, or a release that the roadmap has not recorded as complete.

## Working principles

- **Evidence over trust.** Treat a prose report as untrusted until you have checked the state it
  describes. Cite command output, diffs, commit hashes, and URLs.
- **One bounded move at a time.** Stop and report after each one. See
  [`docs/agents/bounded-moves.rst`](docs/agents/bounded-moves.rst).
- **No oracle, no capability.** A new agent-facing capability needs a validator that can fail. See
  [`docs/agents/oracles-and-evidence.rst`](docs/agents/oracles-and-evidence.rst).
- **Workflow as scaffold.** Create the parent issue, branch, and roadmap entry before the work.
- **Structured handoff.** Issues, roadmap entries, notes, and the changelog carry the state. A new
  session should not need this conversation.
- **Preserve uncertainty.** Say what you did not verify, and why.
- **Scope discipline.** Stay inside the active phase and task. Record adjacent ideas; do not start them.
- **Sanitized output.** Keep raw transcripts, credentials, private data, and personal paths out of
  tracked files.

## The green dashboard rule

The dashboard in `scripts/dashboard.py` is the single signal that the repository is healthy. It
runs every quality gate: lint, format, strict types, tests with the coverage gate, the workflow
validator, the docs build with warnings as errors, and the seed generator.

- Every commit leaves the dashboard green. Run `python scripts/dashboard.py`, or let the pre-commit
  hooks run, before each commit.
- Any change from green is investigated and fixed immediately. There are no exceptions. Do not move
  on to the next task, and do not plan to fix it later.
- A failure you did not cause is still yours to fix, or to report with evidence before you continue.
- Do not weaken a gate to make it pass. A gate changes only with a changelog entry that explains why.
- Record the dashboard result in the changelog entry for each task that you close.

Details: [the green dashboard](docs/agents/green-dashboard.rst) and
[quality gates](docs/reference/quality-gates.rst).

## Typing and docstrings

- Every function, method, and test has complete type annotations. `mypy --strict` must pass on
  `scripts/`, `tests/`, and `docs/conf.py`.
- Every public function in `scripts/` has a numpy-style docstring. Its parameters and return value
  match its annotations.
- Do not use `Any`, `# type: ignore`, or `cast` without a comment that says why. A suppression names
  its error code.

Details: [typing and docstrings](docs/reference/typing-and-docstrings.rst).

## Testing policy

- Every function you write or change gets unit tests in the same change set. Tests must be able to
  fail, and each one asserts a specific behavior.
- Keep the layers: unit tests for each function, contract tests for public interfaces, integration
  tests that run the command-line tools, property tests for invariants, and the seed self-check.
- The coverage gate is 90 percent branch coverage of `scripts/`. Aim near 100 percent. Do not chase
  the number with tests that assert nothing.

Details: [testing policy](docs/reference/testing-policy.rst).

## CI and merges

- CI runs every gate on every pull request, and on every push to `main`.
- No pull request merges while CI is red. A maintainer makes the CI jobs required in branch
  protection.
- The agent does not merge. The maintainer does.

## Planning workflow

- One phase is one GitHub parent issue and one feature branch, `feature/p<n>-<slug>`.
- One task is one child issue, linked to the parent as a sub-issue.
- A subtask is a checklist item in the child issue body. Three levels at most.
- Record issue numbers beside phases and tasks once they exist.
- Keep `ROADMAP.md`, `CHANGE_LOG.md`, `notes/`, issue bodies, and PR descriptions in step.

Details: [workflow model](docs/reference/workflow-model.rst) and
[GitHub mapping](docs/reference/github-mapping.rst).

## Approval gates

You may, within the active phase: create and commit to its branch, push that branch, open and update
its issues and pull requests, and run local checks.

You must ask, and wait for an explicit answer, before you: activate a phase; merge a pull request;
close a parent issue; create a tag or a release; change visibility, settings, or branch protection;
create an external account, repository, or server; touch private data or credentials; or delete
anything.

Details: [approval gates](docs/reference/approval-gates.rst).

## GitHub hygiene

- Audit read-only first: `gh issue list`, `gh issue view <n>`, `gh pr list`.
- Write issue bodies and comments to files and post them with `--body-file`. Never build them from
  escaped strings, which can inject control characters.
- Read back every comment or edit with `gh issue view` before you report it as posted.
- Post a progress comment when a task or phase milestone completes. Post a closeout comment before you
  close any issue.
- If GitHub is unavailable, record the failed command, its exit status, and the error text. Keep an
  issue-tree manifest in the repository until access returns. Do not describe the GitHub side as
  current while it is not.

Details: [issue standard](docs/reference/issue-standard.rst) and
[git conventions](docs/reference/git-conventions.rst).

## Formatting

- Put section labels on their own lines, such as `Phase identifier: P0` and `Status: active`.
- Use real task-list syntax, one item per line. Never write an inline pseudo-checklist.
- Wrap branch names, paths, commands, and commit hashes in backticks.
- Start commit messages with the task ID, for example `P0.7 add the green dashboard`.

## Verification

Before you report a change as done, run the dashboard:

```bash
python scripts/dashboard.py
```

It runs `python -m ruff check .`, `python -m ruff format --check .`, `python -m mypy`,
`python -m pytest`, `python scripts/check_workflow.py`, and `sphinx-build -b html docs _build/html -W`,
and it generates a project from the seed and runs that project's dashboard. Record the result in the
changelog entry for the milestone.

## Documentation rules

- Update the affected docs page in the same change set as the behavior it describes.
- When you add or rename a docs page, update its toctree and [`docs/llms.txt`](docs/llms.txt).
- Keep each rule in one place. Link to the reference page instead of copying it here.

## Public safety

- No private data, credentials, raw transcripts, unpublished documents, or machine-specific paths in
  tracked files.
- Use placeholders, repository-relative paths, or environment variables in examples.
- Run `python scripts/check_workflow.py` before each push. It rejects personal paths, control
  characters, byte-order marks, and secret-shaped strings.

## Notes and decisions

- Record a decision that will matter later as an ADR in `notes/adr/`. Never rewrite an accepted ADR;
  supersede it with a new one.
- Keep notes living: update them in the same change set as the work they describe.

## What does not belong here

Domain rules, project-specific runbooks, and model choices stay out of this file. Projects built from
the seed keep their domain rules in their own `AGENTS.md` and reference pages. Model choice is
configuration; see the dev server guide.
