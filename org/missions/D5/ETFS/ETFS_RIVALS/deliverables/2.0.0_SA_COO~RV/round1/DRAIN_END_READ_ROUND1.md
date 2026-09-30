# ETFS_RIVALS round 1 -- the COO's drain-end read (`/dispatch` step 6)

**Seat:** `2.0.0_SA_COO~RV`, 2026-09-30 ~15:5xZ. **To:** `1.0.0_SA_CTO~Z`.

## Round state: 9 of 9 task orders terminal

| order | merged | verdict |
|---|---|---|
| RIV-r-1 | 442e265a0c | complete |
| RIV-w-1 | 2274b529ef, amendment 1 @302cdd9556 | complete |
| RIV-c-1 | ce9f413acb | complete |
| RIV-d-1 | f42f12108f, amendment 1 @746558e232 | complete |
| RIV-s-1, g-1, g-2, p-1 | b2834dc66a (chain ~1) | complete |
| RIV-d-2 | b4915310f4, amendments 1-4 | complete; ledger `etfs-rivalfunds-thread-r1` CLOSED @08494e3984 |

**The BASG thread is live end to end from AWS.** d-2's AC1-AC3 PASS, re-run by the issuer at 15:25Z:
- 325 bronze days and 325 silver days;
- 325 canonical_shape days and 324 trade_schedule days;
- the day's page, published by the Lambda with its guardrails passing;
- `/rivalfunds` on the gateway at deploy-only ref `4ce7946426` (tag `deploy-gw-etfs-rivalfunds-r1`).

**OPEN for a human:** the CTO half's condition 5, one authenticated `/rivalfunds` read.

## The CVO's watermark against the channel

- **Channel:** `surprise-channel/investigations/INVESTIGATION_v1.Z.md`, **29 rows**. By class: 8 BLOCKING/ARMED, 2 BLOCKING/INERT, 19 OBSERVATION/INERT.
- **CVO watermark:** NONE. No compiled channel exists in the tree (the project's `surprise-channel/` holds `investigations/` only), so **0 of 29** rows are compiled. The L8 compile is owed by `3.0.0_SA_CVO~Z`.

## Armed rows: every owner was seated

All 8 name `2.0.0_SA_COO~RV` as `disarm_owner`. This seat was live and disarmed each one by an act. Investigation rows are
immutable at the row gate, so the act is recorded here for the CVO's adjudication.

| row | hazard | disarming act |
|---|---|---|
| W5-S1 | gate 1: HEAD's gateway carries 23 riders | amendment 2 @c19a7e0ea7: deploy-only ref, no rollback |
| W5-S4 | gold Lambda package omits `etf_positioning_gold.py` | amendment 3 @6b5500cd56; worker fix 3eaa380467, in-place code update 0/5/0 |
| W5-S6 | view imports differ at the old base | amendment 3: ruled immaterial (names identical) |
| W5-S8 | the manifest base moved to 288fa78c93 | amendment 4 @6a049b4d48: act-time BASE |
| W5-S9 | the harness denies a worker `reset --hard` | the issuer re-cut the deploy worktree at BASE (branch `-r1b`) |
| W5-S10 | the lane gate refuses the deploy ref (BASE carries no order) | the issuer committed ref 4ce7946426 under the audited override (the 288fa78c93 / 093fc247c6 precedent) |
| W5-S12 | the halt gate cannot resolve a worker on the ref | the issuer deployed at 14:37Z (the pair bounds the act, not the actor) |
| W5-S16 | NFRA_MCPINDEX 2e2254156e overwrote the gateway at 14:41Z | Plan A (1.0.0_SA_CTO~O 27225/27228): this seat redeployed 4ce7946426 at 15:23Z, host == ref 80/80; row S17 records it |

## For the round-1 analysis (not armed)

- **No lock across seats' gateway deploys.** That let 2e2254156e overwrite 4ce7946426 four minutes later. Its base guard was
  read before 14:36Z. Owner: CTO-class.
- **Today's deploy-only refs 288fa78c93 and 093fc247c6 carry no tag** (row S15). This seat keeps local branches at both.
- **`safe-ec2-deploy`'s manifest rewrite turns escaped non-ASCII into mojibake** (row S14).
- **The crosswalk resolves 0 of 35 BASG positions** (W1-S4), so every trade is UNRESOLVED.
- **Rows W1-S1 / W1-S2:** the daily event's date semantics, and the bronze key carrying no requested date.
- **Row W1-S5:** guardrail thresholds are provisional; PARTIAL means a not-updated page.
- **Scope arriving:** the IDVZ peer group. CRO~Z's brief `docs/briefs/etfs-rivals-idvz-expansion-20260930.md` @a5dde65360, and
  this seat's intake `deliverables/2.0.0_SA_COO~RV/INTAKE_IDVZ_PEER_GROUP_20260930.md`. Per Andrew, storage stays flat and the
  grouping is the page Lambda's.
