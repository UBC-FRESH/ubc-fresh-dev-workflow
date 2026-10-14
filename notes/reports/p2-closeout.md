# P2 close-out report: Dev server kit

Phase: P2, Dev server kit
Parent issue: #10
Pull request: #33, `feature/p2-dev-server-kit` into `main`
Evidence head: `b34ca96`. CI run 38493188725 is green in all four jobs on this head.
Report commit: the commit that adds this report. Its CI run is posted on PR #33 and on #10.
Date: 2026-10-14
Status: queued for approval. Not merged.

## Recommendation

Approval is requested for items 1 to 4. Each item can be approved or declined on its own. The agent carries out the approved items in this order, and reads back each result. Item 1 merges only if the pull request head is the report commit. The exact merge command, with that commit's hash, is posted on PR #33 with the report commit's CI run.

1. Squash-merge PR #33 once CI is green on the report commit, and delete the branch on the remote and locally.

   ```bash
   gh pr merge 33 -R UBC-FRESH/ubc-fresh-dev-workflow --squash --delete-branch --match-head-commit <report commit> --subject "P2 Dev server kit (#10, PR #33)"
   ```

2. Close parent issue #10 with a closeout comment that cites the merge commit, and set its body to the complete state.

   ```bash
   gh issue comment 10 -R UBC-FRESH/ubc-fresh-dev-workflow --body-file <closeout file>
   gh issue close 10 -R UBC-FRESH/ubc-fresh-dev-workflow
   ```

3. Delete the Phase 1 leftover local branch. Git refused to delete it after the Phase 1 squash merge, because the squash commit is not an ancestor of `main`. Its tree matches `main`, so no work is lost. The remote branch is already gone.

   ```bash
   git branch -D feature/p1-dogfood-validation
   ```

4. Launch Phase 3, Lifecycle playbooks and deployment, from the merged `main`.

   ```bash
   git switch main
   git pull --ff-only origin main
   git switch -c feature/p3-lifecycle-playbooks
   ```

   In its first commit, set P2 to `complete`, and set P3 to `active` with parent `#11`. Update the tracker map and the next-steps notes to match. Add the Phase 3 acceptance criteria if they are approved. Create P3.1 to P3.4 as sub-issues of #11, and post the activation on #11. Push with `git push -u origin feature/p3-lifecycle-playbooks`. P3.1 starts in a later move.

Settings changes: none. This phase changes no repository setting, tag, release, or external account.

## 1. Objectives and acceptance

The acceptance criteria were approved at the Phase 1 close-out. The table gives the evidence for each.

| Criterion | Evidence | Status |
| --- | --- | --- |
| Each script has a read-only or `--dry-run` mode, and a test shows that the mode changes nothing on the host where it runs. | `server/host-check.sh` is read-only. Nine tests in `tests/test_host_check.py` stub `snap`, `id`, and `lxc`, log every call, and check that only read commands run and that no file changes (`81da087`). `server/provision-base.sh --dry-run` runs no command, and `--apply` changes nothing on a provisioned base (`53889d0`). `server/new-project-container.sh --dry-run` runs no command (`e46af46`). Stated limit: the tests use stubs, and no script has run on a lab host. | Met with a stated limit |
| `shellcheck` passes on every script in CI. | The `quality` job runs `shellcheck server/*.sh` and `bash -n` on each script (`980d439`). In CI run 38493188725, on `b34ca96`, both quality jobs pass both new steps. shellcheck 0.9.0 passes locally. | Met |
| The committed dry-run transcript matches the scripts' dry-run output, and a test checks it. | `notes/reference/server-dry-run-transcript.md` records both dry runs. `tests/test_server_transcript.py` runs each command and compares its output (`980d439`). The tests gate is green at `b34ca96`. | Met |
| The dev server guide links to each script, and the docs build passes with `-W`. | The guide links `server/host-check.sh`, `server/provision-base.sh`, and `server/new-project-container.sh` to their files on GitHub (`b34ca96`). The docs gate builds the guide with `-W`, and it passes. Stated limit: the links point to `main`, which does not have the scripts until this phase merges. | Met with a stated limit |

The suite passes 202 tests at `b34ca96`, with 100 percent branch coverage of `scripts/` against the gate of 95 percent.

## 2. Workflow compliance

- **Parent issue before the branch.** #10 was created at 2026-10-13T18:40:00Z. The first commit on the branch, `ec7a753`, was made at 2026-10-14T00:18:13Z. Met.
- **Child issues before work.** #29 to #32 were created at 00:16:37 to 00:16:41Z, before `ec7a753` and before the first task commit, `81da087`. Met.
- **Sub-issue links.** `gh api repos/UBC-FRESH/ubc-fresh-dev-workflow/issues/10/sub_issues` lists 29, 30, 31, and 32. Met.
- **Branch from `main`.** The merge base of `feature/p2-dev-server-kit` and `main` is `8f063fb`, which is the head of `main`. Met.
- **Commit messages start with IDs.** All six commits do. Four start with a task ID (`81da087`, `53889d0`, `e46af46`, `980d439`). Two start with the phase ID, which the convention allows for phase-level changes: the activation `ec7a753` and the guide links `b34ca96`. Met.
- **Roadmap and changelog in step with the tasks.** The changelog changed in all six commits. The roadmap changed in the five commits that activated the phase or closed a task. `b34ca96` closes no task, so it changed no roadmap line. Met.
- **Gates for each commit.** Section 3. Met.
- **Child issues closed with closeout evidence.** #29, #30, #31, and #32 are closed. Each has a closeout comment that names its commit and its verification scope. Met.
- **Progress comments at milestones.** #10 has its activation comment and a progress comment for each task, P2.1 to P2.4. Met.
- **Approval gates respected.** This phase merged nothing, changed no setting, and created no tag, release, or external account. The runner pin was approved at the Phase 1 close-out as a default. It landed in P2.4 on this branch, so no separate runner pull request exists. Met.

## 3. Gate evidence

Each commit was checked with the validator, the dashboard, and the five pre-commit hooks before it was committed. The changelog entry for each commit records the root dashboard as green before the commit.

| Commit | Task | Gates | Result |
| --- | --- | --- | --- |
| `ec7a753` | Activation | Validator, dashboard, and pre-commit before the commit. | Green |
| `81da087` | P2.1 | Validator, dashboard, and pre-commit before the commit. Nine new tests. | Green |
| `53889d0` | P2.2 | Validator, dashboard, and pre-commit before the commit. Nine new tests. | Green |
| `e46af46` | P2.3 | Validator, dashboard, and pre-commit before the commit. Ten new tests. | Green |
| `980d439` | P2.4 | Validator, dashboard, and pre-commit before the commit. Six new or changed tests, and the new CI steps were checked locally with shellcheck 0.9.0 and `bash -n`. | Green |
| `b34ca96` | Phase-level docs | Validator, dashboard, and pre-commit before the commit. The docs build passes with `-W`. This is the evidence head. | Green |

## 4. CI evidence

Jobs: "Quality gates, Python 3.11", "Quality gates, Python 3.12", "Green dashboard summary", and "Pre-commit parity".

| Run ID | Head | Conclusion | Notes |
| --- | --- | --- | --- |
| 38493188725 | `b34ca96`, the evidence head | Success in all four jobs | The first CI run on this phase. Both quality jobs passed the new steps, "Install shellcheck" and "Check the server scripts". The run has no annotations, so the Node 20 deprecation warnings from the Phase 1 runs are gone. |
| Posted on PR #33 | The report commit | See the PR comment | The run for the commit that adds this report. |

## 5. Deviations

| # | Deviation | Cause | Remedy |
| --- | --- | --- | --- |
| 1 | The guide said that the P2 scripts would re-check the LXD commands. They reproduce them, and they do not check them against the LXD reference. | The sentence was written before the scripts existed, and I did not revisit it when they were built. | Corrected in `b34ca96`. The changelog records the correction. |
| 2 | Acceptance criterion 4 asks for links to each script, but the guide named the scripts only in plain text. | I did not check the criterion against the guide's text when I wrote the phase's scope. | Fixed in `b34ca96`, with a link to each script. |
| 3 | P2.4's first subtask says "CI job". The shellcheck check is a step of the required `quality` job. | A separate job would need a branch-protection change, which is a settings change. | The check is part of a required status check, and no settings change was needed. The closeout of #32 states it. |
| 4 | In my report after P2.2, I asked for approval of a separate runner pull request before 19 October. That was wrong, because the pin could land on this branch. | I asked before checking where the pin would land. | The pin landed in P2.4 on this branch, so the separate pull request was withdrawn. No such pull request exists. |
| 5 | The dry run of `new-project-container.sh` required the workspace to exist, so the transcript could not use the guide's example path. | The existence check was written for both modes. | Fixed in `980d439`. Only `--apply` requires the directory. Tests cover both cases. |

Stated limits, which are not deviations:

- No script has run on a lab host. The `--apply` paths are tested with stubbed `lxc`, `snap`, and `id` commands.
- The port check in `new-project-container.sh` reads only the proxy devices that LXD knows about. It cannot see a port that other software on the host uses.
- The tests do not check the wording of the plan's comment lines.
- The dashboard does not run shellcheck. It is in CI only, because shellcheck is not in the dev requirements, and adding it there is a dev-tool decision (F7).
- The guide's install step names no snap channel, but `server/host-check.sh` expects `latest/stable`. Recommended default: name `latest/stable` in that step, in the first commit of Phase 3, so the check matches the guide.

## 6. Next phase: Phase 3, Lifecycle playbooks and deployment (proposed)

**Goal** (from `ROADMAP.md`): give every lifecycle stage an exit gate, and write the playbooks a team needs for release, data handling, and agent roles.

**Tasks** (from `ROADMAP.md`, and the scope in #11):

- P3.1 Lifecycle stage gates and exit criteria. It also carries two decisions agreed at the Phase 1 close-out: the ADR for F4 (#25), which separates the local steps of Phase 0 from the GitHub steps, and the acceptance-criteria block for the seed's roadmap template (F9, #27).
- P3.2 Release and deployment playbook.
- P3.3 Data management playbook.
- P3.4 Agent roles and model routing playbook.

**Acceptance criteria** (proposed). The roadmap has none for Phase 3, so the report uses the two criteria in #11:

- Each lifecycle stage has entry criteria, exit criteria, and a named gate owner.
- The release playbook has been dry-run on the demo project from P1.

**Child issues.** P3.1 to P3.4 are created as sub-issues of #11 at launch, as item 4 describes.

**Open choices, each with a recommended default:**

- **Lifecycle stages.** Default: the six stages that #11 names: scope and design, build, verify, release, operate, and retire. Reason: #11 defines them, and P3.1 can revise the names when it writes the gates.
- **Gate owners.** Default: the maintainer owns every gate, and the agent prepares the evidence and the report. Reason: ADR 0008 makes the maintainer the approver.
- **Tags and releases.** Default: Phase 3 writes the release playbook, and it creates no tag and no release. The playbook names the commands for tags, releases, and Pages, and each one waits for its own approval. Reason: those actions are public and external.
- **PyPI trusted publishing.** Default: the playbook documents it for projects that are packages. This repository configures nothing, because the seed is a template and no package exists. Reason: the scope in #11 asks for the topic, not for a setting.
- **Data management.** Default: the playbook covers private vaults, DataLad and git-annex, and sanitized artifacts. Raw transcripts stay local, and no project data enters this repository. Reason: the public-safety rules, and the institutional questions are out of scope in #11.
- **Model routing.** Default: model choices are configuration. Each choice is recorded with the evidence behind it, and each one is re-checked at the P5.2 quarterly review. Reason: #11 says that model choices are not permanent rules.
- **Snap channel in the guide.** Default: the first Phase 3 commit names `latest/stable` in the guide's install step, as section 5 describes. Reason: the check in `server/host-check.sh` expects that channel.

**Roadmap defaults, reviewed:**

- Seed issue forms: keep Markdown templates. No friction entry asks for issue forms.
- `scripts/new_project.py`: keep writing local files only. Creating a repository stays a separate approved action.
- License: the root repository is MIT, and the seed ships no license file. The choice stays with each project (F6), as the Phase 1 close-out corrected.
- Coverage: 95 percent, as P1.5 set it.
- CI runner: pinned to `ubuntu-24.04`, with actions on Node 24, as P2.4 set it.

## 7. Decision

- [ ] Approve items 1 to 4 as written. Item 4 includes the Phase 3 acceptance criteria and the defaults for the open choices.
- [ ] Approve items 1 to 3, and hold item 4.
- [ ] Approve with the changes stated here: <changes>.
