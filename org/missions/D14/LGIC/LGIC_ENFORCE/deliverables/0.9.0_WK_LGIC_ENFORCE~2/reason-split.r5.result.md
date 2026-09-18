# reason-split.r5.result -- LGIC_ENFORCE.TO-EN-g-30-r5 (EN-g-30), 0.9.0_WK_LGIC_ENFORCE~2

**Fixed at commit `bfb7abbe01`** (worktree `wk-lgic-enforce-5-2`, cut from round-5 issuance `2befae9891`).

## The defect

`NAMING_CENSUS_COMPARISON.r4.md`'s fenced json carried `"uncompared_reasons": {"NOT-GRADED-TYPE": 23,
"AWS_FIXED-EXCLUDED": 2, "CARDED": 11, "HAND-SPECIMEN-ABSENT": 11, "total": 42}` -- `23+2+11+11=47`, not
`42`. Section 3's own prose said `THREE distinct, individually-verified reasons` above a list of four.

## What this worker measured, independently

Re-counted all 42 rows of Section 3's own per-row table by their stated `reason` column, with a small
Python script parsing the table body (not the fence, not the order text, not the remediation row's
proposed numbers):

```
row count: 42
Counter({'NOT-GRADED-TYPE': 20, 'HAND-SPECIMEN-ABSENT': 10, 'CARDED': 10, 'AWS_FIXED-EXCLUDED': 2})
sum: 42
```

This is an independent measurement that happens to match the remediation row's proposed 20/2/10/10 --
corroborating, not inherited.

## What changed

1. **Coverage paragraph** (Section 1/2 boundary): the split is now printed beside the existing "42 are
   not" total: `NOT-GRADED-TYPE 20 + AWS_FIXED-EXCLUDED 2 + CARDED 10 + HAND-SPECIMEN-ABSENT 10 = 42`.
2. **Section 3's opening sentence**: `THREE` -> `FOUR` (0 occurrences of `THREE` remain in the document).
3. **Section 3's four bullet counts**: `23/2/11/11` -> `20/2/10/10` (each bullet's parenthetical row count
   now matches the table).
4. **The fenced json's `uncompared_reasons`**: `{23,2,11,11,total:42}` -> `{20,2,10,10,total:42}`.

No row's individually stated reason in the 42-row table changed; the table body and the `disagreements`
array are byte-identical to the pre-edit version (confirmed by diff: 8 insertions, 6 deletions, all four
edits above, one file).

## Acceptance

| id | invocation | expect | result |
|---|---|---|---|
| G30R5-AC1 | `check_en_r5.py g30-split` | `PASS-G30-REASON-SPLIT-RECONCILES-TO-ITS-OWN-TABLE` | PASS -- fence parts sum to 42, 0 keys disagree with the table |
| G30R5-AC2 | `check_en_r5.py g30-prose` | `PASS-G30-STALE-COUNT-WORD-REMOVED` | PASS -- 0 occurrences of `THREE` |
| G30R5-AC3 | judgment (3.0.0_SA_CVO at L9) | N/A | `UNVERIFIABLE-BY-INSTRUMENT`; evidence recorded: prose, bullets and fence now agree with each other and with an independent re-count |

Both mechanical checks re-run twice (pre- and post- a repeat pass) on the committed tree at `bfb7abbe01`:
identical PASS/PASS both times. `selftest-arms` on `check_en_r5.py`: 20 of 20 arms discriminating,
including `g30-split`, `g30-split-table`, `g30-split-notable` and `g30-prose`; `VERDICT:
PASS-ARMS-DISCRIMINATE`.

## Proof

`org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~2/LGIC_ENFORCE.TO-EN-g-30-r5.reason-split.proof_of_spec.json`
-- `python .tools/proof-of-spec-check.py <instance> G30R5-AC1,G30R5-AC2,G30R5-AC3 --governing-order
org/missions/D14/LGIC/LGIC_ENFORCE/task-orders/LGIC_ENFORCE.TO-EN-g-30-r5.reason-split.md` -> `VALID (rc=0)`.

## Surprises

None filed for this cell. This worker's independent re-count matched the remediation row's proposed
parse exactly, so there is no discrepancy to report -- the order requires a row only "if you get
something else."
