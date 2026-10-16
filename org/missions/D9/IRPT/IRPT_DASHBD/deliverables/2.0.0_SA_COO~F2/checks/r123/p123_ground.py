"""IRPT_DASHBD round 123, workstream F-SHIP ~F2 (issuer 2.0.0_SA_COO~F2) -- FWD-5: the transaction producer's GROUND READ for 49 Financial.

  DB-f-901 (~901) a READ of code and tracked records: for each of the 14 columns the backend brief names for `account_transaction`, the
                  49 Financial custody-silver source column (or ABSENT), the producer to copy, the address the naming builder gives
                  for a third gold table, and what emitting it would touch.                                      DBF123-1-AC1

The checker binds the record to the code it cites: a cited line must hold the token the record says it holds. A target with
no source column is claim `absent` and has `source` null; the count of absent targets is computed here and must equal the record's.

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                        the pure helpers on synthetic arms
"""
import json
import re
import sys
from pathlib import Path

REC = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~901/RD_FWD5_PRODUCER_GROUND_R123.json"
TARGETS = ("trade_date", "settle_date", "action", "txn_type", "symbol", "asset_name", "units", "price", "amount", "fee",
           "custodian", "flow_class", "source_txn_id", "coverage")
CLAIMS = ("measured", "inferred", "held", "absent")
LONG_DIGITS = re.compile(r"\d{8,}")
DIGIT_OK_KEYS = ("sha256", "path", "file", "key", "where", "vintage", "uri")
ZERO_READS = {"s3_reads": 0, "s3_writes": 0, "dynamodb_writes": 0, "vendor_calls": 0, "secret_reads": 0}
KEYS = ("as_of", "firm", "targets", "absent_count", "pattern_producer", "silver_source", "address", "emit_path", "reads",
        "files_in_repo", "served_values_changed", "pushed", "deployed")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def digits_ok(obj, key=""):
    if isinstance(obj, dict):
        return all(digits_ok(v, k) for k, v in obj.items())
    if isinstance(obj, list):
        return all(digits_ok(v, key) for v in obj)
    if isinstance(obj, str) and LONG_DIGITS.search(obj) and key not in DIGIT_OK_KEYS:
        return False
    return True


def claim_ok(d):
    return isinstance(d, dict) and d.get("claim") in CLAIMS


def words_ok(d):
    return isinstance(d, dict) and isinstance(d.get("words"), str) and d["words"].strip() != ""


def line_of(root, d):
    f, line = d.get("file"), d.get("line")
    if not (isinstance(f, str) and isinstance(line, int) and not isinstance(line, bool)):
        return None
    p = Path(root) / f
    if not p.is_file():
        return None
    lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
    return lines[line - 1].lower() if 1 <= line <= len(lines) else None


def cites(root, d, tokens):
    text = line_of(root, d)
    return text is not None and any(t.lower() in text for t in tokens)


def target_problems(root, targets):
    pr = []
    if not (isinstance(targets, list) and [t.get("target") if isinstance(t, dict) else None for t in targets] == list(TARGETS)):
        return ["targets must be exactly the 14 brief columns, in the brief's order: " + ", ".join(TARGETS)]
    for t in targets:
        name = t["target"]
        if not (claim_ok(t) and words_ok(t)):
            pr.append("%s: claim or words" % name)
            continue
        if t["source"] is None:
            if t["claim"] != "absent":
                pr.append("%s: a null source needs claim absent" % name)
            continue
        if not (isinstance(t["source"], str) and t["source"]):
            pr.append("%s: source form" % name)
        elif t["claim"] == "absent":
            pr.append("%s: claim absent with a source" % name)
        elif not cites(root, t, (t["source"],)):
            pr.append("%s: the cited line does not hold the source column %r" % (name, t["source"]))
    return pr


def absent_count(targets):
    return sum(1 for t in targets if isinstance(t, dict) and t.get("source") is None)


def problems(root, rec):
    if not isinstance(rec, dict) or sorted(rec.keys()) != sorted(KEYS):
        return ["top-level fields are not exactly " + repr(KEYS)]
    pr = []
    if not (isinstance(rec["as_of"], str) and re.match(r"\d{4}-\d{2}-\d{2}$", rec["as_of"])):
        pr.append("as_of not an ISO date")
    if rec["firm"] != "49financial":
        pr.append("firm is not 49financial")
    pr += target_problems(root, rec["targets"])
    if rec["absent_count"] != absent_count(rec["targets"]):
        pr.append("absent_count is not the count computed from the targets (%d)" % absent_count(rec["targets"]))
    pp = rec["pattern_producer"]
    if not (claim_ok(pp) and words_ok(pp) and cites(root, pp, ("def ", "arrow_schema", "emit", "table_"))):
        pr.append("pattern_producer form or citation")
    ss = rec["silver_source"]
    if not (claim_ok(ss) and words_ok(ss) and cites(root, ss, ("fact_trn", "transaction", "trn"))):
        pr.append("silver_source form or citation")
    ad = rec["address"]
    if not (claim_ok(ad) and words_ok(ad) and isinstance(ad.get("uri"), str) and ad["uri"].startswith("s3://")
            and "49financial" in ad["uri"] and "account_transaction" in ad["uri"] and isinstance(ad.get("registry_row_exists"), bool)):
        pr.append("address form (uri must be an s3 uri for 49financial and account_transaction, registry_row_exists a boolean)")
    ep = rec["emit_path"]
    if not (claim_ok(ep) and words_ok(ep) and cites(root, ep, ("account_class_daily", "class", "emit", "put", "prefix"))):
        pr.append("emit_path form or citation")
    if rec["reads"] != ZERO_READS:
        pr.append("reads block is not the all-zero form")
    for k in ("files_in_repo", "served_values_changed", "pushed", "deployed"):
        if rec[k] is not False:
            pr.append(k + " is not false")
    if not digits_ok(rec):
        pr.append("a run of 8 or more digits outside the exempt fields")
    return pr


def ac_ground(root):
    p = Path(root) / REC
    need(p.is_file(), "missing record " + REC)
    pr = problems(root, json.loads(p.read_text(encoding="utf-8")))
    need(not pr, "; ".join(pr[:6]))


def selftest():
    bad = 0
    count = 0

    def arm(name, got, want):
        nonlocal bad, count
        count += 1
        if got != want:
            bad += 1
            print("SELFTEST FAIL %s: got %r want %r" % (name, got, want))

    arm("targets-count", len(TARGETS), 14)
    arm("digits-red", digits_ok({"words": "id 12345678901"}), False)
    arm("digits-uri", digits_ok({"uri": "s3://b/k/12345678901"}), True)
    arm("form-red", problems(".", {"as_of": "x"})[0].startswith("top-level"), True)
    arm("targets-red-order", target_problems(".", [{"target": "price"}])[0].startswith("targets must be"), True)
    absent = [{"target": t, "source": None, "claim": "absent", "words": "no source"} for t in TARGETS]
    arm("targets-green-absent", target_problems(".", absent), [])
    arm("absent-count", absent_count(absent), 14)
    bad_absent = [dict(a) for a in absent]
    bad_absent[0]["claim"] = "measured"
    arm("null-source-needs-absent", len(target_problems(".", bad_absent)), 1)
    arm("cites-red", cites(".", {"file": "nope", "line": 1}, ("a",)), False)
    print("selftest %s" % ("FAIL" if bad else "PASS (%d arms)" % count))
    return 1 if bad else 0


def main(argv):
    if len(argv) == 2 and argv[1] == "--selftest":
        return selftest()
    if len(argv) != 3:
        print(__doc__)
        return 2
    root, ac = argv[1], argv[2]
    if ac != "DBF123-1-AC1":
        print("%s FAIL (unknown criterion)" % ac)
        return 1
    try:
        ac_ground(root)
    except Fail as e:
        print("reason: %s" % e)
        print("%s FAIL" % ac)
        return 1
    except Exception as e:  # noqa: BLE001
        print("reason: %s: %s" % (type(e).__name__, e))
        print("%s FAIL" % ac)
        return 1
    print("%s PASS" % ac)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
