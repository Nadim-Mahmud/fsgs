#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
ROOT_DIR="${1:-${REPO_ROOT}/data/cameleon}"

if (( $# > 0 )); then
    shift
fi

command -v xvfb-run >/dev/null || {
    echo "xvfb-run is not installed; rebuild the Docker image." >&2
    exit 1
}

# Use Qt's X11 backend with the virtual display, including in older containers.
export QT_QPA_PLATFORM=xcb
exec xvfb-run -a -s "-screen 0 1920x1080x24" \
    python "${REPO_ROOT}/convert.py" -s "${ROOT_DIR}" "$@"
