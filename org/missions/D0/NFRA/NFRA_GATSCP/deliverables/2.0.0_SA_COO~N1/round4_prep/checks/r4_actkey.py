"""GS-h-2 AC1 (FWD-8; ROUND_ANALYSIS.round3 ADDENDUM 1): BLOCK and OVERRIDE lines carry one act key and the act's full path list,
and a commit writing outside its seat's paths is still stopped.

Drives the real hook `.tools/git-hooks/owned-paths-check.sh` with its test seam `OWNED_PATHS_AUDIT_LOG` pointed at a temp file (the
real audit log is never written; at the base, where the seam's key is absent, this check refuses to run the hook at all).
Act: GIT_AUTHOR_NAME=2.0.0_SA_COO~N1 stages two paths: one in its own deliverables folder, one outside its lanes
(`org/tier0/ledger/LD-0001.md`).
Arm 1 (the planted outside-paths commit is still stopped): rc 1, one BLOCK line with `act=<12 hex>` and `paths=2:` naming BOTH paths.
Arm 2: the same act under GIT_COMMIT_AUTHOR_OVERRIDE -> rc 0, one OVERRIDE line with the SAME act key and the same path list.
Arm 3 (the difference): the own path alone -> rc 0 and a DIFFERENT act key (the key is the act, not the author).
"""
import os
import re
import shutil
import sys
import tempfile

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "..", "round1_prep", "checks"))
from r1_common import ROOT, git_bash, run, tail  # noqa: E402

HOOK = os.path.join(ROOT, ".tools", "git-hooks", "owned-paths-check.sh")
OWN = "org/missions/D0/NFRA/NFRA_GATSCP/deliverables/2.0.0_SA_COO~N1/round4_prep/probe_actkey.md"
OUT = "org/tier0/ledger/LD-0001.md"
KEY = re.compile(r"\bact=([0-9a-f]{12})\b")

src = open(HOOK, encoding="utf-8").read()
arms = []
if "act=" not in src:
    arms = [("hook-writes-act-key", False, "owned-paths-check.sh has no act= field; the hook is not run against the real log")]
else:
    d = tempfile.mkdtemp(prefix="gatscp-r4-")
    try:
        def go(staged, override=""):
            log = os.path.join(d, "audit-%d.log" % len(os.listdir(d)))
            env = dict(os.environ, OWNED_PATHS_AUDIT_LOG=log, GIT_AUTHOR_NAME="2.0.0_SA_COO~N1",
                       OWNED_PATHS_STAGED_FILES="\n".join(staged), PRECOMP_REPO_ROOT=ROOT)
            env.pop("GIT_COMMIT_AUTHOR_OVERRIDE", None)
            if override:
                env["GIT_COMMIT_AUTHOR_OVERRIDE"] = override
            rc, out = run([git_bash(), HOOK], env)
            text = open(log, encoding="utf-8", errors="replace").read() if os.path.exists(log) else ""
            return rc, out, text

        rc1, o1, l1 = go([OWN, OUT])
        rc2, o2, l2 = go([OWN, OUT], "TIER0_MSTR")
        rc3, o3, l3 = go([OWN])
        k1, k2, k3 = KEY.search(l1), KEY.search(l2), KEY.search(l3)
        full1 = " BLOCK " in l1 and "paths=2:" in l1 and OWN in l1 and OUT in l1
        full2 = " OVERRIDE " in l2 and "paths=2:" in l2 and OWN in l2 and OUT in l2
        arms = [
            ("outside-paths-stopped-with-key-and-list", rc1 == 1 and bool(k1) and full1, "rc=%s :: %s" % (rc1, l1.strip()[-220:])),
            ("override-same-act-key", rc2 == 0 and bool(k1 and k2) and k1.group(1) == k2.group(1) and full2,
             "rc=%s keys=%s/%s" % (rc2, k1 and k1.group(1), k2 and k2.group(1))),
            ("own-path-act-differs", rc3 == 0 and bool(k1 and k3) and k3.group(1) != k1.group(1),
             "rc=%s key=%s :: %s" % (rc3, k3 and k3.group(1), tail(o3, 1))),
        ]
    finally:
        shutil.rmtree(d, ignore_errors=True)
for name, ok, detail in arms:
    print("  %s %s: %s" % ("PASS" if ok else "FAIL", name, detail))
bad = sum(1 for a in arms if not a[1])
print("GS-H2-ACTKEY ok=%s arms=%d failed=%d" % (bad == 0, len(arms), bad))
sys.exit(0 if bad == 0 else 1)
