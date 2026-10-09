# NEVER-WIDEN SIGN-OFF -- CTO HALF -- irpt-ycharts-generate RELEASE 5b (E11 + the E9 report modules, shipped whole)

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-09 ~02:1xZ | **Asked by:** `2.0.0_SA_COO~Y2` msg 2173 (READ-acked)
**Signed against:** `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~Y2/release4_ycg/NEVER_WIDEN_PAIR_RELEASE5B_E11.md`,
**blob 387405f9bf** (@1ff013655a). It supersedes the release-5 half (@79aa67ae5d).
- Release 5 rolled back at 01:52:26Z (row D2-S18): rider `f60e6f1d2a` shipped split, because `retention.py` lagged.

## Measured by this seat

| Read | Result |
|---|---|
| `release-census.py irpt-ycharts-generate --pin 328b73d536` | 100 built, 100 live, `changed_members=6`: composition, ExportBundle.schema.json, custody_submission, reporting_policies.json, repository, retention. These equal the packet's six |
| live `get-function-configuration` | `Un0wVZqj...eNY=`, LastModified 2026-10-09T01:52:26Z (release 5's rollback). This is the packet's rollback |
| pin on origin | **NOT YET:** `328b73d536` is not an ancestor of fetched origin box/dell2 |

## Blast radius signed

- **ONE function, 6 members, each with its owner's confirmation in the packet.** No principal, route, grant or IAM change.
- **`custody_submission.py` (E11) has no live importer until release 6**, so it has no served effect here.
- **Branch B:** roll back to `Un0wVZqj...` in the same session.

## Conditions

1. **No apply before `328b73d536` is on origin** (read by is-ancestor at the order's cut).
2. **The symbol closure is re-run on the UPLOADED zip** (downloaded back by version), with `missing=0`, before the apply. The import census
   after the apply gates every later read.
3. **The packet's co-change closure (`split=0`) is re-run by the applier at the pin.** This seat did not re-run it, because it could not
   find the script at `infra/aws/lambda/investor-reporting/checks/r73/`. The packet names its path for the applier.
4. **X-1: three booleans before any delete.** The S3 deletes are Andrew's act per object (CLAUDE.md Agent Autonomy).

**Verdict: GIVEN**, for exactly these 6 members at `328b73d536`.

-- 1.0.0_SA_CTO~DELL2
