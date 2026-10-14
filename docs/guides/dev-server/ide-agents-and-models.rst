IDE, agents, and models
=======================

Run these steps inside the project container. Each tool's upstream documentation is the
reference for its commands. Check a command against that documentation when it fails.

code-server: the browser IDE
----------------------------

Install code-server with the upstream install script. On Ubuntu, the script installs
the Debian package:

.. code-block:: bash

   curl -fsSL https://code-server.dev/install.sh | sh
   sudo systemctl enable --now code-server@$USER

Keep the IDE on loopback. Edit ``~/.config/code-server/config.yaml`` so that the server
binds to loopback, and store a password hash rather than a plain password:

.. code-block:: yaml

   bind-addr: 127.0.0.1:8080
   auth: password
   hashed-password: "<hash generated as described in the code-server docs>"

Restart the service after you change the file:

.. code-block:: bash

   sudo systemctl restart code-server@$USER

Open the project workspace, not the home directory. A ``.code-workspace`` file that
lists only the project's folders keeps the IDE's context small. For example:

.. code-block:: json

   {
     "folders": [
       { "path": "/workspace/repos/my-project" },
       { "path": "/workspace/scratch" }
     ]
   }

GitHub CLI
----------

Install the GitHub CLI from its official package repository, as described at
https://cli.github.com/. Then log in with the browser flow:

.. code-block:: bash

   gh auth login --hostname github.com --git-protocol https --web
   gh auth status

Use the narrowest credentials that still let you work. Do not paste tokens into the
terminal history, into files in the workspace, or into a chat.

git-annex and DataLad
---------------------

Use git-annex for large files, and DataLad for dataset metadata. The base container
already installs git-annex from apt. Install DataLad into the project's virtual
environment, not into the system Python:

.. code-block:: bash

   python3 -m venv .venv
   . .venv/bin/activate
   python -m pip install datalad

Keep private data in vaults, and keep public repositories to sanitized artifacts. The data
management guide, :doc:`../data-management`, sets out the rules.

OpenCode: the agent CLI
-----------------------

Install the OpenCode CLI with the installer listed in the V2 documentation at
https://opencode.ai/v2/docs/:

.. code-block:: bash

   curl -fsSL https://opencode.ai/v2/install | bash

Check that the background service is healthy, and that its API answers:

.. code-block:: bash

   opencode service status
   opencode api get /api/info

Configure OpenCode from the V2 configuration guide at https://opencode.ai/v2/docs/config.
Global settings live under ``~/.config/opencode/``. A project can add its own
``opencode.json``, or ``.opencode/opencode.json``. Terminal preferences are separate, in
``cli.json``, as described at https://opencode.ai/v2/docs/cli/config.

Keep provider credentials out of tracked files. Use the credential flow that the V2
documentation describes, or environment-variable substitution. Never commit a literal key.

Start the agent from the project root, so that its working directory matches the project:

.. code-block:: bash

   cd /workspace/repos/my-project
   opencode

Model choice is configuration
-----------------------------

Choose a model for each kind of task, on evidence from your own runs, and record the choice in
the log on :doc:`../../agents/roles-and-models`. That page also sets out the agent roles and
the rule for choosing a model. Configure the chosen model in OpenCode's settings, as described
in the OpenCode section above.
