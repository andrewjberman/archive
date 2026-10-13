"""IB-pr-498 release census of irpt-holdings (BUILD ONLY; reads zip bytes and git blobs; no AWS write, no invoke).

Usage: python -I census_498.py <worktree> <built_zip> <built_zip_second_build> <live_zip>
Writes IB171-3_release_census.json next to this file. Prints one line per measured value.
"""
import base64
import hashlib
import json
import os
import re
import subprocess
import sys
import zipfile

W = sys.argv[1].replace("\\", "/")
BUILT, BUILT2, LIVE = sys.argv[2], sys.argv[3], sys.argv[4]
HERE = os.path.dirname(os.path.abspath(__file__))
D = HERE.replace("\\", "/") + "/"
CAND = D + "candidate_source_map_498.json"
REAL = W + "/infra/aws/lambda/ci/lambda-source-map.json"
PIN = "f91aedd1efd0ea1f36966593fbf949595e49737e"
FN = "irpt-holdings"
SIG = W + "/org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~278/signature_closure_attr.py"
REAL_BEFORE = "a8c55c584d0f346bbf552dad63871a040e8eb12a8774d613ccf160126b739987"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def zmembers(p):
    z = zipfile.ZipFile(p)
    out = {}
    for i in z.infolist():
        if not i.filename.endswith("/"):
            out[i.filename] = z.read(i.filename)
    return out


def git_blob(path, pin=PIN):
    r = subprocess.run(["git", "-C", W, "show", pin + ":" + path], capture_output=True)
    if r.returncode != 0:
        raise SystemExit("git show failed for " + path)
    return r.stdout


def instrument(zip_path):
    r = subprocess.run([sys.executable, "-I", SIG, zip_path], capture_output=True)
    lines = [ln for ln in (r.stdout + r.stderr).decode("utf-8", "replace").splitlines() if ln.strip()]
    last = lines[-1] if lines else ""
    m1 = re.search(r"\bmismatched=(\d+)", last)
    m2 = re.search(r"attr_mismatched=(\d+)", last)
    if not (m1 and m2):
        raise SystemExit("instrument line unreadable: " + last[:200])
    return last, int(m1.group(1)), int(m2.group(1)), r.returncode


built_bytes = open(BUILT, "rb").read()
built2_bytes = open(BUILT2, "rb").read()
live_bytes = open(LIVE, "rb").read()
b_sha, b2_sha, l_sha = sha(built_bytes), sha(built2_bytes), sha(live_bytes)
print("built_sha256=" + b_sha)
print("second_build_sha256=" + b2_sha)
print("live_sha256=" + l_sha)
if b_sha != b2_sha:
    raise SystemExit("NOT byte-identical twice")

built = zmembers(BUILT)
live = zmembers(LIVE)
cand = json.load(open(CAND, encoding="utf-8"))
rows = {r["packaged_as"]: r for r in cand["functions"][FN]["staged_from"]}

only_b = sorted(set(built) - set(live))
only_l = sorted(set(live) - set(built))
diff = sorted(n for n in set(built) & set(live) if built[n] != live[n])
print("members_built=%d members_live=%d only_in_built=%s only_in_live=%s differing=%s" % (len(built), len(live), only_b, only_l, diff))

changed = []
unintended = []
for n in diff:
    row = rows.get(n)
    if row is None:
        unintended.append(n)
        changed.append({"name": n, "repo_path": None, "built_member_sha256": sha(built[n]),
                        "repo_blob_sha256_at_pin": None, "live_member_sha256": sha(live[n])})
        continue
    blob = git_blob(row["repo_path"])
    changed.append({"name": n, "repo_path": row["repo_path"], "built_member_sha256": sha(built[n]),
                    "repo_blob_sha256_at_pin": sha(blob), "live_member_sha256": sha(live[n])})

# every staged row: built member equals the repo blob at the pin (the positive control for the whole set)
staged_equal = 0
staged_total = 0
for packaged, row in rows.items():
    if packaged not in built:
        continue
    staged_total += 1
    if sha(git_blob(row["repo_path"], row["pin"])) == sha(built[packaged]):
        staged_equal += 1
print("staged rows: built member == repo blob at pin for %d of %d" % (staged_equal, staged_total))

sig_b = instrument(BUILT)
sig_l = instrument(LIVE)
print("built instrument: " + sig_b[0])
print("live instrument: " + sig_l[0])

real_after = sha(open(REAL, "rb").read())
print("real_source_map_sha256 before=%s after=%s" % (REAL_BEFORE, real_after))

rec = {
    "to_id": "IRPT_BCKEND.TO-IB-pr-498",
    "base_commit": PIN,
    "pin_commit": PIN,
    "uploaded": False,
    "build_command": "BUILD_ONLY=1 TMPDIR=<scratch> BAU_SOURCE_MAP_OVERRIDE=<candidate_source_map_498.json> bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-holdings",
    "candidate_map": "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~348/candidate_source_map_498.json",
    "candidate_map_change": "irpt-holdings staged_from row docs/contracts/investor-reporting/v1/HoldingsSnapshot.schema.json only: pin 4cc72587d6 -> f91aedd1ef, sha256 fde5dd4171 -> 5d9e7fe165 (two lines changed, nothing else)",
    "real_source_map_sha256_before": REAL_BEFORE,
    "real_source_map_sha256_after": real_after,
    "functions": [{
        "function": FN,
        "built_sha256": b_sha,
        "built_codesha256_b64": base64.b64encode(hashlib.sha256(built_bytes).digest()).decode("ascii"),
        "built_bytes": len(built_bytes),
        "live_sha256": l_sha,
        "live_codesha256_b64": base64.b64encode(hashlib.sha256(live_bytes).digest()).decode("ascii"),
        "live_bytes": len(live_bytes),
        "sha256_form": "built_sha256 and live_sha256 are the zip's SHA-256 in hex",
        "built_twice_identical": b_sha == b2_sha,
        "second_build_sha256": b2_sha,
        "built_signature_mismatched": sig_b[1],
        "built_attribute_mismatched": sig_b[2],
        "built_instrument_last_line": sig_b[0],
        "built_instrument_rc": sig_b[3],
        "live_instrument_last_line": sig_l[0],
        "live_instrument_rc": sig_l[3],
        "live_signature_mismatched": sig_l[1],
        "live_attribute_mismatched": sig_l[2],
        "instrument": "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~278/signature_closure_attr.py",
        "members_built": len(built),
        "members_live": len(live),
        "members_only_in_built": only_b,
        "members_only_in_live": only_l,
        "changed_members": changed,
        "unintended_changed_members": unintended,
        "staged_rows_built_equal_pin_blob": "%d of %d" % (staged_equal, staged_total),
    }],
}
with open(D + "IB171-3_release_census.json", "w", encoding="utf-8", newline="\n") as f:
    json.dump(rec, f, indent=1)
    f.write("\n")
print("wrote IB171-3_release_census.json; changed=%d unintended=%d" % (len(changed), len(unintended)))
