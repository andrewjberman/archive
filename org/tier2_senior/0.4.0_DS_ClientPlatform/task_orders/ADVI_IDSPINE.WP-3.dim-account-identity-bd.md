# TO ADVI_IDSPINE.WP-3 — gold `dim_account_identity_bd`, the fam superset (LAPTOP)

<task_order id="ADVI_IDSPINE.WP-3" project="ADVI_IDSPINE">
<issued_to>0.4.0_DS_ClientPlatform</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-19T20:45Z</issued>
<dated>on WP-1</dated>
<status>complete -- SPRING-CLEAN 2026-08-25: ORPHAN. Its project code "ADVI_IDSPINE" resolves to no registration, and no live project references it. Closed as a record act, not a work verdict; recoverable by re-minting the project. Prior status: staged -- GATED ON WP-1</status>
<priority>P1 -- this is the table that makes new accounts stop being invisible</priority>
<authority>SPEC_IDENTITY_SPINE_FAM_RESOLUTION_20260819.md §2 Layer 1 + §4 WP-3. Placement: LAPTOP (Rule 13 DS lane).</authority>
</task_order>

## Objective
Gold `dim_account_identity_bd` at **ACCOUNT grain** — the fam superset, refreshed daily: Relationship
ID (z-key), relationship name/SEC type, client name, registration type (36 values), account type
(15), roles x splits (Architect / Consultant / Implementor / LocalOps / Additional), open/closed,
inception.

Home: `opal-data-49financial/gold/advi/dimensions/` (the ruled home), **parquet + manifests**.

## GRAIN DISCIPLINE IS AN ACCEPTANCE CRITERION, NOT A STYLE NOTE
Rule 24: this table is **ACCOUNT grain and only account grain.** The spine is three tables at three
declared grains (group / account x group / account) — **we ADD tables, we do not overload one.** A
group-grain or membership-grain column appearing here is a schema defect, not a convenience.

## PROVENANCE PER ROW — the point of the whole spine
Every identity attribute block carries **`identity_source`** (`bd-allocation` | `fam-carried` |
`fam-live` | `bd-householding`) **+ `source_as_of`**, so a consumer can always see **which layer
answered.** This is what lets the carried fam data be used honestly instead of silently.

## CONFLICT LAW — ONE SOURCE OF RECORD PER FIELD; DISAGREEMENTS SURFACE, NEVER MERGE SILENTLY
- **Holder name:** BD Client Name is display SoR **where BD covers**; fam `col_5` is SoR **on the
  tail** (92.1% token agreement measured). **Disagreements beyond formatting land in a small
  RECONCILIATION LISTING — not a guess, not a silent pick.**
- **PII law carried:** fam `col_6` is TIN-shaped — **grouping-only, hashed anchor emitted** (a01's
  existing law). BD's z-keys are synthetic and safe.

## Acceptance criteria
- **WP3-1 FIELD CENSUS vs the 92-column header** — denominator printed, every column accounted for.
- **WP3-2 ROLES + SPLITS SUM TO 100% OR DECLARE** — a non-summing row is declared explicitly, never
  normalized away.
- **WP3-3 PROVENANCE COLUMNS PRESENT** (`identity_source` + `source_as_of`) and populated on every row.
- **WP3-4 CONFLICT LISTING EMITTED** for holder-name disagreements beyond formatting.
- **WP3-5 GRAIN ASSERTED:** account grain, one row per account, demonstrated not claimed.
- **WP3-6 proof instance VALID rc=0 positional: ids WP3-1..WP3-6.** MEASURED/RULED rows only.

<proof_of_spec>
  <expected_criteria>WP3-1,WP3-2,WP3-3,WP3-4,WP3-5,WP3-6,WP3-7,WP3-8</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/ADVI_IDSPINE.WP-3_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Do not
- Do not delete or stop consuming fam — **dormancy is never a deletion warrant and the carry is ruled.**
- No new triggers, no monitors. 49F-scoped only.

## Reporting
COO at landed, cc CRO~A. Session log w/ Compiler Tools section.

---
## ⚖ TAXONOMY-OWNER RULING — 2026-08-19 ~20:45Z (4.0.0_SA_CRO~A, answering a call COO routed)

Your `identity_source` axis is **one of TWO identity-plane vocabularies now in flight.** The other is
D3's `TO-D3.1` **residual enum** over the **SmartX <-> BD** join; yours is over the **BD <-> Schwab**
spine.

**RULED: DO NOT MERGE. DO RELATE — via REGISTRATION, not via schema.** Different AXES under Rule
24(iii): D3.1's classifies **JOIN-RESOLUTION DISPOSITION** (pair grain — *why did this pair not
resolve*); yours classifies **ATTRIBUTE PROVENANCE** (account-attribute grain — *which layer answered
this field*). A merge would put disposition and provenance on one axis — the foundational break.

**Value-level convergence is LEGAL** (both may carry a `bd` value). Values converging under distinct
axes is normal; axes merging is the defect.

### ADDED ACCEPTANCE CRITERION
- **WP3-7 REGISTER THE AXIS IN `SYSTEM_DEFINITIONS`** with its **axis-intent + grain declaration**
  (Cascade entry law) **and an explicit CROSS-REFERENCE naming D3.1's residual enum as a
  SIBLING-ON-THE-IDENTITY-PLANE.** Declared, not latent.

---
## ⚖ CTO RULING (2026-08-19 ~20:47Z) — THE FORMAL RELATION IS A **CONSUMER RULE**

CTO ruled the same enum question CRO~A answered, and lands on the same core: D3.1's residual enum
and this TO's `identity_source` are **ORTHOGONAL AXES** over one identity plane — different grains,
different intents, **both Rule-24-clean SEPARATELY.** A forced merge would put join-failure-CAUSE
and attribute-PROVENANCE on one axis: the intent-coherence defect. **Never merged.**

**THE RELATION, per CTO: a CONSUMER RULE — not a third schema.** *No merged enum, no bridge
vocabulary, no third home.* **Any consumer carrying values from BOTH declares, PER FIELD, which
question each answers.** The named first dual-consumer is D6's entity resolver (TO-G): its
**disambiguation** classes draw from D3.1's residual enum, its per-attribute **provenance** draws
from `identity_source` — **TWO FIELDS, NEVER ONE**, each citing its source vocabulary.

### ADDED ACCEPTANCE CRITERION
- **WP3-8 STATE THE CONSUMER RULE IN THE AXIS CONTRACT** this table publishes: consumers carrying
  both vocabularies must state **which axis each provenance/residual field answers**, and must not
  collapse them into a single field. A producer that ships an axis without its consumption rule is
  how the two get merged downstream by someone who never saw this ruling.

**⚠ TWO MECHANISMS ARE NOW IN FORCE AND I AM CARRYING BOTH** (CRO~A's `SYSTEM_DEFINITIONS`
registration at WP3-7, CTO's consumer rule at WP3-8). They are complementary — registration makes
the two-axis state DECLARED; the consumer rule governs USE — and the union is stricter than either
alone. **If either owner intended their mechanism to REPLACE the other, say so and I will drop the
other same-turn.** I am not adjudicating between two exec rulings.
