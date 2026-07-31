# WS-C7 SPECIMEN 4 -- AN ADDRESS SPACE BLIND TO A SIBLING SERVICE, WITH A PAGINATION FAULT NESTED INSIDE IT

**Captured:** 2026-07-31 by `0.7.0_AE_CloudOps~Z` | **Gate:** `1.0.0_SA_CTO~Z` | **Verify:** `3.0.0_SA_CVO~Z`
**CANONICAL SPECIMEN #2** from `NFRA_DEBTLOOPS_ANDREW_VOICE_MEMO_20260729.md:145` -- *"`aws events
list-rules` -> structurally blind to EventBridge Scheduler; 11 live schedules absent."*
**Basis: EXERCISED.** Re-derived live on account `313476888478`, 2026-07-31 ~17:19Z.
**Status:** LIVE. Not fixed; it is a property of the AWS API surface, not of our code.

> **WHY THIS ONE, WHILE TWO RULINGS ARE OPEN:** it is **in scope under BOTH readings of the suite
> fork** -- under (a) it IS a member of the canonical nine; under (b) it is available to choose. **It
> costs nothing under either answer**, which is why it is the one I could write while blocked.
> **The `Class 1 / Class 2` classification line is DELIBERATELY ABSENT** -- that term resolves
> nowhere in the estate and inventing it to complete my own acceptance criterion is the invented-
> oracle failure. **The line goes in when the term is defined.**

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

1. **`Class 1 / Class 2` classification is ABSENT from this specimen by design.** The term resolves
   nowhere; the line lands when it is defined. **Flagged rather than invented.**
2. **Whether this specimen counts toward the suite depends on the (a)/(b) fork** -- it is safe under
   both, which is why it exists now.
3. **The estate may hold other sibling-service blind spots** (the same shape wherever two AWS
   services do one job). **Not enumerated here; that is a census, not a specimen.**

**CONTROL 2 CHECK:** nothing here types where an assertion sits. Not rail vocabulary.
