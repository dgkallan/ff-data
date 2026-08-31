#!/usr/bin/env python3
"""
Trade value model for Empty Stadiums (8-team superflex, 2 IDP, no K/DST).

Implements references/trade-value-model.md:
  TRUE value    = lineup points lost if a player is gone and the slot is
                  refilled from the wire, leverage-weighted for the week.
  MARKET value  = the same calculation run on a recency-heavy projection,
                  i.e. how the room prices him off what's visible on ESPN.
  ARBITRAGE     = TRUE - MARKET.  Positive = buy.  Negative = sell.

Trades are ALWAYS evaluated as one before/after lineup comparison with every
piece applied at once. Player values are path-dependent and must never be summed.

Usage:
    python3 trade_value.py --demo
    python3 trade_value.py --week 6 --roster roster.json --offer offer.json
"""

import argparse, json, copy
from collections import defaultdict

# ---------------------------------------------------------------- league setup
START = {"QB": 2, "RB": 2, "WR": 3, "TE": 1, "IDP": 2}   # + 1 OP handled below
OP_POS = ("QB", "RB", "WR", "TE")
MAXP = {"QB": 4, "RB": 4, "WR": 6, "TE": 2, "IDP": 4}
REG_WEEKS, LAST_WEEK = 15, 17

# Best freely-available player at each position, in season points.
# Reset these to real rostered depth after the draft (see the .md).
WIRE = {"QB": 300, "RB": 205, "WR": 210, "TE": 155, "IDP": 213}

# Championship-equity leverage per week.
def leverage(w, p_playoff=0.72, p_final=0.36):
    if w <= 9:    base = 1.00
    elif w <= 13: base = 1.35
    elif w <= 15: base = 2.00
    else:         base = 5.00
    if w == 16: base *= p_playoff
    if w == 17: base *= p_final
    return base

def weeks_left(week):
    """Leverage-weighted weeks remaining, and the raw count."""
    rem = [w for w in range(max(week, 1), LAST_WEEK + 1)]
    return sum(leverage(w) for w in rem), len(rem)

# ------------------------------------------------------------- lineup scoring
def lineup(roster):
    """Total points from the optimal starting eleven. Players carry season pts."""
    by = defaultdict(list)
    for p in roster:
        by[p["pos"]].append(p["pts"])
    for k in by:
        by[k].sort(reverse=True)
    total, used = 0.0, defaultdict(int)
    for pos, n in START.items():
        take = by[pos][:n]
        total += sum(take)
        used[pos] = len(take)
    spare = []
    for pos in OP_POS:
        spare += by[pos][used[pos]:]
    if spare:
        total += max(spare)
    return total

def _wire(pos):
    return {"n": f"FA-{pos}", "pos": pos, "pts": WIRE[pos]}

# --------------------------------------------------------------- true value
def value_of(roster, names, week=1):
    """
    Lineup points lost if `names` leave and each vacated slot is refilled
    from the wire. Handles multiple players simultaneously — this is the
    only correct way to price a package.
    """
    names = {names} if isinstance(names, str) else set(names)
    base = lineup(roster)
    keep = [p for p in roster if p["n"] not in names]
    gone = [p for p in roster if p["n"] in names]
    after = keep + [_wire(p["pos"]) for p in gone]
    season_delta = base - lineup(after)
    lev, raw = weeks_left(week)
    per_week = season_delta / REG_WEEKS
    return {"season": season_delta, "per_week": per_week,
            "ros_linear": per_week * raw, "ros_leveraged": per_week * lev}

# ------------------------------------------------------- market (perceived)
MARKET_W = [(3, (0.60, 0.30, 0.10)), (7, (0.30, 0.50, 0.20)), (99, (0.10, 0.55, 0.35))]
TRUTH_W  = [(3, (0.80, 0.20)),       (7, (0.55, 0.45)),       (99, (0.30, 0.70))]

def _pick(table, week):
    for cutoff, w in table:
        if week <= cutoff:
            return w
    return table[-1][1]

def market_pts(p, week):
    """How the room projects him: preseason anchor + recency-heavy recent form."""
    a, r, s = _pick(MARKET_W, week)
    pre = p.get("preseason", p["pts"]) / REG_WEEKS
    l3 = p.get("last3", pre)
    std = p.get("season_avg", pre)
    return (a * pre + r * l3 + s * std) * REG_WEEKS

def true_pts(p, week):
    """What he's actually worth: preseason talent + opportunity-adjusted usage.
       No weight on a three-game sample."""
    a, s = _pick(TRUTH_W, week)
    pre = p.get("preseason", p["pts"]) / REG_WEEKS
    std = p.get("season_avg", pre)
    # touchdown-luck correction: the largest and most reliable adjustment
    std -= p.get("td_luck_per_week", 0.0)
    return (a * pre + s * std) * REG_WEEKS

def _reproject(roster, week, fn):
    r = copy.deepcopy(roster)
    for p in r:
        p["pts"] = fn(p, week)
    return r

def arbitrage(roster, name, week=1):
    """TRUE vs MARKET value for one player on this roster."""
    t = value_of(_reproject(roster, week, true_pts), name, week)["ros_leveraged"]
    m = value_of(_reproject(roster, week, market_pts), name, week)["ros_leveraged"]
    return {"true": t, "market": m, "edge": t - m,
            "call": "BUY" if t - m > 15 else "SELL" if t - m < -15 else "hold"}

# ------------------------------------------------------------------- offers
def evaluate(roster, give, get, week=1):
    """One before/after comparison with every piece applied at once."""
    give, get = set(give), [dict(p) for p in get]
    before = lineup(_reproject(roster, week, true_pts))
    after_roster = [p for p in roster if p["n"] not in give] + get
    # refill any slot left empty below starter requirements from the wire
    counts = defaultdict(int)
    for p in after_roster:
        counts[p["pos"]] += 1
    for pos, need in START.items():
        while counts[pos] < need:
            after_roster.append(_wire(pos)); counts[pos] += 1
    after = lineup(_reproject(after_roster, week, true_pts))
    lev, raw = weeks_left(week)
    per_week = (after - before) / REG_WEEKS
    return {"before": before, "after": after, "season_delta": after - before,
            "ros_leveraged": per_week * lev,
            "verdict": "ACCEPT" if after - before > 0 else "DECLINE"}

# --------------------------------------------------------------------- demo
DEMO = [("Gibbs","RB",396),("St. Brown","WR",354),("Jefferson","WR",322),
        ("McConkey","WR",266),("Purdy","QB",424),("Herbert","QB",380),
        ("Goff","QB",371),("Judkins","RB",257),("Kraft","TE",189),
        ("Cashman","IDP",392),("Brooks","IDP",387),("Bolton","IDP",355),
        ("Warner","IDP",350),("Bigsby","RB",181),("Johnson","RB",171),
        ("Andrews","TE",149)]

def demo():
    roster = [{"n": n, "pos": p, "pts": v, "preseason": v} for n, p, v in DEMO]
    print(f"Lineup: {lineup(roster):.0f}\n")
    print(f"{'PLAYER':<14}{'PROJ':>6}{'VALUE wk1':>11}{'wk8':>8}{'wk14':>8}")
    print("-" * 47)
    rows = [(p["n"], p["pts"],
             value_of(roster, p["n"], 1)["ros_leveraged"],
             value_of(roster, p["n"], 8)["ros_leveraged"],
             value_of(roster, p["n"], 14)["ros_leveraged"]) for p in roster]
    for n, v, a, b, c in sorted(rows, key=lambda x: -x[2]):
        print(f"{n:<14}{v:>6.0f}{a:>11.0f}{b:>8.0f}{c:>8.0f}")

    print("\nPATH DEPENDENCE — values are not additive")
    ind = sum(value_of(roster, n, 1)["ros_leveraged"]
              for n in ["Cashman","Brooks","Bolton","Warner"])
    tog = value_of(roster, ["Cashman","Brooks","Bolton","Warner"], 1)["ros_leveraged"]
    print(f"  four LBs summed individually : {ind:>6.0f}")
    print(f"  four LBs priced together     : {tog:>6.0f}   <- {tog/max(ind,1):.1f}x")

    print("\nCONSOLIDATION — what clears Gibbs?")
    g = value_of(roster, "Gibbs", 1)["ros_leveraged"]
    for pkg in (["McConkey","Judkins"], ["Herbert","Goff"],
                ["Jefferson","Judkins"], ["Jefferson","Herbert"]):
        v = value_of(roster, pkg, 1)["ros_leveraged"]
        print(f"  {' + '.join(pkg):<28}{v:>6.0f}  {'CLEARS' if v >= g else 'short'} ({g:.0f})")

    print("\nARBITRAGE — week 6, two players the market has misread")
    hot = copy.deepcopy(roster)
    for p in hot:
        if p["n"] == "Judkins":      # hot streak the room is extrapolating
            p["last3"], p["season_avg"], p["td_luck_per_week"] = 24.0, 19.0, 4.0
        if p["n"] == "McConkey":     # quiet stretch, role intact
            p["last3"], p["season_avg"], p["td_luck_per_week"] = 8.0, 16.0, -2.0
    for n in ("Judkins", "McConkey"):
        a = arbitrage(hot, n, 6)
        print(f"  {n:<12} TRUE {a['true']:>5.0f}   MARKET {a['market']:>5.0f}   "
              f"edge {a['edge']:>+5.0f}   {a['call']}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--week", type=int, default=1)
    ap.add_argument("--roster"); ap.add_argument("--offer")
    a = ap.parse_args()
    if a.demo or not a.roster:
        demo()
    else:
        roster = json.load(open(a.roster))
        if a.offer:
            o = json.load(open(a.offer))
            print(json.dumps(evaluate(roster, o["give"], o["get"], a.week), indent=2))
        else:
            for p in roster:
                print(p["n"], round(value_of(roster, p["n"], a.week)["ros_leveraged"]))
