# Live Draft Playbook

Built for Empty Stadiums (ESPN, 8-team PPR, pick 2, Aug 22 2026) and reusable for TX2025 (CBS, 2QB, Aug 29 2026) by swapping in that league's strategy and inverting the QB guardrail.

**Read `draft-postmortem-2026.md` first.** The Aug 2026 draft produced six execution failures; the hard rules below came from them and are non-negotiable.

## HARD RULES (learned Aug 22 2026, at real cost)

1. **Gap first, always.** Every recommendation leads with the gap to the next survivor at that position. Deviating from the plan requires a gap ≥ 30 at the position taken. A big raw projection is never a reason — that error cost 40 points (Burrow over Lamb: QB gap was +3, WR gap was +50).
2. **Projections come ONLY from the pre-built board.** The live tab is read for who is gone — never for numbers. A player missing from the pre-built board is announced as "NOT ON MY BOARD" with his 2025 finish stated before any recommendation. Rank and projection must agree within ~40 spots; a rank-200 player with a top-30 projection is a parse bug, not an edge (the Malik Washington error, ~−80 pts).
3. **Check the activity feed, not a cached list, before naming anyone.** The last-10-picks log is the only fresh data on the page. Recommending an already-drafted player happened twice (Goff, C. Williams).
4. **Re-read the roster panel before every recommendation from round 6 on.** State open starting slots aloud ("Open: OP, DP, DP"). Never from memory — memory said 3 QBs when the roster had 2.
5. **One line per pick:** `PICK: Name (proj, 2025 finish) | gap +X | backup: Name`. Analysis between turns only. If verification can't finish in ~30 seconds, answer from the pre-built board and verify after.
6. **Restate ambiguous questions in six words before answering.** Answering the wrong question wastes a turn.
7. **Untested overrides don't exist.** Any "take X if he falls" exception must be gap-tested or sim-tested before the draft, or it's dropped.

David runs the draft in his league's tab; this session runs alongside holding the board. As players come off the board they get crossed off, so there is always an answer ready for **"who do I take and why?"**

## Tracking picks

**Mode A — Claude in Chrome (preferred).** David has the draft room open with Claude in Chrome connected. On each request, read the tab: pick list, players already drafted, whose turn it is, and David's current roster. No typing from him.

**Mode B — manual paste (fallback).** He types `gone: Jefferson, Bowers, Jacobs`. Cross them off and answer. Keep it forgiving — last names are enough, resolve ambiguity without asking unless two plausible players genuinely share a name.

Confirm which mode is live during setup, and switch to B without ceremony if reading the tab fails mid-draft. Losing thirty seconds to a debugging session during a pick is the worst outcome available.

## Pre-draft setup (~30 min before)

1. **Pull FantasyPros data** using `FP_API_KEY` from `.env` — season-long PPR projections (top 150+), ECR overall and positional, analyst tiers by position, and ADP.
2. **Confirm actual league settings** from the draft room tab: roster positions, starter counts, bench size, whether K/DEF are required, scoring. Report anything that differs from the strategy doc's assumptions and what it changes. This step is not a formality — starter counts set replacement level, which sets every VORP number downstream.
3. **Re-adjust ADP for league size.** FantasyPros ADP assumes 10–12 teams. In an 8-team room, fewer starters means replacement level rises, QBs and TEs slide, and elite players gain. Flag the players whose adjusted value diverges most from raw ADP, in plain terms: "Allen's ADP 19 is a 12-team price; in this room he can last to round 4–5."
4. **Compute VORP** for everyone: projection minus replacement-level projection at that position. For 8 teams with a flex: QB8, TE8, RB~18, WR~18 (the flex spreads RB/WR replacement deeper). Adjust to the settings actually confirmed in step 2. `scripts/build_board.py` does this — use it rather than recomputing by hand.
5. **Build one working board** and keep it as the single source of truth:
   ```
   [ECR] Player (POS, Team, Bye) — tier — proj — VORP — adj ADP — note
   ```
6. **Confirm pick slots** and show David the top 25 plus the planned pair for his first turn, so he can sanity-check before the clock starts.

## Decision logic by phase

The right basis for a pick changes as the draft progresses, because what's scarce changes.

**Early (Empty Stadiums picks 2 and 15): strategy guardrails rule.** The pre-draft plan was made with hours of research and a full board; a VORP number computed under time pressure shouldn't override it. **Elite QB at 1.02, QB2 plus best skill at the 15/18 turn** — see `empty-stadiums.md`. The one override is a genuine faller from the top of the board.

**Middle (picks 18 through ~63): VORP rules.** Recommend the highest-VORP player who fits roster construction, and cite the math every time — "McBride projects 208, TE8 projects 146 → +62 VORP, biggest edge on the board." Use tier breaks to time positions: taking the last player in a tier captures value that evaporates one pick later.

**Late (pick 66 on, roster largely full): ECR upside rules.** VORP starts favoring safe floors exactly when floors stop mattering, because bench spots in a shallow league are lottery tickets. Switch to ceiling: players whose ECR sits well ahead of where they're going, ambiguous backfields, injury-discounted stars, rookies with a path to volume. VORP becomes a tiebreaker only.

## Risk posture by phase

David wants **floor early, ceiling late**, and the recommendation format should make that explicit rather than leaving it implied.

On starters (roughly rounds 1–7), name the bust risk out loud when it exists and say why you're accepting or avoiding it — age cliffs at running back, first year back from a major lower-body injury, efficiency-dependent profiles, and pass-catchers who just lost target share are the four archetypes to flag. On the bench (rounds 10+), do the reverse: lead with the ceiling and treat a high bust rate as the price of admission. A bench player with a 20% shot at a league-winning role beats a safe veteran who will never crack the lineup.

The trap to avoid in the middle rounds is drifting: taking floor plays at pick 90 out of habit when the starting lineup is already full. Once every starting slot has a name, every remaining pick should be a swing.

**Strength of schedule is a tiebreaker only.** It's among the least predictive inputs available, built on last season's defensive numbers. It separates comparable players; it never moves someone up a tier. Weight it to **weeks 16–17**, the Empty Stadiums playoff window.

## Response format

When David asks who to take, answer in this shape — punchline first, readable in under five seconds:

```
PICK: [Player] (POS, Team)

Why: [1-2 sentences with the number — projected points in David's scoring,
and the value over replacement]

Why now and not later: [the timing case — where ESPN ranks him vs the safety
line for this turn. "ESPN has him 9th; 12 picks until your next, so he's gone."
Or: "ESPN has him 31st — he survives, take X first."]

Backup if sniped: [Player 2], then [Player 3]

Next pick (N): expect [names] to survive — leaning [position]
```

The backup pair isn't optional. Turns come fast, snipes happen between the question and his click, and a recommendation with no fallback forces him to think on his own clock.

## Standing rules during the draft

- **Track his roster.** By round 6, recommendations must reflect what he actually has, not abstract best-available.
- **Flag tier breaks before they happen**, not after: "last back in this tier — after him the position drops 40 points." Note that the tight end cliff, which earlier runs treated as urgent, is no longer worth reaching for after the Aug 2026 scoring change.
- **Call position runs.** Three or more of one position going consecutively means a decision. In Empty Stadiums specifically, expect a QB run in round 1 and a defensive run starting around pick 79 — neither is a surprise, so plan for them rather than reacting.
- **Byes barely matter — draft talent.** Up to three starters on a week, ignore them completely. Only at 3→4 does a ~5-spot tiebreaker apply, and at 4→5 a ~15-spot one. Early clusters (weeks 5–9) are the dangerous ones because there's no waiver or trade market yet; late clusters (11–14) relax one step, since they're fixable by trade. No bye can touch the playoffs under the weeks 16–17 format. Full rule in `empty-stadiums.md`.
- **Stay quiet between picks.** Keep the board current silently; only interrupt when a tier break or run genuinely changes the plan. Chatter during someone else's pick is noise on a clock.

## ★ The core mechanic: model opponents on THEIR board, decide on YOURS

This is the most valuable technique in the skill and it should drive every recommendation.

**Opponents and David use different information.** In Empty Stadiums the room drafts off **ESPN rankings** — it's an ESPN league and that's the board in front of them. David decides off FantasyPros plus the custom scoring conversion, which is strictly richer. That asymmetry is not a tiebreaker; it's a scheduling tool.

**Use the opponents' board to answer "when," not "who."**

- To predict what disappears before David's next pick, read down the **ESPN rank** column of available players.
- To decide which player he actually wants, read **projected points in his scoring**.
- The gap between those two answers tells you what to take now and what to leave.

### The waiting rule

Count the opponent picks between David's current pick and his next one. That number is the **safety line**: the top *N* available players by ESPN rank will be gone; anyone ESPN ranks deeper than *N* among available players survives.

**Empty Stadiums gaps alternate 12 and 2 all draft long:**

| David's pick | Opponents before his next | Safety line |
|---|---|---|
| 2, 18, 34, 50, 66, 82, 98, 114 | **12** | ESPN top 12 available are gone; #13+ survives |
| 15, 31, 47, 63, 79, 95, 111 | **2** | ESPN top 2 available are gone; #3+ survives |

**What this means in practice:**

- **At a 2-gap pick (15, 31, 47, 63, 79, 95, 111): take the player ESPN ranks highest among your targets.** He's the only one at risk. Everything else on your list will still be there three picks later — this is close to a free look.
- **At a 12-gap pick (18, 34, 50, 66, 82, 98, 114): take the best player who sits inside ESPN's top 12 available.** Anyone ESPN ranks 13th or deeper among available survives the turn, so taking him here wastes the pick.

### Where ESPN is systematically wrong (2026)

Measured against ESPN's *own* projections in Empty Stadiums scoring:

| Position | Average ESPN error |
|---|---|
| **QB** | **+9.5 spots too low** |
| RB | −3.1 too high |
| TE | −6.0 too high |
| WR | −6.6 too high |

Biggest individual gaps — **buy late:** Purdy (ESPN 33 / true 7), Dak (26/8), Nix (27/9), Lawrence (25/10), Burrow (16/4), Maye (10/2), Dart (17/11). **Will cost a premium:** McBride (21/32), Bijan (5/14), Chase (6/15), Smith-Njigba (8/17), Gibbs (4/12), London (20/28).

The practical consequence: **quarterbacks can be waited on a full round or more beyond where their value says**, while elite RB/WR/TE must be taken at or before their ESPN rank. Don't avoid the fade names — just don't spend an early pick on one when the board will hand you a 420-point quarterback two rounds later.

### TX2025 (CBS, Aug 29 2026)

Same mechanic, different opponent model. That room's sources vary but lean on **CBS rankings**, so CBS becomes the "when" input there. The CBS-vs-value gap table hasn't been built yet — do it before Aug 29, the same way this one was built.

## Reading the pick predictor

FantasyPros shows a percentage per player: the chance he's gone before David's *next* pick. It's the most useful number on the screen at a turn, because it converts "who's better" into "who won't be here."

The rule that follows: **when two players are close in value, take the one more likely to disappear.** Note that "close in value" means close in *this league's* scoring, not close in ECR — and after the Aug 2026 change, at genuinely equal value **the running back wins over the receiver**, and tight end is no longer worth reaching for.

Two cautions. The predictor moves fast — a receiver at 23% jumped to 88% after one WR came off the board two picks earlier, so re-read it at the turn rather than trusting a number from ten picks ago. And it reads **N/A for defensive players**, which does not mean they're safe; the sim just doesn't model IDP demand, while the real league needs sixteen IDP starters.

## After the draft

Save the final roster to the league's data file, grade the draft against the strategy (what went to plan, best value, biggest reach), list week-1 waiver targets from undrafted players, and note learnings for the next draft.
