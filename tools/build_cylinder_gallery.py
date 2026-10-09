"""Build the large cylinder candidate gallery from saved, verified PNG masters.

Usage: python tools/build_cylinder_gallery.py
Prerequisites: data/code-cylinder-gallery-v2.json and its saved PNG files.
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
OUTPUT = ROOT / "assets/code-cylinder-review.html"
HISTORY = ROOT / "assets/code-cylinder-review-v1.html"


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def build() -> None:
    if not MANIFEST.is_file():
        raise FileNotFoundError(f"Required saved-image manifest is missing: {MANIFEST}")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    candidates = manifest["candidates"]
    if not candidates:
        raise ValueError("The gallery requires at least one candidate.")
    cards = []
    for candidate in candidates:
        relative = Path(candidate["png_path"])
        image = (ROOT / relative).resolve()
        if not image.is_relative_to((ROOT / "assets/cylinders/v2").resolve()):
            raise ValueError(f"Candidate PNG must be inside assets/cylinders/v2: {relative}")
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
        description = candidate.get("description", descriptions.get(candidate["id"], "Independent cylinder design study."))
        cards.append(f'''<article id="{esc(candidate['id'])}">
<header><span class="status">CANDIDATE</span><h2>{esc(label)}</h2></header>
<a class="preview" href="{esc(url)}" target="_blank" rel="noopener" aria-label="Open full-size {esc(label)}"><img src="{esc(url)}" alt="{esc(label)} — full cylinder design candidate" width="{width}" height="{height}"></a>
<div class="caption"><p>{esc(description)}</p><p class="dimensions">{width:,} × {height:,} px · original PNG</p>
<nav aria-label="Image actions"><a href="{esc(url)}" target="_blank" rel="noopener">Open native size ↗</a><a href="{esc(url)}" download>Download PNG ↓</a></nav></div></article>''')
    # Snapshot before replacing the entrypoint, so earlier component/layout
    # studies remain accessible and later builds cannot overwrite that history.
    if not HISTORY.exists():
        HISTORY.write_bytes(OUTPUT.read_bytes())
    document = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Imperial Republic — full-size cylinder candidates</title><style>
:root{color-scheme:dark;font-family:system-ui,sans-serif;font-size:13px;color:#e4eaf1;background:#0b1016}*{box-sizing:border-box}body{max-width:1500px;margin:0 auto;padding:24px}a{color:#9dccfa;text-underline-offset:3px}h1{font-size:24px;margin:10px 0}h2{font-size:15px;line-height:1.4;margin:7px 0 0}p{line-height:1.55;color:#b8c7d7;margin:8px 0}.intro{max-width:95ch}.eyebrow,.status{font:11px/1.4 ui-monospace,monospace;letter-spacing:.1em;color:#efba74}.toolbar{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin:20px 0}button{font:inherit;padding:6px 10px;color:#e4eaf1;background:#172432;border:1px solid #47566b;border-radius:4px;cursor:pointer}button:focus-visible,a:focus-visible{outline:2px solid #9dccfa;outline-offset:4px}main{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}article{min-width:0;border:1px solid #2e3a48;border-radius:7px;overflow:hidden;background:#131c26}article header{padding:15px;min-height:85px}.preview{height:520px;display:flex;align-items:center;justify-content:center;padding:10px;background:#0d141d}.preview img{display:block;max-height:500px;max-width:100%;width:auto;height:auto;object-fit:contain}.caption{padding:15px}.caption p{min-height:42px}.caption .dimensions{min-height:0;font:11px/1.5 ui-monospace,monospace;color:#92a5b9}nav{display:flex;gap:15px;flex-wrap:wrap;margin-top:14px}.checker .preview{background-color:#14202c;background-image:conic-gradient(#263747 25%,transparent 0 50%,#263747 0 75%,transparent 0);background-size:24px 24px}.note{margin-top:20px;border-top:1px solid #2e3a48;padding-top:15px}footer{margin-top:25px;font-size:12px;color:#92a5b9}@media(min-width:1250px){.preview{height:620px}.preview img{max-height:600px}}@media(max-width:850px){main{grid-template-columns:1fr}.preview{height:500px}.preview img{max-height:480px}body{padding:16px}article header{min-height:0}}
</style></head><body>
<div class="eyebrow">IMPERIAL REPUBLIC · VISUAL DEVELOPMENT</div>
<h1>Code cylinder design candidates</h1>
<p class="intro">Large, separately saved cylinder studies for comparing shape, clip construction and finish. Review each full-size image before choosing a design to fit beside rank plaques.</p>
<p class="intro"><strong>These are unapproved design options.</strong> They have not been fitted to plaques and do not replace the cylinders currently used in rank previews. Rank counts and wearer-side assignments are separate decisions.</p>
<div class="toolbar"><a href="catalog-review.html">Rank catalog</a><a href="code-cylinder-review-v1.html">Earlier component and layout studies</a><button id="checker" type="button" aria-pressed="false">Show transparency checker</button><a href="../data/code-cylinder-gallery-v2.json">Manifest and image hashes</a></div>
<main>__CARDS__</main>
<p class="note">PNG alpha is part of each saved image; the optional checker is only a CSS preview background. Open a native image to inspect the full resolution. These design studies still need alpha-edge cleanup before fitting beside plaques; inspect halos and isolated flecks on the checker. No small-preview artwork is enlarged to create these masters.</p>
<footer>Candidate history is retained locally. Selection and canon approval require Ryan’s explicit ruling on the exact version.</footer>
<script>document.getElementById('checker').addEventListener('click',function(){const enabled=document.body.classList.toggle('checker');this.setAttribute('aria-pressed',String(enabled));this.textContent=enabled?'Use plain dark background':'Show transparency checker';});</script>
</body></html>'''.replace("__CARDS__", "\n".join(cards))
    OUTPUT.write_text(document, encoding="utf-8", newline="\n")
    print(f"Built {OUTPUT.relative_to(ROOT)} with {len(cards)} verified full-size candidate PNGs.")


if __name__ == "__main__":
    build()
