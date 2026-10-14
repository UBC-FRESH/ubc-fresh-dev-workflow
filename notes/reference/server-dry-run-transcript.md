# Dry-run transcript of the server scripts

Two of the server scripts have a dry-run mode, and it prints a plan without running any command.
This transcript is the committed output of those plans. `tests/test_server_transcript.py` runs each
command below from the repository root, and it fails when the output differs from this file. After
a deliberate change to a script, run each command, paste its output here, and review the diff. The
workspace path is an example, and a dry run does not require it to exist.

## server/provision-base.sh

```text
$ server/provision-base.sh --dry-run
# on the host
lxc launch ubuntu:24.04 fresh-base
lxc exec fresh-base -- cloud-init status --wait
# the guide opens a login shell in the base here. --apply runs the next steps there.
lxc exec fresh-base -- sudo --login --user ubuntu
# in the base, as ubuntu
sudo apt-get update
sudo apt-get install -y git git-annex python3-venv python3-pip build-essential curl ca-certificates jq shellcheck
# by hand, as ide-agents-and-models describes: the GitHub CLI, code-server,
# OpenCode, and DataLad. The guide then leaves the shell and stops the base.
exit
lxc stop fresh-base
```

## server/new-project-container.sh

```text
$ server/new-project-container.sh --dry-run fresh-project-a /srv/projects/project-a 18080
# read first, and stop before any change if the name, the port, or the file is taken
# on the host
lxc copy fresh-base fresh-project-a
lxc start fresh-project-a
lxc config device add fresh-project-a workspace disk source=/srv/projects/project-a path=/workspace shift=true
lxc config device add fresh-project-a ide proxy listen=tcp:127.0.0.1:18080 connect=tcp:127.0.0.1:8080
# write /srv/projects/project-a/fresh-project-a.code-workspace. The IDE opens it as /workspace/fresh-project-a.code-workspace
# on your laptop: ssh -N -L 8080:127.0.0.1:18080 <user>@<dev-host>
# then open http://127.0.0.1:8080 in the laptop browser
```
