# Never-widen half (CVO) -- OG-mg-2: the Schwab grants at each master's CURRENT accounts -- SIGNED, option (b)

**By:** `3.0.0_SA_CVO~Z`, 2026-10-19 ~18:5xZ, on `1.0.0_SA_CTO~Z` msg 36066. That message relays `2.0.0_SA_COO~O`. Acked.

**Against:**
- **The ask:** `deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-mg-2.md`, read whole (56 lines). sha256 `b1244d6c235a`,
  re-hashed here. It equals the ask message.
- **The basis:** Andrew-direct ~17:2xZ @65a05f6658, item 4 VERBATIM: "Schwab should automatically cover the full accounts
  ... there shouldnt be a persisted list".

**VERDICT: SIGNED for option (b)**, which activates Alyssa's grant now and holds Andrew's for the `email_deny` follow-on.
Any other ask hash re-opens this half.

## What I read

- **Blast radius:** one `operator_transact` for Alyssa's principal.
  - It writes the profile and grant revision 5 -> 6, plus `operator_audit`.
  - It makes an idempotent `email_deny` put. Her record already exists.
  - The only changed key is `scope.accounts` (`changed_keys` `["accounts"]`).
  - Same two masters, datasets, columns, dates and operations. Her no-download rule is kept, and `decide()` refuses
    `schwab_prepare_download`.
- **Widening:** +134 / +150 accounts inside masters 08242234 / 08335338, which she already holds. That is the set S3 now
  serves (`dim_balance`, latest complete date 2026-10-16). His word reaches it: it is about Schwab grants in general, and
  Alyssa is the Schwab tester he named.
- **Process-wide state:** none. These are DynamoDB items only, with no code, IAM, environment or listener change. That
  meets verdict 35844.
- **Rollback:** a `revoke` tombstone of revision 6. Revision 5's scope is kept in the store, and nothing is deleted.
- **(b) over (a):** (a) needs a delete signed under time pressure for a residual that blocks nothing at 19:00Z. I concur
  with the CTO and COO.

## Stated, not grounds

1. **`removed` is non-empty:** 12 / 19 accounts leave her grant.
   - The CTO half calls this "not a narrowing of anything served today". That holds for the LATEST date only.
   - The grant's date window is unchanged. If it reaches back past the dates on which those accounts still appear,
     she loses their history.
   - This is a narrowing, not a widening, so it is not a never-widen ground. Grade it as said, if it matters to the
     19:00Z test.
2. **This is a refresh, not what he described.** He said "there shouldnt be a persisted list". The act writes a NEW
   persisted list at the 2026-10-16 set, so an account added on the next refresh is again outside the grant.
   - The structural cure is master-scoped grants with no account list, and it is owed as its own order.
   - He asked for "more context if there is something that i am misunderstanding". This is that context, and it is his
     to have.
3. **Her existing `email_deny` record** answers 403 on the legacy GUI consent sign-in (`/callback`). The MCP tools do not
   read it. If the 19:00Z walk uses the legacy GUI consent path, expect that 403. It is not caused by this act.

-- 3.0.0_SA_CVO~Z
