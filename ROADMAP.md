# UBC-FRESH Dev Workflow Roadmap

This roadmap is the plan of record and the issue tracker map for this repository. It is kept in step with the GitHub issues, `CHANGE_LOG.md`, and `notes/`. `scripts/check_workflow.py` parses the phase headers, status lines, and checkboxes below, so keep their format.

## Issue Tracker Map

| Phase | Parent issue | Branch | Status |
| --- | --- | --- | --- |
| P0 Bootstrap scaffold | #1 | `feature/p0-bootstrap-scaffold` | complete |
| P1 Dogfood and validation | #9 | `feature/p1-dogfood-validation` | active |
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
- A phase becomes `active` only after its parent issue exists and the maintainer approves the activation. The approval comes in the close-out of the phase before it, or directly for the first phase.
- A phase becomes `complete` only after its pull request merges to `main` and its parent issue closes.
- A child issue closes after its work, checklist, and verification are complete, with a closeout comment.
- A phase ends with a close-out. The agent queues the pull request, writes the report in `notes/reports/`, and recommends the next actions. After the maintainer approves, the agent merges, closes the parent issue, deletes the branch, and launches the next phase. See `docs/reference/phase-closeout.rst`.

## Phase 0: Bootstrap scaffold

Parent issue: #1
Branch: `feature/p0-bootstrap-scaffold`
Status: complete

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
- [x] P0.8 Typed API reference and docstring validation (#15)
  - [x] Numpy-style docstrings for every public function in scripts/
  - [x] tests/test_api_docstrings.py
  - [x] docs/api pages with autodoc and napoleon, and a search index entry
- [x] P0.9 Embedded capability pattern, documented with conformance checks (#16)
  - [x] docs/agents/embedded-capabilities.rst with the contract and conformance checklist
  - [x] ADR 0007, and links from the agents index and llms.txt
- [x] P0.10 Phase closeout and review handoff (#8)
  - [x] Acceptance commands and dashboard recorded in the changelog
  - [x] Child issues closed with closeout comments
  - [x] Pull request opened for maintainer review
  - [x] Close-out report queued for approval (`notes/reports/p0-closeout.md`)

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
Status: active

Goal: prove the seed works end to end on a throwaway project. Run the loop once, record every failure, and fix or file each one.

- [x] P1.1 Generate and exercise the synthetic demo project (#18)
- [x] P1.2 Fresh-clone rehearsal of this repository's checks (#19)
- [x] P1.3 Friction log, fixes, and validator gap list (#20)
- [x] P1.4 Walk mode honors the root `.gitignore`, with a test (#21)
- [ ] P1.5 Coverage gate ratchet to 95 percent (#22)
- [ ] P1.6 Close-out rehearsal on the demo project (#23)

Acceptance criteria:

- The demo renders, its validator reports no errors, and its dashboard is green.
- A fresh clone of this repository passes the dashboard.
- The friction log lists every failure, and each entry names its fix, its deferred issue, or its accepted reason.
- Walk mode honors `.gitignore`, and the coverage gate is 95 percent.
- The demo's close-out report is queued and approved.

Phase 1 verification:

- `python scripts/new_project.py --name "Synthetic Demo" --slug synthetic-demo --dest tmp/synthetic-demo`
- `python scripts/check_workflow.py tmp/synthetic-demo`
- `python tmp/synthetic-demo/scripts/dashboard.py`
- `python scripts/dashboard.py`

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
- [ ] P4.2 Pages live-site check and template flag (approval required; Pages is enabled at the P0 close-out)
- [ ] P4.3 Tag, GitHub release, announcement, and onboarding feedback issue (approval required)

## Phase 5: Maintenance and feedback loop

Parent issue: #13
Branch: `feature/p5-maintenance-loop`
Status: planned

Goal: keep the seed current: triage incoming ideas, review it on a cadence, and version it for downstream projects.

- [ ] P5.1 Incoming-ideas queue and triage rule
- [ ] P5.2 Quarterly review checklist, exercised once
- [ ] P5.3 Seed versioning and migration policy

## Detailed Next Steps Notes

1. Phase 0 is complete. Pull request #17 merged as `2943d83`, GitHub Pages is live, branch protection requires the four CI checks on `main`, and #1 is closed.
2. Phase 1 is active. Its child tasks are #18 to #23, under the parent #9. P1.1 to P1.4 are complete. Their records are on #18 to #21. The findings deferred from the dogfood log are on #24, #25, and #26. P1.5, the coverage gate ratchet to 95 percent (#22), is next.
3. Phase 1 closes with its own close-out report, `notes/reports/p1-closeout.md`, queued in a pull request. The maintainer approves the report. Then the agent squash-merges the pull request, closes #9, and deletes the branch.
4. Recommended defaults, as approved with the Phase 0 close-out. The Phase 1 report can change them:
   - Seed issue forms (YAML) stay deferred. The default is Markdown templates, until the friction log shows the need.
   - `scripts/new_project.py` keeps writing local files only. Creating a repository stays a separate approved action.
   - The seed carries the MIT license.
   - The coverage gate is 90 percent through P0. P1.5 raises it to 95 percent.
