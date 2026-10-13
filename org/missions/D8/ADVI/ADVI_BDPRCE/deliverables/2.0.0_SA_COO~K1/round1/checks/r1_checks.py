"""ADVI_BDPRCE round 1: record-shape graders for the four cells, issuer 2.0.0_SA_COO~K1.

  writers --file <WRITERS.json>   BP-a-1: the writer census record
  gap     --file <GAP.json>       BP-a-3: the served-versus-recomputed classification
  trace   --file <TRACE.json>     BP-a-2: one instrument output over a real served row
  thread  --file <THREAD.json>    BP-a-4: the thread record

Each prints one last line `<NAME> record ok ...` or `<NAME> record FAIL <why>`, exit 0 on ok. The graders prove shape,
read-only discipline and arithmetic (a class partition sums to its denominator); they do not prove the measurement is
right -- the issuer re-reads cited objects. ASCII only. Never edit this file.
"""
import argparse
import json
import re
import sys

WRITE_VERBS = re.compile(
    r"\b(put-object|delete-object|delete-objects|copy-object|put-bucket|update-function|invoke|put-rule|put-targets|"
    r"start-execution|s3 cp [^ ]+ s3://|s3 rm|s3 sync [^ ]+ s3://|terraform apply)\b")
CLAIMS = {"measured", "inferred", "held", "absent"}
GAP_CLASSES = ["EQUAL", "EXPLAINED_BY_VERSION_AT_WRITE", "EXPLAINED_BY_MULTIDAY_WINDOW", "EXPLAINED_OTHER",
               "UNEXPLAINED", "NOT_RECOMPUTABLE"]


def fail(name, why):
    print("%s record FAIL %s" % (name, why))
    return 1


def load(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def no_write_calls(rec):
    calls = rec.get("calls")
    if not isinstance(calls, list) or not calls:
        return "calls missing or empty"
    for c in calls:
        if WRITE_VERBS.search(str(c)):
            return "write verb in calls: %s" % str(c)[:80]
    return None


def writers(rec):
    why = no_write_calls(rec)
    if why:
        return fail("WRITERS", why)
    if rec.get("claim") not in CLAIMS:
        return fail("WRITERS", "claim not in the closed set")
    ws = rec.get("writers")
    if not isinstance(ws, list) or not ws:
        return fail("WRITERS", "writers missing or empty")
    keys = set()
    for w in ws:
        for k in ("writer_id", "bucket", "object_key", "evidence", "rule_copy", "claim"):
            if k not in w:
                return fail("WRITERS", "writer row lacks %s" % k)
        if w["claim"] not in CLAIMS:
            return fail("WRITERS", "writer claim not in the closed set")
        keys.add(w["object_key"])
    need = ("canonical_prices.parquet", "silver/prices/")
    for n in need:
        if not any(n in k for k in keys):
            return fail("WRITERS", "no writer row for %s" % n)
    vr = rec.get("object_versions_read")
    if not isinstance(vr, int) or vr <= 0:
        return fail("WRITERS", "object_versions_read (the denominator) missing")
    un = rec.get("unidentified")
    if not isinstance(un, list):
        return fail("WRITERS", "unidentified must be a list (empty when none)")
    print("WRITERS record ok writers=%d unidentified=%d versions_read=%d" % (len(ws), len(un), vr))
    return 0


def gap(rec):
    why = no_write_calls(rec)
    if why:
        return fail("GAP", why)
    if rec.get("claim") not in CLAIMS:
        return fail("GAP", "claim not in the closed set")
    cls = rec.get("classes")
    served = rec.get("served_rows")
    if not isinstance(cls, dict) or not isinstance(served, int) or served <= 0:
        return fail("GAP", "classes or served_rows (the denominator) missing")
    if sorted(cls) != sorted(GAP_CLASSES):
        return fail("GAP", "class keys are not the closed set")
    if sum(int(v) for v in cls.values()) != served:
        return fail("GAP", "classes sum %d != served_rows %d" % (sum(int(v) for v in cls.values()), served))
    if cls["EXPLAINED_OTHER"] and not rec.get("other_causes"):
        return fail("GAP", "EXPLAINED_OTHER > 0 but other_causes empty")
    if not rec.get("window") or not rec.get("bound_statement"):
        return fail("GAP", "window and bound_statement are required")
    explained = sum(int(cls[k]) for k in GAP_CLASSES if k.startswith("EXPLAINED"))
    print("GAP record ok served=%d equal=%d explained=%d unexplained=%d"
          % (served, cls["EQUAL"], explained, cls["UNEXPLAINED"]))
    return 0


def trace(rec):
    for k in ("asset_name", "date", "served_price", "price_source", "rule", "trade_ids", "recomputed_price", "match"):
        if k not in rec:
            return fail("TRACE", "lacks %s" % k)
    if not isinstance(rec["trade_ids"], list):
        return fail("TRACE", "trade_ids must be a list")
    if rec["price_source"] == "transaction_observed" and not rec["trade_ids"]:
        return fail("TRACE", "transaction_observed with no trade ids")
    if not isinstance(rec["match"], bool):
        return fail("TRACE", "match must be boolean")
    print("TRACE record ok source=%s trades=%d match=%s"
          % (rec["price_source"], len(rec["trade_ids"]), str(rec["match"]).lower()))
    return 0


def thread(rec):
    if "account_id" in rec or "advisor_name" in rec or "client_name" in rec:
        return fail("THREAD", "a raw account id or a name is present")
    for k in ("served_object_key", "as_of_date", "account_ref", "asset_name", "served_price", "price_source",
              "rule", "trade_ids", "recomputed_price", "recompute_equals_served", "instrument", "claim"):
        if k not in rec:
            return fail("THREAD", "lacks %s" % k)
    if rec["claim"] not in CLAIMS:
        return fail("THREAD", "claim not in the closed set")
    if rec.get("ticker") not in (None, "", "UNKNOWN"):
        return fail("THREAD", "the holding is not untickered (ticker=%s)" % rec.get("ticker"))
    if not isinstance(rec["trade_ids"], list) or not rec["trade_ids"]:
        return fail("THREAD", "trade_ids empty")
    if not re.fullmatch(r"[0-9a-f]{12}", str(rec["account_ref"])):
        return fail("THREAD", "account_ref is not a 12-hex digest")
    print("THREAD record ok rule=%s trades=%d equal=%s"
          % (re.sub(r"\s+", "_", str(rec["rule"]))[:40], len(rec["trade_ids"]),
             str(rec["recompute_equals_served"]).lower()))
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["writers", "gap", "trace", "thread"])
    ap.add_argument("--file", required=True)
    a = ap.parse_args()
    try:
        rec = load(a.file)
    except Exception as e:  # noqa: BLE001 -- the grader reports, never raises
        return fail(a.cmd.upper(), "unreadable record: %s" % type(e).__name__)
    return {"writers": writers, "gap": gap, "trace": trace, "thread": thread}[a.cmd](rec)


if __name__ == "__main__":
    sys.exit(main())
