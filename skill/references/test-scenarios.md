# Test Scenarios for TX2025 Fantasy Skill

Use these scenarios to validate the skill before the season starts.

---

## Scenario 1: Waiver Bid Strategy (Mid-Season)

**Input:**
```
Week 6 waiver wire. My roster:
QBs: Lamar Jackson, Jalen Hurts
RBs: Derrick Henry, Tony Pollard
WRs: Justin Jefferson, Deebo Samuel, Courtland Sutton
TE: Mark Andrews
Bench: Daniel Jones (QB), Jonathan Taylor (RB), Tyler Higbee (TE), D'Andre Washington (RB)

Available on waivers (top RBs):
- Kenneth Walker III (SEA, bye 8, 15% owned)
- Jaleel McLaughlin (DEN, bye 11, 8% owned)
- Rachaad White (TB, bye 10, 22% owned)

Remaining FAAB: $1,650

What's my strategy?
```

**Expected Output:**
1. Identifies RB depth as priority (3 starters, shallow bench)
2. Ranks: KW3 (Tier A, ~$220), Jaleel (Tier B, ~$120), Rachaad (Tier B, ~$140)
3. Suggests: Bid KW3 first, fallback to Jaleel if outbid
4. Notes: Hold $800+ for future waivers (2 months left)

---

## Scenario 2: Trade Evaluation

**Input:**
```
Trade offer received:

I GIVE: Lamar Jackson (QB, BAL, bye 7) + Tyler Higbee (TE, LAR, bye 4)
I GET: Patrick Mahomes (QB, KC, bye 10) + Tee Higgins (WR, CIN, bye 12)

My current roster:
QBs: Lamar, Jalen Hurts
RBs: Henry, Pollard, J-Taylor
WRs: Jefferson, Deebo, Sutton
TE: Higbee, Engel
Bench: Daniel Jones, D'Andre Washington

Their roster:
QBs: Mahomes, Daniel Jones, Kirk Cousins (deep)
RBs: Josh Jacobs, AJ Dillon
WRs: Tyreek Hill, CeeDee Lamb, Jaylen Waddle
TE: Darren Waller

Should I accept?
```

**Expected Output:**
1. Maps values (Lamar ~64 SF, Higbee ~15 → 79 total vs. Mahomes ~58, Higgins ~34 → 92 total)
2. Analysis: You're trading down slightly in QB value but gaining significant WR upside
3. Roster fit: You get a WR1 (Higgins) to replace Sutton (3rd), which is a plus
4. Recommendation: Accept if you're confident Mahomes is enough at QB; decline if you want Lamar's ceiling
5. Flag: Opponent has QB depth, so they benefit from the trade; be mindful

---

## Scenario 3: Draft Strategy (Pre-Season)

**Input:**
```
I'm picking 6th overall in our 12-team 2QB league. FantasyPros says:
- Top 5 consensus: Lamar Jackson, Patrick Mahomes, Josh Allen, Derrick Henry, Christian McCaffrey

Should I reach for QB at 6, or take a RB/WR?
```

**Expected Output:**
1. Shows ADP spread: QBs are heavily concentrated in rounds 1–2 (likely 1.01–1.08)
2. At 1.06, consensus best-ball is elite RB (Henry, CMC, or next-tier RB)
3. Recommendation: **Take RB at 1.06**, secure a strong QB in round 2 (e.g., pick 2.06 ≈ ~Jalen Hurts or similar tier)
4. Why: QB value cliff between round 1 and 2 is minimal; RB supply is tighter in 2QB
5. Bye week note: Check 1.06 RB's bye; avoid clustering with 2QB's bye

---

## Scenario 4: Streaming QB (Late-Season Waiver)

**Input:**
```
Week 13. I have Lamar (bye 7, done) and Jalen Hurts (bye 10, done).
Available QBs on waivers:
- Brock Purdy (SF) - $50 bid reasonable?
- Daniel Jones (NYG) - $35?
- Joe Flacco (IND) - $20?

Remaining FAAB: $400

Who do I bid on?
```

**Expected Output:**
1. Flags: In a 2QB league, streaming at week 13 is late; you should have secured backups earlier
2. Ranks by RoS strength: Purdy > Jones > Flacco
3. Bid strategy: $50 for Purdy (secure), $30 for Jones (fallback), leave $320 for emergencies
4. Note: If both are drafted, consider stashing an unreliable QB over a bench flex

---

## Test Execution

1. **For each scenario**, paste the input into the skill
2. **Evaluate output** against expected results (does ranking make sense? Are bids reasonable? Is reasoning sound?)
3. **Iterate** if output seems off (refine scoring logic, adjust bid tier thresholds, etc.)

---

**Success Criteria:**
- Waiver bids are grounded in remaining budget + position need
- Trade evaluations cite trade values + roster fit
- Draft strategy avoids naive QB-at-6 mistakes in 2QB leagues
- Recommendations are actionable (clear priorities, not hedging)
