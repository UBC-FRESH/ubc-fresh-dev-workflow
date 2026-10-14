# P1 close-out report: Dogfood and validation

Phase: P1, Dogfood and validation
Parent issue: #9
Pull request: #28, `feature/p1-dogfood-validation` into `main`
Evidence head: `1932b2e`. CI run 38488267064 is green in all four jobs on this head.
Report commit: the commit that adds this report. Its CI run is posted on PR #28 and on #9.
Date: 2026-10-14
Status: queued for approval. Not merged.

## Recommendation

Approval is requested for items 1 to 4. Each item can be approved or declined on its own. The agent carries out the approved items in this order, and reads back each result. Item 1 merges only if the pull request head is the report commit. The exact merge command, with that commit's hash, is posted on PR #28 with the report commit's CI run.

The first queue of this report named `d38b65e` as its evidence head. Review of PR #28 then found two defects, which are fixed on the branch. This report replaces the first queue. Section 5 records the defects.

1. Squash-merge PR #28 once CI is green on the report commit, and delete the branch on the remote and locally.

   ```bash
   gh pr merge 28 -R UBC-FRESH/ubc-fresh-dev-workflow --squash --delete-branch --match-head-commit <report commit> --subject "P1 Dogfood and validation (#9, PR #28)"
   ```

2. Close parent issue #9 with a closeout comment that cites the merge commit.

   ```bash
   gh issue comment 9 -R UBC-FRESH/ubc-fresh-dev-workflow --body-file <closeout file>
   gh issue close 9 -R UBC-FRESH/ubc-fresh-dev-workflow
   ```

3. Records. Tick the subtask boxes on #18, #19, and #20, so that each matches the closeout comment already on it. The agent edits only those boxes, shows each diff, and validates each body before it posts it.

   ```bash
   gh issue edit 18 -R UBC-FRESH/ubc-fresh-dev-workflow --body-file <file>
   gh issue edit 19 -R UBC-FRESH/ubc-fresh-dev-workflow --body-file <file>
   gh issue edit 20 -R UBC-FRESH/ubc-fresh-dev-workflow --body-file <file>
   ```

4. Correct the license default, and launch Phase 2 from the merged `main`.

   ```bash
   git switch main
   git pull --ff-only origin main
   git switch -c feature/p2-dev-server-kit
   ```

   In its first commit, set P1 to `complete`, and set P2 to `active` with parent `#10`. Update the tracker map and the next-steps notes to match. Correct the license default in `ROADMAP.md`, as section 6 describes. Add the Phase 2 acceptance criteria if they are approved. Create P2.1 to P2.4 as sub-issues of #10, and post the activation on #10. Push with `git push -u origin feature/p2-dev-server-kit`. P2.1 starts in a later move.

Settings changes: none. This phase changes no repository setting, tag, release, or external account.

## 1. Objectives and acceptance

| Criterion | Evidence | Status |
| --- | --- | --- |
| The demo renders, passes its own validator, and has a green dashboard. | P1.1 rendered the demo, and P1.6 ran its validator after each step: `0 error(s), 3 expected warnings`. Its dashboard passed six gates at `fd1f45f` and at `99adefe`. Stated limit: six gates, not eight (F5), because the demo has no `scripts/new_project.py`. | Met with a stated limit |
| A fresh clone of this repository passes the dashboard. | P1.2, `8733eae`: a fresh clone of `main` at `2943d83` passed the five pre-commit hooks, the dashboard with eight gates, and 146 tests at 100 percent branch coverage. Stated limit: the clone was of `main`. This branch's CI run, 38488267064, passes the same gates on `1932b2e`. | Met |
| The friction log lists every failure, and each entry names its fix, its deferred issue, or its accepted reason. | `notes/reference/dogfood-log.md` at `1932b2e`. Fixed: F1 in `928223e`, F8 in `14f9cd2`, and F11 in `d38b65e`. Accepted: F2, F5, F6, and F10. Deferred: F3 to #24, F4 to #25, F7 to #26, and F9 to #27. The validator gaps are V1 accepted, V2 in #24, and V3 fixed in P1.4. | Met |
| Walk mode honors `.gitignore`, and the coverage gate is 95 percent. | Walk mode is in `7158ec5`. The negation fix in `9a6369d` closes a gap in its stated behavior (deviation 8). The gate is in `4b048bd`, and the seed's template states it in `1932b2e` (deviation 9). The suite passes 168 tests, with 100 percent branch coverage of `scripts/` against the gate of 95. The tests gate is green in CI run 38488267064. | Met |
| The demo's close-out report is queued and approved. | Queued in the demo at `fdd38a1`. The report named three actions and one decision. The maintainer's message 'go' approved it as written, and the actions ran in `a23ad15` (squash merge) and `99adefe` (Phase 1 activation). Stated limit: the GitHub steps of the close-out were not rehearsed, because the rehearsal has no GitHub repository (P4). | Met with a stated limit |

## 2. Workflow compliance

- **Parent issue before the branch.** #9 was created at 2026-10-13T18:39:58Z. The first commit on the branch, `cdb022c`, was made at 21:59:18 +0000. Met.
- **Child issues before work.** #18 to #23 were created at 21:57:45 to 21:57:55Z, before `cdb022c`, and before each task's first commit. Met.
- **Sub-issue links.** `gh api repos/UBC-FRESH/ubc-fresh-dev-workflow/issues/9/sub_issues` lists 18, 19, 20, 21, 22, and 23. Met.
- **Branch from `main`.** The merge base of `feature/p1-dogfood-validation` and `main` is `2943d83`, which is the head of `main`. Met.
- **Commit messages start with task IDs.** 12 of the 13 phase commits do. The first, `cdb022c`, starts with the phase ID, which the commit convention allows for activation. Met.
- **Roadmap and changelog in step with the tasks.** The changelog changed in every phase commit. The roadmap changed in 8 of the 11 commits before the review fixes. The other three, `43a3a82`, `928223e`, and `14f9cd2`, are mid-task commits, and their checkboxes changed in the commit that closed each task. The two review fixes changed no checkbox. Met.
- **Gates for each commit.** Section 3. Met, with the record gap in deviation 1.
- **Child issues closed with closeout evidence.** #18 to #23 are closed. Each has a closeout comment that names its commits. #23's closeout is its execution record. Met, with the boxes in deviation 5. #21 and #22 each receive a correction comment, because the review fixes change what their closeouts said (deviations 8 and 9).
- **Progress comments at milestones.** #9 has its activation comment, and a progress comment for each task from P1.1 to P1.6. Met.
- **Approval gates respected.** This phase merged nothing on GitHub, deleted no GitHub branch, changed no setting, and created no tag, release, or external account. In the demo, the merge and the branch deletion ran only after the approval. The approval is recorded in deviation 2. Met.

## 3. Gate evidence

Each row gives the gate result that the record shows for the commit. The changelog entry for each commit records the root dashboard as green before the commit, unless the row says otherwise.

| Commit | Task | Gates | Result |
| --- | --- | --- | --- |
| `cdb022c` | Activation | Its changelog entry does not record a run. A re-run at the commit, in a temporary worktree, passed eight gates. | Green (deviation 1) |
| `7ac1e75` | P1.1 | Dashboard before the commit. The demo's own dashboard was green before each demo commit. | Green |
| `8733eae` | P1.2 | Dashboard before the commit. A fresh clone passed the five pre-commit hooks and the dashboard. | Green |
| `43a3a82` | P1.3 | Dashboard before the commit. | Green |
| `928223e` | P1.3 | Dashboard before the commit, with 147 tests. The regression test failed on the unfixed seed and passes on the fix. | Green |
| `db5868d` | P1.3 | Dashboard before the commit. | Green |
| `7158ec5` | P1.4 | Dashboard before the commit, with 164 tests. The five pre-commit hooks passed with the venv on `PATH`. | Green |
| `4b048bd` | P1.5 | Dashboard before the commit, with 166 tests. The five pre-commit hooks passed with the venv on `PATH`. | Green |
| `14f9cd2` | P1.6 | Dashboard and the five pre-commit hooks, with the venv on `PATH`, before the commit. | Green |
| `22afe5b` | P1.6 | Dashboard and the five pre-commit hooks before the commit. | Green |
| `d38b65e` | P1.6 | Dashboard and the five pre-commit hooks before the commit. This was the head of the first queue. | Green |
| `9a6369d` | P1.4 review fix | Dashboard and the five pre-commit hooks before the commit, with 168 tests. The new test failed on the previous reader and passes on the fix. | Green |
| `1932b2e` | P1.5 review fix | Dashboard and the five pre-commit hooks before the commit. The new policy check failed on the template and passes on the fix. This is the evidence head. | Green |

The five pre-commit hooks use the same tools as the dashboard's lint, format, types, tests, and validator gates. The hooks are recorded only for the commits that name them.

## 4. CI evidence

Jobs: "Pre-commit parity", "Quality gates, Python 3.11", "Quality gates, Python 3.12", and "Green dashboard summary".

| Run ID | Head | Conclusion | Notes |
| --- | --- | --- | --- |
| 38488267064 | `1932b2e`, the evidence head | Success in all four jobs | The run that this report relies on. |
| 38487721549 | `b98e509`, the report commit of the first queue | Success in all four jobs | Superseded by the review fixes, so this report does not rely on it. |
| 38487392426 | `d38b65e`, the head of the first queue | Success in all four jobs | Superseded by the review fixes. It was the first CI run on this phase. |
| Posted on PR #28 | The report commit | See the PR comment | The run for the commit that adds this report. |

Annotations on the runs, which are not failures: GitHub reports that Node.js 20 is deprecated for `actions/checkout@v4`, `actions/setup-python@v5`, and `actions/upload-artifact@v4`. It also reports that `ubuntu-latest` moves to Ubuntu 26 from 19 October 2026. Section 6 proposes the fix.

## 5. Deviations

| # | Deviation | Cause | Remedy |
| --- | --- | --- | --- |
| 1 | The activation commit `cdb022c` has no recorded dashboard run before the commit. | Its changelog entry does not state a gate result. | A re-run at the commit, in a temporary worktree, passed eight gates. The commit is unchanged. Later changelog entries state their gate results, as the table in section 3 shows. |
| 2 | The approval of the P1.6 demo close-out was the message 'go'. | The approval request listed the actions and a default decision, and the reply was a single word. | The agent read it as approval of the report as written. The P1.6 record quotes the message. This report asks for approval item by item, so that each item can be approved or declined. |
| 3 | In the P1.6 rehearsal, the demo's validator ran after the P0.3 commit, not before it. | The first command used an interpreter path that does not exist inside the demo, and a pipe hid the failure. | The validator ran after the commit with the correct path, and exited 0 with 0 errors and 3 expected warnings. The commit's content did not change. The P1.6 record discloses it. |
| 4 | CI did not run on the Phase 1 commits until PR #28 opened. | The workflow runs on pull requests and on pushes to `main`. A branch without a pull request gets no run. | The local dashboard and pre-commit runs cover each commit in section 3. The first CI run was on `d38b65e`, and the review fixes added the runs on `1932b2e`. |
| 5 | The subtask boxes on #18, #19, and #20 are unticked, though each issue is closed with a closeout comment. | Closing those issues did not tick their checklists. | Item 3 of the recommendation. |
| 6 | The demo's gates ran on the root's virtual environment, and the demo predates F1 and P1.5. | The demo has no environment of its own, and a generated project keeps the files it was generated with. | A stated limit, recorded as F10, which is accepted. |
| 7 | The roadmap's next-steps note says the seed carries the MIT license. The seed ships no license file, and the first-project guide leaves the choice to the project (F6). | The note was written before F6 was recorded. | Item 4 of the recommendation corrects the note. The root repository stays MIT. |
| 8 | Review of PR #28 found that walk mode dropped a negated ignore line it could not apply. An earlier rule could then hide a file that git would commit, so the walk missed it. The P1.4 closeout and changelog said that a skipped line scans more files, not fewer. That was true for ignore lines, but not for negations. | I tested ignore lines that the reader could not apply, and I did not test a negation of one. | Fixed in `9a6369d`. The reader now keeps one rule that re-includes every path for each such negation, so it scans a superset. The test `test_an_unsupported_negation_cannot_hide_a_file` failed on the previous reader and passes now. The correction is in the changelog, and in a comment on #21. The current ignore files of this repository contain no negation, so the defect did not hide a file in any current run. |
| 9 | Review of PR #28 found that the seed's `AGENTS.md` template still stated the 90 percent gate, while generated projects enforce 95 percent. | My search for the old gate covered `.md`, `.rst`, `.toml`, and `.py` files, and it missed `.tmpl` files. | Fixed in `1932b2e`. The template states 95 percent, and the policy test now checks the template as well. The test failed on the template and passes now. The correction is in the changelog, and in a comment on #22. |

Stated limits, which are not deviations:

- The rehearsal has no GitHub repository. The GitHub steps of the close-out were not rehearsed, and P4 rehearses them with approval.
- The fresh-clone rehearsal in P1.2 used `main`, not this branch. The CI run on `1932b2e` covers this branch's gates.

## 6. Next phase: Phase 2, Dev server kit (proposed)

**Goal** (from `ROADMAP.md`): turn the dev server guide into idempotent helper scripts with a dry-run mode, shellcheck-clean and tested in CI.

**Tasks** (from `ROADMAP.md`):

- P2.1 Host check script with a read-only mode
- P2.2 Base container provisioning with `--dry-run`
- P2.3 Per-project container script and workspace file generator
- P2.4 CI linting and a committed dry-run transcript

**Acceptance criteria** (proposed). The roadmap has none for Phase 2, so the report proposes these:

- Each script has a read-only or `--dry-run` mode, and a test shows that the mode changes nothing on the host where it runs.
- `shellcheck` passes on every script in CI.
- The committed dry-run transcript matches the scripts' dry-run output, and a test checks it.
- The dev server guide links to each script, and the docs build passes with `-W`.

**Child issues.** P2.1 to P2.4 are created as sub-issues of #10 at launch, as item 4 describes.

**Open choices, each with a recommended default:**

- **Shell dialect.** Default: Bash with `set -euo pipefail`, checked by shellcheck. Reason: the guide's commands are Bash, and shellcheck targets Bash.
- **Tests for the scripts.** Default: pytest calls each script in its dry-run or read-only mode. Reason: one test runner, which the dashboard already runs.
- **Host changes.** Default: none in Phase 2. The scripts run only in dry-run or read-only modes. A run on a real host is a separate approved action. Reason: a shared host falls under the rule for settings and external actions.
- **CI runner.** Default: pin the runner, and move the three actions named in section 4 to versions that run on Node 24, before 19 October 2026. The default puts this in the Phase 2 pull request. If that pull request cannot merge before the date, the change becomes a separate small pull request, which needs its own approval. Reason: GitHub moves `ubuntu-latest` to Ubuntu 26 from 19 October 2026.

**Deferred findings.** Each needs a decision before any change. The recommended default for each is given.

- **F3, #24: the validator's placeholder check.** Default: keep it deferred, and review it at the P5.2 quarterly review. Reason: it adds a finding code, and no Phase 2 task needs it.
- **F4, #25: separate the seed's local Phase 0 steps from its GitHub steps.** This needs an ADR. Default: write the ADR under P3.1, the lifecycle stage gates. Reason: the stage gates say which steps are local and which are GitHub.
- **F7, #26: pin the dev tools.** This needs an ADR. Default: decide it with P5.3, the seed versioning and migration policy. Reason: pins decide how the seed reproduces over time, and P5.3 defines that.
- **F9, #27: acceptance criteria in the seed's roadmap template.** Default: fold it into P3.1, because exit criteria are the same concept. Reason: Phases 2 to 5 of this roadmap have no acceptance criteria either, so each close-out must propose them until P3.1 lands.

**Roadmap defaults, reviewed:**

- Seed issue forms: keep Markdown templates. No friction entry asks for issue forms.
- `scripts/new_project.py`: keep writing local files only. Creating a repository stays a separate approved action.
- License: correct the note, as item 4 describes. The root repository is MIT. The seed ships no license file, so the choice stays with each project (F6).
- Coverage: 95 percent, as P1.5 set it.

## 7. Decision

- [ ] Approve items 1 to 4 as written. Item 4 includes the Phase 2 acceptance criteria and the defaults for the open choices.
- [ ] Approve items 1 and 2 only, and hold items 3 and 4.
- [ ] Approve with the changes stated here: <changes>.
