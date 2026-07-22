<task_order>
<id>MDPF_3FIRMS.3F-G8b</id>
<title>Cottonwood appended daily model-snapshot series — FORWARD-APPEND-ONLY, consumes G8, never re-derives</title>
<project>MDPF_3FIRMS</project>
<workstream>WS-G (Gold) — G8 EXTENSION, same B5-gate</workstream>
<issued_to>0.4.0_DS_ClientPlatform</issued_to>
<advisory>4.0.0_SA_CRO — authored the snapshot spec @26f218a75; holds the source-keying design. Consult, do not re-derive.</advisory>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_at>2026-07-22T22:31Z</issued_at>
<status>staged</status>
<authorization>Andrew-direct to CRO ~2210Z (spec @26f218a75) -> CTO ruling 222856Z (bindings below) -> COO wiring. Custody of the Andrew verbatim is CRO's.</authorization>

<references>
  <ref type="prd">docs/architecture/MDPF_3FIRMS_PRD.md — v1.19 fold coming from CTO; §5 ruling 10 (backfill developing subject, COTTONWOOD-ONLY, unchanged)</ref>
  <ref type="spec">4.0.0_SA_CRO daily model-holdings snapshot spec @26f218a75</ref>
  <ref type="predecessor">3F-G8 (the current-state Portfolio-Analytics pair) — this consumes its output</ref>
</references>

<scope>
Append a **daily model-snapshot series** for Cottonwood: per opal model, the daily allocation count + value,
accumulated forward one day at a time. **It CONSUMES 3F-G8's output with ZERO re-derivation** — G8 already
computes the per-model decomposition; this series records G8's result each day and appends it. It does not
recompute the decomposition, re-read the rebalancer, or re-run the crosswalk.

**FOUR CTO BINDINGS (his ruling 222856Z) — all four are hard:**
1. ⛔ **G8 CORE FIRST.** The portal pair (account-distribution + aum-metrics, 3F-G8) **NEVER waits on this
   appender.** G8 ships on its own gate; G8b rides behind it. If sequencing them ever forces G8 to wait,
   G8b yields — the served product is G8, not the series.
2. ⛔ **GOLD ARTIFACT -> NO `fact_` PREFIX.** The naming law binds: `fact_*` is a SILVER completeness-table
   name; this is a GOLD projection/series. **DS finalizes the name in the `dim_*`/series family** (e.g. a
   `dim_`-family series name), never `fact_`. Getting this wrong is the same class as the `_s{N}` LAW-1
   defect — a name asserting the wrong layer.
3. ⛔ **FORWARD-APPEND ONLY.** Each day appends that day's snapshot. **No historical rewrite. No backfill.**
   The appender writes today's row and never a past one.
4. ⛔ **CRO's SOURCE-KEYING so future backfill is NON-CONFLICTING but NEVER ENABLED by the appender.** The
   rows carry CRO's source-key design (from @26f218a75) so that IF a CTO-gated backfill design later lands,
   it can populate past dates **without colliding** with appender-written rows. **But the appender itself
   NEVER writes a past date** — ruling 10 (backfill = developing subject, CTO-gated) is UNCHANGED. The
   source-keying makes the series *forward-compatible with* a future backfill; it does not *perform* one.

⚠ **THE DISTINCTION THAT MATTERS (and it is exactly the developing-subject boundary): this TO builds an
APPENDER, not a BACKFILL.** An appender that starts today and grows forward is in-scope and unblocked. A
past-date write is backfill EXECUTION, which is outside every current dispatch and CTO-gated. The
source-keying is the seam that lets those two coexist later without contradiction — design the seam, never
cross it.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>Read CRO's spec @26f218a75 + request the source-keying design BEFORE authoring the appender</run>
      <expect>Snapshot shape + source-key scheme in hand; you implement to it, not a re-derivation.</expect>
      <if_mismatch>If the spec is ambiguous on source-keying, MCP CRO — do not invent a key scheme that a future backfill cannot align to.</if_mismatch>
    </step>
    <step>
      <run>comp-pipescript io on the 3F-G8 producer + the intended appender</run>
      <expect>The appender READS G8's output only; WRITES the series artifact only. No rebalancer/crosswalk reads (that would be re-derivation).</expect>
      <if_mismatch>Any read of a G8 INPUT (rebalancer, fact_holdings, crosswalk) means you are re-deriving, not consuming. STOP and re-scope to consume G8's OUTPUT.</if_mismatch>
    </step>
    <step>
      <run>comp-blast on the series artifact name candidate (now monolith-resolvable per PRD v1.18) + naming-law check</run>
      <expect>Name is in the dim_/series family, NOT fact_. No collision with an existing artifact.</expect>
      <if_mismatch>A fact_-prefixed gold artifact is a LAW-1-class naming defect — rename before writing.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>.tools/commit-gate.sh on every .py touched</run>
      <expect>py_compile + ds-precommit-check + ruff clean; `from __future__ import annotations` present.</expect>
      <if_mismatch>STOP.</if_mismatch>
    </step>
    <step>
      <run>comp-validate &lt;appender&gt; --artifact &lt;emitted series&gt;</run>
      <expect>PASS or WAIVED.</expect>
      <if_mismatch>NO_CONFIG/ZERO_CHECKS = UNVALIDATED, never signal SAFE.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>Prove FORWARD-APPEND: run two consecutive days; day 2 ADDS a row, day 1's row is BYTE-IDENTICAL (ETag)</run>
      <expect>Append-only proven as a positive AND negative control — a new row appears; no existing row changes.</expect>
      <if_mismatch>⛔ ANY change to a prior day's row is a forward-append violation — STOP and escalate. This is the whole guarantee.</if_mismatch>
    </step>
    <step>
      <run>Confirm the series appears in the NIGHTLY-EMITTED staged set (not an ad-hoc run)</run>
      <expect>Present, consuming G8's same-nightly output.</expect>
      <if_mismatch>⛔ No ad-hoc gold run to validate (NEVER#4). Validate on the scheduled nightly.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<data_reprocess_scope>
  <no_reprocess_needed>Forward-append only. No historical partition is written or rewritten. The appender
  begins from its first run date and grows forward; past dates are the province of a future CTO-gated
  backfill, which this TO makes non-conflicting via source-keying but never performs.</no_reprocess_needed>
</data_reprocess_scope>

<cross_domain_coordination>
  <resource path="3F-G8 output" shared_with="0.4.0_DS (3F-G8 — same lane, same B5 gate)">
    G8 CORE FIRST is binding. Author G8b so it can never block G8. If they contend, G8 wins.
  </resource>
  <resource path="source-keying design" shared_with="4.0.0_SA_CRO">
    CRO's spec + key scheme. Consult; do not re-derive. The key is what a future backfill aligns to.
  </resource>
  <resource path="ruling 10 / backfill developing subject" shared_with="1.0.0_SA_CTO">
    The appender must be forward-compatible with a future backfill WITHOUT enabling one. If the
    source-keying design appears to require writing a past date, STOP — that crosses the gate.
  </resource>
</cross_domain_coordination>

<dependencies>
  <dependency agent="0.4.0_DS_ClientPlatform" task="MDPF_3FIRMS.3F-G8" status="staged" blocking="true">
    Consumes G8's output; G8 must be built and core-first. Same B5 (~03:30Z) gate.
  </dependency>
</dependencies>

<acceptance_criteria>
1. An append-only daily model-snapshot series that CONSUMES 3F-G8's output with ZERO re-derivation
   (proven by comp-pipescript io: reads G8 output, not G8 inputs).
2. G8 CORE FIRST demonstrably preserved — the appender cannot delay the portal pair.
3. Artifact named in the `dim_`/series family, NEVER `fact_` (naming law).
4. FORWARD-APPEND proven on both sides: day-2 run adds a row, day-1 row byte-identical by ETag.
5. CRO's source-keying carried so a future backfill is non-conflicting — with NO past-date write performed
   by the appender (ruling 10 unchanged).
6. Series present in the nightly-emitted staged set; no ad-hoc gold run.
7. Session log Compiler Tools section reproduces every `<run>` with observed output and pass/fail.
</acceptance_criteria>

<escalation>
Report to 2.0.0_SA_COO; CTO gates. Escalate immediately if the source-keying design appears to require a
past-date write (that crosses ruling 10's gate), or if G8b sequencing would force G8 to wait.
</escalation>
</task_order>
