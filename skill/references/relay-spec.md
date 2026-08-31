# ff-data — league state relay

Machine-readable snapshots of David Kallan's two fantasy leagues, written twice a
week by a Claude Cowork task and read by Claude in chat.

**Why this exists.** Claude's analysis sandbox is network-allowlisted to package
registries plus GitHub. It cannot reach CBS, ESPN, FantasyPros' site, or David's
VPS. It *can* reach `raw.githubusercontent.com`. So Cowork reads the leagues
through a browser, commits JSON here, and Claude pulls it. This is the only
hands-off path from a league into a chat.

**The FantasyPros API cannot replace this.** It has no roster endpoint. Its
`league_key` parameter is MLB-only and is silently ignored on NFL endpoints
(tested Aug 24 2026: a deliberately fake key returned HTTP 200). The API gives
projections, rankings, injuries and news — league state comes from here.

## Schedule

Waiver deadlines are **Wednesday and Saturday nights**; claims process
**Thursday and Sunday early morning**.

| Run | When | Purpose |
|---|---|---|
| Thursday | **06:00 local, AFTER waivers process** | See what claims landed; plan for Saturday's deadline |
| Sunday | **06:00 local, AFTER waivers process** | See what landed; plan for Wednesday's deadline |

**Do not run before waivers process.** A Wednesday-night run captures pre-waiver
rosters, which are stale by the time anyone reads them.

## Layout

```
tx2025/latest.json          # CBS, 12-team true 2QB — David's primary league
tx2025/2026-09-03.json      # dated copy, one per run
empty/latest.json           # ESPN, 8-team superflex + IDP
empty/2026-09-03.json
```

Write both the dated file and overwrite `latest.json` every run.

## Schema

```json
{
  "league": "tx2025",
  "pulled": "2026-09-03T06:02:11Z",
  "week": 1,
  "my_team": "Ja'Marr You Not Entertained?",
  "teams": [
    {
      "name": "Ja'Marr You Not Entertained?",
      "faab_left": 2500,
      "record": "0-0",
      "roster": [
        {"name": "Bo Nix", "pos": "QB", "slot": "QB", "status": ""},
        {"name": "Jahmyr Gibbs", "pos": "RB", "slot": "BE", "status": "Q"}
      ]
    }
  ],
  "free_agents": [
    {"name": "Rachaad White", "pos": "RB", "pct_rostered": 41}
  ],
  "transactions": [
    {"date": "2026-09-03", "team": "Red Dogs", "type": "waiver",
     "added": "Tank Dell", "dropped": "Justice Hill", "faab_spent": 180}
  ],
  "standings": [
    {"team": "Bills Mafia", "record": "2-0", "pts_for": 512.4}
  ],
  "matchup": {"week": 1, "opponent": "Red Dogs"}
}
```

### Field notes

- **`faab_left` is the highest-value field.** It determines who can outbid
  David, which is the entire bidding decision. Never omit it.
- **`slot`** — the actual lineup slot (`QB`, `RB`, `WR`, `TE`, `FLEX`, `OP`,
  `DP`, `BE`, `IR`). Tells Claude what each manager *thinks* their best lineup
  is, which sometimes exposes a hole they haven't noticed.
- **`status`** — injury tag exactly as shown (`Q`, `O`, `IR`, `D`), empty string
  if none.
- **`pos`** — for Empty Stadiums IDP, use `DP`.
- **`free_agents`** — top ~40 by percent rostered. Rising percentage is the
  signal; it means other leagues are already claiming him.
- Player names verbatim from the site. Claude fuzzy-matches and flags anything
  it can't resolve rather than guessing.

## Source — FantasyPros MyPlaybook

`fantasypros.com/nfl/myplaybook/my-team.php`. League dropdown upper-left switches TX2025 / Empty Stadiums. **The second dropdown, below "My Playbook", switches to any of the 12 managers' teams** — that is what makes the needs matrix possible.

**⚠️ PRESS SYNC BEFORE READING.** MyPlaybook caches. Without an explicit sync the task reads whatever was last pulled, which during a live draft could be hours old.

**⚠️ An empty CBS roster is CORRECT, not an error.** The TX2025 league was cleared for the 2026 season and stays empty until the draft populates it. Do not retry, do not fall back to last year's cached roster, do not treat it as a failure. Write `"roster": []` and move on.

MyPlaybook also exposes **transactions and standings** beyond rosters — capture both once the season starts. Transactions show who claimed whom and for how much, which is the best read on how each manager values FAAB.

Fall back to CBS/ESPN directly only if MyPlaybook is missing a field.

(Superseded guidance below kept for reference.)
Prefer **FantasyPros MyPlaybook** if both leagues are synced — one site for both
leagues means one task and one thing to fix when it breaks. Fall back to CBS
(`tx2008.football.cbssports.com`) and ESPN (`leagueId 42908600, teamId 5`)
directly if MyPlaybook is stale or missing a field.

## Consuming it

```bash
python3 scripts/pull_league.py --repo <owner>/ff-data                 # tx2025 latest
python3 scripts/pull_league.py --repo <owner>/ff-data --league empty
python3 scripts/pull_league.py --repo <owner>/ff-data --date 2026-09-03
```

Prints a needs matrix across all rosters, FAAB standings, David's valued roster,
and ranked free agents.

## What the brief does NOT do

It surfaces state. It does not decide.

- **Waivers** — rank by rest-of-season marginal gain over the player being
  *dropped*, not over a theoretical replacement. Bid odd numbers; ties go to the
  worse team by inverse standings. See `faab-waivers.md`.
- **Lineups** — never use season totals. Pull weekly projections
  (`/nfl/2026/projections?week=N`), weekly ECR, and injury probabilities. See
  `weekly-lineup.md`.
- **Trades** — the needs matrix identifies buyers. Price both sides with a
  before/after optimal-lineup comparison. Never sum chart values.

## Nothing sensitive belongs here

Rosters and FAAB only. No credentials, no `.env`, no API keys. Add `.env` and
`*.key` to `.gitignore` before the first commit.
