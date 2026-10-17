# OG-ap-33 -- STOP before the merge (0.7.0_AE_CloudOps~NFRA1, 2026-10-17)

Order: `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ap-33.land-harvst-release-on-trunk.md` (GO msg 35397). Read-only so far: no worktree, no merge, no commit of a merge. Row `NFRA_OPLGTW-Z-S356` (BLOCKING).

## What was measured (`git merge-tree --write-tree --name-only trunk_base hvst`; trunk_base `dc076cc44f`, hvst `319c9413a2`, merge base `91811b648a`)

- **Conflicted paths: 20** (the order named 18). The two extra, neither in the order's `<paths>`:
  - `infra/aws/ec2/opal-gateway/tests/test_og_en13.py`: a gateway TEST file, covered by the order's test-file rule (trunk's side).
  - `infra/logic/registry/legacy_addresses.json`: add/add of a registry file. hvst side 209 rows, trunk side 215; every hvst row is in trunk's with the identical row, 0 rows only in hvst, 0 rows that differ, 6 only in trunk; the `_about` blocks are equal. Trunk's side is a strict superset, so taking it drops nothing; no rule in the order names it.
- **The five gateway live-byte paths resolved to the blobs at `release_sha` `9d5b712557`** (the order's rule):

| path | trunk blob | live blob | trunk commits since the merge base | resolves to live without loss |
|---|---|---|---|---|
| `app/client_adapter_bd49f.py` | `48c8cc2d2f` | `48c8cc2d2f` | 9 | yes (equal) |
| `app/refs/DATA_CATALOG.yaml` | `2cbe275d03` | `2cbe275d03` | 21 | yes (equal) |
| `app/tools.py` | `cd37a28fb6` | `e335c267f5` | 16 | **NO** |
| `app/destructive_ops.py` | `3b2c845fe8` | `3058b6a732` | 14 | **NO** |
| `deploy-to-ec2.sh` | `28ef9af407` | `7385fbec55` | 14 | **NO** |

## The STOP

The order: "STOP, file a BLOCKING row and create no merge commit if resolving any gateway path to the live blob would drop a trunk change that is not deployed (the trunk blob differs from the live blob and a trunk order since the merge base changed it)". It holds for three paths. The live blob equals the hvst blob in each, and each side carries lines the other lacks:

- `app/tools.py`: trunk has 9 lines live lacks (the `harvest_published` import and the `harvest_get_published_analysis` tool, commit `1b89afbb62`, OG-gt-11 hookup, order OG-gt-5); live has 7 lines trunk lacks (the HVST release's own).
- `app/destructive_ops.py`: trunk has 1 line live lacks (the `harvest_get_published_analysis` entry in the read-only list, same commit `1b89afbb62`); live has 1 line trunk lacks.
- `deploy-to-ec2.sh`: trunk has 22 lines live lacks (the OG-db-1 preflight, commit `3a40dffdcc`, order OG-db-1); live has 35 lines trunk lacks (the HVST release's own).

Neither blob is the merged result: a real three-way merge of these three files is needed, which the CTO's rule (msg 35311) did not foresee, and the issuer's order forbids resolving beyond it. The live release `9d5b712557` does not carry `harvest_get_published_analysis`, so trunk-side bytes would change the live code; live-side bytes would delete a trunk order's work.

## What the issuer decides (one question)

For `app/tools.py`, `app/destructive_ops.py` and `deploy-to-ec2.sh`: (a) a true three-way merge keeping both sides' lines (no live byte moves on the host; trunk would then differ from live by the trunk-only lines, which is the state before this landing), or (b) the order's live-blob rule with the trunk changes re-landed later by their own order. Also: `test_og_en13.py` (trunk side) and `legacy_addresses.json` (trunk side, a superset) are extra conflicts outside the order's `<paths>`; they need the issuer's word to be resolved here.

Order status: left `staged`. No merge commit exists.
