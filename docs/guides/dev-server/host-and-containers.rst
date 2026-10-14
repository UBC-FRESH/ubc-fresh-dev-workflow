Host and containers
===================

This page covers the server, the base container, and one container per project. The
installation steps follow the upstream LXD install page. The other commands are written
from the LXD reference and have not been re-checked against it. The P2 scripts reproduce
these commands, and they do not check them against the LXD reference. Names such as ``fresh-project-a`` and paths such as
``/srv/projects/project-a`` are examples; replace them.

Host requirements
-----------------

- Ubuntu Server 24.04 LTS on amd64. This guide was written for that release.
- Enough CPU, memory, and disk for your projects. A starting point is 8 cores, 32 GB of
  memory, and 500 GB of storage. Measure, then adjust. These are not requirements.
- A non-root administrator account with SSH key login, and unattended security updates
  enabled.
- A storage pool with cheap snapshots, such as ZFS or btrfs, if you can use one. The
  directory backend works, but its snapshots are full copies.
- Backups for the host, and for the exported project containers.

Install and initialize LXD
--------------------------

Run the read-only host checks first: `server/host-check.sh <https://github.com/UBC-FRESH/ubc-fresh-dev-workflow/blob/main/server/host-check.sh>`__.
It reports the state of the LXD snap, its channel, the ``lxd`` group, the daemon, and a storage
pool. It changes nothing on the host.

Install the LXD snap, and add your user to the ``lxd`` group. The group change applies
in new login sessions. ``newgrp`` applies it to the current shell:

.. code-block:: bash

   sudo snap install lxd --channel=latest/stable
   sudo usermod -aG lxd "$USER"
   newgrp lxd

Read :doc:`security-and-verification` before you add anyone to the ``lxd`` group. Then
initialize LXD, and accept the defaults unless you have a reason not to:

.. code-block:: bash

   sudo lxd init

Choose the storage backend on purpose. Changing it later means migrating every
instance.

Create the base container
-------------------------

The base container holds the common tools and no project data. Each project copies it.

The script `server/provision-base.sh <https://github.com/UBC-FRESH/ubc-fresh-dev-workflow/blob/main/server/provision-base.sh>`__
prints the commands below with ``--dry-run``, in the same order, and runs none of them.
``--apply`` runs them on a host, and a maintainer runs it. The login shell, the ``exit``, and the
final stop stay manual.

.. code-block:: bash

   lxc launch ubuntu:24.04 fresh-base
   lxc exec fresh-base -- cloud-init status --wait
   lxc exec fresh-base -- sudo --login --user ubuntu

Inside the container, install the common packages:

.. code-block:: bash

   sudo apt-get update
   sudo apt-get install -y git git-annex python3-venv python3-pip build-essential \
       curl ca-certificates jq shellcheck

Then install the GitHub CLI, code-server, OpenCode, and DataLad, as described in
:doc:`ide-agents-and-models`. When the base is ready, leave the container and stop it:

.. code-block:: bash

   exit
   lxc stop fresh-base

Create one container per project
--------------------------------

The script `server/new-project-container.sh <https://github.com/UBC-FRESH/ubc-fresh-dev-workflow/blob/main/server/new-project-container.sh>`__
prints, with ``--dry-run NAME WORKSPACE PORT``, the commands in this
section, and the workspace file that it writes, and it runs none of them. ``--apply`` runs them,
and a maintainer runs it. Before any change, it stops if the name, the port, or the workspace
file is already taken.

Copy the base for each new project, and start the copy:

.. code-block:: bash

   lxc copy fresh-base fresh-project-a
   lxc start fresh-project-a

Mount only that project's workspace, meaning the directory that holds its repositories
and its scratch space, and nothing else. The ``shift=true`` option keeps files owned by
your user inside the container. It needs a kernel with idmapped-mount support. If the
mount fails, check the disk device reference in the LXD documentation:

.. code-block:: bash

   lxc config device add fresh-project-a workspace disk \
       source=/srv/projects/project-a path=/workspace shift=true

Forward the IDE port
--------------------

Bind the IDE to the container's loopback interface, and forward a host loopback port to
it. You reach the forwarded port through an SSH tunnel, so the IDE never listens on a
public address:

.. code-block:: bash

   lxc config device add fresh-project-a ide proxy \
       listen=tcp:127.0.0.1:18080 connect=tcp:127.0.0.1:8080

On your laptop, open the tunnel:

.. code-block:: bash

   ssh -N -L 8080:127.0.0.1:18080 <user>@<dev-host>

Then open ``http://127.0.0.1:8080`` in the laptop browser.

Snapshots and backups
---------------------

Take a snapshot before a risky change, and restore it if the change fails:

.. code-block:: bash

   lxc snapshot fresh-project-a before-upgrade
   lxc restore fresh-project-a before-upgrade

Export a project container to a file that lives off the host:

.. code-block:: bash

   lxc export fresh-project-a ./backups/fresh-project-a.tar.gz

Keep the base current on a schedule. For a new project, copy the updated base. Avoid
upgrading old project containers in place, because their setups then drift apart.
