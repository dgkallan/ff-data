import random, statistics
from collections import defaultdict

# ---------- PLAYER POOL ----------
# Real ESPN projections in Empty Stadiums scoring (Aug 21 2026) + modelled tail.
real=[("Josh Allen","QB",495.6,1),("Jayden Daniels","QB",435.2,2),("Lamar Jackson","QB",448.2,3),
("Jahmyr Gibbs","RB",395.7,4),("Bijan Robinson","RB",386.5,5),("Ja'Marr Chase","WR",371.2,6),
("Puka Nacua","WR",393.0,7),("Jaxon Smith-Njigba","WR",362.7,8),("C. McCaffrey","RB",368.1,9),
("Drake Maye","QB",450.9,10),("Jalen Hurts","QB",433.6,11),("Jonathan Taylor","RB",351.4,12),
("Amon-Ra St. Brown","WR",354.5,13),("CeeDee Lamb","WR",322.2,14),("De'Von Achane","RB",321.4,15),
("Joe Burrow","QB",445.8,16),("Jaxson Dart","QB",407.1,17),("James Cook","RB",310.0,18),
("Justin Jefferson","WR",322.2,19),("Drake London","WR",293.1,20),("Trey McBride","TE",256.3,21),
("Ashton Jeanty","RB",302.7,22),("Rashee Rice","WR",290.0,23),("Nico Collins","WR",270.9,24),
("Trevor Lawrence","QB",407.7,25),("Dak Prescott","QB",420.7,26),("Bo Nix","QB",417.4,27),
("Jeremiyah Love","RB",300.0,28),("Saquon Barkley","RB",299.9,29),("Derrick Henry","RB",308.4,30),
("Chase Brown","RB",290.3,31),("Brock Bowers","TE",254.7,32),("Brock Purdy","QB",424.0,33),
("Tyler Warren","TE",221.4,40),("Colston Loveland","TE",216.5,45),("Sam LaPorta","TE",196.2,55),
("Harold Fannin","TE",195.9,60),("Kyle Pitts","TE",194.5,58),("Tucker Kraft","TE",189.2,62),
("Blake Cashman","IDP",392.1,150),("Jordyn Brooks","IDP",387.2,148),("Nick Bolton","IDP",354.9,155),
("Fred Warner","IDP",350.5,145),("Jack Campbell","IDP",346.7,152),("F. Oluokun","IDP",345.4,158),
("Cedric Gray","IDP",342.1,160),("C. Schwesinger","IDP",335.0,156),("N. Emmanwori","IDP",315.9,165),
("Maxx Crosby","IDP",263.7,140),("Myles Garrett","IDP",232.3,138)]

pool=[]
for n,p,pts,er in real: pool.append({"n":n,"pos":p,"pts":pts,"espn":er})

# modelled tail — decay curves anchored to the real data
tail={"QB":(12,26,400,320),"RB":(12,46,286,120),"WR":(10,54,266,120),"TE":(10,20,185,120),"IDP":(12,30,310,230)}
espn_start={"QB":34,"RB":34,"WR":34,"TE":64,"IDP":170}
for pos,(i0,i1,hi,lo) in tail.items():
    k=i1-i0
    for j in range(k):
        pts=hi-(hi-lo)*(j/max(1,k-1))**0.85
        pool.append({"n":f"{pos}{i0+j+1}","pos":pos,"pts":round(pts,1),
                     "espn":espn_start[pos]+j*(2 if pos in("RB","WR") else 3)})
# de-dup espn ranks
pool.sort(key=lambda x:x["espn"])
for i,p in enumerate(pool): p["espn"]=i+1

START={"QB":2,"RB":2,"WR":3,"TE":1,"IDP":2}   # OP handled separately
MAXP={"QB":4,"RB":4,"WR":6,"TE":2,"IDP":4}

MANAGERS=[("Quintero",{"RB":-14,"WR":-2,"QB":+10}),
          ("Waymire", {"WR":-10,"RB":-4,"QB":+40}),
          ("Thompson",{"QB":-14,"WR":-2}),
          ("Rice",    {"QB":-8,"RB":-6}),
          ("Minnie",  {"QB":-12,"WR":-4}),
          ("Weaver",  {"QB":-10,"WR":-6}),
          ("Firestone",{"QB":-10,"WR":-6})]

def cnt(r,pos): return sum(1 for x in r if x["pos"]==pos)

def needs_starter(r,pos):
    if pos=="IDP": return cnt(r,"IDP")<2
    return cnt(r,pos)<START[pos]

def cpu(r,rd,bias,avail):
    best=None;bs=1e9
    for p in avail:
        if cnt(r,p["pos"])>=MAXP[p["pos"]]: continue
        if p["pos"]=="IDP" and rd<13: continue          # verified: IDP goes rds 13-16
        s=p["espn"]+bias.get(p["pos"],0)+random.gauss(0,4)
        if needs_starter(r,p["pos"]): s-=25             # starters before depth
        elif rd<=9: s+=30
        if s<bs: bs=s;best=p
    return best or avail[0]

def lineup(r):
    by=defaultdict(list)
    for p in r: by[p["pos"]].append(p["pts"])
    for k in by: by[k].sort(reverse=True)
    tot=0;used=defaultdict(int)
    for pos,k in START.items():
        take=by[pos][:k]; tot+=sum(take); used[pos]=len(take)
    op=[]
    for pos in ("QB","RB","WR","TE"): op+=by[pos][used[pos]:]
    if op: tot+=max(op)
    return tot

def mypick(r,rd,strat,avail):
    def bestpts(cands):
        return max(cands,key=lambda p:p["pts"]) if cands else None
    ok=[p for p in avail if cnt(r,p["pos"])<MAXP[p["pos"]]]
    if rd<13: ok=[p for p in ok if p["pos"]!="IDP"] or ok
    if rd>=13:
        idp=[p for p in ok if p["pos"]=="IDP"]
        if idp and cnt(r,"IDP")<2: return bestpts(idp)
    forced=strat.get(rd)
    if forced:
        c=[p for p in ok if p["pos"]==forced]
        if c: return bestpts(c)
    need=[p for p in ok if needs_starter(r,p["pos"]) and p["pos"]!="IDP"]
    return bestpts(need or ok)

STRATS={
 "A QB at 1.02":        {1:"QB"},
 "B Elite RB at 1.02":  {1:"RB"},
 "C Elite WR at 1.02":  {1:"WR"},
 "D RB then QB-QB":     {1:"RB",2:"QB",3:"QB"},
 "E WR then QB-QB":     {1:"WR",2:"QB",3:"QB"},
 "F RB-RB start":       {1:"RB",2:"RB"},
 "G WR-WR start":       {1:"WR",2:"WR"},
 "H Zero-QB thru rd4":  {1:"RB",2:"WR",3:"WR",4:"RB",5:"QB",6:"QB"},
 "I Pure best-pts":     {},
 "J QB-QB start":       {1:"QB",2:"QB"},
}

def run(seed,strat):
    random.seed(seed)
    mans=MANAGERS[:]; random.shuffle(mans)
    seats=[None]*8; seats[1]="ME"
    it=iter(mans)
    for i in range(8):
        if seats[i] is None: seats[i]=next(it)
    avail=sorted([dict(p) for p in pool],key=lambda x:x["espn"])
    rost={i:[] for i in range(8)}
    for rd in range(1,17):
        seq=range(8) if rd%2==1 else reversed(range(8))
        for t in seq:
            if not avail: break
            if seats[t]=="ME": p=mypick(rost[t],rd,strat,avail)
            else: p=cpu(rost[t],rd,seats[t][1],avail)
            avail.remove(p); rost[t].append(p)
    return lineup(rost[1]),[lineup(rost[i]) for i in range(8)]


print(f"{'STRATEGY':<22}{'AVG PTS':>9}{'MARGIN':>9}{'MIN MRG':>9}")
print("-"*50)
res={}
for name,st in STRATS.items():
    tots=[];margins=[]
    for seed in range(20):
        me,alls=run(seed,st)
        rivals=[v for i,v in enumerate(alls) if i!=1]
        tots.append(me); margins.append(me-max(rivals))
    res[name]=(statistics.mean(tots),statistics.mean(margins),min(margins))
for name,(a,m,mn) in sorted(res.items(),key=lambda x:-x[1][1]):
    print(f"{name:<22}{a:>9.0f}{m:>9.0f}{mn:>9.0f}")
print()
base=res["A QB at 1.02"][1]
print("vs. taking a QB at 1.02:")
for name,(a,m,mn) in sorted(res.items(),key=lambda x:-x[1][1]):
    if name!="A QB at 1.02":
        print(f"  {name:<22}{m-base:+7.0f} pts")
