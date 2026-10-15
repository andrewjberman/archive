"""IB218-2 -- READ-ONLY split delta for the 49 Financial stock-split adjustment (IRPT_BCKEND TO IB-pr-581).

For each of the 47 split days named by the READ record IB211-1_split_adjust_read.json, the producer's own
read path holdings_performance._frame_for() is run TWICE on one shared PartitionCache:
  BEFORE = the 49F declaration with the split_adjust key removed (an in-memory copy; no file is edited)
  AFTER  = the 49F declaration exactly as it is in sources.json
Only reads are made (list_objects_v2 and get_object through the producer's own readers). No put, delete,
copy, invoke, publish, sign-in or land call is made. The record carries counts only: no account id, no
security identifier, no object key.

Run from the worktree root:
  python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~423/ib218_2_split_delta.py
Optional: --out <path> (default: the record beside this file), --limit <n> (first n split days, for a trial).
"""
from __future__ import annotations

import argparse
import copy
import json
import subprocess
import sys
from collections import Counter, OrderedDict
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[7]
GOLD = ROOT / "data" / "assets" / "scripts" / "gold" / "irpt_holdings_performance"
READ_RECORD = (ROOT / "org" / "missions" / "D9" / "IRPT" / "IRPT_BCKEND" / "deliverables"
               / "0.9.0_WK_IRPT_BCKEND~415" / "IB211-1_split_adjust_read.json")
DEFAULT_OUT = HERE.parent / "IB218-2_split_delta.json"
SOURCE = None  # set in main(): the declaration entry whose positions prefix names the schwab channel
FIRM_SCOPE_LABEL = "49financial"
EXPECTED_SPLIT_DAYS = 47
PROBE_DAY = "2026-04-21"
RULING_920 = 920

sys.path.insert(0, str(GOLD))
sys.path.insert(0, str(ROOT / "lib"))
import boto3  # noqa: E402
import holdings_performance as hp  # noqa: E402
import trading_calendar as tc  # noqa: E402
import numpy as np  # noqa: E402


def git_head():
    out = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(ROOT), capture_output=True,
                         text=True, check=True)
    return out.stdout.strip()


def split_days_from_read_record():
    rec = json.loads(READ_RECORD.read_text(encoding="utf-8"))
    days = rec["split_source"]["49financial"]["split_days"]
    return sorted(str(d) for d in days)


def _reason(note):
    """The first word of a producer note only (ABSENT / SKIP / ...). The rest names partitions, which
    carry the custody master number, so the record keeps the category and never the text."""
    return (note or "").split(":", 1)[0].strip() or "NONE"


def run_day(s3, cache, doc_before, doc_after, day):
    fa, na = hp._frame_for(s3, doc_after, SOURCE, day, cache=cache)
    fb, nb = hp._frame_for(s3, doc_before, SOURCE, day, cache=cache)
    if fa is None or fb is None:
        return {"day": day, "not_computable": True, "account_days_run": 0,
                "account_days_changed": 0,
                "reason_after": _reason(na), "reason_before": _reason(nb)}, None

    src = hp.validate_entry(hp.source_entry(doc_after, SOURCE), SOURCE)
    sa = src["split_adjust"]
    bucket = src["bucket"]
    firm = hp.firm_scope(src)
    pos_cols = hp.declared_columns(src)
    pos_prefix = hp.resolved_prefix(src, "positions_prefix", firm)
    pr = fa.attrs["partitions_read"]
    part0 = pr["prior_close"]["partition"]
    part1 = pr["day_close"]["partition"]
    p0 = cache.get(s3, bucket, pos_prefix, part0, pos_cols)
    p1 = cache.get(s3, bucket, pos_prefix, part1, pos_cols)
    trn_cols = list(OrderedDict.fromkeys([sa["split_source_column"], sa["split_text_column"],
                                          *src["identifier_columns"], sa["account_column"]]))
    trn = cache.get(s3, bucket, sa["transactions_prefix"], day, trn_cols)
    ident_cols = list(src["identifier_columns"])
    pad = src.get("account_id_zero_pad", 0)
    if trn is None or p0 is None or p1 is None:
        raise SystemExit("REFUSED: a partition the producer read is not re-readable (day=%s)" % day)
    ratios, _split_rows = hp._split_ratios_for_day(trn, p0, p1, sa, src)
    split_secs = sorted(ratios.keys())
    p0r = p0.reset_index(drop=True)
    ident0 = hp.identifier(p0r, ident_cols)
    acct0 = hp._pad(p0r[src["account_column"]], pad).values
    if split_secs:
        mask = ident0.isin(split_secs).values
    else:
        mask = np.zeros(len(p0r), dtype=bool)
    holding_accounts = set(acct0[mask])

    ca = fa.set_index("account_id")
    cb = fb.set_index("account_id")
    if not (ca.index.is_unique and cb.index.is_unique):
        raise SystemExit("REFUSED: an arm carries a duplicate account_id (day=%s)" % day)
    common = ca.index.intersection(cb.index)
    only_mismatch = int(len(ca.index.symmetric_difference(cb.index)))
    ra = ca.loc[common, "daily_return"].astype(float)
    rb = cb.loc[common, "daily_return"].astype(float)
    both_nan = ra.isna() & rb.isna()
    ret_diff = (((ra - rb).abs() > 1e-12) | (ra.isna() != rb.isna())) & ~both_nan
    stat_a = ca.loc[common, "status"]
    stat_b = cb.loc[common, "status"]
    stat_diff = stat_a != stat_b
    changed = int((ret_diff | stat_diff).sum()) + only_mismatch
    moves = Counter()
    for fr, to in zip(stat_b[stat_diff], stat_a[stat_diff]):
        moves["%s->%s" % (fr, to)] += 1
    ra_full = fa["daily_return"].astype(float)
    rb_full = fb["daily_return"].astype(float)
    le_b = int((rb_full.notna() & (rb_full <= -0.5)).sum())
    le_a = int((ra_full.notna() & (ra_full <= -0.5)).sum())
    adj = fa.attrs["split_adjust"]
    row = {
        "day": day,
        "not_computable": False,
        "account_days_run": int(len(fa)),
        "account_days_changed": changed,
        "account_days_holding_a_split_security": int(len(holding_accounts)),
        "securities_adjusted": int(adj["securities_adjusted"]),
        "securities_ratio_absent": int(adj["securities_ratio_absent"]),
        "split_security_count_measured": int(len(split_secs)),
        "at_or_below_minus_50pct_before": le_b,
        "at_or_below_minus_50pct_after": le_a,
        "status_moves": dict(moves),
        "account_set_mismatch": only_mismatch,
        "split_adjust_status": str(fa.attrs.get("split_adjust_status")),
        "split_rows_on_day": int(adj["split_days"]),
        "guard_changed_le_holding": bool(changed <= len(holding_accounts)),
        "reason_after": _reason(na),
        "reason_before": _reason(nb),
    }
    return row, {"moves": moves}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args(argv)

    days = split_days_from_read_record()
    if len(days) != EXPECTED_SPLIT_DAYS:
        raise SystemExit("REFUSED: the READ record names %d split days, not %d"
                         % (len(days), EXPECTED_SPLIT_DAYS))
    not_trading = [d for d in days if not tc.is_trading_day(date.fromisoformat(d))]
    print("split days read: %d; not trading days under %s: %d"
          % (len(days), tc.calendar_source(), len(not_trading)))
    if not_trading:
        raise SystemExit("STOP: %d split day(s) are not trading days" % len(not_trading))
    if args.limit:
        days = days[:args.limit]

    global SOURCE
    doc_after = hp.load_declaration()
    SOURCE = next(s for s in hp.declared_sources(doc_after)
                  if doc_after[s]["positions_prefix"].startswith("schwab/"))
    if "split_adjust" not in doc_after[SOURCE]:
        raise SystemExit("REFUSED: the declaration carries no split_adjust for %s" % SOURCE)
    doc_before = copy.deepcopy(doc_after)
    del doc_before[SOURCE]["split_adjust"]
    if "split_adjust" in doc_before[SOURCE] or "split_adjust" not in doc_after[SOURCE]:
        raise SystemExit("REFUSED: the two arms do not differ by split_adjust alone")

    s3 = boto3.client("s3")
    cache = hp.PartitionCache()
    per_day, computed = [], []
    for day in days:
        row, _extra = run_day(s3, cache, doc_before, doc_after, day)
        per_day.append(row)
        if row["not_computable"]:
            print("%s not_computable reason_after=%s reason_before=%s"
                  % (day, row["reason_after"], row["reason_before"]))
        else:
            print("%s run=%d changed=%d holding_split=%d adjusted=%d ratio_absent=%d "
                  "le50_before=%d le50_after=%d guard=%s status=%s"
                  % (day, row["account_days_run"], row["account_days_changed"],
                     row["account_days_holding_a_split_security"], row["securities_adjusted"],
                     row["securities_ratio_absent"], row["at_or_below_minus_50pct_before"],
                     row["at_or_below_minus_50pct_after"], row["guard_changed_le_holding"],
                     row["split_adjust_status"]))
        computed.append(row)
    print("CACHE: %d hit(s), %d miss(es)" % (cache.hits, cache.misses))

    ok = [r for r in per_day if not r["not_computable"]]
    moves = Counter()
    for r in ok:
        moves.update(r["status_moves"])
    totals = {
        "account_days_run": sum(r["account_days_run"] for r in ok),
        "account_days_changed": sum(r["account_days_changed"] for r in ok),
        "account_days_holding_a_split_security": sum(r["account_days_holding_a_split_security"]
                                                     for r in ok),
        "securities_adjusted": sum(r["securities_adjusted"] for r in ok),
        "securities_ratio_absent": sum(r["securities_ratio_absent"] for r in ok),
        "at_or_below_minus_50pct_before": sum(r["at_or_below_minus_50pct_before"] for r in ok),
        "at_or_below_minus_50pct_after": sum(r["at_or_below_minus_50pct_after"] for r in ok),
        "status_moves": dict(sorted(moves.items())),
    }
    probe = next((r for r in per_day if r["day"] == PROBE_DAY), None)
    probe_changed = probe["account_days_changed"] if probe else None
    guard_fail = [r["day"] for r in ok if not r["guard_changed_le_holding"]]
    mismatch = sum(r["account_set_mismatch"] for r in ok)
    not_comp = [r["day"] for r in per_day if r["not_computable"]]

    notes = [
        "Split days are the 47 named in IB211-1_split_adjust_read.json split_source.49financial.split_days; "
        "each was checked against lib/trading_calendar.py before any read and all are trading days "
        "(calendar source: %s)." % tc.calendar_source(),
        "Each day ran holdings_performance._frame_for twice on one shared PartitionCache: BEFORE with the "
        "split_adjust key removed from an in-memory copy of the declaration, AFTER with the declaration as "
        "written. The producer file and sources.json were not edited.",
        "NOT READ: the Cottonwood and Inflection channels (their declarations carry no split_adjust), "
        "positions partitions outside the split days, and the guard grading set behind the ruling's 920.",
        "Probe day %s: the ruling states %d account-days; this run measured %s account-days changed on that "
        "day. The two are not reconciled here; the difference is a finding to read, not a value to force."
        % (PROBE_DAY, RULING_920, probe_changed if probe_changed is not None else "NO ROW"),
        "Days not computable in either arm (excluded from totals, flagged in per_day): %s."
        % (", ".join(not_comp) if not_comp else "none"),
        "Account-set mismatch between arms summed over computable days: %d. Guard account_days_changed <= "
        "account_days_holding_a_split_security failed on %d day(s)%s."
        % (mismatch, len(guard_fail), (": " + ", ".join(guard_fail)) if guard_fail else ""),
        "Sparse directories added locally to the worktree and NOT committed: "
        "data/assets/scripts/gold/irpt_holdings_performance/ and data/assets/scripts/lib/ (on top of the "
        "lib/ and org/ paths the worktree already carried).",
        "Counters: functions_invoked counts write-surface calls and is 0; the read-path calls _frame_for, "
        "_split_ratios_for_day, identifier and PartitionCache.get were made and are the measurement itself. "
        "sign_ins_made, aws_writes_made, rows_written, figures_written and vendor_requests_sent are 0 by "
        "construction of the run.",
    ]
    record = {
        "base_commit": git_head(),
        "read_date": date.today().isoformat(),
        "firm_scope": FIRM_SCOPE_LABEL,
        "split_days": [r["day"] for r in per_day],
        "totals": totals,
        "per_day": per_day,
        "method": (
            "For each of the 47 split days in ascending order, the harness calls holdings_performance._frame_for "
            "for the 49 Financial entry twice on one shared PartitionCache: the BEFORE arm with the split_adjust key "
            "removed from an in-memory copy of sources.json, and the AFTER arm with the declaration as written. "
            "Per day it counts accounts whose daily_return differs by more than 1e-12 or whose status differs, the "
            "accounts with a t-1 row on a split security (identifier chain, producer identifier(), split securities "
            "from _split_ratios_for_day), the adjusted and ratio-absent securities from the AFTER attributes, and the "
            "rows at or below -0.5 in each arm; totals are the sums over computable days. Reads only; no write call."),
        "claim": "measured",
        "notes": notes,
        "functions_invoked": 0,
        "sign_ins_made": 0,
        "aws_writes_made": 0,
        "rows_written": 0,
        "figures_written": 0,
        "vendor_requests_sent": 0,
    }
    out = Path(args.out)
    out.write_text(json.dumps(record, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    print("WROTE %s (%d day rows; totals changed=%d holding=%d)"
          % (out.name, len(per_day), totals["account_days_changed"],
             totals["account_days_holding_a_split_security"]))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except Exception as exc:  # counts and the type only: a traceback could print a value
        print("ERROR: %s during the run; nothing further is recorded" % type(exc).__name__)
        sys.exit(2)
