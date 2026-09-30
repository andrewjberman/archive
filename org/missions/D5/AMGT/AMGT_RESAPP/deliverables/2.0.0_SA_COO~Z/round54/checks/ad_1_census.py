"""AMGT_RESAPP round 54, AMGT-ad-1 AC1 -- the census of NON-VERBATIM SERVED D-1 sentences equals an independent recount.
Population of record: the MEASURED security_keys of the newest crosswalk/v1/<date>.json (drafting_build._measured_population), each
name's stored D-1 document at drafting/v1/<slash_safe_key(key)>.json (read-only). A sentence counts when it sits in the STORED
`sections[].sentences` and carries no non-blank quoted span -- the DEPLOYED adapter's own read gate (scoped_amgt.py ~:1833), which
already HOLDS it at read (the served /thesis shows it as held_no_span_at_read, never as a sentence).
The worker's census file (CENSUS below) must carry, per name, the same count and the same (section, text) set as this recount, over the
same population key and denominator. Prints the population, the names with a stored document, the total and the per-name counts.
usage: python <this> [--recount-only]   (from the repo root; S3 read-only; writes nothing)"""
import json
import os
import sys

sys.path.insert(0, os.getcwd())
import boto3  # noqa: E402
from lib.research.filings import drafting_build as db  # noqa: E402
from lib.research.identity import crosswalk  # noqa: E402

CENSUS = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~193/D1_UNSPANNED_CENSUS.json"


def unspanned(doc):
    out = []
    for sec in doc.get("sections") or []:
        for s in sec.get("sentences") or []:
            if not any(str(x).strip() for x in s.get("quoted_spans") or []):
                out.append([sec.get("section"), str(s.get("text"))])
    return out


def recount(cl):
    listing = cl.list_objects_v2(Bucket=crosswalk.POOL_BUCKET, Prefix="crosswalk/v1/")
    pop_key = max(o["Key"] for o in listing.get("Contents", []))
    keys, denom = db._measured_population(pop_key, cl)
    names, stored = {}, 0
    for k in keys:
        raw = db._get_object_bytes_or_none(cl, db._drafting_pool_key(k))
        if raw is None:
            continue
        stored += 1
        u = unspanned(json.loads(raw.decode("utf-8")))
        if u:
            names[k] = {"unspanned": len(u), "sentences": u}
    return pop_key, denom, stored, names


def main():
    cl = boto3.client("s3", region_name="us-east-1")
    pop_key, denom, stored, names = recount(cl)
    total = sum(v["unspanned"] for v in names.values())
    print("population %s: MEASURED %d; stored D-1 documents %d; names with a non-verbatim served sentence %d; total %d"
          % (pop_key, denom, stored, len(names), total))
    for k in sorted(names):
        print("  %s %d" % (k, names[k]["unspanned"]))
    if "--recount-only" in sys.argv:
        return 0
    try:
        census = json.load(open(CENSUS, encoding="utf-8"))
    except FileNotFoundError:
        print("no census at %s" % CENSUS)
        print("THE CENSUS EQUALS AN INDEPENDENT RECOUNT: NO")
        return 1
    bad = []
    if census.get("population_key") != pop_key or census.get("denominator") != denom:
        bad.append("population %r/%r vs %r/%r" % (census.get("population_key"), census.get("denominator"), pop_key, denom))
    cn = census.get("names") or {}
    for k in sorted(set(cn) | set(names)):
        a, b = cn.get(k) or {}, names.get(k) or {}
        if a.get("unspanned", 0) != b.get("unspanned", 0) or \
                sorted(map(tuple, a.get("sentences") or [])) != sorted(map(tuple, b.get("sentences") or [])):
            bad.append("%s: census %d, recount %d" % (k, a.get("unspanned", 0), b.get("unspanned", 0)))
    if census.get("total") != total:
        bad.append("total: census %r, recount %d" % (census.get("total"), total))
    for x in bad[:20]:
        print("  BAD", x)
    ok = not bad
    print("THE CENSUS EQUALS AN INDEPENDENT RECOUNT: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
