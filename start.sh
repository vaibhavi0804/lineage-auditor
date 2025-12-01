#!/usr/bin/env bash
# start.sh - ensure app package is importable then exec uvicorn
set -euo pipefail

# make PYTHONPATH absolute to be safe
export PYTHONPATH="${PYTHONPATH:-}${PYTHONPATH:+:}$PWD/src/backend"

echo "Starting with PYTHONPATH=$PYTHONPATH"
exec python -m uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"
