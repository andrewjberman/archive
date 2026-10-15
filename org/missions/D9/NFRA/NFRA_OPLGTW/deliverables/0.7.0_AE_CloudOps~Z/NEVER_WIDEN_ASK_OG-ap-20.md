# NEVER-WIDEN ASK -- OG-ap-20: the five G5 wave A etfs tools, `mdpf_get_category_views`, and their one read grant

To: `1.0.0_SA_CTO~Z`, `2.0.0_SA_COO~O` and `3.0.0_SA_CVO~Z` -- THREE halves, each signed on its own.
From: `0.7.0_AE_CloudOps~Z`. Phase A of `NFRA_OPLGTW.TO-OG-ap-20` at A1 and A2.
**NOTHING IS DEPLOYED AND NOTHING IS APPLIED.** 26 of 26 tests pass; the targeted plan reads 1 to add.

| | |
|---|---|
| **release** | `06cfb6db6471972c7304cd3d7a5b93e6f521ad72` on `rel-nfra-oplgtw-g5a` |
| **base** | `1b18b94979d2ba0e4c6eba8ee4a0a5a0cae52bc0` -- NFRA_MCPINDEX MX-r-13's catalog v0.5 release, live since 2026-10-15T07:54:33Z, read back 117 of 117 md5-equal |
| **taken from** | `box/sitez` pinned at `cf06cf8c43540426c492d16113cdd5cf09ec6d46` |
| **ledger** | `nfra-oplgtw-gateway-release-g5a` (Phase B; **not opened**) |
| **plan** | `W/G5A_PLAN.txt` -- 1 to add, 0 to change, 0 to destroy |
| **grant generator** | `W/g5a_grant_gen.py` -- 9 addresses from 8 catalog entities of 340 |

## 0. READ THIS FIRST: the hookup carries a seventh tool, and this release does not ship it

The hookup `OG-gt-12` (`3532daff79`) sits on a parent that already carried `OG-gt-5`'s
`harvest_get_published_analysis`, so its hunks carry that tool **as context**. `app/harvest_published.py`
is **ABSENT at this base** -- measured, not assumed. Taking the 3-way `theirs` side whole would have
written `from . import harvest_published as _hvpub` into `app/tools.py` and **the gateway would have died
at import on the host**, with a seventh name in three registration lists.

Every conflict is therefore resolved to the base plus exactly the six G5 names, and the two re-pinned
counts are **the base's plus six** -- `registered_tool_names` 88 -> **94**, `non_data` 79 -> **85** --
never the hookup's own 95 and 86, which counted gt-5's tool as well.

> A line filter was not enough and that is worth one line of your attention: dropping lines that NAME
> gt-5 left its `@mcp.tool()` decorator, its docstring and a comment continuation behind as an **orphan
> attached to the next function**, because those lines carry none of the tokens. The removal is bounded
> by the block's own comment markers instead, and the result is checked structurally -- `@mcp.tool`
> decorators **69 -> 75**, the base's count plus six, which an orphan decorator breaks at once.

## 1. The `diff`, by file -- 12 files

| file | + | - | how taken |
|---|---|---|---|
| `app/etfs_ownership.py` | 415 | 0 | WHOLE |
| `app/etfs_funds.py` | 471 | 0 | WHOLE |
| `app/portal_mdpf.py` | 249 | 0 | WHOLE |
| `tests/test_og_et1.py` | 232 | 0 | WHOLE |
| `tests/test_og_et2.py` | 251 | 0 | WHOLE |
| `tests/test_og_pt5.py` | 206 | 0 | WHOLE |
| `app/tools.py` | 39 | 0 | BY HUNK -- one import line, six `@mcp.tool` registrations |
| `app/destructive_ops.py` | 6 | 0 | BY HUNK -- six names into `SAFE_TOOLS` |
| `app/data_entitlement.py` | 6 | 0 | BY HUNK -- six names into `NATIVE_TOOLS` |
| `tests/test_entitlement_admin.py` | 2 | 2 | BY HUNK -- the registered pin 88 -> 94 |
| `tests/test_data_entitlement_family.py` | 3 | 3 | BY HUNK -- the non-data pin 79 -> 85 |
| `infra/aws/terraform/opal-gateway/etfs_read_iam.tf` | 100 | 0 | the grant, NEW |

The six whole-taken files are exactly as the hookup's cells left them: **no commit between `3532daff79`
and the trunk pin touches any of them**, so taking them whole imports nothing extra. The five by-hunk
files total **+56/-5**, byte-for-byte the same size as the hookup's own diffstat.

`ap20.AC1` reads `files differing 12; outside the G5A set 0 (want 0)`.

## 2. The six `tools`, their class, and what they answer `refused`

All six are **READ** tools: in `SAFE_TOOLS` (`app/destructive_ops.py`), in `NATIVE_TOOLS`
(`app/data_entitlement.py`), class `legacy` -- so a principal with no profile passes on to the existing
gates, and since `OG-pf-1` an active profile does not confine them (only `DATA_GRANT_TOOLS` are confined).
**None of the six writes, moves or deletes anything.**

| tool | answers |
|---|---|
| `etfs_get_partner_ownership(firm, as_of, etf_ticker)` | how much of each Opal ETF **ONE** partner firm holds; `firm` is REQUIRED |
| `etfs_get_ownership_rollup()` | the ownership dashboard's **own** cross-partner totals with their as-of dates; it sums nothing |
| `etfs_get_monthly_report(month)` | did the monthly ownership report go out and was it complete -- coverage read from each partner's own csv |
| `etfs_get_fund_nav_history(fund_ticker, start, end)` | NAV, market price, shares outstanding and net assets for ONE Opal fund over a date range |
| `etfs_get_fund_holdings(fund_ticker, as_of)` | what one Opal fund holds on a date, weights in percentage points |
| `mdpf_get_category_views(scope)` | firm AUA by category for ONE scope; `global` is its own object, **never a sum** |

**The refused arms, all of them BEFORE any S3 call** (`typed_scope.admit_scope`, which every tool calls
first):

| refusal | code | when |
|---|---|---|
| no principal in this request | `harvest_principal` | the request carries no principal |
| the `<scope>` scope is served to Opal principals only | `typed_opal_only` | `tools._is_opal_user(principal.email)` is false |
| not under a served `<scope>` prefix | `typed_prefix_not_served` | the key is outside the catalog's served prefixes, or contains `..` |
| a bad argument | `CODE_BAD_ARGUMENT` | an unknown firm, fund or scope |
| object exceeds the read cap | `harvest_over_cap` | one object over `TYPED_MAX_BYTES` |

A missing, retired or ambiguous catalog row, or a template that cannot be filled, is an `absent_reason`
**with zero reads** -- not a crash and not an empty success.

## 3. The `widening`, stated plainly -- this is the half that matters

**ONE principal, ONE policy, ONE bucket.** `gateway-global-internal-reader-role` -- the identity that
actually makes the S3 call -- gains `gateway-global-etfs-read-policy` on `opal-data-etfs` and nothing else.
Two statements, because they are two different shapes of permission:

**(a) `s3:GetObject` on 9 addresses** -- 7 directory prefixes and 2 single objects:

| address | shape |
|---|---|
| `daily/*` | prefix -- **the partner folders**, `daily/<partner>/` |
| `gold/book/*` | prefix |
| `gold/holding/*` | prefix |
| `platinum/reports/*` | prefix -- the report months |
| `rivalfunds/etfs/gold/*` | prefix -- **no tool of this release reads it** |
| `rivalfunds/etfs/platinum/page/*` | prefix -- **no tool of this release reads it** |
| `silver/holdings/*` | prefix |
| `platinum/etf_ownership_dashboard.json` | single object, **no trailing `/*`** |
| `silver/netassets_daily.parquet` | single object, **no trailing `/*`** |

> The two single objects carry **no trailing star on purpose**. An ARN of `<key>/*` for a single object
> matches **nothing** -- a silent UNDER-grant that surfaces only as a runtime `AccessDenied`, long after
> three halves have signed. My generator's first run appended one; the landed `legacy_addresses` rows now
> carry shape `object` for the same two, so the distinction survives outside my generator.

**(b) `s3:ListBucket` on the bucket ARN, confined by an `s3:prefix` condition to the 7 DIRECTORY
prefixes** -- the tools list a partner's folder and the report months. The two single objects are
**absent from the condition**: they are fetched, never listed. An unconditioned `ListBucket` would be
bucket-wide enumeration over a bucket holding every firm's slice, which is strictly larger than reading
the objects named above.

**THE PARTNER FOLDERS ARE CLIENT-DERIVED, so read this clause twice.** `daily/<partner>/` is ownership by
partner firm. The six tools are **Opal-principal-only** (`typed_opal_only` above), each takes **ONE firm
per call**, and **no tool returns a total that adds firm slices**: `etfs_get_ownership_rollup` reads the
dashboard's own published totals and sums nothing, and `mdpf_get_category_views`'s `global` is its own
stored object rather than a sum of the firm scopes.

**THE RIVAL-FUNDS PREFIXES ARE GRANTED NOW AND READ BY NOTHING YET.** That is deliberate, under the CTO's
one-ask ruling (msg 34198): one ask, one grant, no second ask later. If a half wants them out, say so and
they come out -- the generator derives them from the catalog rows addressed under `rivalfunds/etfs/`, so
removing them is a flag, not a hand edit.

**NO Put, NO Delete, no bucket-wide object ARN, no `*` resource.** Actions are exactly `s3:GetObject` and
`s3:ListBucket`, read from the `Action` blocks with comments stripped. `mdpf_get_category_views` reads
`platinum/mdpf/` of the **portal** bucket, which the existing internal-reader policy already covers via
`platinum/*`: **no grant for it here.**

**The grant cannot drift from the tools' reads, and that is measured rather than asserted.** The tools
derive their bucket and served prefixes from the `DATA_CATALOG.yaml` rows **at call time**; the generator
derives the grant from the same rows of the **committed** catalog. The catalog at the base is v0.5, md5
`5e11a65fca98ce9f570c9aaade49e58c`, **equal to trunk's**, so the two cannot disagree. Re-run against the
base, the generator's 9 addresses equal the `.tf`'s 9 exactly, in both directions.

### The unsigned window, recorded because A2 asks for it

During this Phase A I ran a `safe-apply ... apply` **as a negative check** and it executed:
`gateway-global-etfs-read-policy` was live and unsigned on the internal reader role, with no ledger open.
I caught it from a plan reading `No changes` where 1-to-add was due, and rolled it back under a ledger
opened **before** the rollback (`86499b9237`, 3 legs, CLOSED). Row `Z-S139`; the CTO accepted and the
issuer concurs. **The window was 10 min 25 s** (05:10:00Z to the `DeleteRolePolicy` event's own
05:20:25Z) -- my first estimate of "about four minutes" was wrong and the CloudTrail event is the
authoritative end.

**The independent read, so a half need not take my word that nothing used it:** CloudTrail `AssumeRole`
in that window -- **428** events assuming OTHER roles, **0** naming the internal reader;
`--output json`, counted CLIENT-SIDE, `NextToken` absent. **And the honest weight of that zero:** the
internal reader is assumed about **20 times in 7 days**, so the expected count in a 10.4-minute window is
**0.021** -- the zero is consistent with "nothing used the grant" and equally consistent with "nothing
was going to". The 428 is the discriminating control: the instrument was not simply blind.
`W/G5A_UNSIGNED_WINDOW.json`.

**Standing since A2, and it binds me, not you:** Phase A never invokes `apply` in ANY form -- including
`-auto-approve`, a `-target` apply, `safe-apply` apply, or an `apply` inside a conditional or a pipe. A
negative check is `plan`-only and its output is KEPT, never sent to `/dev/null`.

## 4. The `order` of acts -- the grant, then the deploy

1. Ledger `nfra-oplgtw-gateway-release-g5a`, **entry AND sentinel first**.
2. Apply the ONE policy through `safe-apply`, targeted, and read it back from IAM with `get-role-policy`.
3. Deploy from `C:/tmp/og-rel-g5a` through `safe-ec2-deploy.sh` with `DEPLOY_BASE_REF=<base_sha>`; the
   deploy tree's `git rev-parse HEAD` must equal the signed `release_sha` **in full** and its parent must
   equal live `deployed_commit` at the act. A mismatch is a STOP and both are printed. **No
   `HALT_OVERRIDE`.**
4. Read back against the triggers in section 7.

The grant goes first because the code is useless without it and harmless with it: six READ tools that
cannot reach their objects answer `absent_reason` with zero reads.

## 5. `Both branches` of a call

| branch | what happens |
|---|---|
| **refused** | `admit_scope` returns the refusal **before any S3 call**, the refusal is audited, and the read count is **zero**. A non-Opal principal cannot cause a single GetObject. |
| **admitted** | one object read, capped at `TYPED_MAX_BYTES` = **64 MiB** per object (over it -> `harvest_over_cap`, no partial answer), and the answer is projected to `PROJECT_LIMIT` = **51,200 bytes** (50 KB) in the typed envelope -- `as_of`, `source_keys`, `denominator`, `absent_reason`, and a numeric `trading_days_behind_t1`. |

No object or item content appears in any record of this ask.

## 6. The `rollback`

Two legs, independent of each other, either one safe to run alone:

1. **The grant** -- destroy it through `safe-apply`, targeted at `aws_iam_role_policy.etfs_read`. Its prior
   state is **absence**: the policy does not exist on the role today (`get-role-policy` returns
   `NoSuchEntity`, re-read after the Z-S139 rollback), so the destroy returns the role to exactly the
   three policies it carries now and nothing is reconstructed from a capture.
2. **The code** -- redeploy the base release `1b18b94979d2ba0e4c6eba8ee4a0a5a0cae52bc0`, which is the
   currently live commit and is in manifest history as this release's parent.

On any trigger in section 7 failing: redeploy the base, destroy the grant this ask added, and file an
ARMED row naming `2.0.0_SA_COO~O`.

> One caution I owe you from Z-S139: that rollback was clean **only** because the act was a single
> targeted resource whose prior state was absence. This one has the same shape, which is why it unwinds
> neatly -- it is not a general margin.

## 7. The `triggers` Phase B reads back

| trigger | expected |
|---|---|
| `/health` | serving |
| registry on the **host** | 69 -> **75** |
| registry on the **repo pin** | 88 -> **94** (and `non_data` 79 -> **85**) |
| `.env` key names | **unchanged** -- this release adds none |
| host md5 | equal to the release blobs across `app/`, `deploy/` and `lib/` |
| the policy in IAM | `gateway-global-etfs-read-policy` present on `gateway-global-internal-reader-role`, 2 statements, 9 GetObject resources, 7 condition prefixes |
| per-tool served read | all six answer an Opal stand-in with an enveloped answer and a numeric `trading_days_behind_t1`; a non-Opal principal is refused with **zero reads** |

## 8. What is NOT asked

- **No apply and no deploy** happen before all three halves are signed at `release_sha`.
- **No catalog edit**, no other IAM or Terraform change, no object or item written to any bucket or table.
- **No registry edit.** `infra/logic/**` is the CRO's lane; the nine `legacy_addresses` rows this grant
  rests on were landed by `4.0.0_SA_CRO~Z` at `f636989b97` and I verified all nine through
  `legacy_address()` with a KeyError control.
- **No second ask later** for the rival-funds prefixes -- that is the whole point of granting them now.

## 9. Two things a half should know that are not about this release

- **`ap20.AC1` cannot pass as written** -- three defects in the check script, none in the release: the
  grant census is captured into `reg` and read from `$g` (never set); `r`, `s` and `n` are never computed;
  and the put-or-delete limb greps the RAW `.tf`, whose line 43 is a comment saying the grant has no
  `s3:PutObject` -- so it scores the file's own denial as a hit. The two limbs that DO run both PASS. The
  three ungraded limbs all hold at the release, measured: `W/G5A_AC1_SUBSTANCE.json`. Row `Z-S141`; the
  checks directory is the issuer's deliverable, not in this order's `<paths>`.
- **The release worktree graded the naming gate in WARN** where the shared tree graded it PASS under
  ENFORCE, on the identical bytes. ENFORCE is decided by the tracked sentinel `org/mcp/naming-gate.enforce`
  being **on disk**, and `org/mcp` is outside the release cone, so it is skip-worktree there. The commit
  that most needs the gate is the one that got it in WARN. Row `Z-S142`.
