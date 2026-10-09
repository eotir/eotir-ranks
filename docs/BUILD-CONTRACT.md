# Candidate build contract — active full-chart goal

Date: 2026-10-09. Status: engineering contract for draft production, not canon.

## Ownership and shared interface

- Catalog/research worker: tools/build_catalog.py, data/rank-catalog.json, docs/PATTERN-RATIONALE.md, docs/research/full-chart-reference*.json/md.
- Composition worker: tools/compose_assets.py, assets/components/, assets/composed/, assets/design-system.json. Never edit the catalog or original candidates.
- Review/chart worker: tools/build_review.py, assets/catalog-review.html, assets/charts/, tools/verify_catalog.py. Never edit catalog/composition data; generate consumer outputs from them.
- Root: repository setup, integration staging, shared docs, main review navigation, final independent audit.

Workers preserve others' edits. No canonical/production writes. All records/designs/assignments remain CANDIDATE with approval null.

## Catalog schema

data/rank-catalog.json includes schema_version, date, status, branches, grades, patterns, rank_records, blank_cells, shared_records and coverage.

- branches: id, label, source_column (1-based Nexus branch cell position), military boolean. Twelve original branch labels retained.
- grades: id (E-1 etc), order_bottom_up (1…30), family. Military common ground spans E-1…HC-4.
- patterns: id (safe slug), rows (ordered arrays of local tile tokens), status CANDIDATE, approval null, design_basis, reference_urls, adaptation_notes. No empty rows. Tokens: red, blue, gold (yellow/gold enamel), green, orange, white (pearl), charcoal, black, bright-white, grey, purple, silver, metallic-gold, cyan, teal, amber.
- rank_records: id, branch_id, grade, grade_order, title_raw, title_display, pattern_id, status CANDIDATE, approval null, source_assertions, candidate_notes. 210 populated branch cells including 69 military records. Titles preserved, corrections/encoding repairs explicit in notes.
- source_assertions: source, url, capture, row_index_zero_based, cell_index_zero_based, title, grade; spreadsheet assertions may also include gid/cell/struck. Do not drop conflicts.
- blank_cells: branch_id, grade, source coordinates, reason (source blank; no rank invented).
- shared_records: same core fields as ranks but branch_id null, separate 7 spanning upper/Throne records. Preserve merged titles and disputed grade alternatives, do not duplicate across 12 branches.
- coverage: counts for all branch records, military records, blank cells, shared records, per-branch totals and patterns. Workers must compute these from data.

## Composition outputs

assets/composed/<pattern-id>.png and .svg for every pattern. SVG self-contained, embeds local normalized raster tiles as data URIs and describes backplate geometry. PNG transparent outside. Reuse exact normalized components and constant tile dimensions/gaps/margins; no generative redraw for combinations.

assets/composed/manifest.json: schema_version, status, design_system_path, components, patterns. Components record token, original_path/hash, normalized_path/hash, crop/alpha method and dimensions. Pattern entries: id, rows, png_path, svg_path, width, height, sha256_png, sha256_svg, tile_count, tile_boxes (row,column,token,x,y,width,height), status, approval. Paths workspace-relative.

assets/design-system.json stores exact dimensions and reference/component rules. Preserve source bytes and record all transformations. All geometry uses one tile unit independent of grade.

## Review/chart outputs

assets/catalog-review.html works offline with embedded data; accessible table, search/branch/grade filters, blank/source/conflict visibility, source/rationale/native asset links and coverage totals. Individual pattern and chart links work.

assets/charts/military-chart.png/.svg, all-branches-chart.png/.svg and branch-<id>.png/.svg. Chart labels/images come from the same catalog/manifest. Full-resolution SVG text legible and raster chart exports sized for practical viewing. Shared upper titles shown separately with uncertainty. Do not treat them as settled hierarchy.

tools/verify_catalog.py independently checks source/title/grade/cell fidelity, 69 military/210 branch/66 blank/7 shared coverage, record/pattern identities, source conflicts, exact rendered component pixel placement, counts/colors, geometry, alpha, chart/browser inputs and file hashes. If observed source counts differ, stop and report rather than fudging them. Verification is technical, not creative approval.
