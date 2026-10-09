"""Independently check candidate cylinder assets, side conventions and source joins.

Usage: python tools/verify_cylinders.py
Prerequisites: Python 3 and Pillow; build_cylinders/build_cylinder_assignments outputs.
This verifies technical consistency, not visual approval or uniform entitlement.
"""
from pathlib import Path
import hashlib
import json
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))

def main():
    components = read('data/code-cylinder-components.json')
    assignments = read('data/code-cylinder-assignments.json')
    catalog = read('data/rank-catalog.json')
    evidence = read('docs/research/code-cylinder-image-evidence.json')
    layouts = {l['id']: l for l in components['layouts']}
    assert len(components['components']) == 2 and len(layouts) == 9
    for asset in components['components'] + list(layouts.values()):
        assert asset['status'] == 'CANDIDATE' and asset['approval'] is None
        for ext in ('png', 'svg'):
            assert hashlib.sha256((ROOT / asset[ext + '_path']).read_bytes()).hexdigest() == asset[ext + '_sha256']
        with Image.open(ROOT / asset['png_path']) as image:
            assert image.mode == 'RGBA' and list(image.size) == asset['dimensions']
            assert list(image.getchannel('A').getextrema()) == asset['alpha_extrema']
        if 'wearer_left_count' in asset:
            assert asset['viewer_left_count'] == asset['wearer_right_count']
            assert asset['viewer_right_count'] == asset['wearer_left_count']
            assert len(asset['placements']) == asset['wearer_left_count'] + asset['wearer_right_count']
            assert (asset['alpha_bbox'] is None) == (asset['wearer_left_count'] + asset['wearer_right_count'] == 0)
    ranks = {r['id']: r for r in catalog['rank_records'] + catalog['shared_records']}
    assert len(assignments['assignments']) == len(ranks) == 217
    assert {a['rank_id'] for a in assignments['assignments']} == set(ranks)
    military = 0
    for item in assignments['assignments']:
        assert item['approval'] is None and not item['canonical']
        rank = ranks[item['rank_id']]
        assert item['grade'] == rank['grade'] and item['title'] == rank['title_display']
        if item['layout_id'] is None:
            assert item['wearer_left_count'] is None and item['wearer_right_count'] is None
            assert item['basis'] == 'UNRESOLVED'
        else:
            military += 1
            assert rank['branch_id'] in ('navy', 'marine', 'army')
            layout = layouts[item['layout_id']]
            assert item['wearer_left_count'] == layout['wearer_left_count']
            assert item['wearer_right_count'] == layout['wearer_right_count']
            for source in item['source_observations']:
                index = int(source['json_pointer'].rsplit('/', 1)[1])
                observed = evidence['whatsahonda_military_observations'][index]
                assert source['external_title'] == observed['external_title']
                assert item['wearer_left_count'] == observed['viewer_right']
                assert item['wearer_right_count'] == observed['viewer_left']
    assert military == 69
    for path, expected in assignments['input_hashes'].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected
    print(json.dumps({'status': 'PASS', 'device_views': 2, 'layouts': 9,
                      'military_proposals': military, 'unresolved': 148,
                      'creative_approval': False}))

if __name__ == '__main__':
    main()
