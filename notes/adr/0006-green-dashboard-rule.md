# ADR 0006: The green dashboard rule, with no exceptions

Status: accepted
Date: 2026-10-13
Issues: #14

## Context

A repository decays one exception at a time. A failing check gets muted, a warning gets
postponed, a test gets skipped, and the signal that the team relies on stops meaning anything.
Coding agents make this worse, because they generate changes faster than a reviewer can notice
drift.

## Decision

- Every commit leaves the dashboard green. The dashboard runs every quality gate.
- Any change from green is investigated and fixed immediately. The rule has no exceptions.
- A gate changes only with a changelog entry that explains the change. Lowering a threshold, or
  removing a gate, needs an ADR.
- CI runs the same gates on every pull request, and a maintainer makes them required in branch
  protection.

## Consequences

- Work is slower in the short run, and the repository stays trustworthy in the long run.
- Agents stop to fix a failure before they start new work. The rule is written into the agent
  contract, and the dashboard prints an instruction when it is red.
- A failure that was not caused by the current change still belongs to the current change,
  because the commit is the only place where it can be fixed.

## Alternatives considered

- A documented list of allowed exceptions. Rejected: exceptions accumulate, and the list becomes
  the new dashboard.
- Running the gates only in CI. Rejected: a commit that fails in CI has already left the
  developer's working context.
