"""AMGT_CORPUS round 40, CRPS-ap-10 (u) -- what a unit-map build WOULD change, field by field, before any write.

Read-only: it runs the production builder's own `--dry-run` path in memory (S3 reads of the landed raw; no Bloomberg call, no
file written, no S3 write) and compares the per-security entries it would produce with the committed `field_map.json`.

  python ap10u_unit_map_preview.py "<security>" ["<security>" ...]     (PYTHONPATH=. from the repository root)
  python ap10u_unit_map_preview.py --population                        (every crosswalk name; slower)

Per security it prints every field whose entry would be ADDED or CHANGED, with the old and new unit_status and unit; then,
over all the securities read, a count by field of ADDED and CHANGED, and the four dispersion fields' new statuses.
"""
import collections
import json
import os
import sys

RES = os.path.join("integrations", "bloomberg", "research")
sys.path.insert(0, RES)
import build_unit_map as bum  # noqa: E402

FOUR = ["BEST_CPS_STDDEV", "BEST_CPS_NUMEST", "BEST_EPS_STDDEV", "BEST_EPS_NUMEST"]


def per_security(doc):
    """{mnemonic: {security: {"unit": ..., "detail": ...}}} from a field_map document (`fields` is a list of entries, each
    carrying `unit` and `per_security_detail` dicts keyed by the security string)."""
    out = collections.defaultdict(dict)
    for entry in doc.get("fields") or []:
        name = entry.get("mnemonic")
        unit = entry.get("unit")
        detail = entry.get("per_security_detail") if isinstance(entry.get("per_security_detail"), dict) else {}
        units = unit if isinstance(unit, dict) else {sec: unit for sec in detail}  # a new field carries ONE unit string
        for sec in set(units) | set(detail):
            out[name][sec] = {"unit": units.get(sec), "detail": detail.get(sec),
                              "measured": sec in (entry.get("measured_on") or [])}
    return out


def brief(entry):
    if entry is None:
        return "ABSENT"
    return "%s | %s" % ("MEASURED" if entry.get("measured") else "not measured", str(entry.get("unit"))[:70])


def main(argv):
    args = [a for a in argv if a != "--population"]
    with open(bum.FIELD_MAP_PATH, encoding="utf-8") as fh:
        old_doc = json.load(fh)
    old = per_security(old_doc)
    import argparse
    s3 = bum._mbp._s3()
    ns = argparse.Namespace(securities=None if "--population" in argv else args,
                            population="crosswalk" if "--population" in argv else None)
    resolved = {}
    for sk in bum.resolve_population(ns, s3):
        got = bum.load_raw_for_key(s3, sk)
        if got is None:
            print("UNRESOLVED: no raw landed for %s" % sk)
            continue
        security, header, hist_rows, raw_stamp = got
        resolved[sk] = (security, bum.prepare_header(s3, security, sk, header, raw_stamp), hist_rows, raw_stamp)
    new_doc, summaries = bum.build_entries(resolved, False)
    new = per_security(new_doc)
    added = collections.Counter()
    changed = collections.Counter()
    four = collections.Counter()
    restamped = collections.Counter()
    securities = sorted({s for per in new.values() for s in per})
    shown = 0
    for name in sorted(new):
        for sec, entry in sorted(new[name].items()):
            before = old.get(name, {}).get(sec)
            if before == entry:
                continue
            if before is not None and before.get("unit") == entry.get("unit") and before.get("measured") == entry.get("measured"):
                restamped[name] += 1  # same unit and status; only the sample's raw stamp or value moved
                continue
            (added if before is None else changed)[name] += 1
            if name in FOUR:
                four[(name, "MEASURED" if entry.get("measured") else "not measured", str(entry.get("unit"))[:60])] += 1
            if shown < 60:
                shown += 1
                print("%-8s %-16s %-30s old %s -> new %s" % ("ADDED" if before is None else "CHANGED", sec, name, brief(before), brief(entry)))
    print("securities read %d (resolved %d) | fields with an ADDED entry %d (entries %d) | with a CHANGED entry %d (entries %d)" % (
        len(securities), len(resolved), len(added), sum(added.values()), len(changed), sum(changed.values())))
    print("RESTAMPED only (same unit and status) entries %d over %d fields" % (sum(restamped.values()), len(restamped)))
    print("ADDED by field:", dict(added.most_common(20)))
    print("CHANGED by field:", dict(changed.most_common(20)))
    for key, count in sorted(four.items()):
        print("FOUR %-18s %-28s %-60s x%d" % (key[0], key[1], key[2], count))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
