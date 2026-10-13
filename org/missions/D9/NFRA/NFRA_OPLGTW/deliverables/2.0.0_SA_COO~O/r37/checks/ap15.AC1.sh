#!/usr/bin/env bash
# OPLGTW OG-ap-15 AC1 (round-37 R2, Phase A; amended A1): the five per-family drain packages are BUILT, off trunk, and asked:
#  - W/ap15_build.json names exactly {schwab, etf, orion, eclipse, blackdiamond}, each with a "route";
#  - route "full" (schwab, etf): AT build_commit every BUILD_MANIFEST vendored module is byte-equal between the package dir
#    and its source (the package is the source);
#  - route "drain-only" (blackdiamond, orion, eclipse; CTO ruling msg 33818, route (a)): AT build_commit every package
#    member except mirror_conversion.py has the SAME blob as at base_sha (the deployed copy, deployed_equals_base true),
#    and mirror_conversion.py differs from base_sha's copy ONLY by lines that OG-fd-1 (12a92ffa49) and OG-fd-2
#    (b2538131ea) added or removed in data/assets/scripts/silver/mirror_conversion.py, with at least one such line;
#  - each family carries package_sha256, prior_code_sha256 and drift_lines (int);
#  - the ask W/NEVER_WIDEN_ASK_OG-ap-15.md exists and names every family.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z"
[ -f "$W/ap15_build.json" ] || { echo "ap15_build.json absent"; echo "RESULT: FAIL"; exit 1; }
python - "$(native "$W/ap15_build.json")" "$(native "$W/NEVER_WIDEN_ASK_OG-ap-15.md")" <<'EOF'
import json, os, subprocess, sys
WANT = {"schwab", "etf", "orion", "eclipse", "blackdiamond"}
ROUTE = {"schwab": "full", "etf": "full", "orion": "drain-only", "eclipse": "drain-only", "blackdiamond": "drain-only"}
SRC = "data/assets/scripts/silver/mirror_conversion.py"
def git(*a):
    r = subprocess.run(["git", *a], capture_output=True)
    return r.returncode, r.stdout.decode("utf-8", "replace").replace("\r", "")
def lines(diff):
    p, m = set(), set()
    for ln in diff.split("\n"):
        if ln.startswith("+++") or ln.startswith("---"): continue
        if ln.startswith("+") and ln[1:].strip(): p.add(ln[1:].strip())
        if ln.startswith("-") and ln[1:].strip(): m.add(ln[1:].strip())
    return p, m
dp, dm = set(), set()
for c in ("12a92ffa49", "b2538131ea"):
    a, b = lines(git("diff", "-U0", c + "~1", c, "--", SRC)[1]); dp |= a; dm |= b
doc = json.load(open(sys.argv[1], encoding="utf-8"))
fams = doc.get("families", [])
names = {f.get("family") for f in fams}
ok_n, bad = 0, []
for f in fams:
    fam, c, base = f.get("family"), f.get("build_commit", ""), f.get("base_sha", doc.get("base_sha", ""))
    pkg = "infra/aws/lambda/opal-assets/opal-assets-silver-%s/" % fam
    fields = all(f.get(k) for k in ("package_sha256", "prior_code_sha256")) and isinstance(f.get("drift_lines"), int)
    if f.get("route") != ROUTE.get(fam):
        bad.append("%s: route %s, want %s" % (fam, f.get("route"), ROUTE.get(fam))); continue
    if git("cat-file", "-e", c + "^{commit}")[0]:
        bad.append(fam + ": build_commit not a commit"); continue
    if ROUTE[fam] == "full":
        rc, man = git("show", c + ":" + pkg + "BUILD_MANIFEST.json")
        try: mods = json.loads(man)["vendored_modules"]
        except Exception: bad.append(fam + ": manifest unreadable at build_commit"); continue
        eq = sum(1 for m in mods if git("rev-parse", c + ":" + m)[1].strip() and
                 git("rev-parse", c + ":" + m)[1].strip() == git("rev-parse", c + ":" + pkg + os.path.basename(m))[1].strip())
        good = eq == len(mods)
        if not good: bad.append("%s: vendored %d of %d byte-equal" % (fam, eq, len(mods)))
    else:
        if git("cat-file", "-e", base + "^{commit}")[0] or f.get("deployed_equals_base") is not True:
            bad.append(fam + ": base_sha missing or deployed_equals_base not true"); continue
        names_c = set(git("ls-tree", "--name-only", c, pkg)[1].split()); names_b = set(git("ls-tree", "--name-only", base, pkg)[1].split())
        same = [n for n in names_b | names_c if os.path.basename(n) != "mirror_conversion.py"
                and git("rev-parse", c + ":" + n)[1].strip() == git("rev-parse", base + ":" + n)[1].strip()]
        others = len((names_b | names_c) - {pkg + "mirror_conversion.py"})
        p, m = lines(git("diff", "-U0", base, c, "--", pkg + "mirror_conversion.py")[1])
        stray = len(p - dp) + len(m - dm)
        good = len(same) == others and stray == 0 and (p or m)
        if not good: bad.append("%s: other members unchanged %d of %d; mirror_conversion stray lines %d; drain lines %d" % (fam, len(same), others, stray, len(p) + len(m)))
    if good and fields: ok_n += 1
    elif good: bad.append(fam + ": fields missing")
ask = sys.argv[2]
ask_ok = os.path.isfile(ask) and all(n in open(ask, encoding="utf-8").read() for n in WANT)
print("families named %d; expected set equal: %s" % (len(names), "yes" if names == WANT else "no"))
print("families built per their route with fields: %d of 5; ask names all five: %s" % (ok_n, "yes" if ask_ok else "no"))
for b in bad: print("  " + b)
ok = names == WANT and ok_n == 5 and ask_ok
print("RESULT: " + ("PASS" if ok else "FAIL")); sys.exit(0 if ok else 1)
EOF
