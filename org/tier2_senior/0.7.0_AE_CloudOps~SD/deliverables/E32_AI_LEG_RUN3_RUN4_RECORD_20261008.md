# MDPF_SECCLASS TO-AI-e32 -- the RUN3 window and the RUN4 transport-14 re-plan

**Seat:** `0.7.0_AE_CloudOps~SD` (dell1) | **Order:** `MDPF_SECCLASS.TO-AI-e32.old-list-v3-ai-leg-laptop`
**Issuer:** `2.0.0_SA_COO~M1` | **Ledger entry:** `secclass-e32-ai-leg-i-20261007` (one entry, never a second)
**Why this file exists:** row `MDPF_SECCLASS-D1-S3` -- `deploy_ledger.py` regenerates the change_management
markdown on its next `close-leg`/`hold`/`close` and silently discards hand-appended prose. The durable
narrative therefore lives here; only the structured facts ride the tool's own `--proof` text.

---

## 1. The planned set reconciles EXACT at 2,291

| term | count | instrument |
|---|---|---|
| planned (signed V3 AI keys) | 2,291 | the halves; dry run `ai_keys` at run 1 |
| landed, run 1 (laptop `~SC`, chunk 1 of 10, then killed on box memory) | 187 | ledger log `20261007T230xxZ` |
| landed, the 1313Z probe (amendment 6 step 1, `--chunk 1`) | 2 | `e32_20261008_1313Z_probe_chunk1.log` |
| landed, RUN3 1326Z (`--workers 4 --chunk 25`) | 1,323 | `RECLASSIFY-WRITE ... ai_written=1323` |
| **landed, total** | **1,512** | 187 + 2 + 1,323 |
| UNRESOLVED lines in the RUN3 log | 779 | `comp-read --enumerate 'UNRESOLVED .*'` -- denominator 866 lines |
| of those, model-stated refusals (no class / no sub-class) | 765 | 779 - 14, by subtraction from the printed denominator |
| of those, transport refusals (`KIMI_TIMEOUT`) | 14 | `comp-read --enumerate 'UNRESOLVED .*KIMI_TIMEOUT.*'` -- 14 of 779 |
| **total** | **2,291** | 1,512 + 765 + 14 |

RUN3's own closing line: `RECLASSIFY-WRITE direct_written=0 ai_to_model=2102 ai_written=1323 ai_refused=0
model_calls=2105 snapshot=...E32_AI_SNAPSHOT_20261008.RUN3_1326Z.json`.

Per amendment 7 item 4 a transport refusal is NOT a final refusal, so the 14 stay absent and are
re-planned. The 765 ARE final and must not be re-sent -- that was the whole point of msg 1014 and the
ruling in amendment 8.

## 2. The 14 transport keys

```
NAME::BEACON PARTNERS FUNDII LP            NAME::CALL ALPHABET INC 295 EXP 01 02 26
CRDBX                                      NAME::CAVA 241018C00120000
CRTBX                                      NAME::COIN 250117C00310000
NAME::APP 240517C00080000                  NAME::ESH5 EWZ4 241231P5450
NAME::ASC 240719P00017500                  NAME::NVDA APR 17 26 200 CALL
NAME::BABA 250620C00150000                 NAME::PIMCO ALL ASSET ALL AUTHORITY I2
NAME::BDPR3C6C                             NAME::PUT NVIDIA CORP 170 EXP 03 20 26
```

Eleven of the fourteen are option contracts or an internal identifier (`BDPR3C6C`) -- the shapes the
model has least to say about. That is an observation, not a prediction: a key that times out again
stays transport (amendment 8 step 4) and is reported, not looped.

## 3. ONE DEVIATION FROM AMENDMENT 8's LITERAL TEXT, with its measurement

Amendment 8 step 1 says to take the rows of `OLD_LIST_RECLASSIFY_SET_20261007.tsv`. **I built the
subset from `OLD_LIST_RECLASSIFY_SET_V3_20261007.tsv` instead**, because the amendment's own binding
sentence is "It is a subset of the signed set, so the signed halves still cover it" -- and the signed
set is V3 (the order's step 1, and amendment 1's ruling, both name V3). The unsuffixed filename reads
as a slip for the V3 one.

The two files are NOT interchangeable for these keys, so this is material and was measured, not assumed:

- both files hold 10,965 rows and all 14 keys; the subset is 16 rows in both (two keys carry 2 rows)
- the 16-row subsets are **not** byte-identical: V3 sha256 `f382f1b22c4b7b33`, non-V3 `8409e9e24f4619e7`
- the delta is confined to `clean_name`, on 3 of the 14 keys, and V3 is the better payload every time:

| key | V3 `clean_name` | non-V3 `clean_name` |
|---|---|---|
| `NAME::BEACON PARTNERS FUNDII LP` | `Beacon Partners Fundii LP` | `Beacon Partners Fundii Lp` |
| `NAME::NVDA APR 17 26 200 CALL` | `NVDA Apr 17'26 $200 Call` | `Nvda Apr 17'26 $200 Call` |
| `NAME::PIMCO ALL ASSET ALL AUTHORITY I2` | `PIMCO All Asset All Authority I2` | `Pimco All Asset All Authority I2` |

V3 preserves the acronyms (`LP`, `NVDA`, `PIMCO`); the unsuffixed file naively title-cases them. The
runner sends name and key only, so `clean_name` IS the model's payload -- taking the unsuffixed file
would have sent a degraded name on 3 of 14 keys. **Issuer `2.0.0_SA_COO~M1` owns this call**; if the
non-V3 bytes were intended, say so and the 3 keys re-run in minutes.

Subset written: `org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/E32_TRANSPORT14_SET_20261008.tsv`
-- 1,516 bytes, sha256 `c0c528dbae4dc595`, header + 16 rows, 14 distinct `shared_key`, byte-for-byte from V3.

## 4. Amendment 8 step 2 -- the dry run, read-only

```
INFO set_rows=16 live_rows=10480 direct_keys=0 ai_keys=14 collapsed_duplicate_keys=2 now_present=0 off_vocab=0 bound=contract 0.8.0 vendor_ceiling=8495
INFO AI-RUN held=14 present=0 direct=0 to_model=14 would_land=0 written=0 model_calls=0 index_address=s3://opal-data-mdpf/mdpf/global/gold/ai_classified_securities/date=2026-10-08/index.json
RECLASSIFY-DRY-RUN direct=0 to_ai=16 unplaced_key=0 present=0 puts=0 model_calls=0
```

`direct_keys=0` and `ai_keys=14` are exactly what step 2 demands, `to_model=14` equals it, `off_vocab=0`,
and the last line carries no `-BAD`. `to_ai=16` is the ROW count, the same key-vs-row distinction
amendment 1 already ruled CONTINUE on. `now_present=0` independently confirms all 14 are still absent
from the table -- the re-plan is not re-writing anything that landed.

## 5. Pre-write conditions, re-measured this window

1. **Seat-gate dry pass** (amendment of ~01:5xZ): `safe-deploy.sh --dry-seat-gates` reported
   `SKIP [seat-gates] no data/<pipeline>/scripts path in the files or commit range; nothing to measure`.
   Recorded as SKIP WITH ITS REASON, never as `verdict=CLEAR` -- this act deploys no gold/silver/bronze
   script, so the CROSSBOX limb has nothing to grade. No verdict=STOP in any mode.
2. **Write targets** are the two this seat has already been measured able to write BY EXECUTION in the
   1326Z window: `dynamodb:PutItem` on `table/etf-classifications` (1,323 conditional puts landed) and
   `s3:PutObject` on the `date=2026-10-08` AI listing (rewritten per chunk, 85 chunks). Execution is a
   stronger measurement than the policy-document read that preceded it; both are APPLIED-plane facts.
3. **Rollback input unchanged**: `~SC`'s preserved run-1 copy,
   `org/tier2_senior/0.7.0_AE_CloudOps~SC/deliverables/E32_AI_SNAPSHOT_20261007.RUN1_PRESERVED_COPY.json`,
   sha256 prefix `5fd655e06f0b4a0e`, 8,968 keys. Never regenerated on dell1 (amendment 4).
4. **Snapshot** is fresh per invocation (amendment 7 item 3):
   `E32_AI_SNAPSHOT_20261008.RUN4_1742Z.json`. An invocation's own snapshot is never the rollback input.
5. **Watchdog** (amendment 6 item 2): the runner is spawned under a wrapper that kills it when no output
   line has arrived for 600 s. On a single-chunk run the chunk line arrives at the end, so the bound is
   measured against ANY progress line, which is stricter than chunk-line-only and cannot read a trickle
   as progress the way `urlopen(timeout=90)` can.
6. **`--workers 2`** per amendment 8 step 3, down from RUN3's 4. RUN3 produced 14 transport failures in
   2,102 sends at 4 workers; 2 is the amendment's own answer to that.

## 6. RUN4 -- what the 14 keys actually did

Launched 2026-10-08T17:45:00Z, exited 17:48:41Z, `rc=0`, `watchdog_killed=False` (3m41s; the 600 s
no-progress bound was never approached).

```
AI chunk 0-25: keys_sent=14 model_calls=14 landed_outside_contract=0 AI-RUN held=14 present=0 direct=0 to_model=14 would_land=7 written=7 model_calls=14 index_address=s3://opal-data-mdpf/mdpf/global/gold/ai_classified_securities/date=2026-10-08/index.json
RECLASSIFY-WRITE direct_written=0 ai_to_model=14 ai_written=7 ai_refused=0 model_calls=14 snapshot=...E32_AI_SNAPSHOT_20261008.RUN4_1742Z.json
```

14 sent, 14 model calls, **7 landed**, `landed_outside_contract=0`. The other 7 split the way amendment 7
item 4 draws the line, and the split is the point of the whole re-plan:

| key | RUN4 outcome | class |
|---|---|---|
| `CRDBX` | landed | -- |
| `NAME::BABA 250620C00150000` | landed | -- |
| `NAME::CALL ALPHABET INC 295 EXP 01 02 26` | landed | -- |
| `NAME::CAVA 241018C00120000` | landed | -- |
| `NAME::COIN 250117C00310000` | landed | -- |
| `NAME::ESH5 EWZ4 241231P5450` | landed | -- |
| `NAME::PUT NVIDIA CORP 170 EXP 03 20 26` | landed | -- |
| `NAME::BEACON PARTNERS FUNDII LP` | `no sub-class for alternatives` | MODEL-STATED, final |
| `CRTBX` | `no sub-class for equity` | MODEL-STATED, final |
| `NAME::APP 240517C00080000` | `no sub-class for structured` | MODEL-STATED, final |
| `NAME::ASC 240719P00017500` | `no sub-class for structured` | MODEL-STATED, final |
| `NAME::NVDA APR 17 26 200 CALL` | `no sub-class for structured` | MODEL-STATED, final |
| `NAME::PIMCO ALL ASSET ALL AUTHORITY I2` | `no class (...no 'multi-asset' category exists among the six allowed values)` | MODEL-STATED, final |
| **`NAME::BDPR3C6C`** | **`no class (refused: KIMI_TIMEOUT)`** | **TRANSPORT, still not final** |

So 13 of the 14 transport failures were transport after all -- the vendor answered every one of them on
the retry. Only `NAME::BDPR3C6C` timed out a second time. Amendment 8 step 4 governs it exactly: a key
that times out again stays transport, is reported, and is NOT looped. It is not looped here.

Worth the issuer's eye: `BDPR3C6C` is the one key in the fourteen that is not a security name at all --
it is an internal identifier. `PIMCO ALL ASSET ALL AUTHORITY I2`'s refusal is the known
no-multi_asset-category shape (the Andrew-direct six-classes rule), not a vendor problem.

## 7. The close arithmetic, MEASURED, not computed by hand

```
python .../R12_CHECKS/ai_leg_verify.py e32 \
  org/tier2_senior/0.7.0_AE_CloudOps~SC/deliverables/E32_AI_SNAPSHOT_20261007.RUN1_PRESERVED_COPY.json \
  --unresolved-log <probe 1313Z> <run3 1326Z> <run4 1742Z>

AI-LEG-VERIFY act=e32 ok=False planned=2291 landed=1519 refused_final=771 refused_transport=1
  unresolved=772 problems=0 first=[] snapshot_keys_gone=0 multi_asset=0
  model_rows=1532 listing_count=1532 listing=mdpf/global/gold/ai_classified_securities/date=2026-10-08/index.json
```

**1,519 + 771 + 1 = 2,291 EXACT.** The logs are passed in chronological order deliberately: the tool
documents "the LAST reason per key wins", so a key like `CRTBX` that was `KIMI_TIMEOUT` in RUN3 and
`no sub-class for equity` in RUN4 must be graded on RUN4's reason. Passing the logs newest-first would
have mis-graded 13 keys as transport.

Every sub-condition of `grade()` passes except one:

| sub-condition | reads | verdict |
|---|---|---|
| `problems == 0` | 0 | PASS |
| `snapshot_keys_gone == 0` | 0 | PASS (nothing deleted; the rollback input is intact) |
| `multi_asset == 0` | 0 | PASS (the Andrew-direct six-classes rule holds) |
| `listing_count == model_rows` | 1532 == 1532 | PASS |
| `landed + refused_final == planned` | 1519 + 771 = 2290 vs 2291 | **FAIL by exactly 1** |

`ok=False` therefore turns on `NAME::BDPR3C6C` ALONE. It is not a partial leg in any other sense: no key
is in an unknown state, no key needs rollback, and `landed>0` was never the test (row S66).

**AC1 as written expects `ok=True`, and amendment 8 step 4 defines the close with a transport term.
Those two cannot both be satisfied while one key times out.** That is the issuer's call, not this
seat's -- stated in the close report, with no gate invented on either side. The two shapes it could
take: accept `transport=1` as the terminal close (which is what amendment 8's own sentence reads like),
or authorise ONE further attempt on that single key. This seat does neither unasked.

## 8. RUN5 -- the last key answers, and the leg closes ok=True

AMENDMENT 9 @`31f7cf0bea` ruled one final 1-key attempt and corrected the set name (section 3's
deviation was ruled CORRECT: "~SD's subset cut from the V3 set is the correct one and stands").

1-key subset: `org/tier2_senior/0.7.0_AE_CloudOps~SD/deliverables/E32_TRANSPORT1_BDPR3C6C_SET_20261008.tsv`
-- 121 bytes, sha256 `d6979299dbb69737`, header + the single V3 row for that key. Written into THIS
seat's deliverables, not the COO's: amendment 9 names no path, and the COO deliverables dir is lane
BASE_EXEC, which refused this seat on the five files of section 9. Dry run read `ai_keys=1 direct_keys=0
now_present=0`, `to_model=1`, no `-BAD`.

RUN5 launched 17:58Z, `--workers 1`, fresh `E32_AI_SNAPSHOT_20261008.RUN5_1758Z.json`, exited
17:59:50Z `rc=0 watchdog_killed=False` -- about 90 seconds.

**IT DID NOT TIME OUT. The vendor answered, and the answer is a MODEL-STATED refusal:**

```
UNRESOLVED NAME::BDPR3C6C: no class (The name 'BDPR3C6C' appears to be an opaque identifier
(resembling a partial CUSIP or internal security code) with no descriptive text indicating security
type, issuer, sector, coupon, or fund strategy. The ticker 'NAME::BDPR3C6C' adds no additional
information. There is no basis to classify this security into any of the six asset classes.)
```

That reading was available in the set file before the call: this key's `clean_name` is the literal
string `BDPR3C6C`. There is no name to classify, which is why it is the one key of the fourteen the
model had nothing to say about. Its two earlier `KIMI_TIMEOUT`s look like the vendor stalling on a
zero-information prompt rather than a network fault -- an observation, not a measured cause.

`is_final_refusal` grades `no class (` NOT followed by `refused:` as FINAL, so the key moves from
`refused_transport` to `refused_final` and the plan closes:

```
AI-LEG-VERIFY act=e32 ok=True planned=2291 landed=1519 refused_final=772 refused_transport=0
  unresolved=772 problems=0 first=[] snapshot_keys_gone=0 multi_asset=0
  model_rows=1532 listing_count=1532 listing=mdpf/global/gold/ai_classified_securities/date=2026-10-08/index.json
```

**1,519 + 772 = 2,291 EXACT, `ok=True`.** This satisfies AC1 as ORIGINALLY written -- amendment 9's
widened expectation (`ok=False` whose only problem is `refused_transport=1`) was NOT needed and is not
invoked. The four logs are passed probe -> RUN3 -> RUN4 -> RUN5 because the tool takes the LAST reason
per key: newest-first would have graded this key on RUN4's timeout and held the leg open.

## 9. What is NOT closed by this window

- **Deployment Rules 4 and 6** for `mdpf-secclass-new-security-lambda` stay surfaced-not-actioned:
  `last_deployed_commit` still reads `none` and no version tag was cut. The tag needs a shared-branch
  push this seat does not make.
- **Surprise rows `D1-S1` .. `D1-S4`** dispositions are the CVO's and the issuer's, not this seat's.
- **TO-AI-e49** opens its own ledger entry and starts only after this order is complete.
