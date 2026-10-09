# account_return_daily_build -- Cottonwood, built locally through the one producer (CB-al-1)

NO S3 write. Local day files: `.scratch/advi_cotbkf/ard_cottonwood/date=<D>/data.parquet` (uncommitted); manifest `ard_cottonwood_manifest.json` (sha256 and content hash per day) beside this file.

Sources (VersionId): daily_returns=w9j5YeV1LnNIakNlRTBX6jW1.SDHqmJR, account_day_value=qIWjLLwCIh_Gx6IblSgyaint2tfJ37pr, month_grades=QI5Ks8vQwGTwnc9ekyh.DOsyN8PKN3PB
Method claim: field return_basis, value None (status BLOCKING_GAP_NOT_STATED); method_version null. Review: {"TWR": ["REFUSED", "the producer's arithmetic label under METHOD_VERSION 2, whose dim_return_method row names the custodian's equity as V; carries no 'rebuilt from positions' and no 'net of fees'"], "HOLDINGS_INCOME_FALLBACK": ["REFUSED", "the withdrawn guard substitution (PRD ruling 17, 'never emitted'); FWD-3 is not a fallback and is not holdings-price-plus-income"], "NOT_MEASURABLE": ["REFUSED", "says there is no number; true only on a blank day, where it is used"]}
Exceptions: absent_months=5 absent_days=110 (cross-check disagree=0); held_days=988 (cross-check disagree=0)
Blank-day reasons (sidecar): {"UNPRICED": 1558187, "NON_POSITIVE_BASE": 22521, "FIRST_DAY": 1533, "DVR_CLOSE_STEP": 1069, "HELD_SOURCE_UNDER_REVIEW": 988, "REGRESSED_UNDER_AS_TRADED": 110, "FLOW_UNVALUED": 5}
day_quality census over all rows: {"NOT_MEASURABLE": 1584413, "MEASURED": 107316}
Nulls: {"income_received": "FWD-3 does not separate income (inside the value through the cash leg); no _reason column exists", "income_return": "same; derived from income_received", "fee_amount": "FWD-3 is after fees (a drag inside the return); reason FEE_RAIL_UNUSED is the producer's only admitted reason", "method_version": "NULL on purpose: the producer's version 2 names the custodian equity as V", "return_basis": "NULL on a measured day: no admitted value states the positions-rebuilt, net-of-fees method (BLOCKING gap)"}
Neighbour holdings partition days: 75; rows matched to the neighbour: 0
First address: s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2013-04-03
Last address: s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-22
First day 2013-04-03, last day 2026-06-22

ARD-COTTONWOOD days=3325 rows=1691729 absent_days=110 held_days=988 enum_ok=True addresses_from_builder=True
