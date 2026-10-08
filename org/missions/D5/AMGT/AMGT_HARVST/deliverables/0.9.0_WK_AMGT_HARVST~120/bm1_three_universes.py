# The FINAL rank_universe_20261008.json and rank_universe_identity_20261008.json are built by 0.9.0_WK_AMGT_HARVST~121/bn1_names_made_whole.py in ONE run; this script is kept as the record of how they were first made, and re-running it reverts the final files.
"""HVST-bm-1 (round 68): reconcile the three security universes and write the missing identity records as NEW files.

The three sets (join key for every one: the pool `security_key`, e.g. `CAT_US_Equity`):
  - the SERVED GOLD LIST (`round64/securities.universe.r64.json`, one object per security, `security_key`);
  - the CROSSWALK (`crosswalk/v1/<latest>.json` in the pool, `records[].security_key`; the loader's own latest read);
  - the COLLECTOR'S UNIVERSE (`round47/rank_universe_20261005.json` `entries[].security_key`) with its search identities
    (`round47/rank_universe_identity_20261005.json` `records[].security_key`; the record's own `key` is the collector's job
    key, not a join key).

Writes, beside this file (NOT in round 47, and `lib/opal_data_harvest/config.json` is not touched):
  - `rank_universe_20261008.json`: the 234 round-47 entries unchanged, then one entry per key that is on the gold list and
    absent from the collector (built like the pool entries `chatter_axis._universe_entries` makes; an entry whose pool record
    carries no name takes `identity.name` from `lib/research/identity/registrations.json`, the HVST-bh-4 precedent).
  - `rank_universe_identity_20261008.json`: `0.9.0_WK_AMGT_HARVST~94/build_rank_identity.py`'s own rules (R0-R3), run
    against the widened snapshot, as `at-5.widen_universe.py` runs them. The 234 round-47 records must come out identical.

Reads only: the local files above, `lib/research/identity/registrations.json`, and TWO read-only S3 GETs (the pool universe
`universe/v1/2026-10-06.json` and the latest crosswalk). NO put, NO vendor, NO publisher, NO Bloomberg, NO job.

Run: PYTHONPATH=. python org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~120/bm1_three_universes.py
"""

import contextlib
import hashlib
import importlib.util
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, *([os.pardir] * 7)))
sys.path.insert(0, ROOT)

DELIV = os.path.join(ROOT, "org", "missions", "D5", "AMGT", "AMGT_HARVST", "deliverables")
GOLD = os.path.join(DELIV, "2.0.0_SA_COO_H", "round64", "securities.universe.r64.json")
R47_SNAPSHOT = os.path.join(DELIV, "2.0.0_SA_COO_H", "round47", "rank_universe_20261005.json")
R47_IDENTITY = os.path.join(DELIV, "2.0.0_SA_COO_H", "round47", "rank_universe_identity_20261005.json")
W94_BUILDER = os.path.join(DELIV, "0.9.0_WK_AMGT_HARVST~94", "build_rank_identity.py")
REGISTRATIONS = os.path.join(ROOT, "lib", "research", "identity", "registrations.json")
NEW_SNAPSHOT = os.path.join(HERE, "rank_universe_20261008.json")
NEW_IDENTITY = os.path.join(HERE, "rank_universe_identity_20261008.json")

BUCKET = "opal-data-harvest"
UNIVERSE_KEY = "universe/v1/2026-10-06.json"
ORDER_CROSSWALK_KEY = "crosswalk/v1/2026-09-29.json"
NAMED_THREE = ("CAT_US_Equity", "CSL_AU_Equity", "6861_JP_Equity")
AUTHOR = "0.9.0_WK_AMGT_HARVST~120"

REGIONS = (
    ("IN ALL THREE", (1, 1, 1)),
    ("LIST AND CROSSWALK, NOT COLLECTOR", (1, 1, 0)),
    ("LIST AND COLLECTOR, NOT CROSSWALK", (1, 0, 1)),
    ("CROSSWALK AND COLLECTOR, NOT LIST", (0, 1, 1)),
    ("LIST ONLY", (1, 0, 0)),
    ("CROSSWALK ONLY", (0, 1, 0)),
    ("COLLECTOR ONLY", (0, 0, 1)),
)


def load(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def _refuse_live_collector_pointer(path):
    """Row AMGT_HARVST-Z-W120-S3, disarmed by row AMGT_HARVST-Z-S105 (2.0.0_SA_COO~H): a file that
    lib/opal_data_harvest/config.json names is the LIVE collector list, and re-running this record script would silently
    revert the repairs made to it after this script ran. Writing it is refused."""
    root = os.path.dirname(os.path.abspath(__file__))
    while not os.path.exists(os.path.join(root, "lib", "opal_data_harvest", "config.json")):
        parent = os.path.dirname(root)
        if parent == root:
            return
        root = parent
    with open(os.path.join(root, "lib", "opal_data_harvest", "config.json"), encoding="utf-8") as handle:
        config = json.load(handle)
    target = os.path.normcase(os.path.abspath(path))
    for value in config.values():
        if isinstance(value, str) and target == os.path.normcase(os.path.abspath(os.path.join(root, value))):
            raise SystemExit("REFUSED: %s is a live collector pointer in config.json (row AMGT_HARVST-Z-W120-S3)" % path)


def write_json(path, value):
    _refuse_live_collector_pointer(path)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(value, indent=2, ensure_ascii=True) + "\n")


def s3_get(client, key):
    body = client.get_object(Bucket=BUCKET, Key=key)["Body"].read()
    return json.loads(body.decode("utf-8")), hashlib.sha256(body).hexdigest()


def first_name(*pairs):
    for label, value in pairs:
        if isinstance(value, str) and value.strip():
            return value, label
    return None, "no source gives a name"


def main():
    import boto3
    from lib.research.identity import crosswalk as crosswalk_mod

    client = boto3.client("s3", region_name="us-east-1")
    gold = load(GOLD)
    old_snap = load(R47_SNAPSHOT)
    old_ident = load(R47_IDENTITY)
    pool_doc, pool_sha = s3_get(client, UNIVERSE_KEY)
    cw_doc, cw_key = crosswalk_mod._read_pool_latest(client)
    order_cw, order_cw_sha = s3_get(client, ORDER_CROSSWALK_KEY)
    registrations = load(REGISTRATIONS)["registrations"]

    gold_by = {g["security_key"]: g for g in gold}
    cw_by = {r["security_key"]: r for r in cw_doc["records"]}
    entry_by = {e["security_key"]: e for e in old_snap["entries"]}
    rec_by = {r["security_key"]: r for r in old_ident["records"]}
    pool_by = {n["security_key"]: n for n in pool_doc["names"] if n.get("security_key")}
    reg_by = {r["security_key"]: r for r in registrations if r.get("security_key")}

    list_keys, cw_keys, col_keys = set(gold_by), set(cw_by), set(entry_by)
    print("DENOMINATORS: gold list %d, crosswalk %d, collector universe %d, collector identity records %d"
          % (len(list_keys), len(cw_keys), len(col_keys), len(rec_by)))
    print("JOIN KEYS: gold list `security_key` (equals `key`); crosswalk records[].`security_key`; collector universe "
          "entries[].`security_key`; collector identity records[].`security_key` (the record's own `key` is the "
          "collector's job key, not used to join)")
    print("SOURCES READ: pool s3://%s/%s (%d name records, %d with a security_key, sha256 %s); crosswalk s3://%s/%s "
          "(as_of %s, %d records); registrations.json (%d registrations, %d with a security_key)"
          % (BUCKET, UNIVERSE_KEY, len(pool_doc["names"]), len(pool_by), pool_sha, BUCKET, cw_key, cw_doc.get("as_of"),
             len(cw_doc["records"]), len(registrations), len(reg_by)))
    order_keys = {r["security_key"] for r in order_cw["records"]}
    print("CROSSWALK OBJECT NOTE: the order's 237 is s3://%s/%s (%d records, sha256 %s); the loader reads the latest, "
          "%s (%d). In the latest and not in the 237: %s; in the 237 and not in the latest: %s"
          % (BUCKET, ORDER_CROSSWALK_KEY, len(order_keys), order_cw_sha, cw_key, len(cw_keys),
             sorted(cw_keys - order_keys), sorted(order_keys - cw_keys)))
    print("COLLECTOR FILES CHECK: entry keys == identity record keys: %s (entries only %s, records only %s)"
          % (col_keys == set(rec_by), sorted(col_keys - set(rec_by)), sorted(set(rec_by) - col_keys)))

    union = list_keys | cw_keys | col_keys
    members = {}
    for key in sorted(union):
        members.setdefault((int(key in list_keys), int(key in cw_keys), int(key in col_keys)), []).append(key)
    print("REGIONS OF THE THREE-SET COMPARISON (union %d):" % len(union))
    total = 0
    for label, flags in REGIONS:
        keys = members.get(flags, [])
        total += len(keys)
        print("  %-36s %d" % (label, len(keys)))
    off_list = len(members.get((1, 1, 0), [])) + len(members.get((1, 0, 0), []))
    off_col = len(members.get((0, 1, 1), [])) + len(members.get((0, 0, 1), []))
    print("ON THE LIST, NOT IN THE COLLECTOR: %d" % off_list)
    print("IN THE COLLECTOR, NOT ON THE LIST: %d" % off_col)
    print("IN THE CROSSWALK ONLY: %d" % len(members.get((0, 1, 0), [])))
    print("IN THE CROSSWALK, NOT ON THE LIST: %d" % (len(members.get((0, 1, 1), [])) + len(members.get((0, 1, 0), []))))
    print("IN THE CROSSWALK, NOT IN THE COLLECTOR: %d"
          % (len(members.get((1, 1, 0), [])) + len(members.get((0, 1, 0), []))))
    print("REGION SUM %d vs UNION %d" % (total, len(union)))
    for label, flags in REGIONS[1:]:
        for key in members.get(flags, []):
            pool_rec, reg, cwr = pool_by.get(key), reg_by.get(key), cw_by.get(key)
            name, name_src = first_name(
                ("gold list company", (gold_by.get(key) or {}).get("company")),
                ("crosswalk legal_name", ((cwr or {}).get("legal_name") or {}).get("value")),
                ("registry identity.name", ((reg or {}).get("identity") or {}).get("name")),
                ("pool name", (pool_rec or {}).get("name")),
                ("collector entry name", (entry_by.get(key) or {}).get("name")))
            carried = []
            if pool_rec:
                carried.append("pool record (source=%s, name=%r)" % (pool_rec.get("source"), pool_rec.get("name")))
            if reg:
                carried.append("registry entry (registered_at %s)" % reg.get("registered_at"))
            if cwr:
                carried.append("crosswalk record (coverage_source %s)" % cwr["source_row"].get("coverage_source"))
            print("  [%s] %s | %s (%s) | carried by: %s"
                  % (label, key, name, name_src, "; ".join(carried) or "none of pool record, registry entry, crosswalk record"))

    # ---- the new files -------------------------------------------------------------------------------------------
    to_add = sorted(list_keys - col_keys)
    added = []
    nameless = set()
    for key in to_add:
        pool_rec = pool_by.get(key)
        if pool_rec is None:
            raise SystemExit("ERROR: %s is on the gold list and has no pool record to build an entry from" % key)
        name = pool_rec.get("name")
        origin = "lib/research/harvest/universe_securities.py build() off universe/v1/2026-10-06.json names[] (pool record, source=%s)" % pool_rec.get("source")
        if not (isinstance(name, str) and name.strip()):
            reg = reg_by.get(key)
            name = ((reg or {}).get("identity") or {}).get("name")
            if not (isinstance(name, str) and name.strip()):
                raise SystemExit("ERROR: %s has no name in the pool record or in registrations.json" % key)
            nameless.add(key)
            origin = ("pool record (source=%s) carries name null; name from lib/research/identity/registrations.json "
                      "identity.name, registered_at %s" % (pool_rec.get("source"), reg.get("registered_at")))
        added.append({"identity": key, "security_key": key, "ticker": pool_rec["ticker"],
                      "identity_status": "MEASURED", "name": name, "resolution": pool_rec["resolution"],
                      "added_from": "HVST-bm-1: on the gold list r64 and absent from rank_universe_20261005.json; " + origin})

    doc = dict(old_snap)
    doc["entries"] = old_snap["entries"] + added
    doc["names_considered"] = len(doc["entries"])
    doc["widened"] = {"by": "HVST-bm-1 (%s for 2.0.0_SA_COO~H)" % AUTHOR, "base": os.path.basename(R47_SNAPSHOT),
                      "base_names": len(old_snap["entries"]), "added": len(added),
                      "added_from_source": "s3://%s/%s plus lib/research/identity/registrations.json (names only)"
                                           % (BUCKET, UNIVERSE_KEY),
                      "authority": "1.0.0_SA_CTO~Z msg 31637 (R19, R20) on 4.0.0_SA_CRO~Z research @2394cfc3d8; "
                                   "nothing fetched, no config pointer moved; a run for any added name waits on "
                                   "Andrew's per-use word",
                      "previous": old_snap.get("widened")}
    write_json(NEW_SNAPSHOT, doc)

    spec = importlib.util.spec_from_file_location("build_rank_identity", W94_BUILDER)
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    builder.SNAPSHOT, builder.IDENTITY = NEW_SNAPSHOT, NEW_IDENTITY
    saved_argv = sys.argv
    sys.argv = [sys.argv[0]]
    with contextlib.redirect_stdout(io.StringIO()):
        builder.main()
    sys.argv = saved_argv

    ident = load(NEW_IDENTITY)
    for rec in ident["records"]:
        if rec["security_key"] in nameless:
            rec["pool_name"] = None
            rec["company"]["status"] = "MEASURED"
            rec["company"]["evidence"] = ("pool record carries name null; lib/research/identity/registrations.json "
                                          "identity.name (the Bloomberg NAME of the registration pull)")
    ident["artifact"] = "rank universe search identities (HVST-as-1, widened by HVST-bm-1)"
    ident["author"] = AUTHOR
    ident["rules"] = list(old_ident["rules"]) + [
        "",
        "HVST-bm-1 (round 68, %s): the keys on the gold list r64 and absent from rank_universe_20261005.json are appended" % AUTHOR,
        "after the 234 round-47 records, built by R0-R3 above from stored sources only (the pool record,",
        "registrations.json). N1: an entry whose pool record carries no name takes registrations.json identity.name",
        "(the HVST-bh-4 precedent), status MEASURED, and its pool_name is null. No vendor call.",
    ]
    ident["snapshot"] = os.path.basename(NEW_SNAPSHOT)
    ident["denominator"] = {"names": len(ident["records"]), "from_round47": len(old_ident["records"]), "added": len(added)}
    write_json(NEW_IDENTITY, ident)

    # ---- checks, read back from the written files ---------------------------------------------------------------
    new_snap = load(NEW_SNAPSHOT)
    new_ident = load(NEW_IDENTITY)
    new_entry_by = {e["security_key"]: e for e in new_snap["entries"]}
    new_rec_by = {r["security_key"]: r for r in new_ident["records"]}
    changed = 0
    for key, old in entry_by.items():
        changed += int(new_entry_by.get(key) != old)
    for key, old in rec_by.items():
        changed += int(new_rec_by.get(key) != old)
    order_same = (new_snap["entries"][:len(old_snap["entries"])] == old_snap["entries"]
                  and new_ident["records"][:len(old_ident["records"])] == old_ident["records"])
    print("ADDED: %d" % len(added))
    for entry in added:
        rec = new_rec_by[entry["security_key"]]
        print("  %s | company %r [%s: %s] | ticker %r [%s] | search forms %r [%s] | sa_symbol %r [%s: %s] | key %s"
              % (entry["security_key"], rec["company"]["value"], rec["company"]["status"], rec["company"]["evidence"],
                 rec["ticker"]["value"], rec["ticker"]["evidence"], rec["aliases"]["value"], rec["aliases"]["evidence"],
                 rec["sa_symbol"]["value"], rec["sa_symbol"]["status"], rec["sa_symbol"]["evidence"], rec["key"]))
        print("    entry source: %s" % entry["added_from"])
    print("EXISTING RECORDS CHANGED: %d (compared %d entries and %d records with the round-47 files; round-47 order kept: %s)"
          % (changed, len(entry_by), len(rec_by), order_same))
    print("NEW FILES: %s (%d entries, names_considered %d), %s (%d records)"
          % (os.path.basename(NEW_SNAPSHOT), len(new_snap["entries"]), new_snap["names_considered"],
             os.path.basename(NEW_IDENTITY), len(new_ident["records"])))

    failures = []
    for label, count in (("gold list", len(list_keys)), ("crosswalk", len(cw_keys)),
                         ("collector universe", len(col_keys)), ("collector identity records", len(rec_by))):
        if count <= 0:
            failures.append("denominator %s is %d" % (label, count))
    if total != len(union):
        failures.append("regions sum %d != union %d" % (total, len(union)))
    if len(added) < 3 or not set(NAMED_THREE) <= set(new_rec_by) - set(rec_by):
        failures.append("ADDED %d does not include the three named keys" % len(added))
    if changed != 0 or not order_same:
        failures.append("EXISTING RECORDS CHANGED %d (order kept %s)" % (changed, order_same))
    if len(new_rec_by) != len(new_entry_by) or set(new_rec_by) != set(new_entry_by):
        failures.append("new entries and new records do not cover the same keys")
    if failures:
        print("RECONCILE FAIL: " + "; ".join(failures))
        return 1
    print("RECONCILE OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
