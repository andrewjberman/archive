# V2-8 pre-fire: rl* drift-boundary binary search + shell census (verbatim transcripts)

**Method:** `crs_reader.parse_crs` header inspection per probe (full parse, read-only GetObject);
binary search over the 754 sorted rld partitions of 0824; bracket probes on rlu/rly; boundary re-probed
on 0833. Shell census = full-lane size listing per type (ListObjectsV2, ContinuationToken drained).
Session: 0.6.2_AE_PartnerETL 2026-07-14 ~16:4xZ, repo vintage e9d1a6817.

## Binary search (0824 rld, target column `schwab_order_id`)

```
rld partitions: 754
  probe 20250108: schwab_order_id=missing
  probe 20251008: schwab_order_id=PRESENT
  probe 20250523: schwab_order_id=missing
  probe 20250801: schwab_order_id=PRESENT
  probe 20250627: schwab_order_id=missing
  probe 20250716: schwab_order_id=missing
  probe 20250724: schwab_order_id=PRESENT
  probe 20250721: schwab_order_id=PRESENT
  probe 20250717: schwab_order_id=missing
  probe 20250718: schwab_order_id=PRESENT
0824 RLD boundary: last-missing=20250717 first-present=20250718 (probes=10)
0833 RLD 20250717: schwab_order_id=missing
0833 RLD 20250718: schwab_order_id=PRESENT
```

## Refusal counts at boundary 2025-07-18 + rlu/rly bracket probes (both lanes)

```
08242234 rld: n=754 pre-boundary drift-refuse=506 shell-refuse=1 post-boundary-clean=247 [pre-last=20250717 post-first=20250718]
08242234 rlu: n=12  pre-boundary drift-refuse=8   shell-refuse=0 post-boundary-clean=4   [pre-last=20250606 post-first=20250905]
   probe rlu 20250606: missing (expect missing)
   probe rlu 20250905: PRESENT (expect PRESENT)
08242234 rly: n=36  pre-boundary drift-refuse=24  shell-refuse=0 post-boundary-clean=12  [pre-last=20250630 post-first=20250731]
   probe rly 20250630: missing (expect missing)
   probe rly 20250731: PRESENT (expect PRESENT)
08335338 rld: n=754 pre-boundary drift-refuse=506 shell-refuse=1 post-boundary-clean=247 [pre-last=20250717 post-first=20250718]
08335338 rlu: n=12  pre-boundary drift-refuse=8   shell-refuse=0 post-boundary-clean=4   [pre-last=20250606 post-first=20250905]
   probe rlu 20250606: missing (expect missing)
   probe rlu 20250905: PRESENT (expect PRESENT)
08335338 rly: n=36  pre-boundary drift-refuse=24  shell-refuse=0 post-boundary-clean=12  [pre-last=20250630 post-first=20250731]
   probe rly 20250630: missing (expect missing)
   probe rly 20250731: PRESENT (expect PRESENT)
== 08242234: TOTAL drift-refusals=538 shells=1
== 08335338: TOTAL drift-refusals=538 shells=1
```

## Shell census (size minima per type; only rld has a shell-sized object)

```
08242234 rld min4: (525, 20250109) (4288, 20240305) (4746, 20240531) (5291, 20241129)
08335338 rld min4: (513, 20250109) (4277, 20240305) (4730, 20240531) (4919, 20241129)
-- every other type's minimum is >= 25KB (trn) and carries data rows.
-- 2025-01-09 = national day of mourning (markets closed); vendor delivered header+trailer-only files.
-- parse verdict on the shells: CrsFormatError "no data rows" -> quarantine class (exercised, both lanes).
```

## RLD day-law enumeration (sweep refusal precondition)

```
08242234: bronze_keys=5978 dates=754 refused_dates=0
08335338: bronze_keys=6945 dates=754 refused_dates=0
-- every date carrying pipe types carries rld: assert_rld_covered refuses nothing in the backlog.
```
