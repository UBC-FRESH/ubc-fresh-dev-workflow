Git conventions
===============

Branches
--------

- Phase branch: ``feature/p<n>-<slug>``, created from the current ``main``. For
  example, ``feature/p1-dogfood-validation``.
- Short-lived task branch, rarely: ``issue-<n>-<slug>``, merged back into the
  phase branch.
- Release tags: ``v<major>.<minor>.<patch>``, placed on ``main`` only.

Commits
-------

- Start the subject line with the task ID, for example ``P0.5 add project
  initializer``.
- Keep one task to one commit where practical. Prefer several small commits to one
  large mixed commit.
- Commit only tracked, public-safe files. Check ``git status`` before each commit.
- Do not rewrite a branch that someone else has reviewed, unless the maintainer
  asks you to.

Pull requests
-------------

- Title: ``P<n> <phase name> (#<parent>)``, for example ``P0 Bootstrap scaffold
  (#1)``.
- Body: ``Part of #<parent>``, the child issues with their status, the
  verification commands and their results, and anything deferred.
- The maintainer merges with a squash merge, so that ``main`` gains one commit per
  phase. The squash commit keeps the phase ID and the pull request number in its
  title.
- The agent does not merge. The maintainer does.

Tags and releases
-----------------

- A tag marks a release on ``main``. Create it only after the release checklist
  passes, and only with maintainer approval.
- Signed tags are preferred where the lab has signing keys set up.

Ignored paths
-------------

The ``.gitignore`` keeps these out of git: ``.venv/``, ``_build/``, ``tmp/``,
``local/``, ``data/private/``, ``outputs/``, and caches. Scratch work goes in
``tmp/``. Private data goes in ``data/private/``, or in a private repository,
never in a tracked file.
