# ADR 0008: Phase close-out, with approval before execution

Status: accepted
Date: 2026-10-13
Issues: #1, #8
Refines: ADR 0004

## Context

ADR 0004 requires an explicit answer from the maintainer before an agent merges a pull request, closes a parent issue, or deletes a branch. The approval gates table and the workflow pages then went further, and said that agents never merge and that the maintainer merges and closes. The result left the end of every phase without an executor. The agent did the work and wrote the evidence, but the merge, the cleanup, and the launch of the next phase had no owner, and the maintainer was left to do the bookkeeping. The maintainer's job is to review and approve.

## Decision

- At the end of a phase, the agent queues the phase's pull request, and commits a close-out report to `notes/reports/`. The report holds the evidence, the workflow compliance record, the CI runs, the deviations, the recommended actions, and the next phase's plan.
- The maintainer approves the report, or asks for changes. That approval is the explicit answer that ADR 0004 requires.
- After approval, the agent executes the approved actions in the order the report gives: squash-merge the pull request, delete its branch, close the parent issue, apply any approved settings change, and launch the next phase.
- Settings changes, tags, releases, external accounts, and deletions beyond the approved branch are named in the report with their exact commands. Each one runs only after its own approval.
- A report does not ask open questions. Each open choice is a recommendation with a default and its reason.

## Consequences

- The maintainer reviews one document per phase. The agent carries out the execution and keeps the record.
- The evidence for every phase is in the repository, where a reviewer can audit it later.
- An approval covers only what the report names. Anything else goes back into a report.
- A report that names a head commit that has since moved is stale. It is refreshed before the next approval request.

## Alternatives considered

- The maintainer merges and closes each phase. Rejected: it makes the maintainer the operator, and the evidence for the phase is then assembled by whoever happens to merge.
- The agent merges as soon as CI is green. Rejected: CI verifies what it tests. It does not show that the phase is what the maintainer wanted, and ADR 0004 already rules this out.
