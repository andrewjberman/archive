# DEPLOY LEDGER -- ADVI_49F.c02-FLOORHOLD: hold `advi-49f-gold-floor` until one convention

**Opened:** 2026-08-30T01:52Z by `0.7.0_AE_CloudOps` (base)
**TO:** `org/tier2_senior/0.7.0_AE_CloudOps/task_orders/ADVI_49F.c02-FLOORHOLD.hold-advi-49f-gold-floor-until-one-convention.md`
**Authority:** never-widen sign-off, BOTH halves signed -- `2.0.0_SA_COO` 84137 + GO 84186,
`1.0.0_SA_CTO` 84165. CVO objection window open to 12:40Z today (`3.0.0_SA_CVO`, per 84165).
**State:** ⚠ **OPEN** -- closes at the LIFT, not at the apply.

---

## Why (one paragraph, so the lift reader does not have to reconstruct it)

c02's gross-return sign fix is live in the served code, but the **534 already-served partitions
still carry the inverted convention**. `--production` derives `D = prev_trading_day(now)`, so
**SUN 2026-08-30 and MON 2026-08-31 both derive `D=2026-08-28`** -- a partition that already exists
-- and `runner_common.py:123-125` puts **unconditionally**. Today's 12:45Z fire would therefore
**overwrite served `date=2026-08-28` in place**, flipping `r_gross`'s sign on one partition while 533
keep the old convention, `schema_version` still `"1.0"`, no vintage field, nothing recording the
change. Time-shape measured by `0.4.0_DS_ClientPlatform~N` 84104.

**The hold is FREE through Monday** (both fires re-derive an existing date). **TUE 2026-09-01 is the
first fire deriving a NEW date (`D=2026-08-31`)** -- the hard lift-by.

**Why this knob:** c02 has ONE executor (`chain_49f_entrypoint.py:181-186`) and the entrypoint has no
stage-scoping (P14 @`f62e93b9bb`). A c02-only skip would be a production code edit under an 11-hour
clock -- **wider in risk, not narrower.**

---

## Manifest (every leg carries proof before CLOSE)

| leg | kind | target | proof required | proof | state |
|---|---|---|---|---|---|
| H-1 | verify | read-before-hold: deployed dispatcher bytes, SSM applied state, no off-schedule leg | byte comparison vs BUILD INPUT; live SSM read; host + in-flight command read | **DONE, and the hold is NOT moot.** (a) `advi-49f-gold-dispatch` deployed bytes are **byte-identical to the build input**: package member `lambda_function.py` sha256 `1fd82d3842ca0ffb76ea...` == the repo tree at `e2be5c2f42^` (LF-normalised both sides -- CRLF/LF splits sha256), 7,959 B each; in-package `BUILD_MANIFEST.json` independently self-attests `built_from_commit 1abc54fa4c` with the SAME member digest. Function `State=Active/Successful`, `CodeSha256 fEMCZ4usqXuIC1GhklcClwOn/O6vR+uV+xgbk+oj8lk=`, `LastModified 2026-08-19T17:32:12Z`. **The dispatcher is healthy, so today's 12:45Z fire is real and the hold is REQUIRED.** (b) SSM document `advi-49f-chain-dispatch` APPLIED plane: `DocumentVersion 3` (Latest 3, Default 3), `Status Active`, params `Date` (default `''`), `DeclaredHistorical` (`'false'`), `StartedByDispatcher` (`'false'`). ⚠ NOTE: the 08-27 record closed this document at version 2 with two params; it is now **v3 with a third param `DeclaredHistorical`** -- a change after 08-27, surfaced not chased. (c) Off-schedule leg: host `i-01003b035d2988dfb` is **stopped** (r6i.4xlarge, last launch 2026-08-29T23:00:30Z); last 10 SSM commands on it are ALL terminal (7 Success / 3 Cancelled, all `ADVI_49F.P14-VEHICLE` campaign backfills); **zero InProgress/Pending**. | CLOSED 20260830T015000Z |
| H-2 | deploy | `aws_scheduler_schedule.advi_49f_gold_floor` State -> DISABLED, TF-declared, targeted safe-apply | targeted plan = exactly 1 change; `scheduler get-schedule` State read back (NOT tf output) | **APPLIED.** Declared at `advi_49f_floor.tf` (`state = "DISABLED"`). Plan cut on the **1.9.8 shim** (`.tools/terraform.exe`, the binary `safe-apply` resolves -- PATH terraform is 1.14.5 and safe-apply REFUSES a cross-version plan file): targeted plan read **`Plan: 0 to add, 1 to change, 0 to destroy`**, sole diff `~ state = "ENABLED" -> "DISABLED"`. Applied via `.tools/safe-apply.sh -chdir=infra/aws/terraform/opal-assets apply c02-floorhold.tfplan`, rc=0. **READ-BACK ON THE LIVE PRIMITIVE, not tf output** (`aws scheduler get-schedule --name advi-49f-gold-floor`): **`State = DISABLED`**, `LastModificationDate 2026-08-30T01:53:22Z`; Expression `cron(45 12 * * ? *)` tz=UTC, Target `...function:advi-49f-gold-dispatch`, Input `{"run_class":"production","source":"advi.49f.scheduled-floor"}`, FlexWindow OFF -- **all unchanged, only State moved.** POST-APPLY TARGETED RE-PLAN: **`No changes. Your infrastructure matches the configuration.`** = 0-diff. **NEGATIVE CONTROL (so "DISABLED" is not a blanket effect or a misread):** `opal-assets-bd49f-dim-convert-daily` read `ENABLED` in the same breath. **TARGETING WAS REQUIRED, not stylistic:** the untargeted plan carries 3 foreign rows -- the 08-11 emitter repoint `2740e4de8f` + its IAM adds (the known coupling, surprise channel 76182 / CVO-accepted 76186) and this seat's own P2F-3b accelerator rows; `-target` excluded all of them. ⚠ HALTGT: safe-apply's inbox checkpoint passed, and per `ADHC_HALTGT` **that pass is NOT cited as evidence of no halt** -- a live Monitor moves messages before the checkpoint reads them. The real basis is that every message this seat received was read this session and none was `[STOP]`/`[HALT]` class. | CLOSED 20260830T015322Z |
| H-3 | record | this entry, carrying lift condition + lift-by + the accelerator coupling | the entry exists before the apply and names all three | **DONE** -- this file, written before H-2. | CLOSED 20260830T015200Z |
| H-4 | lift | re-enable `advi-49f-gold-floor` | lift condition met OR lift-by reached; `get-schedule` State reads ENABLED | *pending -- see LIFT below* | OPEN |

### Pre-change baseline, read LIVE (so the lift restores a measured state, not a remembered one)

```
  aws scheduler get-schedule --name advi-49f-gold-floor        (2026-08-30T01:4xZ)
    State       ENABLED            <- THE VALUE H-4 RESTORES
    Expression  cron(45 12 * * ? *)   tz=UTC
    GroupName   default
    Target      arn:aws:lambda:us-east-1:313476888478:function:advi-49f-gold-dispatch
    Input       {"run_class":"production","source":"advi.49f.scheduled-floor"}
    FlexWindow  OFF
```

⛔ **H-4 restores `State=ENABLED` and NOTHING ELSE.** Expression, target, input and flex-window are
untouched by this hold; a lift that changes any of them is out of scope for this entry.

---

## LIFT CONDITION -- whichever comes FIRST

1. **`C02-g-3` R-5 READ:** `gross_leg_vintage` present on **534 of 534**, **zero** at `"1.0"`.
2. **HARD LIFT-BY: TUE 2026-09-01 ~12:40Z** (12:45Z fire minus one chain runtime).

⛔ **AT THE LIFT-BY THE HOLD LIFTS ANYWAY**, even if the re-emission has not landed. The mixed column
then becomes a **repair** rather than a prevented state. **A missed production date is the larger
cost.** Stated in advance, per `1.0.0_SA_CTO` 84165, so the grader reads it as a decision and not a
discovery. This is consistent with Andrew's LD-0477 A2 word (*"lets just push on"*): the hold costs
zero new data through Monday and does not contradict that ruling.

---

## ⛔ NAMED COUPLINGS -- READ BEFORE THE LIFT, AND BEFORE ANY OTHER APPLY IN THIS WORKSPACE

**1. The P2F-3b accelerator is a SECOND path into the same chain** (`1.0.0_SA_CTO` 84165 (2)).
`aws_s3_bucket_notification.monolith_bronze` block `advi-49f-silver-complete-accelerator` targets
**`advi-49f-gold-dispatch` -- the same dispatcher this hold silences.** A schedule hold does not
cover it. **Its apply is SEQUENCED AFTER THIS HOLD LIFTS.** It cannot fire today (the M-2 producer
emit is BUILT-NOT-DEPLOYED; `schwab/08335338/meta/complete/` held 0 objects, positive control
`meta/conversions/` = 480), but **the sequencing is the control, not that fact** -- an M-2 deploy plus
an accelerator apply between now and the lift would re-open exactly the hazard this hold closes.

**2. A SECOND STARTER EXISTS AND IT IS NOT THIS SCHEDULE.** Both trigger planes swept at the hold:

```
  events     list-rule-names-by-target <dispatcher arn>  ->  []          (no rule-plane path)
  scheduler  list-schedules  denominator 18 in account, 5 advi/49f-named:
               advi-49f-gold-floor   ENABLED   -> dispatcher   <- THIS RESOURCE
               advi-49f-publisher    DISABLED  -> dispatcher   <- SECOND PATH, same target
```

⛔ **The hold is complete ONLY while `advi-49f-publisher` stays DISABLED.** Enabling it during the
hold re-opens the path with no warning from anything.

**3. THE HOLD DOES NOT COVER A DIRECT SSM SEND-COMMAND.** The `P14-VEHICLE` campaign legs in H-1(c)
invoked `advi-49f-chain-dispatch` **directly**, bypassing both the schedule and the dispatcher Lambda.
`0.7.0_AE_CloudOps~L`'s c02 re-emission campaign uses that same direct path **by design**. So this
hold stops the SCHEDULED fire; it does not and cannot stop a campaign driver. That is correct -- the
campaign is the remedy -- but **"the floor is held" must not be read as "nothing can write c02."**

---

## Rollback

`state = "DISABLED"` is a one-line TF attribute. Rollback == the lift: set `state = "ENABLED"` (or
drop the attribute, whose provider default is ENABLED), targeted `safe-apply`, `get-schedule` read
back. No data is moved by either direction.

## Log

- 20260830T015000Z H-1 closed: dispatcher deployed bytes byte-identical to build input; SSM doc v3 Active; host stopped, 0 in-flight commands. Hold NOT moot.
- 20260830T015200Z H-3 closed: this entry opened before the apply, carrying lift condition, lift-by and all three couplings.
- 20260830T015322Z H-2 closed: state DISABLED applied via targeted safe-apply (1.9.8 shim); live get-schedule reads DISABLED at 01:53:22Z; targeted re-plan 0-diff; negative control opal-assets-bd49f-dim-convert-daily still ENABLED.
