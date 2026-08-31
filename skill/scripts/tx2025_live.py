#!/usr/bin/env python3
"""TX2025 live draft assistant — slot 9, 12-team true 2QB, no K/DEF.

Enforces the draft-postmortem-2026 rules mechanically so they cannot be skipped:
  * gap-to-next-survivor is stated FIRST, before any name
  * a deviation from plan requires gap >= 30 AND a smaller gap at the plan position
  * players not on the board are flagged, never recommended
  * roster open slots are printed every time, never recalled from memory
  * already-drafted players are impossible to recommend (set subtraction)

USAGE
  python3 tx2025_live.py --gone "Josh Allen, Bijan Robinson, ..." \
                         --mine "Ja'Marr Chase, Jaxon Smith-Njigba" \
                         --pick 33
  # names are fuzzy-matched; --gone should include YOUR players too
"""
import json, argparse, difflib, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BOARD = json.load(open(os.path.join(HERE, "tx2025_board.json")))
BY = {p["name"]: p for p in BOARD}

SLOT = 9
PICKS = [r * 12 + (SLOT if r % 2 == 0 else 13 - SLOT) for r in range(14)]
PLAN = {1: "SKILL", 2: "SKILL", 3: "QB", 4: "RB", 5: "SKILL", 6: "QB",
        7: "RB", 8: "TE", 9: "SKILL", 10: "SKILL", 11: "ANY", 12: "ANY",
        13: "ANY", 14: "ANY"}
REQ = {"QB": 2, "RB": 2, "WR": 3, "TE": 1}
CAPS = {"QB": 3, "RB": 6, "WR": 7, "TE": 3}
FLEX = {"RB", "WR", "TE"}
DO_NOT_DRAFT = {"Jordan Love"}          # David's standing preference
BYE_WATCH = 11                          # week 11 clusters badly


def match(raw):
    """Fuzzy-match a typed/OCR'd name to the board. Returns (name|None, note)."""
    s = raw.strip()
    if not s:
        return None, ""
    if s in BY:
        return s, ""
    lo = s.lower()
    for n in BY:
        if n.lower() == lo or n.lower().replace(".", "") == lo.replace(".", ""):
            return n, ""
    # "J. Smith-Njigba" style
    parts = lo.replace(".", " ").split()
    if parts:
        surname = parts[-1]
        hits = [n for n in BY if n.lower().split()[-1] == surname]
        if len(hits) == 1:
            return hits[0], ""
        if len(hits) > 1 and len(parts) > 1:
            ini = parts[0][0]
            hits2 = [n for n in hits if n.lower()[0] == ini]
            if len(hits2) == 1:
                return hits2[0], ""
    close = difflib.get_close_matches(s, list(BY), n=1, cutoff=0.82)
    if close:
        return close[0], f"(read '{s}' as {close[0]})"
    return None, f"*** '{s}' NOT ON MY BOARD — do not draft without checking his actual 2025 finish ***"


def rnd_of(pick):
    return (pick - 1) // 12 + 1


def analyse(gone_names, mine_names, pick):
    notes = []
    gone = set()
    for r in gone_names:
        n, note = match(r)
        if note: notes.append(note)
        if n: gone.add(n)
    mine = []
    for r in mine_names:
        n, note = match(r)
        if note: notes.append(note)
        if n:
            mine.append(n); gone.add(n)

    avail = [p for p in BOARD if p["name"] not in gone and p["name"] not in DO_NOT_DRAFT]
    rnd = rnd_of(pick)
    picks_left = 14 - len([p for p in PICKS if p < pick])
    try:
        nxt = [p for p in PICKS if p > pick][0]
    except IndexError:
        nxt = 999

    cnt = {k: 0 for k in REQ}
    for n in mine:
        cnt[BY[n]["pos"]] += 1
    open_slots = []
    for pos, need in REQ.items():
        for _ in range(max(0, need - cnt[pos])):
            open_slots.append(pos)
    flex_used = sum(max(0, cnt[p] - REQ[p]) for p in FLEX)
    if not flex_used:
        open_slots.append("FLEX")

    # survivor gap: best at pos now vs best at pos expected to survive to my next pick
    def survivors(pos):
        c = [p for p in avail if p["pos"] == pos]
        c.sort(key=lambda p: -p["pts"])
        return c

    # my current worst starter at each position (for marginal-value discounting)
    mine_by = {}
    for n in mine:
        mine_by.setdefault(BY[n]["pos"], []).append(BY[n]["pts"])
    for k in mine_by:
        mine_by[k].sort(reverse=True)

    def starts(pos, pts):
        """Would a player at `pos` scoring `pts` crack the starting lineup?"""
        have = mine_by.get(pos, [])
        if len(have) < REQ[pos]:
            return True
        if pos in FLEX and not flex_used:
            return True
        return pts > (have[REQ[pos] - 1] if len(have) >= REQ[pos] else 0)

    gaps = {}
    for pos in ("QB", "RB", "WR", "TE"):
        c = survivors(pos)
        if not c:
            continue
        best = c[0]
        surv = [p for p in c[1:] if p["adp"] > nxt + 4]
        nextbest = surv[0] if surv else (c[-1] if len(c) > 1 else None)
        raw = best["pts"] - (nextbest["pts"] if nextbest else 0)
        # A position you already fill contributes nothing to the STARTING lineup.
        gaps[pos] = (best, nextbest, raw if starts(pos, best["pts"]) else 0.0)

    qb_gone = len([n for n in gone if BY[n]["pos"] == "QB"])

    print("=" * 68)
    print(f"PICK {pick}  (round {rnd})   |   next pick: {nxt}   |   {picks_left} picks left")
    print("=" * 68)
    for n in notes:
        print("  " + n)
    print(f"\nROSTER ({len(mine)}): " + (", ".join(f"{BY[n]['pos']} {n}" for n in mine) or "empty"))
    print(f"OPEN STARTING SLOTS: {', '.join(open_slots) if open_slots else 'none — all filled'}")
    print(f"QBs OFF THE BOARD: {qb_gone}")
    if pick >= 24 and qb_gone <= 10:
        print("  >> TRIGGER: slow QB start = fast reload coming. Move QB2 up to pick 57.")
    elif pick >= 24 and qb_gone >= 13:
        print("  >> TRIGGER: hot room, runs cool later. Hold QB2 for pick 64.")

    want = PLAN.get(rnd, "ANY")
    print(f"\nPLAN SAYS: round {rnd} -> {want}")

    print(f"\nGAP TO NEXT SURVIVOR (survivor = ADP past pick {nxt})")
    print(f"  {'pos':<5}{'best available':<24}{'pts':>7}{'next survivor':>24}{'gap':>7}")
    for pos in ("QB", "RB", "WR", "TE"):
        if pos not in gaps:
            continue
        b, nb, g = gaps[pos]
        blocked = cnt[pos] >= CAPS[pos]
        tag = "   [POSITION FULL]" if blocked else ("   [bench only - gap zeroed]" if g == 0 else "")
        print(f"  {pos:<5}{b['name']:<24}{b['pts']:>7.0f}{(nb['name'] if nb else '-'):>24}{g:>7.0f}{tag}")

    # the call
    legal = [p for p in avail if cnt[p["pos"]] < CAPS[p["pos"]]]
    if len(open_slots) >= picks_left:
        need_pos = [s for s in open_slots if s != "FLEX"]
        if need_pos:
            cand = [p for p in legal if p["pos"] == need_pos[0]]
            if cand:
                pick_it = max(cand, key=lambda p: p["pts"])
                print(f"\n>>> FORCED: {picks_left} picks left, {len(open_slots)} slots open.")
                print(f">>> TAKE {pick_it['name']} ({pick_it['pos']}, {pick_it['pts']:.0f})")
                return

    planpos = {"SKILL": FLEX, "QB": {"QB"}, "RB": {"RB"}, "TE": {"TE"},
               "ANY": {"QB", "RB", "WR", "TE"}}[want]
    pc = [p for p in legal if p["pos"] in planpos]
    pc.sort(key=lambda p: -p["pts"])
    plan_gap = max((gaps[p][2] for p in planpos if p in gaps), default=0)
    off = [p for p in legal if p["pos"] not in planpos]
    best_any = max(off, key=lambda p: p["pts"]) if off else None
    off_gap = gaps.get(best_any["pos"], (None, None, 0))[2] if best_any else 0

    print()
    if pc:
        top = pc[0]
        MARGIN = 20
        dev_ok = (best_any and off_gap >= 30 and off_gap >= plan_gap + MARGIN)
        if dev_ok:
            print(f">>> DEVIATION JUSTIFIED: {best_any['pos']} gap {off_gap:.0f} >= 30 "
                  f"and clears plan gap {plan_gap:.0f} by {off_gap-plan_gap:.0f} (need 20+)")
            print(f">>> TAKE {best_any['name']} ({best_any['pos']}, {best_any['pts']:.0f})")
            print(f"    fallback: {top['name']} ({top['pos']}, {top['pts']:.0f})")
        else:
            print(f">>> TAKE {top['name']} ({top['pos']}{BY[top['name']]['rank']}, "
                  f"{top['pts']:.0f} pts, bye {top['bye']})")
            if best_any:
                why = ("below the 30 threshold" if off_gap < 30
                       else f"only {off_gap-plan_gap:.0f} over plan gap {plan_gap:.0f}, need 20+")
                print(f"    plan gap {plan_gap:.0f} | best off-plan {best_any['name']} ({best_any['pos']}) gap {off_gap:.0f} -> {why}. No deviation.")
            else:
                print(f"    plan gap {plan_gap:.0f} | nothing off-plan is legal. No deviation.")
            alts = [p for p in pc[1:4]]
            if alts:
                print("    next: " + " | ".join(f"{p['name']} {p['pts']:.0f}" for p in alts))
        if top["bye"] == BYE_WATCH:
            n11 = sum(1 for n in mine if BY[n]["bye"] == BYE_WATCH)
            print(f"    ! bye {BYE_WATCH} — you'd have {n11 + 1} players on that bye")
    else:
        print(f">>> No legal {want} left. Best available: {best_any['name']} ({best_any['pos']})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--gone", default="", help="comma-separated drafted players (include yours)")
    ap.add_argument("--mine", default="", help="comma-separated YOUR players")
    ap.add_argument("--pick", type=int, required=True)
    a = ap.parse_args()
    sp = lambda s: [x for x in s.split(",") if x.strip()]
    analyse(sp(a.gone), sp(a.mine), a.pick)
