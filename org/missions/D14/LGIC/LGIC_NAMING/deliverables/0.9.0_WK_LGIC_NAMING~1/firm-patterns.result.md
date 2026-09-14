# LGIC_NAMING.TO-LN-f-1 -- result

**Worker:** `0.9.0_WK_LGIC_NAMING~1`. **Branch:** `wk-lgic-naming-1-1`. **Base:** `3d671ff59c`.

## What landed

`org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/n4-firm-patterns.md`: one pattern per firm, over canonical
IAM role names, written from PRD S3-S5.

| firm | pattern | attributed |
|---|---|---|
| 49financial | `*-49f-*-role` | 24 |
| inflection | `*-inf-*-role` | 31 |
| cottonwood | `*-cot-*-role` | 12 |
| demo | `*-demo-*-role` | 1 |

Denominators: 240 live IAM_ROLE, 69 with a firm alias token, 68 attributed, 1 excluded.
Verdicts among the 68: 2 CONFORMANT, 7 ALIAS, 59 OUT-OF-PATTERN; 48 canonical forms carry `{system}`.

## Criteria

| id | status | deciding line |
|---|---|---|
| F1-AC1 | PASS | `VERDICT: PASS-ONE-EACH` (4 of 4 keys) |
| F1-AC2 | PASS | `ATTRIBUTED CANONICAL FORMS: 68  CAUGHT BY OWN FIRM'S PATTERN: 68` |
| F1-AC3 | PASS | `CROSS-FIRM CATCHES: 0` |
| F1-AC4 | PASS | `... 69 of 240 roles  ATTRIBUTED OR EXCLUDED WITH A REASON: 69  MISSING: []` |
| F1-J1 | RECORDED (judgment) | for `3.0.0_SA_CVO` at L9 |

## Controls

- **Mutant:** the real checker was run on five mutated copies in a scratch tree, and each one turned exactly its
  criterion FAIL. A widened pattern crossed 37 times; a LONG-form pattern missed 24; a dropped attribution and an
  emptied reason each left their name uncovered; a missing pattern failed f1-one. The restored copy passed 4 of 4.
- **Determinism:** two runs gave identical output, 12 lines of 12.
- **Second method for the grading:** a scratch script that encodes R1-R6 agrees with the hand grading on 69 of 69 names.

## Row

- `LGIC_NAMING-W1-S5` (OBSERVATION, INERT): `wp5-49f-feeder-scheduler-role` RAISEs at R1.f, so it can be neither
  attributed with a canonical form nor called no firm's principal. It is filed under `excluded`, and its reason says so.

## Not claimed

- The patterns are sound over canonical names only. The no-cross property comes from R4, not from the glob.
- Over today's live names the patterns reach 12 of the 68 attributed roles.
- No role's permissions were read. No IAM condition was applied, and nothing live moved.
