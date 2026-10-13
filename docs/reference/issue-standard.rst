Issue standard
==============

Issue bodies are the project specification. Write each one so that a new student,
an external collaborator, or a coding agent can understand the task, do it,
verify it, and close it, without the conversation that created it.

Titles
------

- Phase issues: ``P<n>: <phase name>``.
- Task issues: ``P<n>.<m>: <task name>``.

Required sections: phase issues
-------------------------------

A phase issue has these labelled sections, in this order:

- ``Phase identifier:``, ``Status:``, ``Branch:``, ``Roadmap:``, and
  ``Pull request:``.
- ``Goal:``
- ``Scope:``
- ``Out of scope:``
- ``Architecture notes:``
- ``Child task checklist:``, with task-list items that carry the issue number and
  the task ID.
- ``Acceptance criteria:``
- ``Verification:``, as commands that can be run.
- ``Closeout requirements:``

Required sections: task issues
------------------------------

A task issue has these labelled sections:

- ``Task identifier:``, ``Parent phase issue:``, ``Status:``, ``Branch:``, and
  ``Related planning:``.
- ``Goal:``, ``Scope:``, and ``Out of scope:``.
- ``Subtasks:``, as task-list items.
- ``Acceptance criteria:``, ``Verification:``, and ``Artifacts:``.
- ``Risks:``
- ``Completion metadata:``, which is filled in at closeout with the commit, the
  verification result, and the pull request.

Formatting rules
----------------

- Put each section label on its own line.
- Use real task-list syntax, one item per line.
- Wrap branch names, paths, commands, and commit hashes in backticks.
- Never write an inline pseudo-checklist, such as this one:

.. code-block:: text

   Checklist: [ ] first. [ ] second.

Write the list as separate lines instead:

.. code-block:: text

   Subtasks:
   - [ ] First.
   - [ ] Second.

Control characters and corrupt bodies
-------------------------------------

Build issue bodies from files, not from escaped strings. In a shell or a program,
a sequence such as ``\f`` (form feed) or ``\t`` (tab) becomes a control
character, not the two characters that were typed. The result can be a branch
name that lost its first letter, or a command with a tab in it. A byte-order mark
(U+FEFF) can appear at the start of a line. A published parent issue in a sibling
repository showed all three.

Two protections apply:

1. Write the body to a file, with an editor or the ``write`` tool, and pass it
   with ``--body-file``. Do not pass hand-built escapes with ``--body "..."``.
2. Run the validator on body files before you post them:

.. code-block:: bash

   python scripts/check_workflow.py --files path/to/body.md

The validator rejects control characters, carriage returns, and byte-order marks.

Anti-patterns
-------------

- A placeholder body: a title and a short checklist, with no goal, scope, or
  acceptance criteria. Use the templates in ``.github/ISSUE_TEMPLATE/``.
- A silent scope change. When the scope changes, edit the body and post a comment
  that says what changed and why.
- A closed issue with no closeout comment.
