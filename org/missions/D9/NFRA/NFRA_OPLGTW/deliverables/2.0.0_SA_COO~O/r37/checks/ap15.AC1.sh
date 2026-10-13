#!/usr/bin/env bash
# OPLGTW OG-ap-15 AC1 (round-37 R2, Phase A): the five per-family drain packages are BUILT, off trunk, and asked:
#  - W/ap15_build.json names exactly {schwab, etf, orion, eclipse, blackdiamond};
#  - each family's build_commit exists and, AT that commit, every BUILD_MANIFEST vendored module is byte-equal between the
#    package dir and its source (the package is the source, nothing hand-edited);
#  - each family carries package_sha256, prior_code_sha256 and drift_lines (int);
#  - the ask W/NEVER_WIDEN_ASK_OG-ap-15.md exists and names every family.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z"
[ -f "$W/ap15_build.json" ] || { echo "ap15_build.json absent"; echo "RESULT: FAIL"; exit 1; }
python - "$(native "$W/ap15_build.json")" "$(native "$W/NEVER_WIDEN_ASK_OG-ap-15.md")" <<'EOF'
import json, os, subprocess, sys
WANT = {"schwab", "etf", "orion", "eclipse", "blackdiamond"}
def git(*a):
    r = subprocess.run(["git", *a], capture_output=True)
    return r.returncode, r.stdout.decode("utf-8", "replace").strip()
fams = json.load(open(sys.argv[1], encoding="utf-8")).get("families", [])
names = {f.get("family") for f in fams}
ok_n, bad = 0, []
for f in fams:
    fam, c = f.get("family"), f.get("build_commit", "")
    pkg = "infra/aws/lambda/opal-assets/opal-assets-silver-%s/" % fam
    if git("cat-file", "-e", c + "^{commit}")[0]:
        bad.append(fam + ": build_commit not a commit"); continue
    rc, man = git("show", c + ":" + pkg + "BUILD_MANIFEST.json")
    try: mods = json.loads(man)["vendored_modules"]
    except Exception: bad.append(fam + ": manifest unreadable at build_commit"); continue
    eq = 0
    for m in mods:
        a = git("rev-parse", c + ":" + m)[1]; b = git("rev-parse", c + ":" + pkg + os.path.basename(m))[1]
        eq += int(bool(a) and a == b)
    fields = all(f.get(k) for k in ("package_sha256", "prior_code_sha256")) and isinstance(f.get("drift_lines"), int)
    if eq == len(mods) and fields: ok_n += 1
    else: bad.append("%s: vendored %d of %d byte-equal; fields %s" % (fam, eq, len(mods), "yes" if fields else "no"))
ask = sys.argv[2]
ask_ok = os.path.isfile(ask) and all(n in open(ask, encoding="utf-8").read() for n in WANT)
print("families named %d; expected set equal: %s" % (len(names), "yes" if names == WANT else "no"))
print("families built from source with fields: %d of 5; ask names all five: %s" % (ok_n, "yes" if ask_ok else "no"))
for b in bad: print("  " + b)
ok = names == WANT and ok_n == 5 and ask_ok
print("RESULT: " + ("PASS" if ok else "FAIL")); sys.exit(0 if ok else 1)
EOF
