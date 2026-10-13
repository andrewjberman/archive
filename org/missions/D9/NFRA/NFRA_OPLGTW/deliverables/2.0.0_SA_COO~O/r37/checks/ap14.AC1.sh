#!/usr/bin/env bash
# OPLGTW OG-ap-14 AC1 (round-37 R1, the r30 release re-cut, Phase B1): the release in W/ap14_release.json sits on the
# LIVE ref and carries ONLY the four cells' gateway hunks (CTO ruling @8f236865cc):
#  - live: base == EC2_MANIFEST deployed_commit at HEAD, or (after B2) deployed_commit == release and
#    previous_deployed_commit == base;
#  - every file differing base -> release is a gateway file one of the cells' commits touched;
#  - every added and every removed line of that diff is an added / removed line of one of the cells' commits
#    (a line from any other unreleased cell is a line outside: want 0);
#  - each cell's marker is in the release tree (pf-1 DATA_GRANT_TOOLS, tg-1 its gate test, bd-2 its test,
#    sh-1 list_shared_folder): 4 of 4.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
REC="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/ap14_release.json"
[ -f "$REC" ] || { echo "ap14_release.json absent"; echo "RESULT: FAIL"; exit 1; }
python - "$(native "$REC")" <<'EOF'
import json, subprocess, sys
G = "infra/aws/ec2/opal-gateway/"
CELLS = ["5c5549b8bd", "9abb699720", "b47fc56a98", "27e1969db3", "c37fdf95a5", "47cee985ee"]
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
markers = [has("app/data_entitlement.py", "DATA_GRANT_TOOLS"), has("tests/test_opal_users_gate.py", None),
           has("tests/test_og_bd2.py", None), has("app/tools.py", "list_shared_folder")]
print("base %s is the live ref: %s; release %s" % (base[:10], "yes" if live else "no", rel[:10]))
print("files differing %d; outside the four cells' files %d (want 0)" % (len(files), len(outside_files)))
for f in outside_files[:10]: print("  outside: " + f)
print("diff lines outside the four cells' hunks %d (want 0); cell markers present %d of 4" % (outside_lines, sum(markers)))
ok = live and not outside_files and outside_lines == 0 and all(markers)
print("RESULT: " + ("PASS" if ok else "FAIL")); sys.exit(0 if ok else 1)
EOF
