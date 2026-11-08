# p051 freehub geometry (units mm, driver frame, gear axis +Z, seen from the drive side).
# Ring: 24 internal ratchet teeth (tips Ri, roots Ro). Driver: 2 pawls at 90 and 270 deg, pivot at the heel, tip leads clockwise.
import json, math
from shapely.geometry import Polygon, Point, box
from shapely.ops import unary_union
from shapely import affinity
N=24; Ri=15.0; Ro=16.6; RD=14.35; PIV=(-3.1,12.85); LIM=0.36
def pol(r,a): return (r*math.cos(a), r*math.sin(a))
# pawl at the top, nominal (retracted, db=0): top edge on r=14.45 from heel to tip, tip face radial, bottom on r=12.45
aH=math.atan2(PIV[1],PIV[0]); aT=math.radians(90-12.0)   # tip angle (to +x of top)
pts=[]
for i in range(0,21): a=aH+(aT-aH)*i/20; pts.append(pol(13.75+0.7*(i/20)**1.3,a))
pts.append(pol(13.4,aT-0.004)); pts.append(pol(12.45,aT+0.035))
for i in range(1,16): a=(aT+0.03)+(aH-0.06-(aT+0.03))*i/15; pts.append(pol(12.45,a))
paw=unary_union([Polygon(pts).buffer(0), Point(PIV).buffer(1.25,48)]).buffer(0.12).buffer(-0.12)
paw=paw.buffer(-0.08,join_style=1).buffer(0.08,join_style=1)
ring=list(paw.exterior.coords)[:-1]
if not Polygon(ring).exterior.is_ccw: ring=ring[::-1]
# spring bore under the pawl (radial), centre angle
aS=math.radians(90-6.0); sb=[pol(10.4,aS-0.075),pol(10.4,aS+0.075),pol(13.6,aS+0.075),pol(13.6,aS-0.075)]
sweep=[affinity.rotate(paw,d,origin=PIV,use_radians=True) for d in [-0.03+i*(LIM+0.06)/20 for i in range(21)]]
pocket=unary_union([s.buffer(0.22,join_style=1) for s in sweep]+[Polygon(sb)]).buffer(0.2).buffer(-0.2)
pocketB=affinity.rotate(pocket,180,origin=(0,0))
body=Point(0,0).buffer(RD,256).difference(pocket).difference(pocketB).difference(Point(0,0).buffer(5.2,96))
assert body.geom_type=='Polygon', body.geom_type
body=body.buffer(0.05).buffer(-0.05)
tipLocal=[p for p in ring]; 
json.dump({'N':N,'Ri':Ri,'Ro':Ro,'RD':RD,'pivot':PIV,'lim':LIM,'pawl':ring,'body':list(body.exterior.coords)[:-1],
  'bodyHoles':[list(h.coords)[:-1] for h in body.interiors],'springAng':aS,'tipAng':aT},open('geom.json','w'))
print('pawl pts',len(ring),'area',round(paw.area,2),'body holes',len(body.interiors),'tip dist', round(math.dist(PIV,pol(14.45,aT)),2))
