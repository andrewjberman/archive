"""IRPT_BCKEND round 102 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of four orders (CTO halves @a946f8b829 and @7f294053f0, msg 2765):
  IB102-1  IB-pr-397  apply the NEW irpt-commentary-composition-read-lambda (IB-pr-391) on 0.7.0_AE_CloudOps~IB2
  IB102-2  IB-pr-398  apply irpt-holdings ONLY (IB-pr-394) on ~IB2; irpt-narrative untouched
  IB102-3  IB-pr-399  irpt-narrative: TypeError fixed while a no-row internal caller stays bound to opal-capital (worker ~264)
  IB102-4  IB-pr-400  FWD-14 release packet: the runner bundle carrying the holdings publish gate (worker ~265)

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IB102-1-AC1  live CodeSha256 of irpt-commentary-composition-read-lambda == ZZmWOFSA...; after-reads A1: ledger CLOSED stating pin, sha256 and
               version_id; replay_rerun_before_ledger 8 arms all identical/expected-diff; after_read_invoke {status, counts} with no
               composition content. Base: FAIL (function absent).
  IB102-2-AC1  live irpt-holdings == CKpZUMD5...; live irpt-narrative unchanged (es/S9azussVLY2DfTj6hRjV1pqhZ8EaVCnaVcELqhPc=); after-reads
               A2: ledger CLOSED stating pin + sha256; replay arms re-run. Base: FAIL.
  IB102-3-AC1  narrative tests: `-k opal_capital_binding` >= 2 pass AND `-k served_error_path` >= 2 pass AND the narrative suite passes.
               Base: FAIL (no binding tests).
  IB102-3-AC2  census C3 + packet P3 (worker ~264): narrative built sha + live_before, BUILD_ONLY rc 0 clean; the replay R3 has an arm
               `no_row_internal_selects_other_firm` with verdict identical. Base: FAIL.
  IB102-4-AC1  census C4 + packet P4 (worker ~265): the runner bundle built sha256 + live_before; BUILD_ONLY rc 0 clean; packet names
               Branch A/B and the QA trace; replay R4 arms identical/expected-diff with a negative control. Base: FAIL.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/"
A1 = D + "0.7.0_AE_CloudOps~IB2/IB102-1_reader_release_after_reads.json"
A2 = D + "0.7.0_AE_CloudOps~IB2/IB102-2_holdings_release_after_reads.json"
W3, W4 = D + "0.9.0_WK_IRPT_BCKEND~264/", D + "0.9.0_WK_IRPT_BCKEND~265/"
NARR = "infra/aws/lambda/investor-reporting/narrative"


def live(root, fn):
    p = subprocess.run(["bash", str(root / ".tools" / "aws"), "lambda", "get-function-configuration", "--function-name", fn,
                        "--query", "CodeSha256", "--output", "text"], capture_output=True, timeout=120)
    return p.stdout.decode("utf-8", "replace").strip() if p.returncode == 0 else ""


def pyt(cwd, *args):
    p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *args], cwd=str(cwd), capture_output=True, timeout=280)
    out = re.sub(r"\x1b\[[0-9;]*m", "", (p.stdout + p.stderr).decode("utf-8", "replace")).strip().splitlines()
    last = out[-1] if out else ""
    m = re.search(r"\b(\d+) passed", last)
    return p.returncode, (int(m.group(1)) if m else 0), last


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB102"))
        sys.exit(1)

    def load(rel):
        f = root / rel
        if not f.is_file():
            fail("no %s" % rel)
        return json.loads(f.read_text(encoding="utf-8"))

    def arms_ok(arms, n=1):
        return len(arms) >= n and all(x.get("verdict") in ("identical", "expected-diff") for x in arms)

    if cid == "IB102-1-AC1":
        if live(root, "irpt-commentary-composition-read-lambda") != "ZZmWOFSA/GjO0d/cKHSm9G5+xDc5sNfEHOpbmfIabQ0=":
            fail("reader live != built")
        a = load(A1)
        led = a.get("ledger") or {}
        if led.get("state") != "CLOSED" or not all(led.get(k) for k in ("pin", "sha256", "version_id")):
            fail("ledger %r" % led)
        if not arms_ok(a.get("replay_rerun_before_ledger") or [], 8):
            fail("replay arms")
        inv = a.get("after_read_invoke") or {}
        if not inv.get("status") or "composition" in inv:
            fail("after_read_invoke %r" % inv)
        print("OK: reader live == built; ledger CLOSED; 8 arms; invoke %s" % inv.get("status"))
    elif cid == "IB102-2-AC1":
        if live(root, "irpt-holdings") != "CKpZUMD5RVWyY/2oyo8zZwN7Ss8J2FbkeNFr2XYbXD8=":
            fail("holdings live != built")
        if live(root, "irpt-narrative") != "es/S9azussVLY2DfTj6hRjV1pqhZ8EaVCnaVcELqhPc=":
            fail("narrative moved")
        a = load(A2)
        led = a.get("ledger") or {}
        if led.get("state") != "CLOSED" or not led.get("pin") or not led.get("sha256") or not arms_ok(a.get("replay_rerun_before_ledger") or []):
            fail("ledger/replay %r" % led)
        print("OK: holdings live == built; narrative unchanged; ledger CLOSED")
    elif cid == "IB102-3-AC1":
        for sel, n in (("opal_capital_binding", 2), ("served_error_path", 2)):
            rc, k, last = pyt(root / NARR, "tests", "-k", sel)
            if rc != 0 or k < n:
                fail("-k %s rc %d: %s" % (sel, rc, last))
        rc, k, last = pyt(root / NARR, "tests")
        if rc != 0:
            fail("narrative suite rc %d: %s" % (rc, last))
        print("OK: binding + error-path tests; suite %s" % last)
    elif cid in ("IB102-3-AC2", "IB102-4-AC1"):
        w = W3 if cid.startswith("IB102-3") else W4
        k = "3" if w == W3 else "4"
        c = load(w + "IB102-%s_release_census.json" % k)
        bo = c.get("build_only") or {}
        arts = c.get("artifacts") or []
        if bo.get("rc") != 0 or bo.get("tree_clean") is not True or not arts:
            fail("census %r" % bo)
        r = load(w + "IB102-%s_release_replay.json" % k)
        arms = r.get("arms") or []
        if not arms_ok(arms) or not any(x.get("negative_control") for x in arms):
            fail("replay arms")
        if k == "3" and not any(x.get("name") == "no_row_internal_selects_other_firm" and x.get("verdict") == "identical" for x in arms):
            fail("no identical no_row_internal_selects_other_firm arm")
        pp = root / (w + "NEVER_WIDEN_SIGNOFF_PACKET_%s.md" % ("IB-pr-399" if k == "3" else "IB-pr-400"))
        if not pp.is_file():
            fail("no packet")
        pk = pp.read_text(encoding="utf-8")
        for s in ["Branch A", "Branch B", str(c.get("pin", ""))] + [str(a.get("built_sha256", "")) for a in arts]:
            if not s or s not in pk:
                fail("packet lacks %r" % s)
        print("OK: census + %d arm(s) + packet" % len(arms))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
