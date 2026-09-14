# LGIC_NAMING.TO-LN-h-1 -- hand-grader A -- result

**Worker:** `0.9.0_WK_LGIC_NAMING~7` | **Branch:** `wk-lgic-naming-1-7` | **Base:** `3d671ff59cfba948d00af61d2d7145ea254f63b7`
**Cell:** `LN-h-1` (PRD candidate N6) | **Deliverable:** `org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/n6-grader-a.tsv`

## What was graded

All 88 names in `2.0.0_SA_COO~G/fixed_inputs/N6_SAMPLE.json` (85 `discriminating` + 3 `overlap`), by hand. I used only
`GRADING_RULE.md`, `LEGACY_SERVED_PATHS.json`, `org/standards/NAMING_SCHEMA.json` v1.4 and
`infra/logic/05_IDENTITY_SPINE.md` v0.1. The TSV was emitted by a generator in `.scratch/`. It keys each hand verdict to
the sample's own `(type, position)` pair, so no name is retyped, and it fails closed if a pair is missing or extra.

| verdict | count |
|---|---|
| CONFORMANT | 13 |
| ALIAS | 1 |
| OUT-OF-PATTERN | 37 |
| RAISE | 18 |
| NOT-GRADED | 19 |
| **total** | **88 of 88** |

## Criteria (verbatim output, `timeout 120`)

- `H1-AC1`: `SAMPLE: 88 (85 discriminating + 3 overlap)  GRADED WITH A VERDICT: 88  MISSING: []` / `VERDICT: PASS-ALL-GRADED`. **PASS-by-output.**
- `H1-AC2`: `BASE: 3d671ff59cfba948d00af61d2d7145ea254f63b7` / `VERDICT: PASS-BASE-RECORDED`. **PASS-by-output.**

The mutant control: one verdict (`SECURITY_GROUP mdpf-daily-runner-sg`) was set to `GUESS`, and `h1-graded` printed
`GRADED WITH A VERDICT: 87 MISSING: [('SECURITY_GROUP', 'mdpf-daily-runner-sg')]` / `VERDICT: FAIL-UNGRADED`. The file was
then restored byte-identical (`cmp`). The checker exits 0 on FAIL as well as on PASS, so the VERDICT line decides and the
exit code does not.

## Where the rule's text left a reading to choose (stated for the L9 comparison, not decided here)

Each case below was placed by the rule. None was a guess and none raised. I record each one because a second grader
could read the same clause another way:

1. **`SECRET opal/bd/credentials` -> ALIAS `opal/49f/credentials`.** R2 needs "t2". I read it as the first token of the
   next segment, as S2 does for R1.d. That token is `bd`, and no firm token is next to it, so R3 reads it as the FIRM,
   not the vendor. The system therefore stays `opal`. S3 says segment 2 is the scope "when it is a V4 token". `bd` is not
   in the V4 table: it appears only as a V4 bullet ("a refused alias; see R3"). I took it as a scope under R4 ("the scope
   tokens are the V4 tokens, plus `bd` read as the firm"), in the short form `49f`. V-4 then applies, since the only change
   is `bd` -> the firm's form for the slot. The other reading of t2 (none, because segment 1 has one token) also leaves
   the system as `opal`.
2. **`SECRET FredApiKey` -> OUT-OF-PATTERN `fred/api-key`.** I applied N2 (camel split) to the secret before S1's "first
   kebab token is the system". This gives `fred` (a V1 feed) with purpose `api-key`, and no scope (S5).
3. **`S3_BUCKET opal-313476888478-globgrph` -> CONFORMANT.** B3 does not consult V2 for the purpose, so `globgrph` does not
   raise here, although it raises in every resource-name system slot.
4. **`SSM_DOCUMENT opal-cot-bd-session-fetch` -> OUT-OF-PATTERN `opal-cot-blackdiamond-session-fetch-document`.** R2 reads
   only t2 (`cot`, a firm), so the system is `opal`. `bd` sits next to `cot`, so R3 reads it as the vendor `blackdiamond`.
   It stays in the function, because R1 takes the system from t1 and R2 never reaches t3.
5. **`DYNAMODB_TABLE bd-securities` -> OUT-OF-PATTERN `{system}-49f-securities-table`.** No firm token is next to `bd`, so
   R3 reads it as the firm. It is therefore V3 in the system slot (R1.d) and the scope `49f` (R4).
6. **`N4` suffixes** (`smartx-exporter-profile-2025...04`, `smartx-exporter-2025...02`, 26 digits each) are dropped. The
   8-digit `20260911` in `ycharts/session/research-20260911` is under the 14-digit bar and stays.

## Not read

GRADING_RULE.md also cites `infra/logic/09_NAMING_CENSUS.md` and `LGIC_NAMING_PRD.md`. I did not open either: the rule
inlines the CENSUS vocabulary it uses (V1-V3), and the order's read list names neither. Also not read, as the order
requires: the rule author's other files, other `exercises/` files, `N3_*`, `N5_*`, the decomposition and this project's
task orders (except this one).

## Surprise rows

None filed.
