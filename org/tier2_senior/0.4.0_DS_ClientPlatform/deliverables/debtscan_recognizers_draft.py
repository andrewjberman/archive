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


# --- Recognizer 3: smartx/portal lambda S3-reads (READY -- 0.8.0-grounded, read-callee-disciplined) ----
# smartx_allocations.parquet reads isolated because the smartx/portal LAMBDA readers aren't parsed for their
# S3 reads. READ/WRITE-CLASSIFIER family: a lambda READS the key IFF a read-callee (download_file/get_object/
# read_parquet) references the key LITERAL or a KEY-const bound to it -- NOT a mere comment mention
# (compute_account_distribution mentions it DEAD in a comment but reads the MDPF feed -> correctly excluded).
_SMARTX_KEY_FRAG = "smartx_allocations.parquet"
_READ_CALLEE = re.compile(r"\b(download_file|get_object|read_parquet)\s*\(")


def parse_smartx_reads(ws_root: Path) -> dict[str, list[str]]:
    """Return {'smartx_allocations': [lambda basenames that genuinely READ it]}. inject_pipeline_edges emits
    lambda -[READS]-> S3_DATA_KEY(smartx_allocations) for each -- the reader-edges that clear the isolated key."""
    readers: set[str] = set()
    dirs = [ws_root / "infra" / "aws" / "lambda" / "smartx_ingestion_pipeline",
            ws_root / "infra" / "aws" / "lambda" / "portal"]
    for d in dirs:
        if not d.exists():
            continue
        for f in d.glob("*.py"):
            content = f.read_text(encoding="utf-8")
            if _SMARTX_KEY_FRAG not in content:
                continue
            # KEY constants bound to the smartx key (e.g. S3_CONSOLIDATED_KEY / PARQUET_KEY = "...parquet")
            key_consts = set(re.findall(r'(\w+)\s*=\s*["\'][^"\']*' + re.escape(_SMARTX_KEY_FRAG) + r'["\']',
                                        content))
            # A read-callee whose arg window references the key LITERAL or a bound KEY-const = a real read.
            for m in _READ_CALLEE.finditer(content):
                args = content[m.end(): m.end() + 200]
                if _SMARTX_KEY_FRAG in args or any(k in args for k in key_consts):
                    readers.add(f.stem)
                    break
    return {"smartx_allocations": sorted(readers)}
