"""Read-only helper for the Monday 2026-10-19 11:30Z organic 49 Financial performance read (IB-pr-612 / IB-pr-614 / IB-pr-613 pair close).

Usage: python monday_49f_read.py [YYYY-MM-DD]   (default: the Monday fire day 2026-10-19)

Prints counts and statuses only, one line each, for the issuer to grade:
  FN     CodeSha256 of irpt-holdings-performance-lambda (expect LiDXhN74...)
  METRIC Invocations and Errors in the 11:00Z to 12:30Z window of the fire day
  NEWEST newest day key of the 49F daily gold table: its latest VersionId, LastModified (expect the fire day, after 11:30Z), size
  MANIF  newest manifest key LastModified of the 49F performance manifest table
Reads only. It writes nothing and invokes nothing. It does not decide: PASS means the organic fire ran clean on the
new grant (1 invocation, 0 errors, a day key written by that fire); anything else is read by the issuer.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[8]
AWS = [str(ROOT / ".tools" / ("aws.cmd" if os.name == "nt" else "aws"))]
FN = "irpt-holdings-performance-lambda"
BUCKET = "opal-data-49financial"
DAILY = "irpt/49financial/gold/holdings_performance_daily/"
MANIFEST = "irpt/49financial/gold/holdings_performance_manifest/"
CAND = "LiDXhN74TsATYhoQKzs+Oy1qtNn3hDJxxjkLa0ZlfLg="
day = sys.argv[1] if len(sys.argv) > 1 else "2026-10-19"


def aws(*a):
    p = subprocess.run(AWS + list(a), capture_output=True, text=True, timeout=120)
    if p.returncode != 0:
        print("AWSFAIL rc=%s %s" % (p.returncode, p.stderr.strip()[:200]))
        sys.exit(2)
    return p.stdout


def newest(prefix):
    """Newest key under the prefix by key name (date=YYYY-MM-DD sorts). One listing; the tables hold under 1000 keys."""
    out = json.loads(aws("s3api", "list-objects-v2", "--bucket", BUCKET, "--prefix", prefix, "--output", "json", "--no-paginate") or "{}")
    if out.get("IsTruncated"):
        print("TRUNCATED the listing of %s is cut; read it by hand" % prefix)
        sys.exit(2)
    keys = out.get("Contents") or []
    return max(keys, key=lambda o: o["Key"]) if keys else None


sha = aws("lambda", "get-function-configuration", "--function-name", FN, "--query", "CodeSha256", "--output", "text").strip()
print("FN     code_sha256=%s %s" % (sha, "OK" if sha == CAND else "DIFFERS"))
inv = err = None
for m in ("Invocations", "Errors"):
    out = aws("cloudwatch", "get-metric-statistics", "--namespace", "AWS/Lambda", "--metric-name", m,
              "--dimensions", "Name=FunctionName,Value=" + FN, "--start-time", day + "T11:00:00Z", "--end-time", day + "T12:30:00Z",
              "--period", "5400", "--statistics", "Sum", "--query", "Datapoints[].Sum", "--output", "text").strip()
    val = sum(float(x) for x in out.split()) if out else 0.0
    if m == "Invocations":
        inv = val
    else:
        err = val
print("METRIC window=%sT11:00Z..12:30Z invocations=%s errors=%s" % (day, inv, err))
n = newest(DAILY)
if n:
    print("NEWEST daily_key_date=%s last_modified=%s size=%s" % (n["Key"].split("date=")[-1].split("/")[0], n["LastModified"], n["Size"]))
else:
    print("NEWEST none")
# the manifest table is large: read only the fire day's own partition(s), not the table
mk = json.loads(aws("s3api", "list-objects-v2", "--bucket", BUCKET, "--prefix", MANIFEST + "date=" + day, "--output", "json", "--no-paginate") or "{}").get("Contents") or []
print("MANIF  fire_day_manifest_keys=%d newest_last_modified=%s" % (len(mk), max(o["LastModified"] for o in mk) if mk else "none"))
ok = sha == CAND and inv is not None and inv >= 1 and err == 0 and n is not None and str(n["LastModified"]).startswith(day)
print("VERDICT %s" % ("PASS_CANDIDATE (issuer still reads the manifest declared flag)" if ok else "NOT_YET_OR_DIFFERENT (read it)"))
