"""OG-rl-13 runner for r27_read_host.py.txt (one host run, through r27_ssm_prog.py).
usage: python r27_run_read.py <mode: before|rehearsal|after|probe> <served sha> <out-file> [--stage <release gateway dir>] [--before <file with the R27_BEFORE_VALUES line>] [--json]
  --stage  : REHEARSAL -- the three release files that differ between r27_live_md5.txt and r27_release_md5.txt are staged into a host scratch copy (the installed tree is untouched).
  --before : the BEFORE run's output; its newest day and the page/audit-page status, size and digest ride to the host as R27_BEFORE_PAGE so the host compares them.
  --json   : (after only, Phase B) write RL13_READ.json from the host's RL13_BODY line when the host also printed the matching RL13_DIGEST.
The known execution id is read read-only from the portal's execution table (r27_exec_id.py) into THIS process's memory and goes to the host only inside an SSM parameter; the runner
redacts it from the saved output. Never printed or stored."""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
a = sys.argv[1:]
mode, served, outfile = a[0], a[1], a[2]
stage = a[a.index("--stage") + 1] if "--stage" in a else None
before = a[a.index("--before") + 1] if "--before" in a else None
want_json = "--json" in a

p = subprocess.run([sys.executable, os.path.join(HERE, "r27_exec_id.py")], capture_output=True, text=True, encoding="utf-8", errors="replace")
line = [x for x in p.stdout.split("\n") if x.startswith("{")]
if p.returncode != 0 or not line:
    print("no execution id read (rc %d)" % p.returncode)
    sys.exit(9)
sec = json.loads(line[0])
assert "R27_EXEC_ID" in sec and sec["R27_EXEC_ID"]
# AMENDMENT A3: the concierge's principal (tid, oid) comes ONLY from the issuer's off-repo file; it rides to the host inside SSM parameters (redacted from every output), never printed or stored.
_pf = os.path.join(os.environ.get("LOCALAPPDATA", ""), "opal", "og-salt", "r27", "concierge_principal.json")
if not os.path.isfile(_pf):
    print("STOP: the issuer's off-repo principal file is absent")
    sys.exit(8)
_pj = json.load(open(_pf, encoding="utf-8"))
assert _pj.get("tid") and _pj.get("oid")
sec["R27_TID"], sec["R27_OID"] = _pj["tid"], _pj["oid"]
if before:
    m = re.search(r"^R27_BEFORE_VALUES (\{.*\})$", open(before, encoding="utf-8").read(), re.M)
    assert m, "no R27_BEFORE_VALUES line in " + before
    bv = json.loads(m.group(1))
    sec["R27_BEFORE_PAGE"] = json.dumps({k: bv[k] for k in ("newest_day", "page_status", "page_bytes", "page_sha16", "audit_status", "audit_bytes", "audit_sha16")}, sort_keys=True)
env = dict(os.environ, R27_SECRET_ENV=json.dumps(sec))
if stage:
    env["R27_STAGE_FROM"] = stage
if want_json:
    env["R27_JSON_DIR"] = HERE
    env["R27_JSON_SPECS"] = json.dumps([["RL13_BODY", "RL13_DIGEST", "RL13_READ.json"]])
rr = subprocess.run([sys.executable, os.path.join(HERE, "r27_ssm_prog.py"), os.path.join(HERE, "r27_read_host.py.txt"), outfile, "%s %s" % (mode, served)],
                    env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
sys.stdout.write("\n".join(x for x in rr.stdout.split("\n") if "warnings.warn" not in x and "IncompleteField" not in x))
sys.exit(rr.returncode)
