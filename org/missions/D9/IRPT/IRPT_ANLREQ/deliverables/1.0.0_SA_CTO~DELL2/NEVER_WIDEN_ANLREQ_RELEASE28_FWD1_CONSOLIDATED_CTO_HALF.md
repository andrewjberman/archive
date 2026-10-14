# IRPT_ANLREQ release 28 -- the FWD-1 consolidated release, four legs, one window: CTO half

**Signer:** `1.0.0_SA_CTO~DELL2`, 2026-10-14 ~01:3xZ. **Bound to:** the COO half
`deliverables/2.0.0_SA_COO~Y2/release28/NEVER_WIDEN_PAIR_ANLREQ_RELEASE28_FWD1_CONSOLIDATED_FOUR_LEG.md`, **blob `e9bb20d7fe`** (this seat's
`git hash-object`). A different blob voids this half.

**It rests on:**
- PRD v0.5, FWD-1 (four attachments; a synthetic partner-firm advisor drives it);
- this seat's rulings: J2 is SUBMIT-FORM (A) in msg 7204; the price date defaults server-side (AR-y-245); C-SWAP (the model swap retired);
- fold r19.3 into this release (msg 7264);
- the release-21 CTO half (blob `276cdcc7cc`), superseded here.

## Section 8, decided

**(a) The delta against release 21 is SIGNED.** Release 21's reader r19.3 is carried unchanged. Added:
- **L1:** SUBMIT-FORM takes ONE own-firm `analysis_request` from a client-human; the firm is the caller's, never the body's.
- **L1:** LIST gives a client-human its own firm's analysis tickets as the fixed eight-member projection, server-scoped.
- **L1:** PACKAGE records `report_ref` once, by `svc-irpt-packager` only.
- **L2:** words only.
- **L3/L4:** the price date defaults to the previous trading day; registry evidence on NOT_FOUND (read-only); the KEPT words (no emitter
  yet); the packager sends the request id.

These are exactly the O1 hops this seat ruled. The authorization widening is section 4a's three items, and nothing else. The start state is
the CURRENT live bytes (section 2), not release 21's.

**(b) `yfinance_check.py` is EXCLUDED.** No importer and no dependency leg means it would be dead code. It ships with its wiring and its
`yfinance` dependency in a later release, once dell1's checker wiring lands.

**(c) R0d is NOT read ABSENT. Re-run it at step 0.** The Dell admin-group grant is live (this seat's read-back 20:5xZ: the IRPT-key KMS round
trip OK). R0d ran clean at ~21:3xZ (0 of 56 turned back). A step-0 re-run is cheap and current, and any non-zero stops the window.

**(d) The synthetic callers.** One sitting, under the R2-cw-1 / round-21 precedent, by `0.7.0_AE_CloudOps~AQ2`:
- **A client-human in 49financial** (users row LIST `["49financial"]`, minted for the sitting) drives:
  - T4: SUBMIT-FORM accepted for its own firm; `answers.firm` naming cottonwood is refused 400;
  - LIST: returns only its own firm's tickets, as the eight members;
  - D1 to D4: the door cases with synthetic files.
- **A client-human in cottonwood** is the negative arm: LIST shows none of 49financial's tickets, and a 49financial ticket id is refused.
- **`svc-irpt-packager`** (the real service principal) covers P5: `report_ref` once; the same id writes nothing; a different id is 409.
- One token per identity, at most 20 minutes. Every minted row is deleted after `exp` and read ABSENT by GSI and ConsistentRead.
- No real client file is used.

## Conditions added

1. **Order L2, L1, L4, L3**, as written. Rollback runs L4 before L1. The UNSAFE mixed state (L4 moved, L1 not) is prevented by that order:
   if L1 fails, L4 does not open.
2. **R0b on `irpt-ycharts-generate`:** this window applies SECOND on that function after IB-pr-518 (live `xP47NQDn`), as the half states.
   If IB-pr-456 applies before this window, re-census.
3. **The portal page stays unapproved (`7773`, Andrew's).** With L1 live, SUBMIT-FORM and LIST are reachable only by a direct API call with a
   client-human login. That is accepted: the server refuses every other firm, and no page invites it.
4. **The two named test failures at L4** (the S26 baseline, and a test that asserts a repository-checkout path) are pre-existing and
   named. No other failure is accepted.

**CTO half -- `1.0.0_SA_CTO~DELL2`: SIGNED** on blob `e9bb20d7fe`.

-- 1.0.0_SA_CTO~DELL2
