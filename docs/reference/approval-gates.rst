Approval gates
==============

Agents work fast. Gates keep the people who own a project in control of what other
people see and depend on. The maintainer decides by approving. The agent carries out
what was approved.

The rules in the table mean:

- **allowed**: do it, and record the result.
- **after approval**: queue it in the phase close-out report, and do it only after the
  maintainer approves that report. See :doc:`phase-closeout`.
- **ask first**: name it in the report or in chat, with its exact command, and wait for
  an explicit yes before you do it.
- **never**: do not do it. Ask for access through the approved route.

.. list-table::
   :header-rows: 1
   :widths: 45 15 40

   * - Action
     - Rule
     - Note
   * - Read files, issues, pull requests, and docs
     - allowed
     - Start with a read-only GitHub audit before any change.
   * - Run local checks, builds, and validators
     - allowed
     - Record the commands and their results.
   * - Create branches, and commit to the active phase branch
     - allowed
     - Start commit messages with the task ID.
   * - Push the active phase branch
     - allowed
     - Never force-push a branch that has been reviewed.
   * - Create, edit, or comment on issues of the active phase
     - allowed
     - Write bodies from files, and read them back after posting.
   * - Open a pull request from the phase branch to ``main``
     - allowed
     - The pull request is the review artifact. It is queued with the close-out report.
   * - Write a close-out report and recommend the next actions
     - allowed
     - The report is the evidence that the maintainer reviews. See :doc:`phase-closeout`.
   * - Activate a phase, or start a second active phase
     - after approval
     - Recommended in the close-out of the phase before it. Launched after the approval.
   * - Squash-merge a phase pull request
     - after approval
     - Only after the maintainer approves the close-out report, and only with a green CI
       run on the head commit that the report names.
   * - Close a parent issue
     - after approval
     - Only after the phase pull request has merged. The closeout comment cites the merge
       commit.
   * - Delete a feature branch
     - after approval
     - Only the branch that the approved report names, and only after its merge.
   * - Create a tag, a GitHub release, or a package publication
     - ask first
     - The steps are in :doc:`../guides/release`.
   * - Change repository visibility, settings, the template flag, Pages, or branch protection
     - ask first
     - These change what the public sees. Each change is named with its command, and it
       runs only after its own yes.
   * - Create an external account, repository, or server
     - ask first
     - Name, owner, and visibility must be approved first.
   * - Touch private data, credentials, or paths outside the workspace
     - never
     - Ask the maintainer to supply access through the approved route.
   * - Delete branches, issues, or data beyond what an approved report names
     - ask first
     - Deletion is hard to reverse.

The rule of thumb: if other people can see it, depend on it, or pay for it, a human
decides. The human decides by approving. The agent does the work that the approval names.
