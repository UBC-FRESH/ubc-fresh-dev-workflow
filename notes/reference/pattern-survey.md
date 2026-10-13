# Pattern survey: public UBC-FRESH repositories

Date: 2026-10-13
Issues: #3
Scope: public repositories only. Private repositories were not quoted or summarized.

## Method

The agent contracts, roadmaps, changelogs, notes, docs layouts, and CI workflows of these public repositories were read:

- `freshforge`: a workflow-as-code core. Phases P0 to P18, each with a parent issue and a branch.
- `femic`: a large domain pipeline with a long agent contract, a roadmap, and planning notes.
- `ws3`: a wood supply simulator, with an agent capability design, an onboarding guide, and issue templates.
- `fhops`: an operations planner, with a notes tree that holds architecture decision records and reference notes, and a sub-issue workflow.
- `nemora`: distribution fitting, with a short agent contract and a notes directory.
- `modelwright`: spreadsheet-to-Python conversion, with a roadmap that has parent issues and a list of lifecycle deliverables.
- `agent-workbench` and `fresh-agent-core`: supervised multi-agent workflows and the capability pattern.

## What is common

- An agent contract at the repository root.
- A roadmap that is the plan of record, with phases, tasks, and checkboxes.
- A changelog that is an append-only narrative.
- A planning or notes directory with focused design notes.
- Parent issues for phases, child issues for tasks, and one feature branch per phase.
- A Sphinx docs site published to GitHub Pages, with warnings treated as errors.
- Verification commands that run ruff, pytest, the docs build, and a package build.

## What varies, and what this seed standardizes

| Topic | Variants seen | Seed choice |
| --- | --- | --- |
| Changelog name | `CHANGE_LOG.md`, `CHANGELOG.md` | `CHANGE_LOG.md` |
| Planning directory | `planning/`, `notes/` | `notes/`, with `adr/` and `reference/` |
| Phase branch | `feature/p<n>-<slug>`, `feature/phase<n>-<slug>` | `feature/p<n>-<slug>` |
| Child branch | `issue-<n>-<slug>` in one repository | Not required. Commit to the phase branch with task IDs. |
| Agent contract size | From 27 lines to more than 400 | A short root contract, with detail in `docs/reference/` |
| Work-kind field | Labels, or GitHub issue types | Labels `phase` and `task`; sub-issues for hierarchy |
| Status syntax | Free text, status lines, checkboxes | Status lines and checkboxes, parsed by the validator |

## Lessons from the survey

- **Control characters in issue bodies.** One published parent issue shows a branch name that lost its first letter and a stray tab inside a command. Both fit escape sequences inside hand-built strings. The seed requires body files, and the validator rejects control characters.
- **Placeholder parents.** One repository keeps bootstrap-created parent issues for future phases and marks them as inactive lanes. The seed mirrors future phases as real parent issues with full bodies, marked `planned`.
- **Contract sprawl.** The longest contract mixes general rules with domain runbooks. The seed keeps the root contract short and moves detail into reference pages.
- **Capability claims need oracles.** One repository's capability design records that fabricated APIs reached its docs, its tests, and its code before a validator existed. The seed carries "no oracle, no capability" into its agent docs.
- **Lifecycle deliverables.** One repository lists its expected phases from bootstrap to packaging. The seed turns that kind of list into a lifecycle map in `ROADMAP.md`.

## Deliberately left out

- Domain rules, such as runner selection, benchmark stop-lines, and data-semantics guardrails. Those belong to their projects.
- Private repository names, private data, and links to a knowledge base that requires lab login.
- Machine-specific setup instructions, including Windows-only bootstraps.
- Model names and vendor pricing. The seed treats models as configuration, to be checked against evidence.
