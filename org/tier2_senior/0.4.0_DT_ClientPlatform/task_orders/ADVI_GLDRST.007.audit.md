# GLDRST.007 S3 Path Migration Audit

**Agent:** 0.4.0_DT_ClientPlatform
**Date:** 2026-04-06
**Source of truth:** `data/black_diamond/scripts/gold/lib/s3_layout.py`

---

## Migration Rules

- **READS:** Switch from old key to new key (both exist via dual-write in .004)
- **WRITES:** Dual-write to BOTH old and new key (until .008/.010 clean up old paths)
- **COMMENTS/DOCSTRINGS:** Update to reflect new paths (informational only)
- **NO CHANGE keys:** `gold/views/*` and `gold/timeseries/nna_*` are already at final location

---

## File 1: bd-portal-publisher (2,059 lines)

### READS to migrate

| Line | Old Key | New Key | Type |
|------|---------|---------|------|
| 191 | `gold/aua_certification/{today}.json` | `gold/validation/aua_certification/{today}.json` | f-string |
| 394,400 | `gold/client_performance.parquet` | `gold/timeseries/client_performance.parquet` | string literal |
| 426 | `gold/client_dimension.parquet` | `gold/dimensions/client_dimension.parquet` | string literal |
| 436 | `gold/accounts_dimension_latest.parquet` | `gold/dimensions/accounts_dimension_latest.parquet` | string literal |
| 487 | `gold/holdings_lots/` (prefix) | `gold/timeseries/holdings_lots/` | string literal |

### READS that stay (NO CHANGE)

| Line | Key | Reason |
|------|-----|--------|
| 409 | `gold/views/nna_aua_by_advisor.parquet` | Already at final location |
| 418 | `gold/views/nna_aua_by_geography.parquet` | Already at final location |
| 445 | `gold/views/client_tax_liability.parquet` | Already at final location |
| 460 | `gold/views/nna_aua_by_geography_city.parquet` | Already at final location |

### WRITES to dual-write (old + new)

| Line | Old Key (KEEP) | New Key (ADD) |
|------|----------------|---------------|
| 1903 | `gold/snapshots/aua_by_architect.json` | `gold/artifacts/snapshots/aua_by_architect.json` |
| 1905 | `gold/snapshots/aua_by_tax_status.json` | `gold/artifacts/snapshots/aua_by_tax_status.json` |
| 1907 | `gold/snapshots/aua_by_state.json` | `gold/artifacts/snapshots/aua_by_state.json` |
| 1909 | `gold/snapshots/aua_by_region.json` | `gold/artifacts/snapshots/aua_by_region.json` |
| 1971 | `gold/timeseries_chart.json` | `gold/artifacts/timeseries_chart.json` |
| 1976 | `gold/architect_leaderboard.json` | `gold/artifacts/architect_leaderboard.json` |
| 1981 | `gold/clients_tab.json` | `gold/artifacts/clients_tab.json` |
| 1986 | `gold/summary/header_metrics.json` | `gold/artifacts/summary/header_metrics.json` |
| 2001 | `gold/filters/dimensions.json` | `gold/artifacts/filters/dimensions.json` |

### COMMENTS/DOCSTRINGS to update (informational)

| Line | Content |
|------|---------|
| 4 | Trigger path (comment: `gold/pipeline-complete.json` -> `gold/meta/pipeline-complete.json`) |
| 11-20 | Output list (comments) |
| 187 | Docstring ref to `gold/aua_certification/` |
| 563 | Docstring ref to `gold/aua_certification/` |
| 1996 | Disabled partner_analytics comment |
| 2024 | Comment about `gold/` writes |

---

## File 2: bd-portal-advisor-publisher (1,158 lines)

### READS to migrate

| Line | Old Key | New Key | Type |
|------|---------|---------|------|
| 96 | `gold/holdings_lots/` (prefix) | `gold/timeseries/holdings_lots/` | string literal |
| 113 | `gold/account_performance.parquet` | `gold/timeseries/account_performance.parquet` | string literal |
| 140 | `gold/client_dimension.parquet` | `gold/dimensions/client_dimension.parquet` | string literal |
| 691 | `gold/client_timeseries/{rel_id}.json` | `gold/entities/clients/{rel_id}.json` | f-string |

### READS that stay (NO CHANGE)

| Line | Key | Reason |
|------|-----|--------|
| 126 | `gold/views/client_tax_liability.parquet` | Already at final location |
| 163 | `gold/views/rel_architect_lookup.parquet` | Already at final location |

### WRITES to dual-write (old + new)

| Line | Old Key (KEEP) | New Key (ADD) |
|------|----------------|---------------|
| 605 | `gold/advisors/{id}/book.json` | `gold/entities/advisors/{id}/book.json` |
| 664 | `gold/advisors/{id}/timeseries.json` | `gold/entities/advisors/{id}/timeseries.json` |
| 732 | `gold/advisors/{id}/mix_timeseries.json` | `gold/entities/advisors/{id}/mix_timeseries.json` |
| 1037 | `gold/clients/{rel_id}.json` | `gold/entities/clients/{rel_id}/detail.json` |
| 1091 | `gold/implementor_leaderboard.json` | `gold/artifacts/implementor_leaderboard.json` |

### COMMENTS/DOCSTRINGS to update (informational)

| Line | Content |
|------|---------|
| 4 | Trigger path comment |
| 615 | Docstring ref |
| 673,675 | Docstring refs |
| 981 | Docstring ref |

---

## File 3: opal-partners-data (1,365 lines)

### READS to migrate

| Line | Old Key | New Key | Type |
|------|---------|---------|------|
| 526 | `gold/snapshots/aua_by_{dim}.json` | `gold/artifacts/snapshots/aua_by_{dim}.json` | f-string |
| 539 | `gold/filters/dimensions.json` | `gold/artifacts/filters/dimensions.json` | string literal |
| 551 | `gold/clients/growth_timeseries.json` | `gold/artifacts/clients/growth_timeseries.json` | string literal |
| 563 | `gold/clients/tax_basis_breakdown.json` | `gold/artifacts/clients/tax_basis_breakdown.json` | string literal |
| 575 | `gold/clients/tax_deferred_candidates.json` | `gold/artifacts/clients/tax_deferred_candidates.json` | string literal |
| 587 | `gold/summary/header_metrics.json` | `gold/artifacts/summary/header_metrics.json` | string literal |
| 599 | `gold/partner_analytics/header_metrics.json` | `gold/artifacts/partner_analytics/header_metrics.json` | string literal |
| 616 | `gold/advisors/{id}/book.json` | `gold/entities/advisors/{id}/book.json` | f-string |
| 665 | `gold/summary/header_metrics.json` (head_object) | `gold/artifacts/summary/header_metrics.json` | string literal |
| 746 | `gold/holdings_lots/` (prefix) | `gold/timeseries/holdings_lots/` | string literal |
| 778 | `gold/account_performance.parquet` (error msg) | `gold/timeseries/account_performance.parquet` | f-string |
| 803 | `gold/client_performance.parquet` | `gold/timeseries/client_performance.parquet` | string literal |
| 809 | `gold/account_performance.parquet` | `gold/timeseries/account_performance.parquet` | string literal |
| 1009,1016 | `gold/client_timeseries/{id}.json` | `gold/entities/clients/{id}.json` | f-string |
| 1042 | `gold/advisors/{id}/timeseries.json` | `gold/entities/advisors/{id}/timeseries.json` | f-string |
| 1057 | `gold/advisors/{id}/mix_timeseries.json` | `gold/entities/advisors/{id}/mix_timeseries.json` | f-string |
| 1080 | `gold/firm_mix_views.json` | `gold/artifacts/firm_mix_views.json` | string literal |
| 1091 | `gold/advisors/{id}/mix.json` | `gold/entities/advisors/{id}/mix.json` | f-string |
| 1115 | `gold/advisors/{id}/composition.json` | `gold/entities/advisors/{id}/composition.json` | f-string |

### READS that stay (NO CHANGE)

| Line | Key | Reason |
|------|-----|--------|
| 503 | `gold/timeseries/nna_total.json` | Already at final location |
| 505 | `gold/timeseries/nna_by_{dim}.json` | Already at final location |
| 1102 | `gold/views/firm_composition.json` | Already at final location |

NOTE: `gold/snapshots/aua_by_{dim}.json` (line 526) DOES migrate -- see reads table above.
Publisher dual-writes to both old and new; opal-partners-data switches to new path.

### NO WRITES (read-only API Lambda)

### COMMENTS/DOCSTRINGS to update (informational)

| Line | Content |
|------|---------|
| 40-43 | Module docstring |
| 1001 | Comment about gold script 06b |
| 1036 | Docstring about advisor-publisher |
| 1050 | Docstring about advisor-publisher |
| 1075 | Docstring about 06b |
| 1086 | Docstring about 06b |
| 1097 | Docstring about 12 |
| 1108 | Docstring about 12 |

---

## Verification Checklist (post-edit)

For each file, after editing:
1. `grep -n "gold/" <file>` — every remaining `gold/` reference must either:
   - Be a NO CHANGE key (`gold/views/*`, `gold/timeseries/nna_*`, `gold/snapshots/aua_by_*`)
   - Be a legacy dual-write path (old key kept alongside new key)
   - Be a comment/docstring that has been updated
2. No orphaned old-format read paths remain
3. All write paths have both old + new
