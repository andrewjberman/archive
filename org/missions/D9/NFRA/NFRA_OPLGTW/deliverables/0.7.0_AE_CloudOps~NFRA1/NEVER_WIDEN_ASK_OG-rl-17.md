# NEVER-WIDEN ASK -- `OG-rl-17` -- the round-47 sixteenth batched gateway release (`batch16`): the client fences and resolve envelope, the Cottonwood date parse, the 50 KB projection, the in-flight guard and the 8 GiB capacity key, the search and poll bounds, `index_pairs`, `news_for_security`, the YCharts and data-refresh repairs, the error-text mask; ONE code release plus two manifest keys; no IAM, no Terraform, no env key

Applier: `0.7.0_AE_CloudOps~NFRA1`. Order: `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-rl-17.round-47-sixteenth-batched-release-the-client-fences-the-size-caps-and-the-in-flight-guard.md` (GO for Phase A: msg 36175; method `OG-ap-50`'s). Source: the CTO's round-46 analysis items 1-5, 7 and 8 and the small items. **Phase A deploys nothing in any form** and writes no SSM parameter and nothing to the audit lake.
**The release signed:** `release_sha` `8e3eddf95916e430e4e9bbf615ca4fd91f9e852f` (the RE-CUT at the in-flight cap 26: the first cut `ce99b7463b` plus `app/inflight_guard.py` and `tests/test_og_mg3.py` taken whole from trunk `c0a0ee2e9c`), on branch `rel-nfra-oplgtw-batch16` in the sparse tree `C:/tmp/og-rel-batch16` (LOCAL, not pushed), cut on `base_sha` `13917ef993207bee6b8df0124eec5444da4d62cd` = the live ref READ ON THE HOST (`/opt/opal-gateway/.deployed_commit` at PRESENT 13917ef993; `W/rl17_pa/step1_before.json`), from `trunk_sha` `c0a0ee2e9c21c4b9d4d0080b095240038be09354`. dell1's harvest release `6575999df5` is an ancestor of `base_sha`; dell1's four harvest files are byte-equal between base and release (the diff does not touch them).
Records: `W/rl17_release.json`, `W/PHASE_A_OG-rl-17.json`, `W/rl17_pa/{step1_before,host_leg,tests,take,lease_param}.json`, `W/rl17_pa/failed_{release,live}.txt`, and the scripts `W/rl17_take.py`, `W/rl17_host.py`, `W/rl17_tests.py`, `W/rl17_phasea.py`, `W/rl17_ask.py`.

## 1. The diff, by file (26 files differ from the live ref: 1969 insertions, 75 deletions)

Twenty-five files taken WHOLE from trunk, each byte-equal to trunk's blob at `trunk_sha`; the manifest by two text edits. For each of the fifteen files that already exist at the live ref I read that the live blob equals the blob at trunk `9095ce68f3` (batch15's trunk), and that only the named commit touched the file since, so the hunks below are that cell's alone. "Hunks" counts live-to-trunk diff hunks.

| file under `infra/aws/ec2/opal-gateway/` | hunks | cell |
|---|---|---|
| `app/client_core.py` | 6 | OG-fc-1 (D1 fence kinds for orion, eclipse, commonwealth; D3 merged resolve envelope), merge `6c747e7e50` |
| `app/client_adapter_bdcottonwood.py` | 2 | OG-sx-1 (D2 Cottonwood M/D/YYYY trade-date parse), merge `77834d2acb` |
| `app/family_depth.py` | 2 | OG-sx-1 (the error-text mask, Z-S407), merge `77834d2acb` |
| `app/integrations/ycharts/integration.py` | 9 | OG-sx-1 (the YCharts repairs), merge `77834d2acb` |
| `app/integrations/opal_portal/integration.py` | 3 | OG-sx-1 (the data-refresh repair), merge `77834d2acb` |
| `app/harvest_typed.py` | 8 | OG-sz-1 (P4-P7: size measured as the indented JSON the server serves; project() per field), merge `0dad6e544b` |
| `app/integrations/portal_index/integration.py` | 2 | OG-sz-1 (the aggregate-AUA projection), merge `0dad6e544b` |
| `app/integrations/opal_discover/integration.py` | 2 | OG-sz-1 (the opal_discover projection), merge `0dad6e544b` |
| `app/inflight_guard.py` | 1 (new) | OG-mg-3 (NEW: the in-flight guard), merge `2d2a56cb04` |
| `app/tools.py` | 8 | OG-tp-1 (6 hunks: result caps on search_files, search_site_files and the Teams poll) and OG-mg-3 (2 hunks: the import and the call_tool hook), merge `2d2a56cb04` |
| `app/admin_gateway_breakdown.py` | 4 | OG-ix-1 (index_pairs per catalog segment), merge `d1c30de58b` |
| `app/news_typed.py` | 11 | OG-nf-1 (news_for_security searches by name), merge `fb46590b00` |
| `app/admin_people_access.py` | 1 (new) | NFRA_MCPORTAL's inert, unmounted pair (written yes msgs 35981 and 35990; mounting stays NFRA_MCPORTAL's) |
| `deploy/NFRA_OPLGTW_CONTRACT.json` | 1 | OG-mg-3 (the one value capacity.target_memory_mib 2048 -> 8192), merge `2d2a56cb04` |
| `tests/test_og_fc1.py` | 1 (new) | OG-fc-1 (new) |
| `tests/test_og_sx1.py` | 1 (new) | OG-sx-1 (new) |
| `tests/test_og_sz1.py` | 1 (new) | OG-sz-1 (new) |
| `tests/test_og_mg3.py` | 1 (new) | OG-mg-3 (new) |
| `tests/test_og_tp1.py` | 1 (new) | OG-tp-1 (new) |
| `tests/test_og_ix1.py` | 1 (new) | OG-ix-1 (new) |
| `tests/test_og_nf1.py` | 1 (new) | OG-nf-1 (new) |
| `tests/test_og_gt0.py` | 1 | OG-sz-1 (one assertion: the projection measure) |
| `tests/test_og_gt5.py` | 1 | OG-sz-1 (one assertion: the projection measure) |
| `tests/test_og_rv2.py` | 4 | OG-sz-2 (the wide-row count the new measure moves; the issuer's full-suite comparison found it) |
| `tests/test_admin_people_access.py` | 1 (new) | NFRA_MCPORTAL's inert pair (new) |

`infra/aws/ec2/EC2_MANIFEST.json` (the release tree's copy), EXACTLY two keys: the gateway's `machine_type` `t4g.nano` -> `t4g.large` (the stale live-backfill value; `OG-rz-2` resized the host) and `services.opal-gateway.mcportal_commit` `59e802a4185a` -> `21ad40432cae0d09c5ab9d806307944baaf45cb9` (`2.0.0_SA_COO~MP`'s pin; its page cells `MP-z-7` and `MP-z-8` ride the bundle). The deploy script's own `deployed_commit` bookkeeping is unchanged.
**NOT in this release (the check counts them at 0):** `app/data_entitlement.py`, `app/account_ref.py`, `app/integrations/schwab/integration.py` (`OG-rt-1`, owner `2.0.0_SA_COO~O`, rides `OG-rl-18` alone so an entitlement-parser defect has its own rollback), `app/destructive_ops.py` and `app/refs/partner_roster.json` (`2.0.0_SA_COO~O`), `app/server.py`, `graph.py`, `probe_listener.py`, `audit.py`, `owner_gate.py`, `typed_scope.py`, the other six client adapters, `deploy-to-ec2.sh`, the unit file, every `.tf`, `infra/logic/`, and `org/standards/NFRA_OPLGTW_CONTRACT.json` (the standards copy lands with the landing, Phase C).
**Other seats' trunk changes that stay out, with their owners:** tests and docs only: `tests/test_admin_gateway_breakdown.py` and `tests/test_admin_people.py` (`0.9.0_WK_NFRA_MCPORTAL~39`), `tests/test_blackdiamond.py`, `tests/test_portal_index.py`, `tests/test_firm_catalog_visibility.py`, `tests/baseline/*`, `tests/suite_delta.py`, `tests/routing/*` (`0.9.0_WK_NFRA_MCPINDEX~28/32/43/44`), `tests/test_cc1_model_basis.py`, `test_cc2_research_misfiled.py`, `test_cc3_ticker_shaped_never_exact_on_name.py` (`0.9.0_WK_AMGT_HARVST~150-152`), `tests/test_mail_route.py`, `test_teams_route.py`, `test_transcript_route.py`, `tests/acceptance/WALKTHROUGH_PROTOCOL.md` (`0.9.0_WK_NFRA_OPLGTW~158/162`), `tests/test_og_cp1.py`, `test_og_en26.py`, `test_og_gt6.py` (`0.9.0_WK_NFRA_OPLGTW~94/141/77`), `tests/test_og_rt1.py` (`OG-rt-1`, `0.9.0_WK_NFRA_OPLGTW~170`), `runbooks/SCHWAB_PILOT_RUNBOOK.md` (`0.7.0_AE_CloudOps~NFRA1`).

## 2. Phase A measurements (every host run in a FRESH process under the cgroup hard guard `oom_score_adj_1000_cgroup_memmax_1400mb`; the running service untouched: PID 2297 before and after, `NRestarts` 0; host 7.1 -> 7.1 percent used; scratch removed)

- **Tests, release tree (both orders equal).** Named set (31 files: the 8 new test files, the edited ones, the admin, owner-gate, `OG-cd`, and client files): 217 passed, 11 failed in each order, and the 11 are the SAME failures as at the live ref (11 of 11); **new reds against the live ref: 0**. Window set (51 existing `test_og_*` files that are green at the live ref): 199 passed, 0 failed in both orders. Four tests that compare the gateway's contract copy with `org/standards`' copy read red in the release tree ALONE, because this release carries the gateway copy (8192) and not the standards copy (the take list is the gateway folder); with trunk's standards copy laid over (uncommitted, restored to the live ref's bytes after, True) they pass 4 of 4, and trunk holds both copies equal.
- **Full suite, per test id against the live ref's tree** (the same sparse cone and invocation): release 78 failed, live ref 74 failed, 74 in both; **only in the release: the four above** (`test_ogcm1_ac05`, `test_ogmg3_contract_capacity`, `test_ogms1_ac04`, `test_shipped_contract_equals_the_standard`); only at the live ref: none. The suite carries a native crash in a process-wide run and the live ref's own ~70 failures; this release adds none.
- **`bash -n deploy-to-ec2.sh`: OK; `--preflight-only`: PREFLIGHT OK; host-shaped import check:** 13 of 13 modules of the take list import from the candidate scratch tree with the service's own `lib/` and `.venv`; the candidate registry counts 103 tools (the live ref 103): `tools/list` does not change.
- **(a) The guard.** Six concurrent `tools.mcp.call_tool("whoami")` against a scratch `InflightGuard(2, 0.1)` through a fake slow parent: 2 ran, 4 returned the `gateway_busy` result (an error result with the body `gateway_busy`, one audit row each, denied/gateway_busy), at most 2 bodies at once, the slots free again and a single call afterwards ran.
- **(b) The fences, on the deployed catalog.** `client_core.Ctx().firm_segments`: orion 1, eclipse 1, commonwealth 1 segment(s) for the served pairs; the three unserved-pair controls read 0 (orion with the cottonwood firm, eclipse with 49financial, commonwealth with the inflection firm).
- **(c) The contract.** The gateway copy equals `org/standards/NFRA_OPLGTW_CONTRACT.json` at trunk byte for byte; `capacity.target_memory_mib` reads 8192.
- **The listener.** The lease parameter `/opal-gateway/probe/lease` is ABSENT now (read); I wrote no SSM parameter; nothing here arms it.

## 3. The widening, stated plainly

- The `client_*` tools now ANSWER for orion, eclipse and commonwealth. Before this release every such call returned `firm_not_served`. They answer only for principals ALREADY entitled to the client surface, reading the S3 prefixes the gateway role already reads; the fence is per vendor and firm (an unserved pair, such as orion with the cottonwood firm, still returns `firm_not_served`). The Cottonwood transaction and fee reads now return rows (the date parse; the round-46 false zero).
- `search_files`, `search_site_files`, `poll_addressed_teams_messages`, `mdpf_get_aggregate_aua`, `opal_discover` and the typed tools answer SMALLER (result caps and the 50 KB projection on the bytes served): a behaviour change for any caller that relied on the full reply.
- `news_for_security` answers more (a name search). The breakdown route (owner only) gains `index_pairs`.
- A NEW refusal, `gateway_busy`, when more than 26 tool calls run at once (the 27th waits up to 20 s and is then refused): a poller treats it as a missed cycle. The cap is 26 by the CTO's ruling on the C1 reading (msg 36195; `OG-mg-4`, drained at `c0a0ee2e9c`): the busiest second of the last 24 hours logged 13 completions, and the cap is twice that.
- **No new tool, no `tools/list` change (103 before and after), no env key (the `.env` key count stays 65), no IAM, no Terraform, no unit or deploy-script change, no SSM write.** `app/admin_people_access.py` is inert: unmounted, nothing imports it.

## 4. The order of acts (Phase B, on a GO that names all three halves signed at `release_sha` and the window)

Window **2026-10-21 06:00Z-06:45Z**, abort line `/health` 200 by 06:30Z; I tell `0.0.0_AB_MSTR~Z` the window (the gateway restarts for about 16 seconds) and again when it is over.
1. Ledger `nfra-oplgtw-gateway-release-batch16`, entry AND sentinel first; re-read the live ref on the host (it must still equal `base_sha`; if dell1 deployed, STOP and file a row); pre-window reads (memory, clock, failed units, lease absent, caller identities in the window).
2. Deploy from `C:/tmp/og-rel-batch16` through `safe-ec2-deploy.sh`, `DEPLOY_BASE_REF=<the live ref read on the host>`, `HALT_ACK=1`, no `HALT_OVERRIDE`.
3. Served read, UNARMED ONLY, with the 27-tool read 27 of 27 under the hard guard, `tools/list` 103 before and after, the host md5 walk, the unit limits `5600M`/`6400M`, and the `inflight` fields read from the DEPLOYED tree (`/opt/opal-gateway/app/inflight_guard.py` constants and the `call_tool` hunk) into `W/CODE16_SERVED.json`.
4. The proofs inside the 30-minute read-back (`W/RL17_PROOFS.json`): D1 one live `client_resolve_account` per vendor plus the unserved control; D2 one Cottonwood `client_get_transactions` returning at least one transaction; the LOAD proof (eight parallel large calls in one turn, `/health` sampled once a second, service peak below 5600 MB); the projection sizes; `index_pairs` in one guarded fresh process. The battery stays at two concurrent calls everywhere else.
5. Host clock and `systemctl --failed` read and printed BEFORE the ledger closes; close the ledger; `rl17.AC2` and `rl17.AC3`; send `2.0.0_SA_COO~O` the CLOSED time and the live sha. Then Phase C, the landing on the `box/sitez` lineage (never a rebase).

## 5. Both branches

- **A 27th concurrent call** while 26 run is refused `gateway_busy` after 20 s; **a single sequential call is never refused** (Phase A burst against a scratch limit of 2: the single call after the burst ran).
- **An entitled caller's D1 call** answers for orion, eclipse and commonwealth; **a caller outside the client surface** is still refused as before (the entitlement denial comes BEFORE the slot, so a denied call takes none).
- **If a trigger fires:** redeploy the live ref's tree (section 6) and file an ARMED row naming `2.0.0_SA_COO~O`.

## 6. Rollback

Redeploy the live ref's tree (`13917ef993207bee6b8df0124eec5444da4d62cd`, the fifteenth release) from the deploy wrapper's pre-deploy tarball of the live tree, whose key, size and hash I record at the start of Phase B. The guard, caps, fences and the new refusal disappear with it; the contract key returns to 2048 with it. The manifest keys revert with the same redeploy (the deploy bookkeeping rewrites `deployed_commit`).

## 7. Triggers (any one: roll back as section 6)

`/health` not 200 in 60 s; a tool of the 27 not answering under the guard; the `.env` key count not 65; `tools/list` changing from 103; md5 beyond the take list; the md5 of any of dell1's four harvest files not equal to its blob; host memory above 85 percent; `NRestarts` above 0; the listener answering any call with no lease; the marker not equal to the release sha; no `POST /mcp` access line under traffic in the 30-minute read-back; any `audit-lake WARN` line in the journal during the read-back; **a `gateway_busy` refusal for a single sequential call**; **the parallel-load proof reading `/health` non-200**.

## 8. Gate lines

process-wide state this change touches: The service imports one new module, app/inflight_guard.py, whose module-level instance `guard` is a process-wide object (constants MAX_INFLIGHT 26 and QUEUE_WAIT_S 20.0; the asyncio primitives are created lazily inside the running loop, so import creates no semaphore, task or loop), and app/tools.py's _PolicyGuardedMCP.call_tool, the dispatch chokepoint of EVERY tool, now runs the tool body inside `async with inflight_guard.guard.slot(name)` after the entitlement denial (a denied call takes no slot): a call beyond the 26-th concurrent one waits up to 20 s and is then returned as an enveloped gateway_busy refusal, audited as denied/gateway_busy. app/harvest_typed.py's project() (used by every typed tool and the client core) now measures size as json.dumps(indent=2). READ, not instrumented: I opened app/inflight_guard.py whole (76 lines: imports asyncio, contextlib and typing, two constants, the Busy exception, the InflightGuard class and `guard = InflightGuard()`), the OG-mg-3 hunks of app/tools.py (the added import and the try/except around call_tool; no other module-level statement) and the OG-sz-1 hunks of app/harvest_typed.py (the _size measure and project()). No logger, handler, signal, thread, socket, environment read, sys.path change or global-config change happens at import. tools/list does NOT change: the candidate registry counted 103 tools on the host against 103 at the live ref (no tool is added). Nothing arms the probe listener or writes any parameter.

I read: the release diff against the live ref (26 files), `app/inflight_guard.py` whole, the OG-mg-3 hunks of `app/tools.py`, the OG-sz-1 hunks of `app/harvest_typed.py`, the OG-mg-3 test's burst, the live-ref/trunk lineage of each taken file. No IAM, Terraform, env, unit or deploy-script change. The window's caller identities are read at the start of Phase B (`OG-rz-2`'s method). No account number, person's name, credential or object content appears in any record.

## 9. The three halves (sign ONCE, on `release_sha` `8e3eddf95916e430e4e9bbf615ca4fd91f9e852f` and this ask's sha256)

### CTO half (`1.0.0_SA_CTO~Z`)

To be signed on `release_sha` and this ask's sha256, with the widening (section 3), the take list and the `OG-rt-1` hold-back (section 1) and the new `gateway_busy` refusal and the cap 26 (section 3) read.

### COO half (`2.0.0_SA_COO~O`)

To be signed on `release_sha` and this ask's sha256, with the Phase A measurements (section 2), the window (section 4) and the triggers (section 7) read.

### CVO half (`3.0.0_SA_CVO~Z`)

To be signed on `release_sha` and this ask's sha256, with the process-wide state line (the verdict 35844; section 8), the widening (section 3) and the suite difference named (section 2) read.
