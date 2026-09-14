# LGIC_ENFORCE.TO-EN-c-1 -- result (0.9.0_WK_LGIC_ENFORCE~1)

**Branch** `wk-lgic-enforce-1-1`, cut from `CLOUD` @fd9c9ca174 (HEAD at the read: `fd9c9ca1742c54dee0c2c918b13f659c0dd9822a`).
**Proof instance:** `LGIC_ENFORCE.TO-EN-c-1.carrier-census.proof_of_spec.json`, in this folder.

## What landed

- `org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/CARRIER_CENSUS.md`: prose, then ONE json fence in the order's shape.
  - **189,011 token hits across 32,448 files scanned**, the denominator comp-find printed. 9,804 files hold hits.
  - The hits split into **12,949 carriers + 176,062 excluded**. A further **4 definition-pattern carriers** make
    `hits` = **189,015**.
  - **All 8 DEC-5 definitions are carriers.** 4 are found by token hit and 4 are admitted by definition pattern.
  - **12,917 carriers across 1,506 files sit outside the eight.** All are mapped to `LGIC_ENFORCE-W1-S1`.
  - The file is 36,642,889 bytes. About 189,000 of its lines are json entries, one per carrier, excluded hit or row mapping.
- Three rows appended to `org/missions/D14/LGIC/LGIC_ENFORCE/surprise-channel/investigations/INVESTIGATION_v1.md`:
  - `LGIC_ENFORCE-W1-S1`: the carriers outside the eight, filed as one row. OBSERVATION, INERT.
  - `LGIC_ENFORCE-W1-S2`: four DEC-5 definitions carry no firm token, so a token read cannot find them. They are admitted
    by definition pattern. OBSERVATION, INERT.
  - `LGIC_ENFORCE-W1-S3`: comp-find reads a worker's untracked `.scratch/`, so a census counts its own saved output, and
    `:(exclude)` scans 0 files. OBSERVATION, ARMED, disarm_owner `2.0.0_SA_COO~G`.

## Criteria (each run as `cd <WS> && timeout 120 python .../fixed_inputs/check_en.py <sub>`)

| id | deciding output | rc | verdict |
|---|---|---|---|
| C1-AC1 | `DENOMINATOR: {'files_scanned': 32448, 'hits': 189015, 'token_hits': 189011, 'definition_pattern_additions': 4, 'files_with_token_hits': 9804}` / `VERDICT: PASS-DENOMINATOR` | 0 | PASS-by-output |
| C1-AC2 | `DEC-5 DEFINITIONS: 8  PRESENT: 8  MISSING: []` / `VERDICT: PASS-DEC5-PRESENT` | 0 | PASS-by-output |
| C1-AC3 | `HITS: 189015  CARRIERS+EXCLUDED: 189015  EXCLUDED WITHOUT REASON: []` / `VERDICT: PASS-PARTITIONED` | 0 | PASS-by-output |
| C1-AC4 | `CARRIERS OUTSIDE DEC-5: 12865  FILED AS A ROW: 12865  UNFILED: []` / `VERDICT: PASS-EXTRA-FILED` | 0 | PASS-by-output |
| C1-J1 | recorded for 3.0.0_SA_CVO at L9 (the material is in the instance) | -- | RECORDED, no verdict |

The checker's "outside DEC-5" count is 12,865: carriers whose PATH is not one of the eight DEC-5 paths. The census's
12,917 is carriers outside the eight DEFINITION SPANS. The 52 between them sit in DEC-5 files but outside the
definitions, for example `perfrp_firm_pin.py`'s `FOREIGN_FIRM_BUCKETS`, and they are mapped to the row as well.

## Controls

- **Mutant, FIRED-AS-EXPECTED.** The real `check_en.py` ran in scratch trees against mutated copies of the record, with no
  committed file touched. Each mutant failed exactly the criterion it targeted:

  | mutant | criterion | output |
  |---|---|---|
  | M1: one excluded entry dropped | `c1-partition` | `CARRIERS+EXCLUDED: 189014`, `FAIL-NOT-PARTITIONED` |
  | M2: FIRM_CONFIG's carriers dropped | `c1-dec5` | `MISSING: ['infra/aws/lambda-edge/_shared/firm-config.mjs:65']`, `FAIL-DEC5-MISSING` |
  | M3: one row mapping dropped | `c1-extra-filed` | `UNFILED: ['.claude/settings.local.json:26']`, `FAIL-EXTRA-UNFILED` |
  | M4: `files_scanned` zeroed | `c1-denominator` | `FAIL-NO-DENOMINATOR` |

  The unmutated copy restored 4 of 4 PASS.
- **Determinism, STABLE.** The four invocations ran twice on the same bytes and `cmp` found them IDENTICAL: 16 lines, with 4
  PASS verdicts of 4.

## Instrument notes

- The census is run 3: the order's segment pattern with `-i`, over 38 top-level pathspecs (the worktree minus `.scratch`
  and `.git`), `--all`.
- Run 2 over the whole worktree printed 387,942 hits, 198,931 of them from run 1's saved output under `.scratch/`. Run 2
  minus those hits equals run 3 exactly (189,011). That is row W1-S3.
- The classification is a scratch script, not committed. Its rules are stated in section 3 of the deliverable, with each
  rule's count, and those counts sum to the 176,062 excluded.

## Not claimed

- No carrier is graded as wrong or due to move. Repointing is `ADVI_FIRMBKTS` FWD-3's.
- Tokens bounded by whitespace, `:`, `=` or `,` are outside the order's split and were not classified.
- Binary files (1,868), unreadable files (3), ephemeral-floor files (3) and the `portal/` submodule were not read.
- Every file-level exclusion is a rule applied to a whole file, not a line-by-line read. C1-J1 grades whether each reason
  holds.
- Nothing live moved. No AWS read, write or apply was made.
