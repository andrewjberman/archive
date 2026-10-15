"""IRPT_DASHBD round 137, workstream B-49F (issuer 2.0.0_SA_COO~D2) -- DB-b-269, the UNREPORTED-DAY STATEMENT of the Cottonwood report-build handler (CTO ROUND ANALYSIS rounds 130-132 @b3dc83e664,
ADDENDUM 1 @3204c9ab6d, msg 8524): three trading days (2026-08-19, 2026-09-24, 2026-09-25) have no Black Diamond gold partition because the source holds no flows for them. The ruling: no sidecar
write, no grant, no redeploy; the HANDLER takes the trading calendar minus the present Black Diamond partitions and states "N trading days not reported by the source (dates)" for any window that
holds them, NEVER filling a day. It follows round 135's contract guard (the same file) and comes before the report-build pair (the handler's bytes are in the bundle).
LOCAL: nothing is planned, applied, uploaded or deployed.

  DB-b-269 (~218)   infra/aws/lambda/investor-reporting/reporting-gold-cot/handler.py (+ tests/), a facts record
                    DB137-1-AC1 (static: every round-135 clause, the statement's words present; the grant),
                    DB137-1-AC2 (the PROBE: every round-135 scenario still passes, and a gap in the middle of a landed run: the day's result lists the unreported days, states the sentence,
                                 names which windows hold them, never reads or writes the absent day; a day before the gap states none),
                    DB137-1-AC3 (the worker's tests pass and span 2026-08-19; the facts record equals the recount)

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
_spec = importlib.util.spec_from_file_location("p135", str(HERE.parent / "r135" / "p135_contract.py"))
p135 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(p135)
p131 = p135.p131

D = p131.D
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~218/RD_COT_UNREPORTED_FACTS_R137.json"
ORDER_REL = "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-269.cottonwood-report-build-handler-unreported-trading-days-statement.md"
AUTHOR = "0.9.0_WK_IRPT_DASHBD~218"
HANDLER_REL, TEST_DIR, FLOOR_DAY = p131.HANDLER_REL, p131.TEST_DIR, p131.FLOOR_DAY
GRANT_PREFIXES = ("infra/aws/lambda/investor-reporting/reporting-gold-cot/", D + "0.9.0_WK_IRPT_DASHBD~218/", "org/missions/D9/IRPT/IRPT_DASHBD/surprise-channel/investigations/",
                  "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/")
SENTENCE = re.compile(r"\d+ trading days not reported by the source \(\d{4}-\d{2}-\d{2}(, \d{4}-\d{2}-\d{2})*\)\Z")
WINDOWS = ("qtd", "ytd", "last_12_months", "since_inception")
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
    p135.check_static(src)
    need("not reported by the source" in src and "trading days" in src, "the handler never holds the statement's words 'trading days not reported by the source'")
    return True


def check_grant(changed):
    bad = [f for f in changed if not f.startswith(GRANT_PREFIXES)]
    need(not bad, "the worker's commits touch files outside its grant: %s" % bad[:3])
    need(HANDLER_REL in changed, "the handler was not changed")
    return True


def check_unreported(res):
    s = res["scenarios"]
    g = s["gap"]
    r = g["result"]
    need("failed" not in r and r.get("rows", 0) > 0, "the day after a gap must still build: %s" % r)
    need(r.get("unreported_days") == [g["gap_day"]], "unreported_days must be exactly [%s]: %s" % (g["gap_day"], r.get("unreported_days")))
    need(isinstance(r.get("statement"), str) and SENTENCE.match(r["statement"]) and r["statement"] == "1 trading days not reported by the source (%s)" % g["gap_day"],
         "the statement must read '1 trading days not reported by the source (%s)': %s" % (g["gap_day"], r.get("statement")))
    w = r.get("windows")
    need(isinstance(w, dict) and sorted(w) == sorted(WINDOWS), "windows must name %s: %s" % (WINDOWS, w))
    need(all(w[n] == [g["gap_day"]] for n in WINDOWS), "every window of the day holds the gap day and lists it: %s" % w)
    need(g["gap_keys_touched"] == [], "the absent day was listed, read or written: %s" % g["gap_keys_touched"][:3])
    need(g["puts"] == [g["expected_key"]], "the day must put exactly once, at %s, never a filled absent day: %s" % (g["expected_key"], g["puts"]))
    c = s["clear"]["result"]
    need("failed" not in c and c.get("unreported_days") == [] and c.get("statement") is None and all(c.get("windows", {}).get(n) == [] for n in WINDOWS),
         "a day before the gap must state no unreported day: %s" % c)
    ne = s["narrow"]["result"]
    need("failed" not in ne and ne.get("unreported_days") == [s["narrow"]["gap_day"]] and ne["windows"].get("qtd") == [] and ne["windows"].get("since_inception") == [s["narrow"]["gap_day"]],
         "a window that does not reach the gap must not list it, one that does must: %s" % ne)
    return True


def check_facts(rec):
    exp = {"rule", "statement_form", "windows", "fills", "words"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["rule"] == "the trading calendar from the era's first day to the day, minus the present Black Diamond returns partitions", "rule differs from the ruling")
    need(rec["statement_form"] == "N trading days not reported by the source (dates)" and rec["windows"] == list(WINDOWS) and rec["fills"] == "never", "statement_form, windows or fills")
    need(isinstance(rec["words"], str) and 80 <= len(rec["words"]) <= 1800 and not LONG_DIGITS.findall(rec["words"]), "words must be one paragraph of 80 to 1800 characters with no long digit run")
    return True


# ------------------------------------------------------------------------------------------------ the probe (child interpreter)
EXTRA = r'''
# ---- round 137: a gap in the middle of a landed run
import trading_calendar as tc_
frv.build_document = lambda members, ref, as_of, accounts, src, frontiers=None: {"ref": ref}
frv.to_rows = stub_rows

def full_store(skip, end=dt.date(2026, 8, 24)):
    f = build_store()
    f.store = {k: v for k, v in f.store.items() if "account_return_daily" not in k[1]}
    for d in tc_.trading_days_between(dt.date(2026, 7, 10), end):
        iso = d.isoformat()
        if iso in skip: continue
        b, k = addr("account_return_daily", iso)
        f._p(b, k, tbl_bytes(returns(iso, ["A1", "A2", "A3"]))); f._p(b, k.replace("data.parquet", "manifest.json"), mf("0.3.0", 2))
    return f

GAP = "2026-08-19"
f = full_store({GAP}); out = H.lambda_handler({"day": "2026-08-21"}, None, s3=f)
S["gap"] = {"result": out["result"], "gap_day": GAP, "puts": list(f.puts), "expected_key": addr("filled_report_values", "2026-08-21")[1],
            "gap_keys_touched": [k for (op, b, k) in f.calls if "date=" + GAP in k]}
f = full_store({GAP}); out = H.lambda_handler({"day": "2026-08-18"}, None, s3=f)
S["clear"] = {"result": out["result"]}
# a window that does not reach the gap: a gap on 2026-07-14 and an as-of in the next quarter (2026-10-02): the quarter-to-date window starts 2026-10-01 and must not list it
GAP2 = "2026-07-14"
f = full_store({GAP2}, end=dt.date(2026, 10, 2)); out = H.lambda_handler({"day": "2026-10-02"}, None, s3=f)
res_n = out["result"]
S["narrow"] = {"result": res_n, "gap_day": GAP2}
print(json.dumps(res))
'''


def probe_source():
    base = p135.PROBE
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
    if cid == "DB137-1-AC1":
        check_static(src)
        changed = set()
        for c in own_commits(root):
            changed |= set(p131.git(root, "show", "--name-only", "--format=", c)[0].split())
        check_grant(changed)
        print("OK: static: every round-135 clause holds and the handler holds the statement's words; %d files changed, all in the grant" % len(changed))
        return True
    if cid in ("DB137-1-AC2", "DB137-1-AC3"):
        if cid == "DB137-1-AC3":
            n = p131.run_tests(root)
        res = run_probe(root)
        need(res.get("import_ok") is True, "the staged handler does not import: %s" % res.get("import_error"))
        p135.check_guard(res)
        check_unreported(res)
        if cid == "DB137-1-AC2":
            print("OK: probe: every round-135 scenario passes; a day after a gap lists exactly the absent day, states '1 trading days not reported by the source (<date>)', names the windows that hold it, never lists, reads or writes the absent day and puts once; a day before the gap states none; a gap before a later window's start is not listed there")
            return True
        rec = json.loads((root / REC_REL).read_text(encoding="utf-8"))
        check_facts(rec)
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
                'def g(m):\n    return m["contract_version"], m["method_version"], "manifest.json", "%d trading days not reported by the source (%s)"\n')
    assert check_static(good_src)
    red(lambda: check_static(good_src.replace("not reported by the source", "missing")), "no statement words")
    red(lambda: check_static(good_src.replace("manifest.json", "m.json")), "round-135 clause lost")
    assert check_grant({HANDLER_REL, TEST_DIR + "t.py"})
    red(lambda: check_grant({HANDLER_REL, "lib/x.py"}), "outside grant")
    red(lambda: check_grant({TEST_DIR + "t.py"}), "no handler")
    gap = "2026-08-19"
    ok = {"scenarios": {
        "gap": {"result": {"rows": 4, "unreported_days": [gap], "statement": "1 trading days not reported by the source (%s)" % gap, "windows": {n: [gap] for n in WINDOWS}}, "gap_day": gap, "gap_keys_touched": [],
                "puts": ["k"], "expected_key": "k"},
        "clear": {"result": {"rows": 4, "unreported_days": [], "statement": None, "windows": {n: [] for n in WINDOWS}}},
        "narrow": {"result": {"rows": 4, "unreported_days": ["2026-07-14"], "statement": "1 trading days not reported by the source (2026-07-14)", "windows": {"qtd": [], "ytd": ["2026-07-14"], "last_12_months": ["2026-07-14"], "since_inception": ["2026-07-14"]}}, "gap_day": "2026-07-14"}}}
    assert check_unreported(copy.deepcopy(ok))
    arms = (("failed", lambda r: r["scenarios"]["gap"]["result"].update(failed="x")), ("no list", lambda r: r["scenarios"]["gap"]["result"].update(unreported_days=[])),
            ("wrong day", lambda r: r["scenarios"]["gap"]["result"].update(unreported_days=["2026-08-20"])), ("statement text", lambda r: r["scenarios"]["gap"]["result"].update(statement="1 days missing")),
            ("statement none", lambda r: r["scenarios"]["gap"]["result"].update(statement=None)), ("windows keys", lambda r: r["scenarios"]["gap"]["result"].update(windows={"qtd": [gap]})),
            ("a window lacks it", lambda r: r["scenarios"]["gap"]["result"]["windows"].update(ytd=[])), ("absent touched", lambda r: r["scenarios"]["gap"].update(gap_keys_touched=["k"])),
            ("filled put", lambda r: r["scenarios"]["gap"].update(puts=["k", "date=2026-08-19"])), ("no put", lambda r: r["scenarios"]["gap"].update(puts=[])),
            ("clear states", lambda r: r["scenarios"]["clear"]["result"].update(unreported_days=[gap])), ("clear statement", lambda r: r["scenarios"]["clear"]["result"].update(statement="x")),
            ("clear window", lambda r: r["scenarios"]["clear"]["result"]["windows"].update(qtd=[gap])), ("narrow lists in qtd", lambda r: r["scenarios"]["narrow"]["result"]["windows"].update(qtd=["2026-07-14"])),
            ("narrow misses since inception", lambda r: r["scenarios"]["narrow"]["result"]["windows"].update(since_inception=[])))
    for label, fn in arms:
        r = copy.deepcopy(ok)
        fn(r)
        red(lambda: check_unreported(r), label)
    rec = {"rule": "the trading calendar from the era's first day to the day, minus the present Black Diamond returns partitions", "statement_form": "N trading days not reported by the source (dates)",
           "windows": list(WINDOWS), "fills": "never", "words": "w" * 100}
    assert check_facts(rec)
    for label, fn in (("rule", lambda r: r.update(rule="x")), ("form", lambda r: r.update(statement_form="x")), ("windows", lambda r: r.update(windows=["qtd"])), ("fills", lambda r: r.update(fills="sometimes")),
                      ("words", lambda r: r.update(words="short")), ("extra", lambda r: r.update(z=1)), ("digits", lambda r: r.update(words="w" * 100 + " 123456789"))):
        r2 = dict(rec)
        fn(r2)
        red(lambda: check_facts(r2), label)
    assert "print(json.dumps(res))" in probe_source() and "full_store" in probe_source()
    print("selftest: static (3 red arms), grant (2), unreported (%d red arms) and facts (7 red arms) clauses behave" % len(arms))
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
