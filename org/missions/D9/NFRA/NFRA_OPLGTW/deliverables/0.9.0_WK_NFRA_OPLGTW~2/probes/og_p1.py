#!/usr/bin/env python3
"""OG-p-1 -- deployed parity and the pre-change baseline (NFRA_OPLGTW.TO-OG-p-1). READ ONLY.

Usage:
    og_p1.py AC<n> [--record]      measure criterion OGP1-AC<n>; print measurement, vintage, denominator,
                                   then exactly one line  VERDICT: PASS-OGP1-AC<n> | FAIL-OGP1-AC<n> <reason>
    og_p1.py render-md             render BASELINE.md from BASELINE.json (no AWS call)

--record writes this run's measurement into BASELINE.json under key OGP1-AC<n>; without it the probe only
prints, so a verifier re-run never rewrites the recorded baseline.

EVERY AWS call goes through aws() below, which runs the workspace shim `.tools/aws` (CLI v1) and appends one
row per call to command_log.jsonl beside this probe's deliverables folder: UTC time, service, CLI operation,
API operation, rc, the criterion that made it. AC13 reads that log. No other code path calls AWS.

Host reads use SSM (send-command with AWS-RunShellScript, then get-command-invocation), as the task order
names. Every host script below is read-only: it reads files, /proc, /sys and systemd state and writes
nothing. It never reads the Gateway's .env or any key file, and never prints an audit record's user or args.

No secret enters the output: the OIDC client id is reduced to a digest, policy documents to their
statements' Effect/Action/Resource plus condition KEYS and a sha256 of the canonical document.
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
from pathlib import Path

REGION = "us-east-1"
SERVICE_KEY = "opal-gateway"
BUCKET = "opal-data-assets"
GATEWAY_ROLE = "opal-gateway-role"
ABSENT_ROLES = ("opal-mcp-emp-menachem-schwab-read", "opal-mcp-schwab-catalog-read")
ABSENT_TABLE = "opal-gateway-access-state"
ALB_NAME = "opal-gateway"
# Extended per the RE-HAND's hand-off facts ("GetItem/Query/Scan are read verbs"): AC12's OAuth client
# inventory reads the access-state table with a Scan (no GSI on record_type exists to Query it), so
# "Scan"/"Query" join the set AC13 grades every AWS call against. GetItem already matches "Get".
READ_VERBS = ("Describe", "Get", "List", "Head", "Scan", "Query")

# RECORDED values the task order gives as "facts to re-ground, not to trust" (certified L4 rectangle,
# workflows/atom_decomposition/runs/nfra-oplgtw/20260914T1919Z/rectangle.final.certified.json). They are
# compared against, never used as a measurement.
RECORDED = {
    "alb_arn": "arn:aws:elasticloadbalancing:us-east-1:313476888478:loadbalancer/app/opal-gateway/89166a68f337e5a4",
    "idle_timeout_seconds": "60",
    "versioning": "Enabled",
    "sse": "AES256",
    "notification_id": "advi-49f-silver-complete-accelerator",
}

HERE = Path(__file__).resolve()
DELIV = HERE.parents[1]
CMDLOG = DELIV / "command_log.jsonl"
BASELINE = DELIV / "BASELINE.json"
BASELINE_MD = DELIV / "BASELINE.md"


def _root() -> Path:
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=str(HERE.parent),
                         capture_output=True, text=True, check=True)
    return Path(out.stdout.strip())


ROOT = _root()
sys.path.insert(0, str(ROOT / ".tools"))
from msys_argv_guard import msys_safe_run  # noqa: E402

CRIT = "?"
LINES: list = []
LOCK = ROOT / ".scratch" / "og_p1" / "write.lock"


class _Lock:
    """Exclusive create-lock so parallel criterion runs never interleave a command-log or BASELINE write."""

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


def canon_digest(obj) -> str:
    return sha256_bytes(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def _api_op(cli_op: str) -> str:
    return "".join(p[:1].upper() + p[1:] for p in cli_op.split("-"))


def aws(service: str, cli_op: str, *args: str, note: str = ""):
    """One AWS CLI call through .tools/aws. Returns (parsed_json_or_None, error_text_or_None, rc)."""
    argv = [".tools/aws", service, cli_op, *args, "--region", REGION, "--output", "json"]
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"  # the shim's cp1252 truncation trap
    started = utcnow()
    r = msys_safe_run(argv, cwd=str(ROOT), env=env, capture_output=True, timeout=90)
    row = {
        "ts": started, "serial": os.environ.get("OPAL_AGENT_SERIAL", ""), "criterion": CRIT,
        "service": service, "cli_op": cli_op, "api_op": _api_op(cli_op), "rc": r.returncode,
        "instrument": ".tools/aws (AWS CLI v1) via msys_safe_run", "note": note,
    }
    with _Lock(), open(CMDLOG, "a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(row, separators=(",", ":")) + "\n")
    out = r.stdout.decode("utf-8")  # strict: a truncated or mis-encoded payload raises, never shrinks
    err = r.stderr.decode("utf-8", errors="replace")
    if r.returncode != 0:
        return None, err.strip() or f"rc={r.returncode}", r.returncode
    return (json.loads(out) if out.strip() else {}), None, 0


def manifest() -> dict:
    d = json.loads((ROOT / "infra/aws/ec2/EC2_MANIFEST.json").read_text(encoding="utf-8"))
    return d["services"][SERVICE_KEY]


# ----------------------------------------------------------------------------------------------- SSM
SSM_LIMIT = 24000  # get-command-invocation truncates StandardOutputContent at 24,000 characters
END = "__OGP1_END__"


def ssm_read(script: str, label: str) -> tuple:
    """Run a READ-ONLY shell script on the Gateway host. Returns (stdout, meta) or raises."""
    inst = manifest()["instance_id"]
    lines = script.strip("\n").split("\n") + [f"echo {END}"]
    params = json.dumps({"commands": lines, "executionTimeout": ["60"]})
    note = f"host read {label}; script sha256={sha256_bytes(chr(10).join(lines).encode())[:16]}"
    sent, err, _ = aws("ssm", "send-command", "--instance-ids", inst, "--document-name", "AWS-RunShellScript",
                       "--comment", f"OG-p-1 read-only {label}", "--parameters", params, note=note)
    if err:
        raise RuntimeError(f"send-command failed: {err[:300]}")
    cid = sent["Command"]["CommandId"]
    deadline = time.time() + 70
    inv = None
    while time.time() < deadline:
        time.sleep(2)
        inv, err, _ = aws("ssm", "get-command-invocation", "--command-id", cid, "--instance-id", inst,
                          note=f"poll {label}")
        if err:
            if "InvocationDoesNotExist" in err:
                continue
            raise RuntimeError(f"get-command-invocation failed: {err[:300]}")
        if inv.get("Status") in ("Success", "Failed", "Cancelled", "TimedOut", "Undeliverable", "Terminated"):
            break
    if not inv or inv.get("Status") != "Success":
        raise RuntimeError(f"ssm {cid} status={inv and inv.get('Status')}")
    out = inv.get("StandardOutputContent", "")
    meta = {"command_id": cid, "instance_id": inst, "status": inv["Status"],
            "executed_utc": inv.get("ExecutionEndDateTime", ""), "stdout_chars": len(out),
            "complete": END in out and len(out) < SSM_LIMIT}
    if not meta["complete"]:
        raise RuntimeError(f"ssm {cid} output incomplete ({len(out)} chars, end marker "
                           f"{'present' if END in out else 'ABSENT'})")
    return out.split(END)[0], meta


def sections(out: str) -> dict:
    """Split host output on '### name' headers."""
    res: dict = {}
    cur = "_"
    for line in out.splitlines():
        if line.startswith("### "):
            cur = line[4:].strip()
            res[cur] = []
        else:
            res.setdefault(cur, []).append(line)
    return res


# ------------------------------------------------------------------------------------------- criteria
def _ac1_script(remote: str) -> str:
    """The exact read-only host script AC1 has always sent (extracted so AC13 can regenerate and grade
    it byte-for-byte without touching AC1 itself; AC1 is not re-run this round)."""
    return f"""
cd {remote} || exit 3
echo "### unit"
systemctl show opal-gateway -p MainPID -p ActiveEnterTimestamp --no-pager
PID=$(systemctl show opal-gateway -p MainPID --value)
echo "### pidstart"
stat -c %Y /proc/$PID 2>&1
echo "### files"
find app deploy requirements.txt identity_tool_allowlist.txt -type f ! -path '*/__pycache__/*' ! -name '*.pyc' | LC_ALL=C sort | while IFS= read -r f; do printf '%s %s %s\\n' "$(sha256sum < "$f" | cut -c1-64)" "$(stat -c %Y "$f")" "$f"; done
"""


def ac1(commit_override: str = "") -> tuple:
    m = manifest()
    commit = commit_override or m["deployed_commit"]
    src = m["source_path"].rstrip("/")
    remote = m["remote_path"].rstrip("/")
    # the deploy artifact's member set: deploy-to-ec2.sh tar -C <src> app deploy requirements.txt
    # identity_tool_allowlist.txt, excluding __pycache__ (and .env/audit.jsonl/*.log/.token_cache/infra)
    roots = ["app", "deploy", "requirements.txt", "identity_tool_allowlist.txt"]
    ls = subprocess.run(["git", "ls-tree", "-r", commit, "--", *[f"{src}/{r}" for r in roots]],
                        cwd=str(ROOT), capture_output=True, text=True, check=True).stdout
    tree: dict = {}
    excl = re.compile(r"(^|/)(__pycache__|infra)(/|$)|\.log$|(^|/)(\.env|audit\.jsonl|\.token_cache)$")
    for line in ls.splitlines():
        meta, path = line.split("\t", 1)
        mode, typ, blob = meta.split()
        rel = path[len(src) + 1:]
        if typ != "blob" or excl.search(rel):
            continue
        data = subprocess.run(["git", "cat-file", "blob", blob], cwd=str(ROOT), capture_output=True,
                              check=True).stdout
        tree[rel] = sha256_bytes(data)
    script = _ac1_script(remote)
    out, meta = ssm_read(script, "AC1 digests")
    sec = sections(out)
    host: dict = {}
    mtimes: dict = {}
    for line in sec.get("files", []):
        parts = line.split(" ", 2)
        if len(parts) == 3 and re.fullmatch(r"[0-9a-f]{64}", parts[0]):
            host[parts[2]] = parts[0]
            mtimes[parts[2]] = int(parts[1])
    pidstart = None
    for line in sec.get("pidstart", []):
        if line.strip().isdigit():
            pidstart = int(line.strip())
    union = sorted(set(tree) | set(host))
    match = [p for p in union if p in tree and p in host and tree[p] == host[p]]
    differ = [p for p in union if p in tree and p in host and tree[p] != host[p]]
    host_only = [p for p in union if p not in tree]
    tree_only = [p for p in union if p not in host]
    newer = sorted(p for p, t in mtimes.items() if pidstart and t > pidstart)
    say(f"instrument: SSM AWS-RunShellScript sha256sum on {meta['instance_id']} ({remote}) vs git blob sha256 "
        f"at {commit} ({src}); ssm {meta['command_id']} {meta['status']} at {meta['executed_utc']}")
    say(f"vintage: {utcnow()}  deployed_commit(manifest)={m['deployed_commit']} compared_commit={commit}")
    say(f"denominator: {len(union)} files (tree {len(tree)}, host {len(host)})")
    say(f"match={len(match)} digest_mismatch={len(differ)} host_only={len(host_only)} tree_only={len(tree_only)}")
    for p in differ:
        say(f"  MISMATCH {p} host={host[p][:16]} tree={tree[p][:16]}")
    for p in host_only:
        say(f"  HOST-ONLY {p} host={host[p][:16]}")
    for p in tree_only:
        say(f"  TREE-ONLY {p} tree={tree[p][:16]}")
    say(f"running process start (epoch, /proc/<MainPID> ctime)={pidstart}; files modified after it: {len(newer)}"
        + (f" {newer}" if newer else ""))
    measure = {"compared_commit": commit, "manifest_deployed_commit": m["deployed_commit"],
               "instance_id": meta["instance_id"], "ssm_command_id": meta["command_id"],
               "denominator": len(union), "tree_files": len(tree), "host_files": len(host),
               "match": len(match), "digest_mismatch": differ, "host_only": host_only, "tree_only": tree_only,
               "process_start_epoch": pidstart, "files_newer_than_process": newer,
               "host_sha256": host}
    ok = bool(tree) and bool(host)
    return ok, ("" if ok else "comparison did not complete (empty side)"), measure, len(union)


def _ac2_script(remote: str) -> str:
    """AC2's read-only host script, extracted for AC13's regeneration (AC2 is not re-run this round)."""
    return f"""
echo "### dmi"
cat /sys/devices/virtual/dmi/id/product_name 2>&1
cat /sys/devices/virtual/dmi/id/sys_vendor 2>&1
echo "### cloudinit"
grep -o '"instance[-_]type": *"[^"]*"' /run/cloud-init/instance-data.json 2>&1 | sort -u
echo "### arch"
uname -m
echo "### kernel"
uname -r
echo "### nproc"
nproc
echo "### memtotal"
grep MemTotal /proc/meminfo
echo "### unit"
systemctl show opal-gateway -p MainPID -p ActiveState -p SubState -p ActiveEnterTimestamp -p NRestarts -p ExecStart --no-pager
echo "### ps"
ps -eo pid=,ppid=,etimes=,rss=,comm=
echo "### mainargs"
PID=$(systemctl show opal-gateway -p MainPID --value)
ps -o args= -p $PID
echo "### children"
ps -o pid=,args= --ppid $PID
echo "### pyv"
PYTHONDONTWRITEBYTECODE=1 {remote}/.venv/bin/python -V 2>&1
echo "### pyvenv"
cat {remote}/.venv/pyvenv.cfg
echo "### distinfo"
ls -1d {remote}/.venv/lib/python*/site-packages/*.dist-info | sed 's#.*/##'
"""


def ac2() -> tuple:
    remote = manifest()["remote_path"].rstrip("/")
    script = _ac2_script(remote)
    out, meta = ssm_read(script, "AC2 host shape")
    sec = sections(out)
    dmi = [x.strip() for x in sec.get("dmi", []) if x.strip()]
    ci = [x.strip() for x in sec.get("cloudinit", []) if x.strip()]
    unit = dict(line.split("=", 1) for line in sec.get("unit", []) if "=" in line)
    mainpid = int(unit.get("MainPID", "0") or 0)
    procs = []
    for line in sec.get("ps", []):
        f = line.split(None, 4)
        if len(f) == 5 and f[0].isdigit():
            procs.append({"pid": int(f[0]), "ppid": int(f[1]), "etimes": int(f[2]), "rss_kb": int(f[3]),
                          "comm": f[4]})
    desc = {mainpid}
    changed = True
    while changed:
        changed = False
        for p in procs:
            if p["ppid"] in desc and p["pid"] not in desc:
                desc.add(p["pid"])
                changed = True
    tree = [p for p in procs if p["pid"] in desc]
    mainargs = " ".join(sec.get("mainargs", [])).strip()
    wm = re.search(r"--workers\s+(\d+)", mainargs)
    execstart = unit.get("ExecStart", "")
    wx = re.search(r"--workers\s+(\d+)", execstart)
    pyv = " ".join(sec.get("pyv", [])).strip()
    pyvenv = {k.strip(): v.strip() for k, v in (line.split("=", 1) for line in sec.get("pyvenv", []) if "=" in line)}
    pkgs = []
    for d in sec.get("distinfo", []):
        d = d.strip()
        mm = re.fullmatch(r"(.+?)-([^-]+)\.dist-info", d)
        if mm:
            pkgs.append(f"{mm.group(1)}=={mm.group(2)}")
    pkgs.sort(key=str.lower)
    desc_api, err, _ = aws("ec2", "describe-instances", "--instance-ids", meta["instance_id"],
                           note="AC2 cross-instrument: EC2 API view of the same instance")
    api = {}
    if desc_api:
        i = desc_api["Reservations"][0]["Instances"][0]
        api = {"InstanceType": i.get("InstanceType"), "Architecture": i.get("Architecture"),
               "State": i.get("State", {}).get("Name"), "LaunchTime": i.get("LaunchTime"),
               "ImageId": i.get("ImageId")}
    inst_type_host = dmi[0] if dmi else ""
    ci_type = ""
    for x in ci:
        mm = re.search(r'"([^"]*)"\s*$', x)
        if mm:
            ci_type = mm.group(1)
    arch = " ".join(sec.get("arch", [])).strip()
    say(f"instrument: SSM AWS-RunShellScript on {meta['instance_id']} (ssm {meta['command_id']} at "
        f"{meta['executed_utc']}); cross-check ec2 DescribeInstances")
    say(f"vintage: {utcnow()}")
    say(f"instance_type host DMI product_name={inst_type_host!r} cloud-init cache={ci_type!r} | EC2 API={api.get('InstanceType')!r}")
    say(f"architecture host uname -m={arch!r} | EC2 API={api.get('Architecture')!r}")
    say(f"kernel={' '.join(sec.get('kernel', [])).strip()} nproc={' '.join(sec.get('nproc', [])).strip()} "
        f"{' '.join(sec.get('memtotal', [])).strip()}")
    say(f"unit: ActiveState={unit.get('ActiveState')} SubState={unit.get('SubState')} MainPID={mainpid} "
        f"ActiveEnterTimestamp={unit.get('ActiveEnterTimestamp')} NRestarts={unit.get('NRestarts')}")
    say(f"process tree under MainPID: {len(tree)} process(es): "
        + "; ".join(f"pid={p['pid']} ppid={p['ppid']} comm={p['comm']} rss_kb={p['rss_kb']} etimes={p['etimes']}" for p in tree))
    say(f"worker count: running argv --workers={wm.group(1) if wm else None}, unit ExecStart --workers="
        f"{wx.group(1) if wx else None}, child processes of MainPID={len(tree) - 1}")
    say(f"main argv: {mainargs}")
    say(f"python: {pyv}; pyvenv.cfg version={pyvenv.get('version') or pyvenv.get('version_info')}")
    say(f"installed packages (dist-info dirs in the service venv): denominator {len(pkgs)}")
    for p in pkgs:
        say(f"  {p}")
    measure = {"instance_id": meta["instance_id"], "ssm_command_id": meta["command_id"],
               "instance_type_host_dmi": inst_type_host, "instance_type_host_cloudinit": ci_type,
               "instance_type_ec2_api": api.get("InstanceType"), "architecture_host": arch,
               "architecture_ec2_api": api.get("Architecture"), "ec2_api": api,
               "kernel": " ".join(sec.get("kernel", [])).strip(), "nproc": " ".join(sec.get("nproc", [])).strip(),
               "memtotal": " ".join(sec.get("memtotal", [])).strip(), "unit": unit,
               "process_tree": tree, "workers_argv": wm.group(1) if wm else None,
               "workers_execstart": wx.group(1) if wx else None, "main_argv": mainargs,
               "python_version": pyv, "pyvenv_cfg": pyvenv, "packages": pkgs, "package_count": len(pkgs)}
    missing = [k for k, v in (("instance_type", inst_type_host or ci_type), ("architecture", arch),
                              ("process", mainpid and tree), ("worker_count", wm or wx),
                              ("python", pyv), ("packages", pkgs)) if not v]
    return (not missing), ("unread on host: " + ",".join(missing) if missing else ""), measure, len(pkgs)


def _oidc_sanitize(action: dict) -> dict:
    a = json.loads(json.dumps(action))
    cfg = a.get("AuthenticateOidcConfig")
    if cfg:
        if "ClientId" in cfg:
            cfg["ClientId"] = "sha256:" + sha256_bytes(cfg["ClientId"].encode())[:16]
        cfg.pop("ClientSecret", None)
    return a


def ac3() -> tuple:
    lbs, err, _ = aws("elbv2", "describe-load-balancers", "--names", ALB_NAME, note="AC3 resolve ALB by name")
    if err:
        return False, f"describe-load-balancers: {err[:200]}", {}, 0
    lb = lbs["LoadBalancers"][0]
    arn = lb["LoadBalancerArn"]
    t_lb = utcnow()
    attrs, err, _ = aws("elbv2", "describe-load-balancer-attributes", "--load-balancer-arn", arn, note="AC3")
    t_attr = utcnow()
    at = {a["Key"]: a["Value"] for a in (attrs or {}).get("Attributes", [])}
    lis, err2, _ = aws("elbv2", "describe-listeners", "--load-balancer-arn", arn, note="AC3")
    t_lis = utcnow()
    listeners = []
    nrules = 0
    for li in (lis or {}).get("Listeners", []):
        rules, e3, _ = aws("elbv2", "describe-rules", "--listener-arn", li["ListenerArn"], note="AC3")
        t_r = utcnow()
        rr = []
        for r in (rules or {}).get("Rules", []):
            rr.append({"RuleArn": r["RuleArn"], "Priority": r["Priority"], "IsDefault": r.get("IsDefault"),
                       "Conditions": r.get("Conditions", []),
                       "Actions": [_oidc_sanitize(a) for a in r.get("Actions", [])], "read_utc": t_r})
        nrules += len(rr)
        listeners.append({"ListenerArn": li["ListenerArn"], "Port": li["Port"], "Protocol": li["Protocol"],
                          "SslPolicy": li.get("SslPolicy"), "read_utc": t_lis,
                          "DefaultActions": [_oidc_sanitize(a) for a in li.get("DefaultActions", [])],
                          "rules": rr, "rules_error": e3})
    waf, e4, _ = aws("wafv2", "get-web-acl-for-resource", "--resource-arn", arn, note="AC3 WAF association")
    t_waf = utcnow()
    webacl = (waf or {}).get("WebACL")
    waf_rec = {"read_utc": t_waf, "resource_arn": arn, "error": e4,
               "WebACL": ({"Name": webacl.get("Name"), "ARN": webacl.get("ARN"), "Id": webacl.get("Id"),
                           "DefaultAction": webacl.get("DefaultAction"),
                           "Rules": [{"Name": x.get("Name"), "Priority": x.get("Priority")} for x in webacl.get("Rules", [])]}
                          if webacl else None)}
    idle = at.get("idle_timeout.timeout_seconds")
    say("instrument: elbv2 DescribeLoadBalancers/DescribeLoadBalancerAttributes/DescribeListeners/DescribeRules, "
        "wafv2 GetWebACLForResource via .tools/aws")
    say(f"vintage: {utcnow()}")
    say(f"load balancer {arn} (read {t_lb}) scheme={lb.get('Scheme')} state={lb.get('State', {}).get('Code')} "
        f"| recorded ARN {'MATCH' if arn == RECORDED['alb_arn'] else 'DIFFERS'}")
    say(f"idle_timeout.timeout_seconds={idle} (read {t_attr}, resource {arn}) | recorded "
        f"{RECORDED['idle_timeout_seconds']} {'MATCH' if idle == RECORDED['idle_timeout_seconds'] else 'DIFFERS'}")
    say(f"denominator: {len(listeners)} listener(s), {nrules} rule(s)")
    oidc_default = []
    for li in listeners:
        say(f"listener {li['ListenerArn']} {li['Protocol']}:{li['Port']} (read {li['read_utc']}) default actions: "
            + ", ".join(a["Type"] for a in li["DefaultActions"]))
        for r in sorted(li["rules"], key=lambda x: (x["Priority"] == "default", int(x["Priority"]) if x["Priority"].isdigit() else 0)):
            conds = "; ".join(f"{c.get('Field')}={c.get('Values') or c.get('PathPatternConfig', {}).get('Values') or c.get('HostHeaderConfig', {}).get('Values')}" for c in r["Conditions"])
            acts = ", ".join(a["Type"] for a in r["Actions"])
            say(f"  rule prio={r['Priority']} {r['RuleArn']} (read {r['read_utc']}) if [{conds}] -> {acts}")
            if r["IsDefault"]:
                for a in r["Actions"]:
                    if a["Type"] == "authenticate-oidc":
                        c = a.get("AuthenticateOidcConfig", {})
                        oidc_default.append({"listener": li["ListenerArn"], "Issuer": c.get("Issuer"),
                                             "ClientId": c.get("ClientId"),
                                             "OnUnauthenticatedRequest": c.get("OnUnauthenticatedRequest"),
                                             "Scope": c.get("Scope"), "SessionTimeout": c.get("SessionTimeout")})
    for o in oidc_default:
        say(f"default browser OIDC action on {o['listener']}: issuer={o['Issuer']} client_id={o['ClientId']} "
            f"on_unauthenticated={o['OnUnauthenticatedRequest']} scope={o['Scope']} session_timeout={o['SessionTimeout']}")
    if webacl:
        say(f"WAF association (read {t_waf}, resource {arn}): {webacl.get('Name')} {webacl.get('ARN')} "
            f"rules={len(webacl.get('Rules', []))}")
    else:
        say(f"WAF association (read {t_waf}, resource {arn}): NONE (GetWebACLForResource returned no WebACL)"
            + (f" error={e4[:160]}" if e4 else ""))
    measure = {"load_balancer_arn": arn, "read_utc": t_lb, "recorded_arn_match": arn == RECORDED["alb_arn"],
               "attributes": at, "attributes_read_utc": t_attr, "idle_timeout_seconds": idle,
               "listeners": listeners, "default_oidc": oidc_default, "waf": waf_rec,
               "listener_count": len(listeners), "rule_count": nrules}
    problems = []
    if idle is None:
        problems.append("idle_timeout unread")
    if not listeners:
        problems.append("no listener read")
    if any(li["rules_error"] for li in listeners):
        problems.append("a describe-rules call failed")
    if e4 and "WAFNonexistentItemException" not in e4:
        problems.append("WAF association unread")
    if not oidc_default:
        problems.append("no default authenticate-oidc action found")
    return (not problems), "; ".join(problems), measure, len(listeners) + nrules


def ac4() -> tuple:
    reads = {}
    for op in ("get-bucket-versioning", "get-bucket-encryption", "get-public-access-block",
               "get-bucket-policy-status"):
        data, err, _ = aws("s3api", op, "--bucket", BUCKET, note="AC4")
        reads[op] = {"read_utc": utcnow(), "data": data, "error": err}
    ver = (reads["get-bucket-versioning"]["data"] or {}).get("Status")
    rules = ((reads["get-bucket-encryption"]["data"] or {}).get("ServerSideEncryptionConfiguration") or {}).get("Rules", [])
    sse = [r.get("ApplyServerSideEncryptionByDefault", {}).get("SSEAlgorithm") for r in rules]
    kms = [r.get("ApplyServerSideEncryptionByDefault", {}).get("KMSMasterKeyID") for r in rules]
    bke = [r.get("BucketKeyEnabled") for r in rules]
    pab = (reads["get-public-access-block"]["data"] or {}).get("PublicAccessBlockConfiguration") or {}
    flags = {k: pab.get(k) for k in ("BlockPublicAcls", "IgnorePublicAcls", "BlockPublicPolicy", "RestrictPublicBuckets")}
    ps = (reads["get-bucket-policy-status"]["data"] or {}).get("PolicyStatus")
    say("instrument: s3api GetBucketVersioning/GetBucketEncryption/GetPublicAccessBlock/GetBucketPolicyStatus via .tools/aws")
    say(f"vintage: {utcnow()}  bucket={BUCKET}")
    say("denominator: 4 reads, 7 values (versioning, encryption, 4 public-access-block flags, policy status)")
    say(f"versioning={ver} (read {reads['get-bucket-versioning']['read_utc']}) | recorded Enabled "
        f"{'MATCH' if ver == RECORDED['versioning'] else 'DIFFERS'}")
    say(f"default encryption SSEAlgorithm={sse} KMSMasterKeyID={kms} BucketKeyEnabled={bke} "
        f"(read {reads['get-bucket-encryption']['read_utc']}) | recorded AES256 "
        f"{'MATCH' if sse == [RECORDED['sse']] else 'DIFFERS'}")
    say(f"public access block {flags} (read {reads['get-public-access-block']['read_utc']}) | recorded all four true "
        f"{'MATCH' if all(v is True for v in flags.values()) else 'DIFFERS'}")
    say(f"policy status {ps} (read {reads['get-bucket-policy-status']['read_utc']})"
        + (f" error={reads['get-bucket-policy-status']['error'][:160]}" if reads['get-bucket-policy-status']['error'] else ""))
    measure = {"bucket": BUCKET, "versioning": ver, "sse_algorithm": sse, "kms_key": kms, "bucket_key_enabled": bke,
               "public_access_block": flags, "policy_status": ps,
               "read_utc": {k: v["read_utc"] for k, v in reads.items()},
               "errors": {k: v["error"] for k, v in reads.items() if v["error"]}}
    unread = [k for k, v in reads.items() if v["error"]]
    return (not unread), ("unread: " + ",".join(unread) if unread else ""), measure, 7


def _stmt_summary(doc: dict) -> list:
    st = doc.get("Statement", [])
    if isinstance(st, dict):
        st = [st]
    out = []
    for s in st:
        out.append({"Sid": s.get("Sid"), "Effect": s.get("Effect"),
                    "Principal": s.get("Principal"), "Action": s.get("Action") or s.get("NotAction"),
                    "Resource": s.get("Resource") or s.get("NotResource"),
                    "ConditionKeys": sorted(f"{op}:{k}" for op, kv in (s.get("Condition") or {}).items() for k in kv)})
    return out


def ac5() -> tuple:
    role, err, _ = aws("iam", "get-role", "--role-name", GATEWAY_ROLE, note="AC5 trust")
    if err:
        return False, f"get-role: {err[:200]}", {}, 0
    r = role["Role"]
    trust = r["AssumeRolePolicyDocument"]
    t_role = utcnow()
    inl, e1, _ = aws("iam", "list-role-policies", "--role-name", GATEWAY_ROLE, note="AC5")
    att, e2, _ = aws("iam", "list-attached-role-policies", "--role-name", GATEWAY_ROLE, note="AC5")
    inline = []
    for name in (inl or {}).get("PolicyNames", []):
        p, e, _ = aws("iam", "get-role-policy", "--role-name", GATEWAY_ROLE, "--policy-name", name, note="AC5")
        doc = (p or {}).get("PolicyDocument") or {}
        inline.append({"name": name, "read_utc": utcnow(), "error": e, "sha256": canon_digest(doc) if doc else None,
                       "statements": _stmt_summary(doc)})
    attached = []
    for a in (att or {}).get("AttachedPolicies", []):
        pol, e, _ = aws("iam", "get-policy", "--policy-arn", a["PolicyArn"], note="AC5")
        ver = (pol or {}).get("Policy", {}).get("DefaultVersionId")
        doc = {}
        e5 = None
        if ver:
            pv, e5, _ = aws("iam", "get-policy-version", "--policy-arn", a["PolicyArn"], "--version-id", ver, note="AC5")
            doc = (pv or {}).get("PolicyVersion", {}).get("Document") or {}
        attached.append({"name": a["PolicyName"], "arn": a["PolicyArn"], "default_version": ver,
                         "read_utc": utcnow(), "error": e or e5, "sha256": canon_digest(doc) if doc else None,
                         "statements": _stmt_summary(doc)})
    say("instrument: iam GetRole/ListRolePolicies/GetRolePolicy/ListAttachedRolePolicies/GetPolicy/GetPolicyVersion via .tools/aws")
    say(f"vintage: {utcnow()}  role={r['Arn']} (read {t_role}) created={r.get('CreateDate')} "
        f"permissions_boundary={r.get('PermissionsBoundary')} max_session={r.get('MaxSessionDuration')}")
    say(f"denominator: 1 trust document + {len(inline)} inline + {len(attached)} attached policies")
    ts = _stmt_summary(trust)
    say(f"trust sha256={canon_digest(trust)[:16]} statements={len(ts)}: "
        + "; ".join(f"{s['Effect']} {s['Action']} principal={s['Principal']} cond={s['ConditionKeys']}" for s in ts))
    for p in inline:
        say(f"inline {p['name']} sha256={(p['sha256'] or '')[:16]} statements={len(p['statements'])}"
            + (f" ERROR {p['error'][:120]}" if p["error"] else ""))
        for s in p["statements"]:
            say(f"    {s['Effect']} {s['Action']} on {s['Resource']} cond={s['ConditionKeys']}")
    for p in attached:
        say(f"attached {p['arn']} v={p['default_version']} sha256={(p['sha256'] or '')[:16]} statements={len(p['statements'])}"
            + (f" ERROR {p['error'][:120]}" if p["error"] else ""))
        for s in p["statements"]:
            say(f"    {s['Effect']} {s['Action']} on {s['Resource']} cond={s['ConditionKeys']}")
    measure = {"role_arn": r["Arn"], "read_utc": t_role, "permissions_boundary": r.get("PermissionsBoundary"),
               "trust_sha256": canon_digest(trust), "trust_statements": ts, "inline": inline, "attached": attached}
    bad = [p["name"] for p in inline + attached if p["error"] or not p["sha256"]]
    if e1 or e2:
        bad.append("list call failed")
    return (not bad), ("unread: " + ",".join(bad) if bad else ""), measure, 1 + len(inline) + len(attached)


def ac6() -> tuple:
    names = list(ABSENT_ROLES)
    mut = os.environ.get("OGP1_MUTANT_ROLE")
    if mut:
        names[0] = mut
        say(f"MUTANT CONTROL: first role name replaced by {mut!r} (OGP1_MUTANT_ROLE)")
    res = {}
    for n in names:
        data, err, rc = aws("iam", "get-role", "--role-name", n, note="AC6 absence")
        res[n] = {"read_utc": utcnow(), "rc": rc,
                  "result": "NoSuchEntity" if err and "NoSuchEntity" in err else ("EXISTS " + data["Role"]["Arn"] if data else f"ERROR {err[:160]}")}
    say("instrument: iam GetRole via .tools/aws")
    say(f"vintage: {utcnow()}")
    say(f"denominator: {len(names)} role names")
    for n, v in res.items():
        say(f"GetRole {n}: {v['result']} (rc={v['rc']}, read {v['read_utc']})")
    not_absent = [n for n, v in res.items() if v["result"] != "NoSuchEntity"]
    return (not not_absent), ("not NoSuchEntity: " + ",".join(not_absent) if not_absent else ""), {"roles": res}, len(names)


def ac7() -> tuple:
    data, err, rc = aws("dynamodb", "describe-table", "--table-name", ABSENT_TABLE, note="AC7 absence")
    t = utcnow()
    result = "ResourceNotFound" if err and "ResourceNotFoundException" in err else (
        "EXISTS " + data["Table"]["TableArn"] if data else f"ERROR {(err or '')[:160]}")
    say("instrument: dynamodb DescribeTable via .tools/aws")
    say(f"vintage: {t}")
    say("denominator: 1 table name")
    say(f"DescribeTable {ABSENT_TABLE}: {result} (rc={rc})")
    return result == "ResourceNotFound", ("" if result == "ResourceNotFound" else result), {"table": ABSENT_TABLE, "result": result, "read_utc": t, "rc": rc}, 1


def ac8() -> tuple:
    top, err, _ = aws("s3api", "list-objects-v2", "--bucket", BUCKET, "--prefix", "schwab/", "--delimiter", "/",
                      note="AC8 enumerate masters")
    if err:
        return False, f"list masters: {err[:200]}", {}, 0
    masters = sorted(p["Prefix"].split("/")[1] for p in (top or {}).get("CommonPrefixes", []))
    scratch = ROOT / ".scratch" / "og_p1"
    scratch.mkdir(parents=True, exist_ok=True)
    per = {}
    for m in masters:
        pre = f"schwab/{m}/meta/complete/"
        lst, e, _ = aws("s3api", "list-objects-v2", "--bucket", BUCKET, "--prefix", pre, note="AC8 markers")
        objs = (lst or {}).get("Contents", []) if not e else []
        t = utcnow()
        rec = {"prefix": pre, "count": len(objs), "read_utc": t, "error": e}
        if objs:
            newest = max(objs, key=lambda o: (o["LastModified"], o["Key"]))
            newest_by_name = max(o["Key"] for o in objs)
            rec.update({"newest_key": newest["Key"], "newest_last_modified": newest["LastModified"],
                        "newest_key_by_name": newest_by_name, "newest_size": newest["Size"]})
            dest = scratch / f"marker_{m}.json"
            g, e2, _ = aws("s3api", "get-object", "--bucket", BUCKET, "--key", newest["Key"], str(dest),
                           note="AC8 read newest marker")
            if e2:
                rec["schema_error"] = e2[:200]
            else:
                body = json.loads(dest.read_text(encoding="utf-8"))
                rec["version_id"] = (g or {}).get("VersionId")
                rec["top_level_keys"] = sorted(body.keys()) if isinstance(body, dict) else type(body).__name__
                rec["schema_field"] = {k: body[k] for k in body if "schema" in k.lower()} if isinstance(body, dict) else {}
        per[m] = rec
    with_markers = [m for m in masters if per[m]["count"]]
    say("instrument: s3api ListObjectsV2 (auto-paginated) + GetObject of the newest marker via .tools/aws")
    say(f"vintage: {utcnow()}  bucket={BUCKET}")
    say(f"denominator: {len(masters)} master prefix(es) under schwab/, {len(with_markers)} with meta/complete/ objects")
    for m in masters:
        r = per[m]
        say(f"master {m}: count={r['count']} (read {r['read_utc']})"
            + (f" newest={r['newest_key']} last_modified={r['newest_last_modified']} newest_by_name={r['newest_key_by_name']}"
               f" schema_field={r.get('schema_field')} keys={r.get('top_level_keys')}" if r["count"] else "")
            + (f" ERROR {r['error'][:120]}" if r["error"] else ""))
    errs = [m for m in masters if per[m]["error"] or per[m].get("schema_error")]
    noschema = [m for m in with_markers if not per[m].get("schema_field")]
    problems = []
    if not with_markers:
        problems.append("no master carries meta/complete/ objects")
    if errs:
        problems.append("read error on " + ",".join(errs))
    if noschema:
        problems.append("no schema field in newest marker of " + ",".join(noschema))
    return (not problems), "; ".join(problems), {"masters": per}, len(masters)


def _prefix_covers(p: str) -> bool:
    """Can an object key of the form schwab/<master>/meta/complete/... also start with prefix p?"""
    if not p.startswith("schwab/"):
        return "schwab/".startswith(p)
    rest = p[len("schwab/"):]
    if "/" not in rest:
        return True
    _seg, tail = rest.split("/", 1)
    return "meta/complete/".startswith(tail) or tail.startswith("meta/complete/")


def ac9() -> tuple:
    cfg, err, _ = aws("s3api", "get-bucket-notification-configuration", "--bucket", BUCKET, note="AC9")
    t = utcnow()
    if err:
        return False, f"get-bucket-notification-configuration: {err[:200]}", {}, 0
    rows = []
    for kind, key, arnkey in (("lambda", "LambdaFunctionConfigurations", "LambdaFunctionArn"),
                              ("sqs", "QueueConfigurations", "QueueArn"),
                              ("sns", "TopicConfigurations", "TopicArn")):
        for c in cfg.get(key, []):
            fr = {x["Name"].lower(): x["Value"] for x in c.get("Filter", {}).get("Key", {}).get("FilterRules", [])}
            pre, suf = fr.get("prefix", ""), fr.get("suffix", "")
            created = any(e.startswith("s3:ObjectCreated") for e in c.get("Events", []))
            sample = "schwab/00000000/meta/complete/date=2026-01-01.json"
            covers = created and _prefix_covers(pre) and (suf == "" or sample.endswith(suf))
            rows.append({"kind": kind, "id": c.get("Id"), "target": c.get(arnkey), "events": c.get("Events"),
                         "prefix": pre, "suffix": suf, "object_created": created, "covers_meta_complete": covers})
    eb = cfg.get("EventBridgeConfiguration")
    eb_rules = []
    if eb is not None:
        lr, e2, _ = aws("events", "list-rules", note="AC9 EventBridge enabled on bucket: default-bus rules")
        for r in (lr or {}).get("Rules", []):
            pat = r.get("EventPattern") or ""
            if "aws.s3" in pat and BUCKET in pat and "Object Created" in pat:
                eb_rules.append({"name": r.get("Name"), "arn": r.get("Arn"), "state": r.get("State"),
                                 "pattern_sha256": sha256_bytes(pat.encode())[:16]})
    covering = [r for r in rows if r["covers_meta_complete"]]
    say("instrument: s3api GetBucketNotificationConfiguration via .tools/aws"
        + ("; events ListRules (bucket has EventBridge enabled)" if eb is not None else ""))
    say(f"vintage: {t}  bucket={BUCKET}")
    say(f"denominator: {len(rows)} notification configuration(s) "
        f"({sum(r['object_created'] for r in rows)} ObjectCreated); EventBridge enabled={eb is not None}")
    say(f"ObjectCreated consumers whose filter covers schwab/*/meta/complete/: {len(covering)}")
    for r in covering:
        say(f"  COVERS {r['kind']} id={r['id']} target={r['target']} events={r['events']} prefix={r['prefix']!r} suffix={r['suffix']!r}")
    if eb is not None:
        say(f"EventBridge default-bus rules matching aws.s3 + {BUCKET} + Object Created: {len(eb_rules)}")
        for r in eb_rules:
            say(f"  EB {r['name']} {r['arn']} state={r['state']}")
    rec = [r for r in rows if r["id"] == RECORDED["notification_id"]]
    say(f"recorded consumer {RECORDED['notification_id']}: {'PRESENT prefix=' + repr(rec[0]['prefix']) if rec else 'ABSENT'}")
    measure = {"read_utc": t, "configurations": rows, "covering": covering, "eventbridge_enabled": eb is not None,
               "eventbridge_rules": eb_rules}
    return True, "", measure, len(rows)


def _ac10_script() -> str:
    """AC10's read-only host script, extracted for AC13's regeneration (AC10 is not re-run this round)."""
    return """
PID=$(systemctl show opal-gateway -p MainPID --value)
echo "### unit"
systemctl show opal-gateway -p MainPID -p ActiveEnterTimestamp -p ControlGroup -p MemoryCurrent --no-pager
echo "### now"
date -u +%Y-%m-%dT%H:%M:%SZ
echo "### lstart"
ps -o lstart= -p $PID
echo "### procs"
for p in $PID $(ps -o pid= --ppid $PID); do printf 'pid=%s ' "$p"; grep -E '^(VmHWM|VmRSS):' /proc/$p/status | tr -s ' \\t' ' ' | tr '\\n' ' '; echo; done
echo "### cgpeak"
CG=$(systemctl show opal-gateway -p ControlGroup --value)
cat /sys/fs/cgroup$CG/memory.peak 2>&1
echo "### cgcurrent"
cat /sys/fs/cgroup$CG/memory.current 2>&1
"""


def ac10() -> tuple:
    script = _ac10_script()
    out, meta = ssm_read(script, "AC10 peak RSS")
    sec = sections(out)
    unit = dict(line.split("=", 1) for line in sec.get("unit", []) if "=" in line)
    procs = []
    for line in sec.get("procs", []):
        mm = re.search(r"pid=(\d+).*?VmHWM: (\d+) kB.*?VmRSS: (\d+) kB", line)
        if mm:
            procs.append({"pid": int(mm.group(1)), "VmHWM_kB": int(mm.group(2)), "VmRSS_kB": int(mm.group(3))})
    now = " ".join(sec.get("now", [])).strip()
    lstart = " ".join(sec.get("lstart", [])).strip()
    cgpeak = " ".join(sec.get("cgpeak", [])).strip()
    cgcur = " ".join(sec.get("cgcurrent", [])).strip()
    peak = max((p["VmHWM_kB"] for p in procs), default=None)
    say("instrument: /proc/<pid>/status VmHWM (kernel resident-set high-water mark since the process exec'd), "
        "read on the host by SSM; cgroup v2 memory.peak shown beside it (includes page cache, so it is NOT RSS)")
    say(f"vintage: {now} (host clock), ssm {meta['command_id']} at {meta['executed_utc']}")
    say(f"window: process start {unit.get('ActiveEnterTimestamp')} (ps lstart {lstart!r}) -> {now}")
    say(f"denominator: {len(procs)} process(es) in the service (MainPID + children)")
    for p in procs:
        say(f"  pid={p['pid']} VmHWM={p['VmHWM_kB']} kB ({p['VmHWM_kB'] / 1024:.1f} MiB) VmRSS={p['VmRSS_kB']} kB")
    say(f"peak RSS (max VmHWM) = {peak} kB" + (f" ({peak / 1024:.1f} MiB)" if peak else ""))
    say(f"cgroup {unit.get('ControlGroup')} memory.peak={cgpeak} memory.current={cgcur}")
    measure = {"instrument": "/proc/<pid>/status VmHWM", "window_start": unit.get("ActiveEnterTimestamp"),
               "window_start_lstart": lstart, "window_end": now, "processes": procs, "peak_rss_kB": peak,
               "cgroup": unit.get("ControlGroup"), "cgroup_memory_peak_bytes": cgpeak,
               "cgroup_memory_current_bytes": cgcur, "ssm_command_id": meta["command_id"]}
    return peak is not None, ("" if peak is not None else "VmHWM unread"), measure, len(procs)


# AC11/AC12/AC13 rebuilt per 1.0.0_SA_CTO ruling R-OG-2 (msg 97499 @d6583eab37; RULINGS_NFRA_OPLGTW_20260916.md)
# before this cold re-hand. AC1..AC10 above are UNCHANGED and NOT re-run; their script-building logic was
# factored out (_ac1_script/_ac2_script/_ac10_script) only so AC13 can regenerate and grade those calls'
# exact bytes without touching AC1/AC2/AC10 themselves.

DURATION_KEYS = ("duration", "duration_ms", "duration_s", "latency", "latency_ms", "elapsed", "elapsed_ms",
                 "elapsed_s", "took_ms")
# CloudWatch keeps 1-minute-resolution datapoints for exactly 15 days; a percentile (ExtendedStatistics)
# query whose period spans that boundary does NOT clip to the requested window -- it silently SPLITS into
# two datapoints at the retention boundary, and the two are NOT a clean partition of the window (measured
# live: a 30-day query for this ALB returned SampleCount [10, 79222] -- taking Datapoints[0] alone would
# have reported a p95 from a 10-sample sliver as if it were the whole 30-day window's 79232 samples, off by
# ~17x). Empirically walked day-by-day (0..16) against this ALB: exactly 1 datapoint for every window <=14
# days, 2 for every window >=15. AC11_WINDOW_DAYS stays under that boundary so ONE CloudWatch period always
# covers the whole window in ONE bucket; _cw_datapoint below still refuses (never silently mis-picks) if
# CloudWatch ever returns more than one anyway.
AC11_WINDOW_DAYS = 14
ALB_CW_NAMESPACE = "AWS/ApplicationELB"
ALB_CW_METRIC = "TargetResponseTime"
OAUTH_CLIENT_RECORD_TYPE = "oauth_client"

# A coarse but printable read-only certifier for a host shell script: every mutating command token, and
# every real file redirect ('>' not part of an fd-merge like '2>&1'), fails it. Used only to grade the
# SSM scripts this probe itself sends (AC1/AC2/AC10 exactly; AC11/AC12's retired template structurally).
_WRITE_TOKENS = re.compile(
    r'(?:^|[\s;|&])(rm|mv|cp|chmod|chown|chgrp|kill|killall|reboot|shutdown|mkfs|mount|umount|'
    r'truncate|useradd|userdel|usermod|passwd|visudo|crontab|apt|apt-get|yum|dnf|dpkg|rpm|touch|'
    r'systemctl\s+(?:start|stop|restart|reload|kill|enable|disable|mask|unmask|set-)|'
    r'service\s+\S+\s+(?:start|stop|restart)|tee|dd|mknod|ln\s+-s|sed\s+-i|'
    r'pip\s+install|npm\s+install|curl\s+-o|curl\s+-O|wget\s+-O)\b')
_WRITE_REDIRECT = re.compile(r'>(?!\s*[&=])')  # excludes an fd-merge ('2>&1') and a comparison ('>=', as in
                                               # an awk/shell numeric test) -- neither is a file redirect


def _script_is_read_only(script: str) -> tuple:
    bad = [ln.strip() for ln in script.splitlines() if _WRITE_TOKENS.search(ln) or _WRITE_REDIRECT.search(ln)]
    return (not bad), bad


def _ssm_script_digest(script: str) -> str:
    """The exact digest ssm_read() logs for a script: sha256 of its lines plus the appended END marker,
    first 16 hex chars -- so AC13 can recompute and compare against a logged command_log.jsonl row."""
    lines = script.strip("\n").split("\n") + [f"echo {END}"]
    return sha256_bytes("\n".join(lines).encode())[:16]


def _audit_census_script(remote: str, since: str) -> str:
    """The retired AC11/AC12 host script (unchanged text; AC11/AC12 no longer call it -- kept solely as
    AC13's evidence of what those 8 historical ssm:SendCommand rows in command_log.jsonl actually ran).
    `since` was call-time data (a computed cutoff timestamp), never a command; AC13 passes a placeholder."""
    dur_alt = "|".join(DURATION_KEYS)
    return f"""
F={remote}/audit.jsonl
echo "### stat"
stat -c '%s %Y' $F 2>&1
wc -l < $F
echo "### first"
head -1 $F | grep -o '"ts":"[^"]*"'
echo "### last"
tail -1 $F | grep -o '"ts":"[^"]*"'
echo "### window"
awk -v since='{since}' 'match($0, /"ts":"[^"]*"/) {{ ts=substr($0,RSTART+6,RLENGTH-7); if (ts>=since) n++ }} END {{ print n+0 }}' $F
echo "### firstinwin"
awk -v since='{since}' 'match($0, /"ts":"[^"]*"/) {{ ts=substr($0,RSTART+6,RLENGTH-7); if (ts>=since) {{ print ts; exit }} }}' $F
echo "### tools"
awk -v since='{since}' 'match($0, /"ts":"[^"]*"/) {{ ts=substr($0,RSTART+6,RLENGTH-7); if (ts>=since) print }}' $F | grep -o '"tool":"[^"]*"' | LC_ALL=C sort | uniq -c
echo "### events"
awk -v since='{since}' 'match($0, /"ts":"[^"]*"/) {{ ts=substr($0,RSTART+6,RLENGTH-7); if (ts>=since) print }}' $F | grep -o '"event":"[^"]*"' | LC_ALL=C sort | uniq -c
echo "### outcomes"
awk -v since='{since}' 'match($0, /"ts":"[^"]*"/) {{ ts=substr($0,RSTART+6,RLENGTH-7); if (ts>=since) print }}' $F | grep -o '"outcome":"[^"]*"' | LC_ALL=C sort | uniq -c
echo "### durationkeys"
awk -v since='{since}' 'match($0, /"ts":"[^"]*"/) {{ ts=substr($0,RSTART+6,RLENGTH-7); if (ts>=since) print }}' $F | grep -c -E '"({dur_alt})":'
echo "### durationkeys_all"
grep -c -E '"({dur_alt})":' $F
echo "### clientid"
awk -v since='{since}' 'match($0, /"ts":"[^"]*"/) {{ ts=substr($0,RSTART+6,RLENGTH-7); if (ts>=since) print }}' $F | grep -c '"client_id"'
echo "### clientid_all"
grep -c '"client_id"' $F
echo "### clientid_values"
grep -o '"client_id":"[^"]*"' $F | LC_ALL=C sort | uniq -c
echo "### topkeys"
awk -v since='{since}' 'match($0, /"ts":"[^"]*"/) {{ ts=substr($0,RSTART+6,RLENGTH-7); if (ts>=since) print }}' $F | sed -e 's/"args":{{[^}}]*}}/"args":{{}}/' | grep -o '"[a-z_]*":' | LC_ALL=C sort | uniq -c
"""


def _lb_dim(arn: str) -> str:
    m = re.search(r":loadbalancer/(.+)$", arn)
    if not m:
        raise RuntimeError(f"cannot parse LoadBalancer ARN {arn!r}")
    return m.group(1)


def _tg_dim(arn: str) -> str:
    m = re.search(r"(targetgroup/.+)$", arn)
    if not m:
        raise RuntimeError(f"cannot parse TargetGroup ARN {arn!r}")
    return m.group(1)


def _cw_p95(dims: list, start: str, end: str, period: int, note: str) -> tuple:
    dim_args = [",".join(f"{k}={v}" for k, v in d.items()) for d in dims]
    data, err, _ = aws("cloudwatch", "get-metric-statistics", "--namespace", ALB_CW_NAMESPACE,
                       "--metric-name", ALB_CW_METRIC, "--dimensions", *dim_args,
                       "--start-time", start, "--end-time", end, "--period", str(period),
                       "--statistics", "SampleCount", "--extended-statistics", "p95", note=note)
    return data, err


def _cw_datapoint(data: dict) -> tuple:
    """(sample_count, p95_seconds, problem). Refuses (problem set, values None) rather than silently
    picking Datapoints[0] when CloudWatch returns more than one datapoint for a one-period query --
    that split is the retention-boundary trap AC11_WINDOW_DAYS is sized to avoid; if it ever recurs this
    is the second, independent guard."""
    dps = (data or {}).get("Datapoints", [])
    if not dps:
        return None, None, None
    if len(dps) > 1:
        return None, None, (f"CloudWatch returned {len(dps)} datapoints for a one-period query "
                            f"(expected 1): {[(d.get('Timestamp'), d.get('SampleCount')) for d in dps]} "
                            "-- refusing rather than picking one")
    dp = dps[0]
    return dp.get("SampleCount"), (dp.get("ExtendedStatistics") or {}).get("p95"), None


def ac11() -> tuple:
    """R-OG-2: p95 from the ALB's own TargetResponseTime (CloudWatch), overall and per target group. The
    ALB has no tool dimension, so no per-tool figure is claimed (row NFRA_OPLGTW-W2-S1 stays the finding
    against the audit record's missing latency field; this criterion no longer depends on that record)."""
    lbs, err, _ = aws("elbv2", "describe-load-balancers", "--names", ALB_NAME, note="AC11 resolve ALB")
    if err:
        return False, f"describe-load-balancers: {err[:200]}", {}, 0
    arn = lbs["LoadBalancers"][0]["LoadBalancerArn"]
    lb_dim = _lb_dim(arn)
    tgs, err2, _ = aws("elbv2", "describe-target-groups", "--load-balancer-arn", arn, note="AC11 target groups")
    if err2:
        return False, f"describe-target-groups: {err2[:200]}", {}, 0
    tg_arns = [tg["TargetGroupArn"] for tg in tgs.get("TargetGroups", [])]
    end_dt = _dt.datetime.now(_dt.timezone.utc)
    start_dt = end_dt - _dt.timedelta(days=AC11_WINDOW_DAYS)
    start, end = start_dt.strftime("%Y-%m-%dT%H:%M:%SZ"), end_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    period = int((end_dt - start_dt).total_seconds())
    period -= period % 60  # CloudWatch Period must be a multiple of 60; one datapoint spans the window
    problems = []
    overall, oerr = _cw_p95([{"Name": "LoadBalancer", "Value": lb_dim}], start, end, period,
                           "AC11 overall p95 TargetResponseTime")
    t_overall = utcnow()
    if oerr:
        problems.append(f"overall: {oerr[:160]}")
    o_sample, o_p95, o_dp_problem = _cw_datapoint(overall)
    if o_dp_problem:
        problems.append(f"overall: {o_dp_problem}")
    per_tg = {}
    for tarn in tg_arns:
        tname = tarn.split("/")[-2] if tarn.count("/") >= 2 else tarn
        data, terr = _cw_p95([{"Name": "LoadBalancer", "Value": lb_dim}, {"Name": "TargetGroup", "Value": _tg_dim(tarn)}],
                             start, end, period, f"AC11 p95 TargetResponseTime tg={tname}")
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
        ".tools/aws; elbv2 DescribeLoadBalancers/DescribeTargetGroups resolve the dimensions")
    say(f"vintage: {utcnow()}  load_balancer={arn}  target_groups={len(tg_arns)}")
    say(f"window: {start} .. {end} ({AC11_WINDOW_DAYS} days, period={period}s)")
    say("the ALB does not know the MCP tool: this is per target group and overall, and claims no per-tool figure "
        "(the audit record's missing latency field, row NFRA_OPLGTW-W2-S1, is a separate finding, not fixed here)")
    say(f"denominator: 1 overall + {len(per_tg)} target group metric read(s)")
    say(f"overall: sample_count={o_sample} p95_seconds={o_p95}"
        + (f" ({o_p95 * 1000:.1f} ms)" if isinstance(o_p95, (int, float)) else "") + f" (read {t_overall})")
    for tname, r in per_tg.items():
        say(f"  target group {tname} ({r['target_group_arn']}): sample_count={r['sample_count']} "
            f"p95_seconds={r['p95_seconds']}"
            + (f" ({r['p95_seconds'] * 1000:.1f} ms)" if isinstance(r['p95_seconds'], (int, float)) else "")
            + f" (read {r['read_utc']})")
    measure = {"load_balancer_arn": arn, "window_start": start, "window_end": end, "period_seconds": period,
              "overall": {"sample_count": o_sample, "p95_seconds": o_p95, "read_utc": t_overall},
              "per_target_group": per_tg,
              "per_tool": None, "per_tool_note": "the ALB has no tool dimension; no per-tool figure is claimed"}
    ok = (not problems) and o_sample is not None
    reason = "" if ok else ("; ".join(problems) or "overall TargetResponseTime returned no datapoint in the window")
    return ok, reason, measure, 1 + len(per_tg)


def _ddb_val(v):
    if not isinstance(v, dict):
        return v
    for tag in ("S", "N", "BOOL"):
        if tag in v:
            return v[tag]
    if "NULL" in v:
        return None
    if "L" in v:
        return [_ddb_val(x) for x in v["L"]]
    if "M" in v:
        return {k: _ddb_val(x) for k, x in v["M"].items()}
    if "SS" in v:
        return v["SS"]
    return v


def ac12() -> tuple:
    """R-OG-2: the OAuth client inventory read from the Gateway's persisted registrations (the durable
    access-state table OG-i-1 created), never the audit record (row NFRA_OPLGTW-W2-S2 stays the finding
    against FWD-8: the audit record still carries no client_id). Process-locality is stated AS MEASURED
    from the DEPLOYED commit's own code, not asserted from the (now durable, unreleased) HEAD design."""
    commit = manifest()["deployed_commit"]
    src = manifest()["source_path"].rstrip("/")
    has_access_state = subprocess.run(
        ["git", "cat-file", "-e", f"{commit}:{src}/app/access_state.py"], cwd=str(ROOT),
        capture_output=True).returncode == 0
    oauth_src = subprocess.run(["git", "show", f"{commit}:{src}/app/oauth_as.py"], cwd=str(ROOT),
                               capture_output=True, text=True, encoding="utf-8", errors="replace",
                               check=True).stdout
    deployed_in_memory = re.search(r"_clients\s*[:=]", oauth_src) is not None
    data, err, rc = aws("dynamodb", "scan", "--table-name", ABSENT_TABLE,
                        "--filter-expression", "record_type = :rt",
                        "--expression-attribute-values", json.dumps({":rt": {"S": OAUTH_CLIENT_RECORD_TYPE}}),
                        "--projection-expression", "pk, client_id, created_at, redirect_uris",
                        "--consistent-read", note="AC12 OAuth client inventory (Scan record_type=oauth_client)")
    t = utcnow()
    if err:
        return False, f"dynamodb scan: {err[:200]}", {}, 0
    items = [{k: _ddb_val(v) for k, v in it.items()} for it in (data or {}).get("Items", [])]
    scanned, counted = (data or {}).get("ScannedCount"), (data or {}).get("Count", len(items))
    clients = []
    for it in items:
        cid = it.get("client_id", "")
        clients.append({"client_id_digest": ("sha256:" + sha256_bytes(cid.encode())[:16]) if cid else None,
                        "created_at": it.get("created_at"), "redirect_uri_count": len(it.get("redirect_uris") or [])})
    say(f"instrument: dynamodb Scan (FilterExpression record_type={OAUTH_CLIENT_RECORD_TYPE!r}, ConsistentRead) "
        f"on {ABSENT_TABLE} via .tools/aws; deployed-commit source read (git show, no AWS call) for "
        "process-locality")
    say(f"vintage: {t}")
    say(f"denominator: {scanned} item(s) scanned, {counted} matching record_type={OAUTH_CLIENT_RECORD_TYPE!r} (read {t})")
    say(f"registered clients (persisted store): {len(clients)}")
    for c in clients:
        say(f"  client {c['client_id_digest']} created_at={c['created_at']} redirect_uris={c['redirect_uri_count']}")
    say(f"process-locality AS MEASURED: deployed_commit={commit[:10]} -- app/access_state.py "
        f"{'PRESENT' if has_access_state else 'ABSENT'} at that commit; app/oauth_as.py there "
        f"{'still defines' if deployed_in_memory else 'does not define'} an in-memory '_clients' store. "
        f"So the RUNNING gateway's OAuth client store is "
        f"{'process-local (in-memory; workers pinned to 1)' if (not has_access_state and deployed_in_memory) else 'NOT process-local by this test'}"
        f"; the persisted table read above is the durable store OG-a-1/OG-d-1 built at HEAD but not yet "
        "released to this host, so today it is independent of process locality either way -- a finding "
        "carried to L10 (row NFRA_OPLGTW-W2-S2) is that the audit record still cannot name which client "
        "made a given call.")
    measure = {"table": ABSENT_TABLE, "scanned_count": scanned, "matching_count": counted, "clients": clients,
              "deployed_commit": commit, "deployed_has_access_state": has_access_state,
              "deployed_client_store_process_local": (not has_access_state) and deployed_in_memory}
    return True, "", measure, scanned  # denominator = items scanned, not matched (0 matches is legitimate)


_NOTE_RE = re.compile(r"host read (?P<label>.+?); script sha256=(?P<digest>[0-9a-f]+)")
_EXACT_DIGEST_LABELS = ("AC1 digests", "AC2 host shape", "AC10 peak RSS")


def _known_script_texts() -> dict:
    remote = manifest()["remote_path"].rstrip("/")
    return {
        "AC1 digests": _ac1_script(remote),
        "AC2 host shape": _ac2_script(remote),
        "AC10 peak RSS": _ac10_script(),
        "AC11 audit latency census": _audit_census_script(remote, "SINCE_PLACEHOLDER_TS"),
        "AC12 audit client census": _audit_census_script(remote, "SINCE_PLACEHOLDER_TS"),
    }


def ac13() -> tuple:
    """R-OG-2: every AWS call is a read verb, except ssm:SendCommand is admitted iff its command text is
    printed and is itself read-only. AC1/AC2/AC10's 3 scripts regenerate byte-identical (their digest is
    recomputed and compared against the logged one); AC11/AC12's retired template (2 calls each, 4 total)
    embedded a per-call cutoff timestamp that cannot be recomputed after the fact, so those are graded by
    the unchanged surrounding template's own read-only shape instead of an exact digest."""
    rows = []
    if CMDLOG.exists():
        for line in CMDLOG.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
    by_op: dict = {}
    for r in rows:
        by_op[f"{r['service']}:{r['api_op']}"] = by_op.get(f"{r['service']}:{r['api_op']}", 0) + 1

    scripts = _known_script_texts()
    send_rows = [r for r in rows if r["api_op"] == "SendCommand"]
    admitted, refused = [], []
    for r in send_rows:
        m = _NOTE_RE.search(r.get("note", ""))
        label, logged_digest = (m.group("label"), m.group("digest")) if m else (None, None)
        text = scripts.get(label)
        if text is None:
            refused.append({**r, "reason": f"label {label!r} not in the known script registry"})
            continue
        ro, bad = _script_is_read_only(text)
        if not ro:
            refused.append({**r, "reason": f"script contains a non-read line: {bad[:1]}"})
            continue
        digest_check = "template-match (per-call timestamp, not a command, cannot be recomputed)"
        if label in _EXACT_DIGEST_LABELS:
            recomputed = _ssm_script_digest(text)
            if recomputed != logged_digest:
                refused.append({**r, "reason": f"recomputed digest {recomputed} != logged {logged_digest}"})
                continue
            digest_check = f"EXACT MATCH ({recomputed})"
        admitted.append({"criterion": r["criterion"], "label": label, "logged_digest": logged_digest,
                        "digest_check": digest_check})

    other = [r for r in rows if r["api_op"] != "SendCommand"]
    non_read_other = [r for r in other if not r["api_op"].startswith(READ_VERBS)]
    nr_ops: dict = {}
    for r in non_read_other:
        k = f"{r['service']}:{r['api_op']}"
        nr_ops[k] = nr_ops.get(k, 0) + 1

    say(f"instrument: this probe reads {CMDLOG.relative_to(ROOT).as_posix()} (one row per AWS call, written "
        "by aws()); ssm:SendCommand rows are graded against this file's own script-building functions -- "
        "this criterion makes no AWS call itself")
    say(f"vintage: {utcnow()}")
    say(f"denominator: {len(rows)} AWS call(s) in the command log")
    say(f"per operation: {dict(sorted(by_op.items()))}")
    say(f"Describe/Get/List/Head/Scan/Query calls: {len(other) - len(non_read_other)} of {len(rows)}")
    say(f"ssm:SendCommand calls: {len(send_rows)} of {len(rows)}; admitted (read-only script) "
        f"{len(admitted)}, refused {len(refused)}")
    for a in admitted:
        say(f"  ADMITTED {a['criterion']} label={a['label']!r} logged_digest={a['logged_digest']} "
            f"digest_check={a['digest_check']}")
    say(f"the {len(scripts)} distinct SSM script text(s) this cell's evidence relies on, verbatim "
        "(AC1/AC2/AC10 regenerated identically; AC11/AC12's retired template shown with its per-call "
        "cutoff timestamp replaced by a placeholder):")
    for label, text in scripts.items():
        ro, bad = _script_is_read_only(text)
        say(f"--- {label} (read_only={ro}) ---")
        for line in text.strip("\n").splitlines():
            say(f"    {line}")
    if non_read_other:
        say(f"non-read-verb, non-SendCommand calls: {len(non_read_other)} {dict(sorted(nr_ops.items()))}")
    if refused:
        say(f"refused SendCommand row(s): {len(refused)}")
        for r in refused:
            say(f"  REFUSED {r['criterion']} {r.get('reason')}")

    problems = []
    if not rows:
        problems.append("command log empty")
    if non_read_other:
        problems.append(f"{len(non_read_other)} non-read, non-SendCommand call(s): {dict(sorted(nr_ops.items()))}")
    if refused:
        problems.append(f"{len(refused)} SendCommand call(s) not admitted as read-only")
    ok = not problems
    reason = "; ".join(problems)
    measure = {"calls": len(rows), "per_operation": by_op, "send_command_calls": len(send_rows),
              "send_command_admitted": admitted, "send_command_refused": refused,
              "non_read_non_sendcommand": nr_ops}
    return ok, reason, measure, len(rows)


CRITERIA = {"AC1": ac1, "AC2": ac2, "AC3": ac3, "AC4": ac4, "AC5": ac5, "AC6": ac6, "AC7": ac7, "AC8": ac8,
            "AC9": ac9, "AC10": ac10, "AC11": ac11, "AC12": ac12, "AC13": ac13}


def render_md() -> None:
    b = json.loads(BASELINE.read_text(encoding="utf-8"))
    out = ["# NFRA_OPLGTW OG-p-1 -- deployed parity and pre-change baseline",
           "",
           "Rendered from `BASELINE.json` by `probes/og_p1.py render-md`. Each section is one criterion: the probe's "
           "own printed measurement (instrument, UTC vintage, denominator) and its verdict line, verbatim. READ ONLY: "
           "every value below came from a read; nothing in AWS or on the host was changed.", ""]
    for k in sorted(b, key=lambda x: int(x.split("AC")[1])):
        e = b[k]
        out += [f"## {k}", "", f"- measured: {e['measured_utc']}", f"- instrument: {e['instrument']}",
                f"- denominator: {e['denominator']}", f"- verdict: `{e['verdict']}`", "", "```"]
        out += e["printed"]
        out += ["```", ""]
    BASELINE_MD.write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {BASELINE_MD.relative_to(ROOT).as_posix()} ({len(b)} criteria)")


def main(argv: list) -> int:
    global CRIT
    if not argv:
        print(__doc__)
        return 2
    if argv[0] == "render-md":
        render_md()
        return 0
    key = argv[0].upper()
    if key not in CRITERIA:
        print(f"unknown criterion {argv[0]!r}; expected AC1..AC13 or render-md")
        return 2
    CRIT = key
    kwargs = {}
    if key == "AC1" and "--commit" in argv:
        kwargs["commit_override"] = argv[argv.index("--commit") + 1]
    try:
        ok, reason, measure, denom = CRITERIA[key](**kwargs)
    except Exception as e:  # a failed read is a FAIL with its reason, never a silent pass
        ok, reason, measure, denom = False, f"probe error: {type(e).__name__}: {str(e)[:300]}", {}, 0
    verdict = f"VERDICT: PASS-OGP1-{key}" if ok else f"VERDICT: FAIL-OGP1-{key} {reason}"
    if "--record" in argv and not os.environ.get("OGP1_MUTANT_ROLE") and not kwargs:
        with _Lock():
            b = json.loads(BASELINE.read_text(encoding="utf-8")) if BASELINE.exists() else {}
            instrument = next((ln[len("instrument: "):] for ln in LINES if ln.startswith("instrument: ")), "")
            b[f"OGP1-{key}"] = {"measured_utc": utcnow(), "instrument": instrument, "denominator": denom,
                                "verdict": verdict, "measurement": measure, "printed": LINES + [verdict]}
            BASELINE.write_text(json.dumps(b, indent=1, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(verdict, flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
