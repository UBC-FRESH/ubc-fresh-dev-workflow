# UBC-FRESH Dev Workflow Roadmap

This roadmap is the plan of record and the issue tracker map for this repository. It is kept in step with the GitHub issues, `CHANGE_LOG.md`, and `notes/`. `scripts/check_workflow.py` parses the phase headers, status lines, and checkboxes below, so keep their format.

## Issue Tracker Map

| Phase | Parent issue | Branch | Status |
| --- | --- | --- | --- |
| P0 Bootstrap scaffold | #1 | `feature/p0-bootstrap-scaffold` | active |
| P1 Dogfood and validation | #9 | `feature/p1-dogfood-validation` | planned |
| P2 Dev server kit | #10 | `feature/p2-dev-server-kit` | planned |
| P3 Lifecycle playbooks and deployment | #11 | `feature/p3-lifecycle-playbooks` | planned |
| P4 v0.1.0 public release and onboarding | #12 | `feature/p4-v0.1.0-release` | planned |
| P5 Maintenance and feedback loop | #13 | `feature/p5-maintenance-loop` | planned |

## Lifecycle Map

Every project built from the seed moves through the same stages. This table shows where the repository's own phases sit in that lifecycle.

| Stage | Exit criteria | Phases |
| --- | --- | --- |
| Scope and design | Goal, scope, and out-of-scope items recorded; decisions in ADRs | P0 |
| Build | Tasks committed to the phase branch with task IDs; docs updated in the same change set | P0, P2 |
| Verify | Ruff, pytest, the docs build, and the validator pass; dogfood evidence recorded | P0, P1 |
| Release and deploy | Tag, release notes, Pages live, and a generated project verified from the template | P3, P4 |
| Operate and maintain | Review cadence held; incoming ideas triaged | P5 |
| Retire | Archive notice, final changelog entry, and issues closed | P5 (procedure) |

## Conventions

- A phase is `P<n>`. A task is `P<n>.<m>`. A subtask is a checklist item inside the task's issue body. Three levels at most.
- Status values are `planned`, `active`, `pr-open`, `complete`, and `deferred`.
- A phase becomes `active` only after its parent issue exists and the maintainer approves the activation.
- A phase becomes `complete` only after its pull request merges to `main` and its parent issue closes.
- A child issue closes after its work, checklist, and verification are complete, with a closeout comment.

## Phase 0: Bootstrap scaffold

Parent issue: #1
Branch: `feature/p0-bootstrap-scaffold`
Status: active

Goal: make the repository a self-describing seed. The workflow is documented in an agent-friendly Sphinx site. A project seed, a validator, and a green dashboard enforce it. Every commit must pass the full dashboard. The API is typed and documented, and the embedded capability pattern is specified. The repository is built with the pattern it describes.

- [x] P0.1 Repository identity and governance files (#2)
  - [x] LICENSE, CITATION.cff, CODE_OF_CONDUCT.md, CONTRIBUTING.md, and .gitignore
  - [x] README.md with reading paths and the workflow picture
  - [x] Control-character and public-safety rules in CONTRIBUTING.md
- [x] P0.2 Agent operating contract and planning surfaces (#3)
  - [x] AGENTS.md as a short root contract
  - [x] ROADMAP.md and CHANGE_LOG.md
  - [x] notes/ index, ADRs 0001 to 0004, and the pattern survey
- [x] P0.3 Sphinx docs, RTFM index, and Pages workflow (#4)
  - [x] docs/conf.py, index, llms.txt, and requirements
  - [x] Guides and agent protocol pages
  - [x] .github/workflows/docs.yml
- [x] P0.4 Workflow reference contracts and issue templates (#5)
  - [x] Workflow model, GitHub mapping, issue standard, git conventions, and approval gates
  - [x] Phase and task issue templates
- [x] P0.5 Seed templates, initializer, validator, and CI (#6)
  - [x] templates/project seed
  - [x] scripts/check_workflow.py and scripts/new_project.py
  - [x] pytest suite and CI workflow
- [x] P0.6 FRESH-style dev server guide (#7)
  - [x] Host and containers, IDE and agents, and security and verification pages
- [x] P0.7 Quality gates, strict typing, coverage, and the green dashboard (#14)
  - [x] Gate configuration in pyproject.toml, requirements-dev.txt, and .pre-commit-config.yaml
  - [x] Full annotations in scripts/ and tests/, passing mypy --strict
  - [x] Numpy-style docstrings for the framework scripts (the numpydoc validation test is P0.8)
  - [x] Hypothesis property tests for the roadmap grammar, and subprocess integration tests
  - [x] scripts/dashboard.py with typed pure functions, and an integration test per exit path
  - [x] CI quality matrix, dashboard summary job, and pre-commit parity job
  - [x] Policy pages, ADRs 0005 and 0006, AGENTS.md, CONTRIBUTING.md, and README badges
  - [x] Dashboard result recorded in the changelog
- [ ] P0.8 Typed API reference and docstring validation (#15)
  - [ ] Numpy-style docstrings for every public function in scripts/
  - [ ] tests/test_api_docstrings.py
  - [ ] docs/api pages with autodoc and napoleon, and a search index entry
- [ ] P0.9 Embedded capability pattern, documented with conformance checks (#16)
  - [ ] docs/agents/embedded-capabilities.rst with the contract and conformance checklist
  - [ ] ADR 0007, and links from the agents index and llms.txt
- [ ] P0.10 Phase closeout and review handoff (#8)
  - [ ] Acceptance commands and dashboard recorded in the changelog
  - [ ] Child issues closed with closeout comments
  - [ ] Pull request opened for maintainer review

Acceptance criteria:

- Bootstrap content reaches `main` only through the reviewed pull request.
- The full green dashboard passes on the branch: ruff lint and format, mypy in strict mode, pytest with the coverage gate, the docstring tests, the validator, the Sphinx build with `-W`, and the seed generation.
- `pre-commit run --all-files` passes.
- The initializer renders a project that passes the validator and its own gates.

Phase 0 verification:

- `python scripts/dashboard.py`
- `pre-commit run --all-files`
- `python scripts/check_workflow.py`
- `python scripts/new_project.py --name "Demo Project" --slug demo-project --dest tmp/demo-project`
- `python scripts/check_workflow.py tmp/demo-project`

## Phase 1: Dogfood and validation

Parent issue: #9
Branch: `feature/p1-dogfood-validation`
Status: planned

Goal: prove the seed works end to end on a throwaway project. Run the loop once, record every failure, and fix or file each one.

- [ ] P1.1 Generate and exercise the synthetic demo project
- [ ] P1.2 Fresh-clone rehearsal of this repository's checks
- [ ] P1.3 Friction log, fixes, and validator gap list

## Phase 2: Dev server kit

Parent issue: #10
Branch: `feature/p2-dev-server-kit`
Status: planned

Goal: turn the dev server guide into idempotent helper scripts with a dry-run mode, shellcheck-clean and tested in CI.

- [ ] P2.1 Host check script with a read-only mode
- [ ] P2.2 Base container provisioning with `--dry-run`
- [ ] P2.3 Per-project container script and workspace file generator
- [ ] P2.4 CI linting and a committed dry-run transcript

## Phase 3: Lifecycle playbooks and deployment

Parent issue: #11
Branch: `feature/p3-lifecycle-playbooks`
Status: planned

Goal: give each lifecycle stage an exit gate, and write the release, data-management, and agent-roles playbooks.

- [ ] P3.1 Lifecycle stage gates and exit criteria
- [ ] P3.2 Release and deployment playbook
- [ ] P3.3 Data management playbook
- [ ] P3.4 Agent roles and model routing playbook

## Phase 4: v0.1.0 public release and onboarding

Parent issue: #12
Branch: `feature/p4-v0.1.0-release`
Status: planned

Goal: publish v0.1.0 as a public template, with live docs and an onboarding path for collaborators.

- [ ] P4.1 Release candidate: versions, citation metadata, release notes
- [ ] P4.2 Pages enablement, live-site check, and template flag (maintainer action)
- [ ] P4.3 Tag, GitHub release, announcement, and onboarding feedback issue (maintainer action)

## Phase 5: Maintenance and feedback loop

Parent issue: #13
Branch: `feature/p5-maintenance-loop`
Status: planned

Goal: keep the seed current: triage incoming ideas, review it on a cadence, and version it for downstream projects.

- [ ] P5.1 Incoming-ideas queue and triage rule
- [ ] P5.2 Quarterly review checklist, exercised once
- [ ] P5.3 Seed versioning and migration policy

## Detailed Next Steps Notes

1. P0.7 is complete on the branch, and the full dashboard is green. Next comes P0.8 (the typed API reference and the numpydoc test), then P0.9 (the embedded capability pattern). Each one lands as its own commit, and each commit passes the full dashboard before the next one starts.
2. P0.10 closes the phase. It opens the pull request, which is the review artifact. The agent does not merge it.
3. After the maintainer merges P0: confirm the CI and docs workflows on `main`, enable GitHub Pages from the workflow (maintainer approval), require the CI checks in branch protection (maintainer approval; see `docs/reference/quality-gates.rst`), and close #1.
4. Activate P1 only with maintainer approval. Then create its child issues as sub-issues of #9, and create `feature/p1-dogfood-validation` from `main`.
5. Open questions for the maintainer:
   - Should the seed also ship GitHub issue forms (YAML) next to the Markdown templates?
   - Should `new_project.py` create the GitHub repository itself? It does not today, because GitHub mutations need approval. A flag could add that later.
   - Should the seed carry the same MIT license as the lab's other public repositories? Assumed yes.
   - Is a 90 percent branch-coverage gate the right starting point? The plan ratchets it to 95 percent in P1.
