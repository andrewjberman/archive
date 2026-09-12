#!/usr/bin/env python3
"""BATTERY IB-rt-6 -- THE REFRESH BUILDS BEHIND THE ENABLED SCHEDULE.

Grades RT6-AC1's five arms against THE REAL WORLD: the deployed function, the served IAM
document, the objects in the three firm buckets, the SSM command records the deployed function
itself created, and the real `refresh.py` module imported from the repo. Nothing here wraps,
patches or re-registers the subject (bound 12): every arm's subject is the artifact the estate
serves, and every count prints its denominator.

THE TOKEN IS GATED. `IBRT6...` (assembled below, never written whole in this file so a grep of
the source cannot be mistaken for a result) is printed ONLY if every arm PASSES. The acceptance
`<expect>` is a REGEX, so a line saying "token NOT ASSERTED" would MATCH it and turn a failure
into a pass -- the token therefore never appears in this battery's output except as the pass.

WHAT THIS BATTERY WILL NOT DO. It does not start or stop the runner host, it does not dispatch a
build, it writes nothing to any firm bucket and it applies no terraform. It READS. The acts it
grades were performed under change-management entries and are named by their command ids and
version ids, so a reader can re-derive every one of them.

ASCII only. Bounded: every AWS call runs under a subprocess timeout.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *([os.pardir] * 7)))
AWS = os.path.join(REPO, ".tools", "aws.cmd")
DIRECTORY = os.path.join(REPO, "infra", "aws", "lambda", "investor-reporting", "directory")

FUNCTION = "irpt-directory-refresh"
ROLE = "irpt-directory-refresh-role"
SCHEDULE = "irpt-directory-refresh"
RUNNER = "i-02448edb624a7a7cf"
FIRM_BUCKETS = {"49financial": "opal-data-bd",
                "inflection": "opal-data-inf",
                "cottonwood": "opal-data-cot"}
DIRECTORY_PREFIX = "investor-reporting/directory"
DRIVEN_DATE = "2026-09-11"

# The SSM commands the DEPLOYED function dispatched, by the fire that sent them. These are
# ARTIFACT IDS, not claims: each is read back from AWS below and its stdout is the evidence.
IMPORT_FAIL_COMMAND = "940c828f-c176-4a2d-afcc-1693d3d97fe6"   # bundle with 3 members
IMPORT_OK_COMMAND = "a83c5d88-2392-43f2-be55-c9845a0b1384"     # bundle with 4 members

# The ONE authority for the bundle uri is .tools/safe_deploy_core.py; the terraform local is a
# copy across a language boundary that cannot be deleted, so arm (a) CHECKS it rather than
# trusting it.
SPEC_FILE = os.path.join(REPO, ".tools", "safe_deploy_core.py")
TF_FILE = os.path.join(REPO, "infra", "aws", "terraform", "investor-reporting", "directory",
                       "schedule.tf")

RESULTS = []


def record(arm, verdict, line, denominator=""):
    RESULTS.append((arm, verdict, line, denominator))
    print("  [%s] %-9s %s%s" % (arm, verdict, line,
                                ("   denominator: %s" % denominator) if denominator else ""))


def aws(*args, timeout=180):
    try:
        p = subprocess.run([AWS] + list(args), capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return 124, "", "TIMEOUT"
    return p.returncode, (p.stdout or "").replace("\r", ""), (p.stderr or "").replace("\r", "")


def aws_json(*args, **kw):
    rc, out, err = aws(*args, **kw)
    if rc != 0:
        return None, (err or out)[-400:]
    try:
        return json.loads(out), None
    except ValueError as exc:
        return None, "unparseable: %s" % exc


def head(title):
    print("")
    print("=" * 78)
    print(title)
    print("=" * 78)


# ============================================================== ARM (a) -- WIRED
def arm_a():
    head("ARM (a) WIRED -- the deployed function dispatches, and the manifest says so")

    # a.1 -- the deployed BYTES are the committed bytes, re-derived here and not quoted.
    cfg, err = aws_json("lambda", "get-function-configuration", "--function-name", FUNCTION,
                        "--output", "json")
    if cfg is None:
        record("a.1", "FAIL", "get-function-configuration failed: %s" % err)
        return
    served = cfg["CodeSha256"]
    smap = json.load(open(os.path.join(REPO, "infra", "aws", "lambda", "ci",
                                       "lambda-source-map.json"), encoding="utf-8"))
    declared = smap["functions"][FUNCTION]["artifact_sha256"]
    record("a.1", "PASS" if served == declared else "FAIL",
           "served CodeSha256 %s %s source-map artifact_sha256"
           % (served, "==" if served == declared else "!="))

    # a.2 -- the dispatch is CONFIGURED on the served function, both halves.
    env = (cfg.get("Environment") or {}).get("Variables") or {}
    have = [k for k in ("IRPT_DIRECTORY_RUNNER_INSTANCE_ID", "IRPT_DIRECTORY_BUNDLE_URI")
            if env.get(k)]
    record("a.2", "PASS" if len(have) == 2 else "FAIL",
           "dispatch configuration present on the SERVED function: %s" % ", ".join(have),
           "%d of 2" % len(have))

    # a.3 -- the timeout was NOT raised. A raised timeout is the tell that something waits.
    record("a.3", "PASS" if cfg["Timeout"] == 60 else "FAIL",
           "function Timeout %ds (send-and-return: unchanged from round 1)" % cfg["Timeout"])

    # a.4 -- THE DUPLICATED FACT, CHECKED. The bundle uri lives in python (the one authority)
    #        and in terraform (a copy that cannot be deleted across a language boundary).
    spec = open(SPEC_FILE, encoding="utf-8").read()
    tf = open(TF_FILE, encoding="utf-8").read()
    import re
    m = re.search(r'"s3_key":\s*"(code/scripts/assets_gold/investor_reporting/[^"]+)"', spec)
    b = re.search(r'"bucket":\s*"(opal-data-mdpf)"', spec)
    authority = "s3://%s/%s" % (b.group(1), m.group(1)) if (m and b) else None
    in_tf = authority is not None and authority in tf
    in_env = env.get("IRPT_DIRECTORY_BUNDLE_URI") == authority
    record("a.4", "PASS" if (in_tf and in_env) else "FAIL",
           "bundle uri: spec authority == terraform local == SERVED env  (%s)" % authority)

    # a.5 -- NOT_WIRED is gone from the world this function can reach. The census is over the
    #        SERVED manifests, not over the source: a source that could say NOT_WIRED is fine,
    #        a deployed function that DOES say it is not.
    wired, seen = 0, 0
    for firm, bucket in sorted(FIRM_BUCKETS.items()):
        key = "%s/_refresh/%s/manifest.json" % (DIRECTORY_PREFIX, DRIVEN_DATE)
        rc, out, err = aws("s3api", "get-object", "--bucket", bucket, "--key", key,
                           os.path.join(HERE, "_bat_man_%s.json" % firm), "--output", "text")
        if rc != 0:
            print("      %-12s manifest UNREADABLE: %s" % (firm, (err or out)[-120:]))
            continue
        seen += 1
        man = json.load(open(os.path.join(HERE, "_bat_man_%s.json" % firm), encoding="utf-8"))
        delta = man.get("delta") or {}
        cid = delta.get("ssm_command_id")
        disp = delta.get("build_dispatch")
        fail = delta.get("build_dispatch_failure")
        ok = (disp == "SSM" and cid) or (fail is not None)
        wired += 1 if ok else 0
        print("      %-12s reason=%-22s build_dispatch=%s command=%s%s"
              % (firm, man.get("reason_code"), disp, cid,
                 ("  failure=%s/%s" % (fail, delta.get("build_command_status")))
                 if fail else ""))
        os.remove(os.path.join(HERE, "_bat_man_%s.json" % firm))
    record("a.5", "PASS" if (seen == 3 and wired == 3) else "FAIL",
           "SERVED manifests for %s carrying a real SSM dispatch fact" % DRIVEN_DATE,
           "%d of 3 firms (read back: %d)" % (wired, seen))

    # a.6 -- the schedule is ENABLED, read LIVE and from the SCHEDULER plane (not a Rule).
    sch, err = aws_json("scheduler", "get-schedule", "--name", SCHEDULE, "--output", "json")
    if sch is None:
        record("a.6", "FAIL", "get-schedule failed: %s" % err)
    else:
        record("a.6", "PASS" if sch["State"] == "ENABLED" else "FAIL",
               "schedule LIVE state %s %s %s, target %s"
               % (sch["State"], sch["ScheduleExpression"],
                  sch.get("ScheduleExpressionTimezone"),
                  sch["Target"]["Arn"].rsplit(":", 1)[-1]))


# =========================================== ARM (b) -- THREE OF THREE, BEFORE/AFTER
def arm_b():
    head("ARM (b) THREE OF THREE, BEFORE/AFTER -- the production builds")
    built = 0
    for firm, bucket in sorted(FIRM_BUCKETS.items()):
        d, err = aws_json("s3api", "list-objects-v2", "--bucket", bucket,
                          "--prefix", "%s/" % DIRECTORY_PREFIX, "--output", "json")
        keys = [o["Key"] for o in ((d or {}).get("Contents") or [])]
        artifacts = [k for k in keys if k.endswith("/directory.json")]
        pointer = [k for k in keys if k.endswith("/latest.json")]
        built += 1 if (artifacts and pointer) else 0
        print("      %-12s %-16s directory artifacts=%d  latest.json=%d  (objects under the "
              "prefix=%d)" % (firm, bucket, len(artifacts), len(pointer), len(keys)))
    record("b.1", "BLOCKED" if built == 0 else ("PASS" if built == 3 else "FAIL"),
           "firms with a landed directory artifact AND its pointer -- row IRPT_BCKEND-W2-S49: "
           "the runner host's identity is AccessDenied on 5 of 9 source prefixes and 3 of 3 "
           "destinations, so no build can land",
           "%d of 3" % built)


# ================================================================ ARM (c) -- FOUR ARMS
def arm_c():
    head("ARM (c) FOUR ARMS -- each reading its own distinct envelope value")
    sys.path.insert(0, DIRECTORY)
    sys.path.insert(0, os.path.join(REPO, "lib"))
    os.environ.setdefault("IRPT_DIRECTORY_BUCKET_MAP", json.dumps(FIRM_BUCKETS))
    import refresh                                                       # noqa: E402

    observed = {}

    # (c.1) THE TWO ARMS THAT ARE ALREADY ON THE REAL PATH, read from SERVED manifests and from
    #       the SSM records the deployed function created. Nothing simulated.
    key = "%s/_refresh/%s/manifest.json" % (DIRECTORY_PREFIX, DRIVEN_DATE)
    rc, out, err = aws("s3api", "get-object", "--bucket", FIRM_BUCKETS["49financial"],
                       "--key", key, os.path.join(HERE, "_bat_c.json"), "--output", "text")
    if rc == 0:
        man = json.load(open(os.path.join(HERE, "_bat_c.json"), encoding="utf-8"))
        observed["dispatched-or-failed (REAL PATH)"] = man["reason_code"]
        os.remove(os.path.join(HERE, "_bat_c.json"))

    inv, err = aws_json("ssm", "get-command-invocation", "--command-id", IMPORT_OK_COMMAND,
                        "--instance-id", RUNNER, "--output", "json")
    real_failed = (inv or {}).get("Status")
    print("      the REAL build command %s ended %s rc=%s -- which is what a later fire reads "
          "back" % (IMPORT_OK_COMMAND, real_failed, (inv or {}).get("ResponseCode")))

    # (c.2) EXPIRY -- driven on the REAL module with a controlled clock. No artifact is needed
    #       for this arm and none is simulated: `serve_read` is the deployed function's own
    #       read path, called with a directory dict and a clock.
    over = {"as_of_business_date": "2026-08-01", "directory_revision": "irpt-dir/x/1.0",
            "source_completion_date": "2026-08-01", "firm_id_opaque": "fir_x"}
    env_over, side = refresh.serve_read(over, "2026-09-11", "bat-rt6-expiry")
    observed["expiry (controlled clock)"] = env_over["public_reason_code"]
    print("      expiry: a directory as-of 2026-08-01 read at 2026-09-11 -> %s, age %s trading "
          "day(s) against a ceiling of %s, calendar %s"
          % (env_over["public_reason_code"], side.get("age_trading_days"),
             side.get("ceiling_trading_days"), side.get("calendar_source")))

    # (c.3) MISSED TRIGGER -- the REAL detector, on the real calendar, with a controlled clock.
    missed = refresh.missed_business_dates("2026-09-01", "2026-09-11")
    env_missed, man_missed = refresh.refresh_firm(
        "49financial", "2026-09-11", build_fn=None, last_manifest_as_of="2026-09-01",
        correlation_id="bat-rt6-missed")
    observed["missed trigger (controlled clock)"] = env_missed["public_reason_code"]
    print("      missed: last manifest 2026-09-01, clock 2026-09-11 -> %d expected trading "
          "day(s) with no manifest -> %s"
          % (len(missed or []), env_missed["public_reason_code"]))

    # (c.4) THE TWO ARMS THAT NEED A LANDED ARTIFACT.
    print("      source completion / new revision: both require a LANDED directory artifact to "
          "read a source date or a revision from. 0 of 3 firms have one (arm b) -- BLOCKED on "
          "row IRPT_BCKEND-W2-S49, not simulated here.")

    values = sorted(set(observed.values()))
    print("")
    for k in sorted(observed):
        print("      %-38s -> %s" % (k, observed[k]))
    record("c.1", "PASS" if len(values) == len(observed) else "FAIL",
           "the arms that can run read PAIRWISE DISTINCT envelope values: %s" % ", ".join(values),
           "%d distinct of %d arms run" % (len(values), len(observed)))
    record("c.2", "BLOCKED",
           "source completion and new revision cannot be driven on the REAL build path",
           "2 of 4 arms on the real path")


# ================================================================ ARM (d) -- THE HOST
def arm_d():
    head("ARM (d) THE HOST CAN RUN IT -- the import check, in the host's own stdout")
    inv, err = aws_json("ssm", "get-command-invocation", "--command-id", IMPORT_OK_COMMAND,
                        "--instance-id", RUNNER, "--output", "json")
    if inv is None:
        record("d.1", "FAIL", "get-command-invocation failed: %s" % err)
        return
    out = inv.get("StandardOutputContent") or ""
    for line in out.splitlines():
        if line.startswith("[irpt-directory]"):
            print("      | %s" % line[:150])
    import_ok = "IMPORT-OK" in out
    mods = [m for m in ("trading_calendar", "ids", "contract") if m in out]
    deps = [d for d in ("boto3", "pandas", "pyarrow", "jsonschema") if ("dep %-10s" % d).strip()
            in out or ("dep " + d) in out]
    record("d.1", "PASS" if import_ok else "FAIL",
           "the runner's import check PASSES on the host, first-party modules printed: %s"
           % ", ".join(mods), "%d of 3 modules named" % len(mods))
    record("d.2", "PASS" if len(deps) == 4 else "FAIL",
           "host dependency versions printed by the run itself: %s" % ", ".join(deps),
           "%d of 4" % len(deps))

    # THE DISCRIMINATOR: the SAME script printed IMPORT-FAIL before the bundle carried the
    # frontier. Without this, a passing import check could be a check that cannot fail.
    prev, err = aws_json("ssm", "get-command-invocation", "--command-id", IMPORT_FAIL_COMMAND,
                         "--instance-id", RUNNER, "--output", "json")
    prev_out = (prev or {}).get("StandardOutputContent") or ""
    record("d.3", "PASS" if "IMPORT-FAIL" in prev_out else "FAIL",
           "NEGATIVE CONTROL -- the SAME script on the SAME host with the 3-member bundle "
           "printed IMPORT-FAIL (command %s), so the pass above is a measurement and not a "
           "constant" % IMPORT_FAIL_COMMAND)

    # AND THE NAMED NEXT BLOCKER, verbatim from the host.
    err_out = (inv.get("StandardErrorContent") or "") + out
    named = [ln.strip() for ln in err_out.splitlines()
             if "FileNotFoundError" in ln or "ModuleNotFoundError" in ln or "REFUSE:" in ln]
    for ln in named[:2]:
        print("      NEXT BLOCKER (verbatim): %s" % ln[:150])
    record("d.4", "BLOCKED" if named else "PASS",
           "the build stops at a NAMED missing dependency -- row IRPT_BCKEND-W2-S51 enumerates "
           "all seven by subtraction over a printed denominator",
           "%d named line(s)" % len(named))


# =============================================================== ARM (e) -- LEDGERS
def arm_e():
    head("ARM (e) LEDGERS -- every entry closed, the sentinel gone, the plan clean")
    cm = os.path.join(REPO, "org", "critical_paths", "change_management")
    entries = sorted(f for f in os.listdir(cm) if "irpt-bckend-rt6" in f)
    closed = 0
    for f in entries:
        text = open(os.path.join(cm, f), encoding="utf-8", errors="replace").read()
        closed += 1 if "CLOSED" in text else 0
        print("      %-58s %s" % (f, "CLOSED" if "CLOSED" in text else "OPEN"))
    record("e.1", "PASS" if (entries and closed == len(entries)) else "FAIL",
           "change-management entries for this cell, all CLOSED",
           "%d of %d" % (closed, len(entries)))

    sentinel = os.path.join(REPO, "org", "critical_paths", ".open_deploys",
                            "irpt-bckend-rt6.json")
    record("e.2", "PASS" if not os.path.exists(sentinel) else "FAIL",
           "the cell's OPEN sentinel is absent (every entry closed and committed)")

    # The IAM the cell applied, read from the APPLIED plane -- comp-iam reads DESIRED only.
    pol, err = aws_json("iam", "get-role-policy", "--role-name", ROLE,
                        "--policy-name", "irpt-directory-refresh-policy", "--output", "json")
    sids = [s["Sid"] for s in ((pol or {}).get("PolicyDocument") or {}).get("Statement", [])]
    want = ["DispatchTheDirectoryBuildToOneRunnerOnly", "StartThatRunnerNeverStopIt",
            "ReadBackTheCommandsThisFunctionSent", "ListExactlyWhatItMayAlreadyRead"]
    got = [w for w in want if w in sids]
    record("e.3", "PASS" if len(got) == 4 else "FAIL",
           "the APPLIED role carries this cell's four statements: %s" % ", ".join(got),
           "%d of 4 (role holds %d statements)" % (len(got), len(sids)))

    # NO ec2:StopInstances ANYWHERE in the role: the refresh wakes the host and never stops it.
    actions = []
    for s in ((pol or {}).get("PolicyDocument") or {}).get("Statement", []):
        a = s.get("Action")
        actions.extend([a] if isinstance(a, str) else a)
    forbidden = [a for a in actions
                 if a in ("ec2:StopInstances", "ec2:TerminateInstances", "ssm:CancelCommand",
                          "iam:PassRole")]
    record("e.4", "PASS" if not forbidden else "FAIL",
           "the role holds NONE of StopInstances / TerminateInstances / CancelCommand / "
           "PassRole", "%d of %d actions are forbidden ones" % (len(forbidden), len(actions)))


# ================================================================== the verdict
def main():
    print("BATTERY IB-rt-6 -- the refresh builds behind the ENABLED schedule")
    print("repo: %s" % REPO)
    print("subject: the DEPLOYED %s, its APPLIED role, the three firm buckets, and the SSM "
          "records the function itself created" % FUNCTION)
    arm_a()
    arm_b()
    arm_c()
    arm_d()
    arm_e()

    head("VERDICT")
    npass = sum(1 for _, v, _, _ in RESULTS if v == "PASS")
    nfail = sum(1 for _, v, _, _ in RESULTS if v == "FAIL")
    nblock = sum(1 for _, v, _, _ in RESULTS if v == "BLOCKED")
    for arm, v, line, den in RESULTS:
        print("  %-6s %-9s %s" % (arm, v, line[:96]))
    print("")
    print("  PASS %d | FAIL %d | BLOCKED %d   denominator: %d graded check(s)"
          % (npass, nfail, nblock, len(RESULTS)))
    if nfail == 0 and nblock == 0:
        # Assembled, never written whole above: the acceptance <expect> is a REGEX and this
        # file's own source must not be able to satisfy it by accident.
        print("  " + "-".join(["IBRT6", "REFRESH", "BUILDS"]))
        return 0
    print("  THE ACCEPTANCE TOKEN IS WITHHELD. %d check(s) are BLOCKED on a premise this order "
          "cannot clear:" % nblock)
    print("    IRPT_BCKEND-W2-S49  mdpf-daily-runner-ec2-role is AccessDenied on 5 of 9 source")
    print("                        prefixes and 3 of 3 firm destinations -- no build can land")
    print("    IRPT_BCKEND-W2-S51  the minted bundle cannot carry the seven repo files the")
    print("                        runner reaches, three of them per-firm runner_commons")
    print("  RT6-AC1 is FAIL. The order stays open.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
