Phase close-out
===============

A phase ends with a close-out package. The agent queues the phase's pull request, writes
the close-out report, and recommends the next actions. The maintainer reviews the report,
and approves it or asks for changes. After approval, the agent executes what the report
approves, and reads back each result. The maintainer reviews and approves. The agent does
the work.

The lifecycle
-------------

.. list-table::
   :header-rows: 1
   :widths: 16 62 22

   * - Step
     - What happens
     - Who acts
   * - Activate
     - The phase has a parent issue, a feature branch from ``main``, a roadmap entry with
       status ``active``, and child issues linked as sub-issues. The maintainer approved
       the phase in the close-out of the phase before it, or directly for the first phase.
     - agent
   * - Work
     - Bounded moves. Every commit starts with its task ID and leaves the full dashboard
       green. The roadmap, the changelog, the notes, and the issues stay in step with the
       work.
     - agent
   * - Queue
     - Open the pull request to ``main`` with ``Part of #<parent>`` in its body. Write the
       close-out report from the seed template into ``notes/reports/``, and commit it to
       the phase branch. Post the summary on the pull request and on the parent issue.
     - agent
   * - Approve
     - The maintainer approves the report as written, or asks for changes. Changes go on
       the branch, and the report is refreshed to name the new head commit.
     - maintainer
   * - Execute
     - Squash-merge the pull request, and delete its branch. Close the parent issue with a
       closeout comment that cites the merge commit. Apply each approved settings change,
       and read it back.
     - agent
   * - Launch
     - Switch to ``main`` and update it. Create the next phase's branch. In its first
       commit, set the finished phase to ``complete`` and the next phase to ``active`` in
       the roadmap. Create the next phase's child issues as sub-issues of its parent, post
       the activation on the parent, and start the first task.
     - agent

The report
----------

The report is the review artifact. Write it from the seed's template,
``notes/reports/phase-closeout-template.md``, and keep it in ``notes/reports/``. It has
these sections, in this order:

1. **Header.** The phase, the parent issue, the pull request, the evidence head commit,
   the report date, and the status.
2. **Recommendation.** Each action to approve, in the order the agent executes them. Each
   settings change is written with its exact command.
3. **Objectives and acceptance.** Each acceptance criterion from the roadmap, its evidence,
   and one status: met, met with a stated limit, or not met.
4. **Workflow compliance.** The evidence for each rule in ``AGENTS.md``: the parent issue
   before the branch, the branch from ``main``, commit messages that start with task IDs,
   the gates for each commit, the roadmap and the changelog in step, the child issues
   closed with closeout evidence, and the approval gates respected.
5. **Gate evidence.** The gates that each commit could run, and what they reported.
6. **CI evidence.** Each run on the evidence head, with its run ID, its head commit, its
   conclusion, and its job names. A failed run appears too, with its cause and its fix.
7. **Deviations.** Each deviation, its cause, and its remedy.
8. **Next phase.** The proposed phase: its goal, its tasks, its acceptance criteria, its
   child issues, and a recommended default for each open choice.
9. **Decision.** Approve as written, or approve with the changes that are stated.

Evidence rules
--------------

- Cite a commit, a run ID, an issue or pull request number, or command output for each
  claim.
- State the verification scope. A check that was not run is listed as not run.
- A red gate is a deviation until the report names the commit that fixed it.
- A report goes stale when the head moves. Refresh it before the next approval request.
- Do not rewrite a pushed branch to tidy the record. Disclose the history instead.

Recommendations, not questions
------------------------------

A report does not hand decisions back as open questions. Each open choice is written as a
recommendation, with a default and the reason for it. The maintainer approves the default
or changes it.

Settings and external actions
-----------------------------

Settings changes, such as Pages, branch protection, visibility, the template flag, tags,
and releases, are named in the recommendation with their exact commands. The agent runs
each one only after the maintainer approves that item. Creating an external repository or
account follows the same rule.

Stop conditions
---------------

Stop, and fix the cause, before you queue or execute when:

- CI is red on the head commit that the report names.
- A gate is red on your machine.
- An approved action would cover more than the approval names.
- GitHub is unavailable. Record the failed command, its exit status, and the error text.

Relation to the other pages
---------------------------

The rule for each action is in :doc:`approval-gates`. The branch, commit, and pull request
conventions are in :doc:`git-conventions` and :doc:`github-mapping`. The decision is
recorded in ADR 0008.
