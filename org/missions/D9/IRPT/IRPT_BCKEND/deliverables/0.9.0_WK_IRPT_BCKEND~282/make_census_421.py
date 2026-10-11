"""IB-pr-421 census writer (from IB-pr-416's make_census_416.py; ONE function). From the worktree root:
    python <this file> <scratch_dir> <pin> <candidate_map_repo_path> <out_json>
<pin> is the commit that holds the candidate map (the staged rows inside it are pinned to the PRODUCT commit, recorded as
product_commit). Runs release-census.py (read only; the live zip is read from AWS), attaches the BUILD_ONLY outputs
(<scratch>/zips/irpt-performance-adapter.1.zip and .2.zip), reads live_before (CodeSha256) and the rollback S3 version from AWS,
runs the name / attribute / method closure limbs on the built zip (and on the live zip), and finds each changed member's owner
commits (the commits that touched its path after the commit holding the LIVE blob, up to the one holding the BUILT blob).
ASCII only. No client data: counts, sha256 prefixes and commit subjects only.
"""
import base64
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, check=True).stdout.decode().strip())
scratch, pin, map_path, out_path = Path(sys.argv[1]), sys.argv[2], sys.argv[3], Path(sys.argv[4])
FN = "irpt-performance-adapter"
D278 = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~278/"
Y2 = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/checks/r2/signature_closure.py"
ATTR, METHOD = D278 + "signature_closure_attr.py", D278 + "method_call_limb_416.py"
TAB = chr(9)


def limb(script, zip_path):
    r = subprocess.run([sys.executable, script, str(zip_path)], cwd=str(ROOT), capture_output=True, timeout=120)
    line = r.stdout.decode().strip().splitlines()[-1]
    return dict(p.split("=") for p in line.split()[1:]), line


def git(*a):
    return subprocess.run(["git"] + list(a), cwd=str(ROOT), capture_output=True)


cmap = json.loads(git("show", "%s:%s" % (pin, map_path)).stdout.decode("utf-8"))
smap = cmap["functions"]
product = cmap["_repins_IB_pr_421"][FN][0]["new_pin"]


def source_path(member):
    for s in smap[FN].get("staged_from") or []:
        if s["packaged_as"] == member:
            return s["repo_path"]
    return "%s/%s" % (smap[FN]["source_dir"].strip("/"), member)


def blob_prefix(commit, path):
    r = git("show", "%s:%s" % (commit, path))
    return hashlib.sha256(r.stdout).hexdigest()[:12] if r.returncode == 0 else None


def owners(path, built_p, live_p):
    log = git("log", "--format=%H" + TAB + "%s", product, "--", path).stdout.decode("utf-8", "replace").strip().splitlines()
    rows = [(ln.split(TAB)[0], ln.split(TAB, 1)[1] if TAB in ln else "") for ln in log]
    pref = [(h, s, blob_prefix(h, path)) for h, s in rows]
    bi = next((i for i, (_, _, p) in enumerate(pref) if p == built_p), None)
    li = next((i for i, (_, _, p) in enumerate(pref) if p == live_p), None)
    if bi is None:
        return []
    chosen = pref[bi:li] if (li is not None and li > bi) else pref[bi:bi + 1]
    return [{"commit": h[:10], "subject": s[:110]} for h, s, _ in chosen]


cmd = [sys.executable, "infra/aws/lambda/ci/release-census.py", FN, "--pin", pin, "--map", map_path]
r = subprocess.run(cmd, cwd=str(ROOT), capture_output=True)
text = r.stdout.decode("utf-8", "replace")
changed = []
for line in text.splitlines():
    parts = line.split()
    if parts and parts[0] in ("changed", "added", "removed"):
        kv = dict(p.split("=", 1) for p in parts[2:] if "=" in p)
        built, live = kv.get("built", "-"), kv.get("live", "-")
        path = source_path(parts[1])
        changed.append({"member": parts[1], "status": parts[0], "built": built, "live": live, "source_path": path,
                        "inside_performance_dir": path.startswith("infra/aws/lambda/investor-reporting/performance/"),
                        "commits": owners(path, None if built == "-" else built, None if live == "-" else live)})
cfg = json.loads(subprocess.run(["aws", "lambda", "get-function-configuration", "--function-name", FN, "--output", "json"],
                                capture_output=True, check=True).stdout.decode("utf-8"))
vers = json.loads(subprocess.run(["aws", "s3api", "list-object-versions", "--bucket", "opal-313476888478-lambda-artifacts", "--prefix",
                                  "investor-reporting/%s.zip" % FN, "--output", "json"], capture_output=True, check=True).stdout.decode("utf-8"))["Versions"]
rollback = None
for v in vers:
    if v["Key"] != "investor-reporting/%s.zip" % FN:
        continue
    ho = json.loads(subprocess.run(["aws", "s3api", "head-object", "--bucket", "opal-313476888478-lambda-artifacts", "--key", v["Key"],
                                    "--version-id", v["VersionId"], "--output", "json"], capture_output=True, check=True).stdout.decode("utf-8"))
    if ho.get("Metadata", {}).get("content-sha256") == cfg["CodeSha256"]:
        rollback = v["VersionId"]
        break
z1, z2, live = scratch / "zips" / (FN + ".1.zip"), scratch / "zips" / (FN + ".2.zip"), scratch / "live" / (FN + ".zip")
h1, h2, lh = (hashlib.sha256(p.read_bytes()) for p in (z1, z2, live))
bs, bsl = limb(Y2, z1)
ba, bal = limb(ATTR, z1)
bm, bml = limb(METHOD, z1)
ls_, lsl = limb(Y2, live)
la, lal = limb(ATTR, live)
lm, lml = limb(METHOD, live)
doc = {"to_id": "IRPT_BCKEND.TO-IB-pr-421", "function": FN, "pin": pin, "product_commit": product, "candidate_map": map_path,
       "built_sha256": base64.b64encode(h1.digest()).decode(), "built_sha256_hex": h1.hexdigest(), "built_bytes": z1.stat().st_size,
       "built_twice_identical": h1.digest() == h2.digest(),
       "live_before": cfg["CodeSha256"], "live_sha256_of_fetched_zip": base64.b64encode(lh.digest()).decode(),
       "live_fetched_zip_matches_codesha256": base64.b64encode(lh.digest()).decode() == cfg["CodeSha256"], "live_last_modified": cfg["LastModified"],
       "rollback_version": rollback, "rollback_bucket_key": "s3://opal-313476888478-lambda-artifacts/investor-reporting/%s.zip" % FN,
       "built_signature_mismatched": int(bs["mismatched"]), "built_attribute_mismatched": int(ba["attr_mismatched"]),
       "built_method_mismatched": int(bm["mismatched"]), "built_attribute_checked": int(ba["attr_checked"]), "built_method_checked": int(bm["checked"]),
       "built_last_lines": {"signature": bsl, "attribute": bal, "method": bml},
       "live_signature_mismatched": int(ls_["mismatched"]), "live_attribute_mismatched": int(la["attr_mismatched"]),
       "live_method_mismatched": int(lm["mismatched"]),
       "live_last_lines": {"signature": lsl, "attribute": lal, "method": lml},
       "changed_members": changed, "changed_members_all_inside_performance_dir": all(c["inside_performance_dir"] for c in changed),
       "census_command": " ".join(cmd[1:]), "census_rc": r.returncode,
       "census_summary": [ln for ln in text.splitlines() if ln.startswith(("function=", "changed_members="))],
       "build_only": {"command": "TMPDIR=<scratch> BAU_SOURCE_MAP_OVERRIDE=<candidate map> BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-performance-adapter",
                      "nothing_uploaded": True, "source_map_untouched": True}}
out_path.write_text(json.dumps(doc, indent=1) + chr(10), encoding="utf-8")
print(FN, doc["built_sha256"], doc["built_twice_identical"], doc["live_before"], doc["rollback_version"],
      doc["built_signature_mismatched"], doc["built_attribute_mismatched"], doc["built_method_mismatched"], "changed", len(changed))
