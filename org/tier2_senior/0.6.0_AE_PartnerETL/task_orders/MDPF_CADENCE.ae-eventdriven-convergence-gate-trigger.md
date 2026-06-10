<task_order>
<metadata>
  <to_id>MDPF_CADENCE</to_id>
  <project>MDPF_CADENCE (Andrew-sovereign Inflection cadence-sync; CVO originator, CTO design-ruled)</project>
  <title>AE: replace MDPF weekday cron with an event-driven CONVERGENCE GATE — EventBridge on INF spine sentinel + in-Lambda PER-SOURCE-vintage BD-silver freshness precondition</title>
  <assigned_to>0.6.0_AE_PartnerETL</assigned_to>
  <issued_by>1.0.0_SA_CTO design ruling 2026-06-08T1415Z + precondition-confirm 1417Z (CVO originator). COO sequences + registers.</issued_by>
  <issued_date>2026-06-08</issued_date>
  <status>in_progress</status>
  <priority>Gate BUILT + DEPLOYED (eventbridge S3-sentinel rule replaced cron, IAM granted, DLQ alarm live, DLQ=0). Remaining close gates: AC3 simulated weekend-fire proof (COO GO 2026-06-10 — build independent of the INF_D_08 spine stall) + AC6 RAVC2. Status flipped staged→in_progress per COO 2026-06-10T1307Z.</priority>
</metadata>

<scope>
## Design of record (CTO ruling — 3 messages 2026-06-08, inbox read/)
The root bug: MDPF rollup ran on a weekday-only cron `cron(0 15 ? * MON-FRI *)` -> missed the Sat T+1 INF reconciliation that advances the spine on weekends. Fix = sync MDPF to the INF spine event + a cross-firm source-readiness gate.

## Two rollup sources (DIFFERENT pipelines, DIFFERENT calendars)
- **Inflection:** opal-data-inf spine, sentinel `gold/meta/pipeline-complete.json`, ~10:13/10:21 UTC **DAILY incl weekends** (the Sat T+1 reconciliation advances it).
- **49financial:** BD silver (opal-data-bd `silver/allocations/{date}.parquet` + `silver/fees`), produced by the **weekday-only Path-A ETL (~21:40Z Mon-Fri)** — the wse_49f feeder reads these, NOT the INF spine.
The single `mdpf-daily-trigger` runs the WHOLE chain (all feeders + mdpf_aggregate_aua, partners {inflection, 49financial}). INF-sentinel-ALONE would re-run the 49F feeder against possibly-stale BD silver -> transposes the bug to 49F.

## Mechanism (ruled)
1. **EventBridge:** replace the weekday cron with an **S3-ObjectCreated rule on the INF spine sentinel** `opal-data-inf/gold/meta/pipeline-complete.json` -> `mdpf-daily-trigger` (same pattern as inf-silver-chain / inf-assets-trigger; opal-data-inf has EventBridge enabled). DELETE the old weekday cron fully (no double-fire). TF-vs-live clock drift becomes moot (fire on sentinel, no absolute clock) — keep a one-line TF comment noting live spine time for ops.
2. **In-Lambda PRECONDITION (precondition-only — NOT a BD sentinel, NOT two-event convergence):** before dispatching, `s3:HeadObject` the ACTUAL artifact the feeder reads — `silver/allocations/{BD-expected-vintage}.parquet` (+ silver/fees) — verify-the-served-artifact discipline (a gold-chain-complete EventBridge event would be a wrong-layer/stale-able proxy). Dispatch only when both sources fresh-vs-their-own-cadence.
3. **>>> LOAD-BEARING CONSTRAINT (CTO 1417Z — get this right or the gate misfires) <<<** Evaluate EACH source against ITS OWN expected-vintage, NOT a shared date / NOT date-equality:
   - INF spine: daily-incl-weekend+holiday calendar -> expected = today's trading-or-reconciliation vintage (sentinel just fired -> ~always true).
   - BD silver: WEEKDAY-only Path-A calendar -> on a weekend there is NO new BD silver; **Friday's IS the correct latest**. Require "BD silver at-or-after its OWN most-recent-expected weekday vintage," NOT "BD as_of == INF as_of."
   - **Net gate semantic:** dispatch when INF spine advanced for today AND BD silver >= its own most-recent-expected weekday vintage. Fires DAILY incl weekends (reconciled INF + Friday's BD); defers ONLY on a genuine BD Path-A miss/delay.
   - **Failure if violated:** naive date-equality FALSE-DEFERS every weekend (waits for a BD silver that never lands Sat/Sun) -> reintroduces the weekday-only bug at the gate. The feeder already "rolls forward to the latest spine date on-or-before as_of," so a fresh-but-older BD weekend vintage is CORRECT input.
4. **Reuse** `mdpf-freshness-checker`'s trading-day expected-vintage primitive (holiday set + weekend logic), **PARAMETERIZED PER-SOURCE** (INF = daily-incl-weekend+holiday; BD = weekday Path-A). Factor into a shared helper if clean — do NOT reinvent.
5. **Defer path:** if BD stale, do NOT dispatch -> log "deferring: BD silver stale for {date}" + bounded EventBridge recheck (~30min until a cutoff). Steady state BD is fresh by 10:13 -> gate passes immediately; defer is the rare safety net.
6. **KEEP** the `mdpf-freshness-checker` alarm — now also catches a defer-loop that never resolves (rollup as_of stops advancing -> staleness alarm).

## Explicitly OUT of scope
- **NO BD silver-ready sentinel in this TO (CTO hard-no):** adding one is a bd-gold-pipeline change (gold_dispatch.sh / Path-A) that expands blast radius into the pipeline GLDINC is actively incrementalizing — no concurrent churn. Future-cleanliness item (a BD silver-ready sentinel benefits multiple consumers; fold into a later GLDINC/BD-hygiene pass). BD currently emits only a custom EventBridge `bd-pipeline.gold-chain`/`chain-complete` event (gold_dispatch.sh:661) — wrong layer for this gate.
- **Output contract UNCHANGED:** only WHEN the chain fires changes. `mdpf_aggregate_aua` rollup logic + artifact shape (the MDPF_COUNTS-validated count-population state closing today) UNTOUCHED — no risk to that validation.

<acceptance_criteria>
- [ ] AC1 — eventbridge.tf: S3-ObjectCreated rule on opal-data-inf/gold/meta/pipeline-complete.json -> mdpf-daily-trigger; old weekday cron rule DELETED (no double-fire). TF comment notes live spine time.
- [ ] AC2 — mdpf-daily-trigger/lambda_function.py: per-source-vintage precondition (INF daily-incl-weekend calendar AND BD weekday-Path-A HeadObject freshness, NOT date-equality) + bounded recheck on BD-stale defer. Reuses mdpf-freshness-checker expected-vintage logic parameterized per-source.
- [ ] AC3 — WEEKEND CORRECTNESS PROOF (the load-bearing test): demonstrate the gate FIRES on a simulated Sat/Sun (reconciled INF advanced + Friday's BD silver as latest-expected), does NOT false-defer. This is the regression the whole ruling exists to prevent.
- [ ] AC4 — comp-iam service mdpf-daily-trigger confirms/adds opal-data-bd silver s3:HeadObject/GetObject perm BEFORE apply.
- [ ] AC5 — Deploy per CLAUDE.md: commit -> source-map -> plan -> safe-apply (HALTGT) -> 0-diff -> record-deploy -> tag. Output contract regression-checked (mdpf_aggregate_aua artifact unchanged).
- [ ] AC6 — RAVC2 CTO + COO + CVO (originator) with deploy evidence + the weekend-fire proof.
</acceptance_criteria>

<compiler_tools_mandate>
- Before: comp-iam service mdpf-daily-trigger (BD silver read perm); comp-blast mdpf-daily-trigger + the cron rule (confirm no other consumer of the weekday cron).
- Before apply: .tools/safe-apply.sh (HALTGT checkpoint).
- After: 0-diff plan; comp-iam gaps if iam.tf changed.
</compiler_tools_mandate>
<cross_domain_coordination>opal-data-inf spine sentinel (INF/DS-owned — read-only event trigger). opal-data-bd silver (AE/DS — read-only HeadObject). mdpf-freshness-checker (shared expected-vintage primitive — parameterize per-source, don't fork). NO bd-gold pipeline change (GLDINC incrementalization in flight — keep blast radius out). COO sequences behind CMPAWS D-list + 15:55Z one-shot + registers MDPF_CADENCE. CVO originator.</cross_domain_coordination>
</scope>
</task_order>
