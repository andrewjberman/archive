"""AMGT_RESAPP round 78 -- READ: filing coverage (CTO round-78 ruling, "What the two counts of section A change").

  python r78_read_filing_coverage.py [--write <folder>]

A READ. No build, no store write, no SEC or vendor call. It makes:
  - one GET-shaped direct invoke of the deployed function's /thesis route per covered name (the page's own stated
    reason splits the names with no filing analysis into "no cik" and "no drafted document");
  - S3 reads of opal-data-harvest: the pool list (crosswalk/v1/<newest>.json), every universe vintage under
    universe/v1/, the identity bronze, the stored SEC ticker table, the filing-attempt state markers, the two
    filing_source silver tables, the old filings/v1/ prefix and drafting/v1/;
  - one local read of lib/research/identity/registrations.json.

PART A, the names whose page reads "no cik": per name, every stored place that holds a company number (CIK), and what
the filing step's own planner (lib.research.filings.batch.plan, a pure function) decides for that name on the NEWEST
stored universe. Classes:
  CIK_IN_NEWEST_UNIVERSE      the newest universe row carries source edgar and a cik: the served "no cik" reason is
                              an old marker, written from an older universe and never re-written;
  CIK_STORED_NOT_IN_UNIVERSE  a CIK is stored (pool list, registrations, identity bronze, or the SEC ticker table
                              for a US listing) but the newest universe row carries none, so the planner cannot see it;
  ASKED_BLOOMBERG_NO_CIK      no stored place holds a CIK; Bloomberg was asked (an identity bronze object exists) and
                              returned none;
  NEVER_ASKED                 no stored place holds a CIK and no identity bronze object exists for the name.
PART B, the names whose page reads "no drafted document": the first pipeline stage with no stored object. Stages, in
the order the code runs them (build_universe.filing_identity_for, then batch.plan and batch.run_group):
  S1 CIK        the newest universe row carries source edgar and a cik;
  S2 FORM       that row's form_expected is a form (10-K, 20-F, 40-F), not the text "none";
  S3 SOURCE     a RESOLVED source object is stored (filing_source silver, or the old filings/v1 *.source.json);
  S4 ANALYSIS   filings/v1/<name>/<accession>.analysis.json;
  S5 DRAFT      drafting/v1/<name>.json.
Verdict: R78 READ FILING COVERAGE: DONE (exit 0) when every name of both parts falls in exactly one class.
"""
from __future__ import annotations

import argparse
import collections
import io
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor

FN = "opal-amgt-scoped-api"
PREFIX = "/api/scoped/amgt"
BUCKET = "opal-data-harvest"
REGISTRATIONS = "lib/research/identity/registrations.json"
SILVER_PREFIXES = ("sec/harvest/silver/filing_source/", "issuer-site/harvest/silver/filing_source/")
STATE_PREFIX = "amgt/harvest/state/filing_attempt/"
IDENTITY_BRONZE = "bloomberg/harvest/bronze/identity/"
SEC_TABLE_PREFIX = "sec/harvest/bronze/company_tickers/"
A_CLASSES = ("CIK_IN_NEWEST_UNIVERSE", "CIK_STORED_NOT_IN_UNIVERSE", "ASKED_BLOOMBERG_NO_CIK", "NEVER_ASKED")
B_STAGES = ("S1 CIK", "S2 FORM", "S3 SOURCE", "S4 ANALYSIS", "S5 DRAFT")
FORMS = ("10-K", "20-F", "40-F")


def _event(path):
    return {"rawPath": path, "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"},
            "queryStringParameters": None}


def _list(s3, prefix):
    out = []
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=prefix):
        out += page.get("Contents", []) or []
    return out


def _get_json(s3, key):
    return json.loads(s3.get_object(Bucket=BUCKET, Key=key)["Body"].read().decode("utf-8"))


def _stamp(obj):
    return obj["LastModified"].strftime("%Y-%m-%dT%H:%MZ")


def served_reason(key, lam):
    raw = json.loads(lam.invoke(FunctionName=FN, Payload=json.dumps(
        _event("%s/security/%s/thesis" % (PREFIX, key))).encode())["Payload"].read())
    try:
        body = json.loads(raw.get("body") or "{}")
    except (ValueError, TypeError):
        body = {}
    return {"status_code": raw.get("statusCode"), "drafting_status": body.get("drafting_status"),
            "drafting_reason": " ".join(str(body.get("drafting_reason") or "").split()),
            "held": body.get("drafting_reason_held") is True,
            "newer_reason": body.get("drafting_reason_newer")}


def _int_cik(value):
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return None


def read_everything():
    import boto3
    import pyarrow.parquet as pq

    from lib.research.coverage import covered_universe
    from lib.research.filings import batch
    from lib.research.identity import crosswalk

    s3 = boto3.client("s3", region_name="us-east-1")
    lam = boto3.client("lambda", region_name="us-east-1")
    covered = sorted(covered_universe.covered_security_keys())

    with ThreadPoolExecutor(max_workers=8) as pool:
        served = dict(zip(covered, pool.map(lambda k: served_reason(k, lam), covered)))

    crosswalk_keys = sorted(o["Key"] for o in _list(s3, "crosswalk/v1/") if o["Key"].endswith(".json"))
    pool_doc = _get_json(s3, crosswalk_keys[-1])
    pool_by_key = {r["security_key"]: r for r in pool_doc["records"]}

    with open(REGISTRATIONS, encoding="utf-8") as fh:
        registrations = {r["security_key"]: r for r in json.load(fh)["registrations"] if r.get("security_key")}

    universe_keys = sorted(o["Key"] for o in _list(s3, "universe/v1/") if o["Key"].endswith(".json"))
    universes = {k: _get_json(s3, k) for k in universe_keys}
    newest_universe_key = universe_keys[-1]
    newest = universes[newest_universe_key]
    plans = {}
    for ukey, doc in universes.items():
        planned = batch.plan(doc)
        fetchable = {}
        for group in planned["fetch_groups"]:
            for member in group["security_keys"]:
                fetchable[member] = {"cik": group["cik"], "form_expected": group["form_expected"]}
        plans[ukey] = fetchable
    rows_by_universe = {ukey: {r.get("security_key"): r for r in doc["names"] if r.get("security_key")}
                        for ukey, doc in universes.items()}

    sec_objects = sorted(o["Key"] for o in _list(s3, SEC_TABLE_PREFIX) if o["Key"].endswith(".json"))
    sec_table_key = sec_objects[-1]
    sec_raw = _get_json(s3, sec_table_key)
    sec_by_ticker = {}
    for entry in sec_raw.values():
        ticker = str(entry.get("ticker") or "").upper()
        if ticker and ticker not in sec_by_ticker:
            sec_by_ticker[ticker] = {"cik": entry.get("cik_str"), "title": entry.get("title")}
    other_identity = [o["Key"] for o in _list(s3, "identity/")]
    other_sec = [o["Key"] for o in _list(s3, "sec/")]

    silver = {}
    silver_parts = []
    for prefix in SILVER_PREFIXES:
        for obj in _list(s3, prefix):
            if not obj["Key"].endswith(".parquet"):
                continue
            silver_parts.append(obj["Key"])
            table = pq.read_table(io.BytesIO(s3.get_object(Bucket=BUCKET, Key=obj["Key"])["Body"].read()))
            for row in table.to_pylist():
                silver.setdefault(row.get("security_key"), []).append(
                    {"part": obj["Key"], "accession": row.get("accession"), "form": row.get("form"),
                     "filing_date": str(row.get("filing_date"))})

    def per_name(key):
        safe = crosswalk.slash_safe_key(key)
        partition = crosswalk.security_key_partition(key)
        old = _list(s3, "filings/v1/%s/" % safe)
        old_sources = []
        analyses = []
        for obj in old:
            name = obj["Key"].rsplit("/", 1)[-1]
            if name.endswith(".analysis.json"):
                analyses.append({"key": obj["Key"], "stored": _stamp(obj)})
            elif name.endswith(".source.json"):
                if name.startswith("UNRESOLVED-SOURCE"):
                    doc = _get_json(s3, obj["Key"])
                    old_sources.append({"key": obj["Key"], "status": doc.get("status"), "stored": _stamp(obj),
                                        "reason": " ".join(str(doc.get("reason") or "").split())[:200]})
                else:
                    old_sources.append({"key": obj["Key"], "status": "RESOLVED (by name; body not opened)",
                                        "stored": _stamp(obj), "reason": None})
        state = []
        for obj in _list(s3, "%s%s/" % (STATE_PREFIX, partition)):
            doc = _get_json(s3, obj["Key"])
            state.append({"key": obj["Key"], "stored": _stamp(obj), "status": doc.get("status"),
                          "retrieved_at": doc.get("retrieved_at"), "parser_version": doc.get("parser_version"),
                          "reason": " ".join(str(doc.get("reason") or "").split())[:240]})
        bronze = sorted(_list(s3, "%s%s/" % (IDENTITY_BRONZE, partition)), key=lambda o: o["Key"])
        bronze_cik, bronze_key, bronze_fields, bronze_errors = None, None, None, {}
        if bronze:
            bronze_key = bronze[-1]["Key"]
            doc = _get_json(s3, bronze_key)
            inner = next(iter(doc.values())) if isinstance(doc, dict) and doc else {}
            inner = inner if isinstance(inner, dict) else {}
            bronze_fields = sorted(inner.keys())
            bronze_cik = inner.get("CENTRAL_INDEX_KEY_NUMBER")
            bronze_errors = inner.get("__field_errors__") if isinstance(inner.get("__field_errors__"), dict) else {}
        draft = _list(s3, "drafting/v1/%s.json" % safe)
        return key, {"old_sources": old_sources, "analyses": analyses, "state": state, "bronze_key": bronze_key,
                     "bronze_cik": bronze_cik, "bronze_fields": bronze_fields, "bronze_errors": bronze_errors,
                     "draft": [{"key": o["Key"], "stored": _stamp(o)} for o in draft]}

    with ThreadPoolExecutor(max_workers=8) as pool:
        store = dict(pool.map(per_name, covered))

    newest_of = {}
    for label, prefix in (("filing-attempt markers", STATE_PREFIX), ("filing_source silver (sec)", SILVER_PREFIXES[0]),
                          ("filing_source silver (issuer-site)", SILVER_PREFIXES[1]), ("old filings/v1", "filings/v1/"),
                          ("drafting/v1", "drafting/v1/")):
        objs = _list(s3, prefix)
        newest_of[label] = {"objects": len(objs), "newest": max(_stamp(o) for o in objs) if objs else None}
    return {"last_wrote": newest_of, "covered": covered, "served": served, "pool_key": crosswalk_keys[-1], "pool_by_key": pool_by_key,
            "registrations": registrations, "universe_keys": universe_keys, "newest_universe_key": newest_universe_key,
            "newest": newest, "plans": plans, "rows_by_universe": rows_by_universe, "sec_table_key": sec_table_key,
            "sec_rows": len(sec_raw), "sec_by_ticker": sec_by_ticker, "other_identity": other_identity,
            "other_sec": other_sec, "silver": silver, "silver_parts": silver_parts, "store": store}


def build_table(data):
    covered = data["covered"]
    newest_key = data["newest_universe_key"]
    no_analysis = [k for k in covered if not data["store"][k]["analyses"]]
    part_a = [k for k in no_analysis if "no cik" in data["served"][k]["drafting_reason"]]
    part_b = [k for k in no_analysis if data["served"][k]["drafting_reason"].startswith("no drafted document")]
    other = [k for k in no_analysis if k not in part_a and k not in part_b]

    def places(key):
        root = key.rsplit("_", 2)[0].upper()
        exchange = key.rsplit("_", 2)[1]
        pool_identity = (data["pool_by_key"].get(key) or {}).get("identity") or {}
        reg_identity = (data["registrations"].get(key) or {}).get("identity") or {}
        row = data["rows_by_universe"][newest_key].get(key) or {}
        sec = data["sec_by_ticker"].get(root.replace("/", ""))
        st = data["store"][key]
        return {
            "name": key, "exchange": exchange,
            "pool_cik": pool_identity.get("cik"), "pool_sec_id": pool_identity.get("sec_id"),
            "pool_field_errors": pool_identity.get("field_errors") or {},
            "pool_has_identity_block": bool(pool_identity),
            "registrations_cik": reg_identity.get("cik"), "registrations_sec_id": reg_identity.get("sec_id"),
            "bronze_object": st["bronze_key"], "bronze_cik": st["bronze_cik"], "bronze_fields": st["bronze_fields"],
            "universe_cik": row.get("cik"), "universe_filing_identity": row.get("filing_identity"),
            "universe_filing_note": str(row.get("resolution_reason") or "").split("filing identity: ", 1)[-1][:260],
            "bronze_cik_error": ((st.get("bronze_errors") or {}).get("CENTRAL_INDEX_KEY_NUMBER") or {}).get("message"),
            "universe_row_present": bool(row),
            "universe_by_vintage": {u: (data["rows_by_universe"][u].get(key) or {}).get("filing_identity")
                                    for u in data["universe_keys"]},
            "planner_by_vintage": {u: data["plans"][u].get(key) for u in data["universe_keys"]},
            "sec_table": sec, "sec_table_us_listing": exchange == "US",
            "state": st["state"], "old_sources": st["old_sources"],
        }

    rows_a = []
    for key in part_a:
        row = places(key)
        stored = []
        if row["pool_cik"]:
            stored.append("pool list")
        if row["registrations_cik"]:
            stored.append("registrations.json")
        if _int_cik(row["bronze_cik"]):
            stored.append("identity bronze")
        if (row["universe_filing_identity"] or {}).get("cik"):
            stored.append("universe")
        if row["sec_table"] and row["exchange"] == "US":
            stored.append("SEC ticker table")
        elif row["sec_table"]:
            stored.append("SEC ticker table (same ticker text, not a US listing: not counted)")
        row["cik_stored_in"] = stored
        counted = [s for s in stored if "not counted" not in s]
        ciks = {_int_cik(v) for v in (row["pool_cik"], row["registrations_cik"], row["bronze_cik"],
                                      (row["universe_filing_identity"] or {}).get("cik"),
                                      (row["sec_table"] or {}).get("cik") if row["exchange"] == "US" else None)}
        ciks.discard(None)
        row["distinct_cik_values"] = sorted(ciks)
        identity = row["universe_filing_identity"] or {}
        row["form_decided"] = identity.get("form_expected") in FORMS
        if identity.get("source") == "edgar" and identity.get("cik"):
            row["class"] = "CIK_IN_NEWEST_UNIVERSE"
        elif counted:
            row["class"] = "CIK_STORED_NOT_IN_UNIVERSE"
        elif row["bronze_object"]:
            row["class"] = "ASKED_BLOOMBERG_NO_CIK"
        else:
            row["class"] = "NEVER_ASKED"
        rows_a.append(row)

    rows_b = []
    for key in part_b:
        row = places(key)
        st = data["store"][key]
        resolved_old = [s for s in st["old_sources"] if str(s["status"]).startswith("RESOLVED")]
        silver = data["silver"].get(key) or []
        identity = row["universe_filing_identity"] or {}
        stage = {"S1 CIK": bool(identity.get("source") == "edgar" and identity.get("cik")),
                 "S2 FORM": identity.get("form_expected") in FORMS,
                 "S3 SOURCE": bool(resolved_old or silver),
                 "S4 ANALYSIS": bool(st["analyses"]), "S5 DRAFT": bool(st["draft"])}
        elsewhere = []
        if row["pool_cik"]:
            elsewhere.append("pool list")
        if row["registrations_cik"]:
            elsewhere.append("registrations.json")
        if _int_cik(row["bronze_cik"]):
            elsewhere.append("identity bronze")
        row["cik_stored_in"] = elsewhere
        row["bloomberg_asked"] = bool(row["bronze_object"])
        row["first_universe"] = next((u for u in data["universe_keys"] if row["universe_by_vintage"][u]), None)
        row["stages"] = stage
        row["first_missing_stage"] = next((s for s in B_STAGES if not stage[s]), "none")
        before = (B_STAGES[:B_STAGES.index(row["first_missing_stage"])]
                  if row["first_missing_stage"] != "none" else B_STAGES)
        row["last_stored_stage"] = before[-1] if before else "none (the universe row only)"
        row["silver_rows"] = silver
        row["resolved_old_sources"] = resolved_old
        row["unresolved_markers"] = [s for s in st["old_sources"] if not str(s["status"]).startswith("RESOLVED")]
        row["ever_planned"] = [u for u in data["universe_keys"] if row["planner_by_vintage"][u]]
        rows_b.append(row)

    return {
        "covered": len(covered), "no_filing_analysis": len(no_analysis),
        "part_a_names": part_a, "part_b_names": part_b, "other_reason": other,
        "other_reason_text": {k: data["served"][k]["drafting_reason"][:200] for k in other},
        "part_a_classes": {c: sorted(r["name"] for r in rows_a if r["class"] == c) for c in A_CLASSES},
        "part_b_first_missing": dict(collections.Counter(r["first_missing_stage"] for r in rows_b)),
        "part_b_last_stored": dict(collections.Counter(r["last_stored_stage"] for r in rows_b)),
        "rows_a": rows_a, "rows_b": rows_b,
        "sources": {"pool_list": data["pool_key"], "universes": data["universe_keys"],
                    "newest_universe": newest_key, "sec_ticker_table": data["sec_table_key"],
                    "sec_ticker_table_rows": data["sec_rows"], "objects_under_identity_prefix": data["other_identity"],
                    "objects_under_sec_prefix": data["other_sec"], "silver_parts": data["silver_parts"],
                    "registrations": REGISTRATIONS},
        "not_200": sorted(k for k in covered if data["served"][k]["status_code"] != 200),
        "covered_planner_newest": {
            "would_fetch": sorted(k for k in covered if data["plans"][newest_key].get(k)),
            "form_none": sorted(k for k in covered if (data["plans"][newest_key].get(k) or {}).get("form_expected")
                                == "none")},
        "newest_universe_forms": dict(collections.Counter(
            "%s / %s" % ((r.get("filing_identity") or {}).get("source"),
                         (r.get("filing_identity") or {}).get("form_expected")) for r in data["newest"]["names"])),
        "covered_forms": dict(collections.Counter(
            "%s / %s" % (((data["rows_by_universe"][newest_key].get(k) or {}).get("filing_identity") or {}).get("source"),
                         ((data["rows_by_universe"][newest_key].get(k) or {}).get("filing_identity") or {}).get(
                             "form_expected")) for k in covered)),
        "part_a_form_decided": sum(1 for r in rows_a if r.get("form_decided")),
        "part_b_first_universe": dict(collections.Counter(str(r["first_universe"]) for r in rows_b)),
        "part_a_first_universe": dict(collections.Counter(
            str(next((u for u in data["universe_keys"] if r["universe_by_vintage"][u]), None)) for r in rows_a)),
        "part_b_cik_elsewhere": dict(collections.Counter(
            "%s | %s" % (r["first_missing_stage"], "CIK held in " + "+".join(r["cik_stored_in"]) if r["cik_stored_in"]
                         else ("Bloomberg asked, no CIK" if r["bloomberg_asked"] else "never asked")) for r in rows_b)),
        "part_b_with_any_marker_or_source": sum(1 for r in rows_b if r["state"] or r["old_sources"] or r["silver_rows"]),
        "filing_step_last_wrote": data["last_wrote"],
        "state_marker_stamps": dict(collections.Counter(
            (s["retrieved_at"] or "")[:10] for k in part_a for s in data["store"][k]["state"])),
    }


def print_table(t):
    print("   covered %d; /thesis not 200: %d; names with no stored filing analysis: %d"
          % (t["covered"], len(t["not_200"]), t["no_filing_analysis"]))
    print("   the page's stated reason: 'no cik' %d; 'no drafted document' %d; any other reason %d %s"
          % (len(t["part_a_names"]), len(t["part_b_names"]), len(t["other_reason"]), t["other_reason_text"]))
    print("   sources: pool list %s; newest universe %s of %s; SEC ticker table %s (%d rows)"
          % (t["sources"]["pool_list"], t["sources"]["newest_universe"], t["sources"]["universes"],
             t["sources"]["sec_ticker_table"], t["sources"]["sec_ticker_table_rows"]))
    print("   objects under identity/: %s" % t["sources"]["objects_under_identity_prefix"])
    print("   objects under sec/: %s" % t["sources"]["objects_under_sec_prefix"])
    print("PART A -- %d names reading 'no cik'" % len(t["part_a_names"]))
    for c in A_CLASSES:
        print("   %-28s %2d  %s" % (c, len(t["part_a_classes"][c]), ", ".join(t["part_a_classes"][c])))
    print("   sum %d of %d" % (sum(len(v) for v in t["part_a_classes"].values()), len(t["part_a_names"])))
    place = collections.Counter(p for r in t["rows_a"] for p in r["cik_stored_in"])
    print("   CIK held, by place (a name can be in several): %s" % dict(place))
    print("   state marker written (retrieved_at day): %s" % t["state_marker_stamps"])
    print("   of the %d, the newest universe row's form is decided on: %d" % (len(t["rows_a"]), t["part_a_form_decided"]))
    print("   first universe vintage each name appears in: %s" % t["part_a_first_universe"])
    print("   newest universe, all %d rows, source / form: %s" % (sum(t["newest_universe_forms"].values()),
                                                                  t["newest_universe_forms"]))
    print("   newest universe, the %d covered names, source / form: %s" % (t["covered"], t["covered_forms"]))
    print("   what the filing step last wrote: %s" % json.dumps(t["filing_step_last_wrote"]))
    for r in t["rows_a"]:
        print("   %-18s %-27s cik %s in %s | universe newest %s | bronze fields %s"
              % (r["name"], r["class"], r["distinct_cik_values"], r["cik_stored_in"],
                 json.dumps(r["universe_filing_identity"]), "none" if r["bronze_fields"] is None else
                 ("CIK present" if r["bronze_cik"] else "asked, no CIK: %s" % r["bronze_cik_error"])))
        if r["sec_table"] and r["exchange"] != "US":
            print("      SEC ticker table row for the same ticker text: %s; the universe says: %s"
                  % (json.dumps(r["sec_table"]), r["universe_filing_note"]))
    print("PART B -- %d names reading 'no drafted document'" % len(t["part_b_names"]))
    print("   first stage with no stored object: %s" % t["part_b_first_missing"])
    print("   last stage with a stored object:   %s" % t["part_b_last_stored"])
    print("   first universe vintage each name appears in: %s" % t["part_b_first_universe"])
    print("   names with any filing-attempt marker, old source object or silver row: %d of %d"
          % (t["part_b_with_any_marker_or_source"], len(t["rows_b"])))
    print("   first missing stage | where a CIK is held outside the universe: %s" % t["part_b_cik_elsewhere"])
    for r in t["rows_b"]:
        print("   %-18s first-missing %-9s | universe newest %s | CIK elsewhere %s %s | silver rows %d | old resolved "
              "%d | markers %d | state %d"
              % (r["name"], r["first_missing_stage"], json.dumps(r["universe_filing_identity"]),
                 sorted({_int_cik(v) for v in (r["pool_cik"], r["registrations_cik"], r["bronze_cik"]) if _int_cik(v)}),
                 r["cik_stored_in"] or ("Bloomberg asked, no CIK: %s" % r["bronze_cik_error"] if r["bloomberg_asked"]
                                        else "never asked"),
                 len(r["silver_rows"]), len(r["resolved_old_sources"]), len(r["unresolved_markers"]), len(r["state"])))
        if r["first_missing_stage"] == "S1 CIK":
            print("      the universe says: %s" % r["universe_filing_note"])
    print("   covered names the planner would fetch on the newest universe: %d of %d (of them form 'none': %d)"
          % (len(t["covered_planner_newest"]["would_fetch"]), t["covered"],
             len(t["covered_planner_newest"]["form_none"])))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", default=None, help="folder to write FILING_COVERAGE_READ.json to")
    a = ap.parse_args()
    table = build_table(read_everything())
    print_table(table)
    if a.write:
        os.makedirs(a.write, exist_ok=True)
        with open(os.path.join(a.write, "FILING_COVERAGE_READ.json"), "w", encoding="utf-8", newline="\n") as fh:
            json.dump(table, fh, indent=1, sort_keys=True, default=str)
            fh.write("\n")
        print("   wrote FILING_COVERAGE_READ.json to %s" % a.write)
    ok = (sum(len(v) for v in table["part_a_classes"].values()) == len(table["part_a_names"])
          and sum(table["part_b_first_missing"].values()) == len(table["part_b_names"]) and not table["not_200"])
    print("R78 READ FILING COVERAGE: %s" % ("DONE" if ok else "NOT DONE"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
