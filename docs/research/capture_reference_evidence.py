"""Purpose: inventory supplied sources and expose local reference art for discovery.
Usage: python docs/research/capture_reference_evidence.py
Prerequisites: Python 3 and Pillow. Run in this ranks workspace.
Only writes derived evidence under docs/research; never modifies supplied sources.
This is inspection tooling, not a plaque generator or canon importer.
"""
from pathlib import Path
from datetime import datetime, timezone
from email import policy
from email.parser import BytesParser
from io import BytesIO
from html.parser import HTMLParser
import hashlib
import json
import zipfile
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "docs" / "research"
OUT.mkdir(parents=True, exist_ok=True)
inventory = []
for directory in ("official", "references"):
    for path in sorted((ROOT / directory).rglob("*")):
        if not path.is_file():
            continue
        entry = {"path": path.relative_to(ROOT).as_posix(),
                 "bytes": path.stat().st_size,
                 "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
        if path.suffix.lower() in (".png", ".jpg", ".jpeg", ".gif", ".webp"):
            with Image.open(path) as source:
                entry["dimensions"] = list(source.size)
        if path.suffix.lower() == ".zip":
            with zipfile.ZipFile(path) as archive:
                entry["members"] = archive.namelist()
        inventory.append(entry)
sources = ROOT / "sources.md"
inventory.append({"path": "sources.md", "bytes": sources.stat().st_size,
                  "sha256": hashlib.sha256(sources.read_bytes()).hexdigest()})
(OUT / "source-inventory.json").write_text(json.dumps({
    "captured_at_utc": datetime.now(timezone.utc).isoformat(),
    "authority": "Evidence fingerprints only; file presence is not approval.",
    "files": inventory}, indent=2), encoding="utf-8")

# Preserve spans rather than expanding merged titles into invented branch records.
class Tables(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tables = []
        self.table = None
        self.row = None
        self.cell = None
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "table":
            self.table = []
        elif tag == "tr" and self.table is not None:
            self.row = []
        elif tag in ("td", "th") and self.row is not None:
            self.cell = {"tag": tag, "text": "", "rowspan": attrs.get("rowspan", "1"),
                         "colspan": attrs.get("colspan", "1"), "class": attrs.get("class", "")}
        elif tag == "br" and self.cell is not None:
            self.cell["text"] += " "
    def handle_data(self, text):
        if self.cell is not None:
            self.cell["text"] += text
    def handle_endtag(self, tag):
        if tag in ("td", "th") and self.cell is not None:
            self.cell["text"] = " ".join(self.cell["text"].split())
            self.row.append(self.cell)
            self.cell = None
        elif tag == "tr" and self.row is not None:
            self.table.append(self.row)
            self.row = None
        elif tag == "table" and self.table is not None:
            self.tables.append(self.table)
            self.table = None

live = OUT / "nexus-live-2026-10-09.html"
if live.exists():
    parsed = Tables()
    parsed.feed(live.read_text(encoding="utf-8"))
    (OUT / "nexus-table-2026-10-09.json").write_text(json.dumps({
        "source_url": "https://nexus.eotir.com/rankchart.html/",
        "source_sha256": hashlib.sha256(live.read_bytes()).hexdigest(),
        "authority": "Published source snapshot, not a newly approved rank dictionary.",
        "tables": parsed.tables}, indent=2), encoding="utf-8")

saved = ROOT / "references" / "combine-galactic-empire-ranks.mhtml"
message = BytesParser(policy=policy.default).parsebytes(saved.read_bytes())
plaques = []
for part in message.walk():
    if part.get_content_type() == "image/gif":
        payload = part.get_payload(decode=True)
        with Image.open(BytesIO(payload)) as source:
            plaques.append((part.get("Content-Location", ""), source.convert("RGBA").copy()))
    elif part.get_content_type() == "text/html":
        parsed = Tables()
        payload = part.get_payload(decode=True)
        parsed.feed(payload.decode(part.get_content_charset() or "utf-8"))
        (OUT / "combine-saved-table.json").write_text(json.dumps({
            "source": saved.relative_to(ROOT).as_posix(),
            "snapshot_url": message.get("Snapshot-Content-Location"),
            "snapshot_date": message.get("Date"),
            "tables": parsed.tables}, indent=2), encoding="utf-8")

# This sheet exposes already supplied images; it is not native-size approval evidence.
tile_width, tile_height, columns = 150, 90, 8
sheet = Image.new("RGB", (columns * tile_width,
                         ((len(plaques) + columns - 1) // columns) * tile_height), "#dddddd")
draw = ImageDraw.Draw(sheet)
links = []
for i, (url, plaque) in enumerate(plaques):
    x, y = (i % columns) * tile_width, (i // columns) * tile_height
    draw.text((x + 5, y + 3), url.rsplit("/", 1)[-1], fill="#000000")
    preview = plaque.copy()
    preview.thumbnail((140, 60))
    sheet.paste(preview, (x + 5, y + 23), preview)
    links.append({"index": i, "url": url, "dimensions": list(plaque.size)})
sheet.save(OUT / "combine-saved-plaques-contact.png")
(OUT / "combine-saved-plaques.json").write_text(json.dumps(links, indent=2), encoding="utf-8")

# Exact pixel crops make portions of the large supplied uniform chart inspectable.
uniform = ROOT / "references" / "imperial-uniform-recognition-chart-2-taivaansusi.png"
with Image.open(uniform) as source:
    source.crop((2500, 1200, 4500, 2600)).save(OUT / "uniform-reference-crop-1.png")
    source.crop((2000, 2600, 4000, 4000)).save(OUT / "uniform-reference-crop-2.png")
print(json.dumps({"files_fingerprinted": len(inventory),
                  "embedded_combine_plaques": len(plaques),
                  "output": str(OUT)}))
