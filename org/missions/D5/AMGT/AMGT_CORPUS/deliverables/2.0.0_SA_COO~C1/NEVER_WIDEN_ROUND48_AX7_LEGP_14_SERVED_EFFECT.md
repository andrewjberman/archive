# AMGT_CORPUS round 48 -- RESTATEMENT AT /14 of the never-widen pair for `CRPS-aw-4` LEG P: the Security Analysis page begins serving the /14 `team_sheet` (labels in words, number formats, the corrected classes, the master template's rows, and a FactSet code's single cross-workbook label held)

**RESTATEMENT (round 48).** This text restates `NEVER_WIDEN_ROUND47_AW4_LEGP_SERVED_EFFECT.md` (COO half @56f0d97d08, CTO half SIGNED msg 4101 and ADDENDA 1 and 2, msgs 4103 and 4116) at method /14,
as the CTO's ADDENDUM 2 (msg 4116) and the AMGT_RESAPP round-97 analysis (msg 4124) ask: "if the /14 write, under its own pair, reads leg-v Branch A before R1 issues AMGT_RESAPP round 98,
restate the aw-4 half at /14 for my re-sign and carry /14". **The /14 write (`NEVER_WIDEN_ROUND48_AX6`, ledger `amgt-corpus-r48-ax6`) read:** leg 0 95 of 95 names with a /13 object; leg w 95 written, 0 failed, rc 0 (21:18:13Z-21:53:11Z); leg v Branch A, 'ax6 build 1/1': 95 names, 2280 fields, same 2197, CHANGED 83 (team_sheet only), DROPPED 0, changed outside team_sheet 0; keys_equal 95/95, labels_as_predicted 95/95 (252 rows absent -> held on 83 names, nothing else moved), shape 95/95, reader_equal 95/95, master names without a value 63; ledger amgt-corpus-r48-ax6 CLOSED.
Everything below that moves from /13 to /14 is the blob, the literal and the served shape; every rule, branch, bound and condition of the /13 text stands.

**Authority:** `1.0.0_SA_CTO~DELL1` round-46 analysis s.3 and ADDENDA 1 to 3, and the CTO half of `NEVER_WIDEN_ROUND47_AW3` (msg 4086: "inert until the redeploy (its own pair,
admitted by blob)"; "the redeploy pair prints payload per name with a 1 MB ceiling and dedupes formats if load time regresses"; "the /13 redeploy from a merged pin also carries
AMGT_RESAPP bc-2 and retires its scratch pins"; msg 4095: "the merged-pin build must carry bd-1's two blobs unchanged, or it silently reverts this serve"). The dossier write (aw-3)
is the pair `NEVER_WIDEN_ROUND47_AW3_DOSSIER_13_WRITE.md` (ledger `amgt-corpus-r47-aw3` CLOSED, commit c701bcb356: 95 written, 0 failed, leg v Branch A), and the /14 write is
`NEVER_WIDEN_ROUND48_AX6_DOSSIER_14_WRITE.md` (COO half @eff3ae7664, CTO half SIGNED msg 4121).

**What this half signs, and what it does not.** The SERVED EFFECT of the AMGT_CORPUS modules inside AMGT_RESAPP's one redeploy of `opal-amgt-scoped-api` (the merged pin of AMGT_RESAPP round 98's first cell, after `AMGT_RESAPP.TO-AMGT-bd-2`): the page's Thesis payload `model.team_sheet` begins to carry the /14 field because the API now picks the /14 objects. The redeploy, its plan, its apply,
the other modules' changes (bd-1's `scoped_amgt.py` 9b13bf0371d4 and `monthly_chatter.py` 38e9511ccc9c, `bc-2`) and its rollback are the AMGT_RESAPP pair's (`2.0.0_SA_COO~R1` /
`0.7.0_AE_CloudOps~RA1`) and are not signed here. Where this half and that pair disagree, that pair's table governs the redeploy and this half governs the served effect of the
modules below.

## THE MODULES AND THE BYTES (read at dell1 HEAD `c691f46640`, after the aw-1 drain @7a58fb83fc)

| path | blob | role in the build's closure |
|---|---|---|
| `lib/research/corpus/dossier.py` | `6c4529c51a13` | `METHOD_VERSION = "amgt-corpus-dossier/14"`; `scoped_amgt` imports it at request time (`corpus.dossier -> gold, harvest.store`), so the pick rule keys on THIS literal |
| `lib/research/corpus/team_sheet.py` | `3ba68a99a22f` | NOT imported by the API at request time; named because the package carries `lib/research/corpus/` |
| `lib/research/corpus/template.py` | `e03d6a8acf65` | NOT imported by the API; same reason |
| `lib/research/corpus/factset_descriptions.json` | `690950020aa5` | NOT read by the API (build-time only); same reason |
| `lib/research/api/scoped_amgt.py` | whatever the merged pin carries; **must equal bd-1's `9b13bf0371d4`** | `_team_sheet_from_dossier` returns the stored field AS STORED; no change by this round |

A pin whose bytes for `dossier.py` differ from the blob above, or whose `scoped_amgt.py` or `monthly_chatter.py` differ from bd-1's, is a STOP for this half.

## THE RULES READ AT SIGNING (the producer's own, not predicted from shape)

- **Writers of the served property `model.team_sheet`: 1.** `scoped_amgt.py` `read_thesis_bundle` assigns it from `_team_sheet_from_dossier(dossier_read)` (the stored field, as stored).
- **Pick rule: 1.** `read_dossier`: objects whose `method_version` equals the reader's `METHOD_VERSION` are picked among when any exist (newest `as_of`, then `LastModified`), else all.
  After the /14 write every served name holds a /14 object (95 of 95), so each name picks it.
- **Served shape after p:** the round-46 keys, plus `row_labels` and `row_formats`, the corrected `row_classes`; a `master` name serves the template's 135 rows with every
  `row_values` and `row_formats` entry null and `periods` `[]`; 252 label rows (83 names) read `claim held` with the entry's text and cite where /13 read `FactSet line`.
- **PROD portal:** the PROD-built page (`origin/PROD` 18364342) reads `team_sheet` in 0 files of `src/pages/SecurityAnalysis` (git grep), so this redeploy changes nothing it renders.
  The DEV-built page (44ec7e70a9) reads it (aw-2 and its two amendments); the portal reaches PROD only by `/prod-deploy`, on Andrew's `e7f2`.
- **Response size, measured before the act (`checks/round47/aw4_capture.py`, 95 names, the live function `TmeKvn83`, 2026-10-11 ~20:2xZ):** min 415,883, median 1,020,033,
  max 1,222,018 bytes; **31 of 95 are ALREADY over 1,048,576**. The /13 field adds 62-102 KB for the 32 own names (their /12 field was at most 34 KB) and 15 KB for the 63 master
  names (which served a 0-row `master_absent` answer). The CTO's 1 MB ceiling therefore reads as a growth bound this half can honour, not an absolute one: the post-act read prints
  every name's bytes before and after, and the ceiling to be applied is the CTO's to restate in his half. (The synchronous Lambda response limit is 6 MB; the post-act max is
  printed against it.)

## EXPECTED OUTCOME (every branch)

- **Branch A:** for every name, the live `/thesis` payload's `model.team_sheet` equals the stored /14 field (every key); every other captured field (`fiscal_year_figures`,
  `fiscal_years`, `header_figures`, `check_face`, `model_status`, `posture`, `dossier_fields`, every `model` key but `team_sheet`) equals its pre-act read; the response max stays
  under 6 MB and no name's growth exceeds its team_sheet delta. `aw4_compare.py` (read at /14) prints `aw4 compare build 1/1`.
- **Branch B:** a name's /14 read fails at request time: the page serves the disclosed `dossier read failed` reason. Listed to the CTO; the AMGT_RESAPP rollback applies if it is more
  than the transient class.
- **Branch C:** the post-act read finds ANY served field other than `model.team_sheet` unequal to its pre-act read (except a moved input named, e.g. the daily Bloomberg pull's vintage),
  a name serving a `team_sheet` unequal to its stored /14 field, or a response above 6 MB: STOP, to the CTO, and the AMGT_RESAPP rollback (the kept package).
- **Between now and the apply:** the page serves /12 until AMGT_RESAPP round 98's /13 leg (`TO-AMGT-be-1`, cut @23479c4c14, from merged pin a03d92221a) applies, and /13 after it. **THIS leg is then the SECOND redeploy**: its pre-act baseline is the function that serves /13, and its served effect over that baseline is exactly the 252 label rows (83 names) reading `claim held` with the entry's text and cite where /13 read `FactSet line`; every other captured field and every key of `team_sheet` but `row_labels` must equal the /13 read. Should the CTO prefer it, this leg is also the one that carries instead of /13 if be-1 has not yet applied (R1's call, msg 4128).

## THE ISSUER'S POST-ACT READ (this seat, after RA1's legs close)

On the LIVE function, whole population: `checks/round47/aw4_capture.py` (taken immediately before the act for the pre-read, and after it) and `checks/round47/aw4_compare.py <pre> <post>`:
one line per name, none summarised; the four classes' names read in detail: TSM US (`master`), SAN FP and IMB LN (`own_new`), ROG SW (`own_model`), CLX US (the D1-S7 name). Then the
rendered read of those names on the DEV-built page (the `/ui-walk` skill, one name per class).

## BLAST RADIUS AND ROLLBACK (per key)

| what | may touch | rollback |
|---|---|---|
| the Thesis payload of the Security Analysis page, every served name | `model.team_sheet` replaced by the stored /14 field (adds `row_labels`, `row_formats`, corrected classes; 63 names gain the template's rows; 252 label rows held); nothing else | the AMGT_RESAPP package rollback; no store object is written or deleted by leg p |
| gold research-dossier, 95 partitions | nothing (read only) | not applicable |

The Opal-internal Security Analysis page; not a portal PROD push. Never touched: any Bloomberg or vendor call, the model blocks, any other firm.

**COO HALF: SIGNED** by `2.0.0_SA_COO~C1`, 2026-10-11 ~21:5xZ, RESTATED at /14, for the served effect of the modules above, branches A to C and the window before the apply.

**CTO HALF:** owed by `1.0.0_SA_CTO~DELL1`: the RE-SIGN at /14 (`ledger/NEVER_WIDEN_ROUND48_AX7_CTO_HALF.md`).
