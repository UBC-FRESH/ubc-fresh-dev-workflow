Agent roles and models
======================

This page sets out the agent roles of the workflow, the task families that each role covers,
the rule for choosing a model for a family, and the log of each choice. Model choice is
configuration. It is not a permanent rule, and it stays out of `AGENTS.md
<https://github.com/UBC-FRESH/ubc-fresh-dev-workflow/blob/main/AGENTS.md>`__. The P5.2 quarterly
review re-checks every choice in the log.

Roles
-----

.. list-table::
   :header-rows: 1
   :widths: 16 54 30

   * - Role
     - What it does
     - Task families
   * - Planner
     - Drafts phases, tasks, and subtasks, the issue bodies that mirror them, and the ADRs that plan them. Keeps the roadmap in step with the issues.
     - Planning and decomposition.
   * - Implementer
     - Makes one bounded change at a time, with its tests in the same change set, and commits it with its task ID. Updates the docs and the changelog in the same change set.
     - Implementation with tests; documentation and records.
   * - Verifier
     - Runs the gates, reproduces any red result, and checks each claim in a close-out report against its evidence.
     - Verification and debugging; close-out evidence review.
   * - Maintainer
     - Approves each gate, and each action that changes a setting, publishes, or touches private data.
     - Approvals and sensitive work.

Each role has its own instructions and permissions. A verifier is separate from the
implementer, even when one model runs both, because one model in two roles is still one
reviewer. The independent check comes from the gates, which are mechanical, and from the
evidence rules in :doc:`oracles-and-evidence`.

Choosing a model
----------------

Choose a model for each task family on evidence from real runs. A claim by a provider, or a
benchmark on its own, is not evidence. A model meets the bar for a family when, on that
family's tasks:

- each commit it makes leaves the full dashboard green (:doc:`green-dashboard`);
- each new test it writes is shown to fail on the old code, and to pass on the new code;
- its close-out evidence cites a commit, a run ID, or command output for each claim, and the
  verifier finds no unsupported claim.

A model that misses the bar is replaced for that family, and the replacement is logged with
its reason. A benchmark may inform a choice. The log says so when it does.

Sensitive work
--------------

Private data, credentials, settings, and publication form a separate task family. No model
handles them without an approval that names the action and the data. The log grants no access.
See :doc:`../reference/approval-gates`, and the data rules in :doc:`../guides/data-management`.

Routing
-------

A task that spans families is split into bounded moves, and each move goes to the role for its
family. See :doc:`bounded-moves`.

The model log
-------------

Each row records one choice. A row is dated, names its role and task families, and states its
evidence and how strong that evidence is. When a choice changes, add a row. Do not edit an old
row, so that the log keeps its history.

.. list-table::
   :header-rows: 1
   :widths: 12 22 22 34 10

   * - Date
     - Role and task families
     - Model choice
     - Evidence
     - Re-check
   * - 2026-10-13
     - Planner and implementer, for planning, implementation, and documentation.
     - deepseek v4.1 flash, at its maximum thinking setting, through OpenCode's gateway.
     - The maintainer reports that this setup works well in the lab dev container. This is one data point, not a comparison.
     - P5.2 review
   * - 2026-10-14
     - Implementer and verifier, in the Phase 3 sessions, for implementation, documentation, and verification.
     - claude-haiku-5-5, through OpenCode, with the opencode-go provider.
     - Each Phase 3 commit, from ``d3593bb`` to ``fed5c45``, passed the full dashboard before it was made. These are gate results, not a comparison.
     - P5.2 review

Re-checks
---------

The P5.2 quarterly review re-checks every row. A choice must also be re-checked when the
provider or the model changes, as the dev server guide requires. A re-check that keeps a
choice adds a row with its new date and evidence. A re-check that changes a choice adds a row
for the new choice.

Related pages
-------------

- :doc:`oracles-and-evidence` sets the evidence standards for close-out claims.
- :doc:`../reference/approval-gates` says which actions wait for approval.
- :doc:`../guides/dev-server/ide-agents-and-models` configures OpenCode and the chosen model.
