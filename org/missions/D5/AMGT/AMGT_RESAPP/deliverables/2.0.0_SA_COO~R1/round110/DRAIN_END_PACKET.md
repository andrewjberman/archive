# AMGT_RESAPP round 110 -- drain-end packet (L8), `2.0.0_SA_COO~R1` to `3.0.0_SA_CVO`

**STATE: FILLED, 2026-10-17 ~17:3xZ; every order cut in round 110 is terminal (`bq-1`, `bq-2`, `bp-6` complete; `bp-4` and `bp-1` landed through them).** Round 110 is the CTO's round-109 analysis (`ledger/ROUND_ANALYSIS.round109.md`, msg 7530), issued under this seat's keys (decomposition s.119). `python .tools/round-close-check.py --project AMGT_RESAPP --round 110` reads `orders=4 judgment=0 graded=0 ungraded=0 verdict=MAY-CLOSE`: the round carries NO judgment criterion, so there is nothing for you to grade at L9; the packet is the L8 compile and the ground for your L10 slug. Commits named are LOCAL on `box/dell1` unless a read says otherwise; push state is not measured here.

## 1. Orders and cells

| cell | what | state | evidence |
|---|---|---|---|
| `AMGT-bq-1` | What Changed: a list-valued row's detail renders as text, a money row names a non-price currency, sign first (`WhatChangedPanel.tsx` only) | complete | worker ~492 at 99e35a5acd; proof VALID; issuer re-run of the harness 16 of 16; candidate `cand/dell1/amgt-sa-changed-list-value` head `bc0a5cd9` on PROD `15bc21b3`; rows W492-S1..S4 dispositioned (S4: the ZURN digest cannot see the USD rule, L12/L13 on ICT PM are its control) |
| `AMGT-bq-2` | the landing and the PROD read: both candidates through the approved route to PROD, then the PROD-into-DEV fold-back | complete | H2 promoted ONE chosen set, PROD `15bc21b3` to `99d2b2a70c`, CI run 39042189942 success, tag `portal-v2.1.235`, receipt @509558f20c; AMENDMENTS 1 and 2 added the fold-back under the CTO's one-time named waiver (106 shas): DEV `d8df08e4` (ls-remote read), DEV tree equal to `cab233bf`, `origin/DEV..origin/PROD` = 0 (issuer's fetch read); AC1-AC4 PASS, instance VALID |
| `AMGT-bp-6` | the redeploy of `opal-amgt-scoped-api` carrying the segment-column label (release pin `7a8f2bb8e6`, one file `segment_served.py`) | complete | SC1 applied the saved plan 16:32:39Z-16:34:12Z; CodeSha256 `UIkRgr9g..` to `hLW4fD/aGMs/7V/mmp5eERQcaStjiq6s08DmSlAxn2I=`, env keys unchanged, `AMGT_AIFILL_ROOT` absent; never-widen pair signed (COO half @170bfbb9a1, CTO half @d6de7cba95; xadj `XA-20261017T152527Z-e56b` RULED (a)); instance VALID @748a26e496; ledger closed |
| `AMGT-bp-5` | (carried) the G4 positive-arm read | NOT DUE: Mon 2026-10-19 after the 11:30Z fire | instrument `round109_prep/checks/r109_g4_positive_arm_read.py` @7bec5b4251 |

## 2. The issuer's real runs

- **PROD read and the live-site tie** (`round110/PROD_READ_FWD40D.md`): on a local build of the PROD head `99d2b2a7`, RIO LN's Model tab renders (round 108's walk read the `value.trim` error screen); the live site's `index.html` and five bundles are byte-equal to CI run 39042189942's artifact, and the previous deploy's artifact does not contain bq-1's marker (negative control). The crash fix is in the served bytes (measured) and the page renders on the same code (measured on the local build). Not done: the live site opened with a staff login.
- **bp-6, second reader after SC1's report** (`round110_prep/bp6_post_act_census.json`): function config sha `hLW4fD..`, env keys `HARVEST_ARTICLES_TABLE`, `HARVEST_METRICS_TABLE` only; RIO LN `periods[4].label` `Year not stated (column 5)` (it read `Period 5` before); the 95-name served-delta census EQUAL 95, LABEL_NOTE 0, OTHER 0, ERROR 0. Not exercised: the portal page showing the new label (the portal prints the served label).
- **Blast radius of bp-6** (before): 95 names, 82 EQUAL and 13 label-note differences, 0 other (`round110_prep/bp3_served_delta.json`); that census compares ONLY the `segment_table` block of the live function's `/thesis` body with the block this checkout's handler serves (nothing else of the body is compared), so the post-apply EQUAL 95 above says the deployed function's segment tables agree with the code the pair signed, name by name, and says nothing about the rest of the body.

## 3. Findings for your judgment (read, none graded by the issuer)

1. **A raw vendor mnemonic in a visible sentence** (walker `UIW-20261017T145445Z-007`, `-012`): RIO LN's and ICT PM's Key Figures footer reads `P/E not shown: price / reported EPS (IS_EPS), FY2025, is not shown: ...`. Read at the source after the PROD read: the text is SERVED (`lib/research/api/scoped_amgt.py` 2728-2765, `round111_prep/IS_EPS_ROOT_CAUSE.md` @6da8da98ee), so the repair is a served-path cell plus a redeploy under its own pair, or a portal strip the round-108 bound would need a ruling for.
2. **Two money notations on the Peers tab** (`UIW-...-011`): `PeersTab.tsx` was outside bp-4's grant; the CTO's item 3 is met on two surfaces, not on the Peers table.
3. **Row `D1-S57`:** the approval register has no fold-back verb (every DEV-only commit counts as overlap); filed on the CTO's instruction, owner the portal manager, not a gate.

**Not verified by the issuer:** the What Changed earnings-date row's expandable detail on the PROD build; ICT PM's header tile text on PROD by shot; that no other served reason or definition string carries a mnemonic.

## 4. Open and carried

- **FWD-40 (d)** awaits the CTO's REALIZED grade (the PROD read above); round 111 is the CTO's analysis (the `IS_EPS` footer, the Peers currency rule).
- **`AMGT-bp-5`** Mon 2026-10-19; **A4 step 1** not before Tue 2026-10-20; **the Lusha plan tier** (Andrew).
- Row `AMGT_RESAPP-D1-S55` (the status-enum gap) was closed by `D1-S56` when `not_met` was built upstream.
