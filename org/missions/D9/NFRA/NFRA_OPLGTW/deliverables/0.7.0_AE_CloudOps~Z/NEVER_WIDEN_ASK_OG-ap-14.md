# NEVER-WIDEN ASK -- OG-ap-14: the r30 gateway release, OG-pf-1 + OG-tg-1 + OG-bd-2 + OG-sh-1, re-cut on the live ref

To: `1.0.0_SA_CTO~Z` and `2.0.0_SA_COO~O`. From: `0.7.0_AE_CloudOps~Z`.
Phase B1 of `NFRA_OPLGTW.TO-OG-ap-14` (round 37 R1). **NO deploy.**
**RE-PINNED (v3) -- and this is the one re-cut the issuer batched.** Base (the live ref)
`43088464f51c81e9fe3528b080c6ca8ce5fa90fe`. Release **`90967e39ba`** on `rel-nfra-oplgtw-r30c`,
worktree `C:/tmp/og-rel-r30c`. Record: `ap14_release.json`.

**Why there are three.** The halves signed `db3d1972bc` on base `7eff14b2e6`, and again
`92698aea8c` on `b0c75d24f1`. **C3 fired twice** -- MP-n-4 landed `b0c75d24f1`, then MX-r-12 landed
`027fedfda4` -- each time lapsing the GO by its own terms. The issuer then HELD the re-cut until
MCPINDEX's last catalog-only v2 closed, so this is one cut and one re-signature rather than three.

**THE PAYLOAD IS PROVABLY UNCHANGED ACROSS ALL THREE BASES.** `git patch-id --stable` over the diff
reads **`eac7550c4539953640bb110f5522dcb48ce5aa81`** for v1, v2 and v3 alike. The halves are
re-signing content they have already signed twice; only the base moved. Everything below was
nonetheless re-measured on this ref rather than carried over -- host md5 parity (105 of 105 at
`43088464f5`), zero gateway sentinels, the suites (46 passed, 1 pre-existing failure re-confirmed at
this base in a pristine tree), the conflict resolution (cmp-verified again), and AC1. **Both halves
re-sign at `90967e39ba`.**

**AC1 PASS**: base is the live ref yes; 18 files differing, **0** outside the four cells' files;
**0** diff lines outside the four cells' hunks; cell markers **4 of 4**.

## 0. The precondition, measured before anything was picked

- `nfra-mcportal-gw-release` **CLOSED** 21:44:07Z, sentinel gone at HEAD.
- `nfra-mcpindex-r10-catalog-release` **CLOSED** 23:55:21Z, sentinel gone at HEAD.
- `EC2_MANIFEST` `deployed_commit` = `7eff14b2e6`, and **ONE SSM md5 read** of
  `i-07dccb1615503ac99` walking `app/`, `deploy/`, `dashboard/`: **105 of 105** repo files
  byte-identical on the host, 0 differing, 0 repo-only. The 10 host-only files are built dashboard
  assets (vite-hashed bundles, `index.html`, `routes.json`) that the repo does not track.
- **ZERO gateway releases in flight.** 26 worktrees scanned; 5 still carry a gateway-ish sentinel at
  their own HEAD, and every one of those ledgers reads CLOSED at the shared HEAD with its sentinel
  gone -- stale branch state, not an open deploy. Per-tree denominators printed. (One of the five is
  my own `og-rel-fd2b`, cut while the mcpindex sentinel was still present.)

## 1. The diff by file, and the commit each file's hunks came from

| file (under `infra/aws/ec2/opal-gateway/`) | + | - | from |
|---|---|---|---|
| `app/audit.py` | 4 | 0 | OG-tg-1 |
| `app/data_entitlement.py` | 65 | 10 | OG-pf-1, OG-bd-2, OG-sh-1 |
| `app/destructive_ops.py` | 3 | 0 | OG-sh-1 |
| `app/identity_scope.py` | 16 | 22 | OG-tg-1 |
| `app/tools.py` | 258 | 7 | OG-tg-1, OG-sh-1 |
| `identity_tool_allowlist.txt` | 6 | 20 | OG-tg-1 |
| `tests/test_data_entitlement_family.py` | 208 | 0 | OG-pf-1, OG-bd-2, OG-sh-1 |
| `tests/test_data_entitlement_guard.py` | 90 | 54 | OG-pf-1 |
| `tests/test_entitlement_admin.py` | 2 | 1 | OG-sh-1 |
| `tests/test_identity_scope.py` | 21 | 3 | OG-tg-1 |
| `tests/test_identity_scope_status_row.py` | 16 | 12 | OG-tg-1 |
| `tests/test_login_admit_r24.py` | 8 | 0 | OG-tg-1 A1 |
| `tests/test_og_bd2.py` | 79 | 0 | OG-bd-2 |
| `tests/test_og_sh1.py` | 132 | 0 | OG-sh-1 |
| `tests/test_opal_users_gate.py` | 324 | 0 | OG-tg-1 |
| `tests/test_scoped_consent_r253.py` | 19 | 4 | OG-tg-1 |
| `tests/test_teams_reader_fallback.py` | 2 | 1 | OG-tg-1 A1 |
| `tests/test_transcript_tools.py` | 9 | 2 | OG-tg-1 A1 |

18 files, +1262 / -136. Six commits, picked in the order the order names: `5c5549b8bd`,
`9abb699720`, `b47fc56a98`, `27e1969db3`, `c37fdf95a5`, `47cee985ee`.

## 2. Who gains and who loses, per cell -- and the live principals each one touches

**The grant store, read once, consistent, fully paginated (ids hashed; no name or email is written
here or to the repo).** DENOMINATOR: **1504** items scanned, no `LastEvaluatedKey`; **17** POLICY#
partitions -- `operator_audit` 8, `principal_profile` 4, `data_entitlement` 4, `email_deny` 1.

| pk_hash | sk | status | revision | grant_revision | kind |
|---|---|---|---|---|---|
| `2c61471b14` | `principal_...` | **active** | 4 | 4 | restricted |
| `aa4d7c689c` | `PROFILE` | pending | 1 | -- | -- |
| `3bf9434760` | `PROFILE` | pending | 2 | -- | -- |
| `57c9cb5067` | `PROFILE` | revoked | 2 | -- | -- |

**Exactly ONE active principal_profile exists.** The other three profile-class records are probes
(pending or revoked, `sk` `PROFILE`). That single number is what bounds every "who is touched"
claim below, and it is why this release's blast radius is far narrower than its line count suggests.

- **OG-pf-1 -- WIDENS.** A restricted profile now confines ONLY
  the data-grant family (`DATA_GRANT_TOOLS`: the five `schwab_*` tools plus `blackdiamond_list_fees`),
  so a profiled principal regains reach to every non-data tool. **Touches: the 1 active profile
  (`2c61471b14`), and no one else** -- an unprofiled principal has no profile to confine, so nothing
  about its reach changes. Before this cell that principal was confined across the whole registry;
  after it, the 54 non-data tools fall back to each tool's own existing gate rather than the
  profile's blanket denial.
- **OG-bd-2 -- NARROWS.** `blackdiamond_list_fees` is denied to an **unprofiled** principal unless
  its tier is `master_admin`. **Touches: every caller that holds no profile and is not
  `master_admin`.** Against the store above, that is every principal except `2c61471b14`, whose
  reach to that tool is governed by its profile instead. Nobody gains.
- **OG-tg-1 -- NARROWS in one direction and WIDENS in another. CORRECTED on the COO half's
  condition C1 @`d8119a4d7a`; the first version of this ask called tg-1 narrowing-only and claimed
  pf-1 was the sole widening. That was wrong, and the widening is the half that matters more.**
  - **NARROWS:** Teams reads now carry the sender's identity (UPN, tenant) for every caller, and the
    Bloomberg concierge is gated to **Opal senders only** (`OPAL_USERS_ONLY`). Touches every
    Teams-read caller (identity now recorded) and every non-Opal sender to the concierge (refused).
    The identity fields are added to records the routes already fetch, so no new Graph scope and no
    new call.
  - **WIDENS -- `opalbloomberg`'s tool set becomes Andrew's** (PRD v2.3 item 2). Measured in the
    release diff, not taken from the summary: `app/identity_scope.py` DELETES that principal's
    `_SEED` frozenset entry, and `identity_tool_allowlist.txt` DELETES both of its overlay rows --
    the client-qualified `opal_data_refresh_upload client=...` row (OA-f-1) and the
    `opal_data_refresh_status` row (OG-al-2). Before r30 that identity was SCOPED to exactly those
    two tools; after it, it is UNSCOPED and inherits the general set, i.e. Andrew's. **Touches: the
    `opalbloomberg` principal, whose reach goes from 2 allowlisted tools to the full set.** This is
    the widening A2's `bbg_identity_admitted_8` grades, and it is the reason v2.3 item 4 couples
    item 2 to item 1: the Opal-users-only gate above is what bounds who can drive that now-unscoped
    identity. Sign the two together or neither.
- **OG-sh-1 -- ADDS one READ tool.** `list_shared_folder(url)` resolves a sharing URL via
  `/shares/{id}/driveItem` and lists `/children`, **under the signed-in user's own delegated token**,
  so it can reach only what is already shared to that user. **Touches: every principal that can call
  tools**, bounded by each caller's own token. `Files.ReadWrite.All` is already consented
  (`app/config.py:64`); no new scope, no role, policy or consent change.

## 3. Every other unreleased `app/` diff, listed as EXCLUDED

`app/` files differing live base -> `box/sitez` HEAD: **9**. Five are this release. **Four are
EXCLUDED and do not ride:**

| excluded file | whose |
|---|---|
| `app/harvest_read.py` | OG-hv-1 (its release is OG-hv-2, a separate order) |
| `app/admin_fabric_gitstate.py` | NFRA_MCPORTAL's later cells |
| `app/family_depth.py` | not in these four cells |
| `app/refs/silver_families.json` | not in these four cells |

AC1 independently confirms the same thing from the other direction: 0 files and 0 diff lines outside
the four cells' own hunks, so no line of any other unreleased cell is present.

## 4. The triggers, relative to the live base

- **Tools: +1 by name, `list_shared_folder`, and nothing else.** Measured by extracting every
  `@mcp.tool()`-decorated function name from every `app/*.py` in both trees: live base **39**,
  release **40**, added `['list_shared_folder']`, removed `[]`. (Grain: this is the `@mcp.tool()`
  decorated set. The suites' own census prints a larger total -- 58 at the live base -- because it
  also counts integration tools registered through a different mechanism. Both are true; the
  decorated set is the one that answers "+1 by name".)
- **`.env` names unchanged.** `.env.example`: 15 names live, 15 names release, 0 added, 0 removed.
  No `.env` value, name or email is printed in this ask.
- **md5 = release.** After B2, one SSM md5 read of the host over `app/`, `deploy/`, `dashboard/`
  must equal the release tree, the same instrument that established the precondition above (105 of
  105 at the base). The 10 built dashboard assets are expected to remain host-only.

## 5. Suites -- seven named, and the one failure is pre-existing

**Release tree: 46 passed, 1 failed.** The single failure is
`tests/test_data_entitlement_guard.py::test_ogz1_ac08`, and **it is PRE-EXISTING, not introduced**:
it fails at the live ref too, with the identical signature -- 57 routes and the same four extra
items (`/hx/teams/teams`, `/hx/teams/teams/{team_id}/channels`,
`/hx/teams/channels/{team_id}/{channel_id}/messages`, `/{path:path}`). Same test id, same assertion,
same object, present with and without this release. Those `/hx/teams/*` routes are OG-ap-7's, already
live since `28ba9532b6`; the test's pinned route set has not been moved to match.

**Only 3 of the 7 suites can be run at the live ref** -- `test_data_entitlement_family.py`,
`test_opal_users_gate.py`, `test_og_bd2.py` and `test_og_sh1.py` do not exist there, because these
cells add them. Those 3: **30 passed, 1 failed**, the same one. (An earlier combined run at the live
ref printed nothing at all; that was pytest erroring on the four missing paths, and it is recorded
with its cause rather than as a pass.)

## 6. The conflicts and how each was resolved

**Three paths outside the gateway were RESTORED, never taken.** The surprise-channel
`INVESTIGATION_v1.md` (from `5c5549b8bd` and again from `b47fc56a98`) and
`0.9.0_WK_NFRA_OPLGTW~60/NEVER_WIDEN_ASK_OG-bd-2.md` (from `c37fdf95a5`). The channel is append-only
and already further along here, so taking a stale copy would have destroyed peers' rows. Restored
with `git reset HEAD -- <path>` plus `git show HEAD:<path>` -- never `checkout --`, which BOUNDS bars.

**One real textual conflict, resolved to sh-1's side VERBATIM** (cmp-verified byte-equal to
`47cee985ee`'s version of the file): `tests/test_data_entitlement_family.py`'s non-data tool-count
assertion. pf-1's side asserts 52, sh-1's asserts 54. **I first resolved it to 53** -- reasoning 52
plus sh-1's one new tool -- **and the suite immediately read 54.** The error was inferring the count
from a sibling pick's BASE instead of measuring this tree: the re-cut sits on the live ref, which
already carries MX-r-11's catalog tools, so the live ref holds 53 non-data tools and sh-1's addition
makes 54. The live ref's own test prints "Schwab 5 allowed + 53 others", which confirms it on a
second instrument. Recording it because the wrong number would have passed a reviewer's eye.

**One WARN, left alone deliberately:** `commit-gate` reports 7 non-ASCII lines in `app/tools.py`.
They arrive with the cells' own commits and are not authored here. Fixing a pre-existing deviation
inside an unrelated signed release is the `terraform fmt` trap the cloud-ops rules name, so the WARN
is reported rather than silenced.

## 7. Rollback, and what is being asked

**Rollback: redeploy the live base `7eff14b2e620c8c1f688d41de6f37c09addde7b4`** -- the commit the
host is proven to be running right now (105 of 105 md5 parity), so the rollback target is measured
rather than assumed. No grant, profile, policy or Terraform state is touched by this release, so
there is nothing else to unwind.

**Sign or refuse the release at `release_sha` `db3d1972bc`.** B2 deploys only on the issuer's GO
naming both halves signed at that sha, inside the 11:00Z-23:00Z window, with the ledger
`nfra-oplgtw-gateway-release-r30` opened entry-and-sentinel-first.

The two r30 grant writes (Andrew's profile and the Bloomberg mirror) are **not** in this release:
they are OG-mg-1, a separate order, and its own Phase A is running read-only.
