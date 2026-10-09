"""Scratch: live zip vs BUILD_ONLY zip, per function. AWS reads only. Writes C:/dev/_scratch268/census_raw.json and live zips."""
import base64
import hashlib
import json
import subprocess
import urllib.request
import zipfile
import io
from pathlib import Path

ROOT = Path("C:/dev/wk-irpt-bckend-268")
S = Path("C:/dev/_scratch268")
FNS = ["irpt-status", "irpt-performance-adapter", "irpt-directory-search", "irpt-narrative", "irpt-ycharts-generate",
       "irpt-export-render", "irpt-holdings", "irpt-49f-reporting-read-lambda"]
BUCKET = "opal-313476888478-lambda-artifacts"
MINE = ("served.py", "entry.py", "owned_report.py")


def aws(*args):
    r = subprocess.run(["aws", *args, "--output", "json"], capture_output=True, cwd=str(ROOT), timeout=120)
    if r.returncode:
        raise SystemExit("aws %s rc=%d %s" % (args[:3], r.returncode, r.stderr.decode()[:300]))
    return json.loads(r.stdout.decode() or "null")


def members(data):
    out = {}
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        for i in z.infolist():
            if not i.is_dir():
                out[i.filename] = z.read(i.filename)
    return out


def sha(b):
    return hashlib.sha256(b).hexdigest()


res = {}
(S / "live").mkdir(exist_ok=True)
for fn in FNS:
    g = aws("lambda", "get-function", "--function-name", fn)
    cfg = g["Configuration"]
    live = urllib.request.urlopen(g["Code"]["Location"], timeout=120).read()
    live_b64 = base64.b64encode(hashlib.sha256(live).digest()).decode()
    (S / "live" / (fn + ".zip")).write_bytes(live)
    vers = aws("s3api", "list-object-versions", "--bucket", BUCKET, "--prefix", "investor-reporting/%s.zip" % fn)
    versions = [v for v in vers.get("Versions", []) if v["Key"] == "investor-reporting/%s.zip" % fn]
    latest = next((v for v in versions if v["IsLatest"]), None)
    head = aws("s3api", "head-object", "--bucket", BUCKET, "--key", "investor-reporting/%s.zip" % fn,
               "--version-id", latest["VersionId"]) if latest else None
    meta = (head or {}).get("Metadata", {})
    built = (S / "runA" / fn / ("lambda-artifact-%s.zip" % fn)).read_bytes()
    built_b = (S / "runB" / fn / ("lambda-artifact-%s.zip" % fn)).read_bytes()
    bm, lm = members(built), members(live)
    changed = []
    for name in sorted(set(bm) | set(lm)):
        b, lv = bm.get(name), lm.get(name)
        if b is None or lv is None or b != lv:
            changed.append({"member": name, "status": "added" if lv is None else "removed" if b is None else "changed",
                            "built_sha256_prefix": sha(b)[:12] if b is not None else None,
                            "live_sha256_prefix": sha(lv)[:12] if lv is not None else None,
                            "is_ib_pr_405_member": name in MINE})
    res[fn] = {
        "function": fn, "live_before": live_b64, "live_code_sha256_reported": cfg["CodeSha256"],
        "live_zip_matches_reported": live_b64 == cfg["CodeSha256"], "live_last_modified": cfg["LastModified"],
        "live_bytes": len(live), "s3_latest_version": latest["VersionId"] if latest else None,
        "s3_latest_last_modified": latest["LastModified"] if latest else None,
        "s3_latest_sha256_metadata": meta.get("sha256"),
        "s3_latest_is_live_zip": bool(meta.get("sha256") == live_b64) if meta.get("sha256") else None,
        "built_sha256": base64.b64encode(hashlib.sha256(built).digest()).decode(), "built_sha256_hex": sha(built),
        "built_bytes": len(built), "built_twice_identical": built == built_b,
        "built_members": len(bm), "live_members": len(lm), "changed_member_count": len(changed), "changed_members": changed,
    }
    print(fn, "live_ok=%s s3_latest_is_live=%s changed=%d mine=%s" % (res[fn]["live_zip_matches_reported"], res[fn]["s3_latest_is_live_zip"],
          len(changed), [c["member"] for c in changed if c["is_ib_pr_405_member"]]))
(S / "census_raw.json").write_text(json.dumps(res, indent=1))
