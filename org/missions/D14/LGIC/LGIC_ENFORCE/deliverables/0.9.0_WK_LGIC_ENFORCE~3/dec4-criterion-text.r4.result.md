# EN-d-26 result -- DEC-4(ii) amended criterion text + the fence-disposition guard

`LGIC_ENFORCE.TO-EN-d-26-r4`, `0.9.0_WK_LGIC_ENFORCE~3`, worktree `wk-lgic-enforce-4-3`.

## Deliverables

- `DEC4_II_AMENDED.r4.md` -- the replacement DEC-4(ii) evidence-clause text, carrying all four of
  R-30's parts, written for `1.0.0_SA_CTO` to lift verbatim into `prd/LGIC_ENFORCE_PRD.md`. This
  worker does not edit the PRD.
- `fence_disposition_check.py` -- the stdlib-only, ASCII-only guard: `python <file> <claim.json>`
  refuses a `NOT_A_PRINCIPAL` row on a bucket absent from both trail declarations' bucket lists,
  printing the bucket and the reason and exiting non-zero; accepts one on a covered bucket that
  carries evidence, exiting zero. Coverage is read from the two trail declarations' own `local`
  bucket-list literals (`cloudtrail-organization-trail.tf`'s `local.org_trail_read_logged_buckets`,
  `item2e_served_write_trail.tf`'s `local.served_write_trail_buckets`), never a hand-typed list.

## Both directions, exercised by hand before grading (worker's own run, per the cell's step 3)

At this tree, the union of both trail declarations' bucket lists is 4: `opal-data-49financial`,
`opal-data-bd`, `opal-data-cot`, `opal-data-inf` (4 in the org trail's ReadOnly list, 3 in the
served-key write trail's WriteOnly list). `opal-data-demo` is a member of neither.

**Arm A -- planted `NOT_A_PRINCIPAL` on `opal-data-demo` (uncovered; must be REFUSED):**

```
$ python fence_disposition_check.py .scratch/planted_uncovered.json
DENOMINATOR: 4 covered bucket(s) (4 in the org trail's ReadOnly data-event selector, 3 in the
served-key write trail's WriteOnly data-event selector, union counted once)
REFUSED: role=demo-transform-runner-ec2-role bucket=opal-data-demo disposition=NOT_A_PRINCIPAL --
bucket opal-data-demo carries no live CloudTrail data-event selector (absent from both the org
trail's ReadOnly list and the served-key write trail's WriteOnly list); silence in a trail that
never covered the bucket is never evidence (R-30 parts 1 and 4)
RC=1
```

**Arm B -- planted `NOT_A_PRINCIPAL` on `opal-data-49financial` (covered, with evidence; must be
ACCEPTED):**

```
$ python fence_disposition_check.py .scratch/planted_covered.json
DENOMINATOR: 4 covered bucket(s) (4 in the org trail's ReadOnly data-event selector, 3 in the
served-key write trail's WriteOnly data-event selector, union counted once)
ACCEPTED: role=irpt-core-firm-49financial bucket=opal-data-49financial disposition=NOT_A_PRINCIPAL
-- bucket opal-data-49financial is covered by a live data-event selector and the row carries
evidence
RC=0
```

Both arms discriminate: Arm A refuses, Arm B accepts on the same run of the same tool -- a guard
that refused everything would fail Arm B, and one that accepted everything would fail Arm A.

**`--self-test` (own arms, in-process, both directions):**

```
$ python fence_disposition_check.py --self-test
DENOMINATOR: 4 covered bucket(s) (...)
ARM1 (uncovered, must refuse): REFUSED: role=planted-probe-role-uncovered bucket=opal-data-demo ...
ARM2 (covered, must accept): ACCEPTED: role=planted-probe-role-covered bucket=opal-data-49financial ...
  uncovered-bucket-claim-refused   PASS
  covered-bucket-claim-accepted    PASS
SELF-TEST: 2 of 2 PASSED
RC=0
```

## Criteria, run against the issuer's fixed checker (post-commit; see proof_of_spec for the pinned run)

- `D26R4-AC1` (`d26-text`): `VERDICT: PASS-D26-TEXT-AMENDED` -- all 4 clauses R-30 requires are
  present (refused-on-uncovered + data-event; iam + grant; not-judged; silence).
- `D26R4-AC2` (`d26-planted-refusal`): `VERDICT: PASS-D26-PLANTED-REFUSAL` -- "planted claim on
  opal-data-demo: rc=1 (must be non-zero)"; "planted claim on opal-data-49financial: rc=0 (must be
  zero)".
- `D26R4-AC3` (`fence_disposition_check.py --self-test`): `SELF-TEST: 2 of 2 PASSED`, matching
  `(?m)^SELF-TEST: ([0-9]+) of \1 `.
- `D26R4-AC4`: judgment, `3.0.0_SA_CVO` at L9. This worker records no verdict.
