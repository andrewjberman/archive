# EN-s-2 round 2 -- the result record

**TO:** `LGIC_ENFORCE.TO-EN-s-2-r2` (`org/missions/D14/LGIC/LGIC_ENFORCE/task-orders/LGIC_ENFORCE.TO-EN-s-2-r2.census-comparison.md`@`4f9a9eb3f3`)
**Worker:** `0.9.0_WK_LGIC_ENFORCE~2` | **Worktree:** `C:/Users/AndrewBerman/Desktop/ajb_workspace/.worktrees/wk-lgic-enforce-2e-2b`
**Branch:** `wk-lgic-enforce-2e-2b`, cut from CLOUD @`2a2b853f79` | **Artifact commit:** `171a18b377` (LOCAL)
**Order status:** STAYS `pending`. `S2R-AC3` is FAIL by output.

## 1. The four criteria, as measured

Every invocation ran from the worktree root under `timeout 120`, verbatim from the order with `<WS>` expanded.

| criterion | verdict | deciding line | rc |
|---|---|---|---|
| `S2R-AC1` | **PASS-by-output** | `COMPARED AGAINST: {'N2': 1, 'N6': 2, 'IV7': 10}` / `VERDICT: PASS-THREE-COMPARED` | 0 |
| `S2R-AC2` | **PASS-by-output** | `DISAGREEMENTS: 0  MALFORMED: 0` / `VERDICT: PASS-DISAGREEMENTS-NAMED` | 0 |
| `S2R-AC3` | **FAIL** | `CENSUS STOPPED: True  LIVE 3 of 1821 judged  REPO 0 of 1878 judged  COMPARISON RECORD PARSES: True` / `VERDICT: FAIL-PARTIAL-POPULATION` | 1 |
| `S2R-J1` | RECORDED, no verdict | judgment; `3.0.0_SA_CVO` grades it at L9 | -- |

`S2R-AC3` FAILs **by measurement**, which is the outcome the order anticipates in terms: *"If the census stopped on
a RAISE, S2R-AC3 FAILs by measurement and the order stays pending (decomposition v2 s.0b). Compare what the report
judged anyway, and say what it did not reach."* The comparison was made on what the report judged, and section 5 of
`NAMING_CENSUS_COMPARISON.md` states what it did not reach, with denominators. **The `<status>` was NOT flipped.**

Nothing in this cell can move `S2R-AC3`. `s2r_real_population` (`check_en_r2.py`:701-708 @`5e908a4929`) reads the
REPORT's `stopped` key and its judged/total denominators; the only term it reads from this cell's artifact is
whether the comparison's fenced json parses, and that term reads `True`. The stop clears when the registry gains a
row resolving `token:sentiment` -- `EN-r-2`'s surface, outside this order's `<paths>`.

## 2. What the comparison found

Matched on `(name, type)`, compared on verdict AND canonical form, byte for byte:

| against | denominator (graded by both) | agree | hand population |
|---|---|---|---|
| N2 `GRADING_RULE.md`@`fd6ce8c330` | 1 | 1 | 45 worked cases over 26 types |
| N6 `n6-grader-a.tsv`@`388b07f486` | 2 | 2 | 88 rows over 33 types |
| IV7 `TENSION_RANKING.md`@`3497a41c31` | 0 names (10 ranked surfaces) | -- | no per-name verdict |

**0 disagreements over 3 compared pairs.** `opal-portal-data-proxy-api` CONFORMANT on both sides (N2);
`inf-otp-relay-api` OUT-OF-PATTERN `{system}-inf-otp-relay-api` on both sides and `opal-session-analytics-api`
CONFORMANT on both sides (N6). Grader B's answer file is byte-identical to grader A's, so the N6 agreements hold
against both graders.

**What the census did not reach:** 1818 of 1821 nameable live names unjudged; the repo plane never ran at all
(0 of 1878); 24 of the 25 graded types carry no judged row; 44 of N2's 45 cases and 86 of N6's 88 rows have no
census verdict to sit beside; the stopped name `sentiment-query-api` is in none of the three hand products.

**One hand product moved since round 1** and the record says so: N2 went 43 -> 45 worked cases when
`GRADING_RULE.md` was re-cut to NAMING_SCHEMA v1.9. Measured by diffing the two section-9 json blocks
(`51b0952d71` against `fd6ce8c330`): 2 cases added (`LAMBDA mdpf-lambda-lambda`, `LAMBDA orion-orion-lambda-lambda`),
0 removed, 1 verdict changed (`SECURITY_GROUP default` RAISE -> NOT-GRADED), 1 canonical form changed
(`LOAD_BALANCER opal-gateway` `opal-gateway-lb` -> `gateway-lb`). None of the four touches the one name N2 shares
with the census. N6 and IV7 are at the same commits round 1 read.

## 3. Controls

- **Mutant, three arms**, each running the shipped limb unchanged against a mutated input in `.scratch/mutant/`, with
  the checkers loaded as modules and only their in-memory path constants redirected (no fixed input edited --
  `git status --porcelain` over `fixed_inputs/` read clean after the run):
  - IV7 dropped from `against` -> `VERDICT: FAIL-COMPARISON`, rc=1.
  - one disagreement entry missing `hand_verdict` -> `DISAGREEMENTS: 1  MALFORMED: 1`, `VERDICT: FAIL-DISAGREEMENTS`, rc=1.
  - **the decisive arm:** `S2R-AC3`'s limb against a copy of THIS report with `stopped` removed and
    judged_live/judged_repo raised to live_nameable/repo, against the SAME comparison file ->
    `CENSUS STOPPED: False  LIVE 1821 of 1821 judged  REPO 1878 of 1878 judged  COMPARISON RECORD PARSES: True`,
    `VERDICT: PASS-COMPARED-ON-THE-WHOLE-POPULATION`, rc=0. So the real FAIL is carried by the report's population
    and by nothing this cell wrote.
  - positive controls on the same redirected modules with the real files: PASS, PASS, FAIL respectively.
- **Determinism:** all three invocations re-run; 3 of 3 verdict lines identical.
- **Negative arm at base:** all three were also run BEFORE any edit, at `2a2b853f79`, against round 1's file --
  `S2R-AC1` and `S2R-AC2` already printed PASS there, with the same evidence lines. Filed as row
  `LGIC_ENFORCE-W2-S11`.

## 4. Rows filed

- `LGIC_ENFORCE-W2-S11` -- OBSERVATION, INERT, UNDER_INVESTIGATION. `S2R-AC1` and `S2R-AC2` both print PASS on the
  round-1 comparison file at this cell's base, before the cell rewrites anything, so neither discriminates round 2's
  rewrite; the round-2 content reaches the record only through `S2R-J1`. Filed for form, not significance: the order
  labels both limbs "round 1's ..., unchanged", and fixed inputs are read-only by BOUNDS.

## 5. Proof

`org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~2/LGIC_ENFORCE.TO-EN-s-2-r2.census-comparison.proof_of_spec.json`
-- `python .tools/proof-of-spec-check.py <instance> S2R-AC1,S2R-AC2,S2R-AC3,S2R-J1` returns **VALID (rc=0)**:
acceptance rows 4, violations 0, artifact-resolution 2 of 2 at pin and 2 of 2 CONTENT-resolved, surprises-frame 1
entry resolving to `LGIC_ENFORCE-W2-S11`, invocation-alignment 3 of 3 comparable rows matching. The first run was
INVALID (rc=1, 6 violations) and is recorded in the instance's own `compiler_tools` rather than hidden.

**A VALID instance is not a met order.** `S2R-AC3` is FAIL, so `LGIC_ENFORCE.TO-EN-s-2-r2` stays `pending` and this
record is the final report on it.
