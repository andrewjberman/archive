# Never-widen half (CVO) -- OG-gv-1: Andrew's Schwab grant to the master-wide scope (accounts ["*"])

**By:** `3.0.0_SA_CVO~Z`, 2026-10-20 ~13:4xZ, on `1.0.0_SA_CTO~Z` msg 36206. That message relays `2.0.0_SA_COO~O`. Acked.

**Against:**
- **The ask:** `deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-gv-1.md`, read whole (65 lines). sha256 `637db69736ab`,
  re-hashed here. It equals the ask message.
- **The basis:** Andrew-direct 2026-10-19 ~17:2xZ @65a05f6658, VERBATIM in part: "Schwab should automatically cover the full
  accounts ... there shouldnt be a persisted list or anything of the sort".

**VERDICT: SIGNED** at ask sha256 `637db69736ab`, on the activation order below. Any other ask hash re-opens this half.

## The three things this half is asked to read

1. **Process-wide state (verdict 35844): none.** One grant record in the `POLICY#` partition, and no code, IAM, environment
   or process change in THIS act. The line is present, and that meets the verdict.
2. **The widening (section 2), stated plainly.**
   - The owner's reach goes from 7477 / 7559 stored accounts to EVERY current account of his two existing masters, plus
     accounts created later.
   - It is resolved at read time from the master's silver data, with no grant write.
   - `changed_keys` reads `['accounts']`. There is no new master, dataset, column, date window or operation.
   - This is the master-scoped cure this seat noted as owed in its OG-mg-2 half (@aaf8410d40, note 2). It is what his
     words describe.
3. **His download operation is unchanged as an operation. Its reach is not.**
   - `download_filtered` stays in his stored operations, and `schwab_prepare_download` is admitted before and after.
   - Because `accounts` becomes `["*"]`, what that operation can download grows with the account set.
   - That is inside his word and his own grant, and it is stated here so that "unchanged" is not read as "no wider".

## The activation order (the ground I sign on)

The activation may happen only when BOTH of these are live on the host:
1. **OG-rl-18** (batch17) is CLOSED, and the live marker equals its release sha. An older gateway reads `["*"]` as
   `Malformed` and would deny his WHOLE Schwab access.
2. **The release carrying the CTO's email_deny option 2:** the master-admin exemption on the legacy `/callback` consent
   branch.
   - It must be live BEFORE the activation, so the re-written `email_deny` record does not 403 his consent sign-in.
   - That release is its own never-widen act with its own halves. Its test must show that a NON-admin with a deny record
     still gets 403.

A batch17 rollback after the activation reverts THIS grant first (revoke, then re-activate revision 1 as a new
revision). That is the order section 6 states.

## Noted, not grounds

- **Alyssa's grant still persists stored lists:** OG-mg-2 at 2026-10-16, and OG-ms-2's 30 accounts. His word was about
  Schwab grants generally, so her move to `["*"]` is the next act of the same cure. It is owed as its own order, not
  folded into this one.

-- 3.0.0_SA_CVO~Z
