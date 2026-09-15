#!/usr/bin/env python3
"""W1-AC4 / W1-AC12 -- READ THE `tickers` BLOCK BACK AND COUNT IT.

POSN_ASTTAX.TO-W1-1, cell AT6-s-1, `0.9.0_WK_POSN_ASTTAX~24`.

TWO MODES, ONE READER, so the dry run and the served artifact are graded by the SAME
instrument and a difference between them cannot hide in a difference between two scripts:

    python3 dry_run_tickers_report.py <LOCAL_OUT>   W1-AC4: the local dry-run artifact, read
                                                    against holdings.json (the ticker
                                                    denominator), positioning_data.json and
                                                    the Bloomberg partition (the two sources
                                                    it claims to have read), plus the PEAK RSS
                                                    of a producer process.
    python3 dry_run_tickers_report.py --served      W1-AC12: the SERVED artifact, read back
                                                    with get-object and compared to <LOCAL_OUT>
                                                    (tickers block DEEP-EQUAL) and to the
                                                    PRE-DEPLOY served copy (satellites block).

EVERY COUNT PRINTS ITS DENOMINATOR. A count with no denominator is a number, not a
measurement, and this reader exists because the criterion asks for measurements.

NOTHING IS WRITTEN. ASCII only.
"""
from __future__ import annotations

import argparse
import datetime as dt
import gzip
import io
import json
import os
import subprocess
import sys
import time

import boto3

LOCAL_OUT_DEFAULT = "C:/tmp/wk-posn-6-24/.scratch/b6_local.json"
PRE_DEPLOY_SERVED = "C:/tmp/wk-posn-6-24/.scratch/served_pre_deploy.json"
PRODUCER = "data/assets/scripts/gold/build_satellites_characteristics.py"

HOLDINGS = ("opal-data-cot", "platinum/satellites/holdings.json")
POSITIONING = ("opal-data-portal-v2", "json/positioning/positioning_data.json")
SERVED = ("opal-data-cot", "platinum/satellites/characteristics.json")
BBG_BUCKET = "opal-data-etfs"

SEVEN = ["fee", "aum", "active", "yield", "duration", "credit", "beta"]
BBG_COLS = {"fee": "FUND_EXPENSE_RATIO", "yield": "EQY_DVD_YLD_IND_NET",
            "duration": "HB_OAS_EFF_DURTN", "beta": "BETA_ADJ_OVERRIDABLE",
            "aum": "FUND_TOTAL_ASSETS"}


def native(path: str) -> str:
    """/c/x -> C:/x. Native python on this device cannot open an MSYS path (W24-S2)."""
    if len(path) > 3 and path[0] == "/" and path[2] == "/":
        return path[1].upper() + ":" + path[2:]
    return path


def s3c():
    return boto3.client("s3")


def read_json_s3(bucket: str, key: str, version: str = None) -> dict:
    kw = {"Bucket": bucket, "Key": key}
    if version:
        kw["VersionId"] = version
    raw = s3c().get_object(**kw)["Body"].read()
    if raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)
    return json.loads(raw.decode("utf-8"))


def triple(doc: dict) -> tuple:
    i = doc.get("inputs") or {}
    return (i.get("holdings_as_of"), i.get("positioning_data_as_of"), i.get("bbg_as_of"))


def deep_equal(a, b, path="$"):
    if type(a) is not type(b):
        return "%s: type %s != %s" % (path, type(a).__name__, type(b).__name__)
    if isinstance(a, dict):
        for k in a:
            if k not in b:
                return "%s.%s: only in the first" % (path, k)
        for k in b:
            if k not in a:
                return "%s.%s: only in the second" % (path, k)
        for k in a:
            d = deep_equal(a[k], b[k], "%s.%s" % (path, k))
            if d:
                return d
        return None
    if isinstance(a, list):
        if len(a) != len(b):
            return "%s: len %d != %d" % (path, len(a), len(b))
        for i, (x, y) in enumerate(zip(a, b)):
            d = deep_equal(x, y, "%s[%d]" % (path, i))
            if d:
                return d
        return None
    return None if a == b else "%s: %r != %r" % (path, a, b)


def distinct_from_holdings(holdings: dict):
    """THE DENOMINATOR: every ticker any satellite holds, deduped, plus the raw row count."""
    seen, rows = [], 0
    for code in holdings.get("satellites") or {}:
        for row in (holdings["satellites"][code].get("holdings") or []):
            t = (row.get("ticker") or "").strip().upper()
            rows += 1
            if t and t not in seen:
                seen.append(t)
    return seen, rows


def yang_rows(positioning: dict) -> dict:
    out = {}
    books = positioning.get("current_holdings") or {}
    for bname in books:
        book = books[bname]
        rs = book.get("holdings") if isinstance(book, dict) else book
        for row in rs or []:
            t = (row.get("ticker") or "").strip().upper()
            if t and t not in out:
                out[t] = row
    return out


def bbg_rows(bbg_as_of: str):
    import pandas as pd
    key = "bbg/%s/characteristics.parquet" % bbg_as_of
    frame = pd.read_parquet(io.BytesIO(s3c().get_object(Bucket=BBG_BUCKET, Key=key)["Body"].read()))
    out = {}
    for rec in frame.to_dict("records"):
        sec = str(rec.get("security") or "").strip()
        if sec:
            out.setdefault(sec.split()[0].upper(), rec)
    return out, key, len(frame)


def show(v):
    return "NULL" if v is None else repr(v)


def null_window_reasons(ticker: str, bbg_as_of: str, windows) -> dict:
    """THE RULE'S OWN REASON for a null window -- derived from the rule's own history.

    Only called when a window IS null: it re-loads the history (a listing plus every backfill
    series), which is the price of naming the reason rather than guessing it.
    """
    from data.etfs.scripts.gold.etf_positioning_gold import _window_start, load_history
    as_of = dt.date.fromisoformat(bbg_as_of)
    hist = load_history(as_of, BBG_BUCKET)
    rows = hist[hist["tkr"] == ticker] if not hist.empty else hist
    out = {}
    if hist.empty or rows.empty:
        return {w: "no series (0 history row(s) for %s)" % ticker for w in windows}
    dates = set(rows["date"].tolist())
    if as_of not in dates:
        return {w: "frontier absent (no observation ON %s)" % bbg_as_of for w in windows}
    first = min(dates)
    for w in windows:
        start = _window_start(as_of, w)
        if start is None:
            out[w] = "no window start defined"
        elif first > start:
            out[w] = "start coverage (series begins %s, window starts %s)" % (first, start)
        else:
            sel = rows[(rows["date"] >= start) & (rows["date"] <= as_of)][
                "DAY_TO_DAY_TOT_RETURN_GROSS_DVDS"]
            out[w] = ("a NaN inside the window (%d of %d observation(s) null)"
                      % (int(sel.isna().sum()), len(sel)))
    return out


def peak_rss_of_producer(bbg_as_of: str) -> str:
    """Peak RSS of a PRODUCER PROCESS -- the object the .tf's memory_size is sized against.

    GRAIN, STATED: this is a SECOND producer process spawned by this reader with the same
    arguments, because a process's peak working set is not readable after it exits, so the
    run in the criterion's own invocation cannot be the one measured. Instrument: psutil
    peak_wset polled while it runs (the raw psapi/ctypes route returns FALSE on this device --
    measured, and recorded in the .tf). It is the WHOLE process: interpreter, boto3, pandas
    and pyarrow included, which is exactly what the Lambda's memory_size has to hold.
    """
    try:
        import psutil
    except ImportError:
        return "UNAVAILABLE (psutil absent) -- no peak RSS measured on this device"
    cmd = [sys.executable, PRODUCER, "--bbg-as-of", bbg_as_of, "--dry-run"]
    t0 = time.time()
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    peak = 0
    try:
        p = psutil.Process(proc.pid)
        while proc.poll() is None:
            try:
                peak = max(peak, p.memory_info().peak_wset)
            except Exception:  # noqa: BLE001 - the process ended between poll and read
                break
            time.sleep(0.15)
    finally:
        rc = proc.wait()
    return ("%.1f MiB (psutil peak_wset, whole process incl. pandas+pyarrow; child rc=%d, "
            "wall %.1f s)" % (peak / 1048576.0, rc, time.time() - t0))


def report_local(local_out: str) -> int:
    doc = json.load(open(local_out, encoding="utf-8"))
    tickers = doc.get("tickers") or {}
    bbg_as_of = (doc.get("inputs") or {}).get("bbg_as_of")
    print("ARTIFACT: %s  schema_version=%s as_of=%s" % (local_out, doc.get("schema_version"), doc.get("as_of")))
    print("INPUTS TRIPLE (holdings_as_of, positioning_data_as_of, bbg_as_of): %s" % (triple(doc),))
    print("method.tickers_block: %s" % json.dumps((doc.get("method") or {}).get("tickers_block")))

    holdings = read_json_s3(*HOLDINGS)
    distinct, raw_rows = distinct_from_holdings(holdings)
    print("")
    print("--- THE COUNT AND ITS DENOMINATOR ---")
    print("holdings.json rows across %d satellite(s): %d ; DISTINCT tickers: %d"
          % (len(holdings.get("satellites") or {}), raw_rows, len(distinct)))
    print("tickers block keys: %d" % len(tickers))
    print("COUNTS EQUAL: %s (%d of %d)" % (len(tickers) == len(distinct), len(tickers), len(distinct)))
    missing = [t for t in distinct if t not in tickers]
    extra = [t for t in tickers if t not in distinct]
    print("held but MISSING from the block: %d %s" % (len(missing), missing))
    print("in the block but held by NOBODY: %d %s" % (len(extra), extra))
    print("NO TICKER TWICE: %s (a json object cannot repeat a key; re-parsed pairs: %d)"
          % (len(tickers) == len(distinct) and not missing and not extra, len(tickers)))

    print("")
    print("--- SOURCES, BY NAME (denominator %d) ---" % len(tickers))
    by = {}
    for t, row in tickers.items():
        by.setdefault(row.get("source"), []).append(t)
    for name in sorted(by):
        print("  %-16s %2d of %d  %s" % (name, len(by[name]), len(tickers), ",".join(sorted(by[name]))))

    print("")
    print("--- THE IDENTITY PAIR (C-HOLDING-IDENTITY), denominator %d ---" % len(tickers))
    both_present = 0
    for t in sorted(tickers):
        row = tickers[t]
        pair_ok = row.get("name") is not None and row.get("management_style") is not None
        both_present += 1 if pair_ok else 0
        print("  %-6s name=%-46s management_style=%-9s source=%s"
              % (t, show(row.get("name"))[:46], show(row.get("management_style")), row.get("source")))
    tb = (doc.get("method") or {}).get("tickers_block") or {}
    print("IDENTITY PAIR PRESENT (both fields non-null): %d of %d" % (both_present, len(tickers)))
    print("name present: %d of %d | management_style present: %d of %d"
          % (sum(1 for r in tickers.values() if r.get("name") is not None), len(tickers),
             sum(1 for r in tickers.values() if r.get("management_style") is not None), len(tickers)))
    print("method.tickers_block.identity_source=%s identity_missing=%s (the table did not carry "
          "that many of the %d distinct tickers)"
          % (tb.get("identity_source"), tb.get("identity_missing"), len(tickers)))

    positioning = read_json_s3(*POSITIONING)
    yang = yang_rows(positioning)
    agree_name = agree_style = yang_n = 0
    for t in sorted(tickers):
        yrow = yang.get(t)
        if not yrow:
            continue
        yang_n += 1
        yname = yrow.get("name")
        yactive = yrow.get("active")
        style = tickers[t].get("management_style")
        n_ok = yname is not None and str(yname).strip() == str(tickers[t].get("name") or "").strip()
        s_ok = (style is not None and yactive is not None
                and ((str(style).lower() == "active") == (int(yactive) == 1)))
        agree_name += 1 if n_ok else 0
        agree_style += 1 if s_ok else 0
    print("CORROBORATION on the %d Yang-carried ticker(s): name agrees %d of %d; "
          "management_style vs Yang `active` agrees %d of %d"
          % (yang_n, agree_name, yang_n, agree_style, yang_n))

    bbg, bbg_key, bbg_n = bbg_rows(bbg_as_of)
    both = [t for t in distinct if t in yang and t in bbg]
    print("")
    print("--- BOTH SOURCES CARRY IT: Yang aum vs %s (s3://%s/%s, %d row(s)) ---"
          % (BBG_COLS["aum"], BBG_BUCKET, bbg_key, bbg_n))
    equal = 0
    for t in sorted(both):
        ya = yang[t].get("aum")
        ba = bbg[t].get(BBG_COLS["aum"])
        try:
            same = ya is not None and ba is not None and abs(float(ya) - float(ba)) < 1e-6
        except (TypeError, ValueError):
            same = False
        equal += 1 if same else 0
        print("  %-6s yang.aum=%-22s bbg.%s=%-22s EQUAL=%s served=%s"
              % (t, show(ya), BBG_COLS["aum"], show(ba), same, show(tickers.get(t, {}).get("aum"))))
    print("AUM EQUAL: %d of %d ticker(s) both sources carry" % (equal, len(both)))

    print("")
    print("--- THE BLOOMBERG-SOURCED ROW(S), AGAINST THE COLUMNS THEY CLAIM ---")
    for t in sorted(by.get("bbg", [])):
        row = tickers[t]
        rec = bbg.get(t, {})
        print("  %s  source=%s" % (t, row.get("source")))
        for f in SEVEN:
            col = BBG_COLS.get(f)
            raw = rec.get(col) if col else None
            print("     %-9s served=%-22s <- %-22s raw=%s"
                  % (f, show(row.get(f)), col or "NO BLOOMBERG COLUMN", show(raw)))
        rets = row.get("returns") or {}
        nulls = [w for w in rets if rets[w] is None]
        print("     returns: %d window(s), %d with a value, %d null"
              % (len(rets), len(rets) - len(nulls), len(nulls)))
        for w in rets:
            print("        %-4s %s" % (w, show(rets[w])))
        if nulls:
            print("     REASONS (from the rule's own history):")
            for w, why in null_window_reasons(t, bbg_as_of, nulls).items():
                print("        %-4s %s" % (w, why))
        print("     active NULL: %s | credit NULL: %s"
              % (row.get("active") is None, row.get("credit") is None))

    print("")
    print("--- THE UNPRICED ROW(S) ---")
    for t in sorted(by.get("none", [])):
        row = tickers[t]
        allnull = all(row.get(f) is None for f in SEVEN) and row.get("returns") is None
        print("  %-6s every field NULL (returns included): %s  %s"
              % (t, allnull, json.dumps({f: row.get(f) for f in SEVEN + ["returns"]})))

    print("")
    print("--- THE SATELLITES BLOCK AGAINST THE SERVED ARTIFACT ---")
    head = s3c().head_object(Bucket=SERVED[0], Key=SERVED[1])
    served = read_json_s3(*SERVED)
    print("served VersionId=%s LastModified=%s bytes=%s"
          % (head["VersionId"], head["LastModified"], head["ContentLength"]))
    print("served  inputs triple: %s" % (triple(served),))
    print("local   inputs triple: %s" % (triple(doc),))
    if triple(served) == triple(doc):
        d = deep_equal(served.get("satellites"), doc.get("satellites"))
        print("TRIPLE UNCHANGED -> satellites block PARSE-IDENTICAL: %s" % (d is None))
        if d:
            print("FIRST DIFFERENCE: %s" % d)
    else:
        print("TRIPLE DIFFERS -> the served artifact was built from other inputs; a "
              "satellites-block comparison would not be a code comparison. STATED, not asserted.")
        d = deep_equal(served.get("satellites"), doc.get("satellites"))
        print("  (for the record, the blocks %s)" % ("are equal anyway" if d is None else "differ at " + d))

    print("")
    print("--- PEAK RSS ---")
    print("peak RSS: %s" % peak_rss_of_producer(bbg_as_of))
    return 0


def report_served(local_out: str) -> int:
    doc = json.load(open(local_out, encoding="utf-8"))
    head = s3c().head_object(Bucket=SERVED[0], Key=SERVED[1])
    served = read_json_s3(*SERVED)
    print("SERVED s3://%s/%s VersionId=%s LastModified=%s bytes=%s"
          % (SERVED[0], SERVED[1], head["VersionId"], head["LastModified"], head["ContentLength"]))
    print("served inputs triple: %s" % (triple(served),))
    print("local  inputs triple: %s  (%s)" % (triple(doc), local_out))
    st = served.get("tickers") or {}
    lt = doc.get("tickers") or {}
    print("served tickers: %d | local tickers: %d" % (len(st), len(lt)))
    print("served identity pair present (both fields non-null): %d of %d"
          % (sum(1 for r in st.values()
                 if r.get("name") is not None and r.get("management_style") is not None), len(st)))
    print("method.tickers_block served: %s" % json.dumps((served.get("method") or {}).get("tickers_block")))
    if triple(served) == triple(doc):
        d = deep_equal(st, lt)
        print("TRIPLE EQUAL -> tickers block DEEP-EQUAL: %s" % (d is None))
        if d:
            print("FIRST DIFFERENCE: %s" % d)
    else:
        d = deep_equal(st, lt)
        print("TRIPLE DIFFERS -> stated, not asserted. tickers blocks %s"
              % ("equal anyway" if d is None else "differ at " + d))

    if os.path.exists(PRE_DEPLOY_SERVED):
        pre = json.load(open(PRE_DEPLOY_SERVED, encoding="utf-8"))
        print("pre-deploy served triple: %s (%s)" % (triple(pre), PRE_DEPLOY_SERVED))
        if triple(pre) == triple(served):
            d = deep_equal(pre.get("satellites"), served.get("satellites"))
            print("TRIPLE UNCHANGED vs PRE-DEPLOY -> satellites block EQUAL: %s" % (d is None))
            if d:
                print("FIRST DIFFERENCE: %s" % d)
        else:
            d = deep_equal(pre.get("satellites"), served.get("satellites"))
            print("TRIPLE DIFFERS vs PRE-DEPLOY -> stated. satellites blocks %s"
                  % ("equal anyway" if d is None else "differ at " + d))
    else:
        print("PRE-DEPLOY COPY ABSENT at %s -- the satellites comparison cannot be made"
              % PRE_DEPLOY_SERVED)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="W1-AC4 / W1-AC12 tickers-block reader")
    ap.add_argument("local_out", nargs="?", default=LOCAL_OUT_DEFAULT)
    ap.add_argument("--served", action="store_true", help="W1-AC12: read the SERVED artifact")
    a = ap.parse_args()
    path = native(a.local_out)
    return report_served(path) if a.served else report_local(path)


if __name__ == "__main__":
    raise SystemExit(main())
