# ADR 0009: Phase 0 is local, and repository creation is an activation step

Status: accepted on 2026-10-14. The maintainer chose Option A.
Date: 2026-10-14
Issues: #25 (F4), #34 (P3.1)
Related: ADR 0004, ADR 0008

## Context

The seed's Phase 0 has one GitHub task, P0.1: "Create the GitHub repository and push the rendered seed." A phase becomes active only after its parent issue exists, and the parent issue lives in the GitHub repository. So the repository must exist before Phase 0 starts, and P0.1 describes work that is already done at activation. The seed's own next steps say the same: "Create the GitHub repository and the Phase 0 parent issue. This needs maintainer approval."

A local rehearsal cannot tick P0.1. The P1.1 rehearsal used a local bare remote in its place, and the P1.6 close-out counted P0.1 as met with a stated limit. The dogfood log records this as F4.

## Options

- **A. Move the GitHub step into activation.** Phase 0 keeps only its local tasks. Repository creation, the first push, and the Phase 0 parent issue become activation steps, each with maintainer approval. The first-project guide already describes them.
- **B. Keep P0.1, marked as approval-gated.** The seed already marks P5.2 this way, "(maintainer approval required)". The task stays visible, but it is ticked at activation, before the phase starts. A local rehearsal still needs a stand-in remote to tick it.
- **C. Split Phase 0 into a local phase and a GitHub phase.** The GitHub phase still needs a repository before its parent issue exists, so the external step stays outside the phase. Every project gets an extra phase and an extra close-out.

## Recommendation

Option A. P0.1 repeats an activation step, and removing it lets Phase 0 finish on a machine without GitHub access. It also keeps an external action out of the phase's evidence, where ADR 0004 and the approval gates place it.

## Decision

Option A, accepted by the maintainer on 2026-10-14. Phase 0 keeps only local tasks. Repository creation, the first push, and the Phase 0 parent issue are activation steps, and each one needs maintainer approval.

## Consequences of Option A

- Phase 0 keeps two local tasks, renumbered: P0.1 "Adapt `AGENTS.md` and `README.md` to this project", and P0.2 "Confirm the validator and the docs build pass". Renumbering is cheap while the seed is still being built, and costly once projects are generated from it.
- The Phase 0 goal drops "create the repository".
- The first-project guide's activation steps stay as they are.
- F4 closes when the template change lands, and #25 closes with a closeout comment.
