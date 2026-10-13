# P0 close-out report: Bootstrap scaffold

Phase: P0, Bootstrap scaffold
Parent issue: #1, open until the pull request merges
Pull request: #17, `feature/p0-bootstrap-scaffold` into `main`
Evidence head: `2cf80b9`. CI run 38455561379 is green in all four jobs on this head.
Report commit: the commit that adds this file. Its CI run is posted on PR #17 and on #1.
Date: 2026-10-13
Status: queued for approval. Not merged.

## Recommendation

Approval is requested for items 1 to 5. Items 2 and 3 are settings changes, so each can be approved or declined on its own. The agent carries out the approved items in this order, and reads back each result.

1. Squash-merge PR #17 once CI is green on the report commit, and delete the branch on the remote and locally.

   ```bash
   gh pr merge 17 -R UBC-FRESH/ubc-fresh-dev-workflow --squash --delete-branch
   ```

2. Enable GitHub Pages from the GitHub Actions source, so that `.github/workflows/docs.yml` publishes the site on each push to `main`. Read back the first `Docs` run on `main`, and the live site address.

   ```bash
   gh api -X POST repos/UBC-FRESH/ubc-fresh-dev-workflow/pages -f build_type=workflow
   ```

3. Require the four CI checks on `main`, and block force pushes and branch deletion. No approving review is required. The phase pull requests are opened from the maintainer's account, and GitHub does not let an author approve their own pull request, so the maintainer's approval of this report is the review. `docs/reference/quality-gates.rst` holds the same command.

   ```bash
   gh api -X PUT repos/UBC-FRESH/ubc-fresh-dev-workflow/branches/main/protection --input - <<'JSON'
   {
     "required_status_checks": {
       "strict": true,
       "contexts": [
         "Quality gates, Python 3.11",
         "Quality gates, Python 3.12",
         "Green dashboard summary",
         "Pre-commit parity"
       ]
     },
     "enforce_admins": false,
     "required_pull_request_reviews": null,
     "restrictions": null,
     "allow_force_pushes": false,
     "allow_deletions": false
   }
   JSON
   ```

4. Post a closeout comment on #1 that cites the merge commit, and close #1.

5. Launch Phase 1, Dogfood and validation, as section 6 proposes. Create `feature/p1-dogfood-validation` from the merged `main`. In its first commit, set P0 to `complete` and P1 to `active` in `ROADMAP.md` and in the tracker map. Create P1.1 to P1.6 as sub-issues of #9, and start P1.1.

## 1. Objectives and acceptance

| Criterion | Evidence | Status |
| --- | --- | --- |
| Bootstrap content reaches `main` only through the reviewed pull request. | PR #17 is the only route. `main` holds one earlier commit, `e749b6a`, from repository creation (deviation 9). The merge waits for item 1. | Not yet met: pending item 1 |
| The full green dashboard passes on the branch: lint and format, strict types, tests with the coverage gate, docstring tests, the validator, the Sphinx build with `-W`, and seed generation. | Sweep: the dashboard is GREEN at `2cf80b9`, with 146 tests and 100 percent branch coverage of `scripts/`. CI run 38455561379 is green in all four jobs. The working tree of this commit is recorded in the CHANGE_LOG entry. | Met |
| `pre-commit run --all-files` passes. | The working tree of this commit is recorded in the CHANGE_LOG entry. CI job "Pre-commit parity" is green in run 38455561379. | Met |
| The initializer renders a project that passes the validator and its own gates. | Sweep at `2cf80b9`: the seed and seeded-dashboard gates are green. The Phase 0 demo command rendered and validated a project (CHANGE_LOG entry). The roadmap names `tmp/demo-project`, which already held output, so the run used `tmp/p0-verify-demo` with the same arguments (deviation 12). | Met |
| The docs publish to GitHub Pages (P0.3, and the original requirement). | The docs workflow builds with `-W` in the dashboard, and it is green. Pages is not enabled: `gh api repos/UBC-FRESH/ubc-fresh-dev-workflow/pages` returns 404. | Met with a stated limit: publication waits for item 2 |

## 2. Workflow compliance

- **Parent before branch.** #1 was created at 2026-10-13T18:39:45Z. The first phase commit, `93d1d26`, was made at 18:45:48 +0000. Met.
- **Child issues before work.** #2 to #8 were created at 18:39:47 to 18:39:57Z, before the first commit. #14 to #16 were created at 19:06:39 to 19:06:42Z, before their commits: `9322fd8` at 19:12:24, `721c10c` at 19:18:50, and `5f6a4b1` at 19:20:12. Met.
- **Sub-issue links.** `gh api repos/UBC-FRESH/ubc-fresh-dev-workflow/issues/1/sub_issues` lists 2, 3, 4, 5, 6, 7, 8, 14, 15, and 16. Met.
- **Branch from `main`.** The merge-base is `e749b6a`, which is the only commit on `main`. Met.
- **Commit messages start with task IDs.** 17 of 17 commits do. Met.
- **Roadmap and changelog in step with the tasks.** 10 of 17 commits changed `ROADMAP.md` or `CHANGE_LOG.md`. The other seven are `93d1d26`, `d6106f6`, `d3d626e`, `f2c4fbe`, `82f6e7a`, `9322fd8`, and `fedb131`. Partly met (deviation 3).
- **Gates for each commit.** Section 3. Partly met (deviations 1 and 2).
- **Child issues closed with closeout evidence.** #2 to #7 closed at 19:21:21 to 19:21:50Z. #14, #15, and #16 closed at 19:17:22, 19:19:08, and 19:20:29Z. #8 closed at 19:33:10Z. Each has one closeout comment that names its commits. Met, with deviations 4 and 5.
- **Progress comments at milestones.** The child issues have only their closeout comments. #1 has two comments: the scope change, and the progress comment that opened the pull request. Not met (deviation 4).
- **Approval gates respected.** The repository, the phase plan, and issues #1 to #13 were created under the maintainer's initial request, which asked for a public repository and the phase plan. Issues #14 to #16 were created under the maintainer's new requirements. The maintainer added the `workflow` token scope, so the branch could push workflow files. Pull request #17 was opened from the phase branch, which the rules allow. This phase did not merge anything, delete a branch, change a setting, create a tag or release, create an external account, or change visibility. Met.

## 3. Gate evidence

**Method.** Each of the 17 phase commits was checked out in a temporary worktree. The checks that the commit itself defines were run with this repository's virtual environment. Where a commit had `scripts/dashboard.py`, the dashboard ran. Otherwise the validator, the tests, ruff, mypy, and the Sphinx build ran, each where the commit has the file it needs: `scripts/check_workflow.py` for the validator, `tests/` for the tests, `pyproject.toml` for ruff and mypy, and `docs/conf.py` for Sphinx. The `pyproject.toml` at `f2c4fbe` has no mypy section, so mypy had nothing to check there and exited with status 2 on the commits before `9322fd8`. Those are not gate results, and they are not counted as red. The worktrees were removed afterward.

| Commit | Task | Gates the commit defines | Result |
| --- | --- | --- | --- |
| `93d1d26` | P0.1 | none | No executable gate existed. |
| `d7f50b0` | P0.2 | none | No executable gate existed. |
| `d6106f6` | P0.3 | docs (`-W`) | Red: links to reference and dev-server pages that later tasks wrote (deviation 1). |
| `d3d626e` | P0.4 | docs (`-W`) | Red: links to dev-server pages that a later task wrote (deviation 1). |
| `f2c4fbe` | P0.5 | validator, tests, ruff, docs (`-W`) | Red: validator reports two errors, the self-check test fails, and the docs build fails (deviation 1). |
| `82f6e7a` | P0.6 | validator, tests, ruff, docs (`-W`) | Green. The dev-server pages arrive here. |
| `edcfd13` | P0.7 closeout (superseded) | validator, tests, ruff, docs (`-W`) | Green. |
| `6eccd65` | P0.7 reopen | validator, tests, ruff, docs (`-W`) | Green. |
| `9322fd8` | P0.7 typing | validator, tests, ruff, mypy `--strict`, docs (`-W`) | Green. |
| `fedb131` | P0.7 dashboard | full dashboard | Green: 107 tests, 100 percent. |
| `8c1f7a5` | P0.7 policy | full dashboard | Green: 107 tests, 100 percent. |
| `721c10c` | P0.8 | full dashboard | Green: 140 tests, 100 percent. |
| `5f6a4b1` | P0.9 | full dashboard | Green: 140 tests, 100 percent. |
| `6d1f944` | P0.10 | full dashboard | Green in the sweep. Red in CI run 38454397011 (deviation 8). |
| `12e275e` | P0.10 | full dashboard | Green in the sweep: 145 tests. Red in CI run 38454938913 (deviation 8). |
| `0d0233b` | P0.10 | full dashboard | Green in the sweep: 146 tests. Green in CI run 38455220766. |
| `2cf80b9` | P0.10 | full dashboard | Green in the sweep: 146 tests, 100 percent. Green in CI run 38455561379. |

**Working tree of this commit.** The dashboard, pre-commit, the validator, and the Phase 0 demo command were run on the working tree that this commit contains. Their results are recorded in the CHANGE_LOG entry dated 2026-10-13 that this commit adds.

## 4. CI evidence

Jobs: "Quality gates, Python 3.11", "Quality gates, Python 3.12", "Green dashboard summary", and "Pre-commit parity".

| Run ID | Head | Conclusion | Notes |
| --- | --- | --- | --- |
| 38454397011 | `6d1f944` | Failure in all four jobs | The validator scanned an ignored Hypothesis cache that held runner paths (deviation 8). |
| 38454938913 | `12e275e` | Failure in both quality jobs and the dashboard; pre-commit passed | The validator walked the generated project's own cache (deviation 8). |
| 38455220766 | `0d0233b` | Success in all four jobs | The first green head after the fix. |
| 38455561379 | `2cf80b9` | Success in all four jobs | The evidence head. |
| Posted on PR #17 | Report commit | See the PR comment | The run for the commit that adds this report. |

## 5. Deviations

| # | Deviation | Cause | Remedy |
| --- | --- | --- | --- |
| 1 | The docs build with `-W` was red at `d6106f6`, `d3d626e`, and `f2c4fbe`. At `f2c4fbe` the validator and the self-check test were also red. | The docs and the README linked to pages that were written later. The reference pages arrived in `d3d626e`, and the dev-server guide arrived in `82f6e7a`. | Fixed in `82f6e7a`, the first commit where validator, tests, and docs all pass. The history is kept. Section 3 shows each state. |
| 2 | The first executable checks arrived late. Commits `93d1d26` and `d7f50b0` had none. The validator, the tests, and the ruff configuration arrived in `f2c4fbe` (P0.5). The strict type gate arrived in `9322fd8` (P0.7). | The work started before the gates existed. | From `82f6e7a` on, every commit is green in the sweep under the gates of its time. From `fedb131` on, every commit is green under the full dashboard. |
| 3 | Seven of the 17 commits did not change the roadmap or the changelog. The checkboxes for P0.1 to P0.6 were ticked in `edcfd13`, a closeout that was later superseded. | Roadmap and changelog updates were batched. | The roadmap and the changelog describe the state at the head. This lag stays recorded here. |
| 4 | Progress comments were not posted during the work. The closeouts for P0.1 to P0.6 were posted together at 19:21Z, after the phase had moved to `5f6a4b1`. They cite the dashboard at that head, not evidence from each task's commit. | The closeouts were written at closure, not as each task finished. | From P1 on, each task completion gets a progress comment on its child issue and on the parent. Closeouts state their verification scope. |
| 5 | #8 (P0.10) was closed at 19:33Z, before this report existed. | The close-out report was not part of the task as first written. | This report is the handoff. #8 stays closed. Its body and a comment link to the report. |
| 6 | Some workflow pages, and the first pull request body, said that agents never merge and that the maintainer merges and closes. | The first approval-gates text left out the close-out step, and the maintainer corrected it. | Corrected in this commit: `AGENTS.md`, the seed contract, the approval-gates, git, GitHub-mapping, quality-gates, session, and first-project pages, and ADR 0008. ADR 0004 is marked as refined. |
| 7 | The dev-server guide said its commands came from the upstream LXD documentation. Only the installation steps were checked. | The claim was broader than the check. | Narrowed in `6d1f944`. The P0.6 closeout states the verification scope. |
| 8 | CI failed on `6d1f944` in all four jobs, and on `12e275e` in three of them. The validator read ignored caches that hold machine paths. Local runs passed, because the local cache paths did not match the personal-path rule. | The validator read the working tree, not the set of files that a commit would include. It also walked the generated project's cache. | Fixed in `12e275e` and `0d0233b`. The validator scans what git would commit, and walked trees skip generated caches. Six tests cover the cases: five in `12e275e` and one in `0d0233b`. CI is green on `0d0233b` and `2cf80b9`. A sweep under `/tmp` cannot reproduce the runner's paths, so the CI runs are the evidence for those heads. |
| 9 | `main` holds one earlier commit, `e749b6a`, from 18:37:44Z. It contains `LICENSE` and a placeholder `README.md`. | It was pushed directly when the repository was created, before the workflow existed. | None needed. It holds no phase content. Disclosed for the record. |
| 10 | P0 was reopened from `pr-open` to `active` at the maintainer's new requirements. P0.7 to P0.9 were added, and the closeout moved to P0.10. | Scope change. | Recorded in `CHANGE_LOG.md` at `6eccd65`, and on #1. The superseded closeout, `edcfd13`, is marked as superseded. |
| 11 | The P0 objective to publish the docs to GitHub Pages is not live. Pages returns 404, and branch protection returns "Branch not protected". | Those settings have not been changed. | Items 2 and 3 of the recommendation. |
| 12 | The roadmap's verification command names `tmp/demo-project`, which already held output from an earlier run. The initializer refuses a non-empty destination. | The earlier output was not removed. | The run used `tmp/p0-verify-demo` with the same arguments. Section 3 and the CHANGE_LOG entry record the result. |

**Known risks, not yet deviations.**

- The validator's walk mode does not read the root `.gitignore`. The seeded `.coverage` file is skipped only because it is binary and fails the UTF-8 check. A binary file that decodes as UTF-8 would be scanned. P1.4 closes this.
- The embedded capability page is experimental. Its examples come from public documentation. Nothing in this phase checked them against the packages' code.

## 6. Next phase: Phase 1, Dogfood and validation (proposed)

**Goal** (from `ROADMAP.md`): prove the seed works end to end on a throwaway project. Run the loop once, record every failure, and fix or file each one.

**Tasks.** P1.1 to P1.3 are in the roadmap already. P1.4 to P1.6 are proposed here.

- P1.1 Generate and exercise the synthetic demo project. It stays local, so no external repository is created.
- P1.2 Fresh-clone rehearsal of this repository's checks. It reads the public repository only.
- P1.3 Friction log, fixes, and validator gap list.
- P1.4 Walk mode honors the root `.gitignore`, with a test. This closes the risk in section 5.
- P1.5 Coverage gate ratchet to 95 percent, recorded as a gate change with its reason.
- P1.6 Close-out rehearsal on the demo project: the report from the seed template, the approval, and the execution. This exercises the contract once before the P5 review.

**Acceptance criteria** (proposed):

- The demo renders, passes its own validator, and has a green dashboard.
- A fresh clone of this repository passes the dashboard.
- The friction log lists every failure, and each entry names its fix or its filed issue.
- Walk mode honors `.gitignore`, and the coverage gate is 95 percent.
- The demo's close-out report is queued and approved.

**Child issues and branch.** Branch `feature/p1-dogfood-validation`. The parent is #9. P1.1 to P1.6 are created as its sub-issues when Phase 1 launches.

**Approvals needed for Phase 1.** None beyond this package. Phase 1 creates no external repository, account, or setting.

**Recommended defaults for the open choices.** Each one can be changed when you approve.

- Seed issue forms (YAML): Markdown templates only. Revisit after the P1.3 friction log.
- `scripts/new_project.py` writes local files only. Creating a repository stays a separate approved action.
- License: MIT, as the lab's other public repositories use.
- Coverage: 90 percent through P0, and 95 percent after P1.5.

## 7. Decision

- [ ] Approve items 1 to 5 as written.
- [ ] Approve items 1, 4, and 5 only. Hold items 2 and 3.
- [ ] Approve with the changes stated here: <changes>.
