"""Round 44 (IRPT_BCKEND ~P, row S299, CTO batch 234 item 2) -- three AE roles read the Kimi API key through a wildcard ARN;
each narrows `astn/kimi/api-key-*` to `astn/kimi/api-key-??????` (Secrets Manager's six-character suffix), the shape
irpt-ycharts already uses.

Usage: python <this file> <repo_root> <criterion_id>
  IB44-1-AC1  in each of the three files, every `astn/kimi/api-key` ARN reads `astn/kimi/api-key-??????`, and none
              reads `astn/kimi/api-key-*`. Base: FAIL (three wildcards).
  IB44-1-AC2  a GUARD: against base 80ba60328c, the three files keep their line counts, and the only changed lines
              are the ones carrying `astn/kimi/api-key`, each changed only by `-*` -> `-??????`. Base: PASS (no change).
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import subprocess
import sys
from pathlib import Path

FILES = [
    "infra/aws/terraform/estate-report/iam.tf",
    "infra/aws/terraform/cot-pipeline/iam.tf",
    "infra/aws/terraform/bd-49f-auto-login/iam.tf",
]
TOKEN = "astn/kimi/api-key"
WILD = "astn/kimi/api-key-*"
NARROW = "astn/kimi/api-key-??????"
BASE = "80ba60328c"


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB44-1"))
        sys.exit(1)

    if cid == "IB44-1-AC1":
        for f in FILES:
            lines = [ln for ln in (root / f).read_bytes().decode("utf-8").splitlines() if TOKEN in ln]
            if not lines:
                fail("%s carries no %s line" % (f, TOKEN))
            for ln in lines:
                if WILD in ln:
                    fail("%s still reads the wildcard: %s" % (f, ln.strip()[:120]))
                if NARROW not in ln:
                    fail("%s line does not read %s: %s" % (f, NARROW, ln.strip()[:120]))
        print("OK: %d files, every %s ARN reads %s" % (len(FILES), TOKEN, NARROW))
    elif cid == "IB44-1-AC2":
        changed = 0
        for f in FILES:
            r = subprocess.run(["git", "show", "%s:%s" % (BASE, f)], cwd=str(root), capture_output=True)
            base = r.stdout.decode("utf-8").splitlines()
            if not base:
                fail("cannot read %s at %s (rc=%d)" % (f, BASE, r.returncode))
            now = (root / f).read_bytes().decode("utf-8").splitlines()
            if len(now) != len(base):
                fail("%s line count %d -> %d" % (f, len(base), len(now)))
            for i, (a, b) in enumerate(zip(base, now)):
                if a == b:
                    continue
                if TOKEN not in a or a.replace(WILD, NARROW) != b:
                    fail("%s:%d changed beyond -* -> -??????: %r" % (f, i + 1, b.strip()[:120]))
                changed += 1
        print("OK: only %s lines changed (%d), each -* -> -??????" % (TOKEN, changed))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
