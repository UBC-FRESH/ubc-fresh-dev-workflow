Session protocol
================

Follow this protocol at the start of every session and at every hand-off.

Start prompt
------------

Begin a session with a prompt that names the project and the authoritative
files:

.. code-block:: text

   We are working on the <project> project in this workspace. Before making
   changes, read AGENTS.md, ROADMAP.md, and the notes for this task. Use those
   as the authoritative context. The active phase is P<n>, and the task is
   P<n>.<m>.

Steps
-----

1. Read ``AGENTS.md``, the active phase in ``ROADMAP.md``, the latest entries in
   ``CHANGE_LOG.md``, and the notes that the task names.
2. Read the docs pages that govern the task. Cite them in your report.
3. Audit GitHub read-only before you change anything: ``gh issue view <n>`` for
   the parent and the child, and ``gh pr list`` for open pull requests.
4. Confirm that the task belongs to the active phase. If the phase is not
   active, or the task is not in the roadmap, stop and ask. See
   :doc:`../reference/approval-gates`.
5. For non-trivial work, write the plan into ``ROADMAP.md`` or the task issue
   before you edit anything.
6. Work one bounded move at a time. See :doc:`bounded-moves`.
7. Verify with the checks in ``AGENTS.md``. Read the output yourself, and record
   the exact commands and their results.
8. Update the same change set: roadmap checkboxes, the changelog entry, notes,
   and docs.
9. Commit with the task ID at the start of the message. Push the phase branch.
10. Post a progress comment on the child issue and, when the phase status
    changes, on the parent. Read the comment back with ``gh issue view`` before
    you say it was posted.
11. Report to the maintainer with evidence: commit hashes, command output, issue
    and pull request links, and any blocker. Then stop and wait for the next
    instruction.

Hand-off
--------

Leave the artifacts current, so the next session can start from them. The
roadmap says what is next, the changelog says what happened, and the issue says
what remains. A new session should not depend on this conversation.

What good reporting looks like
------------------------------

- It states what changed, with file paths and commit hashes.
- It states what was verified, with the command and its exit status.
- It states what was not verified, and why.
- It states the blocker, if there is one, with the exact error text.
- It ends with the next move you propose, and waits for approval if that move
  needs it.

Phase close-out
---------------

When every task in the phase is complete, do not end the phase with this list. Follow
:doc:`../reference/phase-closeout`. Queue the pull request, write the close-out report,
and wait for the maintainer's approval before you merge, close the parent issue, delete
the branch, or launch the next phase.
