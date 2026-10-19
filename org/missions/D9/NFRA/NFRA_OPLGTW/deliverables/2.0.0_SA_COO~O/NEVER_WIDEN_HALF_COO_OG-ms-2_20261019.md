# Never-widen half (COO) -- OG-ms-2: add Schwab master `08403355` ("0840", the Tax SMA master) to ALYSSA'S grant; ONLY `scope.masters` and `scope.accounts[08403355]` change (SIGNED)

By: `2.0.0_SA_COO~O` (issuer), 2026-10-19 ~21:4xZ.
Against: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-ms-2.md` (`~NFRA1` Phase A, msg 36124, read 2026-10-19T21:25:20Z), sha256 prefix `30351bdddf2d` (recomputed by this seat from the file: `30351bdddf2d2ef9...`, equal to the applier's).

## SIGNED, on conditions J1-J7

What this seat read at signing:
- **`ms2.AC1`, issuer re-run: PASS** (before-record with Alyssa's `pk_hash`, per-master counts and account-set hashes, the new master's count and latest complete date, the scope hash and a printed denominator; `changed_keys` reads `["accounts", "masters"]`, the two existing masters' accounts unchanged; decide() on the candidate admits the four read tools and refuses `schwab_prepare_download` for the new master; the ask has three halves, the process-wide state line, 0 e-mail-shaped strings, 0 runs of 9 or more digits).
- **The widening, stated plainly:** Alyssa's grant (grant revision 6, written by `OG-mg-2`) gains ONE master, `08403355`, at its full CURRENT set of 30 accounts (the distinct `account_id` of `dim_balance` at the latest complete date 2026-10-16, the `OG-mg-2` method the CTO accepted); the same four datasets, the same operations (`list`, `describe`, `query`; her no-download rule stands), the same columns and rolling window. Her 7,599 and 7,690 accounts on the other two masters are not touched. Andrew's grant (revision 1, held) and every other principal are not touched. `08403355` is the only `0840` prefix under `schwab/` (applier's read) and its four silver datasets hold data at 2026-10-16.
- **The fact the ask puts first, which I carry as the main risk:** the LIVE gateway does not know `08403355` until batch15 (`OG-rz-2`) is deployed; a grant naming it would be rejected by the running code and would deny Alyssa's WHOLE Schwab access, not only the new master. That is why Phase B starts only after the batch15 ledger is CLOSED (J2), and why a batch15 rollback after this activation reverts this grant first (J5).
- **Her `email_deny` record already exists**, so the activation's idempotent put changes nothing; Andrew's is not touched because his grant is not.
- **Rollback (section 4):** `revoke` of the new revision, a tombstone, never a delete; the previous scope (grant revision 6) is re-activated as a new revision if she is to keep her two masters.
- **What I did NOT read:** a live grant, or the running gateway's behaviour. Every Phase B fact is proven only in Phase B.

## Conditions J1-J7

**J1 -- the ask stays at its bytes through the GO** (sha256 prefix above). Any change re-opens all three halves.
**J2 -- Phase B starts only after BOTH:** the batch15 ledger `nfra-oplgtw-gateway-resize-t4g-large` is CLOSED, and the live marker on the host equals the batch15 release sha (read by the applier at the start of Phase B and printed). My GO names this.
**J3 -- ONE record:** Alyssa's activation only, through `activate` under `opal-gateway-access-admin`, `--approver "Andrew Berman"`; no delete of any kind; no other profile or grant is written. A re-read at the start of Phase B finding her grant revision different from 6 re-cuts Phase A once.
**J4 -- the read-back runs against the DEPLOYED tree:** `decide()` on her LIVE grant is run in a guarded fresh process importing the deployed `app/` on the host (not the repo), because the question is whether the RUNNING code accepts her grant; `W/MS2_READBACK_DECIDE.json` carries `"tree": "deployed"` and `"code_sha"` (the live marker) beside its answers, and `ms2.AC2` requires both. It admits the four read tools, refuses `schwab_prepare_download` for `08403355`, and answers as before for her two existing masters.
**J5 -- rollback order:** if batch15 must be rolled back after this activation, this grant is reverted FIRST (the tombstone, then the revision-6 scope re-activated as a new revision), and only then is the live ref's tarball redeployed.
**J6 -- a failed read-back is an incident, not a note:** the new revision is revoked and the revision-6 scope re-activated at once (her whole Schwab access depends on it), the ledger is closed ROLLED BACK, and I am told the same turn.
**J7 -- the CLOSED time** of ledger `nfra-oplgtw-ms2-alyssa-master-0840` goes to `2.0.0_SA_COO~O` at once; counts and hashes only in every record.

Gate limb: none graded (a signed half is a file in lane `TREE_DELIVERABLES`). Push state: LOCAL.
