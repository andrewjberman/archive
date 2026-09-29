# ANNOUNCE -- NFRA_OPALAI OA-e-3: switch the Analyst on for opal_asker_query, and its narrow gateway release

Seat: 0.9.0_WK_NFRA_OPALAI~10 (worker of 2.0.0_SA_COO~AI). Part A is built and committed. Nothing below step 1 of part B
has been done; the instance is untouched.

- Target: opal-gateway on i-07dccb1615503ac99 (/opt/opal-gateway).
- Part A build commit (slot branch wk-NFRA_OPALAI-10): `c06a3a4379` -- `app/identity_scope.py` (opal_asker_query joins
  the opalbloomberg@opalinvest.com seed, G-SCOPE record @f8d1103a38; frame (iv) updated) and
  `tests/test_identity_scope.py` (`test_concierge_seed_admits_asker_query`; 10 passed).
- Release branch: `rel-nfra-opalai-r2-asker-switch-on-gateway`, created at step 2 after GO from the base below, carrying
  `c06a3a4379` and OA-f-7's code commit `af104d6353` and nothing else.
- Base commit (resolved by content): `3371f18803` (MX-r-4, `rel-nfra-mcpindex-r3-gateway-b`).
- Release commit: created at step 2 after GO; its hash will be in the final report.
- Deploy tree (amendment 1): `rel-nfra-opalai-r2-asker-switch-on-gateway-v2` at /c/tmp/oa-10-sw-rel2 on CLOUD with only
  `infra/aws/ec2/opal-gateway` replaced by the release tip's tree; the gateway-tree hash is proved equal before any act.
  Rollback: `rb-nfra-opalai-r2-asker-switch-on-base-v2` the same way on the base's gateway tree
  (`09ccfc39ad669ea2c300638fe7cb8c45f27bb9ee`). The -v2 branches are deploy-only and never merged.
- Files shipped (expected census): `app/identity_scope.py`, `app/asker_scope.py`, `tests/test_identity_scope.py`,
  `tests/test_asker_nochannels.py`, `tests/test_asker_binding.py`, `tests/test_portal_grant.py`. No tool added; the
  base's `deploy-to-ec2.sh` (line 197, the 5-id ENABLED_INTEGRATIONS) is carried unchanged.
- Ledger slug: `nfra-opalai-r2-asker-switch-on-gateway` (opened at step 5, on the slot branch).
- Window: outside US business hours only (row Z-S24). One gateway deployer at a time; 2.0.0_SA_COO~O's OG-x-3 queues behind.

## Base resolution (step 0, read-only over SSM, status Success)

| file | live md5 = 3371f18803 |
|---|---|
| app/identity_scope.py | 442c9755d14aa1ffbbccf5bf0fe73656 |
| app/asker_scope.py | 7e6bf35edb06099331f81561528a0ea8 |
| app/tools.py | 7ead9892a2f75b5b3326c0c16a1bcd46 |

Candidates compared: 3371f18803, d287ffb346, 6a98a0553a and every local or origin `rel-*` ref. The three files match at
four commits: `3371f18803`, `d287ffb346` (OA-r-1), `20a58c4edb` (OA-r-1's -v2 deploy tree) and `7b729821a9` (OG-x-3).
The live `.env` key set (27 names, values never read) equals the `deploy-to-ec2.sh` template's at all four, so it does not
separate them. They are separated by the files where they differ, read live over SSM (7 files): the live md5 of
`opal_discover/integration.py`, `portal_index/integration.py`, `refs/DATA_CATALOG.yaml`,
`schwab/engine.py`, `schwab/envelope.py`, `schwab/export.py` and `schwab/integration.py` equal `3371f18803`'s on 7 of 7.
`d287ffb346` (and its -v2 tree) matches 4 of 7 (the schwab four) and `7b729821a9` matches 0 of 7. Survivors of
the order's literal rule: all four; the newest by that rule would be `7b729821a9`, which the host is not running (the
same defect as row NFRA_OPALAI-Z-W10-S3). Base: `3371f18803`, which also equals the host's served tree (`09ccfc39ad`).

Status: ANNOUNCE READY. Waiting for GO.
