# In-Season Data Pipeline

Recurring pulls that keep recommendations fast and grounded during the season. Set these up as scheduled tasks; each one writes a JSON file that the other tasks and any live question can read, so a Wednesday-afternoon waiver question doesn't start from scratch.

All of this is a convenience layer, not a dependency. **If the data is stale or missing, ask David to paste his roster and the available pool and proceed** — the quality of the answer barely changes, only the speed.

## Credentials

Read from environment / `.env`, never from a file in this skill and never echoed into output:

`CBS_USERNAME`, `CBS_PASSWORD`, `FP_EMAIL`, `FP_API_KEY`

**Verified Aug 24 2026: none of these are on the VPS.** Every `.env` on that box belongs to another project (atmos-trip-planner, openclaw, traefik, finance). This credential list is aspirational — treat any claim that a key 'is in the .env' as unverified until grepped.

**No FantasyPros API endpoint has been verified.** `FP_API_KEY` exists in the `.env` on David's VPS, but nothing in this skill has ever confirmed a working URL, and Claude's sandbox cannot reach either the VPS or `api.fantasypros.com` — the network is allowlisted to package registries only. Treat "use the API" as unproven until someone actually gets a 200 back and records the endpoint here.

**What is verified (Aug 2026):** manual CSV export from `fantasypros.com/nfl/projections/{qb,rb,wr,te}.php` (Season/2026, Download), uploaded by David, parsed with `scripts/rebuild_board.py`. Round-trip tested: 9/9 players matched the existing board to within 0.1 pts.

**Trap to avoid:** the *Draft Rankings* export carries 2026 ranks alongside **2025 actual stats**, not projections. Check implied games-played (pass yards ÷ ~240) before scoring anything — if it scatters from 5 to 19 games across starting QBs, you have last season's actuals.

## Storage layout

```
/tx2025-data/
  fp-rankings-week-<N>.json        # ECR, projections, tiers by position
  fp-ros-projections-2026.json     # rest-of-season, refreshed monthly
  my-roster-week-<N>.json          # TX2025 roster, FAAB, record, opponent
  waiver-recommendations-week-<N>.json
  empty-stadiums-roster-2026.json  # post-draft
```

## Task 1 — FantasyPros rankings (daily, 6 AM PT)

Pull QB top 60, RB top 80, WR top 80, TE top 50: rank, name, team, bye, weekly projection, RoS projection, tier.

**Also pull per-player spread if the Pro export offers it** — low/high projections, or Best Rank / Worst Rank / Std Dev from the ECR export. The draft simulator currently applies a single uniform variance (20% sd) to every player, which is plainly wrong: a workhorse RB1 and a second-year WR do not have the same outcome distribution. Per-player spread would let the sim draw each player from his own distribution, break ties between similarly-valued players, and actually test the floor-early/upside-late heuristic instead of assuming it.

One judgment call worth encoding: **through week 8 use expert consensus; from week 9 on, use the best expert by position.** Early season, consensus smooths out noise from a tiny sample. Later, individual analysts have a track record for the year and the best one at a position beats the average of everyone.

Writes `fp-rankings-week-<N>.json`. No notification — other tasks consume it.

## Task 2 — CBS roster pull (Thu 10 AM, Sun 10 AM PT)

Runs after each waiver processes. From tx2008.football.cbssports.com: starters by slot, the 5 bench players, remaining FAAB, record, current opponent, and every player's bye week.

Writes `my-roster-week-<N>.json`.

## Task 3 — Pre-waiver recommendations (Tue 6 PM, Fri 6 PM PT)

Runs before each waiver deadline. Reads the roster and rankings files, then for each available player computes the RoS delta against the player he'd actually displace — not against an abstract baseline, since the question is always "does this improve my lineup," not "is this player good."

Bid tiers as a percentage of *remaining* budget (see `tx2025.md` for the full tier table). Output the top 5 ranked by RoS improvement, each with the displaced player, the delta, the reasoning, the dollar bid, and the percentage.

Writes `waiver-recommendations-week-<N>.json` and emails the list. Subject: `TX2025 Waiver Picks for Week <N> (bid before <time>)`.

## Task 4 — Weekly trade ideas (Mon 9 AM PT)

Reads David's roster, the RoS projections, and opponent rosters from the CBS league page. For each opponent, find the overlap between their surplus and his need, and the reverse — a trade only happens if both sides improve, so proposals that are merely good for David are wasted effort.

Value each proposal through `trade-values-2qb.md` (SF column, both charts averaged) and only surface ones landing in the fair band or better for David. Include the pitch he'd actually send.

## Task 5 — Lineup advice (Sun 8 AM PT)

Optimal starters for the week from current projections, with the close calls flagged and explained. In a 2QB league, the QB2 decision is frequently the biggest swing in the lineup — lead with it when it's live.

## Setup checklist

- [ ] Credentials in `.env` / password manager, nothing hardcoded
- [ ] FantasyPros Pro API access confirmed (or scraping fallback tested)
- [ ] `/tx2025-data/` created
- [ ] Tasks 1–5 scheduled
- [ ] One manual dry run of Task 3 before week 1, so the first live waiver isn't the first test


## FantasyPros public API — what it does and does not do (verified Aug 24 2026)

**Key works.** Stored at `/opt/ff/.env` on the VPS. Base `https://api.fantasypros.com/public/v2/json`, header `x-api-key`.

**The complete endpoint list** (from the OpenAPI spec David supplied — there are no others):
```
/{sport}/players            /{sport}/news              /{sport}/injuries
/{sport}/compare-players    /{sport}/{season}/rankings
/{sport}/{season}/consensus-rankings                   /{sport}/{season}/rankings/experts
/nfl/{season}/projections   /nfl/{season}/player-points
```

**It returns the NFL. It does NOT return David's leagues.** No roster endpoint, no league endpoint. A `league_key` parameter exists on the MLB projections endpoint only, and refers to MyPlaybook — FantasyPros' league-sync product, which authenticates with David's FP *login*, not this API key. **Do not tell David the API can see his ESPN or CBS rosters. It cannot.** Rosters come from screenshots or from David directly.

**Two useful details found in the spec:**
- `/nfl/{season}/projections` takes **`week`** and **`ros`**. Weekly projections for start/sit, rest-of-season for trade valuation — both from the same key. This is the in-season pipeline.
- `/{sport}/players` carries **`espnid` and `yahooid`** cross-references, which allows exact ID matching between FantasyPros and ESPN instead of fuzzy name matching.

**NFL projections parameters:** `positions` (colon-delimited, e.g. `QB:RB:WR:TE`), `players`, `week` (0 = preseason/full-season), `ros`.
**consensus-rankings parameters:** `position` (single position only — `ALL` is rejected with a 400), `scoring`, `type`.
