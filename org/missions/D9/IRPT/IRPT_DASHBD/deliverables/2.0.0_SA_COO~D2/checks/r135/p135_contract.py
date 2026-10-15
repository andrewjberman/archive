"""IRPT_DASHBD round 135, workstream B-49F (issuer 2.0.0_SA_COO~D2) -- DB-b-267, the CONTRACT GUARD of the Cottonwood report-build handler (CTO ROUND-128 ANALYSIS ADDENDUM 2 @45b66b34e7, row
IRPT_DASHBD-D2-S92, msg 8491): the table `irpt/cottonwood/gold/account_return_daily` holds two eras under one name (Commonwealth: 3,325 dates to 2026-06-22, method_version 3, an asof/firm_scope
manifest; Black Diamond: dates from 2026-07-10, method_version 2, a business_date/contract_version 0.3.0 manifest; a 12-trading-day gap). The ruling: the consumer NEVER chains across a contract.
The handler (round 131) already never lists a partition before the 2026-07-10 floor; this cell makes the guard independent of the date: it reads EACH returns partition's manifest, requires one
(contract_version, method_version) across the partitions it uses, refuses (the day is FILLED_SKIPPED, nothing written) when they differ or a manifest names none, states the era it used in its result
(`returns_from`, `contract`), and a test spans 2026-06-22 and 2026-07-10 and shows the Commonwealth partition never opened and the windows that reach before the floor reading NOT_SPANNED in words.
LOCAL: nothing is planned, applied, uploaded or deployed. (The handler is the bundle's root file: its bytes change here, before the report-build pair is written.)

  DB-b-267 (~217)   infra/aws/lambda/investor-reporting/reporting-gold-cot/handler.py (+ tests/), a facts record
                    DB135-1-AC1 (static: the handler's source reads manifest.json and keeps every earlier clause: imports, one put, one Event invoke, the floor, no other firm; the grant),
                    DB135-1-AC2 (the PROBE: the earlier scenarios, and the contract guard: a consistent era builds and states its floor and contract; a mixed or unnamed contract refuses with
                                 zero puts; the 2026-06-22 partition is never opened or listed; the real build reads NOT_SPANNED in words for a window reaching before the floor),
                    DB135-1-AC3 (the worker's tests pass and span the two eras; the facts record equals the recount)

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
_spec = importlib.util.spec_from_file_location("p131", str(HERE.parent / "r131" / "p131_cothandler.py"))
p131 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(p131)

D = p131.D
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~217/RD_COT_CONTRACT_GUARD_FACTS_R135.json"
ORDER_REL = "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-267.cottonwood-report-build-handler-contract-guard-two-eras.md"
AUTHOR = "0.9.0_WK_IRPT_DASHBD~217"
HANDLER_REL, TEST_DIR, FLOOR_DAY = p131.HANDLER_REL, p131.TEST_DIR, p131.FLOOR_DAY
GRANT_PREFIXES = ("infra/aws/lambda/investor-reporting/reporting-gold-cot/", D + "0.9.0_WK_IRPT_DASHBD~217/", "org/missions/D9/IRPT/IRPT_DASHBD/surprise-channel/investigations/",
                  "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/")
LONG_DIGITS = re.compile(r"\d{8,}")
Fail = p131.Fail
need = p131.need


def own_commits(root):
    base, _ = p131.git(root, "log", "--diff-filter=A", "--format=%H", "--", ORDER_REL)
    need(base.split(), "the order's first commit is not in this history")
    out, _ = p131.git(root, "log", "--reverse", "--format=%H", "--author=" + AUTHOR, base.split()[-1] + "..HEAD")
    need(out.split(), "no commit by %s since the order was issued" % AUTHOR)
    return out.split()


# ------------------------------------------------------------------------------------------------ the pure clauses
def check_static(src):
    p131.check_static(src)
    need("manifest.json" in src, "the handler never names manifest.json: the contract guard reads each partition's manifest")
    need("contract_version" in src and "method_version" in src, "the handler must read contract_version and method_version")
    return True


def check_grant(changed):
    bad = [f for f in changed if not f.startswith(GRANT_PREFIXES)]
    need(not bad, "the worker's commits touch files outside its grant: %s" % bad[:3])
    need(HANDLER_REL in changed, "the handler was not changed")
    return True


def check_guard(res):
    s = res["scenarios"]
    a = s["era_ok"]
    need(a["result"].get("rows", 0) > 0 and "failed" not in a["result"], "a consistent Black Diamond era must build: %s" % a["result"])
    need(a["result"].get("returns_from") == FLOOR_DAY, "the result must state the era's first day (returns_from %s): %s" % (FLOOR_DAY, a["result"].get("returns_from")))
    need(a["result"].get("contract") == {"contract_version": "0.3.0", "method_version": 2}, "the result must state the contract used: %s" % a["result"].get("contract"))
    need(a["history_touched"] == [], "a key of the Commonwealth partition was opened or listed: %s" % a["history_touched"][:3])
    need(a["manifests_read"] >= 2, "the guard must read each used partition's manifest (read %d)" % a["manifests_read"])
    need(a["puts"] == [a["expected_key"]], "the consistent era must put exactly once at %s: %s" % (a["expected_key"], a["puts"]))
    for name in ("contract_mixed", "contract_unnamed"):
        m = s[name]
        need("failed" in m["result"] and "contract" in str(m["result"]["failed"]).lower(), "%s must refuse by name (contract): %s" % (name, m["result"]))
        need(m["puts"] == [], "%s must write nothing: %s" % (name, m["puts"]))
    r = s["real_windows"]
    need(r["ran"] is True, "the real build did not run: %s" % r.get("error"))
    need(r["rows"] > 0 and r["history_touched"] == [], "the real build wrote no rows or opened the Commonwealth partition: %s" % r)
    need(r["not_spanned_rows"] >= 1, "no row reads NOT_SPANNED: a window reaching before the floor must read in words, not serve a number")
    need(r["early_window_status_rows"] >= 3 and r["early_window_status_not_spanned_violations"] == 0, "the qtd, ytd and last_12_months window status of an account must read NOT_SPANNED when the window reaches before the floor (rows %d, violations %d)" % (r["early_window_status_rows"], r["early_window_status_not_spanned_violations"]))
    return True


def check_facts(rec, recount):
    exp = {"era_guard", "floor_day", "stated", "windows_before_floor", "words"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["era_guard"] == recount["era_guard"] and rec["floor_day"] == FLOOR_DAY, "era_guard or floor_day differ from the recount")
    need(rec["stated"] == ["returns_from", "contract"], "stated must list returns_from and contract")
    need(rec["windows_before_floor"] == "NOT_SPANNED in words; no number is served", "windows_before_floor must say NOT_SPANNED in words; no number is served")
    need(isinstance(rec["words"], str) and 80 <= len(rec["words"]) <= 1800 and not LONG_DIGITS.findall(rec["words"]), "words must be one paragraph of 80 to 1800 characters with no long digit run")
    return True


# ------------------------------------------------------------------------------------------------ the probe (child interpreter)
PROBE = p131.PROBE.split("S = res[\"scenarios\"]")[0].replace("install_stubs()\n", "") + r'''
S = res["scenarios"]
import copy

def mf(contract, method, extra=None):
    d = {"business_date": "x"}
    if contract is not None: d["contract_version"] = contract
    if method is not None: d["method_version"] = method
    if extra: d.update(extra)
    return json.dumps(d).encode("utf-8")

def put_manifests(f, spec):
    for day, (c, m) in spec.items():
        b, k = addr("account_return_daily", day); f._p(b, k.replace("data.parquet", "manifest.json"), mf(c, m))

def store(spec):
    f = build_store(); put_manifests(f, spec); return f

BD = {"2026-07-10": ("0.3.0", 2), "2026-07-13": ("0.3.0", 2)}
COMMONWEALTH = {"2026-06-22": (None, 3)}
def history(f):
    ret_pref = addr("account_return_daily", "2000-01-03")[1].split("date=")[0]
    return [k for (op, b, k) in f.calls if "date=2026-06-22" in k or "date=2026-06" in k]

# stubs for the guard scenarios (the real build runs in the last scenario)
real_model = frv.load_model_module
real_bd, real_tr = frv.build_document, frv.to_rows
def stub_model(repo):
    m = real_model(repo)
    class M:
        SERVED_BUCKET, SERVED_KEY = m.SERVED_BUCKET, m.SERVED_KEY
        STEMS = m.STEMS
        @staticmethod
        def read_served_series(reader):
            reader.get_object(m.SERVED_BUCKET, m.SERVED_KEY)
            return {s: [(dt.date(2026, 7, 10), 0.0), (dt.date(2026, 7, 13), 0.0)] for s in m.STEMS}, {"source": "stub"}
        _model_lo = staticmethod(m._model_lo)
        windows_from_series = staticmethod(m.windows_from_series)
    return M
def stub_rows(doc, ref, firm, as_of, cv):
    r = {c: "x" for c in frv.COLUMNS}; r.update(firm=firm, household_ref=ref, as_of=as_of, value_number=None); return [r, dict(r, row_key="k2")]
frv.load_model_module = stub_model
frv.build_document = lambda members, ref, as_of, accounts, src, frontiers=None: {"ref": ref}
frv.to_rows = stub_rows

ek = addr("filled_report_values", "2026-07-13")[1]
f = store(dict(BD, **COMMONWEALTH)); out = H.lambda_handler({"day": "2026-07-13"}, None, s3=f)
S["era_ok"] = {"result": out["result"], "puts": list(f.puts), "expected_key": ek, "history_touched": history(f),
               "manifests_read": sum(1 for op, b, k in f.calls if op == "GET" and k.endswith("manifest.json") and "account_return_daily" in k)}
f = store(dict(BD, **{"2026-07-13": ("0.2.0", 2)})); out = H.lambda_handler({"day": "2026-07-13"}, None, s3=f)
S["contract_mixed"] = {"result": out["result"], "puts": list(f.puts)}
f = store(dict(BD, **{"2026-07-10": (None, None)})); out = H.lambda_handler({"day": "2026-07-13"}, None, s3=f)
S["contract_unnamed"] = {"result": out["result"], "puts": list(f.puts)}

# the real build (no stub of build_document / to_rows): windows that reach before the floor read NOT_SPANNED in words
frv.build_document, frv.to_rows = real_bd, real_tr
captured = []
def capture_rows(doc, ref, firm, as_of, cv):
    rows = real_tr(doc, ref, firm, as_of, cv); captured.extend(rows); return rows
frv.to_rows = capture_rows
real = {"ran": False}
try:
    f = store(dict(BD, **COMMONWEALTH)); out = H.lambda_handler({"day": "2026-07-13", "dry_run": True}, None, s3=f)
    r = out["result"]
    ns = [x for x in captured if x.get("absent_reason") and "NOT_SPANNED" in str(x["absent_reason"])]
    ws = [x for x in captured if str(x.get("member_id", "")).startswith("account.window_status.")]
    early = [x for x in ws if str(x["member_id"]).rsplit(".", 1)[-1] in ("qtd", "ytd", "last_12_months")]
    spliced = [x for x in early if x.get("value_text") != "NOT_SPANNED"]
    real = {"ran": "failed" not in r, "error": r.get("failed"), "rows": r.get("rows", 0), "history_touched": history(f), "not_spanned_rows": len(ns), "early_window_status_rows": len(early), "early_window_status_not_spanned_violations": len(spliced)}
except BaseException as e:
    real = {"ran": False, "error": "%s: %s" % (type(e).__name__, str(e)[:300])}
S["real_windows"] = real
print(json.dumps(res))
'''.replace("import copy\n", "import copy, re\n")


def run_probe(root):
    with tempfile.TemporaryDirectory() as td, tempfile.TemporaryDirectory() as cwd:
        p131.stage(root, td)
        r = subprocess.run([sys.executable, "-I", "-c", PROBE, td], cwd=cwd, capture_output=True, text=True, timeout=600)
        need(r.returncode == 0, "the probe died (rc %s): %s" % (r.returncode, (r.stderr or r.stdout)[-500:].replace("\n", " | ")))
        line = [ln for ln in r.stdout.splitlines() if ln.startswith("{")]
        need(line, "the probe printed no result: %s" % (r.stderr or r.stdout)[-300:])
        return json.loads(line[-1])


def run(root, cid):
    root = Path(root)
    src = (root / HANDLER_REL).read_text(encoding="utf-8")
    if cid == "DB135-1-AC1":
        check_static(src)
        changed = set()
        for c in own_commits(root):
            changed |= set(p131.git(root, "show", "--name-only", "--format=", c)[0].split())
        check_grant(changed)
        print("OK: static: every round-131 clause holds and the handler reads manifest.json with contract_version and method_version; %d files changed, all in the grant" % len(changed))
        return True
    if cid == "DB135-1-AC2":
        res = run_probe(root)
        need(res.get("import_ok") is True, "the staged handler does not import: %s" % res.get("import_error"))
        check_guard(res)
        print("OK: probe: a consistent era builds and states returns_from %s and its contract; a mixed contract and an unnamed contract refuse with zero puts; the Commonwealth partition is never listed or opened; the real build reads NOT_SPANNED in words for windows reaching before the floor" % FLOOR_DAY)
        return True
    if cid == "DB135-1-AC3":
        n = p131.run_tests(root)
        res = run_probe(root)
        check_guard(res)
        rec = json.loads((root / REC_REL).read_text(encoding="utf-8"))
        check_facts(rec, {"era_guard": "manifest contract_version and method_version of each returns partition used; one pair or refuse"})
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
                'def g(m):\n    return m["contract_version"], m["method_version"], "manifest.json"\n')
    assert check_static(good_src)
    red(lambda: check_static(good_src.replace("manifest.json", "m.json")), "no manifest")
    red(lambda: check_static(good_src.replace("contract_version", "cv")), "no contract_version")
    red(lambda: check_static(good_src + "# 49financial\n"), "other firm")
    assert check_grant({HANDLER_REL, TEST_DIR + "t.py", D + "0.9.0_WK_IRPT_DASHBD~217/x.json"})
    red(lambda: check_grant({HANDLER_REL, "lib/opal_naming.py"}), "outside grant")
    red(lambda: check_grant({TEST_DIR + "t.py"}), "no handler")
    ek = "k"
    ok = {"import_ok": True, "scenarios": {
        "era_ok": {"result": {"rows": 4, "returns_from": FLOOR_DAY, "contract": {"contract_version": "0.3.0", "method_version": 2}}, "puts": [ek], "expected_key": ek, "history_touched": [], "manifests_read": 2},
        "contract_mixed": {"result": {"failed": "SystemExit: REFUSED: spans 2 contracts"}, "puts": []}, "contract_unnamed": {"result": {"failed": "SystemExit: REFUSED: no contract_version"}, "puts": []},
        "real_windows": {"ran": True, "rows": 120, "history_touched": [], "not_spanned_rows": 8, "early_window_status_rows": 9, "early_window_status_not_spanned_violations": 0}}}
    assert check_guard(copy.deepcopy(ok))
    arms = (("no rows", lambda r: r["scenarios"]["era_ok"]["result"].update(rows=0)), ("no floor stated", lambda r: r["scenarios"]["era_ok"]["result"].pop("returns_from")),
            ("no contract stated", lambda r: r["scenarios"]["era_ok"]["result"].update(contract=None)), ("history", lambda r: r["scenarios"]["era_ok"].update(history_touched=["k"])),
            ("manifests", lambda r: r["scenarios"]["era_ok"].update(manifests_read=1)), ("puts", lambda r: r["scenarios"]["era_ok"].update(puts=[])),
            ("mixed built", lambda r: r["scenarios"]["contract_mixed"].update(result={"rows": 4})), ("mixed put", lambda r: r["scenarios"]["contract_mixed"].update(puts=["k"])),
            ("mixed reason", lambda r: r["scenarios"]["contract_mixed"].update(result={"failed": "boom"})), ("unnamed built", lambda r: r["scenarios"]["contract_unnamed"].update(result={"rows": 4})),
            ("unnamed put", lambda r: r["scenarios"]["contract_unnamed"].update(puts=["k"])), ("real not run", lambda r: r["scenarios"]["real_windows"].update(ran=False, error="x")),
            ("real history", lambda r: r["scenarios"]["real_windows"].update(history_touched=["k"])), ("no not_spanned", lambda r: r["scenarios"]["real_windows"].update(not_spanned_rows=0)),
            ("spliced window status", lambda r: r["scenarios"]["real_windows"].update(early_window_status_not_spanned_violations=1)), ("no window rows", lambda r: r["scenarios"]["real_windows"].update(early_window_status_rows=0)))
    for label, fn in arms:
        r = copy.deepcopy(ok)
        fn(r)
        red(lambda: check_guard(r), label)
    rec = {"era_guard": "manifest contract_version and method_version of each returns partition used; one pair or refuse", "floor_day": FLOOR_DAY, "stated": ["returns_from", "contract"],
           "windows_before_floor": "NOT_SPANNED in words; no number is served", "words": "w" * 100}
    recount = {"era_guard": rec["era_guard"]}
    assert check_facts(rec, recount)
    for label, fn in (("guard", lambda r: r.update(era_guard="x")), ("floor", lambda r: r.update(floor_day="2026-01-01")), ("stated", lambda r: r.update(stated=["a"])),
                      ("windows", lambda r: r.update(windows_before_floor="spliced")), ("words", lambda r: r.update(words="short")), ("extra", lambda r: r.update(z=1)),
                      ("digits", lambda r: r.update(words="w" * 100 + " 123456789"))):
        r2 = dict(rec)
        fn(r2)
        red(lambda: check_facts(r2, recount), label)
    print("selftest: static (5 red arms), grant (2), guard (%d red arms) and facts (7 red arms) clauses behave" % len(arms))
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
