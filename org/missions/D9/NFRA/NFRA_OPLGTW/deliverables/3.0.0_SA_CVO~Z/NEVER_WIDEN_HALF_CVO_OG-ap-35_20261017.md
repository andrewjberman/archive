# Never-widen half (CVO) -- OG-ap-35: remove `download_filtered` from one live Schwab grant (Alyssa's no-download, enforced)

By: `3.0.0_SA_CVO~Z`, 2026-10-17 ~03:3xZ, on `1.0.0_SA_CTO~Z` msg 35325 (acked).

**Against:** `deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-ap-35.md` @83dc896cad (sha256 `224a80d88a524839`), read whole.

**VERDICT: SIGNED** at ask sha256 `224a80d88a524839`. Any other ask hash re-opens this half.

## Why this act exists

My row `NFRA_OPLGTW-Z-S173` (2026-10-16) found that PRD v2.2 item 4's "Alyssa's no-download" had no carrier: her live grant held
`download_filtered`. It asked the CTO to enforce the rule or strike it. The CTO's ruling enforces Andrew's 2026-10-08 word, "no
downloads needed yet". This act carries it out.

## What I read

- **A narrowing, by one key.** One principal loses one operation, `download_filtered`. `describe`, `list` and `query` are
  unchanged, and nobody gains anything. `prepare()` accepted the candidate, and its diff's only changed key is `operations`; the
  scope-without-operations hash must read equal after.
- **The side-writes, traced** (my OG-mg-1 lesson, the CTO's lesson 3). One transaction writes four items in her partition:
  1. the profile;
  2. a new grant revision (revision 4 stays as history);
  3. one `operator_audit` line;
  4. **one `email_deny` re-put** under a condition matching her existing record's tid and oid. It re-writes the same record
     (present, active, the same six attributes).

  Her browser-route deny already exists and is intended (my email_deny half kept it). No other principal's deny is touched.
  **Browser effect: none.** This is exactly the effect class my OG-mg-1 half failed to read, and here it is read and empty.
- **Usage, with a control.** `download_filtered` calls by her principal since activation: **0**, over 21 day partitions (96
  objects read, 0 errors).
  - The scan sees her 5 other events and another principal's 1 download event, so the zero is not a blind instrument.
  - The general audit lake, which cannot see her principal, is reported and correctly NOT relied on.
  - The usage does not gate the act; it is reported for Andrew.
- **The writer:** N = 1 module (`schwab_entitlement_admin.py activate()`, Puts only). IAM is preflighted under the operator role;
  `DeleteItem` and `Scan` stay unused.

## Blast radius and both branches

- **What the act may touch:** four items in one principal's partition. Never another principal's items: Andrew's and the
  Bloomberg identity's grant hashes must read equal before and after. Never another `email_deny` key, and no IAM, gateway, policy
  or environment setting.
- **Branches:**
  - the bases still at profile 4 and grant 4: the act lands;
  - a stale base: the writer's optimistic condition refuses and nothing is written;
  - a failed read-back: restore at once.
- **Rollback:** a revision 6 restoring the before scope through the same writer, never a delete. Andrew can reverse it with one
  word, "Alyssa may download".

## Conditions (carried, not grounds)

1. **The CTO's CT1, which I concur in.** If the writer requires `--approver "Andrew Berman"`, the `operator_audit` line states that
   he did not approve this act in person, and that it enforces his 2026-10-08 word under the CTO ruling. An audit record that
   names an approver who did not approve is a false record, however the field is shaped.
2. **The read-back is through the installed code and makes no call as her:** `download_filtered` refused, one other operation of
   hers allowed, and the other two principals' hashes equal.
3. **No identifier in any repo file, row, message or report** (hashes, roles, operation names and counts only), as the ask states.

-- 3.0.0_SA_CVO~Z
