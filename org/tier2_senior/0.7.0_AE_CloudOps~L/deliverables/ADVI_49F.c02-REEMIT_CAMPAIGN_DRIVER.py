#!/usr/bin/env python3
"""ADVI_49F.c02-REEMIT campaign driver -- re-emit twr_daily for every STORED partition
under ONE gross-leg convention. Cell C02-g-3. Seat 0.7.0_AE_CloudOps~L.

RUNS ON THE LAPTOP. It dispatches SSM commands to i-01003b035d2988dfb, where
c02_reemit_mirror_pull.py stages the mirror from S3 and invokes the c02 engine.

THE DOMAIN IS CENSUSED AT RUN TIME, NEVER TYPED (3.0.0_SA_CVO 84356 verbatim: "the RANGE
is 'all stored + forward', never a count"). The bar's denominator is every stored twr_daily
partition at the moment the re-emission starts. It was 534 when the cell was written and 535
by the time the campaign was built; a typed number beside a derived one always goes stale, so
this driver derives it every invocation and prints it with its own set-compare.

THE COMPLETION ORACLE IS THE PRODUCED ARTIFACT, NEVER rc. A date counts as done only when its
twr_daily manifest in S3 carries the expected gross_leg_vintage AND schema_version AND a
LastModified after that date's send time. rc=0 from a runner that wrote nothing is exactly the
failure this discipline exists to catch, and the P14 campaign produced one (a send with no
ledger row at all).

RESUME IS FROM THE LEDGER, which is the only durable state. Re-invoking with no arguments
changed re-drives only dates lacking an ARTIFACT-COMPLETE row.

⛔ THE MUTEX IS RE-READ BEFORE EVERY BATCH, not once at start (2.0.0_SA_COO 84243 limit 2):
both advi-49f-gold-floor AND advi-49f-publisher must read DISABLED. If either is ENABLED the
hold is incomplete and this driver STOPS -- it never disables anything itself, which is the
issuer's act on CVO's fallback.

PRE-REGISTERED EXPECTATIONS: three partitions are known-special BEFORE the drive, so the
grade reads a prediction rather than a post-hoc explanation. All three are expected to come
back in a REFUSAL shape; a POPULATED return on any of them is a finding AGAINST the engine,
never a repair. See SPECIAL_DATES.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

BUCKET = "opal-data-49financial"
GOLD_ROOT = "gold/advi"
INSTANCE = "i-01003b035d2988dfb"
REGION = "us-east-1"

# The convention vintage every re-emitted partition must carry (0.4.0_DS_ClientPlatform~N
# 84360; CVO 84129 reading (B) -- a CONVENTION vintage, not an engine-HEAD vintage).
EXPECT_VINTAGE = "946b5c5a3c89b61865ae1f4f60a609e831034cc2"
EXPECT_SCHEMA = "1.1"

HERE = Path(__file__).resolve().parent
LEDGER = HERE / "ADVI_49F.c02-REEMIT_CAMPAIGN_LEDGER.jsonl"

# BOTO3 IN-PROCESS, NOT THE CLI SHIM. `.tools/aws` is a bash script and Windows python
# cannot exec it (WinError 193), and `.tools/aws.cmd` needs a shell. Going through boto3
# also retires three instrument traps this campaign would otherwise carry per call: MSYS
# argv mangling, the paginated-list-* undercount, and `aws s3 ls` rendering LOCAL time
# while s3api renders UTC. Every timestamp below is a boto3 datetime, i.e. UTC-aware.

# Both starters. EITHER one ENABLED means the hold is incomplete.
STARTERS = ("advi-49f-gold-floor", "advi-49f-publisher")

# date -> (why it is special, what a CORRECT re-emission looks like).
# A populated return on any of these is a DEFECT, not a repair.
SPECIAL_DATES = {
    "2024-07-08": (
        "series floor -- no prior trading day exists",
        "REFUSAL-SHAPE (NO-PRIOR-TRADING-DAY); populated returns would be a defect",
    ),
    "2025-01-09": (
        "US market CLOSED (0.4.0_DS_ClientPlatform~N 84375); not a key in prev_map",
        "NO-PRIOR-TRADING-DAY; populated returns here would MANUFACTURE a return for a "
        "closed market -- a NEW defect, never a repair",
    ),
    "2026-08-18": (
        "D-1 (2026-08-17) lies inside the 2026-08-11..08-17 chain-wide outage and has "
        "ZERO objects in S3",
        "REFUSED-NO-BMV again; the free discriminator CANNOT fire because the input is "
        "absent from the store too",
    ),
}


_S3 = None
_SSM = None
_SCHED = None


def s3():
    global _S3
    if _S3 is None:
        import boto3
        _S3 = boto3.client("s3", region_name=REGION)
    return _S3


def ssm():
    global _SSM
    if _SSM is None:
        import boto3
        _SSM = boto3.client("ssm", region_name=REGION)
    return _SSM


def sched():
    global _SCHED
    if _SCHED is None:
        import boto3
        _SCHED = boto3.client("scheduler", region_name=REGION)
    return _SCHED


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def census_domain() -> list[str]:
    """Every stored twr_daily partition, right now. Paginated, counted client-side --
    a bare list_objects_v2 silently stops at 1000 keys and the domain is 1,070."""
    dates: set[str] = set()
    pages = 0
    objs = 0
    for page in s3().get_paginator("list_objects_v2").paginate(
            Bucket=BUCKET, Prefix=f"{GOLD_ROOT}/canonical/twr_daily/"):
        pages += 1
        for o in page.get("Contents", []):
            objs += 1
            m = re.search(r"date=(\d{4}-\d{2}-\d{2})", o["Key"])
            if m:
                dates.add(m.group(1))
    print(f"DOMAIN CENSUS: {len(dates)} partitions from {objs} objects over {pages} "
          f"page(s), {min(dates)}..{max(dates)}", flush=True)
    return sorted(dates)


def check_mutex() -> None:
    """BOTH starters must be DISABLED. Re-read before every batch, never once."""
    for name in STARTERS:
        st = sched().get_schedule(Name=name).get("State")
        if st != "DISABLED":
            raise SystemExit(
                f"BLOCKED: starter {name} reads State={st}, not DISABLED. The hold is "
                "INCOMPLETE and this driver does not disable anything itself -- that is the "
                "issuer's act on CVO 84079's fallback. Stopping with nothing dispatched."
            )
    print(f"OK: mutex held -- {' + '.join(STARTERS)} both DISABLED ({now_iso()})", flush=True)


def load_done() -> dict:
    if not LEDGER.is_file():
        return {}
    done = {}
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if row.get("outcome") == "ARTIFACT-COMPLETE":
            done[row["date"]] = row
    return done


def append_ledger(row: dict) -> None:
    """Append one row and FLUSH. The ledger is the only durable resume state; a row still in
    a buffer when the process dies is a date that gets re-driven."""
    with LEDGER.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, sort_keys=True) + "\n")
        fh.flush()


def versions_for(date: str) -> list[dict]:
    out: list[dict] = []
    for page in s3().get_paginator("list_object_versions").paginate(
            Bucket=BUCKET, Prefix=f"{GOLD_ROOT}/canonical/twr_daily/date={date}/"):
        out.extend(page.get("Versions", []) or [])
    return out


def read_manifest(date: str) -> dict:
    key = f"{GOLD_ROOT}/canonical/twr_daily/date={date}/manifest.json"
    body = s3().get_object(Bucket=BUCKET, Key=key)["Body"].read()
    return json.loads(body)


def dispatch(dates: list[str], mode: str, timeout_s: int) -> str:
    """One SSM command driving N dates sequentially on the box. The per-date evidence is
    preserved: the runner prints one C02_REEMIT_SUMMARY line per date."""
    cmds = [
        "#!/bin/bash",
        "set -uo pipefail",
        f"aws s3 sync s3://{BUCKET}/_code/ /tmp/advi_49f_code/ --delete --only-show-errors",
        "cd /tmp/advi_49f_code",
        "md5sum c02_twr_engine.py c02_reemit_mirror_pull.py",
        "rc_all=0",
    ]
    for d in dates:
        cmds.append("rm -rf /tmp/c02_reemit_mirror /tmp/c02_reemit_out")
        cmds.append(
            f"python3 c02_reemit_mirror_pull.py --date {d} --mode {mode} || rc_all=1"
        )
    cmds.append("exit ${rc_all}")

    out = ssm().send_command(
        DocumentName="AWS-RunShellScript",
        InstanceIds=[INSTANCE],
        Parameters={"commands": cmds, "executionTimeout": [str(timeout_s)]},
        Comment=f"ADVI_49F.c02-REEMIT {mode} x{len(dates)}"[:100],
    )
    return out["Command"]["CommandId"]


def wait(cid: str, timeout_s: int) -> dict:
    t0 = time.time()
    while True:
        try:
            inv = ssm().get_command_invocation(CommandId=cid, InstanceId=INSTANCE)
        except Exception as exc:  # InvocationDoesNotExist races the send by a beat
            if "InvocationDoesNotExist" not in type(exc).__name__ and \
               "InvocationDoesNotExist" not in str(exc):
                raise
            time.sleep(2)
            continue
        if inv.get("Status") in ("Success", "Failed", "Cancelled", "TimedOut"):
            return inv
        if time.time() - t0 > timeout_s + 120:
            raise SystemExit(f"BLOCKED: command {cid} never reached a terminal status")
        time.sleep(5)


def parse_summaries(stdout: str) -> dict:
    out = {}
    for line in stdout.splitlines():
        if line.startswith("C02_REEMIT_SUMMARY "):
            try:
                s = json.loads(line[len("C02_REEMIT_SUMMARY "):])
                out[s["date"]] = s
            except json.JSONDecodeError:
                continue
    return out


def verify(date: str, before: list[dict], send_iso: str) -> dict:
    """THE ORACLE. A date is complete only on PRODUCED-ARTIFACT evidence."""
    after = versions_for(date)
    before_ids = {v["VersionId"] for v in before}
    new_ids = [v["VersionId"] for v in after if v["VersionId"] not in before_ids]
    man = read_manifest(date)
    return {
        "new_versions": len(new_ids),
        "manifest_schema_version": man.get("schema_version"),
        "manifest_gross_leg_vintage": man.get("gross_leg_vintage"),
        "manifest_rows": man.get("rows"),
        "manifest_asof": man.get("asof"),
        "status_census": man.get("status_census"),
        "bmv_source": man.get("bmv_source"),
        "vintage_ok": man.get("gross_leg_vintage") == EXPECT_VINTAGE,
        "schema_ok": man.get("schema_version") == EXPECT_SCHEMA,
        "wrote_something": len(new_ids) > 0,
        "send_time_utc": send_iso,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="ADVI_49F.c02-REEMIT campaign driver")
    ap.add_argument("--mode", choices=("dry-run", "upload"), default="dry-run")
    ap.add_argument("--batch", type=int, default=25)
    ap.add_argument("--limit", type=int, default=0, help="drive at most N dates (0 = all)")
    ap.add_argument("--confirm-campaign-start", action="store_true",
                    help="required for --mode upload; an emission is never a default")
    ap.add_argument("--status", action="store_true", help="report and exit")
    args = ap.parse_args()

    domain = census_domain()
    done = load_done()
    remaining = [d for d in domain if d not in done]

    print(f"LEDGER: {len(done)} ARTIFACT-COMPLETE of {len(domain)} | remaining "
          f"{len(remaining)}", flush=True)
    for d, (why, expect) in SPECIAL_DATES.items():
        state = "DONE" if d in done else ("IN DOMAIN" if d in domain else "NOT IN DOMAIN")
        print(f"  SPECIAL {d} [{state}] {why}\n           EXPECT: {expect}", flush=True)
    if args.status:
        return 0

    if args.mode == "upload" and not args.confirm_campaign_start:
        raise SystemExit("REFUSED: --mode upload requires --confirm-campaign-start. An "
                         "emission over stored partitions is never a default.")
    if not remaining:
        print("OK: nothing remaining -- every domain date has an ARTIFACT-COMPLETE row.")
        return 0

    if args.limit:
        remaining = remaining[: args.limit]
        print(f"LIMIT: driving {len(remaining)} date(s) this invocation", flush=True)

    timeout_s = 1800
    for i in range(0, len(remaining), args.batch):
        batch = remaining[i : i + args.batch]
        check_mutex()  # re-read before EVERY batch, never once at start
        before = {d: versions_for(d) for d in batch}
        send_iso = now_iso()
        cid = dispatch(batch, args.mode, timeout_s)
        print(f"BATCH {i // args.batch + 1}: {len(batch)} date(s) {batch[0]}..{batch[-1]} "
              f"cmd={cid} sent={send_iso}", flush=True)
        inv = wait(cid, timeout_s)
        summaries = parse_summaries(inv.get("StandardOutputContent") or "")

        for d in batch:
            s = summaries.get(d)
            row = {
                "date": d,
                "mode": args.mode,
                "command_id": cid,
                "send_time_utc": send_iso,
                "ledger_written_utc": now_iso(),
                "ssm_status": inv.get("Status"),
                "runner_summary": s,
            }
            if s is None:
                row["outcome"] = "NO-RUNNER-SUMMARY"
                row["note"] = ("the runner printed no summary line for this date -- a send "
                               "that did nothing. A row count answers what I WROTE; only "
                               "this answers what I DID.")
            elif args.mode == "dry-run":
                row["outcome"] = "DRY-RUN-OK" if s.get("engine_rc") == 0 else "DRY-RUN-FAIL"
            else:
                ev = verify(d, before[d], send_iso)
                row["artifact_evidence"] = ev
                ok = (ev["wrote_something"] and ev["vintage_ok"] and ev["schema_ok"]
                      and s.get("engine_rc") == 0)
                row["outcome"] = "ARTIFACT-COMPLETE" if ok else "ARTIFACT-INCOMPLETE"
                if d in SPECIAL_DATES:
                    cen = ev.get("status_census") or {}
                    refusal = all(k != "OK" for k in cen)
                    row["special_date"] = {
                        "why": SPECIAL_DATES[d][0],
                        "expected": SPECIAL_DATES[d][1],
                        "observed_status_census": cen,
                        "refusal_shape_as_predicted": refusal,
                        "verdict": ("AS PREDICTED" if refusal else
                                    "*** UNEXPECTED POPULATED RETURN -- a finding AGAINST "
                                    "the engine, not a repair ***"),
                    }
            append_ledger(row)
            print(f"  {d} -> {row['outcome']}", flush=True)

        bad = [d for d in batch if load_done().get(d) is None and args.mode == "upload"]
        if bad:
            print(f"HALT: {len(bad)} date(s) in this batch did not reach ARTIFACT-COMPLETE: "
                  f"{bad}. Stopping IN PLACE rather than driving past a failure.", flush=True)
            return 1

    print(f"CAMPAIGN PASS COMPLETE at {now_iso()}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
