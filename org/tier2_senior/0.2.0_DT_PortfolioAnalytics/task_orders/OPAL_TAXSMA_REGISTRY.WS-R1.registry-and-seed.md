<task_order>
<to_id>OPAL_TAXSMA_REGISTRY.WS-R1</to_id>
<title>REGISTRY — define the Tax SMA account registry (S3-JSON source-of-truth) + seed the known live accounts, exact-resolved + human-confirmed</title>
<issued_by>1.0.0_SA_CTO</issued_by>
<issued_to>0.2.0_DT_PortfolioAnalytics</issued_to>
<!-- Andrew-direct: CTO writes these TOs directly (not via COO). OPAL_TAXSMA_REGISTRY, couples OPAL_TAXSMA_PT2. -->
<date>2026-07-17</date>
<status>pending</status>
<priority>P2 (Andrew-direct via CTO). Head of the registry chain — WS-R3 (ETL reads it) + WS-R4 (skill enrolls into it) both depend on this substrate + schema.</priority>

<authority>
Andrew-direct 2026-07-17 (DT brief @e43e9d0de -> CTO PRD). PRD docs/architecture/OPAL_TAXSMA_REGISTRY_PRD.md §4 D1/D6, §5 WS-R1.
</authority>

<gate>
D1 (CTO-ruled): substrate = S3 JSON, VERSIONED, at s3://opal-data-assets/blackdiamond/49f/_ops/taxsma_roster.json — a CONTROL prefix OUTSIDE the bronze/silver/gold layer grammar (the roster is control, not a data-layer artifact; confirm the layer logic never treats it as one). Enroll append = read-modify-write with an ETag-conditional PUT (If-Match) so a concurrent modification fails+retries (atomic-enough under single-enroller Alyssa; migrate to DDB ONLY if concurrency ever becomes real). Versioning IS the enrollment audit trail.
D6 seed: every seeded account EXACT-resolved via WS-R2's ladder + HUMAN-CONFIRMED before it lands — NEVER guessed.
</gate>

<scope>
Define the registry: schema {schwab_acct, bd_internal_id, bd_external_id, client_name, trade_start_date, strategy, enrolled_at, enrolled_by, status} + the RMW/ETag-conditional append protocol + the status lifecycle (active / suspended / removed). Then SEED the known live accounts: Chiles 0027265115 -> 22596361 (confirmed via xref int(id[3:])), Bump 0035940058, Macy 0091939812, + any 4th — each resolved via WS-R2's exact-number ladder and HUMAN-CONFIRMED (surface the resolved internalId to a human before writing it). The registry is the ONE source of truth WS-R3's ETL reads.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before seeding">
    <step>
      <run>Confirm the roster path is OUTSIDE the layer grammar (not under bronze/silver/gold/); confirm S3 versioning is ON for the key</run>
      <expect>Control prefix (_ops/), versioning enabled -> the audit trail exists.</expect>
      <if_mismatch>STOP. A roster under a layer prefix or unversioned = re-place it before seeding.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="each seed account">
    <step>
      <run>Resolve the exact number via WS-R2's ladder; present the (schwab_acct -> internalId, client_name) to a human for confirmation BEFORE the append</run>
      <expect>Human-confirmed exact match; fail-loud + STOP on absent-or-!=1 (never a guessed/fuzzy seed).</expect>
      <if_mismatch>STOP. Do not seed an unconfirmed or fuzzy-resolved account.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
WS-R2 (resolver) is the dependency for the seed's exact resolution — build R2's fast-path (xref) at least far enough to resolve the seed set, or seed Chiles (xref-known) first and add Bump/Macy once R2's non-xref path clears. WS-R3 reads this registry; WS-R4 enrolls into it. No alert leg (alert-suspension).
</cross_domain_coordination>

<acceptance_criteria>
1. Registry schema + RMW/ETag-conditional append protocol + status lifecycle defined and documented.
2. Roster at blackdiamond/49f/_ops/taxsma_roster.json, versioned, confirmed OUTSIDE the layer grammar.
3. Known accounts SEEDED, each EXACT-resolved + HUMAN-CONFIRMED (Chiles confirmed; Bump/Macy/4th resolved+confirmed) — zero guessed/fuzzy entries.
4. Session log reproduces each mandate run + the per-seed human-confirmation.
</acceptance_criteria>

<references>
  <ref type="prd">docs/architecture/OPAL_TAXSMA_REGISTRY_PRD.md (§4 D1/D6, §5 WS-R1)</ref>
  <ref type="brief">org/tier2_senior/0.2.0_DT_PortfolioAnalytics/deliverables/TAXSMA_ACCOUNT_REGISTRY_AND_ONBOARDING_BRIEF_20260717.md @e43e9d0de</ref>
</references>
</task_order>
