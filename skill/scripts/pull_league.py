#!/usr/bin/env python3
"""Fetch TX2025 league state from the GitHub relay and produce the Wed/Sat brief.

WHY A RELAY. Claude's sandbox is network-allowlisted to package registries plus
GitHub. It cannot reach CBS, ESPN, or David's VPS. But raw.githubusercontent.com
IS reachable (verified Aug 24 2026, HTTP 200). So a Cowork task reads the CBS
league through Claude in Chrome, commits JSON to a public repo, and this script
pulls it. That is the only hands-off path from David's league into a chat.

CADENCE. Wednesday and Saturday early AM. CBS FAAB deadlines are Wednesday and
Saturday nights, processing Thursday and Sunday early AM — so a morning pull
gives David the full day to review before the deadline.

USAGE
    python3 pull_league.py --repo dkallan/ff-data            # latest
    python3 pull_league.py --repo dkallan/ff-data --date 2026-09-02
"""
import json, urllib.request, argparse, sys, os
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = "https://raw.githubusercontent.com/{repo}/main/{path}"
REQ = {"QB": 2, "RB": 2, "WR": 3, "TE": 1}
FLEX = {"RB", "WR", "TE"}


def get(repo, path):
    url = RAW.format(repo=repo, path=path)
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        print(f"FAILED {url}\n  {type(e).__name__}: {e}", file=sys.stderr)
        return None


def board():
    """Season-scored board — for TRADE valuation only, never start/sit."""
    try:
        return {p["name"]: p for p in json.load(open(os.path.join(HERE, "tx2025_board.json")))}
    except FileNotFoundError:
        return {}


def brief(d, B):
    me = d.get("my_team")
    teams = d.get("teams", [])
    print("=" * 70)
    print(f"TX2025 — pulled {d.get('pulled','?')}   week {d.get('week','?')}")
    print("=" * 70)

    # ---- roster shape across the league: who is short where ----
    print("\nLEAGUE NEEDS MATRIX — starting slots not covered")
    print(f"  {'team':<26}{'QB':>4}{'RB':>4}{'WR':>4}{'TE':>4}{'FAAB':>8}")
    short = defaultdict(list)
    for t in teams:
        c = Counter(p.get("pos") for p in t.get("roster", []))
        gaps = {k: max(0, REQ[k] - c.get(k, 0)) for k in REQ}
        for k, v in gaps.items():
            if v: short[k].append(t["name"])
        flag = "  <== YOU" if t["name"] == me else ""
        print(f"  {t['name']:<26}{c.get('QB',0):>4}{c.get('RB',0):>4}{c.get('WR',0):>4}"
              f"{c.get('TE',0):>4}{t.get('faab_left','?'):>8}{flag}")
    for k in REQ:
        if short[k]:
            print(f"  !! short at {k}: {', '.join(short[k])}")

    # ---- FAAB context: who can actually outbid you ----
    fa = [(t.get("faab_left", 0), t["name"]) for t in teams if isinstance(t.get("faab_left"), (int, float))]
    if fa:
        fa.sort(reverse=True)
        mine = next((v for v, n in fa if n == me), None)
        print(f"\nFAAB REMAINING — you: {mine}")
        rich = [n for v, n in fa if mine is not None and v > mine]
        print(f"  teams with more than you ({len(rich)}): {', '.join(rich) if rich else 'none'}")
        print("  top 3: " + " | ".join(f"{n} {v}" for v, n in fa[:3]))

    # ---- my roster, valued ----
    mine_t = next((t for t in teams if t["name"] == me), None)
    if mine_t and B:
        r = [(B.get(p["name"], {}).get("pts", 0), p.get("pos"), p["name"]) for p in mine_t["roster"]]
        r.sort(reverse=True)
        print("\nYOUR ROSTER (season pts — trade valuation only)")
        for pts, pos, n in r:
            print(f"   {n:<24}{pos:<5}{pts:>7.0f}")

    # ---- free agents worth a claim ----
    fas = d.get("free_agents", [])
    if fas and B:
        scored = [(B.get(f["name"], {}).get("pts", 0), f) for f in fas]
        scored = [(p, f) for p, f in scored if p > 0]
        scored.sort(reverse=True)
        print(f"\nTOP FREE AGENTS ({len(fas)} listed)")
        print(f"  {'player':<24}{'pos':<5}{'pts':>7}{'ros%':>7}")
        for pts, f in scored[:12]:
            print(f"  {f['name']:<24}{f.get('pos','?'):<5}{pts:>7.0f}{f.get('pct_rostered','?'):>7}")
        unknown = [f["name"] for f in fas if f["name"] not in B][:6]
        if unknown:
            print(f"  not on my board (check before claiming): {', '.join(unknown)}")

    print("""
NEXT STEPS — this script only surfaces state. It does not decide.
  waivers : rank targets by RoS marginal gain over the player you would DROP,
            not over a theoretical replacement. Bid odd numbers; ties go to the
            worse team. See faab-waivers.md.
  lineup  : DO NOT use the season points above. Pull weekly projections
            (/nfl/2026/projections?week=N) plus weekly ECR and injury
            probabilities. See weekly-lineup.md.
  trades  : use the needs matrix. A team short at a position is your buyer.
            Price both sides with a before/after optimal lineup, never by
            summing chart values.""")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, help="e.g. dkallan/ff-data")
    ap.add_argument("--date", help="YYYY-MM-DD; omit for latest.json")
    ap.add_argument("--league", default="tx2025")
    a = ap.parse_args()
    path = f"{a.league}/{'latest' if not a.date else a.date}.json"
    d = get(a.repo, path)
    if not d:
        sys.exit("no data — has the Cowork task run yet?")
    brief(d, board())
