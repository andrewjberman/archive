# AMGT_RESAPP round 77 -- `AMGT-ba-22` ACT RECORD: the officers pull ran; 86 of 86 landed; 84 serve, 2 do not read back

`2.0.0_SA_COO~Z`, 2026-10-07 ~11:5xZ. Pair: COO half @8536310333, CTO half @4f79c10223 (C1, C2, C3).

## C1 -- the vehicle completed and ba-21 was finished

The vehicle read is in `BA21_SEGMENTS_ACT_RECORD_20261007.md` (LastTaskResult 0, every leg landed, the 07:30 ET check over).
ba-21 ended on its branch B at 11:32Z. ba-22 started at 11:33Z.

## C3 -- the name list and the count

`PLAN_officers_20261007.txt` (86 names) committed @bb38ea2d43 at 10:39Z, before any call. M = 86, under the bound of 90.

## C2 -- the five-name slice, ALL five read through the deployed handler before the rest ran

Slice: the first five of the plan. `run officers --names <five> --confirm-calls 5` at 11:33:43Z: `pulled 5 failed 0 calls 5`.
BEFORE (the chain, 11:33Z): all five `served NONE`, Bloomberg leg `not tried`, `needs_new_pull`.
AFTER, through the DEPLOYED `opal-amgt-scoped-api` route `/api/scoped/amgt/security/<key>/thesis`, block `management`:

| name | status | roster_source / status | officers | first two rows as served |
|---|---|---|---|---|
| `1299_HK_Equity` (AIA) | 200 | BLOOMBERG_FALLBACK / UNRESOLVED-SOURCE | 15 | Lee Yuan Siong, President/CEO/Executive Director; Garth Brian Jones, Chief Financial Officer |
| `8035_JP_Equity` (Tokyo Electron) | 200 | same | 11 | Toshiki Kawai, President/CEO/Executive Officer; Hiroshi Ishida, Executive Vice President/COO |
| `8306_JP_Equity` (MUFG) | 200 | same | 20 | Hironori Kamezawa, Chairman/Executive Officer; Yasushi Itagaki "Yaz", Vice Chairman/Executive Officer |
| `8316_JP_Equity` (SMFG) | 200 | same | 26 | Makoto Takashima, Chairman; Toru Nakashima, President/CEO:Group/Rep Exec Officer/Exec Officer |
| `8766_JP_Equity` (Tokio Marine) | 200 | same | 27 | Satoru Komiya, Chairman; Masahiro Koike, President/CEO:Group |

Read by this seat as each company's own officers, names in the name field and titles in the role field, no visible truncation.
Branch (a): the remaining names ran. (The read is this seat's judgment of plausibility on five names; it is not a check of
each list against a filing.)

## The rest

`run officers --confirm-calls 81` at 11:35:44Z. The driver recomputed the plan and it read exactly 81 (the five had left the
population), or it would have refused. `pulled 81 failed 0 calls 81 stopped None`, done 11:37:22Z.

**Calls spent under this pair: 86 of at most 86.** No CAPACITY stop, no failed call.

## Acceptance, read after the run (the committed 86 names, each through `exec_roster_chain.run_chain`)

| branch | names | what the page serves |
|---|---|---|
| A: a Bloomberg officer list is served | **84** | officers from Bloomberg's list, labelled; count min 4, median 14, max 51 |
| B: stored list empty | 0 | -- |
| D: nothing landed | 0 | 86 of 86 names have a stored object |
| **landed but NOT read back** | **2**: `BP/ LN Equity`, `NG/ LN Equity` | still "no Bloomberg officer list is stored for this name" |

`plan officers` re-run after: **names 2 calls 2** (it fell by 84, not by 86).

## The two that do not read back: a key-shape mismatch between the writer and the reader, NOT a Bloomberg failure

- The driver writes through `hbloom.bronze_write`, whose partition is slash-safe:
  `.../exec_officers/security_key=BP-SLASH-_LN_Equity/20261007T113610Z.json` (811 B) and
  `.../security_key=NG-SLASH-_LN_Equity/20261007T113644Z.json` (701 B). Both objects are good: `NAME` BP PLC with 10 officer
  entries; `NAME` NATIONAL GRID PLC with 9; no field errors.
- The reader, `bloomberg_fallback.StoredBloombergInput.newest_key`, lists the prefix `security_key=<bloomberg_fallback.security_key(security)>/`,
  and that function is `security.replace(" ", "_")`: `BP/_LN_Equity`, with the raw slash. It never looks under `BP-SLASH-...`.
  `newest_key("BP/ LN Equity")` returns None; the control `newest_key("AMD US Equity")` returns today's object.
- Of 91 partitions under `exec_officers/`, exactly 2 carry `-SLASH-`: these two. No slash name was ever stored there before,
  so the reader's rule was never exercised on one.
- **Consequence for a re-run:** the plan keeps naming these two as needing a pull. Re-running `run officers` would spend two more
  calls and land two more objects the reader still cannot see. It is NOT re-run (the pair says failed names are not re-run; and
  here the call did not fail).
- **The remedy is a code repair in the reader** (`lib/research/management/bloomberg_fallback.py`, one function, plus the Lambda
  package that carries it), not a store change and not a new pull. Filed as a row; a cell for the next recut or an amendment.

## The served move, counted

84 covered names moved from "no officers, a new pull is needed" to a labelled Bloomberg list, at request time, with no deploy.
The freshness page's Bloomberg stamp moves for the 86 names that have an object (the CTO half's second reader; not read here).
No S3 delete was made. No list was withdrawn.
