# Calibrating the FantasyPros Mock Draft Simulator

The simulator drafts off FantasyPros superflex ECR, which is **more quarterback-hungry than Empty Stadiums actually is**. Left at defaults it hands you elite running backs at pick 15 that your league takes at 7 and 10. Every conclusion drawn from an uncalibrated run is wrong in the same direction: it makes QB-first look free.

Calibrate before trusting a run, and verify behaviorally rather than by reading numbers off the board.

## Setup

Start from **Draft Simulator → Start a Mock Draft**, and load settings from the **Empty Stadiums** league — this pulls the custom scoring (6-pt pass TD, full PPR, IDP) that drives everything. Do not unlink the league to unlock the dials; losing the scoring distorts more than the dials fix.

| Setting | Value |
|---|---|
| Teams / type / position | 8, snake, 2nd |
| Roster | QB 2, RB 2, WR 3, TE 1, Flex 0, K 0, DST 0, Bench 5 |
| Behind **Show More Positions** | **SuperFlex 1, IDP 2** |
| Draft Against | All Experts |
| Upside Mode | **Off** |
| Draft Intel | **On** (per-team patterns from league history — better than the global dials) |

**Position Values:** QB **Slightly Low** · RB **High** · WR **High** · TE **Slightly Low** · rest Normal.

**QB was lowered from Normal to Slightly Low on Aug 21** at David's read. Normal produced 11–13 quarterbacks in the first 14–16 picks; his actual 2025 draft took 7 in the first 14 and 8 in the first 16. He knows his leaguemates and says they don't chase the position this hard even with 6-point passing TDs. **Target: 8–10 QBs in the first 16 picks.**

This matters more than a calibration detail. If quarterbacks really do last longer than the sim assumes, the whole "elite QB at 1.02" conclusion is worth re-testing — because a room that lets QBs slide is a room where David could take an elite back at 2 *and* still get a quality quarterback at 15 or 18. Watch that specifically in the next run.

**History of this dial:** Slightly High was tried in run 5 and overshot badly — 13 QBs in the first 16 and 22 by pick 31, with CPU teams filling three QB slots before touching a skill position. Normal was better but still ran hot at 11–13. Slightly Low is the current setting.

RB is the dial that's actually verified: setting it High moved Gibbs to pick 5 and Bijan to 12, matching the 2025 draft where they went 10th and 7th. Leave it there.

**The counter-argument, recorded honestly:** 2025 was played with 4-point passing TDs and 2026 has 6, so a *rational* room should draft quarterbacks earlier this year, not later — and this room reacted fast to superflex when it arrived. That argues the sim isn't wrong. David's counter is that he knows these managers and they won't. His read on his own league wins, but if the first 16 picks come back QB-heavy anyway, that's the sim being right rather than miscalibrated.

## Verification — behavioral only

**Do not use the "Overall" or "ADP" numbers on player cards to check calibration.** Those come from the Default Cheat Sheet (Latest FantasyPros ECR) and don't move when Position Values change. Gibbs will read "Overall 26" whether the dials are set or not. This wasted a full round of testing.

Instead, let it run and count the first 16 picks:

| Metric | 2025 actual | 2026 expectation |
|---|---|---|
| QB | 8 | **8–10** (David's read; see the dial note above) |
| RB | 4 | 4 |
| WR | 4 | 3–4 |
| Bijan gone by | pick 7 | pick 7–12 |
| Gibbs gone by | pick 10 | pick 5–10 |

The RB and skill targets carry over directly from 2025.

If elite RBs are still on the board at 15, the dials aren't biting and the run is worthless for strategy questions.

**Known limitation:** Position Values are greyed out when a league is synced. Editing them means going through the FantasyPros league settings page, which changes David's stored league config — ask before doing that.

## Do not chase the FantasyPros grade

**The letter grade measures conformity to consensus rankings, not roster quality.** It therefore penalizes exactly the adjustments this skill exists to make — custom scoring conversion, bye discipline, return-yard valuation. None of those are visible to a grader built on national ECR.

Evidence from Aug 20: the run that ignored byes entirely graded **A / 95**. The run that followed David's stated rules graded **B / 83** — and was the better roster by his preferences.

**Judge a draft on:** the Draft Analyzer's **projected standings** (which score the actual lineup rather than obedience to rankings), the bye grid, and whether the scoring-conversion logic in `scoring-values.md` was applied. **Expect a good draft here to grade B. Be suspicious of an A** — it likely means consensus was followed where this league rewards deviation.

Never adjust a pick to improve the grade.

## Run log (Aug 20, 2026)

| Run | Pick 1.02 | Calibration | Grade | QB room |
|---|---|---|---|---|
| 2 | Gibbs | tilted — RBs survived past 15 | C− / 72 | Purdy, Darnold, D. Jones |
| 3 | Maye | tilted — RBs survived past 15 | B / 86 | Maye, Stroud, Ward |
| 4 | Maye | **RB calibrated** (Gibbs 1.05, Bijan 2.04) | **A / 95** | Maye, Lawrence, Ward |
| 5 | Maye | QB Slightly High — **overshot**, 13 QB in first 16 | not finished | Maye, Purdy, Ward |
| 6 | Maye | calibrated | B / 83 | Maye, Lawrence, Ward |
| 7 | Maye | calibrated, full rule set | **B− / 81, David approved** | Maye, Goff, Ward |

**Run 7 is the reference draft.** First run with the complete rule set — scoring buckets, loosened bye thresholds, availability-vs-production risk, return-yard valuation. Result: Maye / Goff · Bijan / Hampton · St. Brown / Jefferson / Waddle · Bowers · Ward (OP) · Schwesinger / Roquan, with Turpin (ECR 360) and Mims (ECR 278) stashed for return production.

David reviewed it and approved everything except the OP quarterback.

**The one repeated failure across runs 6 and 7: the OP slot.** Both times the quarterback pool was picked clean by pick 63 and the slot got a ~10-PPG rookie. The fix is now in `empty-stadiums.md` — commit to the OP decision at picks 47–50 rather than drifting into the 60s.

Run 5 is still worth reading for the skill positions even though the QB dial was wrong. With the room spending 22 of its first 31 picks on quarterbacks, the receiver board at pick 31 still held Smith-Njigba (30), St. Brown (31), Lamb (38) and Jefferson (39) — only Chase had gone. Directionally that's real: **the more this league chases quarterbacks, the later elite receivers last.** The magnitude in run 5 is inflated, but the shape of the opportunity isn't.

Run 4's starting lineup: Maye / Lawrence · Cook / Chase Brown · Nacua / Lamb / McConkey · Bowers · Ward (OP) · Campbell / Roquan (IDP).

**How much to trust run 4:** the RB dial calibrated but QB still ran hot — 11 quarterbacks in the first 14 picks against the league's 8. That over-drafting is why Nacua fell to 18, Lamb to 31, Bowers to 50, and McConkey to 63. Expect meaningfully less skill-player value in the 31–63 range on a real board.

**What the runs actually established**, at different confidence levels:

- **High confidence:** the elite RB tier is gone by pick 13 in this league. Any plan that assumes Gibbs or Bijan reaching pick 15 is built on a simulator artifact.
- **High confidence:** the QB tier collapses fast — 12 to 13 QBs gone by pick 18 in every run. If you want a top-8 quarterback you take him in the first two rounds.
- **Reasonably strong:** taking the elite QB at 1.02 beats taking the RB. Both QB-first runs beat the RB-first run. I originally discounted this because the rooms looked QB-tilted — but the 4-to-6 point passing TD change means those rooms were probably about right for 2026, so the discount was unwarranted.
- **Unresolved:** the RB-first line has never been run on a board tuned for 2026 scoring. Lower priority than it looked before the scoring change surfaced, but still the run worth doing if there's time.

## Manual mode

The Chrome connection to the simulator drops frequently, and loading `/live/` without a draft key silently creates junk default drafts (12-team, 1QB, no IDP). If the connection is unstable, work the fallback: David drafts and pastes "gone: [names]" and the analysis happens off the pasted list. Same answers, no plumbing.

To recover a live draft, go to the simulator index and **Resume** the newest CUSTOM row — never navigate to `/live/` directly.
