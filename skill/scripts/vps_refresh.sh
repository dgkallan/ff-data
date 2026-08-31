#!/bin/bash
# TX2025 pre-draft data refresh. Run on the VPS: bash /opt/ff/refresh.sh
set -u
cd /opt/ff || exit 1
set -a; . ./.env; set +a
[ -z "${FP_API_KEY:-}" ] && { echo "FP_API_KEY missing from /opt/ff/.env"; exit 1; }
S=2026; B="https://api.fantasypros.com/public/v2/json/nfl"
mkdir -p fp; ok=1
echo "== projections =="
c=$(curl -s -o fp/projections-$S.json -w "%{http_code}" -H "x-api-key: $FP_API_KEY" \
    "$B/$S/projections?positions=QB:RB:WR:TE&week=0")
echo "  HTTP $c  $(python3 -c "
import json;d=json.load(open('fp/projections-$S.json'));print(len(d['players']),'players, week',d['week'])" 2>/dev/null || echo FAILED)"
[ "$c" = "200" ] || ok=0
for P in QB RB WR TE; do
  c=$(curl -s -o fp/spread-$S-$P.json -w "%{http_code}" -H "x-api-key: $FP_API_KEY" \
      "$B/$S/consensus-rankings?position=$P&scoring=PPR")
  echo "  $P HTTP $c  $(python3 -c "
import json;d=json.load(open('fp/spread-$S-$P.json'));print(len(d['players']),'players, updated',d.get('last_updated'),',',d.get('total_experts'),'experts')" 2>/dev/null || echo FAILED)"
  [ "$c" = "200" ] || ok=0
done
tar czf fp.tar.gz fp/
echo
if [ $ok = 1 ]; then
  echo "OK. Files in /opt/ff/fp/ and /opt/ff/fp.tar.gz"
  echo "From your LAPTOP:  scp -r root@2.25.173.69:/opt/ff/fp ~/Downloads/"
  echo "Then upload the 5 files to Claude."
else
  echo "ERRORS above. If 403: key expired or revoked -> fall back to CSV export."
fi
