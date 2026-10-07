# L8 drain end -- IRPT_BCKEND rounds 70 and 71, workstream ~P

**Issuer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-07 ~19:4xZ | **For:** `3.0.0_SA_CVO` (L8 compile) | **Risk:** WORLD (IB-pr-351,
352, 354; each releases under a pair) and LOCAL (IB-pr-353)

**Cut from:**
- **Round 70:** the CTO's IRPT_CUSTDY round-6 ADDENDUM 1 @c3addc6f25, ruling item 2, cut on msg 917. These are breaks 1, 2 and 4 of
  IRPT_CUSTDY-S14.
- **Round 71:** CTO ruling msg 945 on row W152-S1 (TCKT_VNEXT X-1).

**Judgment criteria:** 0 in all four orders. Every mechanical criterion was re-run by the issuer on the shared tree after the drain.

## Round 70 -- hop 5 of the custody report

| order | slot | drain | result |
|---|---|---|---|
| IB-pr-351 custody write path | ~160 | @32f9796a4c | `reports/custody_write.py` `persist_custody_report` persists a CUSTODY_REPORT through `ReportRepository.persist`, with no second repository. It refuses an owner without a server-issued selection, a document without `as_of_date` (2024 or later), and an empty provenance. It round-trips through `export/retained_export.resolve`. IB70-1-AC1 PASS at HEAD (reports suite 120 passed; custody submit 13 passed); a mutant (the as_of_date check removed) fails 8. Proof VALID. |
| IB-pr-352 accept reads the business date by kind | ~161 | @913d3b9d8c | `export/submit_async.accept` reads `as_of_date` for a CUSTODY_REPORT through `narrative_submit.custody_report_as_of` (imported, not copied), and `dates.actual_end` for the others. A custody document without `as_of_date` is refused by name (`NarrativeSubmitRefused`), never a KeyError. IB70-2-AC1 PASS at HEAD (16 passed). Proof VALID. |
| IB-pr-353 print page mounts the custody template | ~162 | row and proof drained @4b15646e27 | SUPERSEDED by IB-pr-356 (round 72). Its worker stopped on its own refusal clause, row W162-S1: the bundle freezes only `custody_report_ref`, and no route reads a retained custody report. CTO ruling msg 973 (option (a)): a scoped read route (IB-pr-355) and the page half (IB-pr-356). |

## Round 71 -- the on-behalf upload door (TCKT_VNEXT X-1)

| order | slot | drain | result |
|---|---|---|---|
| IB-pr-354 InteractiveAccess carries allowedFirmIds | ~163 | @ff2ccead5b | `_scope/interactive_access.py`: `current()` carries `allowedFirmIds` for a verified internal subject from an injected profile reader (the existing `CanonicalProfileReaders.get_user` shape; no new table client). `ALL`, an absent value or an unreadable value yields no field. `prospect_owner` never stores the field. IB71-1-AC1 PASS at HEAD (28 passed, 7 subtests). Proof VALID. |

## Rows

| row | what it records |
|---|---|
| W162-S1 | BLOCKING, ruled by CTO msg 973; carried by round 72. |
| W163-S1 | OBSERVATION: no production constructor passes the profile reader yet, so the admit is inert in production. Ruled by the issuer: round 72 cell IB-pr-358 wires it on the analysis-input-upload path. |

## Issuer defects caught before any spawn (on the record)

1. **Slot collision.** Round 70 first took slots ~150 to ~152, which ~Y and ~M orders already held. It was re-slotted to ~160 to ~162
   (@6115baf2e7) before any spawn. Slot blocks are now agreed: ~Y 150-159, ~P 160-199, ~M 200-219.
2. **Risk class.** IB-pr-351 and 352 were first declared LOCAL; the L6 gate refused (infra/ floor) and they were re-declared WORLD.
3. **A timed-out commit.** A round-71 commit was killed by the issuer's own `timeout` after staging; it was unstaged and re-committed.
   No foreign path was staged.

## Still open

- **Releases:** IB-pr-351 and 352 release under a pair with the round-72 route (IB-pr-355). IB-pr-354 ships with ~Y's X-1 pair after
  IB-pr-358.
- **Push state:** LOCAL at the time of writing.
