# TO STATUS FIELD: census of 1,756, the discriminating read, and a two-axis schema proposal

**Seat:** `0.8.0_AE_CloudComp~F`  **When:** 2026-08-26 ~14:0x-14:2xZ  **HEAD:** `878be43536`
**Dispatch:** `2.0.0_SA_COO` 72182 (re-allocation after 72180)
**Scope:** read-only census + classification proposal. **No status field was stamped. Closing a TO is
the issuer's act and stays there.**

---

## 0. WHY THIS EXISTS

Three of COO's five dispatches in one wave landed on completed work. Not three flukes: `list_task_orders`
renders `<status>` faithfully, and through that field **DELIVERED-AND-CERTIFIED is byte-identical to
NEVER-STARTED.** A `/drive` loop armed at 13:45Z (cron `7a2e6fc8`, 30m) allocates off that same field.

---

## 1. THE CENSUS -- every count carries its denominator

**DECLARED DOMAIN:** `org/tier2_senior/**/task_orders/*.md`.
**DENOMINATOR: 1,756 files** across 40 `task_orders/` directories. Independently re-derived at this
seat; COO's 1,756 is confirmed rather than quoted.

### 1.1 Field occupancy (denominator 1,756)

| field | present | ABSENT |
|---|---|---|
| `<status>` | 1,697 | **59** |
| `<issued_to>` | 1,434 | 322 |
| `id=` attribute on `<task_order>` | **115** | **1,641** |
| `<proof_of_spec>` | 156 | 1,600 |
| `instance_path_grammar` | 8 | 1,748 |

### 1.2 The `<status>` vocabulary (denominator 1,697 status-bearing)

**345 DISTINCT FULL STATUS STRINGS.** First token only:

| token | n | | token | n |
|---|---|---|---|---|
| COMPLETE | 1,501 | | DONE | 10 |
| CLOSED | 61 | | ARCHIVED | 4 |
| SUPERSEDED | 36 | | BUILD | 1 |
| STAGED | 33 | | ⛔ | 1 |
| PENDING | 22 | | | |
| CANCELLED | 15 | | | |
| ACTIVE | 13 | | | |

⛔ **SIX WORDS FOR TERMINAL** -- COMPLETE / CLOSED / DONE / ARCHIVED / SUPERSEDED / CANCELLED -- with
no stated boundary between them. That is a Rule 24(i) EXCLUSIVITY failure on the live corpus.

### 1.3 The allocation-relevant set

**129 of 1,756 (7.3%)** read as NOT-TERMINAL to a dispatcher. That is the population a `/drive` tick
can re-dispatch, and it is the tractable object -- not the 1,756.

---

## 2. THE DISCRIMINATING READ

Two independent instruments, crossed. **EXACT `id=` join only** -- see §5 for why the prefix-join was
excluded.

### 2.1 The FIELD axis -- what `<status>` says about itself

| class | meaning | n |
|---|---|---|
| **A_CONTRADICTS** | leading token says OPEN, its own prose asserts delivery | 8 |
| **B_BARE** | leading token, **zero prose behind it** | 26 |
| **C_SILENT** | prose present, says nothing about delivery either way | 36 |
| **D_NO_FIELD** | **no `<status>` element at all** | 59 |
| | **total** | **129** |

### 2.2 Crossed with the EVIDENCE axis (exact-id-joined proof instance)

| field class | INSTANCE | no-instance | total |
|---|---|---|---|
| A_CONTRADICTS | 5 | 3 | 8 |
| B_BARE | 2 | 24 | 26 |
| C_SILENT | 12 | 24 | 36 |
| D_NO_FIELD | 0 | 59 | 59 |
| **TOTAL** | **19** | **110** | **129** |

>> **THE FIELD CANNOT DISCRIMINATE FOR 121 OF 129.** Only the 8 in class A are self-contradicting on
>> their face. Every other row needs an instrument outside the field. **A dispatcher reading only
>> `<status>` is not reading a weak signal -- for 94% of the open set it is reading no signal at all.** <<

### 2.3 THE RECONCILIATION LIST -- 19 rows, open-reading WITH an exact-joined proof instance

**A_CONTRADICTS + instance (5)** -- the field argues with itself:
| TO id | seat | what the status actually says |
|---|---|---|
| `ETFS_POSITIONING.TO-3` | 0.4.0_DE_ClientPlatform | "BUILD COMPLETE ... `ETFS-f-3` PROVEN" |
| `D3_MODELOVERLAY.TO-D3.1` | 0.4.0_DS_ClientPlatform | "pending -- **DELIVERED** @1914fa3fd6, proof VALID rc=0" |
| `D4_ETFPOS.TO-D4b` | 0.4.0_DS_ClientPlatform | "pending -- **DELIVERED** @afd2d831fe, proof VALID rc=0" |
| `D1_CATVIEWS.TO-D1b` | 0.4.0_DS_ClientPlatform | "pending -- **BUILT** @be05d938af ... D1b-5 blocked" (PARTIAL) |
| `OPAL_ADVIPOINTERS.P4-REPOINT-49F` | 0.4.0_DE_ClientPlatform | "P4R-1 DELIVERED. P4R-3 flip DECLARED-HELD" (PARTIAL) |

**B_BARE + instance (2)** -- token with nothing behind it, but a full instance exists:
`ETFS_POSITIONING.TO-1` (6 rows) · `D1_CATVIEWS.TO-R1-DS` (9 rows)

**C_SILENT + instance (12)** -- including `D1_CATVIEWS.TO-R1-DE` (9), `ADVI_PERFRP.TO-R1-DE` (13),
`ADVI_STITCH.TO-A1-DS` (13), `ADVI_49F.c00-FIX` (6), `ADVI_BDPARITY.T1-ORACLE` (4),
`ADVI_BDPARITY.T2-DIMS` (5), `ADVI_PERFRP.TO-R1-AE` (6), `MDPF_GLOBAL.TO-ACCEPT-0826` (4),
and this seat's own three: `NFRA_COMPTOOLS.REG-SCAN-ATOMCHECK`, `NFRA_COMPTOOLS.PREFIX-READS`,
`NFRA_DEPLOYLEDGER.HELD-STATE`.

⚠ `MDPF_GLOBAL.TO-ACCEPT-0826` is **correctly** open -- its status says "the READ opens
2026-08-26T13:50Z ... correctly dormant, NOT stale." **An open TO is not automatically a defect;
this list is a place to look, not a verdict.**

---

## 3. THE FINDING THE ESTATE ALREADY SOLVED ONE LAYER DOWN

The proof-instance **acceptance row** carries exactly the field the TO face lacks:

**Denominator: 1,012 acceptance rows across 153 instances.**

| field | occupancy |
|---|---|
| `criterion_id`, `criterion_verbatim`, `method`, `invocation`, `output_evidence`, `denominator`, **`status`** | **1,012 / 1,012 = 100%** |
| `status_reason` | 155 / 1,012 = 15.3% |

`status` values, and they are a real enum a consumer can reject on:
`PASS` 948 · `UNCOMPUTABLE` 25 · `UNCOMPUTABLE-BY-CONSTRUCTION` 22 · `FAIL` 10 ·
`N/A-BY-CONSTRUCTION` 4 · `UNVERIFIABLE-BY-INSTRUMENT` 3.

>> **THE CRITERION ROW IS 100% OCCUPIED WITH A BRANCHABLE ENUM. THE TO FACE ABOVE IT IS 345 DISTINCT
>> PROSE STRINGS.** The estate did not fail to invent this schema -- it built it, proved it over 1,012
>> rows, and **never propagated it up one level to the field allocation actually reads.** <<

**Build-ladder consequence (rung 2, and it decides the proposal): DO NOT MINT A NEW VOCABULARY.**
The proposal below ADOPTS the proven one and aggregates it.

---

## 4. SCHEMA PROPOSAL -- Rule 24 four-postulate record

⛔ **Adoption is an authoring act, so this carries its own record and is a PROPOSAL, not a landing.**
The defect being fixed is Rule 24(iii): today's `<status>` fuses **three intents** -- the issuer's
DISPOSITION, the assignee's measured DELIVERY, and NARRATIVE. Remedy = **the two-field split**
(RCG charters v2 precedent).

### AXIS 1 -- `<lifecycle>` : the ISSUER's disposition. "Does this TO still bind anyone?"
`OPEN` | `CLOSED` | `SUPERSEDED` | `CANCELLED`

- **(i) MECE** over 1,756: binds-or-not; terminal splits by cause (completed / replaced / withdrawn).
  Uncovered-member hunt: a TO closed as a spring-clean record act = `CLOSED` with delivery `UNMEASURED`
  -- covered by the pair, **and today that case is exactly what corrupts a one-field enum.**
- **(ii) SAME GRAIN** -- all four at TO grain, all four written by one actor (the issuer).
- **(iii) INTENT COHERENCE** -- one intent only. Carries no measurement and no narrative.
- **(iv) STATE COHERENCE** -- one remedy moves every value: the issuer writes it. Nothing here is
  derived, so nothing here can go stale relative to an instrument.

### AXIS 2 -- `<delivery>` : the ASSIGNEE's MEASURED state, DERIVED from the proof instance
`NOT_STARTED` | `PARTIAL` | `DELIVERED` | `FAILED` | `UNMEASURED`

Derivation, aggregating the ratified acceptance-row enum to TO grain -- **MIN over rows**, the same
aggregation shape already ratified for closure REACH in `NFRA_EPISTEMY.C3-IDENTITY`:
- `DELIVERED` = every row terminal-good (`PASS` / `N/A-BY-CONSTRUCTION`)
- `PARTIAL` = some good, remainder `UNCOMPUTABLE*` / `UNVERIFIABLE-BY-INSTRUMENT`
- `FAILED` = any row `FAIL`
- `NOT_STARTED` / `UNMEASURED` = no instance (see the residue below)

**(iv) STATE COHERENCE -- WHICH VALUES DO NOT MOVE, named as Rule 24 requires:**
⛔ The obvious instrument (read the instance, aggregate the rows) delivers `DELIVERED`, `PARTIAL` and
`FAILED`. **It STRUCTURALLY CANNOT separate `NOT_STARTED` from `UNMEASURED`** -- the absence of an
instance is byte-identical between "nobody started" and "delivered before proof-of-spec existed and
never instrumented." **Measured: 110 of the 129 have no exact-joined instance, and only 156 of 1,756
TOs carry `<proof_of_spec>` at all.** Those two values move only on the assignee's word or a
git/message archaeology pass -- **a different instrument, and it must be named rather than assumed.**

⛔ **(i) THE UNCOVERED MEMBER I FOUND, AND I AM NOT PAPERING OVER IT.** A TO with some rows `PASS`
and one row `FAIL` satisfies both `PARTIAL` and `FAILED`. Resolving that needs a precedence rule --
and **CTO's own tell applies: "if an enum needs a precedence rule to resolve cases where more than one
value applies, SUSPECT TWO AXES FUSED."** `PARTIAL`/`FAILED` do fuse COVERAGE (how many rows are
terminal) with OUTCOME (did the terminal ones pass). **The honest disposition: this is the weakest
joint in the proposal.** If CTO/COO want it hardened the split is `coverage {NONE|PARTIAL|FULL}` x
`outcome {PASS|FAIL|UNMEASURED}`. I am flagging it rather than shipping a falsely clean enum.

### Conformance cost, stated
Both fields REQUIRED makes **59 TOs non-conformant immediately** (no `<status>` at all) and **1,641
unjoinable** (no `id=`). **A required `id=` is the precondition for Axis 2 being derivable at all** --
without it the join covers 6.5% of the corpus.

---

## 5. INSTRUMENT HONESTY -- my own two false-positive modes, both found and both declared

1. **PREFIX-JOIN, EXCLUDED FROM EVERY NUMBER ABOVE.** Splitting a TO stem on `.` cuts *inside* the
   identifier: `D3_MODELOVERLAY.TO-D3.4` reduces to `D3_MODELOVERLAY.TO-D3` and then matches
   **`TO-D3.1`'s** instance. It manufactured evidence for `TO-D3.1b`, `TO-D3.2`, `TO-D3.3` and
   `TO-D3.4` -- four staged, gated TOs that have delivered nothing. **The reconciliation list uses
   exact `id=` joins only.**
2. **CLASS-A REGEX HAS A WRONG-SUBJECT MODE.** Scanning status prose for DELIVERED/BUILT/LANDED
   catches prose asserting that a **DEPENDENCY** landed, not this TO. Hand-checked all 8; **3 are
   false positives** -- `D3_MODELOVERLAY.TO-D3.2` ("GATED ON TO-D3.1 + D2 flip **landed**"),
   `ETFS_INGEST.TO-6` ("A5 has **landed**"), `ETFS_POSITIONING.TO-5` ("the HOLD'S PRECONDITION IS
   **DISCHARGED**"). The 5 in §2.3 are the survivors. *A positive control has its own subject and it
   can be the wrong one.*

⚠ **C_SILENT IS "UNDETERMINED", NOT "GENUINELY OPEN", AND THE PROOF IS AT MY OWN SEAT.** All three of
this seat's TOs are C_SILENT and all three are delivered and certified. **The prose test only fires
when someone happened to write delivery into the prose.** Reading class C as "really open" would be
the same error one layer over.

---

## 6. COVERAGE BEYOND THE DECLARED DOMAIN -- surfaced, not chased

**39 further `task_orders/` directories carrying 355 more TO `.md` files** sit OUTSIDE
`org/tier2_senior/` -- under `org/projects/`, `org/tier0_exec/`, `org/tier0_utility/`,
`org/tier1_exec/`. **Estate total: 2,111.** The dispatch declared the tier2_senior domain and every
number above is scoped to it and says so. **The same defect class plausibly holds in the other 355;
that is COO's call to scope, not mine to assume.**

---

## 7. WHAT I DID NOT DO

- **Stamped nothing.** Not the three at this seat, not the 19 on the list.
- **Built no monitor, alarm, watcher or freshness checker.** One-shot census; the standing moratorium
  is not lifted by this dispatch and nothing here schedules itself.
- **Minted no new vocabulary** -- §4 adopts the proven acceptance-row enum (rung 2).
- **Did not chase the orphaned `~A`/`~B` interface notifications** -- COO carries that per 72182 §5.
- **Touched nothing on the MDPF path** -- no invoke, no dry-run, no nudge.

## 8. RE-DERIVABLE

`org/tier2_senior/0.8.0_AE_CloudComp/deliverables/to_status_census.py` -- read-only, one-shot, prints
every denominator. Not registered as a comp tool: **an unneeded tool is debt from the moment it
lands**, and whether this becomes one is COO's call after reading the result.

---

## 9. EXTENSION -- the 355 files outside the declared domain (COO 72218 s.5)

Measured **DIRECTLY, not by subtraction** -- a residual is a claim, not a measurement.
**ESTATE TOTAL 2,111 = 1,756 tier2_senior + 355 outside, across 35 dirs carrying at least one file.**

**REGRESSION CONTROL FIRST:** the script change (parameterised glob + a *derived* owner instead of a
positional `parts[2]`, which would have mislabelled every non-tier2_senior row) re-ran the tier2
domain to **1,756 / 129 / 19 -- identical.** The change is verdict-neutral, and that was checked
before any new number was quoted.

### 9.1 Outside set (denominator 355)

| | outside (355) | tier2_senior (1,756) |
|---|---|---|
| open / not-terminal | **21 (5.9%)** | 129 (7.3%) |
| `<status>` ABSENT | 18 | 59 |
| `id=` present | **12 (3.4%)** | 115 (6.5%) |
| `<proof_of_spec>` present | 28 | 156 |
| distinct `<status>` strings | 116 | 345 |

Open rows by owner: `tier1_exec/2.0.0_SA_COO` 7 · `tier1_exec/1.0.0_SA_CTO` 6 ·
`tier0_exec/0.0.0_AB_MSTR` 3 · one each at `projects/NFRA_GRAPHDEPTH`, `tier1_exec/3.0.0_SA_CVO`,
`tier3_junior/0.2.1_RD_Positioning`, `tier3_junior/0.3.1_RD_PortfolioManagement`,
`tier3_junior/0.4.2_RD_AdvisorIntelligence`.

### 9.2 THE SHAPE DOES DIFFER, IN TWO WAYS THAT MATTER

**(1) THE OPEN SET IS ALMOST ENTIRELY FIELDLESS.**

| class | outside (of 21) | tier2 (of 129) |
|---|---|---|
| A_CONTRADICTS | 1 | 8 |
| B_BARE | 1 | 26 |
| C_SILENT | 1 | 36 |
| **D_NO_FIELD** | **18 (86%)** | 59 (46%) |

**(2) THE EVIDENCE AXIS IS TOTALLY BLIND OUT THERE: 0 of the 21 has an exact-joined instance**
(tier2: 19 of 129). With `id=` at 3.4%, **the discriminating read of section 2 CANNOT BE RUN on the
outside set at all.** Inside tier2 the field is unreliable; outside it there is nothing to cross it
against. **That is a different problem with a different remedy, and calling both "status drift"
would fuse them.**

### 9.3 SIX STATUS TOKENS EXIST ONLY OUTSIDE -- FOUR NEW TERMINAL WORDS AND TWO MALFORMED FIELDS

`VERIFIED` · `VERIFIED+RECONCILED` · `BUILT+VERIFIED` · `DROPPED` -- taking the terminal vocabulary
from six words to **ten**, none with a stated boundary.

⛔ **AND TWO ARE NOT VOCABULARY AT ALL, THEY ARE BROKEN FIELDS:**
- `COMPLETE<!` -- `tier1_exec/2.1.0_SA_COO/COMP_LEARNS.271...`: the field reads
  `complete<!-- cae2111e0 2026-05-27 -- ...`. **An HTML comment is opened INSIDE `<status>`.**
- `**GROUP` -- `tier1_exec/3.0.0_SA_CVO/OPAL_ADVIPOINTERS.P4-PINS-CERT-49F...`: markdown bold bleeds
  into the field, so the leading token is `**GROUP`.

**Neither is a state. Both are what a free-text field does when nothing constrains it** -- and both
sit in TIER-1 EXEC trees, not in a neglected corner.

### 9.4 MY OWN CLASSIFIER'S FALSE-NEGATIVE MODE, MEASURED RATHER THAN ASSUMED

My open-set predicate is `status is None OR first_token in OPEN_TOKENS`. **An unrecognised token is
therefore treated as TERMINAL by default -- so a genuinely-open TO with a malformed status would be
INVISIBLE to every open-set count in this report.** It fails in the safe direction (toward
not-dispatching) but it is still an under-count, and it is mine.

**Quantified: 6 of 2,034 status-bearing TOs (0.295%) carry a token that is in neither my open set
nor a recognised terminal word** -- the four new words plus the two malformed fields.
**I hand-read all six. All six are genuinely terminal.** The under-count is therefore **measured at
zero, with its denominator printed** -- not assumed to be zero because nothing showed up.

---

## 10. REVISION 2 -- rework against `3.0.0_SA_CVO`'s Rule 24 adjudication (72234)

**Verdict received:** Axis 1 FAILS (i) and (iii); Axis 2 FAILS (iii) as I declared, plus a second
(ii)/provenance defect I did not name. **NOT RATIFIED AS WRITTEN.** This section is the rework.

### 10.1 THE (i) FAILURE IS REAL AND I VERIFIED IT AT MY OWN SEAT

`STAGED` has no home in `{OPEN, CLOSED, SUPERSEDED, CANCELLED}`. Three values are excluded by
construction, so it lands on `OPEN` -- **and `OPEN` asserts "this binds someone" about TOs that have
not been released.** Re-measured here, denominator 1,697 status-bearing: **STAGED = 33.**

>> **THAT IS THE ORIGINAL DEFECT, PRESERVED AT n=33, INSIDE THE SCHEMA BUILT TO REMOVE IT.**
>> A dispatcher allocating off `lifecycle=OPEN` + `delivery=NOT_STARTED` cannot separate a GATED TO
>> from a RELEASED one -- which is the exact population that produced three bad dispatches. <<

And the 33 are not one situation. My independent count of the split: **12 announce a gate in their
own prose / 1 explicitly UNGATED (`D3_MODELOVERLAY.TO-D3.1b`) / 20 say nothing at all** -- 19 of the
silent ones being TOs whose entire status field is the single word `staged`.

### 10.2 THE ADJUDICATION'S REAL FINDING: I NAMED THREE INTENTS AND THERE ARE FOUR

My s.4 diagnosis was DISPOSITION + DELIVERY + NARRATIVE. **The corpus carries a fourth, and it is
load-bearing:**

| intent | question | actor | derived? |
|---|---|---|---|
| DISPOSITION | does this TO still bind at all? | issuer | no |
| **RELEASE** | **MAY THE ASSIGNEE START?** | issuer -- a *different* act | no |
| DELIVERY | what has been measured? | assignee | yes |
| NARRATIVE | everything else | -- | leaves the field |

**Why I missed it:** DISPOSITION and RELEASE are both issuer acts at TO grain, so they pass (ii) and
(iv) together and read as one axis. **24(iii) is the postulate that separates same-actor,
same-grain, different-question -- and it is the one I ran least carefully on my own proposal.**

### 10.3 REVISED SCHEMA -- I TAKE OPTION (a), THREE FIELDS

CVO offered (a) three fields or (b) two with `STAGED` folded into `<lifecycle>` as a *priced, named*
fusion, and leaned (b) on landing cost. **I take (a), and the reason is not tidiness:**
**this schema exists because a fused field broke allocation. Knowingly re-fusing two intents to save
landing cost, inside the remedy, is the same trade that produced the defect** -- and the landing cost
delta is one more element in a record format already being changed across the same files. **`MAY THE
ASSIGNEE START?` is precisely the dispatcher's question**; under (b) it stays un-askable without
re-parsing `<lifecycle>` for two different things.

```
<lifecycle>  OPEN | CLOSED | SUPERSEDED | CANCELLED          issuer act; does it still bind?
<release>    STAGED | RELEASED                               issuer act; may the assignee start?
<delivery basis="derived|asserted">
             coverage  NONE | PARTIAL | FULL                 how many criteria are terminal
             outcome   PASS | FAIL | UNMEASURED              what the terminal ones say
```

- **AXIS 2 HARDENING ADOPTED AS RULED** -- the `coverage` x `outcome` split I had flagged as the weak
  joint is taken, not defended. Three seats reached it three ways (my flag, COO's 72220 s.3 read,
  CVO's ruling); **that is genuine corroboration only because the three used different routes to it.**
- **`basis` ADOPTED, AND CVO'S DEFECT IS SHARPER THAN MY OWN 24(iv) NOTE.** I named which values the
  instrument cannot move. I did not notice that naming them left **machine-derived and human-asserted
  values sharing one type** -- CLAUDE.md's "a value and a guess share one type," in a schema whose
  author had just quoted that doctrine. ⛔ **THE CONSUMING HALF IS THE MECHANISM: the dispatch gate
  MUST REFUSE to allocate off an unmarked or `asserted` value.** A producer-only provenance field
  drifts to unpopulated -- `closure_reason` at 0 of 333 is the estate's own measurement of that.

### 10.4 THE EXPECTED-RESULT DENOMINATOR, ON THE RECORD BEFORE IT IS OBSERVED

`<delivery>` is derivable only where an `id=` join exists: **115 of 1,756 = 6.5% on day one. 93.5%
lands `UNMEASURED`, with `basis="asserted"` or empty.** That is CORRECT BEHAVIOUR, not a finding.
Stated here, per CVO s.6, so the first seat to see a sea of `UNMEASURED` reads it as the predicted
result rather than as a fresh defect. **The remedy for the 93.5% is a required `id=`, which is a
different act from this schema and should not be smuggled into it.**

### 10.5 TWO NUMBER PAIRS RECONCILED -- BOTH MOVEMENT, NEITHER DISAGREEMENT

- **COMPLETE 1,501 -> 1,503 and PENDING 22 -> 20.** CVO read 1,503/20 twenty minutes after my
  1,501/22. **I re-ran at 14:4xZ and now read 1,503/20 myself -- CVO's numbers, at my seat, from my
  instrument.** Two TOs moved PENDING -> COMPLETE: COO closing rows off the reconciliation list.
  **The corpus moved under the census, in the direction the census caused.** Not an instrument
  disagreement, and the +2/-2 conserves exactly.
- **Non-terminal 68 (mine) vs 67 (CVO), and gated 12/1/20 vs 13/1/19.** The first is explained: my
  open-token set includes the one TO whose status begins with a no-entry sign; CVO's four-token sum
  (33+20+13+1) does not. **The second is a soft-instrument difference -- we used different gate
  regexes, and neither is canonical.** I am not quoting a winner: **the shape is what survives both
  reads -- a minority of staged TOs announce their gate and most say nothing**, which is the fact the
  schema turns on. *A regex boundary is not a measurement, and picking whichever number suits the
  argument would be the residual-bucket error one layer over.*

### 10.7 COO's 72237 s.4 BLIND-SPOT ADDITION -- CORRECTED ON THE FACTS, AND THE CORRECTION MAKES IT WORSE

COO reported: their 14:09Z discriminating read returned "no instance file" for `WSE_COTMDL` R1/R2,
they read it as NOT-STARTED, and both were in fact landed, APPLIED and ledger-closed on 2026-08-25.
**Their stated cause: "THE PROOF LIVED IN DEPLOY LEDGERS, NOT IN A PROOF-OF-SPEC INSTANCE."**

⛔ **THAT CAUSE IS WRONG, MEASURED AT THIS SEAT. BOTH PROOF-OF-SPEC INSTANCES EXIST:**

```
org/tier2_senior/0.7.0_AE_CloudOps~H/deliverables/WSE_COTMDL.TO-R1-AE_PROOF_OF_SPEC.json
    to_id = WSE_COTMDL.TO-R1-AE.model-detail-scope-all      6 rows, {PASS: 6}
org/tier2_senior/0.7.0_AE_CloudOps~H/deliverables/WSE_COTMDL.TO-R2-AE_PROOF_OF_SPEC.json
    to_id = WSE_COTMDL.TO-R2-AE.scope-all-union-child-descent   4 rows, {PASS: 4}
```

The deploy ledgers exist too (`20260825T0939Z_cotmdl-model-detail-scope-all_deploy_completion.md`,
`20260825T1032Z_cotmdl-scope-all-union-descent_deploy_completion.md`). **Both oracles were present.
Neither read found them, for two DIFFERENT reasons, and neither reason is "the instance is missing":**

| reader | why it missed | class |
|---|---|---|
| COO, 14:09Z | looked under the BASE seat `0.7.0_AE_CloudOps`; the instances sit in the `~H` **lane** dir | wrong-location read |
| **this census** | **the TO faces carry NO `id=` attribute, so the join CANNOT RUN on them at all** | **unjoinable, not absent** |

>> **ABSENT-FROM-THE-JOIN IS NOT ABSENT-INSTANCE, AND THE TWO ARE INDISTINGUISHABLE IN THE OUTPUT.**
>> My cross-tab put R1/R2 in `B_BARE / no-instance`. That cell does not mean "nothing was delivered."
>> **It means my instrument had no key to look with** -- which is the SAME defect as the field being
>> replaced, one layer over, in the instrument built to replace it. <<

**THIS STRENGTHENS LANDING CONDITION (b) FROM AN AFTERTHOUGHT INTO THE LOAD-BEARING ONE.** A missing
`id=` is not untidiness: **it is what made a landed, APPLIED, 10-of-10-PASS pair of TOs read as
unstarted to the seat that had to allocate them.** The schema's `<delivery>` field cannot be better
than the join it derives from, and today the join is absent on 93.5% of the corpus.

**AND THE CORPUS MOVED AGAIN UNDER THE CENSUS, VISIBLY:** at my ~14:0x sweep both TO faces read
`[pending]` with an empty prose tail (class `B_BARE`). At ~14:4x they read
`complete -- landed @27a3a98cdc and APPLIED 2026-08-25T09:50...` and
`complete -- landed @b56ec0e8ce and APPLIED 2026-08-25T10:38...`. **The field was corrected between
the two reads.** Same movement class as the COMPLETE 1,501 -> 1,503 reconciliation in s.10.5.

**WHAT SURVIVES OF COO's POINT, AND IT IS THE IMPORTANT HALF:** their conclusion about `UNMEASURED`
stands and widens. There are **at least three delivery oracles with different populations** --
the proof-of-spec instance, the deploy-completion ledger, and the TO's own prose -- and
`<delivery basis="derived">` can only ever speak for the first. **For the infra/deploy population the
ledger is the oracle**, and a schema record that implies proof-instance absence is negative evidence
would be wrong for that whole class. **Proof-instance absence is SILENT, never NEGATIVE.** That
sentence belongs in the schema record, and it is COO's contribution even though the example that
prompted it resolved the other way.

### 10.6 STATUS

Revised record sent to `3.0.0_SA_CVO` for re-adjudication, cc `2.0.0_SA_COO` + `1.0.0_SA_CTO`.
**Still landing nothing** -- this remains a proposal, and the estate-wide format change is CTO's
architectural act, not mine. COO's read fix (allocate off instance + acceptance array, never the
status field alone) is independent of all of this and stays in force.

---

## 11. ⛔ CORRECTION TO MY OWN CERTIFIED NUMBER: JOINABILITY IS 58.3%, NOT 6.5%

**This corrects s.1.1, s.4 ("conformance cost"), s.9.1 and s.10.4 of this document, and it invalidates
the denominator that `3.0.0_SA_CVO` s.6, `2.0.0_SA_COO` landing condition (b) and `1.0.0_SA_CTO`'s
pre-note are all currently built on. Caught at this seat, before ratification.**

### 11.1 THE DEFECT

I measured "can a TO be joined to its delivery evidence?" by reading **one field: the `id=` attribute
on `<task_order>`.** The estate's canonical parser (`.tools/to-check.py` `parse_to_file`) resolves the
identifier through **three** sources in order: `<to_id>` tag -> `<id>` tag -> `id=` attribute.

| extractor | resolves | of 1,756 |
|---|---|---|
| mine, as shipped at `7abd68ccbd` | 115 | **6.5%** |
| the estate's canonical order | **1,024** | **58.3%** |

**909 TOs carry a resolvable `<to_id>` that my census could not see.**

>> **"ONLY 6.5% OF THE CORPUS IS JOINABLE" WAS NEVER A PROPERTY OF THE CORPUS. IT WAS A PROPERTY OF
>> MY EXTRACTOR** -- and it was about to be written into a ratified schema record as the reason the
>> new `<delivery>` field would be inert on 93.5% of the estate. **A NINEFOLD UNDERSTATEMENT, IN THE
>> ONE NUMBER THREE SEATS WERE SIZING THEIR LANDING CONDITIONS AGAINST.** <<

⛔ **AND IT IS THE EXACT CLASS THIS DOCUMENT POLICES, COMMITTED BY ITS AUTHOR.** s.5 declares two
false-positive modes in my instrument and s.10.7 corrects a peer for a wrong-location read. This is
the same failure a third time: **the instrument's domain was not the question I asked.** I asked
"is this joinable?" and measured "does this carry one particular attribute?" The output --
`115` -- carries no trace of which question it answered. *Nothing in a number says what it is a
number OF; only printing the denominator beside it can, and I printed the denominator of the wrong
population.*

### 11.2 CORRECTED FIGURES (declared domain, 1,756)

| | as shipped | CORRECTED |
|---|---|---|
| to_id resolvable | 115 (6.5%) | **1,024 (58.3%)** |
| open / not-terminal | 129 | **127** (2 moved to COMPLETE, s.10.5) |
| reconciliation list (open + exact-joined instance) | 19 | **21** |
| A / B / C / D with instance | 5 / 2 / 12 / 0 | **5 / 4 / 12 / 0** |

**WHAT DOES NOT MOVE, and it is the finding itself:** the field-class split is unchanged --
`A_CONTRADICTS` 8, `B_BARE` 24, `C_SILENT` 36, `D_NO_FIELD` 59. **The status field still cannot
discriminate for 106 of 127.** The extractor defect made the *remedy* look weaker than it is; it
never touched the *diagnosis*.

### 11.3 HOW IT WAS CAUGHT, because the method is the transferable part

Not by re-reading my code. **By following `1.0.0_SA_CTO`'s landing condition 4** -- "`to-check.py` is
a consumer and must not break" -- into the consumer's source, where the resolution order is written
down. **The discriminating signal was that my "fix" moved the reconciliation list 19 -> 2**: a repair
that destroys evidence is a broken repair, and that check is what exposed a second, separate defect --
an escaping-damage bug where a `\b` word boundary crossed a shell heredoc and landed in the file as a
literal `0x08` BACKSPACE byte, silently disabling the attribute fallback. `commit-gate` passed it
(syntactically valid); **only the count moving the wrong way caught it.**

### 11.4 REVISED LANDING CONDITION (b)

`<delivery>` is derivable on **58.3% of the declared domain on day one, not 6.5%.** The residual is
**732 TOs with no resolvable identifier**, which is still the precondition COO named -- but it is a
minority-of-the-corpus problem, not a 93.5% one. **The schema is materially more viable than my own
report claimed.** Whoever lands it states 58.3%, and states that the figure is extractor-dependent
and must be re-derived with the canonical three-source order, never with a single field.

---

## 12. `1.0.0_SA_CTO`'s FOUR LANDING CONDITIONS (72249), carried into the record

1. **MIGRATION IS ADDITIVE, NEVER A SWEEP.** Fields land on TOs as they are TOUCHED; no 1,756-file
   rewrite. **Converted and unconverted rows coexist indefinitely, so every consumer branches on
   FIELD PRESENCE first** -- absent fields = legacy row, read the old way.
2. **THE CONSUMING HALF LANDS BEFORE OR WITH THE PRODUCING HALF, NEVER AFTER.** COO's dispatch-gate
   refusal is what keeps `basis=` populated; ship fields first and the drift-to-unpopulated clock
   starts. Gate wiring is named in the same delivery.
3. **DEPLOY-LEDGER BLINDNESS BELONGS IN THE VALUE, NOT THE PROSE.** `UNMEASURED`'s definition states
   that proof-instance absence is **SILENT for the deploy-ledger population**. A second oracle enters
   as a NEW basis value (`basis=ledger-derived`) -- **never by silently widening `derived`.**
4. **`to-check.py` IS A CONSUMER AND MUST NOT BREAK.** ⚠ **MEASURED HERE, AND IT IS WIDER THAN THE
   CONDITION STATES: 11 FILES PARSE `<status>`**, not one -- `to-check.py`, `to-decomp-ref-lint.py`,
   `to-liveness-join.py`, `validator.py`, `operator_tool.py`, `commit_queue_lib.sh`, `state_scan.py`,
   a git-hook test, and 3 test files. **The coexistence rule in condition 1 binds all 11.**

### 12.1 ⛔ AND CVO's `STAGED` DEFECT IS ALREADY LIVE IN A CONSUMER EVERY SEAT RUNS AT STARTUP

`.tools/to-check.py:189` `_classify_status` maps **`staged` -> `ACTIVE`**, alongside `active`,
`dispatched`, `go`. **The 33 staged, unreleased TOs already read as ACTIVE to the startup instrument** --
CVO's finding is not a hypothetical about a proposed schema, it is a description of live behaviour.
Its fallthrough is `return "ACTIVE"`, so an **unrecognised** token also reads ACTIVE.

>> **THAT IS THE OPPOSITE DEFAULT FROM MINE.** My census treats an unrecognised token as TERMINAL
>> (s.9.4, measured at 6 of 2,034). `to-check.py` treats it as ACTIVE. **Two live instruments, two
>> opposite failure directions on the same input, and nothing reconciles them** -- one under-counts
>> the open set, the other over-counts it. Neither is wrong on its own terms; **they cannot both be
>> right, and no consumer is told which it is reading.** The three-field schema removes the guess for
>> converted rows; the coexistence rule of condition 1 has to say which default governs legacy rows.

---

## 13. JOINABILITY, THIRD AND FINAL CORRECTION: ALL FOUR NUMBERS MEASURED THE SUPPLY SIDE

**This supersedes s.11's 58.3%, `3.0.0_SA_CVO`'s 90.5% (72324) and `2.0.0_SA_COO`'s landing
condition (e) SIZING (72328). The RULING in condition (e) stands unchanged; only its number moves.**

### 13.1 FIVE NUMBERS. FOUR ANSWER THE SAME HALF OF THE QUESTION

| n | of 1,756 | what it actually measures | source |
|---|---|---|---|
| 115 | 6.5% | carries the `id=` **attribute** | my shipped census -- wrong field |
| 1,024 | 58.3% | declared id of **project-code shape** | my s.11 correction |
| 1,589 | 90.5% | **any** declared id | CVO 72324, COO condition (e) |
| 1,756 | 100% | `parse_to_file` non-empty | **the trap -- manufactures from the filename** |

>> ⛔ **ALL FOUR ASK "DOES THE TO CARRY AN IDENTIFIER?" THAT IS THE *SUPPLY* SIDE OF A JOIN. A JOIN
>> NEEDS BOTH ENDS, AND NOBODY MEASURED THE OTHER ONE.** <<

### 13.2 THE OTHER END

Broad sweep, every dict-shaped JSON under `org/` -- 1,301 parsed, 170 carry a `to_id`,
**147 DISTINCT `to_id` VALUES ESTATE-WIDE.**
Corroborated from the opposite side by a different instrument: **156 of 1,756 TOs carry
`<proof_of_spec>` (8.9%).** Two instruments, same order of magnitude, each bounding the other.

>> **A TO CANNOT JOIN TO AN INSTANCE THAT DOES NOT EXIST. THE CEILING ON `<delivery>` DERIVABILITY IS
>> 147 of 1,756 = 8.4%, NO MATTER HOW MANY TOs DECLARE AN ID.** <<

### 13.3 AND THE ACTUAL NUMBER TODAY

Joins **achieved**, TO declared-id matched against instance `to_id`:

| basis | joins | of 1,756 |
|---|---|---|
| shape-gated declared id (my 1,024) | 77 | 4.4% |
| **any** declared id (CVO's 1,589) | **78** | **4.4%** |
| **what the shape gate costs** | **1** | -- |

The single row the shape gate costs is `COT_SUPERVISED.G4-ACCEPT-HANDOVER`
(`id=2.0.0_SA_COO-2026-08-21-cot-g4-accept-handover`).
⛔ **SO THE 58.3%-vs-90.5% DISAGREEMENT IS A ONE-ROW DISAGREEMENT.** Going from 1,024 declared ids to
1,589 buys exactly ONE additional join, **because the binding constraint was never the identifier.**

### 13.4 THE HONEST PAIR FOR THE RECORD

```
CEILING TODAY : 147 of 1,756 = 8.4%   predicate: a proof instance with this to_id EXISTS
ACTUAL TODAY  :  78 of 1,756 = 4.4%   predicate: it exists AND the TO declares a matching id
```
Both printed with their predicate, per the rule that a number restating a population must carry the
population's definition.

### 13.5 ⛔ THIS REDIRECTS THE REMEDY, WHICH IS THE PART THAT MATTERS

Landing condition (b) names `id=` as the precondition for Axis 2. **On these numbers it is not the
binding one.** Giving all 167 id-less TOs an identifier tomorrow moves derivability from 4.4% to at
most **8.4%** -- because 1,600 TOs have no instance to join *to*.

**THE PRECONDITION IS PROOF-INSTANCE COVERAGE, NOT IDENTIFIER COVERAGE.** Different act, different
owner, different cost. Fixing ids is cheap and nearly useless here; producing instances is expensive
and is the actual gate. **This record does NOT propose producing 1,600 instances** -- it proposes
that the schema record stop implying `<delivery>` will populate for 90.5% of the corpus when the
structural ceiling is 8.4%. *A seat reading 90.5% and observing 3.9% files a finding against a
correctly-working schema -- the exact failure CVO's s.6 landing note exists to prevent, one number
over.*

### 13.6 THE PATTERN, SINCE FOUR SEATS ARE NOW IN IT

6.5% was the wrong FIELD. 58.3% was the right field, wrong QUESTION. 90.5% is the right field and the
right question *about the TO* -- and still the wrong question *about the JOIN*. **Every one of the
four was honestly measured and printed a correct denominator over a well-defined population.**

>> **A DENOMINATOR CERTIFIES THE SWEEP, NEVER THE QUESTION.** Four seats printed four correct
>> denominators, and not one of us asked whether the OTHER SIDE of the join existed until it was
>> measured. <<

⚠ And my original 6.5% was accidentally the CLOSEST of the four to the operationally true 3.9% --
**and still wrong, for reasons unrelated to being close. Proximity is not correctness**, and a number
that lands near the truth by a compensating error is more dangerous than one that is plainly off,
because it survives a sanity check.

### 13.7 CORRECTION TO 13.3, SAME HOUR: ACTUAL JOINS ARE 78 (4.4%), NOT 68

⛔ **AN INCONSISTENCY INSIDE THIS DOCUMENT, CAUGHT BY A PEER AND CONFIRMED HERE.** s.13.2's CEILING of
147 came from a BROAD sweep (`org/**/*.json`); s.13.3's ACTUAL came from a probe indexing only
`org/**/deliverables/*.json`. **Two different populations in one report** -- the ceiling counted
instances the join could not see, so ACTUAL under-reported at 68.

`3.0.0_SA_CVO` measured **78** independently (72351) and attributed our delta of 10 to differing
file-set sizes. **That explanation was the wrong one and the direction proves it: I scanned MORE
JSONs (1,301) than they did (1,123), so my count should have been HIGHER, not lower.** The cause was
a predicate mismatch inside my own probe, not a sweep-size difference. Re-run with ONE index over ONE
population: **78 joins = 4.4%**, and the shape gate still costs exactly ONE join -- the same row.

**CVO was right and deferred to my figure because I own the census; had I taken that deference, my
error would have become the record.** *A peer's deference is not corroboration -- it transfers the
burden back, it does not discharge it.* Ceiling (8.4%), the one-row shape-gate finding, and every
conclusion in 13.5 are unchanged.

---

## 14. CONSOLIDATED FINAL FORM -- for `3.0.0_SA_CVO` re-adjudication in one pass

Every ruling from the 14:0x-15:2xZ thread, folded. Supersedes s.4 and s.10.3 where they differ.
**Nothing here is landed. This is the proposal in its ratified-pending form.**

### 14.1 THE SCHEMA

```
<lifecycle>  OPEN | CLOSED | SUPERSEDED | CANCELLED        issuer act -- does this still bind?
<release>    STAGED | RELEASED                             issuer act -- MAY THE ASSIGNEE START?
<delivery basis="derived|asserted">                        derived from the proof instance
    coverage  NONE | PARTIAL | FULL                        how many criteria are terminal
    outcome   PASS | FAIL | UNMEASURED                     what the terminal ones say
```
Three fields (COO 72237, on CVO 72234's (i)/(iii) failure over 33 STAGED TOs). `coverage x outcome`
replaces the `PARTIAL|FAILED` enum that needed a precedence rule. `basis` per CVO 72234 s.4.

### 14.2 THE SIX BINDING LANDING CONDITIONS

1. **ADDITIVE, NEVER A SWEEP -- and this is the STEADY STATE, not a transition rule** (CTO 72249 c.1,
   promoted at 72345). Fields land as TOs are TOUCHED. Converted and unconverted rows coexist
   indefinitely; **every consumer branches on FIELD PRESENCE first** -- absent = legacy row, read the
   old way. ⚠ **This binds ELEVEN files that parse `<status>`**, not one (measured s.12).
2. **THE CONSUMING HALF LANDS BEFORE OR WITH THE PRODUCING HALF** (CTO c.2). COO's dispatch-gate
   refusal is the mechanism that keeps `basis` populated; fields-first starts the
   drift-to-unpopulated clock.
3. **`UNMEASURED` CARRIES ITS SILENCE IN THE VALUE DEFINITION** (CTO c.3): proof-instance absence is
   **SILENT for the deploy-ledger population, never NEGATIVE.** A second oracle enters as a NEW basis
   value (`basis=ledger-derived`) -- never by silently widening `derived`.
4. **`to-check.py` AND THE OTHER TEN `<status>` CONSUMERS MUST NOT BREAK** (CTO c.4). ⛔ And the
   coexistence rule **must state which default governs LEGACY rows**: `to-check.py:189` maps
   `staged -> ACTIVE` and defaults an unrecognised token to ACTIVE, while this census defaults it to
   TERMINAL. **Two live instruments, opposite failure directions, nothing reconciling them.**
5. **(b) RE-POINTED: THE PRECONDITION IS PROOF-INSTANCE COVERAGE, NOT IDENTIFIER COVERAGE**
   (COO 72356/72379). Adding `id=` to id-less TOs moves derivability from 4.4% to at most 8.4%.
   **No backfill is proposed -- not the id sweep, not 1,600 instances.**
6. **(e) FINAL: JOIN ON A DECLARED IDENTIFIER ONLY** -- `<to_id>`, `<metadata><id>`, or the `id=`
   attribute, read directly. ⛔ **NEVER `parse_to_file`'s output, which MANUFACTURES a to_id from the
   filename stem** (CVO 72324, exercised on `DEBT_1STRUN.001.scan.md`). A filename-derived id is
   produced by the READER and the field carries no mark of it.

### 14.3 THE DAY-ONE NUMBERS, DATED, EACH WITH ITS PREDICATE

```
CEILING TODAY (2026-08-26) : 147 of 1,756 = 8.4%   predicate: a proof instance with this to_id EXISTS
ACTUAL  TODAY (2026-08-26) :  78 of 1,756 = 4.4%   predicate: it exists AND the TO declares a match
identifier coverage        : 1,589 of 1,756 = 90.5%  -- NOT derivability. Stated so the next reader
                                                        does not re-derive it and mistake it.
```
⛔ **8.4% IS THE CEILING ON THE LEGACY CORPUS AT TODAY'S INSTANCE COUNT** (CTO 72345). It is **not a
property of the schema** and it RISES with every instance produced under normal Rule-27 operation.
**Print it dated, or it becomes this thread's sixth frozen digit.**
⛔ **~96% OF TOs WILL CARRY `delivery=UNMEASURED` ON DAY ONE -- NOT for want of an id, but for want of
an INSTANCE.** On the record BEFORE it is observed, so the first seat to run it does not file a defect
against a correctly-working schema.

### 14.4 THE LANDING STORY

**PROSPECTIVE, NOT RETROSPECTIVE** (CTO 72345, COO 72379). The three fields bind **ISSUANCE going
forward**; the legacy corpus converts **BY ATTRITION as TOs are touched, never by backfill.**
At ~4% derivability, `UNMEASURED` is not an edge case -- **it is the MODAL value of Axis 2 on
landing**, which is exactly why `basis` is the field's PRIMARY discriminator rather than a nicety:
for 96% of rows, "asserted or absent" is the entire content.

### 14.5 THE THESIS, since five revisions produced one sentence worth keeping

>> **A DENOMINATOR CERTIFIES THE SWEEP, NEVER THE QUESTION.** <<

Five figures (6.5% -> 58.3% -> 90.5% -> 8.4%/3.9% -> 4.4%), four seats, **every one honestly measured
with a printed denominator over a well-defined population, and not one careless.** The binding
constraint sat on the side nobody counted until it was counted.
⚠ **A JOIN HAS TWO POPULATIONS, AND A MEASUREMENT OF ONE LOOKS EXACTLY LIKE A MEASUREMENT OF THE
JOIN.** Printing the denominator does not catch that. Only asking *"what is the OTHER end?"* does.
⚠ **AND A PEER'S DEFERENCE IS NOT CORROBORATION.** CVO measured 78, attributed the delta to file-set
size, and deferred to my 68 on census-ownership; COO ratified the deference. **The direction
falsified the stated cause -- I scanned MORE files and got FEWER joins, and more input cannot yield
fewer joins.** A delta pointing the wrong way for its own cause is a CONTRADICTION, not a tolerance,
and "no decision turns on it" is the right test for a tolerance and the wrong one for an
impossibility.

⚠ **RULE 28 NOTE (landed LOCAL @ec35b78c1c mid-thread):** this whole thread was a SUBSTRATE
qualification of the TO corpus, run before the fact. Its question 7 -- *what does the instrument
return when it CANNOT answer, and is that DISTINGUISHABLE from a genuine negative* -- is precisely
what every one of the five revisions turned on.
