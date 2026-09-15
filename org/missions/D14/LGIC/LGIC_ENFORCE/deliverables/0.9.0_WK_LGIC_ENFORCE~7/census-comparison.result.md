# Result -- LGIC_ENFORCE.TO-EN-s-2 (census mode, the comparison)

**Worker:** `0.9.0_WK_LGIC_ENFORCE~7` | **Branch:** `wk-lgic-enforce-1-7-s2`, base CLOUD @`652d3a2204` | **Cell:** `EN-s-2`

## What landed

| path | commit |
|---|---|
| `org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/NAMING_CENSUS_COMPARISON.md` | `e6ffd3a2a0` |
| `org/missions/D14/LGIC/LGIC_ENFORCE/surprise-channel/investigations/INVESTIGATION_v1.md`, row `LGIC_ENFORCE-W7-S4` appended | `e6ffd3a2a0` |
| this file, the proof-of-spec instance beside it, and the `<status>` flip | the commit that follows `e6ffd3a2a0` |

## The comparison, in figures

The census report (`NAMING_CENSUS_REPORT.md` @`f64b6f35cb`) stopped on its first RAISE. It judged 3 of 1805 nameable
live names and 0 of 1869 repo names, all 3 of type API_GW (row `LGIC_ENFORCE-W7-S1`).

| against | names graded by both | agree | hand product's own size |
|---|---|---|---|
| N2 (`GRADING_RULE.md` @`51b0952d71`) | 1 (`opal-portal-data-proxy-api`) | 1 | 43 worked cases |
| N6 (`n6-grader-a.tsv` @`388b07f486`) | 2 (`inf-otp-relay-api`, `opal-session-analytics-api`) | 2 | 88 rows |
| IV7 (`TENSION_RANKING.md` @`3497a41c31`) | 0 (it grades no name) | -- | 10 ranked surfaces |

In each agreeing pair, both the verdict and the canonical form match. There are 0 disagreements. The stop name,
`sentiment-query-api`, is in no hand product. These denominators are printed as they are, and no name was graded to
fill one. Row `LGIC_ENFORCE-W7-S4` states what the order says beside what the census holds.

## Criteria, verbatim

`cd C:/Users/AndrewBerman/Desktop/ajb_workspace/.worktrees/wk-lgic-enforce-1-7-s2 && timeout 120 python org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/2.0.0_SA_COO~G/fixed_inputs/check_en.py s2-three`
```
COMPARED AGAINST: {'N2': 1, 'N6': 2, 'IV7': 10}
VERDICT: PASS-THREE-COMPARED
(rc=0)
```
**S2-AC1:** PASS by output.

`... check_en.py s2-named`
```
DISAGREEMENTS: 0  MALFORMED: 0
VERDICT: PASS-DISAGREEMENTS-NAMED
(rc=0)
```
**S2-AC2:** PASS by output.

**S2-J1** is a judgment criterion. It is RECORDED for 3.0.0_SA_CVO at L9, with no verdict given here.

## Controls

A scratch script (`.scratch/s2_control.py`, not committed) ran the unmodified checker against mutated copies of the
comparison. Four arms were built to fail. IV7's denominator set to 0 and N6 removed each gave FAIL-COMPARISON (rc 1). A
disagreement with no hand_verdict and the disagreements key removed each gave FAIL-DISAGREEMENTS (rc 1). One positive
arm, a well-formed disagreement, gave PASS-DISAGREEMENTS-NAMED (rc 0). Three runs on the committed bytes gave identical
output.

## What is not claimed

- Nothing about the 1802 live names or the 1869 repo names the census did not judge.
- No verdict on IV7's ranks. IV7 ranks by cost and gives no verdict for any name.
- No verdict on S2-J1.
- This comparison needs re-running once the census runs to completion. That needs the registry rows owed under row
  `LGIC_ENFORCE-W7-S1`, and `TO-EN-s-1` stays pending until then.
