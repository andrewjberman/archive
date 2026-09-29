# NEVER-WIDEN -- COO HALF -- AMGT_RESAPP round 47, AMGT-vv-4 (the redeploy) -- 2.0.0_SA_COO~Z, 2026-09-29

The order this half covers: `org/missions/D5/AMGT/AMGT_RESAPP/task-orders/AMGT_RESAPP.TO-AMGT-vv-4.the-redeploy.md`. It executes only
after BOTH halves are committed. Written AFTER vv-1 (@a6c17f4bcf) and vv-2 (@a8965c9904) drained, against their landed code.

## THE BLAST RADIUS -- what the act MAY touch, and the rollback for each

**Writers of the named properties, counted:** (a) `/thesis` `model.cases` (and its copy `model_cases`): ONE served writer,
`scoped_amgt._model_cases` -> `case_rule.compute_cases` (vv-1 adds `label` in `_model_cases`; the formula constant is
`case_rule.BASE_FORMULA`). (b) `/thesis` `model.team_cases`: ONE writer, `scoped_amgt._team_cases` via the one dossier read
`lib.research.corpus.dossier.read_dossier` (set in `read_thesis_bundle`). (c) The rich export's case line: ONE writer,
`render_pack._model_case_line` (called only from `build_rich_text`; `build_pack`, the pdf path, never calls it). N = 3 rules read.

| act | what it MAY touch | expected outcome (measured below) | rollback |
|---|---|---|---|
| A. ONE artifact write `research/opal-amgt-scoped-api.zip` in `opal-313476888478-lambda-artifacts` | that one object | a new VersionId | the prior VersionId (re-read by the lane at build) stays; a re-point is a copy, never a delete |
| B. ONE `safe-apply` on `infra/aws/terraform/harvest/`: `opal-amgt-scoped-api`'s code, and ONE entry `"amgt/harvest/gold/research-dossier/"` added to `local.scoped_amgt_pool_prefixes` (the file's existing statements then grant `s3:GetObject` under it and a prefix-conditioned `s3:ListBucket` on it -- read-only; no other prefix, action or resource) | every route of that function (`/api/scoped/amgt/*`) and the function role's read set, by exactly that one prefix | below | re-apply at the recorded prior VersionId and remove the one list entry; never a delete of data |

**Expected outcome of B -- measured by running the LANDED code (HEAD after the vv-2 drain) over every live-library name's stored
block and dossier, beside the DEPLOYED `/thesis` (`CtIvirvM...EAOM=`), 2026-09-29 ~07:1xZ, 95 names, 0 read failures:**

1. **`model.cases.base`: SERVED -> SERVED 70, ABSENT -> ABSENT 25, and nothing else moves.** On all 70 SERVED, `formula` changes from
   "adjusted consensus EPS (FY1) x adjusted trailing-median P/E (...)" to "Bloomberg consensus EPS (FY1, BEST_EPS) x adjusted
   trailing-median P/E (PX_LAST / IS_COMP_EPS_ADJUSTED)"; on all 95, `base` gains `"label": "Historical-multiple reference"`. **Every
   other key of every base, and every upside/downside object, is byte-equal on 95 of 95** (0 names move anything beyond formula
   and label). No value moves.
2. **`model.team_cases` is a NEW key on all 95 (served on 0 today):** 28 names carry all three cases SERVED (table, citation and the
   dossier's own `unit_as_written` / `currency` / `currency_basis`, copied as written), 67 carry all three ABSENT with the dossier's
   own reason. The count read 27 at vv-2's drain and 28 here: the dossier population moves by one between reads, so the lane's AC3
   grades "as the dossier holds them" per name at read time, never a fixed 28.
3. **The rich export:** only the Base case line changes, from "Base case: SERVED -- ..." to "Historical-multiple reference: SERVED --
   ..." with the new formula text (70 names) or the label on the ABSENT line (25). `team_cases` is NOT rendered. `/print` pdf:
   UNCHANGED. Every other route: no change beyond what `read_thesis_bundle` carries on `/thesis`.
4. **The page** (not deployed by this act; portal DEV) prints the same labelled line (vv-1) and does not render `team_cases`.

**The lane STOPS on any of five limbs:** (1) the closure diff names a file beyond `lib/research/api/case_rule.py`,
`lib/research/api/scoped_amgt.py`, `lib/research/print/render_pack.py`, and the dossier read's own import closure
(`lib/research/corpus/dossier.py` and what it imports at module level, which must NOT include `fitz`/`pymupdf`); (2) `build_pack`
changed; (3) in `scoped_amgt.py`, any function beyond `_model_cases`, `_team_cases` and `read_thesis_bundle` changed; (4) the plan
moves anything beyond the function's code and the one pool-prefix entry; (5) the served `/print` pdf OUTPUT moves (graded on output
against a pre-apply capture).

## THE FALSIFIERS

1. **vv-4 AC3** reads, per live name, formula AND label as ruled on every SERVED base (70 of 70 at the last read) and `team_cases`
   exactly as `read_dossier` holds each case; at base (the deployed code) it reads formula-as-ruled 0 and no `team_cases`.
2. **FWD-30 holds** (vv-4 AC2: 95 of 95, cases missing 0) with the page and the export both printing the labelled line.

Signed: `2.0.0_SA_COO~Z`, 2026-09-29.

## AMENDMENT 1 (2026-09-29 ~07:2xZ) -- limb 1 admits `publication_gold.py`; limb 6 adopted (the CTO half @5ca429458d, msg 26490)

The build from HEAD also ships `lib/research/harvest/publication_gold.py` as AMGT_HARVST's `HVST-b-1` left it (`f41a4f3a36`,
`bb169815a5`; measured `git diff 0d54b880cf HEAD -- lib/research/`: 366 lines in that file). The timeline routes the combined act
mounted read it. **Limb 1 now also admits `lib/research/harvest/publication_gold.py`**, as the CTO half names it (its changed
functions are reached by no mounted `/timeline` path, 0 diff paths, the CTO's measurement). **STOP limb 6 (the CTO's) is adopted:**
the served `/timeline` output is captured before the apply and must be byte-equal after it. The dossier read's closure (`dossier.py`,
and what it imports at module level, e.g. the new `base_census.py`; CORPUS l-1) was already admitted by limb 1 and stays so; no
`fitz`/`pymupdf` in it. RESAPP's expected outcome (s.1-4 above) is unchanged.

Amended: `2.0.0_SA_COO~Z`, 2026-09-29.
