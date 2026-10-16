# NEVER-WIDEN ASK -- `OG-ap-31` -- the round-39 batched gateway release (one code-only deploy of `opal-gateway`)

Applier: `0.7.0_AE_CloudOps~NFRA1`. Order: `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ap-31.round-39-batched-release.md`. GO for Phase A: msg 35256.
Record: `ap31_release.json` in this folder: `base_sha` bf9d23b518527e0e5f9a26aa240fd5af72af6c11 (the live ref), `release_sha` 4be300110ec912ac8c11a1663403e41eea45117c, `trunk_sha` de8078d5453795eb7d6e4c1507882f247d7be8e9.
Phase A is READ ONLY against the world: nothing is deployed, applied or written to any bucket or table. The release exists as one commit on the local branch `rel-nfra-oplgtw-batch3` in `C:/tmp/og-rel-batch3`.

## 1. The diff, by file (base..release, 12 files, 1495 insertions, 81 deletions)

App code (4 files, taken whole from `trunk_sha`; all 44 live-to-trunk hunks attributed to a named order, 0 unattributable, `ap31_attr.json`):

| file | hunks | order |
|---|---|---|
| `app/client_adapter_bd49f.py` | 37 | OG-en-13 (units, currency, numbers, `as_of`), OG-en-15 (windowed partitions, exact-duplicate removal) |
| `app/data_entitlement.py` | 2 | OG-en-14 (route class on the email-deny guard) |
| `app/server.py` | 4 | OG-en-14 (the browser branch passes `internal_page`) |
| `app/integrations/opal_discover/integration.py` | 1 | MX-c-24 (bucket, vendor and firm echo; 6 lines) |

Tests (8 files): `test_og_en13.py`, `test_og_en14.py`, `test_og_en15.py`, `test_discover_echo.py` (new); `test_opal_discover.py`, `test_og_cl2.py`, `test_login_admit_r24.py`, `test_scoped_consent_r253.py` (changed). `test_og_en4`, `test_og_en12`, `test_og_ch1`, `test_og_en8`, `test_owner_gate` are named by the orders and byte-equal to the live ref (no change).

NOT in the release: `tools.py`, `destructive_ops.py`, `deploy-to-ec2.sh`, `EC2_MANIFEST.json`, any Terraform, any registry file, any data copy. The release diff holds no manifest or deploy-script change (`ap31.AC1` reads it). The 11 other app files that differ between the live ref and trunk (`admin_people_access.py`, `family_depth.py`, `harvest_*.py`, `refs/partner_roster.json`, `refs/silver_families.json`, the yearinreview files, `tools.py`, `destructive_ops.py`) belong to no named order and stay at the base.

Seams: 51 distinct modules over 84 importer edges (`ap31_seams.out`); 48 are in the take (3) or byte-equal to trunk at the base (45). 3 modules, over 4 importer edges, are base files that differ from trunk and are not taken (`data_entitlement` and `test_og_en8` -> `tools.py`; `server` -> `yearinreview_view.py`; `test_opal_discover` -> `destructive_ops.py`). Each was checked by NAME (`ap31_seamcheck.py`): the names the importer uses (`mcp`; `is_yearinreview_path`, `yearinreview_page`, `yearinreview_redirect`; `OpClass`, `classify`) have identical AST at the base and at trunk. 0 of 7 names unsatisfied.

## 2. The widening, stated plainly

- NO new IAM, NO new environment key, NO tool added or removed (`tools/list` is 103 before; AC2 requires the same after). No Terraform. No deploy-script or manifest change at the release commit.
- The 49F transactions and fees answers now read up to 60 dated files per call (`MAX_WINDOW_PARTITIONS = 60`): more S3 reads of the same four prefixes through the same dedicated role `gateway-49f-blackdiamond-live-read-role`, master_admin only. `window_partial` is true only when the cap cut the window.
- **A change in what an analyst sees.** The `transaction_id` dedupe is replaced by exact-duplicate removal: a row is dropped only when every emitted field equals an earlier row's (`exact_duplicates_removed`). The `transaction_id` rule was dropping real rows: in the newest transactions partition 2727 ids repeat across 14132 rows, and none of those groups is byte-identical (rows Z-S314 and its A2 measurement). Counts of transactions served for the same account therefore rise.
- Answers gain `weight_unit` / `weight_unit_basis` (allocation: `null` with `not_established`, because the live scale could not be established, row Z-S313), `currency` / `currency_basis` (transactions and fees: `null` with `source_absent`; `source_mixed` if rows disagree), `exact_duplicates_removed`, `partitions_in_window`, `partitions_read` and `partitions_read_dates`. Figures serve as JSON numbers at 6 decimals (weights) and 2 (money); `as_of` is the partition date when the caller gives none.
- The browser deny guard: on the four internal browser routes (`/login`, `/sprint`, `/rivalfunds`, `/yearinreview`), an email that is EXACTLY one `MASTER_ADMIN_EMAILS` entry passes before the store is read. Every other email, the `/callback` consent branch and every caller that passes no route class keep the record verdict. A denied non-admin (including `alyssa@opalinvest.com`) stays refused. **Measured on the host (names and counts only): `MASTER_ADMIN_EMAILS` holds 1 entry; `andrew@opalinvest.com` is that entry; `opalbloomberg@opalinvest.com` and `alyssa@opalinvest.com` are not members** (`ap31_roster.json`; the code default is also the one entry). So the exemption reaches Andrew's address only. The `opalbloomberg@` record was deleted at OG-ap-30, so it is not refused today, but a deny written for it later would refuse it on these routes (row Z-S322). Widening the roster is an env change and outside this order.
- The discover answers echo `bucket`, `vendor` and `firm` when the row carries a non-empty string.
- No object or item is written to any bucket or table by this release.

## 3. The order of acts (Phase B, only on the issuer's GO naming all three halves at `release_sha`)

1. Re-read the live ref and the host `.env` (65 keys, `MUSE_CLIENT_ID` absent); any mismatch is a STOP.
2. Open ledger `nfra-oplgtw-gateway-release-batch3` (entry and sentinel first).
3. ONE deploy: `infra/aws/ec2/safe-ec2-deploy.sh` with `DEPLOY_BASE_REF=bf9d23b518...` from `C:/tmp/og-rel-batch3`, no `HALT_OVERRIDE`, under the stale-base guard.
4. Read back against the triggers; then the served read through the installed code and the public endpoint (five arms e1, e2, e3, e4, e6), `CODE3_SERVED.json`.
5. Close the ledger, standing clauses, `ap31.AC2`.

Before the deploy tree's clean check, Phase B restores the uncommitted overlay (section 7) to the live ref's bytes.

## 4. Both branches

- The owner on the internal browser routes: the guard does not read the store for an exact roster email; the route answers as it did before the 11:22Z deny.
- A denied non-admin: refused 403. An unreadable store for a non-admin: 503. A caller with no route class: unchanged record verdict.
- A window with 61 or more partitions: the newest 60 are read, `window_partial` is true, `partitions_read` is 60. A window with 60 or fewer: all read, `window_partial` false.
- A source with no currency: `currency` null, `currency_basis` `source_absent`. An allocation scale not established: `weight_unit` null, `weight_unit_basis` `not_established`.

## 5. Rollback

Redeploy the base `bf9d23b518527e0e5f9a26aa240fd5af72af6c11` through the same wrapper (`DEPLOY_BASE_REF` set to the release commit for the reverse stale-base read); the live release is a code-only tar of the same layout, so no data, key or IAM undo exists or is needed. The base's host md5 is recorded: 139 of 139 equal (`ap31_host_md5.json`).

## 6. Triggers (roll back AT ONCE, file an ARMED row naming `2.0.0_SA_COO~O`)

`/health` is not 200 within 90 seconds; the `tools/list` count after differs from 103; the `.env` key count is not 65 or `MUSE_CLIENT_ID` appears; host md5 shows any file other than the 12 released paths differing from the release blobs; the owner or a non-admin answers differently from section 4 on arm e4; any existing route that answered 401/403 to no identity stops doing so. A miss in the e1, e2, e3 or e6 served read alone is graded FAIL as measured, a row is opened, and the issuer decides.

## 7. Gates, tests and disclosures

- The release commit under `GIT_COMMIT_AUTHOR_OVERRIDE=CLOUD_OPS_OR_ETL` (audited): `NAMING-GATE: PASS 0 graded`; no prelude registry commit was needed (0 registry files in the diff). One WARN printed: `client-data-check: hashed account-id list ABSENT at ~/.opal/account_id_hashes.txt -- this commit was NOT checked for client account ids` (the 12 files hold code and tests, no data).
- **Uncommitted gate overlay (the OG-ap-28 precedent).** The live ref's naming module and schema are an inconsistent pair: `lib/opal_naming.py` reads `cadence.interval_form`; the live `org/standards/NAMING_SCHEMA.json` lacks it, so the commit-time gate could not load (`KeyError: 'interval_form'`, first attempt, refused). 27 gate-input paths (14 added, 13 modified: `.tools/naming-*`, `infra/logic/**`, `lib/opal_naming*`, the schema, `DIRECTIVES.yaml`) were laid from `trunk_sha` as an UNCOMMITTED working-tree overlay (`ap31_overlay.json`); the release commit names its 12 paths explicitly and carries none of them.
- Tests: the 13 named files, 103 passed in the forward order and 103 passed in the reverse order (`ap31_tests.out`). The whole gateway suite in the sparse release tree: 74 failed, 1020 passed; the same suite at the pristine live ref: 78 failed, 978 passed. Failing in the release and NOT at the live ref: 0. Failing at the live ref and not in the release: 4 (all `test_opal_discover.py`, fixed by the take). The 74 carried failures are listed by name in `ap31_full_release.out`.
- Host-shaped import check (zero reads, with and without `lib/opal_naming.py`): 6 of 7 modules import; `server` needs the host `.env` (`TENANT_ID`) at import, as it does at the live ref (`ap31_hostshape.json`).
- Live ref: manifest `deployed_commit`, the S3 ref and the host agree on bf9d23b518; host md5 139 of 139 equal, 0 differ, 0 missing, 0 extra; `.env` 65 keys, `MUSE_CLIENT_ID` absent; `tools/list` 103 (registry 103); `gateway-49f-blackdiamond-live-read-role` resolves.
- `NFRA_MCPINDEX.TO-MX-c-24` reads `<status>issued</status>` in its order file though trunk holds its commit and the GO names it; the take follows the GO and the order text.

## 8. The three halves

### CTO half (`1.0.0_SA_CTO~Z`)

To be signed against this ask's sha256 and `release_sha` 4be300110ec912ac8c11a1663403e41eea45117c.

### COO half (`2.0.0_SA_COO~O`)

To be signed against this ask's sha256 and `release_sha` 4be300110ec912ac8c11a1663403e41eea45117c.

### CVO half (`3.0.0_SA_CVO~Z`)

To be signed against this ask's sha256 and `release_sha` 4be300110ec912ac8c11a1663403e41eea45117c.
