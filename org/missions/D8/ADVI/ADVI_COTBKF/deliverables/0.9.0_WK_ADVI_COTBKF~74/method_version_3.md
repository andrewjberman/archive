# method_version_3 -- Cottonwood account_return_daily rebuilt with method_version 3 (round 47 CB-au-1)

Rule commit f043506a7c. Adapter changed: scratch dir r47, row method_version = the entry's version, R47 line, handler tests. Row blank rule: the producer writes the entry's version on every row (none blank); census 1691729 of 1691729 rows read 3.


NO S3 write. Local day files: `.scratch/advi_cotbkf/ard_cottonwood_r47/date=<D>/data.parquet` (uncommitted); manifest `ard_cottonwood_manifest.json` (sha256 and content hash per day) beside this file.

Sources (VersionId): daily_returns=w9j5YeV1LnNIakNlRTBX6jW1.SDHqmJR, account_day_value=qIWjLLwCIh_Gx6IblSgyaint2tfJ37pr, month_grades=QI5Ks8vQwGTwnc9ekyh.DOsyN8PKN3PB
Method claim: field return_basis, value TWR (status STATED); method_version null. Review: {"TWR": ["TRUTHFUL", "the producer's arithmetic label (time-weighted, daily geometric); the V / fee / price method is NOT in the label but in the manifest's valuation_source/fee_treatment/price_basis read from the sources.json entry (ADDENDUM 13.1), so the label states no custodian method"], "HOLDINGS_INCOME_FALLBACK": ["REFUSED", "the withdrawn guard substitution (PRD ruling 17, 'never emitted'); FWD-3 is not a fallback and is not holdings-price-plus-income"], "NOT_MEASURABLE": ["REFUSED", "says there is no number; true only on a blank day, where it is used"]}
Exceptions: absent_months=5 absent_days=110 (cross-check disagree=0); held_days=988 (cross-check disagree=0)
Blank-day reasons (sidecar): {"UNPRICED": 1558187, "NON_POSITIVE_BASE": 22521, "FIRST_DAY": 1533, "DVR_CLOSE_STEP": 1069, "HELD_SOURCE_UNDER_REVIEW": 988, "REGRESSED_UNDER_AS_TRADED": 110, "FLOW_UNVALUED": 5}
day_quality census over all rows: {"NOT_MEASURABLE": 1584413, "MEASURED": 107316}
Nulls: {"income_received": "FWD-3 does not separate income (inside the value through the cash leg); no _reason column exists", "income_return": "same; derived from income_received", "fee_amount": "FWD-3 is after fees (a drag inside the return); reason FEE_RAIL_UNUSED is the producer's only admitted reason", "method_version": "NULL on purpose: the producer's version 2 names the custodian equity as V"}
Neighbour holdings partition days: 75; rows matched to the neighbour: 0
First address: s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2013-04-03
Last address: s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/date=2026-06-22
First day 2013-04-03, last day 2026-06-22

ARD-COTTONWOOD-R47 days=3325 manifests_mv3=3325/3325 rows_mv3=1691729 producer_tests=106 handler_tests=86
