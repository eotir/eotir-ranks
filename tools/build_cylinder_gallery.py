"""Build the large cylinder candidate gallery from saved, verified PNG masters.

Usage: python tools/build_cylinder_gallery.py
Prerequisites: data/code-cylinder-gallery-v2.json and its saved PNG files.
Optional input: data/code-cylinder-engravings-v3.json adds engraving variants.
This script never generates artwork or changes cylinder/rank assignments. It
preserves the first component review as an unchanged historical HTML snapshot.
"""
from __future__ import annotations

import hashlib
import html
import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/code-cylinder-gallery-v2.json"
ENGRAVINGS = ROOT / "data/code-cylinder-engravings-v3.json"
OUTPUT = ROOT / "assets/code-cylinder-review.html"
HISTORY = ROOT / "assets/code-cylinder-review-v1.html"


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def build() -> None:
    if not MANIFEST.is_file():
        raise FileNotFoundError(f"Required saved-image manifest is missing: {MANIFEST}")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    candidates = list(manifest["candidates"])
    if ENGRAVINGS.exists():
        candidates.extend(json.loads(ENGRAVINGS.read_text(encoding="utf-8"))["candidates"])
    if not candidates:
        raise ValueError("The gallery requires at least one candidate.")
    if len({candidate["id"] for candidate in candidates}) != len(candidates):
        raise ValueError("Each base and engraving candidate must have a distinct ID.")
    cards = []
    for candidate in candidates:
        relative = Path(candidate["png_path"])
        image = (ROOT / relative).resolve()
        if not any(image.is_relative_to((ROOT / f"assets/cylinders/{version}").resolve()) for version in ("v2", "v3")):
            raise ValueError(f"Candidate PNG must be inside assets/cylinders/v2 or v3: {relative}")
        blob = image.read_bytes()
        if blob[:8] != b"\x89PNG\r\n\x1a\n":
            raise ValueError(f"Not a PNG: {relative}")
        width, height = struct.unpack(">II", blob[16:24])
        dimensions = candidate["dimensions"]
        expected = tuple(dimensions) if isinstance(dimensions, list) else (dimensions["width"], dimensions["height"])
        if expected != (width, height):
            raise ValueError(f"PNG dimensions disagree with manifest: {relative}")
        if hashlib.sha256(blob).hexdigest() != candidate["png_sha256"]:
            raise ValueError(f"PNG bytes disagree with manifest: {relative}")
        if candidate["status"].upper() != "CANDIDATE" or candidate.get("approval") is not None:
            raise ValueError("This gallery presents unapproved candidates only.")
        url = image.relative_to(ROOT / "assets").as_posix()
        label = candidate["label"]
        descriptions = {
            "long-blue-dosimeter-v2": "Long silver dosimeter family with a blue head and a distinct pocket clip.",
            "compact-grooved-blue-v2": "Compact blue-head family with a grooved metal body and a broader silhouette.",
            "ribbed-pilot-silver-v2": "Silver pilot-style family with ribbed metal detailing and a separate clip profile.",
        }
        heraldry = str(candidate.get("heraldry", "base")).lower()
        metal = str(candidate.get("metal", "original")).lower()
        description = candidate.get("description", descriptions.get(candidate["id"], f"{heraldry.title()} engraving study with {metal} metal finish."))
        cards.append(f'''<article class="cg-card" id="{esc(candidate['id'])}" data-heraldry="{esc(heraldry)}" data-metal="{esc(metal)}">
<header><span class="rk-chip">CANDIDATE</span><h2>{esc(label)}</h2></header>
<a class="preview" href="{esc(url)}" target="_blank" rel="noopener" aria-label="Open full-size {esc(label)}"><img src="{esc(url)}" alt="{esc(label)} — full cylinder design candidate" width="{width}" height="{height}"></a>
<div class="caption"><p>{esc(description)}</p><p class="dimensions">{width:,} × {height:,} px · saved master PNG</p>
<nav aria-label="Image actions"><a href="{esc(url)}" target="_blank" rel="noopener">Open native size ↗</a><a href="{esc(url)}" download>Download PNG ↓</a></nav></div></article>''')
    # Snapshot before replacing the entrypoint, so earlier component/layout
    # studies remain accessible and later builds cannot overwrite that history.
    if not HISTORY.exists():
        HISTORY.write_bytes(OUTPUT.read_bytes())
    document = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Imperial Republic — code cylinder catalog</title>
<link rel="stylesheet" href="site/rank-catalog.css?v=__SHARED_CSS_HASH__"><link rel="stylesheet" href="site/cylinder-gallery.css?v=__GALLERY_CSS_HASH__">
</head><body><div class="rk-app">
<header class="rk-header"><div class="rk-header-l"><span class="rk-mark" aria-hidden="true"></span><div><div class="eo-micro">Imperial Republic · Visual Standards</div><div class="rk-wordmark">Code Cylinder Catalog</div></div></div><nav class="cg-nav" aria-label="Catalog navigation"><a href="catalog-review.html">Rank catalog</a><a href="code-cylinder-review-v1.html">Earlier studies</a></nav></header>
<main class="rk-main">
<section class="rk-brief"><div><div class="rk-strip"><span>Candidate</span><span>Design study</span><span>Approval pending</span></div><h1>Cylinder design library</h1><p>Full-size masters for comparing silhouette, clip construction, finish and heraldry. These options are not yet fitted beside plaques. Existing rank assignments and preview devices remain separate.</p></div><dl class="rk-stats"><div><dt>Base designs</dt><dd>__BASE_COUNT__</dd></div><div><dt>Engravings</dt><dd>__VARIANT_COUNT__</dd></div><div><dt>Approved</dt><dd>0</dd></div></dl></section>
<section class="rk-filters" aria-label="Gallery filters"><div class="rk-fgroup"><span class="eo-micro">Heraldry</span><div class="rk-pills" data-filter="heraldry"><button type="button" data-value="all" aria-pressed="true">All</button><button type="button" data-value="base" aria-pressed="false">Original bases</button><button type="button" data-value="standard" aria-pressed="false">Standard</button><button type="button" data-value="shield" aria-pressed="false">Shield</button></div></div><div class="rk-fgroup"><span class="eo-micro">Metal finish</span><div class="rk-pills" data-filter="metal"><button type="button" data-value="all" aria-pressed="true">All</button><button type="button" data-value="silver" aria-pressed="false">Silver</button><button type="button" data-value="gold" aria-pressed="false">Gold</button></div></div><div class="rk-fgroup rk-fgroup--end"><span class="eo-micro">Preview</span><div class="rk-pills"><button id="checker" type="button" aria-pressed="false">Transparency checker</button></div></div></section>
<div class="rk-secbar"><span class="rk-secbar-code">CC</span><span>Native master gallery</span><span id="visible-count" class="rk-secbar-n" role="status">__COUNT__ designs</span></div>
<div class="cg-grid">__CARDS__</div><p id="empty" class="rk-note" hidden>No designs match these filters. Choose All to include original bases.</p>
<div class="cg-notes"><p class="rk-note">Open any image for native resolution or download its original PNG. PNG alpha belongs to the saved image; the optional checker is a CSS preview background. Alpha-edge cleanup is still needed before fitting: inspect halos and isolated flecks against the checker.</p><p class="rk-note">Gold studies explore the High Command finish direction; no grade or membership is assigned here. Some gold marks read as raised relief or inlay rather than recessed engraving. Heraldry was conditioned on the saved anchors and still needs exact-design review.</p><p class="rk-dim">A base-design selection does not approve its engraving, placement, entitlement or rank mapping. Saved masters and earlier studies remain available for review.</p><nav class="cg-nav" aria-label="Provenance"><a href="../data/code-cylinder-gallery-v2.json">Base manifest and hashes</a>__ENGRAVING_LINK__</nav></div>
</main></div><script>
const filters={heraldry:'all',metal:'all'};
function update(){let count=0;document.querySelectorAll('.cg-card').forEach(card=>{const show=Object.entries(filters).every(([key,value])=>value==='all'||card.dataset[key].includes(value));card.hidden=!show;if(show)count++;});document.getElementById('visible-count').textContent=count+' designs';document.getElementById('empty').hidden=count!==0;}
document.querySelectorAll('[data-filter] button').forEach(button=>button.addEventListener('click',()=>{const group=button.closest('[data-filter]');filters[group.dataset.filter]=button.dataset.value;group.querySelectorAll('button').forEach(other=>other.setAttribute('aria-pressed',String(other===button)));update();}));
document.getElementById('checker').addEventListener('click',function(){const enabled=document.body.classList.toggle('cg-checker');this.setAttribute('aria-pressed',String(enabled));});
</script></body></html>'''.replace("__CARDS__", "\n".join(cards)).replace("__BASE_COUNT__", str(len(manifest["candidates"]))).replace("__VARIANT_COUNT__", str(len(candidates)-len(manifest["candidates"]))).replace("__COUNT__", str(len(candidates))).replace("__ENGRAVING_LINK__", '<a href="../data/code-cylinder-engravings-v3.json">Engraving manifest and hashes</a>' if ENGRAVINGS.exists() else '')
    # Byte-derived versions prevent a refreshed gallery from pairing with a
    # cached layout stylesheet after publishing new masters or presentation.
    for token, stylesheet in (("__SHARED_CSS_HASH__", "rank-catalog.css"), ("__GALLERY_CSS_HASH__", "cylinder-gallery.css")):
        digest = hashlib.sha256((ROOT / "assets/site" / stylesheet).read_bytes()).hexdigest()[:12]
        document = document.replace(token, digest)
    OUTPUT.write_text(document, encoding="utf-8", newline="\n")
    print(f"Built {OUTPUT.relative_to(ROOT)} with {len(cards)} verified full-size candidate PNGs.")


if __name__ == "__main__":
    build()
