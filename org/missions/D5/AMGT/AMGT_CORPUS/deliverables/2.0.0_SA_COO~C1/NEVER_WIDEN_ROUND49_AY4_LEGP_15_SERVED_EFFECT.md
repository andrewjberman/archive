# AMGT_CORPUS round 49 -- never-widen pair for `CRPS-ay-4` LEG P at /15: the Security Analysis page begins serving the /15 `team_sheet` (every value under the header of its own block)

**Authority:** `1.0.0_SA_CTO~DELL1` round-48 analysis ADDENDUM 1 (msg 4165) and the CTO half of `NEVER_WIDEN_ROUND49_AY3` (msg 4176: "R1: carry /15 only if its leg v reads A and my re-sign of the /15 leg p lands before you cut
round 99; otherwise /14 as signed. Do not hold round 99."). **What the /15 write read** (`NEVER_WIDEN_ROUND49_AY3_DOSSIER_15_WRITE.md`, ledger `amgt-corpus-r49-ay3` CLOSED, commit 9993c4810d): leg 0 95 of 95 names with a /14 object;
leg w 95 written, 0 failed, rc 0 (23:50:35Z-00:25:13Z); leg v Branch A, `ay3 build 1/1`: 95 names, 2,280 fields, same 2,185, CHANGED 95 (`team_sheet` only), DROPPED 0, changed outside `team_sheet` 0; `team_sheet_ok 95/95`;
`reader_equal 95/95`; master names without a value in any block 63/63; unread blocks without a value 12/12; 3,103 BLOCK rows = period 401 + case 2,690 + unread 12; 357 blocks; 35 withheld cells; 0 headerless values.

**Where this leg sits.** Round 99 (`AMGT_RESAPP.TO-AMGT-bf-1`) has its GO at /14 (CTO half msg 4184, pin b3d4856531, "/15 not carried"). THIS leg is the THIRD redeploy of `opal-amgt-scoped-api` after be-1: its baseline is the function that
serves /14 after bf-1's post-act read, and its served effect over that baseline is exactly the /15 delta below. If the CTO instead rules that a not-yet-applied round 99 carries /15, the baseline is the /13-serving function and the effect
is the /14 delta (`NEVER_WIDEN_ROUND48_AX7`, 252 label rows held) plus this delta; the rules, branches and bounds below are the same.

**What this half signs, and what it does not.** The SERVED EFFECT of the AMGT_CORPUS modules inside AMGT_RESAPP's redeploy of `opal-amgt-scoped-api`: the page's Thesis payload `model.team_sheet` begins to carry the /15 field because
the API now picks the /15 objects. The redeploy's mechanics, the other modules' changes and its rollback are the AMGT_RESAPP pair's (`2.0.0_SA_COO~R1` / `0.7.0_AE_CloudOps~RA1`) and are not signed here. Where this half and that
pair disagree, that pair's table governs the redeploy and this half governs the served effect of the modules below.

## THE MODULES AND THE BYTES (committed blobs at dell1 HEAD `9993c4810d`)

| path | blob | role in the build's closure |
|---|---|---|
| `lib/research/corpus/dossier.py` | `7b67bf62afdd` | `METHOD_VERSION = "amgt-corpus-dossier/15"`; `scoped_amgt` imports it at request time, so the pick rule keys on THIS literal |
| `lib/research/corpus/team_sheet.py` | `ef4da7cdc85a` | NOT imported by the API at request time; named because the package carries `lib/research/corpus/` |
| `lib/research/corpus/template.py` | `e03d6a8acf65` | NOT imported by the API; same reason |
| `lib/research/corpus/factset_descriptions.json` | `690950020aa5` | NOT read by the API (build-time only); same reason |
| `lib/research/api/scoped_amgt.py` | whatever the merged pin carries; **must equal bd-1's `9b13bf0371d4`** | `_team_sheet_from_dossier` returns the stored field AS STORED; no change by this round |

A pin whose bytes for `dossier.py` differ from the blob above, or whose `scoped_amgt.py` or `monthly_chatter.py` differ from bd-1's, is a STOP for this half.

## THE RULES READ AT SIGNING (the producer's own, not predicted from shape)

- **Writers of the served property `model.team_sheet`: 1.** `scoped_amgt.py` `read_thesis_bundle` assigns it from `_team_sheet_from_dossier(dossier_read)` (the stored field, as stored).
- **Pick rule: 1.** `read_dossier`: objects whose `method_version` equals the reader's `METHOD_VERSION` are picked among when any exist (newest `as_of`, then `LastModified`), else all. After the /15 write every served name holds a
  /15 object (95 of 95), so each name picks it.
- **Served shape after p:** the round-46/47 keys; `row_classes` gains `"BLOCK"` on 3,103 rows (own 709, master 2,394) whose `row_values` and `row_formats` are null; `row_counts` gains `BLOCK`; `blocks` (357) carries each block's `kind`,
  `why`, `withheld`, `columns` and the sheet's own header and body rows verbatim; an `unread` block (12) carries no cell; a master answer's blocks carry no figure. Nothing else in `team_sheet` moves (labels, row numbers, periods,
  class, workbook, sheet are equal to /14).
- **PROD portal:** the PROD-built page (`origin/PROD` 37aa1247) reads `team_sheet` in 0 files of `src/pages/SecurityAnalysis`, so this redeploy changes nothing it renders. The DEV-built page (DEV 46926677c1, CRPS-ay-2 landed) renders
  `blocks`; the portal reaches PROD only by `/prod-deploy`, on Andrew's `e7f2`.
- **Response size, measured (`checks/round47/aw4_capture.py`, live `mbGRmy1H`, 2026-10-11 22:16Z):** min 430,667, median 1,035,671, max 1,289,805 bytes. The /15 `team_sheet` is 4,501,078 bytes over 95 names (the /14 field is
  3,639,504); the largest per-name growth is 13,247 bytes (AZN LN 102,438 -> 115,685). The CTO's bound (msg 4101) holds as written: growth no more than each name's own `team_sheet` delta, and the maximum under 6 MB (margin printed).

## EXPECTED OUTCOME (every branch)

- **Branch A:** for every name, the live `/thesis` payload's `model.team_sheet` equals the stored /15 field (every key); every other captured field (`fiscal_year_figures`, `fiscal_years`, `header_figures`, `check_face`, `model_status`,
  `posture`, `dossier_fields`, every `model` key but `team_sheet`) equals its pre-act read; the response max stays under 6 MB and no name's growth exceeds its `team_sheet` delta. `ay4_compare.py` prints `ay4 compare build 1/1`.
- **Branch B:** a name's /15 read fails at request time: the page serves the disclosed `dossier read failed` reason. Listed to the CTO; the AMGT_RESAPP rollback applies if it is more than the transient class.
- **Branch C:** the post-act read finds ANY served field other than `model.team_sheet` unequal to its pre-act read (a moved input named, e.g. the daily Bloomberg pull's vintage, excepted), a name serving a `team_sheet` unequal to
  its stored /15 field, or a response above 6 MB: STOP, to the CTO, and the AMGT_RESAPP rollback (the kept package).
- **Between now and the apply:** the page serves /13 (be-1) and /14 after bf-1; the /15 objects are stored and picked by nobody.

## THE ISSUER'S POST-ACT READ (this seat, after RA1's legs close and R1's relay)

On the LIVE function, whole population: `checks/round47/aw4_capture.py` (the pre-read is the capture of the function that serves the prior method, taken after its own redeploy and unchanged since) and
`checks/round49/ay4_compare.py <pre> <post>`: one line per name, none summarised. Then, on the DEV-built page: the rendered census (`aw6_rendered_census.cjs` against the live payloads), and three browser walks: a name with a
second PERIOD block (AZN LN), a name with a CASE block (ROG SW), and a master template (TSM US). No capture runs on the function between the GO and R1's relay.

## BLAST RADIUS AND ROLLBACK (per key)

| what | may touch | rollback |
|---|---|---|
| the Thesis payload of the Security Analysis page, every served name | `model.team_sheet` replaced by the stored /15 field (3,103 rows move into `blocks`; labels, numbers, values of every other row unchanged); nothing else | the AMGT_RESAPP package rollback (to the /14 or /13 package); no store object is written or deleted by leg p |
| gold research-dossier, 95 partitions | nothing (read only) | not applicable |

The Opal-internal Security Analysis page; not a portal PROD push. Never touched: any Bloomberg or vendor call, the model blocks, any other firm.

**COO HALF: SIGNED** by `2.0.0_SA_COO~C1`, 2026-10-12 ~00:4xZ, for the served effect of the modules above, branches A to C and the window before the apply.

**CTO HALF:** owed by `1.0.0_SA_CTO~DELL1`: `ledger/NEVER_WIDEN_ROUND49_AY4_CTO_HALF.md`.
