# D1_CATVIEWS.TO-I1-DS — PATH-TO-LIVE CHANNEL ENUMERATION

**Executing lane:** `0.4.0_DS_ClientPlatform~T` · **Issuer:** `2.0.0_SA_COO` (73727)
**TO:** `D1_CATVIEWS.TO-I1-DS.path-to-live-channel-enumeration` `@35f7ea8ced`
**Cells:** `D1-i-1` (executed) · `D1-i-2` (APPLIED-GATED, did not execute) · `D1-inv-5` (binds)
**Class:** DS, **READ-ONLY.** Nothing was applied, re-pinned, deployed or proposed as ready.

---

## 0. ⛔ THE DENOMINATOR THE TO ASKS FOR — AND IT IS NOT 19

The TO says **"19 pinned modules."** Measured, it is not, and the number is not wrong-in-kind — **it is a
VINTAGE.**

| source | entries | `.py` |
|---|---|---|
| `build_package.py` PACKAGE at **HEAD** | **22** | 18 |
| PACKAGE at the **running pin** `1b96f70ad3` | 21 | 17 |
| PACKAGE at `a4d71e9544` (**2026-08-06**) | **19** | 16 |
| **THE EXECUTING ARTIFACT** (deployed zip) | **23** | 18 |

**`19` was true on 2026-08-06 and has been superseded twice since.** The executing artifact's 23 = the 22
PACKAGE members + a `BUILD_MANIFEST.json` the builder GENERATES (not a PACKAGE entry), so **"pinned
modules" = 22, of which 18 are `.py`.**

**OPERATIVE DENOMINATOR USED THROUGHOUT THIS DELIVERABLE: 22.** Every count below is stated as *N of 22*.

---

## 1. `D1-i-1` — THE CHANNEL ENUMERATION (AC1)

**Grounded on the EXECUTING ARTIFACT** (the deployed zip, downloaded and enumerated), not on
`build_package.py`'s declaration — per `D1-inv-5`.

| # | member | ZIP | S3 code channel | EC2 |
|---|---|---|---|---|
| 1 | `mdpf_gold_consolidator.py` | YES | EXISTS+writable | — |
| 2 | `dim_mdpf_aggregate_aua_timeseries.py` | YES | EXISTS+writable | — |
| 3 | `dim_mdpf_account_distribution.py` | YES | EXISTS+writable | — |
| 4 | `dim_mdpf_aum_metrics.py` | YES | EXISTS+writable | — |
| 5 | `dim_mdpf_non_model_assets.py` | YES | EXISTS+writable | — |
| 6 | `mdpf_aggregate_aua.py` | YES | EXISTS+writable | — |
| 7 | `build_mdpf_spine.py` | YES | EXISTS+writable | — |
| 8 | `mdpf_revamp_model_crosswalk.py` | YES | EXISTS+writable | — |
| 9 | `mdpf_calendar_binding.py` | YES | EXISTS+writable | **YES** |
| 10 | `mdpf_category_registry.py` | YES | EXISTS+writable | — |
| 11 | `build_cottonwood_mdpf_slice.py` | YES | EXISTS+writable | — |
| 12 | `build_cottonwood_mdpf_pair.py` | YES | EXISTS+writable | — |
| 13 | `build_cottonwood_interpolated_backfill.py` | YES | **absent** | — |
| 14 | `validate_interpolated_backfill.py` | YES | **absent** | — |
| 15 | `build_dim_model_portfolio.py` | YES | EXISTS+writable | — |
| 16 | `rebalancer_schemas.py` | YES | EXISTS+writable | — |
| 17 | `trading_calendar.py` | YES | **EXISTS / NO-WRITER** | **YES** |
| 18 | `partner_roster.json` | YES | **EXISTS / NO-WRITER** | **YES** |
| 19 | `route_bindings.yaml` | YES | **absent** | — |
| 20 | `mdpf_model_registry.json` | YES | **EXISTS / NO-WRITER** | — |
| 21 | `r7_comparator.py` | YES | **absent** | — |
| 22 | `sectionB_field_paths.json` | YES | **absent** | — |

```
ZIP reached ............ 22 of 22
S3 EXISTS + writable ... 14 of 22
S3 EXISTS / NO-WRITER ... 3 of 22    <-- object present, NO deploy path refreshes it
S3 absent ............... 5 of 22
EC2 (third channel) ..... 3 of 22
```

### ⛔ WHICH CHANNEL THE SCHEDULED FLOOR ACTUALLY EXECUTES: **THE ZIP, FOR ALL 22.**

`build_package.py` assembles each member from an **immutable pin via `git show`** (`pin_bytes :230-232`)
and **refuses a symbolic ref**. The lambda executes `/var/task` — the zip. **The S3 code channel is not
on the scheduled lambda's execution path at all**, which is `D1-inv-5` stated as a measurement rather
than a caution: `safe-deploy` advances `s3-code-channel` and leaves `lambda-zip` exactly where it was.

**"S3 EXISTS + writable" therefore means "a second, non-executing copy is kept current" — NOT "deployed".**

---

## 2. `D1-i-1` — THE THIRD-ROUTE QUESTION (AC2)

**ANSWERED, NOT ASSUMED. THE AXIS GAINS A VALUE: THE SWEEP RETURNED A THIRD ROUTE.**

**METHOD — five candidate routes, each independently capable of firing:**

| # | candidate route | instrument | result |
|---|---|---|---|
| 1 | ZIP bundle | downloaded the deployed artifact, enumerated members | 22 of 22 |
| 2 | S3 code channel | `safe_deploy_core.file_to_s3_target` + `head_object` per key | 17 of 22 have an object |
| 3 | **Lambda LAYERS** | downloaded both attached layers, enumerated 1,507 entries | **NO pinned module** — third-party deps only (`exchange_calendars`, `pandas_market_calendars`, `pytz`, `dateutil`) |
| 4 | **EC2 distribution** | `EC2_MANIFEST.json`, exact-filename sweep over all 22 | **FIRED — 3 of 22** |
| 5 | **runtime code fetch** | read the executing handler's own bytes for `get_object` / `importlib` / `exec` | **ABSENT** — `get_object` reads DATA from the assets bucket; `importlib` loads the **packaged** comparator from a local path |

**THE THIRD VALUE, VERIFIED:**
```
EC2_MANIFEST.json  /services/mdpf-daily-runner/calendar_distribution
  = s3://opal-data-mdpf/code/scripts/gold/trading_calendar.py
    -- 2026-08-11 WS-A recovery (0.7.0_AE_CloudOps, ledger 20260811T0845Z_mdpf-chain-calendar-distribution)
  object HEAD: 6,979 B, LastModified 2026-08-11T08:36:56Z
  NEGATIVE CONTROL: head_object on a bogus key -> 404. The read discriminates.
```

**So `D1-i-1`'s axis is THREE-VALUED, not two:** `lambda-zip` · `s3-code-channel` · **`ec2-distribution`**.

**A NOTE ON HOW CLOSE THIS CAME TO BEING WRONG, because it bears on how much the count is worth:** my
first EC2 sweep matched on module **stems** and I read its output as containing two false positives. The
exact-filename re-run **with a positive control** (`mdpf-accrual-bridge.tar.gz` -> 1) **and a negative
control** (`zzz_nonexistent.py` -> 0) shows **all three are real** — `partner_roster.json` is named inside
the accrual-bundle leaf, past where my first display truncated. **The stem sweep and the filename sweep
returned the same count for different reasons; only the controlled one is evidence.**

---

## 3. ⛔ THE FINDING `i-1` WAS CUT TO PRODUCE

### `trading_calendar.py` HAS THREE ROUTES AND NO WRITER FOR THE ONE AN EC2 SERVICE CONSUMES.

- **ZIP:** present, built from `lib/trading_calendar.py` at the pin.
- **S3:** an object EXISTS at `code/scripts/gold/trading_calendar.py` — **dated 2026-08-11, 15 days old.**
- **`safe_deploy_core.file_to_s3_target("lib/trading_calendar.py")` returns `None`.** There is **NO DS
  deploy path that writes that key.** It was placed by a one-off recovery.
- **`mdpf-daily-runner` (EC2) distributes from that key.**

>> **A change to `lib/trading_calendar.py` reaches the lambda (via the next pin) and DOES NOT reach the
>> EC2 runner, because nothing refreshes the copy the runner reads.** The two consumers of one module
>> silently diverge, and no existing instrument reports it: `comp-pipescript deployed` resolves the
>> repo->S3 pair, and for this file that pair does not exist. <<

**This is the same shape as tonight's D8 defect one layer out** — a delivery route whose currency nobody
owns — and `lib/trading_calendar.py` is the file `NEVER#1` makes load-bearing for every staleness verdict
in the estate.

⚠ **RECORDED, NOT CHASED**, per the standing refactoring/migration embargo (Andrew ~20:32Z). It is
surfaced to `3.0.0_SA_CVO` cc the issuer, and this lane kept working.

**Two lesser observations, same class, stated without action:**
`partner_roster.json` and `mdpf_model_registry.json` also read **EXISTS / NO-WRITER**.
Five members have **no S3 object at all** — for `r7_comparator.py` / `sectionB_field_paths.json` that is
coherent (they are CVO deliverables vendored into the package, with no code-channel home by design).

---

## 4. `D1-i-2` — **APPLIED-GATED. DID NOT EXECUTE.** (AC4)

**No re-pin was performed. No `safe-apply` was run. No pin advance is proposed as ready.**

The NO-SHIP fence, cited verbatim from the TO:

> **`build_package.py:266` carries a stale-pin interlock whose STATED disarm condition is that
> `mdpf_category_registry.py`'s recon line adopt `RECON_TOLERANCE`. It has NOW ADOPTED IT
> (`@4e791e1e82`, 15:16Z) — so a reader will find a build refusal whose written reason no longer
> applies and conclude the pin may advance. IT MAY NOT. `D1_CATVIEWS` IS NO-SHIP FOR MORE THAN THIS
> FINDING: this was the last blocker to the package being LOADABLE, never to it being CORRECT.
> A DISARM CONDITION BEING MET IS NOT A SHIP DECISION.** (ruled 72364 s.3)

And `1.0.0_SA_CTO~Y`'s better statement of why: **the bundled registry copy is pre-defect AND
unreferenced, and a pin advance destroys both properties.**

**I MET THE TRAP AND IT BEHAVED EXACTLY AS THE FENCE PREDICTS.** `mdpf_category_registry.py` is
**PRESENT in the running bundle** (measured in the zip). Its presence is **not** evidence of safety — it
is the inert copy the fence exists to protect. **THE NO-SHIP LIFT IS ANDREW'S BY-NAME WORD AND NOBODY
ELSE'S.**

**AC4 terminal status: `APPLIED-GATED`. Not PASS** — a PASS would assert an apply that must not have
happened.

---

## 5. `D1-inv-5` — COMMITTING IS NOT EXECUTING (AC3)

**No claim in this deliverable reports a served-output or "live" property from a commit hash or an S3
code-channel upload.** Every channel claim is grounded on one of: the **downloaded executing zip**, a
**`head_object` on the actual key with a 404 negative control**, the **downloaded layer contents**, or the
**manifest's own text with positive and negative controls**.

⛔ **AND inv-5 CAUGHT ME MID-TASK, WHICH IS THE STRONGEST THING I CAN SAY FOR IT.** I read
`build_package.py` **at the running pin**, found `mdpf_category_registry.py` absent from its PACKAGE list,
and was one step from reporting that the registry is not in the running bundle. **The zip says it is.**
The pin is an ephemeral cherry-pick, so its `build_package.py` is an older vintage than the builder that
actually ran — **Rule 22a's ephemeral-pin clause `@4424c948f7`, which landed hours ago after two other
seats hit it independently, arriving a third time in one night at a third seat.** Read the bytes, not
the graph.

---

## 6. ACCEPTANCE CRITERIA

| id | criterion | status |
|---|---|---|
| `I1DS-AC1` | all members classified by channel, executing path named, **denominator printed** | **PASS** — 22 of 22, denominator printed and the TO's stale `19` reconciled to its vintage |
| `I1DS-AC2` | third-route question answered by a sweep that **could** have returned a third value | **PASS** — 5 candidate routes, 2 fired (ZIP, S3), **1 third route CONFIRMED (EC2)**, 2 returned controlled negatives (layers, runtime-fetch) |
| `I1DS-AC3` | no served/"live" property claimed from a commit hash or an S3 upload | **PASS** |
| `I1DS-AC4` | `D1-i-2` reported APPLIED-GATED, fence cited verbatim, no pin advance | **APPLIED-GATED** (expected terminal status; not PASS by design) |

---

## 7. CELL STATUS — WRITTEN ONLY FROM OBSERVED STATES

⛔ **NOT synthesized from criterion verdicts.** 4 criteria and 3 cells are different objects.

| cell | status | basis |
|---|---|---|
| `D1-i-1` | **OBSERVED — COMPLETE** | the enumeration in s.1-s.3 was performed end to end at this hand |
| `D1-i-2` | **OBSERVED — DID NOT EXECUTE** | I observed the fence and the decision not to run. I did **not** observe any property of a re-pin, because none occurred |
| `D1-inv-5` | **OBSERVED — HELD** | observed as a binding constraint that changed my own method mid-task (s.5). Not "verified" as a property of the estate — that is not what an invariant cell asserts |

---

## 8. SCOPE BOUNDARY HELD

**`D1-i-3` (portal render path-to-live) joined surface (i) at `@eb73d94342` and is NOT in this TO's cell
set.** This TO was cut `@35f7ea8ced` on `i-1`/`i-2`/`inv-5`; its alignment denominators read **3 cells /
4 criteria** and this deliverable covers exactly those. **A reader who sees "surface (i)" on both and
assumes coverage gets it wrong** — the issuer named that seam and I am carrying the name, not the
assumption. Nothing else on `D1_CATVIEWS` was touched.
