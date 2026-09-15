"""TX-p-1 -- the pre-change baseline, READ ONLY (MDPF_TAXSMA round 1, 0.9.0_WK_MDPF_TAXSMA~6).

Usage (from the worktree root):  py -3.12 <this file> AC<n>     n = 1..10

One criterion per invocation. Prints its measurement with vintage (HEAD + UTC run time) and
denominator, then EXACTLY ONE line:  VERDICT: PASS-TXP1-AC<n>  or  VERDICT: FAIL-TXP1-AC<n> <reason>.

Every AWS call goes through the workspace `.tools/aws` shim (via the Git Bash resolver, never bare
`bash`) and is appended to `command_log.jsonl` in this deliverables folder BEFORE it runs, so a call
that crashes is still in the log. AC10 grades that log and makes no AWS call itself.

Private data: no object body is written to the repository. Served JSON and deployed zips land in
`<worktree>/.scratch/tx_p_1/` only; numeric values of the served `tax` node are printed MASKED
(zero / nonzero / null), never as amounts. The Lambda presigned code URL is never printed or logged.
"""
from __future__ import annotations

import ast
import base64
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
DELIV = HERE.parent
WS = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"],
                                  cwd=str(HERE)).decode().strip())
HEAD = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=str(WS)).decode().strip()
SCRATCH = WS / ".scratch" / "tx_p_1"
LOG = DELIV / "command_log.jsonl"
ACCOUNT = "313476888478"
REGION = "us-east-1"
READ_VERBS = ("describe", "get", "list", "head")

sys.path.insert(0, str(WS / ".tools"))
from git_bash_resolver import git_bash  # noqa: E402

CRIT = "?"


def utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def log_call(service: str, op: str, args: str) -> None:
    rec = {"utc": utc(), "criterion": CRIT, "service": service, "operation": op,
           "args": args[:400], "via": ".tools/aws", "head": HEAD[:10]}
    with open(LOG, "a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(rec, sort_keys=True) + "\n")


def aws(service: str, op: str, *args: str, timeout: int = 60):
    """Run one AWS CLI call through the shim. Returns (rc, parsed_json_or_None, stderr)."""
    bash = git_bash()
    if not bash:
        raise SystemExit("ERROR: no Git Bash resolved -- refusing to fall back to bare bash")
    log_call(service, op, " ".join(args))
    argv = [bash, str(WS / ".tools" / "aws"), service, op, *args,
            "--region", REGION, "--output", "json"]
    env = dict(os.environ, AWS_PAGER="")
    try:
        p = subprocess.run(argv, capture_output=True, timeout=timeout, env=env, cwd=str(WS))
    except subprocess.TimeoutExpired:
        return 124, None, "TIMEOUT after %ss" % timeout
    out = p.stdout.decode("utf-8", "replace")
    err = p.stderr.decode("utf-8", "replace").strip()
    data = None
    if p.returncode == 0:
        data = json.loads(out) if out.strip() else {}
    return p.returncode, data, err


def grain() -> bool:
    rc, d, err = aws("sts", "get-caller-identity")
    acct = (d or {}).get("Account")
    print("GRAIN: sts get-caller-identity rc=%s Account=%s (required %s) region=%s at %s"
          % (rc, acct, ACCOUNT, REGION, utc()))
    if rc != 0:
        print("  stderr: %s" % err[:300])
    return acct == ACCOUNT


def banner(n: int) -> None:
    print("TX-p-1 AC%d | worktree HEAD %s | run_at %s | probe %s" % (n, HEAD, utc(), Path(__file__).name))


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def b64sha(p: Path) -> str:
    return base64.b64encode(hashlib.sha256(p.read_bytes()).digest()).decode()


def cj(o) -> str:
    return json.dumps(o, sort_keys=True, separators=(",", ":"))


# ------------------------------------------------------------------------------------------ AC1
SERVED_BUCKET = "opal-data-portal-v2"
SERVED_KEYS = [("49financial", "platinum/mdpf/49financial/category-views.json"),
               ("global", "platinum/mdpf/global/category-views.json")]
ID_KEYS = ("id", "key", "member_id", "category_id", "slug", "code")


def find_tax(node, path="$", found=None, counter=None):
    if found is None:
        found, counter = [], [0]
    counter[0] += 1
    if isinstance(node, dict):
        if any(node.get(k) == "tax" for k in ID_KEYS):
            found.append((path, node))
        for k, v in node.items():
            if k == "tax" and isinstance(v, dict):
                found.append(("%s.tax" % path, v))
            if isinstance(v, (dict, list)):
                find_tax(v, "%s.%s" % (path, k), found, counter)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            find_tax(v, "%s[%d]" % (path, i), found, counter)
    return found, counter[0]


def masked(v) -> str:
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "bool=%s" % v
    if isinstance(v, (int, float)):
        return "number(zero)" if v == 0 else "number(nonzero)"
    if isinstance(v, str):
        return "str=%r" % v if len(v) <= 80 else "str(len=%d)" % len(v)
    if isinstance(v, list):
        kinds = sorted({type(x).__name__ for x in v})
        return "list(len=%d, item_types=%s)" % (len(v), kinds)
    if isinstance(v, dict):
        return "dict(keys=%s)" % sorted(v)
    return type(v).__name__


def ac1() -> tuple:
    if not grain():
        return False, "account grain not %s" % ACCOUNT
    SCRATCH.mkdir(parents=True, exist_ok=True)
    ok = True
    reasons = []
    for scope, key in SERVED_KEYS:
        out = SCRATCH / ("category-views.%s.json" % scope)
        if out.exists():
            out.unlink()
        rc, d, err = aws("s3api", "get-object", "--bucket", SERVED_BUCKET, "--key", key, str(out).replace("\\", "/"))
        print("\n[%s] s3://%s/%s  (s3api get-object, rc=%s, read_at %s)" % (scope, SERVED_BUCKET, key, rc, utc()))
        if rc != 0 or not out.exists():
            print("  stderr: %s" % err[:300])
            ok = False
            reasons.append("%s unreadable" % scope)
            continue
        raw = out.read_bytes()
        print("  VersionId     : %s" % d.get("VersionId", "ABSENT (unversioned or null)"))
        print("  LastModified  : %s (UTC, as returned by s3api)" % d.get("LastModified"))
        print("  ETag          : %s" % d.get("ETag"))
        print("  ContentLength : %s (bytes on disk %d)" % (d.get("ContentLength"), len(raw)))
        print("  CacheControl  : %s | ContentType %s" % (d.get("CacheControl"), d.get("ContentType")))
        print("  SHA-256       : %s" % hashlib.sha256(raw).hexdigest())
        doc = json.loads(raw)
        top = sorted(doc) if isinstance(doc, dict) else type(doc).__name__
        print("  document top-level keys: %s" % top)
        if isinstance(doc, dict):
            for f in ("taxsma_contract_version", "taxsma_coverage"):
                print("  contract wire_extension document field %-24s: %s" % (f, "PRESENT" if f in doc else "ABSENT"))
        found, walked = find_tax(doc)
        print("  tax node(s) found: %d (JSON nodes walked: %d)" % (len(found), walked))
        if not found:
            ok = False
            reasons.append("%s has no tax node" % scope)
        for path, node in found:
            print("  tax node at %s -- %d field(s):" % (path, len(node)))
            for k in sorted(node):
                print("    %-28s %s" % (k, masked(node[k])))
            print("    contract node_field 'coverage': %s" % ("PRESENT" if "coverage" in node else "ABSENT"))
    return ok, "; ".join(reasons)


# ------------------------------------------------------------------------------------------ AC2
FUNCS = [("mdpf-gold-lambda", "infra/aws/lambda/mdpf-pipeline/mdpf-gold-lambda/build_package.py"),
         ("opal-assets-mdpf-portal-publisher",
          "infra/aws/lambda/opal-assets/opal-assets-mdpf-portal-publisher/build_package.py")]


def zip_members(p: Path) -> dict:
    with zipfile.ZipFile(p) as zf:
        return {i.filename: hashlib.sha256(zf.read(i.filename)).hexdigest() for i in zf.infolist()}


def build(builder: str, pin: str, out: Path) -> tuple:
    for f in (out, Path(str(out).replace(".zip", ".BUILD_MANIFEST.json"))):
        if f.exists():
            f.unlink()
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run([sys.executable, str(WS / builder), "--pin", pin, "--out", str(out)],
                       capture_output=True, cwd=str(WS), timeout=90, env=env)
    tail = (p.stdout.decode("utf-8", "replace") + p.stderr.decode("utf-8", "replace")).strip().splitlines()
    return p.returncode, tail[-4:]


def ac2() -> tuple:
    if not grain():
        return False, "account grain not %s" % ACCOUNT
    SCRATCH.mkdir(parents=True, exist_ok=True)
    ok = True
    reasons = []
    for fn, builder in FUNCS:
        print("\n[%s] builder %s" % (fn, builder))
        rc, d, err = aws("lambda", "get-function", "--function-name", fn)
        if rc != 0:
            print("  get-function rc=%s stderr: %s" % (rc, err[:300]))
            ok = False
            reasons.append("%s get-function failed" % fn)
            continue
        cfg = d["Configuration"]
        live = cfg["CodeSha256"]
        print("  LIVE (lambda get-function, read_at %s): CodeSha256=%s LastModified=%s CodeSize=%s Runtime=%s"
              % (utc(), live, cfg.get("LastModified"), cfg.get("CodeSize"), cfg.get("Runtime")))
        env_vars = (cfg.get("Environment") or {}).get("Variables") or {}
        for k in ("MDPF_GOLD_COMMIT", "MDPF_PUBLISHER_COMMIT"):
            if k in env_vars:
                print("  live env %s=%s" % (k, env_vars[k]))
        dep = SCRATCH / ("%s.deployed.zip" % fn)
        log_call("lambda", "get-function:Code.Location-presigned-s3-get", "presigned URL redacted; function %s" % fn)
        with urllib.request.urlopen(d["Code"]["Location"], timeout=60) as r:
            dep.write_bytes(r.read())
        dep_b64 = b64sha(dep)
        print("  deployed zip downloaded: %d bytes, b64 sha256=%s -> %s the live CodeSha256 (download fidelity)"
              % (dep.stat().st_size, dep_b64, "EQUALS" if dep_b64 == live else "DIFFERS FROM"))
        dep_m = zip_members(dep)
        dep_sv = None
        if "BUILD_MANIFEST.json" in dep_m:
            with zipfile.ZipFile(dep) as zf:
                dep_sv = json.loads(zf.read("BUILD_MANIFEST.json")).get("source_vintage")
        print("  deployed in-zip BUILD_MANIFEST source_vintage: %s" % dep_sv)
        out = SCRATCH / ("%s.HEAD.zip" % fn)
        brc, tail = build(builder, HEAD, out)
        print("  HEAD build (--pin %s): rc=%s | %s" % (HEAD, brc, " || ".join(tail)))
        if brc != 0 or not out.exists():
            ok = False
            reasons.append("%s HEAD build refused rc=%s" % (fn, brc))
            continue
        head_b64 = b64sha(out)
        verdict = "MATCH" if head_b64 == live else "MISMATCH"
        print("  HEAD zip b64 sha256=%s vs live CodeSha256=%s" % (head_b64, live))
        print("  RESULT %s: %s" % (fn, verdict))
        head_m = zip_members(out)
        names = sorted(set(dep_m) | set(head_m))
        same = [n for n in names if dep_m.get(n) == head_m.get(n)]
        diff = [n for n in names if n in dep_m and n in head_m and dep_m[n] != head_m[n]]
        only_dep = [n for n in names if n not in head_m]
        only_head = [n for n in names if n not in dep_m]
        print("  members: %d union | %d identical | %d differ %s | %d deployed-only %s | %d HEAD-only %s"
              % (len(names), len(same), len(diff), diff, len(only_dep), only_dep, len(only_head), only_head))
        # Discrimination arm: the same comparator against a build at the DEPLOYED pin. The pin
        # STRING is taken as the deployed manifest recorded it (source_vintage.pin): the builder
        # stamps that string verbatim into BUILD_MANIFEST.json, so a 10-char pin rebuilt as the
        # 40-char commit differs in one manifest field and in nothing else.
        pin = (dep_sv or {}).get("pin") or (dep_sv or {}).get("commit")
        if pin:
            t = subprocess.run(["git", "cat-file", "-t", pin], capture_output=True, cwd=str(WS))
            if t.stdout.decode().strip() == "commit":
                cout = SCRATCH / ("%s.deployedpin.zip" % fn)
                crc, ctail = build(builder, pin, cout)
                if crc == 0 and cout.exists():
                    cb = b64sha(cout)
                    print("  CONTROL build at deployed pin %s: b64=%s -> %s"
                          % (pin[:10], cb, "MATCH" if cb == live else "MISMATCH"))
                else:
                    print("  CONTROL build at deployed pin %s: builder rc=%s (%s) -- control NOT-EVALUATED"
                          % (pin[:10], crc, " || ".join(ctail)))
            else:
                print("  CONTROL: deployed pin %s does not resolve in this repository -- NOT-EVALUATED" % pin[:10])
    return ok, "; ".join(reasons)


# ------------------------------------------------------------------------------------------ AC3
SCHEDULES = [("mdpf-scheduled-floor", "mdpf-scheduled-floor", None),
             ("publisher 13:50 UTC trigger", "opal-assets-mdpf-portal-publisher", "cron(50 13 * * ? *)")]


def ac3() -> tuple:
    if not grain():
        return False, "account grain not %s" % ACCOUNT
    ok = True
    reasons = []
    for label, prefix, want in SCHEDULES:
        rc, d, err = aws("scheduler", "list-schedules", "--name-prefix", prefix)
        items = (d or {}).get("Schedules", [])
        print("\n[%s] scheduler list-schedules --name-prefix %s: rc=%s, %d schedule(s): %s"
              % (label, prefix, rc, len(items), [(s.get("GroupName"), s.get("Name")) for s in items]))
        if rc != 0 or not items:
            ok = False
            reasons.append("%s not listed" % prefix)
            continue
        for s in items:
            rc2, g, err2 = aws("scheduler", "get-schedule", "--name", s["Name"], "--group-name", s.get("GroupName", "default"))
            if rc2 != 0:
                print("  get-schedule %s rc=%s %s" % (s["Name"], rc2, err2[:200]))
                ok = False
                reasons.append("%s unreadable" % s["Name"])
                continue
            tgt = g.get("Target") or {}
            print("  get-schedule %s (group %s, read_at %s)" % (g.get("Name"), g.get("GroupName"), utc()))
            print("    State              : %s" % g.get("State"))
            print("    ScheduleExpression : %s  timezone=%s" % (g.get("ScheduleExpression"), g.get("ScheduleExpressionTimezone")))
            print("    FlexibleTimeWindow : %s" % cj(g.get("FlexibleTimeWindow")))
            print("    Target.Arn         : %s" % tgt.get("Arn"))
            print("    Target.RoleArn     : %s" % tgt.get("RoleArn"))
            print("    Target.Input       : %s" % tgt.get("Input"))
            print("    LastModificationDate: %s" % g.get("LastModificationDate"))
            if want:
                enc = g.get("ScheduleExpression") == want and g.get("ScheduleExpressionTimezone") in ("UTC", None)
                print("    encodes 13:50 UTC  : %s (expected %s tz UTC)" % ("YES" if enc else "NO", want))
            if not (g.get("State") and g.get("ScheduleExpression") and tgt.get("Arn")):
                ok = False
                reasons.append("%s missing state/expression/target" % s["Name"])
    return ok, "; ".join(reasons)


# ------------------------------------------------------------------------------------------ AC4
ROLES = ["mdpf-gold-lambda-role", "opal-assets-mdpf-egress-publisher-role"]


def as_doc(x):
    if isinstance(x, str):
        return json.loads(urllib.parse.unquote(x))
    return x


def ac4() -> tuple:
    if not grain():
        return False, "account grain not %s" % ACCOUNT
    ok = True
    reasons = []
    for role in ROLES:
        rc, d, err = aws("iam", "get-role", "--role-name", role)
        print("\n[%s] iam get-role rc=%s read_at %s" % (role, rc, utc()))
        if rc != 0:
            print("  stderr: %s" % err[:300])
            ok = False
            reasons.append("%s unreadable" % role)
            continue
        r = d["Role"]
        trust = as_doc(r["AssumeRolePolicyDocument"])
        print("  Arn=%s CreateDate=%s MaxSession=%s" % (r["Arn"], r.get("CreateDate"), r.get("MaxSessionDuration")))
        print("  PermissionsBoundary: %s" % cj(r.get("PermissionsBoundary")))
        print("  TRUST sha256=%s %s" % (hashlib.sha256(cj(trust).encode()).hexdigest()[:16], cj(trust)))
        rc1, li, e1 = aws("iam", "list-role-policies", "--role-name", role)
        inline = (li or {}).get("PolicyNames", [])
        rc2, la, e2 = aws("iam", "list-attached-role-policies", "--role-name", role)
        attached = (la or {}).get("AttachedPolicies", [])
        if rc1 != 0 or rc2 != 0:
            ok = False
            reasons.append("%s policy listing failed" % role)
        read = 0
        for name in inline:
            rc3, gp, e3 = aws("iam", "get-role-policy", "--role-name", role, "--policy-name", name)
            if rc3 != 0:
                print("  INLINE %s rc=%s %s" % (name, rc3, e3[:200]))
                continue
            doc = as_doc(gp["PolicyDocument"])
            read += 1
            print("  INLINE %s (%d statement(s)) sha256=%s\n    %s"
                  % (name, len(doc.get("Statement", [])), hashlib.sha256(cj(doc).encode()).hexdigest()[:16], cj(doc)))
        for ap in attached:
            arn = ap["PolicyArn"]
            rc4, gp, e4 = aws("iam", "get-policy", "--policy-arn", arn)
            if rc4 != 0:
                print("  ATTACHED %s get-policy rc=%s %s" % (arn, rc4, e4[:200]))
                continue
            ver = gp["Policy"]["DefaultVersionId"]
            rc5, pv, e5 = aws("iam", "get-policy-version", "--policy-arn", arn, "--version-id", ver)
            if rc5 != 0:
                print("  ATTACHED %s get-policy-version rc=%s %s" % (arn, rc5, e5[:200]))
                continue
            doc = as_doc(pv["PolicyVersion"]["Document"])
            read += 1
            print("  ATTACHED %s version %s (%d statement(s)) sha256=%s\n    %s"
                  % (arn, ver, len(doc.get("Statement", [])), hashlib.sha256(cj(doc).encode()).hexdigest()[:16], cj(doc)))
        total = len(inline) + len(attached)
        print("  DENOMINATOR %s: trust 1 of 1; policy documents read %d of %d (%d inline %s, %d attached %s)"
              % (role, read, total, len(inline), inline, len(attached), [a["PolicyName"] for a in attached]))
        if read != total:
            ok = False
            reasons.append("%s read %d of %d policies" % (role, read, total))
    return ok, "; ".join(reasons)


# ------------------------------------------------------------------------------------------ AC5
FIRM_BUCKET = "opal-data-49financial"


def ac5() -> tuple:
    if not grain():
        return False, "account grain not %s" % ACCOUNT
    ok = True
    reasons = []
    print("\n[%s] read_at %s" % (FIRM_BUCKET, utc()))
    rc, d, err = aws("s3api", "get-bucket-versioning", "--bucket", FIRM_BUCKET)
    print("  versioning (get-bucket-versioning rc=%s): Status=%s MFADelete=%s"
          % (rc, (d or {}).get("Status", "ABSENT (never enabled)"), (d or {}).get("MFADelete", "ABSENT")))
    ok &= rc == 0
    rc, d, err = aws("s3api", "get-bucket-encryption", "--bucket", FIRM_BUCKET)
    rules = ((d or {}).get("ServerSideEncryptionConfiguration") or {}).get("Rules", [])
    print("  default encryption (get-bucket-encryption rc=%s): %d rule(s) %s" % (rc, len(rules), cj(rules)))
    if rc != 0:
        print("    stderr: %s" % err[:200])
    ok &= rc == 0
    rc, d, err = aws("s3api", "get-public-access-block", "--bucket", FIRM_BUCKET)
    pab = (d or {}).get("PublicAccessBlockConfiguration") or {}
    flags = ["BlockPublicAcls", "IgnorePublicAcls", "BlockPublicPolicy", "RestrictPublicBuckets"]
    print("  public-access-block (get-public-access-block rc=%s): %d of 4 flags returned" % (rc, sum(f in pab for f in flags)))
    for f in flags:
        print("    %-22s %s" % (f, pab.get(f, "ABSENT")))
    if rc != 0 or not all(f in pab for f in flags):
        ok = False
        reasons.append("public-access-block incomplete")
    rc, d, err = aws("s3api", "get-bucket-policy", "--bucket", FIRM_BUCKET)
    if rc != 0:
        print("  bucket policy (get-bucket-policy rc=%s): %s" % (rc, err[:300]))
        ok = False
        reasons.append("bucket policy unreadable")
    else:
        pol = json.loads(d["Policy"])
        st = pol.get("Statement", [])
        st = st if isinstance(st, list) else [st]
        deny = [s for s in st if s.get("Effect") == "Deny"]
        print("  bucket policy (get-bucket-policy rc=0): sha256=%s, %d statement(s), Deny %d of %d, Allow %d of %d"
              % (hashlib.sha256(cj(pol).encode()).hexdigest()[:16], len(st), len(deny), len(st),
                 len(st) - len(deny), len(st)))
        for i, s in enumerate(deny, 1):
            print("  DENY %d/%d Sid=%s" % (i, len(deny), s.get("Sid")))
            for k in ("Principal", "NotPrincipal", "Action", "NotAction", "Resource", "NotResource", "Condition"):
                if k in s:
                    print("    %-12s %s" % (k, cj(s[k])))
        for s in st:
            if s.get("Effect") != "Deny":
                print("  (allow, not itemized by the criterion) Sid=%s" % s.get("Sid"))
    return bool(ok), "; ".join(reasons)


# ------------------------------------------------------------------------------------------ AC6
def ac6() -> tuple:
    if not grain():
        return False, "account grain not %s" % ACCOUNT
    rc, d, err = aws("iam", "get-role", "--role-name", "mdpf-49f-taxsma-role")
    print("\n[mdpf-49f-taxsma-role] iam get-role rc=%s read_at %s" % (rc, utc()))
    print("  stderr: %s" % (err or "(empty)")[:300])
    nse = rc != 0 and "NoSuchEntity" in err
    rcp, dp, errp = aws("iam", "get-role", "--role-name", "mdpf-gold-lambda-role")
    print("  POSITIVE CONTROL: iam get-role mdpf-gold-lambda-role rc=%s (an existing role is returned by the same instrument)" % rcp)
    print("  denominator: 1 of 1 target role queried; 1 of 1 control role queried")
    if not nse:
        return False, "get-role did not return NoSuchEntity (rc=%s)" % rc
    if rcp != 0:
        return False, "positive control failed rc=%s -- NoSuchEntity not discriminating" % rcp
    return True, ""


# ------------------------------------------------------------------------------------------ AC7
CENSUS_TMPL = r"""set -u
R='%(root)s'
[ -d "$R" ] || { echo "CENSUS ROOT_MISSING $R"; exit 3; }
cd "$R"
lst0() { find . \( -name venv -o -name .venv -o -name __pycache__ -o -name node_modules -o -name .git -o -name site-packages \) -prune -o -type f "$@" -print0; }
echo "CENSUS ROOT=$R"
echo "CENSUS PRUNED=venv,.venv,__pycache__,node_modules,.git,site-packages"
echo "CENSUS FILES_ALL=$(lst0 | tr -cd '\0' | wc -c)"
echo "CENSUS FILES_PY=$(lst0 -name '*.py' | tr -cd '\0' | wc -c)"
echo "CENSUS GREP_ERRORS=$(lst0 | xargs -0 -r grep -l -F 'taxsma-workbook' -- 2>&1 >/dev/null | wc -l)"
echo "CENSUS FILES_MATCHING_TAXSMA_WORKBOOK=$(lst0 | xargs -0 -r grep -l -F 'taxsma-workbook' -- | wc -l)"
echo "CENSUS FILES_MATCHING_TAXSMA_ANYCASE=$(lst0 | xargs -0 -r grep -l -i -F 'taxsma' -- | wc -l)"
echo "CENSUS ROUTE_LINES_WITH_TAXSMA_WORKBOOK=$(lst0 -name '*.py' | xargs -0 -r grep -h -F 'taxsma-workbook' -- | grep -c -F 'Route(')"
echo "CENSUS CONTROL_ROUTE_DECL_LINES=$(lst0 -name '*.py' | xargs -0 -r grep -h -c -F 'Route(' -- | awk '{s+=$1} END{print s+0}')"
echo "CENSUS CONTROL_HEALTH_ROUTE=$(grep -c -F 'Route("/health"' app/server.py)"
echo "CENSUS SERVER_PY_MD5=$(md5sum app/server.py | cut -d' ' -f1)"
echo "CENSUS SERVER_PY_MTIME=$(stat -c %%y app/server.py)"
echo "--- lines containing taxsma-workbook (max 40) ---"
lst0 | xargs -0 -r grep -n -F 'taxsma-workbook' -- | head -40
echo "--- end ---"
"""


def ac7() -> tuple:
    if not grain():
        return False, "account grain not %s" % ACCOUNT
    man = json.loads((WS / "infra/aws/ec2/EC2_MANIFEST.json").read_text(encoding="utf-8"))

    def walk(o):
        if isinstance(o, dict):
            if "opal-gateway" in o and isinstance(o["opal-gateway"], dict) and "instance_id" in o["opal-gateway"]:
                return o["opal-gateway"]
            for v in o.values():
                r = walk(v)
                if r:
                    return r
        return None
    gw = walk(man)
    iid, root = gw["instance_id"], gw["remote_path"]
    print("Gateway host from infra/aws/ec2/EC2_MANIFEST.json @%s: instance_id=%s remote_path=%s deployed_commit=%s"
          % (HEAD[:10], iid, root, gw.get("deployed_commit")))
    rc, d, err = aws("ssm", "describe-instance-information", "--filters", "Key=InstanceIds,Values=%s" % iid)
    info = (d or {}).get("InstanceInformationList", [])
    print("ssm describe-instance-information rc=%s: %d record(s) %s" % (rc, len(info), [
        (i.get("PingStatus"), i.get("PlatformName"), i.get("AgentVersion")) for i in info]))
    if not info or info[0].get("PingStatus") != "Online":
        return False, "instance not Online in SSM"
    SCRATCH.mkdir(parents=True, exist_ok=True)
    script = CENSUS_TMPL % {"root": root}
    req = {"DocumentName": "AWS-RunShellScript", "InstanceIds": [iid],
           "Comment": "TX-p-1 read-only census (0.9.0_WK_MDPF_TAXSMA~6)",
           "TimeoutSeconds": 60,
           "Parameters": {"commands": script.splitlines(), "executionTimeout": ["60"]}}
    reqf = SCRATCH / "ssm_census_request.json"
    reqf.write_text(json.dumps(req), encoding="utf-8")
    print("census script sha256=%s (%d lines; every command reads, none writes)"
          % (hashlib.sha256(script.encode()).hexdigest()[:16], len(script.splitlines())))
    rc, d, err = aws("ssm", "send-command", "--cli-input-json", "file://%s" % str(reqf).replace("\\", "/"))
    if rc != 0:
        print("ssm send-command rc=%s %s" % (rc, err[:300]))
        return False, "send-command failed rc=%s" % rc
    cid = d["Command"]["CommandId"]
    print("ssm send-command rc=0 CommandId=%s at %s" % (cid, utc()))
    inv = None
    for _ in range(25):
        time.sleep(3)
        rc, inv, err = aws("ssm", "get-command-invocation", "--command-id", cid, "--instance-id", iid)
        if rc == 0 and inv.get("Status") not in ("Pending", "InProgress", "Delayed"):
            break
    if not inv:
        return False, "no invocation readable"
    print("ssm get-command-invocation Status=%s ResponseCode=%s ExecutionEnd=%s"
          % (inv.get("Status"), inv.get("ResponseCode"), inv.get("ExecutionEndDateTime")))
    outtxt = inv.get("StandardOutputContent", "")
    errtxt = inv.get("StandardErrorContent", "")
    print("----- host stdout -----\n%s\n----- host stderr (%d chars) -----\n%s" % (outtxt.rstrip(), len(errtxt), errtxt[:600]))
    vals = dict(re.findall(r"^CENSUS (\w+)=(.*)$", outtxt, re.M))
    if inv.get("Status") != "Success":
        return False, "census status %s" % inv.get("Status")
    need = ["FILES_ALL", "FILES_PY", "FILES_MATCHING_TAXSMA_WORKBOOK", "ROUTE_LINES_WITH_TAXSMA_WORKBOOK",
            "CONTROL_ROUTE_DECL_LINES"]
    if not all(k in vals for k in need):
        return False, "census fields missing %s" % [k for k in need if k not in vals]
    ctrl = int(vals["CONTROL_ROUTE_DECL_LINES"] or 0)
    reg = int(vals["ROUTE_LINES_WITH_TAXSMA_WORKBOOK"] or 0)
    print("RESULT: route string 'taxsma-workbook' registered: %s (%d Route( line(s) carry it); files containing the "
          "string: %s of %s files (%s .py); positive control: %d Route( declaration line(s) found by the same census"
          % ("YES" if reg else "NO", reg, vals["FILES_MATCHING_TAXSMA_WORKBOOK"], vals["FILES_ALL"],
             vals["FILES_PY"], ctrl))
    if ctrl == 0:
        return False, "positive control found 0 Route( lines -- census cannot discriminate"
    return True, ""


# ------------------------------------------------------------------------------------------ AC8
B00 = "data/assets/scripts/gold/runners_49f/b00_canonical_valuation.py"
RCM = "data/assets/scripts/gold/runners_49f/runner_common.py"


def consts(path: str, names: tuple) -> dict:
    tree = ast.parse((WS / path).read_text(encoding="utf-8"))
    out = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            if node.targets[0].id in names and isinstance(node.value, ast.Constant):
                out[node.targets[0].id] = node.value.value
    return out


def ac8() -> tuple:
    if not grain():
        return False, "account grain not %s" % ACCOUNT
    b = consts(B00, ("TABLE",))
    r = consts(RCM, ("GOLD_BUCKET", "OUT_ROOT"))
    tmpl = [ln.strip() for ln in (WS / RCM).read_text(encoding="utf-8").splitlines() if ln.strip().startswith("data_key = ")]
    print("SOURCE @%s: %s TABLE=%r; %s GOLD_BUCKET=%r OUT_ROOT=%r; emit key template %s; bucket rule "
          "_bucket_for(): OUT_ROOT-rooted keys -> GOLD_BUCKET"
          % (HEAD[:10], B00, b.get("TABLE"), RCM, r.get("GOLD_BUCKET"), r.get("OUT_ROOT"), tmpl))
    if not (b.get("TABLE") and r.get("GOLD_BUCKET") and r.get("OUT_ROOT")):
        return False, "home constants not resolvable from source"
    bucket, prefix = r["GOLD_BUCKET"], "%s/%s/" % (r["OUT_ROOT"], b["TABLE"])
    print("HOME: s3://%s/%s" % (bucket, prefix))
    rc, d, err = aws("s3api", "list-objects-v2", "--bucket", bucket, "--prefix", prefix, "--delimiter", "/")
    if rc != 0:
        print("list-objects-v2 rc=%s %s" % (rc, err[:300]))
        return False, "list failed rc=%s" % rc
    parts = sorted(cp["Prefix"] for cp in (d or {}).get("CommonPrefixes", []))
    dates = sorted(p.rstrip("/").rsplit("date=", 1)[-1] for p in parts if "/date=" in p)
    print("LIVE LIST (s3api list-objects-v2 --delimiter /, read_at %s): %d partition(s) under the home; "
          "oldest=%s newest=%s; non-date prefixes=%d"
          % (utc(), len(dates), dates[0] if dates else None, dates[-1] if dates else None, len(parts) - len(dates)))
    if not dates:
        return False, "no date= partitions under home"
    newest = dates[-1]
    heads = 0
    for leaf in ("data.parquet", "manifest.json"):
        key = "%sdate=%s/%s" % (prefix, newest, leaf)
        rc, h, err = aws("s3api", "head-object", "--bucket", bucket, "--key", key)
        if rc == 0:
            heads += 1
            print("LIVE HEAD s3://%s/%s: LastModified=%s ContentLength=%s VersionId=%s"
                  % (bucket, key, h.get("LastModified"), h.get("ContentLength"), h.get("VersionId", "ABSENT")))
        else:
            print("LIVE HEAD s3://%s/%s: rc=%s %s" % (bucket, key, rc, err[:200]))
    print("RESULT: newest canonical_valuation partition date=%s (confirmed by %d of 2 head-object reads)" % (newest, heads))
    if heads == 0:
        return False, "newest partition not confirmed by head"
    return True, ""


# ------------------------------------------------------------------------------------------ AC9
CUT_FAILS = {"data/mdpf/scripts/gold/tests/test_global_fold_flag2.py::test_carry_within_window_carries_and_labels",
             "data/mdpf/scripts/gold/tests/test_global_fold_flag2.py::test_carry_beyond_window_absent_for_real",
             "data/mdpf/scripts/gold/tests/test_global_fold_flag2.py::test_carry_source_is_measured_never_interpolated"}


def ac9() -> tuple:
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    base = [sys.executable, "-m", "pytest", "data/mdpf/scripts/gold/tests", "-p", "no:cacheprovider", "--color=no"]
    co = subprocess.run(base + ["-q", "--co"], capture_output=True, cwd=str(WS), env=env, timeout=50)
    cot = co.stdout.decode("utf-8", "replace")
    m = re.search(r"(\d+) tests? collected", cot)
    collected = int(m.group(1)) if m else None
    print("COLLECT (python -m pytest data/mdpf/scripts/gold/tests -q --co): rc=%s collected=%s" % (co.returncode, collected))
    t0 = time.time()
    run = subprocess.run(base + ["-q", "-rf"], capture_output=True, cwd=str(WS), env=env, timeout=60)
    txt = run.stdout.decode("utf-8", "replace") + run.stderr.decode("utf-8", "replace")
    summ = [ln for ln in txt.splitlines() if re.search(r"\d+ (passed|failed)", ln) and " in " in ln]
    counts = {k: int(v) for v, k in re.findall(r"(\d+) (passed|failed|error|errors|skipped|xfailed|xpassed)", summ[-1])} if summ else {}
    fails = sorted({ln.split(" ", 1)[1].split(" - ")[0].strip() for ln in txt.splitlines() if ln.startswith("FAILED ")})
    print("RUN (python -m pytest data/mdpf/scripts/gold/tests -q -rf, Python %s, HEAD %s): rc=%s elapsed=%.1fs"
          % (sys.version.split()[0], HEAD[:10], run.returncode, time.time() - t0))
    print("SUMMARY LINE: %s" % (summ[-1].strip() if summ else "NONE"))
    print("COUNTS: collected=%s passed=%s failed=%s errors=%s skipped=%s"
          % (collected, counts.get("passed", 0), counts.get("failed", 0),
             counts.get("error", 0) + counts.get("errors", 0), counts.get("skipped", 0)))
    print("FAILING TEST IDS (%d):" % len(fails))
    for f in fails:
        print("  %s" % f)
    agree = (collected == 92 and counts.get("passed") == 89 and counts.get("failed") == 3 and set(fails) == CUT_FAILS)
    print("VS CUT MEASUREMENT (92 collected, 89 passed, 3 failed, all test_global_fold_flag2.py): %s"
          % ("AGREES" if agree else "DIFFERS"))
    if not summ or run.returncode not in (0, 1):
        return False, "pytest did not complete (rc=%s)" % run.returncode
    if len(fails) != counts.get("failed", 0):
        return False, "failing ids %d != failed count %d" % (len(fails), counts.get("failed", 0))
    return True, ""


# ------------------------------------------------------------------------------------------ AC10
def verb_of(op: str) -> str:
    return re.split(r"[-:]", op, maxsplit=1)[0].lower()


# AC10 as AMENDED by 1.0.0_SA_CTO ruling 97255 (option A) on row MDPF_TAXSMA-W6-S1: every logged call is a
# read verb, OR it is AC7's ONE ssm send-command meeting four conditions. Graded on the EXISTING command log
# and the recorded AC7 evidence (runs/AC7.txt, this probe's own census template); no AWS call is made here.
AC7_RUN = DELIV / "runs" / "AC7.txt"
AC7_REQUEST = SCRATCH / "ssm_census_request.json"   # untracked scratch: a corroborating arm only
READ_ONLY_CMDS = {"set", "echo", "cd", "find", "tr", "wc", "xargs", "grep", "awk", "md5sum", "cut", "stat",
                  "head", "lst0", "[", "exit"}
DENY_TOKENS = {  # word-boundary census over the raw script text; any hit fails condition (2)
    "sudo write": ["sudo", "su", "doas"],
    "file write": ["tee", "dd", "cp", "mv", "rm", "rmdir", "mkdir", "touch", "chmod", "chown", "ln", "install",
                   "truncate", "sed -i", "-delete", "-exec", "-execdir", "-fprint", "-fprintf", "-fls"],
    "package or service action": ["yum", "dnf", "rpm", "pip", "pip3", "apt", "apt-get", "npm", "systemctl",
                                  "service", "kill", "pkill", "killall", "reboot", "shutdown", "crontab"],
    "network call": ["curl", "wget", "nc", "ncat", "ssh", "scp", "rsync", "aws", "git", "ping", "telnet",
                     "/dev/tcp", "/dev/udp", "python", "python3"],
}
REDIRECT_RE = re.compile(r"(\d*)(>>|>\||&>|>)\s*(&?[^\s;|)]+)")


def _shell_command_words(script: str) -> list:
    """First word of every simple command, quotes stripped (a quoted literal is data, not a command)."""
    s = re.sub(r"'[^'\n]*'", " Q ", script)                       # single-quoted literals -> data
    s = re.sub(r'"([^"\n]*)"', lambda m: " ; ".join(re.findall(r"\$\([^()]*\)", m.group(1))) or " Q ", s)
    s = s.replace("\\(", " ").replace("\\)", " ")
    words = []
    for seg in re.split(r"\$\(|\|\|?|;|&&|[{}()]|\n", s):
        toks = seg.split()
        if not toks or re.match(r"^\w+=", toks[0]) or toks[0] == "Q":
            continue
        words.append(toks[0])
        if toks[0] == "xargs":                                     # the command xargs runs is a command too
            rest = [t for t in toks[1:] if not t.startswith("-")]
            if rest:
                words.append(rest[0])
    return words


def _grade_script(script: str, root: str) -> tuple:
    """Condition (2): the script ONLY reads. Returns (ok, reasons, report_lines)."""
    lines, reasons = [], []
    redirs = REDIRECT_RE.findall(script)
    fd_dups = [r for r in redirs if r[2].startswith("&")]
    null_dev = [r for r in redirs if r[2] == "/dev/null"]
    paths = [r for r in redirs if not r[2].startswith("&") and r[2] != "/dev/null"]
    lines.append("  (2a) output redirects in the script: %d total -- %d fd duplication(s) %s (no path), %d to /dev/null "
                 "(the null device: bytes discarded, no file created or modified), %d to any other path %s"
                 % (len(redirs), len(fd_dups), ["%s%s%s" % r for r in fd_dups], len(null_dev), len(paths),
                    ["%s%s%s" % r for r in paths]))
    if null_dev:
        lines.append("       READING, stated so L9 can reject it: /dev/null is graded as the null device, not as a written "
                     "path outside the SSM agent's working directory; a literal reading of 'any path' would FAIL this "
                     "condition on these %d redirect(s) (row MDPF_TAXSMA-W6-S4)" % len(null_dev))
    if paths:
        reasons.append("(2) %d redirect(s) to a path: %s" % (len(paths), ["%s%s%s" % r for r in paths]))
    under_root = [r for r in paths if r[2].startswith(root) or not r[2].startswith("/")]
    lines.append("  (2b) redirect targets under the Gateway app root %s or relative to it (the script cd's there): %d"
                 % (root, len(under_root)))
    for cls, toks in DENY_TOKENS.items():
        hits = {t: len(re.findall(r"(?<![\w/.-])%s(?![\w-])" % re.escape(t), script)) for t in toks}
        hit = {t: n for t, n in hits.items() if n}
        lines.append("  (2c) %-26s tokens checked %2d, hits %d %s" % (cls, len(toks), sum(hit.values()), hit or ""))
        if hit:
            reasons.append("(2) %s token(s) %s" % (cls, hit))
    words = _shell_command_words(script)
    census = {}
    for w in words:
        census[w] = census.get(w, 0) + 1
    off = sorted(w for w in census if w not in READ_ONLY_CMDS)
    lines.append("  (2d) command words: %d simple command(s), %d distinct %s; outside the read-only set: %d %s"
                 % (len(words), len(census), cj(census), len(off), off))
    if off:
        reasons.append("(2) command(s) outside the read-only set: %s" % off)
    if not words:
        reasons.append("(2) no command word parsed -- the census cannot discriminate")
    return not reasons, reasons, lines


def _grade_ac10(recs: list, script: str, ac7: dict, request, gw: dict) -> tuple:
    """The amended criterion over a command log + recorded AC7 evidence. Returns (ok, reasons, report_lines)."""
    lines, reasons = [], []
    sends = [r for r in recs if r["service"] == "ssm" and r["operation"] == "send-command"]
    other_bad = [r for r in recs if verb_of(r["operation"]) not in READ_VERBS
                 and not (r["service"] == "ssm" and r["operation"] == "send-command")]
    lines.append("DENOMINATOR: %d AWS call(s) logged, first %s, last %s"
                 % (len(recs), recs[0]["utc"] if recs else None, recs[-1]["utc"] if recs else None))
    lines.append("READ-VERB CALLS: %d of %d; ssm send-command: %d of %d; any OTHER non-read: %d of %d"
                 % (len(recs) - len(sends) - len(other_bad), len(recs), len(sends), len(recs), len(other_bad), len(recs)))
    for r in other_bad:
        lines.append("  OTHER NON-READ %s %s %s (criterion %s)" % (r["utc"], r["service"], r["operation"], r["criterion"]))
    if other_bad:
        reasons.append("%d other non-read call(s): %s" % (len(other_bad), sorted({"%s %s" % (r["service"], r["operation"])
                                                                                   for r in other_bad})))
    if not sends:
        lines.append("No ssm send-command in the log: the four conditions are not engaged.")
        return not reasons, reasons, lines
    # (1) exactly one, AWS-RunShellScript, only the Gateway host
    doc = ac7.get("document")
    tgt = ac7.get("instance_ids")
    one = len(sends) == 1 and sends[0]["criterion"] == "TXP1-AC7"
    c1 = one and doc == "AWS-RunShellScript" and tgt == [gw["instance_id"]]
    lines.append("(1) send-command count %d (criterion %s); DocumentName=%s; InstanceIds=%s vs the Gateway host %s "
                 "(infra/aws/ec2/EC2_MANIFEST.json @%s) -> %s"
                 % (len(sends), [r["criterion"] for r in sends], doc, tgt, gw["instance_id"], HEAD[:10],
                    "MET" if c1 else "NOT MET"))
    lines.append("    sources: DocumentName and InstanceIds from this probe's ac7() request literal; instance from "
                 "runs/AC7.txt (%s) and the log's get-command-invocation --instance-id (%s); scratch request file: %s"
                 % (ac7.get("run_instance"), ac7.get("log_instance"), ac7.get("request_arm")))
    if not c1:
        reasons.append("(1) not exactly one AWS-RunShellScript send-command to the Gateway host only")
    if ac7.get("run_instance") != gw["instance_id"] or ac7.get("log_instance") != gw["instance_id"]:
        reasons.append("(1) recorded instance differs from the Gateway host")
    # (2) script text recorded with its sha256, and it only reads
    full = hashlib.sha256(script.encode()).hexdigest()
    rec = ac7.get("recorded_sha_prefix") or ""
    c2hash = bool(rec) and full.startswith(rec)
    lines.append("(2) script text (%d lines, root %s), regenerated from this probe's CENSUS_TMPL at %s:"
                 % (len(script.splitlines()), ac7.get("root"), HEAD[:10]))
    lines.extend("    | " + ln for ln in script.splitlines())
    lines.append("    sha256 %s; runs/AC7.txt recorded at run time 'census script sha256=%s' -> %s"
                 % (full, rec, "EQUAL (prefix of %d hex)" % len(rec) if c2hash else "DIFFERENT"))
    if not c2hash:
        reasons.append("(2) script sha256 does not match the recorded run-time value")
    ok2, r2, l2 = _grade_script(script, ac7.get("root") or "")
    lines.extend(l2)
    reasons.extend(r2)
    lines.append("    (2) -> %s" % ("MET" if c2hash and ok2 else "NOT MET"))
    # (3) command id and the invocation's final status logged
    cid_log, cid_run, status = ac7.get("log_command_id"), ac7.get("run_command_id"), ac7.get("status")
    c3 = bool(cid_log) and cid_log == cid_run and status in ("Success", "Failed", "Cancelled", "TimedOut",
                                                             "Cancelling", "DeliveryTimedOut", "ExecutionTimedOut",
                                                             "Undeliverable", "Terminated")
    lines.append("(3) CommandId in command_log.jsonl (get-command-invocation args) %s; in runs/AC7.txt %s; final status "
                 "in runs/AC7.txt %s (ResponseCode %s, ExecutionEnd %s) -> %s"
                 % (cid_log, cid_run, status, ac7.get("response_code"), ac7.get("end"), "MET" if c3 else "NOT MET"))
    if not c3:
        reasons.append("(3) command id or terminal status not logged")
    # (4) side effects recorded as SSM's own bookkeeping; no Gateway app path changed
    lines.append("(4) side effects of the ONE send-command, recorded as SSM's own bookkeeping:")
    lines.append("    - SSM command-history record: %d (CommandId %s, sent %s)" % (len(sends), cid_run, ac7.get("sent_at")))
    lines.append("    - SSM agent working files on the host: the agent's own per-command orchestration files (the "
                 "script it materialises and its captured stdout/stderr) under its working directory; not re-read, "
                 "because this criterion forbids a new AWS act")
    app_writes = [r for r in REDIRECT_RE.findall(script)
                  if not r[2].startswith("&") and r[2] != "/dev/null"]
    mtime, md5 = ac7.get("server_mtime"), ac7.get("server_md5")
    before = bool(mtime and ac7.get("sent_at")) and mtime[:19].replace(" ", "T") < ac7["sent_at"][:19]
    blob = ac7.get("blob_md5")
    lines.append("    - Gateway app paths: the script writes %d path(s) (2a/2c above); app/server.py read DURING the "
                 "command: md5 %s, mtime %s -> %s the send at %s; git blob at deployed_commit %s md5 %s -> %s"
                 % (len(app_writes), md5, mtime, "BEFORE" if before else "NOT before", ac7.get("sent_at"),
                    (gw.get("deployed_commit") or "")[:10], blob, "EQUAL" if blob and blob == md5 else "NOT EQUAL/NOT READ"))
    lines.append("    denominator: 1 of %s app files had md5 and mtime read at run time; 0 write targets are the "
                 "static bound for all %s" % (ac7.get("files_all"), ac7.get("files_all")))
    c4 = len(sends) == 1 and not app_writes and before and bool(blob) and blob == md5
    lines.append("    (4) -> %s" % ("MET" if c4 else "NOT MET"))
    if not c4:
        reasons.append("(4) side effects not bounded to SSM bookkeeping on the recorded evidence")
    return not reasons, reasons, lines


def _ac7_evidence(gw: dict, recs: list) -> tuple:
    """Everything AC10 reads about AC7's one send-command, from recorded evidence only. Returns (evidence, script)."""
    txt = AC7_RUN.read_text(encoding="utf-8")

    def one(pat):
        m = re.search(pat, txt, re.M)
        return m.group(1).strip() if m else None
    ev = {"root": one(r"remote_path=(\S+)"), "run_instance": one(r"instance_id=(\S+)"),
          "recorded_sha_prefix": one(r"census script sha256=([0-9a-f]+)"),
          "run_command_id": one(r"send-command rc=0 CommandId=(\S+)"), "sent_at": one(r"CommandId=\S+ at (\S+)"),
          "status": one(r"get-command-invocation Status=(\w+)"), "response_code": one(r"ResponseCode=(\S+)"),
          "end": one(r"ExecutionEnd=(\S+)"), "files_all": one(r"^CENSUS FILES_ALL=(\d+)"),
          "server_md5": one(r"^CENSUS SERVER_PY_MD5=(\w+)"), "server_mtime": one(r"^CENSUS SERVER_PY_MTIME=(.+)$")}
    inv = [r for r in recs if r["service"] == "ssm" and r["operation"] == "get-command-invocation"]
    m = re.search(r"--command-id (\S+) --instance-id (\S+)", inv[0]["args"]) if inv else None
    ev["log_command_id"], ev["log_instance"] = (m.group(1), m.group(2)) if m else (None, None)
    # DocumentName / InstanceIds: the request literal in this probe's ac7(), read by AST (the bytes that ran are
    # tied to this source by the script sha256 check in condition (2)).
    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            keys = [k.value for k in node.keys if isinstance(k, ast.Constant)]
            if "DocumentName" in keys and "InstanceIds" in keys:
                dv = node.values[keys.index("DocumentName")]
                iv = node.values[keys.index("InstanceIds")]
                ev["document"] = dv.value if isinstance(dv, ast.Constant) else None
                ev["instance_ids"] = ([ev["run_instance"]] if isinstance(iv, ast.List) and len(iv.elts) == 1
                                      and isinstance(iv.elts[0], ast.Name) and iv.elts[0].id == "iid" else None)
    script = CENSUS_TMPL % {"root": ev["root"]}
    if AC7_REQUEST.exists():
        req = json.loads(AC7_REQUEST.read_text(encoding="utf-8"))
        same = ("\n".join(req["Parameters"]["commands"]) + "\n" == script
                and req.get("DocumentName") == ev.get("document") and req.get("InstanceIds") == [ev["run_instance"]])
        ev["request_arm"] = "present, DocumentName=%s InstanceIds=%s, script %s the regenerated text" % (
            req.get("DocumentName"), req.get("InstanceIds"), "EQUALS" if same else "DIFFERS FROM")
        if not same:
            ev["document"] = "MISMATCH-WITH-SENT-REQUEST"
    else:
        ev["request_arm"] = "absent (NOT-EVALUATED; not required)"
    dc = gw.get("deployed_commit")
    if dc:
        p = subprocess.run(["git", "show", "%s:infra/aws/ec2/opal-gateway/app/server.py" % dc],
                           capture_output=True, cwd=str(WS))
        ev["blob_md5"] = hashlib.md5(p.stdout).hexdigest() if p.returncode == 0 and p.stdout else None
    return ev, script


def ac10() -> tuple:
    print("COMMAND LOG %s (read_at %s); AC7 evidence %s; ruling 1.0.0_SA_CTO 97255 option A (row MDPF_TAXSMA-W6-S1)"
          % (LOG.relative_to(WS).as_posix(), utc(), AC7_RUN.relative_to(WS).as_posix()))
    print("No AWS call is made by this criterion.")
    if not LOG.exists():
        return False, "command log absent"
    recs = [json.loads(ln) for ln in LOG.read_text(encoding="utf-8").splitlines() if ln.strip()]
    if not recs:
        return False, "command log empty -- nothing to grade"
    census, ops = {}, {}
    for r in recs:
        census[verb_of(r["operation"])] = census.get(verb_of(r["operation"]), 0) + 1
        k = "%s %s" % (r["service"], r["operation"])
        ops[k] = ops.get(k, 0) + 1
    print("VERB CENSUS: %s" % cj(census))
    print("OPERATIONS: %s" % cj(ops))
    man = json.loads((WS / "infra/aws/ec2/EC2_MANIFEST.json").read_text(encoding="utf-8"))

    def walk(o):
        if isinstance(o, dict):
            if isinstance(o.get("opal-gateway"), dict) and "instance_id" in o["opal-gateway"]:
                return o["opal-gateway"]
            for v in o.values():
                r = walk(v)
                if r:
                    return r
        return None
    gw = walk(man) or {}
    ev, script = _ac7_evidence(gw, recs)
    ok, reasons, lines = _grade_ac10(recs, script, ev, None, gw)
    for ln in lines:
        print(ln)
    # Discrimination: the same grader over mutated copies of the SAME evidence; each must FAIL.
    put = dict(recs[0], service="s3api", operation="put-object", utc="MUTANT")
    mutants = [
        ("an extra s3api put-object in the log", recs + [put], script, ev),
        ("a second ssm send-command in the log", recs + [dict(sends, utc="MUTANT") for sends in recs
                                                         if sends["operation"] == "send-command"], script, ev),
        ("a redirect into the app root", recs, script.replace("--- end ---\"", "--- end ---\" > app/x.txt"), ev),
        ("a sudo curl line in the script", recs, script + "sudo curl -s http://example.invalid\n", ev),
        ("a different target instance", recs, script, dict(ev, instance_ids=["i-00000000000000000"])),
        ("no terminal status recorded", recs, script, dict(ev, status=None)),
    ]
    fired = 0
    for label, mrecs, mscript, mev in mutants:
        mok, mre, _ = _grade_ac10(mrecs, mscript, mev, None, gw)
        fired += (not mok)
        print("MUTANT %-38s -> %s" % (label, "FAIL (as expected), %d reason(s): %s" % (len(mre), " | ".join(mre))
                                              if not mok else "PASS (NOT DISCRIMINATING)"))
    print("MUTANTS: %d of %d FAIL as expected" % (fired, len(mutants)))
    if fired != len(mutants):
        reasons.append("%d of %d mutants passed -- the grader does not discriminate" % (len(mutants) - fired, len(mutants)))
    return not reasons, "; ".join(reasons)


def main() -> int:
    global CRIT
    if len(sys.argv) != 2 or not re.fullmatch(r"AC([1-9]|10)", sys.argv[1]):
        print("usage: tx_p_1.py AC<1..10>")
        return 2
    n = int(sys.argv[1][2:])
    CRIT = "TXP1-AC%d" % n
    banner(n)
    fn = {1: ac1, 2: ac2, 3: ac3, 4: ac4, 5: ac5, 6: ac6, 7: ac7, 8: ac8, 9: ac9, 10: ac10}[n]
    try:
        ok, why = fn()
    except Exception as exc:  # the verdict line must still print, and say why
        ok, why = False, "probe exception %s: %s" % (type(exc).__name__, str(exc)[:200])
    print("VERDICT: PASS-TXP1-AC%d" % n if ok else "VERDICT: FAIL-TXP1-AC%d %s" % (n, why))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
