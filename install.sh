#!/usr/bin/env bash
# /* ---- 💫 4NDR0TRASHER: HUD REBRANDING & DEPLOYMENT MATRIX 💫 ---- */
# Architecture: Statistically pure, offensive POSIX orchestration
# Version: 1.6.0 (3lectric Glass Edition)
# ----------------------------------------------------------------------

set -euo pipefail
IFS=$'\n\t'

SOURCE_DIR="$(cd -- "$(dirname -- "$(readlink -f "${BASH_SOURCE[0]:-$0}")")" && pwd -P)"
SYS_ROOT="/"
GLYPH_SRC="${SOURCE_DIR}/4ndr0666_glyph.png"

# Target Definitions
readonly PKG_SHARE="${SYS_ROOT}usr/share/4ndr0trasher"
readonly IMG_DIR="${PKG_SHARE}/images"
readonly ICON_DIR="${SYS_ROOT}usr/share/icons/hicolor/scalable/apps"

log_info()  { printf "\033[1;32m[INFO]\033[0m  %s\n" "$*"; }
log_error() { printf "\033[1;31m[ERROR]\033[0m %s\n" "$*"; }

if [[ "${EUID}" -ne 0 ]]; then
    log_error "Execute with sudo."
    exit 1
fi

# 1. ──────────────── GEOMETRIC ASSET GENERATION ────────────────
log_info "Verifying geometric lineage: ${GLYPH_SRC}"
if [[ ! -f "$GLYPH_SRC" ]]; then
    log_error "Source glyph missing. Execution halted."
    exit 1
fi

# Identify scaling tool
MAGICK_CMD=$(command -v magick || command -v convert || true)
if [[ -z "$MAGICK_CMD" ]]; then
    log_error "ImageMagick not found. Required for asset generation."
    exit 1
fi

generate_asset() {
    local out="$1" size="$2"
    log_info "Scaling -> ${size} | ${out##*/}"
    mkdir -p "$(dirname "$out")"
    $MAGICK_CMD "$GLYPH_SRC" -interpolate Nearest -filter point -resize "$size" "$out"
}

# Generate sized assets into the local tree before sync
generate_asset "${SOURCE_DIR}/usr/share/4ndr0trasher/images/4ndr0666os-icon.png" "512x512"
generate_asset "${SOURCE_DIR}/usr/share/4ndr0trasher/images/4ndr0trasher-logo.png" "235x235"
generate_asset "${SOURCE_DIR}/usr/share/4ndr0trasher/images/4ndr0trasher-logo-bomb.png" "235x235"
generate_asset "${SOURCE_DIR}/usr/share/4ndr0trasher/images/panel.png" "700x40!"
generate_asset "${SOURCE_DIR}/usr/share/icons/hicolor/scalable/apps/4ndr0trasher.png" "512x512"

# 2. ──────────────── ATOMIC FILESYSTEM SYNC ────────────────
log_info "Synchronizing project matrix to ${SYS_ROOT}..."

# Sync usr/local/bin
mkdir -p "${SYS_ROOT}usr/local/bin"
cp -v "${SOURCE_DIR}/usr/local/bin/4ndr0trasher" "${SYS_ROOT}usr/local/bin/"
chmod 755 "${SYS_ROOT}usr/local/bin/4ndr0trasher"

# Sync Payload
mkdir -p "$PKG_SHARE"
rsync -av --delete --exclude '.git/' "${SOURCE_DIR}/usr/share/4ndr0trasher/" "$PKG_SHARE/"
cp -v "${SOURCE_DIR}/style.css" "$PKG_SHARE/" # Ensure style.css is available to python

# Sync XDG integration
cp -v "${SOURCE_DIR}/usr/share/applications/4ndr0trasher.desktop" "${SYS_ROOT}usr/share/applications/"
cp -v "${SOURCE_DIR}/usr/share/polkit-1/actions/org.4ndr0666os.pkexec.4ndr0trasher.policy" "${SYS_ROOT}usr/share/polkit-1/actions/"
cp -v "${SOURCE_DIR}/usr/share/icons/hicolor/scalable/apps/4ndr0trasher.png" "$ICON_DIR/"

# 3. ──────────────── THEME HOTFIX INJECTION ────────────────
log_info "Applying CSS syntax hotfix to 4ndr0trasher.py..."
# Replaces 'background-image: none !important;' with 'background: none !important;'
# to prevent the "Junk at end of value" GTK 3 CSS parser error.
sed -i 's/background-image: none !important;/background: none !important;/g' "${PKG_SHARE}/4ndr0trasher.py"

# 4. ──────────────── PERMISSIONS & CACHES ────────────────
log_info "Enforcing permissions matrix..."
chmod 755 "${PKG_SHARE}/4ndr0trasher.py"
chmod 644 "${PKG_SHARE}/Functions.py"
chmod 644 "${PKG_SHARE}/GUI.py"
chmod 644 "${PKG_SHARE}/style.css"

# Deploy Sudoers Rule
SUDOERS_TMP="$(mktemp)"
echo "%wheel ALL=(root) NOPASSWD: ${PKG_SHARE}/4ndr0trasher.py" > "${SUDOERS_TMP}"
if visudo -c -f "${SUDOERS_TMP}" &>/dev/null; then
    install -m 0440 -o root -g root "${SUDOERS_TMP}" "/etc/sudoers.d/4ndr0trasher"
fi
rm -f "${SUDOERS_TMP}"

# Refresh System Caches
update-desktop-database -q "${SYS_ROOT}usr/share/applications" || true
if command -v gtk-update-icon-cache &>/dev/null; then
    gtk-update-icon-cache -q -t -f "${SYS_ROOT}usr/share/icons/hicolor" || true
fi

log_info "4ndr0trasher: 3lectric Glass Matrix deployed successfully."
