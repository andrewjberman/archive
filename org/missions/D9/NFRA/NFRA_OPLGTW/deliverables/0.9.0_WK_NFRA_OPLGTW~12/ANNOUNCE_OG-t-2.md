# ANNOUNCE_OG-t-2 -- PHASE A (pre-GO), `0.9.0_WK_NFRA_OPLGTW~12`, 2026-09-30

PHASE A only. Nothing was uploaded, no ledger is open, the host was touched only by read-only SSM. No tid/oid value is
written here: the hand-off values come from `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/PART_D_RECORD_20260930.md`
@205c2e7f6c and appear in no committed file.

| item | value |
|---|---|
| live commit (host md5 authority) | `42c52ed4d9e834b0f1cf4f96eb83f9b0f7a183df` (EC2_MANIFEST `deployed_commit`, MX-r-6 v3, S3 object 2026-09-30T18:33:41Z, `git-ref` metadata = the same sha) |
| release branch | `rel-nfra-oplgtw-tier-auth` at `/c/tmp/og-rel2` |
| release HEAD | `d61fde46933221e8afbac7418f06d7525d3347c8` (3 commits on live) |
| rollback tree | `/c/tmp/og-rb2` detached at the live commit, mcportal at the pin |
| mcportal | `a3bff71ffa3f5c73aa0fb7ea1e7386434e233054` = manifest `mcportal_commit`, unchanged |

## Step 1 -- live commit and release order, by CONTENT

- Manifest `services.opal-gateway.deployed_commit` = `42c52ed4d9` (A1: the host's 13-file md5 read is the authority, below).
- Host vs commit bytes, read-only SSM (command a147e0f1-f6ce-4462-a53b-74d7d26826d9, Success): md5 of the 13 files
  (`tier guard tools token_broker server ratelimit oauth_as config`, `integrations/base`,
  `integrations/schwab/{engine,integration,export,envelope}`) equals `git show 42c52ed4d9:<file>`: **13 of 13 match**.
- OG-x-3 shipped, by content: `0c3d545002` (OG-x-2) added 490 non-blank gateway lines (app + tests); whitespace-insensitive,
  **460 present in live, 30 absent**: 27 in `engine.py` (OG-x-4's rewrite: the live `engine.py` md5 `42445b377079` equals the
  bytes at `132a07ee11`) and 3 in `tests/test_schwab_export_stream.py`. Same numbers A1 gave (460 of 490; 27; 3). Not
  attributed further: the 3 test lines.

## Step 2 -- release tree

- `git worktree add -b rel-nfra-oplgtw-tier-auth /c/tmp/og-rel2 42c52ed4d9` (created `--no-checkout`, sparse cone widened:
  `.tools lib infra/aws/ec2 infra/logic org/critical_paths org/mcp org/ref org/modules/graph org/standards
  org/missions/D9/NFRA/NFRA_OPLGTW`, which the commit gates need).
- `git cherry-pick --no-commit b5a585cf2f 344cca64a1 c4d2274c6d 0906bf01e5` (oldest first, all four applied by diff although
  git calls each an ancestor of live). rc 0, no empty pick; 14 gateway paths changed, none outside `infra/aws/ec2/opal-gateway`.
  11 of 14 files are byte-equal to the last build commit that touched them; `config.py`, `server.py`, `test_principal_cutover.py`
  auto-merged onto newer live bytes and their diff stat equals their build commit's (32, 12, 4 lines).
- Commits (all `GIT_COMMIT_AUTHOR_OVERRIDE=0.9.0_WK_NFRA_OPLGTW~12`, audited; three uses, one per release-branch commit):
  `2be69ae621` (the 11 modified files), `cd7621b4da` (the 3 files the build commits ADD, left untracked by the first path list),
  `d61fde4693` (`deploy-to-ec2.sh`).
- Census, `git diff --stat 42c52ed4d9 HEAD -- infra/aws/ec2/opal-gateway`: **15 files changed, 774 insertions, 42 deletions**;
  files outside the gateway directory: 0. The 15 = the 14 build-cell files + `deploy-to-ec2.sh` (step 6).

## Step 3 -- tests on the release tree (`AUDIT_PATH` isolated; `audit.jsonl` not dirtied, tree clean)

- `tests/test_tier_principal.py tests/test_auth_hardening.py tests/test_dcr_idle_lifetime.py tests/test_min_tier_gate.py
  tests/test_attachment_tools.py tests/test_owner_gate.py tests/test_email_deny.py tests/test_sprint_view.py`: **50 passed**, 1 warning, rc 0.
- `tests/test_ratelimit.py` in its own process: **6 passed**, rc 0.

## Step 4 -- blast-radius pre-read (R-3 (e); Q1)

Instruments: a consistent full scan of `gateway-access-state-table` (303 items) and the host `audit.jsonl` over the last 14 days
(cutoff 2026-09-16T22:27Z: 119,355 lines total, 0 unparseable, 34,559 in window). OLD tier = the live `tier.py` bytes on the
email; NEW tier = the release `tier.py` (`resolve_tier` on the principal, with the hand-off rosters) for persons and the
release `token_broker._machine_tier` rule for server-held identities. The email rosters read: admin 1, write-capable 2
(host `.env`, read-only SSM, key lines only).

| class | identities | OLD -> NEW | delta |
|---|---|---|---|
| table principals (POLICY partition + refresh-family principals, union) | 3 (admin, write #1, write #2; all 3 hand-off principals present) | MASTER_ADMIN -> MASTER_ADMIN; STANDARD -> STANDARD (x2) | 0 |
| audit persons with no principal on record | 2 (sprint_view, denied, tier blank) | READ_ONLY -> READ_ONLY | 0 |
| server-held machine identity (MS-ingest identity = OTP mailbox; callers `ms` 15,837, `49f` 115, `cot` 5 records) | 1 | MASTER_ADMIN -> MASTER_ADMIN (email-roster rule, unchanged) | **0 (machine callers: 0 deltas)** |
| synthetic probe partitions (`probe-og-i1-*`, 2026-09-16) | 3 | no tier either side | 0 (the allowed fixture class) |
| **denominator** | **9 identities** (3 + 2 + 1 + 3); audit users 6 (5 persons/machine email + 1 blank-user cred-observe class) | | **0 deltas** |

- The audit's observed `tier` per person equals the live rule on the email: admin `master_admin` 789 calls, write-capable
  `standard` 25 + 1,969 calls, 0 mismatches. Every tier-bearing tool call arrives on `/mcp`, whose `_bearer_auth` always sets a
  principal (`server.py` 180); the GUI path (`/login`, `/sprint*`) sets an email only and resolves no tier.
- `oauth_client` under OG-u-2's 30-day idle lifetime at release time (2026-09-30, evening UTC, the scan's own clock): 6 records, none carries an
  `expires_at` (expiry computed from `created_at + 2592000 s`): **EXPIRED at `get_client` 0 of 6; EXPIRED at an exchange
  (not held by a live family) 0 of 6.** The operator's upload client (`identity_tool_allowlist.txt:19`) is **not** among them: age 12.3 days,
  expires in 17.7 days (about 2026-10-18). Its one refresh family is revoked (`refresh_token_reuse`, last used 2026-09-29),
  so nothing holds it past that date (row Z-W12-S7). 5 other clients hold 7 live families.
- No STOP condition fired: no delta, and the operator client is not expiring.

## Step 5 -- mcportal pin and rollback proven (built, not uploaded)

- `/c/tmp/og-rel2/mcportal` and `/c/tmp/og-rb2/mcportal`: clones of `/c/tmp/mx-rb9/mcportal` with its `node_modules` copied in;
  HEAD in both = `a3bff71ffa3f5c73aa0fb7ea1e7386434e233054` = manifest `mcportal_commit`.
- `/c/tmp/og-rb2` at `42c52ed4d9` (clean, unedited): `bun install --frozen-lockfile` "Checked 77 installs across 128 packages
  (no changes)"; `bun run build` produced `dist/index.html`. A build-only mirror of the deploy's tar step gives 427,688 bytes,
  87 files. Live `s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/opal-gateway-42c52ed4d9.tar.gz`: 427,691 bytes (head-object),
  87 files, `git-ref` metadata = the live sha. `diff -rq` of the two extracted trees: **empty, 87 of 87 identical** (the
  3-byte container difference is gzip metadata).
- Re-deploy (rollback) command, run with `DEPLOY_BASE_REF` = the release commit's full sha read at act time:
  `cd /c/tmp/og-rb2 && DEPLOY_BASE_REF=<live full sha at that time> HALT_ACK=1 AGENT_NAME=0.9.0_WK_NFRA_OPLGTW~12 bash
  infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`. The live template needs no
  principal variables and renders the old `.env` (33 keys). `safe-ec2-deploy.sh` does not name `DEPLOY_BASE_REF`; it runs
  `bash "$DEPLOY_SCRIPT"` with the inherited environment, and `deploy-to-ec2.sh` reads it (A1 item 3: honoured through the script).

## Step 6 -- `.env` render

- Live template (`42c52ed4d9`): **9 `%s`, 9 printf arguments**. Release template (`d61fde4693`): **11 `%s`, 11 arguments**.
- The one change: `MASTER_ADMIN_PRINCIPALS=%s` and `WRITE_CAPABLE_PRINCIPALS=%s` after `WRITE_CAPABLE_EMAILS`. The values are
  NOT in the file: they come from `OG_MASTER_ADMIN_PRINCIPALS` and `OG_WRITE_CAPABLE_PRINCIPALS` in the deploying shell, and a guard
  refuses (exit 3, before any build or upload) when either is unset or an entry is not a `<tid>/<oid>` GUID pair (row Z-W12-S6).
- Rendered with the hand-off pairs in memory: **35 keys, 35 unique** (live 33; added 2, removed 0, shared values changed 0);
  both principal lines equal the pairs as handed (1 admin pair, 2 write-capable pairs); the four email roster keys stay.
- `ENABLED_INTEGRATIONS` renders `ycharts opal_portal globgrph opal_discover portal_index schwab`, the live six-id value (host
  read 2026-09-30). The order's three-id literal is stale; the release keeps live's value (row Z-W12-S4).

## Rows filed (INVESTIGATION_v1.md)

`NFRA_OPLGTW-Z-W12-S4` (ENABLED_INTEGRATIONS literal stale; AC3 reads FAIL on the literal; ARMED),
`-S5` (AC2's allowed set omits `deploy-to-ec2.sh`; AC2 reads FAIL; ARMED),
`-S6` (principals rendered from deploy-time env, not committed; INERT),
`-S7` (operator client does not expire at release; revoked family holds nothing; INERT),
`-S8` (census: one real POLICY partition with an active email_deny, 3 probe fixtures; INERT).

## At GO (not done; PHASE B is not authorized)

Two things the issuer must supply beyond the order: (1) the two principal environment variables above, exported in the
shell that runs step 10; (2) a ruling on rows S4 and S5 before the criteria run. Step 10 becomes
`cd /c/tmp/og-rel2 && OG_MASTER_ADMIN_PRINCIPALS=... OG_WRITE_CAPABLE_PRINCIPALS=... DEPLOY_BASE_REF=<live full sha at act time>
HALT_ACK=1 AGENT_NAME=0.9.0_WK_NFRA_OPLGTW~12 bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway
infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`; repeat the step-1 13-file read immediately before it and STOP on drift. The
release tree shows `M mcportal` (the clone sits in the tracked gitlink directory); never stage it.
