# Trade Value Model — Empty Stadiums

A trade value algorithm built for this league specifically, and the reasoning behind it. Implemented in `scripts/trade_value.py`. Companion to `trades.md` (the tactics), `scoring-values.md` (the multipliers) and `faab-waivers.md` (which sets replacement cost).

## What the existing charts do, and what they get wrong

Three approaches dominate, and each fails differently for David's use case.

| Chart | Method | Problem here |
|---|---|---|
| **KeepTradeCut** | Crowdsourced from millions of community votes | Pure market sentiment — measures *perception*, not value. Dynasty-only. Its verdicts matched community judgment on only **58%** of trades where it named a winner. |
| **FantasyCalc** | Algorithmic, from hundreds of thousands of real trades | 84% accurate when it names a winner, but calls a decided trade "even" more than half the time. Dynasty-only. |
| **Stats Guy** | Real trades, with the package premium built into the value curve | Closest methodology, but still dynasty and still generic scoring. |
| **Draft Sharks / FantasyPros redraft** | Rest-of-season projections through a cross-positional algorithm | Right shape for redraft, but blind to superflex-with-OP, 2.2-per-solo-tackle IDP, and return yards. |

**Three findings from that research are worth stealing.**

**The package premium must live in the value curve, not in a verdict-time correction.** When each system's raw values were graded as plain sums, KeepTradeCut scored 42% and FantasyCalc 60%, against 85% for the system that shapes the curve itself. A correction bolted on at verdict time can only nudge a total; it never reaches the values you browse.

**Experienced managers demand the package side beat the star's paper value by 15–40%** before calling a deal fair. That's measured against hundreds of community-judged trades, and it means any additive chart systematically overprices piles of depth.

**Observed trades understate elite players.** For every star who gets traded, many more stay put because their manager declined every offer. Those declines are real market information and they never appear in trade data. The right anchor is *hold value* — what the player is worth to the roster that has him — not *clearing price*.

## The core metric

Everything reduces to one question: **how many starting-lineup points does David lose if this player is gone and he refills the slot from the wire?**

```
V(player) = LINEUP(roster) − LINEUP(roster − player + best free agent at that position)
```

Then leverage-weighted for the point in the season (see `faab-waivers.md`):

```
V_ros = V_per_week × Σ leverage(w) for w in remaining weeks
        leverage: wks 1–9 = 1.00 · 10–13 = 1.35 · 14–15 = 2.00 · wk16 = 3.60 · wk17 = 1.80
```

**Why this is the right metric rather than VORP or projected points.** It produces the correct answer for three cases that break every generic chart:

- **IDP collapses to near zero automatically.** Cashman projects 392 — the second-highest number on the roster — and is worth **37**, because Bolton slides up from the bench. No special-case rule required; the wire's depth does the work.
- **Bench players compute to exactly zero.** All five tested at +0. That *is* the consolidation premium, embedded in the curve exactly as the research says it should be.
- **Scarcity beats production.** Kraft projects 189, the lowest starter on the roster, and is worth **34** — nearly as much as Cashman at 392 — because tight end has no cheap replacement.

Validation against the 15–40% premium finding: no two-player package on this roster clears Gibbs at 191. McConkey + Judkins reaches 108, Herbert + Goff 151, Jefferson + Judkins 164. The premium emerges from the structure rather than being applied on top.

## Rule: never sum per-player values

This is where the model departs from every commercial chart, and it matters.

**Player values are path-dependent.** Cashman is worth 37 *because Bolton is on the bench behind him*. Trade Bolton and Warner away and Cashman's value jumps to 179 — the same player, nearly five times the price, because the fallback disappeared. Give up all four linebackers at once and the package costs 353, against 69 if you sum them individually.

**So every trade is evaluated as a single before-and-after lineup comparison**, with all pieces applied simultaneously and every vacated slot refilled from the wire. Never as a sum of individually-computed values. Additive charts cannot represent this and it is a large part of why they misprice packages.

## The second number: perceived value

True value tells David what a player is worth. It does not tell him what his leaguemates will pay. Those are different quantities and **the gap between them is the entire profit**.

Model perceived value by projecting rest-of-season production the way the room does it — from what's visible on the ESPN page — rather than the way the truth does it.

**What the market weights** (recency-heavy, and it shifts as the season goes):

| | Preseason rank | Last 3 games | Season to date |
|---|---|---|---|
| Weeks 1–3 | 0.60 | 0.30 | 0.10 |
| Weeks 4–7 | 0.30 | 0.50 | 0.20 |
| Weeks 8+ | 0.10 | 0.55 | 0.35 |

**What the truth weights** (no weight on a three-game sample at all):

| | Preseason projection | Season to date (opportunity-adjusted) |
|---|---|---|
| Weeks 1–3 | 0.80 | 0.20 |
| Weeks 4–7 | 0.55 | 0.45 |
| Weeks 8+ | 0.30 | 0.70 |

Run both projections through the same replaceability formula. **Arbitrage = V_true − V_perceived.** Buy where it's strongly positive, sell where strongly negative.

### The four hype adjustments, in order of size

**Touchdown luck — the largest and most reliable.** Touchdowns are the most visible statistic and among the least predictive, and this league pays 6 per touchdown. A player scoring well above his opportunity-implied rate is the single best sell candidate available; one scoring below it is the best buy. Compare actual TDs to expected TDs from red-zone touches and yardage, and treat the gap as pure noise the market has priced as signal.

**Recency overreaction.** The documented case: Devin Duvernay was the WR8 in week 1 and finished WR53. Weeks 2 and 3 are the highest-value buy-low window of the season, because three games of data feel like a trend and are statistically almost nothing.

**Injury overreaction.** The market drops an injured player sharply and re-prices him slowly on return. Buy during the absence of a player with a secure role, not after he returns and reminds everybody he exists.

**Draft-cost anchoring.** Managers overvalue players they spent an early pick on and undervalue their own late-round hits. This is sticky and asymmetric — it makes their early picks *expensive to buy* and their late-round producers *cheap to buy*. In this league, David can read every manager's draft cost directly off the recap page.

### The ESPN-rank overlay, and its expiry

Before real games exist, preseason ranking *is* the market's entire anchor, and ESPN's is systematically wrong: quarterbacks under-ranked by 9.5 spots on average, RB/WR/TE over-ranked. That's the arbitrage from `live-draft-playbook.md`, and it applies to trades unchanged — **for about five weeks.** Once six games of scoring exist, the anchor weight drops to 0.10 and real production takes over. Front-load buy-side trades accordingly.

## Output format

Every valuation reports both numbers and the gap:

```
[Player]   TRUE 124   MARKET 78   → BUY, +46

Why they're low: [the specific visible signal — 2 TDs in 5 games, a quiet
3-game stretch, drafted in round 9]
Why we're not: [the opportunity evidence — snap share, targets, red-zone work]
```

For a full offer, always the before-and-after:

```
VERDICT: accept / decline / counter
Lineup now: [X]  →  after: [Y]   net [+/− Z]
The piece that decides it: [usually an IDP or a bench body priced as if it mattered]
Counter: [names, and what it clears by]
```

## Calibration and honest limits

**Recompute after every roster change.** Values are contingent on the roster and shift whenever it does.

**Reset replacement levels at the real rostered depth** once the draft finishes — currently estimated at QB 24, RB 26, WR 34, TE 12, IDP 20 out of 128 total roster spots.

**The weights above are reasoned, not fitted.** The recency-versus-truth split follows from sample-size logic and the documented direction of recency bias, but the specific numbers have not been validated against this league's actual trade history. Treat the *direction* as reliable and the *magnitudes* as a first draft. After a season of real trades, refit them.

**Known blind spots**, shared with every commercial chart: breaking news the market hasn't priced, roster context (whether a rebuilder should be buying at all), and any player whose role changes for reasons no projection captured. On those, David's read beats the model — the model's job is to make the comparison explicit, not to make the decision.

## Sources

- [Comparing trade calculators — Stats Guy Fantasy](https://statsguyfantasy.com/methodology/comparing-trade-calculators)
- [Packages, 1-for-1s, and the Value Curve — Stats Guy Fantasy](https://statsguyfantasy.com/methodology/packages-and-the-value-curve)
- [The Impact of Recency Bias in Dynasty Fantasy Football — FantasyPros](https://www.fantasypros.com/2023/03/impact-recency-bias-dynasty-fantasy-football/)
- [Behavioral biases in the NFL gambling market: Overreaction to news and the recency bias — ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S2214635021000666)
- [Fantasy Football Trade Value Chart — FantasyCalc](https://fantasycalc.com/trade-value-chart)
- [Dynasty Football Trade Calculator — KeepTradeCut](https://keeptradecut.com/trade-calculator)
- [Fantasy Football Trade Value Chart 2026 — Draft Sharks](https://www.draftsharks.com/trade-value-chart)


## Evaluating a trade — the method, learned the hard way (Aug 26 2026)

A four-hour trade negotiation in Empty Stadiums produced these. Apply all of them; each one caught an error the others missed.

### 1. Never quote a chart value as the verdict

The chart prices a player against the **wire**. David's lineup prices him against **whoever he actually replaces**. Those are different numbers and the gap can flip the sign.

> James Cook III is RB7, 17th overall, chart 39.7. DeVonta Smith is WR16, 35th, chart 24.2. FantasyPros agreed Cook was the clear win. **But the trade cost David 12 points**, because the chart valued Cook against a 195-pt wire RB while David's actual RB2 was Hampton at 266. That 71-pt gap was the whole story.

**Always run the before/after optimal lineup. Report the chart number only as context, never as the answer.**

### 2. Decompose the delta by slot, every time

A net number hides what is actually happening. Break it out:

> Pappy deal = **+19**. Decomposed: SFLX **+23** (Mayfield over Stroud), WR **+26** (Olave in, board shifts, DeVonta falls out), RB2 **−31** (Hampton → Irving). David spotted this himself — "the upgrade comes from QB" — before Claude showed it.

### 3. Points are not the whole trade — check the spread

Pull `rank_ecr`, `rank_min`, `rank_max`, `rank_std` for **every player on both sides**, including the bench player who backfills. A projection gain can be a certainty loss.

> Hampton: **RB9, band RB4-13, σ 2.15** — the tightest non-elite player in the deal. His replacement Irving: **RB21, band RB14-29**. Twelve ranks down and a bear case near replacement. Meanwhile Olave (WR10, bull WR7, bear WR22) and DeVonta (WR13, bull WR7, bear WR23) have **almost identical distributions** — so a chunk of the "+26 at WR" is inside expert disagreement.

**A +19 trade that swaps a tight band for a wide one is not a +19 trade.**

### 4. Bench players are worth ~0 to a lineup — on both sides

This kills most "sweeteners" and most 2-for-1s.

> David proposed Hampton + Evans for a stud WR. **Evans changed nothing** — he was bench for David and would be WR8 for a room already 7 deep. Adding him only signalled David thought it mattered.

**Corollary:** a player becomes tradeable the moment another acquisition benches him. DeVonta was a starter worth −11 to move; after Olave arrived he was bench and worth **+58**.

### 5. Sequence changes which chip to send, and by how much

Same endpoint, different risk.

> Cook for **Evans** (bench) = **+27** standalone. Cook for **DeVonta** (starter) = **−11** standalone, **+77** only if the second trade also lands. Order the deals so each one stands alone if the other falls through.

### 6. Superflex kills positional scarcity arguments

Check what actually occupies the flex before claiming a positional need.

> Dan "needed a running back." His SFLX was **Baker Mayfield, a QB, at 377** — so an RB at 266 could not crack his lineup at all. His real gain was only at RB2 over Judkins (+37). Claude nearly built a whole pitch on a need that did not exist.

### 7. Scan every partner before negotiating with the one who asked

> Dan asked. Dan was the **worst** partner available. "I am Warren out with the injuries" carried four RBs and needed WRs — the mirror image of David — and produced +58/+51 deals. Run the full 7-team scan first.

### 8. Rank candidate deals by `min(your gain, their gain)`, not by your gain

Sorting by David's gain surfaces deals nobody signs. The deals that close are the ones where the worse-off side still gains.
