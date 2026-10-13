Bounded moves
=============

A bounded move is one unit of work that you can verify and report on its own.
Exactly one of these counts as a bounded move:

- one code change;
- one validation run;
- one documentation or planning update; or
- one issue or pull request update.

Do not bundle these into one "helpful" step. A code change, followed by a broad
rerun and a downstream check, is three moves, and each one needs its own report.

Rules
-----

- Before an expensive or broad command, state three things: the exact command,
  the single question it answers, and why a smaller run cannot answer it.
- After each move, stop, report the result with evidence, and wait for the next
  instruction, unless the maintainer asked for a sequence.
- Scope expansion is a defect, not initiative. If you notice adjacent work,
  record it as a proposal in the roadmap's "Detailed Next Steps Notes", or as a
  new issue for the maintainer to triage. Do not start it.

Scope breach
------------

If the maintainer says "scope breach", stop any running background work at once.
Return to the last agreed move. Do not propose broader work until the maintainer
expands the scope in writing.
