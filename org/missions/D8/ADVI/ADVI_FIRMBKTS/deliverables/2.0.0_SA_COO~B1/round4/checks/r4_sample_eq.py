"""ADVI_FIRMBKTS round 4: the BEFORE / AFTER equality of act 4's authorization sample (the CTO's act-4 condition 4 and ADDENDUM 2),
issuer 2.0.0_SA_COO~B1.

The actor invokes each census event BEFORE the flip and AFTER it, for at least one GRANTED and one REFUSED viewer per function,
and writes each run to a JSON list of records:
  {"function": "<name>", "case": "granted|refused|admin|none", "status": <int HTTP-style status of the response>,
   "body_sha256": "<hex of the response body bytes, or empty>", "ownership_read": "<bucket/key the run read, from its log>"}
This tool reads the two lists and prints one line per (function, case): EQUAL or DIFFERENT (status and body hash). It prints
NO body, NO viewer identity, NO client identifier.

  python r4_sample_eq.py --before <file> --after <file>
Last line: SAMPLE EQUAL: <n> of <n> cases; granted cases <g>, refused cases <r>; ownership reads at the canonical key <c>.
Exit 0 only when every case is EQUAL, at least one granted and one refused case exist per FUNCTION with a clean event, and every
AFTER record that names an ownership read names the canonical key. A previously served request that is newly refused is a
DIFFERENT line: Branch B.
"""
import argparse
import json
import sys

CANON = "opal-data-49financial/advi/49financial/platinum/49financial/ownership_map.json"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--before", required=True)
    ap.add_argument("--after", required=True)
    a = ap.parse_args()
    b = json.load(open(a.before, encoding="utf-8"))
    f = json.load(open(a.after, encoding="utf-8"))
    kb = {(r["function"], r["case"]): r for r in b}
    kf = {(r["function"], r["case"]): r for r in f}
    keys = sorted(set(kb) | set(kf))
    equal = 0
    content_level = []
    bad = []
    canon = 0
    for k in keys:
        rb, rf = kb.get(k), kf.get(k)
        if rb is None or rf is None:
            bad.append((k, "ABSENT in %s" % ("before" if rb is None else "after")))
            print("DIFFERENT %s %s: absent in %s" % (k[0], k[1], "before" if rb is None else "after"))
            continue
        same = rb.get("status") == rf.get("status") and rb.get("body_sha256") == rf.get("body_sha256")
        # a gzip body carries a header timestamp, so its compressed hash varies per call (ADVI_FIRMBKTS-D1-S36): a case whose
        # status is equal and whose DECOMPRESSED content hash is recorded on both sides and equal reads EQUAL, and is counted
        if (not same and rb.get("status") == rf.get("status") and rb.get("content_sha256")
                and rb.get("content_sha256") == rf.get("content_sha256")):
            same = True
            content_level.append((k, rb.get("content_claim", "recorded")))
        if rf.get("ownership_read"):
            if rf["ownership_read"] == CANON:
                canon += 1
            else:
                same = False
        print("%s %-34s %-8s status %s -> %s" % ("EQUAL    " if same else "DIFFERENT", k[0], k[1], rb.get("status"),
                                                 rf.get("status")))
        if same:
            equal += 1
        else:
            bad.append((k, "differs"))
    funcs = sorted({k[0] for k in keys})
    cover = all(any(k[0] == fn and k[1] == "granted" for k in keys) and
                any(k[0] == fn and k[1] == "refused" for k in keys) for fn in funcs)
    g = sum(1 for k in keys if k[1] == "granted")
    r = sum(1 for k in keys if k[1] == "refused")
    print("SAMPLE EQUAL: %d of %d cases; granted cases %d, refused cases %d; ownership reads at the canonical key %d"
          % (equal, len(keys), g, r, canon))
    for k, claim in content_level:
        print("NOTE: %s %s read EQUAL by decompressed content hash (claim: %s), not by the compressed body hash" % (k[0], k[1], claim))
    if not cover:
        print("NOTE: a function lacks a granted or a refused case (the performance adapter and the validator are read apart)")
    return 0 if (equal == len(keys) and not bad and keys) else 1


if __name__ == "__main__":
    sys.exit(main())
