<task_order>
<id>MDPF_3FIRMS.3F-P1</id>
<title>MDPF consumption contract audit — every rendered aggregate mapped to {served artifact + producer} OR {FE computation file:line}</title>
<project>MDPF_3FIRMS</project>
<workstream>WS-P (Platinum) — READ-ONLY AUDIT, parallel-safe from day one</workstream>
<issued_to>0.4.0_DE_ClientPlatform</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_at>2026-07-22T20:29Z</issued_at>
<status>complete 2026-07-22 (status corrected 2026-08-21 -- work and ISSUER ACCEPTANCE both predate this flip by a month). ACCEPTED AT ISSUER: COO 205817Z, "both TOs ACCEPTED, RAVC closed" (recorded in logs/2026-07-22/mdpf_3f_p1_ruling12_addendum_close_2125Z.md). EVIDENCE PER CRITERION: (1) locus table + denominator 22/22 aggregates, 9/9 hooks, 10/10 producers -- MDPF_3F_P1_CONSUMPTION_CONTRACT_AUDIT_20260722.md @39ea5916e; (2) 7 FE-computed GLOBAL number classes flagged for 3F-P5, headline the Global trend aggregate FE-summed at ModelPortfolios.tsx:724-731 @08c6d8b2; (3) Andrew's "all client-side" answered MIXED PER-AGGREGATE, not in aggregate; (4) ZERO UNKNOWN PRODUCER, stated explicitly rather than by omission; (5) zero FE modifications -- @39ea5916e touched exactly 2 .md files, verified by git show --stat; (5a) RULING-12 addendum @7a2805d4e, all three sub-parts: producer named (mdpf_aggregate_aua.py:91 @47402a90d; the on-page start is the FE rolling window ModelPortfolios.tsx:1602-1611, NOT a data boundary), verdict EMERGENT (no ruling-zero code path exists), and the provenance-label statement (meta coarse-YES; per-date cohort_provenance EXISTS BUT EMPTY 429/429 None; rendered nowhere); (6) Compiler Tools section present in the 2026-07-22 logs. 6/6 evidenced.</status>
<authorization>LD-0333 am.1 @2eef569d2 -> CTO cascade 200805Z (WS-P audits explicitly parallel-safe from day one).</authorization>

<references>
  <ref type="prd">docs/architecture/MDPF_3FIRMS_PRD.md §4 WS-P row 3F-P1; §2.4 (the partial answer / seed); §3.4 aggregation locus</ref>
</references>

<scope>
**This answers a question Andrew asked directly (§0):** *"need to establish of these aggregations what
are server side and what is client-side. I suspect it is all client-side but this needs to be audited
and documented as well."*

⚠ **HIS SUSPICION IS ALREADY PARTIALLY REFUTED — and that is the finding, not an embarrassment.** §2.4
measured: per-firm data is SERVER-side (firmId interpolated into
`/api/general/mdpf/{firmId}/aggregate-aua-timeseries.json` `:238` and
`json/mdpf/{firmId}/account-distribution.json` `:491` — the id IS the S3 scope segment); Global has its
OWN served artifact (`getMdpfAggregateAUATimeSeriesByFirm('global')` `:477-479`), so the Global TREND is
server-composed, not FE-summed. **Verdict so far: MIXED, not all-client-side.** Client-side computation
exists ON TOP: roll-forward lookups `:365`, totalAUM derivations `:883-886`, unfunded counts
`:1486,:1523`, plus the legacy `['aum-metrics']` / `['aum-timeseries']` / `non_model_assets.json`
fetches from `/api/general/portfolios/*`.

**Deliverable: THE COMPLETE LOCUS TABLE.** Every MDPF-page aggregate mapped to EITHER
{served artifact + producing script} OR {FE computation, file:line}. §2.4 is the SEED, not the answer —
it is explicitly partial.

**Flag every FE-COMPUTED GLOBAL number for 3F-P5 disposition.** Target architecture (§3.4): all Global
COMPOSITION is server-side; FE computes presentation only (deltas, formatting, roll-forward display).
Any FE computation that CREATES a Global number either re-points to a served artifact or is documented
as deliberate.

⛔ **READ-ONLY. No FE changes in this TO** — the builds are 3F-P3/P4/P5 and they gate on WS-G.
</scope>

<addendum id="ruling-12-verify" added="2026-07-22T20:53Z" authority="CTO ruling 205217Z, PRD v1.9 @47402a90d">
**ADDED SCOPE — VERIFY-AND-HARDEN, NOT BUILD. Read why, because the framing is the point.**

CTO ruled (ruling 12) that Inflection's pre-2026-05-15 `model_aum` is **RULING-SOURCED KNOWN-ZERO**, not
missing — so `non_model = total − 0` is correct for those dates. **That ruling was initially framed as a
BUILD. It was WRONG to frame it that way: Andrew showed the live chart and THE BEHAVIOR ALREADY SHIPS.**
Non-Model AUM renders continuously from 2025-07-18 through 2026-07-18; the five model bands appear only
from ~2026-05 onward. **A new code path bolted onto working behavior is how a shipping surface breaks
while someone believes they are adding a feature.**

>> **THE CLASS, named in the PRD: we adjudicated what the system SHOULD do from DOCUMENTS, about
behavior we could have LOOKED AT. No instrument lied — nobody rendered the page.** PRD §1.1 asserts
one-sided dates render as ABSENT; the served Inflection product does not behave that way, and §1.1 will
be corrected FROM THE MEASURED IMPLEMENTATION after you answer this — not before. <<

**THREE QUESTIONS, read-only, inside your existing audit:**
1. **WHAT PRODUCES the pre-migration non-model values?** Name the producer + the artifact, file:line
   @ commit-ish.
2. **IS THERE AN EXPLICIT ZERO-FILL / BOUNDARY, OR IS THE BEHAVIOR EMERGENT FROM THE DATA?**
   ⚠ **This is the decisive one.** If `model_aum` is simply absent/zero in the source and `total − model`
   naturally yields `total`, then **there is NO ruling-zero code path at all** — and CTO's proposed
   guardrail (c) ("structurally impossible to apply to dates >= 2026-05-15") **has no referent to guard.**
   If instead there IS an explicit boundary or fill, name it and say whether it is a named constant or a
   scattered literal.
3. **IS THERE A PROVENANCE LABEL?** Can a consumer distinguish a RULED zero from a MEASURED zero in the
   served artifact? (Likely absent — that is fine; report it, do not add it.)

⛔ **DO NOT IMPLEMENT ANYTHING.** No label, no constant, no guard. Guardrails (b)/(c) are HELD pending
your answer; (a) is evaluated on its merits after. **Answering (2) may dissolve (c) entirely** — which is
the cheapest possible outcome and the reason this is a verify, not a build.
</addendum>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-transform schema-check ModelPortfolios</run>
      <expect>Rendered-field inventory; MISSING entries flagged (a MISSING = runtime undefined).</expect>
      <if_mismatch>Itemize MISSING fields — each is a latent runtime undefined on a SEV1 surface.</if_mismatch>
    </step>
    <step>
      <run>comp-transform fields ModelPortfolios</run>
      <expect>Every data-bound field enumerated as the audit's denominator.</expect>
      <if_mismatch>STATE THE DENOMINATOR of your audit — "N of M rendered aggregates mapped". A locus table without a denominator cannot be assessed for completeness.</if_mismatch>
    </step>
    <step>
      <run>comp-platinum page model-portfolios</run>
      <expect>Full-stack artifact->component map as a cross-check on the FE-side enumeration.</expect>
      <if_mismatch>Reconcile any artifact the page consumes that your FE walk missed — two enumerations disagreeing is the finding.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>comp-blast on each served artifact the page consumes</run>
      <expect>Producer named for every served artifact in the table.</expect>
      <if_mismatch>An artifact with no identifiable producer is a finding — record it as UNKNOWN PRODUCER, never guess.</if_mismatch>
    </step>
    <step>
      <run>comp-routes trace on each MDPF endpoint the page calls</run>
      <expect>Each endpoint resolves to a behavior + origin.</expect>
      <if_mismatch>Coordinate with 3F-P2 (route audit) rather than duplicating — hand it over.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>comp-transform schema-check ModelPortfolios (re-run)</run>
      <expect>Unchanged — this is a read-only TO and must leave no footprint.</expect>
      <if_mismatch>If anything changed, something was modified that should not have been.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<data_reprocess_scope>
  <no_reprocess_needed>Read-only audit. No script, no component, no data touched.</no_reprocess_needed>
</data_reprocess_scope>

<cross_domain_coordination>
  <resource path="portal/ ModelPortfolios.tsx" shared_with="0.4.0_DE (3F-P2/P3/P4)">
    Same component across the WS-P family. P1/P2 are read-only and parallel-safe; P3+ gate on WS-G.
  </resource>
  <resource path="served gold artifacts" shared_with="0.4.0_DS (3F-G3/G4/G8)">
    Your locus table defines what gold must produce. Circulate to DS — it is an input to the Global
    fee-basis artifacts.
  </resource>
</cross_domain_coordination>

<dependencies><dependency type="none">Parallel-safe from day one; no gate.</dependency></dependencies>

<acceptance_criteria>
1. **The complete locus table**: every rendered MDPF aggregate -> {served artifact + producer} or
   {FE computation file:line}, **with the denominator stated** ("N of M rendered aggregates mapped").
2. Every FE-computed GLOBAL number explicitly FLAGGED for 3F-P5 disposition.
3. Andrew's "all client-side" suspicion answered with evidence — confirmed, refuted, or mixed, per
   aggregate rather than in aggregate.
4. Any served artifact with no identifiable producer recorded as UNKNOWN PRODUCER, never guessed.
5. Zero FE modifications (read-only TO).
5a. **RULING-12 ADDENDUM ANSWERED** (see `<addendum id="ruling-12-verify">`): the producer of
   pre-migration Inflection non-model values NAMED at `file:line @ commit-ish`; an explicit verdict on
   **EXPLICIT-BOUNDARY vs EMERGENT-FROM-DATA**; and a provenance-label presence/absence statement.
   **Nothing implemented** — a verify, not a build.
6. **Session log Compiler Tools section reproduces every `<run>` with observed output and pass/fail vs
   `<expect>`. Missing rows = REWORK.**
</acceptance_criteria>

<escalation>Report to 2.0.0_SA_COO. Escalate any Global number created client-side that has no served equivalent — that is a §3.4 target-architecture violation with serving consequences.</escalation>
</task_order>
