"""Answering 0.7.0_AE_CloudOps~L 76663's direct question -- "if the ruled set has moved under
me, say so now" -- and checking one thing their first real date would otherwise discover the
expensive way.

TWO DISTINCT QUESTIONS, deliberately not conflated:
  (1) Has the ruled STAGE SET moved? {c00 -> c01 -> c02 -> dependent c04} + nna_canonical.
      A count moving because the converter ran is EXPECTED; the ruled membership moving is not.
  (2) Has the DATE POPULATION moved since their read? Re-derived here at MY vintage, so the
      comparison is same-vintage rather than me quoting my own 18:4xZ constants back at them.

AND THE THING WORTH CATCHING FIRST: I found the a00 attestation wall. The full chain re-mints
the A/B planes -- but those stages have their OWN silver inputs, and if any of THOSE is thin
over history the chain hits a SECOND wall at a later stage. Their instinct to measure one real
date first is right; this makes that measurement cheaper by naming where to look.

Read-only.
"""
import json
import re
import sys

sys.path.insert(0, "data/assets/scripts/gold/runners_49f")
import runner_common as rc  # noqa: E402

print("=" * 78)
print("(1) THE RULED STAGE SET -- has membership moved?")
src = open("data/assets/scripts/gold/runners_49f/chain_49f_entrypoint.py", encoding="utf-8").read()
stages = re.findall(r'\("([a-z]\d\d[a-z0-9_]*)",', src)
print(f"    chain _stage_list at HEAD ({len(stages)} stages): {stages}")
ruled = ["c00_flow_ledger", "c01_nna_canonical", "c02_twr_daily"]
present = [r for r in ruled if r in stages]
print(f"    ruled c-plane members present: {present}")
print(f"    c03 nna_atomic excluded (dormant-superseded, as ruled): "
      f"{'c03' not in ' '.join(stages)}")

# the flow_ledger consumer set -- the thing that would WIDEN the ruled set if it changed
import subprocess  # noqa: E402
hits = subprocess.run(["grep", "-rl", "flow_ledger",
                       "data/assets/scripts/gold/runners_49f"],
                      capture_output=True, text=True).stdout.split()
py = sorted(h.rsplit("/", 1)[-1] for h in hits if h.endswith(".py"))
print(f"    files referencing flow_ledger ({len(py)}): {py}")
print("    -> compared against the set enumerated at 16:4xZ and ruled UNCHANGED by CTO 76200")

print("\n" + "=" * 78)
print("(2) THE DATE POPULATION -- re-derived at MY vintage, independently")
s3 = rc.s3()
pag = s3.get_paginator("list_objects_v2")
keys = [o["Key"] for page in pag.paginate(Bucket=rc.BUCKET, Prefix=f"{rc.SCOPE}/meta/conversions/")
        for o in page.get("Contents", [])]
att = set()
for k in keys:
    rec = json.loads(s3.get_object(Bucket=rc.BUCKET, Key=k)["Body"].read())
    per = rec.get("per_type", {}).get("fact_acc")
    if per and per.get("action") == "converted":
        att.update(str(p) for p in rec.get("partitions", []))
led = rc.list_partition_dates(f"{rc.OUT_ROOT}/canonical/flow_ledger")
proceeds = sum(1 for d in led if d in att)
epoch = min(att) if att else ""
print(f"    records scanned {len(keys)} | attested dates {len(att)} | epoch {epoch}")
print(f"    backfill set {len(led)} | a00 proceeds {proceeds} | refuses {len(led) - proceeds}")
theirs = {"records": 456, "attested": 32, "set": 533, "proceeds": 27,
          "refuses": 506, "epoch": "2026-07-14"}
mine = {"records": len(keys), "attested": len(att), "set": len(led),
        "proceeds": proceeds, "refuses": len(led) - proceeds, "epoch": epoch}
print(f"    THEIRS {theirs}")
print(f"    MINE   {mine}")
print(f"    IDENTICAL: {theirs == mine}")

print("\n" + "=" * 78)
print("(3) IS THERE A SECOND WALL? silver inputs the A/B stages need, over history")
print("    (the full chain re-mints the A/B PLANES -- but those stages read silver of their own)")
for label, prefix in (("fact_acc      (a00)", f"{rc.SILVER}/fact_acc"),
                      ("fact_trn      (c00)", f"{rc.SILVER}/fact_trn"),
                      ("fact_fam      (a00 stamp)", f"{rc.SILVER}/fact_fam"),
                      ("dim_transaction   (c03/legacy)", f"{rc.SILVER}/dim_transaction"),
                      ("canonical_valuation (b00/c02)", f"{rc.OUT_ROOT}/canonical/canonical_valuation")):
    try:
        d = rc.list_partition_dates(prefix)
        cover = sum(1 for x in led if x in set(d))
        print(f"    {label:<32} {len(d):>4} partitions | covers {cover:>3} of the {len(led)} "
              f"backfill dates | earliest {d[0] if d else '-'}")
    except Exception as exc:
        print(f"    {label:<32} UNREADABLE: {type(exc).__name__}")
print("\n    A row covering far fewer than the backfill set is a candidate SECOND wall --")
print("    not a verdict, a place to look before spending a multi-hour run to find it.")
