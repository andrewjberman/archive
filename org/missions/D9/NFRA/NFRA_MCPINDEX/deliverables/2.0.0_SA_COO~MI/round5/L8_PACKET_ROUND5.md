# NFRA_MCPINDEX round 5 -- the issuer's drain-end packet for L8/L9 (2.0.0_SA_COO~MI, 2026-10-01 ~08:1xZ)

Addressed to `3.0.0_SA_CVO~O`.
- **Source:** round 5 is the reinstatement, cut from 1.0.0_SA_CTO~O's rulings B1-B9
  (`deliverables/1.0.0_SA_CTO~O/REINSTATE_RULINGS_20260930.md` @4e598ab7be) against PRD v0.6 (@e91ce9a0d5).
- **Issuance:** @b2ead0491d.
- **Battery:** `deliverables/2.0.0_SA_COO~MI/round5/checks/`.
- **Round-4 stragglers closed in this span:** MX-t-10 and MX-s-14.
- **State:** 8 of 9 orders are terminal and issuer-graded on CLOUD. MX-t-12 is HELD and carried to the L10 slug by
  ruling (Z-S67).

## 1. Orders -- grade on CLOUD (issuer re-run after each drain)

| order | risk | status | mechanical (issuer re-grade) | judgment owed at L9 |
|---|---|---|---|---|
| MX-a-8 (BD analysis) | SERVED | complete @a73e9cf57e | a8.AC1 PASS 9 of 9 | **a8.J1**: `analysis-blackdiamond.r5.result.md` (read fence, first tool, `blackdiamond` id) |
| MX-s-15 (Schwab dim_transaction) | WORLD | complete @46587d5134 | s15.AC1-2 PASS | none |
| MX-q-3 (gateway_query_catalog tool) | WORLD | complete @b26d0b3ae0 | q3.AC1-2 PASS | none |
| MX-t-13 (blackdiamond_list_fees) | WORLD | complete @b0f54d5a1f (drain d3b0efe5c6) | t13.AC1 1/1, AC2 4/4 | none |
| MX-t-10 (etfs_get_positioning; round 4) | WORLD | complete @26cc4e7252 (drain 29a40f5d4c) | t10.AC1 5/5, AC2 16 passed | none |
| MX-r-6 (Schwab enable release) | WORLD | complete, re-graded 2026-10-01 on live 05e3eff563 | r6.AC1 PASS (23/23 sentinels), r6.AC2 PASS (6/6 ids, dim_transaction 2/2) | **r6.J1**: Alyssa's cold run, NOT RUN (section 3) |
| MX-r-7 (BD + ETF release) | WORLD | complete, drain @1232c96dc7 | r7.AC1 PASS (23/23), r7.AC2 PASS (7/7 ids, /health 200) | **r7.J1**: section 2 |
| MX-s-14 (BD Playwright strip; round 4) | WORLD | complete @39b79e73b6 | s14.AC1-3 PASS; ledger 9/9 | none |
| MX-t-12 (advi portal tool) | WORLD | HELD, carried to L10 (Z-S67) | not run | none this round |

## 2. The one real run of each outcome

- **MX-r-6 (Schwab):** LIVE since 2026-09-30T18:33:41Z. The read-back (SSM b6da75a0) gave /health 200, 6 ids, and
  tools 52 -> 58. Alyssa's grant was written at 19:15:29Z (record @c9be59c0c7).
- **MX-r-7 (Black Diamond + ETF):** LIVE since 2026-10-01T07:13:52Z, at `05e3eff563` on base d61fde4693.
  - Ledger `nfra-mcpindex-r5-bd-release` CLOSED 7/7.
  - Never-widen halves: COO @574e0acf6b, CTO @adcbe6b693 (G-A ACCEPTED).
  - Terraform act #1 of the gateway train, applied through safe-apply: "6 added, 0 changed, 0 destroyed".
  - Worker read-back:
    - `.env` 37 keys, with both principal keys;
    - tools 58 -> 60 (+`blackdiamond_list_fees`, +`etfs_get_positioning`, 0 removed);
    - host 89/89 equal to the artifact;
    - one in-process `blackdiamond_list_fees` call: outcome ok, as_of 2026-09-29, 1 of 1 partition, rows_matched 22853.
  - **The issuer's principal-session asks:** `round5/R7_J1_PRINCIPAL_SESSION_20261001.md`. Through the live gateway as
    an admitted Opal principal:
    - `ETF positioning` routes to `etfs_get_positioning`;
    - `what fees did Black Diamond charge` reads **catalogued: false, 0 matches**. `opal_discover` never reads
      `silver_datasets`, where the BD row sits (row Z-W21-S22).
  - So J1's clause "the route discover gave names that tool" is UNMET for BD as measured. This is the same shape as
    your Z-C-S31 adjudication on Schwab.
  - The tool call itself through a principal session needs a session whose tool list postdates 07:13Z. This seat's
    tool list predates it.
- **MX-s-14:**
  - The scheduled fires ran Success on the stripped versions on 09-29 and 09-30.
  - Unrealized v3 wrote 6 silver partitions at 21:39Z.
  - Realized, transaction and allocation silver is written by the S3-triggered `bd-silver-merge` (00:11Z 10-01:
    transactions 110,685 rows). Row Z-S69.

## 3. MX-r-6 J1 -- the cold run is NOT RUN, and why

r6.J1 needs an already-admitted Opal principal who did not author the index and holds a Schwab grant (rulings B1/B2),
in a fresh session with only the MCP connected. That is Alyssa, a person. No seat can run it. It is the one act in this
round that waits on a human.

## 4. Rows this round, and the issuer's rulings

There are 60 rows surfaced 2026-09-30..10-01: 49 OBSERVATION/INERT, 5 BLOCKING/INERT, 4 BLOCKING/ARMED and 2
OBSERVATION/ARMED (in-file flags). The BLOCKING and ARMED ones, joined to the rows that rule them:

| row | in-file | ruled by |
|---|---|---|
| Z-W19-S2 (dim_transaction absent from the OPLGTW contract) | BLOCKING/ARMED | Z-S63 (the contract lists dim_transaction, MX-r-6 v3) |
| Z-W19-S7 / Z-W19-S8 (Schwab host inputs; whole-dir plan) | BLOCKING/ARMED | Z-S66 (A3: host inputs shipped; targeted plan) |
| Z-S68 (MX-r-6 v2 over ~RV's release) | BLOCKING/ARMED | **Z-S71** (this span): plan A done, guard shipped and exercised twice |
| Z-W20-S3 (advi key refused by naming) | BLOCKING/INERT | Z-S67 (MX-t-12 held to L10) |
| Z-W21-S9 / S10 (R20 waiver vs NEW literals) | BLOCKING/INERT | Z-S64/Z-S65; R20 entries landed @0d71a22887 |
| Z-W21-S12 / S13 (BD host inputs; plan 6 not 3) | BLOCKING/INERT | A5 @4db8b62899, recorded on Z-W21-S17 |
| Z-W21-S1 / S3 (bd_ name; fees writer) | OBSERVATION/ARMED | Z-S62; the writer is named in Z-W21-S16 (`bd-49f-fees-runner`) |
| Z-W21-S18..S23 (PHASE B) | OBSERVATION/INERT | Z-S70 |
| Z-S61 (s-14 write arm) | OBSERVATION/INERT | Z-S69 |

## 5. Carried to the round-5 L10 slug (enrichment candidates for 1.0.0_SA_CTO~O)

1. **Discover does not route `silver_datasets` rows** (Z-W21-S22; Schwab Z-C-S31 / CTO 27367). This breaks FWD-4's
   route clause for both BD and Schwab. Thread-relevant: first.
2. **G-RDR:** route `portal_index` and `opal_discover` through `INTERNAL_READER_ROLE_ARN` (CTO 27414 / train ruling
   R7). It follows MS-d-2.
3. **MX-t-12 / advi** (Z-S67): naming key refused; the objects are a frozen twin.
4. **BD ExternalId option A** (a runtime secret read instead of the deploy-time `.env` value), from A5.
5. **The CLOUD opal-gateway Terraform root does not render under safe-apply** (Z-W21-S19). Three data-source secrets
   of other seats' unapplied files are absent. This gates train acts #2/#3.
6. **The BD document merges are a second merge path beside `bd-silver-merge`** (Z-S69): retire or keep.
7. **Shared-tooling defects:** the deploy wrapper's mojibake manifest commit (Z-W21-S23); the halt-gate serial in a
   shared-session worktree (Z-W21-S21).

## 6. Push state

LOCAL. CLOUD is ahead of origin. The site-Z push is MSTR~Z's on Andrew's word.
