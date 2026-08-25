<to_id>ETFS_SETUP.W2</to_id>
<project>ETFS_SETUP</project>
<title>ETFS_SETUP W2 (AE) -- 49F silver/RPS build (/49-schwab-conv converter) + register canonical thread + 49F daily ETF-ownership producer</title>
<assigned_to>0.5.0_AE_OpalETL</assigned_to>
<consult>0.4.0_DS_ClientPlatform (daily-slice contract -- same as W1)</consult>
<verify>3.0.0_SA_CVO</verify>
<issued_by>2.0.0_SA_COO (ETFS_SETUP decomposition wave-2; Andrew-direct 2026-06-23 "get started"; PRD docs/architecture/ETFS_SETUP.md)</issued_by>
<issued_date>2026-06-23</issued_date>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project ETFS_SETUP, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: active</status>
<!-- GATED on W1 (the opal-data-etfs REUSE + write-out IAM + ETF-universe config + daily-artifact contract must land first). B1: 49F silver/RPS is EMPTY (this TO BUILDS it via /49-schwab-conv). B2: 49F Schwab = manual monthly batch (latest raw 06-09, next ~early-July) -> build the converter NOW (provable on the 06-09 batch); the daily-producer rides the next batch. REASSIGNED 0.7.0_AE_CloudOps -> 0.5.0_AE_OpalETL 2026-06-24 (2.0.0_SA_COO): W1 LANDED -> W2 ungated; base-AE fully-occupied on DC2-crawls + COTETL, 0.5.0 (OpalETL, 49F/Schwab role-fit) takes the converter-build. base-AE remains ETFS-owner (coordinate). TO stays in base-AE folder; 0.5.0 commits converter-code under its OpalETL lane; COO handles TO-status flips. -->
<!-- B1: 49F silver/RPS is EMPTY (this TO BUILDS it via /49-schwab-conv). B2: 49F Schwab = manual monthly batch (latest raw 06-09, next ~early-July) -> build the converter NOW (provable on the 06-09 batch); the daily-producer rides the next batch. -->

<objective>
Build the 49Financial leg of the ETFS write-out model: stand up the 49F silver/RPS data (currently EMPTY = B1) via the /49-schwab-conv RPS converter, register it as a canonical thread, + a 49F daily ETF-ownership producer that writes the daily slice to opal-data-etfs/49financial/{date}.json per the W1 daily-artifact contract.
</objective>

<the_work>
1. /49-schwab-conv RPS CONVERTER: build the converter that turns the 49F Schwab manual monthly batch (raw, latest 06-09) into the 49F silver/RPS layer (currently EMPTY). Provable NOW on the 06-09 batch.
2. REGISTER 49F silver/RPS as a canonical thread (pipescript-visible).
3. 49F DAILY PRODUCER: reads 49F silver/RPS holdings -> filters to the 4-ETF universe (W1 config) -> aggregates per-ETF market_value -> writes opal-data-etfs/49financial/{date}.json per the W1 contract. Write-out model (reads own-firm only + writes etfs prefix; comp-iam-verify no firm-bucket-Deny widening, no cross-firm read).
NOTE: 49F Schwab is a MANUAL MONTHLY batch (B2) -- the producer is monthly-granular in practice (the latest batch's positions); next batch ~early-July. Document the cadence honestly (no overstated daily-ness).
</the_work>

<compiler_tools_mandate>
comp-which-first; comp-iam gaps/service (the 49F producer write-out grant + AVGCAP read); ds-commit-gate per touched .py (from __future__ import annotations); safe-deploy firm-sep (49F tree). comp-iam-verify no cross-firm read.
</compiler_tools_mandate>

<acceptance_criteria>
1. /49-schwab-conv RPS converter built + proven on the 06-09 batch (49F silver/RPS populated, was EMPTY).
2. 49F silver/RPS registered as a canonical thread (pipescript-visible).
3. 49F daily producer writes opal-data-etfs/49financial/{date}.json per the W1 contract (4 ETFs, source_as_of, market_value sane); comp-iam-verified write-out (no firm-bucket-Deny widening, no cross-firm read).
4. Cadence documented honestly (monthly-batch granularity, B2).
5. GATED on W1 landing; firm-sep; RAVC2 COO + CVO. Signals AVGCAP-W2 (49F leg) once the slice is live.
</acceptance_criteria>
