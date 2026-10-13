# Change Log

Newest entries last. Each milestone gets a dated entry that matches the roadmap status and the GitHub issue comments.

## 2026-10-13

- Created the public repository `UBC-FRESH/ubc-fresh-dev-workflow` with an MIT license and a stub README on `main`.
- Surveyed public UBC-FRESH repositories for the workflow pattern: freshforge, femic, ws3, fhops, nemora, modelwright, agent-workbench, and fresh-agent-core. Sanitized findings are in `notes/reference/pattern-survey.md`.
- Wrote the bootstrap roadmap in `ROADMAP.md`: six phases (P0 to P5) across the project lifecycle, with the issue tracker map and a lifecycle map.
- Created parent issue #1 (P0), child issues #2 to #8 (P0.1 to P0.7) linked as sub-issues of #1, and parent issues #9 to #13 for planned phases P1 to P5. Planned phases get no child issues until they are activated.
- Opened `feature/p0-bootstrap-scaffold` for the bootstrap content. The content reaches `main` only through a pull request for maintainer review.
- Built the bootstrap content in six commits, one per task: `93d1d26` (P0.1), `d7f50b0` (P0.2), `d6106f6` and `d3d626e` (P0.3 and P0.4), `f2c4fbe` (P0.5), and `82f6e7a` (P0.6).
- Acceptance run on the branch: `python -m ruff check .` passed; `python -m pytest` passed 27 tests, including a self-check that the repository passes the validator; `sphinx-build -b html docs _build/html -W` passed; `python scripts/check_workflow.py` reported 0 errors and 0 warnings.
- Rendered a demo project with `python scripts/new_project.py --name "Demo Project" --slug demo-project --dest tmp/demo-project`. The validator on the output reported 0 errors and 3 expected warnings (missing LICENSE, CODE_OF_CONDUCT.md, and CITATION.cff). Its docs built with `-W`, and `llms.txt` landed at the site root.
- Fixed during the acceptance run, before the P0.5 commit: a fixture test that matched the validator's own source for placeholder syntax, long lines, and import order.
- P0.7 stays open until the pull request exists and the child issues are closed. Its final entries are recorded in the next commit.
- Reopened Phase 0 at the maintainer's request, before its pull request opened. P0.7 adds quality gates, strict typing, branch coverage, pre-commit, and the green dashboard. P0.8 adds a typed API reference with validated docstrings. P0.9 documents the embedded capability pattern. The closeout moved to P0.10 (#8), which now comes last. The earlier closeout record (`edcfd13`) is superseded.
- Created issues #14 (P0.7), #15 (P0.8), and #16 (P0.9) as sub-issues of #1. Renamed #8 to P0.10. Updated the body of #1, and posted a scope-change comment there.
- Cleared the push blocker: the GitHub token now includes the `workflow` scope, which the branch needs because it changes `.github/workflows/`.
- Recorded the reason in the parent issue: P0.1 to P0.6 did not meet the strict typing, docstring, or coverage gates that the template will require. Those gaps are now explicit work, and no commit reaches the pull request without meeting them.
- Completed the P0.7 work on the branch, in three commits. `9322fd8` added strict typing, numpy docstrings, property tests, and the coverage gate. `fedb131` added the green dashboard, the pre-commit hooks, the gate CI, and the shared framework files that every seed receives. The commit that records this entry adds the policy.
- Dashboard result for the policy commit, from `python scripts/dashboard.py`: lint, format, types, tests (with branch coverage of `scripts/` at 100 percent), validator, docs built with `-W`, seed generation, and the seeded project's own dashboard are all GREEN. Overall: GREEN.
- Recorded the policy in `AGENTS.md`, `CONTRIBUTING.md`, the seed contract (`templates/project/AGENTS.md.tmpl` and `CONTRIBUTING.md.tmpl`), the reference pages for quality gates, testing, and typing and docstrings, the green-dashboard agent page, and ADRs 0005 and 0006.
- Removed the seed's private copy of `requirements-dev.txt`. The framework files now come from one source, so a generated project cannot drift from the framework that it ships.
- Not done yet: the numpydoc docstring test and the typed API reference (P0.8), the embedded capability page (P0.9), branch protection (a maintainer action), and the first run of the CI jobs on GitHub, which happens when the pull request opens.
