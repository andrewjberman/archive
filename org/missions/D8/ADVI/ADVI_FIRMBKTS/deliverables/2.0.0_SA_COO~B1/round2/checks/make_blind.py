"""ADVI_FIRMBKTS round 2: cut the readers' location list (FB-e-2, FB-e-3), issuer 2.0.0_SA_COO~B1.

Reads the round-1 table (mapping.json) and writes, with a fixed seed:
  <blind>/LOCATIONS.json   {"locations": [{"id", "location"}]}  -- the ONLY input the two readers are given
  <key>/READING_KEY.json   {"id": {"arm", "class", "bucket"}}  -- the arm map, kept with the issuer's checks
Each placed class (MOVE or HOME) contributes its canonical address and its legacy s3://bucket/sample_key.
Ids are 8 hex characters, new for this round (never the round-1 ids). Run once, at the cut.
"""
import json
import os
import random
import subprocess
import sys

DELIV = "org/missions/D8/ADVI/ADVI_FIRMBKTS/deliverables"
BLIND = "org/tier1_exec/2.0.0_SA_COO~B1/round2/blind"
KEY = DELIV + "/2.0.0_SA_COO~B1/round2/READING_KEY.json"
SEED = 20261011


def main():
    root = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    with open(os.path.join(root, DELIV, "mapping.json"), encoding="utf-8") as fh:
        rows = json.load(fh)["rows"]
    with open(os.path.join(root, DELIV, "census.json"), encoding="utf-8") as fh:
        census = json.load(fh)
    sample = {(b, c["prefix"]): c["sample_key"] for b, bd in census["buckets"].items() for c in bd["classes"]}
    rng = random.Random(SEED)
    items = []
    for r in rows:
        if r.get("disposition") not in ("MOVE", "HOME"):
            continue
        items.append(("canonical", r["address"], r))
        items.append(("legacy", "s3://%s/%s" % (r["bucket"], sample[(r["bucket"], r["prefix"])]), r))
    rng.shuffle(items)
    used, locs, key = set(), [], {}
    for arm, location, r in items:
        while True:
            i = "%08x" % rng.getrandbits(32)
            if i not in used and "opal" not in i:
                used.add(i)
                break
        locs.append({"id": i, "location": location})
        key[i] = {"arm": arm, "class": r["prefix"], "bucket": r["bucket"]}
    os.makedirs(os.path.join(root, BLIND), exist_ok=True)
    with open(os.path.join(root, BLIND, "LOCATIONS.json"), "w", encoding="ascii", newline="\n") as fh:
        json.dump({"locations": locs}, fh, indent=1, ensure_ascii=True)
    with open(os.path.join(root, KEY), "w", encoding="ascii", newline="\n") as fh:
        json.dump(key, fh, indent=1, ensure_ascii=True)
    n_c = sum(1 for v in key.values() if v["arm"] == "canonical")
    print("OK: %d locations (%d canonical, %d legacy) -> %s; key -> %s" % (len(locs), n_c, len(locs) - n_c, BLIND, KEY))


if __name__ == "__main__":
    sys.exit(main())
