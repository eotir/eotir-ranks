"""Independently check candidate data, source fidelity, pixels, SVG and review exports.

Usage: python tools/verify_catalog.py
Prerequisites: Python 3.10+, Pillow; completed catalog, composition and chart builds.
Read-only: no approval, publication, production writes or source edits occur.
"""
import base64
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from PIL import Image, ImageChops, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
NS = '{http://www.w3.org/2000/svg}'

def read(path):
    return json.loads((ROOT/path).read_text(encoding='utf-8-sig'))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def require(condition, message):
    if not condition:
        raise ValueError(message)

class ReviewParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links, self.payload = [], [], ''
        self.in_payload = False
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'tr' and 'data-id' in attrs:
            self.ids.append(attrs['data-id'])
        if tag == 'a' and attrs.get('href'):
            self.links.append(attrs['href'])
        if tag == 'img' and attrs.get('src'):
            self.links.append(attrs['src'])
        if tag == 'script' and attrs.get('id') == 'review-data':
            self.in_payload = True
    def handle_endtag(self, tag):
        if tag == 'script':
            self.in_payload = False
    def handle_data(self, data):
        if self.in_payload:
            self.payload += data

def polygon(x, y, width, height, cut):
    r,b=x+width-1,y+height-1
    return [(x+cut,y),(r-cut,y),(r,y+cut),(r,b-cut),(r-cut,b),(x+cut,b),(x,b-cut),(x,y+cut)]

def main():
    catalog=read('data/rank-catalog.json')
    composition=read('assets/composed/manifest.json')
    records=catalog['rank_records']; shared=catalog['shared_records']; blanks=catalog['blank_cells']
    require((len(records),len(blanks),len(shared))==(210,66,7),'Coverage must be 210 records / 66 blanks / 7 shared')
    military={b['id'] for b in catalog['branches'] if b['military']}
    require(sum(r['branch_id'] in military for r in records)==69,'Military coverage differs from 69')
    require(len({r['id'] for r in records+shared})==217,'Duplicate record identity')
    cells=[(r['branch_id'],r['grade']) for r in records+blanks]
    require(len(set(cells))==276,'Branch cells overlap or duplicate')
    require(all(r['status']=='CANDIDATE' and r['approval'] is None for r in records+shared),'Approval state changed')
    require(catalog['canonical'] is False and catalog['published'] is False,'Candidate canon/publication flags changed')
    for capture in catalog['source_captures']:
        require(sha(ROOT/capture['path'])==capture['sha256'],'Source capture hash changed')
    nexus=read('docs/research/nexus-table-2026-10-09.json')['tables'][0]
    branchmap={b['id']:b for b in catalog['branches']}
    header=next(row for row in nexus if len(row)==13 and row[1]['text']=='Navy')
    for b in catalog['branches']:
        require(header[b['source_column']]['text'].replace('’',"'")==b['label'],'Branch label differs from Nexus')
        n=sum(r['branch_id']==b['id'] for r in records); empty=sum(r['branch_id']==b['id'] for r in blanks)
        require(n+empty==23 and {'branch_id':b['id'],'populated':n,'blank':empty,'total':23} in catalog['coverage']['per_branch'],'Per-branch coverage mismatch')
    workbook=read('docs/research/full-chart-reference-google-ranks.json')
    sheets={s['id']:s for s in workbook['sheets']}
    assertions=0
    for r in records+shared:
        primary=r['source_assertions'][0]
        row=nexus[primary['row_index_zero_based']]; cell=row[primary['cell_index_zero_based']]
        require(cell['text']==r['title_raw']==primary['title'],f"Nexus title mismatch: {r['id']}")
        require(row[0]['text']==r['grade']==primary['grade'],f"Nexus grade mismatch: {r['id']}")
        require(int(cell['colspan'])==(12 if r in shared else 1),f"Merged source mismatch: {r['id']}")
        if r['branch_id']:
            require(primary['cell_index_zero_based']==branchmap[r['branch_id']]['source_column'],'Branch coordinates differ')
        for a in r['source_assertions'][1:]:
            if 'gid' not in a:
                continue
            source_row=next(x for x in sheets[a['gid']]['rows'] if x['row']==a['row_index_zero_based']+1)
            col=a['cell_index_zero_based']
            require(source_row['values'][col]==a['title'],f"Workbook title mismatch: {r['id']}")
            require(source_row['values'][1]==a['grade'],f"Workbook grade mismatch: {r['id']}")
            require((col+1 in source_row['struck_columns'])==a['struck'],f"Workbook strikeout mismatch: {r['id']}")
            require(col>=2,'Workbook assertions must not reference metadata/payroll')
            require(col in source_row['included_title_columns_zero_based'],'Workbook assertion outside sanitized inclusion')
            assertions+=1
    for r in blanks:
        row=nexus[r['row_index_zero_based']]
        require(row[0]['text']==r['grade'] and row[r['cell_index_zero_based']]['text']=='','Source blank changed')
    patterns={p['id']:p for p in catalog['patterns']}
    assets={p['id']:p for p in composition['patterns']}
    require(len(patterns)==len(catalog['patterns']) and set(patterns)==set(assets) and len(assets)>0,'Composition missing or duplicate patterns')
    require(all(p['status']=='CANDIDATE' and p['approval'] is None for p in list(patterns.values())+list(assets.values())),'Pattern approval changed')
    require(catalog['coverage']['patterns']==len(assets) and catalog['coverage']['branch_grid_cells']==len(cells),'Coverage receipt disagrees')
    for r in records+shared:
        require(all(p in assets for p in [r['pattern_id']]+r.get('alternative_pattern_ids',[])),'Missing assignment asset')
    require(composition['catalog_sha256']==sha(ROOT/'data/rank-catalog.json'),'Composition catalog stale')
    components={c['token']:c for c in composition['components']}
    for c in components.values():
        for path,hashkey in [('original_path','original_sha256'),('normalized_path','normalized_sha256'),('native_clean_path','native_clean_sha256')]:
            require(sha(ROOT/c[path])==c[hashkey],'Component provenance hash mismatch')
        img=Image.open(ROOT/c['normalized_path'])
        require(img.mode=='RGBA' and img.size==(160,270) and img.getchannel('A').getextrema()==(0,255),'Component geometry/alpha changed')
    placements=0
    for pid,a in assets.items():
        rows=patterns[pid]['rows']; cols=max(map(len,rows))
        width=cols*160+(cols-1)*10+32; height=len(rows)*270+(len(rows)-1)*10+32
        boxes=[]
        for ri,row in enumerate(rows):
            start=16+((cols-len(row))*170)//2
            for ci,token in enumerate(row):
                boxes.append(dict(row=ri,column=ci,token=token,x=start+ci*170,y=16+ri*280,width=160,height=270))
        require(a['rows']==rows and a['tile_boxes']==boxes and (a['width'],a['height'])==(width,height),f'Ordered geometry mismatch: {pid}')
        expected=Image.new('RGBA',(width,height),(0,0,0,0)); draw=ImageDraw.Draw(expected)
        for offset,cut,color in [(0,5,'#42474c'),(1,4,'#d4d9dc'),(3,3,'#555c63')]:
            draw.polygon(polygon(4+offset,4+offset,width-8-2*offset,height-8-2*offset,cut),fill=color)
        for y in range(11,height-11):
            v=round(116-20*((y-4)/(height-8)))+(1 if y%4==0 else 0)
            draw.line((8,y,width-9,y),fill=(v,v+4,v+7,255))
        for b in boxes:
            expected.alpha_composite(Image.open(ROOT/components[b['token']]['normalized_path']).convert('RGBA'),(b['x'],b['y']))
        actual=Image.open(ROOT/a['png_path'])
        require(actual.mode=='RGBA' and actual.size==(width,height),'Plaque dimensions/mode mismatch')
        require(ImageChops.difference(expected,actual).getbbox(alpha_only=False) is None,f'Plaque pixel mismatch: {pid}')
        require(actual.getchannel('A').getextrema()==(0,255) and actual.getpixel((0,0))[3]==0,'Plaque exterior alpha mismatch')
        svg=ET.parse(ROOT/a['svg_path']).getroot(); images=svg.findall('.//'+NS+'image')
        require(len(images)==len(boxes)==a['tile_count'],'SVG tile count mismatch')
        for node,b in zip(images,boxes):
            require(node.attrib['data-token']==b['token'] and all(int(node.attrib[k])==b[k] for k in ['x','y','width','height']),'SVG ordered geometry mismatch')
            require(base64.b64decode(node.attrib['href'].split(',')[1])==(ROOT/components[b['token']]['normalized_path']).read_bytes(),'SVG component bytes differ')
        for ext in ['png','svg']:
            require(sha(ROOT/a[ext+'_path'])==a['sha256_'+ext],'Plaque hash mismatch')
        placements+=len(boxes)
    charts=read('assets/charts/manifest.json')
    require(len(charts['charts'])==14,'Expected fourteen chart pairs')
    require(charts['catalog_sha256']==sha(ROOT/'data/rank-catalog.json') and charts['composition_manifest_sha256']==sha(ROOT/'assets/composed/manifest.json'),'Chart input hashes stale')
    maxbytes=0
    for chart in charts['charts']:
        expected_ids={r['id'] for r in records if r['branch_id'] in chart['branch_ids']}
        require(set(chart['record_ids'])==expected_ids and set(chart['shared_record_ids'])=={r['id'] for r in shared},'Chart record coverage mismatch')
        require(chart['blank_cells']==sum(r['branch_id'] in chart['branch_ids'] for r in blanks),'Chart blank count mismatch')
        require(chart['asset_scale']==.5,'Chart physical scale changed')
        for x,y,w,h,text in chart['text_bounds']:
            require(x>=0 and y>=0 and x+w<=chart['width'] and y+h<=chart['height'],f'Chart label outside canvas: {chart["id"]}: {text}')
            require(h>=18,'Chart labels below minimum readable 13px')
        headings=[b for b in chart['text_bounds'] if b[1]<chart['layout']['grid_top']]
        for i,(x,y,w,h,text) in enumerate(headings):
            for xx,yy,ww,hh,other in headings[i+1:]:
                require(not (x<xx+ww and xx<x+w and y<yy+hh and yy<y+h),f'Chart heading overlap: {text} / {other}')
        for ext in ['png','svg']:
            path=ROOT/chart[ext+'_path']; require(sha(path)==chart['sha256_'+ext],'Chart hash mismatch')
            maxbytes=max(maxbytes,path.stat().st_size); require(path.stat().st_size<100_000_000,'Chart exceeds ordinary GitHub file limit')
        require(Image.open(ROOT/chart['png_path']).size==(chart['width'],chart['height']),'Chart raster size differs')
        svg=ET.parse(ROOT/chart['svg_path']).getroot()
        require((int(svg.attrib['width']),int(svg.attrib['height']))==(chart['width'],chart['height']),'Chart SVG dimensions differ')
        grid={(r['branch_id'],r['grade']):r for r in records}
        sequence=[grid[(b,g)]['pattern_id'] for g in chart['grade_ids'] for b in chart['branch_ids'] if (b,g) in grid]
        sequence += [pid for r in shared for pid in [r['pattern_id']]+r.get('alternative_pattern_ids',[])]
        image_nodes=svg.findall('.//'+NS+'image')
        require(len(image_nodes)==len(sequence),'Chart SVG image coverage differs')
        for node,pid in zip(image_nodes,sequence):
            payload=base64.b64decode(node.attrib['{http://www.w3.org/1999/xlink}href'].split(',')[1])
            require(hashlib.sha256(payload).hexdigest()==assets[pid]['sha256_png'],'Chart embedded plaque sequence mismatch')
            require(int(node.attrib['width'])==round(assets[pid]['width']*.5) and int(node.attrib['height'])==round(assets[pid]['height']*.5),'Chart SVG plaque scale differs')
        texts=[node.text or '' for node in svg.findall('.//'+NS+'text')]
        require(texts==[b[4] for b in chart['text_bounds']],'Chart SVG labels disagree with receipt')
        layout=chart['layout']; gridbottom=layout['grid_top']+len(chart['grade_ids'])*layout['row_height']
        for gi,g in enumerate(chart['grade_ids']):
            for bi,b in enumerate(chart['branch_ids']):
                x=layout['grade_width']+bi*layout['cell_width']+12
                y=layout['grid_top']+gi*layout['row_height']+10
                row=grid.get((b,g))
                if row:
                    titlelines=[t for xx,yy,ww,hh,t in chart['text_bounds'] if xx==x and y<=yy<y+100 and hh==23]
                    require(' '.join(titlelines)==row['title_display'],'Chart actual title differs from source dataset')
        for x,y,w,h,text in chart['text_bounds']:
            if layout['grid_top']<=y<gridbottom and x>=layout['grade_width']:
                col=int((x-layout['grade_width'])//layout['cell_width']); row=int((y-layout['grid_top'])//layout['row_height'])
                require(x+w<=layout['grade_width']+(col+1)*layout['cell_width'] and y+h<=layout['grid_top']+(row+1)*layout['row_height'],'Chart label spills outside allotted cell')
            for ix,iy,iw,ih,pid in chart['image_bounds']:
                require(not (x<ix+iw and ix<x+w and y<iy+ih and iy<y+h),f'Chart label overlaps plaque: {text}')
    parser=ReviewParser(); parser.feed((ROOT/'assets/catalog-review.html').read_text(encoding='utf-8'))
    ids=[r['id'] for r in records+shared]+['blank-'+r['branch_id']+'-'+r['grade'] for r in blanks]
    require(sorted(ids)==sorted(parser.ids),'HTML row identities differ')
    payload=json.loads(parser.payload)
    require(payload=={'catalog':catalog,'composition':composition,'charts':charts},'Embedded HTML data stale')
    for link in parser.links:
        if not urlsplit(link).scheme and not link.startswith('#'):
            require((ROOT/'assets'/unquote(link.split('#')[0])).is_file(),f'Broken local link: {link}')
    print(json.dumps(dict(status='PASS',branch_records=len(records),military_records=69,source_blanks=len(blanks),shared_records=len(shared),patterns=len(assets),tile_placements=placements,workbook_assertions=assertions,charts=14,html_rows=len(ids),largest_chart_bytes=maxbytes,independent_pixel_reconstruction=True,creative_approval=False)))

if __name__=='__main__':
    main()
