"""ADVI_FIRMBKTS round 3: cut the readers' location list (FB-f-3, FB-f-4), issuer 2.0.0_SA_COO~B1.

Writes, with a fixed seed, the SAME location list into each reader's own project-free directory (--dir-a, --dir-b),
outside any checkout: ONLY LOCATIONS.json. The arm map and the truth for each canonical location are kept with the
issuer's checks (READING_KEY.json) and the list's sha256 beside it. Run once, at the cut.
"""
import argparse
import hashlib
import json
import os
import random
import subprocess
import sys

DELIV = "org/missions/D8/ADVI/ADVI_FIRMBKTS/deliverables"
OUT = DELIV + "/2.0.0_SA_COO~B1/round3"
SEED = 20261012


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir-a", required=True)
    ap.add_argument("--dir-b", required=True)
    a = ap.parse_args()
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
        d = r["dest"]
        key[i] = {"arm": arm, "class": r["prefix"], "bucket": r["bucket"],
                  "truth": {"system": d["source"], "firm": d["scope"], "tier": d["tier"], "table": d["table"]}}
    body = json.dumps({"locations": locs}, indent=1, ensure_ascii=True)
    for d in (a.dir_a, a.dir_b):
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "LOCATIONS.json"), "w", encoding="ascii", newline="\n") as fh:
            fh.write(body)
    sha = hashlib.sha256(body.encode("ascii")).hexdigest()
    os.makedirs(os.path.join(root, OUT), exist_ok=True)
    with open(os.path.join(root, OUT, "READING_KEY.json"), "w", encoding="ascii", newline="\n") as fh:
        json.dump(key, fh, indent=1, ensure_ascii=True)
    with open(os.path.join(root, OUT, "LOCATIONS.sha256"), "w", encoding="ascii", newline="\n") as fh:
        fh.write(sha + "\n")
    n_c = sum(1 for v in key.values() if v["arm"] == "canonical")
    print("OK: %d locations (%d canonical, %d legacy); sha256 %s; dirs %s %s" % (len(locs), n_c, len(locs) - n_c, sha,
                                                                              a.dir_a, a.dir_b))


if __name__ == "__main__":
    sys.exit(main())
