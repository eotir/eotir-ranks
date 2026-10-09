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
            alternate_html+=f'<figure><figcaption><span class="chip unresolved">Alternative</span></figcaption><div class="plaque"><img src="{alturi}" width="{round(alt["width"]*.2)}" height="{round(alt["height"]*.2)}" alt="Alternative candidate plaque: {esc(altrows)}"></div><a href="{esc(apng)}">Native PNG</a> · <a href="{esc(asvg)}">SVG</a><details><summary>Alternative pattern</summary>{esc(alt_id)}<br>{esc(altrows)}</details></figure>'
        branch=branchmap.get(r.get('branch_id'),'Shared upper / Throne — unresolved')
        source=f'<details><summary>Raw source assertions / conflicts</summary>{evidence(r)}<p>Raw display source title: {esc(r["title_raw"])}</p></details>'
        state='<span class="chip unresolved">Unresolved</span>' if not r.get('branch_id') else '<span class="chip">Proposed</span>'
        rows.append(f'<tr data-id="{esc(r["id"])}" data-branch="{esc(r.get("branch_id") or "shared")}" data-grade="{esc(r["grade"])}"><td>{esc(branch)}</td><th scope="row"><span class="grade-label">{esc(r["grade"])}</span><br>{esc(r["title_display"])}</th><td><div class="previews"><figure><div class="plaque"><img src="{uri}" width="{round(a["width"]*.2)}" height="{round(a["height"]*.2)}" alt="Candidate plaque: {esc(ordered)}"></div><a href="{esc(relpng)}">Native PNG</a> · <a href="{esc(relsvg)}">SVG</a></figure>{alternate_html}</div></td><td>{state}<details><summary>Pattern &amp; rationale</summary><p>{esc(p["id"])}<br>{esc(ordered)}</p><p>{esc(rationale)}</p><p>{esc(pattern_notes)}</p>{refs}<p>{esc(notes)}</p><small>{esc(r["id"])}</small></details>{source}</td></tr>')
    for r in catalog['blank_cells']:
        coords=json.dumps(r,ensure_ascii=False)
        rows.append(f'<tr data-id="blank-{esc(r["branch_id"])}-{esc(r["grade"])}" data-branch="{esc(r["branch_id"])}" data-grade="{esc(r["grade"])}" class="blank"><td>{esc(branchmap[r["branch_id"]])}</td><th scope="row">{esc(r["grade"])} · SOURCE BLANK</th><td>No rank or candidate inferred</td><td>{esc(r.get("reason","Source blank"))}<details><summary>Source coordinates</summary><pre>{esc(coords)}</pre></details></td></tr>')
    options=''.join(f'<option value="{esc(b["id"])}">{esc(b["label"])}</option>' for b in branches)+'<option value="shared">Shared upper / Throne</option>'
    gradeopts=''.join(f'<option>{esc(g["id"])}</option>' for g in sorted(catalog['grades'],key=lambda g:g['order_bottom_up']))
    links=''.join(f'<li>{esc(c["id"])}: <a href="charts/{esc(c["id"])}.svg" download>SVG</a> · <a href="charts/{esc(c["id"])}.png" download>PNG</a></li>' for c in charts)
    payload=json.dumps({'catalog':catalog,'composition':manifest,'charts':charts_manifest},ensure_ascii=False).replace('</','<\\/')
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Imperial Republic candidate rank library</title><style>
:root{color-scheme:dark;background:#10161f;color:#dce5ef;font-family:system-ui,sans-serif}*{box-sizing:border-box}body{background:#10161f;font-size:13px;line-height:1.45;margin:0;padding:20px}main{max-width:1500px;margin:auto}h1{font-size:24px;line-height:1.2;margin:12px 0}p{margin:8px 0}a{color:#9bcaff;text-underline-offset:2px}a:hover{color:#d4e8ff}small,.muted{color:#a4b2c3;font-size:11px}.banner{padding:10px 12px;border:1px solid #665735;background:#252219;border-radius:6px;color:#e8d5a8}.controls{display:flex;gap:12px;flex-wrap:wrap;position:sticky;top:0;background:#10161ff5;padding:12px 0;z-index:2;border-bottom:1px solid #334050}label{display:flex;gap:6px;align-items:center;font-size:12px}select,input{font:inherit;color:#dce5ef;background:#18222f;border:1px solid #465467;border-radius:4px;padding:5px 7px;min-height:30px}input{width:190px}select{max-width:220px}:focus-visible{outline:2px solid #9bcaff;outline-offset:2px}.table-wrap{overflow-x:auto;border:1px solid #334050;border-radius:6px}table{border-collapse:collapse;width:100%;table-layout:fixed;background:#141d28}th,td{text-align:left;border-bottom:1px solid #2b394b;padding:9px 10px;vertical-align:top;overflow-wrap:anywhere}thead{background:#1c2836;color:#bfcee0}thead th{font-size:11px;text-transform:uppercase;letter-spacing:.06em;font-weight:600}thead th:nth-child(1){width:15%}thead th:nth-child(2){width:23%}thead th:nth-child(3){width:34%}thead th:nth-child(4){width:28%}tbody th{font-size:13px;font-weight:600}.grade-label{font-size:11px;color:#a3bdd9}caption{text-align:left;padding:9px 10px;color:#a4b2c3;font-size:11px;background:#131b25}.previews{display:flex;flex-wrap:wrap;gap:10px}figure{margin:0;font-size:11px;max-width:100%}figcaption{margin:0 0 4px}.plaque{display:inline-block;padding:5px;background:#10161f;border-radius:3px;max-width:100%}.plaque img{display:block;max-width:none}.plaque.checker{background-color:#18212d;background-image:linear-gradient(45deg,#253142 25%,transparent 25%),linear-gradient(-45deg,#253142 25%,transparent 25%),linear-gradient(45deg,transparent 75%,#253142 75%),linear-gradient(-45deg,transparent 75%,#253142 75%);background-size:12px 12px;background-position:0 0,0 6px,6px -6px,-6px 0}.chip{display:inline-block;padding:2px 6px;font-size:10px;border-radius:3px;border:1px solid #425469;background:#233145;color:#c5d7ea}.chip.unresolved{border-color:#6b5836;background:#302719;color:#e7c994}details{margin-top:6px;font-size:12px}summary{cursor:pointer;color:#b7cce2}details p{margin:6px 0}details ul{padding-left:17px}pre{white-space:pre-wrap;font-size:11px}.blank{background:#111924;color:#93a3b6}.hidden{display:none}li{margin-bottom:5px}#coverage{color:#bfd0e3}#count{font-size:11px;color:#a4b2c3;margin:8px 0}@media(max-width:800px){body{padding:12px}table{min-width:750px}h1{font-size:21px}.controls{position:static;gap:8px}input{width:150px}}
</style><main><a href="review.html">← Candidate library</a><h1>Imperial Republic rank plaques</h1><p class="banner"><strong>CANDIDATE · approval pending.</strong> Shared upper / Throne titles, source precedence and color meanings remain unresolved.</p><p id="coverage">69 military · 210 branch records · 66 source blanks · 7 shared upper records</p><details><summary>Sources, scope &amp; chart downloads</summary><p>Version __REVIEW_DATE__. <a href="https://nexus.eotir.com/rankchart.html/">Nexus</a> and bounded official workbook snapshots retain competing assertions. External references inform candidate aesthetics. No uniform or cylinder entitlement is inferred.</p><p>Preview scale: 20% of native assets. Background controls reveal the transparent exterior; the metal backplate is part of each PNG. Native links preserve exact pixels.</p><p>Source blanks remain visible. Shared titles are separate records, with unresolved alternatives.</p><ul>CHARTLINKS</ul></details><div class="controls"><label>Search <input id="search" type="search" placeholder="Title, pattern or source"></label><label>Branch <select id="branch"><option value="">All branches + shared</option>BRANCHOPTIONS</select></label><label>Grade <select id="grade"><option value="">All grades</option>GRADEOPTIONS</select></label><label>Preview <select id="background"><option value="dark">Dark</option><option value="checker">Dark checker</option></select></label></div><p id="count" role="status" aria-live="polite"></p><noscript>The complete accessible table is available without JavaScript. Filters require JavaScript.</noscript><div class="table-wrap"><table><caption>Draft assignments · expand details for ordered patterns and source evidence</caption><thead><tr><th scope="col">Branch</th><th scope="col">Grade / title</th><th scope="col">Plaque / native exports</th><th scope="col">Details / uncertainty</th></tr></thead><tbody>ROWS</tbody></table></div><script id="review-data" type="application/json">PAYLOAD</script><script>const rows=[...document.querySelectorAll('tbody tr')];const search=document.querySelector('#search'),branch=document.querySelector('#branch'),grade=document.querySelector('#grade');function filter(){const q=search.value.toLowerCase();let n=0;for(const row of rows){const show=(!branch.value||row.dataset.branch===branch.value)&&(!grade.value||row.dataset.grade===grade.value)&&(!q||row.textContent.toLowerCase().includes(q));row.classList.toggle('hidden',!show);if(show)n++;}document.querySelector('#count').textContent=n+' of '+rows.length+' rows visible · records, shared titles and source blanks';}for(const el of [search,branch,grade])el.addEventListener('input',filter);document.querySelector('#background').addEventListener('change',e=>{for(const el of document.querySelectorAll('.plaque'))el.classList.toggle('checker',e.target.value==='checker');});filter();</script></main></html>'''
    for key,value in [('__REVIEW_DATE__',str(catalog['date'])),('CHARTLINKS',links),('BRANCHOPTIONS',options),('GRADEOPTIONS',gradeopts),('ROWS',''.join(rows)),('PAYLOAD',payload)]:
        page=page.replace(key,value)
    from build_rank_site import build_site
    page=build_site(page,catalog,manifest,charts_manifest)
    (ROOT/'assets/catalog-review.html').write_text(page,encoding='utf-8')
    print(json.dumps({'charts':len(charts),'html_rows':len(rows),'status':'CANDIDATE','catalog_sha256':charts_manifest['catalog_sha256']}))

if __name__=='__main__':
    main()
