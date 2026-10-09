# Handoff to Claude Code — one master Imperial Republic art site

Date: 2026-10-09
User and creative/canon authority: Ryan (Stratus)
Rank workspace: D:\eotir\projects\ranks
Repository: https://github.com/eotir/eotir-ranks
Status: current image work saved and published; unified site integration has not begun here.

## What Ryan wants

Build **one master art site**, combining a visual wiki/encyclopedia, browsable gallery and creative staging/review workspace for the Era of the Imperial Republic / Imperial Republic Era. Bring together lightsabers, other armory/equipment, ranks, rank plaques, code cylinders, uniforms, heraldry, ships and related visual collections as real source-backed content becomes available.

The strong preference is one coherent site with shared navigation, search, item pages and review experience. Separate repository ownership may remain underneath, but a directory of separate sites or iframe wrappers is not the desired final result. Links to existing galleries may help during development; they are a transition, not the product goal.

Use Ryan's supplied **Claude Design** site presentation. Dark mode only, compact readable typography and controls. Preserve its visual language rather than inventing another theme. Keep the rank ledger/matrix/ladder and large image inspection where those specialized views are useful. A rank chart and a lightsaber collection need different content views inside the same site.

Art development and canon adoption are connected but distinct. Ryan wants locally saved full-size image masters, candidate history and provenance; eventually approved ranks/uniforms should also have HTML, chart graphics, canonical documents and structured database records associated with canon-service/admin tools. The site should make those relationships understandable without silently converting a draft into canon.

## Division of work

**Claude Code:** own the overall site, collection integration, navigation, search/item routing, shared presentation and data adapters. Ryan chose this because Claude handled the overall design and can bring the collections together efficiently.

**Codex:** focus on image generation and refinement, component/variant production, source-conditioned heraldry work, native-resolution inspection, local master storage and asset provenance. Codex can take bounded image tasks from Claude when the tool/session arrangement supports delegation. Do not assume cross-tool delegation is wired up: an explicit task prompt can be passed to the existing Codex conversation as a fallback.

Ryan approves creative selections and canon promotion. Keep candidate, accepted design direction, selected exact image, design-approved, locked, published and canonical states distinct. A published gallery can contain candidates.

## Presentation inputs

- Latest full handoff: D:\eotir\projects\.handoffs\EOTIR.zip — 114,981,174 bytes; SHA256 73344616b24abcefe2b37e3e2ff0a976ec7198d6fcc9bc468e1e789e58d8b6da.
- Earlier handoffs: D:\eotir\projects\.handoffs\EOTIR-Ranks-site3.zip and Rank Plaque Catalog - Standalone.html.
- Latest ZIP selectively extracted into **ignored** D:\eotir\projects\ranks\tmp\eotir-master-design. All 558 archive entries passed path/symlink checks. Keep the full theme/showroom export outside published source or in ignored staging; import relevant files deliberately.
- ZIP gallery includes 25 lightsaber records and 50 real unlit/ignited PNG originals. The root index is a design showroom, not a completed master-category gallery.
- ZIP contains an **older rank export** and no recent full-size cylinder/engraving work. Use the current rank checkout for these assets and data. Do not overwrite it with ZIP rank snapshots.

Read [archive evidence](research/eotir-master-design-2026-10-09.json) and [integration research](VISUAL-GALLERY-INTEGRATION.md) for actual files, hashes and implementation observations. The full export includes unrelated admin/forum/theme fixtures: those are not new universe facts or mandatory scope.

## Current rank and image deliverables

| Collection | Current source | State |
|---|---|---|
| Rank catalog | data/rank-catalog.json | Source-backed candidate assignments; official source precedence remains mostly undecided |
| Reusable tile/material library | assets/design-system.json and assets/review.html | Sixteen normalized color/material options, with original generation history preserved |
| Plaques | assets/composed/manifest.json and PNG/SVG files | 178 candidate patterns; 1,247 ordered tile placements |
| Charts | assets/charts/ | Fourteen PNG/SVG chart pairs; currently plaque-only snapshots |
| Military cylinder counts | data/code-cylinder-assignments.json | 69 provisional military associations; other/shared mappings unresolved |
| Original large cylinders | data/code-cylinder-gallery-v2.json and assets/cylinders/v2/ | Three designs Ryan said were good; accepted as bases for development |
| New engraved cylinders | data/code-cylinder-engravings-v3.json and assets/cylinders/v3/ | Twelve unapproved studies: three bases × Standard/Shield × silver/gold |
| Heraldry conditioning sources | references/heraldry/ | Four exact LOCKED anchor PNG copies, source Markdown snapshots and usage guide |

Military coverage: Navy, Marine and Army, 23 grade positions each (E-1–E-7, O-1–O-6, C-1–C-6, HC-1–HC-4). Other branches contain 141 populated records. All 66 source blanks and seven shared titles remain explicit. The complete grid/review has 283 rows; these numbers do not imply 283 unique approved insignia.

Ryan chose the Combine grey/blue enlisted family shared across military grades as the starting direction. E-7 and some upper-grade extensions are proposals. External Star Wars charts provide design references, not Imperial Republic rank canon. See MILITARY-BASELINE.md, PATTERN-RATIONALE.md and sources.md.

Latest cylinder masters retain generator bytes at native sizes: blue dosimeter/pilot families 1024×1536, grooved family approximately 814×1931–1933 depending on version. Preview scaling must not replace the original files. New art must be saved locally in versioned folders with exact hashes and provenance.

## Current site and verified delivery

- [Rank catalog](https://eotir.github.io/eotir-ranks/assets/catalog-review.html)
- [Full-size cylinder and engraving gallery](https://eotir.github.io/eotir-ranks/assets/code-cylinder-review.html?v=4cc5f65)
- [Tile/plaque review hub](https://eotir.github.io/eotir-ranks/assets/review.html)

Visual content commit: 4cc5f653bfdb6bf432fcb5e325d5691c114ff6b7. Pages run 37956438118 succeeded. Receipt: [CYLINDER-ENGRAVING-PUBLICATION.json](CYLINDER-ENGRAVING-PUBLICATION.json). Twenty-three HTTP files match local bytes exactly: gallery, two CSS files, v3 manifest, fifteen cylinder PNGs and four heraldry reference PNGs. Local/live browser checks confirm fifteen loaded masters, no broken images or page exceptions, correct dimensions/downloads/filters and responsive layout. Receipt/continuity commit 3e09d5f; integration research checkpoint fa753b1. Later documentation commits do not change the verified artwork bytes.

The rank catalog and cylinder gallery already reuse Claude's carbon/crimson design and local Chakra Petch/Inter/JetBrains Mono fonts. The current cylinder gallery adapts that shell for large image cards. Native-open/download links, original masters and earlier history are retained. CSS/script asset URLs use content hashes to prevent stale browser code.

Cylinder groups **flank** each plaque: wearer-right is viewer-left, wearer-left is viewer-right. Zero/unknown counts have distinct readable states. The small rank-preview cylinders are still the earlier components; the new large masters have **not** yet replaced them. Do not assume approving a large base approves its fitted derivative or count mapping.

Relevant tools: tools/build_cylinder_gallery.py, tools/build_cylinders.py (writes v1 history only), tools/build_rank_site.py, tools/build_rank_ui.cjs, tools/build_review.py and tools/verify_catalog.py. Preserve deterministic plaque composition and existing master bytes when changing presentation. Read assets/site/README.md before changing the compiled rank frontend.

## eotir-art and lightsabers

https://github.com/eotir/eotir-art remains a **private source repository**, with a separately selected gallery publication. Its README identifies the canonical checkout as /repos/eotir-art; no local checkout was found under D:\eotir\projects. Inspected GitHub HEAD: d2acc7311bf2a0f57af4ea82a04a82296d0bf780.

Read gallery/README.md, gallery/PRIMARY-ROLE-UPDATE.md and gallery/catalog.json. The selected catalog pins codex-monarch 67e25928a4eb559ec460b0f51ff0996244985bc2 and eotir-art ee1129ab42c93c561b996fd23f9e2984316d9270. Its builder reads immutable Git blobs, preserves original PNGs and creates separate thumbnails. This is a useful model for the unified site's artifact inputs.

The exported collection has 25 weapons / 50 original views: 24 records claim Design-approved visuals, one has a confirmed training role with image approval unspecified. Approval Markdown is referenced but absent from the ZIP. Check the exact upstream approval records; filenames and old review labels are not sufficient.

Legacy owner means associated character, not necessarily ownership. Preserve Eric Jackson's in-use/non-ownership qualification, Daniela's uncertain possession, hand distinctions and primary/training roles. Unknown stays unknown.

Historical endpoint: https://eotir-lightsabers.stratusweb-ops.workers.dev/. Current revalidation returned HTTP 403; cause unresolved. Historical deployment receipts are not proof of current reachability. Do not change Access or deployment policy just to make the integration work. A combined build can consume verified selected artifacts rather than depend on this endpoint.

## Strongly preferred architecture, with implementation choices left to Claude

Build **one deployed master art site** from the Claude Design handoff, with shared item identities, navigation/search and category pages. eotir-art is a natural candidate for owning the art site's frontend/build, while ranks can remain a source module during development. A third unrelated gallery repository is unnecessary unless Claude finds a concrete reason. Final hosting/domain and repository placement remain implementation choices; there is no requirement to migrate all source repositories first.

Use category adapters to join current rank/cylinder manifests and the selected lightsaber catalog into a common display index. Retain each source's exact records, version/commit/path/hash and approval distinctions. Keep original masters in their owning local repositories; publish verified selected artifacts into the site build. Do not make a second editable canon database merely to combine galleries.

Suggested item records: stable namespaced ID, category/title, source links, original file/hash/dimensions, preview derivative/parent, visual approval evidence, association/role qualifications, canon state and related items. Encyclopedia text should come from actual canon/source records, with drafts identified. Relationships can connect a rank to plaque variants/uniform studies and a weapon to documented characters without inventing entitlement or ownership.

One unified deployment may copy verified artifacts into category paths. An alternative is separate source repositories built into the same frontend deployment through pinned artifact inputs. Both satisfy one master site. A permanent link directory across unrelated gallery frontends would not satisfy Ryan's preferred end state.

## Image work remaining for Codex

1. Ryan reviews exact engraved versions, size and placement, and chooses recessed engraving versus gold inlay/relief. Some gold studies look raised; source-conditioned heraldry is not proven pixel-identical to anchors.
2. Refine selected marks/materials and clean alpha halos/flecks through the image workflow; preserve earlier outputs. Three bases and all engraving variants remain available for comparison.
3. Derive exposed-pocket cutouts and fitted full-size compositions; only then make smaller previews and update the existing rank UI components.
4. Continue source-backed rank/uniform/armory/ship image tasks as directed. Do not invent lore or new category assets to fill empty pages.

The exact locked Standard and Shield are different from the Stratus Phoenix. Gold is the requested High Command finish, with no exhaustive grade/member map; an HC prefix does not grant it automatically. Current heraldry rules distinguish Shield defense/military/security/police/intelligence use from Standard civilian/government/patriotic use. Both were requested as engraving studies, not a new universal uniform entitlement.

## Delegating a useful image task

Give Codex a bounded brief containing: objective and exact base/reference paths; versions to preserve; permitted variations; desired full-size outputs and transparent-background requirements; destination/version naming; known approval/usage rules; and the manifest fields Claude's adapter expects. Return PNG paths, hashes, dimensions, prompt/reference provenance and native/practical-size review notes. Creative approval remains with Ryan. Avoid asking Codex to redesign the site while it is generating/refining artwork.

## Canon/database boundary and acceptance

Intended adopted-rank/uniform destinations remain codex-monarch/content/ranks and content/uniforms. Canonical Markdown is authoritative; PostgreSQL canon-service is its query cache, and any D1 layer should be a projection. The service does not currently provide the complete rank/insignia editorial model. Candidate content must stay outside watched canonical content until an explicit adoption/integration step. Existing lightsaber sources live under sources/visual-designs/lightsabers; do not relocate them casually.

First integrated-site acceptance: one coherent Claude-designed dark site; real selected lightsabers plus current ranks/cylinders; search and stable item deep links; specialized rank and large-image views; native master access; status/provenance/association fidelity; working desktop/mobile/keyboard navigation; unchanged original hashes; and a scoped publication/read-back receipt. Other collections can remain visibly pending until their actual source material is supplied.

This handoff describes intent and inputs. No unified site merge, raw art publication, canon promotion, database migration or cross-repository writes were performed in this session.
