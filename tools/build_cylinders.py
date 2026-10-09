#!/usr/bin/env python3
"""Purpose: build separate unassigned candidate code-cylinder components.

Usage: python tools/build_cylinders.py
Prerequisites: Python 3.10+ and Pillow. No network, plaque edits or publication.
Shared vector primitives produce SVG and antialiased RGBA PNG; layout counts
are wearer-relative and never infer rank entitlement from external references.
"""
from __future__ import annotations
import hashlib
import html
import json
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/cylinders/v1'
SCALE = 3


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def primitives(exposed=False):
    """Blue-cap/silver clipped instrument study, not an approved uniform device.

    The exposed version ends at a proposed pocket occlusion line. No pocket or
    fabric is drawn: consumers can position this reusable transparent asset.
    """
    pieces = []
    def shape(kind, box, color):
        pieces.append((kind, box, color))
    def metal(x, y, w, h):
        # Explicit strips preserve the same metal shading in both file formats.
        stops = [(0, 69), (.16, 157), (.3, 224), (.45, 170), (.65, 112), (.82, 197), (1, 74)]
        for i in range(w):
            f = i / max(1, w-1)
            for (a, av), (b, bv) in zip(stops, stops[1:]):
                if a <= f <= b:
                    v = round(av + (bv-av)*(f-a)/(b-a))
                    shape('rect', (x+i, y, 1, h), f'#{v:02x}{min(255,v+5):02x}{min(255,v+9):02x}')
                    break
    # Deliberately narrow instrument silhouette with a distinct spring clip.
    metal(77, 108, 80, 546 if not exposed else 232)
    shape('ellipse', (77, 646, 80, 24), '#818991') if not exposed else None
    shape('rect', (77, 113, 2, 534 if not exposed else 225), '#505a65')
    shape('rect', (150, 116, 3, 530 if not exposed else 224), '#d1d9de')
    metal(69, 83, 96, 37)
    shape('ellipse', (69, 70, 96, 27), '#d0d8df')
    shape('rect', (77, 40, 80, 43), '#25588e')
    shape('ellipse', (77, 27, 80, 26), '#4683bb')
    shape('rect', (83, 43, 11, 34), '#4d8bc0')
    shape('rect', (145, 44, 9, 35), '#12395e')
    shape('ellipse', (84, 30, 65, 11), '#70a5ce')
    metal(155, 96, 17, 177)
    shape('rect', (169, 103, 3, 165), '#606974')
    shape('rect', (154, 259, 18, 14), '#8d99a3')
    shape('rect', (159, 108, 3, 144), '#e4e9ed')
    return pieces


def render(name, width, height, pieces, description, extra=None):
    image = Image.new('RGBA', (width*SCALE, height*SCALE), (0,0,0,0))
    draw = ImageDraw.Draw(image)
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">', f'<title>{html.escape(description)}</title>']
    for kind, (x,y,w,h), fill in pieces:
        bounds = (x*SCALE,y*SCALE,(x+w)*SCALE-1,(y+h)*SCALE-1)
        if kind == 'rect':
            draw.rectangle(bounds, fill=fill)
            svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"/>')
        else:
            draw.ellipse(bounds, fill=fill)
            svg.append(f'<ellipse cx="{x+w/2}" cy="{y+h/2}" rx="{w/2}" ry="{h/2}" fill="{fill}"/>')
    svg.append('</svg>')
    image = image.resize((width,height), Image.Resampling.LANCZOS)
    # Avoid invisible RGB artifacts around reusable alpha edges.
    image.putdata([(0,0,0,0) if p[3] == 0 else p for p in image.get_flattened_data()])
    png_path, svg_path = OUT / f'{name}.png', OUT / f'{name}.svg'
    image.save(png_path)
    svg_path.write_text('\n'.join(svg)+'\n', encoding='utf-8')
    alpha = image.getchannel('A')
    assert alpha.getpixel((0,0)) == 0
    record = dict(id=name, description=description, status='CANDIDATE', approval=None,
                  dimensions=[width,height], png_path=png_path.relative_to(ROOT).as_posix(),
                  svg_path=svg_path.relative_to(ROOT).as_posix(), png_sha256=digest(png_path),
                  svg_sha256=digest(svg_path), alpha_extrema=list(alpha.getextrema()),
                  alpha_bbox=list(alpha.getbbox()) if alpha.getbbox() else None)
    record.update(extra or {})
    return record


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    components = [render('code-cylinder-full-blue-silver-v1',240,720,primitives(),
                         'Unassigned full blue-cap silver clipped code cylinder candidate'),
                  render('code-cylinder-exposed-blue-silver-v1',240,360,primitives(True),
                         'Unassigned pocket-exposed code cylinder candidate; implied occlusion at y=340',
                         dict(proposed_occlusion_y=340, fabric_or_pocket_rendered=False))]
    layouts = []
    for left in range(3):
        for right in range(3):
            pieces, placements = [], []
            # Front view: the wearer's right occupies the viewer's left.
            for count, start, side in [(right,50,'wearer_right'),(left,750,'wearer_left')]:
                for slot in range(count):
                    x = start + slot*130
                    placements.append(dict(side=side,slot=slot,x=x,y=20,width=120,height=180))
                    for kind, (px,py,pw,ph), fill in primitives(True):
                        pieces.append((kind,(x+px/2,20+py/2,pw/2,ph/2),fill))
            layouts.append(render(f'layout-wearer-left-{left}-right-{right}-v1',1080,230,pieces,
                                  f'Front-view candidate layout: wearer left {left}, wearer right {right}',
                                  dict(wearer_left_count=left,wearer_right_count=right,
                                       viewer_left_count=right,viewer_right_count=left,
                                       placements=placements,rank_assignment=None,
                                       layout_state='EXPLICIT_NONE' if left+right == 0 else 'COUNT_LAYOUT',
                                       reserved_center=[350,0,350,230])))
    manifest = dict(schema_version=1,status='CANDIDATE',approval=None,
        coordinate_convention='Front view: wearer left is viewer right; wearer right is viewer left.',
        scope='Separate component/layout candidates only. No ranks, grades, classes or uniforms assigned.',
        source_basis='Blue-cap silver clipped instrument design study, informed by external cylinder references; no exact prop replication claimed.',
        unresolved_state='null count means unresolved; explicit left=0/right=0 means a deliberate no-cylinder layout.',
        raster_method=f'Pillow shared vector primitives rendered at {SCALE}x then LANCZOS downsample; SVG uses same shapes.',
        approval_note='Saving or publishing candidates does not establish Imperial Republic canon.',
        components=components,layouts=layouts)
    path = ROOT/'data/code-cylinder-components.json'
    path.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    cards=[]
    for item in components + layouts:
        png = item['png_path'].removeprefix('assets/')
        svg = item['svg_path'].removeprefix('assets/')
        label = html.escape(item['description'])
        cards.append(f'<article><h2>{label}</h2><div class="preview"><img src="{png}" alt="{label}" width="{item["dimensions"][0]}" height="{item["dimensions"][1]}"></div><p><a href="{png}">Native PNG</a> · <a href="{svg}">SVG</a></p></article>')
    page = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Code cylinder candidates</title><style>
    :root{color-scheme:dark}body{font:13px/1.5 system-ui,sans-serif;color:#dce5ed;background:#10161f;margin:24px auto;padding:0 20px;max-width:1100px}h1{font-size:24px}h2{font-size:13px;font-weight:600}a{color:#8abde8}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:12px}article{padding:12px;border:1px solid #354453;border-radius:6px;background:#17212d}.preview{display:flex;align-items:center;justify-content:center;height:190px;background:#10161f}.preview img{object-fit:contain;max-width:100%;max-height:180px;width:auto;height:auto}.checker .preview{background-color:#18212c;background-image:linear-gradient(45deg,#25313e 25%,transparent 25%),linear-gradient(-45deg,#25313e 25%,transparent 25%),linear-gradient(45deg,transparent 75%,#25313e 75%),linear-gradient(-45deg,transparent 75%,#25313e 75%);background-size:20px 20px;background-position:0 0,0 10px,10px -10px,-10px 0}button{background:#263545;color:#e4edf6;border:1px solid #52657a;padding:5px 9px;border-radius:4px}</style>
    <h1>Code cylinder components · CANDIDATE</h1><p>Separate blue-cap silver device studies and all nine count layouts. No rank, grade, class, uniform or entitlement assignments.</p><p><strong>Front view: wearer left is viewer right.</strong> Empty 0/0 is an explicit no-cylinder option; unresolved mappings remain null. The center is reserved for a future plaque composition and contains no plaque.</p><p>Full device and exposed-pocket views are separate; the latter is clipped at a proposed occlusion line, without invented pocket/fabric. PNGs have real transparency; checkerboard is CSS only.</p><p><a href="../data/code-cylinder-components.json">Manifest and exact hashes</a> · <a href="catalog-review.html">Existing rank catalog</a> <button type="button" onclick="document.body.classList.toggle('checker')">Toggle dark transparency checker</button></p><main>__CARDS__</main></html>'''
    (ROOT/'assets/code-cylinder-review-v1.html').write_text(page.replace('__CARDS__','\n'.join(cards)),encoding='utf-8')
    assert len(layouts)==9 and len({(a['wearer_left_count'],a['wearer_right_count']) for a in layouts})==9
    assert all(a['approval'] is None for a in components+layouts)
    assert layouts[0]['alpha_bbox'] is None and layouts[0]['layout_state']=='EXPLICIT_NONE'
    for item in layouts[1:]:
        assert item['alpha_extrema']==[0,255]
        assert len(item['placements'])==item['wearer_left_count']+item['wearer_right_count']
        image=Image.open(ROOT/item['png_path'])
        assert image.getchannel('A').crop((350,0,700,230)).getbbox() is None
    print(f'PASS: {len(components)} devices, {len(layouts)} independent count layouts; transparent PNG/SVG pairs and null approvals.')


if __name__ == '__main__':
    build()
