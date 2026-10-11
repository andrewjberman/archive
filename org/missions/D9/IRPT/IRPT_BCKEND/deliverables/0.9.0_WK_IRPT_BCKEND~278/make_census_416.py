"""IB-pr-416 census writer (from IB-pr-409's make_census.py; three functions; both closure limbs). From the worktree root:
    python make_census_416.py <scratch_dir> <pin> <candidate_map_repo_path> <out_json>
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
FUNCS = ["irpt-performance-adapter", "irpt-narrative", "irpt-status"]
Y2 = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/checks/r2/signature_closure.py"
DDIR = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~278/"
ATTR = DDIR + "signature_closure_attr.py"
METHOD = DDIR + "method_call_limb_416.py"
PINCOH = DDIR + "pin_coherence_candidate_416.py"
PINCOH_REAL = str(scratch / "tools" / "pin_coherence.py")       # git show box/dell2:org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/checks/r2/pin_coherence.py
REAL_MAP_REF = sys.argv[5] if len(sys.argv) > 5 else "box/dell2"       # the real source map the live pairing is read from
REPLAY = json.loads((Path(sys.argv[4]).parent / "IB117-1_replay.json").read_text(encoding="utf-8"))


def limbs(zip_path):
    """(orig_mismatched, attr_mismatched, attr_checked, last_line) for one zip, both instruments run on its bytes."""
    o = subprocess.run([sys.executable, Y2, str(zip_path)], cwd=str(ROOT), capture_output=True, timeout=120)
    a = subprocess.run([sys.executable, ATTR, str(zip_path)], cwd=str(ROOT), capture_output=True, timeout=120)
    ol = o.stdout.decode().strip().splitlines()[-1]
    al = a.stdout.decode().strip().splitlines()[-1]
    kv = dict(p.split("=") for p in al.split()[1:])
    ko = dict(p.split("=") for p in ol.split()[1:])
    return int(ko["mismatched"]), int(kv["attr_mismatched"]), int(kv["attr_checked"]), al



def method_limb(zip_path):
    """(checked, mismatched, last_line) of the method-call limb (static) on one zip."""
    m = subprocess.run([sys.executable, METHOD, str(zip_path)], cwd=str(ROOT), capture_output=True, timeout=120)
    ml = m.stdout.decode().strip().splitlines()[-1]
    kv = dict(p.split("=") for p in ml.split()[1:])
    return int(kv["checked"]), int(kv["mismatched"]), ml


def coherence(cmd):
    """(skewed edges, last_line) of a pin_coherence run (exit 1 on a skew is normal)."""
    r = subprocess.run([sys.executable] + cmd, cwd=str(ROOT), capture_output=True, timeout=120)
    ln = r.stdout.decode().strip().splitlines()[-1]
    return int(dict(p.split("=") for p in ln.split()[1:])["skewed"]), ln


def replay_summary(fn):
    """The replay arms of one function, by kind: counts of identical / expected-diff / other, and the method-call arm per route."""
    arms = [a for a in REPLAY["arms"] if a["function"] == fn]
    tally = {}
    for a in arms:
        tally[a["verdict"]] = tally.get(a["verdict"], 0) + 1
    mc = [a for a in arms if a["name"].startswith("method-call arm")]
    lc = [a for a in arms if a["name"].startswith(("prospect arm", "enforcer build"))]
    return {"arms": len(arms), "verdicts": tally, "every_route_replayed": [a["name"].split(" ")[1].rstrip(":") for a in mc],
            "binding_cases_arm": next(a["detail"] for a in arms if a["name"].startswith("binding cases")),
            "live_call_arm_verdicts": sorted(a["verdict"] for a in lc if not a["negative_control"]),
            "method_call_arm_verdicts": sorted(a["verdict"] for a in mc), "negative_controls": sum(1 for a in arms if a["negative_control"])}


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


artifacts, census_cmds, rows = [], [], []
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
    live = scratch / "live" / (fn + ".zip")
    ho = json.loads(subprocess.run(["aws", "s3api", "head-object", "--bucket", "opal-313476888478-lambda-artifacts", "--key",
                                    "investor-reporting/%s.zip" % fn, "--output", "json"], capture_output=True, check=True).stdout.decode("utf-8"))
    h1, h2 = hashlib.sha256(z1.read_bytes()), hashlib.sha256(z2.read_bytes())
    lh = hashlib.sha256(live.read_bytes())
    lo, la, lac, ll = limbs(live)
    bo, ba, bac, bl = limbs(z1)
    lmk, lmm, lml = method_limb(live)
    bmk, bmm, bml = method_limb(z1)
    live_skew, live_skew_line = coherence([PINCOH_REAL, str(ROOT), fn, REAL_MAP_REF])
    built_skew, built_skew_line = coherence([PINCOH, str(ROOT), fn, str(ROOT / map_path)])
    row = {"function": fn, "pin": pin, "built_sha256": base64.b64encode(h1.digest()).decode(), "built_sha256_hex": h1.hexdigest(),
           "built_bytes": z1.stat().st_size, "built_twice_identical": h1.digest() == h2.digest(),
           "live_sha256": base64.b64encode(lh.digest()).decode(), "live_sha256_matches_codesha256": base64.b64encode(lh.digest()).decode() == cfg["CodeSha256"],
           "live_last_modified": cfg["LastModified"],
           "live_signature_mismatched": lo, "live_attribute_mismatched": la, "live_attribute_checked": lac, "live_last_line": ll,
           "built_signature_mismatched": bo, "built_attribute_mismatched": ba, "built_attribute_checked": bac, "built_last_line": bl,
           "live_method_checked": lmk, "live_method_mismatched": lmm, "live_method_last_line": lml,
           "built_method_checked": bmk, "built_method_mismatched": bmm, "built_method_last_line": bml,
           "live_untested_import_pairings": live_skew, "live_pin_coherence_last_line": live_skew_line,
           "built_untested_import_pairings": built_skew, "built_pin_coherence_last_line": built_skew_line,
           "replay": replay_summary(fn),
           "repins": json.loads(git("show", "%s:%s" % (pin, map_path)).stdout.decode("utf-8"))["_repins_IB_pr_416"].get(fn, []),
           "changed_members": changed,
           "s3_rollback_version": ho["VersionId"], "s3_content_sha256_metadata": ho.get("Metadata", {}).get("content-sha256"),
           "s3_is_live_zip": ho.get("Metadata", {}).get("content-sha256") == cfg["CodeSha256"],
           "census_rc": r.returncode, "census_summary": [ln for ln in text.splitlines() if ln.startswith(("function=", "changed_members="))]}
    rows.append(row)
doc = {"to_id": "IRPT_BCKEND.TO-IB-pr-416", "pin": pin, "candidate_map": map_path, "census_commands": census_cmds,
       "tree_pin_of_staged_rows": json.loads(git("show", "%s:%s" % (pin, map_path)).stdout.decode("utf-8"))["_repins_IB_pr_416"]["irpt-narrative"][0]["new_pin"],
       "instruments": {"name_and_attribute_limbs": ATTR, "original": Y2},
       "functions": rows,
       "build_only": {"command": "TMPDIR=<scratch> BAU_SOURCE_MAP_OVERRIDE=<candidate map> BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting <function>",
                      "porcelain_lines_before": 0, "porcelain_lines_after": 0, "nothing_uploaded": True, "source_map_untouched": True}}
out_path.write_text(json.dumps(doc, indent=1) + chr(10), encoding="utf-8")
for r in rows:
    print(r["function"], r["built_sha256"], r["built_twice_identical"], "live", r["live_signature_mismatched"], r["live_attribute_mismatched"],
          "built", r["built_signature_mismatched"], r["built_attribute_mismatched"], "changed", len(r["changed_members"]))
