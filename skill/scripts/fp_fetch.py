#!/usr/bin/env python3
"""Fetch FantasyPros projections + expert spread. RUNS ON DAVID'S VPS, not in Claude's sandbox.

Claude's sandbox is network-allowlisted to package registries and cannot reach
api.fantasypros.com. This script runs where the key lives; David uploads the
output JSON, or a cron job relays it (see RELAY at the bottom).

The API key is read from the environment and is NEVER printed, logged, or written
to output. If it is missing the script exits rather than prompting.

USAGE
    export $(grep -v '^#' /path/to/.env | xargs)     # or however .env is loaded
    python3 fp_fetch.py --season 2026 --out ./fp

WRITES
    fp/projections-<season>.json   full stat lines, all positions
    fp/spread-<season>-<pos>.json  ECR + tier + best/worst/avg expert rank

Endpoints (verified from FantasyPros API docs, Aug 2026):
    GET https://api.fantasypros.com/v2/json/nfl/{season}/projections
    GET https://api.fantasypros.com/public/v2/json/nfl/{season}/consensus-rankings
    auth header: x-api-key
"""
import os, sys, json, argparse, urllib.request, urllib.error, urllib.parse

KEY = os.environ.get("FP_API_KEY", "").strip()
UA = "kallan-ff/1.0"


def get(url, params=None):
    if params:
        url = url + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"x-api-key": KEY, "User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:300]
        # never echo the key, even on failure
        safe = url.replace(KEY, "<KEY>") if KEY else url
        print(f"  HTTP {e.code} on {safe}\n    {body}", file=sys.stderr)
        if e.code in (401, 403):
            print("    -> key rejected. Check FP_API_KEY and that the plan covers this endpoint.", file=sys.stderr)
        if e.code == 404:
            print("    -> endpoint shape wrong for this key tier; try the other base URL below.", file=sys.stderr)
        return None
    except Exception as e:
        print(f"  {type(e).__name__}: {e}", file=sys.stderr)
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--season", default="2026")
    ap.add_argument("--out", default="./fp")
    ap.add_argument("--scoring", default="PPR")
    a = ap.parse_args()

    if not KEY:
        sys.exit("FP_API_KEY not set in environment. Load .env first. Not prompting for it.")
    os.makedirs(a.out, exist_ok=True)
    ok = True

    # ---- projections: the stat lines the board is built from ----
    print("projections...")
    proj = None
    for base in ("https://api.fantasypros.com/v2/json/nfl/%s/projections" % a.season,
                 "https://api.fantasypros.com/public/v2/json/nfl/%s/projections" % a.season):
        proj = get(base, {"position": "ALL", "week": "0", "scoring": a.scoring})
        if proj:
            print(f"  OK via {base.split('/nfl/')[0]}")
            break
    if proj:
        p = os.path.join(a.out, f"projections-{a.season}.json")
        json.dump(proj, open(p, "w"))
        n = len(proj.get("players", []))
        print(f"  wrote {p}  ({n} players)")
        pos = {}
        for pl in proj.get("players", []):
            pos[pl.get("position_id", "?")] = pos.get(pl.get("position_id", "?"), 0) + 1
        print("  by position:", dict(sorted(pos.items())))
        smp = next((x for x in proj.get("players", []) if x.get("position_id") == "QB"), None)
        if smp:
            print(f"  sample QB {smp.get('name')}: {json.dumps(smp.get('stats', {}))[:200]}")
    else:
        ok = False
        print("  FAILED — fall back to CSV export from the projections pages", file=sys.stderr)

    # ---- consensus rankings: ECR, tier, and the expert spread (upside/bust) ----
    for position in ("QB", "RB", "WR", "TE"):
        print(f"spread {position}...")
        d = get("https://api.fantasypros.com/public/v2/json/nfl/%s/consensus-rankings" % a.season,
                {"position": position, "scoring": a.scoring, "type": "draft"})
        if d:
            p = os.path.join(a.out, f"spread-{a.season}-{position}.json")
            json.dump(d, open(p, "w"))
            pl = d.get("players", [])
            print(f"  wrote {p}  ({len(pl)} players)")
            if pl:
                k = [x for x in pl[0].keys() if "rank" in x.lower() or x in ("tier", "player_name")]
                print(f"  fields: {k}")
        else:
            ok = False

    print("\nDONE." if ok else "\nDONE with errors — see above.")
    print("Upload the files in %s to the Claude chat." % a.out)


if __name__ == "__main__":
    main()

# ---------------------------------------------------------------------------
# RELAY (optional) — makes the data reachable from Claude's sandbox.
#
# Claude's sandbox CAN reach raw.githubusercontent.com but NOT the VPS or
# api.fantasypros.com. So a cron job on the VPS can push the JSON to a repo
# and Claude curls it directly:
#
#   0 6 * * *  cd /opt/ff && python3 fp_fetch.py --out ./fp \
#              && git add fp && git commit -m "fp $(date +\%F)" \
#              && git push origin main
#
# Two cautions before doing this:
#   1. Push ONLY the fp/ output. Never the .env. Add `.env` to .gitignore first.
#   2. FantasyPros licenses this data; a PUBLIC repo is redistribution. Use a
#      private repo, which then needs a read token Claude would have to handle —
#      and Claude should not hold your credentials. For a once-a-year draft,
#      uploading the JSON by hand is simpler and avoids both problems.
# ---------------------------------------------------------------------------
