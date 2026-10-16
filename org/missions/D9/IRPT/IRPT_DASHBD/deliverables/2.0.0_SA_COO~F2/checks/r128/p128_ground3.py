"""IRPT_DASHBD round 128, workstream F-SHIP ~F2 (issuer 2.0.0_SA_COO~F2) -- FWD-5: the ground read WITH SOURCE READS, three firms.

  DB-f-1401 (~1401) the CTO's round-126 analysis (msg 9133) voided the `absent` claims of rounds 123 and 126: a ground read that read no
                    source cannot say absent. The issuer read the live schema of each firm's transaction silver (a worker has no AWS
                    access): deliverables/2.0.0_SA_COO~F2/R128_LIVE_SOURCE_CENSUS_3FIRMS.json. This cell names, for each of the brief's 14
                    columns and each firm, the live column that supplies it, or the computation from live columns, or ABSENT with every
                    searched column printed.                                                            DBF128-1-AC1

The checker holds every `source` and `from_columns` entry to the census record's column list, an `absent` target to the full printed
search, the source-read counts to the census record's, and the CTO's fixed points: Inflection's settle date and fee are truly absent; the
Cottonwood columns the census shows (settle date, symbol, units, price, custodian, trade date) are never absent.

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                        the pure helpers on synthetic arms
"""
import json
import re
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
CENSUS = D + "2.0.0_SA_COO~F2/R128_LIVE_SOURCE_CENSUS_3FIRMS.json"
RECS = (("49financial", D + "0.9.0_WK_IRPT_DASHBD~1401/RD_FWD5_GROUND_49FINANCIAL_R128.json"),
        ("cottonwood", D + "0.9.0_WK_IRPT_DASHBD~1401/RD_FWD5_GROUND_COTTONWOOD_R128.json"),
        ("inflection", D + "0.9.0_WK_IRPT_DASHBD~1401/RD_FWD5_GROUND_INFLECTION_R128.json"))
TARGETS = ("trade_date", "settle_date", "action", "txn_type", "symbol", "asset_name", "units", "price", "amount", "fee",
           "custodian", "flow_class", "source_txn_id", "coverage")
CLAIMS = ("measured", "inferred", "held", "absent")
LONG_DIGITS = re.compile(r"\d{8,}")
DIGIT_OK_KEYS = ("sha256", "path", "file", "key", "where", "vintage", "uri", "rows", "partitions_read", "census")
ZERO_READS = {"s3_reads": 0, "s3_writes": 0, "dynamodb_writes": 0, "vendor_calls": 0, "secret_reads": 0}
KEYS = ("as_of", "firm", "source_reads", "targets", "absent_count", "computed_count", "worker_reads", "files_in_repo",
        "served_values_changed", "pushed", "deployed")
NEVER_ABSENT = {"cottonwood": ("trade_date", "settle_date", "symbol", "units", "price", "custodian")}
ALWAYS_ABSENT = {"inflection": ("settle_date", "fee")}


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def load(root, rel):
    p = Path(root) / rel
    need(p.is_file(), "missing file " + rel)
    return json.loads(p.read_text(encoding="utf-8"))


def digits_ok(obj, key=""):
    if isinstance(obj, dict):
        return all(digits_ok(v, k) for k, v in obj.items())
    if isinstance(obj, list):
        return all(digits_ok(v, key) for v in obj)
    if isinstance(obj, str) and LONG_DIGITS.search(obj) and key not in DIGIT_OK_KEYS:
        return False
    return True


def target_problems(firm, targets, columns):
    cols = set(columns)
    if not (isinstance(targets, list) and [t.get("target") if isinstance(t, dict) else None for t in targets] == list(TARGETS)):
        return ["targets must be exactly the 14 brief columns in the brief's order: " + ", ".join(TARGETS)]
    pr = []
    for t in targets:
        n = t["target"]
        if t.get("claim") not in CLAIMS or not (isinstance(t.get("words"), str) and t["words"].strip()):
            pr.append("%s: claim or words" % n)
            continue
        src, frm, method, searched = t.get("source"), t.get("from_columns"), t.get("method"), t.get("searched_columns")
        if not isinstance(frm, list):
            pr.append("%s: from_columns must be a list" % n)
            continue
        if t["claim"] == "absent":
            if src is not None or frm:
                pr.append("%s: an absent target has no source and no from_columns" % n)
            if searched != list(columns):
                pr.append("%s: an absent target must print the full searched column list (%d columns)" % (n, len(columns)))
            continue
        if searched is not None:
            pr.append("%s: searched_columns is for an absent target only" % n)
        if src is not None:
            if src not in cols:
                pr.append("%s: source %r is not a column of the live schema" % (n, src))
            if frm:
                pr.append("%s: a sourced target has no from_columns" % n)
            if t["claim"] == "inferred" and not (isinstance(method, str) and method.strip()):
                pr.append("%s: an inferred target needs a method" % n)
        else:
            if t["claim"] != "inferred" or not frm or not (isinstance(method, str) and method.strip()):
                pr.append("%s: a null source needs claim inferred, from_columns and a method (computed), or claim absent" % n)
            bad = [c for c in frm if c not in cols]
            if bad:
                pr.append("%s: from_columns %r are not columns of the live schema" % (n, bad[:3]))
    absent = {t["target"] for t in targets if t.get("claim") == "absent"}
    for n in NEVER_ABSENT.get(firm, ()):
        if n in absent:
            pr.append("%s: the live schema carries this field for %s; it is never absent" % (n, firm))
    for n in ALWAYS_ABSENT.get(firm, ()):
        if n not in absent:
            pr.append("%s: the CTO's read has this absent for %s; it must be absent with the search printed" % (n, firm))
    return pr


def record_problems(firm, rec, census_firm):
    if not isinstance(rec, dict) or sorted(rec.keys()) != sorted(KEYS):
        return ["top-level fields are not exactly " + repr(KEYS)]
    pr = []
    if not (isinstance(rec["as_of"], str) and re.match(r"\d{4}-\d{2}-\d{2}$", rec["as_of"])):
        pr.append("as_of not an ISO date")
    if rec["firm"] != firm:
        pr.append("firm is not %s" % firm)
    sr = rec["source_reads"]
    want = {"census": CENSUS, "partitions_read": census_firm["partitions_read"], "rows": census_firm["rows"],
            "column_count": census_firm["column_count"]}
    if sr != want:
        pr.append("source_reads must be %r (the issuer's census; partitions read above zero)" % want)
    if not (isinstance(census_firm["partitions_read"], int) and census_firm["partitions_read"] > 0):
        pr.append("the census reads no partition")
    pr += target_problems(firm, rec["targets"], census_firm["columns"])
    if isinstance(rec["targets"], list):
        absent = sum(1 for t in rec["targets"] if isinstance(t, dict) and t.get("claim") == "absent")
        computed = sum(1 for t in rec["targets"] if isinstance(t, dict) and t.get("source") is None and t.get("claim") == "inferred")
        if rec["absent_count"] != absent or rec["computed_count"] != computed:
            pr.append("absent_count / computed_count are not the counts computed from the targets (%d, %d)" % (absent, computed))
    if rec["worker_reads"] != ZERO_READS:
        pr.append("worker_reads is not the all-zero form (the worker reads no source; the census is the issuer's)")
    for k in ("files_in_repo", "served_values_changed", "pushed", "deployed"):
        if rec[k] is not False:
            pr.append(k + " is not false")
    if not digits_ok(rec):
        pr.append("a run of 8 or more digits outside the exempt fields")
    if not json.dumps(rec, ensure_ascii=False).isascii():
        pr.append("non-ASCII text")
    return pr


def ac_ground(root):
    census = load(root, CENSUS)
    pr = []
    for firm, rel in RECS:
        pr += ["%s: %s" % (firm, x) for x in record_problems(firm, load(root, rel), census["firms"][firm])]
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

    cols = ["a", "b", "c"]
    mk = lambda n, **k: dict({"target": n, "source": None, "from_columns": [], "claim": "absent", "method": None,  # noqa: E731
                              "words": "w", "searched_columns": list(cols)}, **k)
    allabs = [mk(n) for n in TARGETS]
    arm("absent-green", target_problems("49financial", allabs, cols), [])
    arm("absent-needs-search", len(target_problems("49financial", [dict(allabs[0], searched_columns=["a"])] + allabs[1:], cols)), 1)
    direct = dict(mk("trade_date"), source="a", claim="measured", searched_columns=None)
    arm("direct-green", target_problems("49financial", [direct] + allabs[1:], cols), [])
    ghost = dict(direct, source="zzz")
    arm("source-must-exist", len(target_problems("49financial", [ghost] + allabs[1:], cols)), 1)
    comp = dict(mk("action"), from_columns=["b"], claim="inferred", method="from b", searched_columns=None)
    arm("computed-green", target_problems("49financial", allabs[:2] + [comp] + allabs[3:], cols), [])
    arm("computed-needs-method", len(target_problems("49financial", allabs[:2] + [dict(comp, method="")] + allabs[3:], cols)), 1)
    arm("cottonwood-fixed-point", len(target_problems("cottonwood", allabs, cols)) >= 6, True)
    arm("inflection-fixed-point", target_problems("inflection", allabs, cols), [])
    arm("digits-red", digits_ok({"words": "id 12345678901"}), False)
    arm("form-red", record_problems("x", {"as_of": "x"}, {})[0].startswith("top-level"), True)
    print("selftest %s" % ("FAIL" if bad else "PASS (%d arms)" % count))
    return 1 if bad else 0


def main(argv):
    if len(argv) == 2 and argv[1] == "--selftest":
        return selftest()
    if len(argv) != 3:
        print(__doc__)
        return 2
    root, ac = argv[1], argv[2]
    if ac != "DBF128-1-AC1":
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
