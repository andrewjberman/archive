"""Battery for IRPT_BCKEND.TO-IB-s-6 -- S6-AC1, the seven arms.

Invocation the task order names:
    timeout 600 python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/
        0.9.0_WK_IRPT_BCKEND~3/battery_ib_s_6.py
Prints IBS6-INTAKE-DURABLE only when every arm passes.

NO LIVE MAILBOX READ, NO LIVE VENDOR CALL. Arms (a)-(e) and the offline half of (g) run in
a SUBPROCESS under an outbound-network guard that refuses every non-loopback destination;
arm (f) reads the committed inspection record; the rest of (g) reads the AWS control plane
and the git record FROM THE PARENT, where those reads belong. A guard with an allow-list
for "our own AWS calls" would have a hole shaped exactly like the thing it guards.

NO SECRET VALUE IS READ OR PRINTED.

Author: 0.9.0_WK_IRPT_BCKEND~3. Cell IB-s-6.
"""
from __future__ import annotations

import base64
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import zipfile

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True, check=True).stdout.strip()

INTAKE = os.path.join(REPO, "infra", "aws", "lambda", "investor-reporting", "intake")
SUITE = os.path.join(INTAKE, "tests", "run_offline_suite.py")
RECORD = os.path.join(INTAKE, "ib_s_6_graph_inspection.md")
AWS = os.path.join(REPO, ".tools", "aws.cmd")

FUNCTION = "irpt-intake-poller"
SCHEDULE = "irpt-intake-poll"
LEDGER_SLUG = "irpt-bckend-s6"
SENTINEL = os.path.join(REPO, "org", "critical_paths", ".open_deploys", LEDGER_SLUG + ".json")

# The zip members, read from the source map -- the registration IS the member list, so the
# battery rebuilds exactly what was registered rather than a list typed twice.
SOURCE_MAP = os.path.join(REPO, "infra", "aws", "lambda", "ci", "lambda-source-map.json")

results = {}


def say(text=""):
    print(text)


def run(cmd, cwd=None, timeout=300, env=None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                          timeout=timeout, shell=False, env=env)


def aws_json(args):
    proc = run([AWS] + args + ["--region", "us-east-1", "--output", "json"], timeout=150)
    if proc.returncode != 0:
        return {"_error": proc.stderr.strip()[:200]}
    text = proc.stdout.replace("\r", "").strip()
    return json.loads(text) if text else None


def offline_suite():
    proc = run([sys.executable, SUITE], cwd=REPO, timeout=400)
    if "RESULT-BEGIN" not in proc.stdout:
        return {"_suite_failed": True, "rc": proc.returncode,
                "stderr_tail": proc.stderr[-2000:], "stdout_tail": proc.stdout[-1000:]}
    blob = proc.stdout.split("RESULT-BEGIN", 1)[1].split("RESULT-END", 1)[0]
    data = json.loads(blob)
    data["_rc"] = proc.returncode
    return data


def rebuild_zip_hash():
    """Rebuild the registered zip from the WORKTREE source and return its base64 sha256.

    Deterministic by construction (fixed member order, fixed timestamp, fixed mode), so a
    match against the deployed CodeSha256 says the served bytes are these bytes -- not that
    a file with the same name was uploaded at some point.
    """
    sm = json.load(io.open(SOURCE_MAP, encoding="utf-8"))
    entry = sm["functions"][FUNCTION]
    members = []
    for rel in entry["files"]:
        if rel in ("gate.py", "keys.py"):
            sib = "_gate" if rel == "gate.py" else "_keys"
            path = os.path.join(REPO, "infra", "aws", "lambda", "investor-reporting", sib, rel)
        elif rel == "firm_destination_policy.json":
            path = os.path.join(REPO, "infra", "aws", "terraform", "investor-reporting",
                                "core", rel)
        elif rel == "firm_registry.json":
            path = os.path.join(REPO, "data", rel)
        else:
            path = os.path.join(INTAKE, rel.replace("/", os.sep))
        members.append((rel, path))
    members.sort(key=lambda t: t[0])
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for arc, path in members:
            info = zipfile.ZipInfo(arc, date_time=(2026, 9, 11, 0, 0, 0))
            info.external_attr = 0o644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            with open(path, "rb") as fh:
                z.writestr(info, fh.read())
    data = buf.getvalue()
    return (base64.b64encode(hashlib.sha256(data).digest()).decode("ascii"),
            len(data), len(members), entry.get("artifact_sha256"))


def inspection_record():
    """Arm (f): the gateway inspection, PRINTED FROM THE RECORD, not restated from memory."""
    with io.open(RECORD, encoding="utf-8") as fh:
        text = fh.read()
    verdict = re.search(r"\*\*The effective `Mail\.Read` grant for the intake is `([A-Z]+)`",
                        text)
    model = "DELEGATED" if "DELEGATED" in text else None
    artifacts = len(re.findall(r"^\| \d+ \|", text, re.M))
    return {
        "record_path": os.path.relpath(RECORD, REPO).replace("\\", "/"),
        "record_bytes": len(text.encode("utf-8")),
        "permission_model_found": model,
        "one_mailbox_grant": verdict.group(1) if verdict else None,
        "artifacts_read_denominator": artifacts,
        "verdict_line": next((ln.strip() for ln in text.split("\n")
                              if ln.startswith("**The effective")), None),
        "application_access_policy_present": ("No `ApplicationAccessPolicy` is declared"
                                              in text),
    }


def ledger_state():
    entry_dir = os.path.join(REPO, "org", "critical_paths", "change_management")
    name = next((f for f in sorted(os.listdir(entry_dir)) if LEDGER_SLUG in f), None)
    text = ""
    if name:
        with io.open(os.path.join(entry_dir, name), encoding="utf-8") as fh:
            text = fh.read()
    log = run(["git", "log", "--format=%h %s", "-n", "3", "--",
               "org/critical_paths/change_management/" + (name or "")], cwd=REPO).stdout
    sentinel_log = run(["git", "log", "--format=%h", "-n", "3", "--",
                        "org/critical_paths/.open_deploys/" + LEDGER_SLUG + ".json"],
                       cwd=REPO).stdout.strip()
    return {
        "entry_file": name,
        "closed": bool(re.search(r"(?i)\bstatus\b.{0,40}\bCLOSED\b", text)),
        "open_leg_markers": len(re.findall(r"(?i)\bOPEN\b\s*\|", text)),
        "legs_declared": len(re.findall(r"(?m)^\|\s*L\d+\s*\|", text)),
        "sentinel_present_on_disk": os.path.exists(SENTINEL),
        "entry_commits": [ln for ln in log.strip().split("\n") if ln],
        "sentinel_ever_committed": bool(sentinel_log),
        "sentinel_disclosure": (
            "The sentinel was never committed in its OPEN state: the source commit landed "
            "before the entry was opened and the entry opened and closed inside one turn. "
            "The open window is in the entry's own header and its proven legs, not in git. "
            "Filed as channel row IRPT_BCKEND-W3-S4 rather than left as an absence."),
    }


def main():
    say("=" * 78)
    say("BATTERY IB-s-6 -- S6-AC1: durability, idempotency, the gate, the scheduler disabled")
    say("repo: " + REPO)
    say("=" * 78)

    suite = offline_suite()
    if suite.get("_suite_failed"):
        say("BLOCKED: the offline suite produced no result block (rc=%s)" % suite.get("rc"))
        say(suite.get("stderr_tail", ""))
        return 1
    arms = suite["arms"]

    # ---- (a) -------------------------------------------------------------
    a = arms["a_persist_before_checkpoint"]
    kb, ka, ctl = a["kill_before_mark"], a["kill_after_mark"], a["control_kill_after_checkpoint"]
    say("")
    say("(a) PERSIST BEFORE CHECKPOINT -- THE DIFFERENCE CONTROL")
    say("    RUN 1, kill AFTER the attachment+receipt and BEFORE the completion mark (%s)"
        % kb["killed_at"])
    say("      checkpoint after the kill: %s   message claimed: %s"
        % (kb["checkpoint_after_kill"], kb["message_claimed_after_kill"]))
    say("      killed message %s: distinct objects %d -> %d, DUPLICATES %d; put calls %d -> %d"
        % (kb["killed_request_id"], kb["distinct_keys_for_killed_message_after_kill"],
           kb["distinct_keys_for_killed_message_after_restart"],
           kb["duplicate_objects_for_killed_message"],
           kb["put_calls_for_killed_message_after_kill"],
           kb["put_calls_for_killed_message_after_restart"]))
    say("      on restart: %d message(s) re-read, checkpoint then advanced=%s to %s"
        % (kb["restart_re_read_messages"], kb["checkpoint_advanced_on_restart"],
           kb["checkpoint_after_restart"]))
    say("    RUN 2, kill AFTER the mark and BEFORE the checkpoint")
    say("      checkpoint after the kill: %s" % ka["checkpoint_after_kill"])
    say("      killed message on restart: outcome=%s, NEW writes=%d, requests_created=%d,"
        " already_complete=%d, checkpoint advanced=%s"
        % (ka["first_message_outcome_on_restart"],
           ka["new_writes_for_killed_message_on_restart"],
           ka["requests_created_on_restart"], ka["already_complete_on_restart"],
           ka["checkpoint_advanced_on_restart"]))
    say("    CONTROL, kill AFTER the checkpoint advanced -- NO RE-READ")
    say("      scan 1: %d message(s), checkpoint -> %s"
        % (ctl["first_scan_messages"], ctl["first_scan_checkpoint"]))
    say("      scan 2: %d message(s) re-read, %d put call(s) added, checkpoint -> %s"
        % (ctl["second_scan_messages_re_read"], ctl["put_calls_added_by_second_scan"],
           ctl["second_scan_checkpoint"]))
    results["a"] = bool(a["pass"])

    # ---- (b) -------------------------------------------------------------
    b = arms["b_delta_pagination_resync_retry"]
    say("")
    say("(b) DELTA, PAGINATION, RESYNC, RETRY-AFTER -- " + b["line"])
    pg = b["legs"]["pagination"]
    say("    pagination: %d page(s), %d message(s), order matches the fixture chain: %s"
        % (pg["pages"], pg["messages"], pg["order_matches_fixture_order"]))
    say("      ids in order: %s" % pg["ids_in_order"])
    dl = b["legs"]["delta_link_persists"]
    say("    deltaLink persists: %s" % dl["stored"])
    rs = b["legs"]["delta_expiry_resync"]
    say("    delta expiry -> resync: resyncs=%d, messages after resync=%d, resynced=%s"
        % (rs["resyncs"], rs["messages_after_resync"], rs["resynced_flag"]))
    say("      declared: %s" % rs["declared_behaviour"])
    ra = b["legs"]["retry_after"]
    say("    Retry-After honoured: waits=%s seconds (injected clock recorded %s);"
        " ceiling %ds, max %d retries; messages after the wait=%d"
        % (ra["waits_honoured_seconds"], ra["clock_sleeps_recorded"], ra["ceiling_seconds"],
           ra["max_retries"], ra["messages_after_wait"]))
    results["b"] = bool(b["pass"])

    # ---- (c) -------------------------------------------------------------
    c = arms["c_idempotency"]
    say("")
    say("(c) ONE REQUEST PER FORWARD; A NEW REQUEST FOR IDENTICAL HOLDINGS")
    say("    first delivery : %d message(s) -> %d request(s)"
        % (c["first_delivery"]["messages"], c["first_delivery"]["requests_created"]))
    say("    SAME messages delivered again: %d message(s) -> %d NEW request(s),"
        " %d already-complete"
        % (c["second_delivery_same_messages"]["messages"],
           c["second_delivery_same_messages"]["requests_created"],
           c["second_delivery_same_messages"]["already_complete"]))
    say("    distinct requests across both deliveries: %d; queue sends: %d"
        % (c["distinct_requests_total"], c["queue_sends_total"]))
    ih = c["identical_holdings"]
    say("    byte-identical holdings, two different messages: sha256 %s == %s -> %s"
        % (ih["att_0001_sha256"][:16], ih["att_0005_sha256"][:16], ih["bytes_identical"]))
    say("      request ids %s vs %s -> distinct: %s"
        % (ih["request_id_message_1"], ih["request_id_message_5"], ih["distinct_request_ids"]))
    say("    keyed on: %s" % c["keyed_on"])
    results["c"] = bool(c["pass"])

    # ---- (d) -------------------------------------------------------------
    d = arms["d_original_sender"]
    say("")
    say("(d) THE ORIGINAL SENDER, NOT DISPLAY From")
    for label, row in d["cases"].items():
        say("    %s" % label)
        say("      message %s: display From=%s | VERIFIED original=%s (method %s,"
            " display_from_used=%s)"
            % (row["message_id"], row["display_from"], row["verified_original_sender"],
               row["verification_method"], row["display_from_used"]))
        say("      gate -> %s firm_id=%s" % (row["gate_outcome"], row["firm_id"]))
        if row["gate_reason"]:
            say("      reason: %s" % row["gate_reason"][:150])
    results["d"] = bool(d["pass"])

    # ---- (e) -------------------------------------------------------------
    e = arms["e_policy_destinations"]
    say("")
    say("(e) LANDS ONLY WHERE THE POLICY SAYS -- " + e["line"])
    say("    enumerated prefixes (read FROM the policy, not typed): %s"
        % e["enumerated_prefixes"])
    say("    keys written %d; inside %d; OUTSIDE %s"
        % (e["keys_written"], e["keys_inside_enumerated_prefixes"], e["keys_outside"]))
    say("    per enumerated prefix: %s" % json.dumps(e["keys_per_enumerated_prefix"]))
    for k in e["sample_keys"]:
        say("      %s" % k)
    say("    NEGATIVE FIXTURE, a cross-firm destination while bound:")
    say("      %s" % str(e["negative_fixture_cross_firm_destination_refused"])[:220])
    results["e"] = bool(e["pass"])

    # ---- (f) -------------------------------------------------------------
    rec = inspection_record()
    say("")
    say("(f) THE INSPECTION IS RECORDED -- printed from %s (%d bytes)"
        % (rec["record_path"], rec["record_bytes"]))
    say("    Graph permission model found in the gateway: %s" % rec["permission_model_found"])
    say("    one-mailbox Mail.Read grant: %s" % rec["one_mailbox_grant"])
    say("    %s" % rec["verdict_line"])
    say("    artifacts read and tabulated: %d" % rec["artifacts_read_denominator"])
    say("    ApplicationAccessPolicy found anywhere in the corpus: %s"
        % ("no" if rec["application_access_policy_present"] else "UNCLEAR"))
    results["f"] = (rec["permission_model_found"] == "DELEGATED"
                    and rec["one_mailbox_grant"] == "UNVERIFIED"
                    and rec["artifacts_read_denominator"] >= 10
                    and rec["application_access_policy_present"])

    # ---- (g) -------------------------------------------------------------
    g = arms["g_offline"]
    guard, control = g["netguard"], g["positive_control"]
    built_hash, built_bytes, built_members, registered = rebuild_zip_hash()
    cfg = aws_json(["lambda", "get-function-configuration", "--function-name", FUNCTION,
                    "--query", "{CodeSha256:CodeSha256,Layers:Layers,Runtime:Runtime}"])
    sched = aws_json(["scheduler", "get-schedule", "--name", SCHEDULE,
                      "--query", "{State:State,Expr:ScheduleExpression,"
                                 "Tz:ScheduleExpressionTimezone}"])
    led = ledger_state()
    served = (cfg or {}).get("CodeSha256")
    say("")
    say("(g) NOTHING LEFT THE MACHINE; THE SCHEDULER IS DISABLED; THE LEDGER CLOSED")
    say("    netguard (offline subprocess): %d external of %d connection attempt(s);"
        " loopback allowed %d"
        % (guard["external_refused"], guard["attempts_observed"], guard["loopback_allowed"]))
    say("      %s" % guard.get("zero_denominator_note", ""))
    say("    POSITIVE CONTROL -- the guard must be able to fire, or its zero is a constant:")
    say("      attempted %s -> refused=%s, guard external %s -> %s"
        % (control["attempted"], control["refused"], control["guard_external_before"],
           control["guard_external_after"]))
    say("      %s" % control["message"])
    say("    served bytes: CodeSha256 %s" % served)
    say("      rebuilt zip %s (%d bytes, %d members); source-map registration %s"
        % (built_hash, built_bytes, built_members, registered))
    say("      served == rebuilt: %s | registered == rebuilt: %s"
        % (served == built_hash, registered == built_hash))
    say("      Layers: %s (no layer -- jsonschema is absent from the runtime and a layer is"
        " a second moving artifact this cell does not own)" % (cfg or {}).get("Layers"))
    say("    scheduler get-schedule --name %s -> State: %s  (%s %s)"
        % (SCHEDULE, (sched or {}).get("State"), (sched or {}).get("Expr"),
           (sched or {}).get("Tz")))
    say("    ledger %s: CLOSED=%s, legs declared=%d, open-leg markers=%d,"
        " sentinel on disk=%s"
        % (led["entry_file"], led["closed"], led["legs_declared"], led["open_leg_markers"],
           led["sentinel_present_on_disk"]))
    for line in led["entry_commits"]:
        say("      %s" % line)
    say("      DISCLOSED: sentinel ever committed = %s. %s"
        % (led["sentinel_ever_committed"], led["sentinel_disclosure"]))
    results["g"] = (bool(g["pass"])
                    and served == built_hash and registered == built_hash
                    and (sched or {}).get("State") == "DISABLED"
                    and led["closed"] and led["open_leg_markers"] == 0
                    and not led["sentinel_present_on_disk"]
                    and bool(led["entry_commits"]))

    # ---- verdict ---------------------------------------------------------
    say("")
    say("=" * 78)
    order = ["a", "b", "c", "d", "e", "f", "g"]
    for key in order:
        say("  arm (%s): %s" % (key, "PASS" if results[key] else "FAIL"))
    passed = sum(1 for key in order if results[key])
    say("  ARMS: %d of %d" % (passed, len(order)))
    say("=" * 78)
    if passed == len(order):
        say("IBS6-INTAKE-DURABLE")
        return 0
    say("BLOCKED: not every arm passed -- IBS6-INTAKE-DURABLE withheld")
    return 1


if __name__ == "__main__":
    sys.exit(main())
