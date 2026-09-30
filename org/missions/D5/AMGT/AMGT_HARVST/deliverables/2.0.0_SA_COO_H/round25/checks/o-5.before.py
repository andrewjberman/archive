"""HVST-o-5 BEFORE snapshot (issuer check, read-only). `--signing` writes the signing snapshot the halves cite;
without it, writes the act-start snapshot to the worker's deliverables and compares it to the signing snapshot."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import o5_common as c  # noqa: E402


def main():
    snap = c.snapshot()
    print("objects per publisher harvest root: %s" % c.counts(snap))
    if "--signing" in sys.argv:
        c.dump(c.SIGNING_BEFORE, snap)
        print("wrote " + c.SIGNING_BEFORE)
        return 0
    c.dump(os.path.join(c.WK, "o5_before.json"), snap)
    signing = c.load(c.SIGNING_BEFORE)
    d = c.diff(signing, snap)
    drift = {p: (len(m), len(r), len(n)) for p, (m, r, n) in d.items() if m or r or n}
    if drift:
        print("BEFORE DIFFERS FROM THE SIGNING SNAPSHOT (moved, removed, new): %s -> STOP" % drift)
        return 1
    print("BEFORE == signing snapshot on every publisher: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
