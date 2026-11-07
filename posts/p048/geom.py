import json
from shapely.geometry import Polygon, Point, LineString
from shapely.ops import unary_union
g=json.load(open('geo_in.json'))
pawls=[Polygon(p) for p in g['pawlSweep']]
pocket=unary_union([p.buffer(0.62,join_style=1) for p in pawls]+[Point(0,0).buffer(g["Rt"]+0.65,256)])
A=g['anchor']; S=g['seats']
spring=unary_union([LineString([A,s]).buffer(2.05,cap_style=2) for s in S]+[Point(A).buffer(2.05,64)])
pocket=unary_union([pocket,spring]).buffer(0.25).buffer(-0.25)
head=unary_union([Point(0,0).buffer(26.0,256), Polygon([(-13.5,-14),(13.5,-14),(6.6,-58),(-6.6,-58)])]).buffer(3.0).buffer(-3.0)
# cover-plate screw holes
screws=[(-18.5,-13.0),(18.5,-13.0)]
for s in screws: assert head.contains(Point(s).buffer(2.5)) and not pocket.intersects(Point(s).buffer(2.0)), s
assert head.buffer(-2.0).contains(pocket), 'wall too thin'
wall=head.exterior.distance(pocket); print('min wall mm',round(head.boundary.distance(pocket.boundary),2))
out={'head':list(head.exterior.coords)[:-1],'pocket':list(pocket.exterior.coords)[:-1],'screws':screws}
json.dump(out,open('geom.json','w'))
print(len(out['head']),len(out['pocket']))
