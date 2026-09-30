"""AMGT_CORPUS round 19, CRPS-u-1 -- the scalar-exception readers, probed on the REAL committed field_map.json, plus the
served-block read the round-18 analysis ruling 1 asks for. Read-only (one S3 GET of the served Hitachi block); the issuer's file.

  line 1 -> 'u1 reader best_sales_6501 unit <CLASS> sign <CLASS> control_8035 unit <U> sign <S> module_in_toplevel <yes|no>'
  line 2 -> 'u1 served best_sales_6501 FY1 value <V> served_unit_class <CLASS> reader_unit_class <CLASS> agree <yes|no>'

<CLASS> is UNRESOLVED when the text starts 'UNRESOLVED', POINTER when it is the not-yet-built pointer, else MEASURED.
module_in_toplevel guards row Z-W1-S18: the module graded must be this tree's bytes, never the main workspace's.
"""
import importlib.util
import json
import os
import subprocess
import sys

TOP = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
SRC = os.path.join(TOP, "integrations", "bloomberg", "research", "model_block_pull.py")
SERVED_KEY = "derived/model_block/6501_JP_Equity/20260929T232834Z/model_block.json"
H, CTRL, M = "6501 JP Equity", "8035 JP Equity", "BEST_SALES"

spec = importlib.util.spec_from_file_location("mbp_u1", SRC)
mbp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mbp)
in_top = os.path.normcase(os.path.realpath(mbp.__file__)).startswith(os.path.normcase(os.path.realpath(TOP)))
in_top = in_top and os.path.normcase(os.path.realpath(str(mbp._FIELD_MAP_PATH))).startswith(
    os.path.normcase(os.path.realpath(TOP)))


def cls(text):
    t = str(text or "")
    if t.startswith("UNRESOLVED"):
        return "UNRESOLVED"
    if t.startswith("SEE field_map"):
        return "POINTER"
    return "MEASURED"


hu = mbp._resolved_unit(M, H)
hs = mbp._resolved_sign(M, H, 1.0)
cu = mbp._resolved_unit(M, CTRL)
cs = mbp._resolved_sign(M, CTRL, 1.0)
print("u1 reader best_sales_6501 unit %s sign %s control_8035 unit %s sign %s module_in_toplevel %s" % (
    cls(hu), cls(hs), cu, cs, "yes" if in_top else "no"))

import boto3  # noqa: E402 -- only the served read needs it

blk = json.loads(boto3.client("s3").get_object(Bucket=mbp.BUCKET, Key=SERVED_KEY)["Body"].read())
fy1 = [f for f in blk.get("figures", []) if f.get("mnemonic") == M and f.get("fiscal_period") == "FY1"]
if len(fy1) != 1:
    print("u1 served best_sales_6501 FY1 count %d (expected 1)" % len(fy1))
    sys.exit(3)
f = fy1[0]
print("u1 served best_sales_6501 FY1 value %s served_unit_class %s reader_unit_class %s agree %s" % (
    f.get("value"), cls(f.get("unit")), cls(hu), "yes" if cls(f.get("unit")) == cls(hu) else "no"))
