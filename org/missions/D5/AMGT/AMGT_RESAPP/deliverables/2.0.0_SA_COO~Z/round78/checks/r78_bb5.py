"""AMGT_RESAPP round 78 -- AMGT-bb-5: why a driver chart is served for 1 covered name of 95 (CTO round-77 ruling 2).

  --crit AC1 --where deployed [--write <folder>]
  --crit AC2 --where local

A READ. GET-shaped direct invokes of the deployed function's /thesis route for every covered name, and one S3 LIST per
name under filings/v1/<name>/ in opal-data-harvest. Nothing is written to any store.

Each covered name falls in exactly ONE of three classes (the three counts sum to the covered count):
  NO_FILING_ANALYSIS  no object ending .analysis.json is stored under filings/v1/<name>/;
  NO_USABLE_TABLE     a filing analysis is stored, and the served chart is ABSENT and was not refused: the drafted notes
                      carry no driver, or the driver has fewer than 2 points located in the filing text;
  HOLDS_A_TABLE       the drafted notes carry a driver with 2 or more located points. This class is split in two:
                      SERVED (the chart is drawn) and REFUSED (round-76 ruling 7's refusal,
                      lib/research/filings/table_class.py driver_refusal, removed it: the served chart reads refused True).
A name whose served chart and stored analysis disagree (a chart with no stored analysis) is printed as UNCLASSIFIED and
fails the sum.

AC1 (a read that prints its counts; PASSES at the base):
    C1 the covered list holds 95 names and every /thesis answers 200;
    C2 the three counts sum to the covered count and nothing is unclassified;
    C3 the controls: BA_US_Equity is HOLDS_A_TABLE and SERVED; ASML_NA_Equity is HOLDS_A_TABLE and REFUSED;
       AMD_US_Equity is NO_FILING_ANALYSIS and its segment reason opens "No filing analysis is stored for this name yet".
    With --write <folder> the table is also written there as DRIVER_CHART_COVERAGE.json and DRIVER_CHART_COVERAGE.md.
AC2 (the committed table; FAILS at the base, where no worker has written one):
    C1 exactly one DRIVER_CHART_COVERAGE.json sits under a worker's deliverables folder;
    C2 its three counts sum to its covered count, and its name lists hold each covered name once;
    C3 the three controls sit in the classes AC1 names.
Verdict: R78 BB5 <CRIT> READ: YES|NO (exit 0|1).
"""
from __future__ import annotations

import argparse
import collections
import glob
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor

FN = "opal-amgt-scoped-api"
PREFIX = "/api/scoped/amgt"
BUCKET = "opal-data-harvest"
TABLE_GLOB = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~*/DRIVER_CHART_COVERAGE.json"
NO_ANALYSIS_WORDS = "No filing analysis is stored for this name yet"
CLASSES = ("NO_FILING_ANALYSIS", "NO_USABLE_TABLE", "HOLDS_A_TABLE")
CONTROLS = {"BA_US_Equity": ("HOLDS_A_TABLE", "SERVED"), "ASML_NA_Equity": ("HOLDS_A_TABLE", "REFUSED"),
            "AMD_US_Equity": ("NO_FILING_ANALYSIS", None)}


def _event(path):
    return {"rawPath": path, "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"},
            "queryStringParameters": None}


def _why_no_table(body):
    driver = body.get("thesis_driver")
    if body.get("drafting_status") != "SERVED":
        return "no drafted notes are served (%s)" % body.get("drafting_status")
    if not isinstance(driver, dict) or not driver.get("series"):
        return "the drafted notes carry no driver"
    points = driver.get("points") if isinstance(driver.get("points"), list) else []
    located = [p for p in points if isinstance(p, dict) and p.get("span")]
    if driver.get("resolution") in (None, "held", "absent"):
        return "the driver was not matched to the filing text (resolution %s)" % driver.get("resolution")
    return "the driver has %d located point(s); 2 are needed" % len(located)


def read_one(key, lam, s3, slash_safe):
    raw = json.loads(lam.invoke(FunctionName=FN, Payload=json.dumps(
        _event("%s/security/%s/thesis" % (PREFIX, key))).encode())["Payload"].read())
    try:
        body = json.loads(raw.get("body") or "{}")
    except (ValueError, TypeError):
        body = {}
    base = "filings/v1/%s/" % slash_safe(key)
    analyses = 0
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=base):
        for entry in page.get("Contents", []) or []:
            name = entry.get("Key") or ""
            if name.endswith(".analysis.json") and "/" not in name[len(base):]:
                analyses += 1
    chart = body.get("thesis_driver_chart") or {}
    seg_reason = str((body.get("segment_breakdown") or {}).get("reason") or "")
    row = {"name": key, "status_code": raw.get("statusCode"), "analyses_stored": analyses,
           "drafting_status": body.get("drafting_status"), "chart_status": chart.get("status"),
           "chart_refused": chart.get("refused") is True, "chart_source": chart.get("source"),
           "chart_points": len(chart.get("points") or []), "driver_series": chart.get("driver_series"),
           "segment_reason": seg_reason, "split": None, "why": None}
    if chart.get("status") == "SERVED":
        row["class"], row["split"] = "HOLDS_A_TABLE", "SERVED"
    elif chart.get("refused") is True:
        row["class"], row["split"] = "HOLDS_A_TABLE", "REFUSED"
        row["why"] = str(chart.get("plain_reason") or chart.get("reason") or "")
    elif analyses == 0:
        row["class"] = "NO_FILING_ANALYSIS"
        row["why"] = " ".join(str(body.get("drafting_reason") or "no reason served").split())[:110]
        if row["why"].startswith("no drafted document at"):
            row["why"] = "no drafted document is stored for the name (the served text names the store address)"
    else:
        row["class"], row["why"] = "NO_USABLE_TABLE", _why_no_table(body)
    if row["class"] == "HOLDS_A_TABLE" and analyses == 0 and row["chart_source"] == "filing":
        row["class"] = "UNCLASSIFIED"
        row["why"] = "a filing chart is served or refused but no filing analysis is stored"
    return row


def build_table():
    import boto3

    from lib.research.coverage import covered_universe
    from lib.research.identity import crosswalk

    keys = sorted(covered_universe.covered_security_keys())
    lam = boto3.client("lambda", region_name="us-east-1")
    s3 = boto3.client("s3", region_name="us-east-1")
    with ThreadPoolExecutor(max_workers=8) as pool:
        rows = list(pool.map(lambda k: read_one(k, lam, s3, crosswalk.slash_safe_key), keys))
    names = {c: sorted(r["name"] for r in rows if r["class"] == c) for c in CLASSES}
    table = {
        "covered": len(keys),
        "counts": {c: len(names[c]) for c in CLASSES},
        "holds_a_table_split": {s: sorted(r["name"] for r in rows if r["split"] == s) for s in ("SERVED", "REFUSED")},
        "names": names,
        "unclassified": sorted(r["name"] for r in rows if r["class"] == "UNCLASSIFIED"),
        "no_filing_analysis_why": dict(collections.Counter(r["why"] for r in rows if r["class"] == "NO_FILING_ANALYSIS")),
        "no_usable_table_why": dict(collections.Counter(r["why"] for r in rows if r["class"] == "NO_USABLE_TABLE")),
        "not_200": sorted(r["name"] for r in rows if r["status_code"] != 200),
        "rows": rows,
    }
    return table


def print_table(table):
    counts = table["counts"]
    print("   covered names %d; /thesis not 200: %d" % (table["covered"], len(table["not_200"])))
    for c in CLASSES:
        print("   %-19s %3d" % (c, counts[c]))
    split = table["holds_a_table_split"]
    print("      of HOLDS_A_TABLE: SERVED %d %s; REFUSED %d %s" % (len(split["SERVED"]), split["SERVED"],
                                                                 len(split["REFUSED"]), split["REFUSED"]))
    print("   sum %d of %d; unclassified %d %s" % (sum(counts.values()), table["covered"], len(table["unclassified"]),
                                                  table["unclassified"]))
    for why, n in sorted(table["no_usable_table_why"].items(), key=lambda kv: -kv[1]):
        print("      NO_USABLE_TABLE because %s: %d" % (why, n))
    for why, n in sorted((table.get("no_filing_analysis_why") or {}).items(), key=lambda kv: -kv[1]):
        print("      NO_FILING_ANALYSIS, the page's stated reason %r: %d" % (why, n))
    for c in CLASSES:
        print("   %s: %s" % (c, ", ".join(table["names"][c])))


def controls_ok(table):
    rows = {r["name"]: r for r in table["rows"]}
    good = []
    for key, (cls, split) in CONTROLS.items():
        row = rows.get(key) or {}
        ok = row.get("class") == cls and row.get("split") == split
        if key == "AMD_US_Equity":
            ok = ok and str(row.get("segment_reason") or "").startswith(NO_ANALYSIS_WORDS)
        print("   control %s: class %s split %s" % (key, row.get("class"), row.get("split")))
        good.append(ok)
    return all(good)


def write_table(table, folder):
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, "DRIVER_CHART_COVERAGE.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(table, fh, indent=1, sort_keys=True)
        fh.write("\n")
    lines = ["# Driver chart coverage over the covered names", "",
             "| class | names |", "|---|---|"]
    for c in CLASSES:
        lines.append("| %s | %d |" % (c, table["counts"][c]))
    lines.append("| sum | %d of %d |" % (sum(table["counts"].values()), table["covered"]))
    lines.append("")
    for s in ("SERVED", "REFUSED"):
        lines.append("HOLDS_A_TABLE, %s: %s" % (s, ", ".join(table["holds_a_table_split"][s]) or "none"))
    lines.append("")
    for why, n in sorted(table["no_usable_table_why"].items(), key=lambda kv: -kv[1]):
        lines.append("- NO_USABLE_TABLE because %s: %d" % (why, n))
    lines.append("")
    lines += ["| name | class | split | analyses stored | drafted notes | why |", "|---|---|---|---|---|---|"]
    for r in table["rows"]:
        lines.append("| %s | %s | %s | %d | %s | %s |" % (r["name"], r["class"], r["split"] or "", r["analyses_stored"],
                                                        r["drafting_status"], r["why"] or ""))
    with open(os.path.join(folder, "DRIVER_CHART_COVERAGE.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    print("   wrote DRIVER_CHART_COVERAGE.json and .md to %s" % folder)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", choices=("AC1", "AC2"), required=True)
    ap.add_argument("--where", choices=("local", "deployed"), required=True)
    ap.add_argument("--write", default=None, help="folder to write the table to (AC1 only)")
    a = ap.parse_args()
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print("%s %s %s" % ("PASS" if cond else "FAIL", name, detail))

    if a.crit == "AC2":
        found = sorted(glob.glob(TABLE_GLOB))
        clause("C1 exactly one committed table", len(found) == 1, "%d found %s" % (len(found), found))
        if len(found) != 1:
            return verdict(a, ok)
        with open(found[0], encoding="utf-8") as fh:
            table = json.load(fh)
    else:
        if a.where != "deployed":
            clause("C0 AC1 reads the deployed function", False, "run with --where deployed")
            return verdict(a, ok)
        table = build_table()
        clause("C1 the covered names are read and every /thesis answers 200",
               table["covered"] == 95 and not table["not_200"], "%d covered" % table["covered"])
    print_table(table)
    listed = [n for c in CLASSES for n in table["names"][c]]
    clause("C2 the three counts sum to the covered count",
           sum(table["counts"].values()) == table["covered"] and not table["unclassified"]
           and len(listed) == len(set(listed)) == table["covered"],
           "%d + %d + %d = %d of %d" % (table["counts"][CLASSES[0]], table["counts"][CLASSES[1]],
                                        table["counts"][CLASSES[2]], sum(table["counts"].values()), table["covered"]))
    clause("C3 the three controls sit in their classes", controls_ok(table))
    if a.crit == "AC1" and a.write:
        write_table(table, a.write)
    return verdict(a, ok)


def verdict(a, ok):
    yes = bool(ok) and all(ok)
    print("R78 BB5 %s READ: %s" % (a.crit, "YES" if yes else "NO"))
    return 0 if yes else 1


if __name__ == "__main__":
    sys.exit(main())
