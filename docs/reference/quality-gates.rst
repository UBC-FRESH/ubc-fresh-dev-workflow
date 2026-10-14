Quality gates
=============

A quality gate is a command that must exit with status 0. The gates together form the
green dashboard. Every commit must leave the dashboard green, and CI runs the same gates
on every pull request.

The gates
---------

.. list-table::
   :header-rows: 1
   :widths: 18 40 42

   * - Gate
     - Command
     - What it protects
   * - ``lint``
     - ``python -m ruff check .``
     - Lint rules: errors, imports, bugs, naming, docstring rules, and annotation rules.
   * - ``format``
     - ``python -m ruff format --check .``
     - One formatting style, so that diffs show changes in meaning rather than layout.
   * - ``types``
     - ``python -m mypy``
     - Strict type checking of ``scripts/``, ``tests/``, and ``docs/conf.py``.
   * - ``tests``
     - ``python -m pytest``
     - Every test passes, and branch coverage of ``scripts/`` meets the gate of 95 percent.
   * - ``validator``
     - ``python scripts/check_workflow.py``
     - The planning surfaces follow the workflow: roadmap grammar, changelog order, links,
       and text hygiene.
   * - ``docs``
     - ``sphinx-build -b html docs _build/html -W``
     - The documentation builds, and every warning is an error.
   * - ``seed``
     - ``python scripts/new_project.py ...``
     - The project seed renders a project that passes the validator. Runs only in a
       repository that contains the generator.
   * - ``seeded-dashboard``
     - ``python tmp/dashboard-seed/scripts/dashboard.py``
     - The rendered project passes its own full dashboard. Runs only in a repository that
       contains the generator.

Run the gates
-------------

.. code-block:: bash

   python scripts/dashboard.py              # table on the terminal; exit 0 only when green
   python scripts/dashboard.py --markdown   # the same results, as a Markdown table
   pre-commit install                       # run the hooks on every commit
   pre-commit run --all-files               # run the hooks on the whole repository

The pre-commit hooks mirror the gates: ruff check, ruff format, mypy, the validator, and
the test suite. The CI job ``pre-commit`` runs every hook on the whole repository, so a
hook that is skipped locally fails in CI.

Continuous integration
----------------------

- The ``quality`` job runs on Python 3.11 and 3.12, for every pull request and every push
  to ``main``. It runs lint, format, types, tests, the validator, and the docs build. It
  also generates a project from the seed and runs the same checks inside it. It runs
  ``shellcheck`` and ``bash -n`` on each script in ``server/``.
- The ``dashboard`` job runs the dashboard and writes its table into the job summary. It
  uploads the JSON record as an artifact.
- The ``pre-commit`` job runs every hook on the whole repository.
- Every workflow runs on the pinned runner ``ubuntu-24.04``, and every action is a version whose
  own metadata declares Node 24. The runner is pinned because GitHub moves ``ubuntu-latest`` to
  Ubuntu 26 from 19 October 2026. ``tests/test_ci_workflows.py`` checks both rules, so a change
  to ``ubuntu-latest`` or to an older action fails the dashboard.

Required status checks (approved settings change)
--------------------------------------------------

Branch protection makes a pull request mergeable only when the required checks pass. The
close-out report that recommends it names the command below. The agent runs the command
after the maintainer approves that item, and reads the rule back with
``gh api repos/OWNER/REPO/branches/main/protection``. The required checks are the
``quality`` job for each Python version, the ``dashboard`` job, and the ``pre-commit``
job. Do not merge a pull request while any of them is red.

.. code-block:: bash

   gh api -X PUT repos/OWNER/REPO/branches/main/protection --input - <<'JSON'
   {
     "required_status_checks": {
       "strict": true,
       "contexts": [
         "Quality gates, Python 3.11",
         "Quality gates, Python 3.12",
         "Green dashboard summary",
         "Pre-commit parity"
       ]
     },
     "enforce_admins": false,
     "required_pull_request_reviews": null,
     "restrictions": null,
     "allow_force_pushes": false,
     "allow_deletions": false
   }
   JSON

No approving review is required. The phase pull requests are opened from the maintainer's
account, and GitHub does not let an author approve their own pull request. The maintainer's
approval of the close-out report is the review. Administrators are not enforced, so the
maintainer can still act in an emergency. The report must name any use of that path.

Changing a gate
---------------

A gate changes only with a changelog entry that says what changed and why, and the
dashboard must be green afterwards. Lowering the coverage gate, or removing a gate, is a
decision for the maintainer and needs an ADR.

When a gate turns red
---------------------

Follow :doc:`../agents/green-dashboard`. The rule has no exceptions.
