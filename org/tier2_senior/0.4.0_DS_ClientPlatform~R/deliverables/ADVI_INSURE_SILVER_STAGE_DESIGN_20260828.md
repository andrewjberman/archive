# ADVI_INSURE — THE PRODUCTION SILVER STAGE (design proposal)

**Seat:** `0.4.0_DS_ClientPlatform~R` · **Authority:** `2.0.0_SA_COO` 78349 (next act; D2-D3 ledger row
12 unblocks (3), CTO 78326 item 3) · **Taken:** 2026-08-28 ~17:0xZ
**Status:** **PROPOSAL — not a build, not a deploy.** `2.0.0_SA_COO` sequences the BUILD after INS-a-5's
first scheduled fire (2026-08-29 11:35Z at the earliest).
⛔ **DISTRIBUTION: NOT TO `4.0.0_SA_CRO`** (PRD s.3, Andrew ~16:1xZ).

---

## 0. WHAT THIS IS, AND THE ONE THING IT IS NOT

Today `bd49f_insurance_conversion.py` is an **ad-hoc QA instrument**: a human passes `--date` and
`--write`. This proposes its promotion to a **scheduled stage** in the 49F chain, converting the three
convertible feeds daily after the bronze lands.

⛔ **IT IS NOT A NEW PIPELINE, A SHADOW PATH, OR A PARALLEL EMITTER.** The producer, the keys and the
grammar are unchanged; what changes is *who invokes it and on what clock*. Andrew's standing veto on
build-alongside pipelines (`memory/feedback_no_shadow_channels_veto_build_correctly_and_port.md`) is
the reason this is a promotion of the existing writer rather than a stage that re-implements it.

**Why it must be scheduled at all:** *"Ad-hoc gold runs are PERMITTED FOR QA; production pipelines MUST
be scheduled"* (CLAUDE.md, HARD STOPS). Every partition landed so far — including the one I wrote this
session — is a QA artifact and **is not production evidence**. The stage is what makes a daily
insurance silver plane real.

---

## 1. INPUTS I DO NOT OWN — named, not assumed

| input | value | grounding |
|---|---|---|
| bronze fire time | **11:35Z daily** | `2.0.0_SA_COO` 78349. ⚠ **RELAYED, UNVERIFIED AT THIS SEAT** — the leg is undeployed (`insurance_leg.py`), so there is no live schedule to read. Carried as the issuer's number with its caveat, not re-derived. |
| the consuming floor | **12:45Z** | 78349. Same caveat. ⚠ I searched the estate for `cron(45 12 …)` and the hits are the **INF pipeline** (`inf-api-assets-v2` et al.), a different chain — so **do not read those as corroboration**; they are a name collision on a clock slot. |
| the bronze leg itself | `0.6.0_AE_PartnerETL`, TO-A3-AE `@80734ba4cf`, seated 16:57:21Z | 78349 |

⛔ **THE STAGE'S WINDOW IS THEREFORE A DEPENDENT VARIABLE, NOT A CHOICE OF MINE.** If the AE lane's
first fire lands at a different time, the placement below moves with it and nothing else in this design
changes. **I am not encoding 11:35Z anywhere in code** — see s.3.

---

## 2. STAGE PLACEMENT

```
  11:35Z   INS-a-5 bronze fire (0.6.0_AE_PartnerETL) -- writes bronze/insurance_*
              |
              v
  ~11:4xZ   >> THIS STAGE <<  bronze -> silver, 3 convertible feeds
              |                 fact_insurance_relationshipaccountdetailsearch
              |                 fact_insurance_insurancerelationshiplist_export
              |                 fact_insurance_relationshipdetail
              v
  12:45Z   the consuming floor
```

It sits **between** the two, in the same position `a0x` occupies for the dimension feeds: a
bronze-to-silver conversion whose output the gold plane later joins. The gold consumer
(`bd49f_insurance_nav_current.py`) is **downstream of this stage and unchanged by it**.

---

## 3. TRIGGER — and why the obvious one is a defect

**PROPOSED: the chain's own sequencing** — this stage is a step in the 49F chain, invoked in order,
the same way `a00_runner` is.

⛔ **REJECTED: success-of-upstream as the only trigger.** *"success-of-upstream as the only trigger is
a defect"* (CLAUDE.md). The failure it hides is precise and this feed is exactly where it bites: if the
bronze fire **succeeds but pulls short** (as the 08-27 detailsearch pull did — 50 of a vendor-attested
77), a success-triggered stage converts a partial cohort on a green signal.

⛔ **REJECTED: a time-only trigger with no sequencing.** A fixed clock that races the bronze write
converts yesterday's partition and reports success.

⛔ **REJECTED, AND NOT MINE TO BUILD ANYWAY: any alarm / SNS / SES / freshness-checker / monitor.**
Standing moratorium — *"NEVER build an alert/alarm/SNS/SES-send/notification/freshness-checker/monitor
unless Andrew explicitly asks."* **A short pull must surface as a STAGE GATE (s.5), not a notification.**

> **THE TRIGGER-TIME ITSELF LIVES IN THE CHAIN DEFINITION, NEVER IN THE SCRIPT.** A time baked into
> the producer is a second source of truth for the schedule, and the two drift silently.

---

## 4. IDEMPOTENCE ON RE-RUN

**Already built and unchanged:** the writer lists the target silver key and, if it exists, prints
`SKIP: already converted (idempotent). Use --force to re-write.` A re-run of a completed day is a
**no-op**, not a re-write. `--force` stays a human's ad-hoc verb and **the stage never passes it.**

An **absent** bronze day is `SKIP: an absent day is ABSENT — no roll-forward, no zero rows.` A holiday
or a missed fire produces **no partition**, never a zero-row one.

> ⚠ **ONE OPEN QUESTION FOR THE ISSUER.** Idempotence is currently keyed on *the silver key existing*,
> not on *the bronze content having changed*. If a day's bronze is **re-pulled and corrected** (the
> 08-27 page-short partition is the live case — a completing `offset50` would make it convertible),
> the stage will SKIP the day because silver already exists. **Options:** (a) leave it — a corrected
> bronze is a human-noticed event and `--force` is the human's verb; (b) key the skip on a bronze
> content digest so a changed bronze re-converts. **(a) is my recommendation** — (b) adds a digest
> the stage must store and trust, and the failure it prevents is rare and already loud. **Issuer's
> call; I have not built either.**

---

## 5. THE COMPLETENESS CONTROL AS THE STAGE GATE

**This is the part that earns the stage.** The control already exists and already fired in anger:

```
COMPLETENESS CONTROL FAILED for insurance_relationshipaccountdetailsearch 2026-08-27:
rows after dedup=50 but the vendor attests total=77.
```

**As a stage gate it binds unchanged:** a page-short bronze partition is **REFUSED, not converted**,
and the stage exits **rc=1**. Converting anyway would launder a short pull into silver, where every
downstream reader would take it as the cohort.

**Per-feed fault isolation (fixed this session, `@07e4e488de`) is what makes that gate safe at stage
scope.** Before it, one feed's refusal aborted the run *before the other feeds were reached* — the
**controlled** feed silently took the **uncontrolled** one down with it. Now each feed is independent:
the finding prints in full, that feed does not convert, the others proceed, and **rc is still 1** so
the stage cannot read as clean.

⚠ **THE FEED WITH NO SUCH CONTROL IS THE ONE TO WATCH.** `relationshipdetail` ships **no
vendor-attested total** — S4 is a per-id fan-out, so its row count is *the number of calls made*.
It therefore reports `COHORT COVERAGE: N of <authority>` against the export partition and, when the
authority is missing, `UNKNOWN — UNKNOWN IS NOT COMPLETE`. **This stays REPORTED, never enforced:** a
shortfall means *fewer calls were made*, never *the vendor withheld rows*, and those demand opposite
responses. **Enforcing it would be a cross-feed inference wearing a control's clothes.**

---

## 6. THE STAGE'S OWN ACCEPTANCE

`insurance_silver_rule17_census.py` (this lane, `@07e4e488de`) is the acceptance instrument — the same
one `2.0.0_SA_COO` 78349 and `1.0.0_SA_CTO` 78287 named. Per run it asserts, per feed:

| arm | asserts |
|---|---|
| **F1** | no field slimming — every bronze field resolves to a silver column |
| **F2** | no invented silver vendor column |
| **F3** | row delta 0 — no business-row filter |
| **F4** | zero-null columns reported as *fillna candidates*, never as verdicts |

⛔ **IT MUST RUN WITH `--self-test`, AND THAT IS NOT CEREMONY.** F1=F2=F3=0 is what a conforming table
prints **and what a dead matcher prints**. The self-test plants one defect per arm from four different
truths and requires each to fire. **A census that cannot fail certifies nothing.**

Its negative control — BLOCK when the supplied page set misses the payload's declared total — exists
because **the instrument's own author tripped it**: my first invocation compared one 50-record page
against a 77-row partition and read `F3=-27`, a caller's pagination error wearing a Rule 17 violation's
clothes.

---

## 7. WHAT CHANGES IN `bd49f_insurance_conversion.py` — the smallest set

**Nothing in the readers, the grammar, the dedup, the controls, or the receipt handling.** The three
changes are all about *invocation*:

1. **A stage entry point** — `<stage>_runner.py` beside it, matching `a00_runner.py`'s shape
   (`--dry-run` / `--upload`, single-prefix law asserted, read-back verify). The core module keeps its
   `--date/--write/--force` CLI for QA. **One producer, two callers** — the runner does not
   re-implement conversion.
2. **The date defaults to the chain's business date** rather than being required, so the stage does
   not carry a second date-derivation. **T-1 vs same-day is resolved from the trading calendar
   frontier (`lib/trading_calendar.py`), never assumed** — and the bronze partition key is the
   vendor's pull date, which is **not** automatically the trading date. *Naming this because the two
   are equal on most days and unequal exactly when it matters.*
3. **The rc contract stated for a scheduler**: `0` = every present feed converted or was correctly
   skipped; `1` = at least one feed refused (finding, per-feed isolated); a raise = instrument
   failure, distinct from both.

⛔ **NOT PROPOSED: a schedule in Terraform, an EventBridge rule, an IAM change, or any deploy act.**
Those are the AE lane's and they follow the issuer's sequencing. This document is the DS half.

---

## 8. WHAT THIS DESIGN DOES NOT SOLVE — stated so nobody reads it as more than it is

- **Cohort coverage on `relationshipdetail` stays open.** Today's partition holds **1 relationship of
  77**. The stage will faithfully convert whatever the fan-out pulls; **making the fan-out cover the
  cohort is the AE lane's act**, not this stage's. *Three converted tables is not 77 covered
  relationships, and the two will look identical on a dashboard.*
- **The 08-27 page-short partition stays unconverted** until its bronze is completed. That is a PULL
  finding riding TO-A3-AE's face (78349), owner = the seat that ran the 08-27 invoke.
- **`comp-validate` has no config for this producer** — it returns `no script matching`, i.e.
  **UNVALIDATED**, and its rc through a pipe is 0. Before this runs as a stage, either a validate
  config is authored or the gap is declared on the stage's face. **I have not authored one; naming it
  is the deliverable here.**
- **Both gold-lane DS gates are structurally blind to this producer** (`postdeps` REFUSES rc=2,
  correctly; `comp-validate` does not fail closed). The predecessor recorded the same blindness against
  the *gold* producer — this is a **second subject**, so it corroborates rather than repeats.

---

## 9. THE ONE DECISION I AM ASKING FOR

**s.4's idempotence question:** re-run keyed on *silver existing* (recommended) or on *bronze content
changing*. Everything else here is either measured, already built, or explicitly the AE lane's.
