# Task Order: ADVI_INFTGT.TO-7 — Concentration Risk Artifact Wired Up

**Receiver:** `0.4.0_DS_ClientPlatform~A`
**Project:** ADVI_INFTGT
**Priority:** P1
**Dispatched by:** 2.0.0_SA_COO (Andrew direct, 1hr deadline 2026-05-11 EOD)
**Status:** <status>complete</status>

## Scope

`INF_D_07.concentration_risk` produces `[]` (empty 2 bytes). Root cause per PRD §4.4 + §5.3:
script reads `silver/accounts_dim/latest.parquet` only with `load_latest_holdings()` that always
takes `keys[-1]` — the most recent date — regardless of whether pricing data is populated.
Empirically: 2026-05-05..08 holdings partitions have all-null `market_value`; the `dropna` call
eliminates all rows → empty output.

**Fix:**
- Update `load_latest_holdings()` to walk backwards from latest (last 10 partitions), selecting
  the first with at least 1 priced row. Log each candidate so operators know which date is used.
- Add `.copy()` after `dropna` to suppress `SettingWithCopyWarning` noise in CloudWatch.

## Acceptance Criteria

- `concentration_risk.json` is non-empty with >= 1 household row
- `top1_pct`, `hhi`, `risk_tier` populated for all rows
- Script exits 0 with clean stderr

## Compiler Tools

- `comp-pipescript io INF_D_07` — confirmed reads only silver/accounts_dim (missing holdings source)
- Verified holdings data via S3 probe: 2026-05-04 has 9,311 priced rows; 2026-05-05..08 all-null
- Dry-run: 294 HH rows | 37,730 bytes | 15 diversified / 194 moderate / 85 concentrated

## Completion Evidence

- Commit: see session log DS_A_session7_inftgt_to7_2026-05-11.md
- S3 deploy: MATCH verified via comp-pipescript deployed
- Upload: `--upload` mode run → non-empty artifact on S3
- RAVC2 to COO
