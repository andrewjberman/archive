"""WP8-DECOM D3 -- 13c verify stage == the V2-5 certificate evidence (deliverable section 3).

Tiers (never loosened silently):
  1. KEYS   -- fresh ListObjectsV2 both sides; every source logical key present monolith-side; only-legacy = 0
  2. SIZE   -- size-tie on all source objects
  3. CONTENT-- ETag-exact where shapes match; multipart/shape-diff class -> sampled true-MD5
               (sample >= 10; positive control run as a SEPARATE invocation: --positive-control)
  4. LOGICAL-- (type,date) coverage: monolith is a SUPERSET of 01_raw; the 988-pair gap reads 0
  5. RPS    -- each bronze/ (rps mirror) object is a member of the 01_raw content set
               (ETag-exact, or size-tie recorded for the shape class)

Denominators re-listed AT RUN TIME. Exit nonzero on ANY tier failing.
"""
from __future__ import annotations
import boto3
import hashlib
import json
import random
import re
import sys
import time

SRC_BUCKET = "opal-data-schwab"
SRC_PREFIX = "01_raw/"
RPS_PREFIX = "bronze/"
DST_BUCKET = "opal-data-assets"
DST_PREFIX = "schwab/08242234/bronze/"
PAT = re.compile(r"^CRS(\d{8})\.([A-Z]+)$")
OUT = r"C:\Users\ANDREW~1\AppData\Local\Temp\claude\C--Users-AndrewBerman-Desktop-ajb-workspace\5ca35ef2-959d-442a-bbc3-775c7151f581\scratchpad\wp8_d3_verify_13c_result.json"

s3 = boto3.client("s3")
random.seed(20260717)  # reproducible sample; seeded, not hand-chosen

def listing(bucket: str, prefix: str) -> dict[str, tuple[str, int]]:
    out: dict[str, tuple[str, int]] = {}
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix=prefix):
        for o in page.get("Contents", []):
            out[o["Key"][len(prefix):]] = (o["ETag"].strip('"'), o["Size"])
    return out

def true_md5(bucket: str, key: str) -> str:
    h = hashlib.md5()
    body = s3.get_object(Bucket=bucket, Key=key)["Body"]
    for chunk in iter(lambda: body.read(1 << 22), b""):
        h.update(chunk)
    return h.hexdigest()

if "--positive-control" in sys.argv:
    # SEPARATE invocation: pick one ETag-exact tied pair, prove the instrument reads MATCH on a
    # known-identical pair and MISMATCH on a known-different pair (mutant leg).
    src = listing(SRC_BUCKET, SRC_PREFIX)
    dst = listing(DST_BUCKET, DST_PREFIX)
    pair = None
    for k, (etag, size) in sorted(src.items()):
        m = PAT.match(k)
        if not m:
            continue
        rel = f"{m.group(2).lower()}/{m.group(1)}/{k}"
        if rel in dst and dst[rel][0] == etag and "-" not in etag and size < 50_000_000:
            pair = (k, rel)
            break
    if pair is None:
        print("POSITIVE CONTROL: no ETag-exact pair available")
        sys.exit(5)
    a = true_md5(SRC_BUCKET, SRC_PREFIX + pair[0])
    b = true_md5(DST_BUCKET, DST_PREFIX + pair[1])
    print(f"POSITIVE CONTROL pair {pair[0]} -> {pair[1]}: src_md5={a} dst_md5={b} match={a == b}")
    # mutant leg: a DIFFERENT source object must NOT tie the same dst md5
    other = next(k for k in sorted(src) if PAT.match(k) and k != pair[0] and src[k][1] != src[pair[0]][1])
    c = true_md5(SRC_BUCKET, SRC_PREFIX + other)
    print(f"MUTANT: different object {other}: md5={c} ties_dst={c == b} (must be False)")
    sys.exit(0 if (a == b and c != b) else 5)

t0 = time.time()
src = listing(SRC_BUCKET, SRC_PREFIX)
dst = listing(DST_BUCKET, DST_PREFIX)
rps = listing(SRC_BUCKET, RPS_PREFIX)
print(f"RUN-TIME DENOMINATORS: 01_raw {len(src)} / monolith-0824-bronze {len(dst)} / rps-mirror {len(rps)}")

unparsed = [k for k in src if not PAT.match(k)]
if unparsed:
    print(f"FAIL tier1: {len(unparsed)} unparsable source keys")
    sys.exit(2)

# Tier 1+2+3 classification
missing, size_mismatch, etag_exact, shape_class = [], [], [], []
for k, (etag, size) in sorted(src.items()):
    m = PAT.match(k)
    rel = f"{m.group(2).lower()}/{m.group(1)}/{k}"
    if rel not in dst:
        missing.append(rel)
        continue
    detag, dsize = dst[rel]
    if dsize != size:
        size_mismatch.append((rel, size, dsize))
    elif detag == etag:
        etag_exact.append((k, rel))
    else:
        shape_class.append((k, rel, size))

print(f"TIER 1 KEYS: only-legacy(missing) = {len(missing)}  [PASS requires 0]")
print(f"TIER 2 SIZE: mismatches = {len(size_mismatch)}      [PASS requires 0]")
print(f"TIER 3 CONTENT: ETag-exact {len(etag_exact)} / shape-class(sampled-MD5) {len(shape_class)}")
if missing:
    print("  missing sample:", missing[:5])
if size_mismatch:
    print("  size-mismatch sample:", size_mismatch[:5])

# Tier 3 sampled true-MD5 over the shape class (sample >= 10, size-capped for wall-clock sanity)
md5_results = []
if shape_class:
    small = [x for x in shape_class if x[2] < 200_000_000] or shape_class
    sample = random.sample(small, min(max(10, len(small) // 500), len(small)))
    print(f"TIER 3 sampling {len(sample)} of shape-class {len(shape_class)} (denominator printed)")
    for k, rel, size in sample:
        a = true_md5(SRC_BUCKET, SRC_PREFIX + k)
        b = true_md5(DST_BUCKET, DST_PREFIX + rel)
        md5_results.append((rel, a == b))
        print(f"  {rel}: {'MATCH' if a == b else 'MISMATCH ' + a + ' vs ' + b}")
md5_fail = [r for r, ok in md5_results if not ok]

# Tier 4 logical superset
def pairs(keys, parse):
    out = set()
    for k in keys:
        p = parse(k)
        if p:
            out.add(p)
    return out
src_pairs = pairs(src, lambda k: (PAT.match(k).group(2).lower(), PAT.match(k).group(1)) if PAT.match(k) else None)
DSTPAT = re.compile(r"^([a-z]+)/(\d{8})/")
dst_pairs = pairs(dst, lambda k: (m.group(1), m.group(2)) if (m := DSTPAT.match(k)) else None)
gap = src_pairs - dst_pairs
print(f"TIER 4 LOGICAL: src pairs {len(src_pairs)} / monolith pairs {len(dst_pairs)} / GAP {len(gap)}  [PASS requires 0]")
if gap:
    print("  gap sample:", sorted(gap)[:10])

# Tier 5 rps-mirror membership
src_etags = {etag for etag, _ in src.values()}
src_sizes = {}
for etag, size in src.values():
    src_sizes.setdefault(size, 0)
    src_sizes[size] += 1
rps_member, rps_size_only, rps_orphan = 0, [], []
for k, (etag, size) in rps.items():
    if etag in src_etags:
        rps_member += 1
    elif size in src_sizes:
        rps_size_only.append(k)
    else:
        rps_orphan.append(k)
print(f"TIER 5 RPS-MIRROR: {len(rps)} objects -- ETag-member {rps_member} / size-tie-only {len(rps_size_only)} / NO-TIE {len(rps_orphan)}")
if rps_orphan:
    print("  no-tie sample:", rps_orphan[:5])

verdict = (not missing and not size_mismatch and not md5_fail and not gap and not rps_orphan)
result = {
    "run_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "denominators": {"src": len(src), "dst": len(dst), "rps": len(rps)},
    "tier1_missing": len(missing), "tier2_size_mismatch": len(size_mismatch),
    "tier3_etag_exact": len(etag_exact), "tier3_shape_class": len(shape_class),
    "tier3_md5_sampled": len(md5_results), "tier3_md5_fail": len(md5_fail),
    "tier4_gap": sorted(gap) if gap else [],
    "tier5_member": rps_member, "tier5_size_only": len(rps_size_only), "tier5_no_tie": rps_orphan,
    "VERDICT": "PASS" if verdict else "FAIL",
}
with open(OUT, "w") as fh:
    json.dump(result, fh, indent=1)
print(f"13c VERDICT: {result['VERDICT']}  wall {time.time()-t0:.0f}s  result -> {OUT}")
sys.exit(0 if verdict else 1)
