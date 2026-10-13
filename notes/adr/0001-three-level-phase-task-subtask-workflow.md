# ADR 0001: Three-level phase, task, and subtask workflow

Status: accepted
Date: 2026-10-13
Issues: #1, #3

## Context

Agent-assisted projects drift when the plan lives in chat, in ad hoc TODO lists, or in a tracker with no link to the repository. A plan written as prose cannot be checked by a tool. Agents are told to stay in scope, but the scope is not something they can see.

## Decision

Plans use three levels:

- **Phase, `P<n>`.** A coherent deliverable with a goal and exit criteria. One phase maps to one GitHub parent issue and one feature branch.
- **Task, `P<n>.<m>`.** One reviewable unit of work inside a phase. One task maps to one child issue, linked as a sub-issue of the parent.
- **Subtask.** A checklist item inside the child issue body. A subtask becomes a fourth-level issue only if it needs its own review, which is rare.

`ROADMAP.md` is the plan of record. Its grammar is checked by `scripts/check_workflow.py`.

## Consequences

- Plans are visible to tools, reviewers, and new people. The validator rejects plans that drift from their GitHub mirrors.
- Each phase needs a parent issue, each task a child issue, and both need updates when their status changes. The seed scaffolds this, and the validator catches the rest.
- Three levels are the limit. A need for a fourth level is a signal to split the phase.

## Alternatives considered

- A flat task list in `ROADMAP.md` with no issues. Rejected: no reviewable artifacts, and no link from work to status.
- Milestones only. Rejected: milestones group issues, but they do not express the phase-to-branch rule or the task grammar.
- GitHub Projects only. Rejected for now: the plan must be readable inside the repository, by agents and by people who never open the web interface.
