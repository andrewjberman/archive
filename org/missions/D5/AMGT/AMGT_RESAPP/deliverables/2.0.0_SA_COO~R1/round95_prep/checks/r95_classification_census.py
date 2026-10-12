"""AMGT_RESAPP round-95 PREP -- no field of a disagreeing table row is served (row D1-S26, CTO round-94 analysis item 2).

  PYTHONPATH=<repo root> python r95_classification_census.py [--where deployed|local]

The classifications table is keyed by the BARE Bloomberg ticker, and `CSL` is Carlisle (name 'Carlisle Cos Inc', sub-asset class 'US Large Cap') while the security
is CSL Ltd (CSL_AU_Equity); `SAN` is a row whose name is 'Banco Santander S.A. ADR' under Sanofi's ticker. Round 94 made the NAME the registered company's; the same
row's classification is still served for the security. The rule: when the table row's name DISAGREES with the registered name (`names_read.names_disagree`, the ff-1
test), no field of that row is served for the security: `classification` is null and `sector` is null, with the plain reason
"classification not available for this listing" (ranked row: `sector_reason`; rank series and collected-chatter row: `classification_reason`).

For every MEASURED crosswalk subject the table row of its bare ticker is read (DynamoDB GetItem, read-only); D is the set whose row disagrees (the base reads 2:
SAN_FP_Equity and CSL_AU_Equity). Then, over the live function (`--where deployed`) or the checkout's handler (`--where local`):
    K1 every ranked row (the four lists) of a D subject serves `classification` null, `sector` null and a `sector_reason` that says the classification is not available
       for this listing (the base serves SAN FP's row 67 'Health Care' in both PRICE lists).
    K2 every rank series of a D ticker serves `classification` null and a `classification_reason` of the same words (the base serves 'Health Care' for SAN FP and 'US
       Large Cap' for CSL AU).
    K3 every collected-chatter row of a D ticker (days = 30, 90, 365) serves `classification` null and a `classification_reason` of the same words.
    K4 the per-security routes of each D subject (overlay, thesis, peers, coverage, compare, timeline) carry no non-null `classification`, `sector`, `sub_asset_class` or
       `asset_class` outside their peers' members (which carry their own companies' sectors); the base serves none, so K4 is a no-regression guard.
    K5 control: every ranked row and rank series of a NON-D subject serves the table row's own classification unchanged (the count judged is printed; 0 differ).
    K6 (round 95 amendment 2) every disagreeing ticker ASKED FOR BY TICKER on the rank timeseries (`/lead-panel/timeseries/TRENDING/PRICE?tickers=<ticker>`), whether or not a
       ranked list holds it and whether or not the covered universe holds it, serves its series with `classification` null, a `classification_reason` of the same words and a
       `name` that is not the table row's (CSL_AU_Equity is a measured subject outside the covered universe: its series read 'Carlisle Cos Inc' and 'US Large Cap' there).
The table rows of the D tickers are printed whole (name, asset_class, sub_asset_class, classified_by, last_updated, updated_by) beside the registered name, so a reader
can see which fields of a disagreeing row were the security's own (SAN's 'Health Care' is a legacy classification under another company's cleaned name).
ROUND 96 (`AMGT-bc-2`): the arms K1-K3 and K6 read "no field of the TABLE row is served", which a withheld listing satisfies by a null classification with the reason OR by its own
model-block sector (null asset_class and sub_asset_class, the source named); `r96_sector_serve_census.py` asserts the latter.
Verdict: R95 CLASSIFICATION CENSUS: YES|NO (exit 0|1). At the base (2026-10-11): K1, K2, K3, K6 FAIL, K4 and K5 PASS (no per-security route carries a subject classification today: a guard).
"""
import argparse
import json
import sys

import boto3

from lib.research.api import names_read, scoped_amgt
from lib.research.identity import crosswalk

FN = "opal-amgt-scoped-api"
PREFIX = scoped_amgt.ROUTE_PREFIX
PLAIN = "not available for this listing"
FIELDS = ("classification", "sector", "sub_asset_class", "asset_class")
_LAM = boto3.client("lambda", region_name="us-east-1")


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


def scan(node, path=""):
    """Every (path, value) of a non-null classification field anywhere in a payload."""
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


def reason_ok(text):
    return PLAIN in str(text or "").lower()


def no_table_field(cls, reason):
    """No field of the TABLE row is served: the classification is null with the plain reason, OR (round 96 `AMGT-bc-2`) it is the listing's own model-block sector with
    `asset_class` and `sub_asset_class` null and no reason; the table's sub-asset class or sector never appears."""
    if cls is None:
        return reason_ok(reason)
    return (isinstance(cls, dict) and cls.get("asset_class") is None and cls.get("sub_asset_class") is None
            and "model_block" in str(cls.get("sector_source") or "") and not reason)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--where", default="deployed", choices=["deployed", "local"])
    where = ap.parse_args().where
    doc, _i, _a = crosswalk.load_crosswalk()
    keys = [r["security_key"] for r in doc["records"] if r.get("resolution") == "MEASURED" and r.get("security_key")]
    registered = scoped_amgt._crosswalk_names()
    index = scoped_amgt._covered_bloomberg_index()
    ticker_of = {}
    for t, k in index.items():
        ticker_of[k] = t
    disagree, rows_by_key = {}, {}
    for k in keys:
        ticker = ticker_of.get(k) or (scoped_amgt.resolve_identity(k) or {}).get("bloomberg")
        if not ticker:
            continue
        row = scoped_amgt._classification_for_ticker(ticker) or {}
        rows_by_key[k] = (ticker, row)
        if names_read.names_disagree(row.get("name"), registered.get(k), ticker):
            disagree[k] = ticker
    print("   where=%s subjects %d | table rows read %d | disagreeing table rows %d: %s" % (where, len(keys), len(rows_by_key), len(disagree),
                                                                                      ", ".join(sorted(disagree))))
    table = boto3.resource("dynamodb", region_name="us-east-1").Table("etf-classifications")
    for k, t in sorted(disagree.items()):
        item = table.get_item(Key={"ticker": t.split(" ")[0]}).get("Item") or {}
        print("   ROW %-14s ticker %-8s registered %r | table name %r asset_class %r sub_asset_class %r classified_by %r last_updated %r updated_by %r" % (
            k, t, registered.get(k), item.get("name"), item.get("asset_class"), item.get("sub_asset_class"), item.get("classified_by"),
            item.get("last_updated"), item.get("updated_by")))
    res = []
    d_tickers = set(disagree.values())
    # ranked lists and the rank series of every listed ticker
    bad_rows, ok_rows, ctl_rows, ctl_diff, bad_series, ok_series, ctl_series, ctl_series_diff = [], 0, 0, [], [], 0, 0, []
    for movement in scoped_amgt.MOVEMENTS:
        for subject in scoped_amgt.SUBJECTS:
            ranked = serve(where, "/lead-panel/rankings/%s/%s" % (movement, subject))
            rows = ranked.get("rows") or []
            for row in rows:
                tkr = row.get("ticker")
                key = row.get("security_key") or index.get(tkr)
                if tkr in d_tickers or key in disagree:
                    # round 97 (`AMGT-bd-1`): the row's own LISTING sector may ride beside the withheld classification (`sector_source` 'Bloomberg, listing', `sector_reason` null);
                    # what must never appear is the TABLE row's: a classification object from the table, or a sector with no listing source.
                    from_listing = row.get("sector_source") == "Bloomberg, listing" and row.get("sector") and row.get("sector_reason") is None
                    if row.get("classification") is None and (from_listing or (row.get("sector") is None and reason_ok(row.get("sector_reason")))):
                        ok_rows += 1
                    else:
                        bad_rows.append((movement + "/" + subject, tkr, (row.get("classification") or {}).get("sub_asset_class"), row.get("sector_reason")))
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
                        if no_table_field(s.get("classification"), s.get("classification_reason")):
                            ok_series += 1
                        else:
                            bad_series.append((movement + "/" + subject, tkr, (s.get("classification") or {}).get("sub_asset_class")))
                    else:
                        table_row = scoped_amgt._classification_for_ticker(tkr) or {}  # the series route asks by ticker alone, as this does
                        ctl_series += 1
                        if (s.get("classification") or None) != (table_row.get("classification") or None):
                            ctl_series_diff.append((movement + "/" + subject, tkr))
    res.append(say(not bad_rows and ok_rows > 0, "K1 every ranked row of a disagreeing subject withholds the classification and says why",
                   "withheld %d, still served %s" % (ok_rows, bad_rows[:4])))
    res.append(say(not bad_series and ok_series > 0, "K2 every rank series of a disagreeing ticker withholds the classification and says why",
                   "withheld %d, still served %s" % (ok_series, bad_series[:4])))
    # collected chatter rows
    chat_bad, chat_ok = [], 0
    for days in ("30", "90", "365"):
        body = serve(where, "/lead-panel/timeseries/collected/chatter", {"days": days})
        for row in body.get("rows") or []:
            tkr = row.get("ticker")
            if tkr in d_tickers:
                if no_table_field(row.get("classification"), row.get("classification_reason")):
                    chat_ok += 1
                else:
                    chat_bad.append((days, tkr, (row.get("classification") or {}).get("sub_asset_class")))
    res.append(say(not chat_bad and chat_ok > 0, "K3 every collected-chatter row of a disagreeing ticker withholds the classification and says why",
                   "withheld %d, still served %s" % (chat_ok, chat_bad[:4])))
    over_bad = []
    for k in sorted(disagree):
        # the peers' members carry their OWN companies' sectors; only the subject's fields are judged
        for leaf in ("overlay", "thesis", "peers", "coverage", "compare", "timeline"):
            found = [(p, v) for p, v in scan(serve(where, "/security/%s/%s" % (k, leaf))) if ".members[" not in p]
            over_bad += [(k, leaf, p, str(v)[:40]) for p, v in found]
    res.append(say(not over_bad, "K4 no per-security route of a disagreeing subject carries a classification field", "found %s" % over_bad[:4]))
    res.append(say(ctl_rows > 0 and not ctl_diff and not ctl_series_diff,
                   "K5 control: a non-disagreeing subject's classification is the table row's own, unchanged",
                   "ranked rows judged %d differ %d; series judged %d differ %d" % (ctl_rows, len(ctl_diff), ctl_series, len(ctl_series_diff))))
    asked_bad = []
    for k, t in sorted(disagree.items()):
        body = serve(where, "/lead-panel/timeseries/TRENDING/PRICE", {"tickers": t})
        series = next((x for x in (body.get("series") or []) if x.get("ticker") == t), None)
        table_name = (rows_by_key.get(k) or (t, {}))[1].get("name")
        if (series is None or not no_table_field(series.get("classification"), series.get("classification_reason"))
                or str(series.get("name")) == str(table_name)):
            asked_bad.append((k, t, (series or {}).get("name"), ((series or {}).get("classification") or {}).get("sub_asset_class")))
    res.append(say(not asked_bad and bool(disagree), "K6 every disagreeing ticker asked for by ticker serves no table row's name or classification",
                   "asked %d, still served %s" % (len(disagree), asked_bad)))
    print("   arms passed %d of %d" % (sum(1 for r in res if r), len(res)))
    ok = all(res)
    print("R95 CLASSIFICATION CENSUS: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
