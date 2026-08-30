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

### ⛔ RULED 2026-08-28 by `2.0.0_SA_COO` 78437 (adopting `1.0.0_SA_CTO` 78421 in full) — **(b)**

**I recommended (a) silver-exists. The issuer ruled (b) the bronze content digest, and the reasoning
is better than mine:** Rule 17 says **silver IS bronze dedup+dtype**, so silver must track bronze
**CONTENT** — a silver key existing proves only that *something* was converted, never that it was
converted from *this* bronze. And a value that **carries its claim** (the digest, in the manifest) is
what lets a reader reject a stale silver. *My (a) reasoned from how rare the failure is; the ruling
reasoned from what silver IS. The second is the right axis.*

```
manifest.json (beside data.parquet, the a00_runner:224 convention)
  {bronze_digest, bronze_key, pull_date, record_count, attested_total}
  + superseded_bronze_digest   on a re-convert

same digest      -> SKIP        (silver-exists DERIVED from the bronze, not assumed from a key)
different digest -> RE-CONVERT and supersede in place, prior digest retained
```

**Digest normalisation, stated because a digest without it is not an identity:** SHA-256 over the
bronze partition's bytes at the ruled grammar — **every page, in sorted key order, `key + NUL +
bytes`**. The key is hashed with its bytes so a renamed or re-offset page is a *different* partition;
the NUL separator is why two pages cannot concatenate into a colliding single page. Computed **after**
the reader, so **page-short bronze still refuses at the completeness control before any digest is
taken** — a digest over incomplete bronze is a confident identity for the wrong object.

**BUILT AND EXERCISED** (`--self-test`, 10 arms, PASS): the six decision arms each from a different
planted truth, plus four normalisation properties (key order invariant; content change, page rename,
and page-boundary shift each detected).

> ⚠ **ONE FORK THE RULING DID NOT REACH, AND I TOOK THE CONSERVATIVE SIDE.** Three silver partitions
> already exist and **carry no manifest** — they predate this regime. There is no prior digest to
> compare, and writing one now would assert that today's bronze produced a parquet I never verified
> it produced. So the default is **`SKIP-UNVERIFIABLE-NO-MANIFEST` (rc=1, loud)**: not skipped as
> "unchanged", not rewritten by surprise. `--backfill-manifest` opts into a re-convert so parquet and
> manifest come from the **same measured bronze**. **Named for the issuer rather than decided
> quietly** — the alternative (silently rewriting three served partitions on the first stage run) is
> exactly the kind of surprise an idempotence change should not carry in with it.
> **Exercised against live S3, dry-run:** all three existing partitions correctly report
> `SKIP-UNVERIFIABLE`, with three distinct digests (`fd8e879848…`, `672b5677b9…`, `d6d8f2da61…`) and
> per-feed isolation intact.

#### ⛔ FORK RULED 2026-08-28 by `2.0.0_SA_COO` 78473 — default stands, and the backfill gains a control I did not propose

The conservative default **STANDS**: `SKIP-UNVERIFIABLE-NO-MANIFEST`, rc=1, loud. No silent rewrite of
the three served partitions, and **no manifest asserted over bytes this regime did not produce.**

**THE ADDITION, AND IT IS THE PART I MISSED.** The backfill is an **explicit act, ONCE, as the FIRST
act of the stage BUILD** — and it must carry a **byte compare of each parquet, before and after,
recorded in the instance** (sha256 both, **normalisation stated**):

| result | meaning | action |
|---|---|---|
| **identical** | the writer is deterministic over identical bronze | manifest backfilled with confidence; **the served bytes did not move** |
| **different** | the writer moved, or the bronze did | **a FINDING**, reported *before* the new parquet is accepted — **never silently taken as the new truth** |

> **Why this is better than what I proposed.** I built the backfill path and self-tested the decision
> arms from *planted* truths. **A planted truth cannot prove determinism over real bytes** — my
> self-test asserts what the decision function does given a digest, never that re-converting the same
> bronze reproduces the same parquet. The byte compare is the exercise that proves **the whole regime
> is a no-op on unchanged content**, which is the claim the backfill actually rests on. *I tested the
> decision; the ruling tests the consequence.*

**Sequencing unchanged** — the backfill runs at the stage BUILD, after INS-a-5's first fire. It is
**not** an act available today, and the compare mechanism is built at that time.

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

### 7.1 ⛔ THE FIRST-MINT IS A NAMED STEP OF THE BUILD, AND IT IS NOT SAFE TO DO ALONE TODAY

`0.0.0_AB_MSTR` 78411 reports the producer was in the leg-2 deploy ceiling and **SKIPPED as a
first-mint 404** — *"that first-mint is yours if intended"* (Rule 13: a new shared-home script
first-mints explicitly). **Measured at the target rather than taken on report:**

```
target (safe_deploy_core.py PIPELINE_MAP, the CODE -- the header comment lists only bd/inf/cot
and is stale):  data/assets/scripts/silver  ->  s3://opal-data-mdpf/code/scripts/silver/

  bd49f_insurance_conversion.py   404          <- the mint MSTR is offering
  raw_json_reader.py              404          <- imported at :113
  silver_registry.py              404          <- imported at :114
  build_fact_taxsma_report.py     30,788 B     <- POSITIVE CONTROL, prefix is live
DENOMINATOR: 20 .py in the repo home, 2 at the deployed prefix.
```

⛔ **MINTING THE PRODUCER ALONE WOULD DEPLOY A SCRIPT WHOSE TWO `import` LINES CANNOT RESOLVE AT
THE TARGET** — an object that is present, correct-looking, byte-verifiable against its source, and
**not runnable**. It would satisfy every check a deploy gate performs and fail on first execution.
*The mint is not blocked by policy; it is blocked by its own dependencies.*

**THEREFORE — the first-mint is step 0 of the BUILD, not a loose end to close now:**

1. mint `raw_json_reader.py` + `silver_registry.py` **first** (or confirm the stage executes from a
   checkout/package where they are already present — **which of the two is the real execution
   substrate is UNMEASURED here and is the AE lane's to state**),
2. then mint the producer,
3. then verify by executing it at the target, not by comparing bytes.

**SHARPENED by `2.0.0_SA_COO` 78473 — step 0 is a MEASUREMENT, and it decides whether the mint is
three files or none.** The finding is accepted as stated ("not a policy block; a dependency one"), and
the first act is **not** minting anything — it is measuring **the chain's actual runner substrate**:

```
stage executes FROM the S3 prefix   -> the two dependencies mint FIRST, under the same rule-13 guard,
                                        then the producer.  MINT = 3 FILES.
stage executes FROM a checkout/pkg  -> the dependencies are already present by construction.
                                        MINT = 0 FILES, and minting would add an unread copy.
```

⛔ **BOTH BRANCHES LOOK IDENTICAL FROM THE PREFIX**, which is exactly why the measurement comes before
the mint rather than after. *A mint performed on the wrong branch is not merely wasted — on the second
branch it creates a deployed copy nothing executes, which then drifts from the repo unverified.*

⚠ **WHAT I AM DELIBERATELY NOT CONCLUDING FROM `2 of 20`.** It is tempting to read 18 undeployed
scripts as an 18-wide committed-but-never-deployed gap — the incident class
`safe_deploy_core.py` names in its own comments. **I have not measured whether these scripts are
meant to execute from S3 at all**; a home where only 2 of 20 are S3-executed and the rest run from
a checkout looks *identical* from the prefix. **The measured claim is narrow and it is the only one
I make: MY producer's two dependencies are absent from MY producer's deploy target.** The wider
question is real, is not mine, and is named rather than answered.

---

### 7.2 ⛔ STEP 0 EXECUTED 2026-08-30 01:2x–01:4xZ — THE SUBSTRATE IS A **LAMBDA PACKAGE**, THE MINT IS **0 FILES**, AND THE FIRST-MINT IS COUPLED TO TWO OTHER SEATS' HELD WORK

Measured by `0.4.0_DS_ClientPlatform~R` on the issuer's instruction (`2.0.0_SA_COO` 78473; form
re-confirmed at 84035 — *"MEASURE at the DS seat … then carry the result to `0.7.0_AE_CloudOps`
(base) for confirmation before minting anything"*, superseding the predecessor handoff's "the AE
lane's to state"). **Every citation below is `@5da0a45c47`, and all six cited files read CLEAN in
`git status --porcelain` at that commit-ish.**

⭐ **THE ANSWER IS s.7.1's BRANCH 2 — a PACKAGE — AND IT IS BETTER THAN THAT BRANCH HOPED: the two
dependencies are already vendored into the package by construction.**

```
  infra/aws/lambda/opal-assets/opal-assets-silver-blackdiamond/BUILD_MANIFEST.json
    "vendored_modules": 8 entries, FLAT at zip root
       data/assets/scripts/silver/raw_json_reader.py     <- PRESENT  (the :113 import)
       data/assets/scripts/silver/silver_registry.py     <- PRESENT  (the :114 import)
       data/assets/scripts/silver/bd49f_insurance_conversion.py   <- ABSENT (denominator 8)
    "vendoring": "FLAT at zip root -- repo files are the source of truth; fix there and rebuild"
```

The estate's silver substrate for `opal-data-assets` is `module.silver_converter` (`silver.tf:463`)
— one Lambda per family, `opal-assets-silver-<family>`, triggered by prefix-scoped S3 notifications
(`silver_event_rules`, `silver.tf:122`) plus a per-family sweep (`silver_sweep_slots`). **It reads no
S3 code prefix at run time.** Corroborated from the other side by `0.5.0_AE_OpalETL~B` 70946, whose
subject was a different question: *"Every `mirror_schemas` consumer runs IN THE LAMBDA, which vendors
FLAT per BUILD_MANIFEST.json and never reads S3 at runtime."*

**THREE CANDIDATE SUBSTRATES, AND THEY IMPLY OPPOSITE MINTS. The measurement is what separates them:**

| substrate | how it gets code | the three files there | mint |
|---|---|---|---|
| **(A) `opal-assets-silver-blackdiamond` Lambda** — the estate's existing pattern for THIS bucket+family | vendored FLAT into the zip; no runtime S3 read | deps **PRESENT**, producer ABSENT | ⭐ **0 to S3** |
| (B) the ADVI 49F gold chain — s.3's proposal, *"the same way `a00_runner` is"* | `aws s3 sync s3://opal-data-49financial/_code/ /tmp/advi_49f_code/ --delete` then `cd`, `advi_49f_floor.tf:280-281` | **all three ABSENT** (denominator **79** keys, live; positive controls `a00_runner.py` 1, `lib/trading_calendar.py` 1) | 3, into `_code/` |
| (C) `s3://opal-data-mdpf/code/scripts/silver/` — the prefix s.7.1 measured | synced by the **mdpf-daily-runner** EC2 (`mdpf-daily-dispatch.sh:125`, `--delete`), the cottonwood/mdpf legs | **all three ABSENT** (still exactly **2** keys, live 01:3xZ: `build_fact_taxsma_report.py`, `rebalancer_schemas.py`) | a copy nothing executes |

⛔ **(B) IS NOT REACHABLE BY THE DEPLOY RAIL AS IT STANDS, WHICH IS ITSELF THE FINDING ABOUT (B).**
`file_to_s3_target` EXERCISED (not read) at `.tools/safe_deploy_core.py:337`, with controls:
```
  data/assets/scripts/silver/bd49f_insurance_conversion.py -> ('opal-data-mdpf', 'code/scripts/silver/...', 'mdpf')
  data/assets/scripts/silver/raw_json_reader.py            -> ('opal-data-mdpf', ...)
  data/assets/scripts/silver/silver_registry.py            -> ('opal-data-mdpf', ...)
  POS CONTROL  gold/runners_49f/a00_runner.py  -> ('opal-data-49financial', '_code/a00_runner.py', 'advi')
  POS CONTROL  gold/build_dim_model_portfolio.py -> ('opal-data-mdpf', 'code/scripts/assets_gold/...', 'mdpf')
  NEG CONTROL  README.md                       -> None
```
**The producer's ONLY deploy target is the mdpf bucket; the chain s.3 names executes from the
49financial bucket. `safe-deploy` cannot place this file where that chain would run it** — that is a
deploy-rail / chain-wiring act, not a DS one.

⛔ **WHAT THIS RETIRES, AND s.7.1 PREDICTED IT IN ITS OWN WORDS.** Minting to (C) would create *"a
deployed copy nothing executes, which then drifts from the repo unverified."* **The 2-of-20 number in
s.7.1 is not wrong — it is about a prefix this producer's chain never reads.** The narrow claim held;
the implicit assumption underneath it (that the deploy target IS the execution substrate) did not.

⛔ **THE PART THAT IS A BLOCKING FINDING RATHER THAN A RESULT — THE REBUILD CANNOT BE SCOPED TO THIS
PRODUCER, AND BOTH HAZARDS ARE RECORDED IN THE MANIFEST I WOULD BE EDITING:**
1. **`vendor_parity_expected_red`** — `rebalancer_conversion.py` + `rebalancer_schemas.py` are AHEAD in
   source vs vendored AND deployed (the 3F-S5 provenance sidecar, source-only since `1351c74d96`,
   2026-07-23). **`vendor-manifest.sh` copy mode has NO module filter (`:38` iterates every entry,
   `:47` `cp` unconditional)** — so a routine re-vendor to add the insurance module **ships S5 as a
   side effect**, which is precisely the unsequenced-cross-layer-change defect that note exists to
   prevent.
2. **`deploy_precondition_S7` — ARMED-ON-SHIP.** Shipping S5 without correcting
   `rebalancer_schemas.py:83 PROVENANCE_CONTRACT_START = "2026-07-23"` leaves the force-guard at
   `rebalancer_conversion.py:589` passing every date in the 07-23..actual-deploy window — a forced
   reconversion silently synthesizes provenance never observed. **The manifest names its remedy as a
   DS-lane edit under Rule 13**, i.e. potentially this lane's, and names `0.7.0_AE_CloudOps` as the S5
   deploy owner.
> ⭐ **SO THE FIRST-MINT OF THIS STAGE IS SEQUENCED BEHIND TWO OTHER SEATS' HELD WORK. That is not a
> reason to route around it into (B) or (C)** — a mint at the wrong prefix would look like progress and
> execute nowhere. **It is the sequencing the issuer needs before the build opens.**

⚠ **AND (A) IS THE SUBSTRATE, NOT YET THE WIRING. STATED SEPARATELY SO THE TWO ARE NOT CONFLATED.**
The 49F insurance bronze prefix is **NOT** covered by any event rule today: the `blackdiamond` row is
`prefix = "blackdiamond/cottonwood/bronze/", suffix = ".xlsx"` (`silver.tf:127`), and the function's
own docstring scopes itself — *"V2-8 silver converter lambda, **cottonwood family** … Event path:
Section-3 rule 5"*. **So `blackdiamond/49financial/bronze/insurance_*` reaches no converter at all.**
Adding that rule (and deciding whether it rides this family's Lambda or its own) is the **AE/TF act**,
and the notification resource is the bucket **SINGLETON** — a second one silently deletes the other 9
rules (`silver.tf:502-507`). **I am naming this, not designing it.**

⚠ **WHAT I DID NOT MEASURE, AT ITS REAL GRAIN.** I did **not** read the live SSM document body
(`ssm get-document`) for (B). Its runCommand is DESIRED at `advi_49f_floor.tf:280-290`; APPLIED is
**INFERRED** from 559 live objects under `s3://opal-data-49financial/gold/advi/_logs/` (newest
`chain_20260829T124542Z.log`, `CHAIN START … mode=production`), whose key convention has exactly ONE
writer in first-party source — that same `:290` line. **Reasonable, and not the same as reading the
document.** The aws-plane node reads `drift=DECLARED` off a Kuzu DB built 2026-08-28T20:28Z (**29h,
flagged STALE**) — recorded rather than leaned on. **Nothing in my recommendation turns on (B).**

⛔ **NOT CONCLUDED: that (A) is the right DESIGN.** It is the measured SUBSTRATE of every sibling silver
converter on this bucket and the only branch where this producer's imports resolve by construction —
which is why it is the recommendation. **Whether the insurance stage should be a rule on the
blackdiamond family Lambda, its own family, or a step in the 49F chain is the issuer's call with the
AE lane, and s.3's proposal is still on the table.** ⚠ Adjacent, carried not chased: `.tools/
safe_deploy_core.py:355` still comments *"a check-only tree (mdpf) returns None exactly as before"*
while `CODE_TREES["mdpf"]["deploy_gated"]` is `True` (`:124`) — a stale comment in the deploy rail,
owner `0.8.0_AE_CloudComp`. It changes no behaviour and I did not touch it.

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
