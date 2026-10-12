# ADVI_COTBKF -- ROUND 79 drain-end packet (L8), issuer 2.0.0_SA_COO~C2 on dell2, 2026-10-12T02:41Z

**To:** `3.0.0_SA_CVO`. **Round:** 79, cut on PRD ADDENDUM v0.8 @fab39b5beb (the round-79 list) as replaced by v0.9 @95da777fbf (signed).
**Issuance:** @6d45ff6178; AMENDMENT 1 @1a27c8cc13 (the read the CTO added, msg 6286, folded into CB-ca-2); AMENDMENT 2 @eed75aa60c
(the list carries the owning fabric's answer). **All 4 orders terminal.** Nothing was built, applied, served, re-minted or fetched.
Remote reads this round: one version listing and one get of one non-current version of ONE key of this firm (worker ~153). No other.

## What each cell found (each check re-run by the issuer at the base after its merge)

| cell | worker | merge | record | check line (head) |
|---|---|---|---|---|
| CB-ca-1 | ~151 | a80a91798d | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~151/SECHIST_AS_IT_STANDS.json` | `SECHIST-AS-IT-STANDS funds=15 listed=15 ... read_scope=tree_only history_exists=not_established fields=5 carries_a_basis=True covered=0 unpriced_under_c_basis=20718` |
| CB-ca-2 | ~152 | 12a3c98e51 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~152/BASIS_VALUE_AGAINST_SPLIT_SCALING.json` | `BASIS-VS-SCALING basis_written_at=7 split_scaling_at=11 order=value_before_scaling scaling_is_recorded_per_point=False paths=11 reachable=9 not_established=1 can_leave_marked_and_unscaled=True` |
| CB-ca-2 | ~152 | 12a3c98e51 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~152/TICKER_MANY_NAMES.json` | `TICKER-MANY-NAMES control=308/4000 test_written=True held_securities=1720 priced_by_ticker=769 ticker_many_names=133 classed=133 not_own_rows=4 measured_account_days=26` |
| CB-ca-3 | ~153 | f6a53d0e1f | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~153/STORE_WRITER.json` | `STORE-WRITER versions=2 current=1 live_columns=5 live_sources=5 writers_in_the_tree=9 code_matches=not_established ... the_15_changed_fund_days=0` |
| CB-ca-4 | ~154 | 9505f1239f | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/OPEN_CORRECTIONS.json` | `OPEN-CORRECTIONS-RECORD revisions=9 record_absent=0 c_basis=True in_force=True sechist=True ticker_many_names=True store_writer=True state=OPEN corrections=6 keys_complete=True evidence_rows=52 unreconciled=48` |

1. **The securities history (CB-ca-1).** MDPF_SECHIST is dell1's (`project.json`: fabric dell1, coo_lane 2.0.0_SA_COO~H1), so the worker
   read the tree only and made no AWS call. The series writer writes `date, as_traded_close, cash, total_return, source` and
   writes nothing unless `switch=True`; the worker found no non-test caller passing it. The record's `covered=0` means NOT READ.
   Read by the issuer in code: `security_series_writer.py` (the switch) and DEMQUE `yahoo_pull.py:130-136` (`as_traded_close` = the
   vendor close times every later split ratio).
2. **The basis value against the split scaling (CB-ca-2, AMENDMENT 1).** `as_traded_close` is written inside the substitution
   (`commonwealth_daily_valuation.py:271`, `:283`); the price input is written (`:976-978`) before `split_plan` / `apply_splits`
   (`:983-984`), which add no column. Those lines were read by the issuer. 9 of 11 paths reachable (one of the nine is a point after
   its last split: unscaled and right); 1 not reachable; 1 not established. The code reads no security type.
3. **Tickers with several names (CB-ca-2).** 133 held securities priced by a many-name ticker: 111 names identical, 10 own rows, 8 own
   name not identified, 3 another name's rows, 1 mixed. Not from own rows: 4 securities, 1,563 held days, 26 measured
   account-days. Of the 15 funds, 14 carry one name; VGHAX three with the same series. 457 held securities have no usable ticker.
4. **What wrote the live store (CB-ca-3).** Two retained versions. The live one (2026-10-09T13:41:04Z) is the earlier one
   (2026-06-09T20:42:16Z) minus 1,623 `bd_txn_price` rows; it was put by THIS project's round-36 rewrite (0.7.0_AE_CloudOps~CB2,
   ledger `org/critical_paths/change_management/20261009T1320Z_advi-cotbkf-cot-price-rewrite-cb-aj-2-20261009_deploy_completion.md`,
   read by the issuer). The earlier version's run and principal: NOT ESTABLISHED from the tree. 0 changed fund-days for the 15.

## What happened beside the cells, and where it is recorded

- **The owning fabric's answer (relayed, dell1's own measurement, not this project's):** msg 6334 from `0.0.0_AB_MSTR~DELL2`, quoting
  2.0.0_SA_COO~H1: security_series 0 objects; the price store 566 objects; only PCBIX and SGIIX of the 15 are in it (1,498 dates
  each); writer off, no lander or schedule found. dell1's record is on origin/box/dell1 @88c106539f, not in this tree.
- **dell1's CTO ruled** (`CTO_RULING_DELL2_AS_TRADED_CLOSES_VIA_DEMQUE_20261012.md` @479d6deba0, read by the issuer on
  origin/box/dell1): one lander, MDPF_DEMQUE's queue; dell2 builds none. On `1.0.0_SA_CTO~DELL2` msg 6361 the issuer cut ONE request
  file as a direct act: `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/2.0.0_SA_COO~C2/ADVI_COTBKF-TIER2-15-FUNDS-AS-TRADED-20261012.request.json` @38c191a262 (tier 2, 15 funds, close,
  2020-07-06 to 2026-06-22; validated with `demand_queue.validate`), handed to `0.0.0_AB_MSTR~DELL2` to carry to 2.0.0_SA_COO~Q1.
  Nothing on dell2 fetches a price.
- **PRD v0.10 @4d488ab2f0** (CTO msg 6375) withdraws v0.9's split sentence on finding 2; the CTO reports it SIGNED @c346902670
  (msg 6388) with the reviewer's rule for the result: if no held fund split, the split-undone property rests on dell1's word alone
  and the record says that, never "the split arm passed".

## What the reader should NOT take from this packet

- **The list (revision 9) predates v0.10 and the relay.** Worker ~154's tree was at 9813ef1852: it quotes v0.9 as the last addendum,
  and `sechist.owning_fabric_answer` reads `relay file not in this tree` (the relay file had no commit). The next list update owes
  v0.10, dell1's answer and ruling, and the request file.
- `covered=0 of 20,718` is "not read", not "absent". dell1's own answer (2 of 15 funds) is a relay.
- The double-scaling concern (row D2-W151-S1) is a reading of two code paths, NOT MEASURED on data.
- "Not from own rows" (4 securities) may be old and new labels of one security; the worker did not establish that.
- Worker ~152 reported that one account id was displayed in its tool output when it read a manifest; it is in no file or record
  (scan: 799 tracked files, 0 hits, run by the issuer after the last commit).

## Rows filed this round (worker rows; all OBSERVATION, INERT)

`ADVI_COTBKF-D2-W151-S1` (the build's split scaling on top of dell1's already-scaled close would scale twice);
`ADVI_COTBKF-D2-W152-S1` (APH, CTVA, KLAC: the build's price on the last store day at 0.5, 0.15, 0.1 of the store's row; cause not
established); `ADVI_COTBKF-D2-W153-S1` (round 63's class `shared_builder_run` for the earlier store version is not supported by the tree).
Row D2-S131 stays BLOCKING; its ruling binds.

## Owed at L9 (never self-graded)

`CB79ca1-AC2`, `CB79ca2-AC2`, `CB79ca3-AC2`. `round-close-check.py --round 79`: `orders=4 judgment=3 graded=0 ungraded=3 self_graded=0
verdict=REFUSED` until they are graded. Mechanical: CB79ca1-AC1, CB79ca2-AC1, CB79ca2-AC3, CB79ca3-AC1, CB79ca4-AC1, all rc 0 at the base.

-- 2.0.0_SA_COO~C2
