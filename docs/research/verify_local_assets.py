"""Verify local evidence and candidate provenance without modifying image pixels.

Usage: python docs/research/verify_local_assets.py
Prerequisites: Python 3, Pillow. Run inside the ranks workspace.
Writes metadata/QC only; fails visibly for changed sources or missing outputs.
"""
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    inventory = json.loads((ROOT / 'docs/research/source-inventory.json').read_text(encoding='utf-8'))
    for entry in inventory['files']:
        assert sha256(ROOT / entry['path']) == entry['sha256'], f"Source bytes changed: {entry['path']}"
    renames = json.loads((ROOT / 'docs/research/file-renames-2026-10-09.json').read_text(encoding='utf-8'))
    for entry in renames:
        assert entry['sha256_before'] == entry['sha256_after'] == sha256(ROOT / entry['new_path']), entry
    for folder in ('official', 'references'):
        for path in (ROOT / folder).rglob('*'):
            if path.is_file():
                # Validate the supplied evidence inventory, preserving unrelated concurrent downloads.
                if path.relative_to(ROOT).as_posix() not in {e['path'] for e in inventory['files']}:
                    continue
                assert re.fullmatch(r'[a-z0-9_.-]+', path.name), f'Unsafe filename: {path}'

    manifest_path = ROOT / 'assets/render-manifest-2026-10-09.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    for entry in manifest['entries']:
        path = ROOT / entry['local_path']
        entry['sha256'] = sha256(path)
        original = Path(entry['generator_original_path'])
        assert sha256(original) == entry['sha256'], f'Generator copy differs: {path}'
        entry['local_copy_matches_generator_bytes'] = True
        for reference in entry['references']:
            assert (ROOT / reference).is_file(), f'Missing reference: {reference}'
        entry['reference_sha256'] = {ref: sha256(ROOT / ref) for ref in entry['references']}
        with Image.open(path) as image:
            assert image.mode == 'RGBA', f'Expected alpha channel: {path}'
            alpha = image.getchannel('A')
            histogram = alpha.histogram()
            entry['width'], entry['height'] = image.size
            entry['mode'] = image.mode
            entry['bytes'] = path.stat().st_size
            entry['alpha_extrema'] = list(alpha.getextrema())
            entry['alpha_nonzero_bbox'] = list(alpha.getbbox())
            entry['fully_transparent_pixel_fraction'] = round(histogram[0] / (image.width * image.height), 6)
            entry['corner_alpha'] = [alpha.getpixel(p) for p in [(0, 0), (image.width-1, 0), (0, image.height-1), (image.width-1, image.height-1)]]
            # Alpha presence proves a transparent canvas, not clean visual edges.
            entry['transparency_visual_approval'] = None
            assert histogram[0] > 0, f'No fully transparent pixels: {path}'
    working_rank_count = 0
    working_path = ROOT / 'data/military-enlisted-working.json'
    if working_path.exists():
        working = json.loads(working_path.read_text(encoding='utf-8'))
        assert working['canonical'] is False and working['published'] is False
        assert len(working['grade_patterns']) == 7 and len(working['rank_records']) == 21
        assert [p['grade'] for p in working['grade_patterns']] == [f'E-{n}' for n in range(1, 8)]
        assert len({r['working_id'] for r in working['rank_records']}) == 21
        for pattern in working['grade_patterns']:
            entry = next(e for e in manifest['entries'] if e['local_path'] == pattern['local_image'])
            assert pattern['tiles'] == pattern['observed_pattern'] == entry['observed_pattern']
            assert pattern['expected_tile_count'] == sum(map(len, pattern['tiles']))
            assert pattern['visual_count_and_order_verified'] and pattern['approval'] is None
        for rank in working['rank_records']:
            assert rank['assignment_approval'] is None and rank['assignment_status'] == 'CANDIDATE'
            for assertion in rank['source_assertions']:
                capture = json.loads((ROOT / assertion['capture']).read_text(encoding='utf-8'))
                if assertion['source'] == 'Nexus':
                    row = capture['tables'][assertion['table_index']][assertion['row_index_zero_based']]
                    assert row[0]['text'] == rank['grade'] and row[assertion['cell_index_zero_based']]['text'] == assertion['title'] == rank['display_title']
                else:
                    sheet = next(s for s in capture['sheets'] if s['title'] == 'IRAF Pay Scale')
                    row = next(r for r in sheet['rows'] if r['row'] == int(assertion['cell'][1:]))
                    column = ord(assertion['cell'][0]) - ord('A')
                    assert row['values'][1] == rank['grade'] and row['values'][column] == assertion['title']
                    assert assertion['struck'] == (column+1 in row['struck_columns'])
        working_rank_count = len(working['rank_records'])
        manifest['approved_rank_assignments'] = manifest.pop('rank_assignments', [])
        manifest['draft_rank_assignment_dataset'] = 'data/military-enlisted-working.json'
    manifest_path.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')

    local_links = 0
    for path in ROOT.rglob('*.md'):
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
            target = target.strip().strip('<>').split('#', 1)[0]
            if not target or re.match(r'[a-zA-Z]+:', target):
                continue
            assert (path.parent / unquote(target)).exists(), f'Broken link in {path}: {target}'
            local_links += 1
    report = {
        'date': '2026-10-09', 'source_files_unchanged': len(inventory['files']),
        'renames_byte_verified': len(renames), 'candidate_pngs_verified': len(manifest['entries']),
        'local_markdown_links_verified': local_links, 'creative_approval': 'pending',
        'candidate_rank_assignments_verified': working_rank_count,
        'approved_rank_assignments': 0, 'image_pixels_modified_by_verifier': False
    }
    (ROOT / 'docs/research/local-verification-2026-10-09.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report))
    for entry in manifest['entries']:
        print(entry['id'], entry['width'], entry['height'], entry['alpha_extrema'], entry['corner_alpha'])


if __name__ == '__main__':
    main()
