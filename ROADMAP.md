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

Goal: make the repository a self-describing seed. The workflow is documented in an agent-friendly Sphinx site, a project seed and its validator exist, and a FRESH-style dev server guide is written. The repository is built with the pattern it describes.

- [ ] P0.1 Repository identity and governance files (#2)
  - [ ] LICENSE, CITATION.cff, CODE_OF_CONDUCT.md, CONTRIBUTING.md, and .gitignore
  - [ ] README.md with reading paths and the workflow picture
  - [ ] Control-character and public-safety rules in CONTRIBUTING.md
- [ ] P0.2 Agent operating contract and planning surfaces (#3)
  - [ ] AGENTS.md as a short root contract
  - [ ] ROADMAP.md and CHANGE_LOG.md
  - [ ] notes/ index, ADRs 0001 to 0004, and the pattern survey
- [ ] P0.3 Sphinx docs, RTFM index, and Pages workflow (#4)
  - [ ] docs/conf.py, index, llms.txt, and requirements
  - [ ] Guides and agent protocol pages
  - [ ] .github/workflows/docs.yml
- [ ] P0.4 Workflow reference contracts and issue templates (#5)
  - [ ] Workflow model, GitHub mapping, issue standard, git conventions, and approval gates
  - [ ] Phase and task issue templates
- [ ] P0.5 Seed templates, initializer, validator, and CI (#6)
  - [ ] templates/project seed
  - [ ] scripts/check_workflow.py and scripts/new_project.py
  - [ ] pytest suite and CI workflow
- [ ] P0.6 FRESH-style dev server guide (#7)
  - [ ] Host and containers, IDE and agents, and security and verification pages
- [ ] P0.7 Phase closeout and review handoff (#8)
  - [ ] Acceptance commands recorded in the changelog
  - [ ] Child issues closed with closeout comments
  - [ ] Pull request opened for maintainer review

Acceptance criteria:

- Bootstrap content reaches `main` only through the reviewed pull request.
- Ruff, pytest, the Sphinx build with `-W`, and the validator pass on the branch.
- The initializer renders a project that passes the validator and has no leftover placeholders.

Phase 0 verification:

- `python -m ruff check .`
- `python -m pytest`
- `sphinx-build -b html docs _build/html -W`
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

1. Finish P0. Close P0.1 to P0.6 with closeout comments, then close P0.7 by opening the pull request. The pull request is the review artifact.
2. After the maintainer merges P0: confirm the CI and docs workflows on `main`, enable GitHub Pages from the workflow (maintainer approval), and close #1.
3. Activate P1 only with maintainer approval. Then create its child issues as sub-issues of #9, and create `feature/p1-dogfood-validation` from `main`.
4. Open questions for the maintainer:
   - Should the seed also ship GitHub issue forms (YAML) next to the Markdown templates?
   - Should `new_project.py` create the GitHub repository itself? It does not today, because GitHub mutations need approval. A flag could add that later.
   - Should the seed carry the same MIT license as the lab's other public repositories? Assumed yes.
