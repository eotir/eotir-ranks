# Imperial Republic ranks and visual standards

Candidate library for the Era of the Imperial Republic. Exact creative approval, rank-pattern adoption and canon promotion remain pending.

Open [assets/review.html](assets/review.html) for the review hub and preserved tile history. [The complete catalog](assets/catalog-review.html) provides military and specialty branch candidates, filters, source assertions, ordered patterns, native PNG/SVG links and unresolved shared upper titles.

- [Military chart PNG](assets/charts/military-chart.png) / [SVG](assets/charts/military-chart.svg).
- [All branches PNG](assets/charts/all-branches-chart.png) / [SVG](assets/charts/all-branches-chart.svg); individual branch charts are linked from the catalog.
- [Working catalog](data/rank-catalog.json): 210 populated branch records including 69 military; 66 source blanks; seven shared upper records represented separately.
- [Composition manifest](assets/composed/manifest.json) and [design system](assets/design-system.json): exact candidate input bytes, ordered patterns, geometry and hashes.
- [Pattern rationale](docs/PATTERN-RATIONALE.md), [decisions](docs/DECISIONS.md), [sources](sources.md) and [discovery](docs/DISCOVERY.md).
- [Intent](INTENT.md), [agent instructions](AGENTS.md), [integration plan](docs/INTEGRATION.md) and [future transfer examples](staging/README.md).
- [Completion report](docs/COMPLETION-REPORT.md): requirement audit and exact next review.
- [Completion report](docs/COMPLETION-REPORT.md): requirement audit and next review.
- [Session handoff](docs/sessions/2026-10-09-session.md) and [goal brief](docs/GOAL-PROMPT.md).

## Rebuild locally

In a terminal in this repository, install Python 3.10+ and dependencies, then run these commands in order:

```sh
python -m pip install -r requirements.txt
python tools/build_catalog.py
python tools/compose_assets.py --verify
python tools/build_review.py
python tools/verify_catalog.py
```

Charts use an available documented font; raster chart bytes can differ across font installations. Source textures and composition geometry remain fixed. Open HTML directly from disk; no application server or database is required.

The rank-only workbook snapshot is versioned. Historical official exports and the raw workbook capture stay local and ignored because they contain unrelated personal/payroll material. The legacy discovery verifier needs those local files and original generator outputs; the complete-catalog verifier above is the repository check.

Private draft repository: https://github.com/eotir/eotir-ranks. This is staging for later approved transfer to codex-monarch/content/ranks and content/uniforms. Candidates remain outside watched canonical content. No live service, database or production publication is part of this build.

Dependency minimum: [Pillow 12.1 release notes](https://pillow.readthedocs.io/en/stable/releasenotes/12.1.0.html) introduce the pixel API used by the composer. Verified environment: Pillow 12.1.1.
