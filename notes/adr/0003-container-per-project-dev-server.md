# ADR 0003: One container per project on a lab dev server

Status: accepted
Date: 2026-10-13
Issues: #7

## Context

Coding agents work better with a small, relevant context. A shared workstation accumulates unrelated repositories, credentials, and scratch data, so an agent in one project can see material from another. The lab also needs a development environment that other people can reproduce.

## Decision

- Each project gets its own LXD container, copied from a base container that holds the common tools. The container is the agent's workspace.
- The workspace holds only that project's repositories and its scratch directory. Data that must not be visible to every project gets its own mount, or stays out of the container.
- The IDE runs inside the container. It is reached through a loopback port forward and an SSH tunnel, not through a public listener.
- The agent CLI runs in a terminal inside the container, with its working directory pinned to the project root.
- Containers provide context hygiene and reproducibility. They are not a security boundary for hostile code. Untrusted code runs in a virtual machine.

## Consequences

- Rebuilding a project environment means copying the base container again, not repairing a shared machine.
- Members of the `lxd` group have root-equivalent access to the host. Membership is a trust decision, and the security guide says so.
- Setup takes time. The dev server guide makes it repeatable, and the P2 scripts will automate the steps.

## Alternatives considered

- Docker or devcontainers on a laptop. Viable for a single developer; the guide names this as the minimum viable variant.
- One shared workstation with virtual environments. Rejected: context and credentials leak between projects.
