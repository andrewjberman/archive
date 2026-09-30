"""HVST-aa-2 BEFORE (issuer, read-only). `--signing` writes the signing snapshot the halves cite; without it, writes the
act-start snapshot (`~77/aa2_before.json`) and STOPs if any root differs from signing or the outbox holds a pending row."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aa2_common as p  # noqa: E402


def main():
    snap = p.snapshot()
    pend = p.outbox_pending()
    print("objects per root: %s" % {k: len(v) for k, v in snap.items()})
    print("outbox pending: %s" % pend)
    if "--signing" in sys.argv:
        p.c.dump(p.SIGNING, {"snapshot": snap, "outbox_pending": pend})
        print("wrote " + p.SIGNING)
        return 0
    s = p.c.load(p.SIGNING)
    p.c.dump(os.path.join(p.WK, "aa2_before.json"), {"snapshot": snap, "outbox_pending": pend})
    drift = {k: tuple(len(x) for x in v) for k, v in p.diff(s["snapshot"], snap).items() if any(v)}
    if drift or any(pend.values()):
        print("BEFORE DIFFERS (moved, removed, new) %s or outbox pending %s -> STOP" % (drift, pend))
        return 1
    print("BEFORE == signing snapshot on every root, outbox empty: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
