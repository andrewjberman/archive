# 49F artifact-layer adjudication -- and my own sweep's SEAT column is wrong

**Author:** `0.4.0_DS_ClientPlatform~G` - **Commissioned by:** `2.0.0_SA_COO` 71560
**Snapshot:** 2026-08-25T22:10Z - **Scope:** the three 49F `CLOSE` rows, plus the P2-FLOOR three-gate read

## NOTE: LEAD FINDING -- I HAVE TO CORRECT MY OWN SWEEP BEFORE ANYTHING ELSE

**`P2-FLOOR-49F` IS NOT A SEAT. THE FLOOR IS APPLIED, ENABLED, AND PRODUCING, AND HAS BEEN FOR SIX
DAYS.** My sweep classified it `SEAT` on the grounds that no proof instance exists. That verdict is
wrong at the artifact layer.

```
  advi-49f-gold-floor    State=ENABLED   cron(45 12 * * ? *) UTC
                         Created 2026-08-19T17:32:28Z   Target: advi-49f-gold-dispatch
                         Input: {"run_class":"production","source":"advi.49f.scheduled-floor"}
  EXERCISED: 7 of 8 canonical tables carry date=2026-08-24 -- T-1, the correct current answer
             today (NEVER#1: counted on the trading-day frontier, not wall-clock)
```

NOTE: **AND THE DEFECT IN MY SWEEP IS EXACTLY THE ONE I SPENT THE NIGHT FLAGGING IN OTHER PEOPLE'S
RECORDS.** I declared, in a box, that `CLOSE` was a RECORD-layer verdict that could not prove work
was done. **I did not declare the same limit for `SEAT`, and it has it just as badly:**

> `NO-INSTANCE` IS NOT `NOT-STARTED`. Both columns infer world-state from the presence or absence
> of a record artifact. I policed one direction and left the other unguarded -- and the unguarded
> one is what would have put a seat on six-day-old finished work.

**This is the third instance tonight of one shape: `<status>` stale, `CLOSE` unproven, `SEAT`
unproven. The record and the world are different planes, and every column I built reads the record.**

## Row verdicts

| row | verdict | basis |
|---|---|---|
| `P1-CLOSE-49F` | **CLOSE EARNED** | partition claim verified live with its invariant intact; cited commits + MCP real |
| `P2-DISPATCH-49F` | **CLOSE EARNED** | contract ordering verified from the AWS control plane, independent of the message |
| `P4-EMIT-49F` | **CLOSE EARNED** | served-plane emission present |
| `P2-FLOOR-49F` | **NOT A SEAT -- applied + exercised** | see above; residual is the accelerator half + an absent proof instance |

### `P1-CLOSE-49F` -- CLOSE EARNED

P1C-2 claimed `canonical_valuation 526 / flow_ledger 526 / nna_canonical 526 / twr_daily 525`,
range `2024-07-08..2026-08-10`. Live at the current home: **531 / 531 / 531 / 530**, range
`2024-07-08..2026-08-24`.

NOTE: **A +5 DELTA IS NOT A FALSIFICATION AND THE DISCRIMINATOR IS THE INVARIANT, NOT THE COUNT.** The
delta is **uniform across all four tables**, the **start date is identical**, and the claim's
internal invariant -- `twr_daily` exactly one behind the other three -- **is preserved on both
sides** (526/526/526/**525** -> 531/531/531/**530**). A claim that was wrong would not carry its own
invariant forward. This is a snapshot that aged by five emission dates, not a bad measurement.

P1C-4's ordering verified: commit `3a924da626` exists under `DS~A`; the MCP to CVO is in the inbox.

NOTE: **AND THE PATH IN THE INSTANCE NO LONGER RESOLVES -- WHICH IS A MIGRATION, NOT AN ABSENCE.** The
instance cites `s3://opal-data-assets/portal/gold/advi/49financial/`. That prefix returns **0
objects**. I did **not** treat that as an absence: positive control shows `portal/gold/` alive with
`etfs/` and `mdpf/`, and `advi/` genuinely gone from it -- the data is at
**`s3://opal-data-49financial/gold/advi/`**, consistent with today's D8 amendment moving gold out of
`opal-data-assets`. **Dormant-because-ABANDONED and dormant-because-KEY-MIGRATED are byte-identical
from a zero alone (Rule 25) and take opposite actions.** The instance was right at its vintage; the
estate moved under it.

### `P2-DISPATCH-49F` -- CLOSE EARNED, with a live residual that is NOT a defect in this row

P2D-4 claimed the invocation contract was delivered to AE **before AE's apply**. Verified, and the
strongest evidence is one neither the instance nor I had planned on:

```
  contract re-issue MCP delivered   2026-08-19T17:10:42Z   (file present in AE's inbox)
  advi-49f-gold-floor CREATED       2026-08-19T17:32:28Z   (AWS scheduler control plane)
  -> the apply follows the contract by 22 minutes
```

**That ordering is corroborated from a plane the authoring seat does not control.** A self-reported
"delivered before the apply" and an AWS-side creation timestamp are genuinely independent
instruments; this is corroboration rather than repetition. Cited commits `4dadd1354c` /
`2276ad55d5` both real under `DS~A`. P2D-3's QA fire is visible: `date=2026-08-18` present in **18
of 19** tables.

NOTE: **RESIDUAL, LIVE NOW, AND IT BELONGS TO NOBODY IN THIS SCOPE:**
`comp-pipescript deployed chain_49f_entrypoint.py` reads **STALE** -- repo ahead of S3.

```
  S3 _code/chain_49f_entrypoint.py   LastModified 2026-08-25T07:17:36Z   25,508 B
  repo HEAD for that file            b9915d8271   2026-08-25T21:24:54Z   31,943 B (LF-normalised)
  editors, last 8 days: OPAL_ADVIPOINTERS (DS~A) - D2_ADVI_49F (DS~B)
                        OPAL_GLDRNS (DS~H) - ADVI_PERFRP (AE~G, twice tonight)
```

**This is NOT a P2D-2 defect** -- that criterion was about the deploy act, which happened and was
verified at the time. It is a **FOUR-PROJECT SHARED ARTIFACT with no `<cross_domain_coordination>`
in any of the TOs**, which is the 0-of-13 finding from my dependency read arriving as a live
condition: `0.7.0_AE_CloudOps~G` edited this entrypoint twice in the last hour for `ADVI_PERFRP`,
and those edits are not on S3. **The scheduled floor is firing S3 code that is 14 hours behind the
repo.** Expected mid-flight; worth knowing before anything else is scheduled against it.

### `P4-EMIT-49F` -- CLOSE EARNED

`s3://opal-data-portal-v2/platinum/advi/49financial/` **exists**. Positive control:
`platinum/` carries `advi/`, `etfs/`, `mdpf/`. The emission that P4E's downstream rows consume is
on the served plane.

## The P2-FLOOR three-gate read -- what COO asked for

Stated gate: *"the 23:01Z fixture + the P2D-4 contract + a CTO per-apply gate."*

| gate | verdict | evidence |
|---|---|---|
| the 23:01Z fixture | **SATISFIED (inferred from ordering, not measured)** | TO issued 2026-08-18T16:05Z, so "tonight's 23:01Z" is 2026-08-18T23:01Z; the apply landed 2026-08-19T17:32Z, after it. **I did not measure the fixture's verdict** -- PHASE_B1 is a bd `gold_dispatch` phase and reading a six-day-old bd fixture outcome is the project ramp you told me to stop at. |
| the P2D-4 contract | **SATISFIED, MEASURED** | delivered 17:10:42Z; apply created 17:32:28Z |
| CTO per-apply gate | **RESIDUAL -- a HUMAN act, not an artifact** | as you said: named, not treated as unmet evidence |

NOTE: **BUT THE GATE QUESTION IS SUPERSEDED, WHICH IS THE ACTIONABLE PART: THE APPLY ALREADY HAPPENED.**
Asking whether P2-FLOOR may apply is asking about a decision taken on 2026-08-19. The floor is
ENABLED and has been producing to T-1 ever since.

**What is NOT discharged**, and I am not overclaiming it:
- the **silver completeness accelerator** half of that TO (its filename carries it; I did not verify it)
- the **unattended-cycle proof bar** (`08-20/21/22`)
- **no proof instance exists** for the row at all

So `P2-FLOOR` is **DELIVERED-BUT-UNEVIDENCED**, a state neither `CLOSE` nor `SEAT` describes.
`advi-49f-publisher` (cron(15 13), same creation timestamp) is applied but **DISABLED** -- consistent
with its publisher half gating on the downstream P4 rows, not with the floor being incomplete.

## Limits

1. **`CLOSE EARNED` here means the row's own acceptance evidence holds against live artifacts** --
   stronger than my sweep's record-layer `CLOSE`, still not a re-execution of the work.
2. **The fixture gate is INFERRED from ordering, not measured.** Marked as such in the table.
3. **I did not verify P2-FLOOR's accelerator half or its unattended-cycle bar** -- both need the
   project ramp your scope excludes. That is why my verdict is "not a seat for the floor half",
   not "close it".
4. **Snapshot of a live tree** -- the entrypoint moved twice while I was reading it.

-- `0.4.0_DS_ClientPlatform~G`
