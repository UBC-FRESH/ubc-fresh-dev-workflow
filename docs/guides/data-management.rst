Data management
===============

This guide says where a project's data lives, what may enter the public repository, and
what stays local. It links to the reference pages and to the public-safety rules in
`AGENTS.md <https://github.com/UBC-FRESH/ubc-fresh-dev-workflow/blob/main/AGENTS.md>`__,
and it does not repeat them. It does not set institutional rules. The last section says
what a project must add.

Three places for data
---------------------

.. list-table::
   :header-rows: 1
   :widths: 20 45 35

   * - Place
     - What goes there
     - Who can read it
   * - Public repository
     - Code, docs, tests, and sanitized artifacts.
     - Anyone who can see the repository.
   * - Private vault
     - Raw data, identifiable data, and unpublished documents, held in DataLad and git-annex, or in another private store.
     - The people that the maintainer names for the vault.
   * - Local scratch
     - Raw transcripts, exports, and working files, in ``tmp/`` or ``data/private/``. Git ignores both paths.
     - The person who works on the machine.

Content from a private vault never enters the public repository, not even as a git-annex
file. The repository holds no credentials, and no path that identifies a person.

Private vaults
--------------

A private vault is a store that only the people the maintainer names can read. It can be a
private repository, a DataLad dataset in private storage, or a folder on a lab server with
restricted access.

- Creating a vault, adding a person to it, and reading its contents each need an explicit
  approval that names the vault. See :doc:`../reference/approval-gates`.
- The agent opens a vault's data only when an approval names that vault.
- Credentials go in neither a vault's files nor the public repository. The credential rules
  for the dev server are in :doc:`dev-server/security-and-verification`.

DataLad and git-annex
---------------------

Large or private data lives in a DataLad dataset, and git-annex holds the file contents.

- `git-annex <https://git-annex.branchable.com/>`__ keeps file contents out of the git history,
  and it records where each copy lives.
- `DataLad <https://www.datalad.org/>`__ manages the dataset around them. It creates datasets,
  records changes with ``datalad save``, and pushes them to sibling repositories.

Keep at least the number of copies that the project's data policy names. Check where a copy
lives with ``git annex whereis <file>``.

Sanitized artifacts
-------------------

A sanitized artifact is a derived file, such as a figure, a summary table, or a log excerpt,
that may leave a vault. It holds no raw records, no identifiers that the data policy protects,
no coordinates, no credentials, and no personal paths.

1. The maintainer approves the vault that the artifact comes from, and what the artifact is
   for. The approval covers that artifact only.
2. The agent prepares the artifact, and it states what it removed.
3. The maintainer decides whether the artifact is sanitized, and approves its move into a
   tracked file.
4. Before the push, run ``python scripts/check_workflow.py``. It rejects personal paths,
   control characters, byte-order marks, and secret-shaped strings.
5. Record the artifact in the changelog, with the vault and the version it came from. Do not
   record the vault's content.

Raw transcripts stay local
--------------------------

A raw transcript is an exported session, a chat log, or any unedited record of an agent's or a
person's work. It stays in local scratch, and it is never committed.

- A report, a changelog entry, or an issue cites a transcript by its evidence: a command, a
  commit, a run ID, or command output. See :doc:`../reference/phase-closeout`. It does not paste
  the transcript into a tracked file.
- If a short excerpt must appear in a tracked file, it is sanitized first, and the maintainer
  approves that excerpt as a sanitized artifact.

Institutional rules
-------------------

This guide does not set institutional rules. Ethics approval, data-sharing agreements, and
retention periods come from the institution and from the data owner. A project records them in
its own policy page, and links that page from its ``AGENTS.md``, before it works with such data.

Related pages
-------------

- :doc:`../reference/approval-gates` says which actions wait for approval.
- :doc:`../reference/git-conventions` lists the paths that git ignores.
- :doc:`../reference/phase-closeout` sets the evidence rules for reports.
- :doc:`dev-server/security-and-verification` sets the credential rules for the dev server.
- `AGENTS.md <https://github.com/UBC-FRESH/ubc-fresh-dev-workflow/blob/main/AGENTS.md>`__ holds
  the public-safety rules.
