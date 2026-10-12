"""AMGT_RESAPP round-96 PREP -- a withheld listing's sector is served from its OWN stored model block, with its source named (CTO round-95 analysis item 1, after `bc-1`
read SECTOR-SERVED).

  PYTHONPATH=<repo root> python r96_sector_serve_census.py [--where deployed|local]

Round 95 made the page say "classification not available for this listing" for a security whose classifications-table row names another company (`SAN_FP_Equity`,
`CSL_AU_Equity`). `bc-1` read that the listing's own stored model block (`derived/model_block/<key>/<newest>/model_block.json`, `figures[]` record `GICS_SECTOR_NAME`, source
bloomberg-dapi) carries 'Health Care' for both. The rule: when the table row is withheld, the row's `sector` is the listing's own GICS sector from that block, and the
`classification` object names it: `sector` the value, `sector_source` 'model_block.GICS_SECTOR_NAME', `sector_as_of` the block's vintage; `asset_class` and `sub_asset_class` stay
null (they are not claimed); `sector_reason` / `classification_reason` null. A listing whose block holds no `GICS_SECTOR_NAME` stays withheld with the round-95 reason.

For every MEASURED crosswalk subject the table row of its bare ticker is read (as `r95_classification_census.py`); D is the set whose row disagrees (2: SAN_FP_Equity,
CSL_AU_Equity). EXPECTED(k) is the newest stored model block's `GICS_SECTOR_NAME` value, read straight from S3 by this script (the instrument is independent of the code). Then,
over the live function (`--where deployed`) or the checkout's handler (`--where local`):
    K1 every ranked row of a D subject serves `sector` EXPECTED, `sector_reason` null and a `classification` whose `sector_source` names the model block.
    K2 every rank series of a D ticker (listed) serves `classification.sector` EXPECTED with the same source and a null `classification_reason`.
    K3 every collected-chatter row of a D ticker (days 30, 90, 365) serves the same.
    K4 every D ticker ASKED FOR BY TICKER on the rank timeseries (listed or not, covered or not) serves `classification.sector` EXPECTED and a `name` that is not the table row's.
    K5 control: every ranked row and rank series of a NON-D subject serves the table row's own classification unchanged (the count judged is printed; 0 differ).
    K6 the overlay and the other per-security routes of a D subject still carry no classification field outside the peers' members (the guard of round 95).
Verdict: R96 SECTOR SERVE CENSUS: YES|NO (exit 0|1). At the base (live TmeKvn83, 2026-10-11): K1-K4 FAIL (withheld), K5 and K6 PASS.
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


def served_from_block(cls, expected):
    return isinstance(cls, dict) and cls.get("sector") == expected and "model_block" in str(cls.get("sector_source") or "")


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
                    exp = expected.get(key or d_tickers.get(tkr))[0]
                    if exp and row.get("sector") == exp and row.get("sector_reason") is None and served_from_block(row.get("classification"), exp):
                        ok_rows += 1
                    else:
                        bad_rows.append((movement + "/" + subject, tkr, row.get("sector"), row.get("sector_reason")))
                else:
                    table_row = scoped_amgt._classification_for_ticker(tkr, key) or {}
                    ctl_rows += 1
                    if (row.get("classification") or None) != (table_row.get("classification") or None):
                        ctl_diff.append((movement + "/" + subject, tkr))
            tickers = [r.get("ticker") for r in rows if r.get("ticker")]
            if tickers:
                ts = serve(where, "/lead-panel/timeseries/%s/%s" % (movement, subject), {"tickers": ",".join(tickers)})
                for s in ts.get("series") or []:
                    tkr = s.get("ticker")
                    if tkr in d_tickers:
                        exp = expected[d_tickers[tkr]][0]
                        if exp and served_from_block(s.get("classification"), exp) and s.get("classification_reason") is None:
                            ok_series += 1
                        else:
                            bad_series.append((movement + "/" + subject, tkr, s.get("classification")))
                    else:
                        table_row = scoped_amgt._classification_for_ticker(tkr) or {}
                        ctl_series += 1
                        if (s.get("classification") or None) != (table_row.get("classification") or None):
                            ctl_series_diff.append((movement + "/" + subject, tkr))
    res.append(say(not bad_rows and ok_rows > 0, "K1 every ranked row of a withheld listing serves its own model block's sector with the source named",
                   "served %d, not %s" % (ok_rows, bad_rows[:3])))
    res.append(say(not bad_series and ok_series > 0, "K2 every rank series of a withheld ticker serves its own model block's sector with the source named",
                   "served %d, not %s" % (ok_series, bad_series[:3])))
    chat_bad, chat_ok = [], 0
    for days in ("30", "90", "365"):
        body = serve(where, "/lead-panel/timeseries/collected/chatter", {"days": days})
        for row in body.get("rows") or []:
            tkr = row.get("ticker")
            if tkr in d_tickers:
                exp = expected[d_tickers[tkr]][0]
                if exp and served_from_block(row.get("classification"), exp) and row.get("classification_reason") is None:
                    chat_ok += 1
                else:
                    chat_bad.append((days, tkr, row.get("classification")))
    res.append(say(not chat_bad and chat_ok > 0, "K3 every collected-chatter row of a withheld ticker serves its own model block's sector with the source named",
                   "served %d, not %s" % (chat_ok, chat_bad[:3])))
    asked_bad = []
    for k, t in sorted(disagree.items()):
        body = serve(where, "/lead-panel/timeseries/TRENDING/PRICE", {"tickers": t})
        series = next((x for x in (body.get("series") or []) if x.get("ticker") == t), None)
        table_name = (rows_by_key.get(k) or (t, {}))[1].get("name")
        exp = expected[k][0]
        if series is None or not exp or not served_from_block(series.get("classification"), exp) or str(series.get("name")) == str(table_name):
            asked_bad.append((k, t, (series or {}).get("name"), (series or {}).get("classification")))
    res.append(say(not asked_bad and bool(disagree), "K4 every withheld ticker asked for by ticker serves its own sector and not the table row's name",
                   "asked %d, not %s" % (len(disagree), asked_bad)))
    res.append(say(ctl_rows > 0 and not ctl_diff and not ctl_series_diff,
                   "K5 control: a non-disagreeing subject's classification is the table row's own, unchanged",
                   "ranked rows judged %d differ %d; series judged %d differ %d" % (ctl_rows, len(ctl_diff), ctl_series, len(ctl_series_diff))))
    over_bad = []
    for k in sorted(disagree):
        for leaf in ("overlay", "thesis", "peers", "coverage", "compare", "timeline"):
            over_bad += [(k, leaf, p) for p, _v in scan(serve(where, "/security/%s/%s" % (k, leaf))) if ".members[" not in p]
    res.append(say(not over_bad, "K6 no per-security route of a withheld listing carries a classification field", "found %s" % over_bad[:3]))
    print("   arms passed %d of %d" % (sum(1 for r in res if r), len(res)))
    ok = all(res)
    print("R96 SECTOR SERVE CENSUS: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
