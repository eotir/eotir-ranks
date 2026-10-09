# Imperial Republic ranks and visual standards

Candidate library for the Era of the Imperial Republic. Exact creative approval, rank-pattern adoption and canon promotion remain pending.

Browse the [live candidate catalog](https://eotir.github.io/eotir-ranks/).

Open [assets/review.html](assets/review.html) for the review hub and preserved tile history. [The complete catalog](assets/catalog-review.html) provides military and specialty branch candidates, filters, source assertions, ordered patterns, native PNG/SVG links and unresolved shared upper titles.

- [Military chart PNG](assets/charts/military-chart.png) / [SVG](assets/charts/military-chart.svg).
- [All branches PNG](assets/charts/all-branches-chart.png) / [SVG](assets/charts/all-branches-chart.svg); individual branch charts are linked from the catalog.
- [Working catalog](data/rank-catalog.json): 210 populated branch records including 69 military; 66 source blanks; seven shared upper records represented separately.
- [Composition manifest](assets/composed/manifest.json) and [design system](assets/design-system.json): exact candidate input bytes, ordered patterns, geometry and hashes.
- [Pattern rationale](docs/PATTERN-RATIONALE.md), [decisions](docs/DECISIONS.md), [sources](sources.md) and [discovery](docs/DISCOVERY.md).
- [Intent](INTENT.md), [agent instructions](AGENTS.md), [integration plan](docs/INTEGRATION.md) and [future transfer examples](staging/README.md).
- [Completion report](docs/COMPLETION-REPORT.md): requirement audit and exact next review.
- [Session handoff](docs/sessions/2026-10-09-session.md) and [goal brief](docs/GOAL-PROMPT.md).

## Rebuild locally

In a terminal in this repository, install Python 3.10+ and dependencies, then run these commands in order:

```sh
python -m pip install -r requirements.txt
python tools/build_catalog.py
python tools/compose_assets.py --verify
python tools/build_cylinders.py
python tools/build_cylinder_assignments.py
python tools/build_review.py
python tools/verify_cylinders.py
python tools/verify_catalog.py
```

Charts use an available documented font; raster chart bytes can differ across font installations. Source textures and composition geometry remain fixed. Open HTML directly from disk; no application server or database is required.

The rank-only workbook snapshot is versioned. Historical official exports and the raw workbook capture stay local and ignored as full historical fictional worldbuilding exports; the working catalog uses a focused rank-only extract. The legacy discovery verifier needs those local files and original generator outputs; the complete-catalog verifier above is the repository check.

Public draft repository: https://github.com/eotir/eotir-ranks. This is staging for later approved transfer to codex-monarch/content/ranks and content/uniforms. Candidates remain outside watched canonical content. No live service, database or production publication is part of this build.

Dependency minimum: [Pillow 12.1 release notes](https://pillow.readthedocs.io/en/stable/releasenotes/12.1.0.html) introduce the pixel API used by the composer. Verified environment: Pillow 12.1.1.

## Static review site

GitHub Actions publishes the saved static review files from main to GitHub Pages. index.html opens the complete candidate chart; .nojekyll disables theme/Jekyll processing so saved assets are served directly. Pushing main updates the site automatically. Public publication is a review convenience and does not promote candidates to canon. The Pages API and public HTTP/browser checks establish the current deployment state.

Ryan clarified that all supplied payroll/personnel material belongs to the fictional Imperial Republic universe. Earlier privacy wording was an incorrect assumption; it is not a reason to withhold fictional source material. Secrets remain excluded.

Publication workflow: .github/workflows/pages.yml packages existing assets/data/docs/references and root review documents. It does not regenerate images or ingest canon. GitHub Pages uses workflow deployment after two managed branch builds failed before running their build steps.

## Code cylinders and redesigned catalog

The Claude Design catalog supplies ledger, matrix and ladder views plus a rank inspector. Existing plaques and authoritative candidate/source data are retained; unrelated exported site content stays in ignored staging. Separate [cylinder components](assets/code-cylinder-review.html) include full/exposed devices and nine side-count arrangements. [Cylinder research and rules](docs/CODE-CYLINDERS.md) explain the provisional 69 military associations, external orientation conflict, enlisted no-device proposal and unresolved other branches. Existing chart downloads remain plaque-only snapshots.

The runtime is served locally with checked-in React/ReactDOM; the source presentation is assets/site/rank-ui.jsx and its compiled runtime is assets/site/rank-ui.js. The Python builder refreshes data and HTML without regenerating plaque bytes.
