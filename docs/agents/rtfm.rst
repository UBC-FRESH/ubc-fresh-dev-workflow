RTFM protocol
=============

RTFM means "read the manual" before you act. In this pattern, the manual is this
site. It is the source of truth for procedures and contracts.

Rules
-----

1. Before a non-trivial action, read the page that governs it. The
   :doc:`session-protocol` names the common ones.
2. Cite the page and its section in your report. Use the published URL, or the
   repository path if the page is not published yet.
3. If a page is wrong, unclear, or missing, fix it in the same change set. If you
   cannot fix it now, open an issue that names the page and the gap, and say so
   in your report.
4. Do not invent a procedure to fill a gap. A gap is a finding.

Machine-readable entry point
----------------------------

``docs/llms.txt`` is a short index of the stable pages, with links. The docs build
copies it to the site root, so the published index is ``llms.txt`` on the Pages
site. The validator checks that every link in it resolves to a real page. Update
it when you add a page.

Stable names
------------

Page paths are part of the contract. A renamed page breaks links, citations, and
any agent that learned the old path. If you must rename a page, keep a short note
in the new page for one release, and update ``llms.txt`` in the same change set.
