#!/usr/bin/env python3
"""Trade values, industry-standard core + three additions. Shows what each adds."""
import json,math,argparse,csv,os
exec(open('trade_chart.py').read().split('def main()')[0])
U="/mnt/user-data/uploads"
proj=json.load(open(f"{U}/projections-2026.json"))["players"]
# overall ECR + std from the rankings CSV (market's cross-positional ordering)
ecr={}
for r in csv.DictReader(open(f"{U}/FantasyPros_2026_Draft_ALL_Rankings__1_.csv")):
    try: ecr[r['PLAYER NAME'].strip()]=dict(rk=int(r['RK']),std=float(r['STD.DEV']),tier=int(r['TIERS']))
    except: pass
OBS={"QB":[1,2,3,4,5,7.5,11.5,13,14.5,18,20,25,29.5,32.5,34.5,36.5,39,42,50,53,55,58,61,66,70,76],
     "RB":[7,11,12.5,18,21,24.5,27.5,29,32,34.5,40,41.5,46,50,51,54,58,59,60,66,72,78,84,90,96,102],
     "WR":[6.5,10,15.5,17,19,21.5,23,25.5,30,38,47,50.5,52,53.5,56,58,64,65,67,72,77,82,87,92,97,102],
     "TE":[35,68,71,91,105,112,115.5,124,132,140,148,156,164,172]}
def obs_adp(p,r):
    a=OBS[p]; return a[r-1] if r<=len(a) else a[-1]+(r-len(a))*(7 if p=="QB" else 4)

for KEY in ("tx2025","empty"):
    cfg=LEAGUES[KEY]; by,wire,board=build(proj,cfg,400)
    B={x['name']:x for x in board}
    # ---- STEP 1 (industry standard): TRUE = curved VORP vs wire  [already in x['val']]
    # ---- ADDITION A: MARKET value. TX2025 = this room's own observed ADP.
    #                                 Empty = national overall ECR (best proxy available).
    vals=sorted([x['val'] for x in board],reverse=True)
    mkt={}
    for x in board:
        if KEY=="tx2025":
            key=obs_adp(x['pos'],x['rank'])            # where THIS room takes him
        else:
            key=ecr.get(x['name'],{}).get('rk',999)     # where the market takes him
        mkt[x['name']]=key
    order=sorted([n for n in mkt if mkt[n]<900],key=lambda n:mkt[n])
    for i,n in enumerate(order):
        B[n]['mkt']=vals[i] if i<len(vals) else 0.0
        B[n]['arb']=round(B[n]['val']-B[n]['mkt'],1)
    # ---- ADDITION B: risk band from expert disagreement
    for x in board:
        s=ecr.get(x['name'],{}).get('std',0)
        x['risk']=s
        x['lo']=round(x['val']*(1-min(.45,s/22)),1); x['hi']=round(x['val']*(1+min(.45,s/22)),1)
    print("="*76); print(f"{cfg['name']}"); print("="*76)
    live=[x for x in board if 'arb' in x and x['val']>8]
    live.sort(key=lambda x:-x['arb'])
    print("\nBUY — worth more in your scoring than this room pays")
    print(f"  {'player':<24}{'pos':<6}{'TRUE':>7}{'MKT':>7}{'ARB':>7}{'risk':>7}")
    for x in live[:8]: print(f"  {x['name']:<24}{x['pos']}{x['rank']:<4}{x['val']:>7.1f}{x['mkt']:>7.1f}{x['arb']:>+7.1f}{x['risk']:>7.1f}")
    print("\nSELL — this room pays more than he's worth to you")
    for x in live[-8:][::-1]: print(f"  {x['name']:<24}{x['pos']}{x['rank']:<4}{x['val']:>7.1f}{x['mkt']:>7.1f}{x['arb']:>+7.1f}{x['risk']:>7.1f}")
    hi=sorted([x for x in board if x['val']>25 and x['risk']>0],key=lambda x:-x['risk'])[:5]
    lo=sorted([x for x in board if x['val']>25 and x['risk']>0],key=lambda x:x['risk'])[:5]
    print("\nRISK BANDS (value +/- expert disagreement)")
    print("  widest:  " + " | ".join(f"{x['name']} {x['lo']}-{x['hi']}" for x in hi[:3]))
    print("  tightest:" + " | ".join(f"{x['name']} {x['lo']}-{x['hi']}" for x in lo[:3]))
    print()
