"""HVST-ac-3 signing measurement + act-start gate (issuer, read-only).

The expected write of `build-daily`, from the producer's own `build_daily` through the real `write_gold` against a capturing
client. `--signing` writes round30/ac3_signing_expected.json. Without it, it re-measures and prints `ACT-START GATE: OK` only
when the parts, the row digest and the bytes all equal signing; otherwise `ACT-START GATE: STOP`.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ac3_common as c  # noqa: E402


def measure():
    summary, key, rows, nbytes = c.dry_build()
    served = c.served()
    d = c.field_diffs(rows, served)
    in_day, rolling_later, other = c.classify(d["moved"])
    return {
        "parts": c.list_parts(),
        "served_rows": len(served),
        "rows": len(rows),
        "digest": c.digest(c.canon(rows)),
        "bytes": nbytes,
        "key_shape": key.rsplit("/", 2)[0],
        "summary": {k: v for k, v in summary.items() if k != "key"},
        "new_keys": d["new_keys"], "gone_keys": d["gone_keys"],
        "moved": d["moved"], "in_window": in_day, "rolling_later": rolling_later, "other": other,
    }


def main():
    m = measure()
    print("chatter_daily parts: %d; served rows %d" % (len(m["parts"]), m["served_rows"]))
    print("dry build: %s" % {k: v for k, v in m["summary"].items() if k in ("rows", "run_records_read", "securities")})
    print("SERIALIZE (the real write_gold, put-captured): 1 put, %d rows, %d bytes, digest %s"
          % (m["rows"], m["bytes"], m["digest"][:16]))
    print("keys new %d, gone %d; moved (row, field) %d: on expected rows %d, rolling fields on later days of expected securities %d, OTHER %d"
          % (len(m["new_keys"]), len(m["gone_keys"]), len(m["moved"]), len(m["in_window"]), len(m["rolling_later"]),
             len(m["other"])))
    for x in m["in_window"]:
        print("  IN-WINDOW " + x)
    for x in m["other"][:30]:
        print("  OTHER     " + x)
    if "--signing" in sys.argv:
        c.dump(c.SIGNING, m)
        print("wrote " + c.SIGNING)
        return 0
    s = c.load(c.SIGNING)
    drift = [k for k in ("parts", "digest", "bytes") if s[k] != m[k]]
    c.dump(os.path.join(c.WK, "ac3_before.json"), m)
    if drift:
        print("BEFORE DIFFERS FROM SIGNING on %s" % drift)
        print("ACT-START GATE: STOP")
        return 1
    print("ACT-START GATE: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
