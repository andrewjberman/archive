"""IRPT_DASHBD round 141, workstream B-49F (issuer 2.0.0_SA_COO~D2) -- DB-b-274, the CHAIN CAP of the Cottonwood report-build handler (CTO ROUND ANALYSIS rounds 133-137, ADDENDUM 1 term 4, msg 8615):
`chain_next` recomputes the owed days on every hop, so MAX_DAYS_PER_FIRE capped the owed LIST and not the CHAIN; one `{}` event (and, after a gap, one scheduled fire) would chain every owed day.
The cap must hold across the whole chain: an event without a budget starts one of MAX_DAYS_PER_FIRE days in all, each self-invoke carries `chain_left` less one, a hop with none left chains
nothing, and a budget outside 0 to MAX_DAYS_PER_FIRE-1 (or not an integer) is refused before any call. It lands BEFORE the reporting-gold schedule is enabled. LOCAL: nothing is deployed here.

  DB-b-274 (~222)   infra/aws/lambda/investor-reporting/reporting-gold-cot/handler.py (+ tests/), a facts record
                    DB141-1-AC1 (static: every round-138 clause, the budget words present; the grant),
                    DB141-1-AC2 (the PROBE: every round-138 scenario still passes; a whole chain driven through the fake builds exactly the cap and then stops; a short backlog stops at its end; an explicit day
                                 event is capped too; a bad budget refuses with zero calls; a dry run chains nothing; a budget of zero chains nothing),
                    DB141-1-AC3 (the worker's tests pass; the facts record equals the recount)

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
_spec = importlib.util.spec_from_file_location("p138", str(HERE.parent / "r138" / "p138_households.py"))
p138 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(p138)
p137, p135, p131 = p138.p137, p138.p135, p138.p131

D = p131.D
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~222/RD_COT_CHAIN_CAP_FACTS_R141.json"
ORDER_REL = "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-274.cottonwood-report-build-handler-chain-cap-across-the-whole-chain.md"
AUTHOR = "0.9.0_WK_IRPT_DASHBD~222"
HANDLER_REL, TEST_DIR = p131.HANDLER_REL, p131.TEST_DIR
GRANT_PREFIXES = ("infra/aws/lambda/investor-reporting/reporting-gold-cot/", D + "0.9.0_WK_IRPT_DASHBD~222/", "org/missions/D9/IRPT/IRPT_DASHBD/surprise-channel/investigations/",
                  "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/")
CAP = 10
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
    p138.check_static(src)
    need("chain_left" in src, "the handler never holds the budget word chain_left")
    return True


def check_grant(changed):
    bad = [f for f in changed if not f.startswith(GRANT_PREFIXES)]
    need(not bad, "the worker's commits touch files outside its grant: %s" % bad[:3])
    need(HANDLER_REL in changed, "the handler was not changed")
    return True


def check_cap(res):
    s = res["scenarios"]
    a = s["cap_full"]
    need(a["hops"] == CAP and len(a["days"]) == CAP and a["days"] == a["expected_first"], "a whole chain from `{}` over 32 owed days must build exactly %d days, the oldest first: %s" % (CAP, a["days"]))
    need(a["chain_left_seq"] == list(range(CAP - 2, -1, -1)), "each self-invoke must carry chain_left one less than the hop before (%s): %s" % (list(range(CAP - 2, -1, -1)), a["chain_left_seq"]))
    need(a["puts"] == CAP and a["last_chain_invoked"] is False, "the chain must put once per day and its last hop must chain nothing: %s" % a)
    sh = s["cap_short"]
    need(sh["hops"] == 4 and sh["days"] == sh["expected"] and sh["last_chain_invoked"] is False, "a backlog shorter than the cap must stop at its end: %s" % sh)
    ex = s["cap_explicit"]
    need(ex["hops"] == CAP and ex["days"][0] == "2026-07-14", "an explicit day event is capped at %d days in all: %s" % (CAP, ex))
    z = s["cap_zero"]
    need(z["puts"] == 1 and z["chain_invoked"] is False and z["invokes"] == [], "a budget of zero builds the day and chains nothing: %s" % z)
    bad = s["cap_bad"]
    need(bad and all(b["raised"] is True and b["calls"] == 0 for b in bad), "a bad budget must refuse before any call: %s" % [b for b in bad if not (b["raised"] and b["calls"] == 0)][:2])
    d = s["cap_dry"]
    need(d["puts"] == [] and d["invokes"] == [], "a dry run chains nothing and writes nothing: %s" % d)
    return True


def check_facts(rec):
    exp = {"cap", "payload_key", "budget_range", "applies_to", "words"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["cap"] == CAP and rec["payload_key"] == "chain_left" and rec["budget_range"] == [0, CAP - 1], "cap, payload_key or budget_range")
    need(rec["applies_to"] == ["empty event", "explicit day event", "scheduled fire"], "applies_to must list the three entry paths")
    need(isinstance(rec["words"], str) and 80 <= len(rec["words"]) <= 1800 and not LONG_DIGITS.findall(rec["words"]), "words must be one paragraph of 80 to 1800 characters with no long digit run")
    return True


# ------------------------------------------------------------------------------------------------ the probe (child interpreter)
EXTRA = r'''
# ---- round 141: the chain cap
class Lam2:
    def __init__(self): self.invokes = []
    def invoke(self, FunctionName, InvocationType, Payload, **kw): self.invokes.append({"FunctionName": FunctionName, "InvocationType": InvocationType, "payload": json.loads(Payload.decode("utf-8"))}); return {}

def drive(f, ev):
    lam = Lam2(); days = []; seq = []; last = None
    for _ in range(60):
        out = H.lambda_handler(ev, Ctx(), s3=f, lambda_client=lam)
        days.append(out.get("day")); last = out.get("chain") or {}
        if not last.get("invoked"): break
        ev = lam.invokes[-1]["payload"]; seq.append(ev.get("chain_left"))
    return days, seq, last, lam

all_days = [d.isoformat() for d in tc_.trading_days_between(dt.date(2026, 7, 10), dt.date(2026, 8, 24))]
f = full_store(set(), dt.date(2026, 8, 24)); days, seq, last, lam = drive(f, {})
S["cap_full"] = {"hops": len(days), "days": days, "expected_first": all_days[:10], "chain_left_seq": seq, "puts": len(f.puts), "last_chain_invoked": bool(last.get("invoked"))}
f = full_store(set(), dt.date(2026, 7, 15)); days, seq, last, lam = drive(f, {})
S["cap_short"] = {"hops": len(days), "days": days, "expected": [d.isoformat() for d in tc_.trading_days_between(dt.date(2026, 7, 10), dt.date(2026, 7, 15))], "last_chain_invoked": bool(last.get("invoked"))}
f = full_store(set(), dt.date(2026, 8, 24)); days, seq, last, lam = drive(f, {"day": "2026-07-14"})
S["cap_explicit"] = {"hops": len(days), "days": days}
f = full_store(set(), dt.date(2026, 8, 24)); lam = Lam2(); out = H.lambda_handler({"day": "2026-07-13", "chain_left": 0}, Ctx(), s3=f, lambda_client=lam)
S["cap_zero"] = {"puts": len(f.puts), "chain_invoked": bool((out.get("chain") or {}).get("invoked")), "invokes": lam.invokes}
bads = []
for badv in (10, -1, True, "3", 2.0, None, 99):
    f = full_store(set(), dt.date(2026, 7, 15)); lam = Lam2(); raised = False
    try: H.lambda_handler({"day": "2026-07-13", "chain_left": badv}, Ctx(), s3=f, lambda_client=lam)
    except (SystemExit, ValueError, TypeError): raised = True
    bads.append({"value": repr(badv), "raised": raised, "calls": len(f.calls) + len(lam.invokes)})
S["cap_bad"] = bads
f = full_store(set(), dt.date(2026, 8, 24)); lam = Lam2(); out = H.lambda_handler({"day": "2026-07-13", "dry_run": True, "chain_left": 5}, Ctx(), s3=f, lambda_client=lam)
S["cap_dry"] = {"puts": list(f.puts), "invokes": lam.invokes}
print(json.dumps(res))
'''


def probe_source():
    base = p138.probe_source()
    i = base.rindex("print(json.dumps(res))")
    return base[:i] + EXTRA.replace("print(json.dumps(res))\n", "", 1) + base[i:]


def run_probe(root):
    with tempfile.TemporaryDirectory() as td, tempfile.TemporaryDirectory() as cwd:
        p131.stage(root, td)
        r = subprocess.run([sys.executable, "-I", "-c", probe_source(), td], cwd=cwd, capture_output=True, text=True, timeout=1800)
        need(r.returncode == 0, "the probe died (rc %s): %s" % (r.returncode, (r.stderr or r.stdout)[-500:].replace("\n", " | ")))
        line = [ln for ln in r.stdout.splitlines() if ln.startswith("{")]
        need(line, "the probe printed no result: %s" % (r.stderr or r.stdout)[-300:])
        return json.loads(line[-1])


def run(root, cid):
    root = Path(root)
    src = (root / HANDLER_REL).read_text(encoding="utf-8")
    if cid == "DB141-1-AC1":
        check_static(src)
        changed = set()
        for c in own_commits(root):
            changed |= set(p131.git(root, "show", "--name-only", "--format=", c)[0].split())
        check_grant(changed)
        print("OK: static: every round-138 clause holds and the handler holds the budget word; %d files changed, all in the grant" % len(changed))
        return True
    if cid in ("DB141-1-AC2", "DB141-1-AC3"):
        n = p131.run_tests(root) if cid == "DB141-1-AC3" else 0
        res = run_probe(root)
        need(res.get("import_ok") is True, "the staged handler does not import: %s" % res.get("import_error"))
        p135.check_guard(res)
        p137.check_unreported(res)
        p138.check_households(res)
        check_cap(res)
        if cid == "DB141-1-AC2":
            print("OK: probe: every round-138 scenario passes; a whole chain from `{}` over 32 owed days builds exactly %d days then stops, each self-invoke carries chain_left one less; a short backlog stops "
                  "at its end; an explicit day event is capped; a budget of zero chains nothing; seven bad budgets refuse with zero calls; a dry run chains nothing" % CAP)
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
                '            "households_as_of", "households_claim", "accounts_dropped", "households_no_rows", "chain_left")\n')
    assert check_static(good_src)
    red(lambda: check_static(good_src.replace("chain_left", "x")), "budget word lost")
    red(lambda: check_static(good_src.replace("accounts_dropped", "x")), "round-138 clause lost")
    assert check_grant({HANDLER_REL, TEST_DIR + "t.py"})
    red(lambda: check_grant({HANDLER_REL, "lib/x.py"}), "outside grant")
    red(lambda: check_grant({TEST_DIR + "t.py"}), "no handler")
    days = ["2026-07-%02d" % d for d in range(10, 20)]
    ok = {"scenarios": {
        "cap_full": {"hops": CAP, "days": days, "expected_first": days, "chain_left_seq": list(range(CAP - 2, -1, -1)), "puts": CAP, "last_chain_invoked": False},
        "cap_short": {"hops": 4, "days": ["a", "b", "c", "d"], "expected": ["a", "b", "c", "d"], "last_chain_invoked": False},
        "cap_explicit": {"hops": CAP, "days": ["2026-07-14"] + ["x"] * 9},
        "cap_zero": {"puts": 1, "chain_invoked": False, "invokes": []},
        "cap_bad": [{"value": "10", "raised": True, "calls": 0}, {"value": "-1", "raised": True, "calls": 0}],
        "cap_dry": {"puts": [], "invokes": []}}}
    assert check_cap(copy.deepcopy(ok))
    arms = (("uncapped", lambda r: r["scenarios"]["cap_full"].update(hops=32, days=days + ["z"] * 22)), ("capped short", lambda r: r["scenarios"]["cap_full"].update(hops=9, days=days[:9])),
            ("not oldest", lambda r: r["scenarios"]["cap_full"].update(days=days[1:] + ["2026-07-20"])), ("budget not decreasing", lambda r: r["scenarios"]["cap_full"].update(chain_left_seq=[8] * 9)),
            ("no budget in payload", lambda r: r["scenarios"]["cap_full"].update(chain_left_seq=[None] * 9)), ("last chains", lambda r: r["scenarios"]["cap_full"].update(last_chain_invoked=True)),
            ("puts", lambda r: r["scenarios"]["cap_full"].update(puts=11)), ("short hops", lambda r: r["scenarios"]["cap_short"].update(hops=5)),
            ("short chains", lambda r: r["scenarios"]["cap_short"].update(last_chain_invoked=True)), ("explicit uncapped", lambda r: r["scenarios"]["cap_explicit"].update(hops=20)),
            ("explicit day", lambda r: r["scenarios"]["cap_explicit"].update(days=["2026-07-10"] + ["x"] * 9)), ("zero chains", lambda r: r["scenarios"]["cap_zero"].update(chain_invoked=True)),
            ("zero no put", lambda r: r["scenarios"]["cap_zero"].update(puts=0)), ("bad accepted", lambda r: r["scenarios"]["cap_bad"][0].update(raised=False)),
            ("bad calls", lambda r: r["scenarios"]["cap_bad"][1].update(calls=2)), ("dry puts", lambda r: r["scenarios"]["cap_dry"].update(puts=["k"])),
            ("dry chains", lambda r: r["scenarios"]["cap_dry"].update(invokes=[{}])))
    for label, fn in arms:
        r = copy.deepcopy(ok)
        fn(r)
        red(lambda: check_cap(r), label)
    rec = {"cap": CAP, "payload_key": "chain_left", "budget_range": [0, CAP - 1], "applies_to": ["empty event", "explicit day event", "scheduled fire"], "words": "w" * 100}
    assert check_facts(rec)
    for label, fn in (("cap", lambda r: r.update(cap=11)), ("key", lambda r: r.update(payload_key="left")), ("range", lambda r: r.update(budget_range=[0, CAP])), ("applies", lambda r: r.update(applies_to=[])),
                      ("words", lambda r: r.update(words="short")), ("extra", lambda r: r.update(z=1)), ("digits", lambda r: r.update(words="w" * 100 + " 123456789"))):
        r2 = dict(rec)
        fn(r2)
        red(lambda: check_facts(r2), label)
    assert "cap_full" in probe_source() and "hh_std" in probe_source()
    print("selftest: static (2 red arms), grant (2), cap (%d red arms) and facts (7 red arms) clauses behave" % len(arms))
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
