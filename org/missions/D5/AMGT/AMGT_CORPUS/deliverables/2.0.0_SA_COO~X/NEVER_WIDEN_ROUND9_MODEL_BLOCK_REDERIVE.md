# AMGT_CORPUS round 9 -- never-widen pair for the model-block re-derive under `case_rule.py` (cell CRPS-k-2, an issuer act)

COO half below, signed by the issuer `2.0.0_SA_COO~X`. The CTO half is owed by `1.0.0_SA_CTO~Z` in its own lane
(`org/missions/D5/AMGT/AMGT_CORPUS/ledger/`). The gate the round-8 analysis set is MET: change entry
`amgt-combined-uu4-a2-scoped-amgt-timeline-and-adjusted-base-20260929` reads `CLOSED -- nothing stranded -- closed
20260929T021144Z` and its sentinel is removed.

## THE ACT
1. `python -m integrations.bloomberg.research.model_block_pull derive --securities <k1> <k2> <k3>` over the **97** keys in
   `checks/round8/model_block_keys_97.txt`, in invocations of at most 3 (the stage's cap), stopping at the first non-zero rc,
   reading raw already landed (no pull, no vendor call). Code at CLOUD HEAD with `case_rule.py` unchanged since `b56fef3032`
   and `model_block_pull.py` at `6a176cc9c4`'s selection (inert on this population, row `Z-W3-S6`).
2. **The follow-on this act forces:** every dossier's `inputs` carries its name's model-block entry (`_model_block_entry`:
   the stored block's content hash), so each new block changes that name's dossier inputs. `dossier --write --workers 10`
   then writes one more object per name (95 puts) so the served dossier reads the re-derived block. Same pair, second act.
A change entry opens before act 1 and closes with content proof of both.

## WRITER CENSUS -- one writer
`derived/model_block/` is written only by `model_block_pull derive`. The stored newest stamps are this seat's: 94 at
`20260926` (round 7 act A), 2 at `20260919` (6861_JP, CSL_AU), 1 at `20260911` (NVDA_US); no commit since 09-26 by any seat
records a model-block derive. N = 1 rule read: `case_rule.compute_cases` via `_compute_cases`.

## BEFORE-STATE -- the SERVED plane (measured 2026-09-29 ~02:2xZ; `evidence/r9_k2_blocks_before.txt`, instrument
`checks/round9/k2_blocks_state.py`, the newest `model_block.json` per key)
`blocks keys 97 served 51 absent 45 nocases 1`. **Note:** the round-8 analysis quotes "49 -> 69"; 49 was `cases-report`
under the round-7 rule, which already read 6861_JP and CSL_AU ABSENT while their stored pre-guard blocks still SERVE. The
served plane is 51.

## EXPECTED OUTCOME, READ FROM THE PRODUCER'S OWN RULE (`cases-report` over the 97 at HEAD, read-only;
`evidence/r9_k2_expected_cases_report_20260929T021453Z.log`) -- every branch named
- **SERVED after: 69.** ABSENT 28 (currency_mismatch and "no adjusted P/E history" / "no consensus EPS" causes).
- **SERVED -> ABSENT: 3 -- 6861_JP_Equity, CAT_US_Equity, CSL_AU_Equity** (reason: "no adjusted P/E history on the landed
  block"; row `Z-W3-S6`: no landed stamp carries `IS_COMP_EPS_ADJUSTED`; no GAAP fallback, analysis s.2 ruling 3).
- **ABSENT -> SERVED: 21** (8035_JP, 8306_JP, 8316_JP, 8766_JP, 9433_JP, CLX_US, COST_US, GPN_US, HD_US, HEI_US, ICICIBC_IN,
  IMB_LN, INTU_US, NFLX_US, NKE_US, NOW_US, SNPS_US, SSE_LN, ST_SP, V_US, WDAY_US).
- **SERVED -> SERVED: 48, every one at a different ratio** (adjusted basis).
- **NOCASES -> ABSENT: 1** (NVDA_US: "no consensus EPS on the landed block").
- **ABSENT -> ABSENT: 24.**

## AFTER-STATE THE VERIFY READS (content, not rc)
1. `k2_blocks_state.py <expected log>`: `blocks keys 97 served 69 ...` and `verify keys 97 match 97 mismatch 0` (status and
   ratio per key equal the rule's expected line).
2. After the follow-on: `dossier_order_census.py` `objects` = before + 95, `read_dossier serves the last write 95 of 95`;
   `dossier --pick-census stale_pick 0`; `dossier --case-census` unchanged (cases come from the packs, not the blocks).

## BLAST RADIUS AND ROLLBACK
- **Touches:** 97 new `model_block.json` objects at new stamps (gold never overwrites; prior stamps stay) and 95 new dossier
  objects. No delete.
- **Readers of a stored block's `cases`:** none on the served page -- `scoped_amgt._model_cases` recomputes cases from the
  block's FIGURES through the same `case_rule.compute_cases` (deployed in the combined act), so the page already shows this
  rule; the re-derive aligns the stored `cases` with it. Readers of the figures (the page, the dossier's model rows) read
  figures derived from the newest landed raw, which is what `cases-report` read.
- **Rollback:** code-and-rewrite, same day: readers take the NEWEST stamp, so a rollback is a re-derive under the reverted rule
  (a newer stamp), not a delete; the dossier follows by its own rewrite.

## STOP LIMBS
1. Any derive rc != 0 -> stop; the keys before it are derived and consistent per key.
2. Verify line 1 reads `mismatch` > 0 -> stop; name the keys; do not run the follow-on.
3. A SERVED -> ABSENT key other than the three named -> stop.

**COO HALF: SIGNED.** `2.0.0_SA_COO~X`, 2026-09-29, against `case_rule.compute_cases` and `model_block_pull` as they stand at
CLOUD HEAD after `6a176cc9c4`. If either moves before the act, this half does not travel with it.
