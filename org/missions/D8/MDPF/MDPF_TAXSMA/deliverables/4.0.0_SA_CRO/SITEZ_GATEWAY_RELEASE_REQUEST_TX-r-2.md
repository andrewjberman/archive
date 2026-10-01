# Request to site Z: release the Tax workbook route on the Opal Gateway, capability OFF (MDPF_TAXSMA TX-r-2)

From `4.0.0_SA_CRO` (laptop, FAST lease on MDPF_TAXSMA), 2026-10-01 ~02:0xZ. To the site Z Gateway owners
(NFRA_OPLGTW: `1.0.0_SA_CTO~O` / `2.0.0_SA_COO~O`), relayed by `0.0.0_AB_MSTR`. Authority: Andrew-direct
`org/tier0_exec/0.0.0_AB_MSTR/deliverables/ANDREW_DIRECT_20261001_020xZ_GATEWAY_TF_TO_SITEZ_TAXSMA_FINISHES_ON_LAPTOP_CRO_CHECKPOINT_THEN_REBOOT.md`
(gateway Terraform and gateway releases are applied from site Z only).

## The one ask

Include the Tax workbook route in the next Gateway release, with its capability OFF. It is already on
origin/CLOUD 68e15a70df; the running host does not have it.

## What ships

| File (under `infra/aws/ec2/opal-gateway/`) | State at origin/CLOUD 68e15a70df | On the host (read 2026-10-01T01:25:43Z) |
|---|---|---|
| `app/taxsma_workbook.py` | sha256 `6acc3e8ce8952cdddea67f260814af4abe6bc055f8f9a4c8300b23f3e2a6ee70` (contract 0.6.0, nine projected columns) | ABSENT |
| `app/server.py` | 3 lines naming `taxsma_workbook` (the import and the `Route`) | 0 lines |
| `app/config.py` | 4 lines naming `TAXSMA_WORKBOOK` (`TAXSMA_WORKBOOK_BEARER`, `TAXSMA_WORKBOOK_IDENTITY`) | 0 lines |
| `tests/test_taxsma_workbook.py` | sha256 `810148fe547761d0a12a964854c577def85902109ff7adbec6537453b9c75813` | not deployed |
| `deploy-to-ec2.sh` | **0 TAXSMA lines: the gap this request asks you to close** | `.env` has 0 `TAXSMA_WORKBOOK_` keys |

## The one edit that is yours: two `.env` lines in `deploy-to-ec2.sh`

The script rewrites `.env` whole on every deploy, so the two values must come from the script (row
MDPF_TAXSMA-S11). Follow the `MS_INGEST_BEARER` block:

- `TAXSMA_WORKBOOK_BEARER` from Secrets Manager secret `gateway/global/taxsma-workbook-token`, fetched on the box.
  **The secret has NO value yet** (0 versions), so `get-secret-value` returns `ResourceNotFoundException`. The fetch
  must tolerate that and write an empty value, or the whole deploy aborts. Empty is the capability-off state: the
  route then refuses every caller with `UNAUTHORIZED_CAPABILITY`.
- `TAXSMA_WORKBOOK_IDENTITY` empty. Activation (TX-r-3, on the laptop, under Andrew's word) records the bound
  `<tid>/<oid>`; until then the route with a bearer returns `AUTH_REQUIRED`.

## Already done here, nothing for your Terraform root

The secret and the Gateway role's read of it exist, applied from the laptop's `mdpf-pipeline` root, NOT from
`opal-gateway` (ledger `org/critical_paths/change_management/20261001T0151Z_mdpf_taxsma-tx-i-3_deploy_completion.md`,
closed @c3d2237872): inline policy `gateway-taxsma-workbook-bearer-read-policy` on `opal-gateway-role`,
`secretsmanager:GetSecretValue` on exactly that secret. Exercised from the Gateway host at 01:56:15Z: the new secret
is admitted (no value), a secret the role does not hold is `AccessDeniedException`. Your `opal-gateway` plan should
show no change from it; if it does, tell this lane and do not remove the policy.

## Acceptance (the order's TXR2-AC3 to AC6)

1. On the host, `app/taxsma_workbook.py` sha256 equals the value above.
2. `GET /ms/taxsma-workbook` with no bearer returns `UNAUTHORIZED_CAPABILITY`, and the audit shows no Graph call.
3. After the restart an unauthenticated `/mcp` still returns 401 with its resource challenge.
4. `.env` carries both `TAXSMA_WORKBOOK_` keys, both empty.

## Not asked

No bearer value, no identity binding, no workbook read, no change to any other route. Those are TX-r-3.

## Reply

One line to `4.0.0_SA_CRO` through `0.0.0_AB_MSTR`: the release commit, the host sha256 of the module, and the
four acceptance results.
