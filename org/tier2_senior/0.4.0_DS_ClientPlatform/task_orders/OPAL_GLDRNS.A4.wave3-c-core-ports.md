# OPAL_GLDRNS.A4 — Wave-3 C-core ports (the seed G2/G4/G5/G6 family → monolith gold)

<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project OPAL_GLDRNS, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: pending -- LIVE, respec-before-execute (2.0.0_SA_COO 2026-08-05 ~0105Z, verdict by 0.4.0_DS_ClientPlatform read against the actual ruling text, not commit subjects). Andrew's 2026-08-05 canonical-medallion ruling (@9dbbb5230e) ratifies the DIRECTION this TO already targets (off opal-data-bd, into the opal-data-assets monolith) -- NOT stale, do not close as superseded. But "monolith gold grammar" as originally scoped is now under-specified: the ruling's own §4(a) names a top-level `gold/` as NON-canonical (vendor/firm grain violation); the target must be pinned to `{vendor}/{firm}/gold/` before any leg executes. Also predates the platinum serving tier -- any leg emitting a serving artifact needs re-reading against it. NOT AUTHORIZING MIGRATION of anything already landed (Andrew's ruling explicitly: direction ratified, migration not authorized) -- this governs new work under A4 only. Related residue, same night: W-1a (MDPF_CANRTE) wrote to the same non-canonical top-level `gold/mdpf_revamp/` path under a separate CTO ruling specific to the live tree; self-flagged by DS, not this TO's concern, noted for whoever eventually runs the §4(a) migration.</status>
**Assignee:** 0.4.0_DS_ClientPlatform~A · **Author/gate:** 1.0.0_SA_CTO · **Cut:** 2026-07-16 ~13:1xZ
**Authority chain:** the Andrew-ratified A-to-D build plan §Wave-3 (`docs/architecture/OPAL_RUNNERS_49F_BUILD_PLAN.md`
@ baba79230) + OPAL_CONSOLIDATION WS-C (S3) + Andrew's standing tempo mandate (the /drive consolidation
end-to-end wording, LD-0302). Inputs landed: C_03 spec fold w/ the hold refinement (9ec609751), M1/M6
spec cells SIGNED (065e0e289), the Wave-2 incremental machinery proven live (run-2 + C_03 first-live
07-16 09:52Z, SCD2 catch fixed 43/43).

## Scope — the C-core ports, in sequence

Per the plan verbatim: *"re-source seed logic fact_→dim_, re-home outputs seed `opal-data-bd/canonical/…`
→ monolith gold grammar, orchestrator = the seed's `build_canonical_daily.py` pattern re-pointed
(idempotent per-date roll-forward survives). Per-script casebook entry lands WITH each port (B_00 entry
first — the ruled-unacceptable core gets its write-up)."*

| Leg | Unit | Notes / ruled cells folded |
|---|---|---|
| L0 | **B_00 casebook entry** (write-up only, no port) | The plan's named FIRST motion — the ruled-unacceptable core gets its record before any further C work builds on its outputs |
| L1 | **C_00-core** (the G-family core port ~A's lane already sequenced) | Seed logic re-sourced fact_→dim_; fixture-first per the Wave-2 pattern; main() refuses live until the runner wires |
| L2 | **C_02.client_performance** | **M1 folds here as SIGNED** (065e0e289): served firm-AUA = C_02's computed total, GATED by C_04 flag state at emit; degenerate floor `> 0` REFUSE-LOUD (threshold verbatim from D_00.portal_aggregates.py:246-285 @ 69d6a5624; hold-last-good RETIRES per D5); cross-contract SUM(C_01 rows)==C_02 rows row-for-row |
| L3 | **~~M4: canonical-prices promotion~~ RETIRED BY ANDREW-DIRECT (verbatim @ acabb3553, 07-16 ~14:1xZ): "any kind of transaction-based pricing framework is deprecated"; the canonical-prices schema "only mattered because we had to reprice based on transactions" and is "unnecessary" on daily RPS-snapshot holdings.** REPLACEMENT LEG: `pct_priced` on C_01/C_02 re-defines as a STATEMENT-PRICE COVERAGE measure (fraction of position rows carrying the statement's own closing_price -- the coverage the built graph actually depends on); one spec line each, superseding the signed M4 rider with the verbatim anchor. Transactions remain FLOWS-ONLY (the F-AMT chain -- already conformant) |
| L4 | **Remaining C-core (G2/G4/G5/G6 residue after L1-L3 mapping)** | Map the G→C correspondence explicitly in L0's casebook entry set — the record, not tribal memory, carries which seed script became which C unit. **Any seed script whose purpose is the price MATRIX (build/consume) = DEPRECATED-NOT-PORTED per acabb3553 -- the mapping records the retirement with the verbatim anchor, ports nothing** |
| L5 | **WP7 authoring half (cross-batch, Rule 13):** the seven Schwab converters' monolith re-point | DS authors the converter changes (unzip-AT-READ — 17a: bronze stays as-delivered, the double-unzip belongs in the reader); 0.5.0 carries deploy + bridge/OneDrive/01_raw retirement; sequence AFTER L1-L2 or interleave at your judgment — state the choice in your first RAVC |

## Standing law folded into every leg

1. **Fixture-first, evidence bar IN CODE** (the C_03 precedent: a bar in a message is remembered, a bar
   in code fires) — every hold/census prints denominators; zero-anomaly holds discriminate
   instrument-vs-day (the 9ec609751 refinement pattern: HOLD on discriminator-contradiction, WARN-and-ship
   with a visible line on quiet days).
2. **Measure the estate before building on a column** — the F-SSN/txn_class/Decimal triple-lesson:
   `pq.read_schema` on the real partition beats any doc; a discriminator keyed on an absent column is a
   silent zero forever.
3. **Rule 17/17a untouched**: silver stays dedup+dtype passthrough; C-group is where judgment lives.
4. **Cross-cutting changes land at EVERY call site** (runner bytes + Lambda bytes + catalog invocation —
   census call sites, not files) and **deploy manifests census the IMPORT CLOSURE** (ecf2eb72c).
5. **PROFILING DUTY (the Andrew open cell)**: profile each ported C table's runtime/memory at 0833+0824
   volumes and REPORT with denominators — Wave-3 profiling is what decides the rust/polars question
   ("likely none at 0833 volumes — decide then"); the numbers go to Andrew's deferred call, not to a
   unilateral adoption.

## Verification (the plan's §Waves-3-4 law, verbatim-in-substance)

Per script: (i) **seed-vs-port output identity on ONE date** — same logic, new home, should tie EXACTLY;
(ii) THEN port-vs-legacy with named-divergence accounting (every divergence carries a design-class name,
the W-2 pattern); (iii) C_02/C_03 cross-contract preserved (SUM(account)==relationship row-for-row);
(iv) listing-verified landings; (v) run 3+ of the incremental machinery keeps first_seen continuity.

## Gates

- CTO per-family code review (the standing pattern) + apply gates on any infra motion (0.7.0 vehicle).
- D-group stays PARALLEL-NOT-SERVING until the Wave-5 parity streak — nothing in this TO serves.
- Live runs ride the now-scheduled machinery (the P0 wave's schedulers); no ad-hoc gold runs (NEVER#5).
- Sovereign-worded cells queue to Andrew at their moments (advisor-"type", pre-floor default, FAM/SLM —
  none block L0-L5).

## Acceptance

All legs landed + verified per the law above; the casebook carries one entry per port INCLUDING the G→C
map; profiling numbers reported; WP7's authoring half handed to 0.5.0 with the interface contract. TO
flips complete in the close commit per the lifecycle-rides-the-close pattern.
