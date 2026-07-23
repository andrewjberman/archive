# TO 3F-B3 — INF/Orion Propagation VERIFIED on the Scheduled Pass — COMPLETE

**Agent:** 0.6.2_AE_PartnerETL~A · **Date:** 2026-07-23 ~03:35Z · **Zero hand-fires** — all evidence from
the scheduled 03:30Z mirror pass (the cot cron(30 3) fire walking all three map rows, as predicted in the
interim) + the event-driven silver conversion.

## Phase 1 (from the 07-22 interim, unchanged)

- `opal-assets-ingest-mirror-inf-daily`: ENABLED, `cron(15 14 * * ? *)` — cited verbatim.
- Source repair premise: opal-data-inf bronze 07-11..15 present at EXACT @b47d2ff10 sizes.
- comp-freshness basis gap recorded (project-wide; wiring with 0.7.0).

## Phase 2 — the acceptance, measured (all explicit-Z)

**Monolith BRONZE (mirror copies, byte-faithful):**
```
2026-07-11  2,176,938B  2026-07-23T03:30:21Z     (source size preserved exactly)
2026-07-12  2,175,913B  2026-07-23T03:30:21Z
2026-07-13  2,172,954B  2026-07-23T03:30:21Z
2026-07-14  2,176,843B  2026-07-23T03:30:21Z
2026-07-15  2,180,491B  2026-07-23T03:30:22Z
```

**Monolith SILVER row counts — silver == source == PRD acceptance, EXACT:**
```
date         silver   source   expected   verdict   silver stamp
2026-07-11   34,935   34,935   34,935     PASS      03:30:30Z
2026-07-12   34,935   34,935   34,935     PASS      03:30:31Z
2026-07-13   34,935   34,935   34,935     PASS      03:30:34Z
2026-07-14   34,942   34,942   34,942     PASS      03:30:42Z
2026-07-15   34,942   34,942   34,942     PASS      03:30:42Z
```
(silver counts from parquet metadata; source counts re-counted from the gzip JSONL — both denominators
counted fresh this window, not inherited.)

**July trading-day gap census: 10 of 10 expected trading days present, missing = [] (expected set from
lib/trading_calendar.py; positive control 2026-07-16 present).** The July Inflection orion chain is
COMPLETE at monolith bronze + silver.

## Phase 3

Re-run within the window: identical (the tables above ARE the re-run output; no drift).

## Acceptance criteria: 1 ✓ (exact counts, explicit-Z) · 2 ✓ (10/10, denominator printed) · 3 ✓ (zero
hand-fires; scheduled-pass artifacts only) · 4 ✓ (rule cited verbatim) · 5 ✓ (session log Compiler Tools
rows) · 6 ✓ (Andrew's-window carrier was 3F-B7, closed CVO-verified; nothing new touched it).

Downstream note: gold/served regeneration over the now-complete silver rides the normal nightly chain —
nothing fired ad hoc, per the no-ad-hoc-gold-runs law.
