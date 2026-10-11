"""AMGT_RESAPP round-94 PREP -- the CTO's census (round-93 analysis item 1): every served subject whose display name differs from its crosswalk company.

  PYTHONPATH=<repo root> python r94_name_census.py [--where deployed|local]

For each of the 243 MEASURED crosswalk subjects the name the page serves (`--where deployed`: the live function's `/overlay` `display_name`; `--where local`: the
checkout's own overlay name path, `scoped_amgt._overlay_name`) is compared with the crosswalk's registered company name. The two AGREE when their cleaned name tokens
(`numeric_tickers.name_token`, legal endings stripped, then the generic words com, stk, cl, class, cos, holdings, holding, group, del, new, and, corp, co, inc, ltd
dropped) share at least one token of two or more letters; a pair that shares none is a DIFFERENT COMPANY.
    C1 the count of subjects whose served name is a different company from the registered one: must be 0 (the base reads 2: SAN_FP_Equity served as
       'Banco Santander S.A.' and CSL_AU_Equity served as 'Carlisle Cos Inc', both bare-ticker collisions in the classifications table).
    C2 control: the denominator is printed: 243 subjects; each judged against EVERY reference name it has -- the crosswalk's registered identity name, the
       record's `legal_name.value` where its status is MEASURED, the record's research folder name (`source_row.folder`, e.g. 'Sanofi SAN FP'), and the key's
       own model-block header NAME (`scoped_amgt._model_block_names`); a served name is a DIFFERENT company only when it shares no token with ANY of them;
       a subject with no reference at all is UNJUDGED (a count, not a pass); the spelling variants (the names differ, the company is the same) are LISTED,
       not counted as defects.
    C3 (round 94 amendment 1) the ranked lists: for each `/lead-panel/rankings/{movement}/{subject}` (`scoped_amgt.MOVEMENTS` x `SUBJECTS`) every row that carries
       a `name` and a `security_key` the crosswalk registers a name for is judged by the same token rule against that registered name; a row whose name is a
       different company is counted (the base reads 2: row `SAN_FP_Equity` of TRENDING/PRICE and of BREAKOUT/PRICE, 'Banco Santander S.A.'). The list's row
       count and the rows judged are printed beside the number.
    C4 (round 94 amendment 3) the rank timeseries: for each ranked list's tickers, `/lead-panel/timeseries/{movement}/{subject}?tickers=...` serves a `name` per
       series from the table by bare ticker; a series whose ticker matches a covered security key (`scoped_amgt._covered_bloomberg_index`, the exact match the
       ranked join uses) that has a registered name is judged by the same token rule. The base reads 2: SAN FP in TRENDING/PRICE and BREAKOUT/PRICE ('Banco
       Santander S.A. ADR').
Verdict: R94 NAME CENSUS: YES|NO (exit 0|1) -- YES only when C1, C3 and C4 all read 0 with a non-zero denominator.
"""
import argparse
import json
import sys

import boto3

from lib.research.api import scoped_amgt
from lib.research.identity import crosswalk
from lib.research.peers import numeric_tickers

FN = "opal-amgt-scoped-api"
PREFIX = "/api/scoped/amgt"
GENERIC = {"com", "stk", "cl", "class", "cos", "holdings", "holding", "group", "del", "new", "and", "corp", "co", "inc", "ltd"}
_LAM = boto3.client("lambda", region_name="us-east-1")


def tokens(name):
    return {t for t in numeric_tickers.name_token(name).split() if len(t) >= 2 and t not in GENERIC}


def served_deployed(key):
    event = {"rawPath": "%s/security/%s/overlay" % (PREFIX, key), "queryStringParameters": None,
             "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"}}
    r = json.loads(_LAM.invoke(FunctionName=FN, Payload=json.dumps(event).encode())["Payload"].read())
    return (json.loads(r.get("body") or "{}")).get("display_name")


def ranked_rows(where):
    """[(combo, security_key, name)] for every row of every ranked list, from the live function or the checkout's own handler."""
    out, sizes, tickers_by_combo = [], {}, {}
    for movement in scoped_amgt.MOVEMENTS:
        for subject in scoped_amgt.SUBJECTS:
            event = {"rawPath": "%s/lead-panel/rankings/%s/%s" % (PREFIX, movement, subject), "queryStringParameters": None,
                     "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"}}
            if where == "deployed":
                r = json.loads(_LAM.invoke(FunctionName=FN, Payload=json.dumps(event).encode())["Payload"].read())
            else:
                r = scoped_amgt.handler(event)
            rows = (json.loads(r.get("body") or "{}")).get("rows") or []
            sizes["%s/%s" % (movement, subject)] = len(rows)
            tickers_by_combo[(movement, subject)] = [row.get("ticker") for row in rows if row.get("ticker")]
            for row in rows:
                out.append(("%s/%s" % (movement, subject), row.get("security_key"), row.get("name")))
    return out, sizes, tickers_by_combo


def series_names(where, tickers_by_combo):
    """[(combo, ticker, name)] of every series of every rank timeseries read for the tickers a ranked list holds."""
    out = []
    for (movement, subject), tickers in sorted(tickers_by_combo.items()):
        if not tickers:
            continue
        event = {"rawPath": "%s/lead-panel/timeseries/%s/%s" % (PREFIX, movement, subject),
                 "queryStringParameters": {"tickers": ",".join(tickers)},
                 "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"}}
        if where == "deployed":
            r = json.loads(_LAM.invoke(FunctionName=FN, Payload=json.dumps(event).encode())["Payload"].read())
        else:
            r = scoped_amgt.handler(event)
        for series in (json.loads(r.get("body") or "{}")).get("series") or []:
            out.append(("%s/%s" % (movement, subject), series.get("ticker"), series.get("name")))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--where", default="deployed", choices=["deployed", "local"])
    args = ap.parse_args()
    doc, _i, _a = crosswalk.load_crosswalk()
    keys = [r["security_key"] for r in doc["records"] if r.get("resolution") == "MEASURED" and r.get("security_key")]
    registered = scoped_amgt._crosswalk_names()
    if args.where == "local":
        # the name the page HEADER serves: the overlay's own name path (`_overlay_name`), not the chatter chain (round 94 amendment 1)
        served = {}
        for k in keys:
            ident = scoped_amgt.resolve_identity(k) or {}
            served[k] = scoped_amgt._overlay_name(ident, k, ident.get("bloomberg")).get("display_name")
    else:
        served = {k: served_deployed(k) for k in keys}
    records = {r["security_key"]: r for r in doc["records"] if r.get("security_key")}
    block = {}
    for i in range(0, len(keys), 8):
        block.update(scoped_amgt._model_block_names(keys[i:i + 8]))
    judged = wrong = unjudged = 0
    by_source = {"registered": 0, "legal_name": 0, "folder": 0, "model block": 0}
    variants, different = [], []
    for k in keys:
        name = served.get(k)
        rec = records.get(k) or {}
        legal = rec.get("legal_name") if isinstance(rec.get("legal_name"), dict) else {}
        refs = [("registered", registered.get(k)),
                ("legal_name", legal.get("value") if legal.get("status") == "MEASURED" else None),
                ("folder", (rec.get("source_row") or {}).get("folder")),
                ("model block", block.get(k))]
        refs = [(src, str(v).strip()) for src, v in refs if v and str(v).strip()]
        if not refs or not name:
            unjudged += 1
            continue
        judged += 1
        for src, _v in refs:
            by_source[src] += 1
        cleans = [scoped_amgt._clean_display_name(v) for _src, v in refs]
        if any(str(name).strip().lower() == str(c).strip().lower() for c in cleans):
            continue
        if any(tokens(name) & tokens(c) for c in cleans):
            variants.append((k, name, refs[0][1]))
        else:
            wrong += 1
            different.append((k, name, "; ".join("%s=%r" % r for r in refs)))
    print("   where=%s subjects %d | judged %d (references held: %s) | UNJUDGED (no reference name at all) %d | same company, names differ "
          "(spelling variants) %d | DIFFERENT company %d" % (args.where, len(keys), judged,
                                                           ", ".join("%s %d" % kv for kv in by_source.items()), unjudged, len(variants), wrong))
    for v in variants:
        print("   variant   %-18s served=%r registered=%r" % v)
    for d in different:
        print("   DIFFERENT %-18s served=%r registered=%r" % d)
    ok = wrong == 0 and judged > 0
    print("%s C1 no served subject name is another company's (%d)" % ("PASS" if ok else "FAIL", wrong))
    rows, sizes, tickers_by_combo = ranked_rows(args.where)
    r_judged, r_wrong = 0, []
    for combo, key, name in rows:
        reg = registered.get(key)
        if not (key and name and reg):
            continue
        r_judged += 1
        clean = scoped_amgt._clean_display_name(reg)
        if str(name).strip().lower() == str(clean).strip().lower() or tokens(name) & tokens(clean) or tokens(name) & tokens(reg):
            continue
        r_wrong.append((combo, key, name, reg))
    print("   ranked lists (%s): rows %d across %d lists (%s) | judged against a registered name %d | DIFFERENT company %d" % (
        args.where, len(rows), len(sizes), ", ".join("%s %d" % kv for kv in sorted(sizes.items())), r_judged, len(r_wrong)))
    for w in r_wrong:
        print("   DIFFERENT row %-18s %-16s served=%r registered=%r" % (w[1], w[0], w[2], w[3]))
    ranked_ok = len(r_wrong) == 0 and r_judged > 0
    print("%s C3 no ranked row's name is another company's (%d of %d judged)" % ("PASS" if ranked_ok else "FAIL", len(r_wrong), r_judged))
    ok = ok and ranked_ok
    index = scoped_amgt._covered_bloomberg_index()
    s_rows = series_names(args.where, tickers_by_combo)
    s_judged, s_wrong = 0, []
    for combo, ticker, name in s_rows:
        reg = registered.get(index.get(ticker))
        if not (name and reg):
            continue
        s_judged += 1
        clean = scoped_amgt._clean_display_name(reg)
        if str(name).strip().lower() == str(clean).strip().lower() or tokens(name) & tokens(clean) or tokens(name) & tokens(reg):
            continue
        s_wrong.append((combo, ticker, name, reg))
    print("   rank timeseries (%s): series %d | judged against a registered name %d | DIFFERENT company %d" % (
        args.where, len(s_rows), s_judged, len(s_wrong)))
    for w in s_wrong:
        print("   DIFFERENT series %-10s %-16s served=%r registered=%r" % (w[1], w[0], w[2], w[3]))
    series_ok = len(s_wrong) == 0 and s_judged > 0
    print("%s C4 no rank series name is another company's (%d of %d judged)" % ("PASS" if series_ok else "FAIL", len(s_wrong), s_judged))
    ok = ok and series_ok
    print("R94 NAME CENSUS: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
