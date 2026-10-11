"""AMGT_CORPUS round 44, CRPS-at-10 LEG P -- key-level companion to at10_legp_read.py. READ-ONLY.

  PYTHONPATH=. python at10_legp_keydiff.py <path to at10_legp_read.py> <pre snapshot.json>

at10_legp_read.py --post compares the whole `model` block (every key but team_sheet), so a per-request stamp such as
`model.generated_at` (scoped_amgt.py read_model) makes it print 0/3. This reads the three names again on the live function
and prints, per name, WHICH keys of `model` differ from the pre snapshot and their pre/post values.
"""
import importlib.util
import json
import sys

import boto3


def _load(path):
    spec = importlib.util.spec_from_file_location("legp", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    legp = _load(sys.argv[1])
    snap = json.load(open(sys.argv[2], encoding="utf-8"))
    lam = boto3.client("lambda", region_name="us-east-1")
    for key in legp.NAMES:
        blocks, _ = legp._served(lam, key)
        pre = snap["names"][key]["blocks"]["model_other_keys"]
        post = blocks["model_other_keys"]
        diff = [k for k in sorted(set(pre) | set(post))
                if legp._canon(pre.get(k, "<ABSENT>")) != legp._canon(post.get(k, "<ABSENT>"))]
        print("%s pre_keys %d post_keys %d differing %s" % (key, len(pre), len(post), diff))
        for k in diff:
            print("    %s PRE %s | POST %s" % (k, legp._canon(pre.get(k, "<ABSENT>"))[:120],
                                             legp._canon(post.get(k, "<ABSENT>"))[:120]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
