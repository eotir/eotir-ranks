"""Generate offline candidate review and charts from the catalog and render manifest.

Usage: python tools/build_review.py
Prerequisites: Python 3 and Pillow; run compose_assets.py and build_catalog.py first.
No canon publication, source edits, approval transitions or external access occurs.
"""
from __future__ import annotations
import base64
import argparse
import hashlib
import html
import json
import math
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/charts'
def discover_fonts():
    # Record font bytes: layout is reproducible on a host, not identical across fonts.
    for regular, bold, family in [('C:/Windows/Fonts/arial.ttf', 'C:/Windows/Fonts/arialbd.ttf', 'Arial'), ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 'DejaVu Sans')]:
        if Path(regular).is_file() and Path(bold).is_file():
            return regular, bold, family
    raise RuntimeError('Install Arial or DejaVu Sans regular and bold before building charts')

FONT, BOLD, FONT_FAMILY = discover_fonts()

def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def entries(value):
    return list(value.values()) if isinstance(value, dict) else value

def esc(value):
    return html.escape(str(value), quote=True)

def wrap(text, width, size=18):
    font = ImageFont.truetype(FONT, size)
    result, line = [], ''
    for word in str(text).split():
        trial = (line + ' ' + word).strip()
        if font.getlength(trial) > width and line:
            result.append(line)
            line = word
        else:
            line = trial
    if line:
        result.append(line)
    return result

class Canvas:
    """Draw parallel raster/vector views so both exports use the same layout."""
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.raster = Image.new('RGB', (width, height), '#f3f5f8')
        self.draw = ImageDraw.Draw(self.raster)
        self.svg = [f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width}" height="{height}" viewBox="0 0 {width} {height}"><title>Imperial Republic candidate rank chart</title><desc>Candidate designs; exact approval and source precedence pending. Source blanks preserved. Shared upper titles remain unresolved.</desc><rect width="100%" height="100%" fill="#f3f5f8"/>']
        self.text_bounds = []
        self.image_bounds = []

    def rect(self, x, y, width, height, fill):
        self.draw.rectangle((x, y, x+width-1, y+height-1), fill=fill)
        self.svg.append(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" fill="{fill}"/>')

    def text(self, x, y, text, size=18, bold=False, color='#18283a'):
        font = ImageFont.truetype(BOLD if bold else FONT, size)
        # SVG uses the same top-aligned line metrics as Pillow's explicit ascender anchor.
        self.draw.text((x, y), str(text), font=font, fill=color, anchor='lt')
        self.svg.append(f'<text x="{x}" y="{y}" dominant-baseline="text-before-edge" font-family="{FONT_FAMILY}, sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}">{esc(text)}</text>')
        self.text_bounds.append([x, y, round(font.getlength(str(text)), 2), size+5, str(text)])

    def image(self, x, y, asset, scale):
        path = ROOT / asset['png_path']
        width, height = round(asset['width']*scale), round(asset['height']*scale)
        img = Image.open(path).convert('RGBA').resize((width, height), Image.Resampling.LANCZOS)
        self.raster.paste(img, (x, y), img)
        uri = 'data:image/png;base64,' + base64.b64encode(path.read_bytes()).decode()
        self.svg.append(f'<image x="{x}" y="{y}" width="{width}" height="{height}" xlink:href="{uri}"/>')
        self.image_bounds.append([x, y, width, height, asset['id']])

    def save(self, name):
        png, svg = OUT / (name+'.png'), OUT / (name+'.svg')
        self.raster.save(png)
        svg.write_text(''.join(self.svg)+ '</svg>', encoding='utf-8')
        return {'id':name, 'png_path':png.relative_to(ROOT).as_posix(), 'svg_path':svg.relative_to(ROOT).as_posix(), 'width':self.width, 'height':self.height, 'sha256_png':digest(png), 'sha256_svg':digest(svg), 'text_bounds':self.text_bounds, 'image_bounds':self.image_bounds}

def chart(catalog, assets, branches, name, title):
    grades = sorted([g for g in catalog['grades'] if g['id'] in {r['grade'] for r in catalog['rank_records']}], key=lambda g:g['order_bottom_up'])
    # One scale across every grade and chart preserves physical tile proportions.
    scale = 0.5
    maxw = max(a['width'] for a in assets.values())
    maxh = max(a['height'] for a in assets.values())
    cw = max(350, math.ceil(maxw*scale)+28)
    max_title_lines=max(len(wrap(r['title_display'],cw-24,18)) for r in catalog['rank_records'])
    rh = max(166, math.ceil(maxh*scale)+max_title_lines*22+95)
    gw, top = 85, 220
    records = {(r['branch_id'],r['grade']):r for r in catalog['rank_records']}
    shared = catalog['shared_records']
    sharedh = max(180, math.ceil(maxh*scale)+340)
    width = max(1250, gw+len(branches)*cw+36)
    height = top+len(grades)*rh+130+len(shared)*sharedh+100
    cv = Canvas(width, height)
    cv.text(24, 18, title, 28, True)
    cv.text(24, 57, 'CANDIDATE · '+str(catalog['date'])+' · visual and assignment approval pending', 20, True, '#8b3f00')
    cv.text(24, 86, 'Nexus + bounded official workbook snapshots; external art informs draft aesthetics only. All tiles use the same display scale.', 17)
    cv.text(24, 112, 'Bottom-up working grades. Source blanks mean no rank was invented. Shared upper records below remain separate and unresolved.', 17)
    cv.text(20, top-28, 'Grade', 18, True)
    for col, branch in enumerate(branches):
        for n,line in enumerate(wrap(branch['label'], cw-20, 18)):
            cv.text(gw+col*cw+10, top-45+n*22, line, 18, True)
    for row, grade in enumerate(grades):
        y = top+row*rh
        cv.text(18,y+12,grade['id'],18,True)
        for col, branch in enumerate(branches):
            x=gw+col*cw
            cv.rect(x+2,y+2,cw-4,rh-4,'#ffffff')
            record=records.get((branch['id'],grade['id']))
            if record:
                lines=wrap(record['title_display'],cw-24,18)
                for n,line in enumerate(lines):
                    cv.text(x+12,y+10+n*22,line,18,True)
                asset=assets[record['pattern_id']]
                py=y+18+len(lines)*22
                cv.image(x+12,py,asset,scale)
                cv.text(x+12,y+rh-43,record['pattern_id'],14)
                cv.text(x+12,y+rh-22,'CANDIDATE · source/rationale: review HTML',13,color='#675020')
            else:
                cv.text(x+12,y+15,'SOURCE BLANK',17,True,color='#677382')
                cv.text(x+12,y+43,'No rank or insignia inferred',15)
    sy=top+len(grades)*rh+25
    cv.text(24,sy,'Shared upper / Throne titles — unresolved alternatives',25,True)
    cv.text(24,sy+38,'Spanning source cells; not twelve branch assignments. Grade, appointment and mapping conflicts remain open.',17)
    for n,record in enumerate(shared):
        y=sy+90+n*sharedh
        cv.rect(20,y,width-40,sharedh-10,'#fff8ed')
        for t,line in enumerate(wrap(record['grade']+' · '+record['title_display'],width-64,22)):
            cv.text(32,y+12+t*26,line,22,True)
        asset=assets[record['pattern_id']]
        cv.text(32,y+71,'A · '+record['pattern_id'],14)
        cv.image(32,y+96,asset,scale)
        for alt_id in record.get('alternative_pattern_ids',[]):
            alt=assets[alt_id]
            ax=64+round(asset['width']*scale)
            cv.text(ax,y+71,'B · '+alt_id,14)
            cv.image(ax,y+96,alt,scale)
        notes=record.get('candidate_notes',[])
        notes=' '.join(notes) if isinstance(notes,list) else str(notes)
        alternatives=' | '.join(str(a.get('grade',''))+': '+str(a.get('title','')) for a in record.get('source_assertions',[]))
        for ln,line in enumerate(wrap('UNRESOLVED · '+alternatives+' · '+notes,width-64,16)[:8]):
            cv.text(32,y+111+round(maxh*scale)+ln*22,line,16)
    cv.text(24,height-48,'Working dataset and asset hashes: assets/charts/manifest.json · Complete evidence and native assets: assets/catalog-review.html',16)
    result=cv.save(name)
    result.update({'branch_ids':[b['id'] for b in branches], 'grade_ids':[g['id'] for g in grades], 'layout':{'grade_width':gw,'cell_width':cw,'row_height':rh,'grid_top':top,'shared_top':sy+90,'shared_height':sharedh}, 'record_ids':[r['id'] for r in catalog['rank_records'] if r['branch_id'] in {b['id'] for b in branches}], 'shared_record_ids':[r['id'] for r in shared], 'blank_cells':sum(1 for b in branches for g in grades if (b['id'],g['id']) not in records),'asset_scale':scale})
    return result

def evidence(record):
    snippets=[]
    for assertion in record.get('source_assertions',[]):
        label=str(assertion.get('source','source'))+' · '+str(assertion.get('grade',''))+' · '+str(assertion.get('title',''))
        coords='; '.join(f'{key}: {assertion[key]}' for key in ('capture','gid','cell','row_index_zero_based','cell_index_zero_based','struck') if key in assertion)
        url=assertion.get('url','')
        snippets.append(f'<li><a href="{esc(url)}">{esc(label)}</a><br><small>{esc(coords)}</small></li>')
    return '<ul>'+''.join(snippets)+'</ul>'

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--html-only',action='store_true',help='Reuse verified existing chart outputs and rebuild only the HTML review')
    args=parser.parse_args()
    catalog=read('data/rank-catalog.json')
    manifest=read('assets/composed/manifest.json')
    assets={a['id']:a for a in entries(manifest['patterns'])}
    patterns={p['id']:p for p in entries(catalog['patterns'])}
    branches=catalog['branches']
    OUT.mkdir(parents=True,exist_ok=True)
    if args.html_only:
        charts_manifest=read('assets/charts/manifest.json')
        if charts_manifest['catalog_sha256']!=digest(ROOT/'data/rank-catalog.json') or charts_manifest['composition_manifest_sha256']!=digest(ROOT/'assets/composed/manifest.json'):
            raise ValueError('Charts are stale; run a complete build before --html-only')
        charts=charts_manifest['charts']
        for c in charts:
            for ext in ['png','svg']:
                if digest(ROOT/c[ext+'_path'])!=c['sha256_'+ext]:
                    raise ValueError('Chart bytes changed; complete rebuild required')
    else:
        charts=[chart(catalog,assets,[b for b in branches if b['military']],'military-chart','Imperial Republic military — working rank plaques'), chart(catalog,assets,branches,'all-branches-chart','Imperial Republic all branches — working rank plaques')]
        charts += [chart(catalog,assets,[b],'branch-'+b['id'],'Imperial Republic · '+b['label']) for b in branches]
        charts_manifest={'schema_version':1,'status':'CANDIDATE','date':catalog['date'],'catalog_sha256':digest(ROOT/'data/rank-catalog.json'),'composition_manifest_sha256':digest(ROOT/'assets/composed/manifest.json'),'font_provenance':{'regular_path':FONT,'bold_path':BOLD,'family':FONT_FAMILY,'regular_sha256':digest(Path(FONT)),'bold_sha256':digest(Path(BOLD))},'charts':charts}
        (OUT/'manifest.json').write_text(json.dumps(charts_manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    branchmap={b['id']:b['label'] for b in branches}
    rows=[]
    for r in catalog['rank_records']+catalog['shared_records']:
        p=patterns[r['pattern_id']]; a=assets[p['id']]
        ordered=' / '.join(', '.join(row) for row in p['rows'])
        notes=r.get('candidate_notes',[])
        rationale=p.get('design_basis','')
        refs=' '.join(f'<a href="{esc(url)}">reference {n+1}</a>' for n,url in enumerate(p.get('reference_urls',[])))
        adaptations=p.get('adaptation_notes',[])
        pattern_notes=' '.join(adaptations) if isinstance(adaptations,list) else str(adaptations)
        notes=' '.join(notes) if isinstance(notes,list) else str(notes)
        relpng='../'+a['png_path'].removeprefix('assets/') if a['png_path'].startswith('assets/') else '../'+a['png_path']
        # The review lives in assets/, so native asset paths are relative to that directory.
        relpng=Path(a['png_path']).relative_to('assets').as_posix()
        relsvg=Path(a['svg_path']).relative_to('assets').as_posix()
        uri=relpng
        alternate_html=''
        for alt_id in r.get('alternative_pattern_ids',[]):
            alt=assets[alt_id]; altp=patterns[alt_id]
            alturi=Path(alt['png_path']).relative_to('assets').as_posix()
            altrows=' / '.join(', '.join(row) for row in altp['rows'])
            apng=Path(alt['png_path']).relative_to('assets').as_posix(); asvg=Path(alt['svg_path']).relative_to('assets').as_posix()
            alternate_html+=f'<p><strong>Unresolved alternative: {esc(alt_id)}</strong><br>{esc(altrows)}</p><div class="plaque"><img src="{alturi}" width="{round(alt["width"]*.5)}" height="{round(alt["height"]*.5)}" alt="Alternative candidate plaque: {esc(altrows)}"></div><a href="{esc(apng)}">Alternative native PNG</a> · <a href="{esc(asvg)}">Alternative SVG</a>'
        branch=branchmap.get(r.get('branch_id'),'Shared upper / Throne — unresolved')
        source=f'<details><summary>Raw source assertions / conflicts</summary>{evidence(r)}<p>Raw display source title: {esc(r["title_raw"])}</p></details>'
        rows.append(f'<tr data-id="{esc(r["id"])}" data-branch="{esc(r.get("branch_id") or "shared")}" data-grade="{esc(r["grade"])}"><td>{esc(branch)}</td><th scope="row">{esc(r["grade"])}<br>{esc(r["title_display"])}<br><small>{esc(r["id"])}</small></th><td><div class="plaque"><img src="{uri}" width="{round(a["width"]*.5)}" height="{round(a["height"]*.5)}" alt="Candidate plaque: {esc(ordered)}"></div><a href="{esc(relpng)}">Native PNG</a> · <a href="{esc(relsvg)}">SVG</a>{alternate_html}</td><td>{esc(p["id"])}<br>{esc(ordered)}<p>{esc(rationale)}</p><p>{esc(pattern_notes)}</p>{refs}<p>{esc(notes)}</p><strong>CANDIDATE · approval pending</strong>{source}</td></tr>')
    for r in catalog['blank_cells']:
        coords=json.dumps(r,ensure_ascii=False)
        rows.append(f'<tr data-id="blank-{esc(r["branch_id"])}-{esc(r["grade"])}" data-branch="{esc(r["branch_id"])}" data-grade="{esc(r["grade"])}" class="blank"><td>{esc(branchmap[r["branch_id"]])}</td><th scope="row">{esc(r["grade"])} · SOURCE BLANK</th><td>No rank or candidate inferred</td><td>{esc(r.get("reason","Source blank"))}<details><summary>Source coordinates</summary><pre>{esc(coords)}</pre></details></td></tr>')
    options=''.join(f'<option value="{esc(b["id"])}">{esc(b["label"])}</option>' for b in branches)+'<option value="shared">Shared upper / Throne</option>'
    gradeopts=''.join(f'<option>{esc(g["id"])}</option>' for g in sorted(catalog['grades'],key=lambda g:g['order_bottom_up']))
    links=''.join(f'<li>{esc(c["id"])}: <a href="charts/{esc(c["id"])}.svg" download>SVG</a> · <a href="charts/{esc(c["id"])}.png" download>PNG</a></li>' for c in charts)
    payload=json.dumps({'catalog':catalog,'composition':manifest,'charts':charts_manifest},ensure_ascii=False).replace('</','<\\/')
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Imperial Republic candidate rank library</title><style>body{font:16px/1.5 system-ui,sans-serif;margin:24px;color:#18283a;background:#f3f5f8}h1{margin-bottom:0}.banner{padding:18px;background:#fff0d5;border:2px solid #9d5700}.controls{display:flex;gap:20px;flex-wrap:wrap;position:sticky;top:0;background:#f3f5f8;padding:14px 0;z-index:2}label{display:flex;gap:8px;align-items:center}select,input{font:inherit;padding:6px}table{border-collapse:collapse;width:100%;background:white}th,td{text-align:left;border:1px solid #ccd4df;padding:14px;vertical-align:top}th{min-width:160px}td:first-child{max-width:170px}td:last-child{min-width:280px}caption{text-align:left;font-weight:700;padding:14px}small{color:#526174}pre{white-space:pre-wrap}.table-wrap{overflow-x:auto}.plaque{padding:12px;background-color:#eee;background-image:linear-gradient(45deg,#ccc 25%,transparent 25%),linear-gradient(-45deg,#ccc 25%,transparent 25%),linear-gradient(45deg,transparent 75%,#ccc 75%),linear-gradient(-45deg,transparent 75%,#ccc 75%);background-size:20px 20px;background-position:0 0,0 10px,10px -10px,-10px 0;margin-bottom:8px;min-width:460px}.plaque img{display:block;max-width:none}.blank{background:#eef1f4}.hidden{display:none}a{color:#034e91}details{margin-top:10px}summary{cursor:pointer}li{margin-bottom:8px}</style><main><a href="review.html">← Tile and candidate history</a><h1>Imperial Republic rank-plaque library</h1><p class="banner"><strong>CANDIDATE — exact visual and rank-assignment approval pending.</strong> Draft coverage is complete; source precedence, shared upper/Throne grades, color meanings and canon remain unresolved. No uniform or cylinder entitlement is inferred.</p><p id="coverage">69 military records · 210 branch records · 66 source blanks · 7 separate shared upper records.</p><p>Version DATE · deterministic tile composition. Source: <a href="https://nexus.eotir.com/rankchart.html/">published Nexus</a> and bounded official workbook snapshots. External references provide aesthetic comparisons only. All plaques display at the same physical scale; native links allow exact inspection.</p><details><summary>Download complete and branch charts (14 PNG / SVG pairs)</summary><ul>CHARTLINKS</ul></details><p>Shared upper / Throne records are separate below, with raw competing assertions. Source blanks remain visible by default. Filtering preserves those distinctions.</p><div class="controls"><label>Search <input id="search" type="search" placeholder="Title, pattern or source"></label><label>Branch <select id="branch"><option value="">All branches + shared</option>BRANCHOPTIONS</select></label><label>Grade <select id="grade"><option value="">All grades</option>GRADEOPTIONS</select></label><label>Plaque background <select id="background"><option value="checker">Checkerboard</option><option value="light">Light</option><option value="dark">Dark</option></select></label></div><p id="count" role="status" aria-live="polite"></p><noscript>The complete accessible table is available without JavaScript. Filters require JavaScript.</noscript><div class="table-wrap"><table><caption>Candidate assignments, original source evidence and preserved blanks</caption><thead><tr><th scope="col">Branch</th><th scope="col">Grade / title</th><th scope="col">Plaque candidate / native exports</th><th scope="col">Ordered pattern, rationale and source uncertainty</th></tr></thead><tbody>ROWS</tbody></table></div><script id="review-data" type="application/json">PAYLOAD</script><script>const rows=[...document.querySelectorAll('tbody tr')];const search=document.querySelector('#search'),branch=document.querySelector('#branch'),grade=document.querySelector('#grade');function filter(){const q=search.value.toLowerCase();let n=0;for(const row of rows){const show=(!branch.value||row.dataset.branch===branch.value)&&(!grade.value||row.dataset.grade===grade.value)&&(!q||row.textContent.toLowerCase().includes(q));row.classList.toggle('hidden',!show);if(show)n++;}document.querySelector('#count').textContent=n+' of '+rows.length+' rows visible (populated records + shared records + source blanks)';}for(const el of [search,branch,grade])el.addEventListener('input',filter);document.querySelector('#background').addEventListener('change',e=>{for(const el of document.querySelectorAll('.plaque')){el.style.backgroundImage=e.target.value==='checker'?'':'none';el.style.backgroundColor=e.target.value==='dark'?'#18212d':e.target.value==='light'?'#fff':'#eee';}});filter();</script></main></html>'''
    for key,value in [('DATE',str(catalog['date'])),('CHARTLINKS',links),('BRANCHOPTIONS',options),('GRADEOPTIONS',gradeopts),('ROWS',''.join(rows)),('PAYLOAD',payload)]:
        page=page.replace(key,value)
    (ROOT/'assets/catalog-review.html').write_text(page,encoding='utf-8')
    print(json.dumps({'charts':len(charts),'html_rows':len(rows),'status':'CANDIDATE','catalog_sha256':charts_manifest['catalog_sha256']}))

if __name__=='__main__':
    main()
