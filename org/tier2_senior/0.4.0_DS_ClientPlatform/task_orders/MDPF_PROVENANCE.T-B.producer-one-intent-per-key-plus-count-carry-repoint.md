# TO MDPF_PROVENANCE.T-B — producer: ONE INTENT PER KEY (R-2) + the FLAG-2 count-carry RE-POINT off `json/mdpf` (the TO-4 prerequisite)

<task_order id="MDPF_PROVENANCE.T-B" project="MDPF_CANPLAT">
<issued_to>0.4.0_DS_ClientPlatform (data/mdpf/scripts/gold lane — 68 of 99 commits since 07-15, the spine's own header "0.4.0_DS_ClientPlatform. Gate: 1.0.0_SA_CTO"; owned-paths data/** = ANY, no gate constrains; authorship is the tiebreak, CTO 132251Z)</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-18T13:35Z</issued>
<dated>2026-08-19 — DATED + OWNED, awaiting spawn (MSTR). Sequenced AFTER ADVI_BDPLAT_RESTORE.TO-1 at the same DS seat — bd platinum (client-facing) closes first; do not interleave. T-B lands after T-A (DE reader is name-tolerant first).</dated>
<status>staged -- DATED 2026-08-19, owner named, awaiting spawn</status>
<priority>P2 for the renames; the RE-POINT half is P1-adjacent: it is the HARD PREREQUISITE for the HELD json/mdpf served-key delete (Andrew's reserved act) — CTO amendment 1: its own criterion-id, its own scheduled-run proof, SHIPS FIRST if bandwidth forces a split</priority>
<authority>CTO RULING @fc74f8f6b4 §2 R-2 + §3 (`docs/architecture/MDPF_PROVENANCE_CANONICAL_FORM_RULING_20260818.md`); COO decomposition per §4. CTO gates the arch (rename + §B3 key-set + harness exemption in ONE change). No new project; contract correction under CANPLAT/CONTRACT §B3. Scheduled path only — no shadow, no comparator, no parallel emitter (Andrew 08-04 veto).</authority>
</task_order>

## Half 1 — THE RE-POINT (ships first; gates a reserved act)

`dim_mdpf_aggregate_aua_timeseries.py:1131-1132` (`build_firm_timeseries`, 49f `count_source=
'served_import'` `:1073`) calls `load_served_account_count` (`:643-663`) which `get_object`s
`s3://opal-data-portal-v2/json/mdpf/49financial/aggregate-aua-timeseries.json` on EVERY 49f build and
RAISES on failure (C2 fail-loud) — CTO verified at the EXECUTING package bytes (member sha
ce9c0284537e == repo). Its own docstring: "the banked json/mdpf-retire blocker … must be re-pointed".
**Re-point the FLAG-2 count carry to a GOLD SELF-CARRY**: the prior vintage of
`portal/gold/mdpf/49financial/aggregate-aua-timeseries/{D-1}.json` (same tier, rolling as the docstring
intended, NO gold-reads-platinum circularity). **Proof (CTO amendment 1): a scheduled 13:30Z run reading
the {D-1} self-carry; `count_as_of` / `count_coverage_end` UNCHANGED before/after; the count carry ties
TO THE CENT against the frozen `json/mdpf` source on all common dates — or the re-point changed the
product and it does not ship.** Also DISPOSITION the second deployed reader:
`opal-smartx-ingestion-pipeline` module `:482` reads `json/mdpf/global/…` (Active, no trigger post
wave-1) — retire the read, re-point it, or state why it is inert; record it (not chased beyond the
disposition).

## Half 2 — ONE INTENT PER KEY (R-2), one change, CTO arch-gated

(a) Rename the per-firm source-identity channel **`cohort_source[]`** (EXACTLY the 07-21 shape:
index-aligned `{model, custody}` source names, `None` on absent — one key rename at `_cohort_provenance`'s
emit site + `mdpf_gold_consolidator` key set). (b) Emit **`cohort_provenance[]` per-firm in the CRO §1a
contract shape** — dated `{date, custody, model}` with class enums — derived per leg under the one law
from inputs the producer already holds (per-leg value presence, `recon_idx`); inflection's 7 EVR dates
carry the real per-cohort information (model `reconstructed` / custody `measured`). (c) Rename Global's
channel **`partner_provenance[]`** (dated per-partner status + `as_of_by_partner`, content unchanged) so
a per-firm reader structurally cannot misread it. (d) `point_class[]` UNCHANGED. **In the SAME change:**
CONTRACT §B3 key-set assertion, `SHAPE_EXEMPT_ROOTS` in the DT parity harness, `provenance-read-guard.mjs`
update. Lands on the scheduled 13:30Z path; verified on the next unattended run.

## Acceptance criteria

- PB-1 (RE-POINT): scheduled 13:30Z run succeeds reading the {D-1} gold self-carry; no `json/mdpf` read
  in the 49f build path at executing bytes (package member sha cited + grep count 0 with the file line
  count as denominator).
- PB-2 (RE-POINT TIE): `count_as_of`/`count_coverage_end` unchanged before/after; count carry ties to the
  cent vs frozen `json/mdpf` on all common dates (dates compared / dates total printed).
- PB-3 (READER 2): smartx-ingestion `json/mdpf/global` read dispositioned, stated.
- PB-4: `cohort_source[]` present per-firm with the 07-21 shape byte-identical to the former
  `cohort_provenance` content on those scopes.
- PB-5: per-firm `cohort_provenance[]` in §1a shape; inflection 7 EVR dates carry model `reconstructed` /
  custody `measured`; derives to `point_class[i]` under the any-cohort rule on every date (contradictions
  = 0, printed).
- PB-6: Global `partner_provenance[]` present, content == former channel; §B3 key-set assertion + harness
  `SHAPE_EXEMPT_ROOTS` + read-guard updated in the same commit; CTO arch-gate stamp cited.
- PB-7: `point_class[]` byte-identical before/after on all four scopes.
- PB-8: served values unchanged (aggregate sums per scope before/after, to the cent).

<proof_of_spec>
  <expected_criteria>PB-1,PB-2,PB-3,PB-4,PB-5,PB-6,PB-7,PB-8</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/MDPF_PROVENANCE.T-B_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>
Positional-id validation, check the rc. If split (re-point first): PB-1..PB-3 as its own instance, PB-4..PB-8 the second — declare the grammar in your first report.

## Tools + discipline
`comp-pipescript io dim_mdpf_aggregate_aua_timeseries --pipeline mdpf` before write; `comp-pipescript
deployed` before any run; `comp-validate` on outputs (NO_CONFIG = say so); commit-gate automatic;
`safe-deploy` (mdpf deploy-gated 08-04). Rule 17b: gold is parquet/JSON per the 08-11 amendment as it
stands in this tree — do not move tiers. No shadow prefix, no comparator (Andrew 08-04 veto).

## reporting
COO (cc CTO, MSTR) at re-point landed, at rename landed, at the scheduled-run proof. IMMEDIATELY if the
count carry does not tie, or the §1a per-firm derivation cannot reproduce `point_class[i]`.
