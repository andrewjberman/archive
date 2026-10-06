# OG-ln-1 -- gateway lineage reconcile (round 18, `0.9.0_WK_NFRA_OPLGTW~22`)

Record: `LINEAGE_R18.json` (same folder). Live = `37be3485db` (manifest `deployed_commit`). Port commit `ebf5fca97d` (LOCAL).

## Live confirmation (read-only)

SSM `md5sum` of the six diff files that ship to the host (`app/admin_refusals.py`, `aws_roles.py`, `envelope.py`,
`integration.py`, `app/server.py`, `deploy/NFRA_OPLGTW_CONTRACT.json`) equals `git show 37be3485db:<path>` for 6 of 6.
`tests/`, `runbooks/` and `deploy-to-ec2.sh` are not extracted to `/opt/opal-gateway`, so they have no host md5. No host write.

## Method

`git diff 37be3485db 079131b3a0 -- infra/aws/ec2/opal-gateway`: 23 files. A merge-base three-way is NOT usable: live's tree
was cut from release trees (`e3567ce5f7`, "CLOUD's tree with the gateway dir replaced"), so live is OLDER than CLOUD on files
CLOUD changed after the fork and NEWER on files only releases touched. Each hunk was classified by provenance instead: a
live-side line that CLOUD's history for that file never held = LIVE_ONLY; a CLOUD-side line live's history never held, or a
hunk whose live side is only superseded CLOUD text = CLOUD_ONLY (script `.scratch/classify.py`, not committed).

## Ported (5 files, each now byte-equal to live)

| path | live-only content |
|---|---|
| `app/integrations/schwab/aws_roles.py` | `environ_with_external_ids`, `_read_external_ids_secret`, `EXTERNAL_IDS_SECRET_VAR`, `EXTERNAL_ID_FIELD`, 2 imports (4 hunks) |
| `app/integrations/schwab/integration.py` | the `environ_with_external_ids(os.environ)` call (1 hunk) |
| `deploy-to-ec2.sh` | live's template: OG-rl-1 rosters, OG-tr-1 / OG-rl-3 bearers, OG-rl-2 sender table, MX-r-7 BD ExternalId, ENV_KEYS announce, quoted `.env` printf (7 hunks; CLOUD's one printf line has no key live lacks) |
| `deploy/NFRA_OPLGTW_CONTRACT.json` | absent on CLOUD |
| `tests/test_schwab_host_inputs.py` | absent on CLOUD |

## CLOUD_ONLY (18 files still differing; all `SHIPS_IN_RELEASE`, none `REVERTS_ON_OWNER_WORD`)

Owners by commit are in the JSON. Headlines: `app/server.py` + `tests/test_login_retire.py` = OA-e-10 `8ed37b3266`
(`/login` narrowing, "a named release after OG-ln-1"); `tests/conftest.py` includes OG-ti-1 `689d034b7c` (untouched);
`app/admin_refusals.py` + its test = MCPMSP MS-sg-1 (via `e138cec769`); `app/.../envelope.py` = OG-o-4 `877339606f`;
the rest are tests, the runbook and walkthrough protocol (source-only, no host effect).

## Test readings (each file in its own process, `infra/aws/ec2/opal-gateway`)

15 schwab files + `test_login_retire.py`: all pass except `test_schwab_export_stream.py` (1 failed `test_ogx4_ac03`, the
recorded baseline id; `test_ogx2_ac01` passed this run) and the ported `test_schwab_host_inputs.py` (2 of 9 failed, row
`Z-W22-S9`: stale key count 51 vs 50, which fails on live's own tree; a build_package call-shape mismatch outside this order's
paths). `test_principal_cutover.py` (run as a neighbour) has 1 failure that predates the port (row `Z-W22-S10`).
