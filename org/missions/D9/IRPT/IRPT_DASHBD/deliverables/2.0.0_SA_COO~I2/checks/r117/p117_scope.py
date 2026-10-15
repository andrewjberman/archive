"""IRPT_DASHBD round 117, workstream B-IN (issuer 2.0.0_SA_COO~I2) -- the Orion Scope probe (CTO round-117 analysis, ruling 2).

  DB-i-5 (~305) ONE Inflection household with 2 or more accounts, Orion's Reporting/Scope called with the Account grouping, with the fee flag `calcGrossOfFees` false and then true over
                one window: (a) does the response carry one Account group per account with a daily series, (b) is the fee flag honoured (equal returns, or a gap that ties to the summed
                feeAmount), (c) is the credential accepted. A vendor READ: no write; the raw responses stay in the private folder.                 DBI117-1-AC1

The checker RECOMPUTES from the private raw response bodies (their sha256 is in the record): the household by the selection rule (the lowest-sha household with 2 or more accounts in the private
account dimension), the Account groups of each response, and the three verdicts by the rule below. It never calls the vendor.

  groups(body): every dict with $type 'calculated-group' and grouping 'Account'; per group: id = str(groupEntityId); perf = the first numeric `performance` of a descendant
                $type 'calculated-performance'; points = the descendants carrying a numeric `factor`; fee = the sum of numeric `feeAmount` over the descendants;
                startv = the numeric `value` of the first descendant $type 'calculated-activity' with id 'startValue'.
  (a) ONE_GROUP_PER_ACCOUNT if the set of group ids equals the household's account ids and every group has perf and points >= 1; else FEWER_GROUPS (a subset), OTHER_GROUPS (not a subset).
  (b) IGNORED if every account's perf is equal (within 1e-12) between the false and the true response; else NET_WHEN_FALSE if every account with fee > 0 has obs = perf_true - perf_false >= 0 and
      |obs - fee/startv| <= max(1e-4, 0.25 * fee/startv) (and at least one such account); else DIFFERENT_UNTIED.
  (c) ACCEPTED if the false call returned 2xx; REFUSED if every call was refused (non-2xx).

Usage: python -I <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python -I <this file> --selftest [<repo_root>]         the pure helpers on synthetic arms
"""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("p114_bin", str(HERE.parent / "r114" / "p114_bin.py"))
P114 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(P114)
Fail, need = P114.Fail, P114.need

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~305/SCOPE_PROBE_R117.json"
DIM = P114.PRIV + "0.9.0_WK_IRPT_DASHBD~171/ACCOUNT_DIM_DRY_RUN.parquet"
MAX_CALLS = 4
A_VERDICTS = ("ONE_GROUP_PER_ACCOUNT", "FEWER_GROUPS", "OTHER_GROUPS", "REFUSED", "NOT_RUN")
B_VERDICTS = ("IGNORED", "NET_WHEN_FALSE", "DIFFERENT_UNTIED", "NOT_RUN")
C_VERDICTS = ("ACCEPTED", "REFUSED", "NOT_RUN")
STORES = ("secretsmanager", "s3_copy", "none")


def key_of(raw):
    if raw is None:
        return None
    if isinstance(raw, float):
        if raw != raw:
            return None
        if raw.is_integer():
            return str(int(raw))
    if isinstance(raw, int):
        return str(raw)
    text = str(raw).strip()
    return text or None


def walk(node):
    if isinstance(node, dict):
        yield node
        for v in node.values():
            yield from walk(v)
    elif isinstance(node, list):
        for v in node:
            yield from walk(v)


def _num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and x == x


def groups(body):
    out = {}
    for g in walk(body):
        if g.get("$type") != "calculated-group" or g.get("grouping") != "Account":
            continue
        gid = key_of(g.get("groupEntityId"))
        perf, points, fee, startv = None, 0, 0.0, None
        for n in walk(g):
            if n is g:
                continue
            if perf is None and n.get("$type") == "calculated-performance" and _num(n.get("performance")):
                perf = float(n["performance"])
            if _num(n.get("factor")):
                points += 1
            if _num(n.get("feeAmount")):
                fee += float(n["feeAmount"])
            if startv is None and n.get("$type") == "calculated-activity" and n.get("id") == "startValue" and _num(n.get("value")):
                startv = float(n["value"])
        out[gid] = {"perf": perf, "points": points, "fee": fee, "startv": startv}
    return out


def verdict_a(grp, account_ids):
    ids = set(grp)
    if not ids:
        return "OTHER_GROUPS"
    if ids == set(account_ids) and all(g["perf"] is not None and g["points"] >= 1 for g in grp.values()):
        return "ONE_GROUP_PER_ACCOUNT"
    if ids < set(account_ids):
        return "FEWER_GROUPS"
    return "OTHER_GROUPS"


def verdict_b(gf, gt):
    ids = sorted(set(gf) & set(gt))
    pairs = [(gf[i], gt[i]) for i in ids if gf[i]["perf"] is not None and gt[i]["perf"] is not None]
    if not pairs:
        return "NOT_RUN", 0, 0
    if all(abs(t["perf"] - f["perf"]) < 1e-12 for f, t in pairs):
        return "IGNORED", len(pairs), sum(1 for f, _ in pairs if f["fee"] > 0)
    fee_pairs = [(f, t) for f, t in pairs if f["fee"] > 0]
    ties = 0
    for f, t in fee_pairs:
        obs = t["perf"] - f["perf"]
        if f["startv"] is None or f["startv"] <= 0 or obs < 0:
            return "DIFFERENT_UNTIED", len(pairs), len(fee_pairs)
        exp = f["fee"] / f["startv"]
        if abs(obs - exp) <= max(1e-4, 0.25 * abs(exp)):
            ties += 1
        else:
            return "DIFFERENT_UNTIED", len(pairs), len(fee_pairs)
    return ("NET_WHEN_FALSE" if ties >= 1 else "DIFFERENT_UNTIED"), len(pairs), len(fee_pairs)


def household_choice():
    import pyarrow.parquet as pq
    rows = pq.read_table(DIM, columns=["account_id", "household_id"]).to_pylist()
    hh = {}
    for r in rows:
        a, h = key_of(r["account_id"]), key_of(r["household_id"])
        if a and h:
            hh.setdefault(h, set()).add(a)
    multi = {h: s for h, s in hh.items() if len(s) >= 2}
    need(multi, "no household with 2 or more accounts in the dimension")
    best = min(multi, key=lambda h: hashlib.sha256(h.encode("utf-8")).hexdigest())
    return hashlib.sha256(best.encode("utf-8")).hexdigest(), sorted(multi[best])


def check(root):
    rec = P114.load(root, REC_REL)
    P114.no_identifiers(rec)
    for k in ("served_values_changed", "pushed", "deployed", "files_in_repo_private"):
        need(rec.get(k) is False, "%s must be false" % k)
    r = rec.get("reads", {})
    for k in ("s3_writes", "dynamodb_writes"):
        need(r.get(k) == 0, "reads.%s must be 0" % k)
    need(isinstance(r.get("secret_reads"), int) and 0 <= r["secret_reads"] <= MAX_CALLS, "reads.secret_reads must be an integer within the call cap")
    need(isinstance(rec.get("basis_words"), str) and len(rec["basis_words"]) > 120, "basis_words missing")
    P114.script_clean(root, rec["script"]["file"], rec["script"]["sha256"])
    # the household, by the selection rule
    digest, accounts = household_choice()
    need(rec.get("household_sha256") == digest, "household differs from the selection rule (lowest-sha household with 2 or more accounts)")
    need(rec.get("accounts_in_household") == len(accounts), "accounts_in_household differs from the dimension")
    calls = rec.get("calls")
    need(isinstance(calls, list) and 1 <= len(calls) <= MAX_CALLS, "calls must be 1 to %d" % MAX_CALLS)
    need(rec.get("calls_made") == len(calls) and r.get("vendor_calls") == len(calls), "calls_made and reads.vendor_calls must equal the calls listed")
    bodies = {}
    for c in calls:
        need(c.get("gross_of_fees_flag") in (False, True), "call flag")
        need(isinstance(c.get("http_status"), int), "call http_status")
        need(c.get("ok") is (200 <= c["http_status"] < 300), "call ok disagrees with its status")
        if c["ok"]:
            f = c["response_file"]
            need(Path(f["path"]).is_file() and f["path"].replace("\\", "/").startswith(P114.PRIV), "response file absent or outside the private folder")
            need(P114.sha(f["path"]) == f["sha256"], "response file sha256 differs from the record")
            bodies.setdefault(c["gross_of_fees_flag"], json.loads(Path(f["path"]).read_text(encoding="utf-8")))
    need(rec.get("token_store_used") in STORES, "token_store_used")
    # (c)
    any_ok_false = any(c["ok"] and c["gross_of_fees_flag"] is False for c in calls)
    all_refused = all(not c["ok"] for c in calls)
    exp_c = "ACCEPTED" if any_ok_false else ("REFUSED" if all_refused else "NOT_RUN")
    need(rec["c_credential"]["verdict"] == exp_c, "c_credential.verdict differs from the recount (%s)" % exp_c)
    need(rec["c_credential"].get("claim") in P114.CLAIMS, "c claim")
    # (a)
    if False in bodies:
        gf = groups(bodies[False])
        exp_a = verdict_a(gf, accounts)
        need(rec["a_multi_account"].get("account_groups_returned") == len(gf), "a: account_groups_returned differs from the recount")
        need(rec["a_multi_account"].get("groups_with_daily_series") == sum(1 for g in gf.values() if g["points"] >= 1), "a: groups_with_daily_series differs from the recount")
    else:
        exp_a = "REFUSED" if all_refused else "NOT_RUN"
    need(rec["a_multi_account"]["verdict"] == exp_a, "a_multi_account.verdict differs from the recount (%s)" % exp_a)
    need(rec["a_multi_account"].get("claim") in P114.CLAIMS, "a claim")
    # (b)
    if False in bodies and True in bodies:
        exp_b, ncmp, nfee = verdict_b(groups(bodies[False]), groups(bodies[True]))
        need(rec["b_fee_basis"].get("accounts_compared") == ncmp and rec["b_fee_basis"].get("accounts_with_fee") == nfee, "b: counts differ from the recount")
    else:
        exp_b = "NOT_RUN"
    need(rec["b_fee_basis"]["verdict"] == exp_b, "b_fee_basis.verdict differs from the recount (%s)" % exp_b)
    need(rec["b_fee_basis"].get("claim") in P114.CLAIMS, "b claim")
    need(rec["a_multi_account"]["verdict"] in A_VERDICTS and rec["b_fee_basis"]["verdict"] in B_VERDICTS and rec["c_credential"]["verdict"] in C_VERDICTS, "verdict enum")


def selftest():
    arms = []

    def arm(name, ok):
        arms.append((name, ok))

    def g(gid, perf, fee, startv, points=2):
        pts = [{"factor": 1.0 + i / 1000.0, "feeAmount": fee / points} for i in range(points)]
        return {"$type": "calculated-group", "grouping": "Account", "groupEntityId": gid,
                "calculations": [{"$type": "calculated-activity", "id": "startValue", "value": startv},
                                 {"$type": "calculated-performance", "performance": perf}, {"series": pts}]}
    bf = {"calculations": [g(1, 0.010, 100.0, 100000.0), g(2, 0.020, 50.0, 50000.0)]}
    bt_net = {"calculations": [g(1, 0.011, 100.0, 100000.0), g(2, 0.021, 50.0, 50000.0)]}
    bt_same = {"calculations": [g(1, 0.010, 100.0, 100000.0), g(2, 0.020, 50.0, 50000.0)]}
    bt_off = {"calculations": [g(1, 0.030, 100.0, 100000.0), g(2, 0.021, 50.0, 50000.0)]}
    gf = groups(bf)
    arm("groups parse", sorted(gf) == ["1", "2"] and gf["1"]["points"] == 2 and abs(gf["1"]["fee"] - 100.0) < 1e-9 and gf["1"]["startv"] == 100000.0)
    arm("a one group per account", verdict_a(gf, ["1", "2"]) == "ONE_GROUP_PER_ACCOUNT")
    arm("a fewer groups", verdict_a(groups({"calculations": [g(1, 0.01, 1.0, 10.0)]}), ["1", "2"]) == "FEWER_GROUPS")
    arm("a other groups", verdict_a(gf, ["1", "3"]) == "OTHER_GROUPS")
    arm("b ignored", verdict_b(gf, groups(bt_same))[0] == "IGNORED")
    arm("b net when false", verdict_b(gf, groups(bt_net))[0] == "NET_WHEN_FALSE")
    arm("b untied", verdict_b(gf, groups(bt_off))[0] == "DIFFERENT_UNTIED")
    arm("b not run", verdict_b(gf, {})[0] == "NOT_RUN")
    arm("key_of", key_of(12.0) == "12" and key_of(" 7 ") == "7" and key_of(None) is None)
    for n, v in arms:
        print(("ok   " if v else "FAIL ") + n)
    return all(v for _, v in arms)


CHECKS = {"DBI117-1-AC1": check}


def main(argv):
    if argv and argv[0] == "--selftest":
        sys.exit(0 if selftest() else 1)
    if len(argv) != 2 or argv[1] not in CHECKS:
        print("usage: <root> DBI117-1-AC1")
        sys.exit(2)
    try:
        CHECKS[argv[1]](argv[0])
    except Fail as e:
        print("%s FAIL: %s" % (argv[1], e))
        print("%s FAIL" % argv[1])
        sys.exit(1)
    except Exception as e:  # a checker error is a FAIL, never a pass
        print("%s FAIL: checker error %s: %s" % (argv[1], type(e).__name__, e))
        print("%s FAIL" % argv[1])
        sys.exit(1)
    print("%s PASS" % argv[1])


if __name__ == "__main__":
    main(sys.argv[1:])
