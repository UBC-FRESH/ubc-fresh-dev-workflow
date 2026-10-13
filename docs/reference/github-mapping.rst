GitHub mapping
==============

The plan lives in ``ROADMAP.md``. GitHub mirrors it, so that people who never
open the repository can see the status, and so that every pull request has a
target.

Parent and child issues
-----------------------

- Each phase is a parent issue. Its title is ``P<n>: <phase name>``, and it has
  the ``phase`` label.
- Each task is a child issue. Its title is ``P<n>.<m>: <task name>``, and it has
  the ``task`` label. It is added as a sub-issue of its parent.
- The parent body lists its child issues as task-list items, with the issue
  number and the task ID, so the list reads correctly without the sidebar.

To link a child to its parent through the API, when the web interface does not
offer the link:

.. code-block:: bash

   child_id=$(gh api repos/OWNER/REPO/issues/CHILD --jq .id)
   gh api -X POST repos/OWNER/REPO/issues/PARENT/sub_issues -F sub_issue_id="$child_id"

Branches
--------

- One phase, one long-lived branch: ``feature/p<n>-<slug>``, created from the
  current ``main``.
- Tasks are committed to the phase branch, with the task ID at the start of each
  commit message.
- A short-lived branch named ``issue-<n>-<slug>`` is allowed only when a task
  needs isolated review. Merge it back into the phase branch.

Pull requests
-------------

- Open one pull request per phase, from the phase branch to ``main``. Its body
  starts with ``Part of #<parent>``, and it lists the child issues with their
  status.
- A pull request for a single task uses the same ``Part of #<parent>`` line. It
  never uses a closing keyword for the parent.
- The agent opens pull requests. The maintainer reviews and merges them.

Closure
-------

- A child issue closes after its closeout comment is posted. The comment names
  the commit, the verification, and the pages that changed.
- The parent issue closes only after the phase pull request has merged to
  ``main``.
- Do not close an issue on a rationale that exists only in chat.

Labels
------

The ``phase`` and ``task`` labels express the level of the work. Add other labels
only for metadata that the level does not express, such as ``docs`` or
``dev-server``. Do not repeat the level as a second label.

Audit before you change anything
--------------------------------

Start with read-only checks before you change any issue state:

.. code-block:: bash

   gh issue list --state open
   gh issue view <n> --json number,title,state,body
   gh pr list --state open

Write bodies and comments to files, and send them with ``--body-file``. Read the
result back with ``gh issue view`` before you report that it was posted.

Offline fallback
----------------

If GitHub is unavailable, record the failed command, its exit status, and the
error text. Then keep an issue-tree manifest in the repository, such as
``notes/issue-tree.md``, with the exact ``gh`` commands that would create the
issues. When access returns, run them, and sync the real numbers back into
``ROADMAP.md``. Do not describe the GitHub side as complete while it is not.
