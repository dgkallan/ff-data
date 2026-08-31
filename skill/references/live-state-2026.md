# Live state — as of Sat Aug 29 2026, ~7am PT

Read this first in any new session. **Both leagues are drafted — this is in-season management now.** It is the "where we are right now" file; the durable strategy lives in `tx2025.md`, `empty-stadiums.md`, `trade-value-model.md`, `faab-waivers.md`.

## TX2025 (CBS) — DRAFT COMPLETE, in-season now

- **Slot 9, LOCKED.** Picks 9 · 16 · 33 · 40 · 57 · 64 · 81 · 88 · 105 · 112 · 129 · 136 · 153 · 160
- Multi-day draft, opens today, runs into next week. Long gaps between picks — **use them to news-check every name before recommending.**
- `scripts/tx2025_board.json` rebuilt from **8/29** FantasyPros data (196 players, all bye weeks present). Verified: QB6→QB15 spans 16 pts (flat band intact), QB25→QB30 cliff is 81.
- Pick-33 QB pool: Goff 364 (adp 30) · Dart 361 (32) · Herbert 361 (34) · Nix 360 (36) · Mayfield 342 (39). Goff went at picks 30 and 32 the last two years — usually just misses.

### News the projections have NOT priced (checked 8/28-8/29)

| Player | Situation | How to treat it |
|---|---|---|
| **Josh Jacobs** | Charged Thu 8/27 w/ misdemeanor battery + criminal damage (reduced from felony strangulation). Court date **Nov 17**. NFL baseline for a personal-conduct DV finding is 6 games; Schefter expects action before Week 1; GB GM says they're preparing. Also a groin issue. | **David's read: the NFL often waits for legal resolution (Kamara 2022 precedent), which is why he isn't discounted.** So the projection may be correct, not stale. Treat as a live coin flip, not a fade. |
| **Ashton Jeanty** | Sprained ankle (more low than high), ECR fell 10 to No. 22, may miss Wk 1 | availability risk, talent unchanged |
| **Jeremiyah Love** | High ankle sprain, first preseason snap | fade at pick 40 |
| **Travis Hunter** | Down 23 ECR to 191 — practicing mostly at **cornerback**, ~0 offensive 11-on-11 one session | **off the board** |
| **Browns QB** | Monken said he'd name a Wk1 starter Mon 8/24. Sanders favored on accuracy metrics. Projection still splits the job (1,633 pass yds). | **check the announcement** — if Sanders won it he's a ~270-pt arm priced as a backup |
| **Raiders QB** | Cousins listed QB1 on first depth chart, sat the preseason finale; Mendoza expected to take over eventually. Projection splits (Cousins 781, Mendoza 2,881). | same logic, opposite direction |
| **MarShawn Lloyd** | Becomes GB lead back if Jacobs sits | late-round dart worth remembering |

**Aug 29 refresh finding:** FantasyPros stat projections did **not** change 8/26→8/29 (zero movement). Only deep ECR moved (WR130+/RB130+, cut-day churn). So none of the above is in the numbers — that is the edge, since the room drafts off the same rankings.

## Empty Stadiums (ESPN) — post-draft, three trades done

Roster after trades: **QB** Burrow 433 · Dak 428 · SFLX Mayfield 377 · **RB** Bijan 393 · Cook 293 · **WR** Jefferson 292 · Olave 278 · Nabers 254 · **TE** Loveland 221 · **IDP** Warner, Roquan · **BN** Irving 235, Evans 213, Parker Washington 192, + waiver add.

- **2,892 → 2,969 (+77).** Trades: DeVonta Smith + Jaylen Warren → James Cook III (Mark); Hampton + Stroud → Mayfield + Olave (Pappy/Dan Weaver); Malik Washington → Parker Washington (Pappy).
- Every starting slot equal or better; RB2 went **up** (Hampton 266 → Cook 293). Risk tightened at RB2 and WR2.
- **No further trades worth making** — best remaining mutual-gain deal is +3. Roster is at a local optimum.
- Waiver plan: claims in for **Brooks and Lemon**, dropping **Cam Ward** (no QB shortage — every team carries 3-4 and the wire has Mendoza/Tua/Watson).
- **Remaining exposure:** Bijan is 13% of the offense; Loveland is the only TE. Neither worth a stash — TE wire is 8 deep inside 17 pts.

## Pipeline status

- **Pipe A LIVE.** `/opt/ff/sync.sh` on the VPS → FantasyPros API → GitHub `dgkallan/ff-data`. Cron Thu + Sun 6am. Read with `scripts/pull_league.py --repo dgkallan/ff-data`, or curl `raw.githubusercontent.com/dgkallan/ff-data/main/nfl/<file>`.
- **Git was corrupted 8/29** by a VPS restart mid-write plus a two-writer conflict (Cowork also pushes). Repaired by re-cloning. `sync.sh` now pulls --rebase before pushing.
- **Pipe B PARTIAL.** Cowork scrapes MyPlaybook → `tx2025/` and `empty/` in the same repo. Works, but **FantasyPros exposes no per-team FAAB** — that has to come from CBS directly, and it's the field that decides bids.
- **TX2025 FAAB — RESOLVED Aug 30:** **$2,500 for New Orleans trip attendees, $2,000 for everyone else.** David is on the $2,500 tier. Still to determine: which opponents are on which tier.


---

# FINAL ROSTERS — both leagues, post-draft

## TX2025 (CBS, 12-team true 2QB, half-PPR for RB / full for WR-TE, no K/DEF)

| Slot | Player | Pts | Bye |
|---|---|---|---|
| QB | Bo Nix | 360 | 10 |
| QB | Tyler Shough | 339 | 8 |
| RB | Bijan Robinson | 321 | 11 |
| RB | Ashton Jeanty | 233 | 13 |
| WR | CeeDee Lamb | 287 | 14 |
| WR | Tee Higgins | 228 | 6 |
| WR | DK Metcalf | 201 | 9 |
| TE | Tyler Warren | 204 | 13 |
| FLEX | Xavier Worthy | 171 | 5 |
| BN | Geno Smith | 285 | 13 |
| BN | Makai Lemon | 154 | 10 |
| BN | MarShawn Lloyd | 97 | 11 |

**Starting total 2,344.** Byes are clean — only week 13 loses two starters (Jeanty + Warren).

**Live watch items:**
- **Jeanty ankle** — low sprain, Kubiak non-committal, first injury report Wednesday before the Sept 13 opener vs MIA. If he sits, RB2 is Lloyd at 97. **This is the roster's one hole.**
- **MarShawn Lloyd** — GB traded for Kaleb Johnson (PIT, 2025 3rd) on cut-down day, so the Jacobs-suspension backfield is a committee (Lloyd / Brooks / Johnson / Strong), not a handoff. Lloyd is the incumbent and had a strong camp, but the unofficial depth chart lists Brooks RB2. Jacobs' court date is **Nov 17**; 6-game baseline.
- **Geno Smith** is the trade asset — ~10 teams have no QB insurance.

## Empty Stadiums (ESPN, 8-team superflex, full PPR, 2 IDP)

QB Burrow 433 · Dak 428 · SFLX Mayfield 377 · RB Bijan 393 · Cook 293 · WR Jefferson 292 · Olave 278 · Nabers 254 · TE Loveland 221 · IDP Warner, Roquan · BN Irving 235, Evans 213, Parker Washington 192.

**2,969 after three trades (+77).** No further trades worth making — best remaining mutual gain +3.


---

## In-season priorities, week 1

**TX2025**
1. **Jeanty's ankle** — first injury report Wednesday before the Sept 13 opener vs MIA. If he sits, RB2 is MarShawn Lloyd at 97. This is the roster's one hole and the first waiver target if it breaks bad.
2. **Geno Smith is the trade asset.** ~10 teams carry exactly two QBs with no insurance. Value spikes the moment any starter goes down. Do not trade him cheap in September.
3. **MarShawn Lloyd** — GB traded for Kaleb Johnson on cut-down day, so the Jacobs backfield is a 4-way committee. Jacobs' court date is **Nov 17**, 6-game baseline. Lloyd is a hold, not a lock.

**Empty Stadiums**
1. Roster is at a local optimum — best remaining mutual-gain trade is +3. **Stop trading, start watching.**
2. **Bijan is 13% of the offense** with Cook behind him and a 158-pt cliff to Irving. That injury is the one that hurts.
3. **Loveland is the only TE.** Wire is 8 deep inside 17 pts, so do not stash — claim when needed.

**Both leagues:** the relay runs Thu + Sun 6am after waivers process. `sync.sh` now pulls --rebase before pushing (fixed Aug 29 after a two-writer corruption).
