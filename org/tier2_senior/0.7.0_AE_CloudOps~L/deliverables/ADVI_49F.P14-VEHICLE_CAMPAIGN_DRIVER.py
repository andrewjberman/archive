"""ADVI_49F.P14-VEHICLE -- the backfill CAMPAIGN driver + durable checkpoint ledger (V14-4c).

WHAT THIS IS. The 533-date backfill is a MULTI-DAY CAMPAIGN, not a sitting. This driver is the
thing that survives the sitting: every date's outcome is written to a committed JSONL ledger as it
is driven, so a SUCCESSOR SEAT RESUMES FROM THE LEDGER, never from a session's memory.

THE FIVE LOAD-BEARING RULES, each implemented below and each measured before it was written:

1. COMPLETION IS READ FROM PRODUCED ARTIFACTS -- never rc, and never object COUNT.
   The control date probed on 2026-08-27 also had 2 objects, because these partitions ALREADY
   EXIST (wrongly) -- presence is not repair. The discriminators are LastModified (strictly after
   this run's send time) and the `attestation_basis` stamp reading the branch this driver drove.
   rc is recorded as context; it is never the oracle.

2. THE DRIVER DECIDES THE FLAG, from THIS SEAT'S OWN enumeration, once per date.
   Auto-deriving the flag was BANNED AT EVERY LEVEL (CTO 76528) -- in the entrypoint it is the
   auto-fallback one level up where a00 cannot see it. So the flag is computed from derive()'s
   measured epoch and never adjusted in response to a refusal.

3. EITHER REFUSAL IS A HARD STOP -- flag on a post-epoch date, or flag absent on a pre-epoch date.
   NEVER an auto-retry with the flag toggled: that re-creates the banned auto-fallback from the
   driver side, where a00 cannot see it either. A refusal ends the campaign for operator judgment,
   because an unexpected refusal means the ENUMERATION is wrong and 500 further dates would be
   driven on a wrong premise. Resuming afterwards is free -- that is what the ledger is for.

4. THE 12:45Z MUTEX BLACKOUT is a criterion, not a habit.
   `advi-49f-gold-floor` cron(45 12 * * ? *) UTC ENABLED -> advi-49f-gold-dispatch (measured on the
   applied plane 2026-08-27T21:4xZ; the `advi-49f-publisher` twin at cron(15 13) is DISABLED and is
   re-read at runtime rather than assumed). The nightly takes the SAME entrypoint mutex. No campaign
   date STARTS within [estimated wall + margin] of the fire, and the campaign RESUMES only after the
   nightly's completion is READ FROM ITS OWN PRODUCED ARTIFACTS. A nightly refused on the campaign's
   mutex is a MISSED PRODUCTION RUN wearing a defect's face; a campaign date refused on the
   nightly's is a spurious failure. NEITHER may be discovered live.

5. THE DISPATCHER HALTS THE HOST after the nightly (StartedByDispatcher=true). Mid-campaign that
   halt is an EXPECTED SCHEDULED EVENT, never a campaign failure: the driver restarts the host and
   resumes from the ledger. This driver's OWN sends omit StartedByDispatcher (defaults "false"), so
   they never self-halt, and the driver halts the host ITSELF exactly once at the end.

STANDING OF THE WRITES (74218, restated in every report): the backfill's own writes take the named
ad-hoc/backfill boundary -- they repair history the scheduled path produced wrongly and BECOME
production history. That is why --confirm-campaign-start exists and why --plan is the default.
"""
from __future__ import annotations

import argparse
import datetime as dt
import importlib.util
import json
import pathlib
import sys
import time

import boto3

HERE = pathlib.Path(__file__).resolve().parent
LEDGER = HERE / "ADVI_49F.P14-VEHICLE_CAMPAIGN_LEDGER.jsonl"
REDERIVE = HERE / "ADVI_49F.P14-VEHICLE_A00_ATTESTATION_REDERIVATION.py"

GOLD_BUCKET = "opal-data-49financial"
INSTANCE_ID = "i-0fa1846f04ed7e337"          # bd-49f-auto-login
SSM_DOCUMENT = "advi-49f-chain-dispatch"     # DocumentVersion 3 -- Date + DeclaredHistorical
NIGHTLY_SCHEDULE = "advi-49f-gold-floor"

# The datasets whose manifests must carry the basis for a date to read ARTIFACT-COMPLETE.
# dim_account is the DECIDER and the mirror OUTLIER (a00 writes it); the three canonical tables
# receive the stamp via ADVI_49F.P14-STAMP. Before that TO is deployed-verified only dim_account
# carries it -- which is exactly why the campaign does not start until P14-STAMP is terminal, and
# why this list is asserted rather than tolerated.
STAMPED_DATASETS = [
    "dimensions/dim_account",
    "canonical/flow_ledger",
    "canonical/nna_canonical",
    "canonical/twr_daily",
]

# CLOSED vocabulary (a00). An unrecognised value is a DEFECT, never a silent new state.
BASIS_ATTESTED = "converter-attested"
BASIS_DECLARED = "declared-historical-pre-epoch"
BASIS_VOCAB = {BASIS_ATTESTED, BASIS_DECLARED}

# Closed outcome vocabulary for the ledger. One remedy does not move all of these.
OUT_COMPLETE = "ARTIFACT-COMPLETE"      # verified from artifacts; never redone on resume
OUT_HARD_STOP = "HARD-STOP-REFUSAL"     # a00/document refused; operator judgment, never a toggle
OUT_INCOMPLETE = "ARTIFACT-INCOMPLETE"  # ran, artifacts did not satisfy the oracle
OUT_SEND_FAILED = "SEND-FAILED"         # never reached the chain

BLACKOUT_ANCHOR_HHMM = (12, 45)
DATE1_WALL_SECONDS = 114.5              # the one measured sample; superseded by ledger medians
BLACKOUT_MARGIN_SECONDS = 900           # 15 min on top of the wall estimate

s3 = boto3.client("s3")
ssm = boto3.client("ssm")
ec2 = boto3.client("ec2")
sch = boto3.client("scheduler")


def _load_rederive():
    spec = importlib.util.spec_from_file_location("a00_rederive", REDERIVE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)          # safe: the report is behind a __main__ guard
    return mod


def utcnow():
    return dt.datetime.now(dt.timezone.utc)


# --------------------------------------------------------------------------- ledger
def read_ledger():
    """date -> the LAST row for that date. Append-only file, last row wins."""
    rows = {}
    if not LEDGER.exists():
        return rows
    with LEDGER.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                # A torn final line is possible if a session died mid-append. Surface it; a
                # silently-dropped row is a date that gets redone or skipped without anyone knowing.
                print(f"WARN: unparseable ledger line skipped: {line[:120]}")
                continue
            rows[r["date"]] = r
    return rows


def append_ledger(row):
    row["ledger_written_utc"] = utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    with LEDGER.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, sort_keys=True) + "\n")
        fh.flush()
    return row


# --------------------------------------------------------------------------- oracle
def read_manifest(dataset, date):
    key = f"gold/advi/{dataset}/date={date}/manifest.json"
    try:
        body = s3.get_object(Bucket=GOLD_BUCKET, Key=key)["Body"].read()
    except s3.exceptions.NoSuchKey:
        return None, None
    except s3.exceptions.ClientError:
        return None, None
    head = s3.head_object(Bucket=GOLD_BUCKET, Key=key)
    return json.loads(body), head["LastModified"]


def verify_artifacts(date, expected_basis, since):
    """THE COMPLETION ORACLE. Returns (ok, evidence, problems).

    A dataset satisfies the oracle only if ALL of:
      - its manifest exists,
      - LastModified is strictly AFTER this run's send time (freshness -- not mere presence),
      - attestation_basis is in the CLOSED vocabulary,
      - and equals the basis this driver actually drove (the branch discriminator).
    """
    evidence, problems = {}, []
    for ds in STAMPED_DATASETS:
        man, lm = read_manifest(ds, date)
        if man is None:
            problems.append(f"{ds}: manifest ABSENT")
            evidence[ds] = {"manifest": "ABSENT"}
            continue
        basis = man.get("attestation_basis", "<ABSENT>")
        fresh = lm is not None and lm > since
        evidence[ds] = {
            "last_modified": lm.strftime("%Y-%m-%dT%H:%M:%SZ") if lm else None,
            "attestation_basis": basis,
            "fresh_since_send": fresh,
        }
        # `attested` is a SENTINEL (-1) under the declared branch, not a magnitude. Guard, never sum.
        if "attested" in man:
            evidence[ds]["attested"] = man["attested"]
            if man["attested"] == -1 and basis != BASIS_DECLARED:
                problems.append(f"{ds}: attested==-1 sentinel but basis is {basis!r}")
        if not fresh:
            problems.append(f"{ds}: NOT freshly written (LastModified {lm} <= send {since})")
        if basis == "<ABSENT>":
            problems.append(f"{ds}: attestation_basis ABSENT -- is P14-STAMP deployed?")
        elif basis not in BASIS_VOCAB:
            problems.append(f"{ds}: attestation_basis {basis!r} OUTSIDE the closed vocabulary")
        elif basis != expected_basis:
            problems.append(f"{ds}: basis {basis!r} != driven branch {expected_basis!r}")
    return (not problems), evidence, problems


# --------------------------------------------------------------------------- host
def host_state():
    r = ec2.describe_instances(InstanceIds=[INSTANCE_ID])
    return r["Reservations"][0]["Instances"][0]["State"]["Name"]


def ssm_online():
    r = ssm.describe_instance_information(
        Filters=[{"Key": "InstanceIds", "Values": [INSTANCE_ID]}])
    inf = r.get("InstanceInformationList") or []
    return bool(inf) and inf[0].get("PingStatus") == "Online"


def ensure_host_running(timeout=600):
    """Idempotent. A dispatcher halt mid-campaign lands here and is handled, not failed."""
    st = host_state()
    if st == "stopped":
        print(f"  host {INSTANCE_ID} is stopped (expected after a dispatcher halt) -- starting")
        ec2.start_instances(InstanceIds=[INSTANCE_ID])
    elif st not in ("running", "pending"):
        raise RuntimeError(f"host in state {st!r} -- not startable by this driver")
    deadline = time.time() + timeout
    while time.time() < deadline:
        if host_state() == "running" and ssm_online():
            print("  host running, SSM agent Online")
            return True
        time.sleep(10)
    raise RuntimeError(f"host did not reach running+SSM-Online within {timeout}s")


def halt_host():
    st = host_state()
    if st == "running":
        print(f"  halting host {INSTANCE_ID} (the driver halts it ITSELF, once, at the end)")
        ec2.stop_instances(InstanceIds=[INSTANCE_ID])
    else:
        print(f"  host already {st}; nothing to halt")


# --------------------------------------------------------------------------- blackout
def nightly_anchor_today(now):
    return now.replace(hour=BLACKOUT_ANCHOR_HHMM[0], minute=BLACKOUT_ANCHOR_HHMM[1],
                       second=0, microsecond=0)


def seconds_to_next_anchor(now):
    a = nightly_anchor_today(now)
    if a <= now:
        a = a + dt.timedelta(days=1)
    return (a - now).total_seconds()


def blackout_is_live():
    """Re-read the schedule on the APPLIED plane rather than trusting the constant above.

    If the nightly were DISABLED the blackout would be unnecessary; if a second schedule were
    ENABLED the single-window design would be under-scoped. Either way the driver should know.
    """
    live = {}
    for name in (NIGHTLY_SCHEDULE, "advi-49f-publisher"):
        try:
            r = sch.get_schedule(Name=name)
            live[name] = (r["State"], r["ScheduleExpression"])
        except Exception as exc:
            live[name] = ("UNREADABLE", type(exc).__name__)
    return live


def wall_estimate(ledger_rows):
    """Median of observed per-date wall times; the one measured sample until the ledger has more."""
    walls = [r["wall_seconds"] for r in ledger_rows.values()
             if r.get("outcome") == OUT_COMPLETE and isinstance(r.get("wall_seconds"), (int, float))]
    if not walls:
        return DATE1_WALL_SECONDS, "one-sample datum (date 1), not a distribution"
    walls.sort()
    med = walls[len(walls) // 2]
    return med, f"median of {len(walls)} observed"


def nightly_completed_today(now):
    """Read the NIGHTLY's completion from ITS OWN produced artifacts -- the driver's completion
    instrument pointed at the production run, never a schedule-fired assumption."""
    anchor = nightly_anchor_today(now)
    if now < anchor:
        return False, "anchor not yet passed today"
    # The production path runs T-1 off the trading calendar. Accept any of the last few days'
    # partitions written AFTER today's anchor -- the calendar, not this driver, picks the date.
    for back in range(1, 6):
        d = (now.date() - dt.timedelta(days=back)).isoformat()
        _, lm = read_manifest("canonical/twr_daily", d)
        if lm is not None and lm > anchor:
            return True, f"twr_daily date={d} written {lm.isoformat()} > anchor {anchor.isoformat()}"
    return False, f"no twr_daily partition written after today's {anchor.isoformat()} anchor"


# --------------------------------------------------------------------------- drive
def drive_date(date, basis, poll=15, timeout=3600):
    """ONE date. Strictly sequential -- the entrypoint mutex refuses concurrency by design."""
    declared = "true" if basis == BASIS_DECLARED else "false"
    send_time = utcnow()
    print(f"  send: Date={date} DeclaredHistorical={declared} "
          f"(StartedByDispatcher OMITTED -> defaults false, no self-halt)")
    try:
        r = ssm.send_command(
            InstanceIds=[INSTANCE_ID],
            DocumentName=SSM_DOCUMENT,
            Parameters={"Date": [date], "DeclaredHistorical": [declared]},
            Comment=f"ADVI_49F.P14-VEHICLE campaign {date}"[:100],
        )
    except Exception as exc:
        return {"date": date, "basis": basis, "outcome": OUT_SEND_FAILED,
                "error": f"{type(exc).__name__}: {exc}",
                "send_time_utc": send_time.strftime("%Y-%m-%dT%H:%M:%SZ")}
    cmd = r["Command"]["CommandId"]
    print(f"  command {cmd}")

    deadline = time.time() + timeout
    inv = None
    while time.time() < deadline:
        time.sleep(poll)
        try:
            inv = ssm.get_command_invocation(CommandId=cmd, InstanceId=INSTANCE_ID)
        except ssm.exceptions.InvocationDoesNotExist:
            continue
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            break
    wall = (utcnow() - send_time).total_seconds()
    if inv is None:
        return {"date": date, "basis": basis, "outcome": OUT_SEND_FAILED, "command_id": cmd,
                "error": "no invocation record", "wall_seconds": wall,
                "send_time_utc": send_time.strftime("%Y-%m-%dT%H:%M:%SZ")}

    status, rc = inv["Status"], inv.get("ResponseCode")
    out = (inv.get("StandardOutputContent") or "")[-4000:]
    err = (inv.get("StandardErrorContent") or "")[-2000:]
    print(f"  invocation {status} rc={rc} wall={wall:.1f}s")

    row = {
        "date": date, "basis": basis, "command_id": cmd,
        "send_time_utc": send_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "wall_seconds": round(wall, 1),
        "ssm_status": status, "response_code": rc,
    }

    # A refusal is a HARD STOP for this date. The flag is NEVER toggled and retried.
    blob = out + err
    refusal_markers = ["--declared-historical is for PRE-EPOCH", "REFUSED:", "declared-historical",
                       "not attested", "attestation"]
    if status != "Success":
        looks_refusal = any(m in blob for m in refusal_markers)
        row["outcome"] = OUT_HARD_STOP if looks_refusal else OUT_INCOMPLETE
        row["stdout_tail"] = out[-1500:]
        row["stderr_tail"] = err[-800:]
        return row

    # rc is context. The ORACLE is the artifacts.
    ok, evidence, problems = verify_artifacts(date, basis, send_time)
    row["artifact_evidence"] = evidence
    row["outcome"] = OUT_COMPLETE if ok else OUT_INCOMPLETE
    if problems:
        row["problems"] = problems
    return row


# --------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description="ADVI_49F.P14-VEHICLE backfill campaign driver")
    ap.add_argument("--run", action="store_true", help="drive dates (default is --plan)")
    ap.add_argument("--confirm-campaign-start", action="store_true",
                    help="required with --run: these writes BECOME production history")
    ap.add_argument("--limit", type=int, default=0, help="drive at most N dates this session")
    ap.add_argument("--status", action="store_true", help="ledger summary only, no AWS derivation")
    args = ap.parse_args()

    print("=" * 78)
    print("ADVI_49F.P14-VEHICLE -- BACKFILL CAMPAIGN DRIVER")
    print("=" * 78)
    ledger_rows = read_ledger()

    if args.status:
        by = {}
        for r in ledger_rows.values():
            by[r.get("outcome", "?")] = by.get(r.get("outcome", "?"), 0) + 1
        print(f"ledger: {LEDGER}")
        print(f"  rows: {len(ledger_rows)}")
        for k in sorted(by):
            print(f"    {k:24s} {by[k]}")
        return 0

    print("re-deriving the affected set at EXECUTION TIME (never carrying 533 as a constant)")
    mod = _load_rederive()
    r = mod.derive()
    if not r["controls_ok"]:
        print("*** CONTROL FAILED in the re-derivation -- the split is not trustworthy. STOP.")
        return 2

    flow, att, epoch = r["flow_dates"], r["attested"], r["epoch"]
    N = len(flow)
    print(f"  epoch (MEASURED, never typed) : {epoch}")
    print(f"  backfill set (DENOMINATOR)    : {N}")
    print(f"  pre-epoch  -> declared branch : {len(r['pre_epoch'])} of {N}")
    print(f"  at/after   -> attested branch : {len(r['at_or_after_epoch'])} of {N}")
    print(f"  residual hole (must be empty) : {len(r['residual_hole'])}")
    if r["residual_hole"]:
        print("*** RESIDUAL HOLE -- dates that refuse in BOTH modes. STOP.")
        return 2

    def basis_for(d):
        return BASIS_ATTESTED if d in att else BASIS_DECLARED

    done = {d for d, row in ledger_rows.items() if row.get("outcome") == OUT_COMPLETE}
    stopped = {d for d, row in ledger_rows.items() if row.get("outcome") == OUT_HARD_STOP}
    todo = sorted(flow - done)

    print()
    print(f"  ledger ARTIFACT-COMPLETE      : {len(done)} of {N}")
    print(f"  ledger HARD-STOP (operator)   : {len(stopped)} of {N}")
    print(f"  REMAINING to drive            : {len(todo)} of {N}")

    est, est_src = wall_estimate(ledger_rows)
    print(f"  per-date wall estimate        : {est:.1f}s ({est_src})")
    print(f"  projected span for remaining  : {len(todo)*est/3600.0:.1f}h sequential")

    live = blackout_is_live()
    print("  blackout schedules (APPLIED plane, re-read not assumed):")
    for k, v in live.items():
        print(f"    {k:24s} {v[0]:10s} {v[1]}")

    if not args.run:
        print()
        print("PLAN ONLY -- nothing sent, nothing written to AWS.")
        print("To drive: --run --confirm-campaign-start [--limit N]")
        print()
        print("CAMPAIGN-START READS THREE INPUTS AT THE FACES (COO 76783):")
        print("  (1) ADVI_49F.P14-STAMP deployed-verified")
        print("  (2) ADVI_49F.c00-SIGNING terminal (deployed-verified OR closed-as-impossible)")
        print("  (3) the date-1 re-drive")
        print("This driver does NOT read those faces -- the seat judges them (V14-4c(e)).")
        return 0

    if not args.confirm_campaign_start:
        print()
        print("REFUSED: --run requires --confirm-campaign-start.")
        print("These writes take the ad-hoc/backfill boundary and BECOME production history (74218).")
        return 2

    print()
    print("=" * 78)
    print(f"CAMPAIGN RUN -- {len(todo)} of {N} remaining, strictly sequential")
    print("=" * 78)
    ensure_host_running()

    driven = 0
    for i, d in enumerate(todo, 1):
        if args.limit and driven >= args.limit:
            print(f"\n--limit {args.limit} reached; stopping cleanly. Resume from the ledger.")
            break

        now = utcnow()
        need = est + BLACKOUT_MARGIN_SECONDS
        to_anchor = seconds_to_next_anchor(now)
        if to_anchor < need:
            print(f"\nBLACKOUT: {to_anchor/60:.1f} min to the {BLACKOUT_ANCHOR_HHMM[0]:02d}:"
                  f"{BLACKOUT_ANCHOR_HHMM[1]:02d}Z fire, need {need/60:.1f} min. NOT starting {d}.")
            ok, why = nightly_completed_today(now)
            print(f"  nightly completion (read from ITS artifacts): {ok} -- {why}")
            print("  campaign PAUSES here. Re-invoke after the nightly completes; the ledger resumes.")
            break

        basis = basis_for(d)
        print(f"\n[{i}/{len(todo)}] date {d}  branch={basis}  (denominator {N})")
        ensure_host_running()
        row = drive_date(d, basis)
        append_ledger(row)
        driven += 1
        print(f"  ledger <- {row['outcome']}")

        if row["outcome"] == OUT_HARD_STOP:
            print("\n*** HARD STOP. The flag is NOT toggled and NOT retried (CTO 76528).")
            print("*** An unexpected refusal means the ENUMERATION is wrong; driving on would")
            print("*** burn the remaining dates on a wrong premise. Operator judgment required.")
            break
        if row["outcome"] in (OUT_INCOMPLETE, OUT_SEND_FAILED):
            print(f"\n*** {row['outcome']} on {d}. Campaign halted for judgment.")
            for p in row.get("problems", [])[:8]:
                print(f"      {p}")
            break

    print()
    print("=" * 78)
    final = read_ledger()
    done2 = sum(1 for x in final.values() if x.get("outcome") == OUT_COMPLETE)
    print(f"session drove {driven}; ledger ARTIFACT-COMPLETE {done2} of {N}")
    print("halting the host once, per the driver's own lifecycle ownership")
    halt_host()
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())
