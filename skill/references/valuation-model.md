# TX2025 Valuation Framework

One valuation engine, four jobs: pre-draft board, live pick decisions, trade evaluation, waiver bidding. This documents what the engine is, what verification it survived, where it breaks, and how each job uses it differently.

**League:** CBS Theta Xi. 12 teams. **No K, no DEF.** Starters (9): 2QB / 2RB / 3WR / 1TE / 1 FLEX (RB/WR/TE). Bench 5. Roster 14 → **168 total picks, 14 rounds.**

---

## 1. The engine

Three layers. Each is a separate object and they must not be conflated.

**Layer 1 — Format points.** Real projected stat lines scored under TX2025 rules: 6-pt pass TD, −1 INT, +3 at 300+ pass yds, full PPR, 6-pt rec TD, +3 at 100+ rec yds, +3 more at 200+. Per-game bonus frequencies are derived from season totals via a lognormal game distribution, not assumed. This layer is *format truth* and is the only layer that never needs a judgment call.

**Layer 2 — VORP.** Points minus a positional replacement baseline. This makes positions comparable. It requires choosing a baseline, and that choice is the single biggest lever in the whole system (see §2, Test 3).

**Layer 3 — Market price.** The trade chart is a pick-slot curve (1.01=69 → 1.12=38 → R4=12 → R6+=8, zero past pick 84). Map a player's ADP to that curve and you have what the room will charge for him.

**The arbitrage is Layer 3 minus Layer 2.** Everything actionable comes from that gap.

---

## 2. Verification results

### Test 1 — Is market price linear in VORP? **PASS**

I expected this to fail. The trade chart decays steeply (69 → 8 over 84 picks) while VORP decays gently, so a straight-line fit should have produced fake "elite players are overpriced, mid-round players are underpriced" residuals.

It didn't. **Correlation between residual and ADP is −0.084** — essentially zero. A linear fit explains **R² = 0.764**. A power fit was materially worse. The linear model is sound, and the individual target/fade list built on it stands.

**Exchange rate: 1 chart point ≈ 3.0 TX2025 fantasy points.**

### Test 2 — Convexity correction. **DISCARDED**

The power-law alternative fit at exponent 0.43 with R² = 0.426 — much worse than linear, and its residuals were an artifact of log-space fitting evaluated in linear space. My own test was flawed. Ignore its output; Test 1 already settled the question.

### Test 3 — Are positional-share verdicts stable? **FAIL**

This is the one that broke. Ratio of market-capital share to VORP share, under three defensible replacement baselines:

| Baseline | QB | RB | WR | TE |
|---|---|---|---|---|
| Market-implied (QB26/RB25/WR28/TE8) | 0.84 | 1.08 | 1.03 | 1.59 |
| Last-starter (QB25/RB29/WR42/TE13) | **1.21** | 1.08 | 0.79 | **1.04** |
| Deep-roster (QB32/RB40/WR55/TE16) | **0.67** | 1.43 | 1.07 | **1.81** |

**QB flips sign** (0.67 underpriced → 1.21 overpriced). **TE swings 1.04 to 1.81.** Only RB is directionally stable, and it sits at or above 1.08 everywhere.

**Consequence: the positional-share diagnostic is not trustworthy and should not drive decisions.** Two claims I made from it are hereby withdrawn — "QB is underpriced, target it" and "TE is overpriced at 1.59x, fade it." Neither survives a change of baseline.

What replaces them: judge players by **individual residual from the validated linear fit**, which doesn't depend on the baseline choice in the same way. On that measure McBride and Bowers land in neither the target nor the fade list — **elite TE is fairly priced.** Not the bargain I called it two turns ago, not the trap I called it one turn ago.

### Test 4 — Does VORP sum correctly in trades? **FAIL, by design**

Trading for Amon-Ra St. Brown when you already start three WRs: naive VORP says +115. But he displaces your flex, and the flex was already a WR4-caliber player. **Real lineup gain: +60. VORP overstates by 1.9x.**

This confirms what `trade-value-model.md` already says — values are path-dependent and must never be summed. **VORP is correct for drafting an empty roster and wrong for trading a full one.**

---

## 3. Application: draft position

**Verdict: draft slot is not worth optimizing.** The rebuilt simulation (real projections, correct replacement, 40 sims × 72 cells) put the best-achievable spread across all twelve slots at 2418–2498 points, an 80-point range against a ±31 standard error — roughly an 85-point noise band. The slots are statistically indistinguishable.

My earlier ranking of "pick 1, then 2, then 6" was reading noise as signal, on top of a model with an inflated QB curve. Retracted. Pick 2 is fine; so is any other slot.

The valuation's real contribution here is negative knowledge: it tells you where *not* to spend effort.

---

## 4. Application: pre-draft strategy

Strategy differences are real where slot differences aren't. At pick 2, 200 sims per strategy:

| Strategy | Points | Verdict |
|---|---|---|
| **Anchor RB** | **2424 ±13** | best |
| Late QB (R6) | 2412 ±14 | within noise |
| Hero WR | 2395 ±13 | within noise |
| Pure BPA | 2388 ±13 | within noise |
| Dual Early QB | 2366 ±15 | **significantly worse** |
| Split QB (R1+R4) | 2362 ±14 | **significantly worse** |

The top four are a cluster; the two QB-first strategies are genuinely worse. Note this simulation scores **actual starting-lineup output**, so it is baseline-free — it does not inherit the Test 3 fragility. That independence is why it's the strongest result in the system.

The mechanism, from Layer 1 directly: QB6 through QB15 spans 14 points (365 → 351). Ten quarterbacks of near-identical value means paying a premium inside that band is waste. Josh Allen (+34 over QB2) is the sole exception. The real cliff is QB25 → QB30, a 72-point fall, which is what forces two QBs by roughly pick 50 — scarcity of *usable* arms, not competition for *elite* ones.

---

## 5. Application: mid-draft

VORP is the wrong tool once the draft is live, because it ignores your pick schedule. The right tool is **VONA — value over next available.**

For each candidate at the current pick:

```
VONA(player) = player.points − E[best points at his position at my next pick]
```

where the expectation comes from ADP survival probability across the gap. Your gaps from slot 2 are: 2 → 23 (21 picks), 23 → 26 (3), 26 → 47 (21), 47 → 50 (3), and so on.

This produces the behavior you actually want at a turn. At 23/26 the gap is three picks — almost everyone survives — so take the scarcer position first and the deeper one second. At 26 → 47 the gap is 21 picks, so positions about to be stripped get priority regardless of raw VORP.

Live loop each pick: update the pool with what's gone, recompute survival odds from observed draft pace rather than static ADP, rank candidates by VONA, and report the top call plus one fallback. Also track the QB drain count — if the room is running hotter than ~10 QBs gone by pick 24, the pick-50 QB2 deadline moves up.

---

## 6. Application: post-draft — trades

Test 4 rules out using VORP here. Trades use **marginal lineup delta**, computed separately for each side:

```
Δ = (my optimal starting lineup WITH the deal) − (my optimal lineup WITHOUT it)
```

Optimal lineup means the 2/2/3/1/flex solve, so a fourth good WR is scored at what he adds over your current flex, not over WR28. Compute the same figure for the opposing roster. A deal can be positive for both — that's what makes trades happen — and the comparison is the two deltas, never a sum of chart values.

Then apply context the numbers can't see: bye collisions, Weeks 15–17 schedule, whether the deal repairs the opponent's only hole, and never trading your QB2 in a 2QB league.

The trade chart still has a role, but a different one: it prices what the *other manager* thinks he's giving up. Gap between his perceived price and your marginal delta is the negotiating room.

## 7. Application: post-draft — waivers

Same marginal-delta engine, different denominator. The comparison is the target's rest-of-season projection minus the RoS projection of whoever you'd actually drop — not against a theoretical replacement rank.

Convert to a bid using the tiers already in `tx2025.md`, as a share of *remaining* budget: Tier A (+50 RoS or better) 15–25%, Tier B (+30–50) 8–15%, Tier C (+10–30) 3–7%, Tier D (under +10) 1–3%. Rank 3–5 targets in bid order with explicit fallbacks, since your Wednesday and Saturday runs mean a losing bid isn't a lost week. Flag any bid that would drop the reserve below a third of the original $2,500 with a month or more left.

---

## 8. What changes once the season starts

**Layer 1 gets replaced, not adjusted.** Preseason projections give way to a blend of actual production and rest-of-season forecast, weighted toward actuals as the sample grows — roughly 30% actual at Week 4, 60% by Week 8, 80% by Week 12.

**Layer 2 gets recomputed off the real wire.** Replacement level stops being a theoretical rank and becomes the best player genuinely available on waivers at that position, which in a 12-team 2QB league means QB replacement collapses to near-unusable by midseason while WR replacement stays healthy. This is the single largest in-season shift, and it is why a QB3 accrues trade value as the season runs.

**Layer 3 decays.** The trade chart is a *draft-pick* curve; its relevance fades once picks stop existing. By roughly Week 6 it should be treated as a prior on how other managers price players, not as a value source.

**What doesn't change:** the scoring conversion in Layer 1, the marginal-lineup principle, and the rule that values are path-dependent and never summed.

---

## 9. Known weaknesses

- Single projection source (Fantasy Six Pack). Re-run against FantasyPros Pro before Aug 29 2026 — and AFTER final NFL roster cuts (~Aug 26).
- ADP proxy is FanDuel *superflex* consensus, which over-drafts QBs relative to true 2QB. Real CBS draft-room ADP would sharpen every Layer 3 number.
- Projections assume 17 games for everyone; no injury or holdout pricing.
- The 12 flex slots were allocated 5 RB / 6 WR / 1 TE by judgment. Test 3 shows how much rides on that, which is precisely why the positional-share diagnostic was demoted.
- Simulation CPU behavior is modeled, not observed. Actual Theta Xi draft history would calibrate it.

---

## 10. Draft-strategy consequences of the trade asymmetry

Two plays were tested once the post-draft trade math was built. One died, one is now standing policy.

**Allen-to-flip — REJECTED.** Drafting an elite QB purely to trade him mid-season nets ~+1 point: QB-first strategies cost 58 points in simulation, and the best realistic Allen return (Gibbs + Breece Hall, +59) exactly cancels it. It also depends on a desperate buyer existing. Not a strategy.

**Deliberate QB3 — ADOPTED.** See `tx2025.md` draft section. Costs a 6th-round pick and zero lineup points; worth +112 to an injured team. This is the single most robust finding in the model because it does not depend on being right about anything — a free option.

### Why a QB gains value between draft day and midseason

On draft day the alternative to Josh Allen is "a flat-band QB in round 4 at 351," so his marginal value is only ~71. By November the alternative is "the wire at 219," so his marginal value is ~203. **The same player nearly triples in marginal worth without changing his projection**, purely because the flat band gets drafted away and cannot be replenished in a 24-slot league.

This is the central exploitable fact about the format. It means: never value a QB in this league with a static number, always price him against what the *acquiring* roster's alternative actually is.

### Worked example — what Josh Allen fetches post-draft

Against a QB-poor, RB-rich counterparty (their QB2 = Cam Ward, 278):

| Package | My Δ | Their Δ | Their mkt outlay |
|---|---|---|---|
| Gibbs + Chase Brown | +89 | −23 | 85 (they decline — use as anchor) |
| **Gibbs + Breece Hall** | **+59** | **+7** | **76** ← settle here, captures 89% of surplus |
| Bijan + Breece Hall | +52 | +14 | 74 |
| Bijan + Judkins | +35 | +32 | 70 ← walk-away floor |

Allen's chart price is 69; the buyer pays 74–76 because their QB hole cannot be fixed on waivers while their RB3/RB4 sit on the bench contributing zero. **That asymmetry is the whole trade.** Against a team already holding two flat-band QBs, Allen's marginal value to them collapses to ~30 and there is no deal.

## Replacement level: the measure point is the whole answer (Aug 30 2026)

David's challenge — "when you pick your VORP, are we picking the right measure point?" — and the answer was no.

**The baseline choice swings a QB by 85 points.** Same player, same projection:

| Baseline | QB | RB | WR | TE | Nix VORP |
|---|---|---|---|---|---|
| A. last starter (24/24/36/12) | 310 | 180 | 186 | 169 | **50** |
| B. starter + flex split | 310 | 166 | 179 | 169 | **50** |
| C. last drafted at that position | 276 | 115 | 144 | 158 | **84** |
| D. first waiver player | 225 | 102 | 129 | 154 | **135** |

Claude's first VORP analysis used ~B — the baseline *least* favourable to QBs — then concluded "VORP undervalues QBs in 2QB." **Part of that conclusion was an artifact of the baseline choice, not a property of VORP.** Say which baseline you are using before quoting any VORP number.

### The rule

**Trades → static VORP at baseline D (first waiver player).** In-season the counterfactual for losing a player genuinely is the wire, so D is correct. This is what `trade_chart.py` should use.

**Drafting → NOT a static baseline at all.** The question at a pick is not "what is he worth over a scrub," it is:

> **What is the best player at this position I can still get at my NEXT pick?**

That is dynamic, changes every pick, and depends on your own pick schedule. It is the gap-to-next-survivor number `tx2025_live.py` already computes. A fixed replacement table cannot express it.

### And gap-to-next-survivor is still myopic — use the two-pick bundle

Single-pick gap under-counts when a position is collapsing. At pick 33 the QB gap to pick 40 was only **21** (Nix 360 → Shough 339), which argues for taking a skill player. But the right unit was the **two-pick bundle**: Nix + Shough = 699 versus one arm + a receiver, because 12 QB slots were chasing 13 usable arms and the tier behind them fell 81 points.

**Evaluate the next TWO picks as a bundle whenever a position's cliff exceeds ~50 points.** Compare `best-now + best-surviving-to-pick-2` against `best-other-position-now + best-position-surviving`.

### Cliff test — when to distrust any replacement baseline

Compute the drop from the replacement player to five spots below him.

- **under ~20 pts** — tier is deep, replacement is real, VORP works
- **over ~50 pts** — replacement is a fiction; there is nothing behind it. Count league-wide supply vs demand instead.

2026 TX2025 example: **QB25 = 307, QB30 = 225 — an 81-point cliff.** With 24 starting slots the 25th arm was the last usable one; 26 QBs went in the first 81 picks and the "replacement" evaporated. WR over the same span dropped only 35 — replacement genuinely existed there.

### What pure VORP would have cost

Simulated over the real draft: **pure VORP finishes at 2,077 vs the actual 2,344.** It never takes a QB, because at baseline B Nix prices at 53 and St. Brown at 162. Adding a naive need constraint changes nothing — "fill starters before you run out of picks" defers QBs until the tier is gone.

**Cliff-aware VORP independently selects Nix, Shough and Geno** at roughly the spots we took them, which is a genuine cross-validation of the QB strategy.

### Counterfactual sims are unreliable — say so

A first pass suggested cliff-aware VORP was +300. **It was an artifact:** the sim held every other team's picks constant, so taking St. Brown at 9 left Bijan available at 16 for free. In reality Bills Mafia takes Bijan at 12. The cascade repeated for London, Lamb, Nix, Shough and Jeanty — David got to re-draft his own players a round later, six times.

**Any "what if I'd drafted differently" answer past the first pick is unfalsifiable.** Report the first pick honestly and label everything after it as illustrative.
