"""AMGT_RESAPP round 50, AMGT-yy-6 -- THE CROSSWALK NEVER DROPS A SERVED RECORD (CTO round-49 s.4 cell 5; AMGT_CORPUS row Z-S63).

`crosswalk.build_crosswalk(as_of, ..., served=None, retire=())` -- when `served` (a served crosswalk document) is given, the build
starts from UNION: every served record whose `security_key` the build's own inputs do not hold is carried, EXCEPT a key named in
`retire` (the only way a record leaves), and ENRICH rows may target a carried record. The --write-pool path passes
`_read_pool_latest()`. Measured at the cut: the plain build on CLOUD REFUSES ("ENRICH row names security_key 'BZLFY_US_Equity',
which matches no coverage record") while the served pool (237 records) holds BZLFY_US_Equity -- that is the fork.
  --arm plant:     (a) a planted served record absent from the inputs survives; (b) naming it in `retire` removes it (control).
  --arm fork:      (d) the served pool's records the CLOUD-side inputs lack (today: BZLFY_US_Equity and any other) are ALL kept by
                   the CLOUD-side build, and that build no longer refuses.
  --arm roundtrip: (c) build at the served `as_of` with served = the served pool -> same record count and same serialised digest.
usage: python <this> --arm plant|fork|roundtrip   (from the repo root; reads the served pool read-only, writes nothing)"""
import argparse
import copy
import hashlib
import inspect
import os
import sys

sys.path.insert(0, os.getcwd())
from lib.research.identity import crosswalk as cw  # noqa: E402


def keys(doc):
    return {r.get("security_key") for r in (doc.get("records") or [])}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", choices=("plant", "fork", "roundtrip"), required=True)
    a = ap.parse_args()
    params = inspect.signature(cw.build_crosswalk).parameters
    if "served" not in params or "retire" not in params:
        print("build_crosswalk takes no served=/retire= (params: %s)" % ", ".join(params))
        print("THE CROSSWALK NEVER DROPS A SERVED RECORD (%s): NO" % a.arm)
        return 1
    s = cw._read_pool_latest()[0]
    as_of = s.get("as_of")
    print("served: %d records, as_of %s" % (len(s["records"]), as_of))
    if a.arm == "plant":
        planted = copy.deepcopy(s["records"][0])
        planted["security_key"] = "ZZPLANTED_US_Equity"
        s2 = dict(s, records=list(s["records"]) + [planted])
        kept = cw.build_crosswalk(as_of, served=s2)
        dropped = cw.build_crosswalk(as_of, served=s2, retire=("ZZPLANTED_US_Equity",))
        a_ok, b_ok = "ZZPLANTED_US_Equity" in keys(kept), "ZZPLANTED_US_Equity" not in keys(dropped)
        print("(a) planted served record survives: %s; (b) retirement removes it: %s" % (a_ok, b_ok))
        ok = a_ok and b_ok
    elif a.arm == "fork":
        try:
            cw.build_crosswalk(as_of)
            plain = None
        except ValueError as exc:
            plain = str(exc)[:120]
        built = cw.build_crosswalk(as_of, served=s)
        lost = sorted(keys(s) - keys(built))
        print("plain CLOUD build: %s" % ("REFUSED -- " + plain if plain else "builds"))
        print("(d) served records the CLOUD-side build+union drops: %d %s" % (len(lost), lost[:5]))
        ok = not lost and "BZLFY_US_Equity" in keys(built)
    else:
        built = cw.build_crosswalk(as_of, served=s)
        d_in = hashlib.sha256(cw.serialise(s)).hexdigest()
        d_out = hashlib.sha256(cw.serialise(built)).hexdigest()
        print("(c) records in %d out %d; digest in %s out %s" % (len(s["records"]), len(built.get("records") or []), d_in[:12], d_out[:12]))
        ok = len(s["records"]) == len(built.get("records") or []) and d_in == d_out
    print("THE CROSSWALK NEVER DROPS A SERVED RECORD (%s): %s" % (a.arm, "YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
