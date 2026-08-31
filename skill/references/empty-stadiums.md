# Empty Stadiums — ESPN, 8-team superflex PPR

**This file supersedes `espn-8team-draft-strategy-2026.md` wherever they conflict.** That doc was written against assumed settings that turned out to be wrong in the one way that matters most — it treats this as a 1QB league. Settings below were read directly from the ESPN league office on Aug 20, 2026 (leagueId 42908600, David is teamId 5).

**Draft:** Saturday, Aug 22, 2026, 6:30 PM PDT. Snake, **4 minutes per pick**. **David picks 2nd — confirmed Aug 21.**

## Confirmed settings

**Starters (11), roster 16, bench 5 + 2 IR:**

| QB | RB | WR | TE | OP | DP |
|---|---|---|---|---|---|
| 2 | 2 | 3 | 1 | 1 | 2 |

OP is Offensive Player Utility — QB/RB/WR/TE eligible, so it functions as a superflex. **No kicker, no D/ST.** DP is individual defensive players.

**Scoring that deviates from standard, and why each matters:**

- **6 pt passing TD** — up from 4 in 2025. A pure quarterback buff worth roughly +70 to an elite passer and +44 to a low-end starter. Any inference from how this league drafted in 2025 understates how early quarterbacks should go now.
- **0.05/passing yard** (a point per 20 yards). Per ESPN's own projections in this scoring: Allen 495.6, Maye 450.9, Lamar 448.2, Burrow 445.8 — against 395.7 for Gibbs and 393.0 for Nacua. **Use `scoring-values.md` for the full table.**
- **Full PPR — 1.0 per reception**, and nothing for a target that isn't caught.
- **⚠️ The 0.5-per-target and 0.05-per-completion bonuses were REMOVED for 2026.** Both existed earlier in the preseason and both are gone. Anything reasoning from them overvalues high-target receivers, pass-catching backs, and volume passers. See `scoring-values.md` for what the change did to the position hierarchy — the short version is that **elite running backs now outscore elite receivers**, and elite tight ends fell below linebackers.
- **−2 per INT and per fumble lost.**
- **IDP: solo tackle 2.2, sack 8, INT 8, pass defensed 4, forced fumble 2.** Unusually rich — a three-down linebacker with 100 solo tackles clears 250 points.
- **Kick/punt return yards 0.1, return TDs 10.** See the return-yard section in `scoring-values.md` — the largest unpriced edge in the league.

**Other:** $500 FAAB with **continuous waivers processing six days a week**, **no trade review**, trade deadline Dec 2. **15 regular-season matchups; playoffs are weeks 16–17 as one-week rounds, 4 teams.**

## Format history — the room is still adjusting

2024 was a **1-QB** league. Superflex arrived in **2025**, and the room overcorrected immediately: six of the eight first-round picks were quarterbacks. For **2026** the passing TD moved from 4 to 6, buffing the position again.

Two seasons, two consecutive QB-favorable rule changes, and a room that reacted to the first one within a single draft. Read the 2025 tendencies below as a floor for how early quarterbacks will go this year, not as a forecast.

## Manager tendencies (2025 draft)

| Manager | Team | R1 pick | QB timing | Finish |
|---|---|---|---|---|
| Mark Minnie | I am Warren out… | Lamar 1.01 | QB @1.01 + 3.01 | 6th, last in points |
| Johnathan Thompson | Raiders 4 life | Daniels 1.02 | QB @1.02 + 2.07 | 2nd |
| Daniel Weaver | J'Drake May… | Allen 1.03 | QB @1.03, no QB2 thru R5 | 5th |
| Stephen Waymire | You've Been Autodrafted | Chase 1.04 (WR) | **zero QBs thru R5** | 4th, most points |
| David Firestone | The OG David | Hurts 1.05 | QB @1.05 + 3.05 | 3rd, best record 9–4 |
| Chris Rice | Should have autodrafted! | Mahomes 1.06 | QB @1.06, no QB2 thru R5 | 8th |
| Frankie Quintero | TushPusher | Bijan 1.07 (RB) | **first QB @5.07** | **1st, champion** |
| David Kallan | My Team Sucks Donkey Nix | Burrow 1.08 | QB-QB @1.08 + 2.01 | 7th |

Note the team names change every season — map managers by owner name, not team name, when reading older drafts.

## The exploitable pattern

**Round 1 is a quarterback feeding frenzy; rounds 2 through 4 are a quarterback desert.** In 2025, six QBs went in round 1, then only three more across the next twenty-four picks (Stroud 2.07, Purdy 3.01, Mayfield 3.05), with QB11 not gone until 5.07.

That shape is the whole edge. The market price of a quarterback in this league peaks in round 1 and collapses immediately after. Meanwhile the elite RB tier is genuinely short — it ends around Gibbs and Bijan — and the room's QB obsession lets skill players slide.

The scoring gaps are close to symmetric (elite QB to QB9 is roughly 95 points; elite RB to the RB available at pick 15 is roughly 97), so the tiebreaker isn't points — it's **which tier actually runs out.** Take the position that disappears, wait on the one this room predictably ignores for three rounds.

Results support it weakly but consistently: the two managers who chased QB hardest finished 6th and 7th; the champion's first QB came in round five and the points leader took none in five rounds. One season of eight teams is thin evidence, and some of it was Lamar's collapse to a QB20 finish rather than strategy — treat it as corroboration, not proof.

## Draft plan — pick 2 (CONFIRMED)

David confirmed the slot on Aug 21. His picks: **2, 15, 18, 31, 34, 47, 50, 63, 66, 79, 82, 95, 98, 111, 114, 127.** Note the 15/18 and 31/34 turns are near-back-to-back — plan those as pairs, since only one or two players come off between them.

Built from the 2025 board and four mock runs — see `mock-calibration.md` for what each claim rests on.

- **1.01:** expect a quarterback. Mark Minnie opened with one in all four mock runs and took Lamar first overall in 2025.
- **1.02: take the elite RB or WR — NOT the quarterback.** This reverses earlier guidance and the reversal is well-supported. See below.
- **15 + 18:** QB2 plus the best skill player. Twelve to thirteen quarterbacks are gone by pick 18 in every run — this is the last exit for a top-10 arm. **At comparable value, take the back over the receiver** (see the reversal note below).
- **31 + 34:** best available skill, RB-leaning. Elite backs are gone by pick 12; you're shopping the RB2 range against the WR2 range, and the back wins ties now.
- **47 + 50:** **the OP decision point** (below), plus RB/WR. **Tight end is no longer urgent here** — the position lost ~65 points when the target bonus went away and now sits below IDP on VORP (+110). Let Bowers and McBride come to you, or take the position in the 60s. Do not reach at 50 the way earlier runs did.
- **63 + 66:** WR3 and tight end.

**The OP slot decision happens at picks 47–50, not 63–66.** This is the one repeated mistake across every mock: waiting until the 60s leaves a QB pool of Cam Ward, Bryce Young, Brissett and Rodgers — lottery tickets in a starting slot. In both August runs the OP quarterback averaged around 10 fantasy points per game as a rookie, which is production risk exactly where the risk rules say not to take it.

At pick 47, check the quarterback board and commit:

- **If a QB projecting 370+ is available** (the Stroud / Daniel Jones / Darnold tier), take him there. That tier is gone by the 60s.
- **If the best remaining QB projects under ~370**, write the position off and plan to fill OP with your WR4 or RB3 instead. A 340-point receiver you're confident in beats a 360-point quarterback you aren't.

Do not drift into the 60s hoping a quarterback falls. The pool is picked clean by then in every simulation.
- **79 + 82:** **skill players, NOT defenders.** See the IDP timing correction below — this is two free premium picks.
- **111 + 114 + 127:** **both IDP starters, plus a swing.** Elite linebackers are available this late in this specific league.

### ⚠️ The 1.02 reversal — take the skill player, not the QB

Earlier versions of this file said "take the elite quarterback at 1.02." **That was wrong**, because it used hand-estimated projections instead of ESPN's actual numbers in this scoring.

**Value over replacement, ESPN projections, Empty Stadiums scoring:**

| Player | Pos | Proj | VORP |
|---|---|---|---|
| Puka Nacua | WR | 393.0 | **+163** |
| Jahmyr Gibbs | RB | 395.7 | **+146** |
| Ja'Marr Chase | WR | 371.2 | +141 |
| Bijan Robinson | RB | 386.5 | +136 |
| Josh Allen | QB | 495.6 | +121 |
| **Drake Maye** | QB | 450.9 | **+76** |
| Lamar Jackson | QB | 448.2 | +73 |

**Eleven quarterbacks project 407 or better.** That flat tier pushes QB replacement to ~375 and guts the elite-QB edge. Allen is the highest-scoring player in the league and still only the seventh-most *valuable* pick.

**Pick 2 + pick 15 as a pair:**

- Gibbs + Burrow at 15 = **841.5**
- Gibbs + Dak/Nix at 15 = 814.7
- Maye + McCaffrey at 15 = 819.0
- Maye + Jonathan Taylor at 15 = 802.3

RB-first wins the median case and ties the worst case.

**The league's tendencies reinforce it.** Five of seven managers open with a quarterback and then abandon the position — 2025 went 6 QBs in round 1, then 2, 2, 0, 1 across rounds 2–5. Only Quintero buys running backs early. The quarterback is replaceable two rounds later at a discount; the elite back is not.

**Recommendation at 1.02: take the best available WR — Nacua or Chase — then Gibbs or Bijan. Never a quarterback.**

**Verified by simulation.** Twenty runs of an in-house model (ESPN board + the 2025 per-manager tendencies + IDP deferred to rounds 13–16), measuring margin over the best rival team:

| Strategy | Margin | vs QB-at-1.02 |
|---|---|---|
| Zero-QB through round 4 | +286 | **+137** |
| WR-WR start | +225 | +76 |
| Elite WR at 1.02 | +175 | +26 |
| QB at 1.02 / pure best-points | +149 | — |
| RB-RB start | +146 | −3 |
| Elite RB at 1.02 | +134 | −15 |

**WR-first > QB-first > RB-first**, stable across model variants. Three starting WR slots means good receivers compound; two RB slots cap what an elite back returns.

**Caveat on the zero-QB line:** its +137 depends on quality quarterbacks surviving to rounds 5–6, and the QB tail in the model is estimated rather than scraped. Against the real room — six QBs in round 1, two in round 2 — the 407+ tier is probably gone by round 5. Treat "wait on QB" as directionally right and "wait until round 5" as unproven. Do not plan on it.

### ⚠️ IDP timing — the mocks were wrong, the league history is right

**Verified from the 2025 ESPN draft, by team.** Every manager deferred defenders to the very end:

| Team | Rounds they took IDP |
|---|---|
| J'Drake May (Weaver) | 15, 16 |
| Raiders 4 Life (Thompson) | 14, 15, 16 |
| I Am Warren Out (Minnie) | 15, 16 |
| Should Have Autodrafted (Rice) | 11, 14, 15 |
| You've Been Autodrafted (Waymire) | 9, 12 |
| David | 15, 16 |

**Jordyn Brooks went 128th — the last pick of the draft. Fred Warner 114th. Jack Campbell 126th. Roquan Smith 107th.** Those four project **387, 350, 347 and ~340** in 2026 scoring.

The FantasyPros simulator showed the defensive run starting around pick 75, and earlier versions of this plan were built on that. **It's a simulator artifact — the real room waits until rounds 14–16.** Trust the league history.

**The consequence:** take skill players at 79 and 82, and draft both linebackers from picks 111 onward. That's two extra premium picks relative to the old plan, and the position cost is close to zero.

**Guardrail:** if two or more defenders come off the board before pick 100, the room has changed — accelerate and take yours immediately.

### How opponents actually draft — roster-need model

Confirmed across all eight 2025 rosters: **managers fill offensive starters before any depth, and defenders dead last.** The typical shape was QB, QB, RB, RB, WR, WR, WR, TE across rounds 1–9, then bench/depth in 10–13, then IDP in 14–16.

Combine that with ESPN rank to predict a specific pick: **the next opponent takes the highest-ESPN-ranked player who fills a starting slot he hasn't filled yet.** A team already carrying two quarterbacks will pass an ESPN-top-10 QB to take a WR3 ranked 40th. That is exactly how elite arms slide, and it compounds the ESPN-rank effect rather than replacing it.
- **95+:** bench upside. A spare startable quarterback is the single best bench asset in this league — eight teams need up to 24 of them, which makes one the most liquid trade chip you can hold. Daniel Jones was available at ECR 24 at pick 127 in run 4.
- **Never:** a kicker or defense. They don't exist in this league.

## Risk posture: floor early, ceiling late

David's stated preference, and it should drive every recommendation: **minimize bust risk on starters, maximize upside on the bench.** The asymmetry is structural — a starter you draft in round 2 costs you points every single week if he busts, while a bench player who busts costs you nothing, because he was never in the lineup. Bench spots are call options. Price them that way.

### Two kinds of risk, priced very differently

This is the distinction that matters most, and it's easy to collapse them into one word ("risky") and get it wrong.

- **Availability risk — will he be on the field?** Injury, suspension, holdout. This reduces *games*, not per-game output. **Cheap.** In an 8-team league the waiver wire is stocked, so a missing week costs a replacement-level fill-in rather than a zero.
- **Production risk — will he produce when he plays?** Unproven role, contested target share, bad quarterback, dependence on repeating outlier efficiency. This attacks the number that actually decides weeks. **Expensive.** Downgrade heavily, especially for a starting slot.

The archetypes carrying real *production* risk: age cliffs at running back (McCaffrey), players whose value rests on efficiency they may not repeat (Achane), and pass-catchers who just lost target share (Kincaid after the D.J. Moore trade). A player merely coming back from injury on a known timeline is a different and much cheaper thing.

### The discounted-return stash — a late-round play

**Most of this league drafts off projected season totals.** A player suspended or injured through week 5 has his total gutted, so he falls far below what he's worth per week. Buy him late and collect elite weekly production for the part of the season that decides anything.

Rashee Rice in 2025 is the template — a late pick, a known return date, and the only cost was carrying depth for five weeks.

Requirements:

- **The return date must be known**, not open-ended. "Out indefinitely" doesn't qualify.
- **Back by roughly week 8**, half of the 15-week regular season.
- **Late-round price only.** Never pay a starter's cost for someone who won't be there in September.

Under the weeks 16–17 playoff format this is stronger than it looks: a player returning at week 6 is available for the entire stretch run *and* both playoff weeks. You buy the part of the season that matters at a discount created by the part that doesn't.

### Variance: David prefers a tighter standard deviation

**A 30-then-5 player is worse than his average suggests.** The cost isn't the season total — it's the start/sit decisions he forces. You guess weekly and you're wrong about half the time, and that loss never appears in any projection.

There's a structural reason too: **in head-to-head, the favorite wants low variance and the underdog wants high.** A QB-first build in a superflex league makes David the favorite most weeks, so protecting the floor is what converts a talent edge into wins. Volatility hands worse teams a puncher's chance.

**Touchdown dependency is the main variance driver.** Yards and receptions accumulate steadily; touchdowns arrive in clumps. How the scoring interacts:

- **Full PPR stabilizes** — receptions are the most predictable input in football and worth 1.0 each.
- **6-point TDs destabilize** — every score is a bigger swing than in a 4-point league.
- **Solo tackles at 2.2 are the most stable input in the entire format** — a three-down linebacker posts 6–9 essentially every week.

### How to measure it — coefficient of variation

**Raw standard deviation is misleading.** In 2020 Tyler Lockett's std dev was 13.36 and Davante Adams' was 12.23 — nearly identical — but Lockett averaged 16.6 points a game and Adams 25.6. Adams was obviously the steadier player.

**Use coefficient of variation: CV = standard deviation ÷ points per game.** Lockett came out at 0.80, Adams at 0.47. Lower is steadier. CV normalizes across scoring levels so a QB can be compared to a WR.

**Positional baselines** (PlayerProfiler, 20 seasons — the peak of each position's distribution):

| Position | Typical CV |
|---|---|
| **QB** | **~0.40** — by far the most stable |
| RB | ~0.50–0.60 |
| WR | ~0.60–0.70 |
| TE | ~0.70–0.80 — least stable |

**Variance is sticky year over year.** Their 20-season study found a strong correlation between a player's CV in one year and the next — high-variance players tend to stay high-variance. That's what makes historical data usable rather than noise.

**Where to get it:** compute from weekly game logs (FantasyPros game logs, or ESPN), converted into this league's scoring. For a fast draft-day proxy, FantasyPros' **Quality Starts "% Poor"** is already league-scored and answers nearly the same question. Full CV is worth computing only for the handful of decisions that are genuinely close.

**Drafting rules that follow:**

1. **IDP: take tackle machines, never sack-and-turnover specialists.** Sacks and interceptions are worth 8 apiece and arrive in clumps — a pass rusher can post zero for three straight weeks, while a three-down linebacker posts 6–9 solos nearly every game. *(Reasoned from the scoring, not from the CV study, which doesn't cover IDP.)*
2. **Receivers: target share over big plays.** Strongly supported. The highest-CV receivers (0.80+) are a recognizable archetype — low target share, deep speed, tertiary options on prolific passing offenses. But note the compression: among receivers above ~11 points per game, CV ranges only about 0.50 to 0.75, and the higher-variance option usually carries a points-per-game deficit that cancels the upside.
3. **~~Backs: three-down roles over committee.~~ CORRECTED — this is not supported.** Controlling for points per game, **running back variance is organized almost entirely by usage level, not by player type.** Nick Chubb, a pure runner, posted an *identical* CV to pass-catchers like Ekeler and Dalvin Cook. Satellite backs match ground-and-pound backs. What actually drives RB variance is workload *changing* mid-season through injury or coaching decisions. So: pick backs on projection and role security, and don't pay a premium for receiving work on variance grounds.
4. **Quarterbacks are the lowest-variance position** — stable snap counts, never game-scripted out, and low per-yard passing value compresses yardage swings. **Refinement: mobile quarterbacks are the higher-variance subset**, because rushing and touchdowns are the volatile inputs. Under a low-variance preference that mildly favors a pocket passer like Maye or Goff over a rushing quarterback.
5. **Returners: distinguish dual-role from pure specialist.** A returner who also collects receptions or carries has two independent income streams that smooth each other — Marvin Mims (Denver WR role plus punt returns) is steadier than his reputation. A **pure specialist** like Turpin matches the classic high-CV archetype: explosive, low-volume, boom/bust. Dual-role returners are lineup-viable; pure specialists are bench lottery tickets.

**The honest caveat on chasing upside:** the same study found that in redraft head-to-head, playing a below-average player for the chance at a spike is almost never correct — you can't predict which week he pops. That's an argument *for* David's low-variance preference on starters, and it means bench upside pays off mainly when a player's **role** changes (injury ahead of him, promotion), not when he happens to spike for one week.

**Where variance is fine: the bench, entirely.** A safe bench player never enters the lineup, so his floor is worth nothing. Ceiling is the only thing being purchased there.

### The bench: five swings, no insurance

**Rounds 10–16 are pure ceiling. Do not reserve a bench spot to cover a bye week.** Talent is liquid — a stud can be traded, a safe body can't — and in an 8-team league the waiver wire supplies replacement-level production for free during the season.

Target ambiguous backfields, injury-discounted starters, second-year receivers with rising target share, rookies with a path to volume, **full-time kick and punt returners** (see `scoring-values.md` — worth 50 to 180 points that nobody else prices), and a spare startable quarterback as a trade chip. A 20% shot at a league-winner beats a 90% shot at a player who never enters the lineup.

## Schedule structure

**Weeks 1–15 are the regular season. Weeks 16 and 17 are the playoffs — one-week rounds, 4 teams.** Verified in ESPN settings Aug 21, 2026: 15 regular-season matchups, 1 week in round 1, 1 week in the championship.

**One-week playoff rounds raise variance sharply.** There's no two-week aggregate to absorb a bad game, so a single dud from a starter can end your season. That's an argument for weekly ceiling over season-long floor among comparable players — and it makes the trade deadline (Dec 2) matter, since it's your last chance to upgrade before single-elimination.

Two consequences that change how byes and schedule get weighted:

- **No bye week touches the playoffs.** NFL byes end at week 14, so weeks 16 and 17 are bye-free. Bye management is purely a seeding concern — it can never cost a playoff game. This is the main reason the bye rule below is as permissive as it is.
- **A compromised week is 1 of 15**, not 1 of 13. Absorbing one bad week is cheaper than it looks.

**Strength of schedule should be weighted to weeks 16–17.** The 2026 research below was gathered for the more common weeks 15–17 window, so treat it as directional and re-pull if precision matters:

- **Easiest late-season slates:** Washington, New Orleans, Arizona
- **Hardest:** Philadelphia, Seattle, San Francisco
- **Softest receiver matchups:** opponents Cleveland, Tennessee, Minnesota

Apply SOS **as a tiebreaker between comparable players, never as a reason to move someone up a tier.** Schedule projections are built on last season's defensive performance and are among the least predictive inputs in fantasy.

## The bye-week rule

**David's stated preference is talent first.** Byes are close to irrelevant on draft day — they cost at most one regular-season week out of fifteen, they can never touch the playoffs, and mid-season trades are the proper fix. Draft accordingly.

| Situation | Threshold |
|---|---|
| Up to **3 starters** on one week | **Ignore byes entirely. Take the best player.** |
| Going from **3 → 4** | Break ties within ~**5 ECR spots** |
| Going from **4 → 5** | ~**15 spots** |

**Weight by timing — early clusters are the dangerous ones.** This is counterintuitive and worth getting right:

- **Weeks 5–9: apply the thresholds as written.** Early in the season you're stuck with the roster you drafted. The waiver wire hasn't produced anything yet, and nobody trades in September because everyone still likes their team. Four starters out in week 7 is genuinely hard to manage.
- **Weeks 11–14: relax one step.** By then you know who busted, the wire has surfaced two or three real contributors, and a trade market exists. Four starters on a late bye is a trade problem, not a draft problem.

Bench players never count toward the total — the bench *is* the coverage.

**Worked example of the rule firing correctly**, from the Aug 20 mock: at pick 34, Maye and Nacua were both on week 11 and Drake London (ECR 42) would have made three. Under the current rule that's fine — three is acceptable — so London was the right pick, and the Jeanty selection (ECR 41, bye 13) was defensible only because it was ECR-neutral.

**Worked example of over-applying it:** at pick 50, week 13 already held three starters and Tee Higgins (ECR 72) was taken over Zay Flowers (ECR 60) to avoid a fourth. That cost twelve spots on a *late* bye, which the timing rule now explicitly forgives. Take Flowers.

**Roster math check:** 11 starters and only 5 bench spots. There is far less room for lottery tickets than a normal 8-team league — you'll spend most picks filling the lineup. The "rounds 8–12 are pure upside swings" advice in the older strategy doc assumed a deeper bench and doesn't apply cleanly.

## Still to confirm

- Whether the room learned from Quintero winning with a round-5 quarterback. If they zag too, QBs last even longer and the case for skill players early gets stronger, not weaker.

## After the draft

Save the roster to `/tx2025-data/empty-stadiums-roster-2026.json`, grade against this plan, list week-1 waiver targets, and record each manager's 2026 tendencies in the table above so next season starts with two years of data instead of one.
