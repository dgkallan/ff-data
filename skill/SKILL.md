---
name: fantasy-football
description: David's fantasy football command center for his two 2026 leagues — TX2025 (Theta Xi, 12-team true 2QB, no K/DEF, on CBS) and Empty Stadiums (8-team PPR on ESPN, pick 2). Use this skill for live draft assistance, draft prep and board building, FAAB waiver bidding, trade evaluation, and weekly lineup calls. Trigger it whenever David mentions a draft, a pick, waivers, FAAB, a trade offer, a start/sit question, his roster, ESPN or CBS league pages, FantasyPros rankings/ECR/ADP, or names fantasy players in a decision context — even casually, like "who do I take at 15?", "is this trade fair?", or "$1800 left, who do I bid on?". Also use it when he asks to set up recurring fantasy data pulls.
---

# Fantasy Football Manager

David plays in two leagues with opposite shapes. Most wrong answers in fantasy come from applying one league's instincts to the other, so **first establish which league the question is about.** If it's ambiguous, ask — one short question beats a confidently wrong recommendation.

| | **Empty Stadiums** | **TX2025 (Theta Xi)** |
|---|---|---|
| Platform | ESPN | CBS (tx2008.football.cbssports.com) |
| Size / format | 8-team **superflex** full PPR, 6-pt pass TD, 2 IDP, no K/DST | 12-team **TRUE 2QB** (flex is RB/WR/TE, *not* superflex), PPR, **no K/DEF** |
| Draft | **DONE** — Aug 22 2026, pick 2 | **DONE** — Aug 29-30 2026, slot 9. Final roster in `live-state-2026.md`. |
| QB posture | Both leagues start 3 QBs (2 + OP). In Empty Stadiums the QB tier is flat and deep and ESPN buries it — **take no QB before round 5**. | **Do NOT "pay up" — that advice was wrong and is retracted.** QB6–QB15 spans 14 pts. Only Josh Allen justifies a premium pick. Take QB1 at the 2/3 turn, QB2 by pick 50, **QB3 in R6–7 as a trade asset**. See `valuation-model.md`. |
| Waivers | **$500 continuous FAAB, 6 nights/week** — `references/faab-waivers.md` | **FAAB is UNEQUAL: $2,500 for managers who went on the New Orleans trip, $2,000 for everyone else.** David is on the $2,500 tier — confirm which opponents are too. Wed & Sat runs. |
| Reference | `references/empty-stadiums.md` | `references/tx2025.md` |

Read the relevant league reference before answering anything league-specific. They hold the settings, scoring, and strategy that make a recommendation right rather than generic.

## Routing

| David says | Go to |
|---|---|
| "who do I take", "pick 15", draft in progress | `references/live-draft-playbook.md` — read its HARD RULES section first and follow them exactly; `references/draft-postmortem-2026.md` explains why each rule exists |
| Draft prep, board, ADP, VORP, tiers | `references/live-draft-playbook.md` (setup section) + `scripts/build_board.py` |
| Waivers, FAAB, "who should I bid on" — **Empty Stadiums** | `references/faab-waivers.md` — bid tiers, the 6-night calendar, scarcity math |
| Waivers, FAAB — **TX2025** | `references/tx2025.md`, waiver section |
| "What's on the wire", streaming IDP / QB / returners | `references/faab-waivers.md`, league-specific edges |
| Trade offer, "is this fair" — **Empty Stadiums** | `references/trades.md` for tactics + `references/trade-value-model.md` for the math; run `scripts/trade_value.py` rather than valuing by hand |
| **Evaluating a specific trade** | `references/trade-value-model.md` — **read the "Evaluating a trade" method section first.** Non-negotiable: run the before/after optimal lineup on BOTH rosters (a chart value is context, never the verdict); decompose the delta by slot; pull `rank_ecr/min/max/std` for every player including the bench backfill, because a points gain can be a certainty loss; treat bench players as worth ~0 to both sides; scan all opponents before negotiating with whoever asked; rank candidates by `min(your gain, their gain)`. |
| "What's X worth", buy-low / sell-high | `references/trade-charts-2026.md` — **per-league value charts** (TX2025 and Empty Stadiums, rescored under each league's own rules), plus `references/trade-value-model.md` for the true-vs-market arbitrage. **Never quote a cross-league value:** Josh Allen is the #3 asset in TX2025 (97.5) and the #11 in Empty Stadiums (47.1), because replacement is 175 in one room and 360 in the other. The chart is a screen; the verdict is always a before/after lineup comparison on both rosters. |
| **Waiver adds / stashing** | `references/faab-waivers.md` — read "Roster-spot scarcity" first. **Measure wire depth (drop from best to 5th available) before recommending any stash.** A roster spot holds what you cannot get later, not the best player available. TE with 8 available inside 17 pts = never stash; the gap is payable in one claim when the injury happens. Cheap to replace = worthless to trade; same fact. |
| **IN-SEASON WEEKLY LOOP — this is the current mode** | Thu/Sun: `scripts/pull_league.py --repo dgkallan/ff-data` for state, then (a) **waivers** — apply "Roster-spot scarcity" from `faab-waivers.md`, measure wire depth before any stash; (b) **lineups** — weekly projections + ECR + injury probabilities, not season totals; (c) **trades** — the 8-rule method in `trade-value-model.md`. **News-check every named player before recommending.** |
| **In-season: "pull the league", waivers, weekly trades** | `scripts/pull_league.py --repo <owner>/ff-data`. League state arrives via a GitHub relay written twice weekly by a Cowork task — spec in `references/relay-spec.md`. Runs **Thursday and Sunday 6am, AFTER waivers process** (deadlines are Wed/Sat nights). The brief surfaces state only; waivers need RoS projections, lineups need weekly projections + ECR + injury probabilities. |
| **David shares an article / analyst take** | `references/expert-board-2026.md` — running log of expert upside and value calls. **Append a new entry; never overwrite.** Record player, the expert's ADP, the case in one line, and the TX2025 board points + room ADP alongside. Always convert national ADP to room ADP (national is 1QB; TX2025 starts two, so skill players drift ~25-45 picks later here). Surface the relevant entry when that player is on the clock. |
| **ANY new session — read this first** | `references/live-state-2026.md` — **both leagues are drafted; this is in-season now.** Final rosters for TX2025 and Empty Stadiums, the live watch items (Jeanty's ankle, the Jacobs suspension and the GB committee, Geno as the trade asset), and pipeline status. |
| **Before the next draft in this league** | `scripts/pull_adp_sources.sh` (VPS) then `scripts/source_fingerprint.py` — fingerprint which ranking list each manager drafts from. The 2026 room tracked CBS positional rank at **0.935 Spearman**, which made Nix (CBS QB10 / our QB3) and Shough (CBS QB8 / our QB5) free. See "Fingerprint each manager's ranking source" in `tx2025.md`. |
| **Mid-draft, round 3 onward (next draft)** | **`scripts/replan.py` — run at EVERY pick.** Re-optimises the remaining position sequence against the live board. The pre-draft plan is a prior, not an instruction. It caught a QB2 move from round 6 to round 4 on Aug 29. But do not pivot on a feeling — when the room surprised us the plan still won by 35; test before changing. See "Adaptive re-planning" in `tx2025.md`. |
| **NEXT TX2025 draft (2027) — "who do I take", pick screenshots** | **`scripts/tx2025_live.py`.** Read the screenshot for who is gone, then run it. It enforces the postmortem rules mechanically: gap-to-next-survivor first, deviation needs gap ≥30 AND +20 over the plan gap, bench-only positions zeroed, unknown names flagged, roster read from input not memory. Never recommend from memory or eyeball — run the script. **Then web-search the player before naming him** — role, depth chart, injury, QB competition. See "How David works" in `tx2025.md`; this check is mandatory, not optional, and the long gaps between picks exist for it. |
| **Any TX2025 valuation, VORP, replacement level, or "what would X fetch"** | `references/valuation-model.md` — **read this before quoting any TX2025 number.** **State which replacement baseline you are using — it swings a QB by 85 pts.** Trades use baseline D (first waiver player). Drafting uses NO static baseline: the measure is gap-to-next-survivor, evaluated as a TWO-PICK BUNDLE whenever a position's cliff exceeds 50 pts. Format-scored points, the three-layer engine, what verification it survived, and why VORP is right for drafting but wrong for trading |
| Trade offer — **TX2025** | `references/trade-values-2qb.md` + `references/tx2025.md` |
| Start/sit, lineup, "who do I play" — **Empty Stadiums** | `references/weekly-lineup.md` — the projection rule, the OP-slot call, lock timing |
| Start/sit — **TX2025** | `references/tx2025.md` for scoring, then current FantasyPros projections |
| "Set up daily pulls", automation | `references/data-pipeline.md` |

## How to answer

David is usually on a clock — mid-draft, or minutes before a waiver deadline. Structure everything punchline-first:

1. **The call**, in one line: a named player, a dollar amount, accept or decline.
2. **The math**, in 1–2 sentences with actual numbers ("McBride projects 208, TE8 projects 146 → +62 VORP").
3. **The fallback**, because targets get sniped and bids get outbid more often than not.

Hedging is the main failure mode. "It depends on your risk tolerance" is not an answer when the pick clock reads 40 seconds. Commit to a recommendation, then name the one condition that would change it. If the data is genuinely too thin, say what's missing and still give the best available call.

## Recommendations need current information

Fantasy value moves daily — injuries, depth-chart changes, beat reporting. Everything in these reference files was true when written and may not be now. Before a real recommendation on a specific player, check current news; a strategy doc written three days ago doesn't know about last night's hamstring.

FantasyPros is the primary data source (David has a Pro subscription). **Verified path, Aug 2026: manual CSV export from the projections pages** — `fantasypros.com/nfl/projections/{qb,rb,wr,te}.php`, set to Season/2026, Download button. David uploads the four files; run `scripts/rebuild_board.py` on them.

**The FantasyPros data API is CLOSED to David. Do not retry it.** Tested live on his VPS, Aug 24 2026: a valid 40-character `FP_API_KEY` returned **HTTP 403 `{"message":"Forbidden"}` on every endpoint** — projections, consensus-rankings, and even the trivial `/articles` path, across both `/v2/` and `/public/v2/` base URLs. The key loads fine (length 40, no quotes/whitespace); it is simply not authorized for the data API. FantasyPros gates data keys to their **HOF tier**, not Pro — David's key is almost certainly a MyPlaybook/league-sync or affiliate credential.

Endpoints, recorded only so a future session doesn't re-derive them if David ever activates a real data key:
```
GET https://api.fantasypros.com/v2/json/nfl/{season}/projections?position=ALL&week=0&scoring=PPR
GET https://api.fantasypros.com/public/v2/json/nfl/{season}/consensus-rankings?position=RB&scoring=PPR&type=draft
header: x-api-key
```
**Usage was verified correct against FantasyPros' own docs (api.fantasypros.com/v2/docs) — do not re-research it.** Header is `x-api-key`, endpoint shape is right, `week=0` = preseason. The decisive test: `/v2/json/nfl/articles` takes NO parameters and still 403s, so no request shape can be at fault. FantasyPros grants data keys by email request ("You can email us here about getting a FantasyPros API key"); they are not included with Pro.

**If David ever obtains a real data key, the payoff is one call:** `GET /v2/json/nfl/{season}/consensus-rankings?position=ALL&scoring=PPR` returns `rank_ecr, rank_min, rank_max, rank_ave, rank_std, pos_rank, player_bye_week` per player — the expert spread the simulator currently fakes with a uniform 20% sd. Note `position=ALL` is valid for consensus-rankings but NOT for projections (use `positions=QB:RB:WR:TE` there).

Plumbing is already in place if a key ever works: `/opt/ff/` on the VPS, `scripts/fp_fetch.py`, and the `.env` pattern. **Before spending any time on it, run one curl and check for a 200.** Two prior sessions burned time on this — one on a nonexistent endpoint, one on a key that turned out to be unauthorized.

**USE THE CSV PATH.** It is the only verified route and it is fully tested (9/9 players matched the board to within 0.1 pts).

Run `scripts/fp_fetch.py` on any machine that has the key exported. **Claude's sandbox cannot reach `api.fantasypros.com` or the VPS** — network is allowlisted to package registries only. David runs the script and uploads the JSON. A cron→GitHub relay is possible (raw.githubusercontent.com *is* reachable) but means either a public repo, which redistributes licensed FantasyPros data, or a private one needing a token Claude shouldn't hold. Manual upload is the right call for a once-a-year draft.

**Two export types, only one is usable.** The *Rankings* export (`FantasyPros_2026_Draft_ALL_Rankings.csv`) pairs 2026 ranks with **2025 actual stats** — Burrow shows 1,809 pass yards because he missed nine games last year. Ingesting it silently would have dropped him from 388 pts to ~180. Always sanity-check pass yards against a ~17-game season before scoring anything; wildly varying implied games-played means you have last year's actuals, not projections. The *Projections* export is the right one and has an **INTS** column, which the rankings export lacks.

For live ESPN and CBS draft rooms and league pages, read the open tab via Claude in Chrome — neither platform exposes a usable public API here.

## Credentials

Never write David's CBS, ESPN, or FantasyPros passwords into files, code, or output. They live in his password manager or `.env` and are referenced as environment variables (`CBS_USERNAME`, `CBS_PASSWORD`, `FP_EMAIL`, `FP_API_KEY`). If a login is needed and unavailable, ask him to enter it himself rather than working around it.

## Bundled resources

- `references/roster-2026.md` — **David's actual Empty Stadiums roster** with projections, weak slots, and action items. The starting point for every in-season question; keep it updated after every transaction

- `references/empty-stadiums.md` — ESPN 8-team league profile and draft-day plan
- `references/espn-8team-draft-strategy-2026.md` — full 2026 strategy doc: pick-by-pick plan, targets, avoids
- `references/tx2025.md` — CBS true-2QB league: scoring, roster, FAAB tiers, waiver and trade workflow, and the **rewritten draft section** (flat QB band, Anchor RB, deliberate QB3, draft position doesn't matter)
- `references/valuation-model.md` — **the TX2025 valuation engine.** Three layers (format points → VORP → market price), the verification log including two withdrawn claims, why VORP breaks on a full roster, and how draft / mid-draft / trade / waiver each use it differently
- `references/trade-values-2qb.md` — The Score + FantasyPros 2QB/SF value charts and the averaging method
- `references/scoring-values.md` — **read this before any Empty Stadiums draft decision.** Conversion multipliers, position value buckets, replacement levels, and the players whose national ranking misleads in this format
- `references/trade-value-model.md` — **the trade value algorithm.** How KTC/FantasyCalc/Stats Guy build charts and why none fit this league; the marginal-lineup metric; why values are path-dependent and must never be summed; the true-vs-perceived split that prices hype, recency, TD luck and draft-cost anchoring
- `scripts/trade_value.py` — runnable implementation. `--demo` shows the value table, path dependence, consolidation thresholds, and a worked buy/sell arbitrage
- `references/trades.md` — **Empty Stadiums trades.** Real value vs. projection (they diverge wildly), why bench players are worth zero and consolidation is free, the ESPN arbitrage and when it expires, the OP-slot sell market, offer-evaluation format
- `references/weekly-lineup.md` — **Empty Stadiums start/sit.** Why projection beats variance (simulated), the OP-slot decision, individual-lock option value, bye handling, and the correct projection source
- `references/faab-waivers.md` — **Empty Stadiums in-season acquisition.** $500 continuous FAAB, the six-night processing calendar and its two real deadlines, 8-team scarcity math (QB is scarce, IDP is free), bid tiers, budget pacing, IR and bench rules
- `references/live-draft-playbook.md` — draft-day operating procedure, phase logic, response format, and the seven HARD RULES from the 2026 draft
- `references/draft-postmortem-2026.md` — **the six failures from the Aug 2026 draft**, root causes, and the rule each produced. Required reading before any live draft
- `references/mock-calibration.md` — how to make the FantasyPros simulator behave like this league, and what four mock runs established
- `references/data-pipeline.md` — recurring data pulls and file layout for in-season automation
- `references/test-scenarios.md` — worked examples showing the shape of a good answer
- `scripts/build_board.py` — builds a VORP-ranked, league-size-adjusted draft board from projections
