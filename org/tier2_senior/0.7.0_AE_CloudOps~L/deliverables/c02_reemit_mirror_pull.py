#!/usr/bin/env python3
"""ADVI_49F.c02-REEMIT -- populate the c02 input mirror for ONE date from S3, then invoke
the c02 TWR engine for that date and NOTHING ELSE.

CELL C02-g-3, criterion R-1. Seat 0.7.0_AE_CloudOps~L.

WHY THIS EXISTS (measured at HEAD 0c88005136, not inherited from the P14 face):
  (i)   chain_49f_entrypoint.py has NO stage scoping -- its argparse carries exactly
        --date, --production, --upload, --declared-historical, --workdir. There is no
        way to ask the entrypoint for c02 alone.
  (iii) a full-chain --date D --upload is PROHIBITED by the cell: it re-runs a00..c01 and
        rewrites canonical_valuation / flow_ledger / nna_canonical / dim_*, every one of
        them OUTSIDE C02-g-3's declared domain, failing R-6 on the first new version.
  (ii)  c02_twr_engine.py's own CLI is the domain-safe vehicle -- its ONLY write is
        rc.emit(table=TABLE_DAILY), so it is STRUCTURALLY incapable of touching another
        canonical table -- but it REFUSES without --date + --canonical-local +
        --calendar-local, and in the chain that mirror is produced by RUNNING the very
        upstream stages (ii) exists to avoid.

  This script closes exactly that gap and nothing wider: it populates the mirror from the
  ALREADY-STORED S3 partitions instead of by re-running producers, so the only writer that
  ever runs is c02.

READ-ONLY ON EVERY OUT-OF-DOMAIN TABLE (3.0.0_SA_CVO 84356's one condition on this build):
  this module calls list_objects_v2, head_object and download_file. It performs NO put,
  copy, or delete against any bucket, ever. The single writer in the whole path is the
  engine subprocess, and only when --mode upload is passed explicitly.

THE FIVE INPUTS the engine reads per date (c02_twr_engine.py:388-401, 449 @HEAD):
  1  {cal}/dimensions/dim_calendar/date=D/data.parquet            -- also the source of PREV
  2  {canon}/canonical/canonical_valuation/date=D/data.parquet
  3  {canon}/canonical/canonical_valuation/date=PREV/data.parquet -- the D-1 BMV
  4  {canon}/canonical/flow_ledger/date=D/data.parquet
  5  {canon}/dimensions/dim_account/date=D/manifest.json          -- attestation basis; the
     engine RAISES rather than defaulting when this is absent (_attestation_basis_from_mirror)

PREV IS DERIVED FROM dim_calendar, NEVER FROM WALL CLOCK. This is NEVER#1 and it lives in
this exact file family already: c02 once carried a hardcoded date=2026-08-07 literal, and a
wall-clock D-1 passes every weekday test and silently returns Sunday on a Monday. The
sentinel guard below is carried verbatim in intent from
chain_49f_entrypoint._pull_prev_valuation_into_mirror (:264-271): astype(str) renders a NULL
prev_trading_day as the STRING "None"/"nan"/"NaT", so a truthiness test alone would send us
pulling date=nan.

A GENUINELY ABSENT D-1 IS A LEGITIMATE STATE, NOT A FAILURE (GLD-a-4). At a series' first
partition -- 2024-07-08 is the gold floor -- there is no prior trading day and the engine
correctly emits NO-PRIOR-TRADING-DAY / REFUSED-NO-BMV. This script must make BMV available
WHERE IT EXISTS and must never manufacture one, and never convert a correct refusal into an
abort.

SAFE DEFAULT: --mode defaults to dry-run. An emission requires the operator to type
`--mode upload`. Same discipline as the P14 vehicle's safe-default parameter.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path

BUCKET = "opal-data-49financial"
GOLD_ROOT = "gold/advi"

DATE_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")

# The string forms a null prev_trading_day takes after astype(str). Guard, not cosmetics.
NULL_SENTINELS = {"", "None", "nan", "NaT", "<NA>", "NaN"}

# The engine's own closed vocabulary (_attestation_basis_from_mirror). A value outside it is
# a DEFECT, never a silent new state -- so this script refuses on it too rather than letting
# the engine discover it 5 objects later.
ATTESTATION_VOCAB = ("converter-attested", "declared-historical-pre-epoch")


def _s3():
    import boto3

    return boto3.client("s3", region_name="us-east-1")


def _pull_prefix(s3, prefix: str, dest_dir: Path) -> int:
    """Download every object under prefix into dest_dir. Returns the object count.

    Paginated and counted client-side -- a non-paginated list silently truncates at 1000 and
    would under-populate the mirror without any error.
    """
    pag = s3.get_paginator("list_objects_v2")
    n = 0
    for page in pag.paginate(Bucket=BUCKET, Prefix=prefix):
        for o in page.get("Contents", []):
            name = Path(o["Key"]).name
            if not name:
                continue
            dest = dest_dir / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            s3.download_file(BUCKET, o["Key"], str(dest))
            n += 1
    return n


def _prev_trading_day(cal_parquet: Path, date: str) -> str | None:
    """PREV from dim_calendar, never from wall clock. None means genuinely absent."""
    import pandas as pd

    cal = pd.read_parquet(cal_parquet)
    prev_map = dict(zip(cal["trading_day"].astype(str), cal["prev_trading_day"].astype(str)))
    prev = prev_map.get(str(date))
    if prev is None or prev.strip() in NULL_SENTINELS:
        return None
    return prev


def build_mirror(s3, date: str, mirror: Path) -> dict:
    """Populate the 5 engine inputs for `date`. Refuses loudly on a missing REQUIRED input.

    The D-1 valuation is the ONE input whose absence is legitimate; every other absence means
    the partition this campaign is re-emitting was never fully produced, which is a real
    defect and must not be papered over with a default.
    """
    report: dict = {"date": date, "objects": {}, "prev": None, "prev_outcome": None}

    # 1. dim_calendar -- first, because PREV is derived from it.
    cal_dir = mirror / "dimensions" / "dim_calendar" / f"date={date}"
    n = _pull_prefix(s3, f"{GOLD_ROOT}/dimensions/dim_calendar/date={date}/", cal_dir)
    report["objects"]["dim_calendar"] = n
    cal_parquet = cal_dir / "data.parquet"
    if not cal_parquet.is_file():
        raise SystemExit(
            f"REFUSED date={date}: dim_calendar data.parquet absent after pulling {n} "
            f"object(s) from {GOLD_ROOT}/dimensions/dim_calendar/date={date}/. PREV is "
            "derived from this file and there is no sanctioned fallback -- a wall-clock D-1 "
            "is banned here (NEVER#1)."
        )

    # 2. dim_account manifest -- the engine RAISES without it, so fail here with the legible
    #    message rather than 4 downloads later with the engine's.
    acct_dir = mirror / "dimensions" / "dim_account" / f"date={date}"
    n = _pull_prefix(s3, f"{GOLD_ROOT}/dimensions/dim_account/date={date}/", acct_dir)
    report["objects"]["dim_account"] = n
    acct_manifest = acct_dir / "manifest.json"
    if not acct_manifest.is_file():
        raise SystemExit(
            f"REFUSED date={date}: no a00 record at {acct_manifest}. The engine refuses "
            "rather than defaulting here, and so does this script -- an absent a00 record "
            "means a00 did not run for this date."
        )
    basis = json.loads(acct_manifest.read_text(encoding="utf-8")).get("attestation_basis")
    if basis not in ATTESTATION_VOCAB:
        raise SystemExit(
            f"REFUSED date={date}: a00 record carries attestation_basis={basis!r}, outside "
            f"the closed vocabulary {ATTESTATION_VOCAB}. A value the consumer does not "
            "recognise is a DEFECT, never a silent new state."
        )
    report["attestation_basis"] = basis

    # 3. canonical_valuation date=D
    val_dir = mirror / "canonical" / "canonical_valuation" / f"date={date}"
    n = _pull_prefix(s3, f"{GOLD_ROOT}/canonical/canonical_valuation/date={date}/", val_dir)
    report["objects"]["canonical_valuation"] = n
    if not (val_dir / "data.parquet").is_file():
        raise SystemExit(
            f"REFUSED date={date}: canonical_valuation data.parquet absent after pulling {n} "
            "object(s). The engine cannot compute a return without the date's own valuation."
        )

    # 4. flow_ledger date=D
    led_dir = mirror / "canonical" / "flow_ledger" / f"date={date}"
    n = _pull_prefix(s3, f"{GOLD_ROOT}/canonical/flow_ledger/date={date}/", led_dir)
    report["objects"]["flow_ledger"] = n
    if not (led_dir / "data.parquet").is_file():
        raise SystemExit(
            f"REFUSED date={date}: flow_ledger data.parquet absent after pulling {n} "
            "object(s). Cash flows are an input to the return, not an optional decoration."
        )

    # 5. canonical_valuation date=PREV -- the D-1 BMV. Absence here is LEGITIMATE.
    prev = _prev_trading_day(cal_parquet, date)
    report["prev"] = prev
    if prev is None:
        report["prev_outcome"] = "NO-PRIOR-TRADING-DAY"
        report["objects"]["canonical_valuation_prev"] = 0
        print(
            f"OK: date={date} has NO-PRIOR-TRADING-DAY in dim_calendar; the engine will "
            "emit NO-PRIOR-TRADING-DAY. Correct at a series' first partition, not a gap.",
            flush=True,
        )
    else:
        prev_dir = mirror / "canonical" / "canonical_valuation" / f"date={prev}"
        n = _pull_prefix(
            s3, f"{GOLD_ROOT}/canonical/canonical_valuation/date={prev}/", prev_dir
        )
        report["objects"]["canonical_valuation_prev"] = n
        if n == 0:
            report["prev_outcome"] = "ABSENT-IN-S3"
            print(
                f"WARN: D-1 valuation for date={prev} (D-1 of {date}) holds 0 object(s) in "
                "S3; the engine will emit REFUSED-NO-BMV as it does today. A genuinely "
                "absent D-1 is a legitimate state, NOT a failure -- this script never "
                "manufactures a BMV.",
                flush=True,
            )
        else:
            report["prev_outcome"] = "PULLED"

    return report


def run_engine(date: str, mirror: Path, mode: str, local_out: Path, workdir: Path) -> dict:
    """Invoke c02_twr_engine for ONE date. The ONLY writer in this whole path."""
    cmd = [
        sys.executable,
        "c02_twr_engine.py",
        "--date",
        date,
        "--canonical-local",
        str(mirror),
        "--calendar-local",
        str(mirror),
    ]
    if mode == "upload":
        cmd.append("--upload")
    else:
        # --local-out plus --dry-run exercises the FULL emit block (provenance stamp,
        # manifest, attestation basis) while rc.emit receives upload=False, because the
        # engine passes upload=(args.upload and not args.dry_run). Nothing reaches S3.
        cmd += ["--local-out", str(local_out), "--dry-run"]

    t0 = time.time()
    proc = subprocess.run(
        cmd, cwd=str(workdir), capture_output=True, text=True, check=False
    )
    wall = time.time() - t0

    out = proc.stdout or ""
    emit = re.search(r"EMIT: rows=(\d+) cols=(\d+)", out)
    return {
        "rc": proc.returncode,
        "engine_wall_seconds": round(wall, 2),
        "rows": int(emit.group(1)) if emit else None,
        "cols": int(emit.group(2)) if emit else None,
        "stdout_tail": out[-2000:],
        "stderr_tail": (proc.stderr or "")[-2000:],
    }


def main() -> int:
    ap = argparse.ArgumentParser(
        description=(
            "ADVI_49F.c02-REEMIT: pull the c02 input mirror for one date from S3 and "
            "re-emit twr_daily for that date ALONE (cell C02-g-3, R-1 vehicle (ii))."
        )
    )
    ap.add_argument("--date", required=True, help="partition date YYYY-MM-DD")
    ap.add_argument(
        "--mode",
        choices=("dry-run", "upload"),
        default="dry-run",
        help="dry-run (default, writes NOTHING to S3) or upload (emits twr_daily)",
    )
    ap.add_argument("--workdir", default="/tmp/advi_49f_code",
                    help="dir holding c02_twr_engine.py + runner_common.py")
    ap.add_argument("--mirror-root", default="/tmp/c02_reemit_mirror")
    ap.add_argument("--out-root", default="/tmp/c02_reemit_out")
    args = ap.parse_args()

    if not DATE_RE.match(args.date):
        raise SystemExit(f"REFUSED: --date {args.date!r} is not YYYY-MM-DD")

    workdir = Path(args.workdir)
    engine = workdir / "c02_twr_engine.py"
    if not engine.is_file():
        raise SystemExit(
            f"REFUSED: no engine at {engine}. The run dir must hold c02_twr_engine.py and "
            "runner_common.py (the engine imports runner_common by name)."
        )

    mirror = Path(args.mirror_root) / args.date
    local_out = Path(args.out_root) / args.date
    mirror.mkdir(parents=True, exist_ok=True)
    local_out.mkdir(parents=True, exist_ok=True)

    s3 = _s3()

    t0 = time.time()
    pull = build_mirror(s3, args.date, mirror)
    pull_wall = time.time() - t0

    result = run_engine(args.date, mirror, args.mode, local_out, workdir)

    summary = {
        "date": args.date,
        "mode": args.mode,
        "pull_wall_seconds": round(pull_wall, 2),
        "objects": pull["objects"],
        "prev": pull["prev"],
        "prev_outcome": pull["prev_outcome"],
        "attestation_basis": pull.get("attestation_basis"),
        "engine_rc": result["rc"],
        "engine_wall_seconds": result["engine_wall_seconds"],
        "total_wall_seconds": round(pull_wall + result["engine_wall_seconds"], 2),
        "rows": result["rows"],
        "cols": result["cols"],
    }
    # ONE machine-readable line for the campaign ledger. The driver parses this, never prose.
    print("C02_REEMIT_SUMMARY " + json.dumps(summary, sort_keys=True), flush=True)

    if result["rc"] != 0:
        print("ERROR: engine stdout tail:\n" + result["stdout_tail"], flush=True)
        print("ERROR: engine stderr tail:\n" + result["stderr_tail"], flush=True)
    return int(result["rc"])


if __name__ == "__main__":
    sys.exit(main())
