#!/usr/bin/env python3
"""Purpose: assemble CANDIDATE plaques from preserved local tile renders.

Usage: python tools/compose_assets.py [--components-only] [--verify]
Prerequisites: Python 3.10+, Pillow; data/rank-catalog.json for full assembly.
No image generation, canon publication, external writes, or original edits occur.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import html
import io
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

from PIL import Image, ImageChops, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
COMPONENT_DIR = ROOT / 'assets/components/v1'
OUTPUT_DIR = ROOT / 'assets/composed'
TW, TH, GAP, MARGIN, PADDING = 160, 270, 10, 12, 4
TOKENS = ('red', 'blue', 'gold', 'green', 'orange', 'white', 'charcoal',
          'black', 'bright-white', 'grey', 'purple', 'silver', 'metallic-gold',
          'cyan', 'teal', 'amber')
GEOMETRY = dict(tile_width=TW, tile_height=TH, gap=GAP, margin=MARGIN,
                transparent_padding=PADDING, plate_rim=3, plate_chamfer=5,
                alignment='center each row; ordered left-to-right, top-to-bottom')


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def central_run(values: list[int], center: int, threshold: int = 180) -> tuple[int, int]:
    """Ignore faint distant halo pixels instead of using alpha's noisy bbox."""
    if values[center] < threshold:
        raise ValueError('Tile center is unexpectedly translucent')
    first = last = center
    while first > 0 and values[first - 1] >= threshold:
        first -= 1
    while last + 1 < len(values) and values[last + 1] >= threshold:
        last += 1
    return first, last + 1


def chamfer_polygon(x: int, y: int, width: int, height: int, cut: int) -> list[tuple[int, int]]:
    # Inclusive raster coordinates are also explicit SVG polygon coordinates.
    right, bottom = x + width - 1, y + height - 1
    return [(x+cut,y), (right-cut,y), (right,y+cut), (right,bottom-cut),
            (right-cut,bottom), (x+cut,bottom), (x,bottom-cut), (x,y+cut)]


def make_components() -> list[dict]:
    COMPONENT_DIR.mkdir(parents=True, exist_ok=True)
    originals = json.loads((ROOT / 'assets/render-manifest-2026-10-09.json').read_text(encoding='utf-8'))
    known = {e['local_path']: e['sha256'] for e in originals['entries']}
    result = []
    for token in TOKENS:
        filename = {'red':'tile-red-v2.png', 'bright-white':'tile-white-v2.png',
                    'white':'tile-white-v1.png'}.get(token, f'tile-{token}-v1.png')
        original = ROOT / 'assets/tiles/candidates/2026-10-09' / filename
        original_hash = sha(original)
        if known.get(rel(original)) != original_hash:
            raise ValueError(f'Original hash differs from provenance manifest: {original}')
        source = Image.open(original).convert('RGBA')
        alpha = source.getchannel('A')
        cx, cy = source.width // 2, source.height // 2
        left, right = central_run(list(alpha.crop((0,cy,source.width,cy+1)).get_flattened_data()), cx)
        top, bottom = central_run(list(alpha.crop((cx,0,cx+1,source.height)).get_flattened_data()), cy)
        # Fit the physical rim, retaining its RGB texture and highlights. Original
        # alpha 254 is a generator artifact, so use a geometric silhouette rather
        # than making the face translucent over each background/backplate.
        crop = (left, top, right, bottom)
        clean = source.crop(crop)
        cut = 34
        mask = Image.new('L', clean.size, 0)
        ImageDraw.Draw(mask).polygon(chamfer_polygon(0,0,*clean.size,cut), fill=255)
        clean.putalpha(mask)
        native_path = COMPONENT_DIR / f'{token}-clean-native.png'
        normal_path = COMPONENT_DIR / f'{token}.png'
        clean.save(native_path)
        normal = clean.resize((TW, TH), Image.Resampling.LANCZOS)
        # Removing hidden color at alpha=0 prevents invisible fringes in consumers
        # that interpolate straight RGBA instead of premultiplied alpha.
        pixels = list(normal.get_flattened_data())
        normal.putdata([(0,0,0,0) if p[3] == 0 else p for p in pixels])
        normal.save(normal_path)
        if sha(original) != original_hash:
            raise ValueError(f'Original changed during build: {original}')
        result.append(dict(token=token, original_path=rel(original), original_sha256=original_hash,
            original_hash=original_hash, original_dimensions=list(source.size),
            original_alpha_extrema=list(alpha.getextrema()), normalized_path=rel(normal_path),
            normalized_sha256=sha(normal_path), normalized_hash=sha(normal_path),
            native_clean_path=rel(native_path), native_clean_sha256=sha(native_path),
            width=TW, height=TH, dimensions=[TW,TH], alpha_extrema=list(normal.getchannel('A').getextrema()),
            crop=list(crop), crop_method='alpha >=180 contiguous center row/column physical silver-rim fit',
            alpha_method='fitted chamfer polygon: opaque interior; outside alpha=0; LANCZOS edge antialiasing',
            native_chamfer_pixels=cut, resampling='Pillow LANCZOS, premultiplied alpha',
            rgb_method='unchanged native crop RGB; scale only, no recolor or texture regeneration',
            status='CANDIDATE', approval=None))
    return result


def plate_geometry(rows: list[list[str]]) -> tuple[int, int, list[dict]]:
    ncols = max(map(len, rows))
    inner_width = ncols * TW + (ncols-1) * GAP
    width = inner_width + 2 * (MARGIN+PADDING)
    height = len(rows) * TH + (len(rows)-1) * GAP + 2 * (MARGIN+PADDING)
    boxes = []
    for r, row in enumerate(rows):
        rw = len(row)*TW + (len(row)-1)*GAP
        start = PADDING + MARGIN + (inner_width-rw)//2
        for c, token in enumerate(row):
            boxes.append(dict(row=r,column=c,token=token,x=start+c*(TW+GAP),
                              y=PADDING+MARGIN+r*(TH+GAP),width=TW,height=TH))
    return width, height, boxes


def backplate(width: int, height: int) -> tuple[Image.Image, list[dict]]:
    """Thin manufactured metal, with shared polygon definitions for PNG/SVG.

    Integer rows avoid renderer-dependent gradient/filter differences. They also
    make every plate pixel reproducible by the independent verifier.
    """
    image = Image.new('RGBA', (width,height), (0,0,0,0))
    draw = ImageDraw.Draw(image)
    p = PADDING
    layers = [dict(points=chamfer_polygon(p,p,width-2*p,height-2*p,5),fill='#42474c'),
              dict(points=chamfer_polygon(p+1,p+1,width-2*p-2,height-2*p-2,4),fill='#d4d9dc'),
              dict(points=chamfer_polygon(p+3,p+3,width-2*p-6,height-2*p-6,3),fill='#555c63')]
    for layer in layers:
        draw.polygon(layer['points'], fill=layer['fill'])
    # Subtle brushed center field. It is behind the reused tiles, never painted
    # onto them, and has no thick raised decorative border.
    stripes = []
    for y in range(p+7, height-p-7):
        fraction = (y-p)/(height-2*p)
        v = round(116 - 20*fraction) + (1 if y % 4 == 0 else 0)
        fill = f'#{v:02x}{v+4:02x}{v+7:02x}'
        x0, x1 = p+4, width-p-5
        draw.line((x0,y,x1,y), fill=fill, width=1)
        stripes.append(dict(x=x0,y=y,width=x1-x0+1,height=1,fill=fill))
    return image, layers + [dict(stripes=stripes)]


def compose_pattern(pattern: dict, components: dict[str,dict]) -> dict:
    pid, rows = pattern['id'], pattern['rows']
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]*',pid):
        raise ValueError(f'Unsafe pattern id: {pid}')
    if not rows or any(not row for row in rows):
        raise ValueError(f'Empty pattern rows: {pid}')
    if any(token not in components for row in rows for token in row):
        raise ValueError(f'Unknown tile token: {pid}')
    width, height, boxes = plate_geometry(rows)
    png, layers = backplate(width,height)
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
             f'<title>{html.escape(pid)} — Imperial Republic CANDIDATE plaque</title>',
             '<desc>Exact local normalized tile PNG components on a procedural thin silver backplate. No canon or creative approval.</desc>',
             '<g id="backplate" shape-rendering="crispEdges">']
    for layer in layers:
        if 'points' in layer:
            points = ' '.join(f'{x},{y}' for x,y in layer['points'])
            parts.append(f'<polygon points="{points}" fill="{layer["fill"]}"/>')
        else:
            for s in layer['stripes']:
                parts.append(f'<rect x="{s["x"]}" y="{s["y"]}" width="{s["width"]}" height="1" fill="{s["fill"]}"/>')
    parts.append('</g><g id="exact-tiles">')
    for box in boxes:
        component = components[box['token']]
        path = ROOT / component['normalized_path']
        tile = Image.open(path).convert('RGBA')
        png.alpha_composite(tile,(box['x'],box['y']))
        uri = 'data:image/png;base64,' + base64.b64encode(path.read_bytes()).decode('ascii')
        parts.append(f'<image data-token="{box["token"]}" data-sha256="{component["normalized_sha256"]}" x="{box["x"]}" y="{box["y"]}" width="{TW}" height="{TH}" href="{uri}" xlink:href="{uri}"/>')
    parts.append('</g></svg>')
    png_path, svg_path = OUTPUT_DIR/f'{pid}.png', OUTPUT_DIR/f'{pid}.svg'
    png.save(png_path)
    svg_path.write_text('\n'.join(parts)+'\n',encoding='utf-8')
    return dict(id=pid, rows=rows, png_path=rel(png_path), svg_path=rel(svg_path),
                width=width,height=height,sha256_png=sha(png_path),sha256_svg=sha(svg_path),
                tile_count=len(boxes),tile_boxes=boxes,alpha_extrema=list(png.getchannel('A').getextrema()),
                status='CANDIDATE',approval=None)


def verify(manifest: dict) -> dict:
    components = {c['token']:c for c in manifest['components']}
    counts = 0
    for c in components.values():
        assert sha(ROOT/c['original_path']) == c['original_sha256'], c['token']
        assert sha(ROOT/c['normalized_path']) == c['normalized_sha256'], c['token']
        tile = Image.open(ROOT/c['normalized_path']).convert('RGBA')
        assert tile.size == (TW,TH)
        assert tile.getchannel('A').getextrema() == (0,255)
    for p in manifest['patterns']:
        width,height,boxes = plate_geometry(p['rows'])
        assert (width,height) == (p['width'],p['height']) and boxes == p['tile_boxes'], p['id']
        expected,_ = backplate(width,height)
        for b in boxes:
            expected.alpha_composite(Image.open(ROOT/components[b['token']]['normalized_path']).convert('RGBA'),(b['x'],b['y']))
            counts += 1
        # Verify embedded bytes and ordered placements separately from the PNG
        # reconstruction so an SVG export cannot silently diverge from its pair.
        svg = ET.parse(ROOT/p['svg_path']).getroot()
        assert (int(svg.attrib['width']), int(svg.attrib['height'])) == (width, height), p['id']
        images = svg.findall('.//{http://www.w3.org/2000/svg}image')
        assert len(images) == len(boxes), p['id']
        for embedded, box in zip(images, boxes):
            component = components[box['token']]
            assert embedded.attrib['data-token'] == box['token'], p['id']
            assert all(int(embedded.attrib[key]) == box[key] for key in ('x', 'y', 'width', 'height')), p['id']
            assert embedded.attrib['data-sha256'] == component['normalized_sha256'], p['id']
            payload = base64.b64decode(embedded.attrib['href'].split(',', 1)[1], validate=True)
            assert payload == (ROOT/component['normalized_path']).read_bytes(), p['id']
        actual = Image.open(ROOT/p['png_path']).convert('RGBA')
        assert ImageChops.difference(expected,actual).getbbox(alpha_only=False) is None,p['id']
        assert sha(ROOT/p['png_path']) == p['sha256_png'] and sha(ROOT/p['svg_path']) == p['sha256_svg'],p['id']
        assert actual.getpixel((0,0))[3] == 0 and actual.getchannel('A').getextrema() == (0,255)
    return dict(components=len(components),patterns=len(manifest['patterns']),tile_placements=counts,
                original_bytes_preserved=True,exact_component_placement=True,geometry_valid=True,
                png_alpha_valid=True,hashes_valid=True,svg_order_geometry_and_embedded_bytes_valid=True,creative_approval=False)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--components-only',action='store_true')
    parser.add_argument('--verify',action='store_true')
    args = parser.parse_args()
    OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
    components = make_components()
    design = dict(schema_version=1,date='2026-10-09',version='v1',status='CANDIDATE',approval=None,
        geometry=GEOMETRY,units='raster pixels; physical dimensions and entitlement remain undecided',
        component_rules='Preserved generated texture and metal rims. No redraw, new heraldry, cylinders, or semantic palette approval.',
        normalization='Per-input physical rim crop, opaque fitted 34px chamfer silhouette, same 160x270 tile ratio (16:27).',
        token_mapping={c['token']:c['original_path'] for c in components},
        backplate_recipe='Nested chamfered polygons at padding4/insets0,1,3; 1px procedural brushed stripes. Source tiles alpha-composited last.',
        transparency='Only silhouette edges antialiased; all exterior pixels alpha0; core tile face alpha255.',
        candidate_limitations=['Texture and bevel are selected draft material only; no creative approval.',
            'Original per-color face microgeometry is retained; outer footprint normalized.',
            'SVG and PNG use identical component bytes and placements; edge rasterization can differ by SVG renderer.'])
    write_json(ROOT/'assets/design-system.json',design)
    patterns = []
    catalog_path = ROOT/'data/rank-catalog.json'
    if not args.components_only:
        if not catalog_path.is_file():
            raise FileNotFoundError('Component library ready; full assembly requires data/rank-catalog.json')
        catalog = json.loads(catalog_path.read_text(encoding='utf-8'))
        for p in catalog['patterns']:
            patterns.append(compose_pattern(p,{c['token']:c for c in components}))
    manifest = dict(schema_version=1,date='2026-10-09',status='CANDIDATE',approval=None,
        design_system_path='assets/design-system.json',components=components,patterns=patterns,
        composition_tool='tools/compose_assets.py; Python/Pillow deterministic direct assembly',
        geometry=GEOMETRY,catalog_path=rel(catalog_path) if catalog_path.is_file() else None,
        catalog_sha256=sha(catalog_path) if catalog_path.is_file() else None,
        data_availability='components-only' if args.components_only else 'catalog patterns complete')
    manifest['technical_qc'] = verify(manifest)
    write_json(OUTPUT_DIR/'manifest.json',manifest)
    print(json.dumps(manifest['technical_qc']))


if __name__ == '__main__':
    main()
