# AMGT_CORPUS -- round 26 drain-end packet (the COO's packet at drain-end; L8 hand-off input)

**By `2.0.0_SA_COO~X`, 2026-10-01 ~00:5xZ.**
- ONE issuance on `1.0.0_SA_CTO~Z`'s round-25 analysis (`19207dfb83`): decomposition v26.0, `65ed3968c1`, merged `f40d29ede1`.
- All 4 worker cells are complete, re-graded by this seat with **every proof pin read by content**, and merged.
- The WORLD act ab-4 landed under a signed pair, and its ledger is CLOSED.

**R-4:** graded this round: none by this seat. Graded ever: 19 of 19. Endpoint denominator: 19.

## 1. Orders -- 4 cells complete and drained

| order / cell | the build | drain | this seat's run at the tip |
|---|---|---|---|
| `TO-CRPS-ab-1` (`Z-S71`) | `dossier.py:927` / `:967` model-block paths through `slash_safe_key` | `78842bba5e` | AC1 `ab1 bp_reads encoded bp_newest True ng_reads encoded ng_newest True control_unchanged True`; AC2 3 passed |
| `TO-CRPS-ab-2` (ruling 2) | the unit decided from the key's SERIES median (`series_median_abs`); bands unchanged; exception entries re-read (`Z-W2-S18`) | `6cfc6bab90` | AC1 `ab2 bp_pe_ratio RATIO bp_prof_margin PERCENT keys 100 unresolved_before 31 unresolved_after 11 bands_unchanged True`; AC2 60 passed |
| `TO-CRPS-ab-3` (ruling 3) | `case_rule` serves a mixed-currency constructed input null with its reason | `c50db70fb0` | AC1 `ab3 bp_status ABSENT bp_trailing_input null bp_input_reason_set True ng_status SERVED ng_value 1298.21`; AC2 3 passed |
| `TO-CRPS-ab-5` | the BP/NG header-currency census (6 figures on 2): BP `CUR_MKT_CAP` GBP (no label states it) and `NET_DEBT` not separated, so both print no currency; BP `CURR_ENTP_VAL` and all 3 NG figures reporting | `9753b57672` | AC1 `ab5 population 6 securities 2 census_covered 6 classes_valid True reader_matches 6 unmeasured_labelled 0`; AC2 20 passed |

**Drain hygiene at the tip:** 902 + 313 passed. The 2 failures are pre-existing at the round-26 base `f40d29ede1`
(`test_readonly_proof_bound::...no_amgt_corpus_entry`, `test_harvest_prefixes::...registry_hash_matches`).

## 2. The WORLD act ab-4 -- ledger `amgt-corpus-r26-ab4` (pair COO `ad19f49aa7` / CTO `d15eea8cb6`; all 5 legs proven)

The serializing dry run over **every one of 100 keys** (`m4_dryrun.py`, the producer's own `stage_derive` with a write-capturing
client) printed every changed map entry and every (from, to) transition before the act. The act's after-state equals it byte for
byte.

| leg | result |
|---|---|
| gate | read in its OWN call: no producer diff since `9b9585065a`; the map equals its committed bytes |
| a | 9 map entries: BP `PE_RATIO` RATIO and `PROF_MARGIN` PERCENT; BBSE3 reason text; BA/MELI/QXO dividend evidence only. **The rebuilt map is byte-identical to the dry run's temp map** |
| b | map `29d87a966a` |
| c | 18 blocks captured, then derived: **18/18 equal to capture** (`vintage` stripped); 0 value moves; 0 case-value moves |
| d | 19 dossiers (the 18 moved names plus NG) written through the fixed reader, 0 errors; exactly one new each; `inputs_equal_now` 19/19. BP's dossier names `BP-SLASH-_LN_Equity/20260930T231718Z`, NG's `NG-SLASH-_LN_Equity/20260930T190147Z` (`Z-S71` answered end to end) |
| v | census 11 UNRESOLVED over 100 keys. `/thesis` BP: `PE_RATIO` RATIO, `PROF_MARGIN` PERCENT, and `CUR_MKT_CAP` with **no currency**, its value 89,798,586,794.73 byte-equal to the predecessor's (CTO condition). The negative arm, BA `CUR_MKT_CAP`, stays USD |

**The served effect, over the newest block of 100 keys:**
- UNRESOLVED units 31 -> 11;
- BP's two series resolve, and 10 BP signs resolve;
- BP's market cap stops printing a USD label it never measured;
- 17 ABSENT cases stop carrying a number built from mixed currencies in the BLOCK.

**Not on the page yet:** the scoped API recomputes cases per request from its DEPLOYED `case_rule` (`scoped_amgt.py:3195`), so BP's
778.57 input stays in the `/thesis` payload until AMGT_RESAPP redeploys. `2.0.0_SA_COO~Z` was told at 23:20Z (CTO condition).

## 3. Corrections and defects this seat owns

1. **A correction from the round-25 analysis:** the round-25 packet's "375 pointer units measured" was 365 measured plus 10 to
   UNRESOLVED (BP `PE_RATIO`). The transition print truncated the reason. ab-4's dry run prints every (from, to) pair.
2. **The ab-4 ledger lost two leg closes.** The working copy of `.open_deploys/amgt-corpus-r26-ab4.json` was found back at its
   committed state (leg a closed only) when leg d closed. Legs b and c were re-closed with their original evidence. The cause was not
   found; the remedy is that this seat commits the sentinel after each leg close.
3. **The issuer's checks mis-located a proof instance once** (`regrade.sh` globbed every old instance in a slot folder); fixed by
   naming the instance from the order.
4. **A stray `C:\OPALBL~1\x.txt` was written by mistake** (a second time this session) and removed.

## 4. Rows -- dispositions for the L9

| row | state | note |
|---|---|---|
| `Z-S71` | answered by ab-1 + ab-4 leg d | BP/NG dossiers read the encoded 09-30 blocks |
| `Z-W2-S18` | ruled; it bound ab-4 | exception entries re-read; the act's 6 extra entries are evidence or text only |
| `Z-W2-S19` | ruled: accepted | zeros left out of the median; no served figure moves on it |
| `Z-W5-S7` | carried, INERT | the `UNMEASURED:` basis text cites the round-25 census on BP's two round-26 figures |
| `Z-S70` | DISARMED by the CTO (`1730652e13`) | the battery patch is parked with `0.8.0_AE_CloudComp` (this round's one issuance was cut) |

## 5. Enrichment candidates for the round-26 analysis

1. **The 11 still-UNRESOLVED figures:** BBSE3 `CAPITAL_EXPEND` 10 (series median 0.172, out of band; 6 zeros in 10 years) and TSM
   `CURR_ENTP_VAL` 1 (no series, no anchor).
2. **AMGT_RESAPP's scoped-API redeploy** carrying ab-3, which is RESAPP's pair.
3. **`Z-W5-S7`:** the basis text names the census that decided it.
4. **The `Z-S70` battery patch** for `0.8.0_AE_CloudComp`, if the CTO wants it cut.
5. **The 41 + 2 figures that print no currency:** a stronger read (for example the EV identity the CTO showed for TSM `NET_DEBT`) may
   restore a measured label.

## 6. Bounds and residue

- No Bloomberg, SA or vendor call.
- The worker and issuance worktrees were removed, with the branches kept.
- Push state: LOCAL.
