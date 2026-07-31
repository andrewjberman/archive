# WS-C7 SPECIMEN 4 -- AN ADDRESS SPACE BLIND TO A SIBLING SERVICE, WITH A PAGINATION FAULT NESTED INSIDE IT

**Captured:** 2026-07-31 by `0.7.0_AE_CloudOps~Z` | **Gate:** `1.0.0_SA_CTO~Z` | **Verify:** `3.0.0_SA_CVO~Z`
**CANONICAL SPECIMEN #2** from `NFRA_DEBTLOOPS_ANDREW_VOICE_MEMO_20260729.md:145` -- *"`aws events
list-rules` -> structurally blind to EventBridge Scheduler; 11 live schedules absent."*
**Basis: EXERCISED.** Re-derived live on account `313476888478`, 2026-07-31 ~17:19Z.
**Status:** LIVE. Not fixed; it is a property of the AWS API surface, not of our code.
**SUITE PROGRESS: 1 of 9** canonical specimens written (this one). **Remaining 8 named at
`NFRA_DEBTLOOPS_ANDREW_VOICE_MEMO_20260729.md:140-161`** -- enumerated in
`WSC7_SUITE_ENUMERATION_AND_COUNT_FINDING.md` section 1. *Printed per L-16: a bare green is not a
count, and a suite with no denominator is the defect this suite exists to demonstrate.*

> **WRITTEN WHILE TWO RULINGS WERE OPEN; BOTH ARE NOW CLOSED.** It was chosen because it was **in
> scope under BOTH readings of the suite fork** -- under (a) a member of the canonical nine, under
> (b) available to choose -- so it cost nothing under either answer. **CTO~Z ruled (a) at
> `173205Z`: this IS canonical #2.**
>
> **The classification line was DELIBERATELY ABSENT** -- `Class 1 / Class 2` resolved nowhere in the
> estate, and inventing it to complete my own acceptance criterion is the invented-oracle failure.
> **CTO~Z repaired the PRD clause at `@05adba68b` and the line has now LANDED (section
> "CLASSIFICATION" below).** *Recorded because the sequence is the point: the hole stayed open for
> ~22 minutes and was filled by a definition, not by me deciding what the term probably meant.*

---

## THESIS

> **A census whose address space is one service is silently missing every sibling service that does
> the same job.** `aws events list-rules` cannot see EventBridge Scheduler. Not "returns them
> unflagged" -- **cannot see them at all**, because they are a different API.

---

## OBSERVATION -- measured, both limbs

```
aws events list-rules      --query 'Rules[].Name'      | count  ->  142   EventBridge RULES
aws scheduler list-schedules --query 'Schedules[].Name' | count ->   12   Scheduler SCHEDULES
                                                    true total ->  154
```

**A trigger census built on `list-rules` alone declares an address space of 142 and has a recall of
142 of 154. The 12 are not late, not filtered, not denied -- they are OUTSIDE THE ADDRESS SPACE THE
QUESTION WAS ASKED IN.**

*(The memo recorded 11 on 2026-07-29; there are 12 today. **The estate grew and the blind spot grew
with it** -- which is the property that makes an unmeasured denominator worse over time, not stable.)*

---

## THE NESTED SECOND FAILURE -- AND I COMMITTED IT WHILE WRITING THIS

**My first measurement of the rule count was 100. The true count is 142.**

```
aws events list-rules --no-paginate --query 'Rules[].Name' | count  ->  100    <- WRONG
aws events list-rules              --query 'Rules[].Name' | count  ->  142    <- TRUE
```

**`--no-paginate` DISABLES auto-pagination -- it returns the FIRST PAGE ONLY.** The page size is
100. **I read a page size as a total.**

> **CLAUDE.md CARRIES THIS EXACT TRAP, ADDED TODAY:** *"`--query 'length(...)'` ON ANY PAGINATED
> `list-*` CALL RETURNS THE PAGE COUNT, NOT THE TOTAL... measured 2026-07-31: `aws events
> list-rules --query 'length(Rules)'` reported 100 when the truth was 142."*
> **I READ THAT RULE THIS MORNING AND WALKED INTO IT SEVEN HOURS LATER**, on the same command, in
> the artifact whose subject is unmeasured denominators.

**Two independent recall failures on one command, nested:**

| # | failure | missing | detectable how |
|---|---|---|---|
| 1 | **structural** -- wrong service entirely | 12 schedules | only by knowing Scheduler exists |
| 2 | **pagination** -- page size read as total | 42 rules | only by comparing against a paginated count |

**Neither is visible from the other.** A census that fixed the pagination bug would still miss 12; a
census that queried both services with `--no-paginate` would still miss 42. **Fixing one produces a
number that looks more correct and is still wrong.**

---

## FAILURE DIRECTION

| limb | value | note |
|---|---|---|
| `self` | **under_report** | both failures under-count; neither can over-count |
| `basis` | **exercised** | |
| `known_negative` | **`--no-paginate` -> 100 against a true 142** | a case that DID come out differently, run by me, by accident |

**The known-negative here is not constructed -- it is my own wrong measurement**, which is the
strongest form available: I did not have to imagine how the instrument could fail.

---

## CLASSIFICATION -- against the REPAIRED acceptance criterion

**Criterion** (`NFRA_VELOCITY_CORE_PRD.md` @`05adba68b`, replacing the undefined `Class 1 / Class 2`):
*"each specimen re-derives as **a true measurement of the wrong proposition** that the contract
surfaces."* **IN CLASS** = the output was CORRECT for the question it actually answered, and that
question was not the one asked. **OUT OF CLASS** = merely a wrong number.

| limb | the question actually answered | the question asked | verdict |
|---|---|---|---|
| structural | *"how many EventBridge **Rules** exist?"* -> **142, exactly right** | *"how many **triggers** exist?"* | **IN CLASS** |
| pagination | *"how many rules are on **page one**?"* -> **100, exactly right** | *"how many rules exist?"* | **IN CLASS** |

> **THE PAGINATION LIMB IS THE SHARPER TEST OF THE CRITERION, BECAUSE IT LOOKS LIKE A WRONG NUMBER
> AND IS NOT.** `100` is not an error, a truncation, or an approximation -- **it is the exact and
> complete answer to a question I did not ask and did not know I was asking.** Under the old
> undefined clause I could have graded this either way; under the repaired one it is decidable, and
> it decides IN. **That is the criterion doing work, which is the property the old one lacked.**

### EVIDENCE ON CTO~Z's PROPOSED TWO-WAY SPLIT -- **found by building, not asserted**

CTO~Z observed a possible split -- *two-states-collapse-to-one-output* (1, 5, 6, 7) vs
*the-check-asks-a-different-question* (2, 3, 4, 8, 9) -- and **declined to mint it**, recording it as
its own inference and asking that it be found by building the nine. **First data point, and it does
not go the easy way:**

- The **structural** limb is cleanly *asks-a-different-question*, as CTO placed canonical #2.
- **The pagination limb satisfies BOTH limbs of the split.** It asks a different question (page vs
  total) **AND** it collapses two states to one output: *"an estate with exactly 100 rules"* and
  *"page one of an estate with 142"* emit the byte-identical `100`.

> **SO THE SPLIT IS NOT A PARTITION -- at least, membership is not exclusive.** One specimen sits in
> both cells. **This does NOT refute the split as a lens; it refutes it as a taxonomy that assigns
> each specimen one home**, which is the form a pass condition would need. **Reported as one data
> point out of nine. I am not ruling on the split from a single specimen** -- that would be the same
> error CTO declined to commit, made by me with a smaller sample.
>
> **METHOD DECISION, stated now so it is not retrofitted:** I will record split-membership evidence
> on **every** remaining specimen as I build it, and rule on the split only at 9 of 9 -- **including
> if the evidence says there is no split.**

---

## HOW IT WOULD READ UNDER THE BOUNDARY CONTRACT (schema v3)

```yaml
boundary_declaration:
  tool: <any EventBridge trigger census built on list-rules>
  address_space:
    kind: enumerable
    denominator_grain: artifact
    row_grain: artifact
    chains:
      - name: eventbridge_rules
        denominator_chain: [{stage: rules_listed, count: 142}]
    denominator_source: independent_precount
    description: "EventBridge RULES only -- see silent_modes"
  traversal_residue:
    reportable: structurally_invisible          # Scheduler is a different API
    channel: none
    per_item_residue: none
    silent_modes:
      - "EventBridge Scheduler schedules are NOT in this address space (12 live at capture)"
      - "--no-paginate returns page 1 only; page size 100 reads as a total"
  failure_direction:
    self: under_report
    basis: exercised
    known_negative: "--no-paginate yielded 100 against a true 142"
```

> **THE CONTRACT SURFACES IT, AND THIS IS THE PART THAT MATTERS:** `reportable:
> structurally_invisible` + the two `silent_modes` entries turn *"142 rules"* into *"142 rules, and
> here is what that number cannot contain."* **The census does not become correct. It becomes
> HONEST, and its consumer can compute what it is missing** -- which is the whole claim WS-C7 makes.
>
> **Note it costs the tool nothing to declare:** the author of a list-rules census does not have to
> support Scheduler. They have to SAY they do not.

---

## RE-DERIVATION (live today; requires estate read access)

```bash
aws events list-rules        --query 'Rules[].Name'      --output text | tr '\t' '\n' | grep -c .
aws scheduler list-schedules --query 'Schedules[].Name'  --output text | tr '\t' '\n' | grep -c .
# KNOWN-NEGATIVE, run it and watch it lie:
aws events list-rules --no-paginate --query 'Rules[].Name' --output text | tr '\t' '\n' | grep -c .
```
**Do NOT use `--query 'length(Rules)'`** -- it applies per page and reports the page count.
**Counting the MATERIALISED auto-paginated list is the control.**

---

## ROUTED, NOT BUILT

1. **CLOSED.** `Class 1 / Class 2` was absent by design; CTO~Z repaired the clause `@05adba68b` and
   the classification landed above. **Flagged rather than invented, and the flag was answered.**
2. **CLOSED.** The (a)/(b) fork was ruled (a) at `173205Z`: **this is canonical #2, 1 of 9.**
2a. **OPEN, and it is the one I am carrying:** whether CTO~Z's two-way split survives the full nine.
   **First evidence above is against it being a partition.** Ruling deferred to 9 of 9 by method,
   not by hesitation.
3. **The estate may hold other sibling-service blind spots** (the same shape wherever two AWS
   services do one job). **Not enumerated here; that is a census, not a specimen.**

**CONTROL 2 CHECK:** nothing here types where an assertion sits. Not rail vocabulary.
