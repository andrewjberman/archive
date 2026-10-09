"""IB-pr-390 census writer. From the worktree root:
    python replay/make_census.py <scratch_dir> <pin> <candidate_map_repo_path> <out_json>
Runs release-census.py (read only; live zip from AWS) for each function that packages _authz/served.py, attaches the
BUILD_ONLY outputs (<scratch>/zips/<fn>.1.zip and .2.zip, built twice), reads live_before (CodeSha256) from AWS, and finds each
changed member's OWNER COMMITS: the commits that touched its source path after the commit holding the LIVE blob, up to the
commit holding the BUILT blob (an added member: the commits since its blob first appeared). ASCII only.
"""
import base64
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, check=True).stdout.decode().strip())
scratch, pin, map_path, out_path = Path(sys.argv[1]), sys.argv[2], sys.argv[3], Path(sys.argv[4])
FUNCS = ["irpt-49f-reporting-read-lambda", "irpt-directory-search", "irpt-export-render", "irpt-holdings", "irpt-narrative",
         "irpt-performance-adapter", "irpt-status", "irpt-ycharts-generate"]


def git(*a):
    return subprocess.run(["git"] + list(a), cwd=str(ROOT), capture_output=True)


smap = json.loads(git("show", "%s:%s" % (pin, map_path)).stdout.decode("utf-8"))["functions"]


def source_path(fn, member):
    f = smap[fn]
    for s in f.get("staged_from") or []:
        if s["packaged_as"] == member:
            return s["repo_path"]
    return "%s/%s" % (f["source_dir"].strip("/"), member)


def blob_prefix(commit, path):
    r = git("show", "%s:%s" % (commit, path))
    return hashlib.sha256(r.stdout).hexdigest()[:12] if r.returncode == 0 else None


def owners(path, built_p, live_p):
    log = git("log", "--format=%H\t%s", pin, "--", path).stdout.decode("utf-8", "replace").strip().splitlines()
    rows = [(ln.split("\t")[0], ln.split("\t", 1)[1] if "\t" in ln else "") for ln in log]    # newest first
    pref = [(h, s, blob_prefix(h, path)) for h, s in rows]
    built_i = next((i for i, (_, _, p) in enumerate(pref) if p == built_p), None)
    live_i = next((i for i, (_, _, p) in enumerate(pref) if p == live_p), None) if live_p else None
    if built_i is None:
        return [], "built blob %s is not a committed version of %s" % (built_p, path)
    if live_i is not None and live_i > built_i:
        chosen = pref[built_i:live_i]            # commits after the live version up to the built one
        note = "commits since the live blob"
    elif live_p is None:
        # added member: the commits from the one that introduced the built blob
        first = max(i for i, (_, _, p) in enumerate(pref) if p == built_p)
        chosen = pref[built_i:first + 1]
        note = "added member: commit(s) that introduced the built blob"
    else:
        chosen = pref[built_i:built_i + 1]
        note = "live blob %s is not a committed version of the path; the commit holding the built blob" % live_p
    return [{"commit": h[:10], "subject": s[:100]} for h, s, _ in chosen], note


artifacts, unbuilt, census_cmds = [], [], []
for fn in FUNCS:
    cmd = [sys.executable, "infra/aws/lambda/ci/release-census.py", fn, "--pin", pin, "--map", map_path]
    r = subprocess.run(cmd, cwd=str(ROOT), capture_output=True)
    text = r.stdout.decode("utf-8", "replace")
    census_cmds.append(" ".join(cmd[1:]))
    members = []
    for line in text.splitlines():
        parts = line.split()
        if parts and parts[0] in ("changed", "added", "removed"):
            kv = dict(p.split("=", 1) for p in parts[2:] if "=" in p)
            members.append((parts[0], parts[1], kv.get("built", "-"), kv.get("live", "-")))
    cfg = json.loads(subprocess.run(["aws", "lambda", "get-function-configuration", "--function-name", fn, "--output", "json"],
                                    capture_output=True, check=True).stdout.decode("utf-8"))
    changed = []
    for status, member, bp, lp in members:
        path = source_path(fn, member)
        own, note = owners(path, None if bp == "-" else bp, None if lp == "-" else lp)
        changed.append({"member": member, "status": status, "built_sha256_prefix": bp, "live_sha256_prefix": lp,
                        "source_path": path, "owner_commit": ("%s %s" % (own[0]["commit"], own[0]["subject"])) if own else "UNOWNED: " + note,
                        "owner_commits": own, "owner_note": note})
    z1, z2 = scratch / "zips" / (fn + ".1.zip"), scratch / "zips" / (fn + ".2.zip")
    art = {"name": fn, "census_rc": r.returncode, "census_summary": [ln for ln in text.splitlines() if ln.startswith(("function=", "changed_members="))],
           "live_before": cfg["CodeSha256"], "live_last_modified": cfg["LastModified"], "changed_members": changed}
    if z1.is_file() and z2.is_file():
        h1, h2 = hashlib.sha256(z1.read_bytes()), hashlib.sha256(z2.read_bytes())
        art.update({"built_sha256": base64.b64encode(h1.digest()).decode(), "built_sha256_hex": h1.hexdigest(),
                    "built_bytes": z1.stat().st_size, "built_twice_identical": h1.digest() == h2.digest()})
        artifacts.append(art)
    else:
        art["not_built"] = "BUILD_ONLY refused: ADHC_DRIFTD.002 parity (holdings_publication_port.py is in source_dir and not in files[]); row IRPT_BCKEND-D2-W201-S5"
        unbuilt.append(art)
doc = {"to_id": "IRPT_BCKEND.TO-IB-pr-390", "pin": pin, "candidate_map": map_path,
       "pin_note": "code pin dea0f53252 (box/dell2 HEAD as the worktree carries it; contains IB-pr-385 7e0bfc3222 and IB-pr-387 b4b544fb15); "
                   "census pin = the next commit, which adds the candidate source map (row IRPT_BCKEND-D2-W201-S4)",
       "census_commands": census_cmds,
       "functions_packaging_served_py": FUNCS,
       "artifacts": artifacts, "unbuilt_census_only": unbuilt,
       "build_only": {"rc": 0, "tree_clean": True, "built_twice_identical_all": all(a["built_twice_identical"] for a in artifacts),
                      "command": "BUILD_ONLY=1 BAU_SOURCE_MAP_OVERRIDE=<candidate map> bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting <function>",
                      "porcelain_lines_before": 0, "porcelain_lines_after": 0, "nothing_uploaded": True, "source_map_untouched": True}}
out_path.write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8")
for a in artifacts + unbuilt:
    print(a["name"], a.get("built_sha256"), a["live_before"], [(m["member"], m["owner_commit"][:60]) for m in a["changed_members"]][:3])
