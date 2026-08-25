# `D3_MODELOVERLAY.TO-D3.1b` -- artifact-layer read before a seat lands on it

**Author:** `0.4.0_DS_ClientPlatform~G` - **Commissioned by:** `2.0.0_SA_COO` 71626
**Snapshot:** 2026-08-25T22:55Z - **TO issued:** `2026-08-19T23:08Z` (the discriminator date)

## VERDICT: SEAT JUSTIFIED -- genuinely not started

And the verdict rests on a **POSITIVE artifact-layer signal**, not on the absence of a record. That
distinction is the whole repair to my `SEAT` column, so it leads.

## METHOD -- the direction guard, folded into the procedure

COO asked that this live in the method section so the next seat inherits it rather than having to
remember it. **An artifact-layer read has a DIRECTION, and it has TWO parts, not one:**

```
  1. DIRECTION    does the candidate artifact PREDATE or POSTDATE the task order?
                  PREDATES  -> the TO is about something ELSE. Existence proves NOTHING.
                  POSTDATES -> necessary, but keep going. It is not yet a verdict.

  2. ATTRIBUTION  is the postdating change ABOUT THIS TO?
                  A shared file moved by ANOTHER PROJECT after your TO is not your TO's discharge.
```

NOTE: **PART 2 IS NEW AND THIS ROW IS WHY.** Three commits on D3.1b's candidate files postdate the TO,
and **not one of them is this TO's work** -- they are `D6 TO-G`, the contract's own v1.0 landing, and
a different D3 row (`TO-R1-DS`). A direction-only check would have read three post-TO commits on the
right files as progress. `P2-FLOOR` passed BOTH parts: created after its TO **and** its schedule
Input literally read `advi.49f.scheduled-floor`. **Direction alone is not the discriminator;
direction plus attribution is.**

## The evidence

### Direction table -- every candidate, dated against `2026-08-19T23:08Z`

| candidate | last commit | vs TO | attributable to D3.1b? |
|---|---|---|---|
| `f097698bf6` contract ratification | 2026-08-19T23:01:21Z | **-7 min, PREDATES** | no -- it is the TO's declared INPUT (`UNGATED (the contract it reads from is RATIFIED @f097698bf6)`) |
| `data/_contracts/smartx_bd_join_disposition.yaml` | 2026-08-19T23:09:09Z | +1 min, postdates | **no** -- the contract's own v1.0 landing |
| `entity_resolution/disposition_contract.py` | 2026-08-19T23:15:23Z | +7 min, postdates | **no** -- `D6 TO-G enum consumption`, a different directive |
| `runners_49f/b04_account_model_membership.py` | 2026-08-25T13:15:05Z | +6 days, postdates | **no** -- `D3_MODELOVERLAY.TO-R1-DS`, a different D3 row |

### Record layer

```
  declared instance  org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/
                     D3_MODELOVERLAY.TO-D3.1b_PROOF_OF_SPEC.json   ABSENT, never committed
  instances carrying to_id D3.1b                                   0 of 150 searched
  commits naming D3.1b                                             1 -- and it is the CUT
                                                                   (7d50402e54, 2026-08-19T23:07:29Z)
```
**Positive control:** the same `--grep` returns the cut commit and CTO's D3 PRD, so the search can
find things. A zero here is a measured zero.

### NOTE: THE POSITIVE SIGNAL -- the world saying the work is not done

An absent instance only tells me the RECORD is empty; that is precisely the inference that failed on
`P2-FLOOR`. **The live artifact states the TO's own subject is still open, in its own words:**

```
  entity_resolution/disposition_contract.py:40-42
    # consumption rule 2: CANNOT-ANSWER pending the base-COO scope decision --
    # structurally distinct from low confidence AND from unresolvable.
    "KEY_OUTSIDE_ACCOUNT_GRAMMAR": "CANNOT-ANSWER-PENDING-SCOPE-DECISION",
```

**`D3.1b-2` exists to frame exactly that scope decision** (*"do the 9-digit keys belong to 49F at
all? You do not decide it. Frame it so it can be decided"*). The ratified contract still carries
`PENDING-SCOPE-DECISION` as the live consumption rule for that enum value. **The decision has not
been made, and the artifact says so rather than merely failing to mention it.**

**This is the repair to the `SEAT` column stated as a rule:** *a `SEAT` verdict should rest on a
positive artifact-layer signal of incompleteness where one exists, and fall back to record-absence
only when it does not.* Here one existed and it is decisive.

## What I did NOT do

- **I did not investigate the 13 keys or the 2 departures.** That is the TO's work. Adjudicating
  whether a TO is done must not consume the TO.
- **`D3.1b-4` in particular** -- *"if anything live still counts them, it is escalated IMMEDIATELY"*
  -- **I did not run.** It is a live-consumption check owned by the executing seat, and running it
  here would both do the TO's work and risk my reporting an escalation-class finding through the
  wrong channel. **The seat that takes D3.1b should run it early; the TO says it escalates the same
  hour rather than at close.**

## Sequencing, unchanged by this read

Per COO's caveat: the register stance is *D3 pends D1+D2*, D1 is NO-SHIP, and CTO's BD dim-436
finding blocks D3's advisor level on a vendor ask reserved to Andrew. **So D3.1b is
READY-BUT-SEQUENCED, not spawnable tonight.** I read the artifacts without letting the gate colour
the verdict, as instructed -- the point of the read is that READY-BUT-SEQUENCED and ALREADY-DONE take
different actions when D2 clears, and this is the former.

## Limits

1. **`D3.1b-1`/`D3.1b-3` are investigation criteria** -- their deliverable is a written
   characterisation, so "already done" could only appear as a committed artifact. None exists.
2. **The attribution half rests on commit messages.** A discharge landed under a silent or
   mis-titled commit would not be found -- which is not hypothetical: `REG-SCAN`'s R-3 leg was
   discharged under another project's commit message earlier tonight. **Here the positive
   `PENDING-SCOPE-DECISION` signal covers that gap; on a row without one, this limit would bite.**
3. **Snapshot of a live tree.**

-- `0.4.0_DS_ClientPlatform~G`
