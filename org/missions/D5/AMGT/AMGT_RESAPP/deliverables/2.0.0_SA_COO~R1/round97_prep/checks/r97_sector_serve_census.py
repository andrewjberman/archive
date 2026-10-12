"""AMGT_RESAPP round-97 PREP -- a withheld listing's sector is served BY LISTING KEY from its own stored model block, with the source and the as-of date named; the
`classification` object stays withheld (CTO round-96 analysis, after D1-S26's ruling).

  PYTHONPATH=<repo root> python r97_sector_serve_census.py [--where deployed|local]

`bc-1` (round 96) read that the listing's own stored model block (`derived/model_block/<key>/<newest>/model_block.json`, `figures[]` record `GICS_SECTOR_NAME`, source
bloomberg-dapi) carries 'Health Care' for `SAN_FP_Equity` and `CSL_AU_Equity`, the two listings whose classifications-table row names another company. The CVO's point,
adopted by the CTO: the LISTING KEY discriminates, not the value (the collided SAN row also reads Health Care), so the sector is served by key from the listing's block and never
"a matching value" from any row. The rule: where the table row is withheld (round 95), the entry also carries `sector` the value, `sector_source` 'Bloomberg, listing' and
`sector_as_of` the block's vintage DATE (YYYY-MM-DD); `classification` stays null with the round-95 `classification_reason` ('classification not available for this listing'); a ranked
row's `sector_reason` is null when its sector is served. A listing whose block holds no `GICS_SECTOR_NAME` (or whose read fails) stays withheld with no sector.

EXPECTED(k) and its as-of date are read straight from S3 by this script (the instrument is independent of the code). D is the set of subjects whose table row disagrees (2).
    K1 every ranked row of a D subject serves `sector` EXPECTED, `sector_source` 'Bloomberg, listing', `sector_as_of` the block date, `sector_reason` null, `classification` null.
    K2 every rank series of a D ticker (listed) serves the same three keys and `classification` null with `classification_reason` saying not available for this listing.
    K3 every collected-chatter row of a D ticker (days 30, 90, 365) serves the same.
    K4 every D ticker ASKED FOR BY TICKER on the rank timeseries (listed or not, covered or not) serves the same three keys, and a `name` that is not the table row's.
    K5 control: every ranked row and rank series of a NON-D subject carries NO `sector_source` / `sector_as_of` key and serves the table row's own classification unchanged
       (the count judged is printed; 0 differ).
    K6 the overlay and the other per-security routes of a D subject carry no classification field outside the peers' members (the guard of round 95).
Verdict: R97 SECTOR SERVE CENSUS: YES|NO (exit 0|1). At the base (live TmeKvn83, 2026-10-11): K1-K4 FAIL (no sector served), K5 and K6 PASS.
"""
import argparse
import json
import sys

import boto3

from lib.research.api import names_read, scoped_amgt
from lib.research.identity import crosswalk

FN = "opal-amgt-scoped-api"
PREFIX = scoped_amgt.ROUTE_PREFIX
BUCKET = "opal-data-harvest"
FIELDS = ("classification", "sector", "sub_asset_class", "asset_class")
_LAM = boto3.client("lambda", region_name="us-east-1")
_S3 = boto3.client("s3", region_name="us-east-1")


def say(ok, label, detail=""):
    print("%s %s%s" % ("PASS" if ok else "FAIL", label, ("  [" + detail + "]") if detail else ""))
    return ok


def serve(where, path, query=None):
    ev = {"rawPath": PREFIX + path, "queryStringParameters": query, "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"}}
    if where == "deployed":
        r = json.loads(_LAM.invoke(FunctionName=FN, Payload=json.dumps(ev).encode())["Payload"].read())
    else:
        r = scoped_amgt.handler(ev)
    return json.loads(r.get("body") or "{}")


def block_sector(key):
    """The newest stored model block's GICS_SECTOR_NAME value for a key, and the block's vintage stamp (the object's folder)."""
    keys = []
    for page in _S3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix="derived/model_block/%s/" % key):
        keys += [o["Key"] for o in page.get("Contents", [])]
    if not keys:
        return None, None
    newest = sorted(keys)[-1]
    doc = json.loads(_S3.get_object(Bucket=BUCKET, Key=newest)["Body"].read())

    def walk(node):
        if isinstance(node, dict):
            if str(node.get("mnemonic", "")).upper() == "GICS_SECTOR_NAME" and node.get("value"):
                yield node["value"]
            for v in node.values():
                yield from walk(v)
        elif isinstance(node, list):
            for v in node:
                yield from walk(v)
    return next(walk(doc), None), newest.split("/")[-2]


def as_date(vintage):
    """'20261011T130935Z' -> '2026-10-11'."""
    v = str(vintage or "")
    return "%s-%s-%s" % (v[0:4], v[4:6], v[6:8]) if len(v) >= 8 else None


def listing_sector_ok(entry, expected):
    """The entry serves the listing's own sector by key: sector value, source 'Bloomberg, listing' and the block's date; classification null."""
    exp, vintage = expected
    return (bool(exp) and entry.get("sector") == exp and entry.get("sector_source") == "Bloomberg, listing"
            and entry.get("sector_as_of") == as_date(vintage) and entry.get("classification") is None)


def scan(node, path=""):
    if isinstance(node, dict):
        for k, v in node.items():
            here = "%s.%s" % (path, k)
            if k in FIELDS and v not in (None, "", {}):
                yield here, v
            else:
                yield from scan(v, here)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from scan(v, "%s[%d]" % (path, i))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--where", default="deployed", choices=["deployed", "local"])
    where = ap.parse_args().where
    doc, _i, _a = crosswalk.load_crosswalk()
    keys = [r["security_key"] for r in doc["records"] if r.get("resolution") == "MEASURED" and r.get("security_key")]
    registered = scoped_amgt._crosswalk_names()
    index = scoped_amgt._covered_bloomberg_index()
    ticker_of = {k: t for t, k in index.items()}
    disagree, rows_by_key = {}, {}
    for k in keys:
        ticker = ticker_of.get(k) or (scoped_amgt.resolve_identity(k) or {}).get("bloomberg")
        if not ticker:
            continue
        row = scoped_amgt._classification_for_ticker(ticker) or {}
        rows_by_key[k] = (ticker, row)
        if names_read.names_disagree(row.get("name"), registered.get(k), ticker):
            disagree[k] = ticker
    expected = {k: block_sector(k) for k in disagree}
    print("   where=%s | disagreeing table rows %d: %s | model-block GICS_SECTOR_NAME read from S3: %s" % (
        where, len(disagree), ", ".join(sorted(disagree)), json.dumps({k: v for k, v in expected.items()})))
    res = []
    d_tickers = {t: k for k, t in disagree.items()}
    bad_rows, ok_rows, ctl_rows, ctl_diff, bad_series, ok_series, ctl_series, ctl_series_diff = [], 0, 0, [], [], 0, 0, []
    for movement in scoped_amgt.MOVEMENTS:
        for subject in scoped_amgt.SUBJECTS:
            ranked = serve(where, "/lead-panel/rankings/%s/%s" % (movement, subject))
            rows = ranked.get("rows") or []
            for row in rows:
                tkr = row.get("ticker")
                key = row.get("security_key") or index.get(tkr)
                if tkr in d_tickers or key in disagree:
                    exp = expected.get(key or d_tickers.get(tkr))
                    if listing_sector_ok(row, exp) and row.get("sector_reason") is None:
                        ok_rows += 1
                    else:
                        bad_rows.append((movement + "/" + subject, tkr, row.get("sector"), row.get("sector_reason")))
                else:
                    table_row = scoped_amgt._classification_for_ticker(tkr, key) or {}
                    ctl_rows += 1
                    if ((row.get("classification") or None) != (table_row.get("classification") or None)
                            or "sector_source" in row or "sector_as_of" in row):
                        ctl_diff.append((movement + "/" + subject, tkr))
            tickers = [r.get("ticker") for r in rows if r.get("ticker")]
            if tickers:
                ts = serve(where, "/lead-panel/timeseries/%s/%s" % (movement, subject), {"tickers": ",".join(tickers)})
                for s in ts.get("series") or []:
                    tkr = s.get("ticker")
                    if tkr in d_tickers:
                        exp = expected[d_tickers[tkr]]
                        if listing_sector_ok(s, exp) and "not available for this listing" in str(s.get("classification_reason")):
                            ok_series += 1
                        else:
                            bad_series.append((movement + "/" + subject, tkr, s.get("classification")))
                    else:
                        table_row = scoped_amgt._classification_for_ticker(tkr) or {}
                        ctl_series += 1
                        if ((s.get("classification") or None) != (table_row.get("classification") or None)
                                or "sector_source" in s or "sector_as_of" in s):
                            ctl_series_diff.append((movement + "/" + subject, tkr))
    res.append(say(not bad_rows and ok_rows > 0, "K1 every ranked row of a withheld listing serves its sector by listing key with source and as-of date",
                   "served %d, not %s" % (ok_rows, bad_rows[:3])))
    res.append(say(not bad_series and ok_series > 0, "K2 every rank series of a withheld ticker serves its sector by listing key with source and as-of date",
                   "served %d, not %s" % (ok_series, bad_series[:3])))
    chat_bad, chat_ok = [], 0
    for days in ("30", "90", "365"):
        body = serve(where, "/lead-panel/timeseries/collected/chatter", {"days": days})
        for row in body.get("rows") or []:
            tkr = row.get("ticker")
            if tkr in d_tickers:
                exp = expected[d_tickers[tkr]]
                if listing_sector_ok(row, exp) and "not available for this listing" in str(row.get("classification_reason")):
                    chat_ok += 1
                else:
                    chat_bad.append((days, tkr, row.get("sector"), row.get("classification")))
    res.append(say(not chat_bad and chat_ok > 0, "K3 every collected-chatter row of a withheld ticker serves its sector by listing key with source and as-of date",
                   "served %d, not %s" % (chat_ok, chat_bad[:3])))
    asked_bad = []
    for k, t in sorted(disagree.items()):
        body = serve(where, "/lead-panel/timeseries/TRENDING/PRICE", {"tickers": t})
        series = next((x for x in (body.get("series") or []) if x.get("ticker") == t), None)
        table_name = (rows_by_key.get(k) or (t, {}))[1].get("name")
        if series is None or not listing_sector_ok(series, expected[k]) or str(series.get("name")) == str(table_name):
            asked_bad.append((k, t, (series or {}).get("name"), (series or {}).get("sector")))
    res.append(say(not asked_bad and bool(disagree), "K4 every withheld ticker asked for by ticker serves its sector by listing key and not the table row's name",
                   "asked %d, not %s" % (len(disagree), asked_bad)))
    res.append(say(ctl_rows > 0 and not ctl_diff and not ctl_series_diff,
                   "K5 control: a non-disagreeing subject carries no sector key of this rule and its classification is the table row's own",
                   "ranked rows judged %d differ %d; series judged %d differ %d" % (ctl_rows, len(ctl_diff), ctl_series, len(ctl_series_diff))))
    over_bad = []
    for k in sorted(disagree):
        for leaf in ("overlay", "thesis", "peers", "coverage", "compare", "timeline"):
            over_bad += [(k, leaf, p) for p, _v in scan(serve(where, "/security/%s/%s" % (k, leaf))) if ".members[" not in p]
    res.append(say(not over_bad, "K6 no per-security route of a withheld listing carries a classification field", "found %s" % over_bad[:3]))
    print("   arms passed %d of %d" % (sum(1 for r in res if r), len(res)))
    ok = all(res)
    print("R97 SECTOR SERVE CENSUS: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
