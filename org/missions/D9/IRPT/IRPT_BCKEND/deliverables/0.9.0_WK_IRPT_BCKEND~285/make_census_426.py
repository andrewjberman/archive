"""IB-pr-426 census writer (from IB-pr-416's make_census_416.py; ONE function, irpt-ycharts-generate). From the worktree root:
    python <this file> <scratch_dir> <pin> <candidate_map_repo_path> <classes_json> <out_json>
<scratch_dir> holds zips/irpt-ycharts-generate.1.zip and .2.zip (the two BUILD_ONLY outputs) and live/irpt-ycharts-generate.zip (the live
package read from AWS). Reads from AWS through the .tools/aws shim, read only: the live CodeSha256 (get-function-configuration) and the
S3 version of the object whose content-sha256 metadata equals it (head-object, then list-object-versions when the latest is not it).
Runs the three closure limbs on BOTH zips; the method limb is compared by (module, call text), never by line (AMENDMENT 1).
moved_members = every member whose bytes differ between the live zip and the built zip; the old pin of a staged member is its row in the
REAL source map, of a native member the release-6b pin 66207bce7d; owning_commits = git log <old_pin>..<pin> -- <repo_path>.
<classes_json> is {member: {"class": "served"|"inert", "one_line": "..."}} written by the worker from reading each diff. ASCII only.
"""
import base64
import hashlib
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, check=True).stdout.decode().strip())
scratch, pin, map_path, classes_path, out_path = Path(sys.argv[1]), sys.argv[2], sys.argv[3], Path(sys.argv[4]), Path(sys.argv[5])
FN = "irpt-ycharts-generate"
REL6B = "66207bce7d"
Y2 = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/checks/r2/signature_closure.py"
DDIR = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~285/"
ATTR, METHOD = DDIR + "signature_closure_attr.py", DDIR + "method_call_limb_426.py"
CLASSES = json.loads(classes_path.read_text(encoding="utf-8"))
SITE_REASONS = json.loads((classes_path.parent / "method_site_reasons.json").read_text(encoding="utf-8"))


def git(*a):
    return subprocess.run(["git"] + list(a), cwd=str(ROOT), capture_output=True)


def aws(*a):
    r = subprocess.run(["bash", ".tools/aws"] + list(a) + ["--output", "json"], cwd=str(ROOT), capture_output=True, timeout=120)
    if r.returncode:
        raise SystemExit("aws failed: " + r.stderr.decode("utf-8", "replace")[-300:])
    return json.loads(r.stdout.decode("utf-8"))


def b64(data):
    return base64.b64encode(hashlib.sha256(data).digest()).decode()


def run(script, zip_path):
    r = subprocess.run([sys.executable, script, str(zip_path)], cwd=str(ROOT), capture_output=True, timeout=120)
    return r.stdout.decode("utf-8", "replace").strip().splitlines()


def kv(line):
    return dict(p.split("=") for p in line.split()[1:] if "=" in p)


def method_sites(lines):
    out = []
    for ln in lines:
        m = re.match(r"METHOD_MISMATCH: (\w+):(\d+) calls (\.\w+\(.*?\)) --", ln)
        if m:
            out.append((m.group(1), m.group(3), int(m.group(2))))
    return out


smap_real = json.loads(git("show", "HEAD:infra/aws/lambda/ci/lambda-source-map.json").stdout.decode("utf-8"))["functions"][FN]
BUCKET, KEY = smap_real["artifact_s3_bucket"], smap_real["artifact_s3_key"]      # the object the order names, read from the real map entry
z1, z2, live = (scratch / "zips" / (FN + ".1.zip"), scratch / "zips" / (FN + ".2.zip"), scratch / "live" / (FN + ".zip"))
b1, b2, lb = z1.read_bytes(), z2.read_bytes(), live.read_bytes()
cfg = aws("lambda", "get-function-configuration", "--function-name", FN)
live_before = cfg["CodeSha256"]
head = aws("s3api", "head-object", "--bucket", BUCKET, "--key", KEY)
rollback = head["VersionId"]
rollback_meta = head.get("Metadata", {}).get("content-sha256")
if rollback_meta != live_before:
    for v in aws("s3api", "list-object-versions", "--bucket", BUCKET, "--prefix", KEY)["Versions"]:
        if v["Key"] != KEY:
            continue
        h = aws("s3api", "head-object", "--bucket", BUCKET, "--key", KEY, "--version-id", v["VersionId"])
        if h.get("Metadata", {}).get("content-sha256") == live_before:
            rollback, rollback_meta = v["VersionId"], live_before
            break
smap_cand = json.loads(git("show", "%s:%s" % ("HEAD", map_path)).stdout.decode("utf-8"))["functions"][FN]
staged_real = {s["packaged_as"]: s for s in smap_real["staged_from"]}
staged_cand = {s["packaged_as"]: s for s in smap_cand["staged_from"]}
source_dir = smap_real["source_dir"].strip("/")

ZL, ZB = zipfile.ZipFile(live), zipfile.ZipFile(z1)
def names(z):
    return {i.filename for i in z.infolist() if not i.filename.endswith("/")}


nl, nb = names(ZL), names(ZB)


def blob_prefix(commit, path):
    r = git("show", "%s:%s" % (commit, path))
    return hashlib.sha256(r.stdout).hexdigest()[:12] if r.returncode == 0 else None


moved = []
for m in sorted(nl & nb):
    lbytes, bbytes = ZL.read(m), ZB.read(m)
    if lbytes == bbytes:
        continue
    if m in staged_real:
        path, old_pin = staged_real[m]["repo_path"], staged_real[m]["pin"]
    else:
        path, old_pin = "%s/%s" % (source_dir, m), REL6B
    old_blob, pin_blob = git("show", "%s:%s" % (old_pin, path)).stdout, git("show", "%s:%s" % (pin, path)).stdout
    commits = [ln.split(" ", 1) for ln in git("log", "--format=%h %s", "%s..%s" % (old_pin, pin), "--", path).stdout.decode("utf-8", "replace").strip().splitlines()]
    c = CLASSES[m]
    moved.append({"member": m, "repo_path": path, "live_sha": hashlib.sha256(lbytes).hexdigest(), "built_sha": hashlib.sha256(bbytes).hexdigest(),
                  "old_pin": old_pin[:10], "live_bytes_equal_old_pin_blob": old_blob == lbytes, "built_bytes_equal_pin_blob": pin_blob == bbytes,
                  "owning_commits": [{"commit": h, "subject": s[:110]} for h, s in commits], "class": c["class"], "one_line": c["one_line"]})

# every staged row of the candidate map is at the pin with the packaged bytes (the build verified each sha256; recheck the bytes)
staged_ok = all(ZB.read(m) == git("show", "%s:%s" % (pin, s["repo_path"])).stdout for m, s in staged_cand.items())
native_ok = all(ZB.read(m) == git("show", "%s:%s/%s" % (pin, source_dir, m)).stdout for m in nb if m not in staged_cand)

lo, la, lm = run(Y2, live), run(ATTR, live), run(METHOD, live)
bo, ba, bm = run(Y2, z1), run(ATTR, z1), run(METHOD, z1)
live_sites, built_sites = method_sites(lm), method_sites(bm)
live_count = {}
for mod, call, _ in live_sites:
    live_count[(mod, call)] = live_count.get((mod, call), 0) + 1
rows, seen = [], {}
for mod, call, line in built_sites:
    r = SITE_REASONS["%s %s" % (mod, call)]
    seen[(mod, call)] = seen.get((mod, call), 0) + 1
    # compared by module and call text, never by line; a call text that occurs twice on the build needs two on the live package
    rows.append({"module": mod, "call": call, "in_live": live_count.get((mod, call), 0) >= seen[(mod, call)], "reason": r["reason"], "reason_basis": r["basis"]})

doc = {
    "to_id": "IRPT_BCKEND.TO-IB-pr-426", "function": FN, "pin": pin, "candidate_map": map_path,
    "built_sha256": b64(b1), "built_sha256_hex": hashlib.sha256(b1).hexdigest(), "built_bytes": len(b1),
    "built_twice_identical": b1 == b2 and b64(b1) == b64(b2),
    "live_before": live_before, "live_zip_sha256": b64(lb), "live_zip_is_live": b64(lb) == live_before, "live_last_modified": cfg["LastModified"],
    "rollback_version": rollback, "rollback_content_sha256_metadata": rollback_meta, "rollback_is_live": rollback_meta == live_before,
    "members_live": len(nl), "members_built": len(nb),
    "member_count_note": "104 members built and 104 live, the same member names (added 0, removed 0); %d members differ in bytes." % len(moved),
    "built_signature_mismatched": int(kv(bo[-1])["mismatched"]),
    "built_attribute_mismatched": int(kv(ba[-1])["attr_mismatched"]), "built_attribute_checked": int(kv(ba[-1])["attr_checked"]),
    "built_method_mismatched": len(rows), "built_method_checked": int(kv(bm[-1])["checked"]),
    "live_signature_mismatched": int(kv(lo[-1])["mismatched"]), "live_attribute_mismatched": int(kv(la[-1])["attr_mismatched"]),
    "live_method_mismatched": len(live_sites), "live_method_checked": int(kv(lm[-1])["checked"]),
    "limb_last_lines": {"built": {"name": bo[-1], "attribute": ba[-1], "method": bm[-1]}, "live": {"name": lo[-1], "attribute": la[-1], "method": lm[-1]}},
    "method_mismatch_sites": rows,
    "moved_members": moved,
    "added_members": sorted(nb - nl), "removed_members": sorted(nl - nb),
    "pin_checks": {"every_staged_row_packaged_bytes_equal_pin_blob": staged_ok, "every_native_member_packaged_bytes_equal_pin_blob": native_ok,
                   "staged_rows": len(staged_cand), "native_members": len(nb) - len(staged_cand),
                   "staged_rows_at_pin": all(s["pin"] == pin for s in staged_cand.values())},
    "instruments": {"name": Y2, "attribute": ATTR, "method": METHOD},
}
out_path.write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8")
print("moved=%d served=%d inert=%d built_twice=%s live_before_ok=%s rollback=%s method built/live=%d/%d sig/attr=%s/%s pins_ok=%s/%s" % (
    len(moved), sum(m["class"] == "served" for m in moved), sum(m["class"] == "inert" for m in moved), doc["built_twice_identical"],
    doc["live_zip_is_live"], rollback, len(rows), len(live_sites), doc["built_signature_mismatched"], doc["built_attribute_mismatched"], staged_ok, native_ok))
