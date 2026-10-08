"""AMGT_CORPUS round 40, CRPS-ap-8, FWD-16 (round-39 analysis ruling 6): the 2026-09-29 comparison
extended to pillars and management, 95 names. Read-only. Issuer's file.

For every resolved name: the BEFORE object is the stored dossier written on 2026-09-29 (gold never
overwrites; the newest LastModified among that date's objects), the AFTER object is the one the
served reader picks today (`dossier._read_dossier_detail`). Per slot kind -- pillars, management,
cases -- each name reads KEPT / GAINED / LOST / CHANGED / NONE, grouped by today's pack_shape.
Cases ride as the control: the 2026-10-06 case census read 0 of 95 changed against the same date.

Usage (repo root): python org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/checks/round40/ap8_fwd16_census.py
"""
import collections
import concurrent.futures
import json
import os
import sys

sys.path.insert(0, os.getcwd())

from lib.research.corpus import dossier, gold  # noqa: E402
from lib.research.harvest import store  # noqa: E402

BASE_DATE = "2026-09-29"


def _pillars(doc):
    v = (doc.get("fields") or {}).get("thesis_pillars")
    if isinstance(v, dict) and "value" in v:
        v = v.get("value")
    if isinstance(v, dict):
        v = v.get("pillars", v.get("items"))
    if isinstance(v, list):
        # compared on the pillar's title and text: `terms` (FWD-18) and citation shape were added after the base date
        return len(v), json.dumps([(p.get("pillar"), p.get("text")) if isinstance(p, dict) else p for p in v])
    return 0, None


def _management(doc):
    v = (doc.get("fields") or {}).get("management")
    if isinstance(v, dict) and v.get("value"):
        return 1, json.dumps(v.get("value"), sort_keys=True)
    return 0, None


def _cases(doc):
    cases = (doc.get("fields") or {}).get("cases") or {}
    n, body = 0, []
    for name in sorted(cases):
        v = cases[name]
        if isinstance(v, dict) and v.get("value"):
            n += 1
            body.append((name, json.dumps(v.get("value"), sort_keys=True)))
    return n, json.dumps(body)


def _verdict(before, after):
    (nb, tb), (na, ta) = before, after
    if nb == 0 and na == 0:
        return "NONE"
    if na < nb:
        return "LOST"
    if na > nb:
        return "GAINED"
    return "KEPT" if tb == ta else "CHANGED"


def one(key, client):
    objects = dossier._list_stored_objects(key, client)
    base = [(k, lm) for k, lm in objects if dossier._dossier_as_of_date(k) == BASE_DATE]
    if not base:
        return key, None
    base_key = max(base, key=lambda p: (p[1], p[0]))[0]
    before = json.loads(gold.gold_get("s3://%s/%s" % (gold.HARVEST_BUCKET, base_key), client=client).decode("utf-8"))
    _uri, after, _cur = dossier._read_dossier_detail(key, client)
    shape = ((after.get("fields") or {}).get("pack_shape") or {})
    shape = shape.get("value") if isinstance(shape, dict) else shape
    row = {"shape": str(shape), "before_method": before.get("method_version"), "after_method": after.get("method_version")}
    for kind, fn in (("pillars", _pillars), ("management", _management), ("cases", _cases)):
        b, a = fn(before), fn(after)
        row[kind] = (_verdict(b, a), b[0], a[0])
    return key, row


def main():
    client = store._default_client()
    keys = sorted(dossier._resolved_security_keys(client=client))
    rows, no_base = {}, []
    with concurrent.futures.ThreadPoolExecutor(8) as ex:
        for key, row in ex.map(lambda k: one(k, client), keys):
            if row is None:
                no_base.append(key)
            else:
                rows[key] = row
    for key in sorted(rows):
        r = rows[key]
        print("fwd16 %s shape %s %s" % (key, r["shape"], " ".join(
            "%s %s %d->%d" % (k, r[k][0], r[k][1], r[k][2]) for k in ("pillars", "management", "cases"))))
    for key in no_base:
        print("fwd16 %s NO-BASE-OBJECT-ON %s" % (key, BASE_DATE))
    print("DENOMINATOR names resolved %d compared %d no_base %d" % (len(keys), len(rows), len(no_base)))
    for kind in ("pillars", "management", "cases"):
        tally = collections.Counter((r["shape"], r[kind][0]) for r in rows.values())
        total = collections.Counter(r[kind][0] for r in rows.values())
        print("TOTAL %s %s" % (kind, " ".join("%s %d" % kv for kv in sorted(total.items()))))
        for shape in sorted({s for s, _ in tally}):
            print("  shape %s %s %s" % (shape, kind, " ".join(
                "%s %d" % (v, c) for (s, v), c in sorted(tally.items()) if s == shape)))
    lost = [(k, kind) for k, r in rows.items() for kind in ("pillars", "management", "cases") if r[kind][0] == "LOST"]
    print("LOST %d %s" % (len(lost), " ".join("%s:%s" % p for p in sorted(lost))))
    print("METHODS before %s after %s" % (dict(collections.Counter(r["before_method"] for r in rows.values())),
                                          dict(collections.Counter(r["after_method"] for r in rows.values()))))


if __name__ == "__main__":
    main()
