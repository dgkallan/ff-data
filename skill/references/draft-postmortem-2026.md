# Empty Stadiums 2026 Draft Postmortem — What Broke and Why

**Read this before running any future live draft.** Six failures from the Aug 22 2026 draft, each with its root cause and the rule that now prevents it. The methodology in `live-draft-playbook.md` was mostly sound — every failure below was an *execution* violation of a rule that already existed, which is why the fixes are hard procedural rules, not strategy changes.

## Failure 1 — Burrow at pick 15 (−40 pts)

**What happened:** Recommended Burrow (445.8, ESPN 16) over Lamb (322.2) because Burrow was "the highest-projecting player at risk." The plan said WR-WR-WR at 15/18/31.

**Root cause:** Led with raw projection instead of gap-to-next-at-position. Burrow's gap to Stafford (442.8, ESPN 34, guaranteed to survive) was **+3**. Lamb's gap to the next WR tier was **+50**. The arbitrage table in the playbook says QBs fall in this league — chasing one at 15 contradicted the skill's own central finding.

**Also:** the pre-draft "only override: Burrow falls to 15" condition was asserted, never sim-tested or gap-tested. An override that was never tested is not an override, it's a hunch with documentation.

**RULE: Every recommendation states the gap to the next survivor at that position FIRST. A deviation from plan requires gap ≥ 30 at the position being taken, AND the alternative position's gap must be smaller. No exceptions for big raw numbers.**

## Failure 2 — Malik Washington at 31 (fabricated data)

**What happened:** Recommended a player as "325.9 projected, ESPN 273" — a WR3-level projection at a rank of 273. The projection was a parse artifact from scraping ESPN's virtualized table; his real 2025 finish was ~WR70. Rationalized the contradiction as "return-yard arbitrage" because that matched a pre-existing thesis.

**Root cause:** Live DOM scraping used for *projections*, and an obvious internal contradiction (rank 273 + top-3 positional projection) explained away instead of investigated.

**RULES:**
- **The pre-draft board (FantasyPros API, built in setup) is the ONLY source of projections.** The live tab is read for one thing: who is gone. Never for numbers.
- **A player not on the pre-built board gets flagged as "NOT ON MY BOARD" and his actual 2025 finish stated aloud before any recommendation.**
- **Rank and projection must agree within ~40 spots. A rank-200 player with a top-30 projection is a parse error, never an edge.** Real edges are 20–30 spots and explainable in one sentence.

## Failure 3 — Recommended already-drafted players (Goff at 66, Caleb Williams at 70)

**What happened:** Recommended Goff at pick 66 when he'd been drafted at pick 60. Then recommended Caleb Williams, also gone. The available-players list I'd scraped was stale.

**RULE: Before naming any player, check the pick-history/activity feed — the append-only log — not a cached available list. The last 10 picks in the activity feed are the freshest data on the page.**

## Failure 4 — Lost track of the roster ("you have three QBs" when he had two)

**What happened:** Late-draft, asserted David had 3 QBs from memory. He had Burrow + Prescott only; the OP slot was empty. This produced a chain of bad advice (told him to skip QB at 70).

**RULE: Re-read the roster panel from the page before EVERY recommendation from round 6 on. State empty starting slots explicitly: "Open: OP, DP, DP." Never answer roster questions from memory — memory is stale the moment a pick processes.**

## Failure 5 — Too slow

**What happened:** Multi-paragraph responses on a 4-minute clock. David missed windows waiting for analysis and eventually said so.

**RULE: During a live draft, the ENTIRE response is one line:**
```
PICK: Name (proj, 2025 finish) | gap +X | backup: Name
```
**Analysis only between turns or when explicitly asked. If a scrape + response can't complete in ~30 seconds, give the answer from the pre-built board and verify after.**

## Failure 6 — Answered a question that wasn't asked

**What happened:** "Should I swap Malik Washington for Brian Thomas" got an answer about a different comparison entirely (Thomas vs Herbert as the pick).

**RULE: If the question could map to two different decisions, restate it in six words and answer the restatement. One line: "You mean drop X, add Y? →"**

## What went right (keep these)

- The waiting rule (12-gap/2-gap safety lines) called survivorship correctly all night.
- The QB-wait thesis held: Prescott at 34, and 400+ QBs were available into round 7.
- Bijan at 2, Jefferson at 18, Loveland — the plan's structure produced a top roster despite the errors.
- Owning mistakes immediately kept trust recoverable. Hiding them would not have.

## The meta-lesson

Every failure shares one root: **trusting fast, unverified state (a scrape, a memory, a big number) over slow, verified state (the pre-built board, the page, the gap test).** Under clock pressure the pull is toward the fast answer. The rules above exist to make the verified answer the fast answer: build the board before the draft, read only the activity feed during it, and answer in one line from data that was already checked.
