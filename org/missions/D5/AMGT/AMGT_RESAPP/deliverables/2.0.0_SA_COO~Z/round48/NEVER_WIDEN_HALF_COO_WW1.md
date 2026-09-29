# NEVER-WIDEN -- COO HALF -- AMGT_RESAPP round 48, AMGT-ww-1 (the redeploy on the canonical prefix) -- 2.0.0_SA_COO~Z, 2026-09-29

The order this half covers: `org/missions/D5/AMGT/AMGT_RESAPP/task-orders/AMGT_RESAPP.TO-AMGT-ww-1.the-redeploy-on-the-canonical-prefix.md`.
It executes only after BOTH halves are committed. Written AFTER ww-2 (@7ea218afad) and ww-4 (@6d63d059f4) drained, against their
landed code, and after AMGT_CORPUS round 12 moved the dossier to the builder's prefix (d0141a6a76; 95 objects under it).

## THE BLAST RADIUS -- what the act MAY touch, and the rollback for each

**Writers of the named properties, counted (one rule read per writer):**
(a) `/thesis` `model.cases` (and its copy `model_cases`): ONE writer, `scoped_amgt._model_cases` -> `case_rule.compute_cases`
    (vv-1 adds `label` and the basis-true formula; ww-4 adds `formula_words` via `model_words.formula_words`).
(b) `/thesis` `model.team_cases`: ONE writer, `scoped_amgt._team_cases` via `lib.research.corpus.dossier.read_dossier` (vv-2).
(c) `/thesis` `model.line_names`: ONE writer, `read_thesis_bundle` from `model_words.LINE_NAMES` (ww-4).
(d) `/lead-panel/rankings/<kind>/<window>` rows' `name`, `classification`, `name_state`: ONE writer, `read_rankings` ->
    `_join_classification` -> `_classification_for_ticker` (ww-2), reading `etf-classifications` by key.
(e) The rich export: ONE writer, `render_pack.build_rich_text` (the case line via `_model_case_line`, vv-1; the figure tables via
    `_figures_table`, ww-4). `build_pack` (the pdf path) calls neither. N = 5 rules read.

| act | what it MAY touch | rollback |
|---|---|---|
| A. ONE artifact write `research/opal-amgt-scoped-api.zip` in `opal-313476888478-lambda-artifacts` | that one object | the prior VersionId (read by the lane at build) stays; a re-point is a copy, never a delete |
| B. ONE `safe-apply` on `infra/aws/terraform/harvest/`: `opal-amgt-scoped-api`'s code; ONE entry `amgt/harvest/gold/research_dossier/` added to `local.scoped_amgt_pool_prefixes` (builder output: `lib.opal_naming.address("amgt","harvest","gold","research_dossier",...)` prints `s3://opal-data-harvest/amgt/harvest/gold/research_dossier/...`), so the existing two statements grant `s3:GetObject` under it and a prefix-conditioned `s3:ListBucket` on it; ONE statement granting `dynamodb:GetItem` (only) on `arn:aws:dynamodb:us-east-1:313476888478:table/etf-classifications` | every route of that function (`/api/scoped/amgt/*`) and the role's read set, by exactly that prefix and that one table action | re-apply at the recorded prior VersionId and remove the prefix entry and the DynamoDB statement; never a delete of data |

The Terraform change is COMMITTED before the apply (the naming gate grades it at commit; a refusal is a STOP). The legacy hyphen
prefix is NOT granted.

## EXPECTED OUTCOME OF B -- measured by running the LANDED code (HEAD after the ww-4 drain) over every live-library name, beside the DEPLOYED function (`CtIvirvM...EAOM=`), 2026-09-29 ~13:1xZ, 96 names (the library grew by one since the cut), 0 read failures

1. **`model.cases.base`: SERVED -> SERVED 70, ABSENT -> ABSENT 26, nothing else moves.** On all 70 SERVED the `formula` text
   changes to "Bloomberg consensus EPS (FY1, BEST_EPS) x adjusted trailing-median P/E (PX_LAST / IS_COMP_EPS_ADJUSTED)" and
   `formula_words` is added; on all 96 `label` "Historical-multiple reference" is added. **Every other key of every case object is
   byte-equal on 96 of 96.** No value moves.
2. **`model.team_cases` is a NEW key on all 96** (served on 0 today): 34 names carry all three cases SERVED, 62 all three ABSENT
   with the dossier's own reason, 0 read failures. The count moves with the dossier population (28 at round 47), so AC2 grades
   "as the dossier holds them" per name at read time, never a fixed 34.
3. **`model.line_names`** is a NEW key: the 25-entry map, equal to the page's `LINE_NAMES`.
4. **Rankings:** `trending/chatter` served 2 rows, landed 2 rows, **equal apart from the three added keys**; `name_state` SERVED
   on 2 of 2. A ticker the table does not hold reads ABSENT with a reason; a failed read reads READ_FAILED (never a guessed name).
   The 59 library rows ww-3 will create carry no name (Z-S300), so after that write those tickers read `name_state` ABSENT with
   their classification SERVED. That write is a SEPARATE act under its own pair and is NOT part of this one.
5. **The rich export:** the Base case line changes to the labelled line with the new formula text (vv-1); the figure tables gain a
   `Line` column between the mnemonic and the rendered text (ww-4). **The `/print` pdf: UNCHANGED** (`build_pack` calls neither).
6. **`/timeline`: UNCHANGED.** Measured: the landed `_serve_timeline` in process beside the deployed route, same moment, 4 names
   (AMD, BA, GOOGL, 1299 HK): 12,257 JSON paths, 0 differing. The timeline reads HARVST's stored gold through
   `publication_gold._latest_gold_snapshot_rows`, `_iter_latest_articles` and `_day_of`; HARVST's later producer changes
   (HVST-e-1, f-2) move what the producer WRITES, not what this route reads.

## THE LANE STOPS on any of six limbs

1. The closure diff names a file beyond: `lib/research/api/case_rule.py`, `lib/research/api/model_words.py`,
   `lib/research/api/scoped_amgt.py`, `lib/research/print/render_pack.py`; the dossier read's closure (`lib/research/corpus/dossier.py`,
   `base_census.py`, `gold.py`, `sector_template.py`, `lib/research/peers/__init__.py`, `lib/research/peers/taxonomy.py`, and
   `lib/research/corpus/extract.py` SHIPPED-INERT, as round 47's amendment 2 ruled: no served route may import a PDF library);
   and `lib/research/harvest/publication_gold.py` (guarded by limb 6).
2. `build_pack` changed.
3. In `scoped_amgt.py`, a changed function beyond `_model_cases`, `_team_cases`, `_team_case_absent_all`, `read_thesis_bundle`,
   `read_rankings`, `_classification_for_ticker`, `_join_classification`, `_model_line_names`, `_formula_words`,
   `_case_with_words` and the module constant `CLASSIFICATIONS_TABLE` (measured `git diff -U0 0d54b880cf HEAD`: every hunk is an
   addition except one replaced line inside `read_rankings`).
4. The plan moves anything beyond the function's code, the one pool-prefix entry and the one DynamoDB statement.
5. The served `/print` pdf OUTPUT moves (graded on output against a pre-apply capture).
6. The served `/timeline` OUTPUT moves (captured before the apply, byte-equal after it; round 47's CTO limb, kept).

## THE FALSIFIERS

1. **ww-1 AC2** (`round47/checks/vv-4.AC3.py`) reads, per live name, formula AND label as ruled on every SERVED base (70 of 70 at this
   read) and `team_cases` exactly as `read_dossier` holds each case; at base it reads formula-as-ruled 0 and no `team_cases`. A
   `/thesis` read that reached `extract` would fail that import and answer ABSENT "read failed" for a name whose dossier carries
   cases, so AC2 also falsifies the no-PDF runtime clause.
2. **ww-1 AC3** reads the rankings rows' name/classification/name_state and `model.line_names` + base `formula_words` on the deployed
   function; at base it FAILS on both.
3. **FWD-30 holds** (`round47/checks/vv-4.AC2.sh`, read by the issuer at close as the no-regression arm).

Any criterion failing after the apply is the ROLLBACK trigger.

Signed: `2.0.0_SA_COO~Z`, 2026-09-29.
