#!/usr/bin/env python3
"""Rebuild tx2025_board.json from FantasyPros projection CSVs.

USAGE
  python3 rebuild_board.py qb.csv rb.csv wr.csv te.csv [--out tx2025_board.json]

Accepts the raw CSV export from FantasyPros projections pages
(/nfl/projections/qb.php etc., "Download" button). Column names vary and
repeat (YDS appears for both passing and rushing) so the parser resolves
them positionally within each stat group rather than by name alone.

Scores every player under TX2025 rules, keeps the observed Theta Xi ADP
(which comes from 240 real league picks and does NOT change with new
projections), and writes the board the live assistant reads.
"""
import sys, os, json, math, re, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
G = 17.0


def games_over(total, thresh, cv):
    mu_g = total / G
    if mu_g <= 0:
        return 0.0
    s = math.sqrt(math.log(1 + cv * cv))
    mu = math.log(mu_g) - s * s / 2
    return 0.5 * math.erfc(((math.log(thresh) - mu) / s) / math.sqrt(2)) * G


def qb_pts(py, ptd, i, ry, rtd, fl):
    return py / 25 + 6 * ptd - i + ry / 10 + 6 * rtd - 2 * fl + 3 * games_over(py, 300, 0.38)


def sk_pts(rec, ryd, rtd, rush, rushtd, fl):
    return (rec + ryd / 10 + 6 * rtd + rush / 10 + 6 * rushtd - 2 * fl
            + 3 * games_over(ryd, 100, 0.75) + 3 * games_over(ryd, 200, 0.75))


def read_csv(path):
    import csv
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.reader(f))
    # find the header row (first row containing a 'player'-ish cell)
    hi = 0
    for i, r in enumerate(rows[:5]):
        if any(c.strip().lower() in ("player", "name") for c in r):
            hi = i
            break
    hdr = [c.strip() for c in rows[hi]]
    return hdr, [r for r in rows[hi + 1:] if r and r[0].strip()]


def num(x):
    x = re.sub(r"[^0-9.\-]", "", str(x))
    try:
        return float(x) if x not in ("", "-", ".") else 0.0
    except ValueError:
        return 0.0


def cols(hdr, want):
    """Indices of every column whose name matches `want` (case-insensitive)."""
    return [i for i, h in enumerate(hdr) if h.strip().lower() == want.lower()]


def parse(path, pos):
    hdr, rows = read_csv(path)
    low = [h.strip().lower() for h in hdr]
    pi = 0
    for i, h in enumerate(low):
        if h in ("player", "name"):
            pi = i
            break
    yds, tds, att = cols(hdr, "YDS"), cols(hdr, "TDS"), cols(hdr, "ATT")
    if not tds:
        tds = cols(hdr, "TD")
    rec = cols(hdr, "REC")
    ints = cols(hdr, "INTS") or cols(hdr, "INT")
    fl = cols(hdr, "FL")
    out = []
    for r in rows:
        if len(r) <= pi:
            continue
        name = re.sub(r"\s*\([^)]*\)\s*$", "", r[pi]).strip()
        name = re.sub(r"\s+(QB|RB|WR|TE)$", "", name).strip()
        # FantasyPros appends the team code: "Josh Allen BUF" -> "Josh Allen"
        name = re.sub(r"\s+(ARI|ATL|BAL|BUF|CAR|CHI|CIN|CLE|DAL|DEN|DET|GB|HOU|IND|JAC|JAX|KC|LV|LAC|LAR|MIA|MIN|NE|NO|NYG|NYJ|PHI|PIT|SF|SEA|TB|TEN|WAS|FA)$", "", name).strip()
        if not name or name.lower() in ("player", "name"):
            continue
        g = lambda idxs, n: num(r[idxs[n]]) if len(idxs) > n and len(r) > idxs[n] else 0.0
        if pos == "QB":
            # passing YDS/TDS first, rushing second
            pts = qb_pts(g(yds, 0), g(tds, 0), g(ints, 0), g(yds, 1), g(tds, 1), g(fl, 0))
        elif pos == "RB":
            # rushing YDS/TDS first, receiving second
            pts = sk_pts(g(rec, 0), g(yds, 1), g(tds, 1), g(yds, 0), g(tds, 0), g(fl, 0))
        else:  # WR / TE — receiving first, rushing second
            pts = sk_pts(g(rec, 0), g(yds, 0), g(tds, 0), g(yds, 1), g(tds, 1), g(fl, 0))
        out.append({"name": name, "pos": pos, "pts": round(pts, 1)})
    out.sort(key=lambda p: -p["pts"])
    for i, p in enumerate(out, 1):
        p["rank"] = i
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csvs", nargs=4, help="qb.csv rb.csv wr.csv te.csv (in that order)")
    ap.add_argument("--out", default=os.path.join(HERE, "tx2025_board.json"))
    a = ap.parse_args()

    old = {p["name"]: p for p in json.load(open(os.path.join(HERE, "tx2025_board.json")))}
    # Observed Theta Xi ADP — from 240 real league picks. Independent of projections.
    ADP = {"QB": [1,2,3,4,5,7.5,11.5,13,14.5,18,20,25,29.5,32.5,34.5,36.5,39,42,50,53,55,58,61,66,70,76],
           "RB": [7,11,12.5,18,21,24.5,27.5,29,32,34.5,40,41.5,46,50,51,54,58,59,60,66,72,78,84,90,96,102],
           "WR": [6.5,10,15.5,17,19,21.5,23,25.5,30,38,47,50.5,52,53.5,56,58,64,65,67,72,77,82,87,92,97,102],
           "TE": [35,68,71,91,105,112,115.5,124,132,140,148,156,164,172]}

    def adp_of(pos, r):
        t = ADP[pos]
        return t[r - 1] if r <= len(t) else t[-1] + (r - len(t)) * (7 if pos == "QB" else 4)

    board, moved = [], []
    for path, pos in zip(a.csvs, ("QB", "RB", "WR", "TE")):
        cap = {"QB": 40, "RB": 55, "WR": 75, "TE": 26}[pos]
        for p in parse(path, pos)[:cap]:
            o = old.get(p["name"])
            if o and abs(o["pts"] - p["pts"]) >= 25:
                moved.append((p["name"], pos, o["pts"], p["pts"], o["rank"], p["rank"]))
            p["bye"] = o["bye"] if o else 0
            p["adp"] = round(adp_of(pos, p["rank"]), 1)
            board.append(p)

    json.dump(board, open(a.out, "w"), indent=0)
    print(f"wrote {len(board)} players -> {a.out}")
    for pos in ("QB", "RB", "WR", "TE"):
        c = [p for p in board if p["pos"] == pos][:5]
        print(f"  {pos}: " + " | ".join(f"{p['name']} {p['pts']:.0f}" for p in c))
    missing = [p["name"] for p in board if not p["bye"]]
    if missing:
        print(f"\n!! {len(missing)} players have no bye week (new to the board): "
              + ", ".join(missing[:8]) + ("..." if len(missing) > 8 else ""))
        print("   Fill byes before the draft or the week-11 check will miss them.")
    if moved:
        print(f"\n!! {len(moved)} players moved 25+ pts vs the old board — verify these:")
        for n, pos, a_, b_, ra, rb in sorted(moved, key=lambda x: -abs(x[3] - x[2]))[:12]:
            print(f"   {n:<22}{pos}  {a_:.0f} -> {b_:.0f}   (rank {ra} -> {rb})")


if __name__ == "__main__":
    main()
