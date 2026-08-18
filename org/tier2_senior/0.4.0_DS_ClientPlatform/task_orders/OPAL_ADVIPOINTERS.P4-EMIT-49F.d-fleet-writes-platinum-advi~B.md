# TO OPAL_ADVIPOINTERS.P4-EMIT-49F — the D fleet becomes the ADVI publisher: platinum/advi/49financial twins for every served key (push plan §3 row 4a, DS~B half)

<task_order id="OPAL_ADVIPOINTERS.P4-EMIT-49F" project="OPAL_ADVIPOINTERS">
<issued_to>0.4.0_DS_ClientPlatform~B (publisher lane; POD4 enumerated)</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-18T16:05Z</issued>
<dated>2026-08-20 — with AE's P4-PUBIAM (the grant gates your first write). Prep (frozen key list, emitter readiness, the CTO routing below) starts NOW.</dated>
<status>staged -- GO paired; first S3 emission waits on AE's grant-live MCP</status>
<priority>P1 — the working phase of the push; every downstream row (4b pins, 4c flip) consumes your output</priority>
<authority>Push plan @a2f27c8d0a §3 row 4a + §2 DS~B row. CRO §15 disposition ledger @27a096f40a (P-1/P-4/P-6/P-7 RULED Andrew-direct 08-18 card 4 — binding lines folded below as criteria). 17b amendment: platinum publishers READ PARQUET; the publisher is the estate's only JSON producer for these keys.</authority>
</task_order>
> **ROOT SUPERSEDED BY REFERENCE (COO, 2026-08-18 ~17:42Z): Andrew-direct ~1730Z moved the ADVI gold home to `opal-data-49financial/gold/advi/` (per-client bucket; ANDREW_DIRECT_20260818_CLIENT_GOLD_BUCKET_SUPERSESSION.md). Every `opal-data-assets/portal/gold/advi/49financial` root reference in this TO reads through OPAL_ADVIPOINTERS.GOLDHOME-REPOINT-49F (one act, before the P2 apply). Key names, criteria ids, dates unchanged.**


## Objective
Emit a `platinum/advi/49financial/{key}.json` twin for every key on the FROZEN SERVED-KEY LIST —
parquet in (the canonical gold root), served-shape JSON out, census-frozen shape, instance per key.
First emission mints the root (you confirmed it does not exist — 154855Z fact 3).

## Context — the three facts from your 154855Z, answered
1. POPULATION: the 35-advisor exposure + hash-labels are CLOSED @33f7d47009 — acknowledged; the OPEN
   half (population 9 vs served 15; role_aua snapshot basis vs jd2 x canonical_valuation) carries the
   design call: **ROUTED TO CTO by COO this window** (should d13/leaderboard-family consume the
   canonical role_aua artifact that lives outside the product root and outside P3's copy scope?).
   Families it gates go DECLARED-GATED-on-CTO-ruling in your per-key work; EMIT everything it does not
   gate — do not stall the fleet on the call.
2. DIMENSIONS GAP CLOSED @4c1219fc34 — emitters read the new root as-is. Confirmed.
3. DENOMINATOR: resolved by P4E-1 below — a jointly FROZEN LIST, not a digit.

## Compiler tools (three-phase)
Phase 1: `comp-pipescript io d01_firm_header_metrics --pipeline bd` (and per emitter you touch) —
expect PORTAL CONSUMERS enumerated; `comp-transform fields` awareness for the FE-read census. Phase 2:
commit-gate. Phase 3: `comp-validate` per emitted artifact (NO_CONFIG = say so, never signal SAFE).

## Cross-domain coordination
- shared_resource: `s3://opal-data-portal-v2/platinum/advi/49financial/**` — you write; AE grants
  (P4-PUBIAM); DE reads (P4-REPOINT); CVO pins (P4-PINS-CERT); DT rendered-reads. You are
  last_write_owner on content. MCP CVO at each key's first emission (their pre-flip pin needs it).
- shared_resource: the FROZEN KEY LIST artifact (P4E-1) — joint DS~B + CVO; both cite ONE commit.
- shared_resource: `opal-data-assets/portal/gold/advi/49financial/**` (read) — written by the
  scheduled chain (DS~A/AE). Read-only for you.

## Acceptance criteria
- P4E-1 FROZEN KEY LIST (FIRST, with CVO): ONE enumerated served-key list committed as an artifact
  both lanes cite — members NAMED (never a digit), reconciling your census run-8d read (15
  platinum/firm/* + platinum/49financial/ownership_map) against CVO's 17-key frame
  (firm/gold_timeseries_chart twins = 2, partner_analytics trio = 3; CVO_49F_KILL_CLEAR_ACCOUNTING,
  COO-pinned 195302Z). Disagreement is a FRAME difference — the list states its grain and any
  twin/trio expansion explicitly. This list IS the denominator for rows 4a/4b/4c; the plan's "15" is
  superseded by the enumeration (COO notifies CTO).
- P4E-2 TWIN PER KEY: every key on the frozen list has a `platinum/advi/49financial/` twin,
  census-frozen shape (byte-schema vs the d00 census; ShapeFrozenPublisher pattern), emitted FROM
  parquet gold (no legacy-bd-gold read except where P4E-6's ruling explicitly permits role_aua), one
  proof-of-spec instance per key group per the declared grammar.
- P4E-3 CRO BINDING LINES (RULED, Andrew-direct 08-18 card 4): (P-1) the NET TWR series is the value
  in *_return_pct_twr; gross rides only where the served shape already carries a gross field. (P-4)
  market_growth = MEASURED net return dollars, served name/unit/nullability UNCHANGED, semantics flip
  from residual; synthetic_correction = recon residual (d09/d10 family). (P-7) v1 = TWR/GRO: no
  benchmark or asset-contribution keys minted; MWR columns nullable, a null MWR is not a defect.
- P4E-4 MEMBERSHIP CONTRACT (P-6, RULED): advisor-grain emitters (d13/d14 family) reproduce the
  CURRENT membership contract — any active 49F role, each account once per advisor, role breakdowns
  full-tagged + NON-ADDITIVE, fee splits NEVER weight return. NOT architect-only, NOT split-weighted.
- P4E-5 NEVER-WIDEN INPUT PER KEY: per emitted key, the disclosure CTO+COO's row-4b determination
  consumes — what loses a read, what becomes newly visible, vs the legacy served twin (the exposure
  axis your 08-12 near-miss proved value-pins cannot see). DELTA=0 keys stated as such.
- P4E-6 THE ROLE_AUA RULING APPLIED: whichever way CTO rules (consume canonical role_aua vs re-derive),
  the affected families implement THAT ruling with the ruling cited; until it lands they are
  DECLARED-GATED, never quietly emitted on your own basis choice.
- P4E-7 proof instances VALID rc=0 positional per group; grammar declared in your first report.
- P4E-8 CLIENT-KEY CONTRACT (added 16:20Z from CRO's consumption map @d774778b58 —
  CLIENT_KEY_GRAMMAR_CONSUMPTION_MAP_20260818.md; PRD §5.B.5 "waits on the consumption map" is
  DISCHARGED by it): v1 emits the SERVED z-grammar — (i) key-set equality clients_tab clients[].key
  <-> advisor-book clients[].client_key <-> gold/entities/clients/{key}/ tree per date (the FE joins
  at runtime; a partial flip breaks the L3 fetch silently); (ii) zero `rel_*` keys on any served
  plane (rel_<hash> stays canonical-internal in gold parquet); (iii) the 138 `acct_z*` prefixes each
  carry a disposition (serve/retire/reclassify) — never silently reproduced. Simplifiers, measured by
  CRO: no URL carries a client key, no durable storage — no migration/redirect work in v1. The
  grammar FLIP itself stays OUT of v1 scope (identity coverage 0/201; household spine map open;
  NEVER#3 when it comes).

<proof_of_spec>
  <expected_criteria>P4E-1,P4E-2,P4E-3,P4E-4,P4E-5,P4E-6,P4E-7,P4E-8</expected_criteria>
  <instance_path_grammar>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/PROOF_OF_SPEC_P4EMIT_49F_{group}_{YYYYMMDD}~B.json</instance_path_grammar>
</proof_of_spec>
Multi-group TO: declare the group set (e.g. keylist / firm-family / advisor-family / twins-trio) with
statuses in your first report; one instance per group; untokened ids collide — these are 49F-scoped by
the P4E prefix.

## Do not
- Do not flip any consumer (DE's row 4c). Do not write outside platinum/advi/49financial/*.
- Do not resolve the two-identity-systems question (0/201 key overlap) — PRODUCT question at Andrew;
  client key grammar waits on CRO's consumption map.
- No shadow/parallel emitters; the legacy publisher keeps running until P5.

## Reporting
COO (cc CTO, CVO, AE, MSTR) at frozen-list committed, at first emission, at fleet-complete. Surprise
channel: one banked line to COO. Session log with Compiler Tools section = deliverable.
