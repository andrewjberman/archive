"""HVST-p-3(a) signing measurement (issuer, read-only): the expected write of `build-daily --as-of 2026-09-30`, produced
by the producer's own `build_daily` against a put-capturing pass-through client. `--signing` writes
round26/p3_signing_expected.json; without it, re-measures and writes the act-start BEFORE (`~68/p3_before.json`), STOP on drift.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p3_common as p  # noqa: E402


def measure():
    summary, rows = p.dry_build()
    ch = p.changes(rows, p.served())
    return {
        "as_of": str(p.AS_OF), "parts": p.list_parts(), "summary": {k: v for k, v in summary.items() if k != "key"},
        "digest": p.digest(p.canon(rows)), **ch,
    }


def main():
    m = measure()
    print("chatter_daily parts: %d; served rows %d; dry build (1 put) rows %d; digest %s"
          % (len(m["parts"]), m["rows_served"], m["rows"], m["digest"][:16]))
    print("dry build summary: %s" % m["summary"])
    print("NEW keys %d, GONE %d; MOVED rows %d over %d securities" % (len(m["new_keys"]), len(m["gone_keys"]), m["moved"], len(m["moved_securities"])))
    print("data_status changed %d: %s; articles_total changed %d" % (len(m["status_changed"]), m["status_transitions"], len(m["articles_total_changed"])))
    print("Lenovo data_status after: %s" % m["lenovo_status"])
    if "--signing" in sys.argv:
        p.c.dump(p.SIGNING, m)
        print("wrote " + p.SIGNING)
        return 0
    s = p.c.load(p.SIGNING)
    drift = [k for k in ("parts", "digest") if s[k] != m[k]]
    p.c.dump(os.path.join(p.WK, "p3_before.json"), m)
    if drift:
        print("BEFORE DIFFERS FROM SIGNING on %s -> STOP" % drift)
        return 1
    print("BEFORE == signing (daily parts, expected-rows digest): OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
