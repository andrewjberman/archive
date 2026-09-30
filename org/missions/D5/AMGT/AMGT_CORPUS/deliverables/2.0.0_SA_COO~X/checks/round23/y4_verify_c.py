"""AMGT_CORPUS round 23 y-4 leg c verify -- each re-derived block (newest stamp) against its predecessor, figure by figure, against
the per-block expectation in evidence/r23_y4_before.txt (its BLOCK lines). Read-only. The issuer's file.

  python y4_verify_c.py <pass_keys_file> <before_evidence>
  -> per mismatch 'MISMATCH <key> ...'; then
  -> 'y4c blocks N new_stamps S unit_changes U expected E blocks_matching M value_moves V other_changes O sign_outside_units G
      filled_by_sa F held_off H'
"""
import json
import re
import sys

import boto3

keys = open(sys.argv[1]).read().split()
expected = {}
for line in open(sys.argv[2], encoding="utf-8"):
    m = re.match(r"^BLOCK (\S+) same_raw \S+ filled_by_sa \S+ sa_figures \d+ unit_flips (\d+) ", line)
    if m:
        expected[m.group(1)] = int(m.group(2))
s3 = boto3.client("s3")
B = "opal-data-harvest"


def fkey(f):
    return (f.get("mnemonic"), f.get("scope"), f.get("fiscal_period"), f.get("fiscal_year"), f.get("period_end_date"),
            f.get("override"))


tot_u = tot_e = match = vm = oc = go = fb = ho = new = 0
for k in keys:
    stamps = sorted(o["Key"] for o in s3.list_objects_v2(Bucket=B, Prefix="derived/model_block/%s/" % k).get("Contents", [])
                    if o["Key"].endswith("model_block.json"))
    if len(stamps) < 2 or not stamps[-1].split("/")[-2].startswith("20260930T08"):
        print("MISMATCH %s no new stamp (newest %s)" % (k, stamps[-1].split("/")[-2] if stamps else None))
        continue
    new += 1
    old = json.loads(s3.get_object(Bucket=B, Key=stamps[-2])["Body"].read())
    cur = json.loads(s3.get_object(Bucket=B, Key=stamps[-1])["Body"].read())
    of = {fkey(f): f for f in old["figures"]}
    nf = {fkey(f): f for f in cur["figures"]}
    u = v = o = g = 0
    for kk in set(of) | set(nf):
        a, b = of.get(kk), nf.get(kk)
        if a is None or b is None:
            o += 1
            continue
        if json.dumps(a.get("value")) != json.dumps(b.get("value")):
            v += 1
        uc = a.get("unit") != b.get("unit")
        u += int(uc)
        if a.get("sign") != b.get("sign") and not uc:
            g += 1
        rest_a = {x: y for x, y in a.items() if x not in ("unit", "sign", "value")}
        rest_b = {x: y for x, y in b.items() if x not in ("unit", "sign", "value")}
        if json.dumps(rest_a, sort_keys=True, default=str) != json.dumps(rest_b, sort_keys=True, default=str):
            o += 1
    ff = cur.get("forecast_fallback") or {}
    fb += int(ff.get("filled_by_sa") or 0)
    ho += int(ff.get("classification") == "HELD_OFF")
    tot_u += u
    tot_e += expected.get(k, -1)
    vm += v
    oc += o
    go += g
    if u == expected.get(k) and v == 0 and o == 0 and g == 0:
        match += 1
    else:
        print("MISMATCH %s unit_changes %d expected %s value_moves %d other %d sign_outside %d" % (k, u, expected.get(k), v, o, g))
print("y4c blocks %d new_stamps %d unit_changes %d expected %d blocks_matching %d value_moves %d other_changes %d "
      "sign_outside_units %d filled_by_sa %d held_off %d" % (len(keys), new, tot_u, tot_e, match, vm, oc, go, fb, ho))
