Workflow model
==============

The workflow has three levels and one plan of record.

Levels
------

.. list-table::
   :header-rows: 1
   :widths: 18 22 60

   * - Level
     - Identifier
     - What it is
   * - Phase
     - ``P<n>``
     - A coherent deliverable with a goal and exit criteria. One phase is one
       parent GitHub issue and one feature branch.
   * - Task
     - ``P<n>.<m>``
     - One reviewable unit of work inside a phase. One task is one child issue,
       linked as a sub-issue of the parent.
   * - Subtask
     - checklist item
     - A step inside a task issue body. A subtask becomes a fourth-level issue
       only in rare cases, and the default is not to make one.

Three levels is the limit. If a phase seems to need a fourth level, split the
phase instead.

Plan of record
--------------

``ROADMAP.md`` is the plan of record. Each phase section begins with three
header lines, in this order. The validator reads them:

.. code-block:: text

   ## Phase 1: Example phase

   Parent issue: #9
   Branch: `feature/p1-example`
   Status: planned

Tasks are checkboxes that begin with the task ID. Subtasks are indented
checkboxes under their task:

.. code-block:: text

   - [ ] P1.1 First task (#10)
     - [ ] First subtask
     - [x] Second subtask

The Issue Tracker Map at the top of ``ROADMAP.md`` has one row per phase, with
the same parent issue, branch, and status as the phase section.

Status values
-------------

.. list-table::
   :header-rows: 1
   :widths: 18 82

   * - Status
     - Meaning
   * - ``planned``
     - The phase is in the roadmap and mirrored in a parent issue. No work has
       started. Only a planned phase may show ``Parent issue: TBD``.
   * - ``active``
     - The maintainer approved the phase. The parent issue, the branch, and the
       child issues exist.
   * - ``pr-open``
     - Every task is done or explicitly deferred. The pull request to ``main`` is
       open. The close-out report is queued for the maintainer's approval.
   * - ``complete``
     - The pull request merged, and the parent issue is closed. Every task is
       checked.
   * - ``deferred``
     - The phase is parked by decision. The roadmap records the reason.

Completion rules
----------------

- A task is checked when its work is committed, its checklist is complete, and
  its verification is recorded. A checked task keeps its issue number.
- A child issue closes after its closeout comment is posted. A parent issue
  closes only after its pull request has merged.
- A phase is ``complete`` only when every task is checked, or deferred with a
  recorded reason.

Where each fact lives
---------------------

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Fact
     - Home
   * - What the phase is for, and its scope
     - The parent issue and ``ROADMAP.md``
   * - Status and the order of work
     - ``ROADMAP.md``, the plan of record, and its tracker map
   * - What happened, in order
     - ``CHANGE_LOG.md``
   * - Why a decision was made
     - ``notes/adr/``
   * - Detail too long for the roadmap
     - A plan in ``notes/``, linked from the task
   * - How a procedure works
     - The pages under ``docs/``

Validation
----------

``scripts/check_workflow.py`` enforces the grammar above. Its finding codes are
stable, and :doc:`../agents/oracles-and-evidence` lists them.
