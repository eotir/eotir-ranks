# Complete candidate-library delivery — 2026-10-09

Status: technical build verified; final delivery commit/push verification recorded separately in [PUBLICATION-RECEIPT.json](PUBLICATION-RECEIPT.json). All visuals and rank associations remain unapproved CANDIDATES.

## Review entry points

- [Review hub](../assets/review.html) preserves original tiles and candidate history.
- [Complete filtered catalog](../assets/catalog-review.html) shows titles, grades, ordered patterns, source coordinates, rationale, conflicts, native PNG/SVG links and background controls.
- [Military PNG](../assets/charts/military-chart.png) / [SVG](../assets/charts/military-chart.svg).
- [All branches PNG](../assets/charts/all-branches-chart.png) / [SVG](../assets/charts/all-branches-chart.svg). Individual charts for all twelve branches are linked from the catalog.
- Current public repository: https://github.com/eotir/eotir-ranks.

## Coverage

69 military cells: Navy, Marine and Army each cover E-1…E-7, O-1…O-6, C-1…C-6 and HC-1…HC-4. Another 141 populated records cover the nine other Nexus branches. All 66 source blanks are explicit, with no invented ranks. Seven spanning upper/Throne titles are separate from the 276-cell branch grid.

The 217 populated/shared records use 178 candidate patterns, including seven shared-title alternative studies. Sixteen normalized tile/material options produce 178 individually addressable transparent PNG/SVG pairs and 1,247 exact tile placements. Twenty-eight original generator outputs, including superseded versions, remain preserved locally.

## Requirement audit

| Goal item | Authoritative evidence |
|---|---|
| 1. Entire military | data/rank-catalog.json: 69 records, three complete 23-grade sets; independent Nexus title/grade/branch-coordinate verification |
| 2. Nine other branches and shared rows | 141 specialty records, 66 blanks, seven separate shared records and their alternatives; accessible HTML table and per-branch graphics |
| 3. Research and source fidelity | DISCOVERY.md, PATTERN-RATIONALE.md, sources.md, saved Nexus/Combine captures and full-chart-reference-google-ranks.json; 354 sanitized title cells support 355 workbook assertions; original coordinates/strikes/hash retained |
| 4. Reusable exact plaques | assets/design-system.json and composed/manifest.json: fixed 160 × 270 components, ordered rows, exact PNG reconstruction, embedded SVG bytes/order/geometry, input/output hashes and alpha checks |
| 5. Maintained HTML and graphics | review.html → catalog-review.html; 283 table rows, 224 candidate image displays, 14 PNG/SVG chart pairs, native links and filters/background controls |
| 6. Private GitHub delivery | Private repository verified by gh; scoped committed paths, remote HEAD and excluded private inputs must agree with PUBLICATION-RECEIPT.json |
| 7. Future integration staging | staging/ examples and INTEGRATION.md; illustrative rank/uniform Markdown, JSON Schema and review-cache DDL; no watched canon or live DB writes |
| 8. Verification and handoff | tools/verify_catalog.py, assets/charts/*-qa.json, local-verification-2026-10-09.json, source-only deterministic rebuild and sessions/2026-10-09-session.md |

Source precedence is still MOSTLY undecided. Nexus is the captured grid for these drafts, not a ruling that overrides the official workbook. Raw source spelling is retained; corrections/encoding repairs are display-only notes. External systems provide visual references, never adopted Imperial Republic ranks or uniform entitlement.

## Proposed adaptations and remaining decisions

See [PATTERN-RATIONALE.md](PATTERN-RATIONALE.md) for every exact ordered array and source graphic. E-7 extends the saved enlisted family, which ends at E-6. C-1 bridges an extra local command position; HC-2/HC-4 bridge/extend upper patterns. Sharing officer/command/high-command patterns across the three military branches is a proposal. Specialty palettes, nearest-reference reassignments and shared neutral alternatives are also proposals.

Ryan must approve the exact tile footprint/material, plaque versions and rank associations before keeper/canon promotion. Source precedence, upper/Throne hierarchy, specialty color meanings, uniform placement, cylinders and heraldic entitlement remain open. No rank-grade prefix grants a phoenix or dress entitlement.

## Verification limits

Technical checks prove coverage, source fidelity, geometry, bytes, labels and working local links. Native representative inspections confirm readable military/specialty chart areas and consistent plaque texture; they are not Ryan's all-assets creative approval. The large all-branches raster is 110,145,979 pixels; use HTML filters or individual branch charts for normal review. Font provenance is recorded; raster chart bytes can vary by host font. PostgreSQL DDL is review-only; SQLite example was executed solely in memory.

Historical payroll/personnel exports and the raw workbook capture remain local and ignored. A minimal-input rebuild without them reproduced the catalog SHA-256 exactly. An unrelated installer is preserved and excluded. No production deployment, live database write, R2 publication or canonical transfer occurred.

## Exact next review step

Open the complete catalog, filter Navy, and review E-1 through HC-4 in order. First select the common tile/material geometry, then the seven grey/blue enlisted candidates, then the sixteen officer/command/high-command mappings. Record approval by exact pattern ID and PNG/SVG hashes, separately from source-hierarchy decisions. Review specialty palettes and shared upper alternatives afterward. Approved transfer requires the coordinated monarch type support and editorial serving gate described in INTEGRATION.md.

## Subsequent public review publication

Ryan authorized public visibility and GitHub Pages after the private delivery checkpoint. The static review URL is https://eotir.github.io/eotir-ranks/. PUBLICATION-RECEIPT.json remains the historical private-content receipt; PAGES-PUBLICATION.json records current public deployment and checks. No candidate approval or canon flag changed.
