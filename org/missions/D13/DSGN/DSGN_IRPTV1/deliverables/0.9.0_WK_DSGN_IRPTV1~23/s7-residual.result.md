# DSGN_IRPTV1.TO-IV-e-35 -- the S7 residual (IV-e-35, row DSGN_IRPTV1-W21-S2 disarm)

Worker: 0.9.0_WK_DSGN_IRPTV1~23. Portal branch `wk-DSGN_IRPTV1-23-portal`, tree branch `wk-DSGN_IRPTV1-23`.

## What this round fixed (real, verified defects; every one committed)

- **fe-s-14/envelope.test.ts** (F14-AC13, resolve-scope): the generic FIRM_ID doesn't satisfy resolve-scope's own
  firm_id-match rule (`envelope.ts`). Now reads the built ResolvedScope's own `verified_request_firm_id`.
- **fe-s-31/every-page.test.ts** (F31-AC4, F31-AC11): `getPerformanceReport` now requires an accepted account
  selection; `frozenPrintBundle` supplied none, masking the real cause as `MissingPayloadError`. Now mirrors
  `PrintEntry.tsx:186-193`'s own `printWindow.ok` spread.
- **fe-s-33/fixtures-reach.test.ts** (all 4 sub-test residuals): `STATUS_SCHEMA` re-pointed to
  `PublicStatusEnvelope.schema.json` (the wire-legal shape); `compareStatus` excludes `internal_correlation_id`
  BY NAME from its byte-for-byte history comparison (a correct S7 strip, not the hazard the control was built
  to catch).
- **fe-s-39/adapter-plane.test.ts** (all 4 rows): `wireStatus()`'s baked-in `internal_correlation_id` removed;
  F39-AC3's status-carried-null arm now asserts the envelope refusal itself as "still reads malformed"; F39-AC7's
  golden markup updated to the Title-Case advisor words IV-e-18 (df5e41b5) shipped after this control's baseline.
- **fe-s-46/timeouts.test.ts BOUNDS**: replaced the naive index-position line diff with a real `git diff -U0`
  hunk classifier (THIRD_ARG / ALLOWED-pinned-exception / VIOLATION), disarming the collision named in row
  DSGN_IRPTV1-W21-S1 without loosening the underlying S7 fix it was rejecting.
- **fe-s-47/no-status-reason.test.ts** (F47-AC3, F47-AC5, F47-AC6, F47-AC7): three independent defects, none the
  shared bug family -- two arms fed `public_reason_code: null` (ruling 101449); `operationWires()` never matched
  `readonly data?:` (submit-export's data made optional, ruling R2); the RULES census predates public-status.ts
  and its generated wire type. `committedInstance()` gained PublicStatusEnvelope's special case.
- **fe-s-54/stated-state-wins.test.ts** (F54-AC3, F54-AC-CROSS): the control's `public_reason_code: null` now
  asserts the envelope refusal (ruling 101449) instead of a graceful NO_STATUS_REASON read.
- **fixtures/wire/SelectedAccounts.valid.json, DirectoryPage.valid.json**: two committed-fixture authoring
  defects (a strict-subset `selected_account_ids`; a mismatched `revision.directory_revision`) that were
  refusing selection-create/directory-browse at the envelope's field-equality check -- both now parse.

## What remains (residual, and why)

- **fe-s-25/absent-vs-null.test.ts** (2 rows) and **fe-s-15/job-states.test.ts's WAF-refresh row**: real,
  root-caused defects requiring an out-of-grant `contracts/public-status.ts`/`contracts/adapt.ts` change or a
  CTO ruling, or an out-of-grant `tabs/analysis/composer.ts` markup fix. Classed Q (fe-s-25's two) or left H
  with the residual honestly named (fe-s-15, Q budget exhausted).
- **fe-s-57/carry.test.ts's F57-AC2**: original defect fixed; a residual `unprojectedGrant`-carry gap
  (`contracts/adapt.ts`, out of grant) named in the row's action text, reclassed H since the Q cap was already
  spent on fe-s-1 (x2) and fe-s-25 (x3).
- **A newly-generalized flakiness finding** (row DSGN_IRPTV1-W23-S1): at least 9 files beyond the 3 W21-S3
  named (fe-s-33/39/46) show a test that passes reliably alone but fails intermittently only under the full
  221-file suite run, with no shared cause this cell could find. This, plus the residual real defects, keeps
  the live failing set above the table's 5-Q cap.

## Criteria

- **IVE35-AC1** (S7-SUITE-OK): FAIL by output. See `DSGN_IRPTV1.TO-IV-e-35.s7-residual.proof_of_spec.json`.
- **IVE35-AC2** (S7-TABLE-OK): PASS.

Status not flipped to `complete`, per BOUNDS' refusal clause and the schema's own PASS-by-output requirement.
