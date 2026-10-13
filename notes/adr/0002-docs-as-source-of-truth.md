# ADR 0002: Docs as the source of truth (RTFM)

Status: accepted
Date: 2026-10-13
Issues: #4, #5

## Context

Agent contracts grew long in several lab repositories. One reached more than 400 lines and mixed general rules with domain-specific runbooks. A long contract is hard to keep current, and agents skim it.

## Decision

- The root agent contract, `AGENTS.md`, stays short. It states rules and links to the page that explains each one.
- The Sphinx site under `docs/` is the source of truth for procedures and contracts. Agents read the relevant page before they act, and cite it in their reports. This is the RTFM rule.
- `docs/llms.txt` is a hand-maintained index for machine readers. The docs build copies it to the site root, and the validator checks its links.
- Warnings are errors in the docs build (`-W`). A page that no toctree includes fails the build, so no page is silently orphaned.

## Consequences

- A rule has one home. Duplicates are defects, and the validator's link checks catch the most common drift.
- Writing docs is part of every change set, not a later task.
- The published site must be reachable. The P4 release phase checks that.

## Alternatives considered

- One long contract. Rejected: it grew past the point where agents read all of it.
- Wiki pages. Rejected: a wiki is not reviewed in the same pull request as the code change it describes.
