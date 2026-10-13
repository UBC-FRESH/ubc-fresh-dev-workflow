# Notes

Notes are the persistent, agent-friendly context for this project. They hold what a future reader, human or agent, needs and cannot get from the code, the issues, or the changelog alone.

## What goes where

| Kind | Location | Rule |
| --- | --- | --- |
| Decisions | `notes/adr/NNNN-slug.md` | One decision per file. Never rewrite an accepted ADR; supersede it with a new one. |
| Reference notes | `notes/reference/*.md` | Facts with provenance: where they came from, how they were read, and what is uncertain. |
| Focused plans | `notes/*.md` | Detail too long for `ROADMAP.md`. Linked from the roadmap task. Kept current while the task is active. |
| Phase close-out reports | `notes/reports/*.md` | One report per phase, written at close-out from the seed's `phase-closeout-template.md`. It is the evidence for the maintainer's approval. Later facts go in the changelog. |

## Rules

- Notes are living documents. Update them in the same change set as the work they describe.
- Record provenance for every external fact: the source, the date checked, and how it was read.
- Keep private material out. Raw transcripts, credentials, unpublished documents, and personal paths stay outside the repository.
- Prefer a short ADR that links to a plan over a long ADR that restates one.

## Index

- [ADR 0001: three-level phase, task, and subtask workflow](adr/0001-three-level-phase-task-subtask-workflow.md)
- [ADR 0002: docs as the source of truth](adr/0002-docs-as-source-of-truth.md)
- [ADR 0003: one container per project on a lab dev server](adr/0003-container-per-project-dev-server.md)
- [ADR 0004: human approval gates](adr/0004-human-approval-gates.md)
- [ADR 0005: strict typing and numpy docstrings](adr/0005-strict-typing-and-docstrings.md)
- [ADR 0006: the green dashboard rule](adr/0006-green-dashboard-rule.md)
- [ADR 0007: embedded agent capabilities, validated and advisory](adr/0007-embedded-capabilities-pattern.md)
- [ADR 0008: phase close-out, with approval before execution](adr/0008-phase-closeout-and-execution.md)
- [Pattern survey](reference/pattern-survey.md): a sanitized survey of public UBC-FRESH repositories
- [P0 close-out report](reports/p0-closeout.md): the evidence and the approval request for Phase 0
- [Dogfood log, Phase 1](reference/dogfood-log.md): the friction found by the first dogfood runs, with a disposition for each entry
