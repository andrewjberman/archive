"""ADVI_FIRMBKTS round 8 graders, issuer 2.0.0_SA_COO~B1.

  plan --file F --firm X [--min N] [--require-text T ...]   FB-l-1, FB-l-2: a per-firm move plan record (moves with order and rollback).
  census --file F [--min N]                                 FB-l-3: the legacy-operation consumer census and the first zero-consumer case.
  retire --file F                                           FB-l-4: the one real retirement's record.
  move --file F                                             FB-l-5: the first moved trigger's record.
  guarddiff --root R --file F --base-blob B                 FB-m-1: the readiness guard is purely additive against a pinned base blob.
  readyhalt --file F                                        FB-m-2: the deployed readiness halt, three arms read live.
  tradeform --file F                                        FB-n-1: the trade-form fence apply (policies, Allow-append, CORS), one scoped apply, read back.
Plain ASCII; exit 0 on a pass. Proves SHAPE and read-only discipline, never that a finding is true.
"""
import argparse
import json
import re
import sys

CLAIMS = ("measured", "inferred", "held", "absent")
WRITE_VERBS = re.compile(
    r"(\s(put|delete|create|update|modify|attach|detach|start|stop|run|terminate|enable|disable|register|deregister|tag|untag|send|publish|invoke)-[a-z-]+)"
    r"|(\ss3(api)?\s+(cp|mv|rm|sync|put-object|delete-object)\b)|(\sterraform\s+(apply|destroy|import)\b)")
ID_TOKEN = re.compile(r"(?<![0-9A-Za-z])[A-Za-z]?[0-9]{9,}(?![0-9A-Za-z])")
OK_TOKENS = ("313476888478",)


def _load(path, tag):
    try:
        raw = open(path, encoding="utf-8").read()
        return raw, json.loads(raw)
    except (OSError, ValueError) as e:
        print("%s: FAIL cannot read %s: %s" % (tag, path, type(e).__name__))
        return None, None


def _common(tag, raw, d, keys):
    p = []
    bad = [m for m in ID_TOKEN.findall(raw) if m not in OK_TOKENS]
    if bad:
        p.append("%d id-shaped token(s) of nine or more digits (replace with <id>)" % len(bad))
    miss = [k for k in keys if k not in d]
    if miss:
        p.append("missing " + ",".join(miss))
        return p
    if d["claim"] not in CLAIMS:
        p.append("claim outside the four")
    return p


def _calls_ok(d, p):
    c = d.get("calls")
    if not isinstance(c, list) or not c or not all(isinstance(x, str) for x in c):
        p.append("calls must be a non-empty list of strings")
    elif any(WRITE_VERBS.search(" " + x) for x in c):
        p.append("a call carries a write verb")


def _den_ok(d, p):
    den = d.get("denominators")
    if not isinstance(den, dict) or not den or not all(isinstance(v, int) and v >= 0 for v in den.values()) or not any(v > 0 for v in den.values()):
        p.append("denominators must be integers with at least one above zero")


def plan(a):
    raw, d = _load(a.file, "PLAN")
    if d is None:
        return 1
    p = _common("PLAN", raw, d, ("order", "read_at", "firm", "calls", "denominators", "moves", "decommission", "retire", "not_read", "claim"))
    if p and p[-1].startswith("missing"):
        print("PLAN: FAIL " + "; ".join(p))
        return 1
    _calls_ok(d, p)
    _den_ok(d, p)
    if d.get("firm") != a.firm:
        p.append("firm is %s, want %s" % (d.get("firm"), a.firm))
    moves = d["moves"]
    if not isinstance(moves, list) or len(moves) < a.min:
        p.append("moves must be a list of at least %d" % a.min)
        moves = []
    ids = [m.get("id") for m in moves if isinstance(m, dict)]
    if len(set(ids)) != len(ids):
        p.append("move ids are not unique")
    for i, m in enumerate(moves):
        if not isinstance(m, dict):
            p.append("move %d is not an object" % i)
            continue
        miss = [k for k in ("id", "function", "kind", "from", "to", "order", "depends_on", "rollback", "proof", "evidence", "claim") if k not in m]
        if miss:
            p.append("move %d missing %s" % (i, ",".join(miss)))
            continue
        if not isinstance(m["order"], int) or m["claim"] not in CLAIMS:
            p.append("move %d order or claim has the wrong type" % i)
        if not str(m["rollback"]).strip() or not str(m["evidence"]).strip() or not str(m["proof"]).strip():
            p.append("move %d has an empty rollback, proof or evidence" % i)
        if not isinstance(m["depends_on"], list) or any(x not in ids for x in m["depends_on"]):
            p.append("move %d depends_on names an unknown move" % i)
    dc = d["decommission"]
    if not isinstance(dc, dict) or dc.get("window_days") != 45 or not str(dc.get("legacy_bucket", "")).startswith("opal-data-") or dc.get("claim") not in CLAIMS:
        p.append("decommission needs legacy_bucket, window_days 45 and a claim")
    if not isinstance(d["retire"], list) or not isinstance(d["not_read"], list):
        p.append("retire and not_read must be lists")
    blob = json.dumps(moves).lower()
    for need in a.require_text or []:
        if need.lower() not in blob:
            p.append("no move names %s" % need)
    if p:
        print("PLAN: FAIL " + "; ".join(p[:6]))
        return 1
    print("PLAN: OK firm=%s moves=%d retire=%d" % (d["firm"], len(moves), len(d["retire"])))
    return 0


def census(a):
    raw, d = _load(a.file, "CENSUS")
    if d is None:
        return 1
    p = _common("CENSUS", raw, d, ("order", "read_at", "calls", "denominators", "candidates", "first_zero_consumer", "not_read", "claim"))
    if p and p[-1].startswith("missing"):
        print("CENSUS: FAIL " + "; ".join(p))
        return 1
    _calls_ok(d, p)
    _den_ok(d, p)
    rows = d["candidates"]
    if not isinstance(rows, list) or len(rows) < a.min:
        p.append("candidates must be a list of at least %d" % a.min)
        rows = []
    zero = []
    for i, r in enumerate(rows):
        if not isinstance(r, dict):
            p.append("candidate %d is not an object" % i)
            continue
        miss = [k for k in ("id", "operation", "consumer_census", "evidence", "claim") if k not in r]
        if miss:
            p.append("candidate %d missing %s" % (i, ",".join(miss)))
            continue
        cc = r["consumer_census"]
        if not isinstance(cc, dict) or not isinstance(cc.get("scanned"), int) or not isinstance(cc.get("consumers"), int) or cc.get("claim") not in CLAIMS:
            p.append("candidate %d consumer_census needs integer scanned and consumers and a claim" % i)
            continue
        if cc["scanned"] <= 0:
            p.append("candidate %d census scanned nothing (a zero with no denominator)" % i)
        if r["claim"] not in CLAIMS or not str(r["evidence"]).strip():
            p.append("candidate %d claim or evidence missing" % i)
        if cc["consumers"] == 0 and cc["scanned"] > 0:
            zero.append(r["id"])
    fz = d["first_zero_consumer"]
    if fz is None:
        if not str(d.get("none_reason", "")).strip():
            p.append("first_zero_consumer is null with no none_reason")
    elif fz not in zero:
        p.append("first_zero_consumer is not a candidate with scanned > 0 and consumers 0")
    if p:
        print("CENSUS: FAIL " + "; ".join(p[:6]))
        return 1
    print("CENSUS: OK candidates=%d zero=%d first=%s" % (len(rows), len(zero), fz))
    return 0


def _act(tag, a, keys):
    raw, d = _load(a.file, tag)
    if d is None:
        return None, None
    p = _common(tag, raw, d, keys)
    if p and p[-1].startswith("missing"):
        print("%s: FAIL " % tag + "; ".join(p))
        return None, None
    pair = d["pair"]
    if not isinstance(pair, dict) or not str(pair.get("coo_half", "")).strip() or not str(pair.get("cto_half", "")).strip():
        p.append("pair needs coo_half and cto_half commits")
    if d["ledger_closed"] is not True:
        p.append("the ledger entry is not closed")
    rb = d["rollback"]
    if not isinstance(rb, dict) or rb.get("recorded") is not True or not str(rb.get("how", "")).strip():
        p.append("rollback needs recorded true and how")
    return d, p


def retire(a):
    d, p = _act("RETIRE", a, ("order", "read_at", "decision_ref", "target", "consumers_before", "change", "after_read", "pair", "rollback", "ledger_closed", "claim"))
    if d is None:
        return 1
    cb = d["consumers_before"]
    if not isinstance(cb, dict) or cb.get("consumers") != 0 or not isinstance(cb.get("scanned"), int) or cb["scanned"] <= 0:
        p.append("consumers_before needs scanned > 0 and consumers 0")
    if not str(d["decision_ref"]).strip() or not isinstance(d["change"], dict) or not str(d["change"].get("commit", "")).strip():
        p.append("decision_ref and change.commit are required")
    ar = d["after_read"]
    if not isinstance(ar, dict) or ar.get("absent") is not True or not str(ar.get("evidence", "")).strip():
        p.append("after_read needs absent true and evidence")
    if p:
        print("RETIRE: FAIL " + "; ".join(p[:6]))
        return 1
    print("RETIRE: OK target=%s consumers=0" % d["target"])
    return 0


def move(a):
    d, p = _act("MOVE", a, ("order", "read_at", "trigger", "old_target_present", "new_target_present", "exercised", "pair", "rollback", "ledger_closed", "claim"))
    if d is None:
        return 1
    if d["old_target_present"] is not False or d["new_target_present"] is not True:
        p.append("the old target must read absent and the new present")
    ex = d["exercised"]
    if not isinstance(ex, dict) or not str(ex.get("event", "")).strip() or ex.get("result") != "fired" or not str(ex.get("evidence", "")).strip():
        p.append("exercised needs event, result fired and evidence")
    if p:
        print("MOVE: FAIL " + "; ".join(p[:6]))
        return 1
    print("MOVE: OK trigger=%s" % d["trigger"])
    return 0


def guarddiff(a):
    """FB-m-1: the guard is PURELY ADDITIVE against a pinned base blob (no existing line changed or removed)."""
    import difflib
    import subprocess
    try:
        base = subprocess.run(["git", "-C", a.root, "show", a.base_blob], capture_output=True, timeout=30, check=True).stdout.decode("utf-8", "replace").splitlines()
        cur = open(a.file, "rb").read().decode("utf-8", "replace").splitlines()
    except (OSError, subprocess.SubprocessError) as e:
        print("GUARDDIFF: FAIL cannot read: %s" % type(e).__name__)
        return 1
    sm = difflib.SequenceMatcher(None, base, cur, autojunk=False)
    ins = 0
    bad = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "insert":
            ins += j2 - j1
        elif tag in ("replace", "delete"):
            bad.append("%s at base line %d-%d" % (tag, i1 + 1, i2))
    if bad:
        print("GUARDDIFF: FAIL an existing line changed or was removed: " + "; ".join(bad[:4]))
        return 1
    if ins == 0 or ins > a.max_insert:
        print("GUARDDIFF: FAIL inserted lines %d (want 1 to %d)" % (ins, a.max_insert))
        return 1
    print("GUARDDIFF: OK inserted=%d changed=0" % ins)
    return 0


def readyhalt(a):
    """FB-m-2: the deployed readiness halt, three arms read live."""
    raw, d = _load(a.file, "READYHALT")
    if d is None:
        return 1
    p = _common("READYHALT", raw, d, ("order", "read_at", "signal", "deployed", "arms", "pair", "rollback", "ledger_closed", "claim"))
    if p and p[-1].startswith("missing"):
        print("READYHALT: FAIL " + "; ".join(p))
        return 1
    sg = d["signal"]
    if not isinstance(sg, dict) or not str(sg.get("key", "")).strip() or not str(sg.get("writer", "")).strip() or "pipeline-complete.json" in str(sg.get("key")):
        p.append("signal needs a key and a single writer, and the key is not the Door 6 marker")
    dp = d["deployed"]
    if not isinstance(dp, dict) or len(str(dp.get("code_sha256", ""))) != 44 and len(str(dp.get("code_sha256", ""))) != 64:
        p.append("deployed needs the function CodeSha256")
    ar = d["arms"]
    ok = isinstance(ar, dict) and all(k in ar for k in ("complete", "incomplete", "log"))
    if not ok:
        p.append("arms needs complete, incomplete and log")
    else:
        if ar["complete"].get("published") is not True:
            p.append("arm complete: published must be true")
        inc = ar["incomplete"]
        if inc.get("halted") is not True or inc.get("listing_before") is None or inc.get("listing_before") != inc.get("listing_after") or not isinstance(inc.get("listing_before"), int):
            p.append("arm incomplete: halted true and the bucket listing equal before and after (integers)")
        lg = ar["log"]
        if lg.get("names_date") is not True or lg.get("names_signal") is not True:
            p.append("arm log: the halt line must name the date and the missing signal")
    pair = d["pair"]
    if not isinstance(pair, dict) or not str(pair.get("coo_half", "")).strip() or not str(pair.get("cto_half", "")).strip():
        p.append("pair needs coo_half and cto_half commits")
    rb = d["rollback"]
    if not isinstance(rb, dict) or rb.get("recorded") is not True or not str(rb.get("how", "")).strip():
        p.append("rollback needs recorded true and how")
    if d["ledger_closed"] is not True:
        p.append("the ledger entry is not closed")
    if p:
        print("READYHALT: FAIL " + "; ".join(p[:6]))
        return 1
    print("READYHALT: OK signal=%s arms=3" % d["signal"]["key"])
    return 0


TF_BUCKETS = ("opal-data-49financial", "opal-data-inflection", "opal-data-cottonwood")
TF_ORIGINS = {"https://opalinvest.dev", "https://www.opalinvest.dev", "http://localhost:5174"}
TF_ALLOWS = {"opal-data-49financial": 0, "opal-data-inflection": 3, "opal-data-cottonwood": 1}


def tradeform(a):
    """FB-n-1: the trade-form fence apply (three policies, the Allow-append, three CORS rules), one scoped apply, read back."""
    raw, d = _load(a.file, "TRADEFORM")
    if d is None:
        return 1
    p = _common("TRADEFORM", raw, d, ("order", "read_at", "preconditions", "plan", "applied", "after", "pair", "rollback", "ledger_closed", "claim"))
    if p and p[-1].startswith("missing"):
        print("TRADEFORM: FAIL " + "; ".join(p))
        return 1
    pc = d["preconditions"]
    if not isinstance(pc, dict):
        p.append("preconditions must be an object")
    else:
        cnt = pc.get("prefix_object_counts")
        if not isinstance(cnt, dict) or sorted(cnt) != sorted(TF_BUCKETS) or any(cnt[b] != 0 for b in cnt):
            p.append("preconditions.prefix_object_counts needs all three buckets at 0")
        if pc.get("role_exists") is not True or pc.get("rows_at_head") != 3:
            p.append("preconditions needs role_exists true and rows_at_head 3")
        if pc.get("baseline_part1") != "No changes":
            p.append("baseline_part1 must read exactly 'No changes'")
        b2 = pc.get("baseline_part2")
        if not isinstance(b2, dict) or b2.get("inflection_allows_added") != 2 or b2.get("cottonwood_allows_added") != 0:
            p.append("baseline_part2 needs inflection_allows_added 2 and cottonwood_allows_added 0")
        if pc.get("prior_policy_saved") is not True or pc.get("prior_cors_absent") is not True:
            p.append("the prior policy JSON must be saved and the prior CORS read absent")
        if pc.get("m02_open_apply_on_inflection") is not False:
            p.append("m02_open_apply_on_inflection must be false (sequenced, never two open applies)")
    pl = d["plan"]
    if not isinstance(pl, dict) or (pl.get("add"), pl.get("change"), pl.get("destroy"), pl.get("statements_removed")) != (3, 3, 0, 0):
        p.append("plan must read add 3, change 3, destroy 0, statements_removed 0")
    ap_ = d["applied"]
    if not isinstance(ap_, dict) or ap_.get("apply_count") != 1 or ap_.get("targets") != 6 or not str(ap_.get("commit", "")).strip():
        p.append("applied needs apply_count 1, targets 6 and the apply commit")
    af = d["after"]
    bk = af.get("buckets") if isinstance(af, dict) else None
    if not isinstance(bk, dict) or sorted(bk) != sorted(TF_BUCKETS):
        p.append("after.buckets must name exactly the three buckets")
    else:
        for b in TF_BUCKETS:
            r = bk[b]
            cors = r.get("cors") if isinstance(r, dict) else None
            if not isinstance(r, dict) or r.get("policy_read_back") is not True or r.get("other_principals_byte_unchanged") is not True:
                p.append("%s: policy_read_back and other_principals_byte_unchanged must be true" % b)
            if not isinstance(cors, dict) or set(cors.get("origins", [])) != TF_ORIGINS or len(cors.get("origins", [])) != 3 \
                    or sorted(cors.get("methods", [])) != ["GET", "PUT"] or cors.get("max_age") != 300:
                p.append("%s: cors needs exactly the three origins, GET and PUT, max_age 300" % b)
        if af.get("allows_added_by_this_apply") != TF_ALLOWS:
            p.append("allows_added_by_this_apply must equal inflection 3, cottonwood 1, 49financial 0")
    pair = d["pair"]
    if not isinstance(pair, dict) or not str(pair.get("coo_half", "")).strip() or not str(pair.get("cto_half", "")).strip():
        p.append("pair needs coo_half and cto_half commits")
    rb = d["rollback"]
    if not isinstance(rb, dict) or rb.get("recorded") is not True or not str(rb.get("how", "")).strip():
        p.append("rollback needs recorded true and how")
    if d["ledger_closed"] is not True:
        p.append("the ledger entry is not closed")
    if p:
        print("TRADEFORM: FAIL " + "; ".join(p[:6]))
        return 1
    print("TRADEFORM: OK buckets=3 applies=1")
    return 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    pl = sub.add_parser("plan")
    pl.add_argument("--file", required=True)
    pl.add_argument("--firm", required=True)
    pl.add_argument("--min", type=int, default=5)
    pl.add_argument("--require-text", nargs="*", default=[])
    ce = sub.add_parser("census")
    ce.add_argument("--file", required=True)
    ce.add_argument("--min", type=int, default=10)
    for nm in ("retire", "move", "readyhalt", "tradeform"):
        q = sub.add_parser(nm)
        q.add_argument("--file", required=True)
    gd = sub.add_parser("guarddiff")
    gd.add_argument("--root", required=True)
    gd.add_argument("--file", required=True)
    gd.add_argument("--base-blob", required=True)
    gd.add_argument("--max-insert", type=int, default=120)
    a = ap.parse_args()
    return {"plan": plan, "census": census, "retire": retire, "move": move, "readyhalt": readyhalt, "tradeform": tradeform, "guarddiff": guarddiff}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
