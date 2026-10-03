"""DB10-1-AC2 -- the P-2 packet's three artifacts, REHEARSED from the map without building or uploading: every pin is sound, the
members rounds 6-9 changed are packaged at HEAD, and each materialized package imports; the publish package resolves its
directory bucket with no environment variable (row IRPT_DASHBD-W4-S1).

For each of irpt-reporting-gold-lambda, irpt-reporting-publish-lambda and irpt-reporting-read-lambda in
infra/aws/lambda/ci/lambda-source-map.json:
  1. every staged_from entry: `git show <pin>:<repo_path>` succeeds and its sha256 (hex) equals the entry's `sha256`;
  2. the package is materialized into a temp dir: each `files` member is the staged blob whose `packaged_as` equals it, else the
     HEAD blob of <source_dir>/<member>;
  3. AT HEAD: in the gold package, account_return_daily.py and sources.json equal HEAD's blobs; in every package that carries
     data/assets/scripts/gold/irpt_reporting/sources.json, it equals HEAD's blob;
  4. a fresh python in the temp dir (cwd = the package root, the repo NOT on sys.path) imports `handler` (gold, publish) or
     `entry` (read) with exit 0;
  5. publish only: in that package, with IRPT_DIRECTORY_BUCKET_MAP unset, handler.directory_bucket("49financial") returns a
     non-empty bucket and handler._ids_module() loads.
Usage: python <this file> <repo_root>
"""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

MAP = "infra/aws/lambda/ci/lambda-source-map.json"
FNS = {"irpt-reporting-gold-lambda": "handler", "irpt-reporting-publish-lambda": "handler", "irpt-reporting-read-lambda": "entry"}
SOURCES = "data/assets/scripts/gold/irpt_reporting/sources.json"
GOLD_AT_HEAD = ("data/assets/scripts/gold/irpt_reporting/account_return_daily.py", SOURCES)


def fail(msg):
    print("FAIL: " + msg)
    print("DB10-1-AC2 FAIL")
    sys.exit(1)


def blob(root, ref, path):
    r = subprocess.run(["git", "show", "%s:%s" % (ref, path)], cwd=str(root), capture_output=True)
    if r.returncode != 0:
        return None
    return r.stdout


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    fmap = json.loads((root / MAP).read_text(encoding="utf-8"))["functions"]
    summary = []
    for name, module in FNS.items():
        e = fmap.get(name)
        if not e:
            fail("%s is not in the map" % name)
        staged = {}
        for s in e.get("staged_from") or []:
            b = blob(root, s["pin"], s["repo_path"])
            if b is None:
                fail("%s: pin %s:%s does not resolve" % (name, s["pin"][:10], s["repo_path"]))
            if hashlib.sha256(b).hexdigest() != s.get("sha256"):
                fail("%s: %s at %s does not hash to its declared sha256" % (name, s["repo_path"], s["pin"][:10]))
            staged[s["packaged_as"]] = (s["repo_path"], b)
        tmp = Path(tempfile.mkdtemp(prefix="db10-"))
        for member in e.get("files") or []:
            if member in staged:
                data = staged[member][1]
            else:
                data = blob(root, "HEAD", "%s/%s" % (e["source_dir"], member))
                if data is None:
                    fail("%s: member %s is neither staged nor at HEAD under %s" % (name, member, e["source_dir"]))
            out = tmp / member
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(data)
        must = GOLD_AT_HEAD if name == "irpt-reporting-gold-lambda" else (SOURCES,)
        for path in must:
            if path not in staged:
                if name == "irpt-reporting-gold-lambda":
                    fail("%s: %s is not staged" % (name, path))
                continue
            if staged[path][1] != blob(root, "HEAD", staged[path][0]):
                fail("%s: %s is packaged at a pin that is not HEAD's blob" % (name, path))
        env = {k: v for k, v in os.environ.items() if k not in ("PYTHONPATH", "IRPT_DIRECTORY_BUCKET_MAP")}
        probe = "import %s" % module
        if name == "irpt-reporting-publish-lambda":
            probe += ("\nb = handler.directory_bucket('49financial')\nassert b, 'empty bucket'\nhandler._ids_module()\n"
                      "print('BUCKET_OK')")
        r = subprocess.run([sys.executable, "-c", probe], cwd=str(tmp), env=env, capture_output=True, text=True, timeout=110)
        if r.returncode != 0:
            fail("%s: the materialized package fails its probe: %s" % (name, (r.stderr or r.stdout).strip()[-300:]))
        if name == "irpt-reporting-publish-lambda" and "BUCKET_OK" not in r.stdout:
            fail("%s: directory_bucket did not resolve" % name)
        summary.append("%s %d members (%d staged)" % (name.replace("irpt-reporting-", "").replace("-lambda", ""),
                                                      len(e.get("files") or []), len(staged)))
    print("OK: " + "; ".join(summary) + "; pins sound, changed members at HEAD, each package imports; publish resolves its "
          "directory bucket with no environment variable")
    print("DB10-1-AC2 PASS")


if __name__ == "__main__":
    main()
