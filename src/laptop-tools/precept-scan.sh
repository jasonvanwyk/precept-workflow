#!/usr/bin/env bash
# precept-scan -- wrapper for network scans with automatic filing and DB registration.
#
# Usage:
#   precept-scan nmap <project> "<nmap args>"
#   precept-scan iperf3 <project> "<iperf3 args>"
#   precept-scan file <project> <description> <filepath>
#
# Runs the scan, saves output to {project}/docs/network/YYYY-MM-DD-{type}-{desc}.txt,
# SCPs to dev server, registers in SQLite via SSH, and git commits.
#
# Requires:
#   - SSH key auth to dev server (10.0.10.21 or ssh.meter-tracker.com)
#   - Projects directory at ~/Projects/

set -euo pipefail

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

DEV_SERVER="${PRECEPT_DEV_SERVER:-10.0.10.21}"
DEV_USER="${PRECEPT_DEV_USER:-jason}"
PROJECTS_DIR="${PROJECTS_DIR:-$HOME/Projects}"
REGISTER_SCRIPT="precept-workflow/src/telegram-bot/register-scan.py"
DB_PATH="\$HOME/.config/precept/precept.db"
DATE=$(date +%Y-%m-%d)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

die() { echo "ERROR: $*" >&2; exit 1; }

usage() {
    cat <<'EOF'
Usage:
  precept-scan nmap <project> "<nmap args>"
  precept-scan iperf3 <project> "<iperf3 args>"
  precept-scan file <project> <description> <filepath>

Examples:
  precept-scan nmap fairfield-water "10.0.10.0/24"
  precept-scan iperf3 fairfield-water "-c 10.0.10.1 -t 30"
  precept-scan file fairfield-water wifi-survey /tmp/results.csv
EOF
    exit 1
}

safe_name() {
    echo "$1" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9_-]/-/g' | sed 's/--*/-/g'
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

[[ $# -lt 3 ]] && usage

SCAN_TYPE="$1"
PROJECT="$2"
shift 2

PROJECT_DIR="$PROJECTS_DIR/$PROJECT"
NETWORK_DIR="$PROJECT_DIR/docs/network"
mkdir -p "$NETWORK_DIR"

case "$SCAN_TYPE" in
    nmap)
        ARGS="$*"
        DESC=$(safe_name "$(echo "$ARGS" | head -c 40)")
        OUTFILE="$NETWORK_DIR/${DATE}-nmap-${DESC}.txt"
        echo "Running: nmap $ARGS"
        echo "Output: $OUTFILE"
        echo "--- nmap scan: $DATE ---" > "$OUTFILE"
        echo "Command: nmap $ARGS" >> "$OUTFILE"
        echo "---" >> "$OUTFILE"
        nmap $ARGS >> "$OUTFILE" 2>&1 || true
        echo "Scan complete."
        ;;

    iperf3)
        ARGS="$*"
        DESC=$(safe_name "$(echo "$ARGS" | head -c 40)")
        OUTFILE="$NETWORK_DIR/${DATE}-iperf3-${DESC}.txt"
        echo "Running: iperf3 $ARGS"
        echo "Output: $OUTFILE"
        echo "--- iperf3 test: $DATE ---" > "$OUTFILE"
        echo "Command: iperf3 $ARGS" >> "$OUTFILE"
        echo "---" >> "$OUTFILE"
        iperf3 $ARGS >> "$OUTFILE" 2>&1 || true
        echo "Test complete."
        ;;

    file)
        [[ $# -lt 2 ]] && die "Usage: precept-scan file <project> <description> <filepath>"
        DESC=$(safe_name "$1")
        SOURCE="$2"
        [[ -f "$SOURCE" ]] || die "File not found: $SOURCE"
        EXT="${SOURCE##*.}"
        OUTFILE="$NETWORK_DIR/${DATE}-${DESC}.${EXT}"
        cp "$SOURCE" "$OUTFILE"
        echo "Filed: $OUTFILE"
        ;;

    *)
        die "Unknown scan type: $SCAN_TYPE (use nmap, iperf3, or file)"
        ;;
esac

# Git commit locally
if [[ -d "$PROJECT_DIR/.git" ]]; then
    cd "$PROJECT_DIR"
    git add "docs/network/$(basename "$OUTFILE")"
    git commit -m "Add ${SCAN_TYPE} scan: $(basename "$OUTFILE")" 2>/dev/null || true
    echo "Git committed."
fi

# SCP to dev server
REMOTE_PROJECT_DIR="$PROJECTS_DIR/$PROJECT"
echo "Copying to dev server..."
ssh "$DEV_USER@$DEV_SERVER" "mkdir -p '$REMOTE_PROJECT_DIR/docs/network'" 2>/dev/null || true
scp "$OUTFILE" "$DEV_USER@$DEV_SERVER:$REMOTE_PROJECT_DIR/docs/network/" 2>/dev/null && echo "Copied." || echo "SCP failed (dev server unreachable?)."

# Register in SQLite via SSH
echo "Registering in database..."
REMOTE_FILE="$REMOTE_PROJECT_DIR/docs/network/$(basename "$OUTFILE")"
ssh "$DEV_USER@$DEV_SERVER" "python3 ~/Projects/$REGISTER_SCRIPT '$PROJECT' '$SCAN_TYPE' '$REMOTE_FILE'" 2>/dev/null && echo "Registered." || echo "DB registration failed."

# Git commit on dev server too
ssh "$DEV_USER@$DEV_SERVER" "cd '$REMOTE_PROJECT_DIR' && git add 'docs/network/$(basename "$OUTFILE")' && git commit -m 'Add ${SCAN_TYPE} scan: $(basename "$OUTFILE")'" 2>/dev/null || true

echo "Done: $OUTFILE"
