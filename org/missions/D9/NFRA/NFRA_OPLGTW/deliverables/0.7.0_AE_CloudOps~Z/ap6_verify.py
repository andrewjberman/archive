"""OG-ap-6 PHASE B2 step 8 verify -- adapted from rl16_verify.py (W~51) for THIS re-cut.

usage:  python ap6_verify.py before <state.json>
        python ap6_verify.py after  <state.json> [--expect-changed NAME,NAME]

WHY THIS IS AN ADAPTED COPY, NOT THE ORIGINAL. rl16_verify.py hardcodes Phase A's ABSOLUTE
counts in both modes: before asserts tools == 66 and env_keys == 52, after asserts
md5_listed == 102, tools 66 -> 67 and env_keys == 53. The COO half @3d5fc13ecf condition 3 and
the order's step 8 both forbid using those here -- "rl16_verify.py takes those from the base
read at the act, never from the 66 / 52 / 100 written at Phase A" -- because MX-r-9 and MP-r-2
moved the base. Measured: the shipped list is 104 entries at base 2a5966dfbd and 106 at release
6aadf7db37, where Phase A had 100 and 102. So every count below is RELATIVE to what `before`
actually read on the host, and the only absolutes asserted are the two the halves name by
NAME: the one added tool copy_site_file_to_s3 and the one added env key
ADVI_FEE_STATEMENT_S3_ROOT.

ALSO ADDED, per AMENDMENT 1: the dashboard/ walk is part of the read-back, and all FOUR
orphans must compare unchanged (index-BP6X9XJd.js, index-BqfQgt7G.css, index-CrZMj-00.js,
index-a6wjv_wv.css). The original walked neither dashboard/ nor any extra.

Inputs read from this directory: ap6_release_md5.txt (106 entries at the release) and
ap6_base_md5.txt (104 at the base), both generated from git blobs -- a method validated by
reproducing Phase A's own embedded list 100 of 100 at 1e32562729.

Never printed: any .env value, bearer, token or identity. Only per-key sha256 digests leave the
host.
"""
import argparse
import base64
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
INST = "i-07dccb1615503ac99"
ADDED_TOOL = "copy_site_file_to_s3"
ADDED_ENV = "ADVI_FEE_STATEMENT_S3_ROOT"

HOST_PROG = r'''
import hashlib, json, os, re, subprocess, urllib.request, urllib.error
R = {}
os.chdir("/opt/opal-gateway")
R["mainpid"] = subprocess.check_output(["systemctl", "show", "opal-gateway", "-p", "MainPID", "--value"]).decode().strip()
R["active"] = subprocess.check_output(["systemctl", "is-active", "opal-gateway"]).decode().strip()
MD5 = """@@MD5@@"""
want = [l.split("  ", 1) for l in MD5.strip().split("\n") if l.strip()]
bad = []
for h, f in want:
    try:
        got = hashlib.md5(open(f, "rb").read()).hexdigest()
    except OSError:
        got = "ABSENT"
    if got != h:
        bad.append(f)
R["md5_listed"] = len(want); R["md5_ok"] = len(want) - len(bad); R["md5_bad"] = bad
# AMENDMENT 1: the dashboard/ walk is part of the read-back. Every dashboard file with its md5,
# so the four orphans and the live bundle can be compared unchanged across the deploy.
dash = {}
for root, ds, fs in os.walk("dashboard"):
    ds[:] = [d for d in ds if d != "__pycache__"]
    for f in fs:
        p = os.path.join(root, f).replace(os.sep, "/")
        try:
            dash[p] = hashlib.md5(open(p, "rb").read()).hexdigest()
        except OSError:
            dash[p] = "ABSENT"
R["dash"] = dash
keys = []
hashes = {}
for line in open(".env", encoding="utf-8"):
    m = re.match(r"^([A-Z0-9_]+)=(.*)$", line.rstrip(chr(10)).rstrip(chr(13)))
    if m:
        keys.append(m.group(1))
        hashes[m.group(1)] = hashlib.sha256(m.group(2).encode("utf-8")).hexdigest()   # only the digest leaves the host
R["env_keys"] = sorted(keys)
R["env_hashes"] = hashes
tool_src = """
import asyncio, os, sys
sys.path.insert(0, "/opt/opal-gateway")
from app import tools, integrations
ids = os.environ["ENABLED_INTEGRATIONS"].split()
rep = integrations.register_enabled(tools.mcp, ids)
from mcp.server.fastmcp import FastMCP
names = sorted(t.name for t in asyncio.run(FastMCP.list_tools(tools.mcp)))
print("TOOLNAMES", ",".join(names))
"""
pid = R["mainpid"]
penv = {}
for kv in open("/proc/%s/environ" % pid, "rb").read().split(bytes([0])):
    if kv.startswith(b"ENABLED_INTEGRATIONS="):
        penv["ENABLED_INTEGRATIONS"] = kv.split(b"=", 1)[1].decode("utf-8", "replace")
out = subprocess.run(["env", "-i", "HOME=/tmp", "PATH=" + os.environ.get("PATH", ""), "MOCK_GRAPH=1",
                      "ENABLED_INTEGRATIONS=" + penv.get("ENABLED_INTEGRATIONS", ""), "/opt/opal-gateway/.venv/bin/python", "-c", tool_src],
                     capture_output=True, text=True).stdout
tn = [l for l in out.split("\n") if l.startswith("TOOLNAMES ")]
R["tools"] = tn[0].split(" ", 1)[1].split(",") if tn else None
try:
    R["health"] = urllib.request.urlopen("http://localhost:8080/health", timeout=15).status
except urllib.error.HTTPError as e:
    R["health"] = e.code
except Exception as e:
    R["health"] = "ERR:" + type(e).__name__
print("HOSTJSON " + json.dumps(R))
'''


def aws(args):
    return subprocess.run(["bash", "-c", 'aws "$@"', "x"] + args, capture_output=True, text=True, encoding="utf-8", errors="replace")


def ssm_run(commands, comment, polls=60, wait=3):
    pf = os.path.join(os.environ.get("TEMP", "/tmp"), "og_ap6_verify_params_%d.json" % os.getpid())
    with open(pf, "w", encoding="utf-8", newline=chr(10)) as fh:
        fh.write(json.dumps({"commands": commands, "executionTimeout": ["1800"]}))
    r = aws(["ssm", "send-command", "--instance-ids", INST, "--document-name", "AWS-RunShellScript", "--comment", comment,
             "--parameters", "file://" + pf.replace(chr(92), "/"), "--region", "us-east-1", "--query", "Command.CommandId", "--output", "text"])
    os.remove(pf)
    if r.returncode != 0:
        print("SEND FAIL", r.stderr.strip()[:300])
        sys.exit(2)
    cid = r.stdout.strip()
    st = ""
    for _ in range(polls):
        time.sleep(wait)
        st = aws(["ssm", "get-command-invocation", "--command-id", cid, "--instance-id", INST, "--region", "us-east-1", "--query", "Status",
                  "--output", "text"]).stdout.strip()
        if st in ("Success", "Failed", "Cancelled", "TimedOut"):
            break
    out = aws(["ssm", "get-command-invocation", "--command-id", cid, "--instance-id", INST, "--region", "us-east-1", "--query",
               "StandardOutputContent", "--output", "text"]).stdout
    print("ssm %s status=%s" % (cid, st))
    return st, out.replace(chr(13), "")


def _list(fn):
    p = os.path.join(HERE, fn)
    return dict((ln.split("  ", 1)[1].strip(), ln.split()[0]) for ln in open(p, encoding="utf-8") if ln.strip())


def host_read():
    md5 = open(os.path.join(HERE, "ap6_release_md5.txt"), encoding="utf-8").read().replace(chr(13), "")
    prog = HOST_PROG.replace("@@MD5@@", md5)
    b64 = base64.b64encode(prog.encode("utf-8")).decode("ascii")
    tmp = "/tmp/og_ap6_verify_%d.py" % os.getpid()      # its own name per run (row Z-W28-S9)
    st, out = ssm_run(["echo %s | base64 -d > %s" % (b64, tmp), "/opt/opal-gateway/.venv/bin/python " + tmp, "rm -f " + tmp,
                       "echo LEFTOVER=$(ls /tmp/og_ap6_verify_* 2>/dev/null | wc -l)"],
                      "OG-ap-6 verify host read")
    line = [x for x in out.split(chr(10)) if x.startswith("HOSTJSON ")]
    if st != "Success" or not line:
        print("HOST READ FAILED")
        print(out[-800:])
        sys.exit(2)
    print([x for x in out.split(chr(10)) if x.startswith("LEFTOVER=")])
    return json.loads(line[0][len("HOSTJSON "):])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=("before", "after"))
    ap.add_argument("state")
    ap.add_argument("--expect-changed", default="")
    a = ap.parse_args()
    R = host_read()

    rel = _list("ap6_release_md5.txt")
    base = _list("ap6_base_md5.txt")
    # What SHOULD differ on a host running the base, measured against the release list.
    differ = sorted(k for k in rel if base.get(k) != rel[k])

    if a.mode == "before":
        json.dump(R, open(a.state, "w", encoding="utf-8"), indent=1)
        # RELATIVE: no absolute tool or env count is asserted. The one absolute is that the
        # host's mismatches against the release list are EXACTLY the base-vs-release differ set.
        md5_is_base = sorted(R["md5_bad"]) == differ
        ok = (R["health"] == 200 and R["active"] == "active"
              and bool(R["tools"]) and len(R["env_keys"]) > 0
              and md5_is_base)
        print("BEFORE saved: MainPID %s, env value digests %d, env key names %d, tools %d, /health %s, "
              "shipped md5 %d of %d vs the RELEASE list; mismatching %d" % (
                  R["mainpid"], len(R["env_hashes"]), len(R["env_keys"]), len(R["tools"] or []),
                  R["health"], R["md5_ok"], R["md5_listed"], len(R["md5_bad"])))
        print("  the host is running the BASE: its mismatches equal the base-vs-release differ set "
              "(%d file(s)): %s" % (len(differ), "yes" if md5_is_base else
                                    "NO -- symmetric difference %s" % sorted(set(R["md5_bad"]) ^ set(differ))))
        print("  dashboard files seen: %d" % len(R.get("dash") or {}))
        print("  counts are RECORDED, not asserted (COO half condition 3): tools %d, env names %d, listed %d"
              % (len(R["tools"] or []), len(R["env_keys"]), R["md5_listed"]))
        print("BEFORE %s" % ("PASS" if ok else "FAIL"))
        return 0 if ok else 1

    B = json.load(open(a.state, encoding="utf-8"))
    res = []

    def chk(name, ok, detail):
        res.append(bool(ok))
        print("%s %s: %s" % ("PASS" if ok else "FAIL", name, detail))

    chk("host /health 200 and service active",
        R["health"] == 200 and R["active"] == "active",
        "health %s, service %s, MainPID %s (before %s)" % (R["health"], R["active"], R["mainpid"], B["mainpid"]))

    chk("shipped md5 = the RE-CUT release bytes (every listed file identical)",
        R["md5_ok"] == R["md5_listed"] and R["md5_listed"] == len(rel) and not R["md5_bad"],
        "%d of %d identical against a release list of %d; not-ok %s" % (R["md5_ok"], R["md5_listed"], len(rel), R["md5_bad"]))

    bt, at = set(B["tools"] or []), set(R["tools"] or [])
    chk("tool list: exactly %s added, none removed (RELATIVE to the base read at the act)" % ADDED_TOOL,
        bool(bt) and sorted(at - bt) == [ADDED_TOOL] and not (bt - at),
        "before %d after %d; added %s removed %s" % (len(bt), len(at), sorted(at - bt), sorted(bt - at)))

    added = sorted(set(R["env_keys"]) - set(B["env_keys"]))
    removed = sorted(set(B["env_keys"]) - set(R["env_keys"]))
    chk(".env key names: exactly %s added, none removed, no duplicate (RELATIVE)" % ADDED_ENV,
        added == [ADDED_ENV] and not removed and len(R["env_keys"]) == len(set(R["env_keys"])),
        "names %d vs before %d; added %s removed %s" % (len(R["env_keys"]), len(B["env_keys"]), added, removed))

    BH, AH = B.get("env_hashes") or {}, R.get("env_hashes") or {}
    exp = sorted(x for x in a.expect_changed.split(",") if x)
    changed = sorted(k for k in BH if AH.get(k) != BH[k])
    chk("every pre-existing .env value has the SAME sha256, except %s" % (",".join(exp) or "none"),
        len(BH) > 0 and changed == exp,
        "before %d, after %d, equal %d of %d, changed %s" % (len(BH), len(AH), len(BH) - len(changed), len(BH), changed))

    # AMENDMENT 1: all four dashboard orphans, and the rest of dashboard/, unchanged.
    BD, AD = B.get("dash") or {}, R.get("dash") or {}
    dash_changed = sorted(k for k in BD if AD.get(k) != BD[k])
    dash_gone = sorted(k for k in BD if k not in AD)
    dash_new = sorted(k for k in AD if k not in BD)
    chk("dashboard/ unchanged across the deploy (all four orphans included, AMENDMENT 1)",
        len(BD) > 0 and not dash_changed and not dash_gone and not dash_new,
        "before %d files, after %d; changed %s removed %s added %s" % (len(BD), len(AD), dash_changed, dash_gone, dash_new))

    ok = all(res)
    print("VERIFY %s: %d of %d" % ("PASS" if ok else "FAIL", sum(res), len(res)))
    if not ok:
        print("ROLL BACK: re-deploy the base with DEPLOY_BASE_REF=<release sha> per the order's step 8, "
              "destroy the one policy through the same Terraform path from C:/tmp/og-tf-e2, and file an "
              "ARMED row naming 2.0.0_SA_COO~O.")
    return 0 if ok else 1


sys.exit(main())
