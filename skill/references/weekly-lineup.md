# Weekly Lineup — Empty Stadiums

Start/sit for an 8-team superflex with 2 IDP, no kicker, no defense. Companion to `scoring-values.md`, which holds the conversion multipliers every projection here depends on.

**Starting eleven:** 2 QB · 2 RB · 3 WR · 1 TE · **1 OP** · 2 DP. Bench 5, IR 2.

## The core rule: start the higher projection

Weekly variance is close to irrelevant to a start/sit decision, and this is worth stating loudly because it contradicts the intuition that a 30-then-5 player is hard to start.

A team in this league scores roughly **248 points a week with a standard deviation near 34**. One player's variance adds to that *in quadrature*, not linearly. A boom/bust starter carrying 9 extra points of weekly SD moves team SD from 34.0 to 35.2 — a 3% change in spread, against a projection loss you take in full.

Simulated over 200,000 weeks:

| Your matchup | Start the safe player | Start the boom/bust player | Edge |
|---|---|---|---|
| Big favorite (−40) | 79.7% | 78.2% | **−1.5%** |
| Favored (−20) | 65.9% | 64.5% | −1.4% |
| Even | 50.0% | 48.5% | −1.5% |
| Underdog (+20) | 33.8% | 32.6% | −1.3% |
| Big underdog (+40) | 20.3% | 19.5% | −0.7% |

**The high-variance player loses in every scenario, including as a heavy underdog.** How much projection you may give up for variance, by matchup:

| Situation | Max projection you can sacrifice |
|---|---|
| Favored by 30 | **−0.7 pts** (i.e. never) |
| Even | 0.0 pts |
| Underdog by 15 | 0.2 pts |
| Underdog by 30 | 0.4 pts |

Even a genuinely wild player (+25 points of SD) only earns a 3.9-point projection discount when David is a 30-point underdog, and +40 SD earns 8.0.

**So: start the higher projection. Full stop.** Not "usually" — the exceptions are too rare and too small to carry in your head.

### Where variance actually does matter

Only in a near-hopeless week. As a 50-point underdog a high-variance lineup gains **+1.4%**; at 70 points down, **+1.8%**. Real but tiny, and only worth invoking when David is mathematically desperate — an elimination game he's projected to lose badly. Flag it then and not before.

### How this squares with the draft-day variance rule

These are different decisions and both rules are right.

**At the draft**, low variance on starters is correct — not because of win probability, but because a boom/bust player degrades every *future* decision. He gets benched in his big weeks and started in his bad ones, and he makes trade and waiver evaluation noisier. That's a decision-quality cost, and it's real.

**At lineup time** the player is already owned and the only question is which name goes in the slot. There, the projection is the whole answer.

## Where the weekly decisions actually are

With three QB slots and a 16-man roster, most weeks the lineup writes itself. Two slots carry real choices.

**The OP slot — which three of four quarterbacks.** This is the highest-leverage weekly call in the league. Six-point passing touchdowns widen the spread between a good and bad matchup more than any other position, and David's QBs will be clustered (roughly 424 / 400 / 385 / 370 by projection), so a matchup swing genuinely can reorder them. This is the one slot where a matchup adjustment should be allowed to override a small projection edge — and the only one.

**The two DP slots.** Solo tackles score 2.2, so a three-down linebacker is worth more than any tight end on the roster. Snap share is what drives tackle volume, and it is fairly stable week to week — **which means "start your highest-snap-share linebacker" is right most weeks.**

Matchup is a tiebreaker between linebackers with similar roles, never a reason to bench a three-down player for a situational one. Churn the DP slots when a **role** opens up somewhere — see `faab-waivers.md` — not on a weekly matchup read.

## Lineup locks individually — use the option value

Players lock at their own kickoff, not at a weekly deadline. That makes lineup slots an **option**, and options have value.

**Prefer the later game when two players are close.** Starting a Thursday player forfeits three days of information — inactives, weather, a Saturday trade, a Sunday-morning scratch. If two players are within a couple of points, start the one who plays later. The projection edge has to be real to justify locking early.

**Never fill a slot Thursday out of tidiness.** There is no benefit to setting the lineup early and a real cost to it.

**Check inactives at 8:30 AM PT Sunday.** That's 90 minutes before the first kickoff and the last clean window to react to a surprise scratch.

**Monday night is a free roll.** If a slot's Sunday options have all played, whatever is left for Monday costs nothing to start.

## Bye weeks

The draft plan deliberately accepted bye clustering on the logic that talent is tradeable and the wire is live six nights a week. Byes fall in weeks 5–14 and **cannot touch the playoffs** under the weeks 16–17 format.

Three starters out in a week is manageable — cover it from the bench and the wire. At four or more, act early: post a trade two weeks ahead rather than scrambling on Saturday, since there's no trade review and deals process instantly.

The QB room is bye-proof by construction. Four quarterbacks for three slots means one bye is absorbed automatically.

## Projections to use

Same method as the draft: pull **FantasyPros weekly stat projections** and re-score them under this league's rules using the multipliers in `scoring-values.md`. Do not use ESPN's or FantasyPros' displayed fantasy points — both are computed under different scoring and will misrank quarterbacks, returners, and defenders specifically.

Two things national projections omit entirely and must be added by hand:

- **Return yards at 0.1 and return TDs at 10.** A full-time returner adds 3–12 points a week that no weekly projection includes. Verify return duty is current — it changes after a muffed punt.
- **IDP scoring at 2.2 per solo tackle.** Most weekly projection sets either omit defenders or score them under a generic system.

## Recommendation format

```
LINEUP: [slot] — start [Player] over [Player]

Why: [projection in David's scoring, both players] — [gap]

Watch: [the one thing that would change it — inactive report, weather,
a snap-count trend] and by when

Close calls this week: [any slot inside 2 pts, flagged so he can decide]
```

Lead with the slots that are genuinely close. If the lineup is obvious, say so in one line rather than walking through eleven slots — most weeks it is obvious, and pretending otherwise wastes his time.

## Rebuilding these numbers

The variance simulation assumes a team mean near 248 and SD near 34, derived from the draft-day roster model. If actual scoring diverges materially once real games are played, re-run it — but the qualitative conclusion is robust, since it follows from variance adding in quadrature rather than from the specific values.
