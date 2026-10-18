"""Compute non-overlapping Dorling cartogram positions for the state spending map (m1).
Usage: python tools/build_dorling_positions.py . 2000 1530
Circle area = population (largest state = 2000 px^2); circles start at each state label point
and are pushed apart until none overlap, with a weak pull back to their real location.
Writes geo/malaysia_dorling_positions.csv."""
import csv, math, sys
ROOT=sys.argv[1]; AREA_MAX=float(sys.argv[2]) if len(sys.argv)>2 else 3200; K=float(sys.argv[3]) if len(sys.argv)>3 else 1570
pop={r['state']:int(r['population']) for r in csv.DictReader(open(f'{ROOT}/data/mnha_state_2024.csv'))}
pts={r['state']:(float(r['longitude']),float(r['latitude'])) for r in csv.DictReader(open(f'{ROOT}/geo/malaysia_state_label_points.csv'))}
pmax=max(pop.values())
merc=lambda la: math.log(math.tan(math.pi/4+math.radians(la)/2))
inv=lambda y: math.degrees(2*math.atan(math.exp(y))-math.pi/2)
S={}
for s,(lo,la) in pts.items():
    x=math.radians(lo)*K; y=-merc(la)*K
    r=math.sqrt(pop[s]/pmax*AREA_MAX/math.pi)
    S[s]=dict(x=x,y=y,x0=x,y0=y,r=r)
PAD=2.5
WEST={'Perlis','Kedah','Pulau Pinang','Perak','Selangor','W.P. Putrajaya','Negeri Sembilan','Melaka','Sarawak'}
for it in range(3000):
    for a in S:
        for b in S:
            if a>=b: continue
            A,B=S[a],S[b]; dx=B['x']-A['x']; dy=B['y']-A['y']; d=math.hypot(dx,dy) or 1e-6
            need=A['r']+B['r']+PAD
            if d<need:
                push=(need-d)/2; ux,uy=dx/d,dy/d
                wa=B['r']**2/(A['r']**2+B['r']**2); wb=1-wa   # small circles move more
                A['x']-=ux*push*2*wa; A['y']-=uy*push*2*wa
                B['x']+=ux*push*2*wb; B['y']+=uy*push*2*wb
    for s in (S if it<2700 else []):
        A=S[s]; A['x']+= (A['x0']-A['x'])*0.02; A['y']+=(A['y0']-A['y'])*0.02
# check overlaps
ov=[(a,b) for a in S for b in S if a<b and math.hypot(S[a]['x']-S[b]['x'],S[a]['y']-S[b]['y'])<S[a]['r']+S[b]['r']]
print('overlaps',ov, file=sys.stderr)

# label placement in screen pixels relative to circle centre: (dx, dy, align, leader)
LBL={'Perak':(0,0,'center',0),'Selangor':(0,0,'center',0),'Johor':(0,0,'center',0),
     'Melaka':(0,'B','center',0),'Negeri Sembilan':('L',8,'right',0),
     'W.P. Putrajaya':(-38,10,'right',1)}
w=csv.writer(open(f'{ROOT}/geo/malaysia_dorling_positions.csv','w',newline=''))
w.writerow(['state','longitude','latitude','radius_px','moved_px','label_longitude','label_latitude','label_align','leader'])
for s,A in S.items():
    west = s in WEST
    dx,dy,al,ld = LBL.get(s, ('L' if west else 'R',0,'right' if west else 'left',0))
    if dx=='L': dx=-(A['r']+4)
    if dx=='R': dx=A['r']+4
    if dy=='B': dy=A['r']+9
    lx=A['x']+dx; ly=A['y']+dy
    w.writerow([s, round(math.degrees(A['x']/K),4), round(inv(-A['y']/K),4), round(A['r'],1), round(math.hypot(A['x']-A['x0'],A['y']-A['y0']),1), round(math.degrees(lx/K),4), round(inv(-ly/K),4), al, ld])
    print(s, round(A['r'],1), round(math.hypot(A['x']-A['x0'],A['y']-A['y0']),1), file=sys.stderr)
