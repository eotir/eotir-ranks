"""Build the complete source-backed Imperial Republic candidate catalog.

Usage: python tools/build_catalog.py
Prerequisites: Python 3, Pillow, included Nexus/rank-only Google JSON and Combine MHTML.
Writes only local draft data and derived reference evidence. Never imports canon,
publishes assets, edits official sources, or treats an external grade as ours.
Context: bounded saved source captures; no AI API call or token usage occurs.
"""
from collections import Counter
from email import policy
from email.parser import BytesParser
from io import BytesIO
from pathlib import Path
import hashlib
import json
import re

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-10-09"
NEXUS_CAPTURE = "docs/research/nexus-table-2026-10-09.json"
# The live workbook capture includes unrelated private historical data. Keep
# this build reproducible from the included minimal rank-only projection; never
# require a clone to recover payroll/personnel exports to generate candidates.
SHEET_CAPTURE = "docs/research/full-chart-reference-google-ranks.json"
SAVED_COMBINE = "references/combine-galactic-empire-ranks.mhtml"
HOL = "https://holocron.swcombine.com/wiki/Ranks_of_the_Galactic_Empire"
CURRENT = "https://www.swc-empire.com/ing/general/ranks"
WHATS = "https://www.deviantart.com/whatsahonda/art/Imperial-Rank-Table-991198927"
BRANCH_IDS = ["navy", "marine", "army", "inquisition", "judiciary", "ministries",
              "security-bureau", "personal-staff", "royal-guard", "state",
              "regional-governance", "intelligence-service"]
GRADE_IDS = ([f"E-{n}" for n in range(1, 8)] + [f"O-{n}" for n in range(1, 7)]
             + [f"C-{n}" for n in range(1, 7)] + [f"HC-{n}" for n in range(1, 8)]
             + [f"RT-{n}" for n in range(1, 5)])
TOKENS = {"red", "blue", "gold", "green", "orange", "white", "charcoal", "black",
          "bright-white", "grey", "purple", "silver", "metallic-gold", "cyan", "teal", "amber"}


def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def write(path, data):
    dest = ROOT / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def classify(rgb):
    """Classify tiny source face samples; this recovers colors, not materials."""
    r, g, b = rgb
    if max(rgb) - min(rgb) < 20:
        return "grey" if sum(rgb) / 3 < 145 else "white"
    if r > 150 and g > 150 and b < 60:
        return "gold"
    if r > 150 and 45 < g < 150 and b < 60:
        return "orange"
    if r > g + 50 and r > b + 50:
        return "red"
    if b > r + 50 and b > g + 50:
        return "blue"
    if g > r + 50 and g > b + 50:
        return "green"
    raise ValueError(f"Unclassified source face pixel: {rgb}")


def decode_combine():
    message = BytesParser(policy=policy.default).parsebytes((ROOT / SAVED_COMBINE).read_bytes())
    refs = {}
    for part in message.walk():
        if part.get_content_type() != "image/gif":
            continue
        url, payload = part.get("Content-Location", ""), part.get_payload(decode=True)
        name = url.rsplit("/", 1)[-1]
        with Image.open(BytesIO(payload)) as im:
            im = im.convert("RGBA")
            samples, rows = [], []
            for y in range(7, im.height, 11):
                row, sampled = [], []
                for x in range(7, im.width, 11):
                    p = im.getpixel((x, y))
                    sampled.append({"x": x, "y": y, "rgba": list(p)})
                    # Some ISB GIFs have a transparent second row of white RGB.
                    # Looking only at RGB would invent a white tile row.
                    if p[3]:
                        row.append(classify(p[:3]))
                samples.append(sampled)
                if row:
                    rows.append(row)
            refs[name] = {"id": name.removesuffix(".gif"), "url": url,
                          "capture": SAVED_COMBINE, "sha256_gif": hashlib.sha256(payload).hexdigest(),
                          "dimensions": list(im.size), "rows": rows, "samples": samples,
                          "method": "Face centers x=7+11n,y=7+11n; transparent padding excluded; colors visually cross-checked against saved contact sheet."}
    assert len(refs) == 88, f"Expected 88 embedded references, observed {len(refs)}"
    # Anchor representative exceptions so any source geometry drift fails loudly.
    assert refs["ME-1.gif"]["rows"] == [["grey", "grey"]]
    assert refs["ME-6.gif"]["rows"] == [["grey"] * 5, ["blue"] * 5]
    assert len(refs["ISBO-4.gif"]["rows"]) == 1
    write("docs/research/full-chart-reference-patterns.json", {
        "date": DATE, "status": "REFERENCE_EVIDENCE", "source_url": HOL,
        "source_capture": SAVED_COMBINE,
        "source_sha256": hashlib.sha256((ROOT / SAVED_COMBINE).read_bytes()).hexdigest(),
        "note": "88 source graphics decoded; color tokens adapt appearance to local candidate tiles, not source entitlement or adopted Imperial Republic patterns.",
        "references": list(refs.values())})
    return refs


def main():
    nexus, workbook, refs = read(NEXUS_CAPTURE), read(SHEET_CAPTURE), decode_combine()
    table = nexus["tables"][0]
    header = next(row for row in table if len(row) == 13 and row[1]["text"] == "Navy")
    branches = [{"id": bid, "label": header[i]["text"], "source_column": i,
                 "military": i <= 3} for i, bid in enumerate(BRANCH_IDS, 1)]
    grades = [{"id": g, "order_bottom_up": i, "family": g.split("-")[0]}
              for i, g in enumerate(GRADE_IDS, 1)]
    orders = {g["id"]: g["order_bottom_up"] for g in grades}
    sheets = {s["id"]: s for s in workbook["sheets"]}
    patterns = {}

    def pattern(pid, rows, names, notes, basis="Combine-inspired candidate adaptation"):
        assert rows and all(rows), pid
        assert all(t in TOKENS for row in rows for t in row), pid
        result = {"id": pid, "rows": rows, "status": "CANDIDATE", "approval": None,
                  "design_basis": basis, "reference_urls": [refs[n]["url"] for n in names] + [HOL, WHATS],
                  "reference_ids": [refs[n]["id"] for n in names],
                  "reference_files": [SAVED_COMBINE, "references/imperial-rank-table-whatsahonda.png"],
                  "adaptation_notes": notes}
        if pid in patterns:
            assert patterns[pid] == result, f"Conflicting pattern identity: {pid}"
        patterns[pid] = result
        return pid

    def source_pattern(pid, name, notes, recolor=None):
        rows = [[(recolor or {}).get(t, t) for t in row] for row in refs[name]["rows"]]
        return pattern(pid, rows, [name], notes)

    military = {}
    for n in range(1, 8):
        grade = f"E-{n}"
        names = [f"ME-{min(n, 6)}.gif"]
        rows = [["grey", "grey"]] if n == 1 else [["grey"] * (n - 1), ["blue"] * (n - 1)]
        military[grade] = pattern(f"military-enlisted-e{n}-grey-blue-v1", rows, names,
                                 ["Ryan selected this shared draft direction for Navy, Marine and Army; exact bytes/assignments remain unapproved.",
                                  "External titles differ; Imperial Republic titles and grade positions retained."]
                                 + (["PROPOSED EXTENSION: E-7 adds a sixth column beyond saved ME-6; no ME-7 source exists."] if n == 7 else []))
    for n in range(1, 7):
        military[f"O-{n}"] = source_pattern(f"military-officer-o{n}-v1", f"MO-{n}.gif",
            ["Shared Navy/Marine/Army design proposal; only the enlisted sharing was explicitly selected by Ryan.",
             "Saved MO grade label used as visual index; external Army/Navy titles differ from Imperial Republic titles."])
    military["C-1"] = pattern("military-command-c1-v1", [["red"] * 4, ["blue"] * 4],
        ["MO-6.gif", "MC-1.gif"], ["PROPOSED BRIDGE: expand the full red-over-blue O-6 pattern from three to four columns for Imperial Republic Line Captain/Colonel.",
                                  "Imperial Republic has six command steps; saved Combine has five. No rank is shifted to fit the external ladder."])
    # C-1's bridge and the alternating mixed/full rows preserve all six local
    # positions while consuming the five saved command designs exactly once.
    for n in range(2, 7):
        military[f"C-{n}"] = source_pattern(f"military-command-c{n}-v1", f"MC-{n-1}.gif",
            [f"PROPOSED MAPPING: Imperial Republic C-{n} uses saved external C-{n-1} graphics, not its title or organizational authority.",
             "C-6 is the extra local command grade; MC-5 remains comparison evidence only."])
    military["HC-1"] = source_pattern("military-high-command-hc1-v1", "MHC-3.gif",
        ["PROPOSED REASSIGNMENT: blue/gold upper row over red is a fleet/surface command comparison; saved MHC-3 titles are Lord Admiral/Lord General, not our HC-1 titles.",
         "The comprehensive Whatsahonda chart's fleet/grand rows support a six-column mixed-color comparison, without importing its rank ladder."])
    military["HC-2"] = pattern("military-high-command-hc2-v1", [["blue"] * 2 + ["gold"] * 4, ["red"] * 6],
        ["MHC-3.gif", "MHC-2.gif"], ["PROPOSED INTERMEDIATE: replace one blue upper tile with gold relative to HC-1; count remains 12. This has no exact external grade image.",
                                       "HC labels do not grant High Command membership, phoenix marks, precious-metal entitlement or uniform rights."])
    military["HC-3"] = source_pattern("military-high-command-hc3-v1", "MHC-2.gif",
        ["PROPOSED TITLE MATCH: saved Grand Admiral/Grand General comparison is HC-2 there, HC-3 here. Grand Marshall remains the local title."])
    military["HC-4"] = pattern("military-high-command-hc4-v1", [["blue"] * 3 + ["gold"] * 4, ["blue"] * 3 + ["red"] * 4],
        ["MHC-2.gif", "MHC-3.gif"], ["PROPOSED EXTENSION: seventh column distinguishes the Lord tier while preserving the grand mixed-row motif. No external HC-4 military design is claimed.",
                                   "An alternative is a fixed six-column pattern with one accent substitution; reviewer may prefer its smaller physical envelope."])

    def extend(rows, n, family, grade):
        """Fill external design gaps without filling blank official rank cells."""
        if family == "E":
            return [["grey"] * max(1, n - 1), [rows[-1][0]] * max(1, n - 1)]
        if family == "C":
            return [row[:-1] + [row[-1], row[-1]] for row in rows]
        return [row + [row[-1]] for row in rows]

    def choose_family(prefix, grade):
        fam, n = grade.split("-")
        n = int(n)
        exact = f"{prefix}{fam}-{n}.gif"
        if exact in refs:
            return exact, refs[exact]["rows"], []
        available = [(int(re.search(r"-(\d+)\.gif$", name).group(1)), name)
                     for name in refs if re.fullmatch(rf"{prefix}{fam}-\d+\.gif", name)]
        if available:
            number, name = min(available, key=lambda item: (abs(item[0] - n), item[0]))
            rows = refs[name]["rows"]
            if n > number:
                rows = extend(rows, n, fam, grade)
            return name, rows, [f"PROPOSED ADAPTATION: no exact {prefix}{grade}.gif; nearest saved {name} supplies the motif, extended/reassigned to the unchanged local grade."]
        name = "ME-1.gif" if fam == "E" else "MHC-3.gif"
        rows = refs[name]["rows"] if fam != "E" else ([["grey", "grey"]] if n == 1 else [["grey"] * (n-1), ["blue"] * (n-1)])
        return name, rows, [f"PROPOSED NEW FAMILY: saved {prefix} has no {fam} pattern here; military tile syntax supplies a comparison without adopting its rank meanings."]

    # These palettes are visual proposals, deliberately independent of source
    # column colors. Several institutions have no external direct counterpart.
    specialty = {
        "inquisition": ("II", {"red": "purple"}, "Purple/gold proposal; no external Inquisition entitlement inferred."),
        "judiciary": ("II", {"red": "white", "gold": "purple"}, "Pearl/purple proposal; judicial office and rank remain distinct."),
        "ministries": ("MI", {}, "Saved Ministry of Industry green/gold motif adapted across local ministry positions."),
        "security-bureau": ("ISB", {}, "Saved ISB red/blue bar family; transparent image padding is not a white tile row."),
        "personal-staff": ("PG", {"blue": "cyan", "orange": "white", "gold": "teal"}, "Cyan/pearl/teal proposal; personal appointments do not become a universal military ladder."),
        "royal-guard": ("M", {"red": "purple", "blue": "white", "gold": "gold"}, "Purple/pearl proposal on military geometry; Royal Guard titles stay at their source grades, including Master Sergeant O-1."),
        "state": ("PG", {}, "Saved central-government blue/orange/gold motif proposed for diplomatic positions; source institutions differ."),
        "regional-governance": ("RG", {}, "Saved regional-government blue/red/gold motif, with explicit gap adaptations."),
        "intelligence-service": ("II", {}, "Saved Intelligence red/gold bars; lower analysts/collaborators use proposed neutral/red enlisted family.")}

    def branch_pattern(branch, grade):
        if branch in BRANCH_IDS[:3]:
            return military[grade]
        prefix, recolor, explanation = specialty[branch]
        name, rows, notes = choose_family(prefix, grade)
        rows = [[recolor.get(t, t) for t in row] for row in rows]
        return pattern(f"{branch}-{grade.lower().replace('-', '')}-v1", rows, [name],
                       [explanation, "All specialty colors, geometry assignments and grade mappings are CANDIDATE proposals. External titles and source chart backgrounds are not color rules."] + notes)

    mapping = {"navy": (11, 2), "marine": (11, 4), "army": (11, 6),
               "inquisition": (0, 3), "judiciary": (0, 4), "ministries": (0, 9),
               "security-bureau": (0, 10), "personal-staff": (9, 3), "royal-guard": (9, 5),
               "state": (0, 7), "regional-governance": (0, 8), "intelligence-service": (0, 2)}

    def sheet_assertion(sheet, row, col):
        title = row["values"][col] if col < len(row["values"]) else ""
        return {"source": sheet["title"], "url": workbook["url"] + f"?gid={sheet['id']}",
                "capture": SHEET_CAPTURE, "gid": sheet["id"],
                "row_index_zero_based": row["row"] - 1, "cell_index_zero_based": col,
                "cell": f"{chr(65+col)}{row['row']}", "grade_cell": f"B{row['row']}",
                "title": title, "grade": row["values"][1], "struck": col+1 in row["struck_columns"]}

    def nexus_assertion(ri, ci):
        return {"source": "Nexus", "url": nexus["source_url"], "capture": NEXUS_CAPTURE,
                "table_index": 0, "row_index_zero_based": ri, "cell_index_zero_based": ci,
                "title": table[ri][ci]["text"], "grade": table[ri][0]["text"],
                "colspan": int(table[ri][ci]["colspan"]), "rowspan": int(table[ri][ci]["rowspan"])}

    repairs = {"Charg\ufffd d'affaires": "Chargé d'affaires", "Senior Attach\ufffd": "Senior Attaché",
               "Attach\ufffd": "Attaché", "Assistant Attach\ufffd": "Assistant Attaché"}
    records, blanks, shared = [], [], []
    for ri, row in enumerate(table):
        grade = row[0]["text"] if row else ""
        if grade not in orders:
            continue
        if len(row) == 13:
            for ci, branch in enumerate(BRANCH_IDS, 1):
                title = row[ci]["text"]
                if not title:
                    blanks.append({"branch_id": branch, "grade": grade,
                                   "source": "Nexus", "capture": NEXUS_CAPTURE, "url": nexus["source_url"],
                                   "table_index": 0, "row_index_zero_based": ri, "cell_index_zero_based": ci,
                                   "reason": "Source blank; no rank invented."})
                    continue
                notes, assertions = [], [nexus_assertion(ri, ci)]
                sid, scol = mapping[branch]
                sheet = sheets[sid]
                sr = next((r for r in sheet["rows"] if len(r["values"]) > 1 and r["values"][1] == grade), None)
                if sr:
                    assertion = sheet_assertion(sheet, sr, scol)
                    assertions.append(assertion)
                    if assertion["title"] != title:
                        notes.append("SOURCE VARIANT/CONFLICT: mapped detailed sheet title differs or is blank; both raw assertions retained without choosing precedence.")
                if title in repairs:
                    notes.append("READABLE ENCODING REPAIR ONLY: Nexus U+FFFD replacement character displayed as é, supported by the mapped General sheet. Raw title remains byte-for-byte in title_raw/source assertions.")
                    assert assertions[-1]["title"].replace(" ", "") == repairs[title].replace(" ", ""), assertions[-1]
                if "(?)" in title:
                    notes.append("Source question mark retained: this position is explicitly uncertain.")
                if "/" in title:
                    notes.append("Slash title is one source cell; not split into independent ranks or appointment records.")
                if title == "Flight Sergeant Major":
                    notes.append("Nexus Flight / IRAF Fight discrepancy preserved. Missing l is a proposed source typo correction only.")
                if any(word in title for word in ["Planatary", "Provincinal", "Lieutentant"]):
                    notes.append("Source spelling retained without correcting it; proposed editorial correction requires a later ruling.")
                records.append({"id": f"imperial-republic-{branch}-{grade.lower().replace('-', '')}",
                                "branch_id": branch, "grade": grade, "grade_order": orders[grade],
                                "title_raw": title, "title_display": repairs.get(title, title),
                                "pattern_id": branch_pattern(branch, grade), "status": "CANDIDATE", "approval": None,
                                "source_assertions": assertions, "candidate_notes": notes})
        else:
            assert len(row) == 2 and int(row[1]["colspan"]) == 12
            title, notes, assertions = row[1]["text"], [], [nexus_assertion(ri, 1)]
            # Shared titles are retained as one spanning assertion. A title word
            # search supplies disputed alternatives without expanding a merged
            # title into twelve invented branch records or equating slash parts.
            keywords = {"RT-4": ["Supreme Ruler", "Supremer Ruler"], "RT-3": ["Executor"],
                        "RT-2": ["Empress"], "RT-1": ["Supreme Chancellor", "Supremer Chancellor"],
                        "HC-7": ["Praetor", "Royal 1st Family"],
                        "HC-6": ["High Councilor", "Chief of Staff", "Grand Minister"],
                        "HC-5": ["Vice Chancellor", "Royal Family"]}[grade]
            for sheet in sheets.values():
                for sr in sheet["rows"]:
                    if sr["row"] <= 2:
                        continue
                    for sc, value in enumerate(sr["values"]):
                        if sc < 2 or not value:
                            continue
                        if any(k.lower() in value.lower() for k in keywords):
                            assertions.append(sheet_assertion(sheet, sr, sc))
            # Grand Vizier is additional struck-out workbook evidence, never a
            # new Nexus row. Include it in the Executor comparison explicitly.
            if grade == "RT-3":
                for sheet in sheets.values():
                    for sr in sheet["rows"]:
                        for sc, value in enumerate(sr["values"]):
                            if value == "Grand Vizier":
                                assertions.append(sheet_assertion(sheet, sr, sc))
                notes.append("Grand Vizier remains struck-out comparison evidence in all three detailed tabs; no new Grand Vizier rank record is created.")
            notes += ["MERGED/SHARED SOURCE ROW: source spans all 12 branches; no branch-specific duplication.",
                      "UNRESOLVED UPPER/THRONE: grades, family titles and special appointments disagree between official sources. Nexus position is retained for chart display, not adopted precedence.",
                      "Plaque is an unapproved visual proposal; wearing a rank plaque, palette entitlement and settled hierarchy are not established for these titles."]
            if grade == "RT-4":
                name = "GEHC-6.gif"
            elif grade == "RT-3":
                name = "GEHC-5.gif"
            else:
                name = "CHC-4.gif"
            rows = refs[name]["rows"]
            recolor = {"RT-2": {"blue": "purple", "gold": "white"},
                       "RT-1": {"blue": "teal", "gold": "white"},
                       "HC-7": {"blue": "purple"}, "HC-6": {"blue": "green"},
                       "HC-5": {"blue": "cyan"}}.get(grade, {})
            rows = [[recolor.get(t, t) for t in r] for r in rows]
            pid = pattern(f"shared-{grade.lower().replace('-', '')}-v1", rows, [name],
                ["PROPOSED SHARED-TITLE STUDY: external executive/Throne motif adapted only for comparison; grade labels and titles have different meanings.",
                 "Color substitutions distinguish review studies and do not imply royal, ministerial or heraldic entitlement."])
            alternate = pattern(f"shared-{grade.lower().replace('-', '')}-alternative-v1",
                [["charcoal"] * len(rows[0]), ["silver"] * len(rows[-1])], [name],
                ["ALTERNATIVE: neutral ceremonial comparison, keeping institutional color meaning undecided; silver is a candidate material, not an entitlement."])
            shared.append({"id": f"imperial-republic-shared-{grade.lower().replace('-', '')}",
                           "branch_id": None, "grade": grade, "grade_order": orders[grade],
                           "title_raw": title, "title_display": title, "pattern_id": pid,
                           "alternative_pattern_ids": [alternate], "status": "CANDIDATE", "approval": None,
                           "source_assertions": assertions, "candidate_notes": notes})

    counts = Counter(r["branch_id"] for r in records)
    blank_counts = Counter(r["branch_id"] for r in blanks)
    records.sort(key=lambda r: (orders[r["grade"]], BRANCH_IDS.index(r["branch_id"])))
    blanks.sort(key=lambda r: (orders[r["grade"]], BRANCH_IDS.index(r["branch_id"])))
    shared.sort(key=lambda r: orders[r["grade"]])
    coverage = {"branch_records": len(records), "military_records": sum(r["branch_id"] in BRANCH_IDS[:3] for r in records),
                "blank_cells": len(blanks), "shared_records": len(shared), "patterns": len(patterns),
                "branch_grid_cells": len(records) + len(blanks),
                "per_branch": [{"branch_id": b, "populated": counts[b], "blank": blank_counts[b], "total": counts[b]+blank_counts[b]} for b in BRANCH_IDS]}
    assert (coverage["branch_records"], coverage["military_records"], len(blanks), len(shared)) == (210, 69, 66, 7), coverage
    assert all(c["total"] == 23 for c in coverage["per_branch"]), coverage
    assert len({r["id"] for r in records+shared}) == len(records+shared)
    assert all(r["approval"] is None and r["status"] == "CANDIDATE" for r in records+shared+list(patterns.values()))
    assert all(r["title_raw"] == table[r["source_assertions"][0]["row_index_zero_based"]][r["source_assertions"][0]["cell_index_zero_based"]]["text"] for r in records+shared)
    write("data/rank-catalog.json", {"schema_version": 1, "date": DATE, "status": "CANDIDATE", "approval": None,
        "canonical": False, "published": False, "scope": "Complete Nexus branch-grid candidate coverage; disputed shared upper/Throne rows shown separately.",
        "source_precedence": "MOSTLY UNDECIDED: Nexus supplies the captured chart grid; official alternatives remain assertions, not overrides.",
        "source_captures": [{"path": p, "sha256": hashlib.sha256((ROOT/p).read_bytes()).hexdigest()} for p in [NEXUS_CAPTURE, SHEET_CAPTURE, SAVED_COMBINE]],
        "branches": branches, "grades": grades, "patterns": list(patterns.values()), "rank_records": records,
        "blank_cells": blanks, "shared_records": shared, "coverage": coverage})
    print(json.dumps(coverage))


if __name__ == "__main__":
    main()
