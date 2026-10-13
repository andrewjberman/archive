# NEVER-WIDEN -- COO HALF: mint a saved Dow Jones session for `wsj` and `barrons` from the existing credential, `HVST-bz-6` (round 84, workstream WSJBARRONS)

**Signer:** `2.0.0_SA_COO~W1`, 2026-10-13 ~12:5xZ. **Pairs with:** `1.0.0_SA_CTO~DELL1`'s half at `ledger/NEVER_WIDEN_ROUND84_BZ6_CTO_HALF.md` (owed).
**Authority for the act itself:** Andrew-direct 2026-10-13 ~12:2xZ item 4 (CTO msg 4795): "we have credentials and HARVEST scripts that do this"; the sign-in
he was asked for is withdrawn and the existing credential and script are to be used with no new vendor scope.

## THE ACT, in the order's words

Site Z, once, the two publishers one at a time (`wsj`, then `barrons`), through ONE script, `deliverables/2.0.0_SA_COO_W1/round84/bz6_session_state.py`:
1. **Read the state first and change nothing** (`<S> <publisher> --runtime-root "<runtime>"`): a saved session is VALID when it has `subscriber=True` and
   `network_auth_corroborated=True`.
2. **Mint only where the read says `VALID=False`, ONE attempt per publisher** (`--mint`), by `SessionManager.refresh`, which runs the CRO's
   `dowjones_harvest_session.py` with the credentials read BY NAME from `dowjones/credentials` and writes the box's own DPAPI vault. A valid session gets no sign-in.
3. **The first refusal stops BOTH publishers** (the account is shared and a second attempt can lock it): one row, no retry.
4. Read the state again. No output file, row or commit holds a secret, a cookie, a username or the vault content.

## BLAST RADIUS

- **Writers of the property N = 1 per publisher:** the box's own vault file `<runtime>/secrets/<publisher>.dpapi`, replaced atomically by `SessionVault.save`.
  It is a per-Windows-user DPAPI file that no other user can decrypt.
- **What it touches in the world:** one Dow Jones SSO sign-in per publisher that needs it, with the existing shared account, from the box that already holds
  its sessions (the runner's own box and user). One headful Chrome window opens on the desktop for the duration (`--wait-seconds 120`).
- **What it reads:** one Secrets Manager secret by name, `dowjones/credentials`, as the existing harvester already does (last accessed 2026-09-30).
- **Not touched:** S3, any bucket, `config.json`, the runner task (not stopped, not started, not re-registered), silver, bronze, gold; no `--park`, so no
  new secret is created. The running runner (PID 50360) is untouched; it reads the vault at its next job.
- **Rollback:** none needed for state (a saved session only enables sign-in-free reads); if a minted session misbehaves the old file's absence is
  the prior state, and the runner's `--no-sign-in` ends a job `sign_in_refused`, a recorded result.

## BOTH BRANCHES (the half is signed for BOTH or for neither)

- **Branch M (the state reads `VALID=False`, the mint returns `DONE` and `VALID=True`):** the session is saved and the cell's criteria hold.
- **Branch S (the state reads `VALID=True`):** no sign-in is made; the criteria hold on the existing session.
- **Branch R (a mint returns `REFUSED` or exit 3):** NO second attempt, the other publisher is not tried, one row; the question returns to the issuer.

## WHAT THIS HALF DOES NOT COVER
- `--park` or any write to Secrets Manager or S3; reading or printing a secret value, a cookie, a username or a password; a second sign-in attempt.
- Any new account, publisher, vendor or scope (Seeking Alpha, FT and Bloomberg are not in it).
- A cycle read (that is `HVST-bz-7`, read-only), or any change to the runner.

## VERDICT: SIGNED (COO). Not started until the CTO half is on file.
