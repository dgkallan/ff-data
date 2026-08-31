# Trades — Empty Stadiums

8-team superflex, **no trade review and no veto** — deals process the instant both sides accept. Deadline **Dec 2, 2026, 9:00 AM PST**. Only seven possible partners, so the market is small and reputation compounds.

Companion to `scoring-values.md` (conversion multipliers) and `faab-waivers.md` (the wire, which sets replacement cost for everything below).

## Trade value is not projected points

The only number that matters is **how many starting-lineup points David loses if the player is gone and he refills the slot from the wire.** Projection is an input to that, not a substitute for it.

Run against the modelled post-draft roster (3,738-point lineup):

| Player | Pos | Projection | **Real trade value** |
|---|---|---|---|
| Jahmyr Gibbs | RB | 396 | **191** |
| Amon-Ra St. Brown | WR | 354 | **144** |
| Brock Purdy | QB | 424 | **124** |
| Justin Jefferson | WR | 322 | **112** |
| Justin Herbert | QB | 380 | 80 |
| Jared Goff | QB | 371 | 71 |
| Ladd McConkey | WR | 266 | 56 |
| Quinshon Judkins | RB | 257 | 52 |
| Blake Cashman | IDP | 392 | **37** |
| Tucker Kraft | TE | 189 | **34** |
| Jordyn Brooks | IDP | 387 | 32 |
| Bolton · Warner · Bigsby · Johnson · Andrews | — | 149–355 | **0** |

Two rows carry the whole lesson. **Cashman projects 392 — the second-highest number on the roster — and is worth 37 in a trade**, because an equivalent linebacker is free on the wire. **Kraft projects 189, the lowest starter on the roster, and is worth 34**, because tight end has no cheap replacement. Scarcity sets value, production doesn't.

### Three rules that follow

**Never trade *for* an IDP, and never expect real value for one.** A three-down linebacker costs $0–2 on waivers all season. Anyone offering a linebacker as a centrepiece is offering nothing; anyone asking for one should get it thrown in free to close a deal.

**Every bench player is worth exactly zero.** All five bench spots tested at **+0 lineup change** when dropped. This is the single most exploitable fact in the league.

**Therefore: always be the side consolidating.** A 2-for-1 or 3-for-1 that upgrades a starter costs David nothing real, because the players leaving don't play and the roster spots refill from a rich wire. In a 12-team league depth is insurance; in an 8-team league it's dead weight. **Give up quantity for quality every time it's offered, and propose it when it isn't.**

## The ESPN arbitrage applies to trades — but it expires

The room evaluates players by **ESPN rank** (see `live-draft-playbook.md`). ESPN under-ranks quarterbacks by an average of 9.5 spots and over-ranks RB, WR and TE. That gap is tradeable in both directions:

**Buy** — players ESPN buries: Purdy (their 33, truly 7), Dak (26/8), Nix (27/9), Lawrence (25/10), Burrow (16/4), Maye (10/2).

**Sell** — players ESPN inflates: McBride (their 21, truly 32), Bijan (5/14), Chase (6/15), Smith-Njigba (8/17), Gibbs (4/12), London (20/28).

**The window closes around week 6.** Preseason, a ranking is the only anchor anyone has. Once six games of real scoring exist, a quarterback putting up 25 a week is undeniable and the discount evaporates. **Front-load buy-side trades into weeks 1–5** — that is when a 424-point quarterback can be had for a receiver the room rates higher.

**The complication worth understanding:** the same bias that lets David buy QBs cheap also means he can't flip them at full price later. Undervaluation cuts both ways. What creates a genuine sell market is **need, not ranking** — see below.

## The OP-slot squeeze is the sell market

Eight teams × three quarterback slots = **24 QBs needed against 32 NFL starters**. Every mock run produced two or three teams that drafted only two quarterbacks and filled the OP with a receiver, giving up roughly 150 points a season without noticing.

Those teams are the trade market. A spare quarterback is worth near zero on David's bench and 60–80 real points to them. **Identify them the night the draft ends** — the rosters page shows it immediately — and open the conversation early, before their OP slot underperforms enough that they start shopping aggressively and the price rises.

The reverse also holds: if David is ever down to three quarterbacks and one gets hurt, a wire QB at ~300 costs him about 75 points. Not fatal, but it argues for carrying a fourth when one is cheap.

## What this roster should be trying to do

The draft plan knowingly produces one soft starter: **RB2 at roughly 257, worth 52.** Every other starting slot is 112 or better. The obvious trade is **spare QB plus bench filler for an RB2 upgrade** — David gives up assets worth 71 and 0, and gains 40–80 real points.

Two structural reminders:

- The draft deliberately accepted bye clustering on the premise that talent is tradeable. **That only works if the trade market actually gets worked.** Post offers two weeks ahead of a cluster, not the Saturday before.
- No trade review means bye-fixing deals process instantly. This is a genuine advantage over most leagues and it should be used.

## Evaluating an incoming offer

```
VERDICT: accept / decline / counter

Value: you give [X real pts], you get [Y real pts] — net [+/− Z]
       (real = starting-lineup points lost, with wire replacement)

Why the numbers differ from the names: [the one place projection misleads —
usually an IDP, a bench body, or a positional-scarcity gap]

Counter: [specific names and why it clears]
```

Always state real value on both sides, never projections. An offer of "my 392-point linebacker for your 266-point receiver" looks like a steal and is a 19-point loss.

**Sleep on anything large.** There is no veto and no review here, so a bad trade is final the moment it's accepted. That cuts both ways — David has no protection from his own mistake either. Nothing above a ~100-point swing should be accepted inside five minutes.

**Reputation is a real constraint in a seven-partner market.** A trade that's obviously lopsided closes off a partner for the rest of the season and possibly next year. Winning a deal by 40 points that both sides feel good about is worth more than winning one by 120 that ends the relationship.

## Rebuilding these numbers

The value table is roster-specific — it's the marginal lineup contribution of *this* roster, and it shifts every time the roster changes. Recompute after the draft with real players, then again after any significant trade or injury. The method is stable: for each player, compare lineup output with him against lineup output with a replacement-level wire body in his slot. Replacement levels live in `scoring-values.md`.
