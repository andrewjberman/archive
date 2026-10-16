"""ADVI_FIRMBKTS round 9, Door 6 step 1 (CTO erratum 1): a LIVE deployed-code census of the readers of the marker gold/meta/pipeline-complete.json.

Read-only. For every Lambda function in the account (paginated list, denominator printed) it downloads the DEPLOYED package from Code.Location and searches every
member for the needle; it also searches each function's environment values, and every object under s3://opal-data-inf/code/runner/. It writes counts and
file:line positions only, never code bodies and never a secret value.
  python door6_live_reader_census.py --out <record.json> [--needle pipeline-complete] [--workers 6]
Prints:  CENSUS functions=<n> zip=<z> image=<i> scanned=<s> errors=<e> hits_functions=<h> env_hits=<v> runner_objects=<r> runner_hits=<rh>
Limits, always printed in the record: container-image functions are NOT scanned (no zip); layers are NOT scanned; a key built from parts that never spell the
needle is NOT found; a function that errors is listed, not counted as clean.
"""
import argparse
import concurrent.futures as cf
import io
import json
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path

REPO = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip() or ".")
AWS = str(REPO / ".tools" / "aws")
BUCKET = "opal-data-inf"
RUNNER_PREFIX = "code/runner/"


def aws(*a):
    return subprocess.run(["bash", AWS, *a], capture_output=True)


def list_functions():
    r = aws("lambda", "list-functions", "--query", "Functions[].[FunctionName,PackageType]", "--output", "json")
    if r.returncode != 0:
        raise SystemExit("list-functions failed rc=%d %s" % (r.returncode, r.stderr.decode()[:200]))
    rows = json.loads(r.stdout.decode())
    return [(n, t) for n, t in rows]


def scan_text(name, text, needle):
    out = []
    for i, ln in enumerate(text.splitlines(), 1):
        if needle in ln:
            out.append("%s:%d" % (name, i))
    return out


def scan_function(fn, needle):
    res = {"function": fn, "pos": [], "env": [], "error": ""}
    r = aws("lambda", "get-function", "--function-name", fn, "--output", "json")
    if r.returncode != 0:
        res["error"] = "get-function rc=%d" % r.returncode
        return res
    d = json.loads(r.stdout.decode())
    env = (d.get("Configuration", {}).get("Environment") or {}).get("Variables") or {}
    for k, v in env.items():
        if needle in str(v) or needle in k:
            res["env"].append(k)
    loc = (d.get("Code") or {}).get("Location")
    if not loc:
        res["error"] = "no Code.Location"
        return res
    try:
        blob = urllib.request.urlopen(loc, timeout=120).read()
        z = zipfile.ZipFile(io.BytesIO(blob))
        for m in z.namelist():
            if m.endswith("/"):
                continue
            data = z.read(m)
            if needle.encode() in data:
                try:
                    res["pos"] += scan_text(m, data.decode("utf-8", "replace"), needle)
                except Exception:
                    res["pos"].append(m + ":binary")
    except Exception as e:
        res["error"] = "%s: %s" % (type(e).__name__, str(e)[:80])
    return res


def scan_runner(needle):
    r = aws("s3api", "list-objects-v2", "--bucket", BUCKET, "--prefix", RUNNER_PREFIX, "--query", "Contents[].Key", "--output", "json")
    keys = [k for k in (json.loads(r.stdout.decode() or "[]") or []) if k and not k.endswith("/")] if r.returncode == 0 else None
    if keys is None:
        return None, [], ["list rc=%d" % r.returncode]
    hits, errs = [], []
    tmp = REPO / ".scratch_door6_runner_obj"
    for k in keys:
        g = aws("s3", "cp", "s3://%s/%s" % (BUCKET, k), str(tmp), "--only-show-errors")
        if g.returncode != 0:
            errs.append(k)
            continue
        txt = tmp.read_bytes().decode("utf-8", "replace")
        hits += ["%s %s" % (k, p) for p in scan_text("", txt, needle)]
    if tmp.exists():
        tmp.unlink()
    return keys, hits, errs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--needle", default="pipeline-complete")
    ap.add_argument("--workers", type=int, default=6)
    a = ap.parse_args()
    funcs = list_functions()
    zips = [n for n, t in funcs if t == "Zip"]
    images = [n for n, t in funcs if t != "Zip"]
    results = []
    with cf.ThreadPoolExecutor(max_workers=a.workers) as ex:
        for r in ex.map(lambda f: scan_function(f, a.needle), zips):
            results.append(r)
    errors = [r for r in results if r["error"]]
    hits = [r for r in results if r["pos"]]
    env_hits = [r for r in results if r["env"]]
    keys, rhits, rerrs = scan_runner(a.needle)
    rec = {"needle": a.needle, "denominators": {"functions_listed": len(funcs), "zip": len(zips), "image_not_scanned": len(images), "scanned_ok": len(zips) - len(errors),
                                                  "errors": len(errors), "runner_objects": None if keys is None else len(keys)},
           "function_hits": [{"function": r["function"], "positions": r["pos"][:12]} for r in hits],
           "env_hits": [{"function": r["function"], "variables": r["env"]} for r in env_hits],
           "errors": [{"function": r["function"], "error": r["error"]} for r in errors],
           "image_functions": images, "runner_hits": rhits[:40], "runner_errors": rerrs,
           "limits": ["container-image functions are not scanned", "layers are not scanned", "a key built from parts that never spell the needle is not found",
                      "an errored function is listed, not counted clean"], "claim": "measured"}
    Path(a.out).write_text(json.dumps(rec, indent=1), encoding="utf-8")
    print("CENSUS functions=%d zip=%d image=%d scanned=%d errors=%d hits_functions=%d env_hits=%d runner_objects=%s runner_hits=%d" % (
        len(funcs), len(zips), len(images), len(zips) - len(errors), len(errors), len(hits), len(env_hits), "none" if keys is None else len(keys), len(rhits)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
