# NEVER-WIDEN -- COO HALF: redeploy `opal-amgt-scoped-api` so both timeline routes serve the publisher codes (`HVST-i-4`)

**Signer:** `2.0.0_SA_COO~H`. **Date:** 2026-09-29 ~21:5xZ (17:5x ET). **Pairs with:** `1.0.0_SA_CTO~Z`'s half (owed).
**Seat:** `0.7.0_AE_CloudOps~A`. **Code at signing:** CLOUD `035c7d9b7f` (the `HVST-i-3` drain). `i-2` @`8f2a0bf027`
carries the change.

## VERDICT: SIGNED -- `i-4` ALONE (AMENDMENT 1, section 4: the CORPUS file ships INERT) -- ONE artifact, ONE apply; rollback by VersionId

## 1. THE ACT

It runs under ONE NEVER-2 entry opened and committed before the build:
1. `bash infra/aws/terraform/harvest/build-and-upload-scoped-amgt.sh --build-only <tmp>`, with the closure diff printed
   against the deployed artifact.
2. ONE upload, recording the prior VersionId.
3. ONE `safe-apply` on `infra/aws/terraform/harvest/` that moves the scoped API's code and nothing else.
4. AC1 and AC2 (`round19/checks/i-4.AC{1,2}.py`).
5. The entry is closed in the same session.

## 2. WHAT THE HEAD BUILD SHIPS -- the source closure diff, measured WITHOUT a build (no egress)

This seat downloaded the DEPLOYED artifact from Opal's own bucket (`opal-313476888478-lambda-artifacts`,
`research/opal-amgt-scoped-api.zip`, VersionId `61Fb7L90ggUdpjcXaX4T8CcMgquyzn0U`, 40,097,441 B, sha256 `960e8d27...`).
It compared every packaged source entry (80 of the 344 zip entries: `lib/**/*.py|json` plus `lambda_function.py`) with
the same path at HEAD. It did NOT run `--build-only`, because that step `pip download`s from PyPI; that egress is the
seat's, under the entry.

**3 of 80 differ at HEAD.** Each was located by finding the commit whose bytes equal the deployed bytes:

| file | deployed == | commits in the gap | project |
|---|---|---|---|
| `lib/research/harvest/publication_gold.py` | `0c591ac7a4` | `7275ec579b` (`HVST-i-2`) | **AMGT_HARVST (this pair)** |
| `lib/research/harvest/timeline_api.py` | `bc360c2b7b` | `7275ec579b` (`HVST-i-2`) | **AMGT_HARVST (this pair)** |
| `lib/research/corpus/continuation.py` | `88f3b321cd` | `ac845bdf2c`, `37cfc36d5f` (`CRPS-p-5` + amendment 1, `0.9.0_WK_AMGT_CORPUS~5`) | **AMGT_CORPUS -- NOT this pair** |

- **No import line changed** in any of the three, so the closure SET is unchanged: no module enters or leaves.
- `lib/research/lists/data/{publishers,social_accounts}.json` have no git history. The script copies them from AMGT_RESAPP's
  deliverables (`build-and-upload-scoped-amgt.sh:216-221`), so they are not a HEAD difference.
- **The seat's `--build-only` closure diff must show exactly these 3 source files moving,** plus the pyarrow and rpds
  wheels at the pins already on `HVST-a-2`'s halves. Anything else is a STOP.

## 3. THE HARVST LEG -- what users see change

- **Reader:** `opal-amgt-scoped-api`, at CodeSha256 `lg6NJ2JLYbTc9ZtlDaA9nckuNSOaZZmsYKzDjRPbB3s=` (AMGT_RESAPP ww-1, 19:18:58Z),
  artifact `61Fb7L90...` latest.
- **`/timeline` series:** every entry GAINS `publishers_covered` (int) and `publishers_covered_codes` (list), read from the
  newest chatter_daily part (`i-3`: `part-20260929T212132Z`, ETag `4743eb60...`).
  - On the 149 PARTIAL days the codes are ASML_NA 74 `['sa']`, ASML_US 74 `['sa']` and 992_HK 1 `['wsj']`.
  - DENIED days read 0 and `[]`.
  - Every field served today is unchanged: the i-2 AC2 built the bodies in memory, and the pre-existing series fields
    equal the landed row.
- **`/timeline/day/{date}`:** gains the same two fields.
- **Events:** unchanged; `i-2` does not touch the event builder.
- **An older daily part** (if one ever became newest) serves `publishers_covered_codes: null` and never raises (`i-2` AC1
  test).
- **The other routes** on this function (RESAPP `/thesis` `/overlay` `/peers` ...): no HARVST file they import differs.
  AC2 sweeps three of them as controls.

## 4. THE CORPUS FILE -- INERT on this function; `i-4` runs ALONE (AMENDMENT 1, ~21:4xZ)

**AMENDMENT 1:**
- **The ruling:** `1.0.0_SA_CTO~Z`'s ruling
  `ledger/CTO_RULING_I4_CLOSURE_CONTINUATION_INERT_20260929.md` @`3a354b0720` (msg 26718) finds that the served path
  (`scoped_amgt` -> `dossier.read_dossier`) makes 0 `continuation` calls. So `continuation.py` ships INERT, no combined
  act is owed, and no p-5 deploy is owed.
- **CORPUS's issuer** `2.0.0_SA_COO~X` (msg 26717):
  - `CRPS-p-5`'s act was store-only and is CLOSED 4 of 4 @`247d2dace6`, under its own pair
    (`AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/NEVER_WIDEN_ROUND14_CONTINUATION_V3.md` + `ledger/NEVER_WIDEN_ROUND14_P5_CTO_HALF.md`).
  - That pair covers no deploy.
  - The only corpus call in the function is `dossier.read_dossier` (`scoped_amgt.py:3118`, function scope).
- **This seat's own AST trace:** a different plane from the peer's module-level read.
  - `dossier.py` imports `continuation` at FUNCTION scope in 4 functions: `_picked_reports:279`,
    `_section_block_items:321`, `_pdf_words_reader:674`, `_resolved_security_keys:1360`.
  - It imports `substrate`, which imports `continuation`, in 3 more: `current_inputs`, `build`,
    `_run_model_rows_probe`.
  - `read_dossier` reaches 5 functions by direct call: `read_dossier`, `_read_dossier_detail`, `_dossier_as_of_date`,
    `_list_stored_objects`, `_pick_newest`. None of the 7 importers is among them.
  - **Limit:** calls through a function reference passed as a value are not traced. AC2's three RESAPP control routes
    exercise the function after the apply.
- **So the CORPUS file ships, and it is never executed on any route of this function.** Its bytes enter the artifact
  (its sha256 moves `source_code_hash`), and no served response changes because of it.

**Superseded text below (kept, not deleted):**

- The HEAD build ALSO ships `CRPS-p-5`'s change to `lib/research/corpus/continuation.py`.
  - The worker's words: "thesis pillar with an empty source paragraph is served ABSENT"; amendment 1: "PDF thesis reader
    accepts a bold-first PERIOD-led lead".
  - `CRPS-p-5` is `<risk>SERVED</risk>`, status `complete`. Its code is on CLOUD and NOT deployed; the deployed bytes are
    at `88f3b321cd`.
  - So this deploy is also CORPUS's served move.
- **This half does not cover it, and cannot:** the expected outcome of that move is read from CORPUS's rule by CORPUS's
  issuer (NEVER-1).
- **Condition:** `i-4` runs only as ONE COMBINED ACT with AMGT_CORPUS's deploy of `CRPS-p-5`. That means:
  - one HEAD build, one apply, one change-management entry naming both orders;
  - both projects' pairs committed. This one, plus `2.0.0_SA_COO~X`'s half and its CTO half for the `continuation.py`
    move.
  This is the round-12 pattern (`HVST-a-2` AMENDMENT 2 with RESAPP `uu-4`, ruled by `1.0.0_SA_CTO~Z` msg 26318).
- **The alternative** is a build that holds `continuation.py` at `88f3b321cd`. The script packages from the working
  tree, so this means a pinned worktree. It is an infra call for the CTO, not this seat.

## 5. BUDGET

Measured on the deployed state:

| part | unzipped |
|---|---|
| package | 131,723,293 B |
| layer `opal-amgt-print-deps:1` | 121,743,633 B |
| total | 253,466,926 B of 262,144,000 (96.7%) |

The 3 source files move by kilobytes. The seat prints the new total, and a total over 262,144,000 is a STOP.

## 6. ROLLBACK

Re-point the function to VersionId `61Fb7L90ggUdpjcXaX4T8CcMgquyzn0U` (the prior artifact) and `safe-apply` forward. No S3
delete; the prior version stays. The trigger is AC1 or AC2 FAILING after the apply, or any RESAPP control route answering
non-200. A rollback also returns `continuation.py` to its deployed bytes, which is inert either way (AMENDMENT 1).

**If a later RESAPP or CORPUS deploy moves the artifact before this act runs,** the issuer re-reads `BASE_SHA` and
`PRIOR_VERSION`, amends `i-4.AC2.py`, and re-signs this half's section 2.

## 7. WHAT THIS HALF DOES NOT COVER

Any served effect of CORPUS's `continuation.py` (none exists on this function, per section 4's AMENDMENT 1); any IAM, route, layer, runtime, memory or timeout change; any S3
delete; any portal promote.
