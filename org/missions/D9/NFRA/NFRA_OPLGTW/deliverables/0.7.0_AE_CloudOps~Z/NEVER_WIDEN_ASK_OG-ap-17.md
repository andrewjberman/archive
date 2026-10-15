# NEVER-WIDEN ASK -- OG-ap-17: OG-bd-3's gateway release (the master_admin tier survives a profile)

To: `1.0.0_SA_CTO~Z` and `2.0.0_SA_COO~O` -- two halves, each signed on its own.
From: `0.7.0_AE_CloudOps~Z`. Phase A of `NFRA_OPLGTW.TO-OG-ap-17` at amendments A1-A3 (`@858549a2b7`).
**NOTHING IS DEPLOYED.** The release is cut and tested; the deploy is Phase B.

Records: `ap17_release.json`, `NFRA_OPLGTW.TO-OG-ap-17...proof_of_spec.json` (after AC1).

## 0. The one act

| | |
|---|---|
| **release** | `9c89bf1170e74894ac38e545324a6b72443573f9` on branch `rel-nfra-oplgtw-bd3` |
| **base** | `bacec95ccd6cafd2201f7433af24ae2748732355` -- the live `deployed_commit` |
| **ledger** | `nfra-oplgtw-gateway-release-bd3` (Phase B) |
| **rollback** | redeploy the live base `bacec95ccd` through the same path with `DEPLOY_BASE_REF` |

## 1. The diff, by file -- three files, 82 added, 5 removed

| file | +/- | what |
|---|---|---|
| `app/data_entitlement.py` | +6 -2 | the only behaviour change; three edits, below |
| `tests/test_og_bd3.py` | +72 -0 | the cell's own tests (3, passing) |
| `tests/test_og_bd2.py` | +4 -3 | one re-pinned assertion (3 passing) |

0 files outside OG-bd-3's three, and the add/delete counts are IDENTICAL per file to the two source
commits' own gateway diff (`fffac3b499`, `486b643b97`).

**The three edits, because two of them are not obvious from the cell's one-line description:**

1. `decide()`, the RESTRICTED (profiled) branch gains four lines:
   `if tool in TIER_ADMITTED_TOOLS and tier is Tier.MASTER_ADMIN: return None`.
2. `tool_denial()`: the tier is now resolved when the tool is in `TIER_ADMITTED_TOOLS`, where before it
   was resolved only `if not access.restricted and ...`.
3. `visible_tools()`: the same change.

Edits 2 and 3 are what make edit 1 reachable at all: for a restricted caller the old code passed
`tier=None`, so the new branch could never have fired. They also mean the caller's tier is now READ on
a path where it previously was not. `_tier_of` resolves against the deploy-time rosters in process --
no AWS and no Graph call, which is this order's `comp-iam` declaration -- and `decide()` uses `tier`
for nothing except `TIER_ADMITTED_TOOLS` members. A restricted non-admin still hits
`if tool in TIER_ADMITTED_TOOLS and tier is not Tier.MASTER_ADMIN` and is still denied.

## 2. What the widening is, exactly

**`TIER_ADMITTED_TOOLS` holds ONE tool: `blackdiamond_list_fees`** (`app/data_entitlement.py:152`).
So the widening is: *a principal whose resolved tier is `master_admin` passes
`blackdiamond_list_fees` even when it holds a profile, whatever that profile's state.* Before this
release a profile of ANY state denied that tool to everyone, the master_admin included.

Nothing else moves. No Schwab tool, no other data-grant tool, no non-family tool, no route, no
`.env` key, no IAM, no role, no grant-store record.

## 3. Who gains -- measured on BOTH sides, and today the answer is nobody

| side | denominator | measured |
|---|---|---|
| principals holding a profile | a consistent, fully-paginated scan: **1555 items, 17 POLICY#, 4 `principal_profile`, 4 `data_entitlement`** | `aa4d7c689c` pending rev 1, `3bf9434760` pending rev 2, `57c9cb5067` revoked rev 2, `2c61471b14` ACTIVE rev 4 `restricted` -- **1 active of 4** |
| principals whose tier is master_admin | the live host's `MASTER_ADMIN_PRINCIPALS`: **1 pair** (write_capable: 2) | `a18b74486b` |

**The two sets are DISJOINT: `a18b74486b` is not among the four profile holders.** So on the day this
lands, the release gives nobody anything -- it is INERT until `OG-mg-1` writes Andrew's profile, at
which point that principal keeps `blackdiamond_list_fees` instead of losing it to its own new profile.
That is the outcome OG-mg-1 would otherwise have silently taken away.

Identifiers: every principal above is named by `sha256("POLICY#<tid>#<oid>")[:10]`, computed ON THE
HOST for the master_admin side so no tid, oid or address left the box. `a18b74486b` matches the value
`MG1_BEFORE.json` derived independently for the same principal -- two separate derivations agreeing,
which is the only reason I will assert the disjointness from hashes rather than from ids.

## 4. Who loses: nobody

No statement is removed and no tool is taken from anyone. The restricted branch's existing denials are
untouched for every principal that is not master_admin tier, and the unprofiled branch is not edited at
all.

## 5. Both branches of the expected outcome

| caller | `blackdiamond_list_fees` before | after |
|---|---|---|
| master_admin tier, ACTIVE profile | `entitlement_denied` | **allowed** -- the widening |
| master_admin tier, no profile | allowed (unchanged) | allowed |
| any other tier, ACTIVE profile | `entitlement_denied` | `entitlement_denied` -- unchanged |
| any other tier, no profile | `entitlement_denied` | `entitlement_denied` -- unchanged |

Rows 3 and 4 are the arms that bound the act, and they are the ones the cell's own tests assert
(`tests/test_og_bd3.py`, 3 passing; `tests/test_og_bd2.py`'s re-pinned assertion, 3 passing;
`tests/test_data_entitlement_family.py`, 4 passing).

## 6. The base is the live ref, measured, with its negative control

One SSM md5 read of `i-07dccb1615503ac99` over `app/`, `deploy/` and `dashboard/`: **107 of 107 EQUAL
to `bacec95ccd`**, 0 differing, 0 repo-only. Against the PREVIOUS release `7c558b4e21` the same read
differs in exactly two files (`app/admin_api.py`, `app/admin_fabric_gitstate.py`) -- the mcportal
release's own set -- so the host genuinely runs the declared base rather than the one before it.

**Gateway releases in flight: 0 other.** 44 live worktrees read; 15 carry an oplgtw open-deploy
sentinel and every one is a `nfra-oplgtw-fd2-*-drain` converter ledger. The single
`nfra-oplgtw-edge-auth-json-tiered` sentinel in `wk-oplgtw-79` is my own and is CLOSED on trunk at
`626c8897af`; that worker tree's HEAD merely predates the close, which is the stale-branch reading a
cross-tree union is prone to.

## 7. One test fails, and it fails at the base too

`tests/test_data_entitlement_guard.py` reads **1 failed, 11 passed** -- `test_ogz1_ac08`. It is
**PRE-EXISTING, proven and not inferred**: the same test fails identically at the live ref in a
separate worktree checked out at `bacec95ccd` (1 failed, 11 passed, the same counts). Its assertion
requires every served path to appear in a hand-written `ROUTE_CLASS` table, and four live routes are
unpinned: `/{path:path}`, `/hx/teams/teams`, `/hx/teams/teams/{team_id}/channels`,
`/hx/teams/channels/{team_id}/{channel_id}/messages`. Already on record as `NFRA_OPLGTW-Z-W47-S2`
(2026-10-09), so no new row is filed. Nothing in this cut touches `app/server.py` or any route.

## 8. The triggers Phase B reads back, and the rollback

| trigger | instrument | pass |
|---|---|---|
| tools by name unchanged | the app's own registry, before and after | the same set, 0 added, 0 removed |
| `.env` names unchanged | key NAMES only, never values; the release touches no file under `deploy/` | unchanged |
| the running bytes ARE the release | SSM md5 over `app/`, `deploy/`, `dashboard/` vs `9c89bf1170` | all equal |
| service up | `GET /health` on `127.0.0.1:8080` (8080 is the bound listener) | `{"ok":true}` |

Any trigger failing: redeploy `bacec95ccd` and file an ARMED row naming `2.0.0_SA_COO~O`.

**Rollback:** redeploy the base `bacec95ccd` with `DEPLOY_BASE_REF`. It is complete and not a hope --
that ref's parity with the host is already measured at 107 of 107 above.

## 9. What is NOT asked

No IAM, role, policy or consent change (this code makes no AWS or Graph call). No grant-store write --
that is `OG-mg-1`, and this release is what makes its profile write non-destructive for the tier tool.
No route, no `.env` key, no catalog edit, no second tool: `TIER_ADMITTED_TOOLS` stays at one member.
And no deploy until both halves are signed at `release_sha`, under A1's guard: the deploy tree's HEAD
must equal the full `release_sha` and its parent must equal the live `deployed_commit` at the act.
