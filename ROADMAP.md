# UBC-FRESH Dev Workflow Roadmap

This roadmap is the plan of record and the issue tracker map for this repository. It is kept in step with the GitHub issues, `CHANGE_LOG.md`, and `notes/`. `scripts/check_workflow.py` parses the phase headers, status lines, and checkboxes below, so keep their format.

## Issue Tracker Map

| Phase | Parent issue | Branch | Status |
| --- | --- | --- | --- |
| P0 Bootstrap scaffold | #1 | `feature/p0-bootstrap-scaffold` | complete |
| P1 Dogfood and validation | #9 | `feature/p1-dogfood-validation` | complete |
| P2 Dev server kit | #10 | `feature/p2-dev-server-kit` | complete |
| P3 Lifecycle playbooks and deployment | #11 | `feature/p3-lifecycle-playbooks` | active |
| P4 v0.1.0 public release and onboarding | #12 | `feature/p4-v0.1.0-release` | planned |
| P5 Maintenance and feedback loop | #13 | `feature/p5-maintenance-loop` | planned |

## Lifecycle Map

Every project built from the seed moves through the same stages. The gate of each stage is defined in `docs/reference/lifecycle.rst`. This table shows where the repository's own phases sit in that lifecycle.

| Stage | Phases |
| --- | --- |
| Scope and design | P0 |
| Build | P0, P2 |
| Verify | P0, P1 |
| Release and deploy | P3, P4 |
| Operate and maintain | P5 |
| Retire | P5 (procedure) |

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
Status: complete

Goal: prove the seed works end to end on a throwaway project. Run the loop once, record every failure, and fix or file each one.

- [x] P1.1 Generate and exercise the synthetic demo project (#18)
- [x] P1.2 Fresh-clone rehearsal of this repository's checks (#19)
- [x] P1.3 Friction log, fixes, and validator gap list (#20)
- [x] P1.4 Walk mode honors the root `.gitignore`, with a test (#21)
- [x] P1.5 Coverage gate ratchet to 95 percent (#22)
- [x] P1.6 Close-out rehearsal on the demo project (#23)

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
Status: complete

Goal: turn the dev server guide into idempotent helper scripts with a dry-run mode, shellcheck-clean and tested in CI.

- [x] P2.1 Host check script with a read-only mode (#29)
- [x] P2.2 Base container provisioning with `--dry-run` (#30)
- [x] P2.3 Per-project container script and workspace file generator (#31)
- [x] P2.4 CI linting and a committed dry-run transcript, with the runner pin (#32)

Acceptance criteria, as approved at the Phase 1 close-out on 2026-10-14:

- Each script has a read-only or `--dry-run` mode, and a test shows that the mode changes nothing on the host where it runs.
- `shellcheck` passes on every script in CI.
- The committed dry-run transcript matches the scripts' dry-run output, and a test checks it.
- The dev server guide links to each script, and the docs build passes with `-W`.

## Phase 3: Lifecycle playbooks and deployment

Parent issue: #11
Branch: `feature/p3-lifecycle-playbooks`
Status: active

Goal: give each lifecycle stage an exit gate, and write the release, data-management, and agent-roles playbooks.

- [x] P3.1 Lifecycle stage gates and exit criteria (#34)
- [x] P3.2 Release and deployment playbook (#35)
- [x] P3.3 Data management playbook (#36)
- [ ] P3.4 Agent roles and model routing playbook (#37)

Acceptance criteria, as approved at the Phase 2 close-out on 2026-10-14:

- Each lifecycle stage has entry criteria, exit criteria, and a named gate owner.
- The release playbook has been dry-run on the demo project from P1.

Phase 3 verification:

- `sphinx-build -b html docs _build/html -W`
- `python scripts/check_workflow.py`

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
2. Phase 1 is complete. Pull request #28 merged as `8f063fb`, and #9 is closed. P1.1 to P1.6 are complete, and their records are on #18 to #23. The findings deferred from the dogfood log are on #24, #25, #26, and #27, with the decisions in item 5.
3. Phase 2 is complete. Pull request #33 merged as `f998cd8`, and #10 is closed. Its child tasks are P2.1 to P2.4, on #29 to #32, linked as sub-issues of #10. The close-out report is `notes/reports/p2-closeout.md`, and the maintainer approved its four items on 2026-10-14. The local branch `feature/p2-dev-server-kit` stays until its deletion is approved.
4. Recommended defaults, as approved with the Phase 0 close-out. The Phase 1 report can change them:
   - Seed issue forms (YAML) stay deferred. The default is Markdown templates, until the friction log shows the need.
   - `scripts/new_project.py` keeps writing local files only. Creating a repository stays a separate approved action.
   - The root repository is MIT. The seed ships no license file, and the first-project guide leaves the choice to the project (F6).
   - The coverage gate is 90 percent through P0. P1.5 raised it to 95 percent.
5. Decisions recorded at the Phase 1 close-out, approved on 2026-10-14:
   - F3, #24: the validator's placeholder check stays deferred, and the P5.2 quarterly review considers it.
   - F4, #25: Option A in `notes/adr/0009-phase-0-local-repository-at-activation.md`, accepted on 2026-10-14. The seed's Phase 0 change lands under P3.1 (#34).
   - F7, #26: the dev-tool pins are decided with P5.3, the seed versioning and migration policy.
   - F9, #27: the acceptance criteria for the seed's roadmap template fold into P3.1.
   - CI runner: done in P2.4, on the phase branch, before the phase pull request opens. That pull request's CI runs on the pinned runner, so no separate pull request is needed.
6. Phase 3 is active. Its parent is #11, and it was launched from `f998cd8` on `feature/p3-lifecycle-playbooks`. Its child tasks are P3.1 to P3.4, on #34 to #37, linked as sub-issues of #11. P3.1 to P3.3 are complete. P3.4 starts in a later move, with `docs/agents/roles-and-models.rst`.
7. Decisions recorded at the Phase 2 close-out, approved on 2026-10-14:
   - Lifecycle stages: the six stages named in #11. The maintainer owns every gate, and the agent prepares the evidence.
   - Tags, releases, and Pages: none in Phase 3. The release playbook names their commands, and each one waits for its own approval.
   - PyPI trusted publishing: documented, not configured. This repository is a template, and no package exists.
   - Data management: private vaults, DataLad and git-annex, and sanitized artifacts. Raw transcripts stay local.
   - Model routing: model choices are configuration. Each one is recorded with its evidence, and each one is re-checked at the P5.2 review.
   - Snap channel: the dev server guide names `latest/stable`, the channel that `server/host-check.sh` expects.
