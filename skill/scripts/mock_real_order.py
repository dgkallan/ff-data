import random
from collections import defaultdict

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

NAMES={"QB":["Caleb Williams","Kyler Murray","Justin Herbert","Jared Goff","C.J. Stroud","Baker Mayfield",
 "Michael Penix","J.J. McCarthy","Cam Ward","Justin Fields","Tua Tagovailoa","Geno Smith","Sam Darnold","Bryce Young"],
"RB":["Kenneth Walker","Omarion Hampton","Bucky Irving","Travis Etienne","Quinshon Judkins","D'Andre Swift",
 "Breece Hall","Cam Skattebo","Tony Pollard","Chuba Hubbard","Rico Dowdle","J.K. Dobbins","Jordan Mason",
 "Rachaad White","Tyrone Tracy","Isiah Pacheco","Braelon Allen","Trey Benson","Tank Bigsby","Zach Charbonnet",
 "Kaleb Johnson","Jaylen Wright","Ray Davis","Blake Corum","Roschon Johnson","Dylan Sampson","Bhayshul Tuten",
 "Woody Marks","Devin Neal","Jarquez Hunter","Kyle Monangai","Trevor Etienne","Damien Martinez","DJ Giddens"],
"WR":["Ladd McConkey","Malik Nabers","Brian Thomas Jr.","Tetairoa McMillan","Garrett Wilson","Marvin Harrison Jr.",
 "Tee Higgins","DK Metcalf","Jaylen Waddle","Courtland Sutton","Zay Flowers","Jerry Jeudy","Chris Olave",
 "Jameson Williams","Rome Odunze","Travis Hunter","Xavier Worthy","Ricky Pearsall","Keon Coleman","Jayden Higgins",
 "Emeka Egbuka","Matthew Golden","Khalil Shakir","Josh Downs","Rashid Shaheed","Marvin Mims","Jauan Jennings",
 "Cooper Kupp","DeMario Douglas","Adonai Mitchell","Luther Burden","Kyle Williams","Jack Bech","Isaac TeSlaa",
 "Tory Horton","Elic Ayomanor","KaVontae Turpin","Pat Bryant","Tre Harris","Xavier Legette","Alec Pierce",
 "Michael Wilson","Quentin Johnston","Darius Slayton"],
"TE":["Dallas Goedert","George Kittle","Travis Kelce","Jake Ferguson","David Njoku","Evan Engram","Mark Andrews",
 "Isaiah Likely","Hunter Henry","Dalton Kincaid","Brenton Strange","Chig Okonkwo","Mason Taylor","Elijah Arroyo"],
"IDP":["Zack Baun","Bobby Wagner","Quay Walker","Devin White","Ernest Jones","Zaire Franklin","Bobby Okereke",
 "Dre Greenlaw","Jamien Sherwood","Trey Hendrickson","Micah Parsons","T.J. Watt","Will Anderson","Aidan Hutchinson",
 "Kyle Hamilton","Budda Baker","Antoine Winfield","Jessie Bates","Derwin James","Xavier McKinney"]}

pool=[{"n":n,"pos":p,"pts":pts,"espn":er} for n,p,pts,er in real]
tail={"QB":(400,300),"RB":(286,110),"WR":(266,110),"TE":(185,115),"IDP":(310,215)}
espn_start={"QB":34,"RB":34,"WR":34,"TE":64,"IDP":170}
for pos,(hi,lo) in tail.items():
    ns=NAMES[pos]; k=len(ns)
    for j,nm in enumerate(ns):
        pts=hi-(hi-lo)*(j/max(1,k-1))**0.85
        pool.append({"n":nm,"pos":pos,"pts":round(pts,1),
                     "espn":espn_start[pos]+j*(2 if pos in("RB","WR") else 3)})
pool.sort(key=lambda x:x["espn"])
for i,p in enumerate(pool): p["espn"]=i+1

START={"QB":2,"RB":2,"WR":3,"TE":1,"IDP":2}
MAXP={"QB":4,"RB":4,"WR":6,"TE":2,"IDP":4}

SEATS=[("Rice",{"QB":-8,"RB":-6}),("ME",None),("Minnie",{"QB":-12,"WR":-4}),
       ("Weaver",{"QB":-10,"WR":-6}),("Waymire",{"WR":-10,"RB":-4,"QB":40}),
       ("Firestone",{"QB":-10,"WR":-6}),("Thompson",{"QB":-14,"WR":-2}),
       ("Quintero",{"RB":-14,"WR":-2,"QB":10})]

def cnt(r,pos): return sum(1 for x in r if x["pos"]==pos)
def needs(r,pos): return cnt(r,pos)<START[pos]

def cpu(r,rd,bias,avail):
    best=None;bs=1e9
    for p in avail:
        if cnt(r,p["pos"])>=MAXP[p["pos"]]: continue
        if p["pos"]=="IDP" and rd<13: continue
        s=p["espn"]+bias.get(p["pos"],0)+random.gauss(0,4)
        if needs(r,p["pos"]): s-=25
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

GAP={2:12,15:2,18:12,31:2,34:12,47:2,50:12,63:2,66:12,79:2,82:12,95:2,98:12,111:2,114:2,127:0}
MYPICKS=[2,15,18,31,34,47,50,63,66,79,82,95,98,111,114,127]

def mypick(r,rd,avail,pk):
    base=lineup(r)
    ok=[p for p in avail if cnt(r,p["pos"])<MAXP[p["pos"]]]
    if rd<13: ok=[p for p in ok if p["pos"]!="IDP"] or ok
    if rd>=13 and cnt(r,"IDP")<2:
        idp=[p for p in ok if p["pos"]=="IDP"]
        if idp: return max(idp,key=lambda p:p["pts"]),"IDP starter slot"
    cands=sorted(ok,key=lambda p:lineup(r+[p])-base,reverse=True)[:10]
    if lineup(r+[cands[0]])-base<=0:
        c2=sorted(ok,key=lambda p:p["pts"],reverse=True)[:6]
        return c2[0],"bench upside"
    gap=GAP.get(pk,12)
    byespn=sorted(avail,key=lambda x:x["espn"])
    best=None;bsc=-1e9;why=""
    for p in cands:
        gain=lineup(r+[p])-base
        rem=[q for q in byespn if q is not p]
        gone=set(id(q) for q in rem[:gap])
        surv=[q for q in rem if id(q) not in gone and cnt(r,q["pos"])<MAXP[q["pos"]]]
        r2=r+[p]; b2=lineup(r2)
        nxt=max((lineup(r2+[q])-b2 for q in surv[:60]),default=0)
        sc=gain+nxt
        if sc>bsc: bsc=sc;best=p;why=f"+{gain:.0f} now, best survivor next +{nxt:.0f}"
    return best,why

def run(seed,verbose=True):
    random.seed(seed)
    avail=sorted([dict(p) for p in pool],key=lambda x:x["espn"])
    rost={i:[] for i in range(8)}
    log=[]
    pk=0
    for rd in range(1,17):
        seq=range(8) if rd%2==1 else reversed(range(8))
        for t in seq:
            pk+=1
            if not avail: break
            if SEATS[t][0]=="ME":
                p,why=mypick(rost[t],rd,avail,pk)
                log.append((pk,rd,p,why))
            else:
                p=cpu(rost[t],rd,SEATS[t][1],avail)
            avail.remove(p); rost[t].append(p)
    return rost,log

def show(seed,n):
    rost,log=run(seed)
    print(f"\n{'='*72}\nMOCK {n}  (seed {seed})\n{'='*72}")
    for pk,rd,p,why in log:
        print(f" {pk:>3}.{rd:>2}  {p['n']:<24}{p['pos']:<5}{p['pts']:>6.0f}   ESPN {p['espn']:<4} {why}")
    r=rost[1]
    by=defaultdict(list)
    for p in r: by[p["pos"]].append(p)
    for k in by: by[k].sort(key=lambda x:-x["pts"])
    used=defaultdict(int); s=[]
    for pos,k in START.items():
        for p in by[pos][:k]: s.append((pos,p))
        used[pos]=min(k,len(by[pos]))
    op=[]
    for pos in ("QB","RB","WR","TE"): op+=by[pos][used[pos]:]
    opp=max(op,key=lambda x:x["pts"]) if op else None
    tot=sum(p["pts"] for _,p in s)+(opp["pts"] if opp else 0)
    print(f"\n  STARTERS ({tot:.0f} pts)")
    for pos,p in s: print(f"    {pos:<4} {p['n']:<24}{p['pts']:>6.0f}")
    if opp: print(f"    OP   {opp['n']:<24}{opp['pts']:>6.0f}")
    others=sorted([lineup(rost[i]) for i in range(8) if i!=1],reverse=True)
    print(f"  Rivals: {[round(x) for x in others]}   margin vs best rival: {tot-others[0]:+.0f}")
    return tot,others[0]

tots=[]
for i,sd in enumerate([11,22,33],1):
    tots.append(show(sd,i))
print(f"\nAvg my lineup {sum(t for t,_ in tots)/3:.0f} | avg best rival {sum(o for _,o in tots)/3:.0f}")
