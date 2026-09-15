# LGIC_CANON.TO-CN-o-2 -- result (the review of the checklist, cell CN-o-2, round 1)

**Worker:** 0.9.0_WK_LGIC_CANON~7, an L7 worker of 2.0.0_SA_COO~G.
**Branch:** `wk-lgic-canon-1-7c`, cut from CLOUD @c08fd0c0eb.
**Worktree:** `/c/Users/AndrewBerman/Desktop/ajb_workspace/.worktrees/wk-lgic-canon-1-2`. It is a reused directory.
Its pre-existing untracked `.scratch/` belongs to earlier workers, and this worker neither read nor cited it. This
worker's own scratch is `.scratch/o2/`.

L9 reads the record `org/missions/D14/LGIC/LGIC_CANON/deliverables/CHECKLIST_REVIEW.md`, committed @894b41f920. This
file is the run log that sits beside the proof instance.

## Verdicts

Each criterion ran exactly as the order names it:

```
cd <WS> && timeout 120 python org/missions/D14/LGIC/LGIC_CANON/deliverables/2.0.0_SA_COO~G/fixed_inputs/r1/check_canon_r1.py <sub>
```

The run was at HEAD 894b41f920, the commit that carries the review. The checker reads the review's author with
`git log -1 --format=%an`, so the review had to be committed before either criterion could run. **The checker exits 0
on every verdict. The VERDICT line decides the result, never the exit code.**

| criterion | output, verbatim | rc | result |
|---|---|---|---|
| (baseline, before the review existed, at c08fd0c0eb) | o2-marks: `checklist: True  review: False` / `VERDICT: FAIL-O2-MARKS-ABSENT`; o2-zero: `checklist or review absent` / `VERDICT: FAIL-O2-ZERO-ABSENT` | 0 | the checker fails without the review |
| O2-AC1 | `STEPS: 16  MARKED WITH A REASON: 16  REVIEWER '0.9.0_WK_LGIC_CANON~7' IS NOT THE AUTHOR '0.9.0_WK_LGIC_CANON~6': True` / `VERDICT: PASS-O2-ALL-MARKED` | 0 | PASS by output |
| O2-AC2 | `STEPS MARKED: 16  MARKED JUDGEMENT: 5 [3, 7, 8, 9, 14]` / `VERDICT: FAIL-O2-JUDGEMENT-STEP` | 0 | **FAIL** |
| O2-J1 | judgment: the reason on each of the 16 lines of CHECKLIST_REVIEW.md | -- | RECORDED; UNVERIFIABLE-BY-INSTRUMENT, graded at L9 by 3.0.0_SA_CVO |

## The order's state

O2-AC2 reads FAIL, so this worker has **not** flipped the order's `<status>`, and it stays `pending`. That is a
finding about the checklist, not a gap in this review. The order itself names the case: marking a real judgement
step MECHANICAL to pass is the defect this cell exists to catch.

The five JUDGEMENT marks have two causes:

- **Steps 3, 7, 8 and 9.** Onboarding bundles the build of the firm's pipelines. The canon fixes a pipeline's homes,
  formats, compute and name grammar, but not its contents: the pipeline directory, the table names, the partition
  forms, the resource set and the function words. The inputs table carries none of these, and `key()` and
  `address()` accept any choice whose shape is valid.
- **Step 14.** The checklist mandates the partner table `opal-partner-<LONG>`. `grade()` reads that name
  OUT-OF-PATTERN, while Step 12 applies only names that read CONFORMANT. The auth handler requires the name, no
  register entry declares the departure, and the checklist names no STOP and no owner for the conflict.

One row is filed: `LGIC_CANON-W7-S3`, on O2-AC2. BLOCKING, INERT.

## What this worker read

The three reads the order names:

- `infra/logic/10_ONBOARDING_CHECKLIST.md`, in full (341 lines; its last commit is 05d5131e5e, by
  0.9.0_WK_LGIC_CANON~6);
- `infra/logic/02_DOCTRINE.md` v1.0, in full (576 lines);
- the CONTRACTS table of `org/missions/D14/LGIC/LGIC_ENFORCE/prd/LGIC_ENFORCE_PRD.md`.

Files the steps name, read only to ground a mark:

- `infra/logic/registry/scopes.json`: the `inflection`, `cottonwood` and `08242234` rows;
- `infra/logic/registry/systems.json`: `_about` and its 17 rows;
- `infra/logic/registry/tiers.json`: `homes`;
- `lib/opal_naming.py`: `_segment`, `key` and `address`, `:1269-1315`;
- `infra/aws/terraform/shared-infra/s3-49financial.tf`, in full;
- `infra/aws/users/ONBOARDING.md`: sections 2 and 5;
- `infra/aws/terraform/partner-firms/demo.tf`;
- `org/standards/NAMING_SCHEMA.json`: `changelog` and `rows_owner`;
- channel rows `LGIC_CANON-W6-S2` and `W6-S3`.

The two instruments this worker ran:

- `grade()`, read-only, on `opal-partner-demo` and `opal-partner-49financial`, both as `DYNAMODB_TABLE`;
- `comp-find "opal-partner"` over `infra/logic`, `org/standards` and `org/missions/D14/LGIC` (corpus `all`): 61 hits
  across 502 files.

`check_canon_r1.py` lines 519-645 show how the two results are computed.

## Instrument limits, stated and not re-measured

- **O2-AC1's author test** reads the name `git log -1 --format=%an` returns for each file (`check_canon_r1.py:92-94`,
  `:629-630`). Whoever commits sets that name with `--author`. So the test shows that the two commits carry different
  author serials. It does not independently show that the two workers are different.
- **O2-AC2 counts marks.** It reads each line's MECHANICAL or JUDGEMENT token (`check_canon_r1.py:620`, `:643`) and
  never its reason. Whether the reasons hold is O2-J1, graded at L9.
- **`review_marks()` keys its dictionary by step number** (`:620`), so a second `STEP <n>:` line would silently
  replace the first. CHECKLIST_REVIEW.md carries exactly one such line for each of steps 1 to 16, and no other.
