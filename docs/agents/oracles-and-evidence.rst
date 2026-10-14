Oracles and evidence
====================

Evidence over trust
-------------------

Treat a prose report as untrusted until you have checked the state it describes.
Acceptable evidence includes:

- command output, with the command and its exit status;
- a diff, or a commit hash;
- a GitHub URL, or a read-back from ``gh issue view`` or ``gh pr view``;
- an inspected file, a rendered page, or a built artifact.

"Done" without evidence is a blocker, not a completion.

No oracle, no capability
------------------------

An agent-facing capability is a prompt, a validator, and a bounded retry budget.
The validator must check the output against real state: resolve the reference,
parse the file, or run the code. A validator that checks a model's output against
the same model, against a regular expression over its own text, or against a
mock proves nothing.

Write the validator first. If you cannot write one that can fail, you do not
have a capability. You have a plausible-sounding guess, and it will reach the
docs, the tests, and the code.

Validators in this repository
-----------------------------

``scripts/check_workflow.py`` is the oracle for the planning surfaces. Each
finding carries a stable code, listed here:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Code
     - Meaning
   * - ``FILE-MISSING``
     - A required governance or seed file is missing.
   * - ``ROADMAP-NO-PHASES``
     - ``ROADMAP.md`` has no ``## Phase <n>:`` headings.
   * - ``ROADMAP-PHASE-ORDER``
     - Phase numbers repeat or do not increase.
   * - ``ROADMAP-PHASE-META``
     - A phase lacks its ``Parent issue:``, ``Branch:``, or ``Status:`` line.
   * - ``ROADMAP-STATUS``
     - A status is not one of the five allowed values.
   * - ``ROADMAP-PARENT-REQUIRED``
     - A phase is active, pr-open, or complete, but its parent issue is ``TBD``.
   * - ``ROADMAP-TASK-ID``
     - A task ID does not match its phase, or repeats.
   * - ``ROADMAP-COMPLETE-OPEN``
     - A complete phase has an unchecked task or subtask.
   * - ``ROADMAP-TRACKER``
     - The Issue Tracker Map disagrees with a phase section, or a row is missing.
   * - ``CHANGELOG-DATE``
     - A changelog heading is not an ISO date.
   * - ``CHANGELOG-ORDER``
     - Changelog entries are not in date order.
   * - ``CHANGELOG-EMPTY``
     - The changelog has no dated entries.
   * - ``LINK-BROKEN``
     - A local Markdown link points to a file that does not exist.
   * - ``LLMS-BROKEN``
     - A link in ``docs/llms.txt`` has no matching page.
   * - ``CONTROL-CHAR``
     - A control character, or a carriage return, is in a scanned file.
   * - ``BOM``
     - A byte-order mark (U+FEFF) is in a scanned file.
   * - ``PATH-PERSONAL``
     - A personal home-directory path is in a scanned file.
   * - ``SECRET-SHAPED``
     - A string has the shape of a credential.
   * - ``ENCODING``
     - A file passed with ``--files`` is not valid UTF-8.
   * - ``PLACEHOLDER-LEFT``
     - Reported by ``new_project.py``: a placeholder survived rendering.

The validator scans the files that a commit would include. When the root is the top level of a
git repository, these are the tracked files and the untracked files that git does not ignore.
Otherwise, as in a generated project inside another repository, the validator walks the tree and
skips the paths that the root ``.gitignore`` ignores. Only the root ``.gitignore`` is read. An ignore line
the reader cannot apply is skipped, so the files that line would match are scanned. A negated
line the reader cannot apply re-includes every path, so no earlier rule hides a file that git
would include.

``FILE-RECOMMENDED`` is the one warning. It names recommended files that are
missing, such as a license. Warnings do not fail the run.

Run the validator before every push. CI runs it on every pull request.

Preserve uncertainty
--------------------

A result is only as strong as its inputs and checks. Say what you did not verify,
and why. If a check cannot run, report the exact command and its error.

Choose gates that measure the right thing
-----------------------------------------

A check should isolate the thing you care about. A test that passes only on
fixtures you wrote to pass proves little. Prefer a few high-signal checks that
would catch the defect you are actually worried about.
