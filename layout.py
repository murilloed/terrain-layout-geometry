"""Planar geometry and deterministic greedy layout search; coordinates in meters."""
import math
from shapely.geometry import Polygon, box

def finite_nonnegative(value,name):
    if not math.isfinite(value) or value<0:raise ValueError(name+' must be finite and nonnegative')

def feasible_region(coords,setback):
    finite_nonnegative(setback,'setback');terrain=Polygon(coords)
    if not terrain.is_valid or terrain.is_empty or terrain.area<=0:raise ValueError('Valid polygon required')
    return terrain,terrain.buffer(-setback,join_style=2)

def generate(coords,setback=4,width=12,depth=8,gap=3,step=4,max_coverage=.45,max_buildings=12):
    for value,name in [(gap,'gap'),(max_coverage,'coverage')]:finite_nonnegative(value,name)
    if max_coverage>1:raise ValueError('Coverage must be at most 1')
    for value in [width,depth,step]:
        if not math.isfinite(value) or value<=0:raise ValueError('Positive dimensions and step required')
    if not isinstance(max_buildings,int) or max_buildings<0:raise ValueError('Invalid building count')
    terrain,region=feasible_region(coords,setback)
    if region.is_empty:return {'terrain':terrain,'region':region,'layouts':[]}
    minx,miny,maxx,maxy=region.bounds
    nx=int((maxx-minx)/step)+1;ny=int((maxy-miny)/step)+1
    if nx*ny>100000:raise ValueError('Search grid too large; increase step')
    candidates=[]
    for w,d in sorted(set([(width,depth),(depth,width)])):
        for ix in range(nx):
            for iy in range(ny):
                x=minx+ix*step;y=miny+iy*step;rect=box(x,y,x+w,y+d)
                if region.covers(rect):candidates.append(rect)
    layouts=[]
    orders={'south_first':lambda r:(r.bounds[1],r.bounds[0],r.bounds[2]),'west_first':lambda r:(r.bounds[0],r.bounds[1],r.bounds[3]),'center_first':lambda r:(r.centroid.distance(region.centroid),r.bounds)}
    for name,key in orders.items():
        placed=[]
        for rect in sorted(candidates,key=key):
            if len(placed)>=max_buildings:break
            if (len(placed)+1)*width*depth>terrain.area*max_coverage+1e-9:continue
            if all(rect.intersection(other).area<=1e-9 and rect.distance(other)+1e-9>=gap for other in placed):placed.append(rect)
        occupied=sum(r.area for r in placed)
        layouts.append({'name':name,'buildings':placed,'count':len(placed),'occupied_area':occupied,'coverage':occupied/terrain.area,'mean_center_distance':sum(r.centroid.distance(region.centroid) for r in placed)/len(placed) if placed else 0})
    return {'terrain':terrain,'region':region,'layouts':layouts}
