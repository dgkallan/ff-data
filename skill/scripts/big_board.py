#!/usr/bin/env python3
"""TX2025 pre-draft big board, 1-200. Ranked by league-scored value over wire."""
import json,math,csv,os,argparse
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'trade_chart.py')).read().split('def main()')[0])
U="/mnt/user-data/uploads"
ap=argparse.ArgumentParser(); ap.add_argument('--n',type=int,default=200)
ap.add_argument('--proj',default=f"{U}/projections-2026.json"); a=ap.parse_args()
proj=json.load(open(a.proj))["players"]
cfg=LEAGUES["tx2025"]; by,wire,board=build(proj,cfg,400)
sp={}
for P in ("QB","RB","WR","TE"):
    try:
        for p in json.load(open(f"{U}/spread-2026-{P}.json"))["players"]:
            sp[p["player_name"]]={"bye":p.get("player_bye_week"),"std":float(p.get("rank_std") or 0),"tier":p.get("tier")}
    except FileNotFoundError: pass
OBS={"QB":[1,2,3,4,5,7.5,11.5,13,14.5,18,20,25,29.5,32.5,34.5,36.5,39,42,50,53,55,58,61,66,70,76],
     "RB":[7,11,12.5,18,21,24.5,27.5,29,32,34.5,40,41.5,46,50,51,54,58,59,60,66,72,78,84,90,96,102],
     "WR":[6.5,10,15.5,17,19,21.5,23,25.5,30,38,47,50.5,52,53.5,56,58,64,65,67,72,77,82,87,92,97,102],
     "TE":[35,68,71,91,105,112,115.5,124,132,140,148,156,164,172]}
def adp(p,r):
    t=OBS[p]; return t[r-1] if r<=len(t) else t[-1]+(r-len(t))*(7 if p=="QB" else 4)
for x in board:
    x['adp']=round(adp(x['pos'],x['rank']),1)
    s=sp.get(x['name'],{}); x['bye']=s.get('bye') or 0; x['std']=s.get('std') or 0
vals=sorted([x['val'] for x in board],reverse=True)
for k,x in enumerate(sorted(board,key=lambda y:y['adp'])):
    x['mkt']=vals[k] if k<len(vals) else 0.0; x['arb']=round(x['val']-x['mkt'],1)
top=sorted(board,key=lambda x:-x['val'])[:a.n]
out=top
lines=["# TX2025 Big Board — 1-%d"%a.n,"",
"Ranked by **value over the waiver wire in TX2025 scoring**, not generic PPR: 6-pt pass TD, −1 INT, +3 at 300 pass yds; **RB 0.5/reception (HALF PPR), WR and TE 1.0**; +3 at 100 rec yds, +3 more at 200. Wire replacement: QB31=%.0f RB48=%.0f WR66=%.0f TE23=%.0f."%(wire['QB'],wire['RB'],wire['WR'],wire['TE']),"",
"**Half-point RB is why this board looks unlike any public ranking.** Pass-catching backs lose 30-40 pts against a full-PPR chart — Bijan −40, McCaffrey −39, Gibbs −36, Achane −33. If your leaguemates draft off CBS rankings built on full PPR, they will overpay for receiving backs. Let them, and take the volume runners they leave.","",
"**ADP** = where *this room* takes him (2024+2025 observed, 240 picks). **ARB** = value minus what the room pays; positive is a bargain. **σ** = expert disagreement (high = boom/bust). Ranking is cross-positional, so no tier column — use the positional rank (QB14, RB8) for within-position tiers.","",
"Do not draft straight down this list — it is need-blind, and it will happily tell you to take five quarterbacks in a row through tier 8. Use it with the round plan for slot 9: **WR at 9 · skill at 16 · QB at 33 · RB at 40 · skill at 57 · QB at 64 · RB at 81 · TE at 88.**","",
"| # | Player | Pos | Pts | Val | ADP | ARB | σ | Bye |","|---|---|---|---|---|---|---|---|---|"]
for i,x in enumerate(out,1):
    ar=f"**{x['arb']:+.0f}**" if abs(x['arb'])>=8 else f"{x['arb']:+.0f}"
    lines.append(f"| {i} | {x['name']} | {x['pos']}{x['rank']} | {x['pts']:.0f} | {x['val']:.1f} | {x['adp']:.0f} | {ar} | {x['std']:.1f} | {x['bye']} |")
open('/mnt/user-data/outputs/tx2025-big-board.md','w').write("\n".join(lines))
print("wrote %d players"%len(out))
print("\nTOP 30:")
print(f"{'#':<4}{'player':<24}{'pos':<6}{'val':>6}{'adp':>6}{'arb':>7}{'sd':>5}{'bye':>5}")
for i,x in enumerate(out[:30],1):
    print(f"{i:<4}{x['name']:<24}{x['pos']+str(x['rank']):<6}{x['val']:>6.1f}{x['adp']:>6.0f}{x['arb']:>+7.1f}{x['std']:>5.1f}{x['bye']:>5}")
