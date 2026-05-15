<task_order>
  <metadata>
    <id>ADVI_TXNAMG.003</id>
    <slug>dsd-amalgamating-writer</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~D</issued_to>
    <date>2026-05-15</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>HELD until ADVI_TXNAMG.001 (TO-1) brief is delivered and validated by COO — TO-3 needs TO-1's definitive join column set + confirmed join key + historical/daily schema-parity verdict. COO releases dispatch_held on TO-1 RAVC2 validation. Same receiver (DS~D) — TO-1 then TO-3 sequential in-lane. RELEASED 2026-05-15 by COO — TO-1 RAVC2 validated (brief docs/briefs/txnamg-001-join-key-column-audit-20260515.md; AC1-5 PASS; the 11-column join set, confirmed join key, and schema-parity verdict are all delivered — see to1_contract). TO-3 is GO.</dispatch_unblock_condition>
    <project_code>ADVI_TXNAMG</project_code>
    <priority>P1 — the core deliverable: establishes the single canonical silver/transactions writer. Gates TO-4 (Lambda trim) and TO-6 (INFINC.006 resume).</priority>
    <sla>~6-8h wall post-unblock + 1-2 chain-validation iterations.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/ADVI_TXNAMG.md (PRD v0.1, commit e7fecbf93) — §3 architecture + sequencing invariant, §4.1 component spec, §6 TO-3.</prd>
    <input>ADVI_TXNAMG.001 deliverable — docs/briefs/txnamg-001-join-key-column-audit-20260515.md (DELIVERED + COO-validated 2026-05-15, AC1-5 PASS). The brief's §4 "Deliverables to TO-3" is the binding no-ambiguity contract — transcribed into to1_contract below.</input>
  </references>

  <to1_contract>
    From the COO-validated TO-1 brief (docs/briefs/txnamg-001-join-key-column-audit-20260515.md, §4 "Deliverables to TO-3") -- the binding no-ambiguity contract for this writer:
    JOIN KEY: REST `id` (left spine) == Custom-Report `Transaction ID` (right). 100% key fidelity wherever the account exists in the REST spine. `orderId`/`tradeOrderId` are 100% NULL in REST bronze -- not keys.
    CARRY EXACTLY THESE 11 Custom-Report-unique columns (from bronze/orion-api/*/transactions.csv): LName, Activity Category, Dwnld Symbol, CreatedDate, CreatedBy, EditedDate, EditedBy, RepName, CurrentAccountValue, CurrentCashValue, Managed Account. camelCase silver naming is a TO-3 call; the SET is binding.
    DO NOT CARRY the other 18 -- 17 are aliases of existing REST columns; `fkTradeStatus` is an encoding variant of REST `status` (TO-1 recommends not carried; absent a CTO override, do not carry).
    CSV HEADER HYGIENE: the Custom-Report CSV header carries whitespace artifacts (e.g. ` Reg ID` with a leading space) -- TO-3 MUST `.str.strip()` the CR CSV headers when reading the join source.
    NO PER-ERA RECONCILIATION: schema parity is confirmed identical across all 14 sampled CSVs 2020-05-26 -> 2026-05-14; the per-era-drift reconciliation item in scope below is MOOT -- no reconciliation logic needed.
    CLOSED-ACCOUNT / UNION FLAG (brief §1.2): the REST pull iterates currently-existing Orion accounts, so the REST spine excludes accounts closed before the pull date -- a left-join-onto-REST-spine drops ~5% of deep-backfill (2021-era) Custom-Report transactions on now-closed accounts. PRD §4.1 as ratified specifies LEFT-JOIN -- BUILD THAT, it is the working directive; do NOT block on the flag. COO has surfaced the left-join-vs-UNION question to CTO in parallel (a PRD §4.1 amendment question). Structure the writer so that, IF CTO later rules UNION, appending the Custom-Report-only rows (id absent from the REST spine; REST-spine columns NULL) is a clean ADDITIVE extension -- do not architect the join in a way that forecloses it.
  </to1_contract>

  <context>
    silver/transactions/{date}.parquet has two live daily writers (PRD §2). This TO makes convert_transactions_to_silver.py the SOLE canonical writer by amalgamation: the REST full-history spine, left-joined with every Custom-Report-unique column by Orion transaction id. The Custom-Report enrichment source already spans the full history (bronze/orion-api/*/transactions.csv — 1,509 files, 2020-05-26→present, already backfilled May 2026 — PRD §2.2). Writer #2 already emits a full-history snapshot every run, so TO-3's first run produces the entire transaction history amalgamated into one partition — there is NO separate 6-year re-pull and no separate "re-run history" step (PRD §4.1). Andrew's "consolidate the backfill data" was already done; this TO consolidates the WRITE FUNCTION.
  </context>

  <objective>
    convert_transactions_to_silver.py is the single writer of silver/transactions/{date}.parquet, emitting a camelCase Rule-17 amalgamated frame: REST spine + the TO-1 join column set, populated on Custom-Report-overlap rows and NULL elsewhere.
  </objective>

  <scope>
    <item>Extend convert_transactions_to_silver.py to read the ACCUMULATED Custom-Report bronze: bronze/orion-api/*/transactions.csv — all ~1,509 historical files, 2020-05-26→present. This is a cumulative/rolling read, NOT same-day-only (PRD §4.1 cadence constraint: the gold chain runs ~06:00 UTC; the Custom-Report CSV for date D is not pulled until D+1 13:00 UTC — so today's rows pick up enrichment on the next run, a ≤1-2-day lag, immaterial).</item>
    <item>LEFT-JOIN the TO-1-defined Custom-Report-unique column set onto the REST spine by the TO-1-confirmed transaction-id key. This is a Rule-17 JOIN-enrichment — same class as the existing rep_id-from-accounts_v2 join. Carry every column TO-1 classified "genuinely absent from REST"; do NOT join the alias columns (REST already carries them).</item>
    <item>Join semantics: the Custom Report 28198 is type+rep-filtered → a strict subset of the REST row set. Joined columns are populated ONLY on overlap rows, NULL elsewhere. NULL = "outside Custom-Report scope" — Rule-17-correct; NO business-default fillna, NO dropna, NO row filtering on the joined columns.</item>
    <item>Error case: missing/empty Custom-Report bronze for a window → emit REST-spine silver with the joined columns NULL, log loud. NEVER fail the gold chain on a missing enrichment source.</item>
    <item>If TO-1's schema-parity verdict found backfill-era vs daily CSV column drift, reconcile per-era so the join column set is consistent across the full history.</item>
    <item>Incremental-compatibility: the join must work join-by-id within a window (PRD §4.6 — INFINC.006 Pattern E resumes on this consolidated writer later; do not design the join in a way that only works on a full-history pull).</item>
  </scope>

  <acceptance_criteria>
    <ac id="AC1">Exactly one writer of silver/transactions/ — convert_transactions_to_silver.py. Output is camelCase Rule-17 + the joined Custom-Report-unique columns.</ac>
    <ac id="AC2">Full-history rows enriched: a transaction with a Custom-Report match carries the joined columns; spot-check a 2021 and a 2023 transaction empirically (PRD §6 TO-3 P3).</ac>
    <ac id="AC3">Joined columns populated-on-overlap / NULL-elsewhere — empirically asserted; no fillna of business defaults; no rows dropped for NULL joined columns.</ac>
    <ac id="AC4">Rule-17 clean: ds-precommit-check.py confirms JOIN-enrichment only — no output_cols field-slimming, no business fillna, no business-logic row filtering. from __future__ import annotations first import.</ac>
    <ac id="AC5">Chain-run empirical: schema assert + row-count assert vs the pre-TO-3 REST-only baseline (row count preserved; column count = REST + joined set).</ac>
    <ac id="AC6">No emoji. safe-deploy.sh cycle PASS + comp-pipescript deployed MATCH before signaling.</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>Phase 1 (before writing): comp-pipescript io convert_transactions_to_silver.py + ds-precommit-check.py awareness (Rule-17 — the edit must be JOIN-enrichment, NOT field-slimming and NOT business fillna). Phase 2 (before commit): ds-commit-gate.sh (py_compile + ds-precommit-check.py + ruff --target-version py39). Phase 3 (after commit): safe-deploy.sh cycle; chain-run + schema/row-count assert + joined-column populated-on-overlap / NULL-elsewhere assert + historical-row (2021/2023) enrichment spot-check. Copy verbatim per PRD §6.</compiler_tools_mandate>

  <cross_domain_coordination>
    GATED BY TO-1 (ADVI_TXNAMG.001, DS~D) — needs the join column set + key + schema-parity verdict. SEQUENCING INVARIANT (PRD §3): TO-3 lands BEFORE OR SAME-WAVE AS TO-4 (ADVI_TXNAMG.004, AE 0.7.0 — removes writer #3's silver-write) — NEVER the reverse. The consolidation must never produce a zero-writer window: writer #2 is continuously live and TO-3 extends it; TO-4 removes writer #3 only after TO-3 is live. On TO-3 ship, COO releases TO-4's dispatch_held. Shared S3 keys: silver/transactions/ (this TO is the writer), bronze/transactions/ + bronze/orion-api/*/transactions.csv (read). TO-2 (DS~B consumer migration) Phase C confirmation-run gates on this TO shipping. Coordinate the silver-stage deploy with AE 0.7.0 (TO-4) so the two land in-wave.
  </cross_domain_coordination>

  <data_reprocess_scope>
    TO-3's first run produces the full amalgamated transaction history in one partition (writer #2 emits a full-history snapshot; the Custom-Report enrichment source already spans 2020-05-26→present). No separate historical re-pull, no 6-year backfill job. Stale per-date silver/transactions/ partition housekeeping is TO-5 scope (gated on §7-Q1), NOT this TO.
  </data_reprocess_scope>

  <deliverables>
    <item>convert_transactions_to_silver.py amalgamating writer — committed + pushed CLOUD + S3-uploaded per the DS deploy cycle (CLAUDE.md Rule 13).</item>
    <item>Chain-validation evidence (schema/row-count/enrichment asserts).</item>
    <item>Session log with Compiler Tools section + RAVC2 to COO + CC CTO + AE 0.7.0 (TO-4 sequencing coordination).</item>
  </deliverables>

  <ravc>DS~D RAVC2 to COO + CC CTO + AE 0.7.0 on AC1-6 PASS. The RAVC2 receipt is the signal COO uses to release TO-4's dispatch_held (sequencing invariant §3).</ravc>

  <notes>
    The amalgamation carries Custom-Report-unique columns that have ZERO current consumers — that is Andrew's explicit forward-looking preservation directive (PRD §1), not a mistake and not something to re-gate. Sparse joined columns (NULL on non-overlap rows) are correct. This is the same Rule-17 JOIN-enrichment class as the existing accounts_v2 rep_id join — if ds-precommit-check flags it, the flag is a false positive on a legitimate join; document and proceed. INFINC.006 (Pattern E) resumes on this consolidated writer as a separate TO once TO-3 + TO-4 ship.
  </notes>
</task_order>
