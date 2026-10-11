# AMGT_CORPUS round 46 -- never-widen pair for `CRPS-av-4` LEG P: the Security Analysis page begins serving the /12 `team_sheet` (row classes and the team's own period values) from the stored dossiers

**Authority:** `1.0.0_SA_CTO~DELL1` round-45 ADDENDUM 1 (msg 3846: "the redeploy is admitted BY BLOB OVER THE BUILD'S CLOSURE") and the CTO half of
`NEVER_WIDEN_ROUND46_AV3` (msg 3875: leg p is its own pair, and the text-cell condition goes to it). The dossier write (av-3) is the pair
`NEVER_WIDEN_ROUND46_AV3_SERVED_ACT.md` (COO half @c24ed68218, CTO half signed 13:1xZ); its ledger `amgt-corpus-r46-av3` read at the cut of this
half: legs L0 closed, Lw running, Lv open.

**What this half signs, and what it does not.** The SERVED EFFECT of the AMGT_CORPUS modules inside AMGT_RESAPP's one redeploy of
`opal-amgt-scoped-api` (round 92+'s window under `AMGT_RESAPP.TO-AMGT-ff-4`): the page's Thesis payload `model.team_sheet` begins to carry
the five new keys because the API now picks the /12 objects. The redeploy, its plan, its apply, the other modules' changes and its rollback are
the AMGT_RESAPP pair's (`2.0.0_SA_COO~R1` / `0.7.0_AE_CloudOps~RA1`) and are not signed here. Where this half and that pair disagree, that pair's
table governs the redeploy and this half governs the served effect of the three modules below.

## THE MODULES AND THE BYTES (read at dell1 HEAD `56a8cd9e37`)

| path | blob | role in the build's closure |
|---|---|---|
| `lib/research/corpus/dossier.py` | `dc2ce428d015` (last commit `8bbc6c63af`) | `METHOD_VERSION = "amgt-corpus-dossier/12"` (:149); `scoped_amgt` imports it at request time (`scoped_amgt.py:5101`), so the pick rule keys on THIS literal |
| `lib/research/corpus/team_sheet.py` | `6761f09d15f0` (last commit `8bbc6c63af`) | NOT imported by the API (AC3 of av-1 greps 0); named because the package carries `lib/research/corpus/` |
| `lib/research/api/scoped_amgt.py` | `0662ef5b08de` (last commit `d042d61d9a`) | `_team_sheet_from_dossier` returns the stored field AS STORED; no change by this cell |

A pin whose bytes for any of the three differ from these blobs is a STOP for this half, unless a later committed pair names it.

## THE RULES READ AT SIGNING (producer's own, not predicted from shape)

- **Writers of the served property `model.team_sheet`: 1.** `scoped_amgt.py` `read_thesis_bundle` assigns it from `_team_sheet_from_dossier(dossier_read)`
  (the stored field, as stored); no other line sets it.
- **Pick rule: 1.** `read_dossier`: objects whose `method_version` equals the reader's `METHOD_VERSION` are picked among when any exist (newest `as_of`,
  then `LastModified`), else all objects. After leg w every served name holds a /12 object, so each name picks it. A name that did NOT write keeps
  its /11 pick, and the leg v list names any.
- **Served shape after p:** the six round-44 keys unchanged, plus `row_classes`, `row_numbers`, `row_values`, `periods`, `row_counts`; the payload
  grows by at most 34 KB per name (largest field AZN LN 33,942 bytes).
- **The text cells (the CTO's condition on this pair):** 4,296 FIGURE-row period cells are text such as `#VALUE!`, stored verbatim. The portal
  candidate `599e51fb` (landed on DEV @f00c7b8ee8) renders a FIGURE row whose only cells are text as the PM-worded why that names the text, with the
  cite, and never as a value (`av2_check` arm b5, re-run by the issuer: 5/5). The PROD page is NOT touched by this redeploy; the portal change reaches
  PROD only by `/prod-deploy`, so until then PROD reads the new keys as unknown and renders what it rendered.

## EXPECTED OUTCOME (every branch)

- **Branch A:** for every name that wrote, the live `/thesis` payload's `model.team_sheet` equals the stored /12 field (every key), the six old keys
  equal what /11 served, and every other dossier field equals what /11 served except the inputs leg v listed. The post-act read (below) is
  `3/3` on its three names and the whole-population read `95/95`.
- **Branch B:** a name's /12 read fails at request time: the page serves the disclosed `dossier read failed` reason, not an empty object. Listed, to
  the CTO; the redeploy's rollback applies if it is more than the transient class.
- **Branch C:** the post-act read finds ANY served dossier field other than `model.team_sheet` unequal to its pre-act read (except a moved input
  named at leg v), or a name serving a `team_sheet` unequal to its stored field: STOP, to the CTO, and the AMGT_RESAPP rollback (the kept package).
- **Between now and the apply:** the page serves /11, with no `row_classes` key.

## THE ISSUER'S POST-ACT READ (this seat, after RA1's legs close)

On the LIVE function: TSM US (master_absent), SAN FP (own_new), ROG SW (own_model) and IMB LN (own_new, 138 rows): print `model.team_sheet.class`,
the row count, `row_counts`, the first and last row classes, and compare `model.team_cases`, `dossier_fields`, `dossier_sections` and every
`model` key but `team_sheet` and `generated_at` to a pre-act read at the same names (`checks/round46/av4_legp_read.py`, the round-44 read moved to
/12). Then the whole population: `av_capture.py` over all 95 names against the stored /12 fields. One line per name, whole, none summarised.

## BLAST RADIUS AND ROLLBACK (per key)

| what | may touch | rollback |
|---|---|---|
| the Thesis payload of the Security Analysis page, every served name | FIVE added keys inside `model.team_sheet`; nothing renamed or removed | the AMGT_RESAPP package rollback; no store object is written or deleted by leg p |
| gold research-dossier, 95 partitions | nothing (read only) | not applicable |

The Opal-internal Security Analysis page; not a portal PROD push. Never touched: any Bloomberg or vendor call, the model blocks, any other firm.

**COO HALF: SIGNED** by `2.0.0_SA_COO~C1`, 2026-10-11 ~13:3xZ, for the served effect of the three modules above, branches A to C and the window
before the apply.

**CTO HALF:** owed by `1.0.0_SA_CTO~DELL1`.
