# Dogfood log, Phase 1

This log records what the first dogfood runs found: the synthetic demo project, its local rehearsal of the loop, and the fresh clone of this repository. Each entry gives the command, its exit status, the cause, and a disposition. A disposition is one of three: **fixed**, with its commit; **deferred**, with its issue; or **accepted**, with its reason. The step-by-step records of the runs are on #18 (P1.1), #19 (P1.2), and #23 (P1.6).

## Provenance

- Dates: 2026-10-13.
- Environment: Linux, Python 3.12.3, git 2.43.0. The dev tools in the fresh clone resolved to ruff 0.17.0, mypy 2.4.0, pytest 9.1.1, pytest-cov 7.1.0, coverage 7.16.2, hypothesis 6.169.0, numpydoc 1.11.0, Sphinx 9.1.0, pre-commit 4.7.0, and sphinx-rtd-theme 3.1.0.
- Sources: the demo at `tmp/synthetic-demo`, its P1.1 rehearsal remote at `tmp/synthetic-demo-origin.git`, its P1.6 stand-in remote at `tmp/p1-6-standin.git`, and the fresh clone at `tmp/fresh-clone`. All four are untracked.

## Entries

### F1. The seed's `.gitignore` does not ignore `.coverage`

- Found in: P1.1. The demo's first dashboard run wrote `.coverage`, and the status check after the initial commit listed it.
- Command: `git -C tmp/synthetic-demo status --short`, run after the initial commit. Exit status: 0.
- Output: `?? .coverage`.
- Cause: `templates/project/.gitignore` lacks the coverage and runtime entries that the root's `.gitignore` gained in P0.7 and P0.10. The seed template was not updated along with the root.
- Confirmed in: P1.2. A fresh clone of `main` finishes with a clean status, because the root's entries are present.
- Disposition: **fixed** in this phase. The fix is a separate commit, with a regression test, `test_generated_project_ignores_the_files_its_gates_write`. That test failed on the unfixed seed and passes on the fix. The changelog's P1.3 entry for the fix describes it.

### F2. The validator checks the form of the parent number, not that the issue exists

- Found in: P1.1, when the demo's Phase 0 was activated with the stand-in parent `#0`.
- Command: `.venv/bin/python tmp/synthetic-demo/scripts/check_workflow.py tmp/synthetic-demo`. Exit status: 0.
- Output: `0 error(s), 3 warning(s)`.
- Cause: the validator is stdlib-only and offline. It checks that the parent is `#` followed by digits, and it never asks GitHub whether the issue exists.
- Disposition: **accepted**. The validator stays offline by design, so that a fresh clone can run it before anything is installed. The read-only GitHub audit in the session protocol comes before any activation edit. Revisit this if a wrong parent number reaches `main`.

### F3. The seed's purpose placeholder survives a green run

- Found in: P1.1, in the same validator run as F2, before P0.2 in the demo.
- Command: the same validator command as F2. Exit status: 0.
- Output: `0 error(s), 3 warning(s)`, with the placeholder sentence still in `README.md`, `AGENTS.md`, and `docs/index.rst`.
- Cause: the validator has no check for the seed's placeholder text, so a placeholder can pass every gate.
- Disposition: **deferred**. A placeholder check is a validator change, so it needs a changelog entry and tests when it lands.
- Issue: #24, filed in P1.3.

### F4. The seed's Phase 0 cannot be finished locally

- Found in: P1.1, during activation.
- Command: a read of `tmp/synthetic-demo/ROADMAP.md`, line 43. Exit status: not applicable, because it was a file read.
- Output: `- [ ] P0.1 Create the GitHub repository and push the rendered seed`.
- Cause: the seed's Phase 0 mixes local steps with a GitHub step. A local rehearsal cannot tick P0.1. The rehearsal used a local bare remote in its place, and the demo's changelog records that substitution.
- Disposition: **deferred**. Separating the local steps from the GitHub steps changes the seed's contract, so it needs an ADR before any change.
- Issue: #25, filed in P1.3.

### F5. The demo's dashboard runs six gates, not eight

- Found in: P1.1, the demo's first dashboard run.
- Command: `.venv/bin/python tmp/synthetic-demo/scripts/dashboard.py`. Exit status: 0.
- Output: `OVERALL: GREEN. Every gate passed.` over six gates: lint, format, types, tests, validator, and docs.
- Cause: the seed gates run only where `scripts/new_project.py` exists, and the generator is not shipped into projects.
- Disposition: **accepted**, by design. The root repository's seed gates cover the generator.

### F6. The three recommended warnings are expected

- Found in: P1.1, in the same validator run as F2 and F3.
- Command: the same validator command as F2. Exit status: 0.
- Output: three warnings: LICENSE, CODE_OF_CONDUCT.md, and CITATION.cff.
- Cause: the seed does not ship those files, and the first-project guide says the seed does not choose a license.
- Disposition: **accepted**. The warnings are recommendations, and they are not errors.

### F7. The development tools are floor-pinned

- Found in: P1.2, the fresh install of the dev requirements.
- Command: `tmp/fresh-clone/.venv/bin/python -m pip install -r tmp/fresh-clone/requirements-dev.txt`. Exit status: 0.
- Output: the newest releases on the day, listed under Provenance.
- Cause: `requirements-dev.txt` sets floors, such as `ruff>=0.6`, so a fresh install takes the newest release available. The working tree and the clone happen to match today.
- Disposition: **deferred**. Choosing a constraints file or exact pins changes how the project is reproduced, so it needs an ADR before any change.
- Issue: #26, filed in P1.3.

### F8. The pre-commit hooks run in whichever Python the shell resolves

- Found in: P1.5, at the pre-commit run before the commit.
- Command: `.venv/bin/pre-commit run --all-files`, run from a shell without `.venv/bin` on `PATH`. Exit status: non-zero.
- Output: `ModuleNotFoundError: No module named 'numpydoc'` while collecting `tests/test_api_docstrings.py`, and `No module named 'hypothesis'` in `tests/test_properties.py`. The traceback names the system Python.
- Cause: the hooks use `language: system` and call `python` from `PATH`. A shell without the venv active resolves the system Python, which lacks the dev tools. The setup steps activate the venv, but they do not say that a commit must run from the activated shell.
- Disposition: **fixed** in `14f9cd2`, which adds the note to the setup steps in `CONTRIBUTING.md` and its seed template. The hook design is unchanged.

### F9. The seed's roadmap has no acceptance criteria for its phases

- Found in: P1.6, while the demo's close-out report was written from the seed template.
- Command: a read of `templates/project/ROADMAP.md.tmpl`, and of the close-out template that the demo received, `notes/reports/phase-closeout-template.md`. Exit status: not applicable, because these were file reads.
- Output: each phase in the roadmap template has a goal and a task list, and no acceptance criteria. The close-out contract in `docs/reference/phase-closeout.rst` asks each report for each acceptance criterion from the roadmap.
- Cause: this repository's roadmap gives each phase an `Acceptance criteria:` block, but the seed's roadmap template does not, so a project's close-out has no criteria to cite.
- Disposition: **deferred**. The wording of the block is a maintainer decision, and the template change needs tests.
- Issue: #27, filed in P1.6.

### F10. Generated projects keep the files they were generated with

- Found in: P1.6, in the demo's working tree and its coverage settings.
- Command: `git -C tmp/synthetic-demo status --short`, and `grep -n "cov-fail-under" tmp/synthetic-demo/pyproject.toml`. Exit status: 0 for both.
- Output: `?? .coverage`, and an `addopts` line that ends in `--cov-fail-under=90`.
- Cause: the demo was generated before `928223e`, which fixed the seed's ignore file, and before P1.5, which raised the gate to 95 percent. A generated project keeps the files it was generated with, and the seed does not update them.
- Disposition: **accepted**. Each project owns its generated files. A rule for updating them after generation is the migration question in P5.3. The demo's commits name their paths, so `.coverage` stays out of them.

## Validator gaps

| Gap | Source | Disposition |
| --- | --- | --- |
| V1. The existence of the parent issue is not checked. | F2 | accepted |
| V2. The seed's placeholder text is not flagged. | F3 | deferred, #24 |
| V3. Walk mode does not read the root `.gitignore`. An ignored binary file is skipped only because it is not UTF-8. | Known risk from the P0 close-out | fixed in P1.4, #21 |

## Open items

None. Every entry has a disposition. F1 is fixed in `928223e`, and F8 in `14f9cd2`. F2, F5, F6, and F10 are accepted. F3, F4, F7, and F9 are deferred to #24, #25, #26, and #27.
