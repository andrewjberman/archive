"""IB-pr-460 moved-members probe (read only; ASCII). From the worktree root:
    python <this file> <scratch_dir> <base_commit> <fn> [<fn> ...]
Per function: compares <scratch>/live/<fn>.zip with <scratch>/zips/<fn>.1.zip member by member; for each member whose bytes differ, finds
its repo path (a staged_from row of the REAL map, else source_dir/<member>), the NEWEST commit on that path whose blob equals the live
bytes (live_blob_commit), and owning_commits = git log <live_blob_commit>..<base> -- <repo_path>. Prints one JSON object per function."""
import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path

scratch, base, fns = Path(sys.argv[1]), sys.argv[2], sys.argv[3:]
BASE = subprocess.run(["git", "rev-parse", base], capture_output=True, check=True).stdout.decode().strip()
smap = json.loads(subprocess.run(["git", "show", "HEAD:infra/aws/lambda/ci/lambda-source-map.json"], capture_output=True, check=True).stdout.decode("utf-8"))["functions"]


def git(*a):
    return subprocess.run(["git"] + list(a), capture_output=True)


out = {}
for fn in fns:
    e = smap[fn]
    staged = {s["packaged_as"]: s for s in e.get("staged_from") or []}
    sd = e["source_dir"].strip("/")
    L, B = zipfile.ZipFile(scratch / "live" / (fn + ".zip")), zipfile.ZipFile(scratch / "zips" / (fn + ".1.zip"))
    nl = {i.filename for i in L.infolist() if not i.filename.endswith("/")}
    nb = {i.filename for i in B.infolist() if not i.filename.endswith("/")}
    rows = []
    for m in sorted(nl & nb):
        lb, bb = L.read(m), B.read(m)
        if lb == bb:
            continue
        path = staged[m]["repo_path"] if m in staged else "%s/%s" % (sd, m)
        old_pin = staged[m]["pin"] if m in staged else None
        live_commit = None
        for h in git("log", "--format=%H", BASE, "--", path).stdout.decode().split():
            r = git("show", "%s:%s" % (h, path))
            if r.returncode == 0 and r.stdout == lb:
                live_commit = h
                break
        built_eq_base = git("show", "%s:%s" % (BASE, path)).stdout == bb
        commits = []
        if live_commit:
            commits = [ln.split(" ", 1) for ln in git("log", "--format=%h %s", "%s..%s" % (live_commit, BASE), "--", path).stdout.decode("utf-8", "replace").strip().splitlines()]
        rows.append({"member": m, "repo_path": path, "staged_row_pin": old_pin[:10] if old_pin else None, "live_sha": hashlib.sha256(lb).hexdigest(), "built_sha": hashlib.sha256(bb).hexdigest(),
                     "live_blob_commit": live_commit[:10] if live_commit else None, "built_bytes_equal_base_blob": built_eq_base,
                     "owning_commits": [{"commit": h, "subject": s[:120]} for h, s in commits]})
    out[fn] = {"members_live": len(nl), "members_built": len(nb), "added": sorted(nb - nl), "removed": sorted(nl - nb), "moved": rows}
print(json.dumps(out, indent=1))
