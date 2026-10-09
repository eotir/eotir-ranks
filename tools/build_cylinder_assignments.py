"""Build provisional cylinder associations without changing rank or plaque records.

Usage: python tools/build_cylinder_assignments.py
Prerequisites: Python 3; saved catalog, cylinder component and image-evidence JSON.
External chart omissions are not entitlement rules. Bridges below are proposals.
"""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))

def build():
    catalog = read('data/rank-catalog.json')
    evidence = read('docs/research/code-cylinder-image-evidence.json')
    components = read('data/code-cylinder-components.json')
    observations = evidence['whatsahonda_military_observations']
    by_title = {(o['external_branch'], o['external_title']): i for i, o in enumerate(observations)}
    # Match titles within branches, never matching an Army Captain to Navy Captain.
    equivalents = {
        'Lieutenant Junior Grade': 'Ensign', 'Line Captain': 'Captain',
        'Third Lieutenant': 'Junior Lieutenant', 'Second Lieutenant': 'Junior Lieutenant',
        'First Lieutenant': 'Lieutenant', 'Lieutenant Colonel': 'Major',
    }
    records = []
    for rank in catalog['rank_records'] + catalog['shared_records']:
        branch = rank.get('branch_id', 'shared')
        item = {'rank_id': rank['id'], 'branch_id': branch, 'grade': rank['grade'],
                'title': rank['title_display'], 'status': 'CANDIDATE', 'approval': None,
                'canonical': False, 'layout_id': None, 'wearer_left_count': None,
                'wearer_right_count': None, 'basis': 'UNRESOLVED', 'source_observations': [],
                'notes': []}
        if branch in ('navy', 'marine', 'army'):
            family = rank['grade'].split('-')[0]
            ext_branch = 'Imperial Navy' if branch == 'navy' else 'Imperial Army'
            title = rank['title_display']
            external_title = equivalents.get(title, title)
            index = by_title.get((ext_branch, external_title))
            if index is not None:
                obs = observations[index]
                left, right = obs['viewer_right'], obs['viewer_left']
                item['basis'] = 'EXTERNAL_TITLE_COMPARISON' if external_title == title and branch != 'marine' else 'PROPOSED_TITLE_BRIDGE'
                item['source_observations'] = [{
                    'file': 'docs/research/code-cylinder-image-evidence.json',
                    'json_pointer': f'/whatsahonda_military_observations/{index}',
                    'external_branch': ext_branch, 'external_title': external_title,
                    'observed_viewer_left': obs['viewer_left'], 'observed_viewer_right': obs['viewer_right'],
                }]
                item['notes'].append('Candidate front-view convention: chart viewer-left becomes wearer-right. The source does not specify wearer sides.')
                if item['basis'] == 'PROPOSED_TITLE_BRIDGE':
                    item['notes'].append('Title/branch analogy is a proposed adaptation, not an externally documented Imperial Republic assignment.')
            elif family == 'E':
                left, right = 0, 0
                item['basis'] = 'PROPOSED_ENLISTED_NONE'
                item['notes'].append('Provisional no-cylinder service layout for review. External enlisted omission does not prove zero entitlement; cylinder-bearing duty variants remain open.')
            else:
                left, right = 2, 2
                item['basis'] = 'PROPOSED_UPPER_EXTENSION'
                item['notes'].append('Unmatched military title: propose the four-device senior family without inventing higher counts. No direct source rank match; approval required.')
            item.update(wearer_left_count=left, wearer_right_count=right,
                        layout_id=f'layout-wearer-left-{left}-right-{right}-v1')
        else:
            item['notes'].append('No researched Imperial Republic branch-specific cylinder mapping. Do not inherit military counts from grade or matching title alone.')
        records.append(item)
    layout_ids = {l['id'] for l in components['layouts']}
    assert len(records) == 217 and len({r['rank_id'] for r in records}) == 217
    assert all(r['layout_id'] is None or r['layout_id'] in layout_ids for r in records)
    assert sum(r['layout_id'] is not None for r in records) == 69
    output = {
        'schema_version': 1, 'date': '2026-10-09', 'status': 'CANDIDATE', 'approval': None,
        'canonical': False, 'published': False,
        'coordinate_convention': 'Front view: wearer left = viewer right. This is a proposed chart convention, not recovered source authority.',
        'scope': '69 military proposals, with all other populated and shared rank records explicitly unresolved; blank source cells are not ranks.',
        'alternatives': [
            {'id': 'saxton-sequence', 'url': 'https://www.theforce.net/swtc/insignia/cylinders.html',
             'total_to_wearer_counts': {'1': [1, 0], '2': [1, 1], '3': [2, 1], '4': [2, 2]},
             'status': 'EXTERNAL_COMPARISON_ONLY', 'note': 'Three-device asymmetry opposes the proposed frontal interpretation of the supplied Whatsahonda chart.'},
            {'id': 'duty-clearance', 'status': 'UNASSIGNED_ALTERNATIVE',
             'note': 'Keep device issue keyed to uniform/duty/access scope rather than a universal grade entitlement.'},
        ],
        'input_hashes': {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in (
            'data/rank-catalog.json', 'data/code-cylinder-components.json',
            'docs/research/code-cylinder-image-evidence.json')},
        'assignments': records,
        'coverage': {'military_proposals': 69, 'unresolved_other_and_shared': 148,
                     'source_blank_cells_preserved': len(catalog['blank_cells'])},
    }
    (ROOT / 'data/code-cylinder-assignments.json').write_text(json.dumps(output, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(json.dumps(output['coverage']))

if __name__ == '__main__':
    build()
