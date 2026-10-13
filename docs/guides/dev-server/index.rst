FRESH-style dev server
======================

This guide describes the environment the lab uses for agent-assisted projects: one
Linux server, one LXD container per project, a browser IDE, and an agent CLI inside
the container. It is a recipe, not a requirement. Read
:doc:`../../agents/session-protocol` to see how the agent uses the environment.

Reference architecture
----------------------

.. code-block:: text

   laptop browser
        |  SSH tunnel
        v
   dev host (Ubuntu LTS, LXD)
        +-- fresh-base           base container: common tools, no project data
        +-- fresh-project-a      workspace: repositories and scratch for project A only
        +-- fresh-project-b      workspace: repositories and scratch for project B only

Each project container runs code-server (the IDE), the GitHub CLI, git-annex and
DataLad, Python, Sphinx, and the OpenCode CLI.

Why this shape
--------------

- **Context hygiene.** An agent sees only its project's repositories and scratch space,
  so unrelated work does not leak into its context or its decisions.
- **Reproducibility.** Every new project starts from the same base container, so the
  setups do not drift apart.
- **Recoverability.** Snapshots and exports are cheap, so a risky step can be undone.

Minimum viable variant
----------------------

No server? A single Linux laptop or virtual machine is enough. Run LXD there, or use
one devcontainer per project. The pattern needs four things: an isolated environment
for each project, a workspace that holds only that project, a browser or SSH entry
point, and an agent CLI with a pinned working directory. Everything else is optional.

Pages in this guide
-------------------

.. toctree::
   :maxdepth: 1

   host-and-containers
   ide-agents-and-models
   security-and-verification
