# Agent instructions — Imperial Republic ranks

## Read first

1. INTENT.md: Ryan's objective and current scope.
2. docs/DECISIONS.md: dated rulings, preferences and unresolved decisions.
3. docs/MILITARY-BASELINE.md: provisional military overlap, not visual canon.
4. docs/DISCOVERY.md and docs/INTEGRATION.md: source evidence and implementation boundaries.
5. The latest docs/sessions/ and docs/insights/ entries before substantial work.

## Project identity

Workspace: D:\eotir\projects\ranks. Universe: Era of the Imperial Republic / Imperial Republic Era. Always write Imperial Republic in full in prose; retain abbreviations in quoted source labels and identifiers. Never invent lore to fill chart gaps.

As of 2026-10-09 this is a candidate asset-development Git workspace on main. Ryan authorized public eotir/eotir-ranks and a static GitHub Pages review site; verify pushed HEAD before claiming publication. Static candidate review publication is authorized; no live project database or adopted plaque standard exists.

## Current direction

- The full goal has verified candidate coverage: data/rank-catalog.json, assets/catalog-review.html, 178 composed PNG/SVG pairs and fourteen chart pairs. Read docs/COMPLETION-REPORT.md and publication receipt. Original enlisted studies remain history; all new visuals/assignments have null approval.

- Ryan strongly prefers starting with the Star Wars Combine Galactic Empire plaque design language plus another comprehensive chart. This is a design preference, not adoption of external ranks or approval of copied images.
- Ryan's 2026-10-09 clarification: remain MOSTLY undecided on source precedence; focus on military ranks first and find common middle ground.
- Begin with the Navy, Marine and Army overlap between Nexus and the IRAF Pay Scale sheet. Upper shared titles, other branches, historical payroll structures and special appointments remain unresolved.
- Discovery authorized research, evidence capture and documentation. Ryan subsequently authorized separate beveled rectangular tile candidates followed by plaque combinations; code cylinders are separate initially. Canon promotion, schema migrations and publication remain later work.
- Ryan then authorized bottom-up military plaque drafts and selected the Combine grey/blue family shared across E-1…E-7. First batch lives in data/military-enlisted-working.json and assets/military-enlisted-review.html. The saved external enlisted family ends at E-6; E-7 is explicitly a proposed extension. This direction choice is not visual or canon approval.
- docs/GOAL-PROMPT.md records the requested complete-chart continuation. Ryan subsequently invoked the complete-chart goal, authorizing full candidate coverage, deterministic composition and private eotir/eotir-ranks creation with scoped commits/pushes. Keep every new visual/assignment provisional.

## Authority and conflicts

- Treat Ryan's explicit dated rulings as decisions. A preferred design, selected candidate, approved image, locked anchor and published asset are separate states.
- sources.md is the supplied bibliography. Its official sources disagree; it does not establish precedence among them. Preserve source assertions rather than choosing silently.
- Nexus and the linked Google workbook are official project sources. Saved HTML/TXT exports are snapshots with formatting and structural losses; extraction dates are not approval dates.
- External Combine, fan charts, costume analyses and Pinterest boards provide comparison evidence only. Never import their rank grades, organizational structure, heraldry or uniform entitlement as Imperial Republic canon.
- Check the Charter and actual canon corpus when a rule intersects established lore. Read D:\eotir\projects\music\docs\CANON-SOURCES.md for broader source locations. It is useful context, not permission to overwrite the unresolved rank-source question here.
- Preserve original spellings, uncertainty, merged cells, blank cells, strikeout formatting, sheet/gid, row/column and raw titles. Store proposed corrections separately. A slash title is not automatically two independent ranks; a blank is not automatically an abolished rank or no insignia.
- If implementation would contradict a prior ruling or adopt an unresolved canon choice, stop that dependent action and ask Ryan. Continue independent reversible research and documentation.

## Visual and approval discipline

- Do not turn a grade label or chart background color into a tile-color rule. Define plaque pattern and rank assignment independently.
- Preserve candidate history and source provenance. Approval must identify exact image/version and bytes; record who, when, scope and the ruling.
- Review tiles and plaques at native resolution as well as practical display size. Contact sheets and screenshots help comparison; they do not establish visual approval.
- Keep rank, appointment, branch, dress class, state heraldry, awards and authorization devices distinct. Code cylinders have no recovered universal rank-count mapping here.
- Archived navy shoulder boards were confirmed concepts only by Ryan on 2026-10-07; do not resurrect them as adopted canon. Current evidence: music/docs/OVERMIND-NAVAL-UNIFORM-WORKING-SPEC.md.
- Read current heraldry and anchor rulings before using any phoenix mark. Gold/silver entitlement and High Command membership must not be inferred from rank prefixes. Production branding is separate from in-world insignia.
- Do not alter existing character anchors or released media as a side effect of rank design work.
- Save every project render locally in versioned candidate folders. Preserve approved images locally with exact hashes and provenance. The generator's default output folder is not this project's asset repository.
- Intended final destinations are codex-monarch/content/ranks and content/uniforms, both currently absent. Stage here, transfer approved material later; do not write there in this task.

## Cross-repository boundaries

- Music's source of truth is videos/refs/anchors/*.md and tools/anchor-schema.json. registry.json is GENERATED. Never hand-edit it. The kind insignia is currently reserved, not supported.
- Canon-service lives in codex-monarch/canon-service and uses PostgreSQL; canonical Markdown is authoritative and the DB is its query cache. D1 may serve a projection, never a competing editable canon authority.
- The service currently lacks rank/insignia types and an editorial approval gate. Candidate assets/documents stay outside watched canonical content directories. Setting approval metadata alone does not suppress serving them.
- Discovery does not authorize changes in music, Nexus, admin-tools or codex-monarch, nor any live D1/R2/PostgreSQL writes or deploys.

## Working conventions

- Prefer local shell/file/image tools. Use MCP only where needed for a connected application or when local access is genuinely unavailable.
- Use cmd for Git commands, PowerShell for native Windows file operations. Search with rg first; batch independent reads and keep writes/dependent steps sequential.
- Preserve concurrent work and supplied official/references files. Use exact paths for any eventual commits. Never broad-stage shared checkouts.
- Confirm destructive operations and production deployments first. Show a plan before multi-step shell work. Keep credentials out of commands, logs and documents.
- Invoke installed infrastructure CLIs directly, including wrangler; do not use npx for them. Address core CLI update warnings if encountered.
- Match project style; code comments explain why. Scripts need purpose, usage and prerequisites. AI/agent implementations must document context assumptions and log actual token usage without fabricating unavailable totals.
- Markdown is used for project/engineering documentation. Future wiki-facing canon output uses MediaWiki syntax; the proposed machine-ingested canon record uses Markdown with agreed frontmatter.
- Before non-trivial work scan continuity documents. Record non-obvious findings immediately in docs/insights/. At natural stopping points update docs/sessions/. Prefer a focused existing document over unnecessary new files.
- Apply the user's efficient-frontier and quick-recap skill instructions where applicable. Delegation is authorized by that skill for bounded independent research; workers must have explicit ownership and preserve others' changes.

## Verification

For discovery: verify document links, source hashes, captured ranges, and the military comparison. Distinguish local code inspection from live deployment/database verification. Do not run production publishers or canon ingestion to test a documentation task.

For later implementation: validate the rank dataset independently of images, then pattern geometry/colors and all rank assignments; verify generated HTML/chart/DB consistency. Publication requires an explicit plan, approved input records, scoped writes, read-back metadata, CDN byte hashes and a receipt. Technical checks do not replace Ryan's creative approval.

## Public static review — 2026-10-09

Ryan authorized public repository visibility and GitHub Pages candidate review. Serve main/root with .nojekyll and index.html. Live URL: https://eotir.github.io/eotir-ranks/. This authorization permits exposing candidate pages/images while leaving every visual/assignment approval null and canon-service published/canonical flags false. The approved-input publication gates above still apply to canon promotion and production integration, not this explicitly authorized draft review site. Preserve historical private-delivery receipts; record current public deployment separately in docs/PAGES-PUBLICATION.json.

## Fictional source data and compact dark review — 2026-10-09

Ryan clarified all supplied payroll/personnel content is fictional worldbuilding. Earlier assumptions that those exports contain private real-world personnel data were incorrect. Do not impose real-person privacy restrictions on that material. Focused rank snapshots remain useful for build scope/provenance; full exports are retained locally. Preserve genuine credential exclusions. Ryan also requires a dark-only, compact review UI. Keep source/rationale expandable, maintain fixed physical preview scale and native image links, and distinguish CSS checkerboard preview from real PNG alpha.
