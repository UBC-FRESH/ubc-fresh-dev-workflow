Embedded capabilities
=====================

.. note::

   Status: experimental. This page states a contract that the FRESH modelling packages are being
   checked against. It does not claim that every package conforms yet.

Some scientific and engineering packages are complicated enough that a coding agent which reads
the documentation once will make mistakes. The mistakes are usually plausible: an argument in the
wrong units, a method that exists in a different version, or a selection that matches nothing. An
*embedded capability* is a narrow operation that a package ships for agents. It runs inside the
package, and it checks its own answer against the package's real state before that answer reaches
the caller.

When the pattern applies
------------------------

Use an embedded capability when all of these hold:

- The task has a precise, checkable answer. Examples are a selection expression that resolves to at
  least one object, an import that succeeds after a suggested fix, or a symbol that an error message
  cites.
- A wrong answer is expensive, and reading the documentation does not prevent it.
- The package can check the answer against its own state, without asking another model.

Do not use the pattern for open-ended design work. There, an agent works well with the
documentation and a reviewer, and a capability adds nothing that a validator can check.

The contract
------------

A capability is a prompt, a validator, and a bounded retry budget. Each part has its own rules.

Name and version
   A stable name, such as ``build_mask``, and a version. A change to the input type, the output
   type, or the validation rule is a new version. The old version stays available until its
   deprecation window ends.

Typed input and output
   The input and the output are annotated types, and mypy checks them in the package that ships the
   capability. Callers pass the package's real objects as context, such as a model instance, rather
   than a description of them.

Validator over real state
   The validator is a function from a proposal and its context to a verdict. It reads the package's
   state and runs no model. It must be able to fail, and its tests show that it does.

Bounded retries
   A rejected proposal goes back to the model with the reasons for the rejection. The number of
   attempts is fixed in advance. When the budget runs out, the capability stops.

Advisory output only
   The capability returns a proposal. It never mutates the caller's state. Applying a proposal is the
   caller's decision.

Explicit failure
   A result is either ``ok`` with a validated value, or not ``ok`` with the accumulated errors. A
   capability never returns a best guess, and a rejected proposal is not an exception.

Provenance
   Every attempt is recorded: the model identifier, a hash of the prompt, the raw output, the verdict,
   and the attempt number. Secrets are redacted before anything is written.

The runtime that implements this contract is ``fresh-agent-core``, a public UBC-FRESH package.
Packages consume it. This template does not ship a runtime.

Testing requirements
--------------------

- Every capability has offline tests that use a fake provider. The fake returns scripted proposals,
  so the tests need no network and no model.
- The offline tests cover four cases: a correct proposal is accepted; a wrong proposal is rejected,
  with a reason; a budget that runs out returns a result that is not ``ok``; and every attempt is
  recorded in the provenance.
- A live smoke test may exist. It is opt-in, selected by an environment variable, documented, and
  never required by CI.
- The validator has unit tests of its own, with inputs that it must reject.

Governance
----------

- Each capability appears in the package's API reference, with its version and its validation rule.
- The documentation states what the validator checks, and what it does not check.
- A capability whose validator cannot fail is not a capability. Remove it, or fix the validator
  before the capability ships.
- Changes to the contract are recorded in the changelog and in an ADR.

Conformance checklist
---------------------

A package that adopts the pattern can copy this list into its own documentation. For each item, it
links to the code or the test that shows the item holds.

- [ ] The capability has a stable name and a version.
- [ ] The input and the output are annotated, and mypy --strict passes on the module.
- [ ] The validator reads real package state, and it does not call a model.
- [ ] A test shows that the validator rejects a wrong proposal.
- [ ] The retry budget is fixed, and a test shows that it stops.
- [ ] Failure returns a result that is not ``ok``, with the errors, and it does not guess.
- [ ] Every attempt is recorded, and secrets are redacted.
- [ ] The offline tests use a fake provider, so CI needs no network and no model.
- [ ] The capability is in the API reference, and the docs say what is and is not validated.

Examples in public packages
---------------------------

- ``ws3`` ships a capability surface whose operations validate their output against the live model.
  Its agent guide states the rule "no oracle, no capability", and it records the fabricated APIs
  that reached its documentation, tests, and code before a validator existed.
- ``fhops`` plans a capability surface on the same runtime. Its planned validators check that every
  symbol a capability cites exists in the installed package.
- ``fresh-agent-core`` is the shared runtime. It provides the capability contract, the retry loop,
  the provenance record, and a fake provider for offline tests.

Relation to RTFM
----------------

Reading the documentation is still required, and a capability does not replace it. A capability
answers the narrow question that the documentation cannot check. The documentation explains the rest.
See :doc:`rtfm`.
