#!/usr/bin/env python3
"""TO-V3-1 -- OFF-CELL PROBE: can a DRY RUN of the guarded seeder discriminate?

The round-5 decomposition's downstream cell AT5-s-8 (R1) is recorded as running
"your guarded seeder's dry run after the retag and expects 0 PRESERVED".

The applied guard computes its conflicts at :295 as
    conflicts = _yang_conflicts(yang_table, sec) if upload else []
so on the dry-run path the conflict list is [] BY CONSTRUCTION, before any
comparison happens. This probe measures whether "0 PRESERVED" from a dry run
therefore carries any information.

METHOD: the SAME conflicting baseline used by the mutant control -- every retag
member carrying its ratified five-class value, which the seeder disagrees with
-- run three ways against the APPLIED bytes:
    A  upload=True   (the guard's live path)     -- expected to REFUSE
    B  upload=False  (the dry-run path)          -- the question
    C  upload=False, NO conflict in the store    -- the negative baseline
If B and C read identically, a dry run cannot distinguish "nothing would be
clobbered" from "four rows would be clobbered".

SCRATCH ONLY. boto3 is faked; no live table is opened.
"""
import importlib.util
import io
import os
import sys
import types
from contextlib import redirect_stdout

ROOT = os.getcwd()
REPO_PATH = "data/black_diamond/scripts/classification/seed_canonical_securities.py"

_spec = importlib.util.spec_from_file_location(
    "re_ctl", os.path.join(ROOT, ".scratch", "v3_mutant_control_re.py"))
re_ctl = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(re_ctl)
ac1 = re_ctl.ac1


def exercise(src, upload, conflicting, label):
    yang = re_ctl.ScratchTableWithGet(ac1.YANG_TABLE)
    bd = re_ctl.ScratchTableWithGet(ac1.BD_TABLE)
    secs = ac1.canonical_securities(src)
    by_ticker = {s["ticker"]: s for s in secs}
    retag_names = dict(ac1.RETAG)
    mint_probe = next(s["ticker"] for s in secs if s["ticker"] not in retag_names)
    if conflicting:
        yang.store = ac1.baseline(by_ticker, mint_probe)
    else:
        # the SAME rows, but already agreeing with the seeder -- no conflict exists
        yang.store = {}
        for ticker, _five in ac1.RETAG:
            if ticker not in by_ticker:
                continue
            sec = by_ticker[ticker]
            yang.store[ticker] = {
                "ticker": ticker, "asset_class": sec["asset_class"],
                "sub_asset_class": sec["sub_asset_class"], "name": sec["name"],
                "management_style": "passive", "sector": "Broad",
            }
    present = [t for t, _ in ac1.RETAG if t in by_ticker]
    before = {t: yang.store[t]["asset_class"] for t in present}

    tables = {ac1.YANG_TABLE: yang, ac1.BD_TABLE: bd}
    saved = sys.modules.get("boto3")
    sys.modules["boto3"] = ac1.make_fake_boto3(tables)
    buf = io.StringIO()
    rc = None
    try:
        mod = types.ModuleType("probe_%s" % abs(hash(label)))
        mod.__name__ = "probe_%s" % abs(hash(label))
        with redirect_stdout(buf):
            exec(compile(src, REPO_PATH, "exec"), mod.__dict__)
            rc = mod.seed(upload=upload, sync_yang=True)
    finally:
        sys.modules["boto3"] = saved if saved is not None else sys.modules.pop("boto3")
    out = buf.getvalue()
    after = {t: yang.store[t]["asset_class"] for t in present}
    return {
        "label": label, "rc": rc,
        "preserved": len([x for x in out.splitlines() if "[PRESERVED]" in x]),
        "refused": len([x for x in out.splitlines() if x.startswith("REFUSED")]),
        "clobbered": len([t for t in present if after[t] != before[t]]),
        "getitem": yang.reads, "writes": yang.updates,
    }


def main():
    src, sha = re_ctl.applied_bytes()
    print("=" * 100)
    print("DRY-RUN INERTNESS PROBE -- applied bytes blob %s" % sha)
    print("guard gating line :295   conflicts = _yang_conflicts(...) if upload else []")
    print("=" * 100)
    rows = [
        exercise(src, True, True, "A  upload=True , store CONFLICTS (the live path)"),
        exercise(src, False, True, "B  upload=False, store CONFLICTS (the DRY RUN)"),
        exercise(src, False, False, "C  upload=False, store AGREES  (negative baseline)"),
    ]
    print("")
    print("  %-48s %-6s %-11s %-9s %-9s %s"
          % ("ARM", "rc", "[PRESERVED]", "REFUSED", "get_item", "clobbered"))
    for r in rows:
        print("  %-48s %-6r %-11d %-9d %-9d %d"
              % (r["label"], r["rc"], r["preserved"], r["refused"],
                 r["getitem"], r["clobbered"]))
    b, c = rows[1], rows[2]
    same = (b["rc"], b["preserved"], b["refused"], b["getitem"]) == \
           (c["rc"], c["preserved"], c["refused"], c["getitem"])
    print("")
    print("  ARM B and ARM C read IDENTICALLY: %s" % same)
    if same:
        print("  -> a DRY RUN reports 0 PRESERVED / rc=0 whether or not the table holds")
        print("     a value the seeder would clobber. It performs ZERO get_item calls,")
        print("     so it never looks. '0 PRESERVED from a dry run' is therefore not a")
        print("     measurement of the guard -- it is the only value that path can emit.")
        print("  -> the arm that DOES discriminate is A: upload=True, which REFUSES")
        print("     (rc=1, %d [PRESERVED]) on the same store." % rows[0]["preserved"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
