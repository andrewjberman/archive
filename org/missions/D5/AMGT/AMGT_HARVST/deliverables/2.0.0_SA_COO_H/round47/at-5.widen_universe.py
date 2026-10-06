"""HVST-at-5 (round 47, Andrew-direct 2026-10-05 ~16:3xZ "Yes I do" to adding the 59 research names): widen the run universe.

The run's universe (`rank_universe_20260916.json`, 191 names) predates the research-name resolutions that landed in
`lib/research/identity/registrations.json` on 2026-09-24/25/29. This adds every research FOLDER registration (MEASURED,
with a Bloomberg ticker) whose security key is not already in the 191: the 56 approved resolutions (@b7819604e0,
@505fc14404) plus the folders added after the 2026-09-16 snapshot that no fund holds (Quanta PWR US, AIA 1299 HK,
Hitachi 6501 JP). NO vendor call, NO S3 call.

Writes, beside this file:
- `rank_universe_20261005.json`: the 191 entries unchanged, then the added entries (same fields).
- `rank_universe_identity_20261005.json`: built by worker ~94's own `build_rank_identity.py` rules (R0-R3), run against
  the widened snapshot. The 191 original records must come out IDENTICAL to `rank_universe_identity_20260916.json`
  (same collector keys), or this script fails.
"""

import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, *([os.pardir] * 8)))
sys.path.insert(0, ROOT)

W94 = os.path.join(ROOT, "org", "missions", "D5", "AMGT", "AMGT_HARVST", "deliverables", "0.9.0_WK_AMGT_HARVST~94")
OLD_SNAPSHOT = os.path.join(W94, "rank_universe_20260916.json")
OLD_IDENTITY = os.path.join(W94, "rank_universe_identity_20260916.json")
REGISTRATIONS = os.path.join(ROOT, "lib", "research", "identity", "registrations.json")
NEW_SNAPSHOT = os.path.join(HERE, "rank_universe_20261005.json")
NEW_IDENTITY = os.path.join(HERE, "rank_universe_identity_20261005.json")


def main():
    old = json.load(open(OLD_SNAPSHOT, encoding="utf-8"))
    have = {e["security_key"] for e in old["entries"]}
    added, seen = [], set()
    for reg in json.load(open(REGISTRATIONS, encoding="utf-8"))["registrations"]:
        key = reg.get("security_key")
        if not reg.get("folder") or not reg.get("bloomberg") or reg.get("resolution") != "MEASURED":
            continue
        if key in have or key in seen:
            continue
        seen.add(key)
        added.append({"identity": key, "security_key": key, "ticker": reg["bloomberg"], "identity_status": "MEASURED",
                      "name": reg["folder"], "resolution": "MEASURED",
                      "added_from": "lib/research/identity/registrations.json registered_at %s" % reg.get("registered_at")})
    doc = dict(old)
    doc["entries"] = old["entries"] + added
    doc["names_considered"] = len(doc["entries"])
    doc["widened"] = {"by": "HVST-at-5 (2.0.0_SA_COO~H)", "base": os.path.basename(OLD_SNAPSHOT),
                      "base_names": len(old["entries"]), "added": len(added),
                      "authority": "Andrew-direct 2026-10-05 'Yes I do' (add the 59 research names)"}
    with open(NEW_SNAPSHOT, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(doc, indent=2, ensure_ascii=True) + "\n")

    spec = importlib.util.spec_from_file_location("build_rank_identity", os.path.join(W94, "build_rank_identity.py"))
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    builder.SNAPSHOT, builder.IDENTITY = NEW_SNAPSHOT, NEW_IDENTITY
    sys.argv = [sys.argv[0]]
    builder.main()

    new_records = json.load(open(NEW_IDENTITY, encoding="utf-8"))["records"]
    old_records = json.load(open(OLD_IDENTITY, encoding="utf-8"))["records"]
    same = new_records[: len(old_records)] == old_records
    print("base names %d, added %d, total %d" % (len(old["entries"]), len(added), len(doc["entries"])))
    print("original %d identity records identical: %s" % (len(old_records), same))
    for e in added:
        print("ADDED %-22s %-12s %s" % (e["security_key"], e["ticker"], e["name"]))
    if not same:
        raise SystemExit("ERROR: the original identity records changed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
