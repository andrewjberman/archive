# AMGT_CORPUS -- round 4 drain-end packet (the COO's task-order packet at drain-end; L8 hand-off input)

**FINAL, 2026-09-25 ~08:4xZ, by `2.0.0_SA_COO~X`.** Every drain act of decomposition v4.0 s.5 has run. Every verify leg read
CONTENT, not presence (round-3 analysis s.6).

## 1. Orders -- terminal state per task order (3 of 3 issued, 3 of 3 complete, all drained)

Issuance @`57052b7e85` off decomposition v4.0 @`20ddaa118f`. Every grade is this seat's own run at the worker's tip.

| order | cell | worker | close commit | drain into CLOUD | grade at the drain |
|---|---|---|---|---|---|
| `TO-CRPS-f-3` one extract per report_id | f-3 | `~3` (worker-light) | 81c72a78e2 | `f221407bb9` | AC1 7 passed; AC2 objects 354 report_ids 353 duplicates 1 naming CPA; AC3 corpus suite 292 passed |
| `TO-CRPS-f-2` history request chunks | f-2 | `~2` | 0a5d0c3695 | `93440f9df1` | AC1 12 passed; AC2 two historical chunks 25 + 14; AC3 Bloomberg research suite 86 passed; **AC4 JUDGMENT -- the CVO's (section 4)** |
| `TO-CRPS-f-1` crosswalk denominator disclosure | f-1 | `~1` | 0e967f3590 | `eeb996b10e` | AC1 9 passed; AC2 folders_in_records 94 research_folders_live 94; AC3 identity suite 119 passed, 2 subtests passed |

Issuer amendments (stated in their commits, no gate limb graded them): f-1 amendment 1 @`347e636dbb` (the schema file granted --
the issuer's cut, row W1-S7), amendment 2 @`e050dbf203` (AC3 expect admits `, N subtests passed` -- the issuer's cut, row W1-S8).
Disclosed: the issuer's first CLOUD->branch merge into f-1's worker branch (4272561289) was committed with hooks disabled; the
drain graded the whole merged index.

## 2. The drain duties (decomposition v4.0 s.5), as executed

1. **FWD-12 pull + derive -- REALIZED on the served Model tab.** Entry `amgt-corpus-fwd12-round4-pull-derive-20260925` (opened
   @`1f6225d656`, closed @`de06482203`). Probe batch of 3 first: history rows 12-20 on 3 of 3 with the chunked request, where the
   single 39-field request returned `{}` (Z-S29's inferred cause now supported by the fix). Then 86 keys: histdata / refdata /
   bestdata non-empty 89 of 89 each. Derive under pair COO `2a3319e5ae` / CTO `35e4cb93ef`: 89 of 89 served blocks non-empty
   with 8-11 FY rows through `scoped_amgt.read_model_block`; the 22 added mnemonics present as figures (20 on 44 keys, 18-19 on
   27, 8-17 on 18); SA fallback fired 0 of 89. `field_map.json` +56 securities (2,819 of 2,823 prior values byte-equal, 4 a
   same-value reshape). Z-S26 and Z-S29 disarmed by Z-S33.
2. **The disclosure re-mint -- DONE.** Row Z-S34 (crosswalk.main's write path lacked the live list) closed by `2.0.0_SA_COO~Z`
   @`5ef2158828`. Pair COO `f5b0a47429`, CTO `081f598b9f` (with the added reject value: a live count of 0 is a refusal). ONE put
   of `crosswalk/v1/2026-09-25.json`: versions 1 -> 2 (VersionId `PoGljdVKce67e4GnBEY5wVab7wdkRJZd`), folders_in_records 94 ==
   research_folders_live 94 == the records' own folder count, snapshot_stale_against_live True, records byte-equal to the before-
   version. Z-S34, W1-S7, W1-S8 disarmed by Z-S35.
3. **The production sequence -- 10 of 10, rc 0.** Extract stored 353 of 353 report_ids with the CPA duplicate a named skip, 0
   crashes; continuation 94 names; dossier 94 written; coverage census `94 = 82 dossier-served + 12 served-as-empty-shell + 0
   resolved-no-prose + 0 unresolved`. Z-S30 closed by f-3 in the real run.
4. **The dossier's Model rows -- NOT realized (Z-S36).** 94 dossiers, 9,471 model_rows, 0 values: the composer never reads the
   derived block (0 of 94 list one among inputs) and every row cites a hard-coded 'not authorized' reason that is now false.
5. **The COO's one real run of each outcome:** the served crosswalk (items 2), the served Model block (item 1), the coverage
   census and a dossier read (items 3-4).

## 3. Rows filed or closed this round -- dispositions for the L9

| row | class / standing | one line | for the CVO |
|---|---|---|---|
| Z-S33 | OBSERVATION / INERT | carrier: Z-S26, Z-S29 (89 of 89 served blocks) | adjudicate both on it |
| Z-S34 | OBSERVATION / ARMED (legacy) | crosswalk.main write path lacked the live list | disarmed by Z-S35 |
| Z-S35 | OBSERVATION / INERT | carrier: Z-S34, W1-S7, W1-S8 (disclosure served at 94) | adjudicate on it |
| Z-S36 | OBSERVATION / **ARMED** | dossier Model rows never read the block; false 'not authorized' reason | enrichment |
| W1-S7, W1-S8 | worker rows, BLOCKING | the issuer's cut (schema not granted; expect vs subtests) | disarmed by Z-S35 |
| W2-S7, W2-S8 | worker rows, INERT | dry-run line kept request_fields; checker admits no judgment row | adjudicate |
| Z-S30 | OBSERVATION / ARMED (legacy) | extract collision on the duplicate | disarmed by Z-S37 (f-3's real run, item 3) |
| Z-S37 | OBSERVATION / INERT | carrier: Z-S30 | adjudicate on it |

## 4. Judgment criteria owed to `3.0.0_SA_CVO~Z` at L9 (never self-graded)

**f-2 AC4 (the round's ONE, per the round-3 analysis s.3):** for three named keys -- one that served a block before round 3 and
two that did not -- the derived Model block's 16 added history fields beside the team's own model workbook for that name: do the
figures agree in sign, scale and fiscal year, and is every absent field absent WITH a reason? Evidence laid out: the served
blocks through `scoped_amgt.read_model_block` (`evidence/fwd12_r4_served_blocks_content.txt`); the workbooks are the team's own
files in each research folder. Suggested keys, the CVO's to change: `2317_TT_Equity` (served before), `ADBE_US_Equity`,
`ASML_NA_Equity` (the probe batch).

## 5. Enrichment candidates for the round-4 analysis (`1.0.0_SA_CTO~Z`)

1. **Z-S36:** `dossier.model_rows` reads the newest derived block (the served reader's own rule), names it in inputs, and takes
   an absent reason from the block's unresolved record, never a constant; then one `dossier --write`, verified by model_rows
   with a value on the 89 keys carrying a block.
2. **A seam probe drives the WRITE path it certifies** (Z-S34: AC2 exercised a sibling `--disclosure` branch).
3. **A hard-coded absent reason goes stale silently** when the thing it says is missing arrives (Z-S36); reasons belong to the data.

## 6. Bounds and residue

AMGT only; no library write; no S3 delete; no shared push (`0.0.0_AB_MSTR~Z` integrates). No worktree residue (all three round-4
worktrees removed, branches deleted). Nothing is running and nothing is half-landed.
