# ADVI_49F — THU 2026-08-20 12:45Z FIRST UNATTENDED GREEN: the read protocol

**Author:** `0.4.0_DS_ClientPlatform~A` (runner-chain lane) · written 2026-08-19 ~23:35Z
**Status:** PREPARATION. Touches nothing, schedules nothing, runs nothing.
**Why it exists:** this chain reported `CHAIN OK` **for weeks while writing none of its own tables**
(P2D-3, caught 2026-08-19). **A green nobody can falsify is the failure mode that already bit this
product once.** So this protocol is organised around *what would falsify a green*, not around confirming one.

---

## 0. ⚠ READ THIS FIRST — THE FIRST GREEN EXECUTES NEWLY-DEPLOYED CODE

Two stage scripts were deployed **tonight**, after the floor was pinned, and the 12:45Z run is the first
thing that will execute them:

| stage | file | deployed | change |
|---|---|---|---|
| c00 | `c00_flow_ledger.py` | 2026-08-19 ~21:50Z | `in_kind_unvalued` defaults TRUE for IC rows; `quantity` added to `out_cols`; `SCHEMA_VERSION` 1.0 → **1.1**; manifest gains `in_kind_census` |
| a01 | `a01_dim_relationship.py` | 2026-08-19 ~22:2xZ | per-row `identity_source` + `source_as_of`; manifest gains `custodial_tail` + `identity_source_axis` |

Both were ordered (c00-FIX C00-3/C00-5; IDSPINE WP-4) and both are byte-verified on the deployed artifact.
**Stated here plainly so it is not discovered tomorrow.** Pre-green risk was exercised locally on real
2026-08-18 inputs, not reasoned about:

| downstream | result |
|---|---|
| c01 / `nna_canonical` | **CHANGES BY DESIGN** — `row_quality=in_kind_unvalued` 0 → 4 accounts, `in_kind_unvalued_count` 0 → 27, on identical 5,351 rows |
| c02 / `twr_daily` | **BIT-IDENTICAL**, `cf_net` 1,779,110.820000 both sides |
| c04 battery | **GRADES IDENTICAL** across all 9 checks |
| schema pin risk | no consumer pins `flow_ledger.schema_version` (c02's `!= "1.0"` guard is on `POLICY_BLOCK.json`, a different file) |
| determinism | two same-input runs, frame-hash identical → STABLE |
| tests | `runners_49f` suite 101 passed |

### ⚖ RULED 2026-08-19 23:40Z (COO): **ACCEPT — the 12:45Z green runs these bytes. DO NOT REVERT.**

Reasoning on the record, because it is the useful half: both deploys were **ordered** and byte-verified; the
risk was **exercised** on real inputs rather than argued (c02 bit-identical to six decimals, c04 grades
identical across all 9 checks, run not inferred); the changes are **honest-labelling** — additive fields, not
computation-path changes; **and reverting is itself an unverified act at midnight** — pulling ordered,
verified fixes hours before a first green, with no exercise of the reverted state, trades a *measured* low
risk for an *unmeasured* one.

**The mechanism COO named, worth keeping:** *two rulings, each correct alone, produced an unstated
consequence when composed.* The fence said don't touch the run; the TOs ordered the deploys. **Both remain
right — the composition was unexamined.**

### ⚠ THE RUN'S MEANING CHANGED — ADDED DUTY ON THE PROOF READ (COO, operative)

It was "the floor proves itself." It is **also** now "these bytes execute unattended for the first time."

1. **Explicitly verify the new fields landed as designed** on the real partition — `in_kind_unvalued` honest
   on IC rows, `quantity` present, `identity_source` / `source_as_of` populated.
2. **If anything is anomalous, ATTRIBUTE TO THE NEW BYTES FIRST** — not because they are the likely cause
   (the evidence says they are not) but because **they are the CHANGED variable, and the cheapest hypothesis
   to test is the one that moved.**
3. **Report the attribution explicitly either way**, including the boring outcome — *"new fields correct,
   anomaly unrelated."* **A silent pass would leave the composition unexamined a second time.**

**The fence stands otherwise: nothing else touches that run.**

### ⚖ RULED 2026-08-19 23:41Z (CTO): **LET IT RUN — the fence and the deploys COMPOSE. No revert pre-positioning.**

Stated strongly so nobody re-litigates it at 12:40Z: the hard fence was ruled against **rescheduling or
interfering with** the run — and **the c00 fix was ordered precisely so the first green would execute the
corrected producer.** *A fence reading that excluded the ordered deploys would have the run proving the
defect we just repaired.* C00-5 required the deploy; the fence protects the run; they compose.

**CTO will read F3 FIRST when validating the first green** — it is the one check that distinguishes
*"the fix RAN"* from *"the fix was DEPLOYED"*, **and the whole point of tonight was the first, not the
second.** F3 is Rule 22a's EC2 clause turned into a falsifier the run carries for free.

---

## 1. WHAT SHOULD HAPPEN

```
12:45Z  advi-49f-gold-floor (cron(45 12 * * ? *), ENABLED)
          -> advi-49f-gold-dispatch (Lambda, 256MB/900s, thin ensure-running dispatcher)
          -> SSM doc advi-49f-chain-dispatch  -> chain_49f_entrypoint.py
             a00..a07 -> b00..b03 -> c00..c02 -> c04
```
Measured E2E basis for the pin: **107.1s** (a02 dominant at 66.6s — the fact_trn 532-partition sweep),
against a 300s dispatcher poll budget and a 3600s document timeout. **Ample margin; no tuning expected.**

---

## 2. THE FALSIFIERS — read these FIRST, before any success signal

**A green that survives all six is a real green. Any one of them failing means the green is not what it looks like.**

| # | falsifier | how to read it | why it exists |
|---|---|---|---|
| **F1** | **`CHAIN OK` with unwritten tables** | For `date=2026-08-19`, read the THREE product tables **by direct S3 read**, not the run log: `canonical/flow_ledger`, `canonical/nna_canonical`, `canonical/twr_daily`. **Absence of any one falsifies the green outright.** | The exact P2D-3 defect. `rc=0` and `CHAIN OK` were both true while these three were never written. |
| **F2** | **Stale artifacts wearing a fresh run's clothes** | Check S3 **`LastModified`**, never `_ingested_at` — that column is stamped from `asof` (`runner_common.stamp_provenance`, "deterministic, never a clock") and reads `2026-08-19` on an object written any time. | A partition rewritten by an older run is indistinguishable from a fresh one on the `_ingested_at` column alone. |
| **F3** | **The new c00 bytes did not actually execute** | The manifest for `flow_ledger` must carry `schema_version: "1.1"` **and** the new `in_kind_census` block; the parquet must carry a `quantity` column. If it reads `1.0` / no `quantity`, **the run executed stale bytes** regardless of what the deploy verified. | Rule 22a: an artifact proves what is *there*, never what *runs*. This is the discriminator that proves execution. |
| **F4** | **Zero-buried rows reappear** | `in_kind_census.zero_buried` must be **0**. A non-zero value means the honest default was regressed or bypassed. | It is the defect signature, now unreachable by construction — so a non-zero is a real regression, not noise. |
| **F5** | **twr moved** | `twr_daily` for the run must be consistent with the pre-change behaviour. **A material move in `cf_net` composition is a RED flag**, because c00-FIX was proven not to touch c02. | COO/CTO's negative control: if twr moves, something widened. Same instrument, two readings. |
| **F6** | **A silent stage skip** | Count the stages that reported. The entrypoint fails LOUD per stage (`CHAIN ABORT` on any `rc!=0`) — but confirm the *stage count*, and confirm `c04` ran. | "Nothing failed" and "everything ran" are different claims; only the second is the one wanted. |

**Print the denominator on every count read.** A count without its frame is the class this estate keeps catching.

> ⚠ **F2 RENDERING TRAP, measured 2026-08-20T00:17Z — `LastModified` ITSELF HAS TWO FRAMES.**
> **`aws s3 ls` renders LOCAL time; `boto3` / `aws s3api` render UTC.** Same object, same instant, both tools:
> ```
> aws s3 ls  ->  2026-08-19 18:09:18            (EDT)
> boto3      ->  2026-08-19 22:09:18+00:00      (UTC)
> ```
> **Four hours apart, and neither output says which frame it is in.** Mixing them in one read makes an
> artifact look stale — or fresh — by exactly the offset, silently. **Tomorrow: use `s3api` / `boto3` and
> compare UTC to UTC**, or state the frame beside the timestamp. *(Caught only because two of my own readings
> of the same object disagreed by ~19 minutes and no timezone story explained it, so I put both tools on one
> object and let them settle it. F2 sends the reader straight at this column, so the warning belongs here.)*

---

## 3. EXPECTED-AND-FINE (do NOT raise these)

- **`fam_declared_stale: true` with `fam_as_of=2026-08-10`** on `dim_relationship`. `fact_fam`'s latest
  partition is 08-10; the SS6 carry is ruled and auto-lifts when Schwab resumes. **Not a finding.**
  *(Note the WP-4 TO and SPEC_IDENTITY_SPINE both say "as-of 2026-08-07" — that prose is stale; the code
  derives the vintage and 08-10 is correct.)*
- **`identity_source: {fam-carried: ~7202, self-family: ~119}`** and a `custodial_tail` count around 2,006 —
  new WP-4 fields, first appearance.
- **c01 `row_quality=in_kind_unvalued` on a handful of accounts** — the honest flag reaching its consumer.
  **This is the fix working, not a regression.**
- **`advi-49f-publisher` DISABLED** — activation is DS~B's Thursday contract (doc mint + allowlist append +
  ENABLE), CTO-gated. Its dispatcher refusal of an unlisted document gets exercised *at activation*, not today.
- **Artifacts serve nothing until the flip.** A green proves the floor; it does not publish.

---

## 4. IF IT DOES NOT FIRE AT ALL

Check in this order, and **do not conclude from the first empty answer**:
1. `scheduler get-schedule advi-49f-gold-floor` → is it still `ENABLED` at `cron(45 12 * * ? *)`?
   *(Verified ENABLED 2026-08-19 21:3xZ.)*
2. The dispatcher Lambda's own invocation record — did it fire and fail, or never fire? **Those take opposite
   remedies.**
3. DLQ `advi-49f-floor-dlq` — a message there means it fired and died.
4. **Never-launched is a third state.** Absent-day / stale-running / failed are three different findings; name
   which one before reporting.

⛔ **A missing artifact is not automatically a dead pipeline — resolve the trading calendar first (NEVER#1).
2026-08-20 is a Thursday, so a T-1 read of 08-19 data is the correct answer, not a staleness finding.**

---

## 5. REPORTING

One line to COO if clean, naming the six falsifiers as checked and the discriminator that proved execution
(F3's `schema_version: 1.1`). **Loud and immediate to COO + CTO** on any falsifier, with the denominator
beside every number. Do not report a green on the run's self-report — the whole point of this document is
that this chain has already produced a truthful-looking `CHAIN OK` over an empty result.
