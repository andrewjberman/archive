# TO OPAL_ADVIPOINTERS.P4-PUBIAM-49F — publisher IAM (Put scoped to platinum/advi/49financial/* ONLY) + publisher schedule after the runner stage (push plan §3 row 4a, AE half)

<task_order id="OPAL_ADVIPOINTERS.P4-PUBIAM-49F" project="OPAL_ADVIPOINTERS">
<issued_to>0.7.0_AE_CloudOps~M [RE-ADDRESSED 2026-09-01T07:5xZ by the issuer 2.0.0_SA_COO, from the bare BASE. REASON: the base holds NO live session (1pt process truth 0 hits, 1a NOT REGISTERED, 1b 0 markers) and it held 5 open TOs spanning TWO projects -- OPAL_ADVIPOINTERS and ADVI_INSURE -- a Rule 27 one-project-per-instance collision at seating time, so the base COULD NOT LAWFULLY BE SEATED on all of them. This lane takes the OPAL_ADVIPOINTERS four ONLY; ADVI_INSURE.TO-S1-AE stays at the base and is re-addressed separately. Authority: Andrew-direct 2026-09-01 ~06:5xZ full-force-on-D2 drive loop, XXX.md COO row @4469fc738c. Nothing else on these faces changes -- scope, acceptance criteria and sequencing are untouched.]</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-18T16:05Z</issued>
<dated>2026-08-20 — with DS~B's P4-EMIT (row 4a). IAM may be prepared/applied 08-19 after the P2 apply window; the publisher schedule activates only when DS~B's emitters are deploy-ready.</dated>
<status>pending -- GO 160648Z @49dd8469d1; sequenced behind P2-FLOOR apply at this seat</status>
<priority>P1 — gates the P4 EMIT: DS~B cannot write platinum/advi without the grant, and an over-wide grant is the never-widen hazard in IAM clothing</priority>
<authority>Push plan @a2f27c8d0a §2 AE row + §3 row 4a. One producer per served key holds by construction (17b amendment: every platinum publisher READS PARQUET; the publisher is the estate's only JSON producer).</authority>
</task_order>
> **ROOT SUPERSEDED BY REFERENCE (COO, 2026-08-18 ~17:42Z): Andrew-direct ~1730Z moved the ADVI gold home to `opal-data-49financial/gold/advi/` (per-client bucket; ANDREW_DIRECT_20260818_CLIENT_GOLD_BUCKET_SUPERSESSION.md). Every `opal-data-assets/portal/gold/advi/49financial` root reference in this TO reads through OPAL_ADVIPOINTERS.GOLDHOME-REPOINT-49F (one act, before the P2 apply). Key names, criteria ids, dates unchanged.**


## Objective
Grant the ADVI publisher exactly what P4 needs — `s3:PutObject` scoped to
`opal-data-portal-v2/platinum/advi/49financial/*` ONLY — and schedule the publisher stage (D fleet) to
run AFTER the canonical runner stage, on its own schedule floor (never event-only).

## Compiler tools (three-phase)
Phase 1: `comp-iam service <publisher role/lambda>` — NECESSARY NOT SUFFICIENT: it models (action),
never (action, resource), and FAILS GREEN on a new bucket. Phase 2: commit before apply. Phase 3:
live-primitive verification (P4I-2) + plan 0-diff + tag.

## Cross-domain coordination
- shared_resource: `s3://opal-data-portal-v2/platinum/advi/49financial/**` — DS~B writes (P4-EMIT),
  DE reads (P4-REPOINT), CVO pins, DT rendered-read. You are last_write_owner on the IAM/TF; MCP DS~B
  when the grant is live so their first emission is not blocked-invisible.
- shared_resource: the publisher schedule — must fire AFTER the runner stage (P2-FLOOR); the ordering
  is part of the contract with DS~A/DS~B.

## Acceptance criteria
- P4I-1 SCOPED GRANT APPLIED: TF-managed policy grants Put on
  `arn:aws:s3:::opal-data-portal-v2/platinum/advi/49financial/*` and NOTHING wider (no platinum/*, no
  bucket-wide Put) — policy JSON cited at applied vintage via `aws iam get-role-policy` (APPLIED truth,
  not the comp-iam DESIRED view).
- P4I-2 LIVE-PRIMITIVE PROOF, three separate invocations, rc + verdicts printed: (a)
  `simulate-principal-policy` allow on `platinum/advi/49financial/test-key.json` (ONE --resource-arns);
  (b) SEPARATE negative control: deny on `platinum/mdpf/test-key.json` (out-of-scope prefix must be
  implicitDeny); (c) action-name validity via `aws accessanalyzer validate-policy` (never
  simulate-principal-policy for name validity).
- P4I-3 PUBLISHER SCHEDULE: schedule floor for the D-fleet publisher stage with a concrete
  ScheduleExpression, sequenced after the runner stage's window; event accelerator optional; never
  event-only (NEVER#4).
- P4I-4 proof instance VALID rc=0 positional: ids P4I-1,P4I-2,P4I-3,P4I-4.

<proof_of_spec>
  <expected_criteria>P4I-1,P4I-2,P4I-3,P4I-4</expected_criteria>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/OPAL_ADVIPOINTERS.P4-PUBIAM-49F_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Do not
- No grant wider than the exact prefix (the never-widen determination in row 4b assumes this scope).
- No monitors/alarms on the publisher (moratorium). No shadow publish paths (08-04 veto).

## Reporting
COO (cc CTO, DS~B, MSTR) at grant-live and schedule-live. Surprise channel: one banked line to COO.
Session log with Compiler Tools section = deliverable.
