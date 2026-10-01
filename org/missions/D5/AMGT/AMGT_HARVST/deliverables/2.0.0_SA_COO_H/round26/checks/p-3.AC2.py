"""HVST-p-3(a) AC2 (issuer check, read-only): the SERVED chatter_daily is the rebuilt one, with the signed changes.

PASS requires: the newest served snapshot's digest equals the signed digest; the changes against the pre-act served snapshot
are exactly the signed ones (the same data_status-changed keys, the same articles_total-changed keys, the same new keys, no
gone keys); and Lenovo's data_status distribution equals the signed one. The gold branch's all-names guard is not graded
here (CTO ruling section 3): RESOLVED stays 0 of 191 by its rule, printed for the record.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p3_common as p  # noqa: E402


def main():
    failures = []
    before = p.c.load(os.path.join(p.WK, "p3_before.json"))
    rows = p.served()
    d = p.digest(p.canon(rows))
    print("served chatter_daily rows %d, digest %s (signed %s)" % (len(rows), d[:16], before["digest"][:16]))
    if d != before["digest"]:
        failures.append("served snapshot is not the signed rebuild")
    lenovo = {}
    for r in rows:
        if r["security_key"] == p.LENOVO:
            lenovo[r["data_status"]] = lenovo.get(r["data_status"], 0) + 1
    print("Lenovo data_status served: %s (signed %s)" % (lenovo, before["lenovo_status"]))
    if lenovo != before["lenovo_status"]:
        failures.append("Lenovo data_status %s != signed %s" % (lenovo, before["lenovo_status"]))
    print("signed changes: data_status %d %s; articles_total %d; new keys %d; gone %d"
          % (len(before["status_changed"]), before["status_transitions"], len(before["articles_total_changed"]),
             len(before["new_keys"]), len(before["gone_keys"])))
    if before["gone_keys"]:
        failures.append("the signed expectation itself removes %d keys" % len(before["gone_keys"]))
    print("AC2 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
