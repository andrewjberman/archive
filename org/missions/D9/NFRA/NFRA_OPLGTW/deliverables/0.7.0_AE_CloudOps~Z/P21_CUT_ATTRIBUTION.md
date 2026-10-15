# OG-ap-21's cut, pinned before the window: whose hunks ride, whose must not, and the three numbers that prove it

Written by `0.7.0_AE_CloudOps~Z` during Phase A, while step 3 waits on `NFRA_MCPINDEX` MX-r-14. The
issuer's standing item 1 for this cut is the reason: *"Pins are the base's plus this release's own only.
Trunk will soon carry ten rival tools and the person-roles hunks. Take hunks, never whole files, so none
of the rival registrations ride this release."* OG-ap-20 nearly shipped a tool whose module was absent at
its base because a hookup commit carried a NEIGHBOUR cell's tool as diff context; this file is that
lesson paid forward, settled while there is time to read rather than during a ledger window.

**The base is `06cfb6db6471972c7304cd3d7a5b93e6f521ad72`** at this writing (OG-ap-20's release, live since
2026-10-15T10:49:37Z). MX-r-14 deploys next on that ref, so **re-read `deployed_commit` and re-run this
attribution before the cut**; the commit list below is stable, the base may not be.

## The three numbers, and what each one catches

| instrument | at the base | ap-21 target | at trunk `a2af250d12` |
|---|---|---|---|
| `assert len(registered_tool_names) ==` | **94** | **95** | 105 |
| `assert len(non_data) ==` | **85** | **86** | 96 |
| `^@mcp.tool` decorators in `app/tools.py` | **75** | **76** | 86 |

ap-21 ships **ONE** new tool, `harvest_get_published_analysis`, so every number is the base's **plus one**,
which is what the order's "pins +1 on the base's" means arithmetically. **A cut reading 86 decorators has
the ten rival tools in it.** A cut reading 76 with pins 95/86 does not. The decorator count is the limb
that catches what a pin cannot: on OG-ap-20 a token filter left an orphan `@mcp.tool()` behind and only
the count saw it.

## Whose hunks RIDE

| commit | what it carries into ap-21 |
|---|---|
| `1b89afbb62` OG-gt-11 | the `harvest_get_published_analysis` registration, its `SAFE_TOOLS` and `NATIVE_TOOLS` entries, and the pin arithmetic in its own frame (88 -> 89 / 79 -> 80 there; **re-derive against THIS base, never copy**) |
| `d5d2fb29bd` OG-cp-1 | the per-person `person_access` reader in `app/data_entitlement.py` and the person hook at `_run` in `app/tools.py` |
| `a445101400` OG-cp-1 A2 | the integration floor admitting a per-person widening, in `app/integrations/base.py` (row NFRA_OPLGTW-Z-W94-S1) |
| `c10c91b797` OG-gt-5 | the one `AMGT_SCOPED_API_FUNCTION` key in `deploy-to-ec2.sh`, named by the order itself |

**A convenient fact, measured rather than assumed:** both cp-1 commits already read **95 / 86 / 76** --
cp-1 was cut on a base carrying gt-11's +1 and nothing of the rivals, so its side of a 3-way already holds
exactly ap-21's target numbers. That makes the pins a confirmation rather than an arithmetic exercise, but
they are still re-derived against the base actually cut.

## Whose hunks MUST NOT ride

| commit | what it would smuggle in |
|---|---|
| `6202abcec8` OG-rv-3 | the hookup of **ten** rival-funds tools, pins 95 -> 105 and 86 -> 96 |
| `1b22c0add7` OG-rv-3 A2 | the rename `etfs_get_peer_group` -> `etfs_get_peer_group_members` across `app/tools.py`, `app/data_entitlement.py` and `app/destructive_ops.py` (12 whole-word occurrences) |

The rename sits in the same three files as the person-roles hunks, so **expect 3-way conflicts whose
`theirs` side carries rival names**. Resolve every one to the base plus the person-roles content only; no
`etfs_get_peer_group_members`, and no rival registration, belongs in this release. `3532daff79` (OG-gt-12)
also appears in a `base..trunk` listing, and that is topology rather than work to take: its content is
already AT the base, carried by OG-ap-20's own by-hunk take, and the commit shows as unreachable only
because the base sits on a release branch.

## The contract closure, read and settled

The order asks for the closure of the contract at the cut. `infra/aws/lambda/mcportal/mcportal-grant-writer-lambda/build_package.py`
reads `services.opal-gateway.deployed_commit` from `EC2_MANIFEST.json` and builds from **that commit's
bytes** via `git show <commit>:<path>`, never from the working checkout (`:7-8`, `:76`, `:94-112`, `:297`),
and `BuildRefused` fires on a missing or unresolvable value. So both contract copies --
`infra/aws/ec2/opal-gateway/deploy/NFRA_OPLGTW_CONTRACT.json` and `org/standards/NFRA_OPLGTW_CONTRACT.json`
-- reach the package **only once this release IS the deployed commit**. That is exactly why
`tests/test_schwab_host_inputs.py::test_grant_writer_stages_the_contract_only_from_the_standard` is
pre-declared RED in Phase A and expected GREEN in Phase B: the test is reading a closure that the deploy
itself closes.

### Taking both contract copies WHOLE is safe, and that is measured

The order says take both copies whole and calls them byte-equal. Both halves checked by git OBJECT ID
rather than by content compare, so this is identity and not coincidence:

- at trunk, `deploy/NFRA_OPLGTW_CONTRACT.json` and `org/standards/NFRA_OPLGTW_CONTRACT.json` are the SAME
  object `1d83cd7aa6a865e5d88cc318e457943d1d2b8c33` -- byte-equal holds;
- at the base they are also one object, `42bba721f1e56ed77e110bc95eaba064203c17d8`, and a DIFFERENT one,
  so the contract moved between base and trunk and this release carries the new bytes.

**And the move is entirely ap-21's own work**, which is the part worth checking before taking a whole file
from trunk: the cumulative diff adds exactly `person_access` -- the member in the key list, the
`person_access` block with its writer, fields, channel and rule, and a comma -- from `d5d2fb29bd` OG-cp-1.
No rival content, no third cell's content. The other commits a `base..trunk` listing shows against these
paths are the same release-branch topology artifact noted above.

## The REVERSE seam, which the forward check cannot ask about

The seam enumeration asks what the taken files IMPORT. It cannot ask what imports THEM, and for this
take-list that is the bigger number. Measured at the base:

| whole-taken module | modules at the base that import it |
|---|---|
| `app/internal_role.py` | **8** -- `etfs_funds`, `etfs_ownership`, `portal_mdpf` (the three OG-ap-20 just put live), `harvest_read`, `portal_macro`, `portal_models`, `query_v0`, `news_typed` |
| `app/access_state.py` | **9** -- `data_entitlement`, `download_routes`, `oauth_as`, `tenant_registry`, `asker_scope`, `account_ref`, `admin_grants`, `admin_refusals`, `admin_gateway_breakdown` |
| `app/news_typed.py` | 1 -- `app/tools.py` |
| `app/harvest_published.py` | 0 -- it is new |

**Taking those first two WHOLE replaces modules that seventeen already-live modules depend on**, so their
base-to-trunk diff is this release's real blast radius and belongs in the ask's `diff` section as such.
Measured, so the statement is narrow rather than alarming:

- **`internal_role.py`, +78/-1: no existing `def` or class changed or removed.** Six new names
  (`_DDB_SERVICE`, `_LAMBDA_SERVICE`, `_default_dynamodb`, `_default_lambda`, `dynamodb_client`,
  `lambda_client`). The single removed line is the module-level cache declaration
  `_CACHE: dict = {}  # arn -> (s3 client, expiry epoch seconds)`, which the additions replace with a
  cache that also holds dynamodb and lambda clients. So the eight base importers keep the behaviour they
  have; what they gain is two client factories they do not call.
- **`access_state.py`, +2/-1: one module-level constant extended**, `POLICY_RECORD_TYPES` gaining
  `person_access`. That constant is read in exactly **three places, all inside `access_state.py` itself**
  -- `RECORD_TYPES = POLICY_RECORD_TYPES + tuple(RUNTIME_KINDS)` (`:79`), a validation refusal
  (`:129`), and a key check (`:186`). **No other module reads it.** So the extension's whole effect is
  that `person_access` becomes an accepted record type inside access_state's own validation, which is
  the person-access feature working as designed. It widens what a record may be CALLED, not what any tool
  may reach.

**And the invoke retarget is not a policy-side choice at all.** `app/harvest_published.py` already reads
its Lambda client from the internal reader (`internal_role.lambda_client`, OG-gt-13), and
`internal_role.lambda_client` **does not exist at the base** -- it arrives with this take. When the role
cannot be assumed the tool answers `harvest_published_unavailable` with **zero invokes and no fallback**.
So the terraform retarget is the grant catching up with code that already assumes that identity, and the
NEW grant A2 names is the permission without which the tool cannot work at all. Refusal arms for the ask's
section 2, read from the module: `harvest_bad_argument`, `harvest_published_unavailable` (also the
role-unavailable arm), `404` for an absent security, and `admit_typed`'s own three
(`principal_required`, `harvest_opal_only`, `harvest_prefix_not_served`), every one of them before any
invoke.

## What step 3 is actually waiting for, traced once so nobody traces it twice

The GO says the cut waits on MX-r-14. Measured 2026-10-15 ~16:4xZ-17:5xZ, so a later reader does not
re-derive it:

- `NFRA_MCPINDEX.TO-MX-r-14.round17-catalog-release.md` -- `issued_to 0.7.0_AE_CloudOps~MI`,
  `<status>issued</status>`, ONE commit (`2d9d5c4503`, 09:30Z, its issuance). Its start condition:
  MX-c-18 and MX-c-19 complete and drained, the regenerated catalog landed, **every NFRA_OPLGTW gateway
  ledger ahead in the queue CLOSED**, and then *"the issuer continues you with an AMENDMENT (A1)... until
  it arrives, do nothing."*
- MX-c-18 `complete`, MX-c-19 `complete`. **OG-ap-20's ledger CLOSED** -- that is the NFRA_OPLGTW ledger
  ahead in its queue, so this project satisfies that clause rather than blocking it.
- **A1 has never been written**: 0 matches for the amendment pattern against a positive control of 1 in
  this very order (OG-ap-21's own A2). The order carries one commit and no amendment.
- `0.7.0_AE_CloudOps~MI` is **LIVE** and reads `IDLE: ... no open task order` -- holding exactly as
  instructed, not stalled.
- `2.0.0_SA_COO~O` is **LIVE** and its own working line reads `waiting CTO ruling, MI r-14, Z ap-21 ask`:
  it holds this seat's ask and sits in the same wait.

**So the single gate is `2.0.0_SA_COO~MI`'s A1 amendment on MX-r-14**, and three live seats queue behind
it. **It is not a deadlock**, which is the thing worth checking and easy to assume: MX-r-14's clause names
ledgers AHEAD of it in the gateway queue, and OG-ap-21 is BEHIND it. A cross-fabric nudge is not this
seat's to send (it routes MSTR to MSTR); the ask that could move it went to this project's own issuer,
offering either a nudge or a release to cut on `06cfb6db64` and accept a re-cut.

## The suites, run at trunk BEFORE the window, so no red gets diagnosed inside it

| suite | at trunk | transferable to the cut? |
|---|---|---|
| `test_og_cp1` | 7 passed | **yes** -- behaviour, not counts |
| `test_og_nw2` | 4 passed | yes |
| `test_og_gt5` | 4 passed | yes |
| `test_og_gt13` | 4 passed | yes |
| `test_access_state` | 7 passed | yes |
| `test_admin_people_access` | 7 passed | yes |
| `test_og_hv1` | 5 passed | yes |
| `test_entitlement_admin` | 9 passed | **NO** -- it asserts the registered pin, and trunk's 105 agrees with trunk's registry. In the cut it must be 95 against 76 decorators |
| `test_data_entitlement_family` | 4 passed | **NO** -- same, the non-data pin, 96 at trunk against 86 in the cut |

51 tests pass at trunk, 0 fail. For the seven behavioural suites that means **there is no pre-existing red
to diagnose inside the ledger window**, which is the whole point of running them now. For the two pin
suites a trunk green proves only internal consistency AT TRUNK and says nothing about the cut; they are
the ones the three numbers above govern.

### The pre-declared RED, with the signature that tells it apart from a real one

`tests/test_schwab_host_inputs.py::test_grant_writer_stages_the_contract_only_from_the_standard` fails at
trunk, as the order says it will. Its exact signature, captured so a DIFFERENT red cannot be mistaken for
the expected one in Phase B:

```
assert zf.read(members[0]) == _STANDARD.read_bytes()
E  assert b'{\n  "contr...on"\n  ]\n}\n' == b'{\n  "contr...on"\n  ]\n}\n'
E    At index 7913 diff: b'\n' != b','
tests\test_schwab_host_inputs.py:168: AssertionError
```

That is the `person_access` addition and nothing else: the package stages the contract from
`deployed_commit`, where index 7913 still ends the `tenant_firm` entry with a newline, while the standard
on disk has a comma there because `person_access` follows. **The staged bytes are the deployed commit's;
the compared bytes are the working tree's.** It turns GREEN in Phase B when the release IS the deployed
commit, because the two then resolve to the same bytes. A red at any other offset, or with any other
assertion, is NOT this one and must be read on its own.

## Seams

Enumerated against the current base with `W/p21_seams.py`: **CLEAR**. Four modules opened, 3 distinct
intra-package imports (`harvest_typed`, `internal_role`, `typed_scope`), every one at the base, nothing
absent at trunk. `app/internal_role.py` and `app/access_state.py` import no app module. Re-runs on the
final base, because a seam answer is only as current as the base it was asked about.
