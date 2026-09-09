#!/usr/bin/env python3
"""NFRA_OUTSET.TO-OS-s-18 battery (O18-AC1): THE PUBLISH -- an outset tool's artifact reaching the
consumption seam, READABLE THERE BY THE RUNNER'S OWN ROLE, and a FAILED publish that reads FAILED
rather than as an absent section.

Run at both required file grains (path per the face AMENDED @cb43d05200, remedy (c) on row
NFRA_OUTSET-S18 -- this file was cut at `.tools/tests/` and cannot be committed there by this
seat, because a `<paths>` block grants only a `0.9.0_WK_*` serial and `.tools/tests/**` is lane
TOOL_BATTERIES):
  python org/missions/D11/NFRA/NFRA_OUTSET/deliverables/0.7.0_AE_CloudOps~W/test_os18_seam_readable.py
  python -m pytest -q org/missions/D11/NFRA/NFRA_OUTSET/deliverables/0.7.0_AE_CloudOps~W/test_os18_seam_readable.py

WHY THIS BATTERY IS NOT test_os10_seam.py AGAIN. OS-s-10's battery is deliberately NO-AWS: it
proves the seam's LOGIC against a tempfile directory and a stub S3 client. It passed, and the
estate still read nothing, because logic was never the thing that was missing -- a producer had
published nothing and the reading principal held no grant. So this battery is the opposite by
construction: it measures the WORLD. It reads the live bucket, it evaluates the live role, and its
green arms cannot pass against a fixture.

THE RED ARM IS THE ONE THAT MATTERS AND IT IS WHY THIS FILE IS LONG. `NFRA_OUTSET-W2-S21` measured
35,752 rows rendering as a confident ZERO with rc=0, answer_state OK, correct vintage, correct
denominators and a correct re-run recipe -- and four batteries with 51 green arms missed it, because
every fixture in the estate put rows at the top level and every arm exercised the happy path. An arm
set that only proves a good publish reads cannot distinguish a working seam from a silent one. So
every green arm here has a red sibling, ARM M plants a mutant to prove the red arms can actually
fire, and ARM R8 asserts the OK rendering and the FAILED rendering are NOT byte-identical.

NEVER-AUTO-DELETE (PRD R-5) IS ABSOLUTE AND SHAPES THE RED ARM. The seam-resident red-arm probe is
ONE object at a FIXED key that is OVERWRITTEN on each run and never deleted, so re-running this
battery a hundred times leaves one object, not a hundred. Nothing this battery writes is ever
removed.

Author: 0.7.0_AE_CloudOps~W (NFRA_OUTSET OS-s-18). 2026-09-09.
"""
from __future__ import annotations

import datetime as _dt
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

def _repo_root() -> Path:
    """DERIVED, never counted. This battery was cut at `.tools/tests/` where the root is
    `parents[2]`, and NFRA_OUTSET-S18's remedy (c) moved it to a deliverables folder six levels
    down -- so a hardcoded depth is the one line that could not survive its own relocation, and
    it would have failed as a WRONG ROOT (every path built from it missing) rather than as a
    move error. CLAUDE.md's own rule for this: derive the workspace root from
    `git rev-parse --show-toplevel`, never hardcode. The marker walk is the fallback for a
    checkout where git is not on PATH; both are location-independent, so the NEXT move of this
    file costs nothing."""
    here = Path(__file__).resolve()
    try:
        out = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=str(here.parent),
                             capture_output=True, text=True, timeout=30)
        if out.returncode == 0 and out.stdout.strip():
            return Path(out.stdout.strip()).resolve()
    except Exception:                                                       # noqa: BLE001
        pass
    for cand in here.parents:
        if (cand / ".owned-paths.yaml").is_file() and (cand / "CLAUDE.md").is_file():
            return cand
    raise RuntimeError("cannot derive the workspace root from %s -- refusing to guess" % here)


ROOT = _repo_root()
PRODUCER = ROOT / "org" / "modules" / "heatmap" / "outset_seam.py"
RUNNER = ROOT / "infra" / "aws" / "ec2" / "estate-report-runner" / "estate_report_runner.py"
TERRAFORM_IAM = ROOT / "infra" / "aws" / "terraform" / "estate-report" / "iam.tf"

REGION = "us-east-1"
BUCKET = "opal-estate-report"
BUCKET_ARN = "arn:aws:s3:::" + BUCKET
ROLE_ARN = "arn:aws:iam::313476888478:role/estate-report-runner-role"
INSTANCE_ID = "i-0512bd3cbaf602b7f"

# The seam prefix and the ONE key the consumer actually composes
# (estate_report_runner.py:1844 -> `<prefix>/comp_heat_drift.json`).
SEAM_PREFIX = "outset"
SEAM_KEY = SEAM_PREFIX + "/comp_heat_drift.json"
# The red arm's seam-resident probe. FIXED key, OVERWRITTEN, never deleted (PRD R-5).
RED_KEY = SEAM_PREFIX + "/_os18_red_arm_probe.json"
# A key that is NEVER published, for the ABSENT arm. Nothing writes this, ever.
ABSENT_KEY = SEAM_PREFIX + "/_os18_never_published.json"

# The runner reads six env vars AT IMPORT. Only the bucket is real; no arm depends on the others.
RUNNER_ENV = {
    "ESTATE_REPORT_BUCKET": BUCKET,
    "ESTATE_GITHUB_SECRET_ID": "x", "ESTATE_KIMI_SECRET_ID": "x",
    "ESTATE_KIMI_URL": "http://127.0.0.1:1", "ESTATE_KIMI_MODEL": "x",
    "ESTATE_REPO_URL": "http://127.0.0.1:1/x.git",
    "AWS_DEFAULT_REGION": REGION,
}

# ARM M's mutant. The seam's whole contract in one dict entry: a producer that FAILED maps to
# INSTRUMENT_FAILED. The mutant maps it to OK -- the exact "silent seam" shape W2-S21 found, where
# a broken instrument and a clean answer become byte-identical to the reader.
FAILED_ANCHOR = '    "FAILED": "INSTRUMENT_FAILED",\n'
FAILED_MUTANT = '    "FAILED": "OK",  # RED MUTANT: a failed publish reads as a clean answer\n'

RESULTS = []          # (arm, ok, detail)
NOT_EVALUATED = []    # (arm, reason) -- never a pass, never a failure


def _record(arm, ok, detail):
    RESULTS.append((arm, bool(ok), str(detail).replace("\n", " ")[:400]))


def _skip(arm, reason):
    """A verdict vocabulary with no NOT-EVALUATED value encodes non-evaluation as a verdict."""
    NOT_EVALUATED.append((arm, str(reason).replace("\n", " ")[:300]))


def _load(path, name, env=None):
    keep = {}
    for k, v in (env or {}).items():
        keep[k] = os.environ.get(k)
        os.environ[k] = v
    try:
        spec = importlib.util.spec_from_file_location(name, str(path))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    finally:
        for k, v in keep.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


def _utc_now():
    return _dt.datetime.now(_dt.timezone.utc)


def _iso(ts):
    return ts.astimezone(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# =============================================================================================
# AXIS 1 -- AUTHORIZATION. Can the RUNNER'S OWN ROLE read the seam?
#
# Two instruments on two different substrates, and the difference is the point (CLAUDE.md Rule 22:
# a second seat's confirmation via the FIRST seat's method is REPETITION, not corroboration):
#   ARM A1  EXERCISED  -- the role itself, on the box, making the real GetObject call. The only
#                         reading that is not a model of the world. Opportunistic: the host STOPS
#                         ITSELF after every run, so when it is down this is NOT-EVALUATED and
#                         never a pass.
#   ARM A2  APPLIED    -- iam:SimulatePrincipalPolicy against the live role. Always available.
# =============================================================================================

def arm_a1_exercised(b3):
    """The runner's own role, making the real call, on the box that holds it."""
    arm = "A1-EXERCISED-by-the-role-itself"
    try:
        ec2 = b3.client("ec2", region_name=REGION)
        st = ec2.describe_instances(InstanceIds=[INSTANCE_ID])
        state = st["Reservations"][0]["Instances"][0]["State"]["Name"]
    except Exception as e:                                                  # noqa: BLE001
        _skip(arm, "could not read instance state: %s: %s" % (type(e).__name__, str(e)[:120]))
        return
    if state != "running":
        _skip(arm, "instance %s is %r -- this host STOPS ITSELF after every run, so the role is "
                   "not holdable right now. NOT a pass and NOT a failure; ARM A2 carries the "
                   "authorization axis when this arm cannot run." % (INSTANCE_ID, state))
        return
    ssm = b3.client("ssm", region_name=REGION)
    # No pipes anywhere in these commands. A pipeline's rc is its LAST command's, so `cmd | head`
    # reports rc=0 for a command that was DENIED -- measured on this very probe 2026-09-09.
    cmds = [
        "set +e",
        "aws sts get-caller-identity --query Arn --output text",
        "aws s3api get-object --bucket %s --key %s /tmp/os18_green.json > /dev/null 2>/tmp/os18_green.err"
        % (BUCKET, SEAM_KEY),
        'echo "GREEN_RC=$?"',
        'echo "GREEN_BYTES=$(wc -c < /tmp/os18_green.json 2>/dev/null || echo 0)"',
        # NEGATIVE CONTROL, and it is sharp on purpose: logs/ holds REAL objects and the role has
        # PutObject there and NOT GetObject. So a deny here is an ACTION-level deny on an object
        # that exists -- not the 403-because-absent that an unpublished key would return.
        "aws s3api get-object --bucket %s --key %s /tmp/os18_neg.json > /dev/null 2>/tmp/os18_neg.err"
        % (BUCKET, "logs/2026-07-30T233515Z-i-09fa5115b3282d6ea.log"),
        'echo "NEG_RC=$?"',
        "aws s3api head-object --bucket %s --key code/estate_report_runner.py > /dev/null 2>&1"
        % BUCKET,
        'echo "POS_RC=$?"',
        "echo OS18_PROBE_END",
    ]
    try:
        cid = ssm.send_command(
            InstanceIds=[INSTANCE_ID], DocumentName="AWS-RunShellScript",
            Parameters={"commands": cmds, "executionTimeout": ["120"]},
            Comment="OS-s-18 O18-AC1 seam readability, exercised by the runner role",
        )["Command"]["CommandId"]
    except Exception as e:                                                  # noqa: BLE001
        _skip(arm, "ssm send_command refused: %s: %s" % (type(e).__name__, str(e)[:150]))
        return
    out, status = "", ""
    for _ in range(20):
        time.sleep(3)
        try:
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=INSTANCE_ID)
        except Exception:                                                   # noqa: BLE001
            continue
        status = inv["Status"]
        if status in ("Success", "Failed", "Cancelled", "TimedOut"):
            out = inv.get("StandardOutputContent") or ""
            break
    if status != "Success":
        _skip(arm, "ssm invocation ended %r (command %s); the box self-stops mid-probe when its "
                   "run finishes, which is a NOT-EVALUATED, not a deny" % (status, cid))
        return

    def _val(tag):
        for line in out.splitlines():
            if line.startswith(tag + "="):
                return line.split("=", 1)[1].strip()
        return None

    who = ""
    for line in out.splitlines():
        if "assumed-role/estate-report-runner-role" in line:
            who = line.strip()
    green_rc, neg_rc, pos_rc = _val("GREEN_RC"), _val("NEG_RC"), _val("POS_RC")
    green_bytes = _val("GREEN_BYTES")
    # GRAIN: the principal that made the call must be the runner's role, not the SSM agent's
    # ambient identity or my own. If that line is absent the arm proves nothing about the role.
    ok_who = "assumed-role/estate-report-runner-role" in who
    ok_green = green_rc == "0" and (green_bytes or "0").isdigit() and int(green_bytes) > 0
    ok_neg = neg_rc not in (None, "0")      # the instrument CAN return denied
    ok_pos = pos_rc == "0"                  # ...and is not denying everything
    _record(arm, ok_who and ok_green and ok_neg and ok_pos,
            "principal=%s | GREEN(get %s) rc=%s bytes=%s | NEG-CONTROL(get logs/, Put-granted "
            "Get-NOT-granted) rc=%s | POS-CONTROL(head code/) rc=%s"
            % (who or "UNREAD", SEAM_KEY, green_rc, green_bytes, neg_rc, pos_rc))


def arm_a2_simulated(b3):
    """iam:SimulatePrincipalPolicy against the live role. ONE --resource-arns per call: a batched
    multi-ARN call flips HELD resources to implicitDeny and would silently disarm the very
    controls this arm leans on. The target statement carries `condition: null` (read from the
    APPLIED census), so no --context-entries are needed and a deny here cannot be the
    conditioned-grant false-deny mode."""
    iam = b3.client("iam", region_name=REGION)

    def sim(resource_arn):
        r = iam.simulate_principal_policy(
            PolicySourceArn=ROLE_ARN, ActionNames=["s3:GetObject"], ResourceArns=[resource_arn])
        return r["EvaluationResults"][0]["EvalDecision"]

    target = BUCKET_ARN + "/" + SEAM_KEY
    neg = BUCKET_ARN + "/logs/2026-07-30T233515Z-i-09fa5115b3282d6ea.log"
    pos = BUCKET_ARN + "/code/estate_report_runner.py"
    try:
        d_target = sim(target)                 # three SEPARATE invocations, deliberately
        d_neg = sim(neg)
        d_pos = sim(pos)
    except Exception as e:                                                  # noqa: BLE001
        _record("A2-APPLIED-simulate", False,
                "simulate_principal_policy failed: %s: %s" % (type(e).__name__, str(e)[:200]))
        return
    ok = d_target == "allowed" and d_neg != "allowed" and d_pos == "allowed"
    _record("A2-APPLIED-simulate-with-both-controls", ok,
            "TARGET %s -> %s | NEG-CONTROL logs/<real object, Get NOT granted> -> %s | "
            "POS-CONTROL code/ -> %s (3 separate calls, 1 resource-arn each)"
            % (SEAM_KEY, d_target, d_neg, d_pos))


def arm_a3_desired_plane():
    """DESIRED != APPLIED. The terraform source must name the prefix too, or the applied grant is
    an out-of-band edit that the next apply reverts."""
    try:
        src = TERRAFORM_IAM.read_text(encoding="utf-8", errors="replace")
    except Exception as e:                                                  # noqa: BLE001
        _record("A3-DESIRED-terraform-names-the-prefix", False, "unreadable: %s" % e)
        return
    needle = '${aws_s3_bucket.estate_report.arn}/outset/*'
    hits = src.count(needle)
    # NEGATIVE CONTROL on the reader itself: a token that must NOT be there. Without this, a
    # read that silently returned the whole file for any query would pass this arm.
    absent_hits = src.count('${aws_s3_bucket.estate_report.arn}/outset-not-a-real-prefix/*')
    _record("A3-DESIRED-terraform-names-the-prefix", hits == 1 and absent_hits == 0,
            "iam.tf occurrences of the seam resource = %d (expected 1); reader negative control "
            "(a prefix that must not exist) = %d (expected 0)" % (hits, absent_hits))


# =============================================================================================
# AXIS 2 -- CONTENT. Is what is AT the seam consumable by the CONSUMER half, from S3?
# =============================================================================================

def arm_b1_live_read(runner):
    """The real object, from the real bucket, through the real consumer function."""
    src = "s3://%s/%s" % (BUCKET, SEAM_KEY)
    try:
        r = runner._outset_read(src, runner._outset_loader, _utc_now(),
                                runner.OUTSET_SEAM_MAX_AGE_HOURS)
    except Exception as e:                                                  # noqa: BLE001
        _record("B1-live-seam-read-OK", False, "%s: %s" % (type(e).__name__, str(e)[:200]))
        return None
    ok = (r["status"] == "OK" and not r["absent"] and r["error"] is None
          and r["tool"] and r["denominator"] and "NO DENOMINATOR" not in r["denominator"])
    _record("B1-live-seam-read-OK", ok,
            "status=%s absent=%s tool=%r age=%.2fh rows=%d denominator=%r"
            % (r["status"], r["absent"], r.get("tool"), r.get("age_hours") or -1.0,
               len(r.get("rows") or []), (r.get("denominator") or "")[:120]))
    return r


# =============================================================================================
# AXIS 3 -- THE RED ARMS. A FAILED publish reads FAILED, never as an absent or clean section.
# =============================================================================================

def arm_r1_producer_fails_loudly(producer, tmp):
    """Make the PRODUCER fail. It must publish a FAILED artifact -- never nothing, and never
    something that looks like a clean answer."""
    dest = str(Path(tmp) / "red_producer.json")
    art = producer.run_and_build(
        "comp-heat drift (DELIBERATELY BROKEN)",
        "the red arm: what does a producer that cannot run publish?",
        [sys.executable, str(ROOT / ".tools" / "no_such_tool_os18_red_arm")],
        timeout_s=30.0)
    receipt = producer.publish_artifact(art, dest)
    ok = (art["answer_state"] == "FAILED" and receipt["published"] is True
          and art["error"] and art["denominators"].get("claim") == "absent")
    _record("R1-broken-producer-publishes-FAILED", ok,
            "answer_state=%s published=%s bytes=%d denominators.claim=%s error=%r"
            % (art["answer_state"], receipt["published"], receipt["bytes"],
               art["denominators"].get("claim"), (art.get("error") or "")[:120]))
    return art


def arm_r2_failed_publish_at_the_seam(runner, b3, failed_art):
    """Put that genuinely-FAILED artifact ON THE SEAM and read it back FROM S3. This is the arm
    the cell names: make the publish fail, then show the report says FAILED.

    The key is FIXED and OVERWRITTEN, never deleted (PRD R-5 NEVER-AUTO-DELETE)."""
    body = json.dumps(failed_art, indent=2).encode("utf-8")
    try:
        b3.client("s3", region_name=REGION).put_object(
            Bucket=BUCKET, Key=RED_KEY, Body=body, ContentType="application/json")
    except Exception as e:                                                  # noqa: BLE001
        _record("R2-FAILED-publish-reads-FAILED-at-the-seam", False,
                "could not place the red-arm probe: %s: %s" % (type(e).__name__, str(e)[:150]))
        return None
    src = "s3://%s/%s" % (BUCKET, RED_KEY)
    r = runner._outset_read(src, runner._outset_loader, _utc_now(),
                            runner.OUTSET_SEAM_MAX_AGE_HOURS)
    ok = (r["status"] == "INSTRUMENT_FAILED" and r["absent"] is False
          and r["error"] and "FAILED" in r["error"] and not r["rows"])
    _record("R2-FAILED-publish-reads-FAILED-at-the-seam", ok,
            "s3 key=%s -> status=%s absent=%s rows=%d error=%r"
            % (RED_KEY, r["status"], r["absent"], len(r["rows"]), (r["error"] or "")[:150]))
    return r


def arm_r3_report_says_failed(runner, b3):
    """THE RENDERED REPORT, not the return value. A stratum that fails must render LOUDLY; an
    omitted stratum reads as 'nothing to report', which is the lie the seam exists to stop."""
    prefix = "s3://%s/%s" % (BUCKET, SEAM_PREFIX)

    def loader_to_red(source):
        # Point the propagation stratum's exact key at the red-arm probe without touching the
        # real one. The CONSUMER code path is unchanged; only the bytes it receives differ.
        return runner._outset_loader("s3://%s/%s" % (BUCKET, RED_KEY))

    s = runner._stratum_propagation("os18-red", prefix=prefix, loader=loader_to_red,
                                    now=_utc_now())
    text = runner.render_stratum(s)
    ok = (s["status"] == "INSTRUMENT_FAILED" and s["row_count"] is None
          and s["instrument_error"] and "STATUS:" in text
          and "INSTRUMENT_FAILED" in text and "PRODUCED NO DATA" in text)
    _record("R3-the-RENDERED-report-says-FAILED", ok,
            "status=%s row_count=%r rendered contains STATUS/INSTRUMENT_FAILED/PRODUCED NO "
            "DATA = %s/%s/%s"
            % (s["status"], s["row_count"], "STATUS:" in text,
               "INSTRUMENT_FAILED" in text, "PRODUCED NO DATA" in text))
    return text


def arm_r4_absent_is_not_clean(runner):
    """A key that was NEVER published. It must read FAILED-and-ABSENT, and `absent` must be a
    FIELD -- a caller choosing between sources cannot grep error prose (OS-s-14, W2-S18)."""
    src = "s3://%s/%s" % (BUCKET, ABSENT_KEY)

    def loader(source):
        try:
            return runner._outset_loader(source)
        except Exception as e:                                              # noqa: BLE001
            # boto3 raises ClientError(NoSuchKey), not FileNotFoundError. The consumer's ABSENT
            # branch keys on FileNotFoundError, so translate at the LOADER -- which is exactly
            # where a real S3 loader would have to, and the translation is asserted, not assumed.
            if "NoSuchKey" in str(e) or "Not Found" in str(e) or "404" in str(e):
                raise FileNotFoundError(source)
            raise

    r = runner._outset_read(src, loader, _utc_now(), runner.OUTSET_SEAM_MAX_AGE_HOURS)
    ok = (r["status"] == "INSTRUMENT_FAILED" and r["absent"] is True and not r["rows"]
          and "ABSENT" in (r["error"] or ""))
    _record("R4-never-published-reads-FAILED-and-ABSENT", ok,
            "status=%s absent=%s error=%r" % (r["status"], r["absent"], (r["error"] or "")[:150]))
    return r


def arm_r5_stale(runner, tmp, good_art):
    """A stale artifact differs from a fresh one in NO field but its vintage."""
    art = json.loads(json.dumps(good_art))
    art["vintage"]["answer_produced_utc"] = _iso(_utc_now() - _dt.timedelta(hours=999))
    p = Path(tmp) / "stale.json"
    p.write_text(json.dumps(art), encoding="utf-8")
    r = runner._outset_read(str(p), runner._outset_loader, _utc_now(), 26.0)
    ok = (r["status"] == "INSTRUMENT_FAILED" and r["absent"] is False
          and "STALE" in (r["error"] or "") and not r["rows"])
    _record("R5-stale-reads-FAILED-not-fresh", ok,
            "status=%s absent=%s age=%.1fh error=%r"
            % (r["status"], r["absent"], r.get("age_hours") or -1.0, (r["error"] or "")[:120]))


def arm_r6_future_dated(runner, tmp, good_art):
    """One-sided staleness is a one-sided control: a future-dated artifact can never trip it."""
    art = json.loads(json.dumps(good_art))
    art["vintage"]["answer_produced_utc"] = _iso(_utc_now() + _dt.timedelta(hours=48))
    p = Path(tmp) / "future.json"
    p.write_text(json.dumps(art), encoding="utf-8")
    r = runner._outset_read(str(p), runner._outset_loader, _utc_now(), 26.0)
    ok = r["status"] == "INSTRUMENT_FAILED" and "FUTURE" in (r["error"] or "").upper()
    _record("R6-future-dated-is-REFUSED", ok,
            "status=%s error=%r" % (r["status"], (r["error"] or "")[:130]))


def arm_r7_unmapped_state(runner, tmp, good_art):
    """An answer_state outside the declared domain is REFUSED, never defaulted to OK."""
    art = json.loads(json.dumps(good_art))
    art["answer_state"] = "TOTALLY_FINE_HONEST"
    p = Path(tmp) / "unmapped.json"
    p.write_text(json.dumps(art), encoding="utf-8")
    r = runner._outset_read(str(p), runner._outset_loader, _utc_now(), 1e9)
    ok = r["status"] == "INSTRUMENT_FAILED" and "outside the seam" in (r["error"] or "")
    _record("R7-unmapped-answer_state-is-REFUSED", ok,
            "status=%s error=%r" % (r["status"], (r["error"] or "")[:130]))


def arm_r8_ok_and_failed_are_distinguishable(runner, good_read, failed_read, failed_text):
    """THE W2-S21 ARM. A working seam and a silent one must not be byte-identical to the reader.
    This is the property every one of those 51 green arms assumed and none asserted."""
    if not good_read or not failed_read:
        _skip("R8-OK-and-FAILED-are-distinguishable",
              "needs both B1 and R2 to have produced a reading")
        return
    same_status = good_read["status"] == failed_read["status"]
    good_stratum = runner._stratum("A_propagation", "q", good_read["rows"], good_read["vintage"],
                                   good_read["denominator"], status=good_read["status"],
                                   error=good_read["error"])
    good_text = runner.render_stratum(good_stratum)
    ok = (not same_status and good_text != failed_text
          and "PRODUCED NO DATA" in failed_text and "PRODUCED NO DATA" not in good_text)
    _record("R8-OK-and-FAILED-renderings-are-NOT-byte-identical", ok,
            "statuses %s vs %s | rendered lengths %d vs %d | 'PRODUCED NO DATA' in failed=%s, "
            "in good=%s" % (good_read["status"], failed_read["status"], len(good_text),
                            len(failed_text), "PRODUCED NO DATA" in failed_text,
                            "PRODUCED NO DATA" in good_text))


# =============================================================================================
# ARM M -- THE PLANTED MUTANT. A declared-but-unrun falsifier is a promise, not a control.
# =============================================================================================

def arm_m_mutant(tmp, failed_art):
    """Break the ONE mapping the whole seam rests on -- FAILED -> INSTRUMENT_FAILED -- in a COPY
    of the runner, and prove the red arm REFUSES it. If the mutated consumer still reads FAILED
    correctly, this battery's red arms are decoration."""
    mutant_path = Path(tmp) / "runner_mutant.py"
    src = RUNNER.read_text(encoding="utf-8", errors="replace")
    if src.count(FAILED_ANCHOR) != 1:
        _record("M-planted-mutant-is-REFUSED", False,
                "anchor is not unique in the runner source (count=%d) -- REFUSING to mutate "
                "rather than silently mutating nothing (W2-S17)" % src.count(FAILED_ANCHOR))
        return
    mutant_path.write_text(src.replace(FAILED_ANCHOR, FAILED_MUTANT), encoding="utf-8")
    mod = _load(mutant_path, "runner_os18_mutant", RUNNER_ENV)
    p = Path(tmp) / "mutant_input.json"
    p.write_text(json.dumps(failed_art), encoding="utf-8")
    r = mod._outset_read(str(p), mod._outset_loader, _utc_now(), 1e9)
    # Under the mutant a FAILED publish reads OK. The arm PASSES when it detects that.
    detected = r["status"] == "OK"
    _record("M-planted-mutant-is-REFUSED", detected,
            "mutated FAILED->OK mapping; the consumer then read a FAILED artifact as status=%s "
            "(the arm passes by DETECTING this, which is what makes R2/R3 real)" % r["status"])


def main():
    print("=" * 92)
    print("NFRA_OUTSET.TO-OS-s-18  O18-AC1 -- the publish reaching the seam, readable by the")
    print("runner's own role, and a FAILED publish reading FAILED.  measured %s" % _iso(_utc_now()))
    print("=" * 92)
    try:
        import boto3 as b3
    except Exception as e:                                                  # noqa: BLE001
        print("BLOCKED: boto3 unavailable (%s). Every world-facing arm needs it." % e)
        return 2

    producer = _load(PRODUCER, "outset_seam_os18", None)
    runner = _load(RUNNER, "estate_report_runner_os18", RUNNER_ENV)
    tmp = tempfile.mkdtemp(prefix="os18_")
    try:
        arm_a3_desired_plane()
        arm_a2_simulated(b3)
        arm_a1_exercised(b3)
        good = arm_b1_live_read(runner)
        failed_art = arm_r1_producer_fails_loudly(producer, tmp)
        failed = arm_r2_failed_publish_at_the_seam(runner, b3, failed_art)
        failed_text = arm_r3_report_says_failed(runner, b3)
        arm_r4_absent_is_not_clean(runner)
        if good is not None:
            raw = json.loads(runner._outset_loader("s3://%s/%s" % (BUCKET, SEAM_KEY)))
            arm_r5_stale(runner, tmp, raw)
            arm_r6_future_dated(runner, tmp, raw)
            arm_r7_unmapped_state(runner, tmp, raw)
        else:
            for a in ("R5-stale-reads-FAILED-not-fresh", "R6-future-dated-is-REFUSED",
                      "R7-unmapped-answer_state-is-REFUSED"):
                _skip(a, "needs the live seam artifact B1 could not read")
        arm_r8_ok_and_failed_are_distinguishable(runner, good, failed, failed_text or "")
        arm_m_mutant(tmp, failed_art)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print("")
    passed = sum(1 for _, ok, _ in RESULTS if ok)
    total = len(RESULTS)
    for arm, ok, detail in RESULTS:
        print("  [%s] %-52s %s" % ("PASS" if ok else "FAIL", arm, detail))
    for arm, reason in NOT_EVALUATED:
        print("  [NOT-EVALUATED] %-42s %s" % (arm, reason))
    print("")
    print("  DENOMINATOR: %d of %d evaluated arm(s) PASSED; %d arm(s) NOT-EVALUATED "
          "(never counted as passes)." % (passed, total, len(NOT_EVALUATED)))
    print("  RED ARMS in the evaluated set: %d (R1,R2,R3,R4,R5,R6,R7,R8,M as reached)."
          % sum(1 for a, _, _ in RESULTS if a[0] in ("R", "M")))
    print("")
    if passed == total and total > 0:
        print("OS18-SEAM-READABLE")
        return 0
    print("OS18-SEAM-NOT-READABLE: %d arm(s) failed" % (total - passed))
    return 1


# pytest grain -- one test per recorded arm, from the same single execution.
def test_os18_seam_readable():
    rc = main()
    failures = [(a, d) for a, ok, d in RESULTS if not ok]
    assert not failures, "OS-s-18 seam arms failed: %s" % failures
    assert rc == 0


if __name__ == "__main__":
    raise SystemExit(main())
