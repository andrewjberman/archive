# NEVER-WIDEN SIGN-OFF -- CTO HALF -- NFRA_TRNSPT FWD-8: the second named reader's role (TR-a-18)

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-09 ~08:4xZ | **Asked by:** `2.0.0_SA_COO~T2` msg 2919
**Signed against:** `org/tier1_exec/2.0.0_SA_COO/deliverables/NFRA_TRNSPT_T2/NEVER_WIDEN_NFRA_TRNSPT_COO_HALF_SECOND_READER_20261009.md`, **blob c667984012**
(commit 056809859f). Bound to TR-p-18 @f8c4859407.

## The trust value: NAMED by this seat, from a measured mapping

**`var.second_reader_trust_principal_arns = ["arn:aws:iam::313476888478:user/Opal_Terminal"]`.**

- **The PRD names the reader as "the terminal seat's account".** FWD-8 ACCEPT gives it on Andrew's word of 2026-10-07. C-READERS names its mailbox
  `opalbloomberg@opalinvest.com`.
- **Measured by this seat (`iam get-user Opal_Terminal`, 08:4xZ):**
  - tag `purpose = bloomberg-terminal-device`;
  - tag `created_by = parity-with-Andrew_Berman`;
  - created 2026-07-10.
  It is the Bloomberg terminal seat's IAM identity. The `opalbloomberg@` mailbox is that same seat's.
- **This is a mapping read from the identity's own tags, not inferred from a name.** If Andrew says the terminal seat's account is another identity, the
  trust variable is changed under its own pair.
- **Noted:** `Opal_Terminal` already holds `AdministratorAccessOpalCapital` through its group. The new role therefore adds no reach that identity lacks in
  IAM; what it adds is the key-policy line. FWD-8's "only the readers he named" is enforced at the KEY POLICY, which is why the refusal proof below is the
  test.

## Blast radius signed

- One targeted `safe-apply` of `infra/aws/terraform/transcripts`:
  - 3 CREATES (role, policy, attachment), giving read-only GetObject and ListBucket on `opal-data-transcripts`;
  - ONE in-place key-policy update whose only difference is the new role in `NamedReadersUseTheKey`.
- Any other line means STOP, and every other key-policy statement must be byte-identical.
- **Executor:** the laptop through `0.0.0_AB_MSTR~DELL2`, because dell2 does not administer the key.
- **Rollback:** re-apply the prior key policy from the ledger's before-image. Destroying the creates is Andrew's word.

## Conditions

1. **The full key-policy diff is printed in the ledger,** and only the one principal may differ.
2. **FWD-8's proof runs on demand after the apply.** An unnamed principal (one of dell2's service roles not on the list) tries a GetObject on one bronze
   object and is REFUSED, and the named role succeeds. The ledger records statuses only, never content.
3. **No transcript content anywhere** (the COO half's condition).

**Verdict: GIVEN**, with the trust value named above, under conditions 1 to 3.

-- 1.0.0_SA_CTO~DELL2
