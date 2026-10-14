# Phase close-out report: v0.1.0 public release and onboarding

Phase: P4, v0.1.0 public release and onboarding
Parent issue: #12
Pull request: to be opened from `feature/p4-v0.1.0-release` into `main`
Evidence head: `7117efe`, the last task commit. The gates in this report were run before it.
Report commit: the commit that adds this report. Its CI run is posted on the pull request and on #12.
Date: 2026-10-14
Status: queued for approval. Nothing is merged, tagged, released, or changed in repository settings.

## Recommendation

Approve these actions. The agent carries them out in this order, and reads back each result. Each item can be approved or declined on its own.

1. Squash-merge the pull request once CI is green on the report commit, and delete the remote branch. The command is pinned to the report commit.

   ```bash
   gh pr merge <pr-number> -R UBC-FRESH/ubc-fresh-dev-workflow --squash --delete-branch --match-head-commit <report commit> --subject "P4 v0.1.0 public release and onboarding (#12, PR <pr-number>)"
   ```

2. Tag the merge commit on `main` as `v0.1.0`, and push the tag. The tag goes on `main`, not on the feature branch, so that Pages, which builds from `main`, serves the tagged commit.

   ```bash
   git fetch origin && git switch main && git pull --ff-only origin main
   git tag -a v0.1.0 -m "v0.1.0: first public release of the UBC-FRESH dev workflow seed" <merge commit>
   git push origin v0.1.0
   ```

3. Create the GitHub release from the tag, with the release notes in `notes/releases/v0.1.0.md`.

   ```bash
   gh release create v0.1.0 -R UBC-FRESH/ubc-fresh-dev-workflow --verify-tag --title "v0.1.0" --notes-file notes/releases/v0.1.0.md
   ```

4. Set the repository as a template, after items 1 to 3 pass their read-backs. This is the P4.2 template flag.

   ```bash
   gh repo edit UBC-FRESH/ubc-fresh-dev-workflow --template
   ```

5. Read back the live site at the tagged commit, and run the rendered-project check again. The live site must return HTTP 200 for `llms.txt`.

6. Open the onboarding feedback issue, as P4.3 names, in this repository, with the template and the notes as its context. This creates an issue only. It posts nothing to any external channel.

   ```bash
   gh issue create -R UBC-FRESH/ubc-fresh-dev-workflow --title "Onboarding feedback for v0.1.0" --body-file <body file>
   ```

7. Close #39, #40, and #41 with closeout comments, close #12 with a closeout comment that cites the merge commit, and set each issue body to its complete state.

## 1. Objectives and acceptance

Goal (from `ROADMAP.md` and #12): publish v0.1.0 of the seed as a public template, with live docs and an onboarding path for collaborators.

Acceptance criteria, as approved at the Phase 3 close-out:

- The live site builds from the tagged commit, and `llms.txt` is reachable. Not met yet. It needs the tag from item 2, and it is checked after item 2.
- A project generated from the template repository passes the validator. Met for a project rendered from this branch: 0 errors, with three warnings for files the seed does not render (`LICENSE`, `CODE_OF_CONDUCT.md`, `CITATION.cff`). Re-checked against the template repository after item 4.
- Release notes list the changes and the known gaps. Met by `notes/releases/v0.1.0.md`.

## 2. Workflow compliance

- P4.1 (#39), the release candidate, is complete in `3711f98`. Its checks are in the changelog. No tag and no release were created.
- P4.2 (#40), the live-site and render checks, is complete for its read-only parts in `7117efe`. Its template flag is not set. It waits for item 4.
- P4.3 (#41), the tag, the release, and the feedback issue, waits for items 2, 3, and 6.
- The approval gates in `AGENTS.md` cover the tag, the release, the settings change, and the merge. None has run.

## 3. Gate evidence

- The root dashboard was green before each commit on this branch, `3711f98` and `7117efe`. The changelog records the result.
- The validator on the repository reports 0 errors and 0 warnings at `7117efe`.
- A project rendered with `scripts/new_project.py` passes `scripts/check_workflow.py` with 0 errors and the three expected warnings.
- The live site, `https://ubc-fresh.github.io/ubc-fresh-dev-workflow/`, returns HTTP 200. `llms.txt` returns HTTP 200.

## 4. CI evidence

- No pull request exists for this branch yet, so CI has not run on `3711f98` or `7117efe`. The pull request for this phase opens with the report commit. Its CI run is the one that counts, and it must be green before item 1.

## 5. Deviations

| # | What happened | Why | How it was handled |
| --- | --- | --- | --- |
| 1 | P4.2's acceptance criterion requires the live site to build from a tagged commit, but the tag is created in P4.3, after P4.2's read-only checks. | The criterion and the sequence were written in different places. | The tag is placed on `main` after the merge, as item 2. The criterion is checked after it, and P4.2 stays active until then. |
| 2 | P4.1 writes `2026-10-14` as the candidate date in `CITATION.cff`. The tag and release date may fall on a different day. | The acceptance criterion asks for a release date before the tag exists. | Item 2 keeps the date if the tag is made on 2026-10-14. If it is made later, `CITATION.cff` and `notes/releases/v0.1.0.md` are updated in the same change set, before the tag. |

## Stated limits, which are not deviations

- The onboarding path has not been tested by a collaborator outside the maintainer. The feedback issue from item 6 collects that evidence.
- No external announcement is planned. The maintainer names any channel, and no post goes out without that approval.
- The template flag makes the repository visible as a template. It is the only setting change in this phase.
- The known gaps in `notes/releases/v0.1.0.md` stay open after the release. They are not fixed by this phase.

## 6. Next phase

No next phase is proposed. After P4 closes, the roadmap's P5 (maintenance and feedback loop, #13) is `planned`. It is activated only by a later maintainer approval.

## 7. Decision

- [ ] Approve as written.
- [ ] Approve items 1 to 4, and hold items 5 to 7.
- [ ] Approve with the changes stated here: <changes>.
