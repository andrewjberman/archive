"""ACCEPTANCE HARNESS -- ADVI_49F.c01-SIGNFIELD (C01-1 .. C01-4).

Builds flow_ledger and nna_canonical TWICE on IDENTICAL inputs -- once with the PRE-fix
modules recovered from git HEAD by CONTENT (`git show HEAD:<path>`), once with the
working-tree modules -- and compares.

  C01-1  NEW FIELD LIVE, OLD CONTRACT INTACT   signed field present on IC legs; every
         pre-existing column byte-identical pre/post on EVERY row (subsumes C01-3).
  C01-2  SIGN CORRECT AT THE CONSUMER          the pre-registered NNA delta table @e8ccd8eb77
         re-read against post-fix nna_canonical: VALUES asserted, not signs.
  C01-3  NEGATIVE CONTROL, non-IC plane        non-IC rows bit-identical pre/post.
  C01-4  NEGATIVE CONTROL, c02 plane           the ENTIRE ledger->engine interface
         (c02_twr_engine.flows_from_ledger) bit-identical on the pre vs post ledger, plus
         the full twr_daily where its other inputs are available.

NEGATIVE CONTROL ON THE HARNESS ITSELF: a planted mutant must make C01-1 and C01-2 FAIL.
Run with --mutant to exercise that arm.

Read-only against S3. Analytic fields only.
"""
import argparse
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

RUNNERS = Path("data/assets/scripts/gold/runners_49f").resolve()
sys.path.insert(0, str(RUNNERS))
import pandas as pd  # noqa: E402
import runner_common as rc  # noqa: E402

DATES = ["2026-08-24", "2026-08-25"]
NEW_COLS = ["in_kind_signed_value", "in_kind_direction_unresolved"]

# The pre-registered NNA delta table, root-cause doc s.5c.1 @e8ccd8eb77. Computed BEFORE the
# fix, on the ruled design. account -> (registered_now, expected_after, corrected_or_None).
#
# ROW 0033493115 IS CORRECTED HERE, AND THE ORIGINAL IS KEPT BESIDE IT RATHER THAN SWAPPED.
# The registered `now` of 64,841.33 does not reproduce: the LIVE S3 nna_canonical partition
# for date=2026-08-24 reads nna_unresolved_direction = 87,054.1359 for that account, and a
# rebuild from fact_trn reproduces the live figure to the cent. The other three rows match
# the live artifact EXACTLY, so the method is not the variable -- that one row was
# mis-transcribed when this seat authored the table, and its `expected` inherited the error.
# The input is NOT the variable either: fact_trn date=2026-08-24 has LastModified
# 2026-08-25T09:46:15Z (s3api plane, UTC), BEFORE the table's 2026-08-27T00:50Z stamp.
# The corrected expectation is the ruled design's own arithmetic, not a re-baseline:
#   post = cash_part(signed, unchanged) + signed_in_kind
#        = -11,658.78 + (-98,712.92) = -110,371.70
# and 30 of 30 of the account's IC legs are SHORT, so the in-kind part is pure-outflow.
PREREG_NNA = {
    "2026-08-24": {
        "0016371483": (89946.62, -91552.00, None),
        "0033493115": (64841.33, -88158.89, (87054.14, -110371.70)),
        "0049284242": (10956.66, -10926.98, None),
        "0032486794": (39361.92, 39361.92, None),  # inflow, correctly positive: MUST NOT MOVE
    },
    "2026-08-25": {},   # "(2 accounts hold a leg) -- NONE MOVE (both LONG)"
}
# `schema_version` is a metadata STAMP whose entire job is to change when the schema changes
# (1.1 -> 1.2 here). Excluding it from the cell-identity compare is required for the compare
# to mean anything -- but an exclusion is a hole, so it is asserted POSITIVELY below instead
# of being dropped: it must move on EVERY row, and to exactly the expected pair.
STAMP_COLS = ["schema_version"]
TOL = 0.01   # the estate's own RECON_TOLERANCE grain: these are cent-rounded dollar figures


def _load_at_head(name: str, relpath: str, workdir: Path):
    """Import a module from its git-HEAD CONTENT (Rule 22a CODE: resolve a pin by content,
    never by filename or by an ancestry predicate)."""
    src = subprocess.run(["git", "show", f"HEAD:{relpath}"], capture_output=True, check=True).stdout
    dst = workdir / f"{name}.py"
    dst.write_bytes(src)
    spec = importlib.util.spec_from_file_location(name, dst)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod, src


def _load_live(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def _inputs(date: str):
    trn = rc.read_partition(f"{rc.SILVER}/fact_trn", date)
    c00_live = _load_live("_c00_probe", RUNNERS / "c00_flow_ledger.py")
    trn = trn[[c for c in c00_live.TRN_COLS if c in trn.columns]]
    ref = rc.read_partition(f"{rc.OUT_ROOT}/reference/ref_txn_classification", date)
    bnd = rc.read_partition(f"{rc.OUT_ROOT}/dimensions/dim_boundary", date)
    try:
        px = rc.read_partition(f"{rc.OUT_ROOT}/canonical/canonical_positions", date,
                               columns=["cusip", "closing_price"])
    except Exception as exc:
        print(f"  INPUT NOTE: canonical_positions unreadable for {date} ({type(exc).__name__}) "
              f"-- prices=None, in-kind legs stay UNVALUED. Stated, not absorbed.")
        px = None
    return trn, ref, bnd, px


def compare_ledgers(pre: pd.DataFrame, post: pd.DataFrame, date: str, res: dict):
    print(f"\n--- LEDGER pre vs post, date={date}  (pre {pre.shape} / post {post.shape})")
    added = [c for c in post.columns if c not in pre.columns]
    dropped = [c for c in pre.columns if c not in post.columns]
    print(f"  columns ADDED   : {added}")
    print(f"  columns DROPPED : {dropped}   <- MUST be empty (fields only ADD, never mutate)")
    ok_shape = (len(pre) == len(post)) and not dropped and sorted(added) == sorted(NEW_COLS)

    # THE STAMP, asserted positively rather than excluded silently.
    sv_pre = sorted(set(pre["schema_version"].astype(str)))
    sv_post = sorted(set(post["schema_version"].astype(str)))
    stamp_ok = sv_pre == ["1.1"] and sv_post == ["1.2"] and len(pre) == len(post)
    print(f"  schema_version stamp: pre={sv_pre} -> post={sv_post} on all "
          f"{len(post)} rows   {'PASS' if stamp_ok else '*** FAIL ***'}")

    # every OTHER pre-existing column, EVERY row, bit-identical.
    shared = [c for c in pre.columns if c in post.columns and c not in STAMP_COLS]
    a = pre[shared].reset_index(drop=True)
    b = post[shared].reset_index(drop=True)
    diffs = {}
    for c in shared:
        neq = ~((a[c] == b[c]) | (a[c].isna() & b[c].isna()))
        if int(neq.sum()):
            diffs[c] = int(neq.sum())
    print(f"  pre-existing columns compared: {len(shared)} | columns with ANY differing "
          f"cell: {len(diffs)}  {diffs if diffs else ''}")

    is_ic = post["is_in_kind"].astype(bool)
    print(f"  IC legs: {int(is_ic.sum())} of {len(post)}   non-IC: {int((~is_ic).sum())}")

    # C01-3: the non-IC plane, named explicitly (a subset of the above, asserted separately
    # so the control has its own SUBJECT and cannot pass on the wrong one).
    nic_diffs = {c: int(n) for c, n in
                 ((c, (~((a.loc[~is_ic, c] == b.loc[~is_ic, c])
                         | (a.loc[~is_ic, c].isna() & b.loc[~is_ic, c].isna()))).sum())
                  for c in shared) if n}
    print(f"  C01-3 non-IC rows differing cells: {nic_diffs if nic_diffs else 'NONE'}")

    # the new field on IC legs
    sv = pd.to_numeric(post["in_kind_signed_value"], errors="coerce").fillna(0.0)
    und = post["in_kind_direction_unresolved"].astype(bool)
    uv = post["in_kind_unvalued"].astype(bool)
    print(f"  signed field on IC legs: in={int((sv[is_ic] > 0).sum())} "
          f"out={int((sv[is_ic] < 0).sum())} zero={int((sv[is_ic] == 0).sum())} | "
          f"direction UNRESOLVED={int(und[is_ic].sum())} | unvalued={int(uv[is_ic].sum())}")
    print(f"  non-IC rows with a nonzero signed value (MUST be 0): "
          f"{int((sv[~is_ic] != 0).sum())}")
    print(f"  non-IC rows flagged direction-unresolved (MUST be 0): "
          f"{int(und[~is_ic].sum())}")
    zero_buried = int((is_ic & ~uv & ~und & (sv == 0)).sum())
    print(f"  signed_zero_buried (valued+directed yet 0.0; MUST be 0): {zero_buried}")

    # MAGNITUDE PRESERVED: |signed| == unsigned on every directed leg.
    iv = pd.to_numeric(post["in_kind_value"], errors="coerce").fillna(0.0)
    directed = is_ic & ~und
    magdiff = int(((sv[directed].abs() - iv[directed]).abs() > 1e-9).sum())
    print(f"  |signed| != unsigned on a directed leg (MUST be 0): {magdiff}")

    res[f"ledger_{date}"] = {
        "rows_pre": int(len(pre)), "rows_post": int(len(post)),
        "cols_added": added, "cols_dropped": dropped,
        "pre_existing_cols_compared": len(shared),
        "pre_existing_cells_differing": diffs,
        "non_ic_cells_differing": nic_diffs,
        "ic_legs": int(is_ic.sum()),
        "signed_in": int((sv[is_ic] > 0).sum()), "signed_out": int((sv[is_ic] < 0).sum()),
        "direction_unresolved_on_ic": int(und[is_ic].sum()),
        "nonic_signed_nonzero": int((sv[~is_ic] != 0).sum()),
        "nonic_flagged": int(und[~is_ic].sum()),
        "signed_zero_buried": zero_buried,
        "magnitude_mismatch_on_directed": magdiff,
        "schema_stamp": {"pre": sv_pre, "post": sv_post, "PASS": bool(stamp_ok)},
        # `direction_unresolved == 0 on IC` is asserted because it is the MEASURED truth on
        # these two partitions (141 of 141 and 71 of 71 carry LONG/SHORT). It is a
        # partition-specific assertion, not a universal law: an undirected leg is a legitimate
        # state the schema exists to express, and over the other 529 partitions it is
        # UNMEASURED. Asserted here so a producer that silently stops directing legs fails.
        "PASS": bool(ok_shape and stamp_ok and not diffs and not nic_diffs
                     and int((sv[~is_ic] != 0).sum()) == 0 and int(und[~is_ic].sum()) == 0
                     and int(und[is_ic].sum()) == 0
                     and zero_buried == 0 and magdiff == 0
                     and int((sv[is_ic] < 0).sum()) > 0),
    }
    return res[f"ledger_{date}"]["PASS"]


def compare_nna(pre: pd.DataFrame, post: pd.DataFrame, date: str, res: dict):
    print(f"\n--- NNA pre vs post, date={date}")
    p = pre.set_index("account_id")
    q = post.set_index("account_id")
    common = p.index.intersection(q.index)
    print(f"  accounts pre={len(p)} post={len(q)} common={len(common)}")

    # C01-2 half 1: the pre-registered table, VALUE-asserted.
    rows, all_ok = [], True
    for acct, (reg_now, reg_expect, corrected) in sorted(PREREG_NNA[date].items()):
        if acct not in q.index:
            print(f"  {acct}: ABSENT from post-fix output -- FAIL")
            all_ok = False
            rows.append({"account": acct, "expected": reg_expect, "observed": None,
                         "PASS": False})
            continue
        now, expect = corrected if corrected else (reg_now, reg_expect)
        obs_now = float(p.loc[acct, "nna_unresolved_direction"]) if acct in p.index else None
        obs = float(q.loc[acct, "nna_unresolved_direction"])
        ok = abs(obs - expect) <= TOL
        pre_ok = obs_now is None or abs(obs_now - now) <= TOL
        all_ok = all_ok and ok and pre_ok
        tag = "  [ROW CORRECTED vs @e8ccd8eb77]" if corrected else ""
        print(f"  {acct}: pre-fix {obs_now:>14,.2f} (registered {now:>14,.2f} "
              f"{'OK' if pre_ok else 'MISMATCH'}) -> post-fix {obs:>14,.2f} "
              f"(EXPECTED {expect:>14,.2f})  {'PASS' if ok else '*** FAIL ***'}{tag}")
        if corrected:
            print(f"            original registered row was ({reg_now:,.2f} -> "
                  f"{reg_expect:,.2f}); superseded by the LIVE-artifact measurement, "
                  f"not by a re-baseline against my own output")
        rows.append({"account": acct, "registered_now": reg_now,
                     "registered_expected": reg_expect,
                     "corrected": bool(corrected), "asserted_now": now,
                     "asserted_expected": expect, "observed_pre": obs_now,
                     "observed_post": obs, "PASS": bool(ok and pre_ok)})

    # C01-2 half 2: the ASSERTED invariants -- headline / inflow / outflow do not move.
    inv = {}
    for col in ("nna_headline", "daily_inflow", "daily_outflow"):
        d = (p.loc[common, col] - q.loc[common, col]).abs()
        inv[col] = {"accounts_moved": int((d > TOL).sum()), "max_abs_delta": round(float(d.max()), 4)}
        print(f"  INVARIANT {col:<14}: accounts moved {inv[col]['accounts_moved']} "
              f"| max |delta| {inv[col]['max_abs_delta']}   (asserted, not assumed)")
    inv_ok = all(v["accounts_moved"] == 0 for v in inv.values())

    # C01-2 half 3 -- 1.0.0_SA_CTO 76200: the EXPLICIT nna_headline SUM assert. Three d-plane
    # emitters (d01:43+:50, d02:33+:41, d04:40+:52) read nna_canonical and SUM nna_headline, so
    # the SUM is the quantity they actually consume. It is also the WEAKER test -- offsetting
    # per-account moves would net to zero here -- which is why it stands BESIDE the per-account
    # invariant above, not instead of it. Converts the "0 of 267 in-kind legs reach the headline
    # bucket" claim from a delta-table inference into a mechanism that fails loud.
    hs_pre = float(p["nna_headline"].sum())
    hs_post = float(q["nna_headline"].sum())
    sum_ok = abs(hs_pre - hs_post) <= TOL
    print(f"  CTO-76200 ASSERT nna_headline SUM: pre {hs_pre:,.2f} vs post {hs_post:,.2f} "
          f"| delta {hs_pre - hs_post:,.4f}   {'PASS' if sum_ok else '*** FAIL ***'}")
    inv["nna_headline_sum"] = {"pre": round(hs_pre, 2), "post": round(hs_post, 2),
                               "delta": round(hs_pre - hs_post, 4), "PASS": bool(sum_ok)}
    inv_ok = inv_ok and sum_ok

    moved = int((( p.loc[common, "nna_unresolved_direction"]
                 - q.loc[common, "nna_unresolved_direction"]).abs() > TOL).sum())
    print(f"  nna_unresolved_direction: accounts moved {moved} of {len(common)}")

    res[f"nna_{date}"] = {"prereg_rows": rows, "invariants": inv,
                          "unresolved_direction_accounts_moved": moved,
                          "PASS": bool(all_ok and inv_ok)}
    return res[f"nna_{date}"]["PASS"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mutant", choices=["resign", "sign", "drop", "c02"], default="",
                    help="plant a defect and prove the harness FAILS. Three mutants because "
                         "the controls are meant to have INDEPENDENT discriminating power: "
                         "`resign` breaks the old contract (C01-1 must fire), `sign` inverts "
                         "the direction map (C01-2 must fire, C01-1 must NOT -- so C01-2 is "
                         "not riding C01-1), `drop` leaves every IC leg undirected (the "
                         "undirected census must fire).")
    ap.add_argument("--out", default="")
    args = ap.parse_args()

    work = Path(sys.argv[0]).resolve().parent / "_head_modules"
    work.mkdir(exist_ok=True)
    (work / "runner_common.py").write_bytes((RUNNERS / "runner_common.py").read_bytes())
    sys.path.insert(0, str(work))

    res: dict = {"mutant_arm": bool(args.mutant), "dates": DATES}
    c00_pre, c00_src = _load_at_head(
        "c00_pre", "data/assets/scripts/gold/runners_49f/c00_flow_ledger.py", work)
    c01_pre, _ = _load_at_head(
        "c01_pre", "data/assets/scripts/gold/runners_49f/c01_nna_canonical.py", work)
    c00_post = _load_live("c00_post", RUNNERS / "c00_flow_ledger.py")
    c01_post = _load_live("c01_post", RUNNERS / "c01_nna_canonical.py")
    c02 = _load_live("c02_engine", RUNNERS / "c02_twr_engine.py")
    print(f"PRE modules from git HEAD by CONTENT ({len(c00_src)} bytes c00) | "
          f"POST from the working tree")
    print(f"  c00 SCHEMA_VERSION pre={c00_pre.SCHEMA_VERSION} post={c00_post.SCHEMA_VERSION}")
    print(f"  c01 SCHEMA_VERSION pre={c01_pre.SCHEMA_VERSION} post={c01_post.SCHEMA_VERSION}")
    res["schema_versions"] = {"c00_pre": c00_pre.SCHEMA_VERSION, "c00_post": c00_post.SCHEMA_VERSION,
                              "c01_pre": c01_pre.SCHEMA_VERSION, "c01_post": c01_post.SCHEMA_VERSION}

    # POSITIVE CONTROL on the refusal guard: post-fix c01 MUST refuse a pre-fix ledger.
    verdicts = {}
    for date in DATES:
        print(f"\n================ date={date}")
        trn, ref, bnd, px = _inputs(date)
        pre_led, pre_man = c00_pre.build_flow_ledger(trn, ref, bnd, px, asof=date)
        post_led, post_man = c00_post.build_flow_ledger(trn, ref, bnd, px, asof=date)
        print(f"  in_kind_census POST: {json.dumps(post_man['in_kind_census'])}")
        res.setdefault("in_kind_census", {})[date] = post_man["in_kind_census"]

        if args.mutant:
            m = post_led.copy()
            ic = m["is_in_kind"].astype(bool)
            if args.mutant == "resign":
                # the exact design CTO 74187 ruled OUT: re-sign in place.
                m.loc[ic, "in_kind_value"] = m.loc[ic, "in_kind_signed_value"]
            elif args.mutant == "sign":
                # direction map inverted: LONG reads as OUT, SHORT as IN. The old contract
                # is untouched, so ONLY the consumer-side controls may catch this.
                m.loc[ic, "in_kind_signed_value"] = -m.loc[ic, "in_kind_signed_value"]
            elif args.mutant == "c02":
                # C01-4 stays GREEN under the other three mutants -- correctly, since none of
                # them touch `signed_amount`, the only ledger field the TWR engine reads. But
                # a control that has never been SEEN to fire is a promise, not a control. This
                # arm perturbs one EXTERNAL cash leg by a cent to prove C01-4 can discriminate.
                tgt = m.index[(m["final_class"] == "EXTERNAL")
                              & (~m["is_in_kind"].astype(bool))][0]
                m.loc[tgt, "signed_amount"] = float(m.loc[tgt, "signed_amount"]) + 0.01
            elif args.mutant == "drop":
                # the producer silently gives up on direction: signed 0.0, flag set.
                m.loc[ic, "in_kind_signed_value"] = 0.0
                m.loc[ic, "in_kind_direction_unresolved"] = True
            post_led = m
            print(f"  *** MUTANT PLANTED: {args.mutant} ***")

        verdicts[f"C01-1/3 {date}"] = compare_ledgers(pre_led, post_led, date, res)

        if date == DATES[0]:
            try:
                c01_post.build_nna_canonical(pre_led, asof=date)
                print("\n  GUARD POSITIVE CONTROL: *** FAILED *** -- post-fix c01 ACCEPTED a "
                      "pre-fix ledger; the refusal is not wired.")
                res["guard_control"] = {"refused": False}
            except ValueError as exc:
                first = str(exc).split(" -- ")[0][:110]
                print(f"\n  GUARD POSITIVE CONTROL: post-fix c01 REFUSED the pre-fix ledger. "
                      f"ValueError: {first}...")
                res["guard_control"] = {"refused": True, "message_head": first}

        pre_nna, _ = c01_pre.build_nna_canonical(pre_led, asof=date)
        post_nna, post_nna_man = c01_post.build_nna_canonical(post_led, asof=date)
        print(f"  in_kind_direction_census POST: "
              f"{json.dumps(post_nna_man['in_kind_direction_census'])}")
        res.setdefault("nna_direction_census", {})[date] = post_nna_man["in_kind_direction_census"]
        verdicts[f"C01-2 {date}"] = compare_nna(pre_nna, post_nna, date, res)

        # C01-4: the ENTIRE ledger -> TWR-engine interface.
        f_pre = c02.flows_from_ledger(pre_led).sort_values(
            ["account_id", "business_date"]).reset_index(drop=True)
        f_post = c02.flows_from_ledger(post_led).sort_values(
            ["account_id", "business_date"]).reset_index(drop=True)
        same = f_pre.equals(f_post)
        n = 0 if same else int((f_pre != f_post).sum().sum())
        print(f"\n--- C01-4 c02 interface (flows_from_ledger) pre vs post: "
              f"rows {len(f_pre)} vs {len(f_post)} | bit-identical={same}"
              + ("" if same else f" | differing cells {n}"))
        res[f"c02_interface_{date}"] = {"rows": int(len(f_pre)), "identical": bool(same),
                                        "differing_cells": n}
        verdicts[f"C01-4 {date}"] = bool(same)

    print("\n================ VERDICTS")
    for k, v in verdicts.items():
        print(f"  {k:<20} {'PASS' if v else '*** FAIL ***'}")
    res["verdicts"] = {k: bool(v) for k, v in verdicts.items()}
    res["ALL_PASS"] = all(verdicts.values())
    print(f"  ALL_PASS = {res['ALL_PASS']}")
    if args.mutant:
        print("  MUTANT ARM: the harness is SOUND only if ALL_PASS is False above.")
    if args.out:
        Path(args.out).write_text(json.dumps(res, indent=2, default=str), encoding="utf-8")
        print(f"  wrote {args.out}")
    return 0 if res["ALL_PASS"] else 1


if __name__ == "__main__":
    sys.exit(main())
