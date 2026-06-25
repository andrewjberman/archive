# NFRA_COMPRAIL TO-6 LEG-C — Gate-1 Enforce Announce (announce-then-enforce)

**Issued:** 2026-06-25 ~13:40Z by 2.0.0_SA_COO (LEG-C announce-relay)
**Build:** CTO commit a62b63e46 (Gate-1, flag-OFF, FP-test 14/14 PASS)
**Scope decision:** OPTION (a) — narrow as-built scope (CTO rec). Option (b) (escalate s3_artifact/portal data-script grep classes) DEFERRED pending TO-5 RUN-GREP-vs-ROUTE telemetry.

## Grace window
- **Announced:** 2026-06-25 ~13:40Z
- **ENFORCE FLIP:** 2026-06-26 ~14:00Z (~24h grace — institutional safe default for a fabric-wide deny)
- **Flip mechanism:** `: > org/mcp/comprail-gate1.enforce` (create the marker = enforce ON). Rollback = remove the marker (instant, reversible).
- **Flip owner:** 2.0.0_SA_COO (primary, if a COO session is live at grace-end); **1.0.0_SA_CTO authorized as backstop** to flip at grace-end if no COO session is live (mechanism-owner). CC CVO for LEG-D.

## ANNOUNCE BLURB (fabric-wide)
comp-rail Gate-1 enforce (NFRA_COMPRAIL / LD-0207): starting **2026-06-26 ~14:00Z**, a BARE recursive repo grep over estate data-scripts (`grep -r` / `grep -R` / `rg` / `find` over `data/*/scripts` etc.) will be **DENIED** with the comp-which guidance. Reach for `comp-which "<question>"` first, OR append `# rail-checked: <why>` for a justified one-off, OR `/freeform` for a time-boxed speed push. **UNAFFECTED:** pipe-greps (`cmd | grep`), single-file greps, non-estate/new-project searches, the deck carve-out, and native Grep/Glob tools (Andrew-direct: native NEVER deny). comp-which now routes all 28 tools, so the rail no longer dead-ends. Rollback is instant.

## Why narrow-first (a)
The comp_which-scoped deny surface is empirically narrow — most estate greps already hit specific advisory classes or already-deny (infra). Gate-1-as-built denies mainly bare `grep -r X data/<firm>/scripts/`. Incremental enforcement (prove the gate behaves, low friction) beats a big-friction first flip; TO-5 telemetry decides whether (b) is warranted.

## Legs
- LEG-A (CTO): Gate-1 build flag-OFF + AC#5 FP-test PASS — DONE (a62b63e46).
- LEG-C (COO): this announce + the grace-end marker flip — IN PROGRESS (announced; flip 06-26 ~14:00Z).
- LEG-D (CVO): post-enforce no-over-gate cert + RUN-GREP-vs-ROUTE telemetry — gated on the flip.
