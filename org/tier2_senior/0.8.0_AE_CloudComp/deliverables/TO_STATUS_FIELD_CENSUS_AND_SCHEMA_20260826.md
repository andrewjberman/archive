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
