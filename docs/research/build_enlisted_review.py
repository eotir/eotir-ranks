"""Build an offline bottom-up enlisted review page from working JSON.

Usage: python docs/research/build_enlisted_review.py
Prerequisites: Python 3, rendered candidates and the project render manifest.
Updates technical QC only; no creative approval or canonical promotion occurs.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
data_path = ROOT / 'data/military-enlisted-working.json'
data = json.loads(data_path.read_text(encoding='utf-8'))
manifest = json.loads((ROOT / 'assets/render-manifest-2026-10-09.json').read_text(encoding='utf-8'))
for pattern in data['grade_patterns']:
    number = pattern['order_bottom_up']
    version = 2 if number in (1, 4) else 1
    pattern['local_image'] = f'assets/plaques/candidates/2026-10-09/enlisted/military-enlisted-e{number}-v{version}.png'
    entry = next(e for e in manifest['entries'] if e['local_path'] == pattern['local_image'])
    assert (ROOT / pattern['local_image']).is_file(), pattern['local_image']
    assert entry['observed_pattern'] == pattern['tiles'], f'Pattern mismatch: {number}'
    assert entry['tile_count_and_order_visually_verified'], f'Uninspected pattern: {number}'
    pattern['observed_pattern'] = entry['observed_pattern']
    pattern['visual_count_and_order_verified'] = True
    pattern['image_version'] = version
    pattern['iteration_history'] = [f'assets/plaques/candidates/2026-10-09/enlisted/military-enlisted-e{number}-v1.png'] if version == 2 else []
data_path.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
payload = json.dumps(data).replace('<', '\\u003c')
html = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Imperial Republic — enlisted military candidates</title>
<style>
:root{font-family:system-ui,sans-serif;color-scheme:dark;background:#10161f;color:#e9eef5}body{max-width:1320px;margin:auto;padding:28px}a{color:#91c8ff}p{color:#bdc9d8;line-height:1.6;max-width:90ch}.status,.extension{color:#ffcf75}.controls{display:flex;gap:10px;flex-wrap:wrap;margin:24px 0}button{font:inherit;color:inherit;background:#1c2634;border:1px solid #607084;border-radius:6px;padding:9px 16px;cursor:pointer}button[aria-pressed=true]{border-color:#91c8ff;background:#263d56}.cards{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}article{border:1px solid #394656;border-radius:8px;overflow:hidden;background:#19222e}article header,article footer{padding:16px}h2{margin:0 0 8px}.surface{height:330px;display:flex;justify-content:center;align-items:center;background-color:#c4c9cf;background-image:conic-gradient(#e9edf0 25%,transparent 0 50%,#e9edf0 0 75%,transparent 0);background-size:24px 24px}.surface img{width:100%;height:100%;object-fit:contain}[data-background=light] .surface{background:#f7f7f5}[data-background=dark] .surface{background:#18202c}table{width:100%;border-collapse:collapse;margin-top:10px;text-align:left}td,th{padding:7px 0;border-bottom:1px solid #394656}small{display:block;line-height:1.5;color:#bdc9d8;margin-top:10px}footer a{margin-right:14px}details{margin-top:12px}body>footer{margin-top:30px;border-top:1px solid #394656;padding-top:12px}@media(max-width:850px){.cards{grid-template-columns:1fr}body{padding:16px}}@media print{.controls{display:none}.cards{grid-template-columns:1fr}article{break-inside:avoid}body{background:white;color:black}}
</style></head><body data-background="checker">
<header><div class="status">CANDIDATE RANK ASSIGNMENTS · 2026-10-09 · APPROVAL PENDING</div>
<h1>Imperial Republic military — enlisted</h1>
<p>E-1 upward through E-7. Ryan selected the Combine grey/blue family shared across Navy, Marine and Army for the first drafts. The titles come from our official source intersection; the artwork and rank associations are candidates.</p>
<p>E-1 uses two grey tiles. E-2 begins with one grey over one blue; each following grade adds a column. <span class="extension">E-7 is a proposed extension: the saved external enlisted family ends at E-6.</span></p>
<p>These are generated material/layout studies. Tile proportions and frame widths still vary; exact composition will be needed before adoption. Images are fitted for review, not shown at one common physical scale. Code cylinders remain separate.</p>
<nav><a href="review.html">Tile palette and earlier studies</a> · <a href="../data/military-enlisted-working.json">Working ranks and ordered patterns</a></nav>
<div class="controls" role="group" aria-label="Preview background"><button data-choice="checker" aria-pressed="true">Checkerboard</button><button data-choice="light" aria-pressed="false">Light</button><button data-choice="dark" aria-pressed="false">Dark</button></div></header>
<main class="cards" id="cards"></main>
<footer><p><a href="render-manifest-2026-10-09.json">Generation prompts and exact provenance</a> · <a href="../docs/MILITARY-BASELINE.md">Military source comparison</a> · <a href="../docs/GOAL-PROMPT.md">Continuation goal prompt</a></p></footer>
<script id="working-data" type="application/json">PAYLOAD</script>
<script>
const data=JSON.parse(document.querySelector('#working-data').textContent);
for(const pattern of data.grade_patterns){
 const article=document.createElement('article');article.dataset.grade=pattern.grade;
 const header=document.createElement('header'), title=document.createElement('h2');title.textContent=pattern.grade+' · '+pattern.expected_tile_count+' tiles';header.append(title);
 const line=document.createElement('div');line.textContent=pattern.tiles.map(row=>row.length+' '+row[0]).join(' over ');header.append(line);
 if(pattern.order_bottom_up===7){const note=document.createElement('small');note.className='extension';note.textContent='Proposed E-7 extension — no matching E-7 plaque in the saved Combine source.';header.append(note);}
 const surface=document.createElement('div');surface.className='surface';const img=document.createElement('img');img.src='../'+pattern.local_image;img.alt=pattern.grade+' candidate: '+line.textContent;surface.append(img);
 const footer=document.createElement('footer'),table=document.createElement('table');table.setAttribute('aria-label',pattern.grade+' branch titles');
 for(const branch of ['navy','marine','army']){const rank=data.rank_records.find(r=>r.grade===pattern.grade&&r.branch===branch),row=document.createElement('tr'),label=document.createElement('th'),cell=document.createElement('td');label.scope='row';label.textContent=branch[0].toUpperCase()+branch.slice(1);cell.textContent=rank.display_title;row.append(label,cell);table.append(row);}
 footer.append(table);const open=document.createElement('a');open.href=img.src;open.target='_blank';open.rel='noopener';open.textContent='Open PNG · v'+pattern.image_version;const save=document.createElement('a');save.href=img.src;save.download='';save.textContent='Save PNG';footer.append(open,save);
 if(pattern.order_bottom_up===7){const note=document.createElement('small');note.textContent='Navy title: Nexus says Flight Sergeant Major; spreadsheet says Fight Sergeant Major. Both source assertions are preserved.';footer.append(note);}
 if(pattern.iteration_history.length){const details=document.createElement('details'),summary=document.createElement('summary');summary.textContent='Earlier iteration retained';details.append(summary);for(const path of pattern.iteration_history){const link=document.createElement('a');link.href='../'+path;link.target='_blank';link.rel='noopener';link.textContent='Open v1';details.append(link);}footer.append(details);}
 article.append(header,surface,footer);document.querySelector('#cards').append(article);
}
for(const button of document.querySelectorAll('[data-choice]'))button.addEventListener('click',()=>{document.body.dataset.background=button.dataset.choice;for(const b of document.querySelectorAll('[data-choice]'))b.setAttribute('aria-pressed',String(b===button));});
</script></body></html>'''.replace('PAYLOAD', payload)
(ROOT / 'assets/military-enlisted-review.html').write_text(html, encoding='utf-8')
print('Built enlisted review: 7 grades, 21 branch records; approval remains pending.')
