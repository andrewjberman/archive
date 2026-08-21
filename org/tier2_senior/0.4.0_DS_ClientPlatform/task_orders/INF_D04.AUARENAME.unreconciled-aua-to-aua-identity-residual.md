<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-08-21-inf-d04-aua-rename</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform (the INF D_04 lane -- Rule 13: DS owns the full commit -> QA-deploy cycle for data/*/scripts/gold/*.py incl. the aws s3 cp)</issued_to>
    <date>2026-08-21</date>
    <status>pending -- STARTS at the lane's next working block (no clock, no urgency; the served key changes at the NEXT SCHEDULED INF run, NEVER ad-hoc). ANDREW-DIRECT AUTHORIZATION, verbatim "rec approved" at the 4.0.0_SA_CRO terminal ~0052Z 2026-08-21 (record: org/tier1_exec/4.0.0_SA_CRO/deliverables/ANDREW_DIRECT_20260821_D04_RENAME_AUA_IDENTITY_RESIDUAL.md; routed to me by 4.0.0_SA_CRO 63977). His word is the authorization; the NEVER#3 never-widen sign-off is the mechanical check on the deploy act, and 1.0.0_SA_CTO has PRE-DISCHARGED their half (64019) -- see the acceptance criteria.</status>
    <project_code>ADVI_INFDRF</project_code>
  </metadata>

  <objective>
    RENAME the served field on INF's D_04 client-portal summary: `total.unreconciled_aua` ->
    `total.aua_identity_residual`. ONE act, ONE field, ONE artifact. D_02's
    `book.unreconciled_aua` KEEPS ITS NAME and is explicitly OUT OF SCOPE -- the ruling resolved
    the one-name-two-computations collision by renaming ONLY the D_04 quantity (Rule 24(iv): the
    two quantities do not move together, so one decision names which one moves).
    Source: data/inf/scripts/gold/INF_D_04.client_portal_summary.py (the field is constructed at
    :842 and computed at :899; its docstring at :825 describes it and must move with it).
  </objective>

  <context>
    WHY THE RENAME (basis on the record, do not re-derive): 3.0.0_SA_CVO 63915 + 4.0.0_SA_CRO~C
    Run 28 both established that BOTH quantities serve 0.0 today, the portal renders NEITHER,
    and the deployed-vs-repo doubt is CLOSED. `aua_identity_residual` names what the D_04
    quantity actually is -- the residual of an identity (total_aua minus the three buckets,
    ~0.00 by construction) -- rather than reusing D_02's book-level name for a different
    computation.

    ⛔ THE NEVER#3 LEG IS PRE-DISCHARGED BY 1.0.0_SA_CTO (64019), measured on the LIVE served
    bytes at three firm trees -- carried here verbatim so the lane never has to chase it:
      opal-data-bd    18 keys  unreconciled_aua ABSENT   (written 2026-08-21T00:26:44Z)
      opal-data-cot   18 keys  unreconciled_aua ABSENT   (written 2026-08-20T11:37:24Z)
      opal-data-inf   23 keys  unreconciled_aua PRESENT  (written 2026-08-20T12:40:09Z)
      bd key set == cot key set: TRUE (the frozen archetype shape is real and genuinely shared)
    ITEM 1 (frontend) DISCHARGED: 3.0.0_SA_CVO's renderer census -- portal/src carries ZERO
    references under either name; that is the correct instrument for a display-breakage claim.
    ITEM 2 (archetype) = NO: `unreconciled_aua` is NOT in the shape bd and cot share, so the
    rename cannot fragment the cross-firm `platinum/firm/header_metrics.json` contract
    (d01_firm_header_metrics.py = archetype, d01_cot_firm_header_metrics.py = byte-schema-frozen
    exemplar) and cannot break either firm -- neither serves the field.
    ITEM 3 (rename vs addition) = RENAME: REMOVE the old key, ADD the new one, NO DUAL-KEY
    WINDOW. Shipping both would WIDEN the served surface and put one logical quantity under two
    names on a served artifact -- the exact defect this act retires. CTO signs against the act
    STATING this on its face; shipping both keys is the ONE branch where the sign-off refuses.
    ⚠ CTO's CORRECTION, carried because it prevents a future wrong inference: INF is NOT "the
    frozen 18 plus 5" -- it is 16 SHARED + 7 INF-ONLY (fee_earning_aua, fee_earning_client_count,
    nmec_aua, nmec_count, non_fee_earning_aua, non_fee_earning_client_count, unreconciled_aua)
    + 2 MISSING that bd and cot both serve (existing_client_aua, existing_client_count). INF
    diverges from the archetype in BOTH directions; a count delta (23-18=5) is not a set delta.
    Whether the 2-key omission is deliberate or a gap is a SEPARATE question, NOT opened by this
    TO and NOT attached to this deploy.
  </context>

  <compiler_tools_mandate>
    Before write: `comp-pipescript io INF_D_04 --pipeline inf` (COLUMN GAPS + portal consumers --
    the flag is REQUIRED, flagless is rc=2); `comp-blast` on the emitting function.
    Before commit: `.tools/commit-gate.sh` (universal, Rule 14); `from __future__ import
    annotations` already present -- keep it (Rule 15).
    Deploy: `.tools/safe-deploy.sh` (Rule 13, atomic; DS owns the cycle incl. the aws s3 cp).
    After the NEXT SCHEDULED INF run: `comp-freshness` / a direct `head-object` + a served-bytes
    read of platinum/firm/header_metrics.json on opal-data-inf -- the APPLIED plane, not the plan.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - 1.0.0_SA_CTO: NEVER#3 never-widen sign-off on the DEPLOY act -- pre-discharged (64019)
      subject ONLY to the act stating item 3 on its face. Send them the one-line statement with
      the deploy; their check is two lines and mechanical.
    - 2.0.0_SA_COO: the second never-widen signature + validation of your close.
    - 0.4.0_DT_ClientPlatform: the portal-side one-liner (types.ts HeaderTotal, typed but
      UNRENDERED) is a SEPARATE TO in their lane -- INF_D04.AUARENAME-FE. Neither blocks the
      other: the field is unrendered, so there is no ordering hazard in either direction. State
      your landed key name to them when it deploys.
    - 4.0.0_SA_CRO (base): registry bump + the contested_unresolved lift ride THE LANDING (base
      registrar act, CVO concur), never this ruling -- do not perform them in-lane.
    - 3.0.0_SA_CVO: their census is the cited basis; no re-run asked.
  </cross_domain_coordination>

  <acceptance_criteria>
    (Rule-24 layer declaration: the layer is the D_04 served-field rename as cut -- N1 code, N2
    scope fence, N3 deploy statement, N4 scheduled-run landing, N5 served verification, N6 proof;
    exhaustive over the act; D_02, the 2-key archetype omission, the portal type, and the
    registry bump are OUTSIDE.)
    N1  CODE: `total.unreconciled_aua` -> `total.aua_identity_residual` in
        data/inf/scripts/gold/INF_D_04.client_portal_summary.py -- the construction (:842), the
        computation (:899) and the docstring (:825) all move together; no other field touched;
        commit-gate PASS.
    N2  SCOPE FENCE, exercised not asserted: D_02's `book.unreconciled_aua` is BYTE-UNCHANGED
        (cite the file sha before/after); a grep of the INF tree shows the old token surviving
        ONLY at its D_02 sites and in tests that belong to D_02.
    N3  DEPLOY ACT STATES ITEM 3 ON ITS FACE, verbatim in the deploy message/ledger: "REMOVE
        total.unreconciled_aua, ADD total.aua_identity_residual, NO DUAL-KEY WINDOW" -- this
        statement is what CTO signs against.
    N4  SERVED KEY CHANGES AT THE NEXT SCHEDULED INF RUN, never an ad-hoc run (Andrew-direct via
        CRO 63977; the ad-hoc-runs law: an ad-hoc run is a QA instrument and its artifacts are
        never production evidence). Name the scheduled run you rode (its trigger + its time).
    N5  SERVED VERIFICATION on the APPLIED plane after that run: the served
        platinum/firm/header_metrics.json on opal-data-inf carries `aua_identity_residual` and
        does NOT carry `unreconciled_aua`; key count moves 23 -> 23 (one out, one in -- a WIDENING
        to 24 is a FAIL); bd and cot BYTE-UNCHANGED at 18 keys each (the cross-firm control:
        an absence verdict names the tree it searched, Rule 21).
    N6  Proof instance VALID rc=0 positional N1-N6 (rc UNPIPED); RAVC close to 2.0.0_SA_COO, cc
        1.0.0_SA_CTO + 4.0.0_SA_CRO + 3.0.0_SA_CVO + 0.4.0_DT_ClientPlatform.
  </acceptance_criteria>

  <proof_of_spec>
    <expected_criteria>N1,N2,N3,N4,N5,N6</expected_criteria>
    <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/INF_D04.AUARENAME_PROOF_OF_SPEC.json</instance_path>
  </proof_of_spec>

  <requirements>
    <requirement id="1">No ad-hoc production run (N4). No dual-key window (N3). Do not touch D_02, the archetype's 2-key omission, the portal type, or the registry. If the served read at N5 shows anything other than a clean one-out-one-in, STOP and surface to COO+CTO the same hour -- a widened served surface is the branch the sign-off exists to catch. Surprise channel: one line to COO.</requirement>
  </requirements>
</task_order>
