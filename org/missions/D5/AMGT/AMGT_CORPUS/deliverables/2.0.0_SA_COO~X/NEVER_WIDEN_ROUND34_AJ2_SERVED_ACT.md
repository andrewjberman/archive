# AMGT_CORPUS round 34 -- never-widen pair for `CRPS-aj-2`: re-pin `amgt-induction-daily` to the round-34 producer and fire its own trigger once on demand

**Authority:**
- Andrew-direct 2026-10-03 ~20:3xZ, verbatim "yes to all recommendations". Card 3: "a daily Bloomberg re-pull with earnings
  dates, the V3 fields and a long-name field -- yes, one daily pull for all of it ... this record is the per-use vendor word"
  (`org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261003_20xxZ_YES_TO_ALL_SEVEN_OPEN_CALL_RECS.md` @`9fe6e6f111`).
- PRD v0.7 `C-NO-VENDOR-CALL` B.2: on that word, the Model-block pull may recur on a schedule from a scripted producer on the
  terminal box.
- Decomposition v34.0 @`bcd3b35abc`, cell CRPS-aj-2.

**Code (the new pin):** CLOUD `a864e82a5c`, the drain of CRPS-aj-1. It carries:
- the `refresh` stage and the 52 appended mnemonics;
- the scheduled refresh step after admit;
- issuer amendment `22eb07e64c`: refresh derives with `sa_fallback=False`.

The old pin is `33c1d096a343`, an ancestor of the new one.

## THE ACT, IN ORDER (one NEVER-2 entry, slug `amgt-corpus-r34-aj2`)

0. **Gate.** CTO half signed at this pin. In a PowerShell session with
   `C:\Users\Opal Bloomberg\AppData\Local\Programs\Python\Python311` PREPENDED to `PATH`,
   `schedule_induction.ps1 -Plan -Commit a864e82a5c` must print the Python311 interpreter. **If it prints any other python, STOP.**
   Measured 22:2xZ: without the prepend the plan resolves `C:\Program Files\Python314\python.exe`, which has no blpapi
   (row `AMGT_CORPUS-Z-S85`); with the prepend it prints Python311, the live task's own interpreter.
1. **(r) Re-pin.** Same session: `schedule_induction.ps1 -Register -Commit a864e82a5c`, then `-Status`.
   - Expected: a pinned checkout at `...\opal-pinned\amgt-induction-daily\a864e82a5c4b`.
   - Expected: the action reads `set OPAL_INDUCTION_FIRE=1&& "<Python311>\python.exe" -m lib.research.corpus.induction_scheduled
     --mode fire`, and the trigger reads daily 13:00Z.
2. **(f) Fire on demand:** `schtasks /run /tn amgt-induction-daily` (the task's own trigger, its own clock: as-of = today UTC).
   Read the run's log `C:\Users\Opal Bloomberg\AppData\Local\opal\amgt-induction-daily\<as_of>.log` to the closing line.
3. **(v) Verify** (section "after-state").

**Deferred, not in this act:** the unit-map leg in decomposition s.1. `build_unit_map.py` has no family for any of the 52
(row `AMGT_CORPUS-Z-W1-S29`), so a rebuild now writes only UNRESOLVED entries. The families are measured on the values this
fire lands, and that is round 35's first item.

## EXPECTED OUTCOME, READ FROM THE PRODUCER'S RULE (every branch)

**Writers of the served property.** The served property is the NEWEST `derived/model_block/<key>/<stamp>/model_block.json` per
name: `scoped_amgt._read_model_block_pool` lists the key's subtree and serves the lexicographically last object, at request
time.
- It has ONE writer function, `model_block_pull.stage_derive`, reached by three callers: `cmd_derive`, `cmd_admit` and
  `cmd_refresh`.
- N = 1 rule read: stage_derive's write-once fresh-stamp landing.

**Branch A: DAPI reachable.** Each step is read at the base dry runs (22:0xZ):
- `induction_run` fire: population 1 (Brookfield `BN CA`, NO_EVIDENCE), so 0 Bloomberg calls.
- `admit`: registered 96, without_block 0, so 0 pulls.
- `refresh`: registered 96, with_block 96, already_current 0 (no latest block is stamped 2026-10-03), so 96 pulls.
  - Each pull is 1 ReferenceDataRequest, ceil(83/25) = 4 HistoricalDataRequests and 3 BEST override requests: about 768
    Bloomberg calls in all.
- Per name, the writes are: 3 bronze objects (`refdata`, `histdata`, `bestdata`) at a new stamp, 1 state pull_log, 1
  input-ledger run record, and 1 new derived model_block.json.
- `field_map.json`: 0 writes. `_ensure_unit_map` returns at once for a security already in the map, and all 96 are.
- Seeking Alpha: 0 calls (`sa_fallback=False` on refresh).
- **Served:** each of the 96 names' newest block moves to the run's stamp.
  - The 66 base fields carry the fresh pull's values with their map units.
  - The 52 new mnemonics are either figures carrying the pointer unit "SEE field_map.json ... not yet built" (read as NOT
    measured), or `unresolved` with Bloomberg's own `__field_errors__` text.
  - `ERN_ANN_DT_AND_PER` is a LIST-valued figure. The served readers type-check before arithmetic
    (`scoped_amgt.py:1143`, `case_rule.py:100/215`), so a list is never coerced.

**Branch B: DAPI unreachable** (terminal signed out). refresh prints its REFUSED line and returns 4, with 0 S3 writes by
refresh. Admit makes 0 pulls. The closing rc is 4. Served is UNCHANGED. The re-pin stands, so the next 13:00Z fire retries on its
own clock.

**Branch C: partial.** One name failing never hides the others: rc 1, and a failed name keeps its prior block.

## AFTER-STATE THE VERIFY READS (leg v)

1. The run log's last refresh line: `refresh population registered 96 with_block 96 already_current 0 pulled <p>
   bloomberg_calls <c>`. Expected p = 96 on branch A.
2. A served census, read-only: for every one of the 96 registered names, the newest block's stamp day equals the run's UTC
   date. The denominator is printed, and any name not at that date is listed with its log line.
3. A field-error census of the 52 over the 96 new blocks, per mnemonic: figures, unresolved, and Bloomberg's error text. This
   is the first read of each field's servability and request type.
4. The served route for 3 names (BA, GOOGL, BP/ LN) returns its model block with the run's stamp. BA's Model tab is looked at
   on the running page (screenshot kept under `deliverables/2.0.0_SA_COO~X/round34/`).

## BLAST RADIUS AND ROLLBACK (per key)

| what | may touch | rollback |
|---|---|---|
| the Scheduled Task `amgt-induction-daily` | its action (Start In = the new pinned checkout; the interpreter unchanged), trigger unchanged | `-Register -Commit 33c1d096a343` in a Python311-first session restores the prior action exactly |
| `opal-data-harvest` bronze `refdata/histdata/bestdata` + state pull_log, per name | up to 96 x 4 NEW write-once keys | none needed: a raw landing is never served |
| `derived/model_block/<key>/<stamp>/model_block.json` | up to 96 NEW write-once keys, each becomes the served newest | forward rollback in this seat's control: `stage_derive(s3, security, raw_stamp=<the prior raw stamp>, sa_fallback=False)` mints a newer block from the prior pull's bytes. Exact restoration (deleting the new object so the prior is newest) is an S3 delete and needs Andrew's word |
| the input ledger | one OK run record per pulled name | append-only; nothing to roll back |

Never touched: `field_map.json`, any portal file, any other firm's prefix, any Seeking Alpha surface.

## STOP LIMBS

- The plan prints any interpreter other than Python311: STOP before `-Register`.
- The fire's log shows REFUSED (branch B): STOP. Card the Bloomberg sign-in to Andrew (his login). The re-pin stands.
- Leg v.4 finds a served route error or a broken Model tab that a pre-fire read did not show: forward-roll-back every moved name
  in the same session, re-pin to `33c1d096a343`, and escalate loud.

**COO HALF: SIGNED** by `2.0.0_SA_COO~X`, 2026-10-03 ~22:3xZ, for legs 0, r, f and v at pin `a864e82a5c`, covering branches A,
B and C. It is signed on the blast radius above, not on the producer's decision.

**CTO HALF:** owed by `1.0.0_SA_CTO~Z`.
