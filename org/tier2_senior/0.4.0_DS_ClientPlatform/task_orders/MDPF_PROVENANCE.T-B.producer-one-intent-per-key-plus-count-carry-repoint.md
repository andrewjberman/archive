# TO MDPF_PROVENANCE.T-B — producer: ONE INTENT PER KEY (R-2) + the FLAG-2 count-carry RE-POINT off `json/mdpf` (the TO-4 prerequisite)

<task_order id="MDPF_PROVENANCE.T-B" project="MDPF_CANPLAT">
<issued_to>0.4.0_DS_ClientPlatform (data/mdpf/scripts/gold lane — 68 of 99 commits since 07-15, the spine's own header "0.4.0_DS_ClientPlatform. Gate: 1.0.0_SA_CTO"; owned-paths data/** = ANY, no gate constrains; authorship is the tiebreak, CTO 132251Z)</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-18T13:35Z</issued>
<dated>2026-08-19 — DATED + OWNED, awaiting spawn (MSTR). Sequenced AFTER ADVI_BDPLAT_RESTORE.TO-1 at the same DS seat — bd platinum (client-facing) closes first; do not interleave. T-B lands after T-A (DE reader is name-tolerant first).</dated>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project MDPF_CANPLAT, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: **SUPERSEDED BY SOVEREIGN DECREE -- Andrew-direct 2026-08-21 at the DS terminal. VERBATIM: "no, none of this work matters" / "mark any of these associated TOs superseded by sovereign decree" / "i do not want this thrash and irrelevant effort".** NO FURTHER WORK ON THIS TO. Half 2 (R-2 renames, PB-4..PB-8) was IN PROGRESS at the DS base seat and is STOPPED: edits were uncommitted and are REVERTED, nothing committed, nothing deployed, no served key moved -- the served artifacts are byte-unchanged by this TO. CTO GO @692a7f8247 (msg 64966, "your plan (a)-(f) ... GO") and the R-2 scope amendment it landed are SUPERSEDED for execution purposes by the decree above; the amendment text stays in the ruling doc as a record, un-acted. SCOPE OF THE DECREE IS ANDREW'S, NOT THIS SEAT'S: it is relayed verbatim, not interpreted -- sibling TOs T-A (complete) and T-C (DE lane, anchored behind this TO's run) are named to their owning seats to mark, not marked here. Half 1 (FLAG-2 count-carry re-point) had ALREADY LANDED 2026-08-19 @12b93b59ba and is unaffected by this decree -- it is done, deployed, exercised; nothing is being rolled back. Prior status preserved below.** PRIOR: **HALF-LANDED -- CORRECTED 2026-08-21 BY THE ISSUER (COO) ON MEASUREMENT; the prior "staged, awaiting spawn" UNDERSTATED what had landed and OVERSTATED what remained.** HALF 1 (the FLAG-2 count-carry re-point OFF json/mdpf) **LANDED 2026-08-19** and is verified at all three rungs: SOURCE (dim_mdpf_aggregate_aua_timeseries.py:650-660 -- carry now reads the GOLD SELF-CARRY, no gold-reads-platinum), DEPLOYED (member sha a7db07bb68f465d5 == safe-deploy-verified HEAD, CTO PB-1 @9a249cb48f), EXERCISED (scheduled 13:31:07Z run green 2026-08-21). NOTE: the FUNCTION NAME load_served_account_count SURVIVED the re-point, so a name-based check reads it as still-reading -- only the implementation moved. HALF 2 (the R-2 provenance renames: cohort_source[] + Global partner_provenance[]) **NEVER STARTED** -- measured ZERO for partner_provenance AND cohort_source across 8,927 files (DS~B 64898), corroborated on the executing plane (current member emits the OLD keys) and by the spec's own layer (ruling sec-2 places R-2 in data/mdpf/scripts/gold, NOT the platinum publisher). **CONSEQUENCE, and it is why this correction matters: downstream MDPF_PROVENANCE.T-C was dated off an ASSUMED completion of this leg, so its "drop the reader name-tolerance" act matured toward a date on which executing it would have DELETED THE ONLY WORKING PROVENANCE PATH on all four scopes** (partner_provenance ABSENT 4/4 on live served artifacts; DE 64886, re-dated @eb64d27e97 with an INDETERMINATE anchor -- correct, do not tidy it into a calendar date). **NEVER DATE A DEPENDENT DESTRUCTIVE ACT OFF A PROJECTED PREREQUISITE; DATE IT OFF THE PREREQUISITE'S OBSERVED COMPLETION.** HALF 2 STILL NEEDS A SEAT: DS base is dark, arch-gated PB-6, and it must be held by ONE seat together with the same ruling's sec-3 work (same emit sites). Sequencing from the original dated field still binds (after ADVI_BDPLAT_RESTORE.TO-1, after T-A -- T-A flipped complete @eb64d27e97). Issuer accountability: this TO sat awaiting a spawn I did not chase for 2 days. Prior status preserved below.</status>
<!-- prior status, preserved for provenance: staged -- DATED 2026-08-19, owner named, awaiting spawn -->
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


## Issuer record 2026-08-30T13:5xZ (2.0.0_SA_COO) -- PB-1 SCORED on the re-pointed fire

PB-1 re-pointed (85997) at the next scheduled mdpf-gold fire with the bytes pinned on the day: the fire ran 2026-08-30T13:30:34Z; scored PASS on both limbs by DS~V (87550), record `org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/MDPF_PROVENANCE.T-B_PROOF_OF_SPEC.json` @924d560a32, checker 3948c766a7 VALID rc=0 unpiped, PB-1/PB-2/PB-3 PASS. THE GRAIN: function LastModified 2026-08-29T02:55:49Z unchanged across the run and the 13:35:53Z read -- a NON-MODIFICATION proof, stronger than the same-minute capture the re-point asked for; the downloaded zip BOUND to the configuration by base64(sha256) == CodeSha256 U/87M1NBA/... BYTE LIMB MET: `dim_mdpf_aggregate_aua_timeseries.py` from the DOWNLOADED package, 3,046 lines (the denominator the criterion names), 2 raw `json/mdpf` hits both opened (docstring), CODE READS = 0, with `portal/gold/mdpf` present on 2 lines as the live control. RUN LIMB MET AS WRITTEN: the D-1 self-carry read OK ($175,738,098.94 from platinum 2026-08-29).

**ISSUER RULING (1), the scope of "run succeeds":** the SELF-CARRY READ, as the criterion was written -- MET. The same cycle's `12/16 A4 objects built; errors=['global']; R1 INCOMPLETE -- aggregate-aua-timeseries / aum-metrics / account-distribution / category-views @ global` is IDENTICAL on 08-29 and 08-30 (measured by the seat): a STANDING CONDITION on the 'global' scope, not this criterion's subject (the 49f build path), routed to 3.0.0_SA_CVO as an OBSERVATION with the owner question (who owns the mdpf-gold cycle's global scope) -- not chased here. **ISSUER RULING (2), the discharge:** the hold on Andrew's RESERVED DELETE of `json/mdpf/{firm}` waited for byte evidence at the right vintage; that evidence exists at @924d560a32. THE ISSUER'S CONDITION IS MET (stated 87579). The delete stays Andrew's act on the issuer's AND the gate's word; the gate's half asked at 87580; `0.0.0_AB_MSTR` carries the card once when both halves are on it, with the record id and the CodeSha256 line. This record reports the issuer's half; it releases nothing. Gate note recorded: the commit went through the prescribed comp-system regenerate-and-stage path (06_current_state refreshed at HEAD=9084473d9c), not the audited override.
