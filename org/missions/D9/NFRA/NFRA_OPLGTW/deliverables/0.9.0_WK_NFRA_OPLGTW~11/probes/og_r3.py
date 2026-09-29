#!/usr/bin/env python3
"""OG-r-3 -- on-host capacity re-cut (NFRA_OPLGTW.TO-OG-r-3). READ ONLY: this probe makes no AWS call and runs no
benchmark. It reads the recorded measurement at CAPACITY.json (beside this probe's parent folder), assembled by
probes/assemble_capacity.py from (a) the on-host full-scale run of tests/acceptance/onhost_bench.py on
i-07dccb1615503ac99 against the served release 4248b70b39, (b) the ALB idle_timeout read taken immediately before
that run, and (c) CloudWatch reads for the two ruled AC4 windows. Every figure printed is quoted from CAPACITY.json;
nothing is re-measured. The memory grade is RE-DERIVED here from each job's recorded peak (never read from a flag
alone), which is the R-OG-24 repair applied a second time.

Usage: og_r3.py AC<n>   -- prints the measurement with vintage and denominator, then exactly one line
    VERDICT: PASS-OGR3-AC<n> | FAIL-OGR3-AC<n> <reason>
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
DELIV = HERE.parents[1]
CAPACITY = DELIV / "CAPACITY.json"
CAP = 268435456
BEFORE_P95 = 0.5535024102704742
REG_MAX = 0.2


def load() -> dict:
    # OGR3_CAPACITY_PATH is a TEST-ONLY override (mutant control): the invocation the order runs never sets it.
    path = Path(os.environ["OGR3_CAPACITY_PATH"]) if os.environ.get("OGR3_CAPACITY_PATH") else CAPACITY
    return json.loads(path.read_text(encoding="utf-8"))


def pr(*a) -> None:
    print(*a)


def verdict(ok: bool, n: str, reason: str = "") -> int:
    if ok:
        pr(f"VERDICT: PASS-OGR3-{n}")
        return 0
    pr(f"VERDICT: FAIL-OGR3-{n} {reason}".rstrip())
    return 1


def ac2(d: dict) -> int:
    a = d["ac2"]
    pr("vintage: host run", d.get("started_utc"), "..", d.get("finished_utc"), "(host wall clock); served release 4248b70b39")
    pr("job_memory_cap_bytes:", CAP)
    jobs = a["jobs"]
    pr("denominator: %d benchmarked job(s) graded (1 maximal query + 2 concurrent queries + %d export run(s))"
       % (len(jobs), len(jobs) - 3))
    over = []
    for j in jobs:
        peak = j["peak_child_rss_bytes"]
        respected = peak is not None and peak <= CAP          # re-derived here from the recorded peak
        flag_agrees = bool(j["cap_respected"]) == respected
        pr("  %-58s ok=%s code=%s peak_child_rss_bytes=%s respected=%s (recorded flag agrees: %s)"
           % (j["job"], j["ok"], j["code"], peak, respected, flag_agrees))
        if not respected:
            over.append((j["job"], peak))
        if not flag_agrees:
            over.append((j["job"] + " [flag disagrees]", peak))
    pr("max_peak_child_rss_bytes:", a["max_peak_child_rss_bytes"], "over the cap by",
       max(0, a["max_peak_child_rss_bytes"] - CAP), "bytes")
    ok = not over
    return verdict(ok, "AC2", "" if ok else "; ".join("%s peaked at %s bytes > cap %d" % (n, p, CAP) for n, p in over))


def ac3(d: dict) -> int:
    e = d["export"]
    f, t = e["full"], e["tenth"]
    pr("vintage: host run", d.get("started_utc"), "..", d.get("finished_utc"), "; export via export.generate_csv (SchwabService.export_query), served release 4248b70b39")
    pr("dataset:", e["dataset"], "columns:", e["columns"], "(the widest exportable set by contract column count;", e["note"], ")")
    pr("denominator: 1 contract-scale export (%d rows) + 1 one-tenth export (%d rows), same width; export_deadline_seconds=%s; csv cap %d bytes"
       % (f["target_rows"], t["target_rows"], e["export_deadline_seconds"], e["csv_target_max_bytes"]))
    for c in (f, t):
        pr("  %-6s rows=%d columns=%d ok=%s code=%s reason=%s elapsed_seconds=%s csv_bytes=%s peak_child_rss_bytes=%s "
           "export_dir_entries_after=%s engine_job_dirs_leaked=%s files_gone=%s"
           % (c["label"], c["target_rows"], c["columns"], c["ok"], c["code"], c["reason"], c["elapsed_seconds"],
              c["csv_bytes"], c["peak_child_rss_bytes"], c["export_dir_entries_after"], c["engine_job_dirs_leaked"],
              c["files_gone"]))
    pr("peak ratio full/tenth: %s (the full run was cut off at the cap when it failed, so its true peak is higher)"
       % e["peak_ratio_full_over_tenth"])
    for p in e["probes"]:
        pr("  probe  rows=%d columns=%d ok=%s elapsed_seconds=%s csv_bytes=%s peak_child_rss_bytes=%s files_gone=%s"
           % (p["target_rows"], p["columns"], p["ok"], p["elapsed_seconds"], p["csv_bytes"],
              p["peak_child_rss_bytes"], p["files_gone"]))
    pr("largest_successful_probe (supporting, never substituted for the contract-scale run):", e["largest_successful_probe"])
    generated = bool(f["ok"]) and f["csv_bytes"] is not None and f["csv_bytes"] <= e["csv_target_max_bytes"]
    on_time = generated and f["elapsed_seconds"] <= e["export_deadline_seconds"]
    ok = generated and on_time and bool(f["files_gone"])
    reason = "" if ok else (
        "the %d-row x %d-column export through export.generate_csv did not complete: ok=%s code=%s reason=%s "
        "peak_child_rss_bytes=%s vs cap %d; files_gone=%s; measured evidence is in verdict.for_prd_revision_if_insufficient"
        % (f["target_rows"], f["columns"], f["ok"], f["code"], f["reason"], f["peak_child_rss_bytes"], CAP, f["files_gone"]))
    return verdict(ok, "AC3", reason)


def _window(w: dict, label: str) -> None:
    pr("%s window: %s .. %s (%d day-buckets), http_5xx_sum_total=%s request_count_total=%s window_sample_count=%s "
       "window_p95_seconds=%s"
       % (label, w["window_start"], w["window_end"], w["day_buckets"], w["http_5xx_sum_total"], w["request_count_total"],
          w["window_sample_count"], w["window_p95_seconds"]))
    for x in w["days"]:
        pr("    %s  HTTPCode_Target_5XX_Count=%s  RequestCount=%s  sample_count=%s  p95_seconds=%s"
           % (x["day"], x["http_5xx_sum"], x["request_count_sum"], x["sample_count"], x["p95_seconds"]))


def ac4(d: dict) -> int:
    a = d["ac4"]
    pr("instrument:", a["instrument"])
    pr("dimensions:", a["dimensions"])
    pr("before reference:", a["before_reference"])
    b, p = a["baseline_window"], a["post_release_window"]
    pr("denominator: baseline %d day-buckets, %d requests; post-release %d day-buckets, %d requests"
       % (b["day_buckets"], b["request_count_total"], p["day_buckets"], p["request_count_total"]))
    _window(b, "BASELINE")
    _window(p, "POST-RELEASE (Q5)")
    reg = (b["window_p95_seconds"] - BEFORE_P95) / BEFORE_P95 if b["window_p95_seconds"] is not None else None
    pr("baseline p95 regression vs OGP1-AC11 %s s: %s (cap %s)" % (BEFORE_P95, reg, REG_MAX))
    pr("post-release p95 regression vs the same reference (printed, supporting): %s" % a["post_release_p95_regression_fraction"])
    pr("named-incident rule:", a["named_incident_disqualification"])
    zero_ok = b["day_buckets"] == 7 and all(x["http_5xx_sum"] == 0 for x in b["days"])
    req_ok = all(x["request_count_sum"] > 0 for x in b["days"])
    p95_ok = reg is not None and reg <= REG_MAX
    second_printed = p["day_buckets"] == 7 and all("request_count_sum" in x for x in p["days"]) and p["request_count_total"] > 0
    ok = zero_ok and req_ok and p95_ok and second_printed
    reasons = []
    if not zero_ok:
        reasons.append("a baseline day-bucket carries HTTPCode_Target_5XX_Count > 0")
    if not req_ok:
        reasons.append("a baseline day-bucket has RequestCount 0")
    if not p95_ok:
        reasons.append("baseline p95 regression %s exceeds %s" % (reg, REG_MAX))
    if not second_printed:
        reasons.append("the post-release window was not printed with its request counts")
    return verdict(ok, "AC4", "; ".join(reasons))


def ac5(d: dict) -> int:
    a = d["ac5"]
    pr("instrument:", a["instrument"])
    pr("load_balancer_arn:", a["load_balancer_arn"], "read_utc:", a["read_utc"], "(taken immediately before the benchmark run at", d.get("started_utc"), ")")
    pr("denominator: 1 ALB attribute read")
    pr("idle_timeout_seconds:", a["idle_timeout_seconds"], "query_export_prep_deadline_seconds:", a["query_export_prep_deadline_seconds"])
    ok = a["idle_timeout_seconds"] > a["query_export_prep_deadline_seconds"]
    return verdict(ok, "AC5", "" if ok else "idle_timeout_seconds does not exceed the 30s prep deadline")


def ac6(d: dict) -> int:
    v = d["verdict"]
    pr("vintage: host run", d.get("started_utc"), "..", d.get("finished_utc"), "; assembled", d.get("assembled_utc"))
    pr("denominator: 1 capacity verdict")
    pr("verdict:", v["verdict"])
    pr("checks:", v["checks"])
    ad = d["admission"]
    pr("admission reserve (formula): %d bytes = ceil(%d x %s) + %d; inputs existing_gateway_peak_rss_bytes=%d (measured VmHWM now %s), "
       "required for 2 jobs %d" % (ad["formula"]["admission_reserve_bytes"], ad["formula"]["inputs"]["existing_gateway_peak_rss_bytes"],
                                    ad["formula"]["inputs"]["multiplier"], ad["formula"]["inputs"]["os_reserve_bytes"],
                                    ad["formula"]["inputs"]["existing_gateway_peak_rss_bytes"],
                                    ad["formula"]["inputs"]["measured_current_peak_rss_bytes"],
                                    ad["formula"]["required_bytes_for_2_jobs"]))
    pr("admission reserve (priced against the measured child peak): %d bytes; inputs max_measured_peak_child_rss_bytes=%d, "
       "overshoot_over_cap_bytes=%d; required for 2 jobs %d; gap vs formula %d bytes; host_memory_bytes=%d"
       % (ad["from_measured_child_peak"]["admission_reserve_bytes"],
          ad["from_measured_child_peak"]["inputs"]["max_measured_peak_child_rss_bytes"],
          ad["from_measured_child_peak"]["inputs"]["overshoot_over_cap_bytes"],
          ad["from_measured_child_peak"]["required_bytes_for_2_jobs"], ad["gap_bytes_for_2_jobs"], ad["host_memory_bytes"]))
    if v["verdict"] == "INSUFFICIENT":
        pr("for_prd_revision_if_insufficient:", json.dumps(v["for_prd_revision_if_insufficient"], sort_keys=True)[:1800])
    ok = v["verdict"] in ("SUFFICIENT", "INSUFFICIENT") and (
        v["verdict"] == "SUFFICIENT" or v.get("for_prd_revision_if_insufficient") is not None)
    return verdict(ok, "AC6", "" if ok else "verdict missing, or INSUFFICIENT without for_prd_revision_if_insufficient")


def main(argv: list) -> int:
    if len(argv) < 2 or not argv[1].upper().startswith("AC"):
        print("usage: og_r3.py AC<n>", file=sys.stderr)
        return 2
    n = argv[1].upper()
    d = load()
    fns = {"AC2": ac2, "AC3": ac3, "AC4": ac4, "AC5": ac5, "AC6": ac6}
    fn = fns.get(n)
    if fn is None:
        print(f"VERDICT: FAIL-OGR3-{n} unknown criterion")
        return 1
    return fn(d)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
