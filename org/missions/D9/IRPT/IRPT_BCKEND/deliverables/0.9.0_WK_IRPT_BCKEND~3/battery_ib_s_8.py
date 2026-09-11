"""Battery for IRPT_BCKEND.TO-IB-s-8 -- S8-AC1, the six arms.

Invocation the task order names:
    timeout 600 python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/
        0.9.0_WK_IRPT_BCKEND~3/battery_ib_s_8.py
Prints IBS8-RUNNER-BUILT only when every arm passes.

NO LIVE VENDOR CALL. Arms (a) through (e) run the node suite against a loopback replay
under an outbound-network guard; arm (f) reads the AWS control plane (describe-secret,
describe-instances) and the git record. Nothing here touches ycharts.com, and arm (e)
carries a POSITIVE CONTROL proving the guard can fire -- a guard that cannot go non-zero
is a constant wearing a measurement's clothes.

NO SECRET VALUE IS READ OR PRINTED. describe-secret returns version STAGES only.

Author: 0.9.0_WK_IRPT_BCKEND~3. Cell IB-s-8.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys

REPO = subprocess.run(
    ["git", "rev-parse", "--show-toplevel"],
    capture_output=True, text=True, check=True,
).stdout.strip()

RUNNER_DIR = os.path.join(REPO, "infra", "aws", "ec2", "investor-reporting-ycharts")
LIBRARY = os.path.join(RUNNER_DIR, "ycharts_session.js")
SUITE = os.path.join("tests", "run_offline_suite.js")
GUARD = os.path.join(".", "tests", "netguard.js")
AWS = os.path.join(REPO, ".tools", "aws.cmd")

SECRET_NAMES = [
    "ycharts/login/credentials",
    "ycharts/session/current",
    "astn/kimi/api-key",
]
INSTANCE_ID = "i-0167fd745ad906a66"
LEDGER_SLUG = "irpt-bckend-s8"
SENTINEL = os.path.join(REPO, "org", "critical_paths", ".open_deploys",
                        LEDGER_SLUG + ".json")

# The token census regex -- the same one comp-read --enumerate was pointed at, so the two
# instruments are answering the same question over the same file.
OTP_TOKENS = re.compile(
    r"(?i)one[- ]?time|otp|verification code|2fa|two[- ]factor")

results: dict[str, bool] = {}
lines_out: list[str] = []


def say(text: str = "") -> None:
    lines_out.append(text)
    print(text)


def run(cmd: list[str], cwd: str | None = None, timeout: int = 240) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                          timeout=timeout, shell=False)


def aws_json(args: list[str]):
    proc = run([AWS] + args + ["--region", "us-east-1", "--output", "json"], timeout=120)
    if proc.returncode != 0:
        return {"_error": proc.stderr.strip()[:200], "_rc": proc.returncode}
    text = proc.stdout.replace("\r", "").strip()
    return json.loads(text) if text else None


# ---------------------------------------------------------------------------
# Arms (a)-(e): the offline suite, run the way the estate runs it.
# ---------------------------------------------------------------------------

def offline_suite() -> dict:
    guard_log = os.path.join(REPO, ".scratch", "netguard_battery.json")
    os.makedirs(os.path.dirname(guard_log), exist_ok=True)
    env = dict(os.environ)
    env["YC_NETGUARD_LOG"] = guard_log
    proc = subprocess.run(
        ["node", "--require", GUARD, SUITE],
        cwd=RUNNER_DIR, capture_output=True, text=True, timeout=300,
        shell=False, env=env,
    )
    out = proc.stdout
    if "RESULT-BEGIN" not in out:
        return {"_suite_failed": True, "rc": proc.returncode,
                "stdout_tail": out[-1500:], "stderr_tail": proc.stderr[-1500:]}
    blob = out.split("RESULT-BEGIN", 1)[1].split("RESULT-END", 1)[0]
    data = json.loads(blob)
    data["_rc"] = proc.returncode
    return data


# ---------------------------------------------------------------------------
# Arm (b), SECOND instrument: a source census over the library, banded.
# The structural census inside the library counts HANDLER ROWS; this one counts
# every TEXT occurrence of a one-time-code token in the file and bands each hit,
# so a code path hiding behind an innocuous comment count cannot pass unseen.
# ---------------------------------------------------------------------------

def declared_table_ranges(lines: list[str]) -> list[tuple[int, int, str]]:
    """Line ranges of the two DECLARATIVE tables, found in the source, not assumed.

    A one-time-code token inside `CHALLENGE_HANDLERS` or
    `UNEXPECTED_CHALLENGE_SIGNATURES` is already accounted for by the structural
    census -- the first is the handler row that says handles_one_time_code: false,
    the second is a DETECTOR that routes to an explicit refusal. Banding them as
    their own regions is a structural fact read out of the file, and it leaves the
    CODE band meaning exactly one thing: an executable one-time-code path outside
    both declarations. That is the thing arm (b) has to be able to see.
    """
    ranges = []
    for name in ("CHALLENGE_HANDLERS", "UNEXPECTED_CHALLENGE_SIGNATURES"):
        start = None
        for index, raw in enumerate(lines, start=1):
            if start is None and raw.startswith("const " + name + " = ["):
                start = index
            elif start is not None and raw.startswith("];"):
                ranges.append((start, index, name))
                break
    return ranges


def source_otp_census() -> dict:
    with open(LIBRARY, encoding="utf-8") as handle:
        src = handle.read()
    lines = src.splitlines()
    table_ranges = declared_table_ranges(lines)
    bands = {"BLOCK-COMMENT": 0, "LINE-COMMENT": 0, "HANDLER-TABLE": 0,
             "SIGNATURE-TABLE": 0, "RECORD-FIELD": 0, "CODE": 0}
    hits = []
    in_block = False
    for number, raw in enumerate(lines, start=1):
        stripped = raw.strip()
        opened = stripped.startswith("/*")
        if opened:
            in_block = True
        is_comment_line = in_block or stripped.startswith("//") or stripped.startswith("*")
        table = next((name for lo, hi, name in table_ranges if lo <= number <= hi), None)
        if "*/" in stripped:
            in_block = False
        for _ in OTP_TOKENS.finditer(raw):
            if is_comment_line:
                block = in_block or opened or stripped.startswith("*")
                band = "BLOCK-COMMENT" if block else "LINE-COMMENT"
            elif table == "CHALLENGE_HANDLERS":
                band = "HANDLER-TABLE"
            elif table == "UNEXPECTED_CHALLENGE_SIGNATURES":
                band = "SIGNATURE-TABLE"
            elif "otp_branch" in raw:
                band = "RECORD-FIELD"
            else:
                band = "CODE"
            bands[band] += 1
            hits.append({"line": number, "band": band, "text": stripped[:110]})
    return {"file_lines": len(lines), "hits": len(hits), "bands": bands, "rows": hits,
            "table_ranges": [{"name": n, "from": lo, "to": hi} for lo, hi, n in table_ranges]}


# ---------------------------------------------------------------------------
# Arm (f): secrets by name, host stopped, ledger closed.
# ---------------------------------------------------------------------------

def arm_f() -> dict:
    secrets = {}
    for name in SECRET_NAMES:
        stages = aws_json(["secretsmanager", "describe-secret", "--secret-id", name,
                           "--query", "VersionIdsToStages"])
        if isinstance(stages, dict) and "_error" in stages:
            secrets[name] = {"error": stages["_error"]}
            continue
        if stages is None:
            secrets[name] = {"versions": 0, "stages": [], "state": "NO_AWSCURRENT_VERSION"}
        else:
            flat = sorted({stage for v in stages.values() for stage in v})
            secrets[name] = {"versions": len(stages), "stages": flat,
                             "state": "AWSCURRENT" if "AWSCURRENT" in flat else "NO_AWSCURRENT"}

    inst = aws_json(["ec2", "describe-instances", "--instance-ids", INSTANCE_ID,
                     "--query", "Reservations[0].Instances[0].State.Name"])

    entry_dir = os.path.join(REPO, "org", "critical_paths", "change_management")
    entry_name = next((f for f in sorted(os.listdir(entry_dir)) if LEDGER_SLUG in f), None)
    entry_text = ""
    if entry_name:
        with open(os.path.join(entry_dir, entry_name), encoding="utf-8") as handle:
            entry_text = handle.read()
    closed = bool(re.search(r"(?i)\bstatus\b.{0,40}\bCLOSED\b", entry_text))
    open_legs = len(re.findall(r"(?i)\bOPEN\b\s*\|", entry_text))

    log = run(["git", "log", "--format=%h %s", "-n", "6", "--",
               "org/critical_paths/.open_deploys/" + LEDGER_SLUG + ".json",
               "org/critical_paths/change_management/" + (entry_name or "")],
              cwd=REPO, timeout=90).stdout.strip().split("\n")
    return {"secrets": secrets, "instance_state": inst, "entry_file": entry_name,
            "entry_closed": closed, "open_leg_markers": open_legs,
            "sentinel_present": os.path.exists(SENTINEL),
            "sentinel_commits": [ln for ln in log if ln]}


# ---------------------------------------------------------------------------

def main() -> int:
    say("=" * 78)
    say("BATTERY IB-s-8 -- S8-AC1: the YCharts session library, the secrets, the host")
    say("repo: " + REPO)
    say("=" * 78)

    suite = offline_suite()
    if suite.get("_suite_failed"):
        say("BLOCKED: the offline suite produced no result block (rc=%s)" % suite.get("rc"))
        say(suite.get("stderr_tail", ""))
        return 1

    arms = suite["arms"]

    # ---- (a) -------------------------------------------------------------
    arm_a = arms["a_five_surfaces"]
    say("")
    say("(a) THE FIVE SURFACES AGAINST THE REPLAY -- " + arm_a["line"])
    say("    precondition getSession on the MEASURED absent secret: present=%s reason=%s"
        % (arm_a["precondition_no_awscurrent"]["present"],
           arm_a["precondition_no_awscurrent"]["reason"]))
    for key, surface in arm_a["surfaces"].items():
        say("    %-28s %-5s  %s" % (key, "PASS" if surface["result"]["pass"] else "FAIL",
                                    surface["result"]["detail"]))
    stale = arm_a["surfaces"]["probeSession_stale"]
    say("      probeSession(stale): authenticated=%s reason=%s http=%s"
        " legs identity=%s cookie=%s probe=%s"
        % (stale["authenticated"], stale["reason"], stale["http_status"],
           stale["identity_leg"], stale["cookie_leg"], stale["probe_leg"]))
    acq = arm_a["surfaces"]["acquireSession"]
    say("      acquireSession: steps=%s" % json.dumps(acq["steps"]))
    say("      identity evidence (REDACTED -- names + sha256 prefix, never a value): %s"
        % json.dumps(acq["identity_evidence"]))
    say("      probe evidence: %s" % json.dumps(acq["probe_evidence"]))
    per = arm_a["surfaces"]["persistSession"]
    say("      persistSession: secret_id=%s fence=%s previous_fence=%s puts=%s"
        % (per["secret_id"], per["fence"], per["previous_fence"], per["puts_recorded"]))
    got = arm_a["surfaces"]["getSession"]
    say("      getSession: present=%s cookies=%s fence=%s"
        % (got["present"], got["cookie_names"], got["fence"]))
    wap = arm_a["surfaces"]["withAuthenticatedPage"]
    say("      withAuthenticatedPage: %s" % json.dumps(wap["callback_result"]))
    results["a"] = arm_a["passed"] == arm_a["denominator"]

    # ---- (b) -------------------------------------------------------------
    arm_b = arms["b_no_otp_branch"]
    census = source_otp_census()
    say("")
    say("(b) NO OTP BRANCH")
    say("    structural census (handler rows): " + arm_b["structural_line"])
    for handler in arm_b["structural_census"]["handlers"]:
        say("      %-22s action=%-14s handles_one_time_code=%s"
            % (handler["id"], handler["action"], handler["handles_one_time_code"]))
    say("    injected challenges: " + arm_b["injected_line"])
    for variant, row in arm_b["injected"].items():
        say("      %-14s class=%-22s reason=%-38s retried=%s submits=%s"
            % (variant, row["failure_class"], row["reason"], row["retried"],
               row["credential_submits_during_attempt"]))
    say("    source token census over ycharts_session.js (SECOND instrument,"
        " different from the handler-row count):")
    say("      denominator: %d hit(s) across %d line(s); bands: %s"
        % (census["hits"], census["file_lines"], json.dumps(census["bands"])))
    say("      declarative tables located in the source: %s"
        % json.dumps(census["table_ranges"]))
    for row in census["rows"]:
        say("        %4d  %-17s %s" % (row["line"], row["band"], row["text"]))
    say("      CODE-band hits (a real one-time-code code path would land here): %d"
        % census["bands"]["CODE"])
    results["b"] = bool(arm_b["pass"]) and census["bands"]["CODE"] == 0

    # ---- (c) -------------------------------------------------------------
    arm_c = arms["c_bounded_eviction"]
    say("")
    say("(c) EVICTION IS BOUNDED -- N declared = %d" % arm_c["n_declared"])
    say("    " + arm_c["line"])
    say("    control  (no eviction injected): reacquisitions_used=%s work_status=%s"
        % (arm_c["control"]["reacquisitions_used"], arm_c["control"]["work_status"]))
    say("    injected (eviction on the work route every time): class=%s"
        " reacquisitions_used=%s allowed=%s terminal=%s evictions_served=%s"
        % (arm_c["injected"]["failure_class"], arm_c["injected"]["reacquisitions_used"],
           arm_c["injected"]["reacquisitions_allowed"], arm_c["injected"]["terminal"],
           arm_c["injected"]["evictions_served_by_replay"]))
    results["c"] = bool(arm_c["pass"])

    # ---- (d) -------------------------------------------------------------
    arm_d = arms["d_lease_and_fencing"]
    say("")
    say("(d) LEASE AND FENCING")
    say("    " + arm_d["concurrent_acquire"]["line"])
    say("      runner_1: %s" % json.dumps(arm_d["concurrent_acquire"]["runner_1"]))
    say("      runner_2: %s" % json.dumps(arm_d["concurrent_acquire"]["runner_2"]))
    say("    fenced-out runner refuses to persist without a lease: class=%s"
        % arm_d["fenced_runner_refuses_without_lease"]["failure_class"])
    say("    " + arm_d["stale_fence_persist_refused"]["line"])
    say("      class=%s my_fence=%s stored_fence=%s"
        % (arm_d["stale_fence_persist_refused"]["failure_class"],
           arm_d["stale_fence_persist_refused"]["my_fence"],
           arm_d["stale_fence_persist_refused"]["stored_fence"]))
    results["d"] = bool(arm_d["pass"])

    # ---- (e) -------------------------------------------------------------
    arm_e = arms["e_offline"]
    say("")
    say("(e) NOTHING LEFT THE MACHINE")
    say("    " + arm_e["line"])
    say("    replay request log (every request the library made), denominator %d:"
        % arm_e["replay_requests_logged"])
    for route, count in arm_e["replay_request_routes"]:
        say("      %-34s %d" % (route, count))
    say("    adapter request hosts: %s | non-loopback hosts: %s"
        % (json.dumps(arm_e["adapter_request_hosts"]), arm_e["non_loopback_hosts"]))
    control = arm_e["positive_control"]
    say("    POSITIVE CONTROL -- the guard must be able to fire, or its zero is a constant:")
    say("      attempted %s -> refused=%s reached_vendor=%s guard_external %s -> %s"
        % (control["attempted"], control["refused"], control["reached_vendor"],
           control["guard_external_before"], control["guard_external_after"]))
    say("      refusal: %s" % control["refusal_message"])
    results["e"] = bool(arm_e["pass"])

    # ---- (f) -------------------------------------------------------------
    far = arm_f()
    say("")
    say("(f) SECRETS BY NAME, HOST STOPPED, LEDGER CLOSED")
    say("    describe-secret (version STAGES only -- no value is read or printed),"
        " denominator %d of %d names:" % (len(far["secrets"]), len(SECRET_NAMES)))
    for name in SECRET_NAMES:
        say("      %-28s %s" % (name, json.dumps(far["secrets"][name])))
    say("    describe-instances %s -> State.Name = %s (declared stopped by"
        " aws_ec2_instance_state.runner)" % (INSTANCE_ID, far["instance_state"]))
    say("    ledger entry: %s" % far["entry_file"])
    say("      CLOSED=%s  open-leg markers remaining=%d  sentinel present on disk=%s"
        % (far["entry_closed"], far["open_leg_markers"], far["sentinel_present"]))
    say("      sentinel/entry commits (newest first):")
    for line in far["sentinel_commits"]:
        say("        " + line)
    secrets_ok = all("error" not in far["secrets"][n] for n in SECRET_NAMES)
    results["f"] = (secrets_ok and far["instance_state"] == "stopped"
                    and far["entry_closed"] and far["open_leg_markers"] == 0
                    and not far["sentinel_present"])

    # ---- verdict ---------------------------------------------------------
    say("")
    say("=" * 78)
    order = ["a", "b", "c", "d", "e", "f"]
    for key in order:
        say("  arm (%s): %s" % (key, "PASS" if results[key] else "FAIL"))
    passed = sum(1 for key in order if results[key])
    say("  ARMS: %d of %d" % (passed, len(order)))
    say("=" * 78)
    if passed == len(order):
        say("IBS8-RUNNER-BUILT")
        return 0
    say("BLOCKED: not every arm passed -- IBS8-RUNNER-BUILT withheld")
    return 1


if __name__ == "__main__":
    sys.exit(main())
