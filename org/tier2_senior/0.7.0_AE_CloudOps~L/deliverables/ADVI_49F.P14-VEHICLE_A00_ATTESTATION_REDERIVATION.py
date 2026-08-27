"""INDEPENDENT re-derivation of the a00 attestation split for ADVI_49F.P14-VEHICLE.

METHOD INDEPENDENCE, stated because it is the whole point (CLAUDE.md Rule 22: a second seat's
confirmation via the FIRST seat's method is REPETITION, not corroboration):
  - I did NOT run 0.4.0_DS_ClientPlatform~U's committed enumeration script.
  - The predicate below is transcribed by ME from a00_runner.py:83-100 at source, not from ~U's
    description of it.
  - Counting, pagination and denominators are my own.
The SUBSTRATE is necessarily the same S3 (it is the very thing a00 reads at run time); independence
here is of METHOD, and I state that limit rather than claiming more.

a00 has TWO refusal gates and they are different questions -- main() checks partition existence
FIRST (:114-116), then attestation (:118). Both are enumerated separately below.
"""
import json
import boto3

SILVER_BUCKET = "opal-data-assets"
GOLD_BUCKET = "opal-data-49financial"
SCOPE = "schwab/08335338"
ACC_PREFIX = f"{SCOPE}/silver/fact_acc/"
CONV_PREFIX = f"{SCOPE}/meta/conversions/"
FLOW_PREFIX = "gold/advi/canonical/flow_ledger/"

s3 = boto3.client("s3")


def list_partition_dates(bucket, prefix):
    """date= partition dirs under a prefix. Paginated (never --no-paginate / page-1 reasoning)."""
    dates = set()
    pag = s3.get_paginator("list_objects_v2")
    for page in pag.paginate(Bucket=bucket, Prefix=prefix, Delimiter="/"):
        for cp in page.get("CommonPrefixes", []):
            part = cp["Prefix"].rstrip("/").rsplit("/", 1)[-1]
            if part.startswith("date="):
                dates.add(part[5:])
    return dates


def attested_dates():
    """a00_runner.py:83-100 predicate, transcribed from source by this seat:
       some conversion record with per_type.fact_acc.action == 'converted'
       AND the date present in that record's 'partitions' list."""
    pag = s3.get_paginator("list_objects_v2")
    keys = [o["Key"] for page in pag.paginate(Bucket=SILVER_BUCKET, Prefix=CONV_PREFIX)
            for o in page.get("Contents", [])]
    attested = {}
    malformed = 0
    for k in keys:
        try:
            rec = json.loads(s3.get_object(Bucket=SILVER_BUCKET, Key=k)["Body"].read())
        except Exception:
            malformed += 1
            continue
        per = (rec.get("per_type") or {}).get("fact_acc")
        if not per or per.get("action") != "converted":
            continue
        for d in rec.get("partitions", []) or []:
            attested.setdefault(d, set()).add(int(per["t1_expected"]))
    return keys, attested, malformed


print("=" * 78)
print("INDEPENDENT RE-DERIVATION -- a00 attestation vs the backfill set")
print("=" * 78)

keys, attested, malformed = attested_dates()
print(f"conversion records SCANNED : {len(keys)}   (malformed/unreadable: {malformed})")
print(f"fact_acc-ATTESTED dates    : {len(attested)}")
if attested:
    ad = sorted(attested)
    print(f"  attested range           : {ad[0]} .. {ad[-1]}")

conflicting = {d: v for d, v in attested.items() if len(v) > 1}
print(f"  of those, CONFLICTING     : {len(conflicting)}  "
      f"(a00 REFUSES these too, :98 -- a second refusal mode)")

acc = list_partition_dates(SILVER_BUCKET, ACC_PREFIX)
flow = list_partition_dates(GOLD_BUCKET, FLOW_PREFIX)
print()
print(f"fact_acc partitions (gate 1 subject) : {len(acc)}")
print(f"flow_ledger partitions (BACKFILL SET): {len(flow)}")

att = set(attested)
proceed = flow & att
refuse_attest = flow - att
print()
print("=" * 78)
print("THE SPLIT, denominator beside every number")
print("=" * 78)
D = len(flow)
print(f"  backfill set (denominator)                       : {D}")
print(f"  a00 PROCEEDS (attested)                          : {len(proceed)}  "
      f"({100.0*len(proceed)/D:.2f}% of {D})")
print(f"  a00 REFUSES  (not attested)                      : {len(refuse_attest)}  "
      f"({100.0*len(refuse_attest)/D:.2f}% of {D})")
print(f"  cross-check proceeds+refuses == denominator      : "
      f"{len(proceed)+len(refuse_attest)} == {D} -> "
      f"{'OK' if len(proceed)+len(refuse_attest)==D else 'MISMATCH'}")
print()
print(f"  ALSO gate 1 (fact_acc partition missing entirely): "
      f"{len(flow - acc)} of {D} backfill dates have NO fact_acc partition")
print(f"  attested dates NOT in the backfill set            : {len(att - flow)} of {len(att)}")

print()
print("=" * 78)
print("CONTROLS -- both arms, on my own enumeration")
print("=" * 78)
POS = ["2026-08-24", "2026-08-25", "2026-08-26"]
NEG = ["2026-03-24", "2026-01-15", "2025-06-10"]
print("  POSITIVE (dates the chain demonstrably ran on -- must be ATTESTED):")
for d in POS:
    print(f"    {d}  attested={d in att}   in_backfill_set={d in flow}")
print("  NEGATIVE (the exercised abort + two others -- must be NOT attested):")
for d in NEG:
    print(f"    {d}  attested={d in att}   in_backfill_set={d in flow}")

pos_ok = all(d in att for d in POS)
neg_ok = all(d not in att for d in NEG)
print()
print(f"  positive control: {'FIRED (all attested)' if pos_ok else '*** FAILED ***'}")
print(f"  negative control: {'FIRED (none attested)' if neg_ok else '*** FAILED ***'}")
if not (pos_ok and neg_ok):
    print("  -> a control failed; the split above is NOT trustworthy. Do not quote it.")

# ---------------------------------------------------------------------------
# COVERAGE CHECK vs CTO 76379's ruled two-mode design.
# The mode REFUSES any date >= the attestation epoch, so any in-set date that is
# at-or-after the epoch AND unattested would refuse under BOTH the guard and the
# mode -- un-runnable either way. That set must be empty for the ruling to cover
# the backfill set. Measured, not assumed.
# ---------------------------------------------------------------------------
epoch = min(att) if att else None
print()
print("=" * 78)
print("COVERAGE vs the ruled two-mode design (CTO 76379)")
print("=" * 78)
print(f"  epoch, MEASURED from the converter record set (never typed): {epoch}")
ge = {d for d in flow if epoch and d >= epoch}
lt = {d for d in flow if epoch and d < epoch}
gap = sorted(ge - att)
print(f"  in-set dates <  epoch -> declared-historical : {len(lt)}")
print(f"  in-set dates >= epoch -> guard must bind     : {len(ge)}")
print(f"  cross-check {len(lt)} + {len(ge)} == {len(flow)} -> {len(lt)+len(ge)==len(flow)}")
print(f"  >= epoch AND NOT attested (the residual hole): {len(gap)} of {len(ge)}")
if gap:
    print(f"    dates: {gap[:15]}{' ...' if len(gap)>15 else ''}")
    print("    -> RESIDUAL HOLE EXISTS: these refuse in BOTH modes. Surface before building.")
else:
    print(f"    -> NO RESIDUAL HOLE. Coverage {len(lt)} declared + {len(ge & att)} attested "
          f"= {len(lt)+len(ge & att)} of {len(flow)}.")
print()
print("PERISHABLE: the epoch and the attested set ADVANCE with every converter run.")
print("These figures measure the instant they were taken. V14-4 re-derives at execution time.")
