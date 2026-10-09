# Imperial Republic visual gallery integration

Date: 2026-10-09  
Status: researched integration proposal; no content merge, approval change or deployment  
Owner: Ryan (Stratus)

Ryan's subsequent role clarification: Codex focuses on image generation, asset masters, variants and provenance. Claude Code is intended to bring the site/gallery collections together, having handled the overall design. This document is Claude's integration handoff; it does not start a Codex site-merger implementation.

## What the new handoff actually contains

`D:\eotir\projects\.handoffs\EOTIR.zip` is 114,981,174 bytes, SHA256
`73344616b24abcefe2b37e3e2ff0a976ec7198d6fcc9bc468e1e789e58d8b6da`.
All 558 entries passed absolute-path, parent-traversal, Windows-separator/drive
and symlink checks. Text sources and the fifty referenced lightsaber PNGs were
selectively extracted into ignored `tmp/eotir-master-design`; archive bytes were
not modified. Full evidence and per-file/image hashes are in
[the research receipt](research/eotir-master-design-2026-10-09.json).

The archive has a functioning `gallery/` static lightsaber collection: index,
CSS, JavaScript, authoring catalog and deployed manifest. It has 25 weapon
records, each with unlit and ignited views: fifty real PNG originals. Every image
decoded successfully, at widths 1,536–2,172 pixels. Pearl & Gold and the Jim
training-reference unlit masters were inspected visually at native resolution;
these are rendered artworks, not generic placeholder cards. The archive's root
index is a broader design showroom, not an implemented master asset-category
gallery. Forum/profile/activity examples elsewhere in the theme are presentation
fixtures and must not become new universe facts.

The archive also contains the **old** rank design export: 210 branch records,
66 blanks, seven shared records, 178 pattern entries and rank WebP previews.
It does not contain the current separate cylinder assignments, accepted large
cylinder bases or twelve engraved versions. Importing its ranks wholesale would
regress current work. Retain this repository's authoritative rank data, PNG/SVG
masters, assignments, full-size cylinder manifests and Claude-based generators.

## Approval and source evidence

The lightsaber manifest pins `codex-monarch` revision
`67e25928a4eb559ec460b0f51ff0996244985bc2` and `eotir-art` revision
`ee1129ab42c93c561b996fd23f9e2984316d9270`. Twenty-four records say
`Design-approved visuals`; one says `Training role confirmed; image approval
unspecified`. Exact source and approval Markdown URLs are included, but those
Markdown files and exact-byte approval receipts are absent from this ZIP. Treat
these as sourced exported assertions until checked against the actual corpus.
Neither an approved-looking filename nor a design approval establishes all
character associations, ownership, chronology, measurements or weapon names.

The legacy field `owner` is displayed by the supplied UI as **Associated
character**, and its notes qualify uncertain possession and in-use associations.
Preserve those distinctions in any adapter. Do not turn a non-null association
into confirmed ownership, nor equate primary role with handedness. Preserve
Eric's in-use qualification, Daniela's uncertain possession and recorded role/
handedness unknowns when reconciling with the upstream art/canon records.

Root research independently identified the existing selected-art gallery at
`https://eotir-lightsabers.stratusweb-ops.workers.dev/`, sourced from the private
`eotir/eotir-art` repository. That existing public allowlist projection is the
starting integration surface; private raw art and unrelated records are not
automatically new public gallery inputs. Its live state is verified separately
by the root task, not by this ZIP inspection. Current revalidation returned HTTP
403 from the Worker root through a native HTTP client, while the web tool could
not access it. Its prior publication is historical evidence, not a fresh claim
of public reachability. The cause may be client or Cloudflare policy and remains
unknown; this discovery does not change Access or deployment settings. Root
verified the current art repository HEAD as
`d2acc7311bf2a0f57af4ea82a04a82296d0bf780`, distinct from the pinned gallery
artifact revision. Reconcile the allowlist and sources before rebuilding.

Current rank and cylinder states also remain distinct: rank assignments and
engraving applications are candidates; Ryan accepted the three cylinder base
directions for further development. Approval of a base does not approve its
engraving, every fitted derivative or its grade entitlement.

## Concrete staging architecture

Use a common Claude Design carbon/crimson shell with shared navigation and local
Chakra Petch, Inter and JetBrains Mono typography. Build one **visual index** over
category adapters, preserving native specialized views rather than replacing
the rank matrix with weapon cards. The visual index is a generated review
projection, not a second editable canon authority.

| Proposed route | Initial authoritative input | Specialized view |
|---|---|---|
| `/gallery/` | Generated category/index manifest | Searchable visual wiki entry cards; explicit status and source |
| `/gallery/armory/lightsabers/` | Existing selected art gallery manifest + verified corpus assertions | Hilt/blade cards, unlit/ignited switching, image inspection |
| `/gallery/ranks/` | Current `data/rank-catalog.json`, composed/charts manifests | Existing Ledger/Matrix/Ladder and source inspector |
| `/gallery/uniform-devices/code-cylinders/` | Current cylinder assignment/base/engraving manifests | Full-size versioned studies and wearer-side arrangements |
| `/gallery/ships/` | Future verified ship allowlist/manifest | Empty until real source-backed assets are available |

Armory is a broad equipment collection; ranks and uniforms have their own
semantics. A navigation grouping may link them without making a code cylinder
a weapon or assigning fictional equipment entitlement from rank alone.

Each projected visual record should carry a namespaced stable identity,
category, title, exact master file URL/hash/dimensions, derivative parent hash,
source repository/revision/path, raw source assertions, and separate visual,
association and canon approval state/evidence. Include a status object rather
than one boolean that conflates `candidate`, `accepted base`, `selected`,
`design-approved`, `locked`, `published` and `canonical`. Preserve null unknowns.

Category adapters retain the complete original source record alongside the
normalized index entry. Ranks keep branch/grade, exact ordered pattern,
alternatives, source blanks and shared unresolved titles. Cylinders keep wearer
left/right versus viewer left/right conventions and accepted-base/engraving
parents. Lightsabers keep association qualifiers, variant/role and source-specific
approval assertions. Ships must not infer owners, dimensions or faction from
appearance. Canonical Markdown remains authoritative; database caches and the
gallery derive from approved records under the established service model.

## Link first, then merge presentation

Recommended first implementation: a master staging landing/index page with the
Claude shell and links to the already published rank/cylinder and selected-art
gallery projections. This delivers a joined entry point with minimal risk and
does not copy private art or replace working category tools. A generated central
search index can follow after source/adoption checks.

Alternative: copy verified allowlisted artifacts into a single static build,
with unified category routes and shared fonts/styles. It permits one-domain
search, offline exports and consistent image inspection, but requires explicit
source revision/hash checks, allowlist parity and maintenance of adapters.
Neither approach requires moving source repositories or inventing a new database
now. Prefer immutable commit-pinned artifact inputs over scraping live DOM or
an iframe-only solution; if an upstream changes, rebuild from a recorded revision.

The supplied gallery currently fetches `./manifest.json`, validates local image
paths, builds text through DOM `textContent`, filters by association/blade/search
and uses a native dialog with Escape, arrow navigation and focus restoration.
It has no category/item URL state, and its 404 Return link points to `/`.
Mount-relative URLs and stable item deep links must be added for a combined
Pages subpath build. Its source URL validator only accepts the two pinned
repository subtrees: extend it deliberately per category, not by disabling it.
The gallery asks Google for fonts; the rank site already vendors the matching
fonts locally, which can support the merged shell without a new runtime CDN.

## Integration sequence and checks

1. Verify selected lightsaber manifest/assets and approval evidence against the
   exact upstream revisions; keep an import/read-back receipt and publication
   allowlist. Preserve current full-size rank/cylinder masters byte-for-byte.
2. Build the master staging shell and links. Label ships/unavailable categories
   as pending source inputs; omit decorative fake records.
3. Add category adapters and a generated index, with deterministic IDs, source
   links, native-size master access, statuses and uncertainty. Keep specialty
   rank views and full cylinder gallery available.
4. Add deep links, back navigation, responsive/native image inspection, keyboard
   controls and the common compact dark styles; check subpath/404 behavior.
5. Verify record counts, source approval/allowlist parity, all original asset
   hashes, derivative parent links, no broken resources and filter behavior.
   Inspect original artwork and desktop/mobile UI separately. Only then publish
   the explicitly scoped review projection with a read-back receipt.
6. Transfer approved canon material later through the existing `codex-monarch`
   ingestion model. Intended ranks/uniforms destinations remain
   `content/ranks` and `content/uniforms`; the existing lightsaber corpus already
   uses `sources/visual-designs/lightsabers`. Do not relocate it or invent a
   replacement canonical ships destination without a corpus/schema decision.

## Boundaries of this discovery

This research changed only this plan, its evidence receipt and ignored local
extraction. It did not import the site, regenerate artwork, overwrite rank or
cylinder data, edit `eotir-art`, publish another site or promote any canon state.
Local code and PNG inspection are verified; archive-source approval assertions
and future unified routing are not an executed merge.
