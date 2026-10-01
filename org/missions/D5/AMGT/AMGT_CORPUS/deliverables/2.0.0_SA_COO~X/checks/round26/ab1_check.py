"""AMGT_CORPUS round 26, CRPS-ab-1 (row Z-S71) -- which model block the DOSSIER's own reader resolves for the slash-bearing names, and
a slash-free control that must be byte-unchanged. Read-only (S3 reads through the producer's own `dossier.current_inputs`). The
issuer's file.

  -> 'ab1 bp_reads raw|encoded bp_newest True|False ng_reads raw|encoded ng_newest True|False control_unchanged True|False'
"""
import hashlib
import json
import os
import re
import subprocess

import boto3

from lib.research.corpus import dossier

TOP = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
HERE = os.path.dirname(os.path.abspath(__file__))
B = "opal-data-harvest"
s3 = boto3.client("s3")


def refs(key):
    s = json.dumps(dossier.current_inputs(key, client=s3), sort_keys=True, default=str)
    return s, sorted(set(re.findall(r"derived/model_block/[^\"]*model_block\.json", s)))


def newest_encoded(enc):
    st = sorted(o["Key"] for o in s3.list_objects_v2(Bucket=B, Prefix="derived/model_block/%s/" % enc).get("Contents", [])
                if o["Key"].endswith("/model_block.json"))
    return st[-1] if st else None


out = []
for ident, enc in (("BP/_LN_Equity", "BP-SLASH-_LN_Equity"), ("NG/_LN_Equity", "NG-SLASH-_LN_Equity")):
    _, r = refs(ident)
    form = "encoded" if r and all("-SLASH-" in x for x in r) else ("raw" if r else "none")
    out.append((form, newest_encoded(enc) in r))
control_json, _ = refs("TSM_US_Equity")
base = open(os.path.join(HERE, "ab1_control_base.sha256")).read().strip()
same = hashlib.sha256(control_json.encode("utf-8")).hexdigest() == base
print("ab1 bp_reads %s bp_newest %s ng_reads %s ng_newest %s control_unchanged %s" % (out[0][0], out[0][1], out[1][0], out[1][1],
                                                                                     same))
