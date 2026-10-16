"""IRPT_DASHBD round 120, workstream F-SHIP ~F2 (issuer 2.0.0_SA_COO~F2) -- two reads for the CTO's round-119 rulings.

  DB-f-701 (~701) FWD-5: each firm's custody transaction fields and its custodian action and type codes, from code and tracked records.   DBF120-1-AC1
  DB-f-702 (~702) FWD-3: the existing account_class_daily producer's gap to the ruled acceptance (the sum to the account, the dated read).  DBF120-2-AC1

The checker binds each record to the code it cites (a cited line must hold the token the record says it holds) and to the form.

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                        the pure helpers on synthetic arms
"""
import json
import re
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC701 = D + "0.9.0_WK_IRPT_DASHBD~701/RD_FWD5_FIELDS_R120.json"
REC702 = D + "0.9.0_WK_IRPT_DASHBD~702/RD_FWD3_PRODUCER_GAP_R120.json"
CLAIMS = ("measured", "inferred", "held", "absent")
LONG_DIGITS = re.compile(r"\d{8,}")
DIGIT_OK_KEYS = ("sha256", "path", "file", "key", "where", "vintage")
ZERO_READS = {"s3_reads": 0, "s3_writes": 0, "dynamodb_writes": 0, "vendor_calls": 0, "secret_reads": 0}


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


def cites(root, d, tokens):
    f, line = d.get("file"), d.get("line")
    if not (isinstance(f, str) and isinstance(line, int) and not isinstance(line, bool)):
        return False
    p = Path(root) / f
    if not p.is_file():
        return False
    lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
    if not (1 <= line <= len(lines)):
        return False
    return any(t in lines[line - 1].lower() for t in tokens)


def common_problems(rec, keys):
    pr = []
    if not isinstance(rec, dict) or sorted(rec.keys()) != sorted(keys):
        return ["top-level fields are not exactly " + repr(keys)]
    if not (isinstance(rec["as_of"], str) and re.match(r"\d{4}-\d{2}-\d{2}$", rec["as_of"])):
        pr.append("as_of not an ISO date")
    if rec["reads"] != ZERO_READS:
        pr.append("reads block is not the all-zero form")
    for k in ("files_in_repo", "served_values_changed", "pushed", "deployed"):
        if rec[k] is not False:
            pr.append(k + " is not false")
    if not digits_ok(rec):
        pr.append("a run of 8 or more digits outside the exempt fields")
    return pr


def problems_701(root, rec):
    keys = ("as_of", "firms", "brief_flow_classes", "opal_vocab_home", "reads", "files_in_repo", "served_values_changed", "pushed", "deployed")
    pr = common_problems(rec, keys)
    if pr and pr[0].startswith("top-level"):
        return pr
    firms = rec["firms"]
    if not (isinstance(firms, list) and len(firms) >= 3):
        pr.append("firms fewer than 3")
    else:
        for i, f in enumerate(firms):
            ok = (isinstance(f, dict) and isinstance(f.get("firm"), str) and f["firm"] and claim_ok(f)
                  and isinstance(f.get("columns"), list) and isinstance(f.get("action_codes"), list)
                  and isinstance(f.get("type_codes"), list) and isinstance(f.get("vocabulary_where"), str))
            if not ok:
                pr.append("firm %d form" % (i + 1))
            elif not cites(root, f, ("transaction", "trn", "fact_", "tran_", "action", "type")):
                pr.append("firm %d citation does not hold a transaction token" % (i + 1))
    b = rec["brief_flow_classes"]
    if not (claim_ok(b) and isinstance(b.get("count"), int) and not isinstance(b.get("count"), bool) and b["count"] >= 0):
        pr.append("brief_flow_classes form")
    elif not cites(root, b, ("flow", "class", "action", "type")):
        pr.append("brief_flow_classes citation does not hold a flow token")
    if not (claim_ok(rec["opal_vocab_home"]) and words_ok(rec["opal_vocab_home"])):
        pr.append("opal_vocab_home form")
    return pr


def problems_702(root, rec):
    keys = ("as_of", "producer", "handler", "sum_test", "classification_read", "swap_snapshot_read", "failing_days_words",
            "reads", "files_in_repo", "served_values_changed", "pushed", "deployed")
    pr = common_problems(rec, keys)
    if pr and pr[0].startswith("top-level"):
        return pr
    if not (claim_ok(rec["producer"]) and cites(root, rec["producer"], ("account_class_daily", "class_return_daily", "asset_class"))):
        pr.append("producer form or citation")
    h = rec["handler"]
    if not (claim_ok(h) and isinstance(h.get("emits_class_table"), bool) and cites(root, h, ("account_class_daily", "class", "emit"))):
        pr.append("handler form or citation")
    s = rec["sum_test"]
    if not (claim_ok(s) and isinstance(s.get("exists"), bool) and words_ok(s)):
        pr.append("sum_test form")
    elif s["exists"] and not cites(root, s, ("sum", "account", "class")):
        pr.append("sum_test citation does not hold a sum token")
    c = rec["classification_read"]
    if not (claim_ok(c) and isinstance(c.get("dated"), bool) and words_ok(c) and cites(root, c, ("etf", "classif", "getitem", "table"))):
        pr.append("classification_read form or citation")
    w = rec["swap_snapshot_read"]
    if not (claim_ok(w) and words_ok(w) and cites(root, w, ("etf", "classif", "snapshot", "swap", "table"))):
        pr.append("swap_snapshot_read form or citation")
    if not (isinstance(rec["failing_days_words"], list) and rec["failing_days_words"]
            and all(isinstance(x, str) and x for x in rec["failing_days_words"])):
        pr.append("failing_days_words form")
    return pr


def load(root, rel):
    p = Path(root) / rel
    need(p.is_file(), "missing record " + rel)
    return json.loads(p.read_text(encoding="utf-8"))


def ac_701(root):
    pr = problems_701(root, load(root, REC701))
    need(not pr, "; ".join(pr))


def ac_702(root):
    pr = problems_702(root, load(root, REC702))
    need(not pr, "; ".join(pr))


def selftest():
    bad = 0
    count = 0

    def arm(name, got, want):
        nonlocal bad, count
        count += 1
        if got != want:
            bad += 1
            print("SELFTEST FAIL %s: got %r want %r" % (name, got, want))

    arm("digits-red", digits_ok({"words": "id 12345678901"}), False)
    arm("digits-green", digits_ok({"sha256": "12345678901"}), True)
    arm("claim", claim_ok({"claim": "held"}), True)
    arm("claim-red", claim_ok({"claim": "guess"}), False)
    arm("words", words_ok({"words": " "}), False)
    arm("form-701-red", problems_701(".", {"as_of": "x"})[0].startswith("top-level"), True)
    arm("form-702-red", problems_702(".", {"as_of": "x"})[0].startswith("top-level"), True)
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
    table = {"DBF120-1-AC1": ac_701, "DBF120-2-AC1": ac_702}
    if ac not in table:
        print("%s FAIL (unknown criterion)" % ac)
        return 1
    try:
        table[ac](root)
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
