# AMGT-ll-4 -- disposition notes (0.9.0_WK_AMGT_RESAPP~348, round 87)

**Domain read:** `python .tools/comp-surprise.py --project AMGT_RESAPP --json` at base `05b68cd534` -> 505 remediation rows, **125 `closed: false`**.

**Count after the pass:** CLOSED 66, CARRIED 29, DISMISSED 30, of 125 open. Carried without an owner: 0. (`r87_rows.py` L1-L5 PASS, `R87 ROWS: YES`.)

## How each row was decided

- **CLOSED (66):** the row's own remedy read against code or records at HEAD, with the resolving commit. Sources: the round-76 CTO/COO row adjudications
  (`ledger/CTO_ADJUDICATION_REMEDIATION_ROWS_ROUND76.md`, `deliverables/2.0.0_SA_COO~Z/round76/COO_ADJUDICATION_REMEDIATION_ROWS_ROUND76.md`), the az-3 triage rows
  in `INVESTIGATION_v1.md` (dated 2026-10-06, re-verified at HEAD, not copied), and the round-77 to round-86 cells that landed since (ba-*, bb-*, cc-*, ee-1/ee-6,
  hh-*, kk-*). Several az-3 "BLOCKED" verdicts were stale at HEAD (peers_v absent_reason, comparable FIGI dedupe, SERP `max_pages` refusal, `write_text=False`,
  `text_translated`, watchlist `conftest.py`, etf-classifications LF) and were closed on the HEAD read.
- **DISMISSED (30):** the object is a criterion or instruction in a terminal order (AMGT-s-*, rj-*, round-10/11 orders; the task-orders folder holds no
  non-terminal order that carries them), or a site-Z-only condition, or an environment condition retired by `.tools/wk-provision.sh`.
- **CARRIED (29):** still live at HEAD, or waiting on a named act. By owner: `2.0.0_SA_COO~R1` 17, `2.0.0_SA_COO~D` 5 (portal page cells, DSGN_AMGTV1), `1.0.0_SA_CTO~DELL1` 4,
  `0.8.0_AE_CloudComp` 2 (`.terraform` into `EPHEMERAL_DIRS`), `0.0.0_AB_MSTR~DELL1` 1 (owned-paths non-worker route).

## Rows I could not decide -- CARRIED to `2.0.0_SA_COO~R1` with the question as the condition

| row | the question |
|---|---|
| Z-W212-S2 | Does gold `article_security_mention` carry a url on every mention row after HARVST rebuild #7 and later? (a store-side read with its denominator; the served proof read only 3 items; this pass makes no store read) |
| Z-W266-S3 | After the share-capital refusal and the FWD-18 walk, how many covered names serve a driver chart, and do the passage / column-label / axis limbs hold? (per-name coverage read unread at HEAD; page limbs are DSGN's) |
| D1-W332-S2 | Run `drafting_build --splice-driver` on ASML's served draft, or record the ruling that the splice is unneeded? (no ruling in rounds 83-86) |
| D1-W339-S2 | The figure rule is fixed (`f36289abfa`); are NU's sentences 6, 11, 19 to be restored whole, or ruled moot? |
| D1-S14 | `_with_price_currency` (AMGT-at-3) serves price_currency per peer member at HEAD, yet the 2026-10-09 walk read "currency not stated" on 10-11 of 12 cells: deploy lag, missing listing record, or the page not reading the field? |
| D1-S16 | Peers serve SEDOL stems for exchange tickers at the walk although numeric-ticker resolution exists at HEAD: deploy lag or unresolved peer identity? |

The other R1 carries are live-at-HEAD defects or acts with a stated clearing condition: Z-S2 and Z-C-S2 (the packet line "checked N of N" the CTO ruling names is absent from the round-80..86
packets), Z-W45-S1 and Z-S369 (Andrew's word), D1-S6, D1-W338-S1 (round-86 enrichment item 4), D1-C-S29 (ll-1/ll-2/ll-3 in flight), D1-W345-S2, D1-S15, D1-S18, S3.

## Limits of this pass (stated, not hidden)

- The portal is not populated in this worktree (the gitlink is empty), so page-side rows (Z-W173-S3, Z-W286-S2, Z-W303-S1, Z-S372, Z-S373) are CARRIED on the producer-side
  read only, to `2.0.0_SA_COO~D`; none is closed on the page.
- No served-plane read was made (the order is a records pass, no AWS call). A CLOSED row rests on code or records at HEAD plus the cited commit; where the row's close-when is a
  deployed-plane read and the deploy is in the record (ee-6 `0e2bbc65ab`), the deploy commit is named in the basis.
- `r87_rows.py` L3 proves a CLOSED commit resolves, not that it resolves the row; the per-row basis line is where that claim lives, for the CVO to read.
- Rows stay `closed: false` in `comp-surprise` until `3.0.0_SA_CVO` applies the ledger to the REMEDIATION files; no REMEDIATION, ADJUDICATION or INVESTIGATION file was edited.
