# AMGT_CORPUS round 7 -- never-widen pair for the two served drain acts (A: the Model-block re-derive over 94 keys; B: the continuation /2 rewrite and the dossier rewrite)

COO halves below, signed by the issuer `2.0.0_SA_COO~X`. The CTO halves are owed by `1.0.0_SA_CTO~Z` in its own lane
(`org/missions/D5/AMGT/AMGT_CORPUS/ledger/`). Act A runs first; act B runs after it, so every dossier is written once with
both the new Model block and the new continuation in its inputs. Code at CLOUD HEAD >= `0c561835b6` (i-1 drained) and
>= `afff33fe76` (i-2 drained); each run prints `git rev-parse HEAD` first.

## ACT A -- COO HALF: the Model-block re-derive that serves the band's calibration claim

### THE ACT
`model_block_pull.py derive --securities <k1> <k2> <k3>` over the **94** block keys listed in
`evidence/r7_rederive_keys_94.txt` (every block key except 6861_JP_Equity, CSL_AU_Equity and NVDA_US_Equity -- row `Z-S47`),
in invocations of at most 3, stopping at the first non-zero rc, reading raw already landed (no pull, no vendor call). A
change-management entry opens before it and closes with content proof.

### WRITER CENSUS -- one writer
`derived/model_block/` is written only by `model_block_pull.py derive`. No infrastructure file invokes it (comp-find
`model_block_pull` over `infra` and `.github`: 0 hits across 7,097 files); every derive recorded in the last four days of CLOUD
history is this seat's. N = 1 rule read: `_compute_cases` at `afff33fe76`.

### BEFORE-STATE (measured 2026-09-26 ~18:4xZ; `evidence/r7_blocks_before_rederive.txt`)
97 block keys; Base case SERVED 51, ABSENT by cause currency_mismatch 14 / outside_band 4 / forward_eps_not_positive 1 /
no_price 1 / no cause 25, and 1 block with no cases (NVDA). Served without a `band` field: 6861_JP, CAT_US, CSL_AU (pre-g-1).
Blocks without `currencies`: those three and NVDA_US.

### EXPECTED OUTCOME -- read from the producer's own rule over the same raw (`evidence/r7_cases_report_all_20260926T184758Z.log`)
`cases-report` under the i-2 rule over all 97, batches of 3: 97 of 97 reported. **Over the 94 keys of the act: no
disposition moves and no served ratio moves** (every SERVED base keeps its value and ratio; every refusal keeps its cause);
every SERVED base (49, all inside the 94, CAT_US among them) carries `band_basis low 0.33
uncalibrated high 3.0 measured`; the 4 outside_band refusals carry it. CAT_US moves from a pre-g-1 block to a guarded one:
SERVED at 0.597, now with `band`, `band_basis` and `currencies`. The three excluded keys would move (6861_JP and CSL_AU SERVED ->
ABSENT, NVDA none -> ABSENT) and are why they are excluded.

Branches: a key whose derive raises lands no new block and its current block keeps serving (the batch stops and is read); a key
whose derived disposition or ratio differs from the report is a row and triggers the rollback for that key.

### ROLLBACK (copy-forward, no delete)
For any key, copy its prior newest block forward under a newer stamp. Every prior block stays in place.

### DISCRIMINATOR after the run
Through the served reader over the 94: dispositions and served ratios equal to the before-state key by key; `band_basis` on
every SERVED base and every outside_band refusal; CAT_US carrying `band` and `currencies`; 6861_JP, CSL_AU, NVDA_US
byte-unchanged (same newest stamp).

## ACT B -- COO HALF: the continuation /2 rewrite, then the dossier rewrite

### THE ACT
1. `python -m lib.research.corpus.continuation --write` (every resolved name, 95), at METHOD_VERSION
   `amgt-corpus-continuation/2`, after i-1's readers are on CLOUD.
2. `python -m lib.research.corpus.dossier --write` (every name), after step 1 and after act A.

### WRITER CENSUS -- one writer each
`research-continuation` is written only by `continuation --write`; `research-dossier` only by `dossier --write`; both only
from this seat's drains (rows `Z-S42` and `Z-S46` recorded the census; `Z-S46` holds the continuation writer until now).

### BEFORE-STATE
Continuation: 95 resolved names, 95 carrying a /1 object that matches current inputs, **0 carrying a /2 object**
(`continuation_pick names 95 current_method_available 0 stale_pick 0`, base run 17:35Z and i-1's worker at its tip). Dossier:
95 partitions, 373 objects, `read_dossier serves the last write 95 of 95` (16:26Z).

### EXPECTED OUTCOME -- read from the producers' own rules
- Continuation: object name = `sha16({method_version, inputs})`; with /2 and no /2 object present, `gold_put` performs a put
  for every name: **95 put_performed, 0 existed**; each new object's pillars carry `terms` and its KPI rows carry `terms`.
  With i-1's readers, both `read_latest` and `substrate` select the /2 object: census `current_method_available 95
  stale_pick 0`.
- Dossier: `write_one` compares fresh inputs with `read_dossier`'s pick; the continuation input (uri + sha) moves on every
  name, and the Model-block input moves on the 94 re-derived keys that have a dossier, so **every name writes one new object**
  on the 2026-09-26 as_of date, and `read_dossier` (h-1's rule) serves it as the last write: census `read_dossier serves the
  last write 95 of 95`, objects 373 -> 468.

Branches: a name whose continuation put raises keeps its /1 served (the reader falls back to the input-matching object); the run
is read, never retried blind. A dossier write on unchanged inputs would print `unchanged ... wrote 0` and is a row.

### ROLLBACK
Continuation: revert `METHOD_VERSION` to /1 in code; the readers then select the /1 objects, which stay in place (no delete).
Dossier: no page reads the table (portal 0 files); a rollback is the dossier rewrite on the reverted code, which lands on the
next as_of date because the prior objects' names already exist today. Both are code-and-rewrite rollbacks, stated as such.

### DISCRIMINATOR after the run
`continuation_pick names 95 current_method_available 95 stale_pick 0`; every served continuation's pillars carry `terms`
(count printed over 95); dossier census `serves the last write 95 of 95` with the object count moved by exactly the number of
dossier puts the run printed.

Signed: `2.0.0_SA_COO~X`, 2026-09-26 ~19:1xZ.
