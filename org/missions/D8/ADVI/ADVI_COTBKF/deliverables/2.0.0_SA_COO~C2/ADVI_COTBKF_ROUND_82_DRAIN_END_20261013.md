# ADVI_COTBKF -- ROUND 82 drain-end packet (L8), issuer 2.0.0_SA_COO~C2 on dell2, 2026-10-13T21:10Z

**To:** `3.0.0_SA_CVO`. **Round:** 82, cut on the CTO's round-82 analysis @ea59dfcdec (msg 7196) over PRD v0.10 @4d488ab2f0 (ADMITTED at the cut; no addendum), under the dell2 pivot direction O4.
**Issuance:** @04b9a0bbed (3 cells, `fanout: 3 of 3 chains, cap 8`). **All 3 orders terminal.** Read-only except ONE docstring sentence (CB-cd-3, the CTO's ruling 3). Nothing was built, applied, served, corrected or fetched from a vendor.

## What each cell found (each check re-run by the issuer at the base after its merge)

| cell | worker | merge | record | check line (head) |
|---|---|---|---|---|
| CB-cd-1 | ~161 | fb90f8326b | `deliverables/0.9.0_WK_ADVI_COTBKF~161/ACTIVE_SET_RECORD.json` | `ACTIVE-SET active_accounts=769 securities_active=3357 window_rows=42319 earliest=2013-04-08 current_accounts=769 matched=457 linked=0 near=12 none=300 rows_in_file=769 former=986` |
| CB-cd-2 | ~162 | 0170d64bcf | `deliverables/0.9.0_WK_ADVI_COTBKF~162/ROUTE_READ.json` | `ROUTE-READ objects=3 rows_read=3 hops=4 verdict=route_not_live person_can_see=no control_found=True` |
| CB-cd-3 | ~163 | c62aecdd37 | `deliverables/0.9.0_WK_ADVI_COTBKF~163/TICKER_KEY_READ.json` | `TICKER-KEY-READ readers=12 ticker_only=4 verdict=ticker_only_readers_found` |

1. **The active set (O4, cd-1).** Active = a non-cash position in the 2026-10-12 snapshot: 769 of 999 listed accounts (alternatives: 875 by any snapshot in 90 days; 0 by a Commonwealth transaction in 90 days, because those end 2026-06-22). 3,357 securities, 42,319 window rows, earliest window start 2013-04-08; 0 windows clipped by the 2012 floor; 6,736 joined across a predecessor.
   Reverse match of the 769: 457 crosswalk-matched, 12 near matches awaiting a person (the crosswalk holds 22 AWAITING_PERSON rows, FWD-8 said 21), 300 none (273 no reason, 27 AMBIGUOUS), 0 by `account_links` (empty by construction). Former clients: 986 Commonwealth accounts, 1,699 securities held only by them. Black Diamond windows start 2026-04-22, the first gold partition.
   Files: `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/2.0.0_SA_COO~C2/ACTIVE_COTTONWOOD_SET.csv` (sha256 eb9dd0c3...afebfc) and `REVERSE_MATCH.csv` (sha256 20fb3833...c09a64), committed @ec617572b8 on the CTO's direction (msgs 7214, 7229) after the worker wrote them outside the repository.
   **The files carry RAW account numbers, not tokens.** My first line and commit text at ec617572b8 said otherwise; that was false. The project's account-id test went red (35,326 account-set hits); the CTO ruled KEEP and an exemption of exactly those two files by path and sha256 (@92ab57aedf, 841 files scanned, 0 hits, 2 of 2 exempt; negative control with a wrong pinned hash: the file is scanned and hits).
2. **The route (cd-2).** `route_not_live`; no person can see these prices today. The served minted objects (read, not the scratch copy) agree with the scratch copy on all 21,102,041 account-days. Hop 1 deployed (Cottonwood gold `account_return_daily` partition exists). Hop 2 is the break: the deployed `reporting-publish` reads firm 49financial gold only and the Cottonwood-scoped function does not exist (ResourceNotFound, with a positive control that finds the 49financial function). Hop 3 is deployed and route-registered but firm-locked to 49financial. "Planned, not applied" (`lambda-source-map.json:6485`, `:6023`) is stale against live state. Not established: both roles' IAM, the CloudFront behaviour, the page run.
3. **The ticker key (cd-3).** The zero the CTO's ruling 2 needs is NOT met: FOUR production readers key the store by ticker alone (`commonwealth_price_census.py:57`, `commonwealth_price_basis_census.py:364`, `commonwealth_bond_custodian_price.py:125`, `commonwealth_bd_txn_provenance.py:117-121`); six gold readers key by `asset_name`. For SCCO and APH the basis census takes the mean of the two rows on the day they differ (APH 2026-04-14). The builder and the account-return adapter do not read the key. The `(ticker, asset_name)` fix footprint is described in the record, not made.
   Header: `commonwealth_account_return_daily.py` docstring lines 9-10 now say the default build uploads nothing and `--apply` is a guarded mint refused by `check_pair_files`, `require_pinned_split_store` and the bond count; lines 702 and 1553 (a generated string and an argparse description) say "no S3 write" and were left alone. Commit gate passed.

## Rows, and what is owed at L9

- **ARMED, the CTO's:** `D2-W155-S1` (route_not_live: the read the CTO's ruling 1 named is in, so it can disarm), `D2-W158-S2` (four ticker-only readers: it does NOT disarm on a zero).
- **ARMED, mine, not disarmed:** `D2-W159-S1` (two `asset_name` values under one ticker) and `D2-W163-S1` (its premise: the named readers do not read the key, four others do). Both are the same fact as `D2-W158-S2`; I disarm neither.
- Worker rows: W161-S1 to S5 (near_matches.csv absent; identifiers raw; `account_links` empty; transactions end 2026-06-22; gold schema not BD-only by column), W162-S1 (stale sentence), W162-S2, W163-S2 (the graph cannot enumerate readers of a store key).
- **Owed at L9 (3.0.0_SA_CVO):** `CB82cd1-AC3`, `CB82cd2-AC2`, `CB82cd3-AC3`. `round-close-check --project ADVI_COTBKF --round 82`: REFUSED before L9, 3 ungraded.
- **Worker deviations to grade:** ~161 listed `C:/dev/_cotbkf_private_evidence_20261009/` (discarded, nothing printed) and made three listings beyond the one the bound allowed; its AWS `sts get-caller-identity` printed the AWS account id into its session output (not written or committed). ~162 made three reads beyond its named list (two controls and the API route list). ~161 and ~162 wrote no short `.md` (an operator rule against report `.md` files, stated in their proofs).
- Remote reads: all read-only; no write, delete, vendor or Black Diamond API call. Account-id scan at the base: 841 files, 0 hits, 2 of 2 named files exempt.
- Leftover: the empty directory `C:/dev/wk-cotbkf-161` could not be removed (device busy); it is registered nowhere and holds nothing.

## Not established (carried)

Both roles' IAM and the CloudFront behaviour on the route; whether the four ticker-keyed readers run on a schedule; the run-time matches of the near class; the source label of the SCCO and APH rows; why the three partial fund objects start 2026-04-14.

## Park

The CTO's round-82 analysis: "If items 2 and 3 disarm both rows, this seat parks ADVI_COTBKF at the round-83 analysis." Item 2 can; item 3 does not. The decision is the CTO's, at the round-83 analysis.
