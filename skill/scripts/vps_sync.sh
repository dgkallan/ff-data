#!/bin/bash
# /opt/ff/sync.sh — pull FantasyPros NFL data, push to the GitHub relay.
# Runs on David's VPS via cron. Claude's sandbox can reach raw.githubusercontent.com
# but NOT api.fantasypros.com or this box, so this script is the bridge.
#
# SETUP (once):
#   1. Create a PUBLIC repo, e.g. github.com/<you>/ff-data
#   2. On the VPS:
#        ssh-keygen -t ed25519 -f ~/.ssh/ffdata -N ""
#        cat ~/.ssh/ffdata.pub          # add to repo -> Settings -> Deploy keys -> Allow write
#        git clone git@github.com:<you>/ff-data.git /opt/ff/repo
#        git -C /opt/ff/repo config user.email "ff@localhost"
#        git -C /opt/ff/repo config user.name  "ff-sync"
#      and add to ~/.ssh/config:
#        Host github.com
#          IdentityFile ~/.ssh/ffdata
#   3. chmod +x /opt/ff/sync.sh && /opt/ff/sync.sh    # test it
#   4. crontab -e:
#        0 6 * * 4  /opt/ff/sync.sh >> /opt/ff/sync.log 2>&1   # Thursday 6am
#        0 6 * * 0  /opt/ff/sync.sh >> /opt/ff/sync.log 2>&1   # Sunday 6am
#
# The API key never leaves this box and is never written into the repo.

set -uo pipefail
cd /opt/ff || exit 1
set -a; . ./.env; set +a
[ -z "${FP_API_KEY:-}" ] && { echo "$(date -Is) FP_API_KEY missing"; exit 1; }

S=2026
B="https://api.fantasypros.com/public/v2/json/nfl"
R=/opt/ff/repo/nfl
D=$(date +%F)
mkdir -p "$R" || exit 1
ok=1

# current NFL week: 0 until the season starts, then weeks since Sep 8 2026
WK=$(python3 - <<'PY'
import datetime
k=(datetime.date.today()-datetime.date(2026,9,8)).days
print(0 if k<0 else min(18,k//7+1))
PY
)
echo "$(date -Is) sync start, week=$WK"

fetch () {  # fetch <outfile> <url>
  code=$(curl -s -o "$R/$1.tmp" -w "%{http_code}" --max-time 60 \
         -H "x-api-key: $FP_API_KEY" "$2")
  if [ "$code" = "200" ] && python3 -c "import json,sys; json.load(open('$R/$1.tmp'))" 2>/dev/null; then
    mv "$R/$1.tmp" "$R/$1"; echo "  OK   $1"
  else
    rm -f "$R/$1.tmp"; echo "  FAIL $1 (HTTP $code)"; ok=0
  fi
}

# --- season-long: trade valuation, big board ---
fetch "projections-season.json" "$B/$S/projections?positions=QB:RB:WR:TE&week=0"

# --- rest of season: WAIVER valuation (what he gains for the games left) ---
[ "$WK" -gt 0 ] && fetch "projections-ros.json" "$B/$S/projections?positions=QB:RB:WR:TE&ros=1"

# --- this week: LINEUP decisions. never use season totals for start/sit ---
[ "$WK" -gt 0 ] && fetch "projections-week$WK.json" "$B/$S/projections?positions=QB:RB:WR:TE&week=$WK"

# --- consensus rankings: ECR, tier, expert spread (upside/bust) ---
for P in QB RB WR TE; do
  fetch "ecr-$P.json" "$B/$S/consensus-rankings?position=$P&scoring=PPR&week=$WK"
done
# --- IDP for Empty Stadiums (2 DP starters) ---
for P in LB DL DB; do
  fetch "ecr-idp-$P.json" "$B/$S/consensus-rankings?position=$P&scoring=PPR&include_idp=true&week=$WK"
done

# --- injuries with play probability, and news ---
fetch "injuries.json" "$B/injuries?year=$S&week=$WK&include_probabilities=true"
fetch "news.json"     "$B/news?limit=120"

python3 - "$R" "$D" "$WK" <<'PY'
import json,os,sys,datetime
R,D,WK=sys.argv[1],sys.argv[2],sys.argv[3]
m={"pulled":datetime.datetime.utcnow().isoformat()+"Z","date":D,"week":int(WK),"files":{}}
for f in sorted(os.listdir(R)):
    if f.endswith(".json") and f!="manifest.json":
        p=os.path.join(R,f)
        try:
            d=json.load(open(p)); n=len(d.get("players",d) if isinstance(d,(dict,list)) else [])
        except Exception: n=-1
        m["files"][f]={"bytes":os.path.getsize(p),"records":n}
json.dump(m,open(os.path.join(R,"manifest.json"),"w"),indent=1)
print("  manifest:",len(m["files"]),"files")
PY

cd /opt/ff/repo || exit 1
git add -A nfl
if git diff --cached --quiet; then
  echo "$(date -Is) no changes"
else
  git commit -q -m "nfl data $D wk$WK" && git push -q origin main \
    && echo "$(date -Is) pushed" || { echo "$(date -Is) PUSH FAILED"; ok=0; }
fi
[ "$ok" = 1 ] && echo "$(date -Is) sync OK" || echo "$(date -Is) sync had errors"
