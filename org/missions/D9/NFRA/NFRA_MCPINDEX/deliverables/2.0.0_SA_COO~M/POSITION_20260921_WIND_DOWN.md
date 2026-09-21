# NFRA_MCPINDEX -- position at wind-down, 2026-09-21 ~10:0xZ

**Author:** `2.0.0_SA_COO~M` (issuer, round 1). **Why this exists:** Andrew-direct to this seat, "take note of your position on
MCPINDEX and wind down your team at the next logical checkpoint", followed by his box reboot (1.0.0_SA_CTO 99027). Committed
state survives; session context does not. A successor COO resumes from this file plus the carriers it names.

## Stage

- PRD v0.5 ADMITTED @b7dc80e2cc. Decomposition v2 @f506f63a8b (38 cells), recut on 1.0.0_SA_CTO 98944 before issuance.
- Round 1 ISSUED @4a475fe055 (38 orders). dep_stage EXECUTING. CLOUD = origin/CLOUD = d7904401ad at this write (ls-remote read).

## Orders: 8 complete of 38 (each proof re-run by the issuer with the ORDER'S ids; each drain verified per file by blob)

| order | drain merge | note |
|---|---|---|
| MX-a-1 portal analysis | 5938ee8ce4 | 11 PASS + 1 J |
| MX-a-2 Schwab analysis | 1310311a9b | first submission bound 0/12 ids; rebound, VALID |
| MX-a-3 Black Diamond analysis | 0c46bec859 LOST 5 of 6 files; REPAIRED 155533ea00 | row W4-S2 |
| MX-a-4 Orion analysis | 0542f3e509 | |
| MX-a-5 Eclipse analysis | 2cdd953be8 | |
| MX-a-7 ETFs analysis | d7904401ad | row W3-S2 ARMED |
| MX-c-1 catalog writer | 41da358d45 + 60464dd3f8 | AC4 re-run under amended grant 8fd757cca8 |
| MX-c-2 catalog silver schema | db73359967 | catalog-gate exercise 16/16 on the regenerated catalog |

## In flight at the reboot -- NOTHING COMMITTED; the worktrees stay on disk, uncommitted

- **MX-c-4** (slot ~1), `C:/tmp/wk-mcpindex-1d`, branch `wk-nfra_mcpindex-1-1d`, base 60464dd3f8, 0 commits. Uncommitted:
  destructive_ops.py, integrations/base.py, integrations/registry.py, tests/test_entitlement_admin.py (modified);
  tests/test_tool_classification_composition.py, the ~1 proof/result/probe for MX-c-4 (new); also `infra/aws/ec2/opal-gateway/audit.jsonl`
  MODIFIED (a runtime side-write, not in its grant -- must not be committed). The worker was mid-run; its evidence is unverified.
  **Successor: treat as unverified draft.** Either re-spawn MX-c-4 fresh (discarding it) or have a worker review it; never commit it unexamined.
  Known cut tension handed to that worker: AC1/AC11 (every tool needs a catalog reference) vs AC5 (the 4 existing integrations,
  14 tools, register unchanged, no catalog entries, their dirs not in the grant). Expect a refusal; route to 1.0.0_SA_CTO for a ruling.
- **MX-a-6** (slot ~4, SmartX analysis), `C:/tmp/wk-mcpindex-4d`, branch `wk-nfra_mcpindex-1-4d`, base 2cdd953be8, 0 commits;
  two untracked probe files only. Re-spawn fresh.

## Not yet started (29): every other order. Held on gates: MX-i-3 (G-S), MX-r-2 (G-A), MX-v-3/v-4/v-5 (G-B; v-4 also G-Q).

## Owed at the round's drain-end (the COO's one message to 1.0.0_SA_CTO), carried here so it does not live in a session

1. **W4-S2** disarm word VERIFIED by 3.0.0_SA_CVO; the clock was REFUSED mid-round by the slug proxy. Re-mint when round 1 is
   terminal. Carrier: 1.0.0_SA_CTO record @ccf51f6e47.
2. **W3-S2** ARMED, disarm_owner 0.4.0_DS_ClientPlatform: trueshares fact_holdings has 0 live silver objects despite 28 bronze
   deliveries per fund since 2026-08-24, while backfill-status.json reports PASS without counting that feed. Owner liveness NOT checked.
3. Cut defects (this seat's): W1-S1 (MX-c-1 grant, amended under ruling), W1-S2 (orders say firm NFRA; ruled FABRIC per proof),
   W1-S3 (MX-c-2's validator side-write outside grant; the worker reverted it with `checkout --`, a bound crossed), MX-c-4's AC tension.
4. Proofs written before the FABRIC ruling carry no firm: MX-c-1 (both runs), MX-c-2, MX-a-3.
5. MX-a-3 drain loss: 0c46bec859 landed 1 of 6 files while a second lane's merge was open in the shared tree; repaired 155533ea00
   (18f48e87d4 under the audited TREE_DELIVERABLES override). 18f48e87d4's SUBJECT overclaims "byte-identical"; its body is exact.
6. Two findings reported in prose only, not as rows: Black Diamond's bd_assets_dim.parquet not rebuilt since 2026-04-14 with no
   schedule (MX-a-3 worker); Eclipse's converter never calls filter_to_inflection() (MX-a-5 worker) -- a C7 firm-scope question.
7. Open at Andrew, unchanged: the five Schwab tools (G-Q); the owner of the Gateway rollback repair (MX-r-1 refuses until it exists).

## Method the successor should keep

- Re-run every proof with the ORDER'S criterion ids; a worker's "VALID" has been wrong once this round.
- After every drain, compare the merge's file set and each file's blob against the branch; a count is not enough (0c46bec859).
- Completed workers cannot be resumed in this harness; hand each next order to a fresh spawn with issuer context.
- The channel file conflicts on every drain from a pre-row base; union it (rows appended unedited, ids never duplicated).
