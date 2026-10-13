Testing policy
==============

Tests are how an agent knows that its change works, and how a reviewer knows that an
earlier change still works. The policy asks for several layers of tests, and each layer
catches a different kind of failure.

The layers
----------

.. list-table::
   :header-rows: 1
   :widths: 16 44 40

   * - Layer
     - What it checks
     - Where it lives
   * - Unit
     - Each function, on its normal path, its edge cases, and its failure paths.
     - ``tests/test_check_workflow.py``, ``tests/test_new_project.py``, ``tests/test_dashboard.py``
   * - Contract
     - Public interfaces. The seed renders a project, the validator passes it, and the shared
       framework files arrive in every project.
     - ``tests/test_new_project.py``, ``tests/test_workflow.py``
   * - Integration
     - The command-line tools, run in subprocesses, as CI runs them.
     - ``tests/test_cli.py``
   * - Property
     - Invariants that must hold for every generated input, found with hypothesis.
     - ``tests/test_properties.py``
   * - Docstring
     - Every public function documents its parameters and return values, checked by numpydoc.
       Added in P0.8.
     - ``tests/test_api_docstrings.py``
   * - Dogfood
     - The seed generates a project, and the project passes its own full dashboard.
     - The ``seed`` and ``seeded-dashboard`` gates

Rules
-----

- Every function you write or change gets unit tests in the same change set.
- Each test asserts a specific behavior. A test that only checks that nothing raised is not
  enough. The test name and its docstring say which behavior it checks.
- Build bad fixtures at runtime, so that test files do not contain the patterns they check
  for. The validator scans the files that a commit would include, and a fixture must not
  trip the check it tests.
- Test the failure paths as carefully as the success paths. The branches that report
  problems are the ones that people rely on.
- Use hypothesis when the input space is large and the property is clear. Keep examples
  small enough that a failure is easy to read.
- Keep tests fast. The whole suite should finish in a few seconds, so that it can run on
  every commit.
- Do not skip, xfail, or delete a failing test to get a green dashboard. Fix the code, or
  change the test with a changelog entry that explains why the old expectation was wrong.

Coverage
--------

Branch coverage of ``scripts/`` is gated at 95 percent in ``pyproject.toml``. The current
suite reaches 100 percent. The gate exists to catch untested code, so a drop below the
current level is a finding. Do not write tests that run lines without asserting anything
about them.

A focused run of one test file can skip the gate with ``--no-cov``. The full dashboard
always runs the gate.

Flaky tests
-----------

A test that sometimes fails is a red gate. Stop, reproduce the failure, and fix its cause.
Do not rerun the job until it happens to pass.
