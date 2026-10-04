"""AMGT_CORPUS round 34, CRPS-aj-2 leg v -- the after-state of the on-demand fire. Read-only (S3 list/get; the served API's
own block reader). The issuer's file.

  v1 newest-stamp census: of the REGISTERED names (the producer's own `_registered_security_keys`), how many have a newest
     derived block stamped on RUN_DAY (UTC). Names not at RUN_DAY are listed.
  v2 the 52-field census over those newest blocks: per new mnemonic, figures / unresolved / absent, the top unresolved reason,
     and the count of figures whose unit is the pointer text ("SEE field_map.json").
  v3 the served read for BA, GOOGL and BP/ LN through `lib.research.api.scoped_amgt.read_model_block` (the API's own reader):
     the block it returns carries a figure vintage on RUN_DAY.
  Usage: python v34.py <RUN_DAY YYYYMMDD>
"""
import collections
import importlib.util
import json
import os
import subprocess
import sys

TOP = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
RES = os.path.join(TOP, "integrations", "bloomberg", "research")
for p in (TOP, RES):
    if p not in sys.path:
        sys.path.insert(0, p)
spec = importlib.util.spec_from_file_location("mbp_v34", os.path.join(RES, "model_block_pull.py"))
mbp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mbp)
from lib.research.identity import crosswalk  # noqa: E402

RUN_DAY = sys.argv[1]
NEW = list(mbp.HEADER_FIELDS[18:]) + list(mbp.HIST_FIELDS[39:]) + list(mbp.FORECAST_FIELDS[11:])
assert len(NEW) == 52, len(NEW)

s3 = mbp._s3()
registered = mbp._registered_security_keys()
def _latest_blocks(client):
    """{store segment: (newest stamp, key)} over every derived model_block.json (one paginated list)."""
    prefix = "derived/%s/" % mbp.ENGINE
    found = {}
    token = None
    while True:
        kwargs = {"Bucket": mbp.BUCKET, "Prefix": prefix}
        if token:
            kwargs["ContinuationToken"] = token
        page = client.list_objects_v2(**kwargs)
        for item in page.get("Contents", []):
            key = item["Key"]
            if not key.endswith("/model_block.json"):
                continue
            seg, stamp, _ = key[len(prefix):].rsplit("/", 2)
            if seg not in found or stamp > found[seg][0]:
                found[seg] = (stamp, key)
        if not page.get("IsTruncated"):
            return found
        token = page.get("NextContinuationToken")


latest = _latest_blocks(s3)

at_day, not_day = [], []
blocks = {}
for sk in registered:
    seg = crosswalk.slash_safe_key(sk)
    hit = latest.get(seg) or latest.get(sk)
    if not hit:
        not_day.append((sk, "NO BLOCK"))
        continue
    stamp, key = hit
    if stamp.startswith(RUN_DAY):
        at_day.append(sk)
        body = json.loads(s3.get_object(Bucket=mbp.BUCKET, Key=key)["Body"].read())
        blocks[sk] = body.get("model_block", body)
    else:
        not_day.append((sk, stamp))
print("v1 registered %d newest_at_%s %d not_at_day %d" % (len(registered), RUN_DAY, len(at_day), len(not_day)))
for sk, why in not_day:
    print("   NOT-AT-DAY %s %s" % (sk, why))

fig_n = collections.Counter()
unres_n = collections.Counter()
reasons = collections.defaultdict(collections.Counter)
pointer = 0
for block in blocks.values():
    present = set()
    for f in block.get("figures", []):
        m = f.get("mnemonic")
        if m in NEW:
            fig_n[m] += 1
            present.add(m)
            if str(f.get("unit", "")).startswith("SEE field_map.json"):
                pointer += 1
    for u in block.get("unresolved", []):
        m = u.get("mnemonic")
        if m in NEW:
            unres_n[m] += 1
            reasons[m][str(u.get("reason"))[:90]] += 1
print("v2 blocks %d new_mnemonics %d figures %d unresolved %d pointer_unit_figures %d"
      % (len(blocks), len(NEW), sum(fig_n.values()), sum(unres_n.values()), pointer))
for m in NEW:
    top = reasons[m].most_common(1)
    print("   %-34s figures %4d unresolved %4d %s" % (m, fig_n[m], unres_n[m], ("top: " + top[0][0]) if top else ""))

from lib.research.api import scoped_amgt  # noqa: E402
for sk in ("BA_US_Equity", "GOOGL_US_Equity", "BP/_LN_Equity"):
    try:
        mb = scoped_amgt.read_model_block(sk)
    except Exception as exc:  # noqa: BLE001
        print("v3 %s READ-FAILED %s: %s" % (sk, type(exc).__name__, exc))
        continue
    doc = mb.get("model_block", mb) if isinstance(mb, dict) else {}
    vint = sorted({str(f.get("vintage", ""))[:10] for f in doc.get("figures", [])})
    print("v3 %s figures %d vintages %s" % (sk, len(doc.get("figures", [])), vint[-3:]))
