"""ADVI_49F.c00-SIGNING -- SG-2 / SG-3 / SG-4 acceptance, transcribed from the FACE.

THE ARMS WERE WRITTEN BEFORE THE BUILD, CLAUSE BY CLAUSE OFF THE CRITERIA, and that ordering
is deliberate: two hours ago on P14-STAMP I wrote the harness after the implementation and it
asserted the ruled fields where my code happened to write them rather than where the criterion
said -- five green arms over a field that reached 1 of 4 tables. A harness transcribed from
what I built scores its own blind spot as a PASS.

THE CRITERIA, VERBATIM, AND THE ARM THAT ANSWERS EACH:
  SG-2  "c00 assigns signed_amount on FC-coded code-rule INTERNAL legs from the existing
        convention -- the `dirred` set widens by exactly that measured class, nothing else.
        NO admission change: c02, its grain filter, and INTER_ACCOUNT_PROVENANCE are UNTOUCHED
        (diff-proven)."
          -> A1 every FC code-rule INTERNAL row signs to sign(debit_credit) * |gross_amount|,
             checked against the ORIGINAL fact_trn row, not against my own output.
          -> A2 EXACT WIDENING: every row outside that class is cell-identical PRE vs POST.
          -> A3 ADMISSION: c02's source is byte-identical between the two vintages, and its
             INTER_ACCOUNT_PROVENANCE and _GRAIN_CLASSES literals are read from BOTH sources
             and compared -- not recalled.
  SG-3  "non-code-rule rows bit-identical pre/post on a produced partition."
          -> A4 the same comparison as A2 but restricted to the criterion's own population,
             with its own denominator, because a superset passing is not this row's evidence.
  SG-4  "twr_daily BIT-IDENTICAL under this TO alone."
          -> A5 c02 run on the PRE ledger and on the POST ledger with every other input held
             identical; all cells compared.
          -> A6 THE REACHABILITY CONTROL FOR A5: the same comparator, run against a ledger with
             ONE ADMITTED row's flow altered, must report DIFFERENT. Without it, "identical"
             and "my comparator is blind" are the same output.

Both arms run REAL SUBPROCESSES out of two staged copies of the deployed bundle; the PRE arm's
c00 is recovered BY CONTENT from a pinned commit (never by filename, never by ancestry).

Usage: python ADVI_49F.c00-SIGNING_SG_ACCEPTANCE.py [--post worktree|deployed] [--date D]

Author: 0.4.0_DS_ClientPlatform~U | ADVI_49F.c00-SIGNING | 2026-08-27
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

import pandas as pd

REPO = Path("C:/Users/AndrewBerman/Desktop/ajb_workspace")
RUNNERS = REPO / "data/assets/scripts/gold/runners_49f"
SCRATCH = Path("C:/Users/ANDREW~1/AppData/Local/Temp/claude/"
               "C--Users-AndrewBerman-Desktop-ajb-workspace/"
               "9c462caa-4942-4b63-85d3-1783cfb1645f/scratchpad")
# The last vintage in which the FC class is UNSIGNED. The guard below REFUSES if this baseline
# already signs the class -- the moving-baseline trap from c01-SIGNFIELD, where my PRE arm was
# pinned to HEAD and my own commit made both arms identical, so the test compared nothing.
BASELINE_COMMIT = "eb99599a50"
REL = "data/assets/scripts/gold/runners_49f/c00_flow_ledger.py"
SIGNED_CLASS = "FC-coded code-rule INTERNAL"
# Columns excluded from the CELL compare because they move BY DESIGN, each asserted
# positively instead so the exclusion cannot hide a real change:
#   _ingested_at    -- a stamp, moves on any re-run
#   schema_version  -- SG-2 bumps 1.2 -> 1.3 on EVERY row, by design
# THE FIRST RUN OF THIS HARNESS FAILED A2 AND A4 WITH 1,681 OF 1,681 AND 77 OF 77 ROWS
# "MOVED" -- a UNIFORM failure across a whole population, which is an INSTRUMENT signature and
# not a defect signature. The mover was schema_version. Same shape as the c01-SIGNFIELD
# acceptance earlier today; the fix there and here is identical: exclude the stamp from the
# cell compare and ASSERT IT POSITIVELY, never silently drop it.
VOLATILE = {"_ingested_at", "schema_version"}


def sh(args, cwd=None):
    return subprocess.run(args, cwd=cwd and str(cwd), capture_output=True, text=True)


def stage_bundle(dst: Path) -> int:
    sys.path.insert(0, str(RUNNERS))
    import runner_common as rc
    if dst.exists():
        shutil.rmtree(dst, ignore_errors=True)
    dst.mkdir(parents=True)
    pag = rc.s3().get_paginator("list_objects_v2")
    keys = [o["Key"] for page in pag.paginate(Bucket="opal-data-49financial", Prefix="_code/")
            for o in page.get("Contents", []) if not o["Key"].endswith("/")]
    for k in keys:
        f = dst / k[len("_code/"):]
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_bytes(rc.s3().get_object(Bucket="opal-data-49financial", Key=k)["Body"].read())
    if not (dst / "lib" / "trading_calendar.py").is_file():
        (dst / "lib").mkdir(exist_ok=True)
        shutil.copy2(REPO / "lib/trading_calendar.py", dst / "lib/trading_calendar.py")
    return len(keys)


def run_c00(stage: Path, mirror: Path, date: str) -> int:
    p = sh([sys.executable, "c00_flow_ledger.py", "--date", date, "--dry-run",
            "--local-out", str(mirror), "--ref-local", str(mirror),
            "--boundary-local", str(mirror), "--prices-local", str(mirror)], cwd=stage)
    line = [x for x in ((p.stdout or "") + (p.stderr or "")).splitlines() if "BUILD OK" in x]
    print(f"    c00 rc={p.returncode} | {(line[0][:100] if line else (p.stderr or '')[-160:])}")
    return p.returncode


def run_c02(stage: Path, mirror: Path, date: str) -> int:
    p = sh([sys.executable, "c02_twr_engine.py", "--date", date, "--dry-run",
            "--local-out", str(mirror), "--canonical-local", str(mirror),
            "--calendar-local", str(mirror)], cwd=stage)
    line = [x for x in ((p.stdout or "") + (p.stderr or "")).splitlines() if "EMIT:" in x]
    print(f"    c02 rc={p.returncode} | {(line[0][:100] if line else (p.stderr or '')[-160:])}")
    return p.returncode


def ledger(mirror: Path, date: str) -> pd.DataFrame:
    return pd.read_parquet(mirror / "canonical" / "flow_ledger" / f"date={date}" / "data.parquet")


def twr(mirror: Path, date: str) -> pd.DataFrame:
    return pd.read_parquet(mirror / "canonical" / "twr_daily" / f"date={date}" / "data.parquet")


def cells_differ(a: pd.DataFrame, b: pd.DataFrame, cols, name="") -> pd.Series:
    """Row mask: True where ANY compared cell differs. NaN == NaN counts as equal.

    Prints the PER-COLUMN moved count whenever anything moved, so a uniform failure names its
    own column instead of reading as a defect across the whole population.
    """
    diff = pd.Series(False, index=a.index)
    per_col = {}
    for c in cols:
        x, y = a[c], b[c]
        both_null = x.isna() & y.isna()
        d = ~(both_null | (x == y))
        if int(d.sum()):
            per_col[c] = int(d.sum())
        diff |= d
    if per_col:
        print(f"      [{name}] columns that moved: {per_col}")
    return diff


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--post", choices=("worktree", "deployed"), default="worktree")
    ap.add_argument("--date", default="2026-03-24")
    args = ap.parse_args()
    date = args.date
    results = {}

    print(f"STAGING the deployed bundle twice (PRE @ {BASELINE_COMMIT}, POST = {args.post})")
    pre_stage, post_stage = SCRATCH / "_sg_pre", SCRATCH / "_sg_post"
    # every stage is rebuilt from scratch each run: a leftover directory from a prior run is
    # the fastest way to compare a fresh arm against a stale one and never notice.
    for st in (post_stage, SCRATCH / "_sg_ctrl"):
        if st.exists():
            shutil.rmtree(st, ignore_errors=True)
    n = stage_bundle(pre_stage)
    shutil.copytree(pre_stage, post_stage, dirs_exist_ok=False)
    print(f"    {n} objects per stage")
    pre_c00 = sh(["git", "show", f"{BASELINE_COMMIT}:{REL}"], cwd=REPO)
    if pre_c00.returncode != 0:
        print(f"REFUSED: cannot recover the baseline c00 by content: {pre_c00.stderr[:200]}")
        return 2
    (pre_stage / "c00_flow_ledger.py").write_bytes(pre_c00.stdout.encode("utf-8")
                                                   if isinstance(pre_c00.stdout, str)
                                                   else pre_c00.stdout)
    if args.post == "worktree":
        shutil.copy2(RUNNERS / "c00_flow_ledger.py", post_stage / "c00_flow_ledger.py")
    # else: POST keeps the bundle's own deployed c00 -- the SG-5 form

    src_pre = (pre_stage / "c00_flow_ledger.py").read_text(encoding="utf-8", errors="replace")
    src_post = (post_stage / "c00_flow_ledger.py").read_text(encoding="utf-8", errors="replace")
    if src_pre == src_post:
        print("REFUSED: PRE and POST c00 are the SAME TEXT -- the two arms would compare "
              "nothing. This is the moving-baseline trap; re-pin BASELINE_COMMIT.")
        return 2

    # the mirror is picked BY DATE, never by a hardcoded arm name: the PS battery staged
    # wd_pre at the pre-epoch date and wd_att at the attested one, and pointing the 08-24 run
    # at the 03-24 mirror would compare two arms built from a partition neither one addresses.
    MIRRORS = {"2026-03-24": "wd_pre", "2026-08-24": "wd_att"}
    if date not in MIRRORS:
        print(f"REFUSED: no staged mirror known for date={date}; known: {sorted(MIRRORS)}")
        return 2
    src_mirror = SCRATCH / "_ps_deployed2" / MIRRORS[date] / "canon_mirror"
    if not (src_mirror / "dimensions" / "dim_account" / f"date={date}").is_dir():
        print(f"REFUSED: no staged mirror with a00's record at {src_mirror} for date={date}")
        return 2
    pre_mirror, post_mirror = pre_stage / "mirror", post_stage / "mirror"
    for m in (pre_mirror, post_mirror):
        shutil.copytree(src_mirror, m, dirs_exist_ok=False)

    print(f"\n{'='*76}\nBUILD BOTH ARMS on date={date} from identical inputs")
    if run_c00(pre_stage, pre_mirror, date) != 0 or run_c00(post_stage, post_mirror, date) != 0:
        print("REFUSED: a c00 arm did not complete")
        return 2
    pre, post = ledger(pre_mirror, date), ledger(post_mirror, date)
    if len(pre) != len(post):
        print(f"*** ROW COUNT MOVED: {len(pre)} -> {len(post)} -- this TO adds no rows")
        return 1
    key = ["account_id", "txn_ref"]
    pre = pre.sort_values(key).reset_index(drop=True)
    post = post.sort_values(key).reset_index(drop=True)
    assert (pre["txn_ref"] == post["txn_ref"]).all(), "row alignment broke"
    cols = [c for c in pre.columns if c in post.columns and c not in VOLATILE]

    cls = ((post["resolution_provenance"] == "code-rule")
           & (post["final_class"] == "INTERNAL") & (post["tr_cd"] == "FC"))
    print(f"\n  {SIGNED_CLASS}: {int(cls.sum()):,} of {len(post):,} rows on this partition")

    print(f"\n{'='*76}\nBASELINE GUARD -- the PRE arm must NOT already sign the class")
    already = int((pre.loc[cls, 'signed_amount'] != 0).sum())
    print(f"    PRE rows in the class carrying a non-zero signed_amount: {already} "
          f"(must be 0; a baseline that already signs makes the test vacuous)")
    if already:
        print("REFUSED: the pinned baseline already signs this class.")
        return 2

    print(f"\n{'='*76}\nA1  SG-2 THE SIGNING -- against the ORIGINAL fact_trn row, not my output")
    sys.path.insert(0, str(post_stage))
    import runner_common as rc
    trn = rc.read_partition(f"{rc.SILVER}/fact_trn", date)
    trn = trn.reset_index(drop=True)
    trn["txn_ref"] = trn["business_date"].astype(str) + ":" + trn.index.astype(str)
    src = trn.set_index("txn_ref")
    dc = (src["debit_credit"].fillna("").astype(str).str.strip().str.upper().str[:1])
    gross = pd.to_numeric(src["gross_amount"], errors="coerce").fillna(0.0).abs()
    want = dc.map({"C": 1.0, "D": -1.0}) * gross
    got = post.set_index("txn_ref")["signed_amount"]
    idx = post.loc[cls, "txn_ref"]
    have_dir = want.loc[idx].notna()
    exact = (got.loc[idx][have_dir] - want.loc[idx][have_dir]).abs() < 0.005
    a1 = bool(have_dir.sum()) and bool(exact.all())
    unrec = (~have_dir).sum()
    print(f"    class rows with a readable CREDIT/DEBIT: {int(have_dir.sum()):,} of "
          f"{len(idx):,}; unreadable: {int(unrec):,}")
    print(f"    signed EXACTLY to sign(dc) * |gross_amount|: {int(exact.sum()):,} of "
          f"{int(have_dir.sum()):,}")
    if int(unrec):
        still_zero = (got.loc[idx][~have_dir] == 0).all()
        print(f"    rows with no readable direction left at 0.00 (never guessed): {still_zero}")
        a1 = a1 and bool(still_zero)
    print(f"    total recovered magnitude: ${got.loc[idx].abs().sum():,.2f} "
          f"(was $0.00 across {len(idx):,} rows)")
    results["A1 SG-2 signing"] = a1

    print(f"\n{'='*76}\nA1b THE STAMP COLUMN, ASSERTED POSITIVELY -- it is excluded from "
          f"every cell compare\n      below, so it is checked HERE or the exclusion hides it")
    pre_v = sorted(pre["schema_version"].astype(str).unique())
    post_v = sorted(post["schema_version"].astype(str).unique())
    print(f"    schema_version PRE {pre_v} -> POST {post_v} on all {len(post):,} rows")
    results["A1b schema stamp"] = pre_v == ["1.2"] and post_v == ["1.3"]

    print(f"\n{'='*76}\nA2  SG-2 EXACT WIDENING -- every row OUTSIDE the class cell-identical")
    outside = ~cls
    moved = cells_differ(pre[outside], post[outside], cols, "A2 outside")
    print(f"    rows outside the class: {int(outside.sum()):,}; rows that MOVED: "
          f"{int(moved.sum()):,} (must be 0)")
    inside_moved = cells_differ(pre[cls], post[cls],
                                [c for c in cols if c != "signed_amount"], "A2 inside")
    print(f"    rows INSIDE the class that moved in any column OTHER than signed_amount: "
          f"{int(inside_moved.sum()):,} of {int(cls.sum()):,} (must be 0 -- the widening is "
          f"one field, not a reclassification)")
    a2 = int(moved.sum()) == 0 and int(inside_moved.sum()) == 0
    # MUTANT for A2's predicate: widen the class to TR as well and the predicate must FAIL.
    mut = post.copy()
    tr_cls = ((mut["resolution_provenance"] == "code-rule")
              & (mut["final_class"] == "INTERNAL") & (mut["tr_cd"] == "TR"))
    mut.loc[tr_cls, "signed_amount"] = -1.0
    mut_moved = cells_differ(pre[outside], mut[outside], cols, "A2 mutant")
    print(f"    NEG CTRL -- if the widening had also caught TR ({int(tr_cls.sum()):,} rows), "
          f"the predicate reports {int(mut_moved.sum()):,} moved rows -> REJECTED: "
          f"{int(mut_moved.sum()) > 0}")
    results["A2 exact widening"] = a2 and int(mut_moved.sum()) > 0

    print(f"\n{'='*76}\nA3  SG-2 ADMISSION UNTOUCHED -- c02 read from BOTH sources, not recalled")
    c02_pre = (pre_stage / "c02_twr_engine.py").read_bytes()
    c02_post = (post_stage / "c02_twr_engine.py").read_bytes()
    same_bytes = c02_pre.replace(b"\r\n", b"\n") == c02_post.replace(b"\r\n", b"\n")
    lits = {}
    for tag, blob in (("PRE", c02_pre), ("POST", c02_post)):
        txt = blob.decode("utf-8", errors="replace")
        lits[tag] = [ln.strip() for ln in txt.splitlines()
                     if ln.startswith(("INTER_ACCOUNT_PROVENANCE", "_GRAIN_CLASSES"))
                     or ln.strip().startswith(('"pair-match"', "in_scope = "))]
    print(f"    c02 source LF-normalised identical PRE vs POST: {same_bytes}")
    print(f"    admission literals PRE : {lits['PRE']}")
    print(f"    admission literals POST: {lits['POST']}")
    gd = sh(["git", "diff", "--stat", f"{BASELINE_COMMIT}..HEAD", "--",
             "data/assets/scripts/gold/runners_49f/c02_twr_engine.py"], cwd=REPO)
    print(f"    git diff {BASELINE_COMMIT}..HEAD -- c02: "
          f"{(gd.stdout.strip() or 'EMPTY (no change)')}")
    results["A3 admission untouched"] = (same_bytes and lits["PRE"] == lits["POST"]
                                         and lits["PRE"] != [] and not gd.stdout.strip())

    print(f"\n{'='*76}\nA4  SG-3 NEGATIVE CONTROL -- non-code-rule rows, own denominator")
    noncode = post["resolution_provenance"] != "code-rule"
    nc_moved = cells_differ(pre[noncode], post[noncode], cols, "A4")
    print(f"    non-code-rule rows: {int(noncode.sum()):,}; MOVED: {int(nc_moved.sum()):,} "
          f"(must be 0)")
    print(f"    provenance census unchanged: "
          f"{pre['resolution_provenance'].value_counts().to_dict() == post['resolution_provenance'].value_counts().to_dict()}")
    results["A4 SG-3 non-code-rule"] = int(nc_moved.sum()) == 0

    print(f"\n{'='*76}\nA5  SG-4 THE SERVE PLANE -- twr_daily bit-identical under this TO alone")
    if run_c02(pre_stage, pre_mirror, date) != 0 or run_c02(post_stage, post_mirror, date) != 0:
        print("REFUSED: a c02 arm did not complete")
        return 2
    t_pre, t_post = twr(pre_mirror, date), twr(post_mirror, date)
    tcols = [c for c in t_pre.columns if c in t_post.columns and c not in VOLATILE]
    same_shape = t_pre.shape == t_post.shape
    t_moved = cells_differ(t_pre.reset_index(drop=True),
                           t_post.reset_index(drop=True), tcols, "A5")
    print(f"    twr_daily rows PRE {len(t_pre):,} / POST {len(t_post):,}; cells compared over "
          f"{len(tcols)} columns; rows that MOVED: {int(t_moved.sum()):,} (must be 0)")
    results["A5 SG-4 twr identical"] = same_shape and int(t_moved.sum()) == 0

    print(f"\n{'='*76}\nA6  REACHABILITY CONTROL FOR A5 -- the comparator must SEE a real move")
    ctrl_stage, ctrl_mirror = SCRATCH / "_sg_ctrl", None
    if ctrl_stage.exists():
        shutil.rmtree(ctrl_stage, ignore_errors=True)
    shutil.copytree(post_stage, ctrl_stage)
    ctrl_mirror = ctrl_stage / "mirror"
    led = ledger(ctrl_mirror, date)
    admitted = (led["final_class"] == "EXTERNAL") & (led["signed_amount"] != 0)
    if not bool(admitted.any()):
        print("    UNRUNNABLE: no admitted EXTERNAL row on this partition to perturb")
        results["A6 comparator reachable"] = False
    else:
        i = led.index[admitted][0]
        before = float(led.at[i, "signed_amount"])
        led.at[i, "signed_amount"] = before + 1_000_000.0
        led.to_parquet(ctrl_mirror / "canonical" / "flow_ledger" / f"date={date}"
                       / "data.parquet", index=False)
        print(f"    perturbed ONE admitted EXTERNAL row ({led.at[i, 'account_id']}) "
              f"{before:,.2f} -> {before + 1_000_000.0:,.2f}")
        if run_c02(ctrl_stage, ctrl_mirror, date) != 0:
            print("    REFUSED: control c02 arm did not complete")
            results["A6 comparator reachable"] = False
        else:
            t_ctrl = twr(ctrl_mirror, date)
            c_moved = cells_differ(t_post.reset_index(drop=True),
                                   t_ctrl.reset_index(drop=True), tcols, "A6")
            print(f"    the SAME comparator now reports {int(c_moved.sum()):,} moved rows "
                  f"-> it can see a real move: {int(c_moved.sum()) > 0}")
            results["A6 comparator reachable"] = int(c_moved.sum()) > 0

    print(f"\n{'='*76}")
    for k, v in results.items():
        print(f"  {k:<28} {'PASS' if v else '*** FAIL ***'}")
    print(f"  ALL: {all(results.values())}")
    return 0 if all(results.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
