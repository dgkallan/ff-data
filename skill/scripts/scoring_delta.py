import json,math
exec(open('trade_chart.py').read().split('def main()')[0])
proj=json.load(open("/mnt/user-data/uploads/projections-2026.json"))["players"]
def industry(pos,s):  # what a public chart uses: generic full PPR
    return s.get("points_ppr", s.get("points",0))
for KEY in ("tx2025","empty"):
    cfg=LEAGUES[KEY]
    custom=dict(cfg); custom["score"]=cfg["score"]
    gen=dict(cfg); gen["score"]=industry
    byC,wC,bC=build(proj,custom,400); byG,wG,bG=build(proj,gen,400)
    C={x['name']:x for x in bC}; Gn={x['name']:x for x in bG}
    for i,x in enumerate(sorted(bC,key=lambda y:-y['val']),1): C[x['name']]['ov']=i
    for i,x in enumerate(sorted(bG,key=lambda y:-y['val']),1): Gn[x['name']]['ov']=i
    both=[n for n in C if n in Gn and (C[n]['val']>5 or Gn[n]['val']>5)]
    mv=sorted(both,key=lambda n:-(Gn[n]['ov']-C[n]['ov']))
    print("="*74); print(f"{cfg['name']}  —  custom scoring vs generic PPR"); print("="*74)
    print(f"\n{'player':<24}{'pos':<6}{'generic rk':>11}{'custom rk':>11}{'move':>8}{'val Δ':>8}")
    print("  RISERS (a public chart undervalues these for you)")
    for n in mv[:9]:
        d=Gn[n]['ov']-C[n]['ov']
        print(f"  {n:<22}{C[n]['pos']:<6}{Gn[n]['ov']:>11}{C[n]['ov']:>11}{d:>+8}{C[n]['val']-Gn[n]['val']:>+8.1f}")
    print("  FALLERS (a public chart overvalues these for you)")
    for n in mv[-6:][::-1]:
        d=Gn[n]['ov']-C[n]['ov']
        print(f"  {n:<22}{C[n]['pos']:<6}{Gn[n]['ov']:>11}{C[n]['ov']:>11}{d:>+8}{C[n]['val']-Gn[n]['val']:>+8.1f}")
    moves=[abs(Gn[n]['ov']-C[n]['ov']) for n in both]
    big=sum(1 for m in moves if m>=10)
    print(f"\n  {len(both)} players compared | mean rank move {sum(moves)/len(moves):.1f} | "
          f"{big} move 10+ spots ({big/len(both)*100:.0f}%)")
    pos={}
    for n in both:
        p=C[n]['pos']; pos.setdefault(p,[]).append(C[n]['val']-Gn[n]['val'])
    print("  avg value change by position: " + "  ".join(f"{p} {sum(v)/len(v):+.1f}" for p,v in sorted(pos.items(),key=lambda kv:-sum(kv[1])/len(kv[1]))))
    print()
