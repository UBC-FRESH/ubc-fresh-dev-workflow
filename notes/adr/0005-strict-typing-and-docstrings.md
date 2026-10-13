# ADR 0005: Strict typing and numpy docstrings for every framework function

Status: accepted
Date: 2026-10-13
Issues: #14, #15

## Context

Agents write and repair code faster than people can review it. Untyped code hides its own
mistakes. A wrong argument type, a missing attribute, or a value that can be ``None`` is
found only when a test happens to exercise it, or when a user does. Coding agents repair
such errors by reading code, which is slow and error-prone.

## Decision

- Every function, method, and test in the framework is fully annotated. mypy runs in strict
  mode on the framework and on the tests.
- Every public function has a numpy-style docstring whose types match its annotations.
- The one approved exception is numpydoc, which ships no type markers. It is handled by a
  narrow override. Any new suppression needs a comment and a specific error code.

## Consequences

- Writing code takes more tokens and more time. The type checker repays that on every commit
  by finding mistakes before the tests do.
- Coding agents debug faster, because a type error names the call, the expected type, and the
  actual type.
- The annotations and docstrings are the source for the API reference (P0.8), so the
  documentation cannot drift from the types without a failing check.

## Alternatives considered

- Loose typing, with type checking only on public modules. Rejected: internal mistakes travel
  quietly into the public surface.
- Google-style docstrings. Rejected for now: numpy style matches the lab's other packages, and
  numpydoc validates it.
