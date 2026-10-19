# Never-widen half (COO) -- OG-mg-2, the Schwab grants at each granted master's current accounts: ALYSSA'S activated now, ANDREW'S held (option b) (SIGNED)

By: `2.0.0_SA_COO~O` (issuer), 2026-10-19 ~18:3xZ.
Against: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-mg-2.md` (`~NFRA1` Phase A, read 18:18:50Z), sha256 `b1244d6c235adc3db2ef35387fefa1a7eba37bb217732bde436b924b382aea8c`, recomputed by this seat from the file at signing (see G1).

## SIGNED for Alyssa's record; Andrew's record HELD -- option (b) of section 3, on conditions G1-G6

What this seat read at signing:
- **`mg2.AC1`, issuer re-run: PASS** (before-record with both roles, `pk_hash`, per-master counts before and current, scope hash and denominator; current >= before on every master; `changed_keys` reads `["accounts"]` for both roles; decide() on Alyssa's CANDIDATE admits `schwab_get_access`, `schwab_list_files`, `schwab_describe_dataset`, `schwab_query` and refuses `schwab_prepare_download`; three halves, the process-wide state line, 0 e-mail-shaped strings, 0 runs of 9 or more digits).
- **The counts (section 1), read from `MG2_DIFF.json` and `MG2_BEFORE.json`:** each of the two grants is the same on both masters: 7,477 -> 7,599 accounts (134 added, 12 removed) on `08242234`; 7,559 -> 7,690 (150 added, 19 removed) on `08335338`. The 7,690 equals the CTO's measure.
- **The method (section 2):** the distinct `account_id` of `dim_balance` at the latest complete date (2026-10-16 for both). Accepted: it reproduces the CTO's measure, and it is the column the gateway's Schwab tools filter on.
- **The removed accounts are named, not hidden:** 12 and 19 accounts are in each frozen grant and are NOT in the latest complete `dim_balance`. Andrew's word is "the full accounts ... what is being refreshed in AWS every single day"; an account the refresh no longer carries leaves the grant. Accepted.
- **The widening, stated plainly:** Alyssa's grant gains 134 and 150 accounts and loses 12 and 19; no operation, master, dataset, column or date window changes; her no-download rule stands.
- **Rollback (section 4):** `revoke` of the new revision, a tombstone, never a delete; the previous revision (grant revision 5) is the value to restore.
- **What I did NOT read:** a live grant. Every Phase B fact is proven only in Phase B.

## Section 3: `email_deny` -- I name (b)

Activating a candidate re-creates the principal's `email_deny` record in the same transaction (row W3-S22, the `OG-mg-1` side effect). Alyssa's record already exists, so her activation is an idempotent put: no change. Andrew's record does NOT exist; re-creating it would make the legacy consent sign-in (`/callback`) answer 403 for him while it stands, and the only way to remove it is an audited DELETE, which this order forbids and which needs its own order, ledger and halves.
**(b): activate Alyssa's grant NOW; HOLD Andrew's grant** until the deny handling is ruled as its own act. Why: (i) the test at 19:00Z is Alyssa's, not Andrew's; Andrew's pages stay open anyway (`OG-en-14`), and his grant still covers 7,559 and 7,477 accounts, an old but valid list; (ii) (a) puts a delete into a live window with no time to read it back; (iii) (c) risks Andrew meeting a 403 on a consent sign-in in front of her. Andrew's activation plus the removal of his one `email_deny` record rides a FOLLOW-ON order after the session (round-47 item 13 area), under its own halves. This is the issuer's reading of "Andrew-direct: the full accounts" for Andrew's own grant; it is his to widen at once if he says so.

## Conditions G1-G6

**G1 -- the ask stays at its bytes through the GO.** Its sha256 is recomputed by the applier and named in the GO; a changed byte re-opens all three halves.
**G2 -- Phase B re-reads step 1 first:** nothing may have moved since 18:18:50Z (a changed grant revision for either principal re-cuts Phase A once).
**G3 -- ONE write:** Alyssa's activation only, through `activate` under `opal-gateway-access-admin`, `--approver "Andrew Berman"`; Andrew's record is NOT activated and the applier writes `W/MG2_ANDREW_HELD.md` (one line: held under option (b), COO half, the reason) so `mg2.AC2` grades it as unchanged.
**G4 -- no delete of any kind:** the `email_deny` records are not touched.
**G5 -- the read-back:** decide() on Alyssa's LIVE grant admits the four read tools and refuses `schwab_prepare_download` (`W/MG2_READBACK_DECIDE.json`); `mg2.AC2` is read by this seat before `OG-mg-2` is flipped.
**G6 -- the CLOSED time** of ledger `nfra-oplgtw-mg2-schwab-full-accounts` goes to `2.0.0_SA_COO~O` at once (the session is at 19:00Z); counts and hashes only in every record.

Gate limb: none graded (a signed half is a file in lane `TREE_DELIVERABLES`). Push state: LOCAL.
