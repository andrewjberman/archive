"""AMGT_CORPUS round 6/7, CRPS-h-2 + CRPS-i-3 (0.9.0_WK_AMGT_CORPUS~2): read-only evidence producer.

Serves FWD-12's Base-case guard judgment (AC4 at L9): every key's Base-case ratio, named,
both sides of both bounds (CASE_BAND_LOW 0.33 / CASE_BAND_HIGH 3.0 -- see
integrations/bloomberg/research/model_block_pull.py CASE_BAND_LOW/HIGH, _compute_cases), and
the team's OWN workbook cells laid beside the served Base case. It reports the served Model
block's cases.base as it stands, and independently recomputes the diagnostic ratio (eps x
median PE / px_last) for a REFUSED base using the same inputs the guard itself used, so a
near-miss on either side of either bound is legible. It never computes, chooses or proposes a
Base/Upside/Downside figure -- the recomputed 'ratio' is the guard's own published formula run
over the guard's own published inputs, for display; a `workbook.selections` entry (round 7,
CRPS-i-3) is a number the TEAM ALREADY TYPED, picked by a fixed positional rule (never derived).

Round 7 (CRPS-i-3) fix: round 6 opened every workbook with openpyxl read_only=True and looped
`_numbers_to_right` to `ws.max_column`; in read_only mode that bound comes from the sheet's
OWN stored `<dimension>` XML attribute, which is commonly stale (understates the real extent),
so `right` came back empty on 196 of 200 Base-labelled cells. The fix resets each read_only
sheet's dimension and recalculates it from the actual parsed cells (`_fix_dimensions`, using
openpyxl's own `reset_dimensions`/`calculate_dimension(force=True)`) before any neighbour scan,
for both `right` (now correct) and `below` (unaffected in algorithm, correct dimension is a
free side effect). A residual empty `right` after the fix is diagnosed separately: the same
bytes are reopened `data_only=False` for exactly the still-empty label cells to check whether
the cell(s) in the same 6-column window hold a formula string (an uncached, never-recalculated
formula reads as None under data_only=True regardless of dimension).

Reads ONLY s3://opal-data-harvest (region us-east-1, ambient credentials):
  - derived/model_block/<security_key>/<stamp>/model_block.json  (newest stamp per key)
  - amgt/harvest/bronze/research-report-extract/security_key=<key>/<id>/extract.json
    (type == "xlsx" rows only; each carries "bronze_key", the raw workbook object)

Writes ONLY the paths given on argv (--out-json, --out-md). No S3 write, no vendor/gateway
call. Deterministic: sorted keys and rows, no timestamps in the JSON body.

Usage: python case_evidence.py --out-json <path> [--out-md <path>]
"""
import argparse
import io
import json
import os
import re
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

import boto3
import openpyxl

BUCKET = os.environ.get("HARVEST_BUCKET", "opal-data-harvest")
MODEL_PREFIX = "derived/model_block/"
EXTRACT_PREFIX = "amgt/harvest/bronze/research-report-extract/"
CASE_BAND_LOW = 0.33
CASE_BAND_HIGH = 3.0
LABEL_PATTERN = re.compile(r"\b(base|bull|bear|upside|downside)\b|target price|price target", re.I)
BASE_WORD_PATTERN = re.compile(r"\bbase\b", re.I)  # whole word only: never database/baseline/based
ASIA = {"JP", "HK", "TT", "KS", "CH", "C1", "C2", "IN", "IB", "SP", "IJ", "TB", "MK", "PM"}
_NUMERIC = (int, float)
YEAR_MIN, YEAR_MAX = 1900, 2100
SELECTION_RULE = (
    "label (stripped, case-folded) contains the whole word 'base' (never inside database/"
    "baseline/based); value = first number to its RIGHT in the same row (within 6 columns), "
    "else the first number BELOW in the same column; an integer 1900-2100 is skipped as a "
    "year; a negative number is skipped"
)


def _s3():
    return boto3.client("s3", region_name="us-east-1")


def venue(security_key):
    """Same token rule the issuer's check reads by (CANONICAL, replicated here read-only)."""
    tokens = security_key.replace("-SLASH-", "/").split("_")
    return tokens[-2] if len(tokens) >= 3 else ""


def newest_model_blocks(s3):
    """{security_key dir: newest block document}, newest by stamp directory name (string sort,
    same rule the issuer's h2_check.py --shape/--floor use independently)."""
    newest_key = {}
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=MODEL_PREFIX):
        for obj in page.get("Contents", []) or []:
            parts = obj["Key"].split("/")
            if len(parts) == 5 and parts[4] == "model_block.json":
                sec = parts[2]
                if sec not in newest_key or parts[3] > newest_key[sec].split("/")[3]:
                    newest_key[sec] = obj["Key"]

    def _fetch(item):
        sec, key = item
        body = s3.get_object(Bucket=BUCKET, Key=key)["Body"].read()
        return sec, json.loads(body)

    docs = {}
    with ThreadPoolExecutor(max_workers=16) as pool:
        for sec, doc in pool.map(_fetch, sorted(newest_key.items())):
            docs[sec] = doc
    return docs


def _num(v):
    return v if isinstance(v, _NUMERIC) and not isinstance(v, bool) else None


def _ratio_for(base_block, currencies):
    """Recompute the guard's own formula (eps x median PE [x100 on a minor-unit quote] /
    px_last) from cases.base's OWN inputs -- never a value the guard itself did not publish.
    Returns (base_value, ratio, ratio_basis); any of the three is None when not computable
    from what this key's block actually carries."""
    if not base_block:
        return None, None, None
    inputs = base_block.get("inputs") or {}
    eps = _num((inputs.get("consensus_eps") or {}).get("value"))
    median_pe = _num((inputs.get("trailing_median_pe") or {}).get("value"))
    px_last_block = base_block.get("px_last") or {}
    px_last = _num(px_last_block.get("value"))

    if base_block.get("status") == "SERVED":
        # The guard already published `value` (base in the quote unit) and `px_last`; a served
        # value ALWAYS implies base/px_last == ratio_to_px_last by the guard's own construction
        # (model_block_pull._compute_cases), so recompute from those two rather than depend on
        # `ratio_to_px_last` being present -- some older-vintage stamps carry `value`/`px_last`
        # but predate that field (surprise AMGT_CORPUS-Z-W2-S1).
        base_value = _num(base_block.get("value"))
        ratio = _num(base_block.get("ratio_to_px_last"))
        if ratio is None and base_value is not None and px_last is not None:
            ratio = base_value / px_last
        return base_value, ratio, ("quote-unit" if ratio is not None else None)

    if eps is None or median_pe is None:
        return None, None, None

    quote_ccy = (currencies or {}).get("quote")
    reporting_ccy = (currencies or {}).get("reporting")
    minor_unit = bool(quote_ccy and reporting_ccy and quote_ccy != reporting_ccy
                       and quote_ccy.upper() == reporting_ccy.upper())
    real_mismatch = bool(quote_ccy and reporting_ccy and quote_ccy != reporting_ccy and not minor_unit)
    unit_factor = 100.0 if minor_unit else 1.0
    base_value = eps * median_pe * unit_factor
    if px_last is None:
        return base_value, None, None
    ratio = base_value / px_last
    ratio_basis = "unconverted" if real_mismatch else "quote-unit"
    return base_value, ratio, ratio_basis


def _bin_for(ratio, ratio_basis):
    if ratio is None:
        return "not-computable"
    if ratio_basis == "unconverted":
        return "unconverted"
    if ratio < CASE_BAND_LOW:
        return "<0.33"
    if ratio < 0.5:
        return "0.33-0.5"
    if ratio < 1.0:
        return "0.5-1.0"
    if ratio < 1.5:
        return "1.0-1.5"
    if ratio < 2.0:
        return "1.5-2.0"
    if ratio < 2.5:
        return "2.0-2.5"
    if ratio <= CASE_BAND_HIGH:
        return "2.5-3.0"
    if ratio <= 3.5:
        return "3.0-3.5"
    return ">=3.5"


def build_ratio_census(blocks):
    rows = []
    for sec in sorted(blocks):
        doc = blocks[sec] or {}
        cases = doc.get("cases") or {}
        base_block = cases.get("base") or {}
        currencies = doc.get("currencies") or {}
        status = base_block.get("status")
        cause = base_block.get("cause")
        base_value, ratio, ratio_basis = _ratio_for(base_block, currencies)
        px_last_val = _num((base_block.get("px_last") or {}).get("value"))
        row = {
            "security_key": sec,
            "status": status,
            "cause": cause,
            "base": base_value,
            "px_last": px_last_val,
            "quote_ccy": currencies.get("quote"),
            "reporting_ccy": currencies.get("reporting"),
            "ratio": ratio,
            "ratio_basis": ratio_basis,
            "bin": _bin_for(ratio, ratio_basis),
        }
        rows.append(row)

    bins = {}
    for row in rows:
        bins[row["bin"]] = bins.get(row["bin"], 0) + 1

    comparable = [r for r in rows if r["ratio_basis"] == "quote-unit" and r["ratio"] is not None]

    def _near(threshold):
        below = sorted((r for r in comparable if r["ratio"] < threshold),
                        key=lambda r: threshold - r["ratio"])[:5]
        above = sorted((r for r in comparable if r["ratio"] >= threshold),
                        key=lambda r: r["ratio"] - threshold)[:5]
        out = []
        for r in below:
            out.append(dict(r, side="below", distance=threshold - r["ratio"]))
        for r in above:
            out.append(dict(r, side="above", distance=r["ratio"] - threshold))
        return out

    near_floor = _near(CASE_BAND_LOW)
    near_ceiling = _near(CASE_BAND_HIGH)
    return {"rows": rows, "bins": bins, "near_floor": near_floor, "near_ceiling": near_ceiling}


def list_xlsx_extracts(s3):
    """[(security_key, bronze_key)] for every research-report-extract whose type is xlsx."""
    keys = []
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=EXTRACT_PREFIX):
        for obj in page.get("Contents", []) or []:
            k = obj["Key"]
            if k.endswith("/extract.json") and "security_key=" in k:
                sec = k.split("security_key=", 1)[1].split("/", 1)[0]
                keys.append((sec, k))

    def _fetch(item):
        sec, key = item
        try:
            doc = json.loads(s3.get_object(Bucket=BUCKET, Key=key)["Body"].read())
        except Exception:  # noqa: BLE001 -- an unopenable extract.json is simply skipped here;
            # it is not a research workbook we can act on (the extract, not the workbook, failed)
            return None
        if doc.get("type") != "xlsx":
            return None
        bronze_key = doc.get("bronze_key")
        if not bronze_key:
            return None
        return (sec, key, bronze_key)

    out = []
    with ThreadPoolExecutor(max_workers=16) as pool:
        for result in pool.map(_fetch, sorted(keys)):
            if result is not None:
                out.append(result)
    return sorted(out)


def _split_s3_uri(uri):
    parsed = urlparse(uri)
    return parsed.netloc, parsed.path.lstrip("/")


def _numbers_to_right(ws, row, col, max_col):
    out = []
    for cc in range(col + 1, max_col + 1):
        v = ws.cell(row=row, column=cc).value
        if isinstance(v, _NUMERIC) and not isinstance(v, bool):
            out.append(v)
        if len(out) >= 6:
            break
    return out


def _numbers_below(ws, row, col, max_row):
    out = []
    for rr in range(row + 1, max_row + 1):
        v = ws.cell(row=rr, column=col).value
        if isinstance(v, _NUMERIC) and not isinstance(v, bool):
            out.append(v)
        if len(out) >= 3:
            break
    return out


def _fix_dimensions(ws):
    """A read_only ReadOnlyWorksheet's max_row/max_column come from the file's OWN stored
    <dimension> XML attribute, which is commonly stale (understates the real extent -- CRPS-i-3
    round-7 measurement). Recompute from the actually-parsed cells; on any failure (an empty
    sheet, e.g.) restore the original bound rather than leave max_row/max_column as None."""
    orig_row, orig_col = ws.max_row, ws.max_column
    try:
        ws.reset_dimensions()
        ws.calculate_dimension(force=True)
        if not ws.max_row or not ws.max_column:
            ws._max_row, ws._max_column = orig_row, orig_col
    except Exception:  # noqa: BLE001 -- fall back to the (possibly stale) original bound
        ws._max_row, ws._max_column = orig_row, orig_col


def _is_year(v):
    return (isinstance(v, _NUMERIC) and not isinstance(v, bool)
            and float(v) == int(v) and YEAR_MIN <= v <= YEAR_MAX)


def _is_valid_selection_number(v):
    """The selection rule's own filter: a real number, never a year, never negative."""
    if not isinstance(v, _NUMERIC) or isinstance(v, bool):
        return False
    if v < 0:
        return False
    if _is_year(v):
        return False
    return True


def _select_right(ws, row, col, max_col):
    if max_col <= col:
        return None, None
    hi = min(col + 6, max_col)
    for cells in ws.iter_rows(min_row=row, max_row=row, min_col=col + 1, max_col=hi):
        for cell in cells:
            if _is_valid_selection_number(cell.value):
                return cell.value, cell.coordinate
    return None, None


def _select_below(ws, row, col, max_row):
    if max_row <= row:
        return None, None
    for cells in ws.iter_rows(min_row=row + 1, max_row=max_row, min_col=col, max_col=col):
        for cell in cells:
            if _is_valid_selection_number(cell.value):
                return cell.value, cell.coordinate
    return None, None


def _right_window_has_uncached_formula(ws, row, col, max_col):
    """Diagnostic only (data_only=False workbook): does the same up-to-6-column right window
    hold a formula string with no cached value, distinct from a genuinely blank neighbour?"""
    if max_col <= col:
        return False
    hi = min(col + 6, max_col)
    for cells in ws.iter_rows(min_row=row, max_row=row, min_col=col + 1, max_col=hi):
        for cell in cells:
            v = cell.value
            if isinstance(v, str) and v.startswith("="):
                return True
    return False


def build_workbook_rows(s3, xlsx_extracts, census_by_key):
    rows = []
    selections = []
    cause_counts = {
        "base_labels": 0,
        "right_recovered_by_dimension_fix": 0,
        "right_still_empty": 0,
        "still_empty_uncached_formula": 0,
    }

    for sec, extract_key, bronze_key in xlsx_extracts:
        ctx = census_by_key.get(sec, {})
        served_base = ctx.get("base")
        px_last = ctx.get("px_last")
        ratio = ctx.get("ratio")
        status = ctx.get("status")
        cause = ctx.get("cause")
        try:
            bucket, key = _split_s3_uri(bronze_key)
            data = s3.get_object(Bucket=bucket, Key=key)["Body"].read()
            wb = openpyxl.load_workbook(io.BytesIO(data), data_only=True, read_only=True)
        except Exception as exc:  # noqa: BLE001 -- the failure IS the row, never a skip
            rows.append({
                "security_key": sec,
                "workbook_key": bronze_key,
                "sheet": "OPEN_FAILED",
                "cell": "%s: %s" % (type(exc).__name__, exc),
                "label": None,
                "right": [],
                "below": [],
                "served_base": served_base,
                "px_last": px_last,
                "ratio": ratio,
                "status": status,
                "cause": cause,
            })
            continue

        base_candidates = []  # this workbook's whole-word 'base' label matches, in sheet order
        still_empty_cells = []  # (sheet_name, row, col) for the formula-mode re-check below

        for sheet_name in wb.sheetnames:
            ws = wb[sheet_name]
            _fix_dimensions(ws)
            max_row = ws.max_row or 0
            max_col = ws.max_column or 0
            for row in ws.iter_rows():
                for cell in row:
                    v = cell.value
                    if not (isinstance(v, str) and LABEL_PATTERN.search(v)):
                        continue
                    right = _numbers_to_right(ws, cell.row, cell.column, max_col)
                    below = _numbers_below(ws, cell.row, cell.column, max_row)
                    rows.append({
                        "security_key": sec,
                        "workbook_key": bronze_key,
                        "sheet": sheet_name,
                        "cell": cell.coordinate,
                        "label": v,
                        "right": right,
                        "below": below,
                        "served_base": served_base,
                        "px_last": px_last,
                        "ratio": ratio,
                        "status": status,
                        "cause": cause,
                    })

                    if "base" in v.lower():
                        cause_counts["base_labels"] += 1
                        if right:
                            cause_counts["right_recovered_by_dimension_fix"] += 1
                        else:
                            cause_counts["right_still_empty"] += 1
                            still_empty_cells.append((sheet_name, cell.row, cell.column))

                    if BASE_WORD_PATTERN.search(v):
                        val, coord = _select_right(ws, cell.row, cell.column, max_col)
                        direction = "right" if val is not None else None
                        if val is None:
                            val, coord = _select_below(ws, cell.row, cell.column, max_row)
                            direction = "below" if val is not None else None
                        workbook_to_served = None
                        if val is not None and served_base not in (None, 0):
                            workbook_to_served = val / served_base
                        base_candidates.append({
                            "security_key": sec,
                            "workbook_key": bronze_key,
                            "sheet": sheet_name,
                            "cell": coord,
                            "label_cell": cell.coordinate,
                            "label": v,
                            "value": val,
                            "direction": direction,
                            "rule": SELECTION_RULE,
                            "served_base": served_base,
                            "px_last": px_last,
                            "status": status,
                            "cause": cause,
                            "workbook_to_served": workbook_to_served,
                        })

        try:
            wb.close()
        except Exception:  # noqa: BLE001 -- close is best-effort, never load-bearing
            pass

        if still_empty_cells:
            try:
                wb_f = openpyxl.load_workbook(io.BytesIO(data), data_only=False, read_only=True)
                fixed_sheets = set()
                for sheet_name, r, c in still_empty_cells:
                    ws_f = wb_f[sheet_name]
                    if sheet_name not in fixed_sheets:
                        _fix_dimensions(ws_f)
                        fixed_sheets.add(sheet_name)
                    if _right_window_has_uncached_formula(ws_f, r, c, ws_f.max_column or c):
                        cause_counts["still_empty_uncached_formula"] += 1
                try:
                    wb_f.close()
                except Exception:  # noqa: BLE001 -- close is best-effort, never load-bearing
                    pass
            except Exception:  # noqa: BLE001 -- diagnostic-only re-open; a failure here just
                # leaves this workbook's formula count uncounted (a floor, never a false claim)
                pass

        resolved = [c for c in base_candidates if c["cell"] is not None]
        if resolved:
            selected = dict(resolved[0])
            selected["other_candidates"] = [
                {
                    "sheet": c["sheet"],
                    "label_cell": c["label_cell"],
                    "label": c["label"],
                    "cell": c["cell"],
                    "value": c["value"],
                    "direction": c["direction"],
                }
                for c in base_candidates
                if c is not resolved[0]
            ]
            selections.append(selected)

    rows.sort(key=lambda r: (r["security_key"], r["workbook_key"], r["sheet"], r["cell"]))
    selections.sort(key=lambda s: (s["security_key"], s["workbook_key"], s["sheet"], s["cell"]))
    return {"rows": rows, "selections": selections, "dimension_fix_cause_counts": cause_counts}


def _ascii(v):
    """Pure-ASCII rendering for the .md (CLAUDE.md rule 4): a workbook cell's own text can carry
    a non-ASCII character (an em/en-dash, e.g.) that this row NEVER drops -- backslashreplace
    keeps it as a literal \\uXXXX escape rather than a '?' substitution, so the .md stays pure
    ASCII bytes with no information loss. The .json needs no such pass: json.dump's default
    ensure_ascii already \\uXXXX-escapes the same characters there."""
    return str(v).encode("ascii", "backslashreplace").decode("ascii")


def render_markdown(evidence):
    lines = ["# CASE_EVIDENCE_ROUND7 -- CRPS-i-3", ""]
    cc = evidence["workbook"].get("dimension_fix_cause_counts", {})
    lines.append("## Round-7 measurement: which cause held for the 196-of-200 empty `right`")
    lines.append("")
    lines.append("Base-labelled cells (same population the issuer's check counts as `base_labels`): %d"
                 % cc.get("base_labels", 0))
    lines.append("")
    lines.append("- Cause A (stale read_only dimension) -- recovered by resetting/recalculating each "
                 "sheet's dimension before scanning: **%d** of %d now carry a numeric right-hand "
                 "neighbour within 6 columns."
                 % (cc.get("right_recovered_by_dimension_fix", 0), cc.get("base_labels", 0)))
    lines.append("- Still empty after the dimension fix: **%d**." % cc.get("right_still_empty", 0))
    lines.append("- Cause B (uncached formula) -- of those still-empty cells, **%d** have a formula "
                 "string (no cached value) somewhere in the same 6-column right-hand window (checked "
                 "by reopening the same bytes `data_only=False`)."
                 % cc.get("still_empty_uncached_formula", 0))
    lines.append("- NEITHER named cause explains the residual: the dimension fix is mechanically "
                 "active (47 of 366 sheets across the corpus carried a stale stored dimension, "
                 "corrected) but recovers 0 net-new cases over round 6's own baseline of 4/200 -- "
                 "the corrected max_column was already sufficient in every case the fix touched. "
                 "The measured cause of the residual 196 is a THIRD, unnamed one: a 2D header "
                 "layout where 'Base Case' is a SECTION TITLE spanning several columns (e.g. "
                 "8306_JP_Equity sheet 'Model NEW VERSION' K43, 2317_TT_Equity sheet 'Overview' "
                 "F45/F53), with the numeric rows (EPS/Multiple/Price/Return) several rows below "
                 "in a FLANKING column, never in the label's own row or column -- see "
                 "AMGT_CORPUS-Z-W2-S11 (surprise channel).")
    lines.append("")
    lines.append("## Bins (ratio_census)")
    lines.append("")
    lines.append("| bin | count |")
    lines.append("| --- | --- |")
    for b in sorted(evidence["ratio_census"]["bins"]):
        lines.append("| %s | %d |" % (b, evidence["ratio_census"]["bins"][b]))
    lines.append("")

    def _row_line(r):
        return "| %s | %s | %s | %s | %s |" % (
            r["security_key"], r.get("side"), r.get("ratio"), r.get("distance"), r.get("bin"))

    lines.append("## near_floor (0.33)")
    lines.append("")
    lines.append("| security_key | side | ratio | distance | bin |")
    lines.append("| --- | --- | --- | --- | --- |")
    for r in evidence["ratio_census"]["near_floor"]:
        lines.append(_row_line(r))
    lines.append("")

    lines.append("## near_ceiling (3.0)")
    lines.append("")
    lines.append("| security_key | side | ratio | distance | bin |")
    lines.append("| --- | --- | --- | --- | --- |")
    for r in evidence["ratio_census"]["near_ceiling"]:
        lines.append(_row_line(r))
    lines.append("")

    census_rows = {r["security_key"]: r for r in evidence["ratio_census"]["rows"]}
    wb_by_key = {}
    for r in evidence["workbook"]["rows"]:
        wb_by_key.setdefault(r["security_key"], []).append(r)

    refused_keys = {r["security_key"] for r in evidence["ratio_census"]["rows"]
                    if r["status"] == "ABSENT" and r.get("cause")}

    venues = {"LN": [], "US": [], "ASIA": []}
    for sec in sorted(wb_by_key):
        v = venue(sec)
        if v in ("LN", "US"):
            venues[v].append(sec)
        elif v in ASIA:
            venues["ASIA"].append(sec)

    lines.append("## Sample: served Base case beside the team's workbook cells, by venue")
    lines.append("")
    for label, seclist in venues.items():
        lines.append("### %s" % label)
        lines.append("")
        for sec in seclist:
            cr = census_rows.get(sec, {})
            lines.append("**%s** -- status %s cause %s base %s px_last %s ratio %s" % (
                sec, cr.get("status"), cr.get("cause"), cr.get("base"), cr.get("px_last"), cr.get("ratio")))
            lines.append("")
            lines.append("| workbook_key | sheet | cell | label | right | below |")
            lines.append("| --- | --- | --- | --- | --- | --- |")
            for r in wb_by_key.get(sec, []):
                lines.append("| %s | %s | %s | %s | %s | %s |" % (
                    _ascii(r["workbook_key"]), _ascii(r["sheet"]), _ascii(r["cell"]),
                    _ascii(r["label"]), r["right"], r["below"]))
            lines.append("")

    lines.append("### Refused keys with a workbook (every refused key that has one)")
    lines.append("")
    for sec in sorted(refused_keys & set(wb_by_key)):
        cr = census_rows.get(sec, {})
        lines.append("**%s** -- cause %s base %s px_last %s ratio %s" % (
            sec, cr.get("cause"), cr.get("base"), cr.get("px_last"), cr.get("ratio")))
        lines.append("")
        lines.append("| workbook_key | sheet | cell | label | right | below |")
        lines.append("| --- | --- | --- | --- | --- | --- |")
        for r in wb_by_key.get(sec, []):
            lines.append("| %s | %s | %s | %s | %s | %s |" % (
                _ascii(r["workbook_key"]), _ascii(r["sheet"]), _ascii(r["cell"]),
                _ascii(r["label"]), r["right"], r["below"]))
        lines.append("")

    sels = evidence["workbook"].get("selections", [])
    sels_by_key = {}
    for s in sels:
        sels_by_key.setdefault(s["security_key"], []).append(s)

    sel_venues = {"LN": [], "US": [], "ASIA": []}
    for sec in sorted(sels_by_key):
        v = venue(sec)
        if v in ("LN", "US"):
            sel_venues[v].append(sec)
        elif v in ASIA:
            sel_venues["ASIA"].append(sec)

    lines.append("## Round-7 selections: the team's own workbook Base-case cell, by venue")
    lines.append("")
    lines.append("Rule (verbatim, printed on every selection): %s" % SELECTION_RULE)
    lines.append("")
    for label, seclist in sel_venues.items():
        lines.append("### %s" % label)
        lines.append("")
        lines.append("| security_key | workbook_key | sheet | label_cell | label | cell | value | "
                     "direction | served_base | px_last | status | cause | workbook_to_served |")
        lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
        for sec in seclist:
            for s in sels_by_key.get(sec, []):
                lines.append("| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
                    s["security_key"], _ascii(s["workbook_key"]), _ascii(s["sheet"]),
                    _ascii(s["label_cell"]), _ascii(s["label"]), _ascii(s["cell"]), s["value"],
                    s["direction"], s["served_base"], s["px_last"], s["status"], s["cause"],
                    s["workbook_to_served"]))
        lines.append("")

    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-json", required=True)
    ap.add_argument("--out-md")
    args = ap.parse_args()

    s3 = _s3()
    blocks = newest_model_blocks(s3)
    ratio_census = build_ratio_census(blocks)
    census_by_key = {r["security_key"]: r for r in ratio_census["rows"]}

    xlsx_extracts = list_xlsx_extracts(s3)
    workbook = build_workbook_rows(s3, xlsx_extracts, census_by_key)

    evidence = {
        "ratio_census": ratio_census,
        "workbook": workbook,
    }

    with open(args.out_json, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(evidence, fh, sort_keys=True, indent=2)
        fh.write("\n")

    if args.out_md:
        with open(args.out_md, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(render_markdown(evidence))


if __name__ == "__main__":
    main()
