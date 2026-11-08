import kin, sys
from shapely import affinity
fr,ev,_=kin.simulate(240)
ts=[float(x) for x in sys.argv[1].split(',')]; out=[]
for j,tt in enumerate(ts):
    f=fr[int(tt*240)]; g=kin.gear_at(f['ag']); p=affinity.rotate(kin.PEND,f['phi'],origin=tuple(kin.P),use_radians=True)
    def path(poly,col): return '<path d="M'+' L'.join(f'{x*20:.1f},{-y*20:.1f}' for x,y in poly.exterior.coords)+f'Z" fill="{col}"/>'
    out.append(f'<g transform="translate({j*600+200},-100)">'+path(g,'#999')+path(p,'orange')+f'<text x="-150" y="-300" font-size="30">t={tt} phi={f["phi"]/kin.D:.1f} ag={f["ag"]/kin.D:.1f}</text></g>')
open(sys.argv[2],'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{600*len(ts)}" height="900" viewBox="0 -400 {600*len(ts)} 900"><rect x="0" y="-400" width="100%" height="900" fill="white"/>'+''.join(out)+'</svg>')
