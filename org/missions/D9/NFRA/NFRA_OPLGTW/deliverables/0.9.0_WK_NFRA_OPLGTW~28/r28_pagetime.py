"""OG-rl-14 AMENDMENT A2: read each rivalfunds page's S3 object (HEAD: status, size, LastModified; GET: sha256 of the body) for the day pages the r28 verify arms compare
(2026-10-06 and the newest published day), both index.html and audit.html. Read-only, through .tools/aws; the bucket name is read from the committed location file and never printed.
usage: python r28_pagetime.py <label> <out-file>      prints one line per object and writes the same plus an R28_PAGETIME json line to <out-file>."""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=HERE, capture_output=True, text=True).stdout.strip()
label, outfile = sys.argv[1], sys.argv[2]
loc = json.load(open(os.path.join(ROOT, "infra/aws/ec2/opal-gateway/app/rivalfunds_location.json"), encoding="utf-8"))
BUCKET, PREFIX = loc["bucket"], loc["key_prefix"]
DAYS_FIXED = ["2026-10-06"]


def aws(a):
    return subprocess.run(["bash", "-c", 'aws "$@"', "x"] + a, capture_output=True, text=True, encoding="utf-8", errors="replace", env=dict(os.environ, MSYS_NO_PATHCONV="1"))


def red(t):
    return t.replace(BUCKET, "<bucket>")


now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
r = aws(["s3api", "list-objects-v2", "--bucket", BUCKET, "--prefix", PREFIX, "--delimiter", "/", "--output", "json", "--region", "us-east-1"])
if r.returncode != 0:
    print("LIST FAIL rc=%d %s" % (r.returncode, red(r.stderr)[:300]))
    sys.exit(2)
days = sorted(p[len(PREFIX) + len("date="):].rstrip("/") for p in [c["Prefix"] for c in (json.loads(r.stdout or "{}").get("CommonPrefixes") or [])] if p[len(PREFIX):].startswith("date="))
newest = days[-1]
want = sorted(set(DAYS_FIXED + [newest]))
rows = []
lines = ["R28_PAGETIME label=%s read_at=%s published_days=%d newest=%s" % (label, now, len(days), newest)]
tmpd = tempfile.mkdtemp(prefix="og_r28_pagetime_")
for d in want:
    for name in ("index.html", "audit.html"):
        key = "%sdate=%s/%s" % (PREFIX, d, name)
        h = aws(["s3api", "head-object", "--bucket", BUCKET, "--key", key, "--output", "json", "--region", "us-east-1"])
        if h.returncode != 0:
            rows.append({"day": d, "object": name, "head": "ERR", "detail": red(h.stderr)[:120].strip()})
            lines.append("  %s %s HEAD ERR %s" % (d, name, rows[-1]["detail"]))
            continue
        _h = json.loads(h.stdout)
        ln, lm, etag = _h["ContentLength"], _h["LastModified"], _h["ETag"]
        tf = os.path.join(tmpd, "obj.bin")
        g = aws(["s3api", "get-object", "--bucket", BUCKET, "--key", key, tf, "--region", "us-east-1"])
        dg = hashlib.sha256(open(tf, "rb").read()).hexdigest()[:16] if g.returncode == 0 and os.path.exists(tf) else "GET-ERR"
        if os.path.exists(tf):
            os.remove(tf)
        rows.append({"day": d, "object": name, "head": 200, "size": ln, "last_modified": lm, "etag": etag.strip('"')[:8], "sha16": dg})
        lines.append("  %s %s HEAD 200 size=%s LastModified=%s ETag8=%s sha16=%s" % (d, name, ln, lm, etag.strip('"')[:8], dg))
os.rmdir(tmpd)
lines.append("R28_PAGETIME_JSON " + json.dumps({"label": label, "read_at": now, "newest": newest, "objects": rows}, sort_keys=True))
text = "\n".join(lines) + "\n"
sys.stdout.write(text)
open(outfile, "w", encoding="utf-8", newline="\n").write(text)
