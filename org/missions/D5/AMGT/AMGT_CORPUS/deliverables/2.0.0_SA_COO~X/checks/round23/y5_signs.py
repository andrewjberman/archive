"""AMGT_CORPUS round 23, CRPS-y-5 -- the sign reader applied to every figure of the newest served block of the 97 y-4 names, with
the committed field_map.json, against each figure's OWN value. Read-only (S3 reads). The issuer's file.

  python y5_signs.py <pass_keys_file>
  -> 'y5 blocks N figures F sign_labelled L plain_disagree P convention_disagree C unresolved_kept U module_in_toplevel yes|no'
     plain_disagree: a POSITIVE/NEGATIVE/ZERO label that contradicts the figure's own value sign.
     convention_disagree: a '<SIGN> (<convention>)' label whose leading sign word contradicts the figure's own value sign.
"""
import importlib.util
import json
import os
import subprocess
import sys

import boto3

TOP = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
SRC = os.path.join(TOP, "integrations", "bloomberg", "research", "model_block_pull.py")
spec = importlib.util.spec_from_file_location("mbp_y5", SRC)
mbp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mbp)
in_top = os.path.normcase(os.path.realpath(mbp.__file__)).startswith(os.path.normcase(os.path.realpath(TOP)))


def own(v):
    try:
        v = float(v)
    except (TypeError, ValueError):
        return None
    return "POSITIVE" if v > 0 else ("NEGATIVE" if v < 0 else "ZERO")


keys = open(sys.argv[1]).read().split()
s3 = boto3.client("s3")
B = "opal-data-harvest"
figs = labelled = plain = conv = unres = 0
for k in keys:
    st = sorted(o["Key"] for o in s3.list_objects_v2(Bucket=B, Prefix="derived/model_block/%s/" % k).get("Contents", [])
                if o["Key"].endswith("model_block.json"))
    blk = json.loads(s3.get_object(Bucket=B, Key=st[-1])["Body"].read())
    sec = blk.get("security")
    for f in blk.get("figures", []):
        figs += 1
        lab = str(mbp._resolved_sign(f.get("mnemonic"), sec, f.get("value")))
        o = own(f.get("value"))
        if lab.startswith("UNRESOLVED"):
            unres += 1
            continue
        if o is None:
            continue
        head = lab.split(" ", 1)[0]
        if head not in ("POSITIVE", "NEGATIVE", "ZERO"):
            continue
        labelled += 1
        if lab in ("POSITIVE", "NEGATIVE", "ZERO"):
            plain += int(lab != o)
        else:
            conv += int(head != o)
print("y5 blocks %d figures %d sign_labelled %d plain_disagree %d convention_disagree %d unresolved_kept %d module_in_toplevel %s" % (
    len(keys), figs, labelled, plain, conv, unres, "yes" if in_top else "no"))
