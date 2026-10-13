# Notes

Notes are the persistent, agent-friendly context for this project. They hold what a future reader, human or agent, needs and cannot get from the code, the issues, or the changelog alone.

## What goes where

| Kind | Location | Rule |
| --- | --- | --- |
| Decisions | `notes/adr/NNNN-slug.md` | One decision per file. Never rewrite an accepted ADR; supersede it with a new one. |
| Reference notes | `notes/reference/*.md` | Facts with provenance: where they came from, how they were read, and what is uncertain. |
| Focused plans | `notes/*.md` | Detail too long for `ROADMAP.md`. Linked from the roadmap task. Kept current while the task is active. |

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
- [Pattern survey](reference/pattern-survey.md): a sanitized survey of public UBC-FRESH repositories
