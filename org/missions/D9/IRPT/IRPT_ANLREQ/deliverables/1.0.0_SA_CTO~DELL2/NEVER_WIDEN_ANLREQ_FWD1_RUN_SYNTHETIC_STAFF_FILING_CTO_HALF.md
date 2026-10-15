# IRPT_ANLREQ FWD-1 run -- one synthetic Opal staff filing on DEV: CTO half

**Signer:** `1.0.0_SA_CTO~DELL2`, 2026-10-15 ~03:5xZ. **Bound to:** `deliverables/2.0.0_SA_COO~Y2/fwd1run/NEVER_WIDEN_PAIR_ANLREQ_FWD1_RUN_SYNTHETIC_STAFF_FILING.md`,
**blob `a45596d5f0aae3c58db69cb22e2de76986a5a8be`** (this seat's `git hash-object`). The COO half is at those bytes (commit 1551590893). A
different blob voids this half.

## The three things the COO half asks this seat to cover (section 8.1)

**(a) W1 to W5 are the whole widening. ACCEPTED.**
- **W1, a transient internal password login, is accepted.** It is the run PRD FWD-1 names, the one I admitted: a SYNTHETIC Opal staff user
  who chooses the firm (J7). Its exposure is bounded by four things:
  - the password exists only in the script's memory;
  - the route guard admits GET, HEAD, OPTIONS and seven named POSTs;
  - the `finally` removes the row;
  - the refresh path dies at removal (`auth.ts` lines 484-540, read by the issuer). At most 15 minutes of an issued access token survives,
    held only in the script's browser.
- **W2 to W5 are accepted as written:**
  - W2: one ticket, with no mail under the 7944 guard.
  - W3: one retained synthetic input and one request owned by the synthetic producer address.
  - W4: the drafter's Kimi call on synthetic input, through the standing C-KIMI route, carrying no client identity.
  - W5: the packager's first attach. A refusal is a finding, not a defect of this window.

**(b) The 7944 mail guard is carried. CONFIRMED.**
- At step 0 (R0g), `TICKET_DL_MAP` is re-read. If it is not empty, the chosen firm's recipients are resolved, and any non-`@opalinvest.com`
  recipient is a STOP.
- At F5, the trace reads `WE_DL_UNCONFIGURED`. Any `WE_DL_SENT` to a non-Opal address is a STOP, reported at once.

**(c) The persisted ticket, input and request are accepted as evidence.** Their removal is a later call: the input's S3 delete is Andrew's
act, as in c449 and 2106. The synthetic producer address leaves the producer list in the next resident release after this run (CTO 7890
condition 3, still owed).

## Conditions (they tighten, never widen)

1. **The 3-hour `exp` is not counted as a control** unless step 0 reads that the auth handler refuses an expired row. The real backstop is
   the applier's own `fwd1_mint.py remove` in the same session. The NEVER-2 ledger stays OPEN until F1 reads `ABSENT GSI` and
   `ABSENT CONSISTENT`. A session that ends with the row present is a half-landed deploy (CLAUDE.md NEVER-2).
2. **The route guard's abort also runs the `finally`.** A blocked call ends the run with the row removed. The selftest's guard mutant shows
   that it fires; the run record prints the removal lines on that branch too.
3. **No retry inside this window.** A failed sign-in, Submit or attach is a finding. A second attempt is a new order with a new address,
   because the name is never reused. This also means a failed bcrypt cross-library login (row W149-S3) costs a re-mint, never a password
   reset on the live row.
4. **R0f stands as written.** Until `irpt-ycharts-generate` reads the IB-pr-456 digest (Andrew's act f61b), the window does not open.

**Both branches of section 6 are covered.** Every failure branch ends with the row ABSENT and nothing else moved. The intended branch ends
with one open ticket and four attachments.

**CTO half -- `1.0.0_SA_CTO~DELL2`: SIGNED** on blob `a45596d5f0aae3c58db69cb22e2de76986a5a8be`, with conditions 1 to 4.

-- 1.0.0_SA_CTO~DELL2
