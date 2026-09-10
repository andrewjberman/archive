#!/usr/bin/env python3
"""ETFS_GUARDRAIL.TO-EG-s-21 -- S21-AC1 battery: THE DRIVEN REFUSAL.

Prints EGS21-REFUSAL-DRIVEN-AND-SENT on stdout ONLY when every arm (a)..(g) holds.

WHAT THIS BATTERY DOES NOT DO, AND WHY THAT IS THE POINT
--------------------------------------------------------
It does NOT invoke `etfs-reports-orchestrator` in `run` mode. The order permits exactly
ONE driven run and that run is still UNSPENT, because arm (a)'s companion PRE-FLIGHT --
"can the path this order drives actually reach a REFUSE verdict?" -- measures NO. The
served renderer calls `remediate._provider_for` on the `--no-ladder` branch (the only
branch that yields a driven REFUSE, R-EG-6 shape 1) and the `coverage` package the
reporter box holds does not define it. Firing would spend the run on an SSM Failed that
writes no verdict, no refusal artifacts and sends nothing. Row ETFS_GUARDRAIL-W4-S17.

So this battery MEASURES the blocking condition with a difference control rather than
asserting it, records arm (a) in full (it PASSES), and records arms (b)..(g) as
NOT-RUN-BLOCKED. It never converts an instrument's limit into a verdict.

EVERY AWS CALL HERE IS A READ OR A STRUCTURALLY SEND-FREE MODE:
  - lambda get-function-configuration / get-function  (read)
  - lambda invoke mode=recipients_qa                  (send-free by construction:
    lambda_function.py's recipients_qa branch resolves and returns; no `_ses` call
    site is reachable on it)
  - s3api list-objects-v2 / get-object / head-object  (read)
  - ec2 describe-instances, ssm describe-instance-information (read)
NO s3 write, NO s3 delete, NO ec2 start/stop, NO ssm send-command, NO SES send.
"""
from __future__ import annotations

import base64
import datetime
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import traceback

REGION = "us-east-1"
FUNCTION = "etfs-reports-orchestrator"
ETFS_BUCKET = "opal-data-etfs"
ARTIFACT_BUCKET = "opal-313476888478-lambda-artifacts"
ARTIFACT_PREFIX = "ec2/etfs-reports"
INSTANCE_ID = "i-070477bf35fc54409"
FORBIDDEN = "aj@opalinvest.com"
REQUIRED = "andrew@opalinvest.com"

# The forcing this order designed. Recorded here so the design is not re-derived.
FORCE_MONTH = "2026-08"
FORCE_PARTNER = "cottonwood"
FORCE_DATE = "2026-08-14"
FORCE_SPEC = "%s:%s" % (FORCE_PARTNER, FORCE_DATE)

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                          *([".."] * 7)))

RESULTS: list = []


def record(arm: str, state: str, detail: str) -> None:
    RESULTS.append((arm, state, detail))
    print("ARM %-4s %-16s %s" % (arm, state, detail))


def aws(*args: str) -> str:
    """Bounded AWS read via the vendored shim. Returns stdout (CR-stripped)."""
    # BOTH SHIM FORMS EXIST (CLAUDE.md: ".tools/aws shim (+aws.cmd, both or neither)").
    # CreateProcess cannot exec the bash form, so on win32 resolve aws.cmd.
    shim = os.path.join(REPO_ROOT, ".tools", "aws.cmd" if sys.platform == "win32" else "aws")
    out = subprocess.run([shim] + list(args), capture_output=True, text=True, timeout=180,
                         shell=False)
    if out.returncode != 0:
        raise RuntimeError("aws rc=%d: %s" % (out.returncode, (out.stderr or "")[:400]))
    return out.stdout.replace("\r", "")


# ---------------------------------------------------------------- arm (a) part 1
def deployed_bytes(tmp: str) -> tuple:
    cfg = json.loads(aws("lambda", "get-function-configuration", "--function-name", FUNCTION,
                          "--region", REGION, "--output", "json"))
    url = aws("lambda", "get-function", "--function-name", FUNCTION, "--region", REGION,
              "--query", "Code.Location", "--output", "text").strip()
    zip_path = os.path.join(tmp, "orch.zip")
    subprocess.run(["curl", "-s", "-o", zip_path, url], check=True, timeout=180)
    raw = open(zip_path, "rb").read()
    hex_sha = hashlib.sha256(raw).hexdigest()
    b64_sha = base64.b64encode(hashlib.sha256(raw).digest()).decode()
    import zipfile
    src = zipfile.ZipFile(zip_path).read("lambda_function.py")
    mod_path = os.path.join(tmp, "deployed_lambda_function.py")
    open(mod_path, "wb").write(src)
    return cfg, hex_sha, b64_sha, mod_path


def load_deployed_handler(mod_path: str, env: dict):
    saved = {k: os.environ.get(k) for k in env}
    os.environ.update(env)
    try:
        spec = importlib.util.spec_from_file_location("egs21_deployed_handler", mod_path)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        return m
    finally:
        for k, v in saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


def arm_a(tmp: str) -> bool:
    """(a) THE PRECONDITION, re-taken at THIS run's time on the DEPLOYED bytes."""
    ok = True
    cfg, hex_sha, b64_sha, mod_path = deployed_bytes(tmp)
    if b64_sha != cfg["CodeSha256"]:
        record("a", "FAIL", "downloaded zip digest %s != CodeSha256 %s" % (b64_sha, cfg["CodeSha256"]))
        return False
    record("a", "measured", "deployed zip sha256=%s (base64 %s == CodeSha256), LastModified=%s"
           % (hex_sha, b64_sha, cfg["LastModified"]))

    env_recipient = cfg["Environment"]["Variables"]["EMAIL_RECIPIENT"]
    record("a", "measured", "live EMAIL_RECIPIENT (the PRODUCER's set) = %r" % env_recipient)

    m = load_deployed_handler(mod_path, {
        "REPORTER_INSTANCE_ID": cfg["Environment"]["Variables"]["REPORTER_INSTANCE_ID"],
        "REPORTS_SNS_TOPIC": cfg["Environment"]["Variables"]["REPORTS_SNS_TOPIC"],
        "EMAIL_RECIPIENT": env_recipient,
        "AWS_DEFAULT_REGION": REGION,
    })

    # INSTRUMENT 1 -- offline, on the deployed artifact, with a NEGATIVE CONTROL.
    cases = {
        "test plain": {"test_run": True},
        "test + aj override": {"test_run": True, "test_recipients": [FORBIDDEN]},
        "test + aj mixed case": {"test_run": True,
                                  "test_recipients": ["AJ@OpalInvest.COM", REQUIRED]},
        "test + joined string": {"test_run": True,
                                  "test_recipients": "%s, %s" % (FORBIDDEN, REQUIRED)},
    }
    hits = 0
    n = 0
    for name, ev in cases.items():
        for label, base in (("report", m.EMAIL_RECIPIENT), ("terminal", m.TERMINAL_RECIPIENT)):
            hdr, dest = m._resolve_recipients(ev, base)
            n += 1
            bad = [a for a in dest if a.lower() == FORBIDDEN]
            if FORBIDDEN in (hdr or "").lower():
                bad = bad + ["<in To header>"]
            if bad:
                hits += 1
                record("a", "FAIL", "TEST branch %s/%s reached aj@: header=%r envelope=%s"
                       % (name, label, hdr, dest))
    record("a", "measured", "offline instrument on deployed bytes: aj@ hits %d of %d "
                            "adversarial TEST resolutions" % (hits, n))
    if hits:
        ok = False

    # THE NEGATIVE CONTROL -- if the scheduled branch does NOT carry aj@, the instrument
    # is blind and its zero above means nothing.
    sched_hdr, sched_dest = m._resolve_recipients({}, m.EMAIL_RECIPIENT)
    if FORBIDDEN not in [a.lower() for a in sched_dest]:
        record("a", "FAIL", "NEGATIVE CONTROL DEAD: scheduled report envelope %s does not "
                            "contain aj@, so the test-branch zero is not discriminating"
               % sched_dest)
        ok = False
    else:
        record("a", "measured", "negative control LIVE: scheduled report envelope=%s "
                                "(carries aj@), scheduled header=%r" % (sched_dest, sched_hdr))

    # INSTRUMENT 2 -- the RUNNING function, send-free recipients_qa, adversarial probe.
    payload = os.path.join(tmp, "rq.json")
    open(payload, "w", encoding="utf-8").write(json.dumps(
        {"mode": "recipients_qa",
         "probe": {"test_recipients": [FORBIDDEN, "AJ@OpalInvest.COM", REQUIRED]}}))
    out_path = os.path.join(tmp, "rq_out.json")
    aws("lambda", "invoke", "--function-name", FUNCTION, "--region", REGION,
        "--payload", "file://" + payload, out_path, "--output", "json")
    live = json.loads(open(out_path, encoding="utf-8").read())
    live_test = live["test"]
    live_bad = [a for grp in live_test.values() for a in grp if a.lower() == FORBIDDEN]
    record("a", "measured", "live recipients_qa on the RUNNING function: test=%s scheduled=%s"
           % (json.dumps(live_test), json.dumps(live["scheduled"])))
    if live_bad:
        record("a", "FAIL", "RUNNING function's test resolution reached aj@: %s" % live_bad)
        ok = False
    if FORBIDDEN not in [a.lower() for a in live["scheduled"]["report"]]:
        record("a", "FAIL", "live negative control DEAD (scheduled.report lacks aj@)")
        ok = False
    if REQUIRED not in live_test["terminal"]:
        record("a", "FAIL", "live test.terminal does not contain %s: %s" % (REQUIRED, live_test["terminal"]))
        ok = False

    # EG-s-20 terminal, its flip cited.
    to20 = os.path.join(REPO_ROOT, "org", "missions", "D8", "ETFS", "ETFS_GUARDRAIL",
                        "task-orders",
                        "ETFS_GUARDRAIL.TO-EG-s-20.the-send-path-correct-and-test-safe.md")
    status = ""
    with open(to20, encoding="utf-8") as f:
        for line in f:
            if line.startswith("<status>"):
                status = line.strip()
                break
    flip = subprocess.run(["git", "log", "--full-history", "-1", "--format=%H %cI %s",
                           "-S", "complete -- 2026-09-10", "--", to20],
                          capture_output=True, text=True, cwd=REPO_ROOT, timeout=180).stdout.strip()
    if not status.startswith("<status>complete"):
        record("a", "FAIL", "EG-s-20 status is not complete: %s" % status[:160])
        ok = False
    else:
        record("a", "measured", "EG-s-20 TERMINAL: %s" % status[:200])
        record("a", "measured", "EG-s-20 flip commit: %s" % (flip or "<not isolated by -S>"))

    record("a", "PASS" if ok else "FAIL",
           "the test-invocation recipient path CANNOT reach %s on the bytes deployed at this "
           "run's time; two instruments, both with a live negative control" % FORBIDDEN)
    return ok


# ------------------------------------------------------- the PRE-FIRE feasibility gate
def preflight_can_the_path_refuse(tmp: str) -> tuple:
    """Can the driven run reach a REFUSE verdict at all?

    Returns (feasible: bool, detail: str). Measured by EXERCISE with a DIFFERENCE
    CONTROL, never by reading the renderer alone -- the renderer is current and the
    package it imports is not, and a per-file check of the renderer certifies clean.
    """
    listing = json.loads(aws("s3api", "list-objects-v2", "--bucket", ARTIFACT_BUCKET,
                              "--prefix", ARTIFACT_PREFIX, "--output", "json"))
    contents = {c["Key"]: c for c in listing.get("Contents", [])}
    print("  artifact prefix denominator: %d object(s)" % len(contents))
    for k in sorted(contents):
        print("    %-58s %8d  %s" % (k, contents[k]["Size"], contents[k]["LastModified"]))

    box = os.path.join(tmp, "box_sim")
    repo_sim = os.path.join(tmp, "repo_sim")
    for d in (box, repo_sim):
        os.makedirs(os.path.join(d, "coverage"), exist_ok=True)

    renderer_repo = os.path.join(REPO_ROOT, "data", "etfs", "scripts", "presentation",
                                 "render_month_end.py")
    dep_renderer = os.path.join(tmp, "render_month_end.deployed.py")
    aws("s3api", "get-object", "--bucket", ARTIFACT_BUCKET,
        "--key", "%s/render_month_end.py" % ARTIFACT_PREFIX, dep_renderer, "--output", "json")
    dep_r = open(dep_renderer, "rb").read()
    repo_r = open(renderer_repo, "rb").read().replace(b"\r\n", b"\n")
    print("  SERVED render_month_end.py sha256=%s  == repo(LF): %s"
          % (hashlib.sha256(dep_r).hexdigest(), dep_r == repo_r))

    # The SERVED renderer is what BOTH arms run. Only the coverage package differs.
    for d in (box, repo_sim):
        shutil.copy(dep_renderer, os.path.join(d, "render_month_end.py"))

    cov_names = ["__init__.py", "classifier.py", "remediate.py", "trading_calendar.py",
                 "_orion_vendor_asof.py"]
    for name in cov_names:
        aws("s3api", "get-object", "--bucket", ARTIFACT_BUCKET,
            "--key", "%s/coverage/%s" % (ARTIFACT_PREFIX, name),
            os.path.join(box, "coverage", name), "--output", "json")
    repo_map = {
        "__init__.py": os.path.join(REPO_ROOT, "data/etfs/scripts/coverage/__init__.py"),
        "classifier.py": os.path.join(REPO_ROOT, "data/etfs/scripts/coverage/classifier.py"),
        "remediate.py": os.path.join(REPO_ROOT, "data/etfs/scripts/coverage/remediate.py"),
        "trading_calendar.py": os.path.join(REPO_ROOT, "lib/trading_calendar.py"),
    }
    for name, src in repo_map.items():
        data = open(src, "rb").read().replace(b"\r\n", b"\n")
        open(os.path.join(repo_sim, "coverage", name), "wb").write(data)
    shutil.copy(os.path.join(box, "coverage", "_orion_vendor_asof.py"),
                os.path.join(repo_sim, "coverage", "_orion_vendor_asof.py"))

    for name in ("classifier.py", "remediate.py"):
        b = open(os.path.join(box, "coverage", name), "rb").read()
        r = open(os.path.join(repo_sim, "coverage", name), "rb").read()
        print("  coverage/%-18s deployed=%6d repo=%6d IDENTICAL=%s"
              % (name, len(b), len(r), b == r))
    dep_defs = re.findall(r"^def (\w+)", open(os.path.join(box, "coverage", "remediate.py"),
                                               encoding="utf-8").read(), re.M)
    repo_defs = re.findall(r"^def (\w+)", open(os.path.join(repo_sim, "coverage", "remediate.py"),
                                                encoding="utf-8").read(), re.M)
    print("  DEPLOYED remediate defs: %s" % dep_defs)
    print("  REPO     remediate defs: %s" % repo_defs)

    results = {}
    for label, sim in (("DEPLOYED", box), ("REPO", repo_sim)):
        results[label] = _exercise(sim, label)
    feasible = results["DEPLOYED"] == "REFUSE"
    detail = ("DEPLOYED-package result=%r ; REPO-package result=%r ; difference control "
              "discriminates=%s" % (results["DEPLOYED"], results["REPO"],
                                     results["DEPLOYED"] != results["REPO"]))
    return feasible, detail


class _StubS3:
    def __init__(self):
        self.puts = []

    def put_object(self, **kw):
        self.puts.append(kw.get("Key"))
        return {}


def _exercise(sim_dir: str, label: str) -> str:
    """Run the SERVED renderer's --no-ladder gate branch over `sim_dir`'s coverage
    package. ZERO AWS calls: stub probe, supplied series, module `s3` stubbed."""
    for mod in [m for m in list(sys.modules) if m == "coverage" or m.startswith("coverage.")]:
        del sys.modules[mod]
    for p in list(sys.path):
        if p.endswith("box_sim") or p.endswith("repo_sim"):
            sys.path.remove(p)
    try:
        spec = importlib.util.spec_from_file_location(
            "egs21_rme_%s" % label, os.path.join(sim_dir, "render_month_end.py"))
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
    except Exception as e:  # noqa: BLE001
        return "IMPORT-FAIL: %s: %s" % (type(e).__name__, e)
    m.s3 = _StubS3()
    d = datetime.date(2026, 8, 1)
    series = {}
    while d <= datetime.date(2026, 8, 31):
        if m.classifier.tcal.is_trading_day(d):
            series[d.isoformat()] = {"any": 1}
        d += datetime.timedelta(days=1)
    daily = {FORCE_PARTNER: dict(series)}
    fx = m._parse_fixture_remove(FORCE_SPEC)
    m._apply_fixture_remove(daily, fx)
    print("  [%s] remediate=%s has _provider_for=%s; %d trading slices, %d after forcing"
          % (label, os.path.basename(os.path.dirname(m.remediate.__file__)),
             hasattr(m.remediate, "_provider_for"), len(series), len(daily[FORCE_PARTNER])))
    try:
        v = m.coverage_gate(FORCE_MONTH, [FORCE_PARTNER], daily, [], ladder=False,
                            probe=lambda p, ds: {"partition": True, "priced": 4},
                            fixture_remove=fx, fixture_remove_spec=FORCE_SPEC,
                            run_id="EGS21-PREFLIGHT", run_id_source="offline exercise")
    except Exception as e:  # noqa: BLE001
        print("  [%s] coverage_gate RAISED: %s: %s" % (label, type(e).__name__, e))
        tb = traceback.format_exc().strip().split("\n")
        print("  [%s]   at %s" % (label, tb[-3].strip() if len(tb) > 3 else tb[-1]))
        return "%s: %s" % (type(e).__name__, e)
    print("  [%s] VERDICT=%s holes=%s C=%s puts=%s"
          % (label, v["verdict"], v["holes"],
             v["per_partner"][FORCE_PARTNER]["summary"]["C"], m.s3.puts))
    return v["verdict"]


def blocked_arms_cost(tmp: str) -> None:
    """What firing anyway would have produced -- measured, not asserted."""
    # AN ABSENCE NEEDS A POSITIVE CONTROL BESIDE IT: an rc!=0 from a broken call and an
    # rc!=0 from a genuine 404 are the same number. Read a key that MUST exist first.
    def head(key: str) -> str:
        try:
            out = json.loads(aws("s3api", "head-object", "--bucket", ETFS_BUCKET,
                                  "--key", key, "--output", "json"))
            return "PRESENT LastModified=%s ETag=%s VersionId=%s" % (
                out.get("LastModified"), out.get("ETag"),
                out.get("VersionId", "<ABSENT -- opal-data-etfs is UNVERSIONED>"))
        except RuntimeError as e:
            return "ABSENT-OR-ERROR (%s)" % " ".join(str(e).split())[:120]

    ctrl_key = "platinum/reports/%s/coverage_verdict.json" % FORCE_MONTH
    print("  POSITIVE CONTROL %s\n      -> %s" % (ctrl_key, head(ctrl_key)))
    tgt_key = "platinum/reports/%s/coverage_unresolved.json" % FORCE_MONTH
    print("  TARGET           %s\n      -> %s" % (tgt_key, head(tgt_key)))
    print("  (control PRESENT + target ABSENT => the absence is the OBJECT'S, not the CALL'S)")
    ec2 = json.loads(aws("ec2", "describe-instances", "--instance-ids", INSTANCE_ID,
                          "--region", REGION, "--output", "json"))
    inst = ec2["Reservations"][0]["Instances"][0]
    print("  reporter box %s state=%s LaunchTime=%s reason=%r"
          % (INSTANCE_ID, inst["State"]["Name"], inst.get("LaunchTime"),
             inst.get("StateTransitionReason")))
    ssm = json.loads(aws("ssm", "describe-instance-information", "--region", REGION,
                          "--filters", "Key=InstanceIds,Values=%s" % INSTANCE_ID,
                          "--output", "json"))
    print("  ssm describe-instance-information denominator: %d (Online rows)"
          % len(ssm.get("InstanceInformationList", [])))


def main() -> int:
    print("EGS21 BATTERY -- ETFS_GUARDRAIL.TO-EG-s-21, 0.9.0_WK_ETFS_GUARDRAIL~4")
    print("started %sZ" % datetime.datetime.now(datetime.timezone.utc)
          .strftime("%Y-%m-%dT%H:%M:%S"))
    tmp = tempfile.mkdtemp(prefix="egs21_")
    try:
        print("\n--- ARM (a) THE PRECONDITION (deployed bytes, this run's time) ---")
        a_ok = arm_a(tmp)

        print("\n--- PRE-FIRE FEASIBILITY GATE (not an arm; it decides whether firing is legal) ---")
        feasible, detail = preflight_can_the_path_refuse(tmp)
        print("  %s" % detail)

        print("\n--- WHAT FIRING ANYWAY WOULD HAVE COST (measured) ---")
        blocked_arms_cost(tmp)

        print()
        if not feasible:
            for arm, why in (
                ("b", "the forcing's DISCLOSURE is read from a produced artifact; no artifact is produced"),
                ("c", "coverage_verdict.json is never written -- coverage_gate raises before it returns"),
                ("d", "no refusal artifacts and no egress ask exist to head-object"),
                ("e", "the terminal send guard is False (coverage_unresolved.json 404 -> [])"),
                ("f", "there is no forcing to undo -- the run did not happen"),
                ("g", "the run wrote no keys, so there is no write enumeration to make"),
            ):
                record(arm, "NOT-RUN-BLOCKED", why)
            record("PRE", "BLOCKING", detail)
            print("\nS21-AC1 RESULT: FAIL -- token NOT printed.")
            print("BLOCKING ROW: ETFS_GUARDRAIL-W4-S17")
            print("THE SINGLE PERMITTED DRIVEN RUN IS UNSPENT.")
            print("arm (a): %s" % ("PASS" if a_ok else "FAIL"))
            return 1

        # Unreachable in this world; kept so a re-cut after the disarm has the shape.
        print("PRE-FIRE GATE CLEAR -- but this battery does not fire: the driven run is the "
              "issuer's to re-authorize (ONE run, and it needs a fresh ruling).")
        print("\nS21-AC1 RESULT: FAIL -- token NOT printed (arms b..g unmeasured).")
        return 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
