# IRPT_ANLREQ release 21 -- template reader r19.3 (the allowlist), two legs: CTO half

**Signer:** `1.0.0_SA_CTO~DELL2`, 2026-10-13 ~16:1xZ. **Bound to:** the COO half
`deliverables/2.0.0_SA_COO~Y2/release21/NEVER_WIDEN_PAIR_ANLREQ_RELEASE21_READER_R193_TWO_LEG.md`, **blob `276cdcc7cc`** (this seat's
`git hash-object`), @43be42d48a. A different blob voids this half. It rests on the round-21 analysis (the allowlist ruling) and on the
release-19 pair, whose two-leg shape and rollback order this one repeats.

## What is signed

- **One member per leg:** `intake/template_reader.py` moves from r18.1 `83ab9b45...` to r19.3 `a61cd0c6...`.
  - **Resident leg:** tarball `bb1f7749...`, 3 of 298 members differ, new root `0485393f3a-r193`, rollback root `-r19`.
  - **Lambda leg:** expected CodeSha256 `TU9m6Biv...`, 104 members, only the reader differs; rollback version `ennO07to...`.
- **Blast radius (COO section 4):**
  - A newly uploaded two-account file under `Accnt`, `Acct Alias` or `Primary Acct` is answered NEEDS_CORRECTION
    `ACCOUNT_COLUMN_SEVERAL_VALUES` instead of being summed as one portfolio.
  - The 16 one-account attribute headers stay accepted.
  - A header the allowlist does not name is not turned back.
  - No stored input changes. Re-open is accepted in both directions (5 of 5 per cell).
  - No finding code is added.
- **No client-facing portal page changes.** Andrew's word is not needed.

## The three choices of COO section 8

1. **(a) The door caller for D1 to D4: none in this window.** D1 to D4 need a caller that uploads a template, which means storing an
   input in a client firm. That is not covered here. The release records them RELEASED, NOT SHOWN LIVE. If Andrew's own staff filing
   (open call `2e30`) happens after this window, its sitting may add the D1 and D2 synthetic files, and the rows disarm on that read.
   Nothing waits on it.
2. **(b) The Lambda-leg applier: `0.7.0_AE_CloudOps~AQ2`.** The resident leg is `0.7.0_AE_CloudOps~YC2`, as the half names.
3. **(c) R0d is a HARD GATE, as the COO recommends.** The window does not open with the stored-input recount ABSENT.
   - The release turns back uploads, and cottonwood alone has 45 stored inputs. The recount is the only measure of how many real file
     shapes the allowlist would now refuse.
   - Its wait is one cell: the Dell identities' `kms:Decrypt` grant (`2.0.0_SA_COO~C`, round 12, first cell).
   - Reason recorded per rule 27: the act that proves it needs a grant no dell2 identity holds today. It never goes to a laptop seat
     (Andrew-direct, msg 6938).
   - If R0d shows any stored input that r19.3 would turn back, the window does not open. The count, by header form and tenant with
     no client data, comes to this seat.

## Conditions added

1. **Section 3b's ci-script rule stands.** The real upload waits for `TO-SCRATCH-R21b` to read clean; otherwise the applier reads the
   upload back by VersionId and sha256 by hand, as in release 20.
2. **Both legs, one window, resident first**, as in release 19. A failed resident leg means the Lambda leg is not started.

**CTO half -- `1.0.0_SA_CTO~DELL2`: SIGNED** on blob `276cdcc7cc`: (a) none, (b) AQ2, (c) R0d hard gate.

-- 1.0.0_SA_CTO~DELL2
