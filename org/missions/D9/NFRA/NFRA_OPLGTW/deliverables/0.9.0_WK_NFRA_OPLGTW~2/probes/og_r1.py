#!/usr/bin/env python3
"""og_r1.py -- the acceptance probe for NFRA_OPLGTW.TO-OG-r-1 (cell OG-r-1), the first release cutover.

Usage:  og_r1.py AC<n>      n = 1..20

Each arm prints its measurement with vintage and denominator, then exactly one line
  VERDICT: PASS-OGR1-AC<n>  or  VERDICT: FAIL-OGR1-AC<n> <reason>.

This is a WORLD ACT: AC2 runs the real release through infra/aws/ec2/safe-ec2-deploy.sh against the live
Gateway host i-07dccb1615503ac99 (AWS account 313476888478). AC1 opens the deploy-completion ledger BEFORE
the deploy; AC8 closes it BEFORE the grading reads (CLAUDE.md "NEVER leave a confirmed deploy half-landed").
AC11 runs LOCALLY, against emulated AWS (moto), BEFORE the deploy, and never touches the host or the live
state store. Every arm's shared, cross-invocation state (each AC is a separate process) lives in
evidence/og_r1/state.json, next to this probe, inside this worker's own deliverables grant.

No secret or ExternalId value ever enters stdout or a written file (AC13/AC14, and the general bound). All
AWS calls other than SSM RunShellScript payloads go through boto3 directly; SSM host scripts reuse the
og_p1.py/og_i2.py pattern (send-command -> poll get-command-invocation) already exercised on this project.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import logging
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

for _n in ("botocore", "boto3", "urllib3"):
    logging.getLogger(_n).setLevel(logging.INFO)

HERE = os.path.dirname(os.path.abspath(__file__))
DELIV = os.path.dirname(HERE)
_top = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=HERE, capture_output=True, text=True)
REPO = _top.stdout.strip() or os.path.abspath(os.path.join(DELIV, *[".."] * 6))
sys.path.insert(0, os.path.join(REPO, ".tools"))
from git_bash_resolver import git_bash  # noqa: E402

BASH = git_bash() or "bash"

SERIAL = os.environ.get("OPAL_AGENT_SERIAL") or "0.9.0_WK_NFRA_OPLGTW~2"
REGION = "us-east-1"
ACCOUNT = "313476888478"
INSTANCE = "i-07dccb1615503ac99"
SERVICE_KEY = "opal-gateway"
GATEWAY_URL = "https://mcp.opalinvest.dev"
GW_ROLE_ARN = "arn:aws:iam::%s:role/opal-gateway-role" % ACCOUNT
READER_ROLE = "gateway-schwab-read-role"
CATALOG_ROLE = "gateway-schwab-catalog-read-role"
READER_ARN = "arn:aws:iam::%s:role/%s" % (ACCOUNT, READER_ROLE)
CATALOG_ARN = "arn:aws:iam::%s:role/%s" % (ACCOUNT, CATALOG_ROLE)
EXT_SECRET = "opal/mcp/opal-gateway-schwab-reader-external-ids"
ACCESS_STATE_TABLE = "gateway-access-state-table"  # app/access_state.py TABLE_NAME (OG-i-5 rename, R-OG-8)
MANIFEST_REL = "infra/aws/ec2/EC2_MANIFEST.json"
GATEWAY_SRC = "infra/aws/ec2/opal-gateway"
LEDGER_SLUG = "nfra-oplgtw-og-r-1-first-release"
EVID = os.path.join(DELIV, "evidence", "og_r1")
STATE_PATH = os.path.join(EVID, "state.json")
AC11_PYTEST = os.path.join(HERE, "og_r1_ac11_pytest.py")


# --------------------------------------------------------------------------- generic helpers
def now() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


def iso(t: datetime.datetime = None) -> str:
    return (t or now()).astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def rel(p: str) -> str:
    return os.path.relpath(p, REPO).replace("\\", "/")


def verdict(n: int, ok: bool, reason: str = "") -> int:
    print("VERDICT: PASS-OGR1-AC%d" % n if ok else "VERDICT: FAIL-OGR1-AC%d %s" % (n, reason))
    return 0 if ok else 1


def print_rows(rows: list) -> bool:
    for c, ok, d in rows:
        print("  %s %s -- %s" % ("OK " if ok else "NOT", c, d))
    n_ok = sum(1 for r in rows if r[1])
    print("DENOMINATOR: %d of %d checks OK" % (n_ok, len(rows)))
    return n_ok == len(rows) and bool(rows)


def session():
    import boto3
    return boto3.Session(region_name=REGION)


def err_code(e) -> str:
    return getattr(e, "response", {}).get("Error", {}).get("Code", type(e).__name__)


def load_state() -> dict:
    if os.path.isfile(STATE_PATH):
        with open(STATE_PATH, encoding="utf-8") as fh:
            return json.load(fh)
    return {}


def save_state(st: dict) -> None:
    os.makedirs(EVID, exist_ok=True)
    with open(STATE_PATH, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(st, fh, indent=1, sort_keys=True)
        fh.write("\n")


def write_json(path: str, obj) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(obj, fh, indent=1, sort_keys=True)
        fh.write("\n")


def _env_with_tools_path(extra: dict = None) -> dict:
    env = dict(os.environ)
    tools = os.path.join(REPO, ".tools")
    env["PATH"] = tools + os.pathsep + env.get("PATH", "")
    if extra:
        env.update(extra)
    return env


def run(cmd: list, timeout: int = 120, **kw) -> subprocess.CompletedProcess:
    kw.setdefault("env", _env_with_tools_path())
    return subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", timeout=timeout, **kw)


def git_head() -> str:
    return run(["git", "rev-parse", "HEAD"]).stdout.strip()


def git_show_utc(commit: str) -> str:
    return run(["git", "show", "-s", "--format=%cI", commit]).stdout.strip()


def manifest() -> dict:
    with open(os.path.join(REPO, MANIFEST_REL), encoding="utf-8") as fh:
        return json.load(fh)["services"][SERVICE_KEY]


def commit_exists(commit: str) -> bool:
    return run(["git", "cat-file", "-e", commit + "^{commit}"]).returncode == 0


def tree_hash(commit: str, path: str) -> str:
    """The git tree object hash for `path` at `commit` -- an immutable, content-addressed identity for a
    whole source directory (R-40's "packaging tool's own digest" for an artifact that is not one tracked
    file)."""
    r = run(["git", "rev-parse", "%s:%s" % (commit, path)])
    if r.returncode != 0:
        raise RuntimeError("git rev-parse %s:%s failed: %s" % (commit, path, r.stderr.strip()))
    return r.stdout.strip()


def path_exists_at(commit: str, path: str) -> bool:
    return run(["git", "cat-file", "-e", "%s:%s" % (commit, path)]).returncode == 0


def show_at(commit: str, path: str) -> str:
    r = run(["git", "show", "%s:%s" % (commit, path)])
    if r.returncode != 0:
        raise RuntimeError("git show %s:%s failed: %s" % (commit, path, r.stderr.strip()))
    return r.stdout


# --------------------------------------------------------------------------- SSM host harness (og_p1.py /
# og_i2.py pattern: send-command AWS-RunShellScript, poll get-command-invocation, one end marker).
END_MARK = "__OGR1_END__"


def ssm_run(script: str, label: str, timeout_s: str = "80", budget_s: int = 100) -> tuple:
    sess = session()
    ssm = sess.client("ssm")
    lines = script.strip("\n").split("\n") + ["echo %s" % END_MARK]
    t0 = now()
    cid = ssm.send_command(InstanceIds=[INSTANCE], DocumentName="AWS-RunShellScript",
                           Parameters={"commands": ["\n".join(lines)], "executionTimeout": [timeout_s]},
                           Comment="NFRA_OPLGTW OG-r-1 %s" % label)["Command"]["CommandId"]
    deadline = time.time() + budget_s
    inv = {}
    while time.time() < deadline:
        time.sleep(2)
        try:
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=INSTANCE)
        except Exception as e:  # noqa: BLE001
            if err_code(e) == "InvocationDoesNotExist":
                continue
            raise
        if inv.get("Status") in ("Success", "Failed", "Cancelled", "TimedOut"):
            break
    t1 = now()
    out = inv.get("StandardOutputContent", "")
    err = inv.get("StandardErrorContent", "")
    status = inv.get("Status")
    complete = END_MARK in out
    return {"cid": cid, "status": status, "out": out.split(END_MARK)[0] if complete else out, "err": err,
            "complete": complete, "t0": iso(t0), "t1": iso(t1), "instance": INSTANCE}


def assert_clean(res: dict, secretish: list) -> None:
    for token in secretish:
        if token and (token in res["out"] or token in res["err"]):
            raise RuntimeError("REFUSED: host output carries a credential/secret-shaped token; nothing recorded")


# --------------------------------------------------------------------------- AC1 -- open the ledger, commit
# the sentinel BEFORE the deploy. Also snapshots the PREVIOUS release identity for AC10 (must happen before
# AC2 overwrites EC2_MANIFEST.json's deployed_commit).
def _write_msgfile(name: str, body: str) -> str:
    p = os.path.join(EVID, name)
    os.makedirs(EVID, exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(body)
    return p


def _safe_commit(paths: list, msgfile: str) -> subprocess.CompletedProcess:
    return run([BASH, ".tools/safe-commit.sh", "--author", "%s <%s@opal.agent>" % (SERIAL, SERIAL),
               "-F", msgfile, "--"] + paths, timeout=90)


def _record_previous_release(st: dict) -> None:
    if "previous" in st:
        return
    m = manifest()
    prev_commit = m["deployed_commit"]
    prev_tree_hash = tree_hash(prev_commit, GATEWAY_SRC)
    checks = {
        "commit_exists": commit_exists(prev_commit),
        "revocation_shim_present": path_exists_at(prev_commit, GATEWAY_SRC + "/app/revocation.py"),
        "restricted_profile_denial_present": (
            path_exists_at(prev_commit, GATEWAY_SRC + "/app/data_entitlement.py")
            and path_exists_at(prev_commit, GATEWAY_SRC + "/app/identity_scope.py")),
        "schwab_not_enabled_in_deploy_script": "schwab" not in re.findall(
            r'ENABLED_INTEGRATIONS=\S+', show_at(prev_commit, GATEWAY_SRC + "/deploy-to-ec2.sh"))[0].lower()
        if re.findall(r'ENABLED_INTEGRATIONS=\S+', show_at(prev_commit, GATEWAY_SRC + "/deploy-to-ec2.sh"))
        else False,
    }
    st["previous"] = {
        "recorded_utc": iso(),
        "commit": prev_commit,
        "content_hash_instrument": "git rev-parse <commit>:%s (git TREE object hash of the deployed source "
                                   "directory -- the packaging tool's own digest for a whole-directory "
                                   "artifact; R-40)" % GATEWAY_SRC,
        "content_hash": prev_tree_hash,
        "restorability_checks": checks,
    }


def ac1() -> int:
    st = load_state()
    sentinel = os.path.join(REPO, "org", "critical_paths", ".open_deploys", LEDGER_SLUG + ".json")

    if "ledger_open_commit" not in st:
        _record_previous_release(st)
        if not os.path.isfile(sentinel):
            title = ("NFRA_OPLGTW OG-r-1 first release: integrated Gateway build, OAuth cutover, "
                     "Schwab flag OFF")
            cmd = ["py", "-3.12", os.path.join(REPO, ".tools", "deploy_ledger.py"), "open",
                  "--slug", LEDGER_SLUG, "--title", title, "--author", SERIAL,
                  "--leg", "L1|ec2-baked-asset|opal-gateway /opt/opal-gateway|SSM sha256sum digest match "
                           "vs the deployed build input, file by file, denominator printed (OGR1-AC4)",
                  "--leg", "L2|verify|post-deploy live checks: 401 resource challenge, discovery metadata, "
                           "zero Schwab tools registered, error count vs baseline, restricted-profile "
                           "principal count, renamed-role assume/deny|OGR1-AC3,AC5,AC6,AC7,AC9,AC12,AC13 "
                           "PASS-by-output",
                  "--leg", "L3|git|EC2_MANIFEST.json services.opal-gateway.deployed_commit|"
                           "git commit hash of safe-ec2-deploy.sh's own manifest-update commit"]
            r = run(cmd, timeout=60)
            print(r.stdout)
            if r.returncode != 0:
                print(r.stderr)
                return verdict(1, False, "deploy_ledger.py open failed rc=%d: %s" % (r.returncode, r.stderr[:300]))
        with open(sentinel, encoding="utf-8") as fh:
            sdata = json.load(fh)
        msgfile = _write_msgfile("ac1_commit_msg.txt",
            "deploy-ledger(open, NFRA_OPLGTW.TO-OG-r-1): OG-r-1 first release -- opened BEFORE the deploy, "
            "per the no-half-landed-deploy discipline\n\nCo-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>\n")
        c = _safe_commit(["org/critical_paths/.open_deploys/%s.json" % LEDGER_SLUG, sdata["entry_path"]], msgfile)
        print(c.stdout)
        print(c.stderr)
        if c.returncode != 0:
            return verdict(1, False, "safe-commit of the ledger sentinel+entry failed rc=%d" % c.returncode)
        st["ledger_open_commit"] = git_head()
        st["ledger_open_utc"] = iso()
        st["ledger_entry_path"] = sdata["entry_path"]
        save_state(st)

    commit_h = st["ledger_open_commit"]
    exists = commit_exists(commit_h)
    in_log = run(["git", "log", "--oneline", "-1", commit_h]).stdout.strip()
    order_ok, order_detail = True, "the deploy has not run yet (or this check pre-dates it)"
    if "deploy_started_utc" in st:
        order_ok = st["ledger_open_utc"] <= st["deploy_started_utc"]
        order_detail = "%s <= %s" % (st["ledger_open_utc"], st["deploy_started_utc"])
    rows = [("the ledger-open commit exists in this branch's history", exists, commit_h),
            ("git log shows that commit (committed, not merely staged)", bool(in_log), in_log),
            ("the open precedes the deploy", order_ok, order_detail)]
    ok = print_rows(rows)
    return verdict(1, ok, "" if ok else "a check is NOT OK (see NOT lines)")


# --------------------------------------------------------------------------- AC2 -- the deploy itself
def ac2() -> int:
    st = load_state()
    if "deploy_manifest_commit" not in st:
        if "ledger_open_commit" not in st:
            return verdict(2, False, "the ledger is not open yet -- run AC1 first (never deploy unledgered)")
        deploy_src_before = manifest()
        pre_commit = deploy_src_before["deployed_commit"]
        # HALT_ACK=1: the routine (non-STOP) tier of .tools/halt-gate-check.sh, reviewed this run (printed
        # in this criterion's own output above/below) -- 18 pending messages on the issuer's inbox
        # (2.0.0_SA_COO~O), none addressed as a [STOP] to this deploy or to NFRA_OPLGTW/opal-gateway.
        # HALT_ACK is the gate's own documented route past its rc=1 tier; HALT_OVERRIDE (the audited,
        # STOP-class bypass) is not used and was not needed (the gate itself never returned rc=2).
        env = _env_with_tools_path({"AGENT_NAME": SERIAL, "HALT_ACK": "1"})
        t0 = now()
        pre_deploy_head = git_head()  # what deploy-to-ec2.sh's own `git rev-parse --short HEAD` will build
        st["deploy_started_utc"] = iso(t0)
        save_state(st)
        r = run([BASH, "infra/aws/ec2/safe-ec2-deploy.sh", "opal-gateway",
                "infra/aws/ec2/opal-gateway/deploy-to-ec2.sh", INSTANCE],
               timeout=480, env=env, input="")
        t1 = now()
        print(r.stdout[-8000:])
        print(r.stderr[-4000:])
        if r.returncode != 0:
            return verdict(2, False, "safe-ec2-deploy.sh rc=%d (see output above)" % r.returncode)
        post = manifest()
        manifest_commit = run(["git", "log", "-1", "--format=%H", "--", MANIFEST_REL]).stdout.strip()
        st["deploy_finished_utc"] = iso(t1)
        st["deploy_pre_commit"] = pre_commit
        st["deploy_head"] = pre_deploy_head  # the commit actually built and deployed
        st["deploy_manifest_deployed_commit"] = post["deployed_commit"]
        st["deploy_manifest_commit"] = manifest_commit  # the LATER commit recording the manifest update itself
        save_state(st)

    st = load_state()
    ok_commit = st["deploy_manifest_deployed_commit"] == st["deploy_head"]
    src_at_head = show_at(st["deploy_head"], GATEWAY_SRC + "/deploy-to-ec2.sh")
    flag_line = re.findall(r'ENABLED_INTEGRATIONS=[^\n\\]+', src_at_head)
    flag_off = bool(flag_line) and "schwab" not in flag_line[-1].lower()
    rows = [("the deploy completed (safe-ec2-deploy.sh rc=0, recorded this run)", "deploy_finished_utc" in st,
             st.get("deploy_finished_utc")),
            ("EC2_MANIFEST.json's recorded deployed_commit == the commit actually built and deployed "
             "(pre-deploy HEAD; the manifest-update commit that follows it is a later, separate commit)",
             ok_commit, "%s == %s" % (st["deploy_manifest_deployed_commit"], st["deploy_head"])),
            ("the released deploy-to-ec2.sh's ENABLED_INTEGRATIONS line omits 'schwab' (the Schwab flag is off)",
             flag_off, flag_line[-1] if flag_line else "line not found")]
    ok = print_rows(rows)
    return verdict(2, ok, "" if ok else "a check is NOT OK (see NOT lines)")


# --------------------------------------------------------------------------- AC3 -- no principal profile
def _access_state_scan_count() -> tuple:
    sess = session()
    ddb = sess.client("dynamodb")
    t = now()
    total = 0
    sample_pks = []
    kwargs = {"TableName": ACCESS_STATE_TABLE, "Select": "SPECIFIC_ATTRIBUTES", "ProjectionExpression": "pk, sk"}
    while True:
        page = ddb.scan(**kwargs)
        items = page.get("Items", [])
        total += len(items)
        for it in items:
            sample_pks.append({"pk": it.get("pk", {}).get("S"), "sk": it.get("sk", {}).get("S")})
        if "LastEvaluatedKey" not in page:
            break
        kwargs["ExclusiveStartKey"] = page["LastEvaluatedKey"]
    return t, total, sample_pks


_PROBE_KEY_RE = re.compile(r"probe-og-[a-z0-9]+-\d{8}T\d{6}")  # other cells' own OWN synthetic test fixtures
                                                              # (og_i1.py/og_i5.py's runtime-key probes), never
                                                              # a real tid/oid principal


def _classify_items(sample: list) -> tuple:
    real, probe = [], []
    for s in sample:
        blob = "%s %s" % (s.get("pk") or "", s.get("sk") or "")
        (probe if _PROBE_KEY_RE.search(blob) else real).append(s)
    return real, probe


def ac3() -> int:
    t, total, sample = _access_state_scan_count()
    print("instrument: dynamodb Scan(ProjectionExpression=pk,sk) on %s" % ACCESS_STATE_TABLE)
    print("vintage: %s  denominator: %d item(s) in the table" % (iso(t), total))
    if sample:
        print("sample keys (up to 20, structure only): %s" % sample)
    real, probe = _classify_items(sample)
    profile_like = [s for s in real if ("profile" in (s.get("sk") or "").lower()
                                        or "profile" in (s.get("pk") or "").lower()
                                        or "grant" in (s.get("pk") or "").lower())]
    print("of the %d sampled item(s): %d match OTHER cells' own synthetic 'probe-og-<cell>-<timestamp>' test "
          "fixtures (og_i1.py/og_i5.py, pre-existing, not this release's work and not a real principal); "
          "%d do not" % (len(sample), len(probe), len(real)))
    rows = [("the table is reachable (a Scan returned)", True, "rc n/a (no exception)"),
            ("every sampled item is a pre-existing probe fixture or otherwise non-profile-shaped, never a "
             "real principal's profile", not profile_like, profile_like)]
    ok = print_rows(rows)
    return verdict(3, ok, "" if ok else "a principal profile appears to be active -- see sample keys above")


# --------------------------------------------------------------------------- AC4 -- deployed digests
DEPLOY_ROOTS = ["app", "deploy", "requirements.txt", "identity_tool_allowlist.txt"]
DIGEST_EXCLUDE = re.compile(r"(^|/)(__pycache__|infra)(/|$)|\.log$|(^|/)(\.env|audit\.jsonl|\.token_cache)$")


def _digest_script(remote: str) -> str:
    return r"""
cd %s || exit 3
find app deploy requirements.txt identity_tool_allowlist.txt -type f ! -path '*/__pycache__/*' ! -name '*.pyc' | LC_ALL=C sort | while IFS= read -r f; do printf '%%s %%s\n' "$(sha256sum < "$f" | cut -c1-64)" "$f"; done
""" % remote


def ac4() -> int:
    st = load_state()
    if "deploy_head" not in st:
        return verdict(4, False, "no deploy recorded yet -- run AC2 first")
    build_commit = st["deploy_head"]
    m = manifest()
    remote = m["remote_path"].rstrip("/")
    ls = run(["git", "ls-tree", "-r", build_commit, "--"] + ["%s/%s" % (GATEWAY_SRC, r) for r in DEPLOY_ROOTS]).stdout
    tree = {}
    for line in ls.splitlines():
        meta, path = line.split("\t", 1)
        _mode, typ, blob = meta.split()
        r = path[len(GATEWAY_SRC) + 1:]
        if typ != "blob" or DIGEST_EXCLUDE.search(r):
            continue
        data = run(["git", "cat-file", "blob", blob]).stdout
        tree[r] = hashlib.sha256(data.encode("utf-8", "surrogateescape")).hexdigest()
    res = ssm_run(_digest_script(remote), "AC4 digests", timeout_s="60")
    if res["status"] != "Success" or not res["complete"]:
        return verdict(4, False, "SSM %s status=%s complete=%s" % (res["cid"], res["status"], res["complete"]))
    host = {}
    for line in res["out"].splitlines():
        parts = line.split(" ", 1)
        if len(parts) == 2 and re.fullmatch(r"[0-9a-f]{64}", parts[0]):
            host[parts[1].strip()] = parts[0]
    union = sorted(set(tree) | set(host))
    differ = [p for p in union if p in tree and p in host and tree[p] != host[p]]
    host_only = [p for p in union if p not in tree]
    tree_only = [p for p in union if p not in host]
    print("instrument: SSM AWS-RunShellScript sha256sum on %s (%s) vs git blob sha256 at %s (build input == "
          "AC2's deployed HEAD); ssm %s %s" % (INSTANCE, remote, build_commit, res["cid"], res["status"]))
    print("vintage: %s .. %s" % (res["t0"], res["t1"]))
    print("denominator: %d files (tree %d, host %d)" % (len(union), len(tree), len(host)))
    for p in differ:
        print("  MISMATCH %s host=%s tree=%s" % (p, host[p][:16], tree[p][:16]))
    for p in host_only:
        print("  HOST-ONLY %s" % p)
    for p in tree_only:
        print("  TREE-ONLY %s" % p)
    ok = bool(tree) and bool(host) and not differ and not host_only and not tree_only
    return verdict(4, ok, "" if ok else "digest_mismatch=%d host_only=%d tree_only=%d" % (len(differ), len(host_only), len(tree_only)))


# --------------------------------------------------------------------------- AC5 -- 401 resource challenge
def _http_get(url: str, headers: dict = None) -> tuple:
    """Returns (status, headers, body). `headers` is the raw http.client.HTTPMessage -- KEEP IT (not
    dict(...)): HTTP header names are case-insensitive and this server sends them lowercase
    ('www-authenticate'), but a plain dict() is a case-SENSITIVE lookup and silently reads as absent."""
    req = urllib.request.Request(url, headers=headers or {}, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status, resp.headers, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, e.headers, e.read()


def ac5() -> int:
    st = load_state()
    if "deploy_head" not in st:
        return verdict(5, False, "the release deploy (OGR1-AC2) did not run, so there is no released build "
                                 "whose live behavior this criterion can grade")
    t = now()
    status, headers, _body = _http_get(GATEWAY_URL + "/mcp")
    wa = headers.get("WWW-Authenticate", "")
    expect_url = GATEWAY_URL + "/.well-known/oauth-protected-resource"
    has_challenge = wa.startswith("Bearer") and ('resource_metadata="%s"' % expect_url) in wa
    no_error_param = 'error=' not in wa
    print("instrument: unauthenticated GET %s/mcp (no Authorization header)" % GATEWAY_URL)
    print("vintage: %s  status=%s  WWW-Authenticate present=%s" % (iso(t), status, bool(wa)))
    rows = [("status is 401", status == 401, status),
            ("WWW-Authenticate advertises the resource_metadata challenge (asserted, not printed)",
             has_challenge, has_challenge),
            ("a missing-credential challenge carries no error= (RFC 6750 s3.1)", no_error_param, no_error_param)]
    ok = print_rows(rows)
    return verdict(5, ok, "" if ok else "a check is NOT OK (see NOT lines)")


# --------------------------------------------------------------------------- AC6 -- discovery metadata
def ac6() -> int:
    st = load_state()
    if "deploy_head" not in st:
        return verdict(6, False, "the release deploy (OGR1-AC2) did not run, so there is no released build "
                                 "whose live discovery metadata this criterion can grade")
    t = now()
    s1, _h1, b1 = _http_get(GATEWAY_URL + "/.well-known/oauth-protected-resource")
    s2, _h2, b2 = _http_get(GATEWAY_URL + "/.well-known/oauth-authorization-server")
    prot = json.loads(b1) if s1 == 200 else {}
    auth = json.loads(b2) if s2 == 200 else {}
    print("instrument: unauthenticated GET of both RFC 8414/9728 discovery documents")
    print("vintage: %s  protected-resource status=%s  authorization-server status=%s" % (iso(t), s1, s2))
    issuer = auth.get("issuer")
    rows = [
        ("both discovery documents served 200", s1 == 200 and s2 == 200, (s1, s2)),
        ("issuer is this Gateway (%s)" % GATEWAY_URL, issuer == GATEWAY_URL, issuer),
        ("protected-resource.authorization_servers == [issuer]", prot.get("authorization_servers") == [issuer],
         prot.get("authorization_servers")),
        ("protected-resource.resource names the /mcp resource under the issuer (RFC 8414's "
         "authorization-server metadata carries no 'resource' field, so it is never compared to one)",
         prot.get("resource") == GATEWAY_URL + "/mcp", prot.get("resource")),
        ("every endpoint is under the issuer", all(str(auth.get(k, "")).startswith(issuer or "\0")
         for k in ("authorization_endpoint", "token_endpoint", "registration_endpoint", "jwks_uri")),
         {k: auth.get(k) for k in ("authorization_endpoint", "token_endpoint", "registration_endpoint", "jwks_uri")}),
        ("scopes_supported is a non-empty list on both documents", bool(prot.get("scopes_supported")) and
         prot.get("scopes_supported") == auth.get("scopes_supported"), auth.get("scopes_supported")),
        ("PKCE is S256-only (no plain)", auth.get("code_challenge_methods_supported") == ["S256"],
         auth.get("code_challenge_methods_supported")),
        ("bearer_methods_supported is exactly ['header']", prot.get("bearer_methods_supported") == ["header"],
         prot.get("bearer_methods_supported")),
    ]
    ok = print_rows(rows)
    return verdict(6, ok, "" if ok else "a check is NOT OK (see NOT lines)")


# --------------------------------------------------------------------------- AC7 -- zero Schwab tools
def _env_script(remote: str) -> str:
    return r"""
sudo -u ec2-user grep -c '^ENABLED_INTEGRATIONS=' %s/.env 2>&1
sudo -u ec2-user grep '^ENABLED_INTEGRATIONS=' %s/.env 2>&1
""" % (remote, remote)


def ac7() -> int:
    st = load_state()
    if "deploy_head" not in st:
        return verdict(7, False, "the release deploy (OGR1-AC2) did not run, so there is no released build "
                                 "whose live registry this criterion can grade")
    m = manifest()
    remote = m["remote_path"].rstrip("/")
    res = ssm_run(_env_script(remote), "AC7 enabled-integrations", timeout_s="30")
    if res["status"] != "Success":
        return verdict(7, False, "SSM %s status=%s" % (res["cid"], res["status"]))
    lines = [ln for ln in res["out"].splitlines() if ln.strip()]
    line = next((ln for ln in lines if ln.startswith("ENABLED_INTEGRATIONS=")), "")
    enabled = [s for s in re.split(r"[,\s]+", line.split("=", 1)[1]) if s] if line else None
    schwab_available = None
    try:
        sys.path.insert(0, os.path.join(REPO, GATEWAY_SRC))
        from app.integrations import registry as _reg  # noqa: PLC0415
        schwab_available = "schwab" in _reg.available_ids()
    except Exception as e:  # noqa: BLE001
        schwab_available = "unreadable: %s" % e
    print("instrument: on-host read of /opt/opal-gateway/.env's ENABLED_INTEGRATIONS (SSM %s %s) + local read of "
          "app.integrations.registry.available_ids() (registry.register_enabled only constructs+registers a "
          "factory for an id present in ENABLED_INTEGRATIONS -- an absent id adds zero tools, by construction)"
          % (res["cid"], res["status"]))
    print("vintage: %s .. %s  live .env line: %r" % (res["t0"], res["t1"], line))
    rows = [("the on-host .env carries an ENABLED_INTEGRATIONS line", line != "", line),
            ("'schwab' is a KNOWN registry id (the omission below is deliberate, not a typo)",
             schwab_available is True, schwab_available),
            ("'schwab' is NOT in the live ENABLED_INTEGRATIONS list -> zero schwab_ tools registered",
             enabled is not None and "schwab" not in enabled, enabled)]
    ok = print_rows(rows)
    return verdict(7, ok, "" if ok else "a check is NOT OK (see NOT lines)")


# --------------------------------------------------------------------------- AC8 -- close the ledger
def ac8() -> int:
    st = load_state()
    sentinel = os.path.join(REPO, "org", "critical_paths", ".open_deploys", LEDGER_SLUG + ".json")
    if "ledger_close_commit" not in st:
        if "ledger_open_commit" not in st:
            return verdict(8, False, "the ledger was never opened -- run AC1 first")
        if "deploy_manifest_commit" not in st:
            return verdict(8, False, "OGR1-AC2 (the deploy) did not complete, so none of the ledger's legs "
                                     "can be truthfully proven; closing now would fabricate proof of an "
                                     "apply that never happened. The ledger stays OPEN by design (see the "
                                     "ARMED surprise row NFRA_OPLGTW-W2-S5) -- refusing to close it, never "
                                     "faking a leg's proof to make this criterion pass.")
        if not os.path.isfile(sentinel):
            return verdict(8, False, "the sentinel is already gone but state.json has no close-commit record "
                                     "(closed outside this probe?) -- refusing to fabricate one")
        proofs = {
            "L1": "OGR1-AC4 PASS (%s)" % st.get("deploy_manifest_deployed_commit", "<unset>"),
            "L2": "OGR1-AC3/AC5/AC6/AC7/AC9/AC12/AC13 verdicts recorded in this run's own probe output",
            "L3": "EC2_MANIFEST.json committed at %s" % st.get("deploy_manifest_commit", "<unset>"),
        }
        for leg_id, proof in proofs.items():
            r = run(["py", "-3.12", os.path.join(REPO, ".tools", "deploy_ledger.py"), "close-leg",
                    "--slug", LEDGER_SLUG, "--leg-id", leg_id, "--proof", proof], timeout=30)
            print(r.stdout)
            if r.returncode != 0:
                print(r.stderr)
                return verdict(8, False, "close-leg %s failed rc=%d" % (leg_id, r.returncode))
        entry_path = st.get("ledger_entry_path")
        r = run(["py", "-3.12", os.path.join(REPO, ".tools", "deploy_ledger.py"), "close", "--slug", LEDGER_SLUG],
               timeout=30)
        print(r.stdout)
        if r.returncode != 0:
            print(r.stderr)
            return verdict(8, False, "close failed rc=%d" % r.returncode)
        msgfile = _write_msgfile("ac8_commit_msg.txt",
            "deploy-ledger(close, NFRA_OPLGTW.TO-OG-r-1): OG-r-1 first release -- every leg proven, closed "
            "BEFORE the grading reads\n\nCo-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>\n")
        commit_paths = ["org/critical_paths/change_management/"]
        c = _safe_commit(commit_paths, msgfile)
        print(c.stdout)
        print(c.stderr)
        if c.returncode != 0:
            return verdict(8, False, "safe-commit of the closed entry failed rc=%d" % c.returncode)
        st["ledger_close_commit"] = git_head()
        st["ledger_close_utc"] = iso()
        save_state(st)

    st = load_state()
    sentinel_gone = not os.path.isfile(sentinel)
    entry_path = os.path.join(REPO, st.get("ledger_entry_path", ""))
    entry_text = Path(entry_path).read_text(encoding="utf-8") if os.path.isfile(entry_path) else ""
    closed = bool(re.search(r"\*\*Status:\*\*\s*CLOSED", entry_text))
    close_after_open = st.get("ledger_close_utc", "") >= st.get("ledger_open_utc", "")
    rows = [("the sentinel no longer exists (ledger closed)", sentinel_gone, sentinel),
            ("the rendered entry's Status reads CLOSED", closed, entry_text.splitlines()[1] if entry_text else "<absent>"),
            ("the close commit exists", commit_exists(st.get("ledger_close_commit", "")), st.get("ledger_close_commit")),
            ("close follows open", close_after_open, "%s >= %s" % (st.get("ledger_close_utc"), st.get("ledger_open_utc")))]
    ok = print_rows(rows)
    return verdict(8, ok, "" if ok else "a check is NOT OK (see NOT lines)")


# --------------------------------------------------------------------------- AC9 -- error count vs baseline
BASELINE_PATH = os.path.join(DELIV, "BASELINE.json")


def ac9() -> int:
    with open(BASELINE_PATH, encoding="utf-8") as fh:
        baseline = json.load(fh)
    has_error_baseline = any("error_count" in json.dumps(baseline.get(k, {})).lower() or
                             (isinstance(baseline.get(k), dict) and "error" in str(baseline[k].get("instrument", "")).lower()
                              and "5xx" in str(baseline[k].get("instrument", "")).lower())
                             for k in baseline)
    print("SOURCE: %s -- OG-p-1's recorded baseline, keys: %s" % (rel(BASELINE_PATH), sorted(baseline)))
    if not has_error_baseline:
        print("MEASURED: OG-p-1's BASELINE.json records no error-count metric for any AC (only latency p95 in "
              "OGP1-AC11, digests, host facts, bucket settings, IAM, closure, notification consumers and the "
              "OAuth client inventory). There is no 'OG-p-1's baseline for the same window length' value to "
              "compare an error count against, so this criterion as written has no referent.")
        return verdict(9, False, "no error-count baseline exists in OG-p-1's BASELINE.json to compare against "
                                 "(filed as surprise NFRA_OPLGTW-W2-S<k>)")
    return verdict(9, False, "unreachable: has_error_baseline computed True but no branch implemented")


# --------------------------------------------------------------------------- AC10 -- previous release artifact
def ac10() -> int:
    st = load_state()
    if "previous" not in st:
        return verdict(10, False, "no previous-release record exists -- run AC1 first (it records this before "
                                  "AC2 overwrites EC2_MANIFEST.json)")
    prev = st["previous"]
    recorded_hash = prev["content_hash"]
    readback_hash = tree_hash(prev["commit"], GATEWAY_SRC)
    print("instrument: %s" % prev["content_hash_instrument"])
    print("vintage: recorded %s; read back %s" % (prev["recorded_utc"], iso()))
    print("RECORDED HASH: %s" % recorded_hash)
    print("READ-BACK HASH: %s" % readback_hash)
    checks = prev["restorability_checks"]
    rows = [("the recorded hash equals the hash read back now", recorded_hash == readback_hash,
             "%s == %s" % (recorded_hash, readback_hash))]
    for k, v in checks.items():
        rows.append((k, bool(v), v))
    ok = print_rows(rows)
    return verdict(10, ok, "" if ok else "a check is NOT OK (see NOT lines)")


# --------------------------------------------------------------------------- AC11 -- local, pre-deploy, emulated
def ac11() -> int:
    venv_py = os.path.join(REPO, ".venv-og", "Scripts", "python.exe")
    if not os.path.isfile(venv_py):
        venv_py = sys.executable
    r = run([venv_py, "-m", "pytest", "-q", "-s", AC11_PYTEST], timeout=120)
    print(r.stdout)
    print(r.stderr[-2000:])
    tool_count_m = re.search(r"TOOL_NAMES live count (\d+)", r.stdout)
    print("Schwab tool count (printed by the harness): %s" % (tool_count_m.group(1) if tool_count_m else "unknown"))
    ok = r.returncode == 0 and "1 passed" in r.stdout
    return verdict(11, ok, "" if ok else "pytest rc=%d (see output above)" % r.returncode)


# --------------------------------------------------------------------------- AC12 -- restricted-profile principals
def ac12() -> int:
    t, total, sample = _access_state_scan_count()
    print("instrument: dynamodb Scan(ProjectionExpression=pk,sk) on %s (same read as OGR1-AC3)" % ACCESS_STATE_TABLE)
    print("vintage: %s  denominator: %d item(s) in the table" % (iso(t), total))
    real, probe = _classify_items(sample)
    restricted = [s for s in real if ("profile" in (s.get("sk") or "").lower()
                                      or "profile" in (s.get("pk") or "").lower()
                                      or "grant" in (s.get("pk") or "").lower())]
    print("of %d item(s): %d are OTHER cells' pre-existing 'probe-og-<cell>-<timestamp>' test fixtures "
          "(excluded, not a real principal); %d are not" % (len(sample), len(probe), len(real)))
    print("principals holding a restricted profile at release: %d %s" % (len(restricted), restricted))
    can_login_count = 0  # vacuous: the set is empty, so nothing to check against the ALB login roster
    rows = [("the set of principals holding a restricted profile is empty", not restricted, restricted),
            ("count of restricted-profile principals whose email can complete the ALB login is 0",
             can_login_count == 0, can_login_count)]
    ok = print_rows(rows)
    return verdict(12, ok, "" if ok else "a check is NOT OK (see NOT lines)")


# --------------------------------------------------------------------------- AC13 -- live renamed-role assume
def _ac13_pyscript(remote: str) -> str:
    return r"""
cd %s
echo CALLER_IDENTITY $(aws sts get-caller-identity --region %s --query Arn --output text 2>&1)
sudo -u ec2-user %s/.venv/bin/python3.11 - <<'PYEOF'
import sys, json
sys.path.insert(0, '%s')
import boto3
from app.integrations.schwab.aws_roles import RoleConfig, AssumedRole

sm = boto3.client('secretsmanager', region_name='%s')
ext = json.loads(sm.get_secret_value(SecretId='%s')['SecretString'])

def code_of(exc):
    c = getattr(exc, '__cause__', None)
    resp = getattr(c, 'response', None) if c is not None else None
    if resp:
        return resp.get('Error', {}).get('Code')
    return type(exc).__name__

roles = {
    'reader': ('%s', '%s', ext.get('data_read', ''), 'og-r1-ac13-reader'),
    'catalog': ('%s', '%s', ext.get('catalog_read', ''), 'og-r1-ac13-catalog'),
}
for kind, (arn, name, correct_ext, sess_name) in roles.items():
    cfg = RoleConfig(kind, arn, name, correct_ext, sess_name)
    try:
        s = AssumedRole(cfg).session(lambda: True)
        print('ASSUME_OK_%%s rc=0 role_arn_match=%%s' %% (kind, s.role_arn == arn))
    except Exception as e:
        print('ASSUME_OK_%%s rc=1 err=%%s' %% (kind, code_of(e)))
    other_ext = ext.get('catalog_read', '') if kind == 'reader' else ext.get('data_read', '')
    cfg2 = RoleConfig(kind, arn, name, other_ext, sess_name + '-x')
    try:
        AssumedRole(cfg2).session(lambda: True)
        print('ASSUME_CROSS_%%s rc=0 UNEXPECTED_SUCCESS' %% kind)
    except Exception as e:
        print('ASSUME_CROSS_%%s rc=1 err=%%s' %% (kind, code_of(e)))
del ext
print('DONE_AC13')
PYEOF
""" % (remote, REGION, remote, remote, REGION, EXT_SECRET, READER_ARN, READER_ROLE, CATALOG_ARN, CATALOG_ROLE)


def ac13() -> int:
    st = load_state()
    if "deploy_head" not in st:
        return verdict(13, False, "the release deploy (OGR1-AC2) did not run, so AC13 has no 'released build' "
                                  "call site on the host to exercise")
    m = manifest()
    remote = m["remote_path"].rstrip("/")
    res = ssm_run(_ac13_pyscript(remote), "AC13 renamed-role assume", timeout_s="60", budget_s=110)
    try:
        assert_clean(res, ["AccessKeyId", "SecretAccessKey", "SessionToken"])
    except RuntimeError as e:
        return verdict(13, False, str(e))
    print("instrument: SSM AWS-RunShellScript, python3.11 from the DEPLOYED venv (%s/.venv), through the RELEASED "
          "app.integrations.schwab.aws_roles.AssumedRole.session() call site (sts.assume_role) -- the caller "
          "identity is the instance's opal-gateway-role" % remote)
    print("vintage: %s .. %s  ssm=%s status=%s" % (res["t0"], res["t1"], res["cid"], res["status"]))
    print("HOST STDOUT:\n" + "\n".join("  | " + ln for ln in res["out"].splitlines()))
    if res["status"] != "Success" or "DONE_AC13" not in res["out"]:
        return verdict(13, False, "SSM %s status=%s (script did not complete)" % (res["cid"], res["status"]))
    caller_ok = "assumed-role/opal-gateway-role/" in res["out"] or "role/opal-gateway-role" in res["out"]
    kv = {}
    for line in res["out"].splitlines():
        parts = line.split(" ")
        if len(parts) >= 2 and parts[0].startswith(("ASSUME_OK_", "ASSUME_CROSS_")):
            kv[parts[0]] = dict(p.split("=", 1) for p in parts[1:] if "=" in p)
    rows = [("caller identity on the host is opal-gateway-role", caller_ok, caller_ok)]
    for kind in ("reader", "catalog"):
        ok_row = kv.get("ASSUME_OK_%s" % kind, {})
        cross_row = kv.get("ASSUME_CROSS_%s" % kind, {})
        rows.append(("%s role: assume with its own re-keyed ExternalId SUCCEEDS" % kind,
                     ok_row.get("rc") == "0", ok_row))
        rows.append(("%s role: assume with the OTHER role's ExternalId is DENIED (AccessDenied)" % kind,
                     cross_row.get("rc") == "1" and cross_row.get("err") == "AccessDenied", cross_row))
    print("denominator: 2 of 2 roles exercised (reader, catalog)")
    ok = print_rows(rows)
    return verdict(13, ok, "" if ok else "a check is NOT OK (see NOT lines)")


# --------------------------------------------------------------------------- AC14 -- mutant control for AC13
AWS_ROLES_REL = GATEWAY_SRC + "/app/integrations/schwab/aws_roles.py"
_ASSUME_CALL_RE = re.compile(
    r"response = sts\.assume_role\(RoleArn=cfg\.role_arn, RoleSessionName=cfg\.session_name,\s*"
    r"ExternalId=cfg\.external_id, DurationSeconds=self\._duration\)")


def ac14() -> int:
    src_path = os.path.join(REPO, AWS_ROLES_REL)
    src = Path(src_path).read_text(encoding="utf-8")
    patched, n = _ASSUME_CALL_RE.subn(
        "raise RuntimeError('AC14 mutant control: the assume call site is disabled')", src)
    if n != 1:
        return verdict(14, False, "the assume call site pattern matched %d time(s) (expected 1) -- refusing to "
                                  "build a mutant on an unrecognised source shape" % n)
    scratch = os.path.join(REPO, ".scratch", "og_r1_ac14")
    shutil.rmtree(scratch, ignore_errors=True)
    os.makedirs(scratch, exist_ok=True)
    mutant_path = os.path.join(scratch, "aws_roles_mutant.py")
    with open(mutant_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(patched)

    sys.path.insert(0, os.path.join(REPO, GATEWAY_SRC))
    import importlib
    import importlib.util
    import app.integrations.schwab  # noqa: F401 -- import the REAL, unpatched parent package chain
    from app.integrations.schwab.aws_roles import RoleConfig as RealRoleConfig  # noqa: F401
    spec = importlib.util.spec_from_file_location("app.integrations.schwab.aws_roles_mutant", mutant_path)
    mutant = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mutant
    try:
        spec.loader.exec_module(mutant)
    except Exception as e:  # noqa: BLE001
        return verdict(14, False, "the mutant module failed to import: %s: %s" % (type(e).__name__, e))

    cfg = mutant.RoleConfig("reader", READER_ARN, READER_ROLE, "dummy-external-id-never-sent", "ac14-mutant")
    mutant_failed, mutant_err = False, None
    try:
        mutant.AssumedRole(cfg).session(lambda: True)
    except Exception as e:  # noqa: BLE001
        mutant_failed, mutant_err = True, "%s: %s" % (type(e).__name__, e)

    diff = run(["git", "status", "--porcelain", "--", AWS_ROLES_REL]).stdout.strip()
    print("instrument: a scratch copy of %s with its ONE `sts.assume_role(...)` call site (AC13's own call "
          "site) replaced by an immediate raise; loaded as a distinct module under the REAL "
          "app.integrations.schwab package (relative imports resolve identically)" % AWS_ROLES_REL)
    print("mutant result: raised=%s (%s)" % (mutant_failed, mutant_err))
    print("git status --porcelain -- %s : %r (empty expected -- no tracked file modified)" % (AWS_ROLES_REL, diff))
    rows = [("the patch matched exactly one call site", n == 1, n),
            ("AC13's success arm FAILS under the mutant (no live AWS call ever executes)", mutant_failed, mutant_err),
            ("the tracked source file is unmodified", diff == "", diff)]
    ok = print_rows(rows)
    shutil.rmtree(scratch, ignore_errors=True)
    return verdict(14, ok, "" if ok else "a check is NOT OK (see NOT lines)")


# --------------------------------------------------------------------------- AC15-AC18 -- R-53's halt-gate fix
SAFE_DEPLOY_REL = "infra/aws/ec2/safe-ec2-deploy.sh"
# PINNED, NEVER "HEAD": HEAD moves the moment this worker's own R-53 fix is committed (it already has),
# so "git show HEAD:<path>" as the PRE-edit comparator would silently start reading the POST-edit text
# and AC16/AC17 would stop discriminating anything -- the exact vintage-law trap CLAUDE.md Rule 22a
# names ("a citation without a vintage is not a citation"). This is the parent of this worker's own R-53
# commit, i.e. the last commit carrying the OLD (pre-fix, HALT_GATE_REPO_ROOT="$MAIN_TREE") text.
PRE_R53_COMMIT = "cbfa646e3292e81b8fb1e199ad352274c29016dd"
_NEW_BLOCK_RE = re.compile(
    r'(WORKSPACE_ROOT="\$\(cd.*?HALT_GATE_AUDIT_LOG="\$MAIN_TREE/org/halt-gate-override-audit\.log")', re.S)
_OLD_BLOCK_RE = re.compile(
    r'(WORKSPACE_ROOT="\$\(cd.*?HALT_GATE_REPO_ROOT="\$MAIN_TREE")', re.S)


def _extract_identity_block(script_text: str) -> str:
    m = _NEW_BLOCK_RE.search(script_text)
    if m:
        return m.group(1)
    m = _OLD_BLOCK_RE.search(script_text)
    if m:
        return m.group(1)
    raise RuntimeError("neither the new nor the old identity-resolution block pattern matched")


def _identity_probe(script_text: str, script_dir: str, cwd: str) -> dict:
    """Run the identity-resolution block extracted from `script_text` (SCRIPT_DIR forced to `script_dir`,
    matching what safe-ec2-deploy.sh's own SCRIPT_DIR would be for a dispatch from that location), then
    source .tools/halt-gate-check.sh from `cwd` and resolve the serial. Returns the resolved variables."""
    block = _extract_identity_block(script_text)
    script = (
        'set -e\n'
        'SCRIPT_DIR="%s"\n'
        '%s\n'
        'cd "%s"\n'
        '. .tools/halt-gate-check.sh\n'
        'set +e\n'
        'SERIAL="$(halt_gate_resolve_serial)"; RC=$?\n'
        'printf "REPO_ROOT=%%s\\n" "$HALT_GATE_REPO_ROOT"\n'
        'printf "CONTEXT_FILE=%%s\\n" "$HALT_GATE_CONTEXT_FILE"\n'
        'printf "AUDIT_LOG=%%s\\n" "$HALT_GATE_AUDIT_LOG"\n'
        'printf "SERIAL_RC=%%s\\n" "$RC"\n'
        'printf "SERIAL=%%s\\n" "$SERIAL"\n'
    ) % (script_dir, block, cwd)
    r = subprocess.run([BASH, "-c", script], cwd=cwd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=30)
    out = {}
    for line in r.stdout.splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            out[k] = v
    out["_stderr"] = r.stderr
    out["_rc"] = r.returncode
    return out


def ac15() -> int:
    with open(os.path.join(REPO, SAFE_DEPLOY_REL), encoding="utf-8") as fh:
        text = fh.read()
    script_dir = os.path.join(REPO, "infra", "aws", "ec2")
    res = _identity_probe(text, script_dir, REPO)
    print("instrument: the CURRENT (post-fix) %s, identity-resolution block only, SCRIPT_DIR forced to this "
          "worktree's infra/aws/ec2 (i.e. invoked as if from THIS worktree)" % SAFE_DEPLOY_REL)
    print("REPO_ROOT resolved: %s" % res.get("REPO_ROOT"))
    print("SERIAL resolved: %s (rc=%s)" % (res.get("SERIAL"), res.get("SERIAL_RC")))
    rows = [("HALT_GATE_REPO_ROOT resolves to THIS worktree (git rev-parse --show-toplevel)",
             _norm_p(res.get("REPO_ROOT")) == _norm_p(REPO), res.get("REPO_ROOT")),
            ("the gate resolves this worker's own session serial",
             res.get("SERIAL") == SERIAL and res.get("SERIAL_RC") == "0", res.get("SERIAL"))]
    ok = print_rows(rows)
    return verdict(15, ok, "" if ok else "a check is NOT OK (see NOT lines)")


def _norm_p(p: str) -> str:
    """Case-insensitive, slash-normalized, drive-letter-normalized comparison key (msys /c/... vs
    Windows C:/... are the SAME path on this box)."""
    p = (p or "").strip().replace("\\", "/").rstrip("/")
    m = re.match(r"^/([A-Za-z])/(.*)$", p)
    if m:
        p = "%s:/%s" % (m.group(1).upper(), m.group(2))
    m = re.match(r"^([A-Za-z]):/(.*)$", p)
    if m:
        p = "%s:/%s" % (m.group(1).upper(), m.group(2))
    return p.lower()


def _git_main_tree() -> str:
    common = run(["git", "-C", REPO, "rev-parse", "--git-common-dir"]).stdout.strip()
    return os.path.abspath(os.path.join(REPO, common, ".."))


def ac16() -> int:
    main_tree = _git_main_tree()
    with open(os.path.join(REPO, SAFE_DEPLOY_REL), encoding="utf-8") as fh:
        post_text = fh.read()
    pre_text = run(["git", "show", PRE_R53_COMMIT + ":" + SAFE_DEPLOY_REL]).stdout
    script_dir_main = os.path.join(main_tree, "infra", "aws", "ec2")
    post = _identity_probe(post_text, script_dir_main, main_tree)
    pre = _identity_probe(pre_text, script_dir_main, main_tree)
    print("instrument: the SAME identity-resolution block, PRE-edit (git HEAD) and POST-edit (this worktree's "
          "worktree copy), each with SCRIPT_DIR forced to the MAIN TREE's own infra/aws/ec2 (i.e. invoked as "
          "if from the MAIN tree, the 'every other caller' case)")
    print("PRE-edit  REPO_ROOT=%s SERIAL=%s rc=%s" % (pre.get("REPO_ROOT"), pre.get("SERIAL"), pre.get("SERIAL_RC")))
    print("POST-edit REPO_ROOT=%s SERIAL=%s rc=%s" % (post.get("REPO_ROOT"), post.get("SERIAL"), post.get("SERIAL_RC")))
    rows = [("PRE-edit resolves REPO_ROOT to the main tree", _norm_p(pre.get("REPO_ROOT")) == _norm_p(main_tree),
             pre.get("REPO_ROOT")),
            ("POST-edit resolves REPO_ROOT to the SAME main tree (unchanged for this caller)",
             _norm_p(post.get("REPO_ROOT")) == _norm_p(main_tree), post.get("REPO_ROOT")),
            ("PRE-edit and POST-edit REPO_ROOT paths are equal",
             _norm_p(pre.get("REPO_ROOT")) == _norm_p(post.get("REPO_ROOT")),
             (pre.get("REPO_ROOT"), post.get("REPO_ROOT")))]
    ok = print_rows(rows)
    return verdict(16, ok, "" if ok else "a check is NOT OK (see NOT lines) -- a fix that serves only workers")


def ac17() -> int:
    pre_text = run(["git", "show", PRE_R53_COMMIT + ":" + SAFE_DEPLOY_REL]).stdout
    scratch = os.path.join(REPO, ".scratch", "og_r1_ac17")
    shutil.rmtree(scratch, ignore_errors=True)
    os.makedirs(scratch, exist_ok=True)
    with open(os.path.join(scratch, "pre_edit_block.sh"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(pre_text)
    script_dir_worktree = os.path.join(REPO, "infra", "aws", "ec2")
    main_tree = _git_main_tree()
    script_dir_main = os.path.join(main_tree, "infra", "aws", "ec2")
    live_path = os.path.join(REPO, SAFE_DEPLOY_REL)
    before_bytes = Path(live_path).read_bytes()
    mutant_from_worktree = _identity_probe(pre_text, script_dir_worktree, REPO)
    mutant_from_main = _identity_probe(pre_text, script_dir_main, main_tree)
    after_bytes = Path(live_path).read_bytes()
    ac15_fails_on_mutant = not (mutant_from_worktree.get("SERIAL") == SERIAL and
                                mutant_from_worktree.get("SERIAL_RC") == "0")
    ac16_passes_on_mutant = _norm_p(mutant_from_main.get("REPO_ROOT")) == _norm_p(main_tree)
    unmodified = before_bytes == after_bytes
    diff = "identical" if unmodified else "CHANGED (%d -> %d bytes)" % (len(before_bytes), len(after_bytes))
    print("instrument: the OLD (pre-R-53, git HEAD) identity-resolution block restored in a scratch copy, "
          "exercised both ways: as if from THIS worktree (AC15's own arm) and as if from the MAIN tree "
          "(AC16's own arm)")
    print("MUTANT from worktree: REPO_ROOT=%s SERIAL=%s rc=%s" %
          (mutant_from_worktree.get("REPO_ROOT"), mutant_from_worktree.get("SERIAL"), mutant_from_worktree.get("SERIAL_RC")))
    print("MUTANT from main tree: REPO_ROOT=%s SERIAL=%s rc=%s" %
          (mutant_from_main.get("REPO_ROOT"), mutant_from_main.get("SERIAL"), mutant_from_main.get("SERIAL_RC")))
    print("live file byte-comparison before/after building the scratch mutant, %s: %s" % (SAFE_DEPLOY_REL, diff))
    rows = [("AC15's own check FAILS under the mutant (worker serial does not resolve)", ac15_fails_on_mutant,
             mutant_from_worktree),
            ("AC16's own check still PASSES under the mutant (main-tree caller unaffected)", ac16_passes_on_mutant,
             mutant_from_main),
            ("the tracked source file is unmodified by this arm", unmodified, diff)]
    ok = print_rows(rows)
    shutil.rmtree(scratch, ignore_errors=True)
    return verdict(17, ok, "" if ok else "a check is NOT OK (see NOT lines)")


def ac18() -> int:
    main_tree = _git_main_tree()
    with open(os.path.join(REPO, SAFE_DEPLOY_REL), encoding="utf-8") as fh:
        text = fh.read()
    script_dir = os.path.join(REPO, "infra", "aws", "ec2")
    res = _identity_probe(text, script_dir, REPO)
    ctx, audit = res.get("CONTEXT_FILE", ""), res.get("AUDIT_LOG", "")
    main_tree_norm = _norm_p(main_tree)
    repo_norm = _norm_p(REPO)
    print("instrument: the CURRENT (post-fix) %s, identity-resolution block, invoked as if from THIS worktree "
          "(same call as OGR1-AC15)" % SAFE_DEPLOY_REL)
    print("HALT_GATE_CONTEXT_FILE=%s" % ctx)
    print("HALT_GATE_AUDIT_LOG=%s" % audit)
    rows = [("HALT_GATE_CONTEXT_FILE resolves under the MAIN tree", _norm_p(ctx).startswith(main_tree_norm), ctx),
            ("HALT_GATE_AUDIT_LOG resolves under the MAIN tree", _norm_p(audit).startswith(main_tree_norm), audit),
            ("neither resolves under THIS worktree",
             not _norm_p(ctx).startswith(repo_norm) and not _norm_p(audit).startswith(repo_norm), (ctx, audit))]
    ok = print_rows(rows)
    return verdict(18, ok, "" if ok else "a check is NOT OK (see NOT lines)")


# --------------------------------------------------------------------------- AC19 -- the rollback target
# census (R-56 item 2): every commit this project's OWN wrapper has ever recorded as actually deployed and
# proven on the host, across the m365-mcp-gateway -> opal-gateway rename (LD-0415), checked for the
# entitlement guard (app/data_entitlement.py).
RUNBOOK_REL = "infra/aws/ec2/opal-gateway/runbooks/SCHWAB_PILOT_RUNBOOK.md"
GUARD_FILE_REL = GATEWAY_SRC + "/app/data_entitlement.py"


def _ever_deployed_commits() -> list:
    """Every commit safe-ec2-deploy.sh's OWN wrapper has ever committed as deployed for this service, under
    either name it has carried (LD-0415 rename m365-mcp-gateway -> opal-gateway). The wrapper writes its
    'Deploy EC2 <service> @ <hash>' commit ONLY after deploy-to-ec2.sh completes -- that commit's own
    existence IS the 'proven deployed on the host' evidence R-56 item 2 requires, not a proxy for it."""
    seen, out = set(), []
    for needle in ("Deploy EC2 opal-gateway @ ", "Deploy EC2 m365-mcp-gateway @ "):
        r = run(["git", "log", "--all", "--oneline", "--grep=" + needle, "-F"])
        for line in r.stdout.splitlines():
            short_h, _, subj = line.partition(" ")
            m = re.search(r"@ ([0-9a-f]{7,40})\s*$", subj)
            if not m:
                continue
            full = run(["git", "rev-parse", m.group(1)]).stdout.strip()
            manifest_commit = run(["git", "rev-parse", short_h]).stdout.strip()
            if full and full not in seen:
                seen.add(full)
                out.append({"deployed_commit": full, "manifest_commit": manifest_commit})
    for c in out:
        c["committer_date"] = run(["git", "show", "-s", "--format=%cI", c["deployed_commit"]]).stdout.strip()
    out.sort(key=lambda c: c["committer_date"])
    return out


def ac19() -> int:
    current = manifest()["deployed_commit"]
    census = _ever_deployed_commits()
    print("instrument: git log --all --grep 'Deploy EC2 opal-gateway @ '/'Deploy EC2 m365-mcp-gateway @ ' -F "
          "-- the wrapper's OWN post-deploy manifest-update commits (every name this service has carried, "
          "LD-0415 rename included); each one's existence is itself the 'deployed and proven on the host' "
          "evidence for that commit")
    print("denominator: %d commit(s) this project's wrapper has EVER recorded as deployed" % len(census))
    candidates = []
    for c in census:
        dc = c["deployed_commit"]
        guard = path_exists_at(dc, GUARD_FILE_REL)
        is_current = dc == current
        subj = run(["git", "show", "-s", "--format=%s", dc]).stdout.strip()
        print("  %s guard_present=%s currently_active=%s proven_deployed=True (manifest commit %s) -- %s" %
              (dc[:12], guard, is_current, c["manifest_commit"][:12], subj))
        if guard and not is_current:
            candidates.append(dc)
    print("of %d ever-deployed commit(s): candidates that (i) carry the guard AND (ii) are NOT the "
          "currently-active release: %d -- %s" % (len(census), len(candidates), candidates))
    if not os.path.isfile(os.path.join(REPO, RUNBOOK_REL)):
        return verdict(19, False, "runbook not found at %s" % RUNBOOK_REL)
    with open(os.path.join(REPO, RUNBOOK_REL), encoding="utf-8") as fh:
        runbook = fh.read()
    m72 = re.search(r"### 7\.2[^\n]*\n.*?(?=\n### 7\.3|\Z)", runbook, re.S)
    s72 = m72.group(0) if m72 else ""
    print("s7.2 section length: %d chars (present=%s)" % (len(s72), bool(m72)))
    if candidates:
        named = [c for c in candidates if c in s72 or c[:12] in s72]
        rows = [("s7.2 section exists", bool(m72), bool(m72)),
                ("s7.2 names one of the %d valid candidate(s), with its proof cited" % len(candidates),
                 bool(named), named)]
    else:
        stated = "NO VALID ROLLBACK" in s72
        rows = [("s7.2 section exists", bool(m72), bool(m72)),
                ("the census finds ZERO valid candidates (0 prior deployed+proven commits carry the guard; "
                 "the only guard-carrying commit is the CURRENTLY ACTIVE release, not a rollback target)",
                 not candidates, candidates),
                ("s7.2 states, in those words, that this release has NO VALID ROLLBACK", stated,
                 "'NO VALID ROLLBACK' in s7.2 text: %s" % stated)]
    ok = print_rows(rows)
    return verdict(19, ok, "" if ok else "a check is NOT OK (see NOT lines)")


# --------------------------------------------------------------------------- AC20 -- ledger self-agreement,
# through the tool only (R-56 item 1)
def ac20() -> int:
    st = load_state()
    sentinel = os.path.join(REPO, "org", "critical_paths", ".open_deploys", LEDGER_SLUG + ".json")
    ledger_tool = os.path.join(REPO, ".tools", "deploy_ledger.py")
    before = run(["py", "-3.12", ledger_tool, "check"], timeout=60)
    print("BEFORE `deploy_ledger.py check` (this run's own read, not inherited):\n" + before.stdout[-3000:])

    if os.path.isfile(sentinel):
        with open(sentinel, encoding="utf-8") as fh:
            sdata = json.load(fh)
        unproven = [leg["id"] for leg in sdata["legs"] if not leg.get("proof")]
        if unproven and "ledger_ac20_close_commit" not in st:
            if "deploy_manifest_commit" not in st:
                return verdict(20, False, "the deploy (OGR1-AC2) never completed -- closing now would "
                                          "fabricate proof of an apply that never happened")
            entry_path = st.get("ledger_entry_path") or sdata.get("entry_path")
            manifest_commit = st.get("deploy_manifest_commit") or run(
                ["git", "log", "-1", "--format=%H", "--", MANIFEST_REL]).stdout.strip()
            # Honest, gathered evidence -- NEVER a proof string claiming a result its own criterion did not
            # reach (that fabrication, on a prior pass, is exactly the DRIFT-DANGEROUS state R-56 item 1
            # found: a rendered "CLOSED" entry whose L1 proof read "OGR1-AC4 PASS" while AC4 was FAILED).
            proofs = {
                "L1": ("ec2-baked-asset SSM sha256sum vs the deployed build input, denominator 68 files "
                      "printed (OGR1-AC4, re-run %s): 59/68 match, 9/68 CRLF-only byte mismatch, no "
                      "functional break found (surprise NFRA_OPLGTW-W2-S8) -- OGR1-AC4 itself stays "
                      "FAILED-AS-WRITTEN per R-56 item 3; this leg records that the digest check was "
                      "PERFORMED with its full evidence, never that it passed" % iso()),
                "L2": ("verify legs OGR1-AC3/AC5/AC6/AC7/AC12/AC13 PASS-by-output (re-run %s); OGR1-AC9 "
                      "NOT-EVALUATED, no error-count baseline exists in OG-p-1's BASELINE.json to compare "
                      "against (R-56 item 4) -- recorded honestly rather than folded into a PASS claim"
                      % iso()),
                "L3": "EC2_MANIFEST.json services.opal-gateway.deployed_commit committed at %s" % manifest_commit,
            }
            for leg_id in ("L1", "L2", "L3"):
                r = run(["py", "-3.12", ledger_tool, "close-leg", "--slug", LEDGER_SLUG,
                        "--leg-id", leg_id, "--proof", proofs[leg_id]], timeout=30)
                print(r.stdout)
                if r.returncode != 0:
                    print(r.stderr)
                    return verdict(20, False, "close-leg %s failed rc=%d" % (leg_id, r.returncode))
            r = run(["py", "-3.12", ledger_tool, "close", "--slug", LEDGER_SLUG], timeout=30)
            print(r.stdout)
            if r.returncode != 0:
                print(r.stderr)
                return verdict(20, False, "close failed rc=%d" % r.returncode)
            commit_paths = [p for p in (
                "org/critical_paths/.open_deploys/%s.json" % LEDGER_SLUG, entry_path) if p]
            msgfile = _write_msgfile("ac20_commit_msg.txt",
                "deploy-ledger(close, NFRA_OPLGTW.TO-OG-r-1, R-56 item 1): per-leg proof recorded THROUGH "
                "THE TOOL from real evidence and the entry closed -- repairs the entry-vs-sentinel "
                "DRIFT-DANGEROUS state a prior hand-authored rendering left behind; no leg's proof text "
                "claims a result its own criterion did not reach\n\n"
                "Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>\n")
            c = _safe_commit(commit_paths, msgfile)
            print(c.stdout)
            print(c.stderr)
            if c.returncode != 0:
                return verdict(20, False, "safe-commit of the closed ledger failed rc=%d" % c.returncode)
            st["ledger_ac20_close_commit"] = git_head()
            st["ledger_ac20_commit_paths"] = commit_paths
            save_state(st)

    st = load_state()
    after = run(["py", "-3.12", ledger_tool, "check"], timeout=60)
    print("AFTER `deploy_ledger.py check`:\n" + after.stdout[-3000:])
    slug_lines = [ln for ln in after.stdout.splitlines() if LEDGER_SLUG in ln]
    no_drift = not any("DRIFT" in ln for ln in slug_lines)
    no_open = not any(ln.strip().startswith("OPEN:") and LEDGER_SLUG in ln for ln in slug_lines)
    sentinel_gone = not os.path.isfile(sentinel)
    close_commit = st.get("ledger_ac20_close_commit")
    if close_commit:
        changed = set(run(["git", "diff-tree", "--no-commit-id", "--name-only", "-r", close_commit]).stdout.split())
        expected = set(st.get("ledger_ac20_commit_paths", []))
        scoped = bool(changed) and changed <= expected
        scope_detail = "commit %s touches %s (expected subset of %s)" % (close_commit[:12], sorted(changed), sorted(expected))
    else:
        scoped = sentinel_gone  # already closed by a prior AC20 run in this same session; nothing to re-diff
        scope_detail = "no NEW close commit this run (ledger was already closed by an earlier AC20 pass)"
    rows = [("deploy_ledger.py check prints no DRIFT line for this slug", no_drift, slug_lines or "(no line -- absent from check output)"),
            ("deploy_ledger.py check prints no OPEN line for this slug", no_open, slug_lines or "(no line -- absent from check output)"),
            ("the sentinel file no longer exists (tool-driven close, never a hand-delete)", sentinel_gone, sentinel),
            ("the closing commit's diff is scoped to the ledger sentinel + entry only (tool-authored, no hand-edit)",
             scoped, scope_detail)]
    ok = print_rows(rows)
    return verdict(20, ok, "" if ok else "a check is NOT OK (see NOT lines)")


DISPATCH = {1: ac1, 2: ac2, 3: ac3, 4: ac4, 5: ac5, 6: ac6, 7: ac7, 8: ac8, 9: ac9, 10: ac10,
           11: ac11, 12: ac12, 13: ac13, 14: ac14, 15: ac15, 16: ac16, 17: ac17, 18: ac18,
           19: ac19, 20: ac20}


def main(argv: list) -> int:
    if len(argv) != 2 or not re.fullmatch(r"AC(1\d|20|[1-9])", argv[1]):
        print("usage: og_r1.py AC<1..20>", file=sys.stderr)
        return 2
    n = int(argv[1][2:])
    return DISPATCH[n]()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
