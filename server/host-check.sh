#!/usr/bin/env bash
# Read-only checks of a lab host for the LXD dev server, as the host and containers guide
# describes it: the LXD snap, its channel, the lxd group, the daemon, and a storage pool.
# The script changes nothing. It runs only read commands, and it prints each check's name and
# state. Exit status: 0 when every check passes, 1 when a check fails, and 2 for a usage error.
set -u

if [[ $# -gt 0 ]]; then
    case "$1" in
        -h | --help)
            printf 'usage: %s [--help]\n' "${0##*/}"
            printf 'Runs the read-only host checks, and changes nothing on the host.\n'
            exit 0
            ;;
        *)
            printf 'usage: %s [--help]\n' "${0##*/}" >&2
            exit 2
            ;;
    esac
fi

failures=0

have() {
    command -v "$1" >/dev/null 2>&1
}

report() {
    local status="$1" name="$2" state="$3"
    printf '%s %s: %s\n' "$status" "$name" "$state"
    if [[ $status == FAIL ]]; then
        failures=$((failures + 1))
    fi
}

check_snap_installed() {
    local name="The LXD snap is installed"
    if ! have snap; then
        report FAIL "$name" "the snap command is not available"
    elif snap list lxd >/dev/null 2>&1; then
        report PASS "$name" "yes"
    else
        report FAIL "$name" "no"
    fi
}

check_snap_channel() {
    local name="The LXD snap tracks the latest/stable channel"
    local info="" line key value tracking=""
    if have snap; then
        info=$(snap info lxd 2>/dev/null) || info=""
    fi
    while IFS= read -r line; do
        read -r key value <<< "$line"
        if [[ $key == "tracking:" ]]; then
            tracking="$value"
        fi
    done <<< "$info"
    if [[ $tracking == "latest/stable" ]]; then
        report PASS "$name" "$tracking"
    elif [[ -n $tracking ]]; then
        report FAIL "$name" "tracks $tracking"
    else
        report FAIL "$name" "the tracked channel is not reported"
    fi
}

check_group() {
    local name="The current shell is in the lxd group"
    local groups=""
    groups=" $(id -Gn 2>/dev/null) "
    if [[ $groups == *" lxd "* ]]; then
        report PASS "$name" "yes"
    else
        report FAIL "$name" "no"
    fi
}

check_daemon() {
    local name="The LXD daemon is reachable"
    if have lxc && lxc list >/dev/null 2>&1; then
        report PASS "$name" "yes"
    else
        report FAIL "$name" "no"
    fi
}

check_storage() {
    local name="A storage pool exists"
    local pools="" row="" driver="" drivers="" count=0 _
    if have lxc; then
        pools=$(lxc storage list --format csv 2>/dev/null) || pools=""
    fi
    while IFS= read -r row; do
        if [[ -z $row ]]; then
            continue
        fi
        IFS=, read -r _ driver _ <<< "$row"
        count=$((count + 1))
        drivers="${drivers:+$drivers, }$driver"
    done <<< "$pools"
    if (( count > 0 )); then
        report PASS "$name" "$count pool(s), driver: $drivers"
    else
        report FAIL "$name" "none"
    fi
}

check_snap_installed
check_snap_channel
check_group
check_daemon
check_storage

if (( failures > 0 )); then
    exit 1
fi
exit 0
