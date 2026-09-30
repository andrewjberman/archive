"""AMGT_RESAPP round 51, AMGT-zz-8 -- the NAMED, NON-INERT RIDER: AMGT_HARVST n-6's /timeline/day read path (timeline_api.py, drained
@150b717373) ships in this build (CTO msg 26878; AMGT_HARVST round-24 analysis @6c5b4339a1 ruling 1). Its body must not move:
for the 4 days n-6 measured (n6_common.ALL_DAYS), the OLD path's body (n6_old_path.py, lib @d357a9e247 verbatim, run locally in a fresh
process) and the DEPLOYED route's body (read-only Invoke) are byte-equal (sha256 each), and the deployed Lambda REPORT duration is
printed beside it (the latency the pair expects to move). Writes nothing (n-6's own n6_body_equality.py writes a HARVST file).
usage: python <this>   (from the repo root; S3 GET/LIST + read-only Invokes)"""
import os
import sys

SCRIPTS = "org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~60/scripts"


def main():
    sys.path.insert(0, os.path.abspath(SCRIPTS))
    import n6_common as c
    equal = 0
    for key, day in c.ALL_DAYS:
        _reps, old_body = c.spawn("old", key, day, 1)
        _w, rep, status, dep_body = c.invoke_deployed(key, day)
        eq = old_body == dep_body
        equal += 1 if eq else 0
        print("%s %s  OLD %s  DEPLOYED %s (status %s, REPORT %s ms)  equal %s" % (
            key, day, c.sha256_text(old_body)[:16], c.sha256_text(dep_body)[:16], status, rep.get("duration_ms"), eq))
    n = len(c.ALL_DAYS)
    print("OLD == DEPLOYED byte-equal on %d of %d days" % (equal, n))
    ok = equal == n
    print("THE TIMELINE DAY BODY DID NOT MOVE ON THE DEPLOYED FUNCTION: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
