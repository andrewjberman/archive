"""AMGT_CORPUS round 25 aa-2 served act, leg c verify -- each re-derived block (its newest stamp) against the predecessor recorded
before the act, figure by figure, against the per-block expectation in the m3 evidence (its BLOCK lines: unit, sign, currency).
The derive's `vintage` stamp moves on every derive by construction; it is excluded from the content compare and counted. Read-only.
The issuer's file; run as a named script with python -u.

  python c25_verify.py <predecessors_file> <m3_evidence>
  -> per mismatch 'MISMATCH <key> ...'; then
  -> 'c25 blocks N new_stamps S unit U/EU sign G/EG currency C/EC blocks_matching M value_moves V case_changes K other_changes O
      measured_to_other X label_moves_outside_header H sign_contradicts_value Z filled_by_sa F vintage_only_figures VT'
"""
import json
import re
import sys

import boto3

pred = dict(line.split() for line in open(sys.argv[1], encoding="utf-8") if line.strip())
expected = {}
for line in open(sys.argv[2], encoding="utf-8"):
    m = re.match(r"^BLOCK (\S+) unit (\d+) sign (\d+) currency (\d+) basis_only (\d+) ", line)
    if m:
        expected[m.group(1)] = tuple(int(x) for x in m.groups()[1:])
s3 = boto3.client("s3")
B = "opal-data-harvest"


def fkey(f):
    return (f.get("mnemonic"), f.get("scope"), f.get("fiscal_period"), f.get("fiscal_year"), f.get("period_end_date"),
            f.get("override"))


def strip_vintage(x):
    if isinstance(x, dict):
        return {q: strip_vintage(w) for q, w in x.items() if q != "vintage"}
    if isinstance(x, list):
        return [strip_vintage(w) for w in x]
    return x


def measured(u):
    u = str(u or "")
    return bool(u) and not u.startswith("UNRESOLVED") and not u.startswith("SEE field_map")


def contradicts(label, value):
    try:
        v = float(value)
    except (TypeError, ValueError):
        return False
    own = "POSITIVE" if v > 0 else ("NEGATIVE" if v < 0 else "ZERO")
    head = str(label).split(" ", 1)[0]
    return head in ("POSITIVE", "NEGATIVE", "ZERO") and head != own


LABEL = ("currency", "currency_basis")
T = dict(new=0, U=0, EU=0, G=0, EG=0, C=0, EC=0, match=0, V=0, K=0, O=0, X=0, H=0, Z=0, F=0, VT=0)
for k in sorted(pred):
    st = []
    for pg in s3.get_paginator("list_objects_v2").paginate(Bucket=B, Prefix="derived/model_block/%s/" % k):
        st += [o["Key"] for o in pg.get("Contents", []) if o["Key"].endswith("/model_block.json")]
    st.sort()
    if st[-1] <= pred[k]:
        print("MISMATCH %s no new stamp (newest %s)" % (k, st[-1].split("/")[-2]))
        continue
    T["new"] += 1
    old = json.loads(s3.get_object(Bucket=B, Key=pred[k])["Body"].read())
    cur = json.loads(s3.get_object(Bucket=B, Key=st[-1])["Body"].read())
    of = {fkey(f): f for f in old["figures"]}
    nf = {fkey(f): f for f in cur["figures"]}
    u = g = c = v = o = x = h = z = 0
    for kk in set(of) | set(nf):
        a, b = of.get(kk), nf.get(kk)
        if a is None or b is None:
            o += 1
            continue
        v += int(json.dumps(a.get("value")) != json.dumps(b.get("value")))
        if a.get("unit") != b.get("unit"):
            u += 1
            x += int(measured(a.get("unit")))
        g += int(a.get("sign") != b.get("sign"))
        z += int(contradicts(b.get("sign"), b.get("value")))
        if any(a.get(q) != b.get(q) for q in LABEL):
            c += int(a.get("currency") != b.get("currency"))
            h += int(b.get("scope") != "header")
        T["VT"] += int(a.get("vintage") != b.get("vintage"))
        skip = ("unit", "sign", "value", "vintage") + LABEL
        ra = {q: w for q, w in a.items() if q not in skip}
        rb = {q: w for q, w in b.items() if q not in skip}
        o += int(json.dumps(ra, sort_keys=True, default=str) != json.dumps(rb, sort_keys=True, default=str))
    kc = int(json.dumps(strip_vintage(old.get("cases")), sort_keys=True, default=str)
             != json.dumps(strip_vintage(cur.get("cases")), sort_keys=True, default=str))
    ta = {q: w for q, w in old.items() if q not in ("figures", "cases")}
    tb = {q: w for q, w in cur.items() if q not in ("figures", "cases")}
    o += int(json.dumps(ta, sort_keys=True, default=str) != json.dumps(tb, sort_keys=True, default=str))
    T["F"] += int((cur.get("forecast_fallback") or {}).get("filled_by_sa") or 0)
    eu, eg, ec, _eb = expected.get(k, (-1, -1, -1, -1))
    for kk, vv in (("U", u), ("EU", eu), ("G", g), ("EG", eg), ("C", c), ("EC", ec), ("V", v), ("K", kc), ("O", o),
                   ("X", x), ("H", h), ("Z", z)):
        T[kk] += vv
    if (u, g, c) == (eu, eg, ec) and v == kc == o == x == h == z == 0:
        T["match"] += 1
    else:
        print("MISMATCH %s unit %d/%d sign %d/%d currency %d/%d value %d case %d other %d measured_to_other %d "
              "outside_header %d contradicts %d" % (k, u, eu, g, eg, c, ec, v, kc, o, x, h, z))
print("c25 blocks %d new_stamps %d unit %d/%d sign %d/%d currency %d/%d blocks_matching %d value_moves %d case_changes %d "
      "other_changes %d measured_to_other %d label_moves_outside_header %d sign_contradicts_value %d filled_by_sa %d "
      "vintage_only_figures %d" % (len(pred), T["new"], T["U"], T["EU"], T["G"], T["EG"], T["C"], T["EC"], T["match"], T["V"],
                                   T["K"], T["O"], T["X"], T["H"], T["Z"], T["F"], T["VT"]))
