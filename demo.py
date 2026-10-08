import argparse,json,csv
from pathlib import Path
from shapely.geometry import mapping
from layout import generate

def svg(result,chosen):
    terrain=result['terrain'];region=result['region'];minx,miny,maxx,maxy=terrain.bounds
    def path(poly,color):
        pieces=[]
        polygons=list(poly.geoms) if poly.geom_type=='MultiPolygon' else [poly]
        for p in polygons:
            if p.is_empty:continue
            rings=[p.exterior,*p.interiors]
            d=' '.join('M '+' L '.join(f'{x},{y}' for x,y in ring.coords)+' Z' for ring in rings)
            pieces.append(f'<path d="{d}" fill="{color}" fill-rule="evenodd" stroke="#73c4d3" stroke-width=".3"/>')
        return ''.join(pieces)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{minx-4} {miny-4} {maxx-minx+8} {maxy-miny+8}"><rect x="{minx-4}" y="{miny-4}" width="{maxx-minx+8}" height="{maxy-miny+8}" fill="#0b1c33"/>'+path(terrain,'#294058')+path(region,'#143c3f')+''.join(path(b,'#efb66b') for b in chosen['buildings'])+'</svg>'

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',default='output');p.add_argument('--setback',type=float,default=4);a=p.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
    coords=[(0,0),(65,0),(65,25),(48,25),(48,52),(0,52)]
    result=generate(coords,setback=a.setback);best=max(result['layouts'],key=lambda x:(x['count'],-x['mean_center_distance'])) if result['layouts'] else {'name':'empty','buildings':[],'count':0}
    metrics=[{k:v for k,v in row.items() if k!='buildings'} for row in result['layouts']]
    report={'synthetic':True,'trained_model':False,'coordinate_system':'local planar meters, synthetic site','parameters':{'setback_m':a.setback,'building_size_m':[12,8],'gap_m':3,'grid_step_m':4,'max_coverage':.45,'max_buildings':12},'terrain_area_m2':result['terrain'].area,'feasible_area_m2':result['region'].area,'alternatives':metrics,'selected':best['name'],'limitation':'Greedy grid search; not a global optimum or legal/engineering approval. Uniform setbacks only. No roads, terrain elevation, fire access or BIM export.'}
    (out/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    features=[{'type':'Feature','properties':{'kind':'terrain'},'geometry':mapping(result['terrain'])},{'type':'Feature','properties':{'kind':'feasible'},'geometry':mapping(result['region'])}]+[{'type':'Feature','properties':{'kind':'building','index':i+1},'geometry':mapping(b)} for i,b in enumerate(best['buildings'])]
    (out/'layout.geojson').write_text(json.dumps({'type':'FeatureCollection','features':features}),encoding='utf-8')
    (out/'layout.svg').write_text(svg(result,best),encoding='utf-8')
    with (out/'alternatives.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=list(metrics[0]) if metrics else ['name']);writer.writeheader();writer.writerows(metrics)
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
