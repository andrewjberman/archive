# NFRA_MCPINDEX round 3 -- the issuer's drain-end packet for L8/L9 (2.0.0_SA_COO~MI, 2026-09-29 ~03:1xZ)

Addressed to `3.0.0_SA_CVO~O`. Every round-3 order is TERMINAL, with 8 of 8 terminal and each drained and
issuer-graded on CLOUD. The analysis this round cuts from is `ledger/ROUND_ANALYSIS.round2.md` @e4445020f5. The
issuance commits are 23e18eb0b4 (MX-s-12) and cc6bf5d0cc (items 2-6). The battery is
`deliverables/2.0.0_SA_COO~MI/round3/checks/`.

## 1. Orders -- grade on CLOUD (issuer re-run after each drain)

| order | item | status | mechanical | judgment owed at L9 |
|---|---|---|---|---|
| MX-s-12 (the analysis's MX-s-10b) | 1 | complete @418f1ec3d4 | s10.AC1-3 PASS | **s10.J1**: the dim written by the 22:10Z scheduled fire (see section 2) |
| MX-s-13 | 2 | complete @5498ce662d (A1: 8 files) | s13.AC1-2 PASS | **s13.J1**: your fingerprint scan over the 8 files |
| MX-d-3 | 3a | complete @29fc9b1e32 | d3.AC1-3 PASS (ROUTING 23/27; dataset asks 2/3) | none |
| MX-r-4 | 3b | complete @b80b80e5e4 | r4.AC1-2 PASS (enabled 2 of 2; tools 46 -> 51) | **r4.J1**: the close run, NOT RUN (section 3) |
| MX-m-1 | 4 | complete @efafa3fedc | m1.AC1 PASS | **m1.J1**: `deliverables/0.9.0_WK_NFRA_MCPINDEX~11/MEASURE_BATCH_ROUND3.md` |
| MX-i-4 | 5 | superseded @e22d869bec | i4.AC1 refused as written (4 LIVE readers), i4.AC2 PASS | none; carried (section 4) |
| MX-x-1 | 6 | complete @37bf952511 | x1.AC1-2 PASS | none |
| MX-x-2 | 6 | complete @067dc14967 (A1: read_tool + accessor) | x2.AC1-3 PASS | none |

The Z-W3-S12 fix (pytest `-rA` verdicts) is in the round-3 battery's `_root.sh`. It is not a cell.

Also owed by you, separate from these criteria:
- G5-G7 live-cert on the enabled integrations (1.0.0_SA_CTO~O's ask, msg 26268; G-A @0d9f28d8f9).

## 2. The one real run of each outcome -- what was run, and by whom

- **MX-s-12:** the SCHEDULED fire, rule `bd-asset-dim-pipeline-trigger` 22:10:00Z -> ssm 16d855de at 22:11:06Z,
  Success. The issuer re-measured both S3 versions itself (G1 `kittUyy...` vs `qcSdLjLW...`):
  - 12,141 = 12,141 unique ids, and the id-set sha256 prefix b38a8b0a5dd07053 is equal;
  - 0 added and 0 removed;
  - non-null cusip 10,957 = 10,957;
  - 0 cusip changes of any kind, so MX-s-6's 42 did not reproduce today (the pull matched the dim).
  - The trigger runs `$LATEST`, not DEFAULT; v4 is both. See row Z-S48.
- **MX-r-4:** a live SSM read of the host by the issuer's check. The worker's N2, by an independent SSM read, gave:
  - the 5-id `.env`;
  - 26 keys before and after;
  - /health 200 and /mcp unauthenticated 401;
  - tools 46 -> 51, 0 removed, and the 5 added being `mdpf_get_account_distribution`, `mdpf_get_aggregate_aua`,
    `mdpf_get_aum_metrics`, `opal_describe` and `opal_discover`.
  The host serves deploy-only `0bce8d322a`, whose gateway tree equals pin `3371f18803` (tree object 09ccfc39ad).

## 3. MX-r-4 J1 -- the close run is NOT RUN, and why

- No legitimate route to call the tools exists from a worker: /mcp answers 401 unauthenticated, and an in-process call
  would need a principal the worker made up.
- None exists from this seat either: its MCP tool list was fixed at connect, and a search for `opal_discover` finds
  nothing.
- The first live exercise is a principal session with a refreshed tool list. That is Andrew's speed and efficacy test
  under the G-ASKER record (@7bfa5811c6, call 1). The test card is 2.0.0_SA_COO~AI's.
- `CLOSE_RUN_MX-r-4.md` in the worker's deliverables records NOT RUN for all 4 A2 surfaces, plus what was measured.
- FWD-1 and FWD-2 are therefore still unexercised by a real ask. The thread's hops are all built and enabled.

## 4. Rows raised this round (18), and the issuer's rulings

| row | class/hazard | the issuer's act |
|---|---|---|
| Z-W8-S1 | BLOCKING/INERT | disarmed by the issuer's serial file; recorded in Z-W8-S2 (a worker row cannot carry `adjudicates`) |
| Z-W8-S2 | OBS/INERT | a record of the above |
| Z-W8-S3 | BLOCKING/ARMED | disarmed by placement, **Z-S52**: 4 LIVE Playwright legs (allocation, realized, transaction, unrealized) still read opal/bd/credentials and fail 21 of 21 at the MFA login. Carried. The account-lockout risk is UNMEASURED. |
| Z-W9-S1 | OBS/ARMED | disarmed, **Z-S53**: the 8th file is redacted under the CTO ruling @8ed938b2d7 and MX-s-13 A1 |
| Z-W9-S2 | OBS/INERT | "extended-backfill.sh carries no second literal": for your J1 scan |
| Z-W10-S1 | OBS/INERT | 4 residual routing misses (Q22 lacks catalog vocabulary; Q09, Q13 and Q25 are precision). Carried. |
| Z-W10-S2 | BLOCKING/INERT | ruled by A2 @14ddaa523a (deploy-only tree, the OA-r-1 pattern); resolved by the deploy |
| Z-W11-S1 | OBS/ARMED | disarmed, **Z-S50**: an instrument trap (BD runs execute `$LATEST`). Standing rule: grade at `$LATEST`. |
| Z-W11-S2 | OBS/ARMED | disarmed by placement, **Z-S51**: the transaction merge skips the dim join; the transaction feed is dead. Carried. |
| Z-W11-S3 | OBS/INERT | the portal submodule is empty in worker worktrees (an instrument limit) |
| Z-W13-S1 | OBS/INERT | the emitter needs `portal/src/api`; the worker extracted it read-only and it is uncommitted |
| Z-W13-S2 | OBS/INERT | validate_catalog_v02.py makes live S3 reads; 1 of 36 rows reported family_mismatch_or_error, unidentified |
| Z-W13-S3 | BLOCKING/INERT | ruled by the CTO @8ed938b2d7 (no waiver; read_tool + accessor); resolved by x-2 A1 |
| Z-S48 | issuer | disarms Z-S42 (the dim is current by its SCHEDULED producer) |
| Z-S49 | issuer | disarms Z-S47 (the fees Playwright leg is destroyed) |
| Z-S50, Z-S51, Z-S52, Z-S53 | issuer | as above |

## 5. Carry candidates for the round-3 analysis (issuer's placement, not a ruling)

1. **Retire or port the 4 BD Playwright daily legs** (allocation, realized, transaction, unrealized) off the portal
   login, on the MX-s-12 pattern. This unblocks MX-i-4 (re-run unchanged) and the dead transaction feed (Z-S51). The
   lockout risk is unmeasured.
2. **The skipped dim join** in the EC2 transaction merge (Z-W11-S2), a DS-lane silver cell, after item 1.
3. **Align DEFAULT to `$LATEST`** on the allocation and transaction SSM documents (Z-W11-S1), or retire them with 1.
4. **Routing precision:** catalog index vocabulary for Q22, and NOT_CATALOGUED precision for Q09, Q13 and Q25
   (Z-W10-S1).
5. **FWD-1/FWD-2 exercise:** the close run through a principal session, which is the round's open judgment (J1).
6. **Carried from the round-2 analysis, unchanged:**
   - the 28 opal_ai-path cells behind NFRA_OPALAI E9 (G-MOVE);
   - the Schwab/BD/Eclipse/Orion/SmartX/ETF tool cells after the live thread;
   - R-11's REMEDIATION_v1 flip, which m1 (c) now answers: 2,800 of 22,344 null cusips are cash.
7. **Housekeeping:** the round-3 worker worktrees and the /c/tmp release, deploy and rollback trees are still on disk.
   Removing them is a recursive delete held for an operator word. The branches are drained, except the dep- and
   rel- branches, which are never drained by design.
