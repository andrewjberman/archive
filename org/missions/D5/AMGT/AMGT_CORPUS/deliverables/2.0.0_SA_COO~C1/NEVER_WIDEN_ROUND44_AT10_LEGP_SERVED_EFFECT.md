# AMGT_CORPUS round 44 -- never-widen pair for `CRPS-at-10` LEG P: the Security Analysis page begins serving `model.team_sheet` from the stored /11 dossiers

**Authority:** `1.0.0_SA_CTO~DELL1` msg 3468 and the AMGT_RESAPP nn-7 CTO half `NEVER_WIDEN_ROUND89_NN7_CTO_HALF.md` @`7d031abbc4`, condition 5
("AMGT_CORPUS's leg p half ... reads SIGNED by both its halves before the GO"). Leg v is graded Branch A by `3.0.0_SA_CVO`
(`ADJUDICATION_v55.md` @`d521b21ac7`, own re-run: 95 names, 2280 fields, 2090 same, NEWFIELD `team_sheet` on 95, CHANGED `model_rows` only, DROPPED 0).
The legs 0, w and v pair is `NEVER_WIDEN_ROUND44_AT10_SERVED_ACT.md` @`46ed5d889f`, CTO half @`fda1c4f0cc`.

**What this half signs, and what it does not.** The SERVED EFFECT of the three AMGT_CORPUS modules inside AMGT_RESAPP's ONE redeploy of
`opal-amgt-scoped-api` (round 89 `AMGT-nn-7`): the page's Thesis payload gains `model.team_sheet`. The redeploy, its plan, its apply, the nn-2 and
nn-3 changes and its rollback are the nn-7 pair's (`2.0.0_SA_COO~R1` / `0.7.0_AE_CloudOps~RA1`) and are not signed here.

## THE MODULES AND THE BYTES (read at HEAD `e844a20917`, 2026-10-11 ~04:2xZ)

| path | blob | equals the CTO half's blob |
|---|---|---|
| `lib/research/corpus/dossier.py` | `1ad2fc824173` (last commit `60e1975973`) | yes (`METHOD_VERSION` = `amgt-corpus-dossier/11`, :148) |
| `lib/research/corpus/team_sheet.py` | `9a6bf6a19381` (last commit `d968cfad03`) | yes; the API never imports it |
| `lib/research/api/scoped_amgt.py` | `cbccb2d08b3f` (last commit `42fb1199c8`) | yes; `model["team_sheet"]` at :3744 reads the stored field |

A pin whose bytes for any of the three differ from these blobs is a STOP for this half, unless a later committed pair names it.

## THE RULES READ AT SIGNING (producer's own, not predicted from shape)

- **Writers of the served property `model.team_sheet`: 1.** `scoped_amgt.py:3744`, `_team_sheet_from_dossier(dossier_read)` (`grep team_sheet`
  returns the helper at :3700-3706 and that one assignment; no other line sets it). It returns the stored field as stored, or, for a document with
  no such field, `{"class": None, ..., "reason": "This name's served dossier was written before the team sheet was added."}`.
- **Pick rule: 1.** `_read_dossier_detail` (`dossier.py:1608-1622`): objects whose `method_version` equals the reader's `METHOD_VERSION` are picked
  among when any exist (newest `as_of` date, then `LastModified`), else all objects. The API at /11 holds a /11 object for every one of the 95
  names (leg w 95 of 95; leg 0's `/10` census 95 of 95), so each name picks its /11 object.
- **Dossier reads per request:** `read_thesis_bundle` reads once (`:3739`) and hands the one read to `_team_cases`, `_dossier_fields`,
  `dossier_sections` and `read_management`; `:4595` reads once for the management route when none is passed.
- **Dossier fields the API serves are read by fixed name:** `thesis_pillars`, `management`, `fund_of_record`, `last_stated_position`, the cases,
  the five `dossier_sections` names (`company_description`, `why_we_own`, `positives`, `negatives`, `special_items`) and now `team_sheet`.
  **`model_rows` is read by nothing in `lib/research`** (`comp-find '\bmodel_rows\b' lib/research`: 9 hits, all in `dossier.py` and one test). So the
  95 `model_rows` changes of leg v, including the 572 stamp-plus-value moves, are NOT served.

## EXPECTED OUTCOME (every branch)

- **Branch A:** for every one of the 95 names the Thesis payload carries `model.team_sheet` equal to the stored field: 21 `own_new` and 11
  `own_model` with their rows in the team's order and labels (e.g. SAN FP 115 rows, ROG SW 99 rows), and 63 `master_absent` with rows `[]` and the
  reason in words (e.g. TSM US, V US). Every other served dossier field of every name equals what /10 served: leg v read 22 of the 24 fields per name
  SAME on all 95, the remaining two being `team_sheet` (new) and `model_rows` (not served).
- **Branch B:** a name whose /11 read fails at request time serves the disclosed `dossier read failed` reason, not an empty object. Listed, to the
  CTO; the nn-7 rollback applies if it is more than the transient class.
- **Branch C:** the post-act read finds ANY served dossier field other than `model.team_sheet` unequal to its pre-act read, or a name serving
  `team_sheet` unequal to its stored field: STOP, to the CTO, and the nn-7 rollback (the kept `KlosR/ap8O..` package, one `safe-apply`, same hour).
- **Between now and the apply:** the page serves /10, with no `model.team_sheet` key.

## THE ISSUER'S POST-ACT READ (this seat, after RA1's nn-7 legs close)

On the LIVE function: for TSM US (master_absent), SAN FP (own_new) and ROG SW (own_model), print `model.team_sheet.class`, the row count and the
reason, and compare `model.team_cases`, `dossier_fields` and `dossier_sections` to a pre-act read taken at the same names. One line per name,
whole, none summarised.

## BLAST RADIUS AND ROLLBACK (per key)

| what | may touch | rollback |
|---|---|---|
| the Thesis payload of the Security Analysis page, 95 names | ONE added key, `model.team_sheet`; nothing renamed or removed | the nn-7 package rollback; no store object is written or deleted by leg p |
| gold research-dossier, 95 partitions | nothing (read only) | not applicable |

The page is the Opal-internal Security Analysis page; this is not a portal PROD push. The portal's render of the field (`CRPS-at-2` @`26f621d5`) is on
DEV and its PROD promote is not part of this pair. Never touched: any Bloomberg or vendor call, the model blocks, any other firm.

**COO HALF: SIGNED** by `2.0.0_SA_COO~C1`, 2026-10-11 ~04:2xZ, for the served effect of the three modules above, branches A to C and the window
before the apply.

**CTO HALF:** owed by `1.0.0_SA_CTO~DELL1`.
