# Phase close-out report: Lifecycle playbooks and deployment

Phase: P3, Lifecycle playbooks and deployment
Parent issue: #11
Pull request: #38, `feature/p3-lifecycle-playbooks` into `main`
Evidence head: `da05118`, the head that the gates and the CI runs below cover
Report commit: the commit that adds this report. Its CI run is posted on PR #38 and on #11.
Date: 2026-10-14
Status: queued for approval. Not merged.

## Recommendation

Approve these actions. The agent carries them out in this order, and reads back each result.

1. Squash-merge pull request #38 once CI is green on the report commit, and delete the branch on the remote and locally. The exact command, pinned to the report commit, is posted on PR #38 with the report commit's CI run.

   ```bash
   gh pr merge 38 -R UBC-FRESH/ubc-fresh-dev-workflow --squash --delete-branch --match-head-commit <report commit> --subject "P3 Lifecycle playbooks and deployment (#11, PR #38)"
   ```

2. Close parent issue #11 with a closeout comment that cites the merge commit.

   ```bash
   gh issue comment 11 -R UBC-FRESH/ubc-fresh-dev-workflow --body-file <closeout file>
   gh issue close 11 -R UBC-FRESH/ubc-fresh-dev-workflow
   ```

3. Delete the local branch `feature/p3-lifecycle-playbooks`. Git is expected to refuse `branch -d`, because the squash commit is not an ancestor of `main`. If it refuses, delete the branch with `git branch -D`, but only after checking that the branch's tree equals the merge commit's tree, as the Phase 1 and Phase 2 deletions did. This item names the forced deletion, so the approval of this item covers it.

   ```bash
   git branch -d feature/p3-lifecycle-playbooks
   git branch -D feature/p3-lifecycle-playbooks
   ```

4. Launch Phase 4, v0.1.0 public release and onboarding, from the merged `main`.

   ```bash
   git switch main
   git pull --ff-only origin main
   git switch -c feature/p4-v0.1.0-release
   ```

   In its first commit, set P3 to `complete`, and set P4 to `active` with parent `#12`. Update the tracker map and the next-steps notes to match. Create P4.1 to P4.3 as sub-issues of #12, post the activation on #12, and push with `git push -u origin feature/p4-v0.1.0-release`. P4.1 starts in a later move.

Settings changes, each with its exact command. Each one runs only after its own approval.

- None. This phase changes no repository setting, tag, release, or external account. The Phase 4 settings changes are named in the Phase 4 report.

## 1. Objectives and acceptance

| Criterion | Evidence | Status |
| --- | --- | --- |
| Each lifecycle stage has entry criteria, exit criteria, and a named gate owner. | `docs/reference/lifecycle.rst` in `90c171a`. It defines the six stages, and the maintainer is the gate owner for each. The seed's Lifecycle Map follows it in `aecda62`. | met |
| The release playbook has been dry-run on the demo project from P1. | Recorded in `3e762cc` and on #35. The demo, rendered into `tmp/release-dry-run`, validates with 0 errors and 3 expected warnings, and its own dashboard is green. Every command in the guide exists with the flags it uses. The Pages and docs-run read-backs return data from this repository. | met with a stated limit: the dry run checks the commands against the installed tools, not against GitHub, PyPI, or Zenodo. |
| Goal (from the roadmap): playbooks for release, data management, and agent roles. | `docs/guides/release.rst` in `655e508`, closed in `3e762cc`. `docs/guides/data-management.rst` in `e870ef4`, closed in `fed5c45`. `docs/agents/roles-and-models.rst` in `927ce30`, closed in `da05118`. | met |

The two acceptance criteria are the ones that the Phase 2 close-out approved.

## 2. Workflow compliance

- **Parent issue before the branch:** #11 was created at 2026-10-13T18:40:01Z. The branch's first commit, `d3593bb`, is at 2026-10-14T04:05:21Z. Met.
- **Branch from `main`:** the merge base of `feature/p3-lifecycle-playbooks` and `main` is `f998cd8`, the head of `main` when the branch was made. Met.
- **Commit messages that start with task IDs:** 12 of 12. `d3593bb` is a phase-level activation, as the convention allows, and the other 11 name P3.1 to P3.4. Met.
- **Gates for each commit:** section 3. Met.
- **Roadmap and changelog in step:** `CHANGE_LOG.md` changed in 12 of 12 commits, and `ROADMAP.md` changed in 11 of 12. `346aaf1` changed only the seed's template, and it closed no task. Met.
- **Child issues before work:** #34 to #37 were created between 2026-10-14T04:03:30Z and 04:03:35Z, before the first task commit, `88fcd46`, at 04:20:35Z. Met.
- **Child issues closed with closeout evidence:** #34 closed at 04:36:06Z, after `aecda62`. #35 closed at 04:47:40Z, after `3e762cc`. #36 closed at 04:54:42Z, after `fed5c45`. #37 closed at 05:01:33Z, after `da05118`. Each closeout comment names its commits. The findings #25 (F4) and #27 (F9), which P3.1 carried, are closed with closeout comments. Met.
- **Sub-issue links:** `gh api repos/UBC-FRESH/ubc-fresh-dev-workflow/issues/11/sub_issues` lists 34, 35, 36, and 37. Met.
- **Progress comments at milestones:** #11 has its activation comment, and progress comments for P3.1 with P3.2 (one comment, posted after both had closed), P3.3, and P3.4. Met with a deviation, see section 5.
- **Approval gates respected:** no tag exists (`git tag -l` lists none), and no release exists (`gh release list` lists none). No setting, Pages source, branch protection, or external account was changed. The only Pages and workflow calls were reads. No private data was read or committed. Met.

## 3. Gate evidence

Before each commit, the full dashboard ran: ruff, mypy, pytest with the coverage gate, the validator, the docs build with warnings as errors, and the seed generation. The validator also ran before each push. Every commit was green when it was made.

| Commit | Task | Gates | Result |
| --- | --- | --- | --- |
| `d3593bb` | Activation | Dashboard, pre-commit, and validator before the commit. | Green |
| `88fcd46` | P3.1, ADR 0009 drafted | Dashboard and validator before the commit. | Green |
| `ed3daa7` | P3.1, ADR 0009 accepted | Dashboard and validator before the commit. | Green |
| `346aaf1` | P3.1, Phase 0 change | Dashboard and validator. The new test `test_generated_phase_0_holds_only_local_tasks` failed on the old template, which had three Phase 0 tasks, and passes on the new one. | Green |
| `aecda62` | P3.1, acceptance block and Lifecycle Map | Two new tests failed on the old template and pass on the new one. The first dashboard run was red on lint and format in the new test, and it was fixed before the commit. | Green |
| `90c171a` | P3.1, lifecycle page | Dashboard, including the Sphinx build with `-W`. | Green |
| `655e508` | P3.2, release guide | Dashboard, including the Sphinx build with `-W`. | Green |
| `3e762cc` | P3.2, closing after the dry run | Dashboard. The dry run on the P1 demo is recorded in section 1. | Green |
| `e870ef4` | P3.3, data guide | Dashboard, including the Sphinx build with `-W`. | Green |
| `fed5c45` | P3.3, closing | Dashboard. | Green |
| `927ce30` | P3.4, roles page | Dashboard, including the Sphinx build with `-W`. | Green |
| `da05118` | P3.4, closing | Dashboard. | Green |

## 4. CI evidence

| Run ID | Head commit | Conclusion | Notes |
| --- | --- | --- | --- |
| 38514639908 | `da05118`, the evidence head | success in all four jobs: Green dashboard summary, Pre-commit parity, Quality gates for Python 3.11, and Quality gates for Python 3.12 | The first CI run on PR #38. |
| Posted on PR #38 | The report commit | See the pull request comment | The run for the commit that adds this report. |

## 5. Deviations

| Deviation | Cause | Remedy |
| --- | --- | --- |
| #11 has one progress comment for P3.1 and P3.2 together, posted after both had closed. The convention is one comment per task. | I checked the two tasks together, once both had closed. | The comment names both tasks and their commits. P3.3 and P3.4 each have their own comment. |
| The first dashboard run for `aecda62` was red on lint and format, in the new test: a long line and a compound assertion. | I did not run `ruff check` on the test file before the dashboard. | Fixed in the same change set, before the commit. `aecda62` leaves the dashboard green. |
| The release guide in `655e508` assumed every project has a `CITATION.cff`, and the seed does not generate one. | I wrote the citation steps without checking which files the seed generates. | The P3.2 dry run found it. `3e762cc` makes the citation steps conditional, before P3.2 closed. |

Stated limits, which are not deviations:

- No playbook has run against a live repository, PyPI, or Zenodo. The release dry run checked commands against the installed tools.
- The second row of the model log names the model that this session ran on. Its evidence is gate results, not a comparison. The maintainer should confirm that row.
- The seed does not ship the lifecycle, release, data, or roles pages. A generated project has no playbooks yet.

## 6. Next phase: Phase 4, v0.1.0 public release and onboarding (proposed)

**Goal** (from `ROADMAP.md` and #12): publish v0.1.0 of the seed as a public template, with live docs and an onboarding path for collaborators.

**Tasks** (from #12):

- P4.1 Release candidate: versions, citation metadata, release notes.
- P4.2 Pages enablement, live-site check, and template flag. Approval required.
- P4.3 Tag, GitHub release, announcement, and onboarding feedback issue. Approval required.

**Acceptance criteria** (from #12):

- The live site builds from the tagged commit, and `llms.txt` is reachable.
- A project generated from the template repository passes the validator.
- Release notes list the changes and the known gaps.

**Child issues:** P4.1 to P4.3 are created as sub-issues of #12 at launch, as item 4 describes.

**Open choices, each with a recommended default:**

- **The seed's docs set in v0.1.0.** Default: the seed does not ship the lifecycle, release, data, or roles pages in v0.1.0. They stay in this repository's docs. Reason: the seed's docs are a small set by design, and the onboarding path can link to this repository's docs. P5.3 can revisit it.
- **Release notes file.** Default: `notes/releases/v0.1.0.md`, named in the release command. Reason: it keeps the root clean, and the approval can name the file.
- **Citation metadata.** Default: P4.1 adds `version: 0.1.0` and a `date-released` to `CITATION.cff`. The DOI is added only after Zenodo is connected, which is an approval-only account action. Reason: #12 scopes the version and the date, and Zenodo is an external account.
- **Template flag.** Default: set it after the tag and the Pages check pass, with `gh repo edit UBC-FRESH/ubc-fresh-dev-workflow --template`, approved as a settings change. Reason: the flag makes the repository visible as a template, so it should follow a tagged and checked release.
- **Announcement.** Default: the text is drafted in P4.3, and it is posted only after the maintainer approves it. Reason: an announcement is an external action.

## 7. Decision

- [ ] Approve as written.
- [ ] Approve with the changes stated here: <changes>.
