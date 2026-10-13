Security and verification
=========================

Read this page before you give anyone access to the server.

The ``lxd`` group is root on the host
-------------------------------------

Membership in the ``lxd`` group gives full access to the LXD daemon through its Unix
socket. That access includes attaching host paths and devices to any instance, and
changing its security features. In practice it is root-equivalent on the host, and the
upstream LXD documentation says so. Add people to the group only if you would give them
root access.

Containers are not a sandbox for hostile code
---------------------------------------------

LXD containers separate context, and they contain most failures well. Unprivileged
containers, which are the default, map root inside the container to an unprivileged user
on the host. The containers still share the host kernel. Do not run code you do not trust
in a container. Use a virtual machine instead:

.. code-block:: bash

   lxc launch ubuntu:24.04 untrusted-check --vm

Avoid privileged containers (``security.privileged=true``). Enable nesting
(``security.nesting=true``) only when a project needs containers inside its container,
and write down why.

Credentials
-----------

- Keep tokens out of the repository, the workspace, shared mounts, and chat logs.
- Use fine-grained tokens scoped to the repositories a project needs, or the browser login
  with the least privilege your account allows.
- Keep provider keys in the provider's credential flow, or in environment variables. Check
  ``git status`` and the notes before each commit.
- If a credential leaks, revoke it first, then investigate.

Exposure
--------

- Keep code-server on loopback. Reach it through an SSH tunnel, or through a reverse proxy
  that terminates TLS and requires authentication.
- Do not publish IDE or LXD ports to the public internet.
- Keep the host patched. Use unattended security updates, and schedule upgrades in a
  maintenance window.

Backups
-------

- Export project containers before risky upgrades, and keep the exports off the host.
- Treat the Git remotes as the primary copy of the code. A container is not a backup of
  your repositories.
- Test one restore each quarter.

Verification checklist
----------------------

Run these checks after setup. Each row names the command that performs the check.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Check
     - Command
   * - The LXD daemon is reachable
     - ``lxc list``
   * - The project container is running, and the base is stopped
     - ``lxc list fresh-``
   * - Passwordless sudo works inside the project container
     - ``lxc exec fresh-project-a -- sudo -n true``
   * - The workspace is mounted and writable
     - ``lxc exec fresh-project-a -- touch /workspace/.probe``, then remove the probe
   * - code-server answers through the tunnel
     - ``curl -sI http://127.0.0.1:8080/`` on the laptop, expecting an HTTP status line
   * - The GitHub CLI is authenticated
     - ``gh auth status``
   * - git-annex is installed
     - ``git annex version``
   * - The OpenCode service is healthy
     - ``opencode service status``
   * - The project's checks pass
     - ``python -m ruff check .`` and ``python -m pytest``, then the docs build with ``-W``
