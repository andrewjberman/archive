# AMGT_CORPUS -- round 24 drain-end packet (the COO's packet at drain-end; L8 hand-off input)

**By `2.0.0_SA_COO~X`, 2026-09-30 ~14:2xZ.**
- ONE issuance on `1.0.0_SA_CTO~Z`'s round-23 analysis (`4cbd61daf8`) and slash-key ruling (`c9081e03d6`): decomposition v24.0,
  `43fd463710`, merged `2a251bfeb4`.
- The three worker cells are complete, re-graded by this seat, and merged. z-3 (the r-1 acceptance) was read at the 13:00Z fire.
- The z-1 WORLD act landed under a signed pair, and its ledger is CLOSED.

**R-4:** graded this round: none by this seat. Graded ever: 19 of 19. Endpoint denominator: 19.

## 1. Orders -- 3 cells complete and drained, plus z-3 read

| order / cell | the build | drain | this seat's run at the tip |
|---|---|---|---|
| `TO-CRPS-z-1` | the 602 still-UNRESOLVED served units in 17 classes; families F1-F6 on stated rules (zero samples take the FIELD_BASIS unit; same-currency bands against PX_LAST / CUR_MKT_CAP; the round-21 discriminator inside `build_entries`) | `d342614233` | AC1 `z1 keys 98 excluded 2 measured_before 602 table_total 602 classes 17 dispositions_complete True projected_after 49 table_remaining 49 consistent True`; AC2 38 passed |
| `TO-CRPS-z-2` | the 13-source census for a TSM same-currency anchor finds none; the no-anchor reason now begins "no same-currency anchor stored:" | `92f1403d25` | AC1 `z2 sources_searched 13 anchor none reason_states_limit True fx_invented False census_file True`; AC2 5 passed |
| `TO-CRPS-z-4` | every per-security path through `crosswalk.slash_safe_key` (14 census functions routed, 10 marked, module-constant sites routed too); readers decode both forms | `6d6d142812` | AC1 `z4 sites 14 encoded 14 raw 0 bp_encoded BP-SLASH-_LN_Equity brk_encoded BRK-SLASH-B_US_Equity roundtrip True planted_refuses True`; AC2 76 passed |
| z-3 (issuer read) | the r-1 acceptance: `amgt-induction-daily`'s 13:00Z scheduled fire | -- | LastRunTime 09:00 local (13:00Z), LastTaskResult 0; branch 1 (population 0, 96 registered, 0 calls, 0 puts); crosswalk newest stays `2026-09-29.json`. `evidence/r24_z3_r1_acceptance.txt` |

Drain hygiene at the tip: 394 passed (`integrations/bloomberg/research/tests` + `lib/research/identity/tests`); `field_map.json`
clean after the run.

## 2. The WORLD act -- ledger `amgt-corpus-r24-unit-closures` (all 5 legs proven)

Pair: COO `ab84e2b6df` / CTO `4acf8806ce` (4 conditions). The act-start gate read the closure diff `04b89561ce..HEAD` as empty,
and the map equal to its committed bytes.

| leg | result |
|---|---|
| a | the map rebuild: 84 entries across the 10 named fields, 0 shared, 0 top-level, 0 added, LF only -- exactly the pair's line |
| b | map commit `6caac02338` |
| c | 28 blocks: **28 of 28 match** the per-figure prediction (`m2_measure.py`). 565 unit changes (553 to measured, 12 reason text, 0 measured-to-other); 115 sign changes (103 UNRESOLVED -> POSITIVE, 12 reason text, 0 contradicting their value); 0 value, 0 case, 0 other; `filled_by_sa 0` |
| d | 27 dossiers: exactly one new object per name, 0 other names written; the changed document keys are `fields.model_rows`, `inputs` and `content_sha256` only; inputs equal now on 27 of 27 |
| v | served census over the 98 non-excluded blocks: not-measured units **602 -> 49**. The CTO's condition-3 served read: the deployed `opal-amgt-scoped-api` (CodeSha256 `nKWCfQRQ...`, ab-6's 11:43Z build) `/thesis` for 8306 JP shows the new label on **36 of 36** moved figures and the predecessor's on 0 |

## 3. Corrections and defects this seat owns

1. **The z-1 order's premise was a restatement miss.** "About 199 outside their band" restated round 23's per-share count,
   which included the zero samples. The census reads 37 outside the band and 450 zeros (`Z-W1-S19`, ruled `717cbb0a14`).
2. **The first leg-c verify counted the derive timestamp as content.** It read 10,083 "other" changes and 26 "case" changes.
   Field by field, all of them are `vintage` and `cases.base.px_last.vintage`, the stamp of the derive that wrote them. The
   timestamp was excluded and counted (`evidence/r24_leg_c_verify{,2}.txt`); the stop limb did not fire on content.
3. **Leg d ran two writers side by side for about 6 minutes.** The first writer (`python -`, PID 21416) survived the harness's
   30-minute background kill. This seat's check for a surviving writer matched `write_one|dossier` on the command line, which a
   stdin script cannot match, so the check read EMPTY and the remainder was relaunched.
   - The writes were idempotent (never-overwrite `gold_put` plus the inputs no-op), with 0 errors and exactly one new object
     per name.
   - Fix owed by this seat: long writers run from a named script with `python -u`, and a survivor check matches on
     CreationDate, never on the command line.
   - `d_verify.py` is the named-script form.
4. **The slash-key ruling counted 30 objects; the bucket holds 40.** A full listing of `opal-data-harvest` (7,048 objects)
   adds scores 4, filings 2 and raw/bloomberg 4. The CTO ruled all 40 into the RESAPP round-53 window (msg 27159); the
   before-state is `SLASH_OBJECTS_BEFORE_STATE.json` (`38702fe8e4`).

## 4. Rows -- dispositions for the L9

| row | state | note |
|---|---|---|
| `Z-S69` (issuer, new) | INERT, carried | TSM `CUR_MKT_CAP`, a USD listing-currency value, is served labelled TWD. The rule reaches 79 header figures on 27 mixed-currency securities; 1 is measured wrong |
| `Z-W1-S19`, `Z-W1-S20` (new) | ruled `717cbb0a14` | the premise was a restatement miss; the zero rule stays in `unit_from_basis_zero` via `build_entries` |
| `Z-W4-S6` (new) | ruled: a precondition of the move | `peers/universe.py` and `corpus/dossier.py` still read the raw form; supplied to `2.0.0_SA_COO~Z` |
| `Z-W4-S7` (new) | ruled: the behavioural gate of the move | the census's `raw 0` is a floor (module-constant prefixes) |
| `Z-W4-S8`, `Z-W4-S9` (new) | closed by the stub | z-4's own `stage_derive` test wrote `field_map.json`; now stubbed |
| `Z-W2-S16` | carried | TSM: no same-currency anchor is stored anywhere searched (13 sources) |
| `Z-S64` | carried; the move is RESAPP r53 cell 3 | BP/_LN and NG/_LN, whose newest blocks are `20260925T200039Z` (BP) and `20260925T200133Z` (NG) |

## 5. Enrichment candidates for the round-24 analysis

1. **The 49 still-UNRESOLVED figures:**
   - 6861 JP, 26 figures: no EQY_FUND_CRNCY;
   - 939 HK BS_TOTAL_LIABILITIES, 10 figures: HKD against CNY, no anchor;
   - BBSE3 CAPITAL_EXPEND, 10 figures: no band;
   - BA BEST_PE_RATIO, 2 figures: 1FY absent;
   - TSM CURR_ENTP_VAL, 1 figure: no anchor.
2. **`Z-S69`:** the per-field currency denomination of the three header fields on the 27 mixed-currency securities, then the
   label rule.
3. **BP/_LN and NG/_LN after the RESAPP r53 move:** a trusted raw-freshness read, then the unit, sign and dossier passes on the
   encoded keys.
4. **The dossier `/5` objects** reach pages only through AMGT_RESAPP's redeploy, which is carried as RESAPP r53 cell 3.

## 6. Bounds and residue

- No Bloomberg call, no SA call, and no vendor call.
- Drained worktrees `wk-crps24-1/2/4` were removed with their branches kept (Andrew 02:5xZ, `8c4f79e531`).
- The slash-key list and preconditions were supplied to `2.0.0_SA_COO~Z` (`7e569c4d1d`, `38702fe8e4`).
