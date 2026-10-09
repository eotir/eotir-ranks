# Code cylinders — reference evidence and candidate associations

Date: 2026-10-09. Status: candidate study; no visual or canon approval.

## Current deliverable

Two separately saved blue-cap silver cylinder views (full instrument and exposed top), nine front-view side-count layouts, and 69 proposed military associations are recorded locally. Every other populated/shared record has an explicit unresolved association (148 records). Source blanks remain blanks. No existing plaque bytes, rank titles or source assertions change.

Review: assets/code-cylinder-review.html and the redesigned assets/catalog-review.html. Data: data/code-cylinder-components.json and data/code-cylinder-assignments.json. Rebuild components with `python tools/build_cylinders.py`, associations with `python tools/build_cylinder_assignments.py`, then HTML with `python tools/build_review.py --html-only`. Run `python tools/verify_cylinders.py` and `python tools/verify_catalog.py`.

## Evidence and conflicts

The supplied [Whatsahonda table](../references/imperial-rank-table-whatsahonda.png) is the most directly useful rank/count comparison. Exact observed Army/Navy rows, image hash and pixel rectangles live in [image evidence](research/code-cylinder-image-evidence.json). The saved Combine graphics and Taivaansusi rank table do not show side-cylinder marks. Their omission does not establish a no-cylinder regulation.

| Whatsahonda external Navy titles | Viewer left | Viewer right |
|---|---:|---:|
| Grand Admiral, Fleet Admiral, Admiral, Vice Admiral, Rear Admiral | 2 | 2 |
| Commodore, Captain, Commander | 2 | 1 |
| Lieutenant Commander, Lieutenant, Ensign | 1 | 1 |
| Midshipman | 1 | 0 |
| Warrant Officer | 1 | 1 |

The parallel Army titles are recorded individually. Large outer gold squares in grand-rank rows are separate devices and were not counted as cylinders. The supplied uniform chart depicts actual pockets, including an Intelligence Commander with one device on viewer-left and two on viewer-right. This opposite asymmetry is preserved as conflicting comparison evidence.

[TheForce.net analysis](https://www.theforce.net/swtc/insignia/cylinders.html), last updated 2000-10-16, proposes a wearer-left/right alternating sequence for totals one through four and treats cylinders as access permits that also differentiate ranks. [CloneIntel](https://cloneintel.com/IntelRanks.html) takes a different position on whether cylinders form rank insignia. Both are external interpretations, not Imperial Republic regulations.

The [501st Line Officer costume standard](https://crls.501st.com/ioc/imperial-line-officer-olive-uniform) permits one to four devices, lists blue-cap dosimeter and other styles, and specifies wearer-left for a single device at optional level two. Its costume certification is not a universal per-rank ladder. Web observations are summarized in research/code-cylinder-web-evidence.json.

## Candidate conventions

All new layout IDs use **wearer** sides. In a front view, wearer-left appears on viewer-right. For the initial Whatsahonda-inspired associations we explicitly propose interpreting its chart as a front view: its 2/1 displayed family therefore becomes wearer-left 1 / wearer-right 2. The chart itself does not specify this convention. The alternative wearer-left 2 / wearer-right 1 layout remains separately available for review.

Military assignments use branch-aware external title comparisons where possible. First/Second/Third Lieutenant subdivisions, Lieutenant Colonel, Line Captain, Marine analogies and unmatched upper titles are labelled proposed bridges/extensions. They are not claims that the external source supplies these Imperial Republic rules. The unmatched upper military titles provisionally use 2/2 rather than invented counts above four.

Enlisted 0/0 is an explicit proposed review layout, not a recovered entitlement rule. A duty-specific cylinder-bearing uniform remains possible. Unknown counts use null; never convert null into zero. Other branches are left unresolved until their own rank/duty/uniform rules are researched or Ryan chooses a proposal. No equal-grade automatic inheritance is applied.

## Integration and next approval

Keep cylinders independent from plaque assets and from rank titles. A cylinder configuration may later depend on uniform class, duty, access or era rather than solely grade. The current side-by-side preview is a schematic, not a regulated physical mounting position or pocket distance.

Claude Design's rank catalog presentation is being integrated from the supplied export. The complete archive is extracted only in gitignored tmp/claude-design; unrelated site pages, administration code, portraits and scenario material are not promoted into this repository. Existing rank records, original plaque PNG/SVG files, source disagreements and candidate states remain authoritative inputs for review.

Before canon promotion, Ryan must approve the exact cylinder design/version, choose the side convention, and approve associations and uniform scope. Static candidate publication is already authorized and does not make these assignments canon. Existing graphic downloads remain the earlier plaque-only charts; they do not silently acquire cylinder entitlements.
