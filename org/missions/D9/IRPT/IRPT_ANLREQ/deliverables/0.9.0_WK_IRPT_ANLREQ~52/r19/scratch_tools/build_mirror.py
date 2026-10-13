"""Build the repo-layout mirror of the pinned Lambda package and the HEAD comparison files (read-only git show).

Usage: python build_mirror.py <scratch_root> <worktree_root>
  mirror/<repo_path>        every staged_from member at its map pin (88), so the test world's ROOT-relative paths resolve
  mirror/<test paths>       test files: test_uploads.py and test_template_uploads.py (HEAD; byte-identical to the pins),
                            test_template_reader.py (pin 3f29017cfc, the reader's own test), reports/tests/test_repository.py (HEAD)
  head/uploads_HEAD.py      HEAD uploads.py (the planned-move half 1)
  head/template_reader_HEAD.py  HEAD template_reader.py (the planned-move half 2, READER_VERSION r18.1)
Writes tools/mirror_manifest.json with sha256 of every file written and the door-closure pin-versus-HEAD comparison.
"""
import hashlib
import json
import os
import subprocess
import sys

SCR, WT = sys.argv[1], sys.argv[2]
MIRROR = os.path.join(SCR, "mirror")
HEAD_DIR = os.path.join(SCR, "head")
INTAKE = "infra/aws/lambda/investor-reporting/intake"
written = {}


def git_show(ref_path):
    got = subprocess.run(["git", "-C", WT, "show", ref_path], capture_output=True)
    if got.returncode != 0 or not got.stdout:
        raise SystemExit("git show failed %s rc=%s" % (ref_path, got.returncode))
    return got.stdout


def put(path, data, key):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(data)
    written[key] = {"path": os.path.relpath(path, SCR).replace("\\", "/"), "sha256": hashlib.sha256(data).hexdigest()}


man = json.load(open(os.path.join(SCR, "tools", "tree_manifest.json"), encoding="utf-8"))
for packaged, m in man["members"].items():
    put(os.path.join(MIRROR, m["repo_path"]), git_show(m["pin"] + ":" + m["repo_path"]), "pin:" + m["repo_path"])

put(os.path.join(MIRROR, INTAKE, "tests", "test_uploads.py"), git_show("HEAD:" + INTAKE + "/tests/test_uploads.py"), "HEAD:test_uploads.py")
put(os.path.join(MIRROR, INTAKE, "tests", "test_template_uploads.py"),
    git_show("HEAD:" + INTAKE + "/tests/test_template_uploads.py"), "HEAD:test_template_uploads.py")
put(os.path.join(MIRROR, INTAKE, "tests", "test_template_reader.py"),
    git_show("3f29017cfcd28c6be36841c61f1b9b313c1f8d29:" + INTAKE + "/tests/test_template_reader.py"), "pin:test_template_reader.py")
put(os.path.join(MIRROR, "infra/aws/lambda/investor-reporting/reports/tests/test_repository.py"),
    git_show("HEAD:infra/aws/lambda/investor-reporting/reports/tests/test_repository.py"), "HEAD:test_repository.py")
put(os.path.join(HEAD_DIR, "uploads_HEAD.py"), git_show("HEAD:" + INTAKE + "/uploads.py"), "HEAD:uploads.py")
put(os.path.join(HEAD_DIR, "template_reader_HEAD.py"), git_show("HEAD:" + INTAKE + "/template_reader.py"), "HEAD:template_reader.py")

# Door closure: which members differ between the pin and HEAD (the planned move touches only the first two).
differ = {}
for packaged in man["door_closure"]:
    m = man["members"][packaged]
    head_bytes = subprocess.run(["git", "-C", WT, "show", "HEAD:" + m["repo_path"]], capture_output=True).stdout
    head_sha = hashlib.sha256(head_bytes).hexdigest() if head_bytes else None
    differ[packaged] = {"pin": m["pin"][:10], "pin_sha256": m["sha256"][:12], "head_sha256": (head_sha or "ABSENT")[:12],
                        "same_as_head": head_sha == m["sha256"]}
out = {"written": written, "door_closure_pin_vs_head": differ,
       "door_members_differing_from_head": sorted(k for k, v in differ.items() if not v["same_as_head"])}
open(os.path.join(SCR, "tools", "mirror_manifest.json"), "w", encoding="utf-8").write(json.dumps(out, indent=1, sort_keys=True))
print("written %d files" % len(written))
print("door members differing from HEAD: %s" % out["door_members_differing_from_head"])
