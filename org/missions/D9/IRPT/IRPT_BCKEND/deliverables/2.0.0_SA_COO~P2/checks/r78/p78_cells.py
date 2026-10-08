"""IRPT_BCKEND round 78 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of cell IB-pr-365 (E4 of the CTO's round analysis
ADDENDUM 1 @e4ad79e976: bound comp-tagauthz's IAM read so the safe-apply gate evaluates a default_tags tree; row S334).

Usage: python <this file> <repo_root> <criterion_id>
Prints "<id> PASS" or "<id> FAIL" as the last line.

  IB78-1-AC1  the gate, run as safe-apply runs it (check --default-tags-tree <tree> scoped by one candidate) on the real
              default_tags tree infra/aws/terraform/investor-reporting/export, returns a verdict (rc 0 or 2) within 240 s; the
              elapsed seconds are printed. Base on dell2 0c9d22dbd1+: PASS (rc 0 in 61.4 s; 26.2 s on a second run) -- the
              read returns on dell2; the laptop hang is S334's. This is the no-regression arm under the new bound; IB78-1-AC2
              is the discriminating arm.
  IB78-1-AC2  with COMP_TAGAUTHZ_IAM_TIMEOUT=1 the same run fails CLOSED: rc 1 and the output names the reason token
              TAGAUTHZ_IAM_READ_TIMEOUT. Base: FAIL (no bound, no token).
  IB78-1-AC3  the investigation channel holds a row whose dismissal_reason starts "Resolves IRPT_BCKEND-S334" and names a
              commit (10+ hex) that exists and changes .tools/comp-tagauthz.py. Base: FAIL (no such row).
"""
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

TREE = "infra/aws/terraform/investor-reporting/export"
CAND = "i-00000000000000000"
CHANNEL = "org/missions/D9/IRPT/IRPT_BCKEND/surprise-channel/investigations/INVESTIGATION_v1.md"
TOKEN = "TAGAUTHZ_IAM_READ_TIMEOUT"


def run_gate(root, env_extra, outer):
    env = dict(os.environ, **env_extra)
    t0 = time.time()
    try:
        p = subprocess.run([sys.executable, str(root / ".tools" / "comp-tagauthz.py"), "check", "--default-tags-tree", TREE,
                            "--candidate", CAND], cwd=str(root), capture_output=True, timeout=outer, env=env)
    except subprocess.TimeoutExpired:
        return None, "", time.time() - t0
    out = (p.stdout + p.stderr).decode("utf-8", "replace")
    return p.returncode, out, time.time() - t0


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB77-2"))
        sys.exit(1)

    if cid == "IB78-1-AC1":
        rc, out, el = run_gate(root, {}, 300)
        print("elapsed_s=%.1f rc=%s" % (el, rc))
        if rc is None:
            fail("no verdict within the 300 s outer bound")
        if rc not in (0, 2):
            fail("rc %s is not a verdict; tail: %s" % (rc, out.strip()[-300:]))
        if el > 240:
            fail("verdict took %.1f s > 240 s" % el)
        print("OK: verdict rc %d in %.1f s on %s" % (rc, el, TREE))
    elif cid == "IB78-1-AC2":
        rc, out, el = run_gate(root, {"COMP_TAGAUTHZ_IAM_TIMEOUT": "1"}, 120)
        print("elapsed_s=%.1f rc=%s" % (el, rc))
        if rc != 1:
            fail("forced bound did not fail closed with rc 1 (rc %s)" % rc)
        if TOKEN not in out:
            fail("output does not name %s; tail: %s" % (TOKEN, out.strip()[-300:]))
        print("OK: forced bound fails closed rc 1 naming %s" % TOKEN)
    elif cid == "IB78-1-AC3":
        text = (root / CHANNEL).read_text(encoding="utf-8")
        found = None
        for m in re.finditer(r"```json\n(\{.*?\})\n```", text, re.S):
            try:
                row = json.loads(m.group(1))
            except ValueError:
                continue
            if str(row.get("dismissal_reason", "")).startswith("Resolves IRPT_BCKEND-S334"):
                found = row
        if not found:
            fail("no row resolving IRPT_BCKEND-S334")
        for h in re.findall(r"\b[0-9a-f]{10,40}\b", found["dismissal_reason"]):
            r = subprocess.run(["git", "show", "--name-only", "--format=", h], cwd=str(root), capture_output=True)
            if r.returncode == 0 and ".tools/comp-tagauthz.py" in r.stdout.decode("utf-8", "replace"):
                print("OK: row %s resolves S334 citing %s (changes .tools/comp-tagauthz.py)" % (found.get("id"), h))
                break
        else:
            fail("row %s names no commit that changes .tools/comp-tagauthz.py" % found.get("id"))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
