Typing and docstrings
=====================

Why full typing
---------------

Full type annotations cost tokens and time when code is written. They pay back quickly when
code is debugged. A type checker that runs on every commit tells a coding agent which call
is wrong, which attribute is missing, and which value can be ``None``, before a test has to
find it. The payback is almost immediate, which is why the workflow requires it.

The rules
---------

- Every function, method, and test has an annotation for every parameter and for its return
  value. Test functions return ``None``.
- ``mypy --strict`` passes on ``scripts/``, ``tests/``, and ``docs/conf.py``.
- Use precise types. Prefer ``list[str]`` to ``list``, a ``Literal`` to a bare ``str`` for a
  fixed set of values, and ``Path`` to ``str`` for paths.
- Do not use ``Any`` in an annotation. Do not use ``# type: ignore`` or ``cast`` without a
  comment that names the reason. A suppression names the error code it suppresses.
- Approved exception: numpydoc ships no type markers. It is the only untyped dependency
  that the framework imports. mypy treats it as ``Any`` through a narrow override in
  ``pyproject.toml``, and the docstring test checks the results that numpydoc produces.

Docstrings
----------

Every public function, class, and module in ``scripts/`` has a numpy-style docstring. The
annotations are the source for the types in the docstring:

- A one-line summary in the imperative mood, such as "Build the report."
- An optional extended description.
- ``Parameters``: one entry for each parameter, with its type and a description.
- ``Returns``: the return type and a description, for any function that returns a value.
- ``Raises``: each exception that the function raises on purpose.

The type in a docstring entry must match the annotation. A mismatch is a documentation bug,
and the docstring test in P0.8 checks the sections that numpydoc validates.

Enforcement
-----------

.. list-table::
   :header-rows: 1
   :widths: 34 66

   * - Check
     - What it catches
   * - ``ruff`` with the ``ANN`` rules
     - Missing annotations on parameters and return values.
   * - ``ruff`` with the ``D`` rules, numpy convention
     - Missing docstrings, and docstring formatting problems.
   * - ``mypy --strict``
     - Type errors, missing annotations, and implicit ``Any``.
   * - numpydoc validation test (P0.8)
     - Missing or inconsistent docstring sections.
