#!/usr/bin/env bash
# File: install.sh
# Description: Professional installer for 4ndr0trasher Module
# Architecture: Superset-compliant / Atomic Deployment

set -euo pipefail
IFS=$'\n\t'

SOURCE_DIR="$(cd -- "$(dirname -- "$(readlink -f "${BASH_SOURCE[0]:-$0}")")" && pwd -P)"
SYS_ROOT="/"
DRY_RUN=false

readonly SUDOERS_DROP="/etc/sudoers.d/4ndr0trasher"
readonly PAYLOAD_PATH="/usr/share/4ndr0trasher/4ndr0trasher.py"
readonly LOG_DIR="/var/log/4ndr0trasher/logs"

log_info()  { printf "\033[1;32m[INFO]\033[0m  %s\n" "$*"; }
log_error() { printf "\033[1;31m[ERROR]\033[0m %s\n" "$*"; }

cleanup() {
    if [[ -n "${SUDOERS_TMP:-}" && -f "${SUDOERS_TMP}" ]]; then
        rm -f "${SUDOERS_TMP}"
    fi
}
trap cleanup EXIT INT TERM

run() {
    if [[ "${DRY_RUN}" == "true" ]]; then
        printf "\033[1;34m[DRY-RUN]\033[0m Would run: %s\n" "$*"
    else
        printf "\033[1;30m[EXEC]\033[0m %s\n" "$*"
        "$@"
    fi
}

if [[ "${EUID}" -ne 0 ]]; then
    log_error "Execute with sudo."
    exit 1
fi

log_info "Initializing 4ndr0trasher Deployment..."

# 1. Sync Execution Wrapper
run mkdir -p "${SYS_ROOT}usr/local/bin"
run cp -v "${SOURCE_DIR}/usr/local/bin/4ndr0trasher" "${SYS_ROOT}usr/local/bin/"
run chmod 755 "${SYS_ROOT}usr/local/bin/4ndr0trasher"

# 2. Sync Payload Architecture
run mkdir -p "${SYS_ROOT}usr/share/4ndr0trasher"
run rsync -av --exclude '.git/' "${SOURCE_DIR}/usr/share/4ndr0trasher/" "${SYS_ROOT}usr/share/4ndr0trasher/"
run cp -v "${SOURCE_DIR}/usr/share/applications/4ndr0trasher.desktop" "${SYS_ROOT}usr/share/applications/"
run cp -v "${SOURCE_DIR}/usr/share/polkit-1/actions/org.4ndr0666os.pkexec.4ndr0trasher.policy" "${SYS_ROOT}usr/share/polkit-1/actions/"

# 3. Create Log Infrastructure
run mkdir -p "${SYS_ROOT}${LOG_DIR}"
run chmod 755 "${SYS_ROOT}${LOG_DIR}"

# 4. Enforce Permissions
run chmod 755 "${SYS_ROOT}${PAYLOAD_PATH}"
run chmod 644 "${SYS_ROOT}usr/share/4ndr0trasher/Functions.py"
run chmod 644 "${SYS_ROOT}usr/share/4ndr0trasher/GUI.py"

# 5. Deploy Sudoers Rule
SUDOERS_TMP="$(mktemp)"
echo "%wheel ALL=(root) NOPASSWD: ${PAYLOAD_PATH}" > "${SUDOERS_TMP}"
if visudo -c -f "${SUDOERS_TMP}" &>/dev/null; then
    install -m 0440 -o root -g root "${SUDOERS_TMP}" "${SUDOERS_DROP}"
    log_info "Sudoers rule validated."
else
    log_error "visudo syntax error."
    exit 1
fi

# 6. Update Caches
if command -v gtk-update-icon-cache &>/dev/null; then
    run gtk-update-icon-cache -q -t -f "${SYS_ROOT}usr/share/icons/hicolor"
fi
if command -v update-desktop-database &>/dev/null; then
    run update-desktop-database -q "${SYS_ROOT}usr/share/applications"
fi

log_info "4ndr0trasher operational."
