#!/usr/bin/env bash
# Upload custom_components/eufy_omni to Home Assistant through the File editor add-on
# ingress API. Reads the HA long-lived token from ~/.claude.json at runtime; writes no secrets.
# Usage: bash tools/upload_component.sh [--restart]
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
COMP="$ROOT/custom_components/eufy_omni"
HA=https://anchored23.duckdns.org:8123
TOKEN=$(grep -o '"Authorization": *"Bearer [^"]*"' ~/.claude.json | head -1 | sed 's/.*Bearer //; s/"//')
export MSYS_NO_PATHCONV=1

tmp="$ROOT/.deploy_tmp"
mkdir -p "$tmp"
trap 'rm -rf "$tmp"' EXIT
echo '{"type":"supervisor/api","endpoint":"/ingress/session","method":"post"}' > "$tmp/cmds.txt"
echo '{"type":"supervisor/api","endpoint":"/addons/core_configurator/info","method":"get"}' >> "$tmp/cmds.txt"
powershell -NoProfile -ExecutionPolicy Bypass -File "C:/dev/HA Claude/ha-ws.ps1" -CommandsFile "$(cygpath -w "$tmp/cmds.txt")" > "$tmp/ws.jsonl"
SESSION=$(sed -n 1p "$tmp/ws.jsonl" | grep -o '"session":"[^"]*"' | sed 's/"session":"//; s/"//')
FE=$(sed -n 2p "$tmp/ws.jsonl" | grep -o '"ingress_url":"[^"]*"' | sed 's/"ingress_url":"//; s/"\/\?$//')
[ -n "$SESSION" ] && [ -n "$FE" ] || { echo "could not open ingress session"; exit 1; }
API="$HA$FE/api"
BASE=/homeassistant/custom_components/eufy_omni

# /api/newfolder wants the parent as `path` and the new folder as `name`.
mkdir_remote() {
  local parent name
  parent=$(dirname "$1"); name=$(basename "$1")
  curl -s -b "ingress_session=$SESSION" -X POST "$API/newfolder" \
      --data-urlencode "path=$parent" --data-urlencode "name=$name" >/dev/null || true
}

mkdir_remote /homeassistant/custom_components
mkdir_remote "$BASE"
cd "$COMP"
find . -type d ! -name '__pycache__' ! -path '*/__pycache__/*' | sed 's#^\./##' | grep -v '^\.$' | sort | while read -r d; do
  mkdir_remote "$BASE/$d"
done
count=0
while IFS= read -r f; do
  rel="${f#./}"
  resp=$(curl -s -b "ingress_session=$SESSION" -X POST "$API/save" \
      --data-urlencode "filename=$BASE/$rel" --data-urlencode "text@$f")
  case "$resp" in
    *'"error": true'*|'') echo "FAILED $rel: $resp"; exit 1 ;;
  esac
  count=$((count+1))
done < <(find . -type f ! -path '*/__pycache__/*' ! -name '*.pyc' | sort)
echo "uploaded $count files to $BASE"
curl -s -b "ingress_session=$SESSION" "$API/listdir?path=$BASE" | grep -oE '"name": *"[^"]*"' | tr '\n' ' '; echo

if [ "${1:-}" = "--restart" ]; then
  echo "restarting Home Assistant Core"
  curl -s -X POST -H "Authorization: Bearer $TOKEN" "$HA/api/services/homeassistant/restart" >/dev/null
fi
