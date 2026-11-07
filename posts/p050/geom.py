# p050 geometry: symmetric 24-tooth gear, rocking double-nose pawl (nominal pose), head + pocket. Units mm.
import json, math
from shapely.geometry import Polygon, Point, LineString
from shapely.ops import unary_union
from shapely import affinity
N=24; Rr=12.0; Rt=14.0; PIV=(0.0,-19.0); DELTA=0.155; SEL=(0.0,-28.6)
def pol(r,a): return (r*math.cos(a), r*math.sin(a))
# right half (nose B at 315 deg) built in its ENGAGED pose (pawl rotated +DELTA)
aN=math.radians(-45); uin=(-math.cos(aN),-math.sin(aN)); t=(-math.sin(aN),math.cos(aN))
def add(p,v,s): return (p[0]+v[0]*s,p[1]+v[1]*s)
tip=pol(12.45,aN)
tipL=add(tip,t,-0.22); tipR=add(tip,t,0.22)
base=add(tip,uin,-1.85)
cFar=add(base,t,1.22); cNear=add(base,t,-1.22)
pts=[]
# top edge from x~0 (angle -90) along r=14.55 to the near base corner
for i in range(0,25):
    a=math.radians(-91.5+ (math.degrees(math.atan2(cNear[1],cNear[0]))+91.5)*i/24); pts.append(pol(14.55,a))
pts+= [cNear, tipL, tipR, cFar]
aF=math.atan2(cFar[1],cFar[0])
for i in range(1,7):
    a=aF+math.radians(1.2*i); pts.append(pol(14.35,a))
aE=aF+math.radians(7.2)
pts.append(pol(17.6,aE+math.radians(1.0)))
# outer/bottom edge: quadratic bezier back to below the pivot boss
P0=pol(17.6,aE+math.radians(1.0)); C=(9.5,-22.6); P2=(-0.5,-22.4)
for i in range(1,21):
    u=i/20; pts.append(((1-u)**2*P0[0]+2*(1-u)*u*C[0]+u*u*P2[0], (1-u)**2*P0[1]+2*(1-u)*u*C[1]+u*u*P2[1]))
half=Polygon(pts).buffer(0)
half=affinity.rotate(half,-DELTA,origin=PIV,use_radians=True)  # to nominal
from shapely.geometry import box
half=half.intersection(box(0,-40,40,0))
full=unary_union([half, affinity.scale(half,-1,1,origin=(0,0)), Point(PIV).buffer(2.9,64)]).buffer(0.15).buffer(-0.15)
assert full.geom_type=='Polygon', full.geom_type
ring=list(full.exterior.coords)[:-1]
# orient CCW
if Polygon(ring).exterior.is_ccw is False: ring=ring[::-1]
gear=Point(0,0).buffer(Rt+0.65,256)
sweep=[affinity.rotate(full,d,origin=PIV,use_radians=True) for d in [ -DELTA-0.03+i*(2*DELTA+0.06)/24 for i in range(25)]]
pocket=unary_union([s.buffer(0.55,join_style=1) for s in sweep]+[gear, Point(SEL).buffer(4.6,96), LineString([SEL,(0,-21)]).buffer(2.6)]).buffer(0.3).buffer(-0.3)
head=unary_union([Point(0,0).buffer(26.0,256), Polygon([(-13.5,-14),(13.5,-14),(6.6,-58),(-6.6,-58)])]).buffer(3.0).buffer(-3.0)
screws=[(-19.5,10.0),(19.5,10.0)]
for s in screws: assert head.contains(Point(s).buffer(2.5)) and not pocket.intersects(Point(s).buffer(2.0)), s
print('min wall mm', round(head.boundary.distance(pocket.boundary),2), 'pawl area', round(full.area,1))
assert head.buffer(-1.5).contains(pocket), 'wall too thin'
json.dump({'pawl':ring,'head':list(head.exterior.coords)[:-1],'pocket':list(pocket.exterior.coords)[:-1],'screws':screws,
           'N':N,'Rr':Rr,'Rt':Rt,'pivot':PIV,'delta':DELTA,'sel':SEL},open('geom.json','w'))
print(len(ring),'pawl pts')
