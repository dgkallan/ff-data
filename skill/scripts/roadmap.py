import json,math,numpy as np
from collections import Counter
exec(open('trade_chart.py').read().split('def main()')[0])
proj=json.load(open("/mnt/user-data/uploads/projections-2026.json"))["players"]
cfg=LEAGUES["tx2025"]; by,wire,board=build(proj,cfg,400)
OBS={"QB":[1,2,3,4,5,7.5,11.5,13,14.5,18,20,25,29.5,32.5,34.5,36.5,39,42,50,53,55,58,61,66,70,76],
     "RB":[7,11,12.5,18,21,24.5,27.5,29,32,34.5,40,41.5,46,50,51,54,58,59,60,66,72,78,84,90,96,102],
     "WR":[6.5,10,15.5,17,19,21.5,23,25.5,30,38,47,50.5,52,53.5,56,58,64,65,67,72,77,82,87,92,97,102],
     "TE":[35,68,71,91,105,112,115.5,124,132,140,148,156,164,172]}
def adp(p,r):
    a=OBS[p]; return a[r-1] if r<=len(a) else a[-1]+(r-len(a))*(7 if p=="QB" else 4)
for x in board: x['adp']=adp(x['pos'],x['rank'])
vals=sorted([x['val'] for x in board],reverse=True)
order=sorted(board,key=lambda x:x['adp'])
for i,x in enumerate(order): x['mkt']=vals[i] if i<len(vals) else 0.0; x['arb']=x['val']-x['mkt']
PICKS=[r*12+(9 if r%2==0 else 4) for r in range(14)]
PLAN={1:"SKILL",2:"SKILL",3:"QB",4:"RB",5:"SKILL",6:"QB",7:"RB",8:"TE",9:"ANY",10:"ANY",11:"ANY",12:"ANY",13:"ANY",14:"ANY"}
print("DRAFT ROADMAP — slot 9, arbitrage at each pick")
print("(ARB = worth-to-you minus what this room pays. + = bargain)\n")
print(f"{'Rd':<4}{'Pick':<6}{'plan':<7}{'best ARB likely available (adp within ~6 of pick)':<52}")
for r,pk in enumerate(PICKS,1):
    live=[x for x in board if pk-2 <= x['adp'] <= pk+14 and x['val']>5]
    live.sort(key=lambda x:-x['arb'])
    s=" | ".join(f"{x['name'].split()[-1]} {x['pos']}{x['rank']} {x['arb']:+.0f}" for x in live[:3])
    print(f"R{r:<3}{pk:<6}{PLAN[r]:<7}{s}")
print("\n\nWHERE THE ROOM'S MISPRICING CONCENTRATES, by round")
for lo,hi,lbl in ((1,24,"rounds 1-2"),(25,48,"rounds 3-4"),(49,84,"rounds 5-7"),(85,168,"rounds 8-14")):
    g=[x for x in board if lo<=x['adp']<=hi and x['val']>5]
    if not g: continue
    pos={}
    for p in ("QB","RB","WR","TE"):
        q=[x['arb'] for x in g if x['pos']==p]
        if q: pos[p]=sum(q)/len(q)
    s="  ".join(f"{p} {v:+.1f}" for p,v in sorted(pos.items(),key=lambda kv:-kv[1]))
    print(f"  {lbl:<12}{s}")
