"""DEBTSCAN reachability FP-root-fix recognizers -- DS-authored draft for AE (0.8.0) to integrate into
org/modules/graph/extract_pipeline.py:inject_pipeline_edges (extract_pipeline is ANY_EXEC-owned; DS
authors, AE commits+wires -- same pattern as the detectors/scorer).

Root cause (CVO 2026-07-07): the reachability scan manufactures a FP block because it doesn't parse 3
dispatch/read sources -> the build_mdpf_*/aggregate/patch/feeder scripts + gldinc_ss4c_weekly + the
smartx/portal-read S3 keys read as isolated orphans. These 3 recognizers edge them at the ROOT
(better than N suppression classes). Same recognizer FAMILY as the D1 gold-dispatch-catalog parse
(84bb8377b): parse the authoritative dispatch/read source -> emit dispatcher/reader edges.

All pure-lexical (file:line source parse), so COMPILERKIT-scope-clean per CTO's #3 ruling.
"""
from __future__ import annotations

import re
from pathlib import Path


# --- Recognizer 1: MDPF EC2 dispatch (READY -- grounded on the source) --------------------------------
# Source: infra/aws/ec2/mdpf-daily-runner/mdpf-daily-dispatch.sh -- an EC2 STAGE runner (NOT the gold
# CATALOG heredoc format). It invokes mdpf scripts via `run_step LABEL <relpath>.py args...` (+ a few
# `X_SCRIPT="${SCRIPTS_DIR}/<relpath>.py"` vars for S0/EMIT). Parse those -> the mdpf script set.
def parse_mdpf_dispatch(ws_root: Path) -> dict[str, str]:
    """Return {script_basename: relpath} for every mdpf script dispatched by mdpf-daily-dispatch.sh.
    inject_pipeline_edges then emits dispatcher('mdpf-daily-runner') -[TRIGGERS]-> gold:<basename>
    for each -- edging the build_mdpf_*/mdpf_aggregate_aua/patch_mdpf_*/wsb/wsd/wse/rollup/ownts block
    that currently reads isolated (the DEBTSCAN reachability FP block)."""
    f = ws_root / "infra" / "aws" / "ec2" / "mdpf-daily-runner" / "mdpf-daily-dispatch.sh"
    if not f.exists():
        return {}
    content = f.read_text(encoding="utf-8")
    scripts: dict[str, str] = {}
    # `run_step LABEL <relpath>.py ...` (WS-B/C/D.1/D.2/E, LEG2-CUSTODY-GATE, WS-A, ROLLUP, OWNTS)
    for m in re.finditer(r'run_step\s+\S+\s+(\S+\.py)\b', content):
        rel = m.group(1)
        scripts[Path(rel).stem] = rel
    # `X_SCRIPT="${SCRIPTS_DIR}/<relpath>.py"` (S0_SCRIPT bronze/pull_orion_model_composition, EMIT_SCRIPT)
    for m in re.finditer(r'\w+_SCRIPT="\$\{SCRIPTS_DIR\}/(\S+\.py)"', content):
        rel = m.group(1)
        scripts[Path(rel).stem] = rel
    return scripts
    # Verified against the source (2026-07-07): catches build_mdpf_wsc_inflection_feeder,
    # build_mdpf_wsd2_etf_netassets_feeder, build_mdpf_wse_49f_non_model_aua, mdpf_aggregate_aua,
    # build_aggregate_aua_timeseries, build_mdpf_etf_ownership_timeseries, validate_schwab_native_custody,
    # wsb_49f_smartx_model_aua, wsd_partner_held_etf, pull_orion_model_composition (S0), build_legacy_compat_emit.
    # NOTE: _trading_day_calendar is an IMPORTED util (calendar_utils shim, dispatch.sh:138) -- NOT a
    # run_step target; it edges via the import-recognizer OR stays a FP_UTIL (CVO-ruled util, benign).


# --- Recognizer 2: gold_dispatch Wed-conditional DIRECT python3 invoke (READY -- 0.8.0-grounded) --------
# ss4c-weekly is dispatched in data/black_diamond/scripts/gold/gold_dispatch.sh as a WED-guarded DIRECT
# invoke (line 1397: python3 "$SCRIPTS/gldinc_ss4c_weekly.py" --run-date ...), NOT a CHAIN_ member (why the
# daily _parse_dispatch misses it). gldinc-ss4c.tf is ONLY the monitoring canary + alarms (does NOT dispatch).
def parse_gold_direct_invoke(ws_root: Path) -> dict[str, str]:
    """Return {basename: relpath} for every `python3 "$SCRIPTS/<script>.py"` DIRECT invoke in BD gold_dispatch.sh
    (the Wed/conditional legs not in a CHAIN_). inject_pipeline_edges emits gold_dispatch -[TRIGGERS]-> gold:X.
    Catches gldinc_ss4c_weekly + any other conditional direct-invoke (same run_step-family shape as #1)."""
    f = ws_root / "data" / "black_diamond" / "scripts" / "gold" / "gold_dispatch.sh"
    if not f.exists():
        return {}
    content = f.read_text(encoding="utf-8")
    scripts: dict[str, str] = {}
    for m in re.finditer(r'python3\s+"?\$\{?SCRIPTS\}?/(\S+?\.py)"?', content):
        rel = m.group(1)
        scripts[Path(rel).stem] = rel
    return scripts
    # 0.8.0-grounded (gold_dispatch.sh:1387 Wed-guard / :1397 direct invoke). Catches gldinc_ss4c_weekly.


# --- Recognizer 3: smartx/portal lambda S3-reads (STUB -- reader-edge family, needs the consumer list) -
# smartx_allocations.parquet / wsb / wsd read isolated because the smartx/portal LAMBDA readers aren't
# parsed for their S3 get_object reads. This is the READ/WRITE-CLASSIFIER family (extract_pipeline's
# existing read-callee classifier), extended to the smartx/portal lambda sources. TODO(DS): enumerate
# the smartx/portal lambdas that read these keys (per CVO's "portal/smartx readers") + run the existing
# _READ_CALLEES classifier over them -> reader edges -> the keys gain consumers.
def parse_smartx_portal_reads(ws_root: Path) -> dict[str, list[str]]:
    raise NotImplementedError("DS to enumerate the smartx/portal lambda readers first")
