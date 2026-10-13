Starting a new project
======================

This guide takes you from the seed to a reviewed first pull request. Use it for
every new project. Steps that touch GitHub need maintainer approval first; see
:doc:`../reference/approval-gates`.

Before you start
----------------

- Decide the project name, the repository slug (lowercase letters, digits, and
  hyphens), and the owner. The slug becomes the repository name.
- Write two sentences of purpose. They go into the README and ``AGENTS.md``.
- Choose a license. The seed does not choose one for you.

1. Render the seed
------------------

Run the initializer from a checkout of this repository. It writes into a new
directory, copies the validator, and runs the validator on the result:

.. code-block:: bash

   python scripts/new_project.py \
       --name "My Project" \
       --slug my-project \
       --dest ../my-project \
       --purpose "Two sentences that say what the project is for."

The initializer refuses to overwrite existing files unless you pass ``--force``.

2. Adapt the contract
---------------------

Open the new ``AGENTS.md``. Replace the placeholder text in the project
sections, and keep the workflow sections as they are. Add the project's own
verification commands and domain guardrails at the end, each with its reason.

3. Make it a repository
-----------------------

From the new directory:

.. code-block:: bash

   git init -b main
   git add .
   git commit -m "Initial commit: project seed"

With maintainer approval, create the GitHub repository and push:

.. code-block:: bash

   gh repo create <owner>/my-project --private --source=. --remote=origin --push

Switch to ``--public`` only after the maintainer has reviewed the repository.

4. Create the Phase 0 parent issue
----------------------------------

Create a parent issue from ``.github/ISSUE_TEMPLATE/phase.md``, titled
``P0: Bootstrap``, with the ``phase`` label. Create one child issue per task
from ``.github/ISSUE_TEMPLATE/task.md``, titled ``P0.1: ...`` and so on, and
link each one as a sub-issue of the parent. Fill in every required section. A
title and a checklist are not an issue body.

5. Activate the phase
---------------------

Once the maintainer approves, edit ``ROADMAP.md``:

- Set the Phase 0 ``Parent issue:`` line to the parent issue number.
- Set the Phase 0 ``Status:`` line to ``active``.
- Set the same parent number and status in the Issue Tracker Map.

Create the branch ``feature/p0-bootstrap`` from ``main``. Then run the
validator, which must pass before you go on:

.. code-block:: bash

   python scripts/check_workflow.py

6. Work the first task
----------------------

Take one task at a time. For each task:

- Make the change and its docs in the same change set.
- Run the local checks listed in the verification section of ``AGENTS.md``.
- Commit with the task ID at the start of the message.
- Check off the task in ``ROADMAP.md`` and in its issue body when it is done.
- Post a closeout comment on the child issue, then close it.

7. Open the phase pull request
------------------------------

When every task in the phase is complete or deferred, open a pull request from
the phase branch to ``main``. Its body starts with ``Part of #<parent>`` and
lists the child issues. Write the close-out report from the seed's
``notes/reports/phase-closeout-template.md``, and commit it to the branch. The maintainer
approves the report. Then the agent merges the pull request, closes the parent issue,
and deletes the branch. See :doc:`../reference/phase-closeout`.
