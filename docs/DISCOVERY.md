# Discovery — ranks, plaque references and existing systems

Date: 2026-10-09
Scope: local sources, live Nexus and selected Google Sheets ranges, supplied images, linked comparisons, music and canon/admin implementations
Status: research findings; no new canon adopted

## Findings that shape the next step

1. There is useful military common ground: Navy/Marine/Army positions HC-4 through E-1 agree between Nexus and the IRAF sheet, allowing design exploration without resolving all historical structures.
2. Official source does not mean every supplied sheet is the same revision or purpose. Historical pay lists, special appointments, peerage and personnel data cannot be merged blindly into a rank dictionary.
3. The preferred visual references agree on modular colored plaques but differ in grade ladders, geometry and coverage. A design reference is not a source of Imperial Republic ranks.
4. The modern music anchor system uses per-anchor Markdown, generated registries and explicit approval/provenance; it is a useful workflow model.
5. Canon-service uses PostgreSQL and authoritative files; it does not currently have rank/uniform types or enforce the creative approval gate needed here.
6. Ryan wants development here first and approved transfer later to codex-monarch/content/ranks and content/uniforms. Local preservation is a requirement.

## Official source review

### Published Nexus

The live table has 37 total HTML rows: 30 grade rows plus section/branch/group headers. Grade families: RT-4…RT-1, HC-7…HC-1, C-6…C-1, O-6…O-1, E-7…E-1. There are 12 branches, grouped as follows:

| Group | Branches |
|---|---|
| Armed Forces | Navy, Marine, Army |
| COMPNOR | Inquisition, Judiciary, Ministries, Security Bureau |
| Throne | His Majesty's Personal Staff, His Majesty's Royal Guard |
| Ministry of State | State, Regional Governance, Intelligence Service |

Seven upper rows have spanning/shared titles. The remaining 23×12 branch cells include 210 populated cells. These are not 210 unique rank entities. Navy/Marine/Army each have 23; other branches contain gaps.

The chart has zero insignia image elements. Its branch background colors identify columns; they do not establish tile colors. The browser screenshot is source evidence, not a newly approved replacement chart.

Local source captures are under nexus/design/uploads/. The JSX transform at design/theme/rankchart_data.jsx claims 13 branches in a comment, but lists 12. It also corrects spellings/removes some uncertainty. Use the actual published source and preserved raw assertions, not the comment or transformed data alone.

### Google workbook and saved exports

Live workbook title: Ranks & Salaries (WIP), America/Phoenix. Metadata confirms 12 tabs, including hidden CIRAF. Live bounded reads captured IRAF A1:O40, General A1:M40 and Special A1:L41. No workbook edits were made; this is not a fresh audit of Personnel or every tab.

Live General includes an RSC Royal Supreme Court row and IRSB alternative Ranks column absent from the supplied General HTML. Thus local exports are not complete substitutes for the live grid. All three live detailed tabs strike out Grand Vizier; archived plain text loses that distinction.

| Local source | Structure and caveat |
|---|---|
| IRAF detailed | 25 graded rows HC-6…E-1 plus Throne/ungraded rows; military branches, R&D, MCIS, justice, civil service |
| General detailed | 28 graded rows HC-9…E-1; multiple government/justice/peerage branches; footer says web update 12/09/2018 |
| Special Revamping | 25 graded rows; special operations, staff, Royal Fleet/Guard, Palace Security, Academy |
| CIRAF | Plan A combined scheme; 23 graded rows; G-21 absent, HC-2 maps differently from detailed IRAF |
| Full Pay Scale | 375 rows across 15 divisions; 208 nonempty title cells |
| Full Pay Scale WIP | 378 rows including three added Throne rows; 224 populated title cells; 46 changed existing cells compared with Full |
| Salaries per level | E-7 and Throne salaries absent; not a complete hierarchy |
| High Council Adjs | 12 named historical adjustment records, not a rank definition table |
| Additions | 15 historical submissions, including modifiers and spelling errors |
| Personnel | Historical payroll; 36 #REF! occurrences in supplied HTML |
| Ground Elements | Unit sizes, examples and command positions, not solely rank definitions |
| Sign-Off | Historical signatures/dates, including 2009; not approval of this new insignia project |

Populated-cell counts retain slash titles/placeholders as one cell and are not counts of approved ranks. The ZIP is preserved as received; renaming its outer file did not rewrite internal export names.

The archival TXT records extraction in May 2025 from an older XLSX. Its IRAF includes a Combined Armed Forces Plan reference column absent from the current detailed read. Extraction recency does not resolve source authority.

### Material contradictions

| Topic | Conflicting evidence |
|---|---|
| Throne | Nexus RT-4 Supreme Ruler, RT-3 Executor, RT-2 Empress, RT-1 Supreme Chancellor; detailed tabs use RT-3/2/1/1 |
| Praetor | Full often HC-4; WIP/detailed commonly HC-6; Nexus shared HC-7 |
| High Councilor | Full Ministries HC-3; WIP/detailed HC-5; Nexus shared HC-6 |
| Grand Minister | Full combined with Praetor HC-4; WIP HC-3; General HC-4; Nexus shared HC-6 |
| Chief of Staff | Full HC-1, WIP HC-2, detailed ungraded G-26; Nexus HC-6 with Deputy Chief of Staff HC-2 |
| Combined military | Flat Full/WIP use different combined grades/titles; IRAF/Nexus have branch-specific ladders |
| MCIS | Flat Director C-2 versus detailed HC-1; several subordinate titles/grades differ |
| Royal Guard | Flat lists shift enlisted and officer titles; detailed/Nexus put Master Sergeant O-1 and Guardsman E-1 |
| Personnel | Individual historical grades/assignments can differ from chart structure; they do not redefine the hierarchy automatically |

Grand Admiral HC-3 agrees between Nexus and detailed IRAF. The disagreement there is with some external/historical systems and unrelated codex descriptions, not this two-source military intersection.

## Saved images and external comparisons

### Combine

The [current Combine page](https://www.swc-empire.com/ing/general/ranks) displays modular beveled colored tiles, often visibly taller than wide, on narrow backing plates. It uses a different hierarchy and emphasizes officer/trainee coverage. The [Holocron page](https://holocron.swcombine.com/wiki/Ranks_of_the_Galactic_Empire) is an older distinct chart, last edited in 2016. Do not conflate them.

The supplied MHTML contains 88 embedded GIF images. Decoded comparison evidence in docs/research/combine-saved-plaques-contact.png shows red, blue, green, yellow/gold, orange and neutral/white/gray elements. Small source graphics establish visual language but not exact physical dimensions. Retain the URL/filename of the particular reference used.

### Whatsahonda

references/imperial-rank-table-whatsahonda.png is the stronger local paired-plaque comparison; its JPG companion is smaller. It spans military, operations/intelligence, governance and COMPNOR columns, often showing single-row and double-row variants, plus separate small side devices. Enlisted entries include bar/other devices rather than a complete uniform tile-only scheme.

This is the recommended second comparison for Ryan's preferred starting direction, not an adopted mapping. The live artist page returned 403, so provenance is limited to the supplied file, filename and bibliography URL.

### Taivaansusi

references/table-of-ranks-in-imperial-service-taivaansusi.png explicitly separates appointments from branch ranks, and covers enlisted/warrant/commissioned/flag/special categories. Its military titles and grade divisions differ from the Imperial Republic. It is particularly useful for separating command assignment from rank and comparing chart coverage.

references/imperial-uniform-recognition-chart-2-taivaansusi.png shows service, formal, field and combat variants across institutions. The overview and two exact pixel crops were inspected. These are costume/placement comparisons only; depicted characters and Galactic Empire uniforms do not establish Imperial Republic entitlement.

The company TOE, escalation, industry and galaxy images were also viewed. They are ancillary context and not sources for initial plaque assignments. Larger overviews were resized by the viewing tool; no pixel-level audit of every map label is claimed.

### Other linked material

[TheForce.net cylinders](https://www.theforce.net/swtc/insignia/cylinders.html) is a dated external analytical model of cylinder function/count. [CloneIntel](https://cloneintel.com/IntelRanks.html) explicitly uses its own canon interpretation. Neither overrides Imperial Republic rulings. Pinterest links were unavailable through the web reader and remain discovery indexes rather than verified design sources.

## Existing uniform evidence

Current music/docs/OVERMIND-NAVAL-UNIFORM-WORKING-SPEC.md records Ryan's 2026-10-07 confirmation that archived shoulder boards were concepts only. Its 2026-10-08/09 rulings distinguish Standard, Shield and Stratus Phoenix designs and image-specific patch placement. Older generic layout suggestions in that document remain proposals and can be superseded by later rulings.

The songbook can document song imagery but is not the canon authority. Broad universal plaque geometry, cylinder-count mapping and uniform rules have not been recovered here. The adjacent wiki Navy example is explicitly example data; eotir-codex/data/rules/rank-structure.md contains conflicting Grand Admiral grades/insignia and must not be silently adopted.

## Reproducibility and access

- Inputs fingerprinted in docs/research/source-inventory*.json; 22 normalized filenames verified byte-identical in docs/research/file-renames-2026-10-09.json.
- Live Nexus HTML/table JSON/screenshots and selected Google cell values/strikeout preserved under docs/research/.
- All research was read-only outside this workspace. No live database, publisher, service write or deployment was run.
- Initial local sandbox startup failed; native read commands worked with the reviewed fallback. Desktop Commander was briefly used after MONTOYA connected; Ryan then preferred local tooling and work returned to native tools.
- The in-app tab was not exposed through Chrome auto-connect; a separate isolated browser inspected the same public URL. Direct Nexus fetch needed a browser User-Agent and the no-trailing-slash starting URL.
- At the discovery checkpoint, local ranks and Nexus folders had no Git repository; ranks was subsequently initialized under the invoked complete-chart goal. Inspected local code revisions: music 604d69882528c1ea5403cce89afdb0f3ddb749f1; admin-tools 829347eb6e208242d8667558b47a697bc8db27a1; codex-monarch d53bc0a66fc4dac4fb0ec0fba1a15dcf61b95ce2. Deployment state was not verified.

## Initial asset studies after discovery

Ryan authorized rendering after the reference review. Seven colors are saved as separate transparent RGBA PNG candidates, with red v1 preserved and red v2 used as the working material reference. Two unassigned plaque studies have six tiles in one row and twelve in two rows. The observed counts/order match their prompts. Neither establishes a rank mapping.

Open assets/review.html from the project root for actual local previews. assets/render-manifest-2026-10-09.json records exact prompts, input/output hashes, dimensions, alpha and candidate status. All ten local PNGs match the generator originals. The supplied 24 source files remain unchanged after 22 filename normalizations. Technical verification and browser inspection do not establish creative approval.

The plaque generator redraws the material rather than copying the exact component pixels. Use these as layout/material studies; deterministic composition remains the recommendation for the complete chart. Code cylinders and rank assignments remain later work.

Follow-up palette expansion on 2026-10-09: Ryan requested additional neutral, purple and metallic options for mix-and-match and possible specialty branches/departments/divisions. Nine additional candidates bring the gallery to sixteen color/material choices and the local library to nineteen PNGs including red history and two plaques. No departmental color mapping was adopted. Orange and yellow/gold enamel remain alongside amber and metallic gold as separate choices.

## Complete-chart reference continuation — 2026-10-09

The included rank-only Google snapshot preserves source coordinates, grades and strikeout while excluding unrelated payroll/personnel data. Full catalog rationale lives in PATTERN-RATIONALE.md. Rechecked the Combine Holocron and current Galactic Empire chart: their upper/officer ladders differ from each other and our official sources. They remain aesthetic evidence; no external grade positions were imported as Imperial Republic authority. References: https://holocron.swcombine.com/wiki/Ranks_of_the_Galactic_Empire and https://www.swc-empire.com/ing/general/ranks. Clone Intelligence remains a comparison for insignia/placement variation: https://cloneintel.com/IntelRanks.html. The saved Combine MHTML supplies 88 decoded plaque images, including some transparent padding rows that must not be interpreted as white tiles.
