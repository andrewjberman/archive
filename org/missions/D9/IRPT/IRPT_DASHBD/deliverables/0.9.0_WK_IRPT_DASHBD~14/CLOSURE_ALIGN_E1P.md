# CLOSURE_ALIGN_E1P -- counts only (IRPT_DASHBD.TO-DB-b-29)

Measured by 0.9.0_WK_IRPT_DASHBD~14 on dell2, 2026-10-07. Read-only against the served 49F gold series; 0 vendor calls; no write to S3; served opal_return untouched.

- Accrual rule: the closure-day accrual is the mean daily `income_return` over the segment's linked days (issuer-accepted rule).
- Gold read: s3://opal-data-49financial/irpt/49financial/gold/account_return_daily/, 564 partitions.
- Denominator: 2,299 closure segments (GROSS UNEXPLAINED rows that are +1-day over 2025-01-09).
- within_bd_convention: 0 (tolerance 0.35 pp)
- outside_bd_convention: 2,299

Record: CLOSURE_ALIGN_E1P.json (per-segment rows).
