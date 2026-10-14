"""plant_gen14.py -- the ISSUER's reference implementation of the gen_silver_rows.py interface, used ONLY to plant the PASS arm of
c14.AC1-AC3 and the loader checks at the cut (standing battery clause 1). Not given to the worker; writes nothing under the repo.

  python plant_gen14.py --g2 F --g5 F --g6 F --out DIR --deployed-tools FILE
"""
import argparse
import json
import os
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import glib  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--g2", required=True)
    ap.add_argument("--g4", required=True)
    ap.add_argument("--g5", required=True)
    ap.add_argument("--g6", required=True)
    ap.add_argument("--g2f", default=None)   # accepted for interface parity; glib loads the pinned G2f itself
    ap.add_argument("--out", required=True)
    ap.add_argument("--deployed-tools", required=True)
    ap.add_argument("--fork-registry-out", default=None)
    a = ap.parse_args()
    deployed = set(json.load(open(a.deployed_tools, encoding="utf-8")))
    os.makedirs(a.out, exist_ok=True)
    n = 0
    reg = {}
    for path in (a.g2, a.g4, a.g5, a.g6):
        for c in glib.parse(open(path, encoding="utf-8").read()):
            if not glib.in_scope(c):
                continue
            row, entry = glib.expected_row(c, "G2", deployed)
            reg[row["contract"]["id"]] = entry
            with open(os.path.join(a.out, glib.entity(c["contract_id"]) + ".yaml"), "w", encoding="utf-8", newline="\n") as f:
                yaml.safe_dump(row, f, sort_keys=False, allow_unicode=True)
            n += 1
    if a.fork_registry_out:
        with open(a.fork_registry_out, "w", encoding="utf-8", newline="\n") as f:
            json.dump({"_about": "planted", "rows": reg}, f, indent=1)
    print("wrote %d rows to %s" % (n, a.out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
