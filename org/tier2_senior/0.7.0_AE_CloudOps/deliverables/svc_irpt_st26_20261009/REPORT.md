# TO23 st26 svc-irpt reader window

## ADD — applied 2026-10-09T01:20:15Z

COO~C GO 107571 and CTO addendum 107569 authorize the same signed window for dell2 ledger `irpt-ycdgen-f1-st26-20261008`. The live resource policy first matched the signed BEFORE document under the required unordered-set comparison. No secret value was read.

The signed ADD document was installed with `--block-public-policy` between 01:20:12Z and 01:20:15Z. The live readback matches ADD under the set rule. Exact-resource IAM simulations returned:

- `cloudops-dell2-agent-user`: `allowed`
- `cloudops-dell1-agent-user`: `explicitDeny`
- `Andrew_Berman`: `allowed`

Evidence is in `before.json`, `start-verdict.json`, `put.json`, `after.json`, `put-verdict.json`, and `live-simulations.json`. Ledger `org/critical_paths/change_management/20261009T0119Z_svc-irpt-st26-window-laptop-20261009_deploy_completion.md` has ADD closed and REMOVE open. Opening commit: `9fe13af4b2`; the evidence commit is supplied in the issuer report.

REMOVE is mandatory at dell2 X1 or 2026-10-09T06:00Z without waiting. It must start from live ADD, restore signed BEFORE with `--block-public-policy`, verify set equality, and simulate both Dells `explicitDeny` and the walker `allowed`. AC1 remains pending until that leg. The separate F1 C2 deadline is also active. LOCAL only; measured origin/CLOUD `71aac4e90db557a8106861d5f7f63c94ab0399b7` and origin/box/laptop `4d7f665001ea6384770fc180b7e3c33474d78d38`. No shared-branch push.

## REMOVE - applied 2026-10-09T01:34:00.7406433Z

COO~C GO 107592 reported the dell2 X1 trigger. The live resource policy matched the signed ADD document under the required unordered-set comparison at 01:33:45Z. The signed BEFORE document was restored with `--block-public-policy` from 01:33:57Z through 01:34:00Z. The live readback matches BEFORE under the same set rule.

Exact-resource IAM simulations against the restored live policy returned:

- `cloudops-dell2-agent-user`: `explicitDeny`
- `cloudops-dell1-agent-user`: `explicitDeny`
- `Andrew_Berman`: `allowed`

The REMOVE evidence is in `remove-start.json`, `remove-start-verdict.json`, `remove-put.json`, `remove-put-timing.json`, `remove-after.json`, `remove-put-verdict.json`, and `remove-live-simulations.json`. No secret value was read. The deploy ledger is closed with both legs proven, its open sentinel is removed, and AC1 passes on the restored `WalkerReadsByExplicitArn` policy. The separate F1 C2 obligation remains open pending its own GO or the 06:00Z hard close.
