# NEVER-WIDEN ASK -- OG-ap-21: the person reader, two role moves, and `harvest_get_published_analysis`

To: `1.0.0_SA_CTO~Z`, `2.0.0_SA_COO~O` and `3.0.0_SA_CVO~Z` -- THREE halves, each signed on its own.
From: `0.7.0_AE_CloudOps~Z`. Phase A of `NFRA_OPLGTW.TO-OG-ap-21` as amended through A3.
**NOTHING IS DEPLOYED AND NOTHING IS APPLIED.** 44 of 44 tests pass; the targeted plan reads 2 to add.

| | |
|---|---|
| **release** | `d577e0e7297b3ecba183023d8374855a93f148a7` on `rel-nfra-oplgtw-p21` |
| **base** | `c4c106aea1cc47d15f81397208226bd9b292c9dc` -- MX-r-14's catalog release, live since 2026-10-15T19:50:39Z, read back **120 of 120** md5-equal |
| **taken from** | `box/sitez` pinned at `5858411c5ca7433ac06459ce402827728fa7bd38` |
| **ledger** | `nfra-oplgtw-gateway-release-p21` (Phase B; **not opened**) |
| **plan** | `W/P21_PLAN.txt` -- **2 to add**, 0 to change, 0 to destroy (A2) |

## 0. READ THIS FIRST: one guard this cut had to actively preserve, and A3 ruled it

`OG-cp-1`'s patch drops the base's guard on the tier line -- `not access.restricted and ...`. It did not
remove it deliberately: **at cp-1's own parent the line already lacked it**, so its branch predates
`OG-bd-2` and `OG-bd-3`. Taking `theirs` wholesale would have silently reverted a live guard while
appearing to add only a feature.

**A3 ruled: keep the BASE guard**, because allowing a profiled master_admin is a widening this ask does
not cover and ships under its own halves (row `Z-W67-S1`, still open and BLOCKING). So the resolution is
cp-1's body with the base's guard restored into its tier line, in **both** the dispatch and the list
path. **Live behaviour at the entitlement chokepoint is unchanged by this release.**

Row `Z-W67-S1` is the same question one layer down: the CTO ruled (msg 33941 route (a)) that a profiled
master_admin be ALLOWED, `OG-bd-2`'s `test_ogbd2_ac03` asserts it be DENIED, and `OG-bd-3`'s order forbade
editing that test. **Both readings deny the tool** -- with the guard the refusal is `entitlement_denied`
from the data-grant gate, without it `person_record_denied` from the person record. Only the gate order
changes. Nothing is widened either way.

## 1. The `diff`, by file -- 20 files

| file | how taken |
|---|---|
| `app/harvest_published.py` | WHOLE (new at this base) |
| `app/internal_role.py`, `app/news_typed.py`, `app/access_state.py` | WHOLE |
| `tests/test_og_cp1.py`, `test_og_nw2.py`, `test_og_gt5.py`, `test_og_gt13.py`, `test_access_state.py` | WHOLE |
| `deploy/NFRA_OPLGTW_CONTRACT.json` + `org/standards/NFRA_OPLGTW_CONTRACT.json` | WHOLE, **one git object** (`1d83cd7aa6`) staged twice -- byte-equal by identity, not by compare |
| `app/data_entitlement.py`, `app/tools.py`, `app/integrations/base.py`, `app/destructive_ops.py` | BY HUNK |
| `tests/test_entitlement_admin.py`, `tests/test_data_entitlement_family.py` | BY HUNK -- pins **94 -> 95** and **85 -> 86** |
| `deploy-to-ec2.sh` | BY HUNK -- the ONE `AMGT_SCOPED_API_FUNCTION` key |
| `infra/aws/terraform/opal-gateway/news_read_internal_iam.tf` | NEW |
| `infra/aws/terraform/opal-gateway/harvest_published_invoke_iam.tf` | retargeted to the internal reader |

The by-hunk take is from **four person-roles commits only**, chronologically with 3-way: `c10c91b797`
(gt-5's env key), `1b89afbb62` (gt-11's registration and lists), `d5d2fb29bd` (cp-1's person reader),
`a445101400` (cp-1 A2's integration floor). **The two `OG-rv-3` commits are deliberately not taken** --
`6202abcec8` hooks up ten rival tools and `1b22c0add7` renames one, both touching the same three files.
The structural oracle says they did not ride: **`@mcp.tool` decorators 75 -> 76**, pins 95 and 86, and
**no rival token anywhere in the cut**.

### Two divergences named here rather than left for a half to find

1. **`test_ogcp1_ac02` carries two changed assertions.** A3 authorised "its one assertion"; the test
   needed **two**, and the second **proved itself in the run** rather than being predicted: with the
   guard kept, a restricted profile refuses `blackdiamond_list_fees` at the data-grant gate whatever the
   person record says, so both the loop assertion and the later `stopped: false` assertion diverge. Both
   now expect `entitlement_denied`, each with a comment citing `Z-W67-S1`. **No other test was touched
   and `tests/test_og_bd2.py` was not opened.**
2. **`tests/test_admin_people_access.py` is NOT taken** (A3). It is in the order's take-list, but
   `app/admin_people_access.py` -- MP-pd-3's handler, an NFRA_MCPORTAL cell -- is absent at this base,
   and all 7 of its tests errored `ModuleNotFoundError`. A3: drop the test, do not add the module;
   MP-pd-3 rides its own release. Row `Z-S154`.

## 2. The `tools`, and the reader's rules

**ONE new tool**: `harvest_get_published_analysis(security_key, sections)` -- a READ tool returning the
published body of one security section, projected to 50 KB with `as_of`, `source_keys`, a `denominator`
and `absent_reason`. In `SAFE_TOOLS` and `NATIVE_TOOLS`, class `legacy`. Registry **75 -> 76** on the
host's own instrument.

**Its refused arms, read from the module and not from the order's prose** -- every one of them BEFORE any
invoke:

| refusal | when |
|---|---|
| `principal_required` | no principal in the request |
| `harvest_opal_only` | `tools._is_opal_user` is false |
| `harvest_prefix_not_served` | the ref is outside the served prefixes |
| `harvest_bad_argument` | a bad `security_key` or `sections` |
| `harvest_published_unavailable` | the Lambda reported a function error **-- and also when the internal reader role cannot be assumed: ZERO invokes, no fallback** |
| `404` | the security is absent |

**THE PERSON READER's rules** (`app/data_entitlement.py`, cp-1):

- **STOP**: an active record with `stopped: true` denies **every** tool, the master_admin included.
- **NARROW**: `tools_deny` denies a tool, `channels_deny` denies its channel, for any principal.
- **WIDEN -- at the identity-scope floor ONLY**: for an **Opal** principal, an active record admits a
  **SERVED** tool past `identity_scope` when the tool is in `tools_allow` or its channel is in
  `channels_allow`. **Deny beats allow.** It widens nothing else: the Opal-only gate, C2, the tier gate
  and the data grants are never overridden -- which is exactly why the base's guard had to survive.
- **FAIL CLOSED**: a dependency failure or a malformed record denies rather than admits
  (`_person_unavailable`), and `visible_tools` returns `[]` rather than the unfiltered list.
- **WHO WRITES IT**: `NFRA_MCPORTAL`'s one grant writer, C18, **Andrew-only writes** (C2). This release
  only READS the record.

## 3. The `widening`, stated plainly -- in two parts, per A2

**(a) The news statement MOVES.** `gateway-global-news-read-policy` lives today on the gateway INSTANCE
role `opal-gateway-role`. This release adds `gateway-global-news-read-internal-policy` on the ASSUMED
internal reader role `gateway-global-internal-reader-role`, with **width identical to the policy it
mirrors**: `dynamodb:Query` and `dynamodb:GetItem` only, on the three news tables and the one
`date-index`. No Scan, no write, no wildcard, no second ARN. **Both stand through this release by
design** -- the old statement is destroyed in Phase B **after** the served read, never before -- so the
instance role narrows at the END of the sequence, not the start.

**(b) The invoke statement is a NEW GRANT, not a move.** `aws_iam_role_policy.gw_harvest_published_invoke`
**was never applied**: it is absent from terraform state and `opal-gateway-role` carries no such policy
live. OG-gt-5 wrote it as Phase A code and the order that would have applied it never came. So the
internal reader **gains** `lambda:InvokeFunction` on the one function `opal-amgt-scoped-api` that **no
role holds today**. That is a real widening and it is stated as one. Row `Z-S149`.

> **And the retarget is not a policy-side choice.** `app/harvest_published.py` already reads its Lambda
> client from `internal_role.lambda_client` (OG-gt-13), and that helper **does not exist at the base** --
> it arrives with this take. So the terraform is the grant catching up with code that already assumes
> that identity, and without it the tool cannot work at all: it answers
> `harvest_published_unavailable` with zero invokes.

**(c) What ELSE this release puts on 17 live modules, which the take-list does not show.**
`app/internal_role.py` is imported by **8** modules at the base -- including the three OG-ap-20 put live
hours ago -- and `app/access_state.py` by **9**. Taking them WHOLE replaces shared dependencies, so their
diffs are this release's real blast radius. Measured, so the statement stays narrow:

- `internal_role.py` **+78/-1, no existing `def` or class changed or removed**: six new names
  (`dynamodb_client`, `lambda_client`, their defaults and two service constants). The one removed line is
  the module-level cache declaration the additions replace with one that also holds DynamoDB and Lambda
  clients. The eight importers keep the behaviour they have.
- `access_state.py` **+2/-1, one constant extended**: `POLICY_RECORD_TYPES` gains `person_access`. That
  constant is read in exactly **three places, all inside `access_state.py` itself**. **No other module
  reads it.** It widens what a record may be CALLED, not what any tool may reach.

**No grant widens for the person reader itself.** It reads one DynamoDB record through the existing
access-state path; it mints no address and no permission.

## 4. The `order` of acts

1. Ledger `nfra-oplgtw-gateway-release-p21`, **entry AND sentinel first**.
2. Apply the TWO new policies through `safe-apply`, targeted, and read each back from IAM.
3. Deploy from `C:/tmp/og-rel-p21` with `DEPLOY_BASE_REF=<base_sha>`; the deploy tree's HEAD must equal
   the signed `release_sha` in full and its parent must equal the live `deployed_commit`. No
   `HALT_OVERRIDE`.
4. The served read.
5. **ONLY THEN** destroy `aws_iam_role_policy.gw_news_read` **by name**, so the news reads never have a
   window with no grant on either role.

## 5. `Both branches` of a call

| branch | what happens |
|---|---|
| **refused** | every arm in section 2 fires BEFORE any invoke or any DynamoDB call; the refusal is audited; the read and invoke counts are **zero**. A non-Opal principal cannot cause one. |
| **admitted** | one Lambda invoke of `opal-amgt-scoped-api`, or one DynamoDB `Query`/`GetItem`, through the internal reader role; the answer is projected to 50 KB in the typed envelope. |

## 6. The `rollback`

1. **The code** -- redeploy the base `c4c106aea1cc47d15f81397208226bd9b292c9dc`, the currently live commit
   and this release's parent.
2. **The two new policies** -- destroy through `safe-apply` targeted at
   `aws_iam_role_policy.int_reader_news_read` and `aws_iam_role_policy.gw_harvest_published_invoke`.
   Both have prior state **absence**, so the destroy reconstructs nothing.
3. **If `gw_news_read` was already destroyed** -- re-create it: it is still in `news_read_iam.tf`, which
   this release does NOT delete, so a targeted apply restores it from code rather than from a capture.

## 7. The `triggers` Phase B reads back

| trigger | expected |
|---|---|
| `/health` | serving |
| registry on the **host** | 75 -> **76** |
| repo pin | 94 -> **95** (and `non_data` 85 -> **86**) |
| `.env` key names | the three `NEWS_*` keys unchanged, **plus** `AMGT_SCOPED_API_FUNCTION` |
| host md5 | equal to the release blobs across `app/`, `deploy/` and `lib/` |
| IAM | both new policies present on the internal reader role; `gw_news_read` present until step 5, absent after |
| the new tool | serves an Opal principal an enveloped answer and refuses a non-Opal one with zero invokes |
| the contract | `test_grant_writer_stages_the_contract_only_from_the_standard` goes **GREEN** once this release IS the deployed commit |

## 8. What is NOT asked

- **No apply and no deploy** before all three halves are signed at `release_sha`.
- **No ruling on `Z-W67-S1`.** The guard is kept; the ruled behaviour ships under its own halves.
- **No MP-pd-3 content.** `app/admin_people_access.py` is not taken and its test is dropped (A3).
- **No deletion of `news_read_iam.tf`.** It stays, so Phase B's destroy is targeted at a resource whose
  code still exists and the rollback can re-create it.

## 9. Two readings a half should have, that are not about this release

- **The naming gate on the release branch cannot exercise the `OG-ng-1` clause**: the clause merge
  `c8ca06fda0` is not an ancestor of this base, so the release tree runs the pre-clause gate (md5
  `7be9e4ed` against trunk's `8798c2dc`). The sentinel IS in this cone, so the MODE is fixed -- the
  remaining gap is the code version, exactly as `W/RELEASE_WORKTREE_CONE.md` predicted. **Graded on trunk
  in ENFORCE, this release's diff exits 0**: `gateway-global-harvest-published-invoke-policy` CONFORMANT,
  `gateway-global-news-read-internal-policy` CONFORMANT, and one `RAISE-EXISTING` on `amgt/security/` in
  `app/harvest_published.py` which the gate itself calls "not a refusal" and notes "the same literal is
  already carried at HEAD ... so this copy mints nothing".
- **The pre-declared RED gave three different failures**, and only the third is the one the order
  describes. In the release tree without the grant-writer in the cone: `build_package.py is not in this
  tree`. With it: `AttributeError: no attribute '_Source'` -- the base's builder predates the API the
  test calls. In the shared tree, where builder and test are both at trunk: the contract byte mismatch at
  index 7913, which is the closure this release closes. **A "pre-declared RED" is not a check unless its
  signature is pinned**, which is why `W/P21_RED_TEST_SIGNATURE.txt` exists.
