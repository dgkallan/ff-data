#!/usr/bin/env bash
# Pull ADP by SOURCE from FantasyPros so we can fingerprint which ranking list
# each league manager actually drafts from.
#
# WHY: in the Aug 2026 TX2025 draft the room drafted QBs at 0.935 Spearman
# correlation with CBS positional rank. That made Bo Nix (CBS QB10 / our QB3)
# and Tyler Shough (CBS QB8 / our QB5) free. We could only test CBS and
# FantasyPros because those were the only two lists we had. With per-source ADP
# we can fingerprint all twelve managers.
#
# Run on the VPS (has the API key). Writes into the ff-data repo.
#   bash /opt/ff/pull_adp_sources.sh
set -euo pipefail
source /opt/ff/.env          # FP_API_KEY
BASE="https://api.fantasypros.com/public/v2/json"
OUT="/opt/ff/repo/nfl"
SEASON="${SEASON:-2026}"
mkdir -p "$OUT"

# FantasyPros exposes ADP filtered by host site. Known values for `filters`:
#   adp        = FantasyPros consensus ADP
#   espn, yahoo, cbs, sleeper, nfl, rtsports  = that site's ADP
for SRC in adp espn yahoo cbs sleeper nfl rtsports; do
  echo -n "  ADP:$SRC ... "
  if curl -sf --max-time 25 -H "x-api-key: $FP_API_KEY" \
       "$BASE/nfl/$SEASON/adp?filters=$SRC&position=ALL" \
       -o "$OUT/adp-$SRC.json"; then
    N=$(python3 -c "import json,sys;d=json.load(open('$OUT/adp-$SRC.json'));print(len(d.get('players',[])))" 2>/dev/null || echo 0)
    echo "OK ($N players)"
  else
    echo "FAILED — endpoint may differ; check FantasyPros API docs"
    rm -f "$OUT/adp-$SRC.json"
  fi
  sleep 2   # rate limit
done

cd /opt/ff/repo
git add -A nfl
git commit -q -m "adp by source $(date +%F)" || true
(git pull -q --rebase origin main || true)
git push -q origin main && echo "pushed"
