#!/usr/bin/env python3
"""Build in-season trade value charts for TX2025 and Empty Stadiums.

WHY A CUSTOM CHART. Every public chart (KeepTradeCut, FantasyCalc, Stats Guy)
is dynasty and generic-scoring. Neither of David's leagues is either. The edge
is not out-evaluating FantasyPros — it is arithmetic they cannot do, because
they do not know these leagues. Convert their stat projections; do not
second-guess their player evaluation.

THE THREE DESIGN DECISIONS, and the reasoning:

1. VALUE IS MEASURED AGAINST THE WIRE, NOT AGAINST A RANK.
   A player's worth is the lineup points you lose if he vanishes and you refill
   the slot from free agency. That makes value league-specific automatically:
   the same running back is worth more in a 12-team league than an 8-team one
   because the wire behind him is thinner. Replacement is computed from roster
   math (teams x roster size, allocated by position), not assumed.

2. THE PACKAGE PREMIUM LIVES IN THE CURVE.
   Research on thousands of community-judged trades found that bolting a
   correction onto the total at verdict time scores far worse than shaping the
   value curve itself (85% vs 42-60% agreement). Experienced managers demand a
   package beat a star's paper value by 15-40% before calling a deal fair.
   So values are raised to an exponent > 1: two players at half a star's raw
   marginal points chart well below the star. With EXP=1.30 a 2-for-1 at equal
   raw value shows the star ~23% ahead, inside the observed band.

3. THE CHART IS A SCREEN, NOT A VERDICT.
   Values are path-dependent: a fourth good receiver is worth far less to a
   roster already starting three. The chart tells you whether a deal is close
   enough to bother modelling. The verdict always comes from one before/after
   optimal-lineup comparison on BOTH rosters. Never sum chart values and
   declare a winner.

USAGE
    python3 trade_chart.py                      # preseason, from projections
    python3 trade_chart.py --ros ros.json       # in-season, rest-of-season proj
    python3 trade_chart.py --league tx2025 --top 40
"""
import json, math, os, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
G = 17.0
EXP = 1.30          # package-premium exponent; see design note 2


def games_over(total, thresh, cv):
    """Expected games clearing a per-game threshold, from a season total."""
    m = total / G
    if m <= 0:
        return 0.0
    s = math.sqrt(math.log(1 + cv * cv))
    mu = math.log(m) - s * s / 2
    return 0.5 * math.erfc(((math.log(thresh) - mu) / s) / math.sqrt(2)) * G


# ---------------------------------------------------------------- league rules
def score_tx2025(pos, s):
    """12-team, 2QB/2RB/3WR/1TE/1FLEX, no K/DEF. 6pt pass TD,
    +3 at 300 pass yds, +3 at 100 rec yds, +3 more at 200.

    *** RB IS HALF-POINT PPR (0.5). WR and TE are full (1.0). ***
    Confirmed by David Aug 24 2026. Earlier versions of this skill said 1.0
    across the board, which overvalued pass-catching backs by ~35-40 pts:
    Bijan -40, McCaffrey -39, Gibbs -36, Achane -33."""
    if pos == "QB":
        py = s.get("pass_yds", 0)
        return (py / 25 + 6 * s.get("pass_tds", 0) - s.get("pass_ints", 0)
                + s.get("rush_yds", 0) / 10 + 6 * s.get("rush_tds", 0)
                - 2 * s.get("fumbles", 0) + 3 * games_over(py, 300, .38))
    ppr = 0.5 if pos == "RB" else 1.0
    ry = s.get("rec_yds", 0)
    return (ppr * s.get("rec_rec", 0) + ry / 10 + 6 * s.get("rec_tds", 0)
            + s.get("rush_yds", 0) / 10 + 6 * s.get("rush_tds", 0)
            - 2 * s.get("fumbles", 0)
            + 3 * games_over(ry, 100, .75) + 3 * games_over(ry, 200, .75))


def score_empty(pos, s):
    """8-team, 2QB/2RB/3WR/1TE/1OP/2DP, no K/DST. 0.05/pass yd, 6pt pass TD,
    -2 INT, +5 at 300 / +10 at 400 pass yds, full PPR, +5 at 100 scrimmage yds.
    NOTE: the 0.5/target and 0.05/completion bonuses were REMOVED for 2026."""
    if pos == "QB":
        py = s.get("pass_yds", 0)
        return (py * 0.05 + 6 * s.get("pass_tds", 0) - 2 * s.get("pass_ints", 0)
                + s.get("rush_yds", 0) * 0.1 + 6 * s.get("rush_tds", 0)
                - 2 * s.get("fumbles", 0)
                + 5 * games_over(py, 300, .38) + 5 * games_over(py, 400, .38))
    ry = s.get("rec_yds", 0)
    rus = s.get("rush_yds", 0)
    return (s.get("rec_rec", 0) + (ry + rus) * 0.1
            + 6 * (s.get("rec_tds", 0) + s.get("rush_tds", 0))
            - 2 * s.get("fumbles", 0)
            + 5 * games_over(max(ry, rus), 100, .75))


LEAGUES = {
    "tx2025": dict(
        name="TX2025 (CBS, 12-team true 2QB)", teams=12, roster=14,
        start={"QB": 2, "RB": 2, "WR": 3, "TE": 1}, flex=1,
        flex_pos=("RB", "WR", "TE"), score=score_tx2025,
        # rostered depth by position, from 2024+2025 observed draft behavior
        rostered={"QB": 31, "RB": 48, "WR": 66, "TE": 23}),
    "empty": dict(
        name="Empty Stadiums (ESPN, 8-team superflex)", teams=8, roster=16,
        start={"QB": 2, "RB": 2, "WR": 3, "TE": 1}, flex=1,
        flex_pos=("QB", "RB", "WR", "TE"), score=score_empty,
        # 2 DP slots consume ~24 roster spots, leaving less offensive depth
        rostered={"QB": 21, "RB": 28, "WR": 38, "TE": 14}),
}


def build(proj, cfg, top):
    scored = []
    for p in proj:
        pos = p.get("position_id")
        if pos not in ("QB", "RB", "WR", "TE"):
            continue
        scored.append(dict(name=p["name"], pos=pos, team=p.get("team_id", ""),
                           pts=round(cfg["score"](pos, p.get("stats", {})), 1)))
    by = {}
    for pos in ("QB", "RB", "WR", "TE"):
        g = sorted([x for x in scored if x["pos"] == pos], key=lambda x: -x["pts"])
        for i, x in enumerate(g, 1):
            x["rank"] = i
        by[pos] = g

    # wire replacement = best player NOT rostered anywhere in the league
    wire = {}
    for pos, n in cfg["rostered"].items():
        g = by[pos]
        wire[pos] = g[min(n, len(g) - 1)]["pts"] if g else 0.0

    for x in scored:
        x["raw"] = max(0.0, x["pts"] - wire[x["pos"]])
    mx = max(x["raw"] for x in scored) or 1.0
    for x in scored:
        x["val"] = round(100 * (x["raw"] / mx) ** EXP, 1)
    return by, wire, sorted(scored, key=lambda x: -x["val"])[:top]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--proj", default="/mnt/user-data/uploads/projections-2026.json")
    ap.add_argument("--league", default="both", choices=["both", "tx2025", "empty"])
    ap.add_argument("--top", type=int, default=60)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    proj = json.load(open(a.proj))["players"]
    keys = ["tx2025", "empty"] if a.league == "both" else [a.league]
    out = {}
    for k in keys:
        cfg = LEAGUES[k]
        by, wire, board = build(proj, cfg, a.top)
        out[k] = dict(wire=wire, board=board)
        print(f"\n{'='*72}\n{cfg['name']}\n{'='*72}")
        print("wire replacement: " + "  ".join(f"{p}{cfg['rostered'][p]}={wire[p]:.0f}" for p in wire))
        print(f"\n{'#':<4}{'player':<24}{'pos':<6}{'pts':>7}{'over wire':>11}{'VALUE':>8}")
        for i, x in enumerate(board, 1):
            print(f"{i:<4}{x['name']:<24}{x['pos']}{x['rank']:<4}{x['pts']:>7.0f}{x['raw']:>11.0f}{x['val']:>8.1f}")
        print("\n2-for-1 check: two players at half the top raw value chart at "
              f"{2*100*0.5**EXP:.0f} vs {100} for one — "
              f"{(100/(2*100*0.5**EXP)-1)*100:.0f}% consolidation premium")
    if a.out:
        json.dump(out, open(a.out, "w"), indent=1)
        print(f"\nwrote {a.out}")


if __name__ == "__main__":
    main()
