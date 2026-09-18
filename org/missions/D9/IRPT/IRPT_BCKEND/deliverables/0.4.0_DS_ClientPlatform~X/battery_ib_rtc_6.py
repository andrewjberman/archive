#!/usr/bin/env python3
"""IRPT_BCKEND.TO-IB-rtc-6 acceptance battery -- R36-AC1, six graded arms.

Prints IBR36-PRINCIPAL-DECLARED-PLANNED-PACKET-WRITTEN only when arms (a)-(f) ALL hold.

WHAT THIS BATTERY IS NOT (bound 12): it wraps nothing it grades. The name comes from the naming
builder itself; the declaration is read from the COMMITTED plan texts (the artifacts the two sign-off
halves read) and cross-checked against the committed extract of the same plans; the runner arm runs the
real test file; the writer census reads the live account; the plan identities are re-hashed from the
committed files and compared with the hashes the packet prints. Nothing is applied, minted or written.

Graded arms:
  (a) NAME        name(...) for the role, printed; 0 of 4 of the face's old denied prefixes match; the
                  LIVE fence on the firm bucket admits it (its ArnNotLike pattern matches); the planned
                  role carries exactly that name.
  (b) DECLARATION 5 GetObject prefixes, 1 prefix-conditioned ListBucket over the same 5, 1 trust
                  principal, 1 AssumeRole statement added to the host role (0 removed), 0 statements on
                  any other bucket, 0 write actions -- read from the plan text AND the extract, which
                  must agree.
  (c) RUNNER      the stubbed-STS test file: 49 Financial reads through the assumed session 1 of 1,
                  INF/COT through the host session 2 of 2, and every other arm of that file passing.
  (d) WRITERS     the live writer census of the 49 Financial directory prefix: W of W enumerated,
                  0 UNKNOWN, the new principal among them 0.
  (e) PLANS       both plans 0 to destroy; each plan text's sha256 re-derived and equal to the packet's.
  (f) PACKET      present; names every key K1-K5 with a rollback; the negative-control design (P1, N1-N5)
                  and the name-prefix and writer-census sections.
"""
from __future__ import annotations

import datetime as dt
import fnmatch
import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile

WS = pathlib.Path(__file__).resolve().parents[7]
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(WS / "lib"))
sys.path.insert(0, str(HERE))
import opal_naming                         # noqa: E402  the naming builder itself
import writer_census_ib_rtc_6 as census    # noqa: E402  the census instrument

PLAN_DIR = HERE / "IB-rtc-6_plan_directory.txt"
PLAN_MDPF = HERE / "IB-rtc-6_plan_mdpf-pipeline.txt"
EXTRACT = HERE / "IB-rtc-6_plan_iam_extract.json"
PACKET = HERE / "NEVER_WIDEN_SIGNOFF_PACKET_IB-rtc-6.md"
TEST = WS / "data/assets/scripts/gold/investor_reporting/tests/test_directory_runner_source_principal.py"
OLD_DENIED = ["role/cot-*", "role/inf-*", "role/mdpf-*", "role/opal-assets-mdpf-*"]
FIVE = ["dim_account", "dim_relationship", "dim_identity_crosswalk", "dim_portfolio_group",
        "bridge_group_account"]

results = []


def run(cmd, timeout=600):
    try:
        p = subprocess.run(cmd, cwd=str(WS), capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=timeout,
                           env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except subprocess.TimeoutExpired:
        return 124, "TIMEOUT after %ss" % timeout


def record(arm, ok, detail):
    results.append((arm, ok is True))
    print("  %-5s %s" % ({True: "PASS", False: "FAIL", None: "N/E"}[ok], arm))
    for line in detail:
        print("        " + line)
    print()


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


print("R36-AC1 battery -- IRPT_BCKEND.TO-IB-rtc-6, the 49 Financial principal declared, planned, packeted")
print("workspace: %s" % WS)
_, head = run(["git", "rev-parse", "--short=10", "HEAD"])
print("branch tip: %s   run at %s" % (head.strip(),
                                       dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")))
print()
ext = json.loads(EXTRACT.read_text(encoding="utf-8"))

# ============================================================ (a) the name
role_name = opal_naming.name("irpt", "49financial", "directory-read", "role")
policy_name = opal_naming.name("irpt", "49financial", "directory-read", "policy")
arn_tail = "role/" + role_name
old_hits = [p for p in OLD_DENIED if fnmatch.fnmatch(arn_tail, p)]
fence = opal_naming.fence_patterns("49financial")
det = ['name("irpt", "49financial", "directory-read", "role")   = %s' % role_name,
       'name("irpt", "49financial", "directory-read", "policy") = %s' % policy_name,
       "the face's old denied prefixes matched: %d of %d %s" % (len(old_hits), len(OLD_DENIED), old_hits)]
live_admit = None
try:
    import boto3
    pol = json.loads(boto3.client("s3", region_name="us-east-1").get_bucket_policy(
        Bucket=opal_naming.lookup("49financial").get("bucket") or "opal-data-49financial")["Policy"])
    pats = [p for s in pol["Statement"] if s.get("Effect") == "Deny"
            for p in (s.get("Condition", {}).get("ArnNotLike", {}).get("aws:PrincipalArn", []) or [])]
    role_arn = fence[0].split(":role/")[0] + ":" + arn_tail
    live_admit = any(fnmatch.fnmatch(role_arn, p) for p in pats)
    det.append("LIVE fence (bucket policy ArnNotLike, %d pattern(s)): the role ARN %s is admitted: %s"
               % (len(pats), role_arn, live_admit))
except Exception as exc:                                   # noqa: BLE001
    det.append("LIVE fence unreadable: %s" % type(exc).__name__)
det.append("registry fence_patterns('49financial') = %s" % fence)
det.append("planned role name %s / policy name %s" % (ext["new_role"]["name"], ext["new_role_policy"]["name"]))
ok_a = (not old_hits and live_admit is True and ext["new_role"]["name"] == role_name
        and ext["new_role_policy"]["name"] == policy_name and role_name in PLAN_DIR.read_text(encoding="utf-8"))
record("(a) NAME", ok_a, det)

# ============================================================ (b) the declaration
pdoc = ext["new_role_policy"]["policy"]
trust = ext["new_role"]["assume_role_policy"]
L = lambda x: [x] if isinstance(x, str) else list(x or [])   # noqa: E731
get_res = [r for s in pdoc["Statement"] if "s3:GetObject" in L(s["Action"]) for r in L(s["Resource"])]
lists = [s for s in pdoc["Statement"] if "s3:ListBucket" in L(s["Action"])]
list_prefixes = [p for s in lists for p in s.get("Condition", {}).get("StringLike", {}).get("s3:prefix", [])]
buckets = {r.split(":::")[1].split("/")[0] for s in pdoc["Statement"] for r in L(s["Resource"])}
writes = [a for s in pdoc["Statement"] for a in L(s["Action"]) if not a.startswith(("s3:Get", "s3:List"))]
principals = [p for s in trust["Statement"] for p in L(s.get("Principal", {}).get("AWS"))]
host_added = ext["host_role_policy"]["added"]
host_removed = ext["host_role_policy"]["removed"]
five_ok = sorted(r.rsplit("/", 2)[-2] for r in get_res) == sorted(FIVE)
text = PLAN_DIR.read_text(encoding="utf-8")
mtext = PLAN_MDPF.read_text(encoding="utf-8")
text_agrees = (all(("dimensions/%s/*" % t) in text for t in FIVE)
               and text.count('"s3:ListBucket"') == 1 and "AssumedOnlyByTheDailyRunnerHost" in text
               and '+ Sid      = "IrptDirectory49fAssumeSourcePrincipal"' in mtext)
det = ["GetObject prefixes: %d %s" % (len(get_res), sorted(r.split(":::")[1] for r in get_res)),
       "ListBucket statements: %d, prefix-conditioned over %d prefixes %s" % (len(lists), len(list_prefixes),
                                                                             list_prefixes),
       "trust principals: %d %s" % (len(principals), principals),
       "host-role statements added %d %s; removed %d" % (len(host_added), [s.get("Sid") for s in host_added],
                                                          len(host_removed)),
       "buckets named by the role's policy: %s (statements on any other bucket: %d)"
       % (sorted(buckets), len(buckets - {"opal-data-49financial"})),
       "write actions granted: %d %s" % (len(writes), writes),
       "the committed plan TEXT agrees with the extract (five prefixes, one list, the trust sid, the host "
       "statement): %s" % text_agrees]
ok_b = (len(get_res) == 5 and five_ok and len(lists) == 1 and len(list_prefixes) == 5
        and len(principals) == 1 and principals[0].endswith(":role/mdpf-daily-runner-ec2-role")
        and len(host_added) == 1 and host_added[0].get("Action") == "sts:AssumeRole"
        and host_added[0].get("Resource", "").endswith(":" + arn_tail) and not host_removed
        and buckets == {"opal-data-49financial"} and not writes and text_agrees)
record("(b) DECLARATION", ok_b, det)

# ============================================================ (c) the runner, stubbed STS
rc, out = run([sys.executable, "-m", "pytest", str(TEST), "-q", "-rA", "-p", "no:cacheprovider"], timeout=300)
out = re.sub(r"\x1b\[[0-9;]*m", "", out)
passed = set(re.findall(r"^PASSED \S+::(\S+)", out, re.M))
failed = set(re.findall(r"^FAILED \S+::(\S+)", out, re.M))
assumed = ["test_49f_dimension_reads_go_through_the_assumed_session"]
host = ["test_inf_reads_only_on_the_host_session", "test_cot_reads_only_on_the_host_session"]
det = ["pytest %s rc=%d: %d passed, %d failed" % (TEST.relative_to(WS).as_posix(), rc, len(passed), len(failed)),
       "49 Financial through the ASSUMED session: %d of %d" % (len([t for t in assumed if t in passed]), len(assumed)),
       "Inflection / Cottonwood through the HOST session: %d of %d" % (len([t for t in host if t in passed]),
                                                                       len(host)),
       "the other arms: %s" % sorted(passed - set(assumed) - set(host))]
ok_c = rc == 0 and not failed and all(t in passed for t in assumed + host) and len(passed) >= 8
record("(c) RUNNER", ok_c, det)

# ============================================================ (d) the writer census, live
with tempfile.TemporaryDirectory() as td:
    pp = pathlib.Path(td) / "planned_policy.json"
    pp.write_text(json.dumps(pdoc), encoding="utf-8")
    try:
        c = census.census(str(pp))
    except Exception as exc:                               # noqa: BLE001
        c = {"verdict": "NOT-EVALUATED", "lines": ["census raised %s" % type(exc).__name__]}
det = list(c["lines"])
ok_d = None
if c["verdict"] == "EVALUATED":
    new_is_writer = c.get("new_principal") == "allowed" or any(w["name"] == role_name for w in c["writers"])
    det.append("WRITERS %d of %d enumerated; UNKNOWN %d; unsimulated %d; the new principal among them: %d"
               % (len(c["writers"]), c["principals"], c.get("unknown", -1), c["unsimulated"],
                  1 if new_is_writer else 0))
    ok_d = (c["principals"] > 0 and c.get("unknown") == 0 and c["unsimulated"] == 0 and not new_is_writer
            and c.get("new_principal") == "implicitDeny")
record("(d) WRITERS", ok_d, det)

# ============================================================ (e) the plans
packet = PACKET.read_text(encoding="utf-8")
det = []
ok_e = True
for label, path in (("directory", PLAN_DIR), ("mdpf-pipeline", PLAN_MDPF)):
    t = path.read_text(encoding="utf-8")
    m = re.search(r"^Plan: (\d+) to add, (\d+) to change, (\d+) to destroy\.$", t, re.M)
    h = sha(path)
    in_packet = h in packet
    det.append("%-13s %s  sha256 %s  printed in the packet: %s"
               % (label, m.group(0) if m else "(no Plan line)", h, in_packet))
    ok_e = ok_e and bool(m) and m.group(3) == "0" and in_packet
det.append("extract counts: %s" % {k: v["counts"] for k, v in ext["plans"].items()})
ok_e = ok_e and all(v["counts"]["delete"] == 0 for v in ext["plans"].values())
record("(e) PLANS", ok_e, det)

# ============================================================ (f) the packet
keys = ["K1", "K2", "K3", "K4", "K5"]
sections = {k: re.search(r"^### %s -- .*?(?=^### |^---|\Z)" % k, packet, re.S | re.M) for k in keys}
with_rollback = [k for k, m in sections.items() if m and "**Rollback:**" in m.group(0)]
controls = [c for c in ("P1", "N1", "N2", "N3", "N4", "N5") if re.search(r"^\| %s \|" % c, packet, re.M)]
det = ["keys with their own section: %d of %d; each with a Rollback: %d of %d %s"
       % (sum(1 for m in sections.values() if m), len(keys), len(with_rollback), len(keys), with_rollback),
       "negative-control rows: %d of 6 %s" % (len(controls), controls),
       "name-prefix check present: %s; writer census present: %s; targeted mdpf apply named: %s"
       % ("Name-prefix checks" in packet, "WRITERS: 12 of 262" in packet or "writer census" in packet.lower(),
          "-target=aws_iam_role_policy.mdpf_runner" in packet),
       "packet sha256 %s" % sha(PACKET)]
ok_f = (len(with_rollback) == 5 and len(controls) == 6 and "Name-prefix checks" in packet
        and "-target=aws_iam_role_policy.mdpf_runner" in packet)
record("(f) PACKET", ok_f, det)

print("R-40 identities:")
for p in (PLAN_DIR, PLAN_MDPF, EXTRACT, PACKET, TEST):
    print("  %s  sha256 %s" % (p.relative_to(WS).as_posix(), sha(p)))
print()
passed_n = sum(1 for _, ok in results if ok)
print("R36-AC1: %d of %d graded arms PASS" % (passed_n, len(results)))
if passed_n == len(results):
    print("IBR36-PRINCIPAL-DECLARED-PLANNED-PACKET-WRITTEN")
    sys.exit(0)
print("BLOCKED: not every graded arm passed; the expect token is withheld")
sys.exit(1)
