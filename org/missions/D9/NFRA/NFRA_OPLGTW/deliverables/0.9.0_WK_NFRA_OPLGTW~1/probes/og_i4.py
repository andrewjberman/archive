#!/usr/bin/env python3
"""OG-i-4 -- the pilot host resize, t4g.nano -> t4g.small (NFRA_OPLGTW.TO-OG-i-4).

Usage:
    og_i4.py AC<n> [--record]   measure criterion OGI4-AC<n>; print measurement, vintage, denominator,
                                then exactly one line  VERDICT: PASS-OGI4-AC<n> | FAIL-OGI4-AC<n> <reason>

--record writes this run's measurement into OGI4_BASELINE.json beside this probe's deliverables folder
(AC6 only; a verifier re-run without --record never rewrites the recorded re-take).

AC1-AC3 grade the ALREADY-COMPLETED act (ledger citation, plan shape, apply-through-safe-apply-under-
the-ledger) by reading the committed evidence this same worker wrote at act time -- the act (a stop/
start of a single production EC2 instance) is not re-run by a grading invocation. AC4-AC6 are live reads
made fresh at every invocation: the instance's own live state, a live unauthenticated HTTP probe, and a
live CloudWatch re-take of OG-p-1's OGP1-AC11 latency instrument.

Every AWS call goes through aws() below, which runs the workspace shim `.tools/aws` (CLI v1) via
msys_safe_run and appends one row per call to command_log.jsonl beside this probe's deliverables folder.
No secret enters the output.
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

REGION = "us-east-1"
INSTANCE_ID = "i-07dccb1615503ac99"
ALB_NAME = "opal-gateway"
GATEWAY_URL = "https://mcp.opalinvest.dev/mcp"
AC11_WINDOW_DAYS = 14  # OG-p-1's own window rule (CloudWatch p95 retention-boundary trap; og_p1.py:804)
EXPECTED_INSTANCE_TYPE = "t4g.small"
EXPECTED_ARCH = "arm64"
LEDGER_SLUG = "nfra-oplgtw-og-i-4-pilot-host"
ANDREW_DIRECT_PATH = ("org/tier1_exec/1.0.0_SA_CTO/deliverables/"
                       "ANDREW_DIRECT_20260918_140xZ_FOUR_CARDS_ANSWERED_GA_YES_SPRINT_EMPLOYEES.md")
ANDREW_DIRECT_COMMIT = "80558e1508"

HERE = Path(__file__).resolve()
DELIV = HERE.parents[1]
EVID = DELIV / "evidence" / "og_i4"
CMDLOG = DELIV / "command_log.jsonl"
OGI4_BASELINE = DELIV / "OGI4_BASELINE.json"
LEDGER_ENTRY = None  # resolved in ac1()/ac3() by scanning change_management/


def _root() -> Path:
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=str(HERE.parent),
                          capture_output=True, text=True, check=True)
    return Path(out.stdout.strip())


ROOT = _root()
sys.path.insert(0, str(ROOT / ".tools"))
from msys_argv_guard import msys_safe_run  # noqa: E402

CRIT = "?"
LINES: list = []
LOCK = ROOT / ".scratch" / "og_i4" / "write.lock"


class _Lock:
    def __enter__(self):
        LOCK.parent.mkdir(parents=True, exist_ok=True)
        deadline = time.time() + 30
        while True:
            try:
                self.fd = os.open(str(LOCK), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                return self
            except FileExistsError:
                if time.time() > deadline:
                    raise RuntimeError(f"lock {LOCK} held for >30 s")
                time.sleep(0.05)

    def __exit__(self, *exc):
        os.close(self.fd)
        os.remove(str(LOCK))


def utcnow() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def say(line: str = "") -> None:
    LINES.append(line)
    print(line, flush=True)


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _api_op(cli_op: str) -> str:
    return "".join(p[:1].upper() + p[1:] for p in cli_op.split("-"))


def aws(service: str, cli_op: str, *args: str, note: str = ""):
    """One AWS CLI call through .tools/aws. Returns (parsed_json_or_None, error_text_or_None, rc)."""
    argv = [".tools/aws", service, cli_op, *args, "--region", REGION, "--output", "json"]
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    started = utcnow()
    r = msys_safe_run(argv, cwd=str(ROOT), env=env, capture_output=True, timeout=90)
    row = {"ts": started, "serial": os.environ.get("OPAL_AGENT_SERIAL", ""), "criterion": CRIT,
           "service": service, "cli_op": cli_op, "api_op": _api_op(cli_op), "rc": r.returncode,
           "instrument": ".tools/aws (AWS CLI v1) via msys_safe_run", "note": note}
    with _Lock(), open(CMDLOG, "a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(row, separators=(",", ":")) + "\n")
    out = r.stdout.decode("utf-8")
    err = r.stderr.decode("utf-8", errors="replace")
    if r.returncode != 0:
        return None, err.strip() or f"rc={r.returncode}", r.returncode
    return (json.loads(out) if out.strip() else {}), None, 0


def ssm_read(script: str, label: str) -> tuple:
    """Run a READ-ONLY shell script on the Gateway host. Returns (stdout, meta) or raises."""
    end = "__OGI4_END__"
    lines = script.strip("\n").split("\n") + [f"echo {end}"]
    params = json.dumps({"commands": lines, "executionTimeout": ["60"]})
    note = f"host read {label}; script sha256={sha256_bytes(chr(10).join(lines).encode())[:16]}"
    sent, err, _ = aws("ssm", "send-command", "--instance-ids", INSTANCE_ID, "--document-name",
                        "AWS-RunShellScript", "--comment", f"OG-i-4 read-only {label}",
                        "--parameters", params, note=note)
    if err:
        raise RuntimeError(f"send-command failed: {err[:300]}")
    cid = sent["Command"]["CommandId"]
    deadline = time.time() + 70
    inv = None
    while time.time() < deadline:
        time.sleep(2)
        inv, err, _ = aws("ssm", "get-command-invocation", "--command-id", cid, "--instance-id",
                           INSTANCE_ID, note=f"poll {label}")
        if err:
            if "InvocationDoesNotExist" in err:
                continue
            raise RuntimeError(f"get-command-invocation failed: {err[:300]}")
        if inv.get("Status") in ("Success", "Failed", "Cancelled", "TimedOut", "Undeliverable", "Terminated"):
            break
    if not inv or inv.get("Status") != "Success":
        raise RuntimeError(f"ssm {cid} status={inv and inv.get('Status')}")
    out = inv.get("StandardOutputContent", "")
    meta = {"command_id": cid, "instance_id": INSTANCE_ID, "status": inv["Status"],
            "executed_utc": inv.get("ExecutionEndDateTime", "")}
    return out, meta


def sections(out: str) -> dict:
    res: dict = {}
    cur = "_"
    for line in out.splitlines():
        if line.startswith("### "):
            cur = line[4:].strip()
            res[cur] = []
        else:
            res.setdefault(cur, []).append(line)
    return res


def _ledger_entry_text() -> tuple:
    """Find the change_management entry for LEDGER_SLUG. Returns (path, text) or (None, '')."""
    cmdir = ROOT / "org" / "critical_paths" / "change_management"
    for p in sorted(cmdir.glob("*_" + LEDGER_SLUG + "_deploy_completion.md")):
        return p, p.read_text(encoding="utf-8", errors="replace")
    return None, ""


# ------------------------------------------------------------------------------------------- AC1
def ac1() -> tuple:
    """The ledger entry cites the Andrew-direct record authorizing this stop/start, by path@commit,
    and that record exists at the cited commit."""
    path, text = _ledger_entry_text()
    if not path:
        return False, f"no change_management entry found for slug {LEDGER_SLUG}", {}, 0
    m = re.search(r"(org/tier1_exec/[^\s@`]+\.md)@([0-9a-f]{7,40})", text)
    denom = 1
    if not m:
        return False, "no <path>@<commit> citation found in the ledger entry", {"ledger_path": str(path)}, denom
    cited_path, cited_commit = m.group(1), m.group(2)
    exists = subprocess.run(["git", "cat-file", "-e", f"{cited_commit}:{cited_path}"], cwd=str(ROOT),
                             capture_output=True)
    ok = exists.returncode == 0
    body = subprocess.run(["git", "show", f"{cited_commit}:{cited_path}"], cwd=str(ROOT),
                           capture_output=True, text=True, errors="replace")
    carries_go = "Yes go ahead" in (body.stdout if ok else "")
    say(f"instrument: read {path.relative_to(ROOT)} for a <path>@<commit> citation; `git cat-file -e "
        f"<commit>:<path>` to confirm existence at that commit; git show to confirm its content")
    say(f"vintage: {utcnow()}")
    say("denominator: 1 ledger entry, 1 citation found")
    say(f"cited: {cited_path}@{cited_commit}")
    say(f"git cat-file -e {cited_commit}:{cited_path} -> rc={exists.returncode} ({'PRESENT' if ok else 'ABSENT'})")
    say(f"cited record carries 'Yes go ahead' (Call 1, G-A lift): {carries_go}")
    measure = {"ledger_path": str(path.relative_to(ROOT)), "cited_path": cited_path,
               "cited_commit": cited_commit, "exists_at_commit": ok, "carries_go_ahead": carries_go}
    ok_all = ok and carries_go
    return ok_all, ("" if ok_all else "citation absent or does not carry the G-A lift text"), measure, denom


# ------------------------------------------------------------------------------------------- AC2
def ac2() -> tuple:
    """The plan changes only instance_type on aws_instance.gw and does not replace the instance."""
    p = EVID / "resize.plan.json"
    if not p.is_file():
        return False, f"no plan evidence at {p}", {}, 0
    d = json.loads(p.read_text(encoding="utf-8"))
    non_noop = d.get("non_noop", [])
    denom = d.get("total_resource_changes", 0)
    say(f"instrument: `terraform show -json` of the saved planfile (redacted to {p.relative_to(ROOT)}); "
        f"source_sha256={d.get('source_sha256')}")
    say(f"vintage: plan generated pre-apply this session; terraform_version={d.get('terraform_version')}")
    say(f"denominator: {denom} resource_changes entries, {len(non_noop)} non-no-op")
    reasons = []
    if len(non_noop) != 1:
        reasons.append(f"expected exactly 1 non-no-op resource, found {len(non_noop)}")
    else:
        e = non_noop[0]
        say(f"  address={e['address']} type={e['type']} actions={e['actions']} replace_paths={e['replace_paths']}")
        say(f"  changed_attribute_names={e['changed_attribute_names']} after_unknown_true={e['after_unknown_true']}")
        say(f"  instance_type: before={e['before_instance_type']} after={e['after_instance_type']}")
        if e["address"] != "aws_instance.gw":
            reasons.append(f"changed resource is {e['address']!r}, not aws_instance.gw")
        if e["actions"] != ["update"]:
            reasons.append(f"actions={e['actions']!r}, not a plain update (a replace/create/delete)")
        if e["replace_paths"]:
            reasons.append(f"replace_paths={e['replace_paths']!r} is non-empty -- this is a replace")
        # concretely-declared changed attributes = changed_attribute_names MINUS those recomputed-to-
        # unknown (after_unknown=true): those are a mechanical side effect of the stop/start (no EIP on
        # this instance), not an independently configured change. See row NFRA_OPLGTW-W1-S14.
        declared_changed = sorted(set(e["changed_attribute_names"]) - set(e["after_unknown_true"]))
        say(f"  concretely-declared changed attribute(s) (excludes recompute-to-unknown side effects): "
            f"{declared_changed}")
        if declared_changed != ["instance_type"]:
            reasons.append(f"declared changed attributes {declared_changed} != ['instance_type']")
        if e["after_instance_type"] != EXPECTED_INSTANCE_TYPE:
            reasons.append(f"after instance_type {e['after_instance_type']!r} != {EXPECTED_INSTANCE_TYPE!r}")
    ok = not reasons
    return ok, "; ".join(reasons), d, denom


# ------------------------------------------------------------------------------------------- AC3
def ac3() -> tuple:
    """The apply runs through safe-apply under a ledger entry opened and committed before the act and
    closed before the reads."""
    apply_txt = (EVID / "apply_output.txt").read_text(encoding="utf-8", errors="replace") \
        if (EVID / "apply_output.txt").is_file() else ""
    path, ledger_txt = _ledger_entry_text()
    sentinel = ROOT / "org" / "critical_paths" / ".open_deploys" / f"{LEDGER_SLUG}.json"
    denom = 4
    reasons = []
    ran_safe_apply = "safe-apply: comp-tagauthz gate PASSED" in apply_txt and "tombstone-gate" in apply_txt
    apply_complete = bool(re.search(r"^Apply complete! Resources: 0 added, 1 changed, 0 destroyed\.$",
                                     apply_txt, re.M))
    say(f"instrument: committed apply evidence ({(EVID / 'apply_output.txt').relative_to(ROOT)}) + the "
        f"change_management ledger entry ({path.relative_to(ROOT) if path else 'MISSING'}) + the sentinel's "
        f"absence (closed)")
    say(f"vintage: {utcnow()}")
    say(f"denominator: {denom} check(s) -- ran-through-safe-apply, apply-complete-line, ledger-status=CLOSED, "
        f"sentinel-absent")
    say(f"ran through safe-apply (tagauthz + tombstone gate markers present): {ran_safe_apply}")
    say(f"'Apply complete! Resources: 0 added, 1 changed, 0 destroyed.' present: {apply_complete}")
    ledger_closed = bool(re.search(r"^\*\*Status:\*\* CLOSED\b", ledger_txt, re.M))
    sentinel_absent = not sentinel.is_file()
    say(f"ledger entry reads CLOSED: {ledger_closed}")
    say(f"sentinel {sentinel.relative_to(ROOT)} absent (closed removes it): {sentinel_absent}")
    if not ran_safe_apply:
        reasons.append("apply evidence does not show safe-apply's own gates running")
    if not apply_complete:
        reasons.append("apply evidence does not show a clean 1-changed apply-complete line")
    if not ledger_closed:
        reasons.append("ledger entry does not read CLOSED")
    if not sentinel_absent:
        reasons.append("open-deploys sentinel still present -- ledger not closed")
    ok = not reasons
    measure = {"ran_safe_apply": ran_safe_apply, "apply_complete": apply_complete,
               "ledger_closed": ledger_closed, "sentinel_absent": sentinel_absent,
               "ledger_path": str(path.relative_to(ROOT)) if path else None}
    return ok, "; ".join(reasons), measure, denom


# ------------------------------------------------------------------------------------------- AC4
def ac4() -> tuple:
    """The instance reads t4g.small, arm64, running (live read)."""
    data, err, _ = aws("ec2", "describe-instances", "--instance-ids", INSTANCE_ID, note="AC4 live instance state")
    if err:
        return False, f"describe-instances: {err[:200]}", {}, 0
    inst = data["Reservations"][0]["Instances"][0]
    itype, arch, state = inst.get("InstanceType"), inst.get("Architecture"), inst["State"]["Name"]
    say(f"instrument: ec2 describe-instances on {INSTANCE_ID} via .tools/aws")
    say(f"vintage: {utcnow()}")
    say("denominator: 1 instance read")
    say(f"InstanceType={itype} Architecture={arch} State={state} LaunchTime={inst.get('LaunchTime')} "
        f"PublicIp={inst.get('PublicIpAddress')}")
    reasons = []
    if itype != EXPECTED_INSTANCE_TYPE:
        reasons.append(f"InstanceType={itype!r} != {EXPECTED_INSTANCE_TYPE!r}")
    if arch != EXPECTED_ARCH:
        reasons.append(f"Architecture={arch!r} != {EXPECTED_ARCH!r}")
    if state != "running":
        reasons.append(f"State={state!r} != 'running'")
    ok = not reasons
    measure = {"instance_type": itype, "architecture": arch, "state": state,
               "launch_time": inst.get("LaunchTime"), "public_ip": inst.get("PublicIpAddress")}
    return ok, "; ".join(reasons), measure, 1


# ------------------------------------------------------------------------------------------- AC5
def ac5() -> tuple:
    """After the restart, the Gateway's systemd unit is active and an unauthenticated /mcp returns 401
    with the resource challenge (both read live)."""
    script = """echo "### unit"
systemctl show opal-gateway -p ActiveState -p SubState -p ActiveEnterTimestamp -p MainPID -p NRestarts --no-pager
"""
    out, meta = ssm_read(script, "AC5 systemd state")
    sec = sections(out)
    unit = dict(line.split("=", 1) for line in sec.get("unit", []) if "=" in line)
    active = unit.get("ActiveState") == "active" and unit.get("SubState") == "running"

    req = urllib.request.Request(GATEWAY_URL, method="GET")
    status, headers, body = None, {}, ""
    http_err = None
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        status, headers = resp.status, dict(resp.headers)
    except urllib.error.HTTPError as e:
        status, headers = e.code, dict(e.headers.items())
        body = e.read().decode("utf-8", "replace")
    except Exception as e:  # pragma: no cover - network problem, reported as a measurement, not swallowed
        http_err = f"{type(e).__name__}: {e}"

    say(f"instrument: SSM AWS-RunShellScript systemctl show on {meta['instance_id']} (ssm {meta['command_id']} "
        f"{meta['status']} at {meta['executed_utc']}); external unauthenticated GET {GATEWAY_URL} via urllib")
    say(f"vintage: {utcnow()}")
    say("denominator: 2 read(s) -- systemd state, HTTP probe")
    say(f"systemd: ActiveState={unit.get('ActiveState')} SubState={unit.get('SubState')} "
        f"MainPID={unit.get('MainPID')} NRestarts={unit.get('NRestarts')} "
        f"ActiveEnterTimestamp={unit.get('ActiveEnterTimestamp')}")
    if http_err:
        say(f"HTTP probe error: {http_err}")
    else:
        say(f"HTTP {status}; WWW-Authenticate={headers.get('www-authenticate') or headers.get('WWW-Authenticate')}")
        say(f"body: {body[:200]}")
    reasons = []
    if not active:
        reasons.append(f"systemd not active/running: ActiveState={unit.get('ActiveState')} "
                        f"SubState={unit.get('SubState')}")
    if http_err:
        reasons.append(f"HTTP probe failed: {http_err}")
    else:
        challenge = (headers.get("www-authenticate") or headers.get("WWW-Authenticate") or "")
        has_challenge = "resource_metadata" in challenge and "Bearer" in challenge
        if status != 401:
            reasons.append(f"HTTP status {status} != 401")
        if not has_challenge:
            reasons.append(f"WWW-Authenticate header lacks a Bearer resource_metadata challenge: {challenge!r}")
    ok = not reasons
    measure = {"systemd": unit, "http_status": status, "http_headers": headers, "http_body": body[:500],
               "http_error": http_err}
    return ok, "; ".join(reasons), measure, 2


# ------------------------------------------------------------------------------------------- AC6
def _lb_dim(arn: str) -> str:
    return re.search(r":loadbalancer/(.+)$", arn).group(1)


def _tg_dim(arn: str) -> str:
    return re.search(r"(targetgroup/.+)$", arn).group(1)


def _cw_p95(dims: list, start: str, end: str, period: int, note: str) -> tuple:
    dim_args = [",".join(f"{k}={v}" for k, v in d.items()) for d in dims]
    data, err, _ = aws("cloudwatch", "get-metric-statistics", "--namespace", "AWS/ApplicationELB",
                        "--metric-name", "TargetResponseTime", "--dimensions", *dim_args,
                        "--start-time", start, "--end-time", end, "--period", str(period),
                        "--statistics", "SampleCount", "--extended-statistics", "p95", note=note)
    return data, err


def _cw_datapoint(data: dict) -> tuple:
    dps = (data or {}).get("Datapoints", [])
    if not dps:
        return None, None, None
    if len(dps) > 1:
        return None, None, (f"CloudWatch returned {len(dps)} datapoints for a one-period query "
                             f"(expected 1): {[(d.get('Timestamp'), d.get('SampleCount')) for d in dps]}")
    dp = dps[0]
    return dp.get("SampleCount"), (dp.get("ExtendedStatistics") or {}).get("p95"), None


def ac6() -> tuple:
    """The existing-user baseline (OG-p-1's OGP1-AC11: p95 TargetResponseTime, 14-day CloudWatch window)
    is re-taken on the new host with the same instrument and window rule."""
    lbs, err, _ = aws("elbv2", "describe-load-balancers", "--names", ALB_NAME, note="AC6 resolve ALB")
    if err:
        return False, f"describe-load-balancers: {err[:200]}", {}, 0
    arn = lbs["LoadBalancers"][0]["LoadBalancerArn"]
    lb_dim = _lb_dim(arn)
    tgs, err2, _ = aws("elbv2", "describe-target-groups", "--load-balancer-arn", arn, note="AC6 target groups")
    if err2:
        return False, f"describe-target-groups: {err2[:200]}", {}, 0
    tg_arns = [tg["TargetGroupArn"] for tg in tgs.get("TargetGroups", [])]
    end_dt = _dt.datetime.now(_dt.timezone.utc)
    start_dt = end_dt - _dt.timedelta(days=AC11_WINDOW_DAYS)
    start, end = start_dt.strftime("%Y-%m-%dT%H:%M:%SZ"), end_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    period = int((end_dt - start_dt).total_seconds())
    period -= period % 60
    problems = []
    overall, oerr = _cw_p95([{"Name": "LoadBalancer", "Value": lb_dim}], start, end, period,
                            "AC6 overall p95 TargetResponseTime (re-take)")
    t_overall = utcnow()
    if oerr:
        problems.append(f"overall: {oerr[:160]}")
    o_sample, o_p95, o_dp_problem = _cw_datapoint(overall)
    if o_dp_problem:
        problems.append(f"overall: {o_dp_problem}")
    per_tg = {}
    for tarn in tg_arns:
        tname = tarn.split("/")[-2] if tarn.count("/") >= 2 else tarn
        data, terr = _cw_p95([{"Name": "LoadBalancer", "Value": lb_dim},
                              {"Name": "TargetGroup", "Value": _tg_dim(tarn)}],
                             start, end, period, f"AC6 p95 TargetResponseTime tg={tname} (re-take)")
        t = utcnow()
        if terr:
            problems.append(f"{tname}: {terr[:160]}")
        tg_sample, tg_p95, tg_dp_problem = _cw_datapoint(data)
        if tg_dp_problem:
            problems.append(f"{tname}: {tg_dp_problem}")
        per_tg[tname] = {"target_group_arn": tarn, "sample_count": tg_sample, "p95_seconds": tg_p95,
                         "read_utc": t}
    say("instrument: cloudwatch GetMetricStatistics AWS/ApplicationELB TargetResponseTime (Statistics "
        "SampleCount, ExtendedStatistics p95), one CloudWatch period spanning the whole window, via "
        ".tools/aws; elbv2 DescribeLoadBalancers/DescribeTargetGroups resolve the dimensions -- OG-p-1's "
        "own OGP1-AC11 instrument, re-taken here on the resized host")
    say(f"vintage: {utcnow()}  load_balancer={arn}  target_groups={len(tg_arns)}")
    say(f"window: {start} .. {end} ({AC11_WINDOW_DAYS} days, period={period}s) -- OG-p-1's own window rule")
    say(f"denominator: 1 overall + {len(per_tg)} target group metric read(s)")
    say(f"overall: sample_count={o_sample} p95_seconds={o_p95} (read {t_overall})")
    for tname, v in per_tg.items():
        say(f"  target group {tname} ({v['target_group_arn']}): sample_count={v['sample_count']} "
            f"p95_seconds={v['p95_seconds']} (read {v['read_utc']})")
    prior = None
    ogp1_path = (ROOT / "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~2/BASELINE.json")
    if ogp1_path.is_file():
        prior_d = json.loads(ogp1_path.read_text(encoding="utf-8")).get("OGP1-AC11", {})
        prior = (prior_d.get("measurement") or {}).get("overall", {})
        say(f"compared against OG-p-1's pre-change reading: sample_count={prior.get('sample_count')} "
            f"p95_seconds={prior.get('p95_seconds')} (same instrument, same {AC11_WINDOW_DAYS}-day window "
            f"rule, an earlier trailing window)")
    ok = not problems and o_sample is not None
    measure = {"window_start": start, "window_end": end, "window_days": AC11_WINDOW_DAYS, "period_seconds": period,
               "load_balancer_arn": arn, "overall": {"sample_count": o_sample, "p95_seconds": o_p95,
               "read_utc": t_overall}, "per_target_group": per_tg, "prior_ogp1_ac11_overall": prior}
    return ok, "; ".join(problems), measure, 1 + len(per_tg)


CRITERIA = {"AC1": ac1, "AC2": ac2, "AC3": ac3, "AC4": ac4, "AC5": ac5, "AC6": ac6}


def main(argv: list) -> int:
    global CRIT
    if len(argv) < 2 or argv[1] not in CRITERIA:
        print(f"usage: og_i4.py AC<n> [--record]   n in {sorted(CRITERIA)}")
        return 2
    crit = argv[1]
    record = "--record" in argv[2:]
    CRIT = crit
    try:
        ok, reason, measure, denom = CRITERIA[crit]()
    except Exception as e:  # measurement failure is itself the reported reason, never swallowed
        print(f"ERROR: {type(e).__name__}: {e}")
        print(f"VERDICT: FAIL-OGI4-{crit} {type(e).__name__}: {e}")
        return 1
    if record and crit == "AC6":
        prev = {}
        if OGI4_BASELINE.is_file():
            prev = json.loads(OGI4_BASELINE.read_text(encoding="utf-8"))
        prev[f"OGI4-{crit}"] = {"denominator": denom, "measured_utc": utcnow(), "measurement": measure,
                                 "printed": list(LINES), "verdict": f"VERDICT: {'PASS' if ok else 'FAIL'}-OGI4-{crit}"}
        OGI4_BASELINE.write_text(json.dumps(prev, indent=1, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    if ok:
        print(f"VERDICT: PASS-OGI4-{crit}")
        return 0
    print(f"VERDICT: FAIL-OGI4-{crit} {reason}")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
