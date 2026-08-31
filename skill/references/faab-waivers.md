# FAAB and Waivers — Empty Stadiums

**Verified against ESPN league settings Aug 22, 2026.** Scope: in-season roster acquisition. Companion to `scoring-values.md`, which holds the conversion multipliers every bid decision depends on.

## The rules, as actually configured

| Setting | Value |
|---|---|
| System | **Free Agent Budget (continuous)** — no rolling priority, no waiver order |
| Budget | **$500**, whole season |
| Minimum bid | **$0** |
| Processing | **12:00 AM ET on Mon, Wed, Thu, Fri, Sat, Sun** |
| Tiebreaker | Inverse order of standings, **reset each week** |
| Season acquisition limit | None |
| Roster | 16 total · 11 starters · 5 bench · **2 IR** |
| Lineup lock | **Individually at each player's kickoff** |
| Trade deadline | Dec 2, 2026, 9:00 AM PST · **no review, no veto** |

Two consequences worth internalizing before anything else. There is **no waiver priority to protect** — every claim is a pure auction, so there is never a reason to "save your spot." And the tiebreaker runs **inverse standings**, meaning that once you're winning, you *lose* every tie. Bid odd numbers. $37 beats $35 and ties $37 to a worse team's advantage.

## The processing calendar

There is no Tuesday run. That single gap shapes the week:

| Deadline (ET) | Deadline (PT) | Processes | What it's for |
|---|---|---|---|
| **Sun 11:59 PM** | Sun 8:59 PM | Mon 12 AM | Fastest reaction to Sunday injuries and breakouts. Most of your league is asleep. |
| **Tue 11:59 PM** | Tue 8:59 PM | Wed 12 AM | The main weekly run — first processing after Monday Night Football. Expect competition here. |
| **Wed 11:59 PM** | Wed 8:59 PM | Thu 12 AM | Last call before Thursday Night Football locks players. |
| Thu–Sat 11:59 PM | 8:59 PM | daily | Practice reports, Friday injury designations, Saturday inactives. |

**The Sunday-night run is the biggest structural edge in this league.** A back who takes over a backfield at 4 PM Sunday can be yours before Monday morning, a full two days before the Wednesday run that most managers treat as "waiver day." Set a recurring Sunday 8:30 PM PT reminder — that habit alone is worth more than any bidding formula below.

## What is actually scarce here

An 8-team league with 16-man rosters holds only 128 players. Against NFL supply:

| Position | League absorbs | Of NFL starters | Wire status |
|---|---|---|---|
| **QB** | 24 | 32 | **75% gone — the scarce position** |
| RB | 16 | 32 | 50% — thin at the top, deep below |
| WR | 24 | 96 | 25% — always startable options |
| TE | 8 | 32 | 25% — always startable options |
| **IDP** | 16 | ~128 | **12% — effectively unlimited** |

This inverts standard FAAB advice, which is written for 12-team single-QB leagues where running back is scarce and quarterback is free.

**Here quarterback is the scarcest thing on the wire and IDP is free.** With three starting QB slots across eight teams, roughly 24 of the league's 32 starters are rostered at any moment. When a starting quarterback gets hurt, the replacement who inherits a full NFL job is worth 300+ points in this scoring — and there are only a handful of such jobs available all season. That is the one position where a large bid is defensible.

**Never spend meaningful money on a linebacker.** There are 120+ unrostered defenders with real snap counts. A three-down linebacker projects 330-390 here, and one is nearly always sitting on the wire for a $0-2 bid. If you lose a claim on one, take the next name down and lose almost nothing.

## Bid framework

Budget is $500 across 15 regular-season weeks plus two playoff weeks.

Two separate questions, and collapsing them is the standard mistake.

**Should David want him?** Rest-of-season value over replacement. This is the default lens — not "does he help this week." Weekly marginal value only takes over when there is an actual hole in the starting lineup, and even then see the gap rule below.

**What does he pay?** The **gap to the next-best free player at the same position** — never the raw VORP.

That distinction is not academic. A three-down linebacker in week 3 carries **+114 ROS VORP, identical to a bellcow running back.** Pricing off VORP says bid $150. But the next free linebacker is +110, so the real gap is 4 points and the correct bid is $1. Supply, not production, sets price.

| Player type | ROS VORP (wk 3) | Next best free | **Real gap** |
|---|---|---|---|
| Three-down LB | +114 | another 3-down LB | **4** |
| Bellcow RB, RB1 workload | +108 | committee back | **65** |
| QB inheriting a starting job | +39 | backup QB | **33** |
| WR in a clear WR2 role | +32 | rotational WR | **45** |
| Every-down TE | +28 | streaming TE | **23** |

### The bid scale

Gap is measured in **leverage-weighted** rest-of-season points — see the next section, which is what makes this work late in the year.

| Gap (leveraged ROS pts) | % of budget | On $500 | Typical case |
|---|---|---|---|
| **130+** | 25–40% | $125–200 | Bellcow with nothing comparable free. Once a season. |
| **80–130** | 15–25% | $75–125 | Clear starter, wire falls off hard behind him. |
| **50–80** | 8–15% | $40–75 | Real upgrade. The most common good add. |
| **25–50** | 3–8% | $15–40 | Flex piece, modest edge over the alternative. |
| **8–25** | 1–3% | $5–15 | Take him cheap, shrug if outbid. |
| **under 8** | under 1% | **$0–2** | IDP, returners, QB streamers, WR depth. |

**Position gaps are cheap; scarcity is expensive.** A hole at WR or TE feels urgent but prices low, because the wire is deep right behind whoever you're chasing. A hole at **QB** is the one that can justify real money — 75% of NFL starters are rostered here, and the drop from a starter to a backup is 30+ points. Pay for scarcity, never for need.

**Bid low and often.** Six processing runs a week and only seven competitors means losing a claim costs almost nothing — there's another try tomorrow, usually on a comparable player. The one exception is the top tier, where the asset is genuinely unique and no second chance is coming.

## Week leverage — why a late-season week is worth more

Weeks are not interchangeable. A point in the semifinal decides a season; a point in week 4 is one-fifteenth of a seeding sample. Weight every remaining week by its effect on championship equity, discounted by the odds of actually being there:

| Weeks | Leverage | Why |
|---|---|---|
| 1–9 | **1.00** | Long recovery runway; small effect on seeding |
| 10–13 | **1.35** | Playoff positioning |
| 14–15 | **2.00** | Clinching and seeding |
| **16** | **3.60** | One-and-done × ~72% you're in it |
| **17** | **1.80** | One-and-done × ~36% you get there |

Effective weeks remaining therefore decays far more slowly than the calendar:

| Add in | Raw weeks | Leveraged | Multiplier |
|---|---|---|---|
| wk 2 | 16 | 22.8 | 1.43× |
| wk 8 | 10 | 16.8 | 1.68× |
| wk 12 | 6 | 12.1 | **2.02×** |
| wk 14 | 4 | 9.4 | **2.35×** |
| wk 16 | 2 | 5.4 | **2.70×** |

**Practical effect: late-season bids roughly double relative to what raw weeks-remaining would suggest.** A player worth $20 in week 14 on a linear model is worth $40–50 once leverage is applied. Because the scale is already leverage-weighted, no separate pacing rule is needed — the same player simply prices differently depending on when he surfaces, which is correct.

### Three rules that follow

**A true one-week rental never justifies a real bid.** A player who helps in exactly one week, at +5 points, is worth 5.0 leveraged in week 6, 10.0 in week 15, and 18.0 even in the semifinal — a $15–40 bid at the absolute peak. Late-season weeks being more valuable does *not* mean paying up for one-week matchup plays; it means paying up for players with a **role** that holds through the playoff window.

**Week 17 is worth half of week 16, not more.** You reach the final only about a third of the time, and you must survive the semifinal first. Never pay a premium for a championship-week matchup — pay for week 16.

**FAAB has zero salvage value.** Leftover budget on the final waiver run is money set on fire; there is no week 18. By the week-16 run, the correct bid on anything that genuinely helps is **the entire remaining balance.** Flag it to David around week 13 if he's still sitting on more than ~$100, since that usually means he's been underbidding all year.

**The failure mode in the other direction** is running dry in November, which in an 8-team league almost always means overpaying for players the wire would have handed over for $5. If two-thirds of the budget is gone before week 8, the gap discipline above has slipped.

## Bid on opportunity — the room bids on the box score

This is the waiver version of the ESPN-rank arbitrage that drives the draft playbook, and it is where most of the cheap value lives.

David's leaguemates see **last week's fantasy points** and ESPN's **Top Adds** list. What actually predicts the next month is snap share, route participation, target share, and carries inside the five — none of which appear where they're looking. That gap routinely moves the price by an order of magnitude:

- **A back gets 19 carries for 41 yards.** Ugly box score, invisible to the room, costs $2. This is the one to take — the workload is the signal and the efficiency will regress up.
- **A back gets 5 carries and a garbage-time touchdown.** Trending everywhere, costs $80. Skip him; the role isn't there.

So every recommendation should say which side of that gap the player sits on, because it determines both whether he's worth having and what he'll cost.

## Recommendation format

Same shape as the draft playbook — punchline first, readable in seconds, because waiver deadlines are also a clock.

```
BID: $[amount] on [Player] ([POS], team)

Why: [role/opportunity in one line — snaps, touches, target share, not last
week's points] · [ROS projection in David's scoring]

Why that number: [gap to the next-best free player at the position] ×
[leveraged weeks remaining] → [tier]. [Expected competition.]

If outbid: [next name], at $[amount] — [how much worse he actually is]

Drop: [player], because [reason]
```

Always name the drop. A 16-man roster is full by week 2, and a bid without a corresponding cut is a recommendation David can't act on.

State expected competition explicitly — whether the player is on ESPN's trending list, how many of the seven rivals have a real hole at that position, and roughly what budget they have left. In an 8-team league with six runs a week, the right bid is the **minimum that clears expected competition**, with the tier above serving as the walk-away ceiling rather than the target. And because the tiebreaker runs inverse standings, **always bid an odd number** once David is winning — $37 beats $35 and ties break against him.

## League-specific edges

**Stream the OP slot.** With 2 QB plus OP, your third quarterback slot does not need to be a season-long asset. Because lineups lock individually at kickoff, you can roster a cheap QB with a good matchup, start him, and swap next week. A $0 quarterback with a plus matchup routinely outscores a rostered mid-tier QB in a bad one — 6-point passing touchdowns make the spread between matchups unusually wide.

**Return duty is unpriced by everyone.** Kick and punt return yards score 0.1 and return TDs score **10**. No national ranking includes any of it, and nobody in your league is looking. When a returner job changes hands — and it changes hands constantly after muffed punts and injuries — the new man is worth 50–180 points and costs $0–2. Check return duty every Tuesday. See `scoring-values.md` for the full valuation.

**IDP is free, so never be short — but don't churn it weekly.** Solo tackles score 2.2 and supply is effectively unlimited, so there is no excuse for a mediocre linebacker in a DP slot. **Chase role changes, not matchups:** when a starting linebacker gets hurt and a backup inherits three-down snaps, claim the replacement immediately for $0–2. Snap share is what drives tackle volume and it's stable week to week, so a healthy three-down linebacker should stay in the lineup rather than being rotated on opponent run rate. See `weekly-lineup.md` for the start/sit side of this.

**Trades process instantly.** No review, no veto. The draft plan deliberately accepted bye-week clustering on the logic that talent is tradeable — that only works if you actually work the trade market. Combined with six-day waivers, "I'll fix it later" is a credible plan in this league in a way it isn't in most.

## Roster mechanics

**The two IR slots are real roster space.** A player with a designation ESPN accepts for IR frees a bench spot without a cut. Always park eligible injured players there rather than holding them on the bench — a 16-man roster is tight and those two slots are worth roughly two extra speculative stashes.

**Your five bench spots are lottery tickets, not insurance.** In a shallow league, a "safe veteran who might be needed" is a wasted spot, because the wire holds equivalent players for free. Bench spots should hold: handcuffs to your own high-value backs, players with a real path to a league-winning role, and returners. Nothing else.

**Drop priority when you need a spot** — cut in this order: a healthy IDP (instantly replaceable), a third TE or a TE2, a WR4/5 with no return duty, a backup QB behind a healthy starter. Never cut a handcuff to your own RB1 to make room for a streamer.

## Right after the draft tonight

1. **Check the wire immediately.** In an 8-team league, 128 players are rostered and everyone else is free. Undrafted starting-caliber players will be sitting there — especially quarterbacks, linebackers, and returners, the three groups this room systematically ignores.
2. **Claim two or three linebackers at $0–2** if the draft didn't get you the tier you wanted. Supply is enormous; there is no reason to be short.
3. **Identify every starting NFL returner** who isn't rostered and stash the ones with an offensive role too.
4. **Note which managers left obvious holes** — an empty OP slot or a single quarterback is a trade target for the rest of the season.
5. Save the final roster to this league's data file and grade the draft against the plan in `empty-stadiums.md`.

## Rebuilding these numbers

The scarcity table is derived from roster size, starter counts, and NFL supply — recompute it if the league changes team count or roster size, since both move every conclusion here. The bid tiers are percentages of budget, so they survive a budget change; the dollar figures do not.

## Roster-spot scarcity — the test for any add or stash (Aug 28 2026)

**David's framing, and it is the right one:** *"If there are ample TEs left and relatively little difference, they hold little trade value — and same for me. Why stash if I can just pick someone up off waivers?"*

**A roster spot should hold what you CANNOT get later.** Not the best player available — the one whose availability is most likely to change.

### Measure wire depth before recommending any stash

For the position in question, compute the drop from best available to ~5th available. That number is the true cost of waiting, and it is paid **only for the weeks the starter is actually out** — not across a season.

Empty Stadiums, Aug 28 2026 (8 available at every position):

| Pos | Best | 5th | Drop 1→5 |
|---|---|---|---|
| **TE** | 187 | 170 | **17** |
| WR | 203 | 182 | 21 |
| RB | 200 | 163 | 37 |
| QB | 244 | 108 | 136 |

**TE was the worst possible stash.** Claude had recommended Tucker Kraft (TE6, tightest band on the wire) as insurance for Loveland — David's only tight end. But eight TEs were available within 17 points of each other. Holding a roster spot four months to protect a 17-point gap that can be closed in one waiver claim is a bad trade. David caught this; Claude did not.

### The chart tells you the same thing from the other side

Kraft priced at **4.9 on the Empty Stadiums chart, 81st overall** — because TE replacement is 164, so being TE6 clears the wire by only 20 points. He was worth roughly a WR30-33 or an RB23-24 in trade. **A player who is cheap to replace is also worthless to trade.** Those are the same fact.

### So the rule

**Add for irreplaceability, not for quality.** Rank candidates by:
1. **How fast could this player's value change?** A rookie who becomes a WR2 on one injury will be claimed the week it happens. A backup TE will still be sitting there in November.
2. **Wire depth at his position** — a 17-point drop means wait; a 136-point drop means act.
3. **Points only as a tiebreaker.**

In an 8-team league (128 rostered), the wire *is* the bench. This principle bites hardest there and matters less in 12-team formats where depth actually thins.

### Corollary for in-season

Do not hold "insurance" at a deep position. Hold the spot open, or hold the player nobody else can replace. When the injury happens, claim then — the 17-to-37 point gap for a few weeks is cheaper than a season-long roster spot.


## TX2025 FAAB budgets are UNEQUAL — resolved Aug 30 2026

**$2,500 for managers who went on the New Orleans trip. $2,000 for everyone else.** David is on the $2,500 tier.

This is a real structural edge and it changes bid strategy:

- **David has 25% more budget than the $2,000 managers.** On a contested must-win claim he can outbid them by a margin they cannot match without spending a much larger share of their season.
- **Express every bid as a % of the bidder's own budget, not in dollars.** A $500 bid is 20% of David's season but 25% of a $2,000 manager's. The dollar figure understates what it costs them.
- **Identify which opponents are on which tier before the first contested claim.** The trip roster determines it. Until that's known, assume $2,000 for opponents — it makes David's edge the conservative case rather than an assumed one.
- Prior notes said $2,500 flat and the FantasyPros sync reported $3,000. **Both were wrong.** FantasyPros exposes no per-team FAAB, so this can only come from CBS or from David directly.
