#!/usr/bin/env bash
# 4ndr0666
set -euo pipefail
#
#                     💀 === GENERATE-ICONS.SH === 💀
# Desc: This file generates the icons for the 4ndr0trasher program using the 
# supplied psi glyph and env paths below.
# ------------------------------------------------------------

# GLOBAL CONSTANTS
SOURCE_GLYPH="4ndr0666_glyph.png"
if [[ ! -f "$SOURCE_GLYPH" ]]; then
    echo "[ERROR] Source glyph ($SOURCE_GLYPH) not found in CWD. Execution halted."
    exit 1
fi

# Define project root relative to script location
PROJECT_ROOT="$(pwd)"
IMG_DIR="${PROJECT_ROOT}/usr/share/4ndr0trasher/images"
ICON_DIR="${PROJECT_ROOT}/usr/share/icons/hicolor/scalable/apps"

# ──────────────────────────────────────────────────────────────────────────────
# 1. ASSET GENERATION MATRIX
# Logic: Map the 42x35 glyph to target dimensions using Nearest Neighbor.
# ──────────────────────────────────────────────────────────────────────────────

# CORE DIRECTIVE 3: Ruthless Resource Reclamation
# We utilize a dedicated temp tree for scaling operations.
TEMP_SCALING_DIR=$(mktemp -d)
trap 'rm -rf "$TEMP_SCALING_DIR" 2>/dev/null' EXIT INT TERM

generate_asset() {
    local target_path="$1"
    local size="$2" # Format: WxH

    echo "[INFO] Scaling glyph to ${size} -> ${target_path}"

    # Use magick (ImageMagick 7+) for aliased, sharp geometric scaling.
    # -interpolate Nearest -filter point ensures zero blurring of the glyph.
    if ! magick "$SOURCE_GLYPH" -interpolate Nearest -filter point -resize "$size" "$target_path"; then
        echo "[ERROR] Failed to scale asset to ${size}."
        exit 1
    fi
}

# ──────────────────────────────────────────────────────────────────────────────
# 2. ATOMIC PURGE & ALIGNMENT
# ──────────────────────────────────────────────────────────────────────────────

echo "[INFO] Initializing atomic rebranding of ${PROJECT_ROOT}..."

# A. Rebrand Application Icon (512x512)
# Replaces: arcolinux.png
generate_asset "${IMG_DIR}/4ndr0666os-icon.png" "512x512"

# B. Rebrand GUI Logo (235x235)
# Replaces: arcolinux-one-liner.png
generate_asset "${IMG_DIR}/4ndr0trasher-logo.png" "235x235"

# C. Rebrand Aggressive Purge Logo (235x235)
# Replaces: arcolinux-one-liner-bomb.png
generate_asset "${IMG_DIR}/4ndr0trasher-logo-bomb.png" "235x235"

# D. Rebrand UI Panel (700x40)
# Replaces: panel.png
# NOTE: This will aspect-stretch the glyph to fit the wide panel format.
generate_asset "${IMG_DIR}/panel.png" "700x40!"

# E. Rebrand XDG System Icon (512x512)
# Replaces: arcolinux-desktop-trasher.svg
# NOTE: Outputting as PNG for compatibility with current loader logic.
generate_asset "${ICON_DIR}/4ndr0trasher.png" "512x512"

# ──────────────────────────────────────────────────────────────────────────────
# 3. LEGACY PURGE
# Logic: Remove all files containing "arcolinux" to ensure zero orphaned refs.
# ──────────────────────────────────────────────────────────────────────────────

echo "[INFO] Purging legacy ArcoLinux naming from images and icons..."

# Purge from images directory
find "$IMG_DIR" -type f -name "*arcolinux*" -delete

# Purge legacy SVG from scalable apps
find "$ICON_DIR" -type f -name "*arcolinux*" -delete

echo "---------------------------------------------------------------------------"
echo "[SUCCESS] Rebranding Matrix Complete."
echo "[VERIFICATION] New Asset Map:"
ls -R "${PROJECT_ROOT}/usr/share/4ndr0trasher/images"
ls -R "${PROJECT_ROOT}/usr/share/icons/hicolor"
echo "---------------------------------------------------------------------------"
echo "[ACTION] Re-run sudo ./install.sh to deploy the rebranded filesystem."
