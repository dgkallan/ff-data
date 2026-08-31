#!/usr/bin/env python3
"""Build a VORP-ranked draft board from FantasyPros (or any) projection data.

Why this exists: during a live draft there is no time to recompute replacement
levels by hand, and doing it in your head is how you end up recommending a QB
in round 3. Run this once during setup, keep the output open, and mark players
off as they go.

Input: CSV or JSON with one row per player. Column names are matched loosely,
so most FantasyPros exports work as-is. Recognized (case-insensitive):

    name / player           required
    pos / position          required  (QB/RB/WR/TE/K/DST)
    proj / points / fpts    required  (season-long projected points)
    team, bye, ecr / rank, tier, adp   optional

Usage:
    python build_board.py projections.csv --teams 8
    python build_board.py projections.csv --teams 12 --superflex
    python build_board.py proj.json --teams 8 --starters QB=1,RB=2,WR=2,TE=1,FLEX=1
    python build_board.py proj.csv --teams 8 --top 40 --json board.json

Replacement level is derived from how many players at a position actually get
started league-wide, which is the only number that matters: a position is
scarce when the last startable player is much worse than the first, not when
the position "feels" thin.
"""

import argparse
import csv
import json
import math
import os
import re
import sys
from collections import defaultdict

FLEX_POSITIONS = ("RB", "WR", "TE")

ALIASES = {
    "name": ("name", "player", "playername", "player_name", "fullname"),
    "pos": ("pos", "position"),
    "proj": ("proj", "projection", "points", "fpts", "pts", "proj_pts",
             "projected_points", "fantasypoints", "season_points"),
    "team": ("team", "tm", "nflteam", "nfl_team"),
    "bye": ("bye", "byeweek", "bye_week"),
    "ecr": ("ecr", "rank", "overallrank", "consensus", "consensus_rank",
            "overall_ecr", "rk"),
    "tier": ("tier", "analyst_tier", "fp_tier"),
    "adp": ("adp", "avg_draft_position", "average_draft_position"),
}


def norm(key):
    return re.sub(r"[^a-z0-9]", "", str(key).lower())


def pick(row, field):
    """Pull a field from a row using loose column-name matching."""
    normalized = {norm(k): v for k, v in row.items()}
    for alias in ALIASES[field]:
        if alias in normalized and normalized[alias] not in ("", None):
            return normalized[alias]
    return None


def to_float(value, default=None):
    if value in (None, ""):
        return default
    try:
        return float(str(value).replace(",", "").replace("$", "").strip())
    except ValueError:
        return default


def load(path):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        if path.lower().endswith(".json"):
            data = json.load(fh)
            # Accept either a list of players or {"players": [...]} / {"QB": [...], ...}
            if isinstance(data, dict):
                if "players" in data:
                    data = data["players"]
                else:
                    flat = []
                    for key, value in data.items():
                        if isinstance(value, list):
                            for item in value:
                                item.setdefault("pos", key)
                                flat.append(item)
                    data = flat
            return data
        return list(csv.DictReader(fh))


def parse_starters(spec):
    out = {}
    for chunk in spec.split(","):
        if not chunk.strip():
            continue
        key, _, val = chunk.partition("=")
        out[key.strip().upper()] = int(val)
    return out


def replacement_ranks(teams, starters, superflex):
    """How many players at each position get started across the whole league.

    The flex is the interesting part: it doesn't belong to one position, so it
    pushes replacement level deeper for every position eligible for it. Same
    logic for a superflex slot and quarterbacks.
    """
    ranks = {}
    for pos in ("QB", "RB", "WR", "TE", "K", "DST"):
        ranks[pos] = teams * starters.get(pos, 0)

    flex_slots = teams * starters.get("FLEX", 0)
    if flex_slots:
        # Spread flex demand across RB/WR/TE by how often each fills it in
        # practice: RB and WR carry it, TE rarely does.
        for pos, share in (("RB", 0.45), ("WR", 0.45), ("TE", 0.10)):
            ranks[pos] += flex_slots * share

    if superflex or starters.get("SUPERFLEX"):
        sf_slots = teams * starters.get("SUPERFLEX", 1 if superflex else 0)
        ranks["QB"] += sf_slots

    return {pos: max(1, int(round(count))) for pos, count in ranks.items() if count}


def build(players, teams, starters, superflex, adp_baseline):
    by_pos = defaultdict(list)
    parsed = []

    for row in players:
        name = pick(row, "name")
        pos = pick(row, "pos")
        proj = to_float(pick(row, "proj"))
        if not name or not pos or proj is None:
            continue
        pos = str(pos).upper().strip()
        pos = {"D/ST": "DST", "DEF": "DST", "PK": "K"}.get(pos, pos)
        entry = {
            "name": str(name).strip(),
            "pos": pos,
            "team": (pick(row, "team") or "").strip() or None,
            "bye": to_float(pick(row, "bye")),
            "proj": proj,
            "ecr": to_float(pick(row, "ecr")),
            "tier": pick(row, "tier"),
            "adp": to_float(pick(row, "adp")),
        }
        if entry["bye"] is not None:
            entry["bye"] = int(entry["bye"])
        parsed.append(entry)
        by_pos[pos].append(entry)

    if not parsed:
        sys.exit("No usable rows found — check that the file has name, position, "
                 "and projected-points columns.")

    repl_rank = replacement_ranks(teams, starters, superflex)
    repl_points = {}
    for pos, group in by_pos.items():
        group.sort(key=lambda p: -p["proj"])
        # A position with no starting slots configured (often K/DST) gets its
        # replacement set at the bottom of the pool, which drives everyone's
        # VORP toward zero — the correct signal that those picks don't matter.
        rank = repl_rank.get(pos) or len(group)
        repl_rank[pos] = rank
        idx = min(rank, len(group)) - 1
        repl_points[pos] = group[idx]["proj"] if idx >= 0 else 0.0

    for entry in parsed:
        entry["repl"] = round(repl_points.get(entry["pos"], 0.0), 1)
        entry["vorp"] = round(entry["proj"] - entry["repl"], 1)

    parsed.sort(key=lambda p: -p["vorp"])
    for i, entry in enumerate(parsed, 1):
        entry["board_rank"] = i
        # ADP in most sources assumes a 10- or 12-team room. Scaling by league
        # size approximates where a player actually goes in a smaller draft;
        # the gap between that and raw ADP is where the value hides.
        if entry["adp"]:
            entry["adj_adp"] = round(entry["adp"] * teams / adp_baseline, 1)
            entry["adp_edge"] = round(entry["adj_adp"] - i, 1)
        else:
            entry["adj_adp"] = None
            entry["adp_edge"] = None

    return parsed, repl_points, repl_rank


def render(board, repl_points, repl_rank, top, teams):
    lines = []
    lines.append(f"DRAFT BOARD — {teams}-team, VORP ranked")
    lines.append("Replacement level: " + ", ".join(
        f"{pos}{repl_rank.get(pos, '?')}={pts:.0f}" for pos, pts in
        sorted(repl_points.items())))
    lines.append("")
    header = f"{'#':>3}  {'PLAYER':<24} {'POS':<4} {'TM':<4} {'BYE':>3} " \
             f"{'TIER':>4} {'PROJ':>6} {'VORP':>6} {'ADP*':>6} {'EDGE':>6}"
    lines.append(header)
    lines.append("-" * len(header))
    for entry in board[:top]:
        lines.append(
            f"{entry['board_rank']:>3}  {entry['name'][:24]:<24} "
            f"{entry['pos']:<4} {entry['team'] or '-':<4} "
            f"{entry['bye'] if entry['bye'] else '-':>3} "
            f"{str(entry['tier'] or '-'):>4} {entry['proj']:>6.1f} "
            f"{entry['vorp']:>6.1f} "
            f"{entry['adj_adp'] if entry['adj_adp'] else '-':>6} "
            f"{entry['adp_edge'] if entry['adp_edge'] is not None else '-':>6}"
        )
    lines.append("")
    lines.append("ADP* = league-size-adjusted ADP.  EDGE = adj ADP minus board rank;")
    lines.append("positive means he lasts longer than he's worth (a target).")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("projections", help="CSV or JSON of player projections")
    ap.add_argument("--teams", type=int, required=True, help="league size")
    ap.add_argument("--starters", default="QB=1,RB=2,WR=2,TE=1,FLEX=1",
                    help="starting slots per team, e.g. QB=2,RB=2,WR=3,TE=1,FLEX=1")
    ap.add_argument("--superflex", action="store_true",
                    help="league has a superflex/2QB slot (adds a QB slot per team)")
    ap.add_argument("--adp-baseline", type=int, default=12,
                    help="league size the source ADP assumes (default 12)")
    ap.add_argument("--top", type=int, default=60, help="rows to print")
    ap.add_argument("--json", metavar="PATH", help="also write the full board as JSON")
    args = ap.parse_args()

    if not os.path.exists(args.projections):
        sys.exit(f"No such file: {args.projections}")

    starters = parse_starters(args.starters)
    players = load(args.projections)
    board, repl_points, repl_rank = build(
        players, args.teams, starters, args.superflex, args.adp_baseline)

    print(render(board, repl_points, repl_rank, args.top, args.teams))

    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(board, fh, indent=2)
        print(f"\nFull board ({len(board)} players) written to {args.json}")


if __name__ == "__main__":
    main()
