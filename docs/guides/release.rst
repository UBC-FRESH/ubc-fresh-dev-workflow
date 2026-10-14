Release and deployment
======================

This guide is the release checklist for the seed, and for a project built from it. It
names the command for each tag, release, and Pages action. Each of those actions is
approval-only. The close-out report names it, the maintainer approves it, and then the
agent runs it and reads the result back. The rules are in :doc:`../reference/approval-gates`.
This guide links to them and does not repeat them.

Versions
--------

- A release tag takes the form ``v<major>.<minor>.<patch>``, and it sits on ``main`` only.
  See :doc:`../reference/git-conventions`.
- The policy for what each number means is written by P5.3, the seed versioning and
  migration policy. Until that policy is accepted, the maintainer names the version in the
  approval.
- The version must match the tag wherever it appears. If the project has a ``CITATION.cff``,
  its ``version`` and ``date-released`` fields name the release. For a project that is a
  package, its package metadata names the release too. The seed does not generate
  ``CITATION.cff``, so a project adds one when it needs citation metadata.

Release checklist
-----------------

Every item must hold before a tag is created. A red item stops the release.

1. The release gate in :doc:`../reference/lifecycle` is passed, including the verify gate.
2. The release commit is on ``main``. Its CI run is green in every job, and the full
   dashboard passes on it.
3. The changelog has an entry that names the version, the release commit, and the
   verification result.
4. The version being released is named in each place the project records it: ``CITATION.cff``,
   if the project has one, and the package metadata, if the project is a package.
5. The release notes are a file in the repository, and the maintainer has read them.
6. The approval names the version, the release commit, and each command below that it
   approves.

Release steps
-------------

Run these in order. Each step is approval-only.

1. Create the tag. Use a signed tag where the lab has a signing key, and an annotated tag
   otherwise.

   .. code-block:: bash

      git tag -s vX.Y.Z -m "vX.Y.Z" <release commit>
      git tag -a vX.Y.Z -m "vX.Y.Z" <release commit>
      git push origin vX.Y.Z

   Read the tag back with ``git ls-remote --tags origin vX.Y.Z``. For an annotated tag, the
   line that ends in ``^{}`` names the commit, and that commit must be the release commit.

2. Create the release as a draft, so that the maintainer can read it before anyone else
   sees it. The ``--verify-tag`` flag stops the command unless the tag already exists on the
   remote.

   .. code-block:: bash

      gh release create vX.Y.Z -R OWNER/REPO --verify-tag --draft --title "vX.Y.Z" --notes-file <release notes file>

3. Publish the draft, once the maintainer has read it.

   .. code-block:: bash

      gh release edit vX.Y.Z -R OWNER/REPO --draft=false

4. Read the release back. It must be published, and it must name the tag you created.

   .. code-block:: bash

      gh release view vX.Y.Z -R OWNER/REPO --json tagName,isDraft,publishedAt,url

5. Record the release. Add its URL to the changelog. Close the issue that tracks the release
   with a closeout comment that names the commit, as :doc:`../reference/github-mapping`
   requires. Report each read-back result with its evidence.

One-time setup
--------------

These steps run once for a repository. Each one changes a setting or an external account,
so each one is approval-only.

GitHub Pages
~~~~~~~~~~~~

The docs site is built and deployed by ``.github/workflows/docs.yml``, on each push to
``main``, once Pages uses the GitHub Actions source.

.. code-block:: bash

   gh api -X POST repos/OWNER/REPO/pages -f build_type=workflow

Read the setting back with ``gh api repos/OWNER/REPO/pages --jq '{build_type, html_url}'``.
Then read back the first ``docs.yml`` run on ``main`` with
``gh run list -R OWNER/REPO --workflow docs.yml --branch main --limit 1``.

PyPI trusted publishing (packages only)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This repository is a template, and no package exists, so it configures nothing. A project
that is a package follows these steps.

- Add a trusted publisher on PyPI for the project. It takes the repository owner, the
  repository name, the workflow file name, and an optional environment name. For a project
  that does not exist on PyPI yet, add a pending publisher from the account page, with the
  project name. A pending publisher reserves nothing until the first publish, and it becomes
  invalid if someone else registers the name first.
- The publish job needs ``permissions: id-token: write``, and it uses
  ``pypa/gh-action-pypi-publish@release/v1``. No token is stored. The PyPI docs also
  recommend a GitHub environment, such as ``pypi``.
- For a new package, rehearse on TestPyPI first. It uses the same action with
  ``repository-url: https://test.pypi.org/legacy/``, and it needs its own trusted publisher.

The maintainer adds each publisher on PyPI.

Zenodo and the archival DOI
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Zenodo archives each published GitHub release, once the repository is connected. To connect
it, connect a GitHub account to Zenodo, then turn the repository on in Zenodo's GitHub page.
In an organization, the connecting account needs GitHub admin permission and Zenodo access
to the organization.

Each release's DOI is on its Zenodo record. If the project has a ``CITATION.cff``, add the
DOI to it in a follow-up commit, after the maintainer confirms it. A DOI cannot be reserved
before the release.
Zenodo's FAQ describes a concept DOI, which covers all versions. Cite the concept DOI when
readers should always get the latest version.

Dry run
-------

A dry run rehearses this guide without side effects. It creates no tag, no release, and no
Pages setting, and it contacts no account. To run one:

1. Render a throwaway project with ``scripts/new_project.py`` into ``tmp/``, then run its
   validator and its dashboard.
2. Check each command in this guide against the installed CLI. For example,
   ``gh release create --help`` lists every flag that step 2 of the release steps uses.
3. Record the result on the issue, with each command's exit status.

A dry run checks the commands against the installed tools. It cannot check them against
GitHub, PyPI, or Zenodo, and its record says so.

Related pages
-------------

- :doc:`../reference/approval-gates` decides which actions wait for approval.
- :doc:`../reference/phase-closeout` covers the report that names these actions, and the
  conditions that stop them.
- :doc:`../reference/lifecycle` defines the release gate.
- :doc:`../reference/git-conventions` sets the tag rules.
