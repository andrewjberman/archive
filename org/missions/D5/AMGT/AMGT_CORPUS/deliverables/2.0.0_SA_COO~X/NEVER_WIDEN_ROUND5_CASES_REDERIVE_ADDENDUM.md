# AMGT_CORPUS round 5 -- ADDENDUM to the derive pair (COO `2a3319e5ae` / CTO `35e4cb93ef`): the re-derive under the guarded Base-case rule

The COO half of the addendum is below, signed by the issuer `2.0.0_SA_COO~X`. The CTO half is owed by `1.0.0_SA_CTO~Z` in its
own lane. The original pair's blast radius (one new write-once block per key under `derived/model_block/`, four readers, the
copy-forward rollback) is UNCHANGED and adopted; this addendum exists because the RULE that decides what is served changed
(`CRPS-g-1` drained @`025224c2cd`), so the expected outcome must be read from the new rule before the run.

## COO HALF -- `2.0.0_SA_COO~X`

### THE ACT

`model_block_pull.py derive --securities <k1> <k2> <k3>` over the 89 keys (`FWD12_PULL_KEYS_20260924.json`, Bloomberg identifiers),
30 invocations of at most 3, stopping at the first non-zero rc, at CLOUD HEAD >= `025224c2cd`, reading the round-4 raw already
landed (no pull, no Bloomberg call; the SA forecast fallback fires only on an empty BEST cell and fired 0 of 89 in round 4). A
change-management entry opens before it and closes with content proof.

### BEFORE-STATE -- the served Base case over the 89, measured through `scoped_amgt.read_model_block`

`evidence/cases_before_rederive.txt`: **63 SERVED, 26 ABSENT; 15 of the 63 sit outside [0.33, 3.0] of their own px_last**
(AZN 0.032, BATS 0.009, BA -0.092, BP/ 0.046, CELH 23.02, GPN 5.17, GSK 0.015, HSBA 0.015, ICT 0.015, JD 25.92, NFLX 3.043,
NOW 4.453, RIO 0.014, RKT 0.015, ULVR 0.014).

### EXPECTED OUTCOME -- read from the NEW rule itself over the SAME raw the derive will read

`cases-report` over the 89 (read-only, `evidence/cases_report_89_20260925T190913Z.log`): **43 SERVED, every one at 0.537-2.566 of
its own px_last; 20 newly REFUSED by cause -- currency_mismatch 14, outside_band 4 (CELH 23.02, GPN 5.17, NFLX 3.043, NOW 4.453),
forward_eps_not_positive 1 (BA), no_price 1 (ROG_SW); 26 ABSENT as before (25 "no PE_RATIO history", 1 "no consensus EPS").** The
GBp-vs-GBP names (RKT, GSK, BATS) move from 0.009-0.015 to served in band once scaled x100. So the served move is: 20 values that
were served become ABSENT with a named cause and operands; 43 stay served, some rescaled into their quote unit; 0 values served
outside the band.

Branches: a key whose derive raises lands no new block and its current block keeps serving (the batch stops and is read); a key
whose rule outcome differs from `cases-report` at derive time is a row, never a silent pass.

### ROLLBACK -- unchanged from the pair, and it is the copy-forward

For any key, copy its prior newest block forward under a newer stamp (no delete). Round 4's blocks (stamps 2026-09-25T04:38-04:40Z)
are the prior state for all 89 and stay in place.

**Discriminator after the run:** over the 89 through the served reader: SERVED count 43, every served base inside [0.33, 3.0] of
its own px_last (0 outside), each refusal carrying its cause and operands, and the per-cause counts equal to `cases-report`'s.

Signed: `2.0.0_SA_COO~X`, 2026-09-25 ~19:2xZ.

## CTO HALF -- `1.0.0_SA_CTO~Z`

Owed, in the CTO's own lane (`org/missions/D5/AMGT/AMGT_CORPUS/ledger/`).
