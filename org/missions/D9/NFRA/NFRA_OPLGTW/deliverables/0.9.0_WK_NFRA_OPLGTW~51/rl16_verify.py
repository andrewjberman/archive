"""OG-rl-16 PHASE B verify, ADAPTED at Phase A from r29_verify.py (OG-rl-15), never run against a deploy by the Phase A worker.
Release r16b = live 1e32562729 + E2 (copy_site_file_to_s3, .xlsx -> fee_statement ONLY): 5 host files change (3 modified, 2 new), 100 -> 102 listed; tools 66 -> 67 (only copy_site_file_to_s3 added);
.env names 52 -> 53 (only ADVI_FEE_STATEMENT_S3_ROOT added); every other .env value hash unchanged. The r29 text below is left for the form; the checks use the rl16_ lists.
Release r29 = live aa75078e1b (r28) + the four cells (OG-md-1, OG-sf-1, OG-rf-1, OG-cm-1) + the release-time edits E2, E3 (ANNOUNCE_OG-rl-15.md); no Bloomberg change (A6).
11 files reach the host (rl16_release_md5.txt vs rl16_base_md5.txt: 10 modified, 1 new: deploy/mail_sender_domain_table.txt). No tool and no route is added or removed (7a).

usage:  python r29_verify.py before <state.json>
        python r29_verify.py after  <state.json> [--expect-changed NAME,NAME]

`before` reads the host on the installed LIVE code (MainPID, /health, tool names, .env key NAMES and per-key value sha256 -- a digest only, never a value, shipped md5 against the
release list: exactly the 11 release files differ) and saves them. Keep the state file OUT of the repository (e.g. <worktree>/.scratch/r29_before.json).
`after` (run IMMEDIATELY after the deploy returns) exits 0 only if all hold:
  1. host /health 200 and the service active;
  2. shipped md5 = the release bytes (98 of 98);
  3. the tool list is UNCHANGED, name for name (66 -> 66);
  4. .env key names: exactly one is added, MAIL_SENDER_DOMAIN_TABLE (51 -> 52), none removed;
  5. every other .env value has the SAME sha256 before and after, except the names in --expect-changed (the MAIL_BEARER leg, if the halves sign it: MAIL_BEARER, MAIL_BEARER_LABELS).
The post-deploy READS (RL15_READ.json) and the floor (rl4.AC1.sh against ENV_KEYS_R29.txt, ht.AC2.sh at 52) follow in r29_postdeploy.sh.
Never printed: any .env value, bearer, token or identity."""
import argparse
import base64
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
INST = "i-07dccb1615503ac99"
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
keys = []
hashes = {}
for line in open(".env", encoding="utf-8"):
    m = re.match(r"^([A-Z0-9_]+)=(.*)$", line.rstrip(chr(10)).rstrip(chr(13)))
    if m:
        keys.append(m.group(1))
        hashes[m.group(1)] = hashlib.sha256(m.group(2).encode("utf-8")).hexdigest()   # only the digest leaves the host; no value is printed or stored
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
    pf = os.path.join(os.environ.get("TEMP", "/tmp"), "og_rl16_verify_params_%d.json" % os.getpid())
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


def host_read():
    md5 = open(os.path.join(HERE, "rl16_release_md5.txt"), encoding="utf-8").read().replace(chr(13), "")
    prog = HOST_PROG.replace("@@MD5@@", md5)
    b64 = base64.b64encode(prog.encode("utf-8")).decode("ascii")
    tmp = "/tmp/og_rl16_verify_%d.py" % os.getpid()      # its own name per run (row Z-W28-S9)
    st, out = ssm_run(["echo %s | base64 -d > %s" % (b64, tmp), "/opt/opal-gateway/.venv/bin/python " + tmp, "rm -f " + tmp, "echo LEFTOVER=$(ls /tmp/og_rl16_verify_* 2>/dev/null | wc -l)"],
                      "OG-rl-16 verify host read")
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
    if a.mode == "before":
        rel = dict((ln.split("  ", 1)[1].strip(), ln.split()[0]) for ln in open(os.path.join(HERE, "rl16_release_md5.txt"), encoding="utf-8") if ln.strip())
        live = dict((ln.split("  ", 1)[1].strip(), ln.split()[0]) for ln in open(os.path.join(HERE, "rl16_base_md5.txt"), encoding="utf-8") if ln.strip())
        differ = sorted(k for k in rel if live.get(k) != rel[k])
        json.dump(R, open(a.state, "w", encoding="utf-8"), indent=1)
        ok = (R["health"] == 200 and R["active"] == "active" and len(R["tools"] or []) == 66 and sorted(R["md5_bad"]) == differ and len(differ) == 5 and len(R["env_keys"]) == 52)
        print("BEFORE saved: MainPID %s, env value sha256 saved %d (hash only), env key names %d, tools %d, /health %s, shipped md5 %d of %d vs the release list; the %d differing are exactly the release's %s => %s" % (
            R["mainpid"], len(R["env_hashes"]), len(R["env_keys"]), len(R["tools"] or []), R["health"], R["md5_ok"], R["md5_listed"], len(R["md5_bad"]),
            "5 host files" if sorted(R["md5_bad"]) == differ else "FILES (MISMATCH with the expected list: %s)" % sorted(set(R["md5_bad"]) ^ set(differ)), "PASS" if ok else "FAIL"))
        return 0 if ok else 1
    B = json.load(open(a.state, encoding="utf-8"))
    res = []

    def chk(name, ok, detail):
        res.append(bool(ok))
        print("%s %s: %s" % ("PASS" if ok else "FAIL", name, detail))

    chk("host /health 200", R["health"] == 200 and R["active"] == "active", "health %s, service %s, MainPID %s (before %s)" % (R["health"], R["active"], R["mainpid"], B["mainpid"]))
    chk("shipped md5 = release bytes", R["md5_ok"] == R["md5_listed"] and R["md5_listed"] == 102, "%d of %d identical; not-ok %s" % (R["md5_ok"], R["md5_listed"], R["md5_bad"]))
    bt, at = set(B["tools"] or []), set(R["tools"] or [])
    chk("tool list: exactly copy_site_file_to_s3 added (66 -> 67), none removed", bool(bt) and sorted(at - bt) == ["copy_site_file_to_s3"] and not (bt - at) and len(B["tools"]) == 66 and len(R["tools"]) == 67,
        "before %d after %d tools; added %s removed %s" % (len(bt), len(at), sorted(at - bt), sorted(bt - at)))
    added = sorted(set(R["env_keys"]) - set(B["env_keys"]))
    removed = sorted(set(B["env_keys"]) - set(R["env_keys"]))
    chk(".env key names: exactly ADVI_FEE_STATEMENT_S3_ROOT added (52 -> 53), none removed", added == ["ADVI_FEE_STATEMENT_S3_ROOT"] and not removed and len(R["env_keys"]) == len(set(R["env_keys"])) == 53,
        "names %d vs before %d; added %s removed %s" % (len(R["env_keys"]), len(B["env_keys"]), added, removed))
    BH, AH = B.get("env_hashes") or {}, R.get("env_hashes") or {}
    exp = sorted(x for x in a.expect_changed.split(",") if x)
    changed = sorted(k for k in BH if AH.get(k) != BH[k])
    chk("every pre-existing .env value has the SAME sha256 before and after, except the names expected to change (%s)" % (",".join(exp) or "none"),
        len(BH) > 0 and changed == exp, "before hashes %d, after hashes %d, equal %d of %d, changed %s" % (len(BH), len(AH), len(BH) - len(changed), len(BH), changed))
    ok = all(res)
    print("VERIFY %s: %d of %d" % ("PASS" if ok else "FAIL", sum(res), len(res)))
    if not ok:
        print("ROLL BACK: re-deploy the base 1e32562729 from a rollback tree (ANNOUNCE_OG-rl-16.md section 7), re-verify, close ROLLED BACK.")
    return 0 if ok else 1


sys.exit(main())
