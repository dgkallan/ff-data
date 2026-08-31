#!/usr/bin/env python3
"""Re-plan the rest of the draft from the LIVE board, not the pre-draft script.

WHY THIS EXISTS
The round-by-round plan in tx2025.md was optimised before the draft, against
average room behaviour. Real drafts diverge. In the Aug 29 2026 draft the room
took five skill players in the top eight — far more than either prior year —
which drained the WR tier and cost David ~77 pts against the mock's expectation
through two picks.

The right response is NOT to abandon the plan on a feeling. It is to re-run the
optimisation on what is actually left. When that was done at pick 19, the plan
still won:

    A  skill / skill / QB@33   972   <- the plan
    C  skill / QB@16 / skill   968
    B  QB@9  / skill / skill   937

The flat band is robust to the room drafting skill early, because the skill
cliff between rounds 1-2 and round 3 is larger than the QB cliff. But that is a
RESULT, not an assumption — re-derive it, do not assert it.

USAGE
    python3 replan.py --gone "Josh Allen, Bijan Robinson, ..." \
                      --mine "Bijan Robinson, CeeDee Lamb" \
                      --pick 33

Prints: what survives to each remaining pick, the best position sequence from
here, and how much the incumbent plan costs if it is now wrong.
"""
import json, os, argparse, itertools, difflib
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
BOARD = json.load(open(os.path.join(HERE, "tx2025_board.json")))
BY = {p["name"]: p for p in BOARD}
SLOT = 9
PICKS = [r * 12 + (SLOT if r % 2 == 0 else 13 - SLOT) for r in range(14)]
REQ = {"QB": 2, "RB": 2, "WR": 3, "TE": 1}
FLEX = {"RB", "WR", "TE"}
CAPS = {"QB": 3, "RB": 6, "WR": 7, "TE": 3}


def match(raw):
    s = raw.strip()
    if not s:
        return None
    if s in BY:
        return s
    lo = s.lower()
    for n in BY:
        if n.lower() == lo:
            return n
    c = difflib.get_close_matches(s, list(BY), n=1, cutoff=0.82)
    return c[0] if c else None


def survives(p, pick):
    """Will this player still be there at `pick`? Room ADP + a safety margin."""
    return p["adp"] > pick + 4


def best_at(avail, pick, pos=None):
    c = [p for p in avail if (pos is None or p["pos"] == pos)]
    return max(c, key=lambda p: p["pts"]) if c else None


def best_surviving(avail, pick, pos=None):
    c = [p for p in avail if survives(p, pick) and (pos is None or p["pos"] == pos)]
    return max(c, key=lambda p: p["pts"]) if c else None


def lineup_value(roster):
    b = {}
    for n in roster:
        b.setdefault(BY[n]["pos"], []).append(BY[n]["pts"])
    for k in b:
        b[k].sort(reverse=True)
    tot = 0; used = {}
    for pos, c in (("QB", 2), ("RB", 2), ("WR", 3), ("TE", 1)):
        v = b.get(pos, [])[:c]; tot += sum(v); used[pos] = len(v)
    fl = [x for pos in FLEX for x in b.get(pos, [])[used.get(pos, 0):]]
    if fl:
        tot += max(fl)
    return tot


def simulate(seq, avail, mine, remaining):
    """Greedy-fill a position sequence against survival estimates."""
    roster = list(mine); pool = list(avail)
    for pos, pick in zip(seq, remaining):
        cand = [p for p in pool if p["pos"] == pos] if pos != "SKILL" \
            else [p for p in pool if p["pos"] in FLEX]
        cand = [p for p in cand if Counter(BY[n]["pos"] for n in roster)[p["pos"]] < CAPS[p["pos"]]]
        if not cand:
            continue
        take = max(cand, key=lambda p: p["pts"])
        roster.append(take["name"]); pool.remove(take)
        # everyone else's picks between now and the next turn
        pool = [p for p in pool if p["adp"] > pick]
    return lineup_value(roster), roster


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gone", default="")
    ap.add_argument("--mine", default="")
    ap.add_argument("--pick", type=int, required=True)
    a = ap.parse_args()
    gone = {m for m in (match(x) for x in a.gone.split(",")) if m}
    mine = [m for m in (match(x) for x in a.mine.split(",")) if m]
    gone |= set(mine)
    avail = [p for p in BOARD if p["name"] not in gone]
    remaining = [p for p in PICKS if p >= a.pick]

    c = Counter(BY[n]["pos"] for n in mine)
    need = {p: max(0, REQ[p] - c[p]) for p in REQ}
    flex_open = 0 if sum(max(0, c[p] - REQ[p]) for p in FLEX) else 1

    print(f"PICK {a.pick} — {len(remaining)} picks left: {remaining}")
    print(f"roster ({len(mine)}): " + ", ".join(f"{BY[n]['pos']} {n}" for n in mine))
    print(f"still need: " + ", ".join(f"{k}x{v}" for k, v in need.items() if v)
          + (f", FLEX x{flex_open}" if flex_open else ""))
    qb_gone = sum(1 for n in gone if BY[n]["pos"] == "QB")
    print(f"QBs off the board: {qb_gone}")
    print()

    print("BEST AVAILABLE NOW vs BEST SURVIVING TO YOUR NEXT PICK")
    nxt = remaining[1] if len(remaining) > 1 else 999
    print(f"  {'pos':<5}{'now':<24}{'pts':>6}   {'survives to '+str(nxt):<24}{'pts':>6}{'GAP':>7}")
    for pos in ("QB", "RB", "WR", "TE"):
        n0 = best_at(avail, a.pick, pos); n1 = best_surviving(avail, nxt, pos)
        if not n0:
            continue
        gp = n0["pts"] - (n1["pts"] if n1 else 0)
        full = c[pos] >= CAPS[pos]
        tag = "  [FULL]" if full else ""
        print(f"  {pos:<5}{n0['name']:<24}{n0['pts']:>6.0f}   "
              f"{(n1['name'] if n1 else '-'):<24}{(n1['pts'] if n1 else 0):>6.0f}{gp:>7.0f}{tag}")
    print()

    # ---- re-optimise the position sequence over the remaining picks ----
    slots = []
    for p, v in need.items():
        slots += [p] * v
    slots += ["SKILL"] * flex_open
    filler = ["SKILL"] * max(0, len(remaining) - len(slots))
    base = slots + filler
    seen = set(); results = []
    for perm in set(itertools.permutations(base[:min(6, len(base))])):
        seq = list(perm) + base[min(6, len(base)):]
        k = tuple(seq)
        if k in seen:
            continue
        seen.add(k)
        val, roster = simulate(seq, avail, mine, remaining)
        results.append((val, seq, roster))
    results.sort(key=lambda r: -r[0])
    print("RE-OPTIMISED SEQUENCE FROM HERE (top 5):")
    for val, seq, roster in results[:5]:
        s = " ".join(f"{p}@{pk}" for p, pk in zip(seq, remaining))
        print(f"  {val:>7.0f}   {s}")
    if results:
        best = results[0]
        print()
        print(f"  best first move: **{best[1][0]}** at pick {a.pick}")
        alt = [r for r in results if r[1][0] != best[1][0]]
        if alt:
            print(f"  next-best opener: {alt[0][1][0]}  ({alt[0][0]-best[0]:+.0f})")
        print()
        print("  resulting lineup:")
        for n in sorted(best[2], key=lambda n: -BY[n]["pts"]):
            print(f"     {BY[n]['pos']:<4}{n:<24}{BY[n]['pts']:>6.0f}  bye {BY[n]['bye']}")


if __name__ == "__main__":
    main()
