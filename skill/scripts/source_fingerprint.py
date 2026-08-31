#!/usr/bin/env python3
"""Fingerprint which ranking source each league manager drafts from.

WHY THIS MATTERS
In the Aug 2026 TX2025 draft the room drafted quarterbacks at 0.935 Spearman
correlation with CBS positional rank. That single fact made Bo Nix (CBS QB10,
our QB3 at 360) and Tyler Shough (CBS QB8, our QB5 at 339) available 20+ picks
past where our board valued them — the two best picks of the draft.

Knowing WHICH list each manager uses tells you two things:
  1. Whose picks are predictable (so ADP-based survival estimates work)
  2. Who systematically undervalues players their list ranks low (buy-low pool)

INPUTS
  draft.json   [{"pick":1,"owner":"Seamus","player":"Josh Allen","pos":"QB"}, ...]
  sources/*.json   one per ranking source, each {"PlayerName": positional_rank}

USAGE
  python3 source_fingerprint.py --draft draft.json --sources sources/

METHOD
For each owner and each candidate source, measure how many players that source
ranked HIGHER at the same position were still on the board when they picked.
A manager drafting straight off a list skips ~0. Low mean = that's their list.

Then compare across sources: the source with the lowest mean skip is the best
fit. If no source is clearly lower, they're using something we don't have (or
their own read) — report that honestly rather than forcing a match.
"""
import json, argparse, os, glob
from collections import defaultdict


def skips(draft, ranks):
    """For each pick, how many same-position players this source ranked higher
    were still available?"""
    out = defaultdict(list)
    for i, p in enumerate(draft):
        r = ranks.get(p["player"])
        if r is None:
            continue
        taken = {ranks.get(q["player"]) for q in draft[:i] if q["pos"] == p["pos"]}
        taken.discard(None)
        better = sum(1 for x in range(1, int(r)) if x not in taken)
        out[p["owner"]].append(better)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--draft", required=True)
    ap.add_argument("--sources", required=True)
    a = ap.parse_args()
    draft = json.load(open(a.draft))
    srcs = {}
    for f in sorted(glob.glob(os.path.join(a.sources, "*.json"))):
        srcs[os.path.basename(f)[:-5]] = json.load(open(f))
    if not srcs:
        print("no source files found"); return

    per = {s: skips(draft, r) for s, r in srcs.items()}
    owners = sorted({p["owner"] for p in draft})
    names = sorted(srcs)

    print("MEAN 'HIGHER-RANKED PLAYERS SKIPPED' BY SOURCE")
    print("lower = that manager drafts off that list\n")
    print(f"{'owner':<14}" + "".join(f"{s:>11}" for s in names) + "   best fit")
    for o in owners:
        row = []
        for s in names:
            v = per[s].get(o, [])
            row.append(sum(v) / len(v) if v else float("nan"))
        best = min(range(len(row)), key=lambda i: row[i])
        spread = sorted(row)[1] - sorted(row)[0] if len(row) > 1 else 0
        verdict = names[best] if spread >= 0.5 else "no clear fit"
        print(f"{o:<14}" + "".join(f"{v:>11.1f}" for v in row) + f"   {verdict}")
    print()
    print("A 'best fit' with <0.5 separation from the runner-up is not a real")
    print("identification — the lists overlap too much. Report it as unknown.")


if __name__ == "__main__":
    main()
