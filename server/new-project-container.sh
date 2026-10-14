#!/usr/bin/env bash
# Create one project container from the base container, as the host and containers guide
# describes it: copy the base, start the copy, mount the project's workspace, forward the IDE
# port, and write a .code-workspace file into the workspace. The base is fresh-base, and the IDE
# listens on port 8080 inside the container.
#
#   new-project-container.sh --dry-run NAME WORKSPACE PORT   print the plan, and run no command
#   new-project-container.sh --apply NAME WORKSPACE PORT     run the plan on a host
#   new-project-container.sh --help                          print usage
#
# NAME is the container name: lowercase letters, digits, and hyphens. WORKSPACE is an existing
# absolute host directory. PORT is a host loopback port from 1024 to 65535. --apply stops before
# any change if NAME exists, if another container already forwards PORT, or if the workspace
# file exists. A maintainer runs --apply on a lab host.
# Exit status: 0 on success, 1 when a check or a step fails, and 2 for a usage error.
set -u

readonly BASE="fresh-base"
readonly IDE_PORT="8080"

usage() {
    printf 'usage: %s (--dry-run | --apply) NAME WORKSPACE PORT\n' "${0##*/}"
    printf '       %s --help\n' "${0##*/}"
}

bad_args() {
    printf '%s\n' "$1" >&2
    usage >&2
    exit 2
}

fail() {
    printf '%s\n' "$1" >&2
    exit 1
}

valid_name() {
    [[ $1 =~ ^[a-z][a-z0-9-]*$ ]] && (( ${#1} <= 63 ))
}

valid_port() {
    [[ $1 =~ ^[1-9][0-9]{3,4}$ ]] && (( $1 >= 1024 && $1 <= 65535 ))
}

plan() {
    local source_arg=""
    printf -v source_arg 'source=%q' "$WORKSPACE"
    printf '# read first, and stop before any change if the name, the port, or the file is taken\n'
    printf '# on the host\n'
    printf 'lxc copy %s %s\n' "$BASE" "$NAME"
    printf 'lxc start %s\n' "$NAME"
    printf 'lxc config device add %s workspace disk %s path=/workspace shift=true\n' \
        "$NAME" "$source_arg"
    printf 'lxc config device add %s ide proxy listen=tcp:127.0.0.1:%s connect=tcp:127.0.0.1:%s\n' \
        "$NAME" "$PORT" "$IDE_PORT"
    printf '# write %s. The IDE opens it as /workspace/%s.code-workspace\n' \
        "$FILE" "$NAME"
    printf '# on your laptop: ssh -N -L %s:127.0.0.1:%s <user>@<dev-host>\n' "$IDE_PORT" "$PORT"
    printf '# then open http://127.0.0.1:%s in the laptop browser\n' "$IDE_PORT"
}

check_free() {
    local -a names=()
    local names_csv="" name="" devices="" line=""
    names_csv=$(lxc list -c n --format csv) ||
        fail "could not list the containers. Nothing was changed."
    while IFS= read -r name; do
        if [[ -n $name ]]; then
            names+=("$name")
        fi
    done <<< "$names_csv"
    for name in "${names[@]}"; do
        if [[ $name == "$NAME" ]]; then
            fail "container $NAME already exists. Nothing was changed."
        fi
    done
    for name in "${names[@]}"; do
        devices=$(lxc config device show "$name") ||
            fail "could not read the devices of $name. Nothing was changed."
        while IFS= read -r line; do
            if [[ $line == *"listen: tcp:127.0.0.1:$PORT" ]]; then
                fail "port $PORT is already forwarded by $name. Nothing was changed."
            fi
        done <<< "$devices"
    done
}

step() {
    local description="$1"
    shift
    if ! "$@"; then
        fail "failed: $description. The steps before it were applied, and the script does not undo them."
    fi
}

write_workspace_file() {
    printf '{\n  "folders": [\n    {\n      "name": "%s",\n      "path": "."\n    }\n  ]\n}\n' \
        "$NAME" >"$FILE" || fail "failed: write $FILE"
}

apply() {
    check_free
    if [[ -e $FILE ]]; then
        fail "$FILE already exists. Nothing was changed."
    fi
    step "copy the base" lxc copy "$BASE" "$NAME"
    step "start $NAME" lxc start "$NAME"
    step "mount the workspace" \
        lxc config device add "$NAME" workspace disk "source=$WORKSPACE" path=/workspace shift=true
    step "forward the IDE port" \
        lxc config device add "$NAME" ide proxy "listen=tcp:127.0.0.1:$PORT" \
        "connect=tcp:127.0.0.1:$IDE_PORT"
    write_workspace_file
    printf '# created %s. The plan shows how to open its IDE from the laptop.\n' "$NAME"
}

if [[ ${1:-} == --help || ${1:-} == -h ]]; then
    usage
    exit 0
fi
if [[ $# -ne 4 ]]; then
    bad_args "expected a mode, NAME, WORKSPACE, and PORT"
fi

MODE="$1"
NAME="$2"
WORKSPACE="$3"
PORT="$4"

case "$MODE" in
    --dry-run | --apply) ;;
    *) bad_args "unknown mode: $MODE" ;;
esac
if ! valid_name "$NAME"; then
    bad_args "NAME must start with a letter, use letters, digits, and hyphens, and be at most 63 characters"
fi
if ! valid_port "$PORT"; then
    bad_args "PORT must be a number from 1024 to 65535"
fi
if [[ $WORKSPACE != /* ]]; then
    bad_args "WORKSPACE must be an absolute path"
fi
if [[ ! -d $WORKSPACE ]]; then
    bad_args "WORKSPACE must be an existing directory"
fi

FILE="$WORKSPACE/$NAME.code-workspace"
if [[ $MODE == --dry-run ]]; then
    plan
else
    apply
fi
