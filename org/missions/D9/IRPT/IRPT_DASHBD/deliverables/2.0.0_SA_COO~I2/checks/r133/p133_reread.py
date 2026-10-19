"""IRPT_DASHBD round 133, workstream B-IN (issuer 2.0.0_SA_COO~I2) -- the RE-READ with the boundary on the next trading day (cell DB-i-22).

CTO round-132 analysis (enrichment E3): once E1 (DB-i-20) is merged and the Scope feed has landed a second day, re-run the live read
on every landed day. The record is the round-132 record in full (every count recounted from the private extract, trading days from
lib/trading_calendar.py, accounts x trading days = PRESENT + ABSENT, 0 unaccounted, the manifest agreement per day) PLUS:

  DBI133-3-AC1  everything round 132's checker grades (this checker calls it on the new record), and
                (a) two or more landed days; (b) run_scope_feed_real.py holds next_trading_day (E1 is in the module that ran);
                (c) the boundary measure reports its PAIR COUNT: at least 1, and pairs, pairs_equal and max_rel_diff_bp all equal the
                checker's recount from the private extract's boundary_rows (status, start and end value per hashed account and day),
                pairing each day with the next trading day of lib/trading_calendar.py.

The extract adds one key to round 132's: boundary_rows = {"<sha256 of the account id string>|<day>": [status, start, end]}.

Usage: python -I <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python -I <this file> --selftest [<repo_root>]
"""
import copy
import hashlib
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT_DEFAULT = HERE.parents[8]
D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~320/SCOPE_REREAD_R133.json"
SCRIPT_REL = D + "0.9.0_WK_IRPT_DASHBD~316/run_scope_feed_real.py"
EQUAL_TOL = 0.005


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


P132 = _load("p132_live_for_r133", HERE.parent / "r132" / "p132_live.py")
P133B = _load("p133_boundary_for_reread", HERE / "p133_boundary.py")
Fail, need, sha = P132.Fail, P132.need, P132.sha


def recount_boundary(extract, calendar_root):
    rows = extract["boundary_rows"]
    need(rows, "the extract holds no boundary_rows")
    sys.path.insert(0, str(calendar_root))
    from lib import trading_calendar as tc
    import datetime as dt

    def nxt(day):
        n = tc.first_trading_day_on_or_after(dt.date.fromisoformat(day) + dt.timedelta(days=1))
        return None if n is None else n.isoformat()

    pairs = equal = 0
    worst = None
    for key, (status, start, end) in rows.items():
        acct, day = key.split("|")
        if status != "RETURNED" or end is None:
            continue
        partner = nxt(day)
        other = rows.get(acct + "|" + partner) if partner else None
        if other is None or other[0] != "RETURNED" or other[1] is None:
            continue
        diff = abs(end - other[1])
        rel = diff / max(abs(other[1]), 1e-9) * 1e4
        pairs += 1
        equal += diff <= EQUAL_TOL
        worst = rel if worst is None or rel > worst else worst
    return {"pairs": pairs, "pairs_equal": equal, "max_rel_diff_bp": None if worst is None else round(worst, 2)}


def check(root, rec_rel=REC_REL, calendar_root=None):
    root = Path(root)
    calendar_root = Path(calendar_root) if calendar_root else root
    P132.check(root, rec_rel=rec_rel, calendar_root=calendar_root)          # everything round 132 graded, on this record
    rec = json.loads((root / rec_rel).read_bytes().decode("ascii"))
    need(rec["days_total"] >= 2, "fewer than two landed days: %r" % rec["days_total"])
    src = (root / SCRIPT_REL).read_bytes().decode("ascii")
    need("def next_trading_day(" in src, "run_scope_feed_real.py has no next_trading_day: E1 (DB-i-20) is not in the module that ran")
    extract = json.loads(Path(rec["extract"]["path"]).read_bytes().decode("utf-8"))
    want = recount_boundary(extract, calendar_root)
    got = rec["run"]["boundary"]
    need(set(got) == set(want), "run.boundary keys: %s" % sorted(got))
    for k, v in want.items():
        need(got[k] == v, "boundary.%s: record %r recount %r" % (k, got[k], v))
    need(want["pairs"] >= 1, "the boundary measure reports 0 pairs: the re-read measured nothing")


# ---- self-test ---------------------------------------------------------------------------------------------------------------
def build_good(root, td):
    """A GOOD record from the feed's own writer (Friday and Monday runs) and the REFERENCE module (E1 in place)."""
    root = Path(root)
    real = root / SCRIPT_REL
    ref_src = P133B.reference_source(real.read_bytes().decode("ascii"))
    mod = P133B.load_variant(ref_src, real, "rsfr_reread_ref")
    silver = P133B.feed_scenario(root, [("2026-10-09", ["2026-10-09"]), ("2026-10-12", ["2026-10-12"])])
    out = Path(td) / "out"
    run = mod.run_real(P133B.P131.P129.FakeReader({"scope_account_returns": silver}), str(out), [str(a) for a in P133B.ACCOUNTS],
                       P133B.P131.weekdays, "FIRM-SYNTH", 0, 400)
    days, brows = {}, {}
    for name, frame in silver.items():
        d = name[len("date="):]
        days[d] = {"silver_rows": int(len(frame)), "universe_rows": int(len(frame)), "households_failed": 0,
                   "call_row_counts": [int(len(frame))], "households_without_id": 0}
        for r in frame.to_dict("records"):
            def num(v):
                return None if v is None or v != v else float(v)
            brows["%s|%s" % (hashlib.sha256(str(int(r["account_id"])).encode()).hexdigest(), d)] = [r["status"], num(r.get("start_market_value")), num(r.get("end_market_value"))]
    extract = {"days": days, "boundary_rows": brows}
    ex_path = Path(td) / "extract.json"
    ex_path.write_text(json.dumps(extract))
    live = Path(td) / "repo"
    (live / D / "0.9.0_WK_IRPT_DASHBD~320").mkdir(parents=True)
    (live / SCRIPT_REL).parent.mkdir(parents=True, exist_ok=True)
    (live / SCRIPT_REL).write_bytes(ref_src.encode("ascii"))
    sp = live / D / "0.9.0_WK_IRPT_DASHBD~320" / "reread.py"
    sp.write_bytes(b"from inflection_account_dim import InflectionSilverReader\nfrom lib import trading_calendar\nreader = InflectionSilverReader()\n")
    want = P132.recompute({"days": days}, root)
    rec = {"script": {"file": sp.relative_to(live).as_posix(), "sha256": sha(sp.read_bytes())},
           "extract": {"path": str(ex_path), "sha256": sha(ex_path.read_bytes())}, "run": run, **want,
           "expected_rows": run["accounts_in_feed"] * want["trading_days_in_window"], "rows_accounted": run["rows_present"] + run["rows_absent"],
           "verdict": "MANIFEST_AGREES", "reads": {"s3_reads": 9, "s3_writes": 0, "dynamodb_writes": 0, "vendor_calls": 0, "secret_reads": 0},
           "files_in_repo_private": False, "served_values_changed": False, "pushed": False, "deployed": False, "basis_words": "w" * 220}
    (live / REC_REL).write_text(json.dumps(rec))
    return live, rec, ex_path, extract


def selftest(root):
    root = Path(root).resolve()
    with tempfile.TemporaryDirectory() as td:
        live, rec, ex_path, extract = build_good(root, td)
        need(rec["run"]["boundary"]["pairs"] == 1 and rec["days_total"] == 4, "selftest world drifted: %r" % rec["run"]["boundary"])
        sp_rel = SCRIPT_REL
        good_module = (live / sp_rel).read_bytes()

        def trial(label, mutate=None, extract_mutate=None, module_bytes=None, expect_fail=True):
            r = copy.deepcopy(rec)
            if mutate:
                mutate(r)
            if extract_mutate:
                e = copy.deepcopy(extract)
                extract_mutate(e)
                ex_path.write_text(json.dumps(e))
                r["extract"]["sha256"] = sha(ex_path.read_bytes())
            if module_bytes is not None:
                (live / sp_rel).write_bytes(module_bytes)
            (live / REC_REL).write_text(json.dumps(r))
            try:
                check(live, calendar_root=root)
                got_fail, why = False, ""
            except Fail as exc:
                got_fail, why = True, str(exc)[:60]
            finally:
                ex_path.write_text(json.dumps(extract))
                (live / sp_rel).write_bytes(good_module)
            need(got_fail == expect_fail, "selftest %s: expected %s" % (label, "FAIL" if expect_fail else "PASS"))
            print("selftest %-34s -> %s" % (label, ("FAIL (%s)" % why) if got_fail else "PASS"))

        trial("GOOD", expect_fail=False)
        trial("pairs overstated", lambda r: r["run"]["boundary"].update(pairs=2))
        trial("pairs_equal overstated", lambda r: r["run"]["boundary"].update(pairs_equal=1))
        trial("max diff changed", lambda r: r["run"]["boundary"].update(max_rel_diff_bp=999.0))
        trial("zero pairs reported", lambda r: r["run"]["boundary"].update(pairs=0, pairs_equal=0, max_rel_diff_bp=None))
        trial("E1 not in the module", module_bytes=b"def measure_boundary(silver):\n    return 0, 0, None\n")
        trial("one landed day only", lambda r: r.update(days_total=1))
        monday_key = hashlib.sha256(b"7001").hexdigest() + "|2026-10-12"
        trial("a boundary row changed", extract_mutate=lambda e: e["boundary_rows"].__setitem__(monday_key, ["RETURNED", 55.0, 60.0]))
        trial("wrong verdict", lambda r: r.update(verdict="MANIFEST_DISAGREES"))
        trial("a date in the record", lambda r: r.update(basis_words=r["basis_words"] + " 2026-10-16"))
    print("selftest PASS")


def main(argv):
    if len(argv) >= 2 and argv[1] == "--selftest":
        try:
            selftest(argv[2] if len(argv) > 2 else ROOT_DEFAULT)
        except Fail as exc:
            print("REASON: %s" % exc)
            print("selftest FAIL")
            return 1
        return 0
    root, cid = Path(argv[1]).resolve(), argv[2]
    try:
        need(cid == "DBI133-3-AC1", "unknown criterion %s" % cid)
        check(root)
    except FileNotFoundError as exc:
        print("REASON: no such file: %s" % Path(str(exc.filename)).name)
        print("%s FAIL" % cid)
        return 1
    except Fail as exc:
        print("REASON: %s" % exc)
        print("%s FAIL" % cid)
        return 1
    except Exception as exc:  # a crash is a FAIL with its type named, never a pass
        print("REASON: %s: %s" % (type(exc).__name__, str(exc)[:300]))
        print("%s FAIL" % cid)
        return 1
    print("%s PASS" % cid)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
