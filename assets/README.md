# Local asset repository

Kept/approved images must remain local. Every project render is copied into this workspace, including initial candidates.

- tiles/candidates/2026-10-09/: separate colored tile renders, versioned filenames.
- plaques/candidates/2026-10-09/: unassigned plaque composition studies.
- Future tiles/keepers/ and plaques/keepers/: exact approved bytes, after explicit approval. Preserve candidate history.
- Code cylinders: future separate component library; no cylinder-count/rank rules inferred.

The render manifest records prompts, tool, references, output paths, dimensions, alpha, hashes and QC. Candidate existence is not canon approval. Never overwrite an approved file during iteration.

Starting direction: tall rectangular colored faces with beveled relief and restrained texture, informed by supplied Combine/Whatsahonda references. Exact proportions, material and rank assignments remain review decisions.

## Current candidates — 2026-10-09

Open [review.html](review.html) locally. It previews sixteen color/material options, two plaque layouts and links the preserved initial red iteration. Switch between checkerboard, light and dark backgrounds, then open the individual PNGs for native-resolution inspection.

- Neutral enamel: black, charcoal, grey, pearl white (white v1) and bright white (white v2).
- Colored enamel: red v2, orange, amber, yellow/gold, green, teal, cyan, blue and purple.
- Metallic faces: satin silver and metallic gold. These differ from grey/white and yellow/gold enamel.
- All seventeen tile PNGs, including preserved red v1, are 1024×1536 RGBA. The canvas size is not a physical tile dimension. White v1 and v2 are distinct variants; neither is user-selected or approved.
- Single-row study: 2043×770; six tiles ordered red, red, blue, blue, gold, gold.
- Double-row study: 1774×887; top blue ×3 then gold ×3; bottom blue ×3 then red ×3.
- No rank assignments, code cylinders or keeper approvals exist.

[Render manifest](render-manifest-2026-10-09.json) contains the exact generation prompts, tool, references, hashes, dimensions and transparency metadata. Native renders were inspected and tile counts/order checked. The palette and early composition studies account for nineteen PNGs. Nine additional enlisted versions bring the current total to twenty-eight exact generator copies. All have fully transparent outside pixels; individual tile alpha peaks at 254 rather than 255. Alpha presence alone does not prove clean edges or visual acceptance.

Review the strong surface texture, silver rim width, proportions and subtle edge fringes before adoption. The generative plaques subtly redraw the tiles, so they are composition studies rather than an exact assembly library. Follow design approval with repeatable SVG geometry/PNG composition before producing rank-specific assets.

Ryan requested mix-and-match options for possible specialty branches, departments and divisions. No palette entry has an assigned organizational meaning. Compare an accent tile on a shared rank pattern against a separate department palette before adopting either approach.

## First rank-associated series

[Military enlisted review](military-enlisted-review.html) covers E-1…E-7, shared across Navy, Marine and Army, using [working records](../data/military-enlisted-working.json). Ryan selected the grey/blue draft family; each image and association remains CANDIDATE. Seven current grade images plus E-1/E-4 history are stored in plaques/candidates/2026-10-09/enlisted/.

E-1 has two grey tiles; E-2 one grey over one blue, with one further column per subsequent grade. E-7 is a proposed extension beyond the saved external reference's E-6 ceiling. Generative tile proportions/frames still vary; the [continuation prompt](../docs/GOAL-PROMPT.md) explicitly authorizes exact component composition for the complete chart when invoked.

## Complete deterministic candidate library

The complete review entry is [catalog-review.html](catalog-review.html), linked from [review.html](review.html). Normalized components in components/v1 retain the original candidate texture and use a common 160 × 270 pixel footprint. Individually addressable PNG/SVG plaques in composed/ use exact ordered arrays from ../data/rank-catalog.json; their manifest records placement, hashes, dimensions and candidate status. No generator originals were replaced. charts/ contains military, all-branch and individual-branch graphics. Early generative studies remain history rather than authoritative geometry. See ../docs/PATTERN-RATIONALE.md for adaptations and color proposals.
