"""IRPT_DASHBD round 138, workstream B-49F (issuer 2.0.0_SA_COO~D2) -- DB-b-271, the HOUSEHOLDS CLAIM of the Cottonwood report-build handler (CTO half of the report-build
pair, msg 8573, question 3): the backfill reads the NEWEST account_dim for every day, so each filled day's object carries `households_as_of` and `households_claim: held` in its schema,
and each built day counts, never silently dropping, the accounts that have a return row on the day but belong to no household of that account_dim and the households that have no
account return row on the day (counts only, no id). LOCAL: nothing is planned, applied, uploaded or deployed.

  DB-b-271 (~220)   infra/aws/lambda/investor-reporting/reporting-gold-cot/handler.py (+ tests/), a facts record
                    DB138-1-AC1 (static: every round-137 clause, the claim words present; the grant),
                    DB138-1-AC2 (the PROBE: every round-137 scenario still passes; the day's one object carries the two claim keys in its parquet schema metadata and the table's columns are unchanged;
                                 the result states households_as_of (the newest account_dim date), households_claim held, accounts_dropped and households_no_rows; no id reaches the output),
                    DB138-1-AC3 (the worker's tests pass; the facts record equals the recount)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                       the pure clauses on synthetic arms
"""
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("p137", str(HERE.parent / "r137" / "p137_unreported.py"))
p137 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(p137)
p135, p131 = p137.p135, p137.p131

D = p131.D
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~220/RD_COT_HOUSEHOLDS_CLAIM_FACTS_R138.json"
ORDER_REL = "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-271.cottonwood-report-build-handler-households-claim-and-counts.md"
AUTHOR = "0.9.0_WK_IRPT_DASHBD~220"
HANDLER_REL, TEST_DIR = p131.HANDLER_REL, p131.TEST_DIR
GRANT_PREFIXES = ("infra/aws/lambda/investor-reporting/reporting-gold-cot/", D + "0.9.0_WK_IRPT_DASHBD~220/", "org/missions/D9/IRPT/IRPT_DASHBD/surprise-channel/investigations/",
                  "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/")
KEYS = ("households_as_of", "households_claim", "accounts_dropped", "households_no_rows")
LONG_DIGITS = re.compile(r"\d{8,}")
Fail, need = p131.Fail, p131.need


def own_commits(root):
    base, _ = p131.git(root, "log", "--diff-filter=A", "--format=%H", "--", ORDER_REL)
    need(base.split(), "the order's first commit is not in this history")
    out, _ = p131.git(root, "log", "--reverse", "--format=%H", "--author=" + AUTHOR, base.split()[-1] + "..HEAD")
    need(out.split(), "no commit by %s since the order was issued" % AUTHOR)
    return out.split()


# ------------------------------------------------------------------------------------------------ the pure clauses
def check_static(src):
    p137.check_static(src)
    need("households_as_of" in src and "households_claim" in src and "accounts_dropped" in src and "households_no_rows" in src,
         "the handler never holds the claim words households_as_of, households_claim, accounts_dropped and households_no_rows")
    return True


def check_grant(changed):
    bad = [f for f in changed if not f.startswith(GRANT_PREFIXES)]
    need(not bad, "the worker's commits touch files outside its grant: %s" % bad[:3])
    need(HANDLER_REL in changed, "the handler was not changed")
    return True


def check_households(res):
    s = res["scenarios"]
    a = s["hh_std"]
    r = a["result"]
    need("failed" not in r and r.get("rows", 0) > 0, "the standard day must still build: %s" % r)
    need(r.get("households_as_of") == a["dim_newest"], "households_as_of must be the newest account_dim date %s: %s" % (a["dim_newest"], r.get("households_as_of")))
    need(r.get("households_claim") == "held", "households_claim must read exactly 'held': %s" % r.get("households_claim"))
    need(r.get("accounts_dropped") == 0 and r.get("households_no_rows") == a["expect_no_rows"], "counts on the standard day: dropped 0, households with no rows %s: %s" % (a["expect_no_rows"], r))
    need(a["puts"] == [a["expected_key"]], "the day must put exactly once, at %s: %s" % (a["expected_key"], a["puts"]))
    need(a["put_meta"].get("households_as_of") == a["dim_newest"] and a["put_meta"].get("households_claim") == "held",
         "the day's object must carry households_as_of and households_claim held in its parquet schema metadata: %s" % a["put_meta"])
    need(a["put_columns_ok"] is True, "the object's columns must stay the filled table's columns, in order")
    e = s["hh_extra"]
    need(e["result"].get("accounts_dropped") == e["expect_dropped"], "accounts with a return row and no household must be counted (%s): %s" % (e["expect_dropped"], e["result"].get("accounts_dropped")))
    need(e["leak"] == [], "an id reached the output or the result: %s" % e["leak"])
    n = s["hh_newest"]["result"]
    need(n.get("households_as_of") == s["hh_newest"]["dim_newest"], "with two account_dim partitions households_as_of must be the newer: %s" % n.get("households_as_of"))
    d = s["hh_dry"]
    need(d["puts"] == [] and all(k in d["result"] for k in KEYS), "a dry run puts nothing and still states the four keys: %s" % d)
    return True


def check_facts(rec):
    exp = {"claim_location", "claim_keys", "counts", "claim", "words"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["claim_location"] == "parquet schema metadata of the day's one object" and rec["claim_keys"] == ["households_as_of", "households_claim"], "claim_location or claim_keys")
    need(rec["counts"] == ["accounts_dropped", "households_no_rows"] and rec["claim"] == "held", "counts or claim")
    need(isinstance(rec["words"], str) and 80 <= len(rec["words"]) <= 1800 and not LONG_DIGITS.findall(rec["words"]), "words must be one paragraph of 80 to 1800 characters with no long digit run")
    return True


# ------------------------------------------------------------------------------------------------ the probe (child interpreter)
EXTRA = r'''
# ---- round 138: the households claim and counts
import contextlib
import re as re_
def meta_of(f, key):
    body = f.store[(GB, key)]
    md = pq.read_schema(io.BytesIO(body)).metadata or {}
    return {k.decode(): v.decode() for k, v in md.items() if k.decode().startswith("households_")}, pq.read_table(io.BytesIO(body)).schema.names == frv.COLUMNS

f = full_store(set(), dt.date(2026, 7, 13)); ek_ = addr("filled_report_values", "2026-07-13")[1]
out = H.lambda_handler({"day": "2026-07-13"}, None, s3=f)
meta, cols_ok = meta_of(f, f.puts[0]) if f.puts else ({}, False)
S["hh_std"] = {"result": out["result"], "puts": list(f.puts), "expected_key": ek_, "put_meta": meta, "put_columns_ok": cols_ok, "dim_newest": "2026-07-13", "expect_no_rows": 1}

f = full_store(set(), dt.date(2026, 7, 13))
b_, k_ = addr("account_return_daily", "2026-07-13")
f._p(b_, k_, tbl_bytes(returns("2026-07-13", ["A1", "A2", "A3", "ZZ9", "ZZ8"])))
cap = io.StringIO()
with contextlib.redirect_stdout(cap):
    out = H.lambda_handler({"day": "2026-07-13"}, None, s3=f)
blob = cap.getvalue() + json.dumps(out, default=str)
S["hh_extra"] = {"result": out["result"], "expect_dropped": 2, "leak": sorted(set(re_.findall(r"\b(ZZ9|ZZ8|HH1|HH2|HH9|A1|A2|A3|H1)\b", blob)))}

f = full_store(set(), dt.date(2026, 7, 13))
b_, k_ = addr("account_dim", "2026-07-14")
f._p(b_, k_, tbl_bytes(pa.table({"account_id": ["A1", "A2", "A3", "H1"], "household_id": ["HH1", "HH1", "HH2", "HH9"]})))
out = H.lambda_handler({"day": "2026-07-13"}, None, s3=f)
S["hh_newest"] = {"result": out["result"], "dim_newest": "2026-07-14"}

f = full_store(set(), dt.date(2026, 7, 13))
out = H.lambda_handler({"day": "2026-07-13", "dry_run": True}, None, s3=f)
S["hh_dry"] = {"result": out["result"], "puts": list(f.puts)}
print(json.dumps(res))
'''


def probe_source():
    base = p137.probe_source()
    i = base.rindex("print(json.dumps(res))")
    return base[:i] + EXTRA.replace("print(json.dumps(res))\n", "", 1) + base[i:]


def run_probe(root):
    with tempfile.TemporaryDirectory() as td, tempfile.TemporaryDirectory() as cwd:
        p131.stage(root, td)
        r = subprocess.run([sys.executable, "-I", "-c", probe_source(), td], cwd=cwd, capture_output=True, text=True, timeout=900)
        need(r.returncode == 0, "the probe died (rc %s): %s" % (r.returncode, (r.stderr or r.stdout)[-500:].replace("\n", " | ")))
        line = [ln for ln in r.stdout.splitlines() if ln.startswith("{")]
        need(line, "the probe printed no result: %s" % (r.stderr or r.stdout)[-300:])
        return json.loads(line[-1])


def run(root, cid):
    root = Path(root)
    src = (root / HANDLER_REL).read_text(encoding="utf-8")
    if cid == "DB138-1-AC1":
        check_static(src)
        changed = set()
        for c in own_commits(root):
            changed |= set(p131.git(root, "show", "--name-only", "--format=", c)[0].split())
        check_grant(changed)
        print("OK: static: every round-137 clause holds and the handler holds the claim words; %d files changed, all in the grant" % len(changed))
        return True
    if cid in ("DB138-1-AC2", "DB138-1-AC3"):
        n = p131.run_tests(root) if cid == "DB138-1-AC3" else 0
        res = run_probe(root)
        need(res.get("import_ok") is True, "the staged handler does not import: %s" % res.get("import_error"))
        p135.check_guard(res)
        p137.check_unreported(res)
        check_households(res)
        if cid == "DB138-1-AC2":
            print("OK: probe: every round-137 scenario passes; the day's one object carries households_as_of and households_claim held in its schema metadata with the columns unchanged; "
                  "the result states the newest account_dim date, held, the dropped-account count and the no-rows household count; no id reaches the output")
            return True
        check_facts(json.loads((root / REC_REL).read_text(encoding="utf-8")))
        print("OK: %d worker tests pass and name cottonwood only; the probe passes again; facts record equals the recount" % n)
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest():
    import copy

    def red(fn, label):
        try:
            fn()
        except Fail:
            return
        raise AssertionError("red arm passed: " + label)
    good_src = ('import json\nimport pyarrow as pa\nimport filled_report_values as frv\nFLOOR_DAY = "2026-07-10"\n'
                'def lambda_handler(event, context=None, s3=None):\n    s3.put_object(Bucket="b", Key="k", Body=b"")\n    lam.invoke(FunctionName="f", InvocationType="Event", Payload=b"")\n'
                'def g(m):\n    return (m["contract_version"], m["method_version"], "manifest.json", "%d trading days not reported by the source (%s)",\n'
                '            "households_as_of", "households_claim", "accounts_dropped", "households_no_rows")\n')
    assert check_static(good_src)
    red(lambda: check_static(good_src.replace("accounts_dropped", "x")), "claim word lost")
    red(lambda: check_static(good_src.replace("not reported by the source", "missing")), "round-137 clause lost")
    assert check_grant({HANDLER_REL, TEST_DIR + "t.py"})
    red(lambda: check_grant({HANDLER_REL, "lib/x.py"}), "outside grant")
    red(lambda: check_grant({TEST_DIR + "t.py"}), "no handler")
    ok = {"scenarios": {
        "hh_std": {"result": {"rows": 4, "households_as_of": "2026-07-13", "households_claim": "held", "accounts_dropped": 0, "households_no_rows": 1}, "puts": ["k"], "expected_key": "k",
                   "put_meta": {"households_as_of": "2026-07-13", "households_claim": "held"}, "put_columns_ok": True, "dim_newest": "2026-07-13", "expect_no_rows": 1},
        "hh_extra": {"result": {"accounts_dropped": 2}, "expect_dropped": 2, "leak": []},
        "hh_newest": {"result": {"households_as_of": "2026-07-14"}, "dim_newest": "2026-07-14"},
        "hh_dry": {"result": {k: 0 for k in KEYS}, "puts": []}}}
    assert check_households(copy.deepcopy(ok))
    arms = (("failed", lambda r: r["scenarios"]["hh_std"]["result"].update(failed="x")), ("as_of", lambda r: r["scenarios"]["hh_std"]["result"].update(households_as_of="2026-07-10")),
            ("claim", lambda r: r["scenarios"]["hh_std"]["result"].update(households_claim="measured")), ("dropped nonzero", lambda r: r["scenarios"]["hh_std"]["result"].update(accounts_dropped=1)),
            ("no_rows", lambda r: r["scenarios"]["hh_std"]["result"].update(households_no_rows=0)), ("two puts", lambda r: r["scenarios"]["hh_std"].update(puts=["k", "k"])),
            ("meta lacks claim", lambda r: r["scenarios"]["hh_std"].update(put_meta={"households_as_of": "2026-07-13"})), ("meta as_of", lambda r: r["scenarios"]["hh_std"]["put_meta"].update(households_as_of="x")),
            ("columns moved", lambda r: r["scenarios"]["hh_std"].update(put_columns_ok=False)), ("dropped not counted", lambda r: r["scenarios"]["hh_extra"]["result"].update(accounts_dropped=0)),
            ("id leaks", lambda r: r["scenarios"]["hh_extra"].update(leak=["ZZ9"])), ("newest dim", lambda r: r["scenarios"]["hh_newest"]["result"].update(households_as_of="2026-07-13")),
            ("dry puts", lambda r: r["scenarios"]["hh_dry"].update(puts=["k"])), ("dry lacks key", lambda r: r["scenarios"]["hh_dry"]["result"].pop("accounts_dropped")))
    for label, fn in arms:
        r = copy.deepcopy(ok)
        fn(r)
        red(lambda: check_households(r), label)
    rec = {"claim_location": "parquet schema metadata of the day's one object", "claim_keys": ["households_as_of", "households_claim"], "counts": ["accounts_dropped", "households_no_rows"],
           "claim": "held", "words": "w" * 100}
    assert check_facts(rec)
    for label, fn in (("location", lambda r: r.update(claim_location="manifest")), ("keys", lambda r: r.update(claim_keys=["households_as_of"])), ("counts", lambda r: r.update(counts=[])),
                      ("claim", lambda r: r.update(claim="measured")), ("words", lambda r: r.update(words="short")), ("extra", lambda r: r.update(z=1)),
                      ("digits", lambda r: r.update(words="w" * 100 + " 123456789"))):
        r2 = dict(rec)
        fn(r2)
        red(lambda: check_facts(r2), label)
    assert "hh_std" in probe_source() and "full_store" in probe_source()
    print("selftest: static (2 red arms), grant (2), households (%d red arms) and facts (7 red arms) clauses behave" % len(arms))
    print("selftest PASS")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        selftest()
        sys.exit(0)
    try:
        run(sys.argv[1], sys.argv[2])
        print(sys.argv[2] + " PASS")
    except Exception as e:  # a failed read or probe is a FAIL, not a traceback
        print("FAIL: " + str(e))
        print(sys.argv[2] + " FAIL")
        sys.exit(1)
