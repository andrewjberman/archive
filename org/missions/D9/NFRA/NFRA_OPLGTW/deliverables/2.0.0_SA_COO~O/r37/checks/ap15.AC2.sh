#!/usr/bin/env bash
# OPLGTW OG-ap-15 AC2 (Phase B, per family): every one of the five families is TERMINAL one of two ways:
#  - RELEASED: its ledger nfra-oplgtw-fd2-<family>-drain is CLOSED at HEAD with no sentinel; W/AP15_GRADE.json records the
#    live CodeSha256 equal to the built package_sha256, a SCHEDULED sweep after the deploy, and that sweep's
#    backfill-status carrying the dlq_drain key; or
#  - REFUSED: a half refused it, and the refusal file it cites exists at HEAD.
# At least one family released (a round that refuses all five has shipped nothing and is not this order's PASS).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z"
[ -f "$W/AP15_GRADE.json" ] || { echo "AP15_GRADE.json absent"; echo "RESULT: FAIL"; exit 1; }
python - "$(native "$W/AP15_GRADE.json")" "$(native "$W/ap15_build.json")" <<'EOF'
import json, subprocess, sys
WANT = {"schwab", "etf", "orion", "eclipse", "blackdiamond"}
def git(*a):
    r = subprocess.run(["git", *a], capture_output=True)
    return r.returncode, r.stdout.decode("utf-8", "replace").replace("\r", "")
grade = {f.get("family"): f for f in json.load(open(sys.argv[1], encoding="utf-8")).get("families", [])}
try: built = {f.get("family"): f for f in json.load(open(sys.argv[2], encoding="utf-8")).get("families", [])}
except Exception: built = {}
cm = git("ls-tree", "-r", "--name-only", "HEAD", "org/critical_paths/change_management/")[1].split("\n")
rel, ref, bad = 0, 0, []
for fam in sorted(WANT):
    g = grade.get(fam)
    if not g: bad.append(fam + ": absent from the grade"); continue
    if g.get("released") is True:
        slug = "nfra-oplgtw-fd2-%s-drain" % fam
        es = [p for p in cm if p.endswith("_%s_deploy_completion.md" % slug)]
        closed = bool(es) and "**Status:** CLOSED" in git("show", "HEAD:" + es[-1])[1]
        sent = git("ls-tree", "--name-only", "HEAD", "org/critical_paths/.open_deploys/%s.json" % slug)[1].strip()
        sha_ok = bool(g.get("live_code_sha256")) and g.get("live_code_sha256") == built.get(fam, {}).get("package_sha256")
        ok = closed and not sent and sha_ok and g.get("sweep_was_scheduled") is True and g.get("dlq_drain_present") is True
        if ok: rel += 1
        else: bad.append("%s: closed=%s sentinel=%s sha=%s scheduled=%s dlq_drain=%s" % (fam, closed, bool(sent), sha_ok, g.get("sweep_was_scheduled"), g.get("dlq_drain_present")))
    elif g.get("released") is False:
        r = str(g.get("refusal_ref", "")).split("@")[0]
        if r and git("cat-file", "-e", "HEAD:" + r)[0] == 0: ref += 1
        else: bad.append(fam + ": refused without a refusal file at HEAD")
    else: bad.append(fam + ": released is neither true nor false")
print("families released and graded %d; refused with a file %d; of 5; defects %d (want 0)" % (rel, ref, len(bad)))
for b in bad: print("  " + b)
ok = rel + ref == 5 and rel >= 1 and not bad
print("RESULT: " + ("PASS" if ok else "FAIL")); sys.exit(0 if ok else 1)
EOF
