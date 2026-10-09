"""Build the focused Claude Design rank UI from authoritative candidate datasets.

Usage: called by build_review.py (including --html-only). Python 3 required.
The checked-in compiled UI avoids network/runtime Babel; rank-ui.jsx is its source.
To edit JSX, compile with Babel's React preset using a local development tool.
This adapter never adopts the design export's lore, ranks or synthetic plaques.
"""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
def read(path):
    return json.loads((ROOT/path).read_text(encoding='utf-8-sig'))
def build_site(legacy_page,catalog,composition,charts):
    items=composition['patterns']
    assets={a['id']:{'w':a['width'],'h':a['height']} for a in (items.values() if isinstance(items,dict) else items)}
    def record(r):
        return dict(id=r['id'],b=r.get('branch_id') or 'shared',g=r['grade'],t=r['title_display'],raw=r['title_raw'],p=r['pattern_id'],alt=r.get('alternative_pattern_ids',[]),n=r.get('candidate_notes',[]),src=[dict(s=a.get('source','Source'),u=a.get('url',''),g=a.get('grade',''),t=a.get('title',''),c=a.get('cell') or 'row '+str(a.get('row_index_zero_based','?'))+', cell '+str(a.get('cell_index_zero_based','?')),x=a.get('struck',False),raw=a) for a in r.get('source_assertions',[])])
    data=dict(date=catalog['date'],coverage={**catalog['coverage'],'per_branch':[{**b,'branch_id':b['branch_id']} for b in catalog['coverage']['per_branch']]},branches=catalog['branches'],grades=catalog['grades'],patterns={p['id']:dict(rows=p['rows'],basis=p.get('design_basis',''),notes=p.get('adaptation_notes',[]),refs=p.get('reference_urls',[])) for p in catalog['patterns']},records=[record(r) for r in catalog['rank_records']],shared=[record(r) for r in catalog['shared_records']],blanks=[dict(b=b['branch_id'],g=b['grade'],raw=b) for b in catalog['blank_cells']],assets=assets,charts=charts['charts'])
    for filename,key in [('data/code-cylinder-assignments.json','cylinders'),('data/code-cylinder-components.json','cylinder_components')]:
        if (ROOT/filename).is_file():data[key]=read(filename)
    js='window.RANKS_DATA='+json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')+';\n'
    (ROOT/'assets/site/rank-data.js').write_text(js,encoding='utf-8')
    # Retain a full, auditable HTML fallback and original data payload. It is also
    # usable when JS is disabled; existing independent provenance verification
    # must keep checking all 283 identities rather than just visible UI rows.
    fallback=re.search(r'<main>(.*?)</main>',legacy_page,re.S).group(1)
    fallback=re.sub(r'<script\b[^>]*>.*?</script>','',fallback,flags=re.S)
    fallback=re.sub(r'</?noscript\b[^>]*>','',fallback)
    payload=re.search(r'(<script[^>]+type="application/json".*?</script>)',legacy_page,re.S).group(1)
    return '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Imperial Republic · Rank Plaque Catalog</title><link rel="stylesheet" href="site/rank-catalog.css"></head><body><div id="root"><p class="rk-error">Loading rank review… If this persists, open the saved datasets or enable JavaScript.</p></div><noscript><main>'''+fallback+'''</main></noscript>'''+payload+'''<script src="site/vendor/react-18.3.1.js"></script><script src="site/vendor/react-dom-18.3.1.js"></script><script src="site/rank-data.js"></script><script src="site/rank-ui.js"></script></body></html>'''
