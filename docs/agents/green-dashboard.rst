The green dashboard
===================

The dashboard is the signal that the repository is healthy. It is green when every gate
passes, and red otherwise. An agent that works in this repository keeps the dashboard green
at all times, and treats any move away from green as the most urgent item in front of it.

The rule
--------

Any change from full green must be investigated and fixed immediately. There are no
exceptions. That includes failures the agent did not cause, flaky tests, warnings, and gates
that seem to be wrong.

What to do when a gate turns red
--------------------------------

1. Stop the current move. Do not start the next task, and do not commit.
2. Read the output tail of the red gate. The dashboard prints it under the gate's name.
3. Reproduce the failure with the gate's own command, from the repository root.
4. Find the cause. Fix the code, the test, or the configuration that is wrong. If the gate
   itself is wrong, fix the gate, and record the change with its reason.
5. Run the full dashboard again, and confirm that it is green.
6. Record the failure, its cause, and its fix in the changelog entry for the task.
7. Report to the maintainer if the fix needed a decision, such as a changed threshold or a
   new dependency.

When you cannot fix it
----------------------

If the cause is outside your authority, such as a service that is down or a repository
setting, do not hide the failure, and do not continue. Report the exact command, the exit
status, and the error text, and wait for a decision.

Where the dashboard runs
------------------------

- Locally, with ``python scripts/dashboard.py``.
- In CI, in the ``dashboard`` job, which writes its table into the job summary.
- Inside every generated project, through that project's own ``scripts/dashboard.py``.

Signal, not theatre
-------------------

A green dashboard is evidence only when its gates measure the right thing. If a gate passes
while the defect it guards against is present, the gate is the defect. Fix the gate, and
record the change in the changelog.
