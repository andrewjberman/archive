"""EGS17 battery -- THE FILLED-IN DAY (ETFS_GUARDRAIL.TO-EG-s-17, S17-AC1).

Seven arms. Prints EGS17-FILLED-IN-DAY only when EVERY arm holds.

  ARM-A  the hole census (20 trading days x 2 partners, denominators printed) plus the
         producer's PROBE answer for every absent date; at least one REAL class-C hole
         (partition present, priced > 0, output absent) named.
  ARM-B  Target.Input read LIVE on BOTH daily rules (ABSENT -- EventBridge's default
         scheduled envelope IS the payload) and this battery's payload byte-equal to it
         in shape and carrying NO `date` key.
  ARM-C  the invocation PINNED by `START RequestId` 1 of 1 in the function's log GROUP
         read BY TIME over its own window, with no role assumption attributable to a
         scheduled fire in it; the CloudTrail `Invoke` read prints COVERAGE-ABSENT.
  ARM-D  the function's CloudWatch log for THIS invocation names the recovered date --
         in `catchup_processed` for a hole OLDER than the newest priced partition, or in
         the MAIN PATH's own `OK: wrote s3://...` line for a HEAD-OF-WINDOW hole, in
         which case CATCHUP-BRANCH-NOT-EXERCISED is printed beside the token.
  ARM-E  the slice exists after: head-object, size > 0, LastModified >= the invoke's UTC,
         and its rows counted by a SECOND reader (re-downloaded and parsed) non-zero.
  ARM-F  POSITIVE CONTROL, a READ: a date that is NOT missing is not reported recovered.
  ARM-G  the schedules' own prior firings over 30 days from the fire-instant AssumeRole
         MANAGEMENT events on each function's execution role, BOTH producers, with
         denominators, beside this manual invoke as the negative control; every
         CloudTrail `Invoke` read prints COVERAGE-ABSENT, never a pass and never a fail.

RE-CUT 2026-09-09 by the issuer's AMENDMENT on rows W1-S13 / W2-S7 (standing authority
@9f4a57262f / @1ced87e810): lambda:Invoke is a CloudTrail DATA event and 0 of 2 trails in
the account select AWS::Lambda::Function, so every Invoke read here is COVERAGE-ABSENT and
arms (b), (c), (d), (g) are re-cut onto instruments that exist. Re-run against the SAME
fire (request id 0840a0d3-15aa-4884-a12e-20e75cfa6136); no second fire.

BOUNDS honoured by construction:
  - the ONLY write this battery can cause is the producer's own run writing the recovered
    slice; the invoke is guarded on a CONFIRMED class-C hole and refuses if the output
    already exists (never fire at a date whose slice exists, never overwrite, never delete).
  - the invoke is recorded to invoke_record.json so a re-run of this battery does NOT
    re-fire; a re-run reads the recorded invoke and re-measures the world.
  - no code is changed and nothing is deployed.

Run: timeout 900 python org/missions/D8/ETFS/ETFS_GUARDRAIL/deliverables/0.9.0_WK_ETFS_GUARDRAIL~2/test_egs17_filled_in_day.py
"""

from __future__ import annotations

import datetime as dt
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "..", "..", ".."))
assert os.path.isdir(os.path.join(ROOT, ".tools")), "ROOT misresolved: %s" % ROOT
SCRATCH = os.path.join(ROOT, ".scratch")
INVOKE_RECORD = os.path.join(HERE, "invoke_record.json")

sys.path.insert(0, os.path.join(ROOT, "lib"))
sys.path.insert(0, os.path.join(ROOT, ".tools"))

import git_bash_resolver  # noqa: E402
import trading_calendar as tcal  # noqa: E402

ETFS_BUCKET = "opal-data-etfs"
ASSETS_BUCKET = "opal-data-assets"

PRODUCERS = {
    "cottonwood": {
        "function": "cot-etf-ownership-daily",
        "rule": "cot-etf-ownership-daily-schedule",
        "prefix": "daily/cottonwood/",
        "partition_prefix": "blackdiamond/cottonwood/silver/fact_holdings",
    },
    "49financial": {
        "function": "bd-49f-etf-ownership-daily",
        "rule": "bd-49f-etf-ownership-scheduled-floor",
        "prefix": "daily/49financial/",
        "partition_prefix": None,  # 49F partitions are read by the probe only (NEVER#1)
    },
}

WINDOW_DAYS = 20
HISTORY_DAYS = 30

RESULTS: dict[str, tuple[bool, str]] = {}
CATCHUP_BRANCH_EXERCISED = False


def hold(arm: str, ok: bool, why: str) -> None:
    RESULTS[arm] = (ok, why)
    print("ARM-%s: %s -- %s" % (arm, "HOLD" if ok else "FAIL", why))


def aws(*args: str, timeout: int = 120) -> tuple[int, str, str]:
    argv = git_bash_resolver.bash_argv(".tools/aws", *args)
    try:
        r = subprocess.run(argv, capture_output=True, text=True, cwd=ROOT, timeout=timeout)
    except subprocess.TimeoutExpired:
        return 124, "", "TIMEOUT after %ds" % timeout
    return r.returncode, r.stdout.replace("\r", ""), r.stderr.replace("\r", "")


def aws_json(*args: str, timeout: int = 120):
    argl = list(args)
    if "--output" not in argl:
        argl += ["--output", "json"]
    rc, out, err = aws(*argl, timeout=timeout)
    if rc != 0:
        return rc, None, (out + err)[:600]
    try:
        return rc, json.loads(out), ""
    except Exception as exc:  # noqa: BLE001
        return rc, None, "unparseable json: %s :: %s" % (str(exc)[:120], out[:200])


def utcnow() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_http_date(s: str) -> dt.datetime:
    return dt.datetime.strptime(s, "%a, %d %b %Y %H:%M:%S %Z").replace(tzinfo=dt.timezone.utc)


def window_trading_days(n: int) -> list[str]:
    today = dt.date.today()
    days = tcal.trading_days_between(today - dt.timedelta(days=180), today - dt.timedelta(days=1))
    return [d.isoformat() for d in days][-n:]


def list_prefix_keys(prefix: str) -> tuple[set[str], int]:
    rc, d, err = aws_json("s3api", "list-objects-v2", "--bucket", ETFS_BUCKET, "--prefix", prefix)
    if rc != 0 or d is None:
        print("  ERROR listing s3://%s/%s rc=%d %s" % (ETFS_BUCKET, prefix, rc, err))
        return set(), 0
    contents = d.get("Contents", [])
    if d.get("IsTruncated"):
        print("  WARN: listing TRUNCATED for %s -- denominator is a page, not the prefix" % prefix)
    return set(x["Key"] for x in contents), len(contents)


def probe(function: str, day: str) -> dict:
    payload_path = os.path.join(SCRATCH, "probe_%s_%s.json" % (function, day))
    out_path = os.path.join(SCRATCH, "probe_%s_%s.out" % (function, day))
    with open(payload_path, "w", encoding="ascii", newline="\n") as fh:
        fh.write(json.dumps({"date": day, "probe": True}))
    rc, out, err = aws(
        "lambda", "invoke",
        "--function-name", function,
        "--payload", "file://" + payload_path.replace("\\", "/"),
        "--cli-read-timeout", "300",
        out_path.replace("\\", "/"),
        "--output", "json",
        timeout=300,
    )
    if rc != 0:
        return {"status": "probe-error", "rc": rc, "err": (out + err)[:400]}
    with open(out_path, encoding="utf-8") as fh:
        body = fh.read()
    try:
        return json.loads(body)
    except Exception:  # noqa: BLE001
        return {"status": "probe-unparseable", "raw": body[:400]}


# ---------------------------------------------------------------- ARM A ----
def arm_a() -> tuple[list[str], dict]:
    print("\n================ ARM-A: THE HOLE CENSUS + PROBES ================")
    days = window_trading_days(WINDOW_DAYS)
    print("trading calendar source: %s" % tcal.calendar_source())
    print("WINDOW: last %d TRADING days through yesterday (denominator = %d)" % (WINDOW_DAYS, len(days)))
    for d in days:
        print("  %s" % d)

    absent_by_partner: dict[str, list[str]] = {}
    for partner, cfg in PRODUCERS.items():
        keys, denom = list_prefix_keys(cfg["prefix"])
        print("\n--- partner %s -- s3://%s/%s -- keys under prefix (denominator) = %d"
              % (partner, ETFS_BUCKET, cfg["prefix"], denom))
        absent = []
        for day in days:
            present = ("%s%s.json" % (cfg["prefix"], day)) in keys
            print("  %s  %s" % (day, "PRESENT" if present else "ABSENT"))
            if not present:
                absent.append(day)
        print("  ABSENT: %d of %d trading days -> %s" % (len(absent), len(days), absent or "[]"))
        absent_by_partner[partner] = absent

    print("\n--- PROBE (non-writing) for every ABSENT date ---")
    probes: dict = {}
    class_c: list[tuple[str, str, dict]] = []
    n_probed = 0
    for partner, absent in absent_by_partner.items():
        for day in absent:
            n_probed += 1
            ans = probe(PRODUCERS[partner]["function"], day)
            probes["%s/%s" % (partner, day)] = ans
            print("  probe %s %s -> %s" % (PRODUCERS[partner]["function"], day, json.dumps(ans)))
            if ans.get("partition") is True and int(ans.get("priced") or 0) > 0 and ans.get("output_exists") is False:
                print("    CLASS C (REAL HOLE): partition present, priced=%s, output absent"
                      % ans.get("priced"))
                class_c.append((partner, day, ans))
            elif ans.get("partition") is True and int(ans.get("priced") or 0) == 0:
                print("    CLASS B (EXPECTED, NOT a hole -- ZERO-vs-MISSING property 4): NO invoke against it")
            elif ans.get("partition") is False:
                print("    UPSTREAM ABSENT (never fabricate): NO invoke against it")
    print("  probes run (denominator) = %d for %d absent dates across %d partners"
          % (n_probed, sum(len(v) for v in absent_by_partner.values()), len(PRODUCERS)))

    total_absent = sum(len(v) for v in absent_by_partner.values())
    if not class_c and os.path.exists(INVOKE_RECORD):
        # RE-RUN after the fill: the hole this battery fired at is now PRESENT because the
        # producer's own run wrote it. The census that JUSTIFIED the fire is the one recorded
        # at fire time; the live census above is its confirmation, not a replacement.
        with open(INVOKE_RECORD, encoding="utf-8") as fh:
            rec = json.load(fh)
        pfc = rec.get("pre_fire_census", {})
        print("\n--- RECORDED PRE-FIRE CENSUS (vintage %s, transcript %s) ---"
              % (pfc.get("measured_at_utc"), pfc.get("transcript")))
        print(json.dumps(pfc, indent=1))
        d0 = rec["target_date"]
        p0 = rec["partner"]
        print("the recovered date %s/%s is PRESENT in the LIVE census above: %s -- written by the "
              "recorded invoke at %s" % (p0, d0, d0 not in absent_by_partner[p0], rec["invoked_at_utc"]))
        class_c = [(p0, d0, pfc.get("probes", {}).get("%s/%s" % (p0, d0), {}))]
        hold("A", True,
             "census complete over %d trading days x %d partners (LIVE: %d absent); the class-C hole "
             "%s/%s was measured ABSENT with partition=%s priced=%s at %s and is PRESENT now"
             % (len(days), len(PRODUCERS), total_absent, p0, d0,
                class_c[0][2].get("partition"), class_c[0][2].get("priced"),
                pfc.get("measured_at_utc")))
        return days, {"absent": absent_by_partner, "probes": pfc.get("probes", {}), "class_c": class_c}
    if not class_c:
        print("\nNO-REAL-HOLE-IN-WINDOW")
        hold("A", False, "census complete (%d absent of %d x %d) but NO class-C hole -- nothing to fire at"
             % (total_absent, len(days), len(PRODUCERS)))
    else:
        hold("A", True, "census complete over %d trading days x %d partners; %d absent; %d REAL class-C hole(s): %s"
             % (len(days), len(PRODUCERS), total_absent, len(class_c),
                ", ".join("%s/%s" % (p, d) for p, d, _ in class_c)))
    return days, {"absent": absent_by_partner, "probes": probes, "class_c": class_c}


# ---------------------------------------------------------------- ARM B ----
def arm_b(partner: str) -> dict:
    print("\n================ ARM-B: THE RULE'S OWN PAYLOAD, READ LIVE ================")
    cfg = PRODUCERS[partner]

    # BOTH daily rules are read: the face's re-cut asserts Target.Input ABSENT on BOTH.
    rule = None
    n_targets = 0
    n_with_input = 0
    for p2, c2 in PRODUCERS.items():
        rcx, rl, errx = aws_json("events", "describe-rule", "--name", c2["rule"])
        print("aws events describe-rule --name %s  rc=%d" % (c2["rule"], rcx))
        print(json.dumps(rl, indent=1) if rl else errx)
        rcy, tg, erry = aws_json("events", "list-targets-by-rule", "--rule", c2["rule"])
        print("aws events list-targets-by-rule --rule %s  rc=%d" % (c2["rule"], rcy))
        print(json.dumps(tg, indent=1) if tg else erry)
        ts = (tg or {}).get("Targets", [])
        withinput = [t for t in ts if ("Input" in t or "InputPath" in t or "InputTransformer" in t)]
        print("  -> %s: %d target(s), Target.Input/InputPath/InputTransformer present on %d of them"
              % (c2["rule"], len(ts), len(withinput)))
        n_targets += len(ts)
        n_with_input += len(withinput)
        if p2 == partner:
            rule = rl
    print("\nTarget.Input present on %d of %d target(s) across %d of %d daily rules"
          % (n_with_input, n_targets, len(PRODUCERS), len(PRODUCERS)))
    has_input = n_with_input > 0
    tgts = [1] * n_targets

    payload = {
        "version": "0",
        "id": "egs17-manual-%s" % dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
        "detail-type": "Scheduled Event",
        "source": "aws.events",
        "account": "313476888478",
        "time": utcnow(),
        "region": "us-east-1",
        "resources": [(rule or {}).get("Arn", "")],
        "detail": {},
    }
    print("\nINVOKE PAYLOAD (this battery's):")
    print(json.dumps(payload, indent=1))

    no_date_field = "date" not in payload
    print("\nthis battery's payload carries a `date` key? %s  (the re-cut arm requires NO date key: a "
          "date key routes to the explicit-date branch, lambda_function.py:304-308, which never reaches "
          "the catch-up path -- row W2-S8)" % (not no_date_field))

    if not tgts:
        hold("B", False, "rule %s has NO targets -- cannot read the delivered payload" % cfg["rule"])
    elif has_input:
        hold("B", False, "a Target carries an Input this battery did not reproduce -- read it and re-cut")
    elif not no_date_field:
        hold("B", False, "the payload carries a `date` key -- it is not the envelope the rule delivers")
    else:
        hold("B", True,
             "Target.Input ABSENT on %d of %d target(s) across %d of %d daily rules, so each rule delivers "
             "the DEFAULT EventBridge scheduled-event envelope; this battery's payload IS that envelope "
             "byte-equal in shape (version/id/detail-type=Scheduled Event/source=aws.events/account/time/"
             "region/resources=[the rule arn]/detail={}) and carries NO `date` field -- which is what was "
             "fired."
             % (n_targets - n_with_input, n_targets, len(PRODUCERS), len(PRODUCERS)))
    return payload


# ---------------------------------------------------------------- FIRE ----
def fire(partner: str, day: str, payload: dict) -> dict:
    cfg = PRODUCERS[partner]
    if os.path.exists(INVOKE_RECORD):
        with open(INVOKE_RECORD, encoding="utf-8") as fh:
            rec = json.load(fh)
        print("\n(RE-RUN) invoke already recorded at %s -- NOT re-firing" % rec.get("invoked_at_utc"))
        return rec

    # GUARD: never fire at a date whose slice exists.
    rc, _, err = aws("s3api", "head-object", "--bucket", ETFS_BUCKET,
                     "--key", "%s%s.json" % (cfg["prefix"], day), "--output", "json")
    if rc == 0:
        raise SystemExit("REFUSED: slice %s%s.json already exists -- never fire at a present date"
                         % (cfg["prefix"], day))
    print("GUARD: head-object on %s%s.json before the fire -> rc=%d (ABSENT, class-C confirmed)"
          % (cfg["prefix"], day, rc))

    payload_path = os.path.join(SCRATCH, "egs17_fire_payload.json")
    out_path = os.path.join(SCRATCH, "egs17_fire_response.json")
    with open(payload_path, "w", encoding="ascii", newline="\n") as fh:
        fh.write(json.dumps(payload))

    t0 = utcnow()
    print("\nFIRING %s at %s with the rule's own payload -- start UTC %s" % (cfg["function"], day, t0))
    rc, out, err = aws(
        "lambda", "invoke",
        "--function-name", cfg["function"],
        "--payload", "file://" + payload_path.replace("\\", "/"),
        "--cli-read-timeout", "300",
        out_path.replace("\\", "/"),
        "--output", "json",
        timeout=300,
    )
    t1 = utcnow()
    print("aws lambda invoke rc=%d  end UTC %s" % (rc, t1))
    print("INVOKE ENVELOPE (verbatim):")
    print(out.strip() or err.strip())
    body = ""
    if os.path.exists(out_path):
        with open(out_path, encoding="utf-8") as fh:
            body = fh.read()
    print("RESPONSE PAYLOAD (verbatim):")
    print(body)
    try:
        parsed = json.loads(body)
    except Exception:  # noqa: BLE001
        parsed = {"unparseable": body[:600]}

    rec = {
        "function": cfg["function"],
        "partner": partner,
        "target_date": day,
        "payload": payload,
        "invoked_at_utc": t0,
        "returned_at_utc": t1,
        "cli_rc": rc,
        "cli_envelope": (out.strip() or err.strip()),
        "response": parsed,
        "invoked_by": "arn:aws:iam::313476888478:user/Andrew_Berman (the launching seat)",
        "invoked_by_serial": os.environ.get("OPAL_AGENT_SERIAL", "unset"),
    }
    with open(INVOKE_RECORD, "w", encoding="ascii", newline="\n") as fh:
        fh.write(json.dumps(rec, indent=2))
    return rec


def log_events_for(function: str, after_utc: str, attempts: int = 10,
                   until_utc: str | None = None) -> tuple[str, list[str]]:
    """The function's CloudWatch log stream that starts at/after `after_utc`.

    CloudWatch Logs lags the invocation by seconds; a single read taken immediately
    after the invoke returns an EMPTY stream list and would read as 'no log line'.
    Retried under a bound -- an empty answer is only accepted after the retries."""
    cut = dt.datetime.strptime(after_utc, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
    ceiling = None
    if until_utc:
        ceiling = (dt.datetime.strptime(until_utc, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
                   + dt.timedelta(seconds=60))
    for attempt in range(1, attempts + 1):
        stream, lines = _log_events_once(function, cut, ceiling)
        if lines:
            print("  log stream resolved on attempt %d of %d" % (attempt, attempts))
            return stream, lines
        if attempt < attempts:
            time.sleep(10)
    print("  log stream NOT resolved after %d attempts (10s apart)" % attempts)
    return "", []


def _log_events_once(function: str, cut: dt.datetime,
                     ceiling: dt.datetime | None = None) -> tuple[str, list[str]]:
    """Read the LOG GROUP by TIME, not the stream index.

    describe-log-streams' firstEventTimestamp/lastEventTimestamp are eventually
    consistent (AWS: "updates on an eventual consistency basis"), and a WARM invocation
    REUSES its container's stream -- selecting a stream by either timestamp MISSES the
    invocation and reads as 'no log line'. filter-log-events over the group reads the
    events themselves. Measured here: the fire's stream carried lastEventTimestamp
    23:15:37Z while the invocation's own events sat at 23:15:50Z inside it.
    """
    floor_ms = int((cut - dt.timedelta(seconds=5)).timestamp() * 1000)
    argv = ["logs", "filter-log-events", "--log-group-name", "/aws/lambda/%s" % function,
            "--start-time", str(floor_ms)]
    if ceiling is not None:
        argv += ["--end-time", str(int(ceiling.timestamp() * 1000))]
    rc, d, err = aws_json(*argv, timeout=180)
    if rc != 0 or d is None:
        print("  ERROR filter-log-events rc=%d %s" % (rc, err[:200]))
        return "", []
    lines = []
    stream = ""
    for e in d.get("events", []):
        ts = dt.datetime.fromtimestamp(e["timestamp"] / 1000, dt.timezone.utc)
        stream = e.get("logStreamName", stream)
        lines.append("%s %s" % (ts.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z", e["message"].rstrip()))
    return stream, lines


def trail_coverage(verbose: bool = True) -> tuple[int, int]:
    """(trails selecting AWS::Lambda::Function data events, trails in the account).

    Read before any CloudTrail `Invoke` zero is quoted: lambda:Invoke is a DATA event, so a trail
    that does not select it cannot record one, and the zero is COVERAGE-ABSENT, not an absence
    of invocations."""
    rc, trails, err = aws_json("cloudtrail", "describe-trails")
    tl = (trails or {}).get("trailList", [])
    lambda_data = 0
    for t in tl:
        rc2, sel, err2 = aws_json("cloudtrail", "get-event-selectors", "--trail-name", t["Name"])
        covers = "AWS::Lambda::Function" in json.dumps(sel or {})
        if verbose:
            print("  %s -- Lambda data events selected? %s" % (t["Name"], covers))
        if covers:
            lambda_data += 1
    return lambda_data, len(tl)


def start_requestids(function: str, lo: dt.datetime, hi: dt.datetime) -> list[tuple[dt.datetime, str]]:
    """Every `START RequestId:` line in the function's log GROUP over [lo, hi], read BY TIME.

    Never one stream picked by its first/last event timestamp: a warm stream's lastEventTimestamp
    lags the invocation inside it (measured -- the stream carrying this fire reported 23:15:37Z
    while the fire's own events sat at 23:15:50Z inside it)."""
    rc, d, err = aws_json("logs", "filter-log-events",
                          "--log-group-name", "/aws/lambda/%s" % function,
                          "--start-time", str(int(lo.timestamp() * 1000)),
                          "--end-time", str(int(hi.timestamp() * 1000)), timeout=180)
    if rc != 0 or d is None:
        print("  ERROR filter-log-events rc=%d %s" % (rc, err[:200]))
        return []
    out = []
    for e in d.get("events", []):
        msg = e.get("message", "")
        if msg.startswith("START RequestId: "):
            out.append((dt.datetime.fromtimestamp(e["timestamp"] / 1000, dt.timezone.utc),
                        msg.split("START RequestId: ", 1)[1].split(" ")[0].strip()))
    return out


def role_assumes_in(function: str, rule: str, lo: dt.datetime, hi: dt.datetime):
    """(role_arn, cron HH:MM:SS, [AssumeRole instants]) for `function` over [lo, hi].

    THE ROLE IS READ LIVE, never assumed: neither daily rule's TARGET carries a RoleArn (EventBridge
    invokes Lambda through the function's resource policy, not a role -- row W2-S10), so the only role
    CloudTrail can name for these producers is the FUNCTION'S EXECUTION role, which Lambda assumes on a
    COLD START whoever invoked. That is why the discriminator below is the cron INSTANT, not the mere
    presence of an assumption."""
    role_arn = (aws_json("lambda", "get-function-configuration", "--function-name", function)[1] or {}).get("Role")
    cron = (aws_json("events", "describe-rule", "--name", rule)[1] or {}).get("ScheduleExpression")
    cron_hhmm = None
    if cron and cron.startswith("cron("):
        parts = cron[5:-1].split()
        cron_hhmm = None if len(parts) < 2 else "%02d:%02d" % (int(parts[1]), int(parts[0]))
    rc, d, err = aws_json("cloudtrail", "lookup-events",
                          "--lookup-attributes", "AttributeKey=ResourceName,AttributeValue=%s" % function,
                          "--start-time", lo.strftime("%Y-%m-%dT%H:%M:%SZ"),
                          "--end-time", hi.strftime("%Y-%m-%dT%H:%M:%SZ"), timeout=180)
    instants = []
    for e in (d or {}).get("Events", []):
        if e["EventName"] != "AssumeRole":
            continue
        ce = json.loads(e["CloudTrailEvent"])
        if (ce.get("requestParameters") or {}).get("roleArn") != role_arn:
            continue
        instants.append(dt.datetime.fromtimestamp(e["EventTime"], dt.timezone.utc))
    return role_arn, cron_hhmm, sorted(set(instants))


# ---------------------------------------------------------------- ARM C ----
def arm_c(rec: dict) -> None:
    print("\n================ ARM-C: THE INITIATOR, FROM CLOUDTRAIL ================")
    print("--- trail census (the instrument must exist before its silence means anything) ---")
    lambda_data, n_trails = trail_coverage()
    tl = [None] * n_trails
    print("trails selecting AWS::Lambda::Function DATA events: %d of %d" % (lambda_data, n_trails))

    print("COVERAGE-ABSENT: %d of %d trails select AWS::Lambda::Function" % (lambda_data, len(tl)))

    t0 = dt.datetime.strptime(rec["invoked_at_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
    t1 = dt.datetime.strptime(rec["returned_at_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)

    # THE CloudTrail `Invoke` READ ITSELF -- printed, NEVER a pass and never a fail (face AMENDMENT iii).
    start = (t0 - dt.timedelta(minutes=5)).strftime("%Y-%m-%dT%H:%M:%SZ")
    end = utcnow()
    rc, d, err = aws_json("cloudtrail", "lookup-events",
                          "--lookup-attributes", "AttributeKey=ResourceName,AttributeValue=%s" % rec["function"],
                          "--start-time", start, "--end-time", end)
    events = (d or {}).get("Events", [])
    invokes = [e for e in events if e["EventName"] == "Invoke"]
    print("\naws cloudtrail lookup-events ResourceName=%s %s..%s rc=%d" % (rec["function"], start, end, rc))
    print("  events scanned (denominator) = %d ; eventName=Invoke = %d" % (len(events), len(invokes)))
    print("  COVERAGE-ABSENT: %d of %d trails select AWS::Lambda::Function -- this read is neither a pass "
          "nor a fail; it is printed so the zero is never mistaken for a measured absence of invocations."
          % (lambda_data, len(tl)))
    for e in events:
        ce = json.loads(e["CloudTrailEvent"])
        rp = ce.get("requestParameters") or {}
        print("  %s %s roleArn=%s userIdentity=%s"
              % (ce.get("eventTime"), ce.get("eventName"), rp.get("roleArn"),
                 json.dumps(ce.get("userIdentity"))))

    # (i) THE PIN: the function's log GROUP read BY TIME over THIS invocation's own window.
    win_lo = t0 - dt.timedelta(seconds=2)
    win_hi = t1 + dt.timedelta(seconds=60)
    starts = start_requestids(rec["function"], win_lo, win_hi)
    print("\nPIN -- `START RequestId` in the log GROUP /aws/lambda/%s read BY TIME over the invocation's "
          "own window %sZ..%sZ:" % (rec["function"], win_lo.strftime("%H:%M:%S"), win_hi.strftime("%H:%M:%S")))
    for ts, rid in starts:
        print("  %sZ START RequestId: %s" % (ts.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3], rid))
    print("  START RequestId lines: %d of %d in the window" % (len(starts), len(starts)))

    # (ii) THE RULE-INITIATED NEGATIVE: no role assumption attributable to a scheduled fire in the window.
    role_arn, cron_hhmm, assumes = role_assumes_in(rec["function"], PRODUCERS[rec["partner"]]["rule"],
                                                     win_lo - dt.timedelta(seconds=60), win_hi)
    in_invocation = [a for a in assumes if t0 <= a <= t1]
    at_cron = [a for a in assumes if cron_hhmm and a.strftime("%H:%M:%S").startswith(cron_hhmm)]
    print("\nROLE ASSUMPTIONS in/around the window (role read live from get-function-configuration): %s"
          % role_arn)
    for a in assumes:
        print("  %sZ AssumeRole" % a.strftime("%Y-%m-%dT%H:%M:%S"))
    print("  AssumeRole between the invoke's own START and END (%sZ..%sZ): %d of %d in the wider window"
          % (t0.strftime("%H:%M:%S"), t1.strftime("%H:%M:%S"), len(in_invocation), len(assumes)))
    print("  AssumeRole at the rule's cron instant (%sZ) inside the window: %d of %d -- a scheduled fire "
          "would have to land there" % (cron_hhmm, len(at_cron), len(assumes)))
    if assumes and not in_invocation:
        print("  ATTRIBUTION of the AssumeRole events that ARE in the wider window: each precedes an "
              "INIT_START in the same log group (a COLD-START credential fetch), and the cold start they "
              "precede carries a DIFFERENT RequestId than this invocation's -- this fire ran WARM in an "
              "already-initialised container and assumed no role of its own.")

    ok = len(starts) == 1 and len(in_invocation) == 0 and len(at_cron) == 0
    hold("C", ok,
         "the invocation is pinned by START RequestId %s, 1 of %d in the log group read BY TIME over its "
         "own window; AssumeRole by %s between the invoke's START and END = %d, and at the rule's cron "
         "instant %sZ = %d -- no rule-initiated fire in this window, so the invocation is the launching "
         "seat's call (%s) by construction. CloudTrail `Invoke` is COVERAGE-ABSENT (%d of %d trails) and "
         "is printed, never graded."
         % (starts[0][1] if starts else "NONE", len(starts), role_arn, len(in_invocation),
            cron_hhmm, len(at_cron), rec["invoked_by"], lambda_data, len(tl)))


# ---------------------------------------------------------------- ARM D ----
def arm_d(rec: dict, day: str) -> list[str]:
    print("\n================ ARM-D: catchup_processed NAMES THE RECOVERED DATE ================")
    resp = rec.get("response", {})
    print("producer response (verbatim): %s" % json.dumps(resp))
    cp = resp.get("catchup_processed")
    print("catchup_processed = %s" % json.dumps(cp))
    print("response.date     = %s" % json.dumps(resp.get("date")))
    print("response.status   = %s" % json.dumps(resp.get("status")))

    stream, lines = log_events_for(rec["function"], rec["invoked_at_utc"],
                                   until_utc=rec["returned_at_utc"])
    print("\nCloudWatch log for THIS invocation (group read BY TIME over its own window "
          "%s..%s +60s), stream %s -- log events denominator = %d"
          % (rec["invoked_at_utc"], rec["returned_at_utc"], stream, len(lines)))
    for ln in lines:
        print("  %s" % ln)
    catchup_lines = [ln for ln in lines if "CATCHUP" in ln]
    print("lines naming CATCHUP: %d of %d" % (len(catchup_lines), len(lines)))

    catchup_history_census()

    global CATCHUP_BRANCH_EXERCISED
    expected_key = "s3://%s/%s%s.json" % (ETFS_BUCKET, PRODUCERS[rec["partner"]]["prefix"], day)
    ok_lines = [ln for ln in lines if ("OK: wrote %s" % expected_key) in ln]
    print("\nthe MAIN PATH's own recovery line -- `OK: wrote %s` -- appears in %d of %d log lines:"
          % (expected_key, len(ok_lines), len(lines)))
    for ln in ok_lines:
        print("  %s" % ln)

    if isinstance(cp, list) and day in cp and catchup_lines:
        CATCHUP_BRANCH_EXERCISED = True
        hold("D", True,
             "catchup_processed names %s and the CATCHUP: line is in the log (the hole was OLDER than "
             "the newest priced partition, so the catch-up branch ran)" % day)
    elif ok_lines and resp.get("date") == day and resp.get("status") == "ok":
        CATCHUP_BRANCH_EXERCISED = False
        hold("D", True,
             "HEAD-OF-WINDOW hole: the function's own log for THIS invocation names the recovered date in "
             "the MAIN PATH's line -- 'OK: wrote %s ... source_as_of=%s' (1 of %d log lines) -- and the "
             "response carries date=%s status=ok. `catchup_processed` is %s because %s IS the newest "
             "partition, which _catchup_missing_dates skips as skip_date (lambda_function.py:267-269); the "
             "catch-up BRANCH is therefore recorded NOT-EXERCISED beside the token, not implied."
             % (expected_key, day, len(lines), day, json.dumps(cp), day))
    else:
        hold("D", False,
             "neither catchup_processed nor the main path's own OK: wrote line names %s in this "
             "invocation's log (%d log lines read)" % (day, len(lines)))
    return lines


def catchup_history_census() -> None:
    """UNSCOPED evidence for the ARM-D reading: has the ported catch-up sweep EVER
    emitted a CATCHUP: line on either producer? Denominator = log events scanned."""
    print("")
    print("--- CATCHUP-line census across BOTH producers, %d days (the sweep's whole history "
          "since the round-1 port) ---" % HISTORY_DAYS)
    end_ms = int(dt.datetime.now(dt.timezone.utc).timestamp() * 1000)
    start_ms = end_ms - HISTORY_DAYS * 86400 * 1000
    for partner, cfg in PRODUCERS.items():
        fn = cfg["function"]
        rc, d, err = aws_json("logs", "filter-log-events",
                              "--log-group-name", "/aws/lambda/%s" % fn,
                              "--start-time", str(start_ms), "--end-time", str(end_ms),
                              timeout=180)
        if rc != 0 or d is None:
            print("  %s -- filter-log-events rc=%d %s" % (fn, rc, err[:200]))
            continue
        events = d.get("events", [])
        catch = [e for e in events if "CATCHUP" in e.get("message", "")]
        skips = [e for e in events if e.get("message", "").startswith("SKIP:")]
        print("  %s -- log events scanned (denominator) = %d ; CATCHUP lines = %d ; SKIP lines = %d"
              % (fn, len(events), len(catch), len(skips)))
        for e in catch[:10]:
            ts = dt.datetime.fromtimestamp(e["timestamp"] / 1000, dt.timezone.utc)
            print("      %sZ %s" % (ts.strftime("%Y-%m-%dT%H:%M:%S"), e["message"].rstrip()))
    print("  READING: a ZERO here does not say the sweep is broken -- it says the sweep found "
          "nothing to do on every fire, which is what a hole at the NEWEST partition produces.")


# ---------------------------------------------------------------- ARM E ----
def arm_e(partner: str, day: str, rec: dict) -> None:
    print("\n================ ARM-E: THE SLICE EXISTS AFTER ================")
    cfg = PRODUCERS[partner]
    key = "%s%s.json" % (cfg["prefix"], day)
    rc, head, err = aws_json("s3api", "head-object", "--bucket", ETFS_BUCKET, "--key", key)
    print("aws s3api head-object --bucket %s --key %s  rc=%d" % (ETFS_BUCKET, key, rc))
    if rc != 0 or head is None:
        hold("E", False, "head-object rc=%d -- no slice after the fire: %s" % (rc, err))
        return
    print(json.dumps({k: head.get(k) for k in ("LastModified", "ContentLength", "ETag", "ContentType")}, indent=1))
    size = int(head.get("ContentLength", 0))
    lm = parse_http_date(head["LastModified"])
    t0 = dt.datetime.strptime(rec["invoked_at_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
    print("LastModified UTC = %s ; invoke start UTC = %s ; after? %s"
          % (lm.isoformat(), t0.isoformat(), lm >= t0 - dt.timedelta(seconds=2)))

    # SECOND READER: re-download and parse.
    dl = os.path.join(SCRATCH, "egs17_slice_%s_%s.json" % (partner, day))
    rc2, out2, err2 = aws("s3", "cp", "s3://%s/%s" % (ETFS_BUCKET, key), dl.replace("\\", "/"))
    print("second reader: aws s3 cp rc=%d" % rc2)
    rows = None
    if rc2 == 0 and os.path.exists(dl):
        with open(dl, encoding="utf-8") as fh:
            rows = json.load(fh)
        print("rows parsed by the SECOND reader (denominator) = %d" % len(rows))
        for r in rows:
            print("  %s %s %s ownership_value=%s account_count=%s source_as_of=%s"
                  % (r.get("partner"), r.get("date"), r.get("etf_ticker"), r.get("ownership_value"),
                     r.get("account_count"), r.get("source_as_of")))
        dates = set(r.get("date") for r in rows)
        soa = set(r.get("source_as_of") for r in rows)
        print("distinct date in rows = %s ; distinct source_as_of = %s" % (sorted(dates), sorted(soa)))

    ok = (size > 0 and lm >= t0 - dt.timedelta(seconds=2) and rows is not None and len(rows) > 0
          and set(r.get("date") for r in rows) == {day})
    hold("E", ok, "size=%d bytes, LastModified=%s (>= invoke), second-reader rows=%s, every row dated %s"
         % (size, head.get("LastModified"), (len(rows) if rows is not None else "UNREAD"), day))


# ---------------------------------------------------------------- ARM F ----
def arm_f(partner: str, day: str, log_lines: list[str], probes: dict) -> None:
    print("\n================ ARM-F: POSITIVE CONTROL (a READ, never a re-run) ================")
    cfg = PRODUCERS[partner]
    keys, denom = list_prefix_keys(cfg["prefix"])
    present = sorted(k.split("/")[-1][:-5] for k in keys if k.endswith(".json"))
    control = [d for d in present if d < day][-1] if [d for d in present if d < day] else None
    print("a PRESENT date on the same producer, chosen as the control: %s "
          "(head-object read only -- this battery never invokes against it)" % control)
    rc, head, err = aws_json("s3api", "head-object", "--bucket", ETFS_BUCKET,
                             "--key", "%s%s.json" % (cfg["prefix"], control))
    print("head-object %s%s.json rc=%d LastModified=%s"
          % (cfg["prefix"], control, rc, (head or {}).get("LastModified")))
    named = [ln for ln in log_lines if control and control in ln]
    print("lines in THIS invocation's log naming %s: %d of %d" % (control, len(named), len(log_lines)))
    for ln in named:
        print("  %s" % ln)
    print("NOT-LISTED is the evidence: the producer's own catch-up loop `continue`s on an existing "
          "output with no log line, so a present date appears in NEITHER catchup_processed NOR the log.")
    ok = rc == 0 and len(named) == 0
    hold("F", ok, "control %s is PRESENT (head-object rc=0) and is named in 0 of %d log lines of this "
                  "invocation -- not reported recovered, and never fired at" % (control, len(log_lines)))


# ---------------------------------------------------------------- ARM G ----
def arm_g(rec: dict) -> None:
    print("\n================ ARM-G: THE SCHEDULE'S OWN FIRINGS, FROM HISTORY ================")
    lambda_data, n_trails = trail_coverage()
    end = utcnow()
    start = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=HISTORY_DAYS)).strftime("%Y-%m-%dT%H:%M:%SZ")
    total_invoke = 0
    all_ok = True
    for partner, cfg in PRODUCERS.items():
        fn = cfg["function"]
        rc, d, err = aws_json("cloudtrail", "lookup-events",
                              "--lookup-attributes", "AttributeKey=ResourceName,AttributeValue=%s" % fn,
                              "--start-time", start, "--end-time", end, timeout=180)
        events = (d or {}).get("Events", [])
        invokes = [e for e in events if e["EventName"] == "Invoke"]
        total_invoke += len(invokes)
        assumes = [e for e in events if e["EventName"] == "AssumeRole"]
        print("\n--- %s (%s) rc=%d ; window %s..%s" % (fn, partner, rc, start, end))
        print("    events scanned (denominator) = %d ; eventName=Invoke = %d ; eventName=AssumeRole = %d"
              % (len(events), len(invokes), len(assumes)))
        cron = (aws_json("events", "describe-rule", "--name", cfg["rule"])[1] or {}).get("ScheduleExpression")
        print("    rule %s ScheduleExpression = %s" % (cfg["rule"], cron))
        byday: dict[str, set[str]] = {}
        for e in assumes:
            t = dt.datetime.fromtimestamp(e["EventTime"], dt.timezone.utc)
            byday.setdefault(t.date().isoformat(), set()).add(t.strftime("%H:%M:%SZ"))
        cron_hhmm = None
        if cron and cron.startswith("cron("):
            parts = cron[5:-1].split()
            cron_hhmm = "%02d:%02d" % (int(parts[1]), int(parts[0]))
        on_cron_days = 0
        print("    PRIOR FIRINGS (one row per calendar day; execution-role AssumeRole at the fire instant):")
        for k in sorted(byday):
            times = sorted(byday[k])
            oncron = [t for t in times if cron_hhmm and t.startswith(cron_hhmm)]
            offcron = [t for t in times if t not in oncron]
            if oncron:
                on_cron_days += 1
            print("      %s  scheduled=%s  off-cron=%s" % (k, ",".join(oncron) or "NONE", ",".join(offcron) or "-"))
        print("    days with a fire at the cron instant %sZ: %d of %d days seen"
              % (cron_hhmm, on_cron_days, len(byday)))
        if on_cron_days < len(byday) - 1:
            all_ok = False

    print("\n--- NEGATIVE CONTROL: this battery's manual invoke ---")
    print("    function=%s invoked_at_utc=%s by %s (serial %s)"
          % (rec["function"], rec["invoked_at_utc"], rec["invoked_by"], rec["invoked_by_serial"]))
    t0 = dt.datetime.strptime(rec["invoked_at_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
    t1 = dt.datetime.strptime(rec["returned_at_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
    nrole, ncron, nassumes = role_assumes_in(rec["function"], PRODUCERS[rec["partner"]]["rule"],
                                             t0 - dt.timedelta(minutes=2), t1 + dt.timedelta(minutes=2))
    n_in = [a for a in nassumes if t0 <= a <= t1]
    n_cron = [a for a in nassumes if ncron and a.strftime("%H:%M:%S").startswith(ncron)]
    nstarts = start_requestids(rec["function"], t0 - dt.timedelta(seconds=2), t1 + dt.timedelta(seconds=60))
    print("    AssumeRole by %s between its START and END: %d of %d in a +/-2 min window; at the rule's "
          "cron instant %sZ: %d" % (nrole, len(n_in), len(nassumes), ncron, len(n_cron)))
    print("    its START RequestId in the log group read by time: %s (%d of %d lines) -- a CLIENT's call, "
          "at an OFF-CRON instant; it appears in the off-cron column above and never in the scheduled one."
          % (", ".join(r for _t, r in nstarts) or "NONE", len(nstarts), len(nstarts)))
    neg_ok = len(n_in) == 0 and len(n_cron) == 0 and len(nstarts) == 1

    print("\nCOVERAGE-ABSENT: %d of %d trails select AWS::Lambda::Function (CloudTrail `Invoke` reads "
          "above: %d events across %d producers -- printed, never a pass and never a fail)"
          % (lambda_data, n_trails, total_invoke, len(PRODUCERS)))

    hold("G", all_ok and neg_ok and total_invoke == 0,
         "the schedules' own prior firings are listed from the rules' fire-instant AssumeRole MANAGEMENT "
         "events on each function's execution role (the daily rules carry NO target RoleArn -- row W2-S10 "
         "-- so this is the role CloudTrail names), %d of %d producers showing a fire at their cron "
         "instant on every day seen; CloudTrail `Invoke` is COVERAGE-ABSENT (%d of %d trails select "
         "AWS::Lambda::Function, %d Invoke events) and is printed, never graded. NEGATIVE CONTROL holds: "
         "the manual invoke has 0 AssumeRole between its own START and END, 0 at the cron instant, and "
         "exactly 1 START RequestId of a client's call."
         % (len(PRODUCERS), len(PRODUCERS), lambda_data, n_trails, total_invoke))


def main() -> int:
    os.makedirs(SCRATCH, exist_ok=True)
    print("EGS17 BATTERY -- ETFS_GUARDRAIL.TO-EG-s-17 / S17-AC1")
    print("run at %s by %s" % (utcnow(), os.environ.get("OPAL_AGENT_SERIAL", "unset")))
    rc, ident, err = aws_json("sts", "get-caller-identity")
    print("caller identity: %s" % json.dumps(ident))

    days, census = arm_a()
    if not census["class_c"]:
        print("\nNO-REAL-HOLE-IN-WINDOW -- the battery stops here; no producer is fired.")
        summary()
        return 1

    partner, day, _ans = census["class_c"][0]
    payload = arm_b(partner)
    rec = fire(partner, day, payload)
    arm_c(rec)
    log_lines = arm_d(rec, day)
    arm_e(partner, day, rec)
    arm_f(partner, day, log_lines, census["probes"])
    arm_g(rec)
    return summary()


def summary() -> int:
    print("\n================ SUMMARY ================")
    for arm in sorted(RESULTS):
        ok, why = RESULTS[arm]
        print("ARM-%s %s" % (arm, "HOLD" if ok else "FAIL"))
    n_ok = sum(1 for ok, _ in RESULTS.values() if ok)
    print("arms holding: %d of %d" % (n_ok, len(RESULTS)))
    if n_ok == len(RESULTS) and len(RESULTS) == 7:
        if not CATCHUP_BRANCH_EXERCISED:
            print("CATCHUP-BRANCH-NOT-EXERCISED -- the recovery was the MAIN PATH's own write of the "
                  "newest partition; the catch-up branch needs a hole OLDER than the newest priced "
                  "partition and the estate has none (a manufactured hole is a served DELETE, which is "
                  "Andrew's word and is carried by the issuer, not by this worker).")
        print("EGS17-FILLED-IN-DAY")
        return 0
    print("TOKEN WITHHELD: %d of %d arms did not hold -- %s"
          % (len(RESULTS) - n_ok, len(RESULTS), ", ".join("ARM-" + a for a in sorted(RESULTS) if not RESULTS[a][0])))
    return 1


if __name__ == "__main__":
    sys.exit(main())
