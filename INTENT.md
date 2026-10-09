# Intent — Imperial Republic ranks and visual standards

Date: 2026-10-09
Owner and canon authority: Ryan (Stratus)
Status: complete candidate library technically verified; creative approval and canon adoption pending

## Desired outcome

Establish official rank titles and reusable visual references for rank squares, rank plaques, other insignia and uniforms. Make them usable by humans and agents through an HTML chart, a complete graphic, canonical documents and structured records associated with the codex/canon-service and admin.eotir.com.

The music anchor workflow is the model for provenance, versioning, approval and publication. It is not a reason to make a music catalog the authority for the entire universe's ranks.

## Ryan's starting preference

Start with the Star Wars Combine Galactic Empire modular plaque system and compare it with a second comprehensive chart. Ryan is mostly, somewhat strongly, inclined toward this direction but has not committed to its exact designs. Keep room for a small parallel alternative-design comparison.

Latest clarification, 2026-10-09: source precedence stays MOSTLY undecided. Focus on military ranks first; establish common middle ground rather than reconcile every rank and institution now.

Ryan subsequently requested an expanded mix-and-match palette including black, white, purple, grey, silver, gold and orange, with possible future specialty branch/department/division use. Sixteen color/material options are staged locally. The palette does not assign departmental or rank meanings.

The first military batch now covers E-1…E-7 with 21 source-backed branch records. Ryan explicitly chose the shared Combine grey/blue family for these drafts. E-7 is a proposed extension; no exact visual/assignment approval has occurred. docs/GOAL-PROMPT.md is the requested complete-chart continuation authorization to invoke next, including exact composition and independent GitHub repository setup; writing it did not start that goal.

## Initial scope

1. Use Navy, Marine and Army titles shared by Nexus and the IRAF detailed sheet as a provisional working set.
2. Choose tile construction, palette, plaque geometry and a mapping rule through review candidates.
3. Produce reusable individual squares, then individual plaques, then a military chart.
4. Extend the chart to the other Nexus branches after their sources and display rules are reconciled.
5. Associate approved definitions/assets with canonical Markdown and database projections; connect them to admin tools through a deliberate integration.
6. Develop uniform and other insignia rules separately, using approved plaques and existing heraldry as references.

The military overlap is 23 grade positions in each of three branches, or 69 occupied branch/grade cells. This is not a count of distinct badge designs, unique titles, physical units or approved assets.

## Eventual deliverables and acceptance

| Deliverable | Acceptance condition |
|---|---|
| Source-backed military rank dataset | Raw sources preserved; abbreviations, disagreements and blank cells explicit; stable identities and branch/grade ordering |
| Individual tile library | Approved shape, palette, materials and exact visual versions; reusable vector masters and practical transparent raster exports are proposed |
| Individual rank plaques | Explicit ordered tile pattern, geometry and approved association with branch/rank/era; no inferred default assignments |
| HTML chart | Generated from the same records as the graphic and DB; readable labels, accessible table and image descriptions; uncertainty visible in review mode |
| Graphic chart | Same version and assignments as HTML; legible full-resolution export with version/status/source attribution |
| Canon document | Human-readable rules and approved machine frontmatter; exact approved scope and provenance; no source research mistaken for canon |
| Database rows | Derived from approved authoritative records; stable IDs, reversible/scoped migrations, no independent conflicting edits |
| Canon/admin association | Type support and asset links verified; approval gates enforced; local code changes distinguished from live deployment |
| Uniform standards | Approved service/dress/era and wearer-side placement rules; do not infer them from a rank plaque or an external costume |

## Design alternatives and tradeoffs

| Approach | Why consider it | Tradeoff |
|---|---|---|
| Combine-inspired modular tiles + comprehensive chart comparison | Closest to Ryan's preference; easy to assemble and compare systematically | External rank ladders differ; Imperial Republic high tiers and enlisted coverage need explicit mapping |
| A related original tile system with different grouping/borders | Preserves the desired plaque language while offering a distinct system | Needs separate approval and a readability comparison |
| Plaques plus optional boards/collar devices | Supports different dress contexts later | Requires a second mapping and uniform regulation; archived boards remain concepts |

Recommendation, not approval: use deterministic SVG composition for exact tile counts/positions and PNG exports; reserve image generation for material/style studies or uniform concepts. Generative images alone are harder to keep identical across a large chart.

## Authority and lifecycle proposal

Keep separate fields or records for source assertion, hierarchy decision, design approval, rank-pattern assignment approval and publication. A complete chart or a database flag must not collapse these into one approved state.

Proposed flow: source evidence → reconciled working ranks → candidate design/pattern → Ryan's exact approval → approved authoritative record and keeper bytes → generated chart/DB projection → verified publication receipt.

No new ranks, patterns, uniforms or assets were canonized in discovery. No D1 schema, PostgreSQL migration or new music anchor kind was created. Ryan then authorized separate rectangular beveled/textured tile candidates followed by plaque combinations; cylinders remain separate initially. Save all project renders here and preserve kept/approved images locally.

Long-term canonical destinations: codex-monarch/content/ranks and content/uniforms. This workspace is the staging/build repository before a later approved transfer.

## Historical starter next-session checkpoint

Read docs/MILITARY-BASELINE.md and docs/DECISIONS.md, then open assets/review.html. Review the sixteen tile color/material options and two unassigned plaque studies before refining the components. Preserve an alternative-design comparison as an option. Settle geometry/palette and how to map the extra Imperial Republic tiers before mass-producing plaques. Consider specialty color use separately; broad nonmilitary reconciliation can remain deferred.

## Active complete-chart scope — 2026-10-09

The saved goal was invoked. Finish 69 military and 141 other populated branch cells, preserve 66 blanks and seven separate shared upper records, and provide individually addressable deterministic plaques and readable graphics/HTML from one working catalog. The public eotir/eotir-ranks repository is the independent draft staging repository; its static review site is served through GitHub Pages. Scoped commits/pushes are authorized. Earlier next-session recommendations describe the starter checkpoint; they do not limit this active draft scope. Canon-service transfer, production databases, uniforms and code cylinders remain later work.

## Current next review

Open assets/catalog-review.html, filter Navy and review all 23 bottom-up military grades. Select exact tile/material geometry before approving plaque versions and associations by pattern ID/hash. Review specialty proposals and unresolved shared upper alternatives afterward. See docs/COMPLETION-REPORT.md for complete coverage, evidence and limits.
