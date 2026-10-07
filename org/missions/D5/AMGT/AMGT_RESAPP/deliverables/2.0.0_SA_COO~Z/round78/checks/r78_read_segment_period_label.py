"""AMGT_RESAPP round 78 -- READ: which fiscal year is "Period 1" of the stored segment table (CTO msg 31077).

  python r78_read_segment_period_label.py [--write <folder>]

A READ. No build, no store write, no Bloomberg, vendor, SEC, model or web call. It makes S3 reads of
opal-data-harvest only:
  - the segment bronze, bloomberg/harvest/bronze/segments/security_key=<partition>/<stamp>.json: per name the
    NEWEST object whose response carries a non-empty PG_REVENUE list;
  - the stored model block, through the page's own reader lib.research.api.scoped_amgt._read_model_block_pool
    (the newest derived/model_block/<key>/<stamp>/model_block.json), rows selected with the page's own
    scoped_amgt._figures(block, "fiscal_year_line_item"), mnemonic SALES_REV_TURN.

Per name with revenue rows: the sum of Period 1 over hierarchy-level-1 rows (a cell with |value| < 1e-6 is
absent) is compared to every stored fiscal year's SALES_REV_TURN. Classes, exactly one per name:
  matched    the Period 1 level-1 sum is within 0.5 percent of one stored fiscal year's revenue;
  unmatched  a block is stored with revenue years and none is within 0.5 percent;
  no-block   no stored model block, or a block with no revenue series.
A second pass, never changing a class: for a matched name, whether the Period 2 level-1 sum is within 0.5 percent
of the stored fiscal year one before the matched one (HOLDS / DOES_NOT_HOLD / CANNOT_TELL).
Control: AMD_US_Equity must read matched on fiscal year 2025. Verdict line:
R78 READ SEGMENT PERIOD LABEL: DONE (exit 0) when the control holds and the classes sum to the names read.
"""
from __future__ import annotations

import argparse
import collections
import io
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

BUCKET = "opal-data-harvest"
SEGMENT_PREFIX = "bloomberg/harvest/bronze/segments/"
REVENUE_MNEMONIC = "SALES_REV_TURN"
LEVEL_FIELD = "Product Geographic Hierarchy Level"
PERIODS = (1, 2, 3, 4, 5)
TOLERANCE = 0.005
ABSENT_BELOW = 1e-6
CONTROL_KEY = "AMD_US_Equity"
CONTROL_YEAR = "2025"
CLASSES = ("matched", "unmatched", "no-block")
P2_CLASSES = ("HOLDS", "DOES_NOT_HOLD", "CANNOT_TELL")


def _repo_root():
    here = os.path.dirname(os.path.abspath(__file__))
    out = subprocess.run(["git", "-C", here, "rev-parse", "--show-toplevel"], capture_output=True)
    return out.stdout.decode("utf-8").strip()


def _present(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and abs(value) >= ABSENT_BELOW


def _level(row):
    try:
        return int(float(row.get(LEVEL_FIELD)))
    except (TypeError, ValueError):
        return None


def _within(a, b):
    return bool(b) and abs(a / b - 1.0) <= TOLERANCE


def newest_revenue_object(s3, keys):
    """(key, body, objects_tried) for the newest object with a non-empty PG_REVENUE list, else (None, None, n)."""
    tried = 0
    for key in sorted(keys, reverse=True):
        tried += 1
        body = json.loads(s3.get_object(Bucket=BUCKET, Key=key)["Body"].read().decode("utf-8"))
        rows = (body.get("response") or {}).get("PG_REVENUE")
        if isinstance(rows, list) and rows:
            return key, body, tried
    return None, None, tried


def level1_sums(rows):
    """Per period: the level-1 sum, how many level-1 rows carry a value, and how many are absent."""
    level1 = [r for r in rows if _level(r) == 1]
    out = {}
    for p in PERIODS:
        vals = [r.get("Period %d Value" % p) for r in level1]
        have = [v for v in vals if _present(v)]
        out[p] = {"sum": round(sum(have), 6) if have else None, "present": len(have), "absent": len(vals) - len(have)}
    levels = collections.Counter(str(_level(r)) for r in rows)
    names = [str(r.get("Metric Name") or "").replace("\xa0", " ").strip() for r in level1]
    return out, len(level1), dict(sorted(levels.items())), names


def model_revenue(scoped, key):
    """The stored revenue series, read with the page's reader. Returns a dict; status is the reader's own."""
    block, record = scoped._read_model_block_pool(key)
    out = {"status": record.get("status"), "object_key": record.get("object_key"), "reason": record.get("reason"),
           "series": [], "header_currency": {}, "units": [], "currency_caveats": [], "raw_stamp_used": None}
    if not block:
        return out
    out["raw_stamp_used"] = block.get("raw_stamp_used")
    for fig in block.get("figures") or []:
        mnem = str(fig.get("mnemonic") or "")
        if fig.get("scope") == "header" and "CRNCY" in mnem and isinstance(fig.get("value"), str):
            out["header_currency"][mnem] = fig.get("value")
    units, caveats = set(), set()
    for fig in scoped._figures(block, scoped.SCOPE_FISCAL_YEAR_LINE_ITEM):
        if fig.get("mnemonic") != REVENUE_MNEMONIC:
            continue
        units.add(str(fig.get("unit")))
        if fig.get("currency_caveat"):
            caveats.add(str(fig.get("currency_caveat")))
        if _present(fig.get("value")):
            out["series"].append([str(fig.get("fiscal_year")), fig.get("value")])
    out["series"].sort()
    out["units"] = sorted(units)
    out["currency_caveats"] = sorted(caveats)
    return out


def classify(sums, model):
    """The class and its evidence. Never raises on a missing piece: a missing piece is a stated field."""
    p1 = sums[1]["sum"]
    series = model["series"]
    row = {"class": None, "matched_year": None, "matched_value": None, "matched_is_newest": None,
           "newest_year": series[-1][0] if series else None, "nearest_year": None, "nearest_value": None,
           "ratio_p1_to_nearest": None, "ratio_p1_to_newest": None, "note": "", "p2": None, "p2_detail": "",
           "later_period_hits": [], "later_periods_place_p1_on_newest": None}
    hits = []
    for p in PERIODS[1:]:
        s = sums[p]["sum"]
        for y, v in series:
            if s is not None and _within(s, v):
                hits.append([p, y])
    row["later_period_hits"] = hits
    if hits and series and series[-1][0].isdigit():
        newest = int(series[-1][0])
        row["later_periods_place_p1_on_newest"] = all(y.isdigit() and int(y) == newest - (p - 1) for p, y in hits)
    if not series:
        row["class"] = "no-block"
        row["note"] = ("block stored, no %s year" % REVENUE_MNEMONIC) if model["status"] == "SERVED" else (
            "reader status %s" % model["status"])
        return row
    if p1 is None:
        row["class"] = "unmatched"
        row["note"] = "no level-1 row carries a Period 1 value" + _hits_note(row)
        return row
    year, value = min(series, key=lambda yv: abs(p1 / yv[1] - 1.0))
    row["nearest_year"], row["nearest_value"] = year, value
    row["ratio_p1_to_nearest"] = round(p1 / value, 5)
    row["ratio_p1_to_newest"] = round(p1 / series[-1][1], 5)
    if not _within(p1, value):
        row["class"] = "unmatched"
        ratio = row["ratio_p1_to_newest"]
        note = "%d of %d level-1 rows carry a Period 1 value" % (
            sums[1]["present"], sums[1]["present"] + sums[1]["absent"])
        if 1.9 <= ratio <= 2.1:
            note += "; about 2x the newest year"
        elif 900 <= ratio <= 1100 or 0.0009 <= ratio <= 0.0011:
            note += "; about 1000x scale difference"
        row["note"] = note + _hits_note(row)
        return row
    row["class"] = "matched"
    row["matched_year"], row["matched_value"] = year, value
    row["matched_is_newest"] = year == series[-1][0]
    by_year = dict(series)
    prior = str(int(year) - 1) if year.isdigit() else None
    p2 = sums[2]["sum"]
    if p2 is None:
        row["p2"], row["p2_detail"] = "CANNOT_TELL", "no level-1 row carries a Period 2 value"
    elif prior is None or prior not in by_year:
        row["p2"], row["p2_detail"] = "CANNOT_TELL", "fiscal year %s is not stored" % prior
    elif _within(p2, by_year[prior]):
        row["p2"], row["p2_detail"] = "HOLDS", "P2 %.3f vs FY%s %.3f" % (p2, prior, by_year[prior])
    else:
        other = [y for y, v in series if _within(p2, v)]
        row["p2"] = "DOES_NOT_HOLD"
        row["p2_detail"] = "P2 %.3f vs FY%s %.3f, ratio %.5f, %d of %d level-1 rows carry a Period 2 value%s" % (
            p2, prior, by_year[prior], p2 / by_year[prior], sums[2]["present"],
            sums[2]["present"] + sums[2]["absent"], ("; P2 matches FY" + ",".join(other)) if other else "")
    return row


def _hits_note(row):
    if not row["later_period_hits"]:
        return "; no later period matches a stored year"
    return "; later periods matching a stored year: %s (%s with Period 1 = the newest stored year FY%s)" % (
        ", ".join("P%d=FY%s" % (p, y) for p, y in row["later_period_hits"]),
        "consistent" if row["later_periods_place_p1_on_newest"] else "NOT consistent", row["newest_year"])


def read_name(args):
    s3, scoped, crosswalk, partition, keys = args
    key = crosswalk.security_key_from_slash_safe(partition[len("security_key="):])
    obj_key, body, tried = newest_revenue_object(s3, keys)
    out = {"security_key": key, "partition": partition, "segment_objects": len(keys), "segment_objects_read": tried,
           "segment_object": obj_key, "has_revenue_rows": obj_key is not None}
    if obj_key is None:
        return out
    rows = body["response"]["PG_REVENUE"]
    sums, n_level1, levels, names = level1_sums(rows)
    model = model_revenue(scoped, key)
    out.update({"pulled_at": body.get("pulled_at"), "name": (body.get("response") or {}).get("NAME"),
                "revenue_rows": len(rows), "level_counts": levels, "level1_rows": n_level1,
                "level1_metric_names": names, "p1_level1_sum": sums[1]["sum"],
                "p1_level1_present": sums[1]["present"], "p1_level1_absent": sums[1]["absent"],
                "level1_sums_by_period": {"P%d" % p: sums[p] for p in PERIODS}, "model": model})
    out.update(classify(sums, model))
    return out


def _num(v):
    return "-" if v is None else ("%.3f" % v)


def render_md(result):
    c, p2 = result["class_counts"], result["p2_counts"]
    rows = result["rows"]
    lines = [
        "# SEGMENT PERIOD LABEL READ -- AMGT_RESAPP round 78 (CTO msg 31077)",
        "",
        "1. Of %d names with stored revenue segment rows: matched %d, unmatched %d, no-block %d (sum %d)." % (
            result["names_with_revenue_rows"], c["matched"], c["unmatched"], c["no-block"], sum(c.values())),
        "2. Re-pull: Period 1 is not labelled by its own sum for %d names (unmatched %d + no-block %d). In %d of "
        "those %d a LATER period matches a stored year at the offset that puts Period 1 on the newest stored "
        "fiscal year, so their Period 1 is incomplete or empty rather than a different year; %d have no such "
        "evidence. Of the %d matched, %d matched the NEWEST stored fiscal year and %d an earlier one "
        "(matched years: %s)." % (
            c["unmatched"] + c["no-block"], c["unmatched"], c["no-block"], result["unmatched_offset_consistent"],
            c["unmatched"] + c["no-block"],
            c["unmatched"] + c["no-block"] - result["unmatched_offset_consistent"], c["matched"],
            result["matched_newest"], result["matched_earlier"],
            ", ".join("FY%s x%d" % kv for kv in sorted(result["matched_year_counts"].items()))),
        "3. Period 2 test on the %d matched names (Period 2 level-1 sum vs the stored fiscal year one before the "
        "matched one): holds %d, does not hold %d, cannot tell %d." % (
            c["matched"], p2["HOLDS"], p2["DOES_NOT_HOLD"], p2["CANNOT_TELL"]),
        "",
        "Measured %s by `%s`. Control %s: %s." % (result["measured_at"], result["script"], CONTROL_KEY,
                                                    result["control"]),
        "",
        "## What was read",
        "",
        "- Segment table: `s3://%s/%ssecurity_key=<partition>/<stamp>.json`, %d partitions listed, %d with a "
        "non-empty `response.PG_REVENUE`, %d without. Per name the NEWEST object carrying revenue rows." % (
            BUCKET, SEGMENT_PREFIX, result["partitions_listed"], result["names_with_revenue_rows"],
            result["partitions_listed"] - result["names_with_revenue_rows"]),
        "- Model block: the page's reader `lib.research.api.scoped_amgt._read_model_block_pool` -- the newest "
        "`s3://%s/derived/model_block/<security_key>/<stamp>/model_block.json`; rows `figures[]` with "
        "`scope == fiscal_year_line_item` and `mnemonic == %s`; fields `fiscal_year` (a calendar-year string) and "
        "`value`." % (BUCKET, REVENUE_MNEMONIC),
        "- Scale: `unit` values seen on those rows: %s. Currency: a revenue row carries no currency field of its "
        "own (only `currency_caveat`, non-null on %d names); the block's header carries `EQY_FUND_CRNCY` (the "
        "fundamentals currency, column `fund ccy`, present on %d of %d names) and `CRNCY` (the trading currency, "
        "column `trade ccy`). The two differ on %d names. Fund-currency counts: %s." % (
            ", ".join("`%s` x%d" % kv for kv in sorted(result["unit_counts"].items())) or "none",
            result["names_with_currency_caveat"], result["names_with_fund_currency"], len(rows),
            result["fund_differs_from_trading"],
            ", ".join("%s x%d" % kv for kv in sorted(result["fund_currency_counts"].items()))),
        "- Match rule: |P1 level-1 sum / stored year - 1| <= %.3f. A cell with |value| < %g is absent." % (
            TOLERANCE, ABSENT_BELOW),
        "",
        "## Per name (%d)" % len(rows),
        "",
        "| security_key | class | L1 rows | P1 absent | P1 level-1 sum | matched FY | newest FY | nearest FY | "
        "nearest value | ratio | fund ccy / trade ccy | P2 test | note |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        hdr = r["model"]["header_currency"]
        ccy = "%s / %s" % (hdr.get("EQY_FUND_CRNCY") or "-", hdr.get("CRNCY") or "-")
        note = "; ".join(x for x in (r["note"], r["p2_detail"] if r["p2"] == "DOES_NOT_HOLD" else "") if x)
        lines.append("| %s | %s | %d | %d | %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
            r["security_key"], r["class"], r["level1_rows"], r["p1_level1_absent"], _num(r["p1_level1_sum"]),
            r["matched_year"] or "-", r["newest_year"] or "-", r["nearest_year"] or "-", _num(r["nearest_value"]),
            "-" if r["ratio_p1_to_nearest"] is None else "%.5f" % r["ratio_p1_to_nearest"], ccy, r["p2"] or "-",
            note.encode("ascii", "replace").decode("ascii") or "-"))
    lines += ["", "## Names with no revenue rows (%d, outside the %d)" % (
        len(result["no_revenue_rows"]), len(rows)), ""]
    lines += ["- %s (%d object(s) read)" % (n["security_key"], n["segment_objects_read"])
              for n in result["no_revenue_rows"]]
    lines += ["", "## NOT MEASURED", ""] + ["- " + x for x in result["not_measured"]] + [""]
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", default=None)
    args = parser.parse_args(argv)
    root = _repo_root()
    sys.path.insert(0, root)
    import boto3
    from botocore.config import Config
    from lib.research.api import scoped_amgt as scoped
    from lib.research.identity import crosswalk
    import datetime

    s3 = boto3.client("s3", config=Config(max_pool_connections=32))
    by_partition = collections.defaultdict(list)
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=SEGMENT_PREFIX):
        for obj in page.get("Contents", []) or []:
            parts = obj["Key"][len(SEGMENT_PREFIX):].split("/")
            if len(parts) == 2 and parts[0].startswith("security_key=") and parts[1].endswith(".json"):
                by_partition[parts[0]].append(obj["Key"])
    jobs = [(s3, scoped, crosswalk, part, keys) for part, keys in sorted(by_partition.items())]
    with ThreadPoolExecutor(max_workers=12) as pool:
        read = list(pool.map(read_name, jobs))
    rows = [r for r in read if r["has_revenue_rows"]]
    none = [r for r in read if not r["has_revenue_rows"]]
    counts = collections.Counter(r["class"] for r in rows)
    p2 = collections.Counter(r["p2"] for r in rows if r["class"] == "matched")
    matched = [r for r in rows if r["class"] == "matched"]
    units = collections.Counter(u for r in rows for u in r["model"]["units"])
    failed = [r["security_key"] for r in rows if r["model"]["status"] == "READ_FAILED"]
    fund = [r["model"]["header_currency"]["EQY_FUND_CRNCY"] for r in rows
            if r["model"]["header_currency"].get("EQY_FUND_CRNCY")]
    control = next((r for r in rows if r["security_key"] == CONTROL_KEY), None)
    control_ok = bool(control and control["class"] == "matched" and control["matched_year"] == CONTROL_YEAR)
    control_text = "ABSENT from the names read" if control is None else "%s on fiscal year %s, P1 level-1 sum %s" % (
        control["class"], control["matched_year"], _num(control["p1_level1_sum"]))
    result = {
        "measured_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "script": "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/"
                  "r78_read_segment_period_label.py",
        "partitions_listed": len(by_partition),
        "names_with_revenue_rows": len(rows),
        "class_counts": {k: counts.get(k, 0) for k in CLASSES},
        "matched_newest": sum(1 for r in matched if r["matched_is_newest"]),
        "matched_earlier": sum(1 for r in matched if not r["matched_is_newest"]),
        "p2_counts": {k: p2.get(k, 0) for k in P2_CLASSES},
        "unit_counts": dict(units),
        "matched_year_counts": dict(collections.Counter(r["matched_year"] for r in matched)),
        "unmatched_offset_consistent": sum(
            1 for r in rows if r["class"] != "matched" and r["later_periods_place_p1_on_newest"]),
        "names_with_fund_currency": len(fund),
        "fund_currency_counts": dict(collections.Counter(fund)),
        "fund_differs_from_trading": sum(
            1 for r in rows if r["model"]["header_currency"].get("EQY_FUND_CRNCY")
            and r["model"]["header_currency"].get("EQY_FUND_CRNCY") != r["model"]["header_currency"].get("CRNCY")),
        "names_with_currency_caveat": sum(1 for r in rows if r["model"]["currency_caveats"]),
        "model_read_failed": failed,
        "control": control_text + (" -- OK" if control_ok else " -- CONTROL FAILED, the reader is wrong"),
        "not_measured": [
            "The CURRENCY of a segment value. The segment object carries no currency field; a match within 0.5 "
            "percent shows the two stored numbers agree, and the model block states its revenue is in millions of "
            "the reporting currency with header EQY_FUND_CRNCY naming it, so the segment currency is inferred from "
            "the match, not read. That EQY_FUND_CRNCY is the currency of the SALES_REV_TURN rows is the block's "
            "own definition, not something this read tested.",
            "A match by coincidence. The GBp trading names differ from pounds by 100x, which no match could "
            "hide, but two adjacent fiscal years within 0.5 percent of each other were not screened for.",
            "The fiscal-year END DATE. The model block labels a year by a calendar-year string (`fiscal_year`); "
            "no period-end date was read here, so 'FY2025' for a name with a non-December year end is the block's "
            "label, not a date.",
            "Why an unmatched name is unmatched. The ratio and the other-period hits are printed; no cause was "
            "tested (restatement, a hierarchy with two level-1 trees, a newer fiscal year in one store than the "
            "other).",
            "PG_OPERATING_INCOME and every other segment list: only PG_REVENUE was compared.",
            "Periods 3, 4 and 5: the second pass tested Period 2 only.",
            "Bloomberg itself: no live call was made; AMD is the only name whose Period 1 was probed live (by the "
            "issuer, earlier today), and this read reproduces that one from stored data.",
        ],
        "no_revenue_rows": [{"security_key": r["security_key"], "segment_objects_read": r["segment_objects_read"]}
                            for r in none],
        "rows": rows,
    }
    print("partitions listed %d; with revenue rows %d; without %d" % (len(by_partition), len(rows), len(none)))
    print("classes: " + ", ".join("%s %d" % (k, result["class_counts"][k]) for k in CLASSES)
          + " (sum %d of %d)" % (sum(result["class_counts"].values()), len(rows)))
    print("matched on newest stored year %d; on an earlier year %d" % (
        result["matched_newest"], result["matched_earlier"]))
    print("period 2: " + ", ".join("%s %d" % (k, result["p2_counts"][k]) for k in P2_CLASSES))
    print("model reads READ_FAILED: %d %s" % (len(failed), failed))
    print("control: " + result["control"])
    for r in rows:
        if r["class"] != "matched" or r["p2"] != "HOLDS" or not r["matched_is_newest"]:
            print("  %-22s %-9s p1=%s matchedFY=%s newestFY=%s nearest=%s ratio=%s p2=%s | %s %s" % (
                r["security_key"], r["class"], _num(r["p1_level1_sum"]), r["matched_year"], r["newest_year"],
                r["nearest_year"], r["ratio_p1_to_nearest"], r["p2"], r["note"], r["p2_detail"]))
    if args.write:
        os.makedirs(args.write, exist_ok=True)
        with io.open(os.path.join(args.write, "SEGMENT_PERIOD_LABEL_READ.json"), "w", encoding="ascii",
                     newline="\n") as fh:
            fh.write(json.dumps(result, indent=1, sort_keys=True) + "\n")
        with io.open(os.path.join(args.write, "SEGMENT_PERIOD_LABEL_READ.md"), "w", encoding="ascii",
                     newline="\n") as fh:
            fh.write(render_md(result))
        print("wrote SEGMENT_PERIOD_LABEL_READ.md and .json to %s" % args.write)
    done = control_ok and sum(result["class_counts"].values()) == len(rows) and not failed
    print("R78 READ SEGMENT PERIOD LABEL: %s" % ("DONE" if done else "NOT DONE"))
    return 0 if done else 1


if __name__ == "__main__":
    sys.exit(main())
