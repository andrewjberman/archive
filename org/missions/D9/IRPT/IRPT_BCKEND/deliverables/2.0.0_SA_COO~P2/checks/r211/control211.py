"""Positive control and negatives for p211_cells.py (run by the issuer at the cut, never by a worker).

Usage: python control211.py <real_repo_root>
Builds a temp tree holding the real lib/trading_calendar.py and a stub producer file, writes a clean synthetic record, runs every criterion expecting PASS, then applies
each mutation expecting the NAMED criterion to FAIL. The temp tree is removed.
"""
import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REAL = Path(sys.argv[1]).resolve()
CHECK = REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r211/p211_cells.py"
sys.path.insert(0, str(CHECK.parent.parent / "r196"))
sys.path.insert(0, str(CHECK.parent))
import p211_cells as P  # noqa: E402

PROD = "data/assets/scripts/gold/irpt_holdings_performance/holdings_performance.py"


def build():
    root = Path(tempfile.mkdtemp(prefix="c211_"))
    (root / "lib").mkdir()
    shutil.copy(REAL / "lib/trading_calendar.py", root / "lib/trading_calendar.py")
    (root / PROD).parent.mkdir(parents=True, exist_ok=True)
    lines = ["# stub"] * 80
    lines[9] = "DECLARATION = 'declaration.json'"
    lines[19] = "def holdings_return(prev_positions, day_positions):"
    lines[29] = "    g0.loc[earning, '_contrib'] = g0['_v'] * (g0['_p1'] / g0['_p0'] - 1.0)"
    lines[39] = "def _frame_for(s3, doc, source, day):"
    (root / PROD).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return root


def st(line, ident):
    return {"file": PROD, "line": line, "identifier": ident}


def firm(days):
    return {"source_found": True, "source_description": "the declared transactions source of the firm, read through the declaration entry", "columns_present": ["tran_srcde", "tr_cd", "sb_cd"],
            "split_days": days, "split_rows": 100, "split_security_days": 6, "measurable": 5, "ratio_absent": 1, "ratio_agrees_with_close": 5, "ratio_disagrees_with_close": 0}


def record():
    return {"base_commit": "a" * 40, "read_date": "2026-10-15",
            "producer": {"contribution_site": st(30, "g0['_p1'] / g0['_p0']"), "pure_core_site": st(20, "def holdings_return"), "partition_loader_site": st(40, "def _frame_for"),
                         "declaration_site": st(10, "DECLARATION"),
                         "quantity_basis_statement": "The price contribution is the t-1 value times the day-t price over the t-1 price minus one, so a split day's price drop reads as a loss."},
            "split_source": {"49financial": firm(["2026-04-21"]), "cottonwood": firm(["2026-04-21", "2026-06-17"]), "inflection": firm([])},
            "known_cusips_found_on_2026_04_21": 4,
            "delta_projection": {"account_days_affected": {"49financial": 300, "cottonwood": 200, "inflection": 420}, "total_account_days_affected": 920, "graded_disagreed_on_2026_04_21": 920,
                                 "claim": "inferred", "statement": "Each account that held a split security on a split day moves its price contribution; the count is the held account-days, derived from the positions partitions."},
            "design": {"adjustment_formula": "ratio = quantity after over quantity before on the same-day STK STOCK SPLIT row for an account with no same-day trade; the t-1 price is divided by the ratio before the contribution.",
                       "new_inputs": ["the custodian transactions rows of the split day, read through the declared source"], "reason_codes": ["SPLIT_RATIO_ABSENT", "SPLIT_UNADJUSTED_COMPARISON"]},
            "notes": ["read the declaration and the producer's pure core; counts only", "no CUSIP and no account id is recorded", "not read: the custodian's own system"],
            **{k: 0 for k in P.P6.BOUND}}


def write(root, rec):
    p = root / P.REC
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(rec, indent=1), encoding="utf-8")


def run(root, cid):
    p = subprocess.run([sys.executable, str(CHECK), str(root), cid], capture_output=True, text=True, timeout=120, env=dict(os.environ))
    return p.stdout.strip().splitlines()[-1] if p.stdout.strip() else "NOOUT " + p.stderr[-200:]


def sp(d, path, v):
    for k in path[:-1]:
        d = d[k]
    d[path[-1]] = v


MUTS = [
    ("AC1", "contribution_line_wrong", lambda r: sp(r, ["producer", "contribution_site", "line"], 3)),
    ("AC1", "core_not_holdings_return", lambda r: sp(r, ["producer", "pure_core_site"], st(10, "DECLARATION"))),
    ("AC1", "declaration_file_missing", lambda r: sp(r, ["producer", "declaration_site", "file"], "data/none.py")),
    ("AC1", "statement_short", lambda r: sp(r, ["producer", "quantity_basis_statement"], "short")),
    ("AC2", "firm_missing", lambda r: r["split_source"].pop("inflection")),
    ("AC2", "columns_wrong", lambda r: sp(r, ["split_source", "cottonwood", "columns_present"], ["tr_cd", "sb_cd"])),
    ("AC2", "split_day_not_trading", lambda r: sp(r, ["split_source", "cottonwood", "split_days"], ["2026-04-18", "2026-04-21"])),
    ("AC2", "measurable_sum_wrong", lambda r: sp(r, ["split_source", "49financial", "ratio_absent"], 3)),
    ("AC2", "close_sum_wrong", lambda r: sp(r, ["split_source", "49financial", "ratio_disagrees_with_close"], 2)),
    ("AC2", "apr21_missing", lambda r: (sp(r, ["split_source", "49financial", "split_days"], []), sp(r, ["split_source", "cottonwood", "split_days"], ["2026-06-17"]))),
    ("AC2", "cusips_over_four", lambda r: sp(r, ["known_cusips_found_on_2026_04_21"], 5)),
    ("AC2", "source_not_found_but_measured", lambda r: sp(r, ["split_source", "inflection"], {"source_found": False, "source_description": "the firm keeps no transaction feed in the declaration", "claim": "measured"})),
    ("AC3", "total_wrong", lambda r: sp(r, ["delta_projection", "total_account_days_affected"], 5)),
    ("AC3", "reason_code_missing", lambda r: sp(r, ["design", "reason_codes"], ["SPLIT_RATIO_ABSENT"])),
    ("AC3", "formula_short", lambda r: sp(r, ["design", "adjustment_formula"], "short")),
    ("AC3", "short_notes", lambda r: sp(r, ["notes"], ["short"])),
    ("AC3", "counter_nonzero", lambda r: sp(r, ["vendor_requests_sent"], 1)),
    ("AC3", "cusip_leaked", lambda r: sp(r, ["notes"], ["the CUSIP 921910816 leaked into this long enough line", "second line that is long enough to count here", "third line that is long enough to count here"])),
]
bad = 0


def expect(label, cid, root, want):
    global bad
    r = run(root, cid)
    ok = r == cid + (" PASS" if want else " FAIL")
    bad += 0 if ok else 1
    print("%s %-12s %-32s -> %s %s" % ("POSITIVE" if want else "NEGATIVE", cid, label, r, "" if ok else "<-- UNEXPECTED"))


root = build()
rec = record()
write(root, rec)
for ac in ("AC1", "AC2", "AC3"):
    expect("clean", "IB211-1-" + ac, root, True)
for ac, name, fn in MUTS:
    r = copy.deepcopy(rec)
    fn(r)
    write(root, r)
    expect(name, "IB211-1-" + ac, root, False)
shutil.rmtree(root, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
