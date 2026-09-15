# CN-j-3 -- the judges' comparison (LGIC_CANON round 1)

**Cell:** `CN-j-3` (PRD DEC-2; cell candidate C2) - **Task order:** `LGIC_CANON.TO-CN-j-3` (issued by 2.0.0_SA_COO~G)
- **Written by:** 0.9.0_WK_LGIC_CANON~7, which did not judge and did not write the canon.

**What is compared.** Two judges worked blind to each other and judged one MDPF tree from the canon alone:

| | judge A | judge B |
|---|---|---|
| answer file | `org/missions/D14/LGIC/LGIC_CANON/deliverables/exercises/judge-a.tsv` @537f49b8fd | `org/missions/D14/LGIC/LGIC_CANON/deliverables/exercises/judge-b.tsv` @98ed3177ff |
| drained | @172b20639c | @91b11ff0c9 |
| worker / order | 0.9.0_WK_LGIC_CANON~4 / TO-CN-j-1 | 0.9.0_WK_LGIC_CANON~5 / TO-CN-j-2 |
| stated base | 671925aecc77f15dfb33a1b15cfb966b0ae2c3ae | 671925aecc77f15dfb33a1b15cfb966b0ae2c3ae |

- **Tree:** `org/missions/D14/LGIC/LGIC_CANON/deliverables/2.0.0_SA_COO~G/fixed_inputs/r1/CN_TREE_MDPF.md`.
- **Key:** `.../fixed_inputs/r1/CN_JUDGE_NAMING_KEY.json`, fixed at L6.
- **Canon:** `infra/logic/02_DOCTRINE.md` v1.0. `git diff --stat 671925aecc 91b11ff0c9 -- infra/logic/02_DOCTRINE.md` is
  empty, so every canon line cited below as `@671925aecc:<n>` is the text both judges read, and it still holds at
  91b11ff0c9.

---

## 1. The four mechanical results

`check_canon_r1.py` was run at 91b11ff0c9. It computes these results from the two answer files and the key; it
never reads this file. It exits 0 on every verdict, so the VERDICT line decides.

| criterion | question | deciding lines | denominator | result |
|---|---|---|---|---|
| J3-AC1 `j3-verdicts` | same verdict per axis | `VERDICT: PASS-J3-SAME-VERDICTS` | `AXES: 5  SAME VERDICT: 5` | PASS |
| J3-AC2 `j3-citations` | same rule set per axis | `CITATIONS DIFFER: A1  A=['R18', 'R9']  B=['R20', 'R9']`, `VERDICT: FAIL-J3-CITATIONS-DIFFER` | `AXES: 5  SAME RULE SET: 4` | **FAIL** |
| J3-AC3 `j3-naming-key` | both judges on the key per case | `CASE OFF THE KEY: J-N3  A=OUT-OF-PATTERN  B=OUT-OF-PATTERN  key=ALIAS`, `VERDICT: FAIL-J3-CASES-OFF-KEY` | `CASES: 3  BOTH JUDGES ON THE KEY: 2` | **FAIL** |
| J3-AC4 `j3-blind` | neither base carries the other's file | `LEAKS: 0 of 2`, `VERDICT: PASS-J3-MUTUALLY-BLIND` | 2 of 2 directions checked | PASS |

---

## 2. Per axis: both verdicts and both rule sets

The rule sets below are the `R<n>` ids in each row's third column, which is also what `j3-citations` compares. The
last column is the canon's section 2 list of rules for that axis (`@671925aecc:88-92`).

| axis | judge A verdict | judge A rules | judge B verdict | judge B rules | verdict same | rule set same | section 2's rules for the axis |
|---|---|---|---|---|---|---|---|
| A1 INGESTION | UNDETERMINED | R9, R18 | UNDETERMINED | R9, R20 | yes | **no** | R9, R18 |
| A2 BUCKET STRUCTURE | VIOLATES | R4, R5, R6, R7 | VIOLATES | R4, R5, R6, R7 | yes | yes | R4, R5, R6, R7, R8, R16 |
| A3 NAMING | VIOLATES | R1 | VIOLATES | R1 | yes | yes | R1, R2, R3, R17 |
| A4 COMPUTE | UNDETERMINED | R13 | UNDETERMINED | R13 | yes | yes | R13 |
| A5 FORMAT | VIOLATES | R11 | VIOLATES | R11 | yes | yes | R9, R10, R11, R12 |

**Counts:** the verdict is the same on 5 of 5 axes, and the rule set is the same on 4 of 5.

**How the judges chose citations.** On A2, A3 and A5 both judges cite the rules that decided a VIOLATES verdict.
That is a subset of the section 2 list: 4 of 6, 1 of 4 and 1 of 4. Both name the other rules only in their reasons:
R16 on A2 ("conforms"), R2 on A3 ("not engaged"), R12 and R9 on A5. On A4 the list has one member, and both cite
it. Only A1 splits, and it is the one axis whose verdict no rule decided (section 4, D1).

**Agreement in the reasons as well as the verdicts:**
- A1: both name X1 (the Orion JWT read) as a DECLARED-EXCEPTION under R20.
- A1: both rank UNDETERMINED as more severe than DECLARED-EXCEPTION.
- A2: both read X7 as covering only 49financial's `category-views.json`.
- A2: both read X2 as covering P7 global.
- A3: both put P2's root `code/` under R1's legacy non-application.
- A4: both cite R13's DEFERRED threshold.

---

## 3. Per naming case: both verdicts against the key

The case names and node types come from `.../fixed_inputs/r1/CN_JUDGE_CASES.json`. The key's verdicts and canonical
forms come from `CN_JUDGE_NAMING_KEY.json:5-6`.

| case | name (type) | judge A | judge B | key | A on the key | B on the key | key canonical_form | judges' canonical form |
|---|---|---|---|---|---|---|---|---|
| J-N1 | `blackdiamond/49f/credentials` (SECRET) | CONFORMANT | CONFORMANT | CONFORMANT | yes | yes | `blackdiamond/49f/credentials` | the name itself (both read it as conforming) |
| J-N2 | `opal-data-bd` (S3_BUCKET) | ALIAS | ALIAS | ALIAS | yes | yes | `opal-data-49financial` | A `opal-data-49financial`; B `opal-data-49financial` |
| J-N3 | `bd-49f-runner-role` (IAM_ROLE) | OUT-OF-PATTERN | OUT-OF-PATTERN | **ALIAS** | **no** | **no** | `blackdiamond-49f-runner-role` | A `{system}-49f-runner-role`; B none printed |

**Counts:** the judges agree with each other on 3 of 3 cases, and both are on the key for 2 of 3.

**Citations.** Both judges cite the same canon parts on every case:
- J-N1: R1, N2 (a secret's scope segment takes the SHORT form) and N3's secret grammar.
- J-N2: R1, N5 ALIAS, N4, and the bucket grammar `opal-data-{scope}`.
- J-N3: R1, N3 ("never a system: a firm"), N5 OUT-OF-PATTERN and N4.

---

## 4. Every disagreement, traced to the canon rule it exposes (J3-J1)

J3-J1 is a judgment criterion. This section is its record, and it carries **no verdict**: 3.0.0_SA_CVO grades it at L9.

**Denominator.** The disagreements were found by subtraction, not recall. The population is the 5 axes, each with a
verdict and a rule set, plus the 3 cases, each with a verdict set against the key: 13 comparisons. 11 agree, which
leaves **two disagreements**:
- **D1:** the A1 rule set, judge against judge.
- **D2:** J-N3, both judges against the key.

There is no verdict disagreement between the judges. DEC-2 returns each disagreement to CN-k-1 as a canon defect.
Each is filed as one row.

### D1 -- axis A1: the same verdict with different rule sets (J3-AC2; row `LGIC_CANON-W7-S1`)

- **Judge A** (`judge-a.tsv@537f49b8fd:4`): `UNDETERMINED  R9,R18`. Its column is exactly the section 2 list for A1.
  Its reason names X1 as "DECLARED-EXCEPTION, R20" in prose only.
- **Judge B** (`judge-b.tsv@98ed3177ff:2`): `UNDETERMINED  R9,R20`.
  - R9 is the rule the missing facts leave undecided.
  - R20 decides X1.
  - R18 is dropped; neither judge could grade it.

**The canon rules it exposes:**
1. **Section 2's A1 row names rules that do not govern ingestion.** `@671925aecc:88` reads "A1 INGESTION | how a
   source arrives, by what mechanism | R9, R18". Neither rule states a law on an arrival mechanism:
   - R9 (`:364`, "BRONZE IS RAW AND UNTOUCHED") sits under `### A5 FORMAT` (`:362`) and governs bronze's bytes.
   - R18 (`:468`, "NO SHADOW PATH, NO DUAL-WRITE, NO STANDING COMPARATOR") sits under `### PROCESS` (`:466`).
   - Section 3's headings (`:110`, `:154`, `:296`, `:362`, `:410`, `:421`, `:446`, `:466`) include no A1 heading.
   - So A1 is the only axis with no rule of its own.
2. **The rule that decides A1's one measured departure is listed on no axis.** X1 is a register entry on axis A1
   (`CN_TREE_MDPF.md:58`, GRANTED, PERMANENT). R20 (`:484`) makes a declared departure "the pattern working". Section 2
   lists R20 only under "Process: R18, R19, R20" (`:94`).
3. **The canon does not say what an axis verdict cites.** It does not say whether a verdict cites the axis's section
   2 list or the rules that decided it:
   - Section 0 says a seat answers "is this conformant, and against which rule" (`:14-15`), which reads as the
     deciding rule.
   - Section 2 gives a list per axis.
   - Where some rule decided the verdict (A2, A3, A5), both judges took the deciding reading and agreed.
   - On A1 no rule decided the verdict (UNDETERMINED), and the one departure was decided by R20. There, judge A fell
     back to the axis list and judge B cited what its reasoning used.

**Also exposed, but it did not split the judges.** Both judges rank UNDETERMINED above DECLARED-EXCEPTION. The
canon states no such order:
- A case-insensitive search of `02_DOCTRINE.md` for `sever`, `adjacen` and `next to` returns 0 lines.
- `UNDETERMINED` appears once, at `:564` (GAP-2).
- `DECLARED EXCEPTION` appears as a ledger disposition at `:330` and `:528`, never as an axis verdict.

The axis verdict vocabulary and its order therefore came to the judges from outside the canon, and this worker did
not read where. If a later judge ranked them the other way, A1's verdict itself would split.

### D2 -- case J-N3: both judges OUT-OF-PATTERN, key ALIAS (J3-AC3; row `LGIC_CANON-W7-S2`)

**Both judges independently read `bd` in the system slot as the alias of the FIRM 49financial.** A firm in the
system slot fails the grammar, so both reached OUT-OF-PATTERN:
- Judge A (`judge-a.tsv@537f49b8fd:11`): "the system slot carries bd, the refused alias of the FIRM 49financial (N4, N5)".
- Judge B (`judge-b.tsv@98ed3177ff:9`): "the canon's only resolution of bd is as the firm's alias".

**The key reads ALIAS, with canonical form `blackdiamond-49f-runner-role`** (`CN_JUDGE_NAMING_KEY.json:5-6`). Its
stated source is `org/missions/D14/LGIC/LGIC_NAMING/deliverables/GRADING_RULE.md` @3cc090827f section 9. That worked
case (`:368`) reads "R3 bd next to firm 49f reads as the VENDOR blackdiamond". The rule it applies is GRADING_RULE R3
(`@3cc090827f:168-173`): `bd` "is the VENDOR `blackdiamond` when a V4 firm token is next to it, before or after, and
the FIRM `49financial` otherwise ... The test is ADJACENCY to a V4 firm token, never position".

**The canon rules it exposes.** All are in the generated naming section, which is rendered from
`org/standards/NAMING_SCHEMA.json` v1.8 (stamp at `@671925aecc:163`).
1. **N4 names both referents and gives no test for choosing one.** `:278` reads "`bd` | refused in EVERY slot ... The
   vendor is blackdiamond; the firm is 49financial."
2. **N5's only placed example of a `bd` alias is the firm reading.** ALIAS (`:285`) is "for example inflection or bd
   in a resource name's scope slot". OUT-OF-PATTERN (`:286`) names "a firm in the system slot", and N3 (`:222`) says
   "never a system: a firm".
3. **Section 1 points to the registry, and the registry puts `bd` on the firm.**
   - Section 1 (`:64`) makes a firm's registry aliases "spellings of one key".
   - The registry's `bd` alias row sits on the firm 49financial (`infra/logic/registry/scopes.json@91b11ff0c9:47-53`).
   - That row's `refused` text repeats N4's two-referent sentence.
4. **No line of the canon carries R3's adjacency test.** A case-insensitive search of `02_DOCTRINE.md` for `adjacen`
   and `next to` returns 0 lines.
   - So from the canon alone, `bd` next to `49f` in the system slot resolves only to the firm, and the judges'
     OUT-OF-PATTERN is the reading the canon supports.
   - The key's ALIAS needs a rule the canon does not state.

**Owner split, stated and not judged.**
- If L9 reads the canon as incomplete, the fix is to carry R3's adjacency test into the naming section. The section
  is generated, so the fix lands in the schema or the renderer and then goes through CN-k-1's re-render.
- If L9 reads the canon as right, the key is what differs.
- This worker did not read whether NAMING_SCHEMA.json carries the test and the renderer drops it, or the schema
  lacks it; neither file is in this order's reads.

**J-N3's canonical forms differ as a consequence of D2, not as a separate disagreement.** Judge A's
`{system}-49f-runner-role` uses N5's placeholder. `:288` allows a placeholder "ONLY for a slot the name does not
carry", and reading `bd` as a firm leaves the system slot empty. The key's `blackdiamond-49f-runner-role` reads `bd`
as the vendor.

### E1 -- one exposed ambiguity that did not split the judges (row `LGIC_CANON-W5-S1`, judge B's)

**R1's census tag and R1's text give two answers for the monolith's tier-first planes (A3):**
- R1's census tag (`:130`) reads "53 of 53 non-SmartX monolith planes CONFORMANT".
- R1's text (`:112-120`, source-first in every bucket) grades P4 `gold/mdpf/` and P5 `portal/gold/` out of the
  grammar. Those planes are in R5's census at `:314`.

Both judges graded A3 by the text: VIOLATES, R1. Judge B named the tension in its row; judge A did not raise it. It
did not split this pair. A judge who took the tag would have answered A3 differently.

---

## 5. The blindness check

- **Result:** both stated bases are 671925aecc77f15dfb33a1b15cfb966b0ae2c3ae. Neither answer file exists at that
  commit (`LEAKS: 0 of 2`). The judge commits carrying the files, @537f49b8fd and @98ed3177ff, both postdate it.
- **Instrument limit:** the base comes from the `# base` line each judge wrote into its own answer file
  (`check_canon_r1.py:107`). The check does not read the ancestry of the judges' branches. This worker did not
  re-measure it; the instrument is the cut's.

## 6. What this record does not do

- It gives no verdict on J3-J1, and it does not say which reading of D1 or D2 is right.
- It edits neither the canon, the key, nor any fixed input.
- Nothing live moves (PRD DEC-9).
