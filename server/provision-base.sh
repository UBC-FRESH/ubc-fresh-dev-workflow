#!/usr/bin/env bash
# Build the LXD base container that the host and containers guide describes, or print the
# commands that build it. The base holds the common tools and no project data.
#
#   --dry-run   print the guide's base container commands, in the guide's order, and run none
#   --apply     create the base if it is missing, and install any missing common packages
#   --help      print usage
#
# Run --apply on a lab host only when a maintainer approves it. The guide's login shell, its
# exit, and its final stop are printed in the plan but not run, because a person does them.
# Exit status: 0 on success, 1 when a step fails, and 2 for a usage error.
set -u

readonly BASE="fresh-base"
readonly IMAGE="ubuntu:24.04"
PACKAGES="git git-annex python3-venv python3-pip build-essential"
PACKAGES="$PACKAGES curl ca-certificates jq shellcheck"

usage() {
    printf 'usage: %s --dry-run | --apply | --help\n' "${0##*/}"
}

plan() {
    printf '# on the host\n'
    printf 'lxc launch %s %s\n' "$IMAGE" "$BASE"
    printf 'lxc exec %s -- cloud-init status --wait\n' "$BASE"
    printf '# the guide opens a login shell in the base here. --apply runs the next steps there.\n'
    printf 'lxc exec %s -- sudo --login --user ubuntu\n' "$BASE"
    printf '# in the base, as ubuntu\n'
    printf 'sudo apt-get update\n'
    printf 'sudo apt-get install -y %s\n' "$PACKAGES"
    printf '# by hand, as ide-agents-and-models describes: the GitHub CLI, code-server,\n'
    printf '# OpenCode, and DataLad. The guide then leaves the shell and stops the base.\n'
    printf 'exit\n'
    printf 'lxc stop %s\n' "$BASE"
}

run_in_base() {
    lxc exec "$BASE" -- sudo --login --user ubuntu bash -c "$1"
}

step() {
    local description="$1"
    shift
    if ! "$@"; then
        printf 'failed: %s\n' "$description" >&2
        exit 1
    fi
}

packages_installed() {
    run_in_base "dpkg -s $PACKAGES" >/dev/null 2>&1
}

apply() {
    if lxc info "$BASE" >/dev/null 2>&1; then
        printf '# %s exists\n' "$BASE"
    else
        step "launch the base" lxc launch "$IMAGE" "$BASE"
        step "wait for cloud-init" lxc exec "$BASE" -- cloud-init status --wait
    fi
    if packages_installed; then
        printf '# the common packages are installed. Nothing to do.\n'
        return 0
    fi
    step "update the package lists" run_in_base "sudo apt-get update"
    step "install the common packages" run_in_base "sudo apt-get install -y $PACKAGES"
    printf '# the common packages are installed. By hand, next: the GitHub CLI, code-server,\n'
    printf '# OpenCode, and DataLad. Then stop the base.\n'
}

if [[ $# -ne 1 ]]; then
    usage >&2
    exit 2
fi

case "$1" in
    --dry-run)
        plan
        ;;
    --apply)
        apply
        ;;
    -h | --help)
        usage
        ;;
    *)
        usage >&2
        exit 2
        ;;
esac
