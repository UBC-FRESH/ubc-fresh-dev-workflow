# ADR 0004: Human approval gates

Status: accepted
Date: 2026-10-13
Issues: #2, #8

## Context

Agents run many commands quickly. Speed without review turns an agent's mistakes into shared state: public issues, merged code, and released artifacts. Several lab repositories already say so in their own contracts.

## Decision

Within an active phase, agents may:

- create branches, commit, and push to the phase branch;
- open and update issues, comments, and pull requests for the active phase;
- run local checks, builds, and validators.

Agents must ask first, and wait for an explicit answer, before they:

- activate a phase, or start a second active phase;
- merge a pull request, close a parent issue, or delete a branch;
- create a tag, a GitHub release, or a package publication;
- change repository visibility, settings, or the template flag;
- create an external account, repository, or server;
- touch private data, credentials, or anything outside the workspace.

The full table is in `docs/reference/approval-gates.rst`.

## Consequences

- Every merge has a human in the loop, and the pull request is the review artifact.
- Agents do not stall on routine work. The gate covers state that other people see or depend on.
- When an agent cannot tell which side of the line an action falls on, it asks.

## Alternatives considered

- Autonomous merges with CI as the only gate. Rejected: CI verifies what it tests, not whether the change is wanted.
