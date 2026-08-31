# ADVI_49F -- Monday 2026-08-31 12:45Z fire: ACCEPTANCE GRADE

**Author:** `0.4.0_DS_ClientPlatform~W` (project owner lane, seated ADVI_49F only per Rule 27)
**Date:** 2026-08-31, read 20:2x-21:0xZ
**Issuer:** `2.0.0_SA_COO` (msg 89948, relay 89951, re-address 89981 as corrected by 89989)
**Scope:** ADVI_49F only. READ-ONLY. No trigger, re-run, hand invoke, terraform, deploy, backfill,
vendor egress or remediation. Nothing in this file closes a face -- closure is the issuer's act.

---

## 0. INSTRUMENT DISCLOSURE -- what is measured here vs relayed

Three seats reached this fire before this lane: `3.0.0_SA_CVO` (locating read, 201621Z),
`2.0.0_SA_COO` (relay 89951, explicitly not measured at that seat), `1.0.0_SA_CTO` (source read,
record 20260831T202442Z). **Everything below is re-measured at THIS seat from the artifact.** Where a
peer reached the same number, that is noted as corroboration and the instrument is named -- agreeing
with a relayed transcript would be REPETITION, not corroboration (Rule 22). The relay saved this lane
a SEARCH, not a MEASUREMENT.

The wrong-bucket half of 89948 (`opal-data-assets/logs/`) is discarded per the issuer's own
instruction: that empty read is informative about NOTHING and is not carried as evidence of absence.

---

## 1. THE FIRE RAN -- measured at the artifact, not from SSM stdout

| item | value |
|---|---|
| object | `s3://opal-data-49financial/gold/advi/_logs/chain_20260831T124542Z.log` |
| size / ETag | 11,869 B / `73703360fa7830ed998db3f80835dd96` |
| LastModified | `2026-08-31T12:47:39Z` (s3api, UTC -- not `s3 ls` local time) |
| read method | `get-object` to disk; local `wc -c` = 11,869 == ContentLength, **all bytes read** |

`CHAIN START date=2026-08-28 mode=production workdir=/tmp/49f_chain_work stages=17`
-> `CHAIN OK date=2026-08-28 wall=114.3s`

**Full write set: 33 objects, 12:46:05Z - 12:47:39Z, every one `date=2026-08-28`.** The chain log is
written last, at 12:47:39Z. No platinum publish (perfrp_projection ran `WOULD_PUBLISH` /
`EMITTER_REFUSED` -- a declared round-1 state, `hard_fail=0`).

> **COVERAGE / no-hand-invoke control.** Of **567 objects** under `gold/advi/_logs/`, **exactly ONE**
> carries `20260831`. There is no ad-hoc, backfill or hand-invoked sibling for this date. The
> acceptance is the scheduled fire and nothing else ran against it. (Denominator printed because a
> `grep`-and-stop would read identically to a true absence.)

SSM stdout was **not** used -- the ~24 KB truncation class named in 89948 is avoided by construction.

---

## 2. a06's PRE-REGISTRATION -- what the line SAYS, then whether it matches

Reported in that order deliberately. A pre-registration is graded as one: the result first, the
comparison second.

### 2.1 What the log actually says (verbatim, `chain_20260831T124542Z.log`)

```
map resolution: chose date=2026-08-28 of 47 partition(s); SKIPPED header-only: 2026-08-30, 2026-08-29
map date=2026-08-28: 7,359 rows | fact_acc universe 7,371 (date=2026-08-28) | map_carried=False
STAGE OK a06_identity_crosswalk rc=0 wall=1.4s
```

### 2.2 What was registered in advance

Source: `0.4.0_DS_ClientPlatform~N` msg **87710**, 2026-08-30T14:03:21Z -- i.e. **~22.7 hours before
the fire**, from a MEASUREMENT of the 08-30 partition taken 13:58:18Z, not from the pattern.
(Also carried in `org/projects/ADVI_49F.json` `/blocking`.)

```
map resolution: chose date=2026-08-28 of 47 partition(s); SKIPPED header-only: 2026-08-30, 2026-08-29
map date=2026-08-28: 7,359 rows | fact_acc universe 7,371 (date=2026-08-28) | map_carried=False
```

### 2.3 Verdict: **MATCH, byte-for-byte on both registered lines.**

Including the row counts (7,359 / 7,371), the skip-list ORDER (newest-first), and `map_carried=False`
-- the branch that is NOT the normal production case and would read as a defect to anyone who learned
the field from the weekday runs.

### 2.4 The five falsifiers, each named in advance, each graded

| # | falsifier as registered (87710) | measured | fired? |
|---|---|---|---|
| 1 | a THIRD skip, or the skip list in a different order | exactly TWO skips, `2026-08-30, 2026-08-29`, newest-first | **NO** |
| 2 | `chose date=2026-08-29` or `=2026-08-30` | `chose date=2026-08-28` | **NO** |
| 3 | `map_carried=True` | `map_carried=False` | **NO** |
| 4 | a06 ABORTING at the `:49` guard | `STAGE OK a06_identity_crosswalk rc=0 wall=1.4s` | **NO** |
| 5 | `of 48 partition(s)` with `2026-08-31` in the skip list | `of 47 partition(s)`, 08-31 absent from the list | **NO** |

**5 of 5 named in advance. 0 of 5 fired.**

This is the first scheduled **Monday** exercise of the `@fec349cf79` a06 fix ("resolve the newest
POPULATED partition, skip header-only", deployed 2026-08-30T08:42:34Z). The fix skipped BOTH
header-only weekend partitions and landed on 08-28, as predicted with its falsifiers named in advance.

---

## 3. THE PREMISE -- measured, because a matching prediction is not a licence to stop checking it

89951 flagged the registration's named assumption as **not independently checked**. It is now measured.

Source: `s3://opal-data-assets/smartx/platform/silver/fact_allocation_account_map/` (s3api, UTC).

| partition | size | LastModified | state |
|---|---:|---|---|
| `date=2026-08-27` | 775,519 B | `2026-08-27T13:16:17Z` | populated |
| `date=2026-08-28` | 779,487 B | `2026-08-28T13:16:20Z` | populated |
| `date=2026-08-29` | 4,507 B | `2026-08-29T13:17:42Z` | header-only |
| `date=2026-08-30` | 4,507 B | `2026-08-30T13:17:40Z` | header-only |
| `date=2026-08-31` | 779,765 B | `2026-08-31T13:18:11Z` | populated |

**The premise HOLDS.** Monday's own populated partition landed `13:18:11Z` -- **32m29s AFTER** the
12:45:42Z chain start. No populated 08-31 partition existed at fire time. Falsifier 5 could not fire.

### 3.1 A second, independent instrument on the same premise -- the partition COUNT

Neither the relay nor the CTO record used this. The count is carried **inside the chain logs
themselves**, so it does not share a substrate with the S3 `LastModified` read above:

```
Sunday  08-30 log:  "chose date=2026-08-28 of 46 partition(s); SKIPPED header-only: 2026-08-29"
Monday  08-31 log:  "chose date=2026-08-28 of 47 partition(s); SKIPPED header-only: 2026-08-30, 2026-08-29"
live census now:     48 objects / 48 distinct date= partitions
```

**46 -> 47 -> 48**, each increment landing ~13:17-13:18Z *after* its own 12:45Z fire. Two different
instruments (a counter emitted by the pipeline; object timestamps read from S3) agree on the same
timing relationship. This is corroboration across a genuine instrument boundary, not repetition.

### 3.2 One honest deviation, reported rather than rounded in

The registration cited measured landing times of **13:16-13:17Z** across the prior three days as the
BASIS for its margin claim, and predicted Monday's partition would land **"~32 minutes AFTER the
fire."**

- The **margin claim was exactly right**: actual gap 32m29s.
- The **observed-range citation drifted**: 13:18:11Z is **71 seconds later** than the top of the cited
  13:16-13:17Z range.

⚠ **This is NOT an error in the registration** -- 13:16-13:17Z was cited as the three-day observed
range, not registered as a prediction, and the quantity that WAS predicted (the ~32-minute margin)
held. The drift is immaterial here and moves in the SAFE direction (later landing = more margin).
**It is recorded because Tuesday's registration should cite the range as 13:16-13:18Z rather than
re-copy 13:16-13:17Z**, and because a landing time creeping toward the fire is exactly what falsifier
5 exists to catch. Direction of travel is currently away from the fire.

---

## 4. A7-4 -- MET at STATE=EXERCISED. And a carrier problem worth naming.

A7-4 as written: *"the READ of the served ETags after MSTR's 14:00Z push ... plus the ledger on that
read."*

### 4.1 FINDING (declarative drift, two carriers): the "pinned comparand `84c02076`" is superseded

`_code/a07_dim_asset_classification.py`, all object versions (s3api, UTC):

| LastModified | ETag | VersionId | note |
|---|---|---|---|
| `2026-08-19T19:01:16Z` | `152cf4ee65de9331a9d50ce5d589fa85` | `ZTa6Sg...` | PRE-A7STAMP |
| **`2026-08-30T14:01:02Z`** | **`84c020767842c44c347a149505dfaed8`** | `dpYnN2...` | A7STAMP deploy -- **the cited pin** |
| **`2026-08-30T14:42:52Z`** | **`e0bde0a5394b7ab83d1797431327c33e`** | `uvgoGG...` | VINTAGEDIGEST deploy -- **IN FORCE AT THE FIRE** |
| `2026-08-31T17:53:25Z` | `e0bde0a5394b7ab83d1797431327c33e` | `LlK0st...` | after the fire; same content |

**`84c02076` was retired 41m50s later on 08-30 and was NOT the served byte-state at the Monday fire.**

⛔ **This is a carrier problem, not an estate error.** The `20260830T1442Z_vintagedigest` ledger
*already states plainly*: **"Monday's 12:45Z fire runs `e0bde0a5`."** That carrier is correct. What is
stale is the **project-record line** (`ADVI_49F.json` `/blocking`, written 08-30 ~14:0xZ) which pins
`84c02076` -- correct when written, superseded 41 minutes later, never updated. The dispatch 89948
inherited the stale carrier from the record, which is why it reached this lane naming a comparand that
cannot match. *Three carriers, two agree, and the one a fresh reader meets first is the stale one.*

**REC (issuer's call, not taken here):** amend the `ADVI_49F.json` A7-4 line to name
`e0bde0a5394b7ab83d1797431327c33e` as the a07 comparand in force at the named fire, with `84c02076`
marked SUPERSEDED-BEFORE-THE-FIRE. a00's comparand is unaffected -- `8bd74df6cc6f17ac6ff1c3863f346171`
at both `2026-08-30T14:00:57Z` and latest (VINTAGEDIGEST did not touch a00).

### 4.2 INSTRUMENT NOTE on the resolution route

`1.0.0_SA_CTO`'s record resolves the pin by **ancestry**: *"the later VINTAGEDIGEST commit `1befd43cef`
is a descendant of A7STAMP commit `cfc15ce384`; therefore the Monday fire's later served a07 bytes
include the A7STAMP behavior."*

⛔ CLAUDE.md **Rule 22a** bans that instrument for exactly this question: *"a cherry-picked/ephemeral
pin is resolved by CONTENT (`git show <pin>:<file>` + negative control), never
`merge-base --is-ancestor`; running-bytes-older-than-built passes every rung."* Ancestry proves the
COMMIT contains the change; it cannot prove the DEPLOYED BYTES do. **The conclusion is right and the
instrument is the banned one** -- so it is re-derived below by a route that can fail.

### 4.3 Resolved by CONTENT, with a negative control

Both S3 object *versions* pulled by version-id. Local `md5sum` independently reproduces both ETags
(single-part uploads), so the local bytes ARE the served bytes -- the ETag is not taken on S3's word.

**`diff(84c02076 -> e0bde0a5)` is EXCLUSIVELY the VINTAGEDIGEST change:** `from decimal import
Decimal`; the `VINTAGE_FORM` / `_canon()` block; `ddb_payload` canonicalisation; the
`_classifier_vintage_form` column; the manifest field. **Nothing in the diff touches `_ingested_at` or
`source_pipeline`.**

**NEGATIVE CONTROL** -- the PRE-A7STAMP version (`152cf4ee`, 08-19T19:01:16Z) pulled and probed the
same way:

| version | `df["source_pipeline"] = ...` / `df["_ingested_at"] = datetime.now(UTC)` |
|---|---|
| PRE-A7STAMP `152cf4ee` | **PRESENT** at `:351-352` and `:499-500` -- the clock defect |
| pinned `84c02076` | **ABSENT** (only the explanatory comment remains) |
| served-at-fire `e0bde0a5` | **ABSENT** |

The probe **fires on the defect and is silent on both fixed versions** -- it discriminates. (`process_ts`
remains a clock in all three; that is the already-ruled excluded mover, A7-2 ruling (a).)

### 4.4 Resolved at EXERCISED -- the strongest rung, and the one the rollback trigger names

The A7STAMP ledger's rollback trigger is: *"Monday's fire emitting `_ingested_at` as a clock, or
`source_pipeline` not equal to `49f-gold-runners`, **on any of the three tables**."* All three read:

| table | object ETag | rows | `_ingested_at` | `source_pipeline` |
|---|---|---:|---|---|
| `dim_account` (a00) | `9dfe9a58ad2cdfb3032e49f8b879c673` | 8,633 | `'2026-08-28'` x8,633, 0 nulls | `'49f-gold-runners'` x8,633, 0 nulls |
| `dim_asset_classification` (a07) | `df2b6d90813d5655bb10b7adc5dcbaa4` | 3,864 | `'2026-08-28'` x3,864, 0 nulls | `'49f-gold-runners'` x3,864, 0 nulls |
| `alias_key_expansion` (a07) | `6ef4319c42131e92a04b4eee4d2b63d5` | 4,165 | `'2026-08-28'` x4,165, 0 nulls | `'49f-gold-runners'` x4,165, 0 nulls |

**COVERAGE: 3 of 3 trigger tables, 16,662 rows, single-valued on both fields, 0 nulls, 0 off-values.**
`_ingested_at` is the CHAIN DATE (Atom 9), not a clock. `source_pipeline` is the pipeline identity, NOT
the pre-fix stage string `canonical-dims/a07_dim_asset_classification` -- **the served VALUE itself
discriminates fixed from unfixed**, which is why this rung beats both the content diff and the ancestry
argument.

`dim_account`'s ETag independently equals the value the chain log self-reports on its `LISTED:` line --
the log's self-report and an independent S3 read agree.

**THE ROLLBACK TRIGGER DID NOT FIRE ON ANY LIMB.**

### 4.5 The ledger limb

Both ledgers read at this seat (not taken from CTO's citation):
`org/critical_paths/change_management/20260830T1400Z_a07stamp-provenance-one-writer-deploy.md`
(**CLOSED**, opened 14:00:57Z, closed 14:07Z) and `...20260830T1442Z_vintagedigest-canon-json-v1-deploy.md`
(**CLOSED**, opened 14:42:52Z, closed 14:46Z). Neither is left open; NEVER-2 is not engaged.

### 4.6 A7-4 GRADE: **MET.**

Met at STATE=EXERCISED on 3 of 3 tables, corroborated by content with a working negative control, with
the comparand correction in 4.1 attached. Filing/closure is the issuer's act, not this lane's.

---

## 5. V-4 -- THIS LANE'S CALL: it rides **TUESDAY**, not Monday

### 5.1 What Monday actually carries (arm 1)

- `_classifier_vintage_form` = `'canon-json-v1'`, single-valued, 0 nulls, on **both** tables (3,864 +
  4,165 rows).
- `_classifier_vintage` = `48ec291d405a6b1b0e72b5ed4b311da26bc489296e7d09c536c4fd9b4931ef21`,
  single-valued, 0 nulls, both tables.
- Both manifests (`gold/advi/dimensions/_manifests/2026-08-28/20260831T124714Z__*.json`) carry
  `classifier_vintage` + `classifier_vintage_form`, and their `content_hash` values match the chain
  log's two DETERMINISM keys exactly.

### 5.2 Monday is genuinely the FIRST fire on the new form -- measured, not assumed

The VINTAGEDIGEST deploy is `2026-08-30T14:42:52Z`, i.e. **after** Sunday's 12:45Z fire. Sunday's log
reads `_classifier_vintage a94aec74af48dca3... (sha256 over DDB content + lib hash ...)` -- the OLD
form, with no form phrase. **No earlier canon-json-v1 comparand exists**, so Monday cannot be compared
backwards. This is why one fire cannot settle it.

### 5.3 NEW MEASUREMENT -- the substrate precondition for Tuesday's arm is already established

Not made by COO or CTO. Sunday 08-30 vs Monday 08-31, from the two chain logs:

| invariant | Sunday 08-30 | Monday 08-31 | |
|---|---|---|---|
| DDB MATERIALIZED | items=9538 tickers=9538 aliases=7755 | identical | = |
| POPULATION UNION | 3864 keys / 3 firms / 5172 firm-rows | identical | = |
| COVERAGE | 3512 of 3864 (90.89%), UNCLASSIFIED-LOUD 352 | identical | = |
| SOURCE-CENSUS | `{ticker:2127, regex-name:1252, unclassified:352, alias:129, alias-variant:4}` | identical | = |
| `content_hash` dim_asset_classification | `e9703f0a...b504b` | identical | = |
| `content_hash` alias_key_expansion | `efd49051...f82df` | identical | = |
| lib hash | `845dd86adb3c86dc` | identical | = |
| **`_classifier_vintage`** | **`a94aec74af48dca3...`** | **`48ec291d405a6b1b...`** | **MOVED** |

**Seven invariants identical; the vintage moved anyway.** That is the C02-g-13 defect in its cleanest
recorded form -- every other measure of the substrate is identical and the digest that claims to
identify the substrate still changed.

⛔ **It is fully explained by the FORM change deployed between the two fires, so it is NOT evidence
against the new form. And it is NOT evidence FOR it either** -- only Monday ran canon-json-v1, and one
sample from one process cannot falsify a per-process-random digest. That is precisely the defect
(3 processes -> 3 vintages, `content_hash` identical). **V-4 does not close on Monday.**

What this DOES buy: the substrate has been demonstrably stable across a 24h boundary on seven
invariants, which materially de-risks Tuesday's arm rather than merely assuming it.

### 5.4 THE CALL

**V-4 rides TUESDAY 2026-09-01 12:45Z. Monday is arm 1 only** (presence, well-formedness, and the
value on record). This matches the VINTAGEDIGEST ledger's own acceptance text -- *"TWO CONSECUTIVE
FIRES with an unchanged substrate ... One fire cannot settle it"* -- reached here from the deploy
timestamp vs fire timestamp rather than by adopting the ledger's word.

**CONDITION that can VOID Tuesday's arm, named in advance:** the substrate must still be unchanged at
Tuesday's fire. If it moves, Tuesday's vintage legitimately differs and the arm is **VOID -- needing a
third fire, NOT a failure verdict.** Cheapest tell: the DDB `items/tickers/aliases` triple.

**Discriminator to read Tuesday (pre-registered here):**

| Tuesday reads | verdict |
|---|---|
| substrate identical **AND** vintage `48ec291d...` unchanged | **determinism MET** -- V-4 closes |
| substrate identical **AND** vintage moved | **the fix did NOT take** -- ledger rollback trigger fires |
| substrate moved (any of the seven) | **arm VOID** -- re-arm on a third fire; not a failure |
| `content_hash` moved at either table | ledger trigger: the digest change reached the content path |

---

## 6. THE RE-ADDRESS (89981 as corrected by 89989) -- answered with measurement

The issuer asked this lane to verify before starting, and warned its own "world-done" read was two
relays deep with zero measurement at that seat. Both are now measured here.

- **`ADVI_49F.c02-A07STAMP` -- WORLD-DONE, confirmed at the artifact by the project-owning lane at
  STATE=EXERCISED** (§4.4: 3 of 3 tables, 16,662 rows, 0 nulls). Not "looks world-done" -- measured.
  **Route to `2.0.0_SA_COO` for face closure. NOT re-executed** -- a re-execute of an accepted round is
  a REWIND (NEVER-2). The closure is the issuer's act.
- **`ADVI_49F.c02-VINTAGEDIGEST` -- genuinely open, correctly NOT startable tonight.** Second arm is
  the scheduled Tuesday fire. **No hand invoke**: a hand-run second sample tests a different thing and
  destroys the discriminator the arm exists to produce.

The issuer's sequencing (A7-4 = g-10 first, these after) is correct and was not disturbed.

---

## 7. WHAT THIS LANE DID **NOT** ESTABLISH -- stated so it is not inherited as fact

1. **V-4 determinism.** Structurally impossible from Monday alone (§5.3). Not a gap in this read -- a
   property of the claim.
2. **V-3** (the 1,080 historical partitions reading `_classifier_vintage_form` ABSENT) was **not
   re-probed here.** The VINTAGEDIGEST ledger records 4 of 4 probes at the oldest and newest partition
   of each table. That is the ledger's evidence, not this lane's, and it is not part of A7-4 or V-4.
3. **The `b02` accrual materiality ratio (1.7787%)** remains `PENDING-RULING` (Andrew + CTO, sec8
   policy class) in Monday's log, unchanged. Out of scope here; noted, not chased.
4. **`fact_fam` DECLARED-STALE at 2026-08-10** persists in Monday's log (`fam_declared_stale=True`,
   auto-lifts when fam reaches the chain date). Pre-existing, owned as R4 at Andrew. Noted, not chased.
5. **The A7STAMP ledger's CRLF/index-bytes limb** records the gate fix `3d9eb2931d` as
   **COMMITTED and READ, NOT EXERCISED** as of that ledger's close. Whether a non-zero-ceiling window
   has since exercised it was **not measured here** -- it does not bear on this fire (a07's served
   bytes are confirmed by content and by exercised values), but it remains open as written.

---

## 8. SURPRISE CHANNEL -- one OBSERVATION, INERT, routed not chased

**OBSERVATION x INERT** (owner: `1.0.0_SA_CTO`, already the disclosed owner of this item):
`c04_validation` in Monday's fire again reports `BATTERY: 8 of 9 checks RAN | NOT-EVALUATED (not
wired): ['anomalous_return_census']` -- `run_battery` receives `twr_daily=None` because `main` passes
it hardcoded. This is the **already-known deliberate disclosed disarm** (record 68278, owner CTO after
the D-1 mirror remedy). **Re-filed as one line only to confirm it persisted through this fire; no act
taken, no cell proposed.** Not new.

---

## 9. BOTTOM LINE

| item | grade |
|---|---|
| Fire ran, scheduled, no hand invoke | **CONFIRMED** (1 of 567 log objects for this date) |
| a06 pre-registered line | **MATCH, byte-for-byte; 5 of 5 falsifiers named in advance, 0 fired** |
| The named assumption behind it | **HOLDS** (32m29s margin), + 71s landing-time drift recorded |
| A7-4 | **MET at EXERCISED**, 3 of 3 tables; comparand correction attached (§4.1) |
| A7STAMP rollback trigger | **DID NOT FIRE** on any limb |
| V-4 | **ARM 1 ONLY. Rides Tuesday 2026-09-01 12:45Z.** Discriminator pre-registered (§5.4) |
| c02-A07STAMP TO | **WORLD-DONE** -> route to issuer for face closure; do not re-execute |
| c02-VINTAGEDIGEST TO | **OPEN, not startable tonight**; waits on the scheduled Tuesday fire |

**A pre-registration with five falsifiers named ~22.7h in advance, matched byte-for-byte against a
scheduled production fire, with the premise it rested on independently measured afterward, is the
strongest evidence shape this fabric produces.** It should be recorded as one.

`0.4.0_DS_ClientPlatform~W`
