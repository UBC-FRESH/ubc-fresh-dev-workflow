Approval gates
==============

Agents work fast. Gates keep the people who own a project in control of what other
people see and depend on.

.. list-table::
   :header-rows: 1
   :widths: 45 15 40

   * - Action
     - Agent
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
     - The pull request is the review artifact.
   * - Activate a phase, or start a second active phase
     - ask first
     - Needs an explicit yes from the maintainer.
   * - Merge a pull request
     - maintainer
     - Agents never merge.
   * - Close a parent issue
     - maintainer
     - Only after the phase pull request has merged.
   * - Create a tag, a GitHub release, or a package publication
     - ask first
     - The release playbook (planned, P3) will list the steps.
   * - Change repository visibility, settings, the template flag, or Pages
     - maintainer
     - These change what the public sees.
   * - Create an external account, repository, or server
     - ask first
     - Name, owner, and visibility must be approved first.
   * - Touch private data, credentials, or paths outside the workspace
     - never
     - Ask the maintainer to supply access through the approved route.
   * - Delete branches, issues, or data
     - ask first
     - Deletion is hard to reverse.

The rule of thumb: if other people can see it, depend on it, or pay for it, a
human decides.
