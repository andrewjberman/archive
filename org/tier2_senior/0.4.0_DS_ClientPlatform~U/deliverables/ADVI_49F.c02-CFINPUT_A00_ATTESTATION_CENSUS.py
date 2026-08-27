"""How many of the ruled 531 backfill dates would ABORT at stage a00?

a00_runner.attested_count() REFUSES unless some meta/conversions record attests fact_acc for
the date -- "the tie guard has no denominator". The local full-chain QA run for 2026-03-24 hit
exactly that and aborted at stage 1 of 15, before c00 ever ran.

If the attested set is small, the ruled FULL-CHAIN backfill (P14-VEHICLE) does not merely run
slowly over history -- it REFUSES on most of it, at the first stage. That is a different failure
from the ones already banked (the D-1 pull, the absent A/B inputs), because it fires BEFORE any
of them and it fires LOUD rather than producing wrong output.

Read-only: lists and reads the converter's own records; writes nothing.
"""
import json
import sys

sys.path.insert(0, "data/assets/scripts/gold/runners_49f")
import runner_common as rc  # noqa: E402

CONV_PREFIX = f"{rc.SCOPE}/meta/conversions/"
s3 = rc.s3()
pag = s3.get_paginator("list_objects_v2")
keys = [o["Key"] for page in pag.paginate(Bucket=rc.BUCKET, Prefix=CONV_PREFIX)
        for o in page.get("Contents", [])]
print(f"conversion records scanned: {len(keys)}  (a00 reported 456 for its own run)")

attested, converted_other, seen_partitions = set(), 0, set()
for k in keys:
    try:
        rec = json.loads(s3.get_object(Bucket=rc.BUCKET, Key=k)["Body"].read())
    except Exception as exc:
        print(f"  UNREADABLE {k}: {type(exc).__name__}")
        continue
    parts = rec.get("partitions", []) or []
    seen_partitions.update(str(p) for p in parts)
    per = rec.get("per_type", {}).get("fact_acc")
    if not per:
        continue
    if per.get("action") == "converted":
        for p in parts:
            attested.add(str(p))
    else:
        converted_other += 1

trn_dates = rc.list_partition_dates(f"{rc.SILVER}/fact_trn")
led_dates = rc.list_partition_dates(f"{rc.OUT_ROOT}/canonical/flow_ledger")
print(f"\nfact_acc ATTESTED dates (a00 will proceed) : {len(attested)}")
if attested:
    a = sorted(attested)
    print(f"  range {a[0]} .. {a[-1]}")
    print(f"  sample: {a[:6]}{' ...' if len(a) > 6 else ''}")
print(f"records naming fact_acc with action != converted: {converted_other}")
print(f"distinct partitions named across ALL records     : {len(seen_partitions)}")

print("\nTHE DENOMINATOR THAT MATTERS FOR P14-VEHICLE:")
print(f"  flow_ledger partitions (the backfill set)   : {len(led_dates)}")
covered = sum(1 for d in led_dates if d in attested)
print(f"  of those, fact_acc-ATTESTED (a00 proceeds)  : {covered}")
print(f"  of those, NOT attested (a00 REFUSES at      : {len(led_dates) - covered}")
print("    stage 1 of 15, before c00 runs)")
print(f"  fact_trn partitions                         : {len(trn_dates)}")
print("\nA REFUSAL IS NOT A WRONG NUMBER -- this guard fails LOUD and by design. The finding is")
print("about the ruled backfill's REACH, not about the guard being wrong.")
