Lifecycle stages and gates
==========================

Every project built from the seed moves through six stages: scope and design, build,
verify, release and deploy, operate and maintain, and retire. Each stage ends at a gate.
The entry criteria say what must be true before a stage starts. The exit criteria say
what must be true, with evidence, before its gate can be passed.

The maintainer owns every gate. The agent prepares the evidence and the report, and it
never passes a gate on its own.

The stages
----------

.. list-table::
   :header-rows: 1
   :widths: 16 28 38 18

   * - Stage
     - Entry criteria
     - Exit criteria
     - Gate owner
   * - Scope and design
     - The project has a repository, a roadmap, and an approved parent issue for its first phase.
     - The goal, scope, and out-of-scope items are recorded. Each decision that will matter later is an ADR, and each one is accepted, or deferred to an issue with its reason.
     - The maintainer
   * - Build
     - The scope and design gate is passed. Each task has a child issue.
     - Each task is committed to the phase branch with its task ID, and each commit leaves the full dashboard green. The docs that describe a change are updated in the same change set. Each task closes with a closeout comment that names its commit.
     - The maintainer
   * - Verify
     - Every build task is closed, and the phase pull request is open against ``main``.
     - The full dashboard and CI pass on the head commit. Each acceptance criterion has evidence in the close-out report: a command, a commit, or a run ID. A red gate is a named deviation, with the commit that fixed it.
     - The maintainer
   * - Release and deploy
     - The verify gate is passed. The release is named in an approved report, with its exact commands.
     - The tag, the release notes, and the live Pages site exist. A clean checkout of the tag, or a project generated from the template, passes the validator and the dashboard.
     - The maintainer, who approves each tag, release, and Pages action on its own
   * - Operate and maintain
     - The release gate is passed. The review cadence is recorded in the roadmap.
     - Each review on the cadence is recorded, and each incoming idea has a disposition. The stage ends with a recorded decision to retire the project.
     - The maintainer
   * - Retire
     - The retirement decision is recorded as an ADR, and the maintainer approves it.
     - An archive notice is posted, a final changelog entry is written, and every open issue is closed with a closeout comment. Archiving the repository is a settings change, so it waits for its own approval.
     - The maintainer

Passing a gate
--------------

- The agent queues the phase's pull request, writes its close-out report, and names the gates that the phase passes. See :doc:`phase-closeout`.
- The maintainer passes a gate by approving the report, as written or with the changes it states. That approval is the explicit answer that ADR 0004 requires.
- An approval covers only what the report names. Anything else goes back into a report.
- A criterion that is not met blocks its gate. A criterion met with a stated limit does not, and the report names the limit.

Actions inside a stage
----------------------

Some actions in the release, operate, and retire stages change settings or publish outside the repository. These are tags, releases, package publication, Pages, visibility, settings, the template flag, and branch protection. Each one is named in an approved report with its exact command, and it runs only after its own approval. The rules are in :doc:`approval-gates`.

Relation to the other pages
---------------------------

The playbooks in this phase, for release, data management, and agent roles, link to this page and do not repeat its rules. The roadmap's Lifecycle Map shows which phases of this repository sit in each stage.
