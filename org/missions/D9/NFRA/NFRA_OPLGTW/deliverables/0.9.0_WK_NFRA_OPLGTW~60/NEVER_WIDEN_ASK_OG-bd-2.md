# Never-widen ask -- OG-bd-2, `blackdiamond_list_fees` denied to unprofiled principals, master_admin admitted by tier

By: `0.9.0_WK_NFRA_OPLGTW~60`. Halves owed: `1.0.0_SA_CTO~Z`, `2.0.0_SA_COO~O`. Source: CTO round-35 analysis E1
(`org/missions/D9/NFRA/NFRA_OPLGTW/ledger/ROUND_ANALYSIS.round35.md` @682d1ced78), on Andrew's YES (sitez-1b36).
Nothing here is released or deployed; this is the ask for the gateway release that ships the code. This change NARROWS
admission; it widens nothing.

## 1. The diff by file

| file | change |
|---|---|
| `infra/aws/ec2/opal-gateway/app/data_entitlement.py` | `decide(tool, access, tier=None)`: a principal with NO profile is denied `blackdiamond_list_fees` (`entitlement_denied`) unless `tier` is `master_admin`. `tool_denial` and `visible_tools` read the tier from `app/tier.py resolve_tier(principal, get_config())` (the one tier source `tools._run` uses; fail-closed to no tier on any error). Profiled principals and the Schwab tools are unchanged. |
| `infra/aws/ec2/opal-gateway/tests/test_og_bd2.py` | new; `test_ogbd2_ac01..03`, offline. |
| `infra/aws/ec2/opal-gateway/tests/test_data_entitlement_family.py` | `test_ogpf1_ac02` re-pinned: the unprofiled Black Diamond answer was `None` (pass-through), now `entitlement_denied`, and `None` for tier `master_admin`. |

## 2. Who is admitted, who is denied (census `BD1_CENSUS.json`, 2 unprofiled callers)

- Admitted class: `master_admin` (by tier, no profile written). The caller `2cdb43ed4d` (tier `master_admin`, 4 calls, outcome ok)
  KEEPS its access.
- Still denied: the unlinked caller `fc9aed2e22` (tier `standard`, 1 call). It was already DENIED by the tool's own gate with no
  principal on record, so it loses nothing it has. After this release the denial arrives earlier, at the data-entitlement guard.
- No profile or grant is written: the only profile kind, `restricted`, confines its holder on the data-grant family.

## 3. Blast radius

ONE tool (`blackdiamond_list_fees`), and only unprofiled principals whose tier is not `master_admin`. A profiled principal's
answer, every other tool, every Schwab tool (denied to unprofiled principals, master_admin included, exactly as before) and
every REST route are unchanged. The only effect on a user is a denial where a principal with no profile used to reach the
tool's own gate.

## 4. Rollback

Rollback is the gateway's standard rollback to the prior live release ref (the release immediately before the one carrying this
commit); the prior release passes `blackdiamond_list_fees` through for an unprofiled principal as today. No data, IAM or profile
state is written by this change, so there is nothing else to unwind.
