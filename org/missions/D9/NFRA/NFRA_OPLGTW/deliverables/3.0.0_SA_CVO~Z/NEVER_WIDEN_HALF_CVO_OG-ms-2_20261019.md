# Never-widen half (CVO) -- OG-ms-2: Schwab master 08403355 added to Alyssa's grant

**By:** `3.0.0_SA_CVO~Z`, 2026-10-19 ~21:4xZ, on `1.0.0_SA_CTO~Z` msg 36127. That message relays `2.0.0_SA_COO~O`. Acked.

**Against:**
- **The ask:** `deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-ms-2.md`, read whole (53 lines). sha256
  `30351bdddf2d`, re-hashed here. It equals the ask message.
- **The basis:** Andrew-direct 2026-10-19T19:55Z (`ANDREW_DIRECT_20261019_195xZ_ALYSSA_SCHWAB_MASTER_0840_ADD_TO_ENTITLEMENTS.md`
  @3c6ce94b4f), VERBATIM: "she needs the 0840 master too added to her entitlements."

**VERDICT: SIGNED** at ask sha256 `30351bdddf2d`, on the ORDER of section 3: Phase B only after batch15's ledger is CLOSED
and the live marker is the batch15 sha. Any other ask hash re-opens this half.

## What I read

- **Only Alyssa's grant changes** (pk_hash `2c61471b14`, revision 6 -> 7). Andrew's grant stays at revision 1, and no other
  principal is touched.
- **Only one master is added,** `08403355`, the only `0840` prefix under `schwab/`. That maps his "0840" to one master,
  read, not assumed.
  - Its accounts are the current 30, by the `dim_balance` method accepted for OG-mg-2.
  - Her two existing masters' account sets are unchanged (7599 / 7690, `other_masters_accounts_unchanged` true).
- **`changed_keys` is `["accounts", "masters"]` and nothing else.** The datasets, columns, window and operations are the
  same.
- **Her no-download rule stands.** `decide()` on the candidate refuses `schwab_prepare_download`, and `download_filtered`
  is refused by the scope.
- **The order is the ground I sign on.** The live code would reject a grant naming an unknown master, and that would deny
  her WHOLE Schwab access. Phase B therefore waits for batch15 CLOSED. A batch15 rollback reverts this grant FIRST (a
  revoke tombstone), and that is the same order OG-rz-2's section 7 states. Both asks agree, and my OG-rz-2 half
  (@86c19380ab) reads it the same way.
- **Process-wide state:** none. These are DynamoDB `POLICY#` items under the operator role. That meets verdict 35844.
- **Rollback:** a revoke tombstone, with revision 6 kept in the store to re-activate. There is no delete.

## Noted, not grounds

- **The same refresh shape as OG-mg-2.** The grant persists a 30-account list at 2026-10-16, so an account added to 0840
  later falls outside it until the master-scoped cure (owed since OG-mg-2) lands.
- **The master's registry row** (`scopes.json`, OG-rz-2) carries `firm: 49financial` for 0840, while Andrew called the
  three masters "the smartx and black diamond masters". Alyssa is Opal staff, so this widens no partner firm. The firm
  label is the registry owner's to confirm.

-- 3.0.0_SA_CVO~Z
