"""AMGT_CORPUS round 3 -- pre-flight of the 40-name induction fire, READ-ONLY (one S3 list + get of universe/v1).

Builds the crosswalk IN MEMORY through add_security's own builder with synthetic registrations shaped exactly as the
fire would write them, for every table row the PRODUCER WOULD CALL -- a row add_security._find_existing matches is
SKIPPED here exactly as the fire skips it (the branch this script missed at 20:4xZ, row Z-S23): the table's root/cc per folder, and `mode: ENRICH` wherever add_security's own
`_collision_mode` would return ENRICH (the key already MEASURED on a record with no folder). No Bloomberg call, no put.

Acceptance the fire needs (FWD-19: every folder ends with exactly ONE record):
  UNRESOLVED 40 -> 0, multi-claimed association forms 0, folders with more than one record 0,
  every prior MEASURED key present, and MEASURED rising by exactly the number of APPENDED registrations.
  FOLDER-FORM COVERAGE (row Z-S24): every called folder's own 'security-<hash>' association form, read from the
  BEFORE build, is claimed AFTER by exactly the record carrying that folder -- the form the corpus ingest resolves by.

  PYTHONPATH="$(pwd)" python org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/preflight_40_fire.py
"""
import collections
import json
import sys

from lib.research.identity import add_security, crosswalk

TABLE = "org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/UNRESOLVED40_CALLS_20260924.json"
AS_OF = sys.argv[1] if len(sys.argv) > 1 else "2026-09-24"


def synthetic(row, mode):
    key = "%s_%s_Equity" % (row["root"], row["cc"])
    out = {
        "folder": row["folder"], "bloomberg": "%s %s" % (row["root"], row["cc"]), "resolution": "MEASURED",
        "security_key": key, "exchange_finding": "AGREES: preflight", "registered_at": AS_OF + "T00:00Z",
        "raw_source": None,
        "identity": {"bloomberg_security": "%s %s Equity" % (row["root"], row["cc"]), "name": "PREFLIGHT " + row["folder"],
                     "exchange": row["cc"], "lei": None, "cik": None, "sec_id": None, "composite_figi": None,
                     "source": None, "registered_at": AS_OF + "T00:00Z", "field_errors": {}},
    }
    if mode == "ENRICH":
        out["mode"] = "ENRICH"
    return out


def summary(doc, label):
    den = doc["denominators"]
    claims = collections.defaultdict(set)
    per_folder = collections.Counter()
    for rec in doc["records"]:
        folder = (rec.get("source_row") or {}).get("folder")
        if folder:
            per_folder[folder] += 1
        for form in rec.get("association_keys") or []:
            claims[form].add(rec.get("security_key") or "<unresolved:%s>" % folder)
    multi = sorted(k for k, v in claims.items() if len(v) > 1)
    twins = sorted(f for f, n in per_folder.items() if n > 1)
    print("%-6s records %s MEASURED %s UNRESOLVED %s registered %s resolved_folders %s enriched %s | multi-claimed %d | twins %d"
          % (label, den.get("records"), den.get("MEASURED"), den.get("UNRESOLVED"), den.get("registered"),
             den.get("resolved_folders"), den.get("enriched"), len(multi), len(twins)))
    return den, multi, twins


def main():
    universe, source = add_security._identity_universe(None)
    rows, reg_path = crosswalk.load_registrations()
    base = add_security._build_document(AS_OF, list(rows), reg_path, universe, source)
    by_key = {r["security_key"]: r for r in base["records"] if r.get("security_key")}
    table = json.load(open(TABLE, encoding="utf-8"))["rows"]
    fakes, modes = [], collections.Counter()
    skipped, refused = [], set()
    for row in table:
        key = "%s_%s_Equity" % (row["root"], row["cc"])
        if add_security._find_existing(rows, row["folder"], "%s %s" % (row["root"], row["cc"])) is not None:
            skipped.append(row["folder"])
            continue
        other = by_key.get(key)
        if other is None:
            mode = None
        else:
            other_folder = (other.get("source_row") or {}).get("folder")
            same = (other.get("source_row") or {}).get("coverage_source") == base.get("coverage_source")
            mode = add_security._collision_mode(other_folder, row["folder"], same)
        modes[mode or "APPEND"] += 1
        if mode == "REFUSE":
            refused.add(row["folder"])
            print("REFUSE (a folder-vs-folder collision) %s -> %s" % (row["folder"], key))
            continue
        fakes.append(synthetic(row, mode))
    print("table %d | already-registered (skipped, no call) %d | modes of the called %s" % (len(table), len(skipped), dict(modes)))
    called = {row["folder"] for row in table if row["folder"] not in refused}
    # each folder's OWN form is the one the corpus ingest resolves by: crosswalk.harvester_key(folder, pilots)
    # (crosswalk.py:266), computed from the folder name -- never read off a build, which is the object under test
    pilots = crosswalk.load_pilots()
    forms_before = {fo: {crosswalk.harvester_key(fo, pilots)[0]} for fo in called}
    b_den, _, _ = summary(base, "BEFORE")
    try:
        after = add_security._build_document(AS_OF, list(rows) + fakes, reg_path, universe, source)
    except Exception as exc:  # the builder's own refusal is a finding, printed whole
        print("BUILD RAISED %s: %s" % (type(exc).__name__, exc))
        return 1
    a_den, multi, twins = summary(after, "AFTER")
    before_keys = {r["security_key"] for r in base["records"] if r.get("security_key")}
    after_keys = {r["security_key"] for r in after["records"] if r.get("security_key")}
    print("prior MEASURED keys present after: %d of %d | new keys %d | appended %d"
          % (len(before_keys & after_keys), len(before_keys), len(after_keys - before_keys), modes["APPEND"]))
    for folder in twins:
        recs = [r for r in after["records"] if (r.get("source_row") or {}).get("folder") == folder]
        print("  TWIN %-42s %s" % (folder, [(r.get("security_key"), r.get("resolution")) for r in recs]))
    uncovered = []
    for fo in sorted(called):
        holders = [r for r in after["records"] if (r.get("source_row") or {}).get("folder") == fo]
        keys_after = set(k for r in holders for k in r.get("association_keys") or [])
        if not forms_before.get(fo) or not forms_before[fo] <= keys_after:
            uncovered.append(fo)
    print("folder-form coverage: %d of %d table folders keep their own form on the record carrying them" % (len(called) - len(uncovered), len(called)))
    for fo in uncovered:
        print("  FORM LOST %s %s" % (fo, sorted(forms_before.get(fo) or [])))
    ok = (a_den.get("UNRESOLVED") == b_den.get("UNRESOLVED") - len(fakes) and not multi and not twins and not uncovered
          and before_keys <= after_keys and len(after_keys - before_keys) == modes["APPEND"])
    print("VERDICT %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
