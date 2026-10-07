"""OG-rl-13 AMENDMENT A3: after the post-deploy read, list the gateway's RAW audit lake prefix (bucket opal-mcp-audit, prefix audit/dt=<day>/, runbook section 5's 'raw lake prefix' paragraph)
for objects written AFTER the deploy time, and read the first `rivalfunds_view` record, if one exists. Read-only (list + get); nothing is written to the lake and no request is made to produce a record.
usage: python r27_lake_read.py <deploy time UTC, e.g. 2026-10-07T16:57:30Z> <out-file> [--merge <RL13_FLOOR.json>]
Prints only: the number of objects listed after the deploy time, the number of those read, and for the first rivalfunds_view record its kept arg NAMES, whether `bytes` is present and the object's
write time; never a field value (no digest, principal or email). With --merge the result is stored in the floor file's body as `lake_record` (the string `none yet` when no such record exists)."""
import datetime
import json
import os
import subprocess
import sys
import tempfile

BUCKET = "opal-mcp-audit"
deploy_t, outfile = sys.argv[1], sys.argv[2]
merge = sys.argv[sys.argv.index("--merge") + 1] if "--merge" in sys.argv else None
T0 = datetime.datetime.strptime(deploy_t, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)


def aws(a):
    return subprocess.run(["bash", "-c", 'aws "$@"', "x"] + a, capture_output=True, text=True, encoding="utf-8", errors="replace", env=dict(os.environ, MSYS_NO_PATHCONV="1"))


now = datetime.datetime.now(datetime.timezone.utc)
days = sorted({T0.strftime("%Y-%m-%d"), now.strftime("%Y-%m-%d")})
objs = []
for d in days:
    r = aws(["s3api", "list-objects-v2", "--bucket", BUCKET, "--prefix", "audit/dt=%s/" % d, "--output", "json", "--region", "us-east-1"])
    if r.returncode != 0:
        print("LIST FAIL rc=%d %s" % (r.returncode, r.stderr[:200]))
        sys.exit(2)
    for o in json.loads(r.stdout or "{}").get("Contents") or []:
        lm = datetime.datetime.fromisoformat(o["LastModified"])
        if lm > T0:
            objs.append((lm, o["Key"]))
objs.sort()
lines = ["R27_LAKE listed_after=%s objects_after_deploy=%d listed_days=%s read_at=%s" % (deploy_t, len(objs), ",".join(days), now.strftime("%Y-%m-%dT%H:%M:%SZ"))]
found = None
read_n = 0
tmpd = tempfile.mkdtemp(prefix="og_r27_lake_")
tf = os.path.join(tmpd, "o.jsonl")
for lm, key in objs:
    g = aws(["s3api", "get-object", "--bucket", BUCKET, "--key", key, tf, "--region", "us-east-1"])
    if g.returncode != 0 or not os.path.exists(tf):
        continue
    read_n += 1
    try:
        recs = [json.loads(x) for x in open(tf, encoding="utf-8") if x.strip()]
    except Exception:  # noqa: BLE001
        recs = []
    os.remove(tf)
    for rec in recs:
        if rec.get("tool") == "rivalfunds_view" or rec.get("event") == "rivalfunds_view":
            a = rec.get("args") or {}
            found = {"arg_names": sorted(a), "bytes_present": "bytes" in rec, "object_write_time": lm.strftime("%Y-%m-%dT%H:%M:%SZ")}
            break
    if found:
        break
os.rmdir(tmpd)
lines.append("R27_LAKE objects_read=%d first_rivalfunds_view_record=%s" % (read_n, json.dumps(found, sort_keys=True) if found else "none yet"))
lake_record = found if found else "none yet"
if found:
    bad = [k for k in found["arg_names"] if k not in ("day", "route", "fund")]
    lines.append("R27_LAKE other_args_kept=%d => %s" % (len(bad), "ROLLBACK TRIGGER" if bad else "within day, route, fund"))
text = "\n".join(lines) + "\n"
sys.stdout.write(text)
open(outfile, "w", encoding="utf-8", newline="\n").write(text)
if merge:
    doc = json.load(open(merge, encoding="utf-8"))
    doc["body"]["lake_record"] = lake_record
    with open(merge, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print("merged lake_record into", os.path.basename(merge))
