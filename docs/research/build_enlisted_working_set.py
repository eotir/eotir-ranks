"""Build source-backed E-1…E-7 review records with proposed plaque assignments.

Usage: python docs/research/build_enlisted_working_set.py
Prerequisites: Python 3 and the saved Nexus/Google/Combine research JSON.
Writes working data only; never modifies canon-service or source evidence.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main():
    nexus = json.loads((ROOT / 'docs/research/nexus-table-2026-10-09.json').read_text(encoding='utf-8'))
    sheets = json.loads((ROOT / 'docs/research/google-sheets-live-2026-10-09.json').read_text(encoding='utf-8'))
    sheet = next(s for s in sheets['sheets'] if s['title'] == 'IRAF Pay Scale')
    refs = json.loads((ROOT / 'docs/research/combine-saved-plaques.json').read_text(encoding='utf-8'))
    grades, ranks = [], []
    for number in range(1, 8):
        grade = f'E-{number}'
        row_index, row = next((i, r) for i, r in enumerate(nexus['tables'][0]) if r and r[0]['text'] == grade)
        source_row = next(r for r in sheet['rows'] if r['values'][1] == grade)
        # Preserve the source's E-1 exception; the grey-over-blue ladder starts at E-2.
        pattern = [['grey', 'grey']] if number == 1 else [['grey'] * (number-1), ['blue'] * (number-1)]
        source_reference = next((r['url'] for r in refs if r['url'].endswith(f'/ME-{number}.gif')), None)
        pattern_id = f'military-enlisted-e{number}-grey-blue-v1'
        grades.append({
            'grade': grade, 'order_bottom_up': number, 'pattern_id': pattern_id,
            'status': 'CANDIDATE', 'approval': None, 'shared_branches': ['navy', 'marine', 'army'],
            'tiles': pattern, 'expected_tile_count': sum(map(len, pattern)),
            'source_design_url': source_reference,
            'design_basis': 'Proposed extension of the saved Combine family; no E-7 source design.' if number == 7 else 'Combine-inspired adaptation to Imperial Republic grade positions; external titles are not imported.',
            'local_image': f'assets/plaques/candidates/2026-10-09/enlisted/military-enlisted-e{number}-v1.png',
            'observed_pattern': None, 'visual_count_and_order_verified': False
        })
        for branch, nexus_column, sheet_column, sheet_letter in [('navy', 1, 2, 'C'), ('marine', 2, 4, 'E'), ('army', 3, 6, 'G')]:
            title = row[nexus_column]['text']
            raw_sheet_title = source_row['values'][sheet_column]
            ranks.append({
                'working_id': f'imperial-republic-{branch}-e{number}', 'branch': branch, 'grade': grade,
                'display_title': title, 'draft_pattern_id': pattern_id,
                'assignment_status': 'CANDIDATE', 'assignment_approval': None,
                'source_assertions': [
                    {'source': 'Nexus', 'title': title, 'grade': grade, 'capture': 'docs/research/nexus-table-2026-10-09.json', 'table_index': 0, 'row_index_zero_based': row_index, 'cell_index_zero_based': nexus_column},
                    {'source': 'IRAF Pay Scale', 'title': raw_sheet_title, 'grade': grade, 'capture': 'docs/research/google-sheets-live-2026-10-09.json', 'gid': 11, 'cell': f"{sheet_letter}{source_row['row']}", 'grade_cell': f"B{source_row['row']}", 'struck': sheet_column+1 in source_row['struck_columns']}
                ],
                'title_note': 'Nexus Flight / sheet Fight discrepancy retained; no source correction performed.' if number == 7 and branch == 'navy' else ('Abbreviated source spelling retained.' if title != raw_sheet_title else None)
            })
    assert len(grades) == 7 and len(ranks) == 21
    data = {
        'schema_version': 1, 'date': '2026-10-09', 'status': 'CANDIDATE',
        'direction': "Ryan selected Combine grey/blue family, shared across military grades, for first drafts.",
        'direction_is_visual_approval': False, 'canonical': False, 'published': False,
        'scope': 'First bottom-up enlisted review batch; not the complete military chart.',
        'grade_patterns': grades, 'rank_records': ranks
    }
    output = ROOT / 'data/military-enlisted-working.json'
    output.parent.mkdir(exist_ok=True)
    if output.exists():
        raise FileExistsError('Working data already exists; preserve its QC and history rather than rebuilding blindly.')
    output.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
    print(f'Created {len(grades)} candidate patterns and {len(ranks)} source-backed working rank records.')


if __name__ == '__main__':
    main()
