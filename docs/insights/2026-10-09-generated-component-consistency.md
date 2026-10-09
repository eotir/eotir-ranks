# Generated tile consistency and transparency need separate checks
Date: 2026-10-09
Project: Imperial Republic ranks
Tags: image-generation, tiles, plaques, transparency, reproducibility

## Context

Create separate beveled rectangular tile candidates, then arrange them into plaque studies while preserving local files and approval state.

## What we tried

1. Generated red v1 from the reviewed references, then a red v2 transparency-cleanup iteration.
2. Used local red v2 to condition six additional color studies.
3. Used local red/blue/gold references for six-tile and twelve-tile plaque compositions.
4. Copied every output unchanged into the workspace, checked hashes/dimensions/alpha, and inspected actual PNGs in an offline browser gallery.
5. Added nine palette/material variants at Ryan's request, keeping bright/pearl white and metallic/enamel gold distinct. Specialty branch/department/division use remains an open design question.
6. Rendered E-1…E-7 after Ryan selected the shared grey/blue family. Iterated E-1/E-4 geometry and retained the originals; counts/order match but tile proportions and framing still vary.

## What happened

Counts and color order match the plaque prompts, but generated plaques subtly change component geometry/material. They do not copy the exact source tile pixels. The generator's display shows dark surroundings; the real PNGs contain fully transparent outside pixels and display on the browser checkerboard. All seventeen individual tile PNGs peak at alpha 254, while the two plaques include alpha 255. Metadata alone cannot establish clean-looking edges. The metallic faces use brushed highlights, while neutral enamel uses the original textured finish; color and material both need explicit records.

## Root cause / why

Image generation produces a new render conditioned on references, not a deterministic component assembly. The visual background used to display an RGBA image can obscure its actual transparency. Alpha and creative acceptance therefore need different checks.

The saved Combine enlisted ladder ends at E-6 and calls E-1 Recruit; our E-1 is Crewman/Private and our ladder adds E-7. The draft adapts the visual family to our grade positions without importing the external titles. E-7 must remain explicitly a proposed extension. A common grade label is not proof of identical rank semantics across universes.

## Takeaway

Use generation for material/layout candidates, then use repeatable composition after the design is settled to preserve exact tile counts, positions and appearance. Save exact outputs/prompts/hashes locally and inspect alpha on multiple backgrounds before requesting approval.

## References

- [Local review page](../../assets/review.html)
- [Render manifest](../../assets/render-manifest-2026-10-09.json)
- [Metadata verifier](../research/verify_local_assets.py)
- [Local verification](../research/local-verification-2026-10-09.json)

## Exact-composition continuation

The saved Combine GIFs can contain fully transparent pixels with white RGB channels. Ignoring alpha invents a white tile row, notably ISBO-4 through ISBO-6 and ISBC-1 through ISBC-4. Decode RGBA face samples and discard transparent padding before classifying colors.

Deterministic assembly now preserves original texture inputs, fits alpha-safe rim crops, normalizes 16 tiles to 160 × 270, and uses ordered arrays with fixed gaps/backplate geometry. Verification reconstructs each PNG pixel and checks embedded SVG component bytes and coordinates. This proves composition fidelity, not canon or creative acceptance. The rank-only snapshot makes source comparisons reproducible without publishing payroll/personnel exports.

## Git and document byte fidelity

Git autocrlf can change captured MHTML, JSON and SVG bytes during staging/checkout, invalidating manifest hashes even when content looks identical. This repository uses .gitattributes with * -text to preserve exact bytes across hosts. Verify index blob hashes against local files before claiming a reproducible delivered asset repository. Windows document scripts must explicitly read/write UTF-8 to avoid punctuation corruption.
