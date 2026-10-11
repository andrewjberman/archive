"""ADVI_FIRMBKTS round 4: the READ-ONLY equivalence of the exec-summary generator's reads in `legacy` and `canonical` mode
(act 4b's object-level read), issuer 2.0.0_SA_COO~B1.

The handler cannot be invoked read-only (it runs every advisor and uploads). Its READ helpers can: this tool unpacks the
artifact zip into a scratch directory and, for each mode in a fresh subprocess with `BD_PLATINUM_MODE` set (or unset for
legacy), imports `platinum_reader` and calls only `list_active_advisors()`, `load_leaderboards(firm)` and
`load_advisor_artifacts(<first advisor>)`. It prints COUNTS and SHA-256 digests only: never an advisor id, never a body.

  python r4_execeq.py --zip <artifact.zip> [--firm 49financial] [--data-bucket opal-data-bd]
Last line: EXEC READS: legacy and canonical <EQUAL|DIFFER>: advisors <n>/<n>, leaderboards <k>/<k>, artifacts <m>/<m>.
Exit 0 only when EQUAL and n >= 1. READ-ONLY (s3 list/get through the seam). Plain ASCII. Never edit this file.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
import zipfile

CHILD = r'''
import hashlib, json, sys
sys.path.insert(0, sys.argv[1])
import platinum_reader as r
firm = sys.argv[2]
ids = r.list_active_advisors()
lb = r.load_leaderboards(firm)
first = sorted(ids)[0] if ids else None
art = r.load_advisor_artifacts(first) if first else {}
def h(o):
    return hashlib.sha256(json.dumps(o, sort_keys=True, default=str).encode("utf-8")).hexdigest()
print(json.dumps({"n": len(ids), "ids": h(sorted(ids)), "lb_keys": len(lb), "lb": h(lb),
                  "art_keys": len(art), "art": h(art)}))
'''


def run(mode, tmp, firm, bucket):
    env = dict(os.environ, DATA_BUCKET=bucket, ANTHROPIC_SECRET_NAME="unused", MODEL="unused", LOG_LEVEL="WARNING",
               MAX_ADVISORS_HARD_CAP="5000", AWS_DEFAULT_REGION="us-east-1")
    env.pop("BD_PLATINUM_MODE", None)
    if mode == "canonical":
        env["BD_PLATINUM_MODE"] = "canonical"
    r = subprocess.run([sys.executable, "-c", CHILD, tmp, firm], capture_output=True, text=True, timeout=110, env=env)
    if r.returncode:
        return None, (r.stderr.strip().splitlines() or ["failed"])[-1][:160]
    return json.loads(r.stdout.strip().splitlines()[-1]), ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--zip", required=True)
    ap.add_argument("--firm", default="49financial")
    ap.add_argument("--data-bucket", default="opal-data-bd")
    a = ap.parse_args()
    with tempfile.TemporaryDirectory() as td:
        with zipfile.ZipFile(a.zip) as z:
            z.extractall(td)
        leg, e1 = run("legacy", td, a.firm, a.data_bucket)
        can, e2 = run("canonical", td, a.firm, a.data_bucket)
    if leg is None or can is None:
        print("ERROR: legacy=%s canonical=%s" % (e1 or "ok", e2 or "ok"))
        print("EXEC READS: legacy and canonical DIFFER: advisors 0/0, leaderboards 0/0, artifacts 0/0")
        return 1
    same = all(leg[k] == can[k] for k in leg)
    print("legacy    : advisors %s ids %s | leaderboards %s %s | artifacts %s %s" % (
        leg["n"], leg["ids"][:12], leg["lb_keys"], leg["lb"][:12], leg["art_keys"], leg["art"][:12]))
    print("canonical : advisors %s ids %s | leaderboards %s %s | artifacts %s %s" % (
        can["n"], can["ids"][:12], can["lb_keys"], can["lb"][:12], can["art_keys"], can["art"][:12]))
    print("EXEC READS: legacy and canonical %s: advisors %s/%s, leaderboards %s/%s, artifacts %s/%s" % (
        "EQUAL" if same else "DIFFER", leg["n"], can["n"], leg["lb_keys"], can["lb_keys"], leg["art_keys"],
        can["art_keys"]))
    return 0 if (same and leg["n"] >= 1) else 1


if __name__ == "__main__":
    sys.exit(main())
