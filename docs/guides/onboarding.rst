Onboarding
==========

This guide is for a new team member, a collaborator who wants to adopt the
pattern, or anyone who needs to understand how work moves through a project.
It takes about thirty minutes and needs nothing more than a browser and a
terminal.

What you will learn
-------------------

- How a plan becomes phases, tasks, and subtasks, and how each level maps to
  GitHub issues and branches.
- What a coding agent may do without asking, and what it must not do.
- How to check whether a project follows the pattern, using the validator.

Reading order
-------------

1. Read the repository ``README.md``. It shows the pattern in one picture.
2. Read ``ROADMAP.md``. Find phase P0 and see how its tasks mirror GitHub
   issues #2 to #8, which are sub-issues of parent issue #1.
3. Read :doc:`../reference/workflow-model`. Every rule in the roadmap comes
   from it.
4. Read :doc:`../reference/approval-gates`. It answers the question "who
   decides?"
5. Read :doc:`../agents/session-protocol`. It is the protocol a coding agent
   follows, and it shows what a good report looks like.
6. Skim :doc:`../reference/issue-standard` and :doc:`../reference/github-mapping`
   before you open your first issue.
7. Read :doc:`dev-server/index` only if you need to set up an environment.

Try it
------

Run the checks from a fresh clone. Each command should succeed:

.. code-block:: bash

   git clone https://github.com/UBC-FRESH/ubc-fresh-dev-workflow.git
   cd ubc-fresh-dev-workflow
   python -m venv .venv
   . .venv/bin/activate
   python -m pip install -r requirements-dev.txt
   python -m ruff check .
   python -m pytest
   sphinx-build -b html docs _build/html -W
   python scripts/check_workflow.py

Then open the parent issue for phase P0 on GitHub, and read one child issue
from start to finish. Ask yourself whether you could do that task, verify it,
and close it without the conversation that created it.

Glossary
--------

Phase
   A coherent deliverable with a goal and exit criteria. One phase is one
   parent issue and one feature branch.

Task
   One reviewable unit of work inside a phase. One task is one child issue,
   linked as a sub-issue of the parent.

Subtask
   A checklist item inside a task's issue body.

Sub-issue
   GitHub's parent and child link between issues. The parent lists its
   children.

Feature branch
   The long-lived branch for a phase, named ``feature/p<n>-<slug>``.

Closeout comment
   The final comment on an issue. It names the commit, the verification, and
   the pages that changed, and it is posted before the issue closes.

Oracle
   A check that can fail against real state, such as the validator or a test.

RTFM
   "Read the manual." In this pattern, the manual is this site.

Seed
   The template that ``scripts/new_project.py`` renders into a new project.
