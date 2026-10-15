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

## Seams

Enumerated against the current base with `W/p21_seams.py`: **CLEAR**. Four modules opened, 3 distinct
intra-package imports (`harvest_typed`, `internal_role`, `typed_scope`), every one at the base, nothing
absent at trunk. `app/internal_role.py` and `app/access_state.py` import no app module. Re-runs on the
final base, because a seam answer is only as current as the base it was asked about.
