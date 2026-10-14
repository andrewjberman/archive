#!/usr/bin/env bash
# OPLGTW OG-ap-17 AC1 (OG-bd-3's release, CTO ruling msg 33941, Phase A): the release in W/ap17_release.json sits on the
# LIVE ref and carries ONLY OG-bd-3's gateway hunks:
#  - live: base == EC2_MANIFEST deployed_commit at HEAD, or (after B2) deployed_commit == release and
#    previous_deployed_commit == base;
#  - every file differing base -> release is a gateway file one of the cells' commits touched;
#  - every added and every removed line of that diff is an added / removed line of one of the cells' commits
#    (a line from any other unreleased cell is a line outside: want 0);
#  - OG-bd-3's markers are in the release tree (its decide() branch, its test file): 2 of 2.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
REC="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/ap17_release.json"
[ -f "$REC" ] || { echo "ap17_release.json absent"; echo "RESULT: FAIL"; exit 1; }
python - "$(native "$REC")" <<'EOF'
import json, subprocess, sys
G = "infra/aws/ec2/opal-gateway/"
CELLS = ["fffac3b499", "486b643b97"]
def git(*a):
    r = subprocess.run(["git", *a], capture_output=True)
    return r.returncode, r.stdout.decode("utf-8", "replace").replace("\r", "")
rec = json.load(open(sys.argv[1], encoding="utf-8"))
base, rel = rec.get("base_sha", ""), rec.get("release_sha", "")
if git("cat-file", "-e", rel + "^{commit}")[0] or git("cat-file", "-e", base + "^{commit}")[0]:
    print("base or release is not a commit here"); print("RESULT: FAIL"); sys.exit(1)
svc = json.loads(git("show", "HEAD:infra/aws/ec2/EC2_MANIFEST.json")[1])["services"]["opal-gateway"]
dep, prev = svc.get("deployed_commit", ""), svc.get("previous_deployed_commit", "")
live = dep == base or (dep == rel and prev == base)
allow, plus, minus = set(), {}, {}
for c in CELLS:
    for f in git("diff", "--name-only", c + "~1", c, "--", G)[1].split():
        allow.add(f)
    cur = None
    for ln in git("diff", "-U0", c + "~1", c, "--", G)[1].split("\n"):
        if ln.startswith("+++ "): cur = ln[6:]; continue
        if ln.startswith("--- "): continue
        if cur and ln.startswith("+"): plus.setdefault(cur, set()).add(ln[1:].strip())
        if cur and ln.startswith("-"): minus.setdefault(cur, set()).add(ln[1:].strip())
files = [f for f in git("diff", "--name-only", base, rel)[1].split() if f]
outside_files = [f for f in files if f not in allow]
outside_lines, cur = 0, None
for ln in git("diff", "-U0", base, rel, "--", G)[1].split("\n"):
    if ln.startswith("+++ "): cur = ln[6:]; continue
    if ln.startswith("--- "): continue
    s = ln[1:].strip()
    if not cur or not s: continue
    if ln.startswith("+") and s not in plus.get(cur, set()): outside_lines += 1
    if ln.startswith("-") and s not in minus.get(cur, set()): outside_lines += 1
def has(path, tok):
    rc, out = git("show", rel + ":" + G + path)
    return rc == 0 and (tok is None or tok in out)
markers = [has("app/data_entitlement.py", "OG-bd-3"), has("tests/test_og_bd3.py", None)]
print("base %s is the live ref: %s; release %s" % (base[:10], "yes" if live else "no", rel[:10]))
print("files differing %d; outside OG-bd-3's files %d (want 0)" % (len(files), len(outside_files)))
for f in outside_files[:10]: print("  outside: " + f)
print("diff lines outside OG-bd-3's hunks %d (want 0); cell markers present %d of 2" % (outside_lines, sum(markers)))
ok = live and not outside_files and outside_lines == 0 and all(markers)
print("RESULT: " + ("PASS" if ok else "FAIL")); sys.exit(0 if ok else 1)
EOF
