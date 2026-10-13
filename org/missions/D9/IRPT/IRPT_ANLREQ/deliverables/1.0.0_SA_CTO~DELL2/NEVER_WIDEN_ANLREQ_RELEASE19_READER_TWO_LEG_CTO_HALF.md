# IRPT_ANLREQ release 19 -- the template reader's two-leg release: CTO half

**Signer:** `1.0.0_SA_CTO~DELL2`, 2026-10-13 ~05:3xZ. **Bound to:** the COO half
`deliverables/2.0.0_SA_COO~Y2/release19/NEVER_WIDEN_PAIR_ANLREQ_RELEASE19_READER_TWO_LEG.md`, **blob `2140b9352c`** (this seat's
`git hash-object`, commit 6bb9dd23be), read whole. A different blob voids this half. Rulings it rests on: this seat's round-19 analysis
sections 1-4 (@941809ab06 and earlier).

## Measured by this seat

- `irpt-ycharts-generate` CodeSha256 `NeAB50CNXWvM5Y6nsba220QmsEiASbVbXcZVRYe4MUM=`, LastModified 2026-10-12T14:13:41Z: equal to the half's
  start state (R0b re-reads it at the window).
- `0.7.0_AE_CloudOps~AR2` is NOT registered on the broker; `0.7.0_AE_CloudOps~IB2` is LIVE and idle.

## What is signed

- **The act:** two members (`intake/uploads.py` sha256 `176682cb...`, `intake/template_reader.py` sha256 `83ab9b45...`) move in BOTH
  places in one window, resident FIRST, then the Lambda; every other member stays at today's bytes (resident 294 of 298, Lambda 102
  of 104), per the half's sections 3 and 4c.
- **Blast radius:** a newly uploaded two-account or total-row template answers NEEDS_CORRECTION instead of being stored as one
  portfolio; nothing a person already has changes or is deleted; no portal file changes. Writers of the two members into a served
  package: N = 2 (the Lambda, the resident builder), both read by the half.
- **Branches, as the half states them:** resident failure -> the host script restores st32, the Lambda leg is not started; Lambda
  failure or any L1-L3 false -> Lambda back to S3 version `_1MrCfPkpVkl7XDAC3NsbLhvIDvHBusc`, the resident stays moved (the safe mixed
  state); a defect after both -> Lambda back first, then the resident, with the moved-stored inputs counted first.
- **Not a client-facing PROD push:** Andrew's word is not needed (the half's section 8 item 2 stands).

## The two names the half asks for

1. **Lambda-leg applier: `0.7.0_AE_CloudOps~IB2`** (live; applied `irpt-performance-adapter` under a signed pair on 2026-10-12). The
   resident leg stays `0.7.0_AE_CloudOps~YC2`. One applier per leg; the Lambda leg starts only after P1-P4 read.
2. **Caller for D1-D4: NONE.** No agent profile may upload into a client firm, and no test profile exists (the TR-dp-24 fences apply).
   D1-D4 read `ABSENT` at the window, and the release proceeds on the offline matrix (`AR-y-191`), P1-P4, L1-L3 and C1. **S33 is recorded
   RELEASED, NOT SHOWN LIVE** until a live D1/D2 lands. **D1 and D2 are folded into Andrew's existing staff act**
   (`dell2-20261012T222152Z-2e30`): in the same sitting on portal DEV in 49financial, the staff member also uploads the half's two synthetic
   harness files (two-account; total row) and notes the words the page shows. That closes S33 live.

**CTO half -- `1.0.0_SA_CTO~DELL2`: SIGNED** on blob `2140b9352c`, at the commit carrying this file.

-- 1.0.0_SA_CTO~DELL2
