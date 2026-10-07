"""OG-rl-14 runner for r28_lake_host.py.txt (ONE host run, through r28_ssm_prog.py). No principal, no execution id, no secret travels.
usage: python r28_run_lake.py <mode: before|rehearsal|after> <served sha> <out-file> [--stage <release gateway dir>] [--json]
  --stage : REHEARSAL -- the files whose md5 differs between r28_live_md5.txt and r28_release_md5.txt (app/audit.py) are staged into a host scratch copy; the installed tree is untouched.
  --json  : (after only, Phase B) write RL14_READ.json from the host's RL14_BODY line when the host also printed the matching RL14_DIGEST (the body's fields are exactly the order's)."""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
a = sys.argv[1:]
mode, served, outfile = a[0], a[1], a[2]
stage = a[a.index("--stage") + 1] if "--stage" in a else None
want_json = "--json" in a
env = dict(os.environ)
if stage:
    env["R28_STAGE_FROM"] = stage
if want_json:
    env["R28_JSON_DIR"] = HERE
    env["R28_JSON_SPECS"] = json.dumps([["RL14_BODY", "RL14_DIGEST", "RL14_READ.json"]])
rr = subprocess.run([sys.executable, os.path.join(HERE, "r28_ssm_prog.py"), os.path.join(HERE, "r28_lake_host.py.txt"), outfile, "%s %s" % (mode, served)],
                    env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
sys.stdout.write("\n".join(x for x in rr.stdout.split("\n") if "warnings.warn" not in x and "IncompleteField" not in x))
sys.exit(rr.returncode)
