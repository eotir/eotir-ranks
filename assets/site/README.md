# Rank-only Claude Design adaptation

The saved Claude Design handoff supplies the carbon/crimson theme, compact Ledger,
Matrix and Ladder layouts, filters and detail inspector. The authoritative rank
catalog supplies every title, pattern, source assertion and asset path. No exported
synthetic insignia or unrelated site page was imported. Cylinder assignments and
devices come from their separate project datasets and remain candidates.

`python tools/build_review.py --html-only` rebuilds the adapter and HTML without
changing saved plaque/chart bytes. A full 283-row no-JavaScript fallback and one
`review-data` payload preserve independent catalog verification. Dark is the only
theme; Checker changes the preview background only.

To edit executable frontend code, edit `assets/site/rank-ui.jsx`, then run:

```
node tools/build_rank_ui.cjs tmp/claude-design/45f7f4be-3b72-41a7-bb01-6c423eae1019.js
python tools/build_review.py --html-only
python tools/verify_catalog.py
```

The first command requires Node.js and the trusted Babel 7.29.0 standalone file
extracted from Ryan's handoff into ignored `tmp/`. Any trusted local Babel
standalone development copy with the React preset may be passed instead.
Python does not compile JSX. Commit both JSX and compiled JavaScript together.

Only React/ReactDOM 18.3.1 and Latin Chakra Petch, Inter and JetBrains Mono font
subsets from the standalone handoff are served locally. React MIT license is in
`vendor/LICENSE.txt`; font SIL Open Font Licenses are in `fonts/*-OFL.txt`.
There are no runtime external scripts/fonts, Babel or full-site archive assets.
Saved chart downloads are plaque-only snapshots; cylinders appear separately in
the interactive review, with wearer-right on viewer-left.
