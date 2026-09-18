#!/usr/bin/env python3
"""OG-r-2 -- on-host capacity and existing-workflow regression on the candidate (NFRA_OPLGTW.TO-OG-r-2).
READ ONLY: this probe makes no AWS call and runs no benchmark itself. It reads the recorded measurement
at CAPACITY.json (beside this probe's parent deliverables folder), assembled from (a) the on-host
full-scale run of infra/aws/ec2/opal-gateway/tests/acceptance/onhost_bench.py, executed via SSM on
i-07dccb1615503ac99 (the OG-i-4 candidate host, released build OG-r-1), and (b) direct AWS reads
(elbv2/cloudwatch via .tools/aws) for the ALB idle timeout and the existing-workflow TargetResponseTime
before/after comparison. Every field printed below is quoted from CAPACITY.json; nothing here is
re-derived or re-measured.

Usage: og_r2.py AC<n>   -- prints the measurement with vintage and denominator, then exactly one line
    VERDICT: PASS-OGR2-AC<n> | FAIL-OGR2-AC<n> <reason>
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
DELIV = HERE.parents[1]
CAPACITY = DELIV / "CAPACITY.json"


def load() -> dict:
    # OGR2_CAPACITY_PATH is a TEST-ONLY override (mutant control): the default invocation this order's
    # criteria run never sets it, so the graded path always reads CAPACITY.json.
    path = Path(os.environ["OGR2_CAPACITY_PATH"]) if os.environ.get("OGR2_CAPACITY_PATH") else CAPACITY
    return json.loads(path.read_text(encoding="utf-8"))


def pr(*a) -> None:
    print(*a)


def verdict(ok: bool, n: str, reason: str = "") -> int:
    if ok:
        pr(f"VERDICT: PASS-OGR2-{n}")
        return 0
    pr(f"VERDICT: FAIL-OGR2-{n} {reason}".rstrip())
    return 1


def ac1(d: dict) -> int:
    a = d["ac1"]
    pr("vintage:", d.get("started_utc"), "..", d.get("finished_utc"), "(host wall clock)")
    pr("denominator: 1 on-host run (scale=%s)" % d.get("scale"))
    pr("app_root_used:", a["app_root_used"], "ran_against_host_install:", a["ran_against_host_install"])
    pr("platform:", a["platform"], "python_version:", a["python_version"])
    pr("bearer_token_minted:", a["bearer_token_minted"], "schwab_tool_enabled:", a["schwab_tool_enabled"],
       "app_server_imported:", a["app_server_imported"])
    pr("synthetic_principals:", a["synthetic_principals"])
    pr("environment_token_like_var_NAMES_present (values never read/printed):", a["environment_token_like_vars_present"])
    ok = (a["ran_against_host_install"] is True and a["platform"] == "linux"
          and a["bearer_token_minted"] is False and a["schwab_tool_enabled"] is False
          and a["app_server_imported"] is False)
    reason = "" if ok else "one of ran_against_host_install/platform/bearer_token_minted/schwab_tool_enabled/app_server_imported failed its expected value"
    return verdict(ok, "AC1", reason)


def ac2(d: dict) -> int:
    a = d["ac2"]
    pr("vintage:", d.get("finished_utc"))
    pr("job_memory_cap_bytes:", a["job_memory_cap_bytes"])
    pr("denominator: 3 job(s) graded (1 maximal + 2 concurrent)")
    pr("maximal: peak_child_rss_bytes=%s cap_respected=%s (ok=%s code=%s)" % (
        a["maximal"]["peak_child_rss_bytes"], a["maximal"]["cap_respected"], a["maximal"]["ok"], a["maximal"]["code"]))
    for c in a["concurrent"]:
        pr("concurrent[%s]: peak_child_rss_bytes=%s cap_respected=%s (ok=%s code=%s)" % (
            c["principal"], c["peak_child_rss_bytes"], c["cap_respected"], c["ok"], c["code"]))
    ok = bool(a["all_cap_respected"])
    return verdict(ok, "AC2", "" if ok else "all_cap_respected is false")


def ac3(d: dict) -> int:
    a = d["ac3"]
    pr("vintage:", d.get("finished_utc"))
    pr("query_deadline_seconds:", a["query_deadline_seconds"])
    pr("denominator: 3 job(s) graded (1 maximal + 2 concurrent)")
    pr("maximal: elapsed_seconds=%s deadline_respected=%s (ok=%s code=%s)" % (
        a["maximal"]["elapsed_seconds"], a["maximal"]["deadline_respected"], a["maximal"]["ok"], a["maximal"]["code"]))
    for c in a["concurrent"]:
        pr("concurrent[%s]: elapsed_seconds=%s deadline_respected=%s (ok=%s code=%s)" % (
            c["principal"], c["elapsed_seconds"], c["deadline_respected"], c["ok"], c["code"]))
    ok = bool(a["all_deadline_respected"])
    return verdict(ok, "AC3", "" if ok else "all_deadline_respected is false")


def ac4(d: dict) -> int:
    a = d["ac4"]
    pr("vintage:", d.get("finished_utc"))
    pr("target_rows:", a["target_rows"], "target_csv_bytes:", a["target_csv_bytes"],
       "export_deadline_seconds:", a["export_deadline_seconds"])
    pr("denominator: 1 export job at contract scale")
    pr("ok:", a["ok"], "code:", a["code"], "elapsed_seconds:", a["elapsed_seconds"],
       "peak_child_rss_bytes:", a["peak_child_rss_bytes"], "csv_bytes:", a["csv_bytes"])
    pr("job_dirs_leaked:", a["job_dirs_leaked"], "engine_temp_root_entries_after_run:", a["engine_temp_root_entries_after_run"])
    pr("largest_successful_probe (supporting, never substituted for the contract-scale measurement):",
       a["largest_successful_probe"])
    # AC4's own text: "a 50 MiB CSV fixture is generated within the export deadline and its temporary
    # files are gone afterwards" -- requires the export to actually SUCCEED and produce the CSV, not
    # merely refuse gracefully (that graceful-refusal case is what AC8/AC3-style "BUSY or LIMIT_EXCEEDED
    # as designed" tolerates; AC4's text names generation as the outcome).
    generated = bool(a["ok"]) and a["csv_bytes"] is not None
    no_leak = not a["job_dirs_leaked"] and not a["engine_temp_root_entries_after_run"]
    within_deadline = bool(a["deadline_respected"])
    ok = generated and no_leak and within_deadline
    reason = "" if ok else (
        f"export did not generate the target CSV at contract scale (ok={a['ok']} code={a['code']} "
        f"peak_child_rss_bytes={a['peak_child_rss_bytes']} vs cap {268435456}); temp cleanup "
        f"no_leak={no_leak}; measured evidence recorded in ac8.for_prd_revision_if_insufficient "
        f"(largest_successful_probe reached {a['largest_successful_probe']['rows'] if a['largest_successful_probe'] else None} rows)")
    return verdict(ok, "AC4", reason)


def ac5(d: dict) -> int:
    a = d["ac5"]
    pr("vintage:", d.get("finished_utc"))
    pr("denominator: 1 on-host peak-RSS read + 1 admission-reserve computation")
    pr("measured_current_peak_rss_bytes:", a["measured_current_peak_rss_bytes"],
       "error:", a["measured_current_peak_rss_error"])
    pr("existing_peak_rss_bytes_used_for_admission:", a["existing_peak_rss_bytes_used_for_admission"],
       "floor_note:", a["floor_note"])
    pr("admission_multiplier:", a["admission_multiplier"], "admission_os_reserve_bytes:", a["admission_os_reserve_bytes"])
    pr("admission_reserve_bytes:", a["admission_reserve_bytes"], "host_memory_bytes:", a["host_memory_bytes"])
    pr("required_bytes_for_1_job:", a["required_bytes_for_1_job"], "required_bytes_for_2_jobs:", a["required_bytes_for_2_jobs"])
    pr("host_can_admit_1_job:", a["host_can_admit_1_job"], "host_can_admit_2_jobs_global_cap:", a["host_can_admit_2_jobs_global_cap"])
    # AC5 only requires these be RECORDED, not that they satisfy any cap (AC8 grades sufficiency).
    ok = a["admission_reserve_bytes"] is not None and a["host_memory_bytes"] is not None
    return verdict(ok, "AC5", "" if ok else "admission reserve or host memory not recorded")


def ac6(d: dict) -> int:
    a = d["ac6"]
    pr("instrument:", a["instrument"])
    pr("load_balancer_arn:", a["load_balancer_arn"], "target_group_arn:", a["target_group_arn"])
    b = a["before"]
    pr("BEFORE window: %s .. %s  sample_count=%s p95_seconds=%s http_5xx_sum=%s (source: %s)" % (
        b["window_start"], b["window_end"], b["sample_count"], b["p95_seconds"], b["http_5xx_sum"], b["source"]))
    a14 = a["after_14d_window"]
    pr("AFTER (14-day, same window rule) window: %s .. %s  sample_count=%s p95_seconds=%s http_5xx_sum=%s (measured_utc=%s)" % (
        a14["window_start"], a14["window_end"], a14["sample_count"], a14["p95_seconds"], a14["http_5xx_sum"], a14["measured_utc"]))
    apr = a["after_post_resize_only_window"]
    pr("AFTER (post-resize-only, supporting) window: %s .. %s  sample_count=%s p95_seconds=%s http_5xx_sum=%s (measured_utc=%s)" % (
        apr["window_start"], apr["window_end"], apr["sample_count"], apr["p95_seconds"], apr["http_5xx_sum"], apr["measured_utc"]))
    pr("denominator: 2 windows measured (14-day trailing + post-resize-only supporting), 1 before-window reference")
    pr("p95_regression_fraction:", a["p95_regression_fraction"], "cap:", a["p95_regression_max_fraction"])
    pr("zero_failures_literal_14d_after:", a["zero_failures_literal_14d_after"],
       "zero_failures_literal_post_resize_only:", a["zero_failures_literal_post_resize_only"])
    pr("failure_rate_before:", a["failure_rate_before"], "failure_rate_after_14d:", a["failure_rate_after_14d"])
    pr("NOTE:", a["note"])
    regression_ok = a["p95_regression_within_cap"]
    # AC6's own text requires BOTH: regression within cap AND zero failures, literally. Both after-windows
    # available to this cell carry non-zero HTTPCode_Target_5XX_Count (18 and 2 respectively), so the
    # literal "zero failures" clause is measured FALSE -- graded here on the WRITTEN text, not weakened to
    # a regression-only substitute (see the surprise row this order's bound requires for exactly this case).
    zero_failures_ok = bool(a["zero_failures_literal_14d_after"]) and bool(a["zero_failures_literal_post_resize_only"])
    ok = regression_ok and zero_failures_ok
    reason = "" if ok else (
        f"p95_regression_within_cap={regression_ok} (fraction={a['p95_regression_fraction']}); "
        f"zero_failures_literal=False (14d-after 5xx={a14['http_5xx_sum']}, post-resize-only 5xx={apr['http_5xx_sum']}) "
        f"-- ambient background 5xx rate present in the BEFORE window too (5xx={b['http_5xx_sum']}), "
        f"unrelated to this cell's changes; filed as a surprise row rather than weakened to pass")
    return verdict(ok, "AC6", reason)


def ac7(d: dict) -> int:
    a = d["ac7"]
    pr("instrument:", a["instrument"])
    pr("load_balancer_arn:", a["load_balancer_arn"], "read_utc:", a["read_utc"])
    pr("denominator: 1 ALB attribute read")
    pr("idle_timeout_seconds:", a["idle_timeout_seconds"], "query_export_prep_deadline_seconds:",
       a["query_export_prep_deadline_seconds"])
    ok = a["idle_timeout_seconds"] > a["query_export_prep_deadline_seconds"]
    return verdict(ok, "AC7", "" if ok else "idle_timeout_seconds does not exceed the 30s prep deadline")


def ac8(d: dict) -> int:
    a = d["ac8"]
    pr("vintage:", d.get("finished_utc"))
    pr("denominator: 1 capacity verdict")
    pr("verdict:", a["verdict"])
    pr("checks:", a["checks"])
    if a["verdict"] == "INSUFFICIENT":
        pr("for_prd_revision_if_insufficient:", a["for_prd_revision_if_insufficient"])
    ok = a["verdict"] in ("SUFFICIENT", "INSUFFICIENT") and (
        a["verdict"] == "SUFFICIENT" or a.get("for_prd_revision_if_insufficient") is not None)
    reason = "" if ok else "verdict missing or INSUFFICIENT without for_prd_revision_if_insufficient measurements"
    return verdict(ok, "AC8", reason)


def main(argv: list) -> int:
    if len(argv) < 2 or not argv[1].upper().startswith("AC"):
        print("usage: og_r2.py AC<n>", file=sys.stderr)
        return 2
    n = argv[1].upper()
    d = load()
    fns = {"AC1": ac1, "AC2": ac2, "AC3": ac3, "AC4": ac4, "AC5": ac5, "AC6": ac6, "AC7": ac7, "AC8": ac8}
    fn = fns.get(n)
    if fn is None:
        print(f"VERDICT: FAIL-OGR2-{n} unknown criterion")
        return 1
    return fn(d)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
