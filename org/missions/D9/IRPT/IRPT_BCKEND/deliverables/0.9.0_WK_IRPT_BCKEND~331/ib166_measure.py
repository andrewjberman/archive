#!/usr/bin/env python3
"""IB-pr-476 (round 166): READ ONLY.  The reader's NEW claim rule (C-CHAINCLAIM) against the reader at the base commit, over the served gold at
the cap day: the accounts whose claim moves from `measured` to `inferred`, and the figures hashed before and after.  Counts and hashes only: no
account id, balance, return or cash amount is written.

  python -I ib164_measure.py fetch <entry> <scratch>      # the cache step (IB-pr-470's, run unchanged): S3 list + get, days <= CAP
  python -I ib166_measure.py measure <entry> <window> <scratch> <base_holdings_gold.py>

The cache step, the window rule, the stand-in source and the reader call are ib164_measure.py's (IB-pr-470), imported not copied.
The base reader is `git show <base_commit>:infra/aws/lambda/investor-reporting/performance/holdings_gold.py`, saved to the scratch and loaded
under another module name; both readers read the same cached partitions.  S3 list/get only, in the fetch step.  No Lambda, no sign-in.
"""
from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "0.9.0_WK_IRPT_BCKEND~325"))
import ib164_measure as m  # noqa: E402  (puts the reader's package on sys.path, ROOT = this worktree)

CAP = m.CAP
WINDOWS = m.WINDOWS


def load_base(path):
    spec = importlib.util.spec_from_file_location("holdings_gold_base", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def read(hg, ids, src, entry, key, a, b):
    canonical, legacy = m.firm_of(entry)
    cid = ids.opaque_account(canonical, key)
    scope = {"resolved_scope": {"scope_ids": [cid]}, "permitted_account_set": [cid], "verified_request_firm_id": legacy}
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            ans = hg.calculate(scope, a, b, src)
    except hg.HoldingsGoldRefused as exc:
        return {"refused": str(exc)}
    vf = m.find(ans["report"], "days_excluded") or {}
    value = ans["report"]["returns"]["account_detail"][0]["value"]
    return {"value": value, "claim": ans["claim"], "vf_claim": vf.get("claim"), "vf": vf, "absences": [x["fact"] for x in ans["absences"]]}


def measure(entry, window, scratch, base_path):
    hg_new, ids = m.setup()
    hg_old = load_base(base_path)
    avail, frames = m.load(entry, scratch)
    src = m.CachedSource(avail, frames)
    a, b = m.window_of(window, avail[-1])
    days = [d for d in avail if a <= d <= b]
    w = src.big[src.big["_day"].isin(set(days))]
    w = w[w["business_date"].map(lambda v: str(v)[:10]).between(a, b)]
    keys = sorted(set(w["account_id"]))
    t0 = time.time()
    figs_old, figs_new = [], []
    n_ref_old = n_ref_new = n_ref_differ = 0
    old_measured = old_inferred = 0
    moves = rule_fires = rule_fires_on_old_inferred = 0
    new_measured = new_inferred = 0
    claim_vf_disagree = 0
    new_members_present = 0
    sums_ok = 0
    new_other_claim_changes = 0
    for i, k in enumerate(keys):
        o = read(hg_old, ids, src, entry, k, a, b)
        n = read(hg_new, ids, src, entry, k, a, b)
        if "refused" in o:
            n_ref_old += 1
        if "refused" in n:
            n_ref_new += 1
        if ("refused" in o) != ("refused" in n) or ("refused" in o and o["refused"] != n["refused"]):
            n_ref_differ += 1
        if "refused" in o or "refused" in n:
            continue
        figs_old.append(repr(float(o["value"])))
        figs_new.append(repr(float(n["value"])))
        old_measured += o["claim"] == "measured"
        old_inferred += o["claim"] == "inferred"
        new_measured += n["claim"] == "measured"
        new_inferred += n["claim"] == "inferred"
        fires = n["vf"].get("days_with_return_left_out", -1) > 0
        rule_fires += fires
        if fires and o["claim"] == "inferred":
            rule_fires_on_old_inferred += 1
        if o["claim"] == "measured" and n["claim"] == "inferred":
            moves += 1
        if o["claim"] == "inferred" and n["claim"] == "measured":
            new_other_claim_changes += 1
        claim_vf_disagree += n["vf_claim"] != n["claim"]
        new_members_present += "days_without_base" in n["vf"] and "days_with_return_left_out" in n["vf"]
        sums_ok += n["vf"].get("days_without_base", -1) + n["vf"].get("days_with_return_left_out", -1) == n["vf"].get("days_excluded")
        if (i + 1) % 2000 == 0:
            print("  %s %s: %d of %d accounts, %.0fs" % (entry, window, i + 1, len(keys), time.time() - t0), flush=True)
    h_old = hashlib.sha256(json.dumps(figs_old, separators=(",", ":")).encode()).hexdigest()
    h_new = hashlib.sha256(json.dumps(figs_new, separators=(",", ":")).encode()).hexdigest()
    out = {"entry": entry, "window": window, "start": a, "end": b, "partitions_read": len(avail), "partitions_in_window": len(days),
           "accounts_read": len(keys), "accounts_refused_old": n_ref_old, "accounts_refused_new": n_ref_new, "refusals_differ": n_ref_differ,
           "figures_compared": len(figs_new), "figures_equal": figs_old == figs_new, "figures_hash_base": h_old, "figures_hash_after": h_new,
           "old_claim": {"measured": int(old_measured), "inferred": int(old_inferred)},
           "new_claim": {"measured": int(new_measured), "inferred": int(new_inferred)},
           "accounts_whose_claim_moves_measured_to_inferred": int(moves),
           "accounts_where_the_new_rule_fires": int(rule_fires),
           "accounts_where_the_new_rule_fires_but_the_base_claim_was_already_inferred": int(rule_fires_on_old_inferred),
           "accounts_inferred_to_measured": int(new_other_claim_changes),
           "accounts_with_both_new_members": int(new_members_present), "accounts_where_the_two_members_sum_to_days_excluded": int(sums_ok),
           "accounts_where_value_facts_claim_differs_from_answer_claim": int(claim_vf_disagree), "seconds": round(time.time() - t0, 1)}
    (Path(scratch) / ("cell166_%s_%s.json" % (entry, window))).write_text(json.dumps(out, sort_keys=True, indent=1))
    print("measure %s %s: %s" % (entry, window, json.dumps(out, sort_keys=True)), flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "measure":
        measure(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    else:
        raise SystemExit("unknown command")
