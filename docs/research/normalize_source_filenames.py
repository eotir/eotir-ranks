"""Purpose: safely normalize supplied source filenames and record byte preservation.
Usage: python docs/research/normalize_source_filenames.py
Prerequisites: Python 3; run only in this ranks workspace.
Refuses destination collisions; does not overwrite files or rewrite ZIP members.
"""
from pathlib import Path
import hashlib
import json
ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "docs/research/file-renames-2026-10-09.json"
MAPPING = {
  "official/Additions.html": "official/additions.html",
  "official/CIRAF Pay Scale.html": "official/ciraf-pay-scale.html",
  "official/Full Pay Scale WIP.html": "official/full-pay-scale-wip.html",
  "official/Full Pay Scale.html": "official/full-pay-scale.html",
  "official/General Pay Scale.html": "official/general-pay-scale.html",
  "official/Ground Elements.html": "official/ground-elements.html",
  "official/High Council Adjs.html": "official/high-council-adjs.html",
  "official/IRAF Pay Scale.html": "official/iraf-pay-scale.html",
  "official/Personnel.html": "official/personnel.html",
  "official/Ranks & Salaries (WIP).zip": "official/ranks-and-salaries-wip.zip",
  "official/Salaries per level.html": "official/salaries-per-level.html",
  "official/Sign-Off.html": "official/sign-off.html",
  "official/Special Pay Scale (Revamping).html": "official/special-pay-scale-revamping.html",
  "references/army_company_toe_by_taivaansusi_dfqpbts.png": "references/army-company-toe-taivaansusi.png",
  "references/defense_industries_and_shipyards.jpg": "references/defense-industries-and-shipyards.jpg",
  "references/galaxy-map-by-taivaansusi.jpg": "references/galaxy-map-taivaansusi.jpg",
  "references/imperial_rank_table-by-whatsahonda.png": "references/imperial-rank-table-whatsahonda.png",
  "references/imperial_rank_table_by_whatsahonda_dge4tzj-pre.jpg": "references/imperial-rank-table-whatsahonda-preview.jpg",
  "references/imperial_rules_of_escalation_by_taivaansusi_dfqpc6i-fullview.jpg": "references/imperial-rules-of-escalation-taivaansusi.jpg",
  "references/imperial_uniform_recognition_chart_2_by_taivaansusi_dfzysvt.png": "references/imperial-uniform-recognition-chart-2-taivaansusi.png",
  "references/Ranks of the Galactic Empire - Holocron - Star Wars Combine.mhtml": "references/combine-galactic-empire-ranks.mhtml",
  "references/table_of_ranks_in_imperial_service_by_taivaansusi_dghzkn3.png": "references/table-of-ranks-in-imperial-service-taivaansusi.png"
}
rows = []
for old, new in MAPPING.items():
    source = ROOT / old
    target = ROOT / new
    if not source.resolve().is_relative_to(ROOT.resolve()) or not target.resolve().is_relative_to(ROOT.resolve()):
        raise RuntimeError("Rename leaves the authorized workspace")
    if not source.is_file():
        raise FileNotFoundError(source)
    # Windows sees a case-only destination as the same file; allow that exact case.
    if target.exists() and source.resolve() != target.resolve():
        raise FileExistsError(target)
    rows.append({"old_path": old, "new_path": new,
                 "sha256_before": hashlib.sha256(source.read_bytes()).hexdigest(),
                 "status": "planned"})
REPORT.write_text(json.dumps(rows, indent=2), encoding="utf-8")
for row in rows:
    source, target = ROOT / row["old_path"], ROOT / row["new_path"]
    source.rename(target)
    row["sha256_after"] = hashlib.sha256(target.read_bytes()).hexdigest()
    if row["sha256_after"] != row["sha256_before"]:
        raise RuntimeError("Content changed during rename")
    row["status"] = "renamed-and-byte-verified"
    REPORT.write_text(json.dumps(rows, indent=2), encoding="utf-8")
print(f"Renamed and hash-verified {len(rows)} source files")

