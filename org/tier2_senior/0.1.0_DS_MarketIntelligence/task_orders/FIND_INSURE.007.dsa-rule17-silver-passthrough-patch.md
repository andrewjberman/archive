# FIND_INSURE.007 — Rule 17 silver passthrough patch (5 dropped bronze meta fields)

**Project:** [FIND_INSURE](../../../projects/FIND_INSURE.json)
**PRD:** `docs/architecture/FIND_INSURE.md` (Rule 17 spec via ws CTO Trigger-2(b)(ii) REPAIR-AMENDMENT — landing parallel; this TO is execution-class, not gated on PRD amend per CVO note "NOT a PRD amend; just a silver-script patch")
**Pod:** 0.1.0_DS_MarketIntelligence~A
**Lane:** DS_MarketIntelligence ~A (Phase 1 silver-tier maintenance)
**Issued to:** 0.1.0_DS_MarketIntelligence~A
**Author:** 2.0.0_SA_COO 2026-05-27T~22:55Z (cycle 165 post-reboot Phase 1 close-gating triad)
**Sizing:** ~30-60min wall (1-file edit + unit-test extension + ds-commit-gate + small empirical re-run against existing 3-IMO bronze)
**Authority anchor:** CVO /verify-channel verdict `54ace66c8` §S1 Rule 17 sub-finding + REPAIR-AMENDMENT-AUTHORIZED (b)(ii) 2026-05-27T~21:00Z + Andrew sovereign goal-set 22:49Z (drive FIND_INSURE end-to-end through Phase 3 close); CVO routes this as routine silver-script impl per [[feedback_silver_no_field_slimming]].

<status>pending</status>

## Objective

Patch `data/find/imo/scripts/silver/parse_web_silver.py` `build_silver_record()` (line ~291) to preserve 5 bronze meta fields currently dropped on the success path. Per CLAUDE.md Rule 17 silver passthrough discipline + CVO 11-axes verdict §S1 finding — these fields are crawler-process diagnostic, load-bearing for debugging the empty-body/blocked-class root-cause path (which is exactly the AC-T2 telemetry surface).

**The 5 dropped fields** (each from bronze `.meta.json` sidecar, confirmed present in B1 schema-inventory):

| Field | dtype | Why load-bearing |
|---|---|---|
| `http_headers` | dict | Bright Data response headers — `x-brd-error*` keys carried the carl-ostenson TLS-cert-mismatch root-cause (`"net_err_cert_common_name_invalid"`). Without this, silver consumers can't audit why a page landed in BLOCKED class. |
| `crawl_depth` | int | Crawler tree depth at fetch — audit + downstream link-graph anti-cycle telemetry. |
| `robots_txt_compliance` | bool | Audit; downstream legal/ethics scan. |
| `scheme_fallback` | str/null | https→http fallback flag — input to Phase 2B job-postings TLS-debug path. |
| `tls_fail_original` | bool | TLS error flag — companion to scheme_fallback for AC-T2 EMPTY-BODY classification refinement. |

Per CVO verdict S1: "The silver script's `build_silver_record` makes [a field-pruning] judgment by NOT carrying these 5 fields forward. The fields are crawler-process diagnostic — they would be load-bearing for debugging 'why did silver land in BLOCKED class' (carl-ostenson empty-body root-cause needed bronze meta.json `x-brd-error*` field inspection — exactly the fields silver drops). This is the diagnostic-loss class Rule 17 exists to prevent."

## Acceptance criteria

- **AC1.** `from __future__ import annotations` first import (Rule 15); ds-commit-gate clean; ruff `--target-version py39` clean.
- **AC2.** `build_silver_record()` SUCCESS path appends the 5 fields verbatim from `bronze_meta` dict, preserving bronze dtypes (no transformation, no fillna, no defaulting). Order: insert after existing `last_modified` field for readability; both 16-field SUCCESS schema becomes 21-field SUCCESS schema.
- **AC3.** `build_blocked_record()` BLOCKED path also appends the 5 fields. carl-ostenson is the canonical anchor — its `http_headers.x-brd-error*` is the diagnostic payload Rule 17 mandates we preserve. The original silver BLOCKED record dropped the entire dict; this patch surfaces it.
- **AC4.** Rule 17 strict — NO new field-pruning / fillna / dtype-coercion on the 5 fields. If a bronze meta record is missing a field (legitimate schema drift case), the silver record sets that field to `null` (carry the absence verbatim, not silently substitute).
- **AC5.** Existing AC1-AC10 of FIND_INSURE.005 remain satisfied — no regression to the 16-field success / 9-field blocked schemas; this is ADDITIVE. Silver consumers (gold-tier score_web_gold.py) keep working because the additive fields are unknown to them and ignored.
- **AC6.** Empirical re-run against existing 3-IMO bronze (`s3://opal-data-imo/corp/avantax-wealth-management/` + `1st-atlantic-insurance-group/` + `carl-ostenson/`) — confirm:
  - 5 success-class records (avantax 5 + atlantic 5 = 10? — confirm; previously 11/11 in .005 AC8) carry the 5 new fields with non-null bronze-meta values
  - 1 blocked-class record (carl-ostenson) carries `http_headers` dict containing the `x-brd-error*` keys; silver record now contains the diagnostic that was previously discarded
  - Spot-check `aws s3 cp s3://opal-data-imo/corp/carl-ostenson/silver/web-scrape/2026-05-27/<url_hash>.json -` and confirm `http_headers["x-brd-error"]` resolves to the `"net_err_cert_common_name_invalid"` value.
- **AC7.** Deployed-Lambda re-run via `aws lambda invoke find-insure-parse-web` against the same 3 IMOs — confirm production parity with local invocation. Tag bump: `imo-pipeline-v0.3.1` (patch-level on top of v0.3.0 which shipped .005 deployment).
- **AC8.** Self-test `python data/find/imo/scripts/silver/parse_web_silver.py` — 35/35 existing checks still pass + new check exercises the 5-field-preserve assertion on both SUCCESS and BLOCKED fixture paths. Aim: 37/37 or 38/38 (new self-tests = +2/3).
- **AC9.** `comp-pipescript io data/find/imo/scripts/silver/parse_web_silver.py` re-runs clean (or "Unknown script" → comp-graph rebuild lag, documented as tooling-not-correctness per .005 precedent).

## Dependencies

- **FIND_INSURE.005 RAVC2-Accept (Phase 1 silver)** — landed pre-reboot; this TO patches the AC2/AC4 schema, leaving AC8/AC10 chain intact.
- **NO PRD-amend dependency.** CVO explicitly noted: "NOT a PRD amend; just a silver-script patch. ws CTO Trigger-2(b)(ii) absorbs the Rule 17 spec for silver passthrough." If ws CTO REPAIR-AMENDMENT lands the spec change in PRD §3.4 ahead of your work — read it for alignment, but do NOT block on it.
- **Bronze data unchanged** — `crawl_web_bronze.py` already writes the 5 fields per .meta.json schema (verified in CVO §B1 inventory); no AE upstream coordination required.

## Sequencing — fast-turnaround

1. ~5min: read CVO 11-axes §S1 finding (anchor) + your .005 `build_silver_record()` + `build_blocked_record()` + bronze .meta.json schema inventory (CVO §B1)
2. ~10min: patch both record-builders + extend self-test fixture
3. ~5min: ds-commit-gate + ruff + py_compile
4. ~5min: local invocation against 3-IMO bronze → spot-check silver output
5. ~10min: AE 0.7~A deploy parity (if AE not yet LIVE: surface to me for SYNC handoff timing)
6. ~5min: commit + RAVC2-Request

**Total ETA:** ~40min wall from spawn-LIVE if AE 0.7~A is co-LIVE for AC7; ~25min if AE not LIVE (defer AC7 to chain with .008 universe-run dispatch).

## RAVC2 deliverable

`[RAVC2-Request] FIND_INSURE.007 — Rule 17 silver passthrough patch` to ws COO with: code commit hash + diff summary (5 field-add lines per record-builder) + AC6 empirical evidence (silver carl-ostenson record showing `http_headers["x-brd-error"]` = `"net_err_cert_common_name_invalid"`) + AC7 deployed-Lambda parity (if AE LIVE) + self-test pass count + comp-pipescript output. CC ws CTO + ws CVO (CVO will validate Rule 17 compliance + close the (b)(ii) trigger).

## Compiler tools mandate

- **Before edit:** `comp-pipescript io data/find/imo/scripts/silver/parse_web_silver.py` — confirm script-level consumers + column-gap state (likely "Unknown script" until comp-graph rebuild)
- **Before commit:** `.tools/ds-commit-gate.sh data/find/imo/scripts/silver/parse_web_silver.py` — mandatory per CLAUDE.md Rule 14
- **After commit:** `comp-pipescript deployed find-insure-parse-web` (after AE deploy) — MATCH gate before AC7 production run

## Cross-domain coordination

`<none/>` — silver-tier script edit, no cross-domain S3 artifact overlap with other active TOs (FIND_INSURE.008 universe-run consumes silver downstream — but is a chain, not a contention).

## Notes

- Per [[feedback_silver_no_field_slimming]] + CLAUDE.md Rule 17: silver is preserve-all; this patch is the structural fix for the violation CVO independently surfaced.
- Per CVO ADDITIVE-class doctrine: this TO closes the (b)(ii) trigger via execution; ws CTO PRD amend separately closes the (b)(ii) spec leg. Both are needed for full close; they're parallel.
- Sister patch hint: when Phase 2 LinkedIn silver lands (`parse_linkedin_silver.py`) and Phase 2B job-postings silver (`parse_jobs_silver.py`) — the same Rule 17 discipline must apply by design; this fix sets the precedent for the channel-pattern.

— ws COO /drive cycle 165 post-reboot Phase 1 close-gating triad 2026-05-27T~22:55Z
