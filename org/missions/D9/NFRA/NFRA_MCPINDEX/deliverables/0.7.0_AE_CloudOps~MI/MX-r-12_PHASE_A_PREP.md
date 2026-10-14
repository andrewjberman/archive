# MX-r-12 PHASE A -- prep done ahead of the cut, and what is still waiting

`0.7.0_AE_CloudOps~MI`, 2026-10-14 ~02:2xZ. Order:
`org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-r-12.depth-v4-release.md` at **A3** (the latest
amendment; A2's "goes NOW" is superseded on timing).

**NOTHING IS CUT.** Per A3, PHASE A starts only when **MX-c-9 A3 drains**, because the six held harvest rows land
through `legacy_addresses.json` and a cut made before that drain would ship a six-row-short catalog and need a v2.
The issuer then names the three blobs at the new drain commit. The 10:00Z ledger-close window stands
(`2.0.0_SA_COO~O` msg 33905; otherwise NFRA_OPLGTW r30 deploys at 11:00Z and MX-r-12 follows it).

This file exists because that window is tight and MX-r-11 lost an apply to a tree that could not run the deploy
script. Everything below is preparation that does not depend on which blobs ship.

## The deploy tree is built and verified -- `C:/tmp/mx-dep-r12`

NEW tree, as A2 requires (MX-r-11's `C:/tmp/mx-dep-r11` is kept and locked as v2's rollback pin).

| | |
|---|---|
| HEAD | `b0c75d24f11808d1de4f70fcca5d39216282054a`, detached, `porcelain` 0 lines |
| cone | `.tools`, `data/transcripts/scripts/teams`, `infra/aws/ec2/opal-gateway`, **`infra/logic/registry`**, `lib`, `org/mcp/inbox/0.7.0_AE_CloudOps`, `org/standards`, `org/tier2_senior/0.7.0_AE_CloudOps` |
| worktree lock | set, so idle GC cannot take a tree a release runs from |

**The closure the deploy script reads, all PRESENT:** `lib/opal_naming.py`,
`infra/logic/registry/systems.json`, `org/standards/NAMING_SCHEMA.json`,
`data/transcripts/scripts/teams/meeting_allowlist.json`, `infra/aws/ec2/EC2_MANIFEST.json`,
`data/firm_registry.json`.

NOTE: **THE ORACLE, run rather than reasoned** -- the two `address()` calls whose closure cost MX-r-11 its first apply
(rows `Z-S108` / `Z-S111`) both resolve from this tree:

```
FEE OK: s3://opal-data-assets/smartx/49financial/bronze/fee_statement/
MKT OK: s3://opal-data-transcripts/sharepoint/transcripts/bronze/market_update/
```

A present-file census is NOT this check: `lib/` was present on MX-r-11's failed attempt and the run still died on the
registry. Exercising the call at the call site is the only form that settles it.

**Halt gate from this tree: rc=0**, agent home resolvable in the cone (`HALT_OVERRIDE` never set). Its valid negative
arms are recorded in MX-r-11's proof instance -- note that `AGENT_NAME` and `CLAUDE_CODE_SESSION_ID` are NOT this
gate's knobs (it resolves from the session serial file, then the EXPORTED `$OPAL_AGENT_SERIAL`, then the shared
checkout), so an arm built on either reads rc=0 and proves nothing.

## Preconditions read, not assumed

- **The live ref is `b0c75d24f11808d1de4f70fcca5d39216282054a` on BOTH planes:** S3 `-latest` `git-ref` and
  `EC2_MANIFEST.json` `deployed_commit` at HEAD agree. That is MP-n-4 (01:31Z), matching A2. **It is re-read from the
  HOST by hash at the cut regardless** -- this is context, not a pin.
- **The gateway slot is free.** `deploy_ledger.py check`, SCAN DENOMINATOR **18 of 18** sentinels: no gateway-host
  release ledger is OPEN or HELD. `nfra-mcportal-c17r2-release` -- which MP-n-4 opened at the very commit this tree
  sits on -- has CLOSED. `nfra-oplgtw-fd2-etf-drain` is HELD on a 23:30Z EventBridge sweep and is a data drain, not a
  host release. OG-ap-14 has not opened an entry yet.
- **The round-11 battery is in place:** `round11/checks/` carries `r12.AC1.sh`, `r12.AC2.sh`, `r12.AC3.sh`,
  `r12_host.py`, `c11_index.py`, `c11_depth.py`, `c11_harvest.py`, `c10_discover.py`, `_root.sh`. Checked early so a
  missing battery would be a row now rather than a refusal at 09:50Z.
- **The YCharts moratorium does not touch this order** (relay of `0.0.0_AB_MSTR~Z` msg 33909 via msg 33918): no
  `ycharts_*` gateway calls and no YCharts walks until dell1's 02:24Z probe reads 200. MX-r-12's checks import the
  tools without calling them and discover's proof questions never route to YCharts.

## One measured fact for the round analysis -- no new row, it refines `Z-S109` / `Z-S111`

**The script MX-r-12 will ship is the SAME blob MX-r-11 shipped, and it still has no pre-flight loop.**

```
deploy-to-ec2.sh   at b0c75d24f1 (r12 base) .... 2e9e3aed368ce0da2690f77deac3c688d1b90141
                   at 7eff14b2e6 (r11 v2) ...... 2e9e3aed368ce0da2690f77deac3c688d1b90141   EQUAL
                   at box/sitez HEAD .......... 76a4f20a6fac20bd72aa175a36387a874df1b9d9   never shipped
grep -c '_pf_need' on the r12 base's copy ...... 0
```

So the `_pf_need` loop lives ONLY on the trunk, has never reached the host, and the recurrence protection for the
cone is therefore **entirely applier-side** -- which is exactly why the order now carries it as a cut-template rule
(item 2, round-10 analysis ruling 3). `Z-S111`'s recommendation (widen that loop to EXERCISE an `address()` call
rather than `stat` `lib/opal_naming.py`) is still fully open, and it becomes live the first time a release's tree
carries the trunk's script. `--preflight-only` is also not a bare flag on the shipped copy: it is read as the target
instance and the run refuses for a missing `DEPLOY_BASE_REF` (rc=2).

## What PHASE A does the moment MX-c-9 A3 drains

1. Re-read the live ref from the HOST by hash; if it is not what the issuer names, file a BLOCKING row and stop.
2. Re-point this tree at that ref and cut the deploy-only commit carrying **exactly the three drained blobs** --
   `app/refs/DATA_CATALOG.yaml`, `app/integrations/opal_discover/integration.py`,
   `app/admin_gateway_breakdown.py` -- as a SINGLE-BLOB-SET OVERLAY through a temporary `GIT_INDEX_FILE`, never a
   merge of the trunk (the MX-r-11 v2 lesson: 44 gateway paths differed from trunk there, and a merge would have
   shipped all of them and voided both halves on the deploy script alone).
3. Write `ANNOUNCE_MX-r-12.md` with the three censuses and **A1's MC Portal per-tool link counts, live vs cut**
   (`admin_gateway_breakdown._catalog_read_tool_rows()`, the reader's line `:108` at HEAD). A difference makes the
   slot conditional on MP-z-6 being closed or not yet started, and the issuer reads that before the GO.
4. Report the pins, and stop for the never-widen pair.

## Also noted, not chased

`nfra-mcpindex-r7-bd-doc-retire` is OPEN, stranded at L5, 20.2 h into a 192 h window, carrying this seat's author
line. It is a bd-doc retire on another host and belongs to the MX-s-19 surface, which is date-gated to 2026-10-19/20;
it is tracked and in-window, so it is recorded here rather than acted on inside this order.
