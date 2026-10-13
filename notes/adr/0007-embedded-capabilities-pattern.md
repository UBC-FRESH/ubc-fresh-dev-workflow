# ADR 0007: Embedded agent capabilities, validated and advisory

Status: accepted, experimental
Date: 2026-10-13
Issues: #16

## Context

Complicated scientific packages are where coding agents make plausible mistakes. Their
documentation is long, their APIs change between versions, and a wrong call can be expensive.
Public UBC-FRESH packages have already tried to close this gap. The ws3 agent guide records
fabricated APIs that reached its documentation, its tests, and its code before a validator
existed. A capability without a validator reproduces that failure.

## Decision

- The template documents one contract for embedded capabilities. A capability has a typed input,
  a validator over real package state, a bounded retry budget, advisory output, explicit failure,
  and provenance for every attempt.
- The runtime lives in `fresh-agent-core`, and packages consume it. This template ships no runtime.
- The contract is experimental until at least one package passes the conformance checklist end to end.
- "No oracle, no capability" is a rule. A capability whose validator cannot fail is removed.

## Consequences

- Packages that adopt the pattern get a reviewable checklist, and reviewers get a common vocabulary.
- Each capability costs a validator and its tests. That cost is the point of the pattern.
- An agent that uses a capability gets a validated answer, and it still reads the documentation for
  everything else.

## Alternatives considered

- Retrieval over the documentation only. Rejected for high-risk calls: a retrieved paragraph is not a
  check against the installed package.
- One shared capability catalog for all packages. Rejected: each package's state is its own, and its
  validators must read that state directly.
