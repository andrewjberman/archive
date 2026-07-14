# OPAL_ASSETS V2-8 -- set-identity guard: the four ruled MUTANT TRANSCRIPTS + the live pre-deploy baseline

**Author:** 0.6.2_AE_PartnerETL . 2026-07-14 ~11:2xZ . ruling 25 (mutants BEFORE first real conversion)
**Module:** data/assets/scripts/silver/set_identity_guard.py . mutants also live as tests/test_set_identity_guard.py

## BASELINE (covered lane)
```json
{
 "ok": true,
 "denominators": {
  "bronze_keys": 4,
  "silver_keys": 10,
  "bronze_types": 2,
  "silver_tables": 5
 },
 "shortfall": [],
 "surplus": [],
 "collisions": [],
 "holes_named": []
}
```

## MUTANT (a) SHORTFALL -- fact_rps_s2 2026-07-13 deleted from the census input
```json
{
 "ok": false,
 "denominators": {
  "bronze_keys": 4,
  "silver_keys": 9,
  "bronze_types": 2,
  "silver_tables": 5
 },
 "shortfall": [
  {
   "table": "fact_rps_s2",
   "date": "2026-07-13",
   "bronze_type": "rps"
  }
 ],
 "surplus": [],
 "collisions": [],
 "holes_named": []
}
```

## MUTANT (b) SURPLUS -- alien fact_acc 2026-07-11 + unknown table fact_zzz planted
```json
{
 "ok": false,
 "denominators": {
  "bronze_keys": 4,
  "silver_keys": 12,
  "bronze_types": 2,
  "silver_tables": 6
 },
 "shortfall": [],
 "surplus": [
  {
   "table": "fact_acc",
   "date": "2026-07-11",
   "keys": [
    "schwab/08335338/silver/fact_acc/date=2026-07-11/data.parquet"
   ]
  },
  {
   "table": "fact_zzz",
   "date": "2026-07-10",
   "keys": [
    "schwab/08335338/silver/fact_zzz/date=2026-07-10/data.parquet"
   ]
  }
 ],
 "collisions": [],
 "holes_named": []
}
```

## MUTANT (c) COLLISION -- second object under fact_acc date=2026-07-13
```json
{
 "ok": false,
 "denominators": {
  "bronze_keys": 4,
  "silver_keys": 11,
  "bronze_types": 2,
  "silver_tables": 5
 },
 "shortfall": [],
 "surplus": [],
 "collisions": [
  {
   "table": "fact_acc",
   "date": "2026-07-13",
   "keys": [
    "schwab/08335338/silver/fact_acc/date=2026-07-13/data(1).parquet",
    "schwab/08335338/silver/fact_acc/date=2026-07-13/data.parquet"
   ]
  }
 ],
 "holes_named": []
}
```

## MUTANT (d) HOLE-MISUSE -- unconverted uln + tcf partitions; uln may NEVER read as a hole
```json
{
 "ok": false,
 "denominators": {
  "bronze_keys": 2,
  "silver_keys": 0,
  "bronze_types": 2,
  "silver_tables": 0
 },
 "shortfall": [
  {
   "table": "fact_uln",
   "date": "2026-07-13",
   "bronze_type": "uln"
  }
 ],
 "surplus": [],
 "collisions": [],
 "holes_named": [
  {
   "type": "tcf",
   "date": "2026-07-13",
   "disposition": "reader-variance (dictionary SS2c)"
  }
 ]
}
```

## LIVE PRE-DEPLOY BASELINE (read-only ListObjectsV2, both lanes, 2026-07-14 ~11:2xZ)

Nothing is deployed; monolith silver is EMPTY by construction. The honest verdict is a
full-lane SHORTFALL -- the guard seeing the entire build ahead of it, plus every
reader-variance partition named. This is the denominator the first sweep must retire.

### lane 08335338: bronze_keys=6945 silver_keys=0 ok=False
  shortfall entries=8436 (facts+projections) . holes named=1039 . surplus=0 . collisions=0
  per-type: {'acc': ('SHORTFALL', 506), 'fam': ('SHORTFALL', 506), 'rld': ('SHORTFALL', 754), 'rlu': ('SHORTFALL', 12), 'rly': ('SHORTFALL', 36), 'rps': ('SHORTFALL', 506), 'rtu': ('SHORTFALL', 12), 'rty': ('SHORTFALL', 36), 'sec': ('SHORTFALL', 506), 'slm': ('SHORTFALL', 502), 'tcf': ('NAMED-HOLE', 754), 'tcfx': ('NAMED-HOLE', 183), 'tnn': ('NAMED-HOLE', 102), 'trn': ('SHORTFALL', 506), 'uln': ('SHORTFALL', 506), 'ult': ('SHORTFALL', 506), 'upn': ('SHORTFALL', 506), 'upt': ('SHORTFALL', 506)}

### lane 08242234: bronze_keys=5978 silver_keys=0 ok=False
  shortfall entries=7468 (facts+projections) . holes named=1040 . surplus=0 . collisions=0
  per-type: {'acc': ('SHORTFALL', 506), 'rld': ('SHORTFALL', 754), 'rlu': ('SHORTFALL', 12), 'rlw': ('SHORTFALL', 40), 'rly': ('SHORTFALL', 36), 'rps': ('SHORTFALL', 506), 'rtu': ('SHORTFALL', 12), 'rty': ('SHORTFALL', 36), 'sec': ('SHORTFALL', 506), 'tcf': ('NAMED-HOLE', 754), 'tcfx': ('NAMED-HOLE', 183), 'tnn': ('NAMED-HOLE', 103), 'trn': ('SHORTFALL', 506), 'uln': ('SHORTFALL', 506), 'ult': ('SHORTFALL', 506), 'upn': ('SHORTFALL', 506), 'upt': ('SHORTFALL', 506)}

