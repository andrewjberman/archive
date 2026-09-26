"""MX-s-4 shared reader over s3://opal-data-bd. Usage: python s4_read.py AC1|AC2|AC3 <workspace-root>.
AC1: the NEWEST logs/asset-dim-download-*.log written after the order's issue reads 'Download exit code: 0' and no
     'FAILED' line (the login worked end to end on the real producer).
AC2: silver/bd_assets.parquet LastModified is after the order's issue (the compaction runs again).
AC3: silver/bd_assets_dim.parquet LastModified is after the order's issue (the bridge is rebuilt from a current input).
Denominators printed; the listing is the CLI's auto-paginated full set, counted client-side."""
import json
import os
import subprocess
import sys

ISSUE = "2026-09-26T06:00:00"
ac, root = sys.argv[1], sys.argv[2]
aws = os.path.join(root, ".tools", "aws")


def run(*args):
    r = subprocess.run(["bash", aws, *args], capture_output=True, timeout=120)
    return r.returncode, r.stdout.decode("utf-8", "replace")


if ac == "AC1":
    rc, out = run("s3api", "list-objects-v2", "--bucket", "opal-data-bd", "--prefix", "logs/asset-dim-download-",
                  "--output", "json")
    try:
        objs = json.loads(out).get("Contents", [])
    except Exception:
        print("LIST-FAILED rc=%s" % rc)
        print("NOT-OK")
        raise SystemExit(0)
    after = sorted([o for o in objs if o["LastModified"][:19] > ISSUE], key=lambda o: o["LastModified"])
    print("logs listed=%d written after issue=%d" % (len(objs), len(after)))
    if not after:
        print("NOT-OK")
        raise SystemExit(0)
    newest = after[-1]
    rc, body = run("s3", "cp", "s3://opal-data-bd/" + newest["Key"], "-")
    ok = "Download exit code: 0" in body and "FAILED" not in body
    print("newest=%s download_rc0=%s failed_lines=%d" % (newest["Key"].split("/")[-1],
          "yes" if "Download exit code: 0" in body else "no", body.count("FAILED")))
    print("OK" if ok else "NOT-OK")
else:
    key = "silver/bd_assets.parquet" if ac == "AC2" else "silver/bd_assets_dim.parquet"
    rc, out = run("s3api", "head-object", "--bucket", "opal-data-bd", "--key", key, "--output", "json")
    try:
        lm = json.loads(out)["LastModified"]
    except Exception:
        print("HEAD-FAILED rc=%s" % rc)
        print("NOT-OK")
        raise SystemExit(0)
    print("%s LastModified=%s after issue=%s" % (key, lm, "yes" if lm[:19] > ISSUE else "no"))
    print("OK" if lm[:19] > ISSUE else "NOT-OK")
