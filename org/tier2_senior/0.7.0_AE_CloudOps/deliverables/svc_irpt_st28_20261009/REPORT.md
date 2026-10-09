# TO28 st28 svc-irpt reader window

## ADD — applied 2026-10-09T09:09:10Z

COO~C GO 107857 and CTO consent 107850 authorize the signed Dell2 reader window for ledger `irpt-ycdgen-f1-st28-20261009`. The live resource policy first matched the signed BEFORE document under the required unordered-set comparison. No secret value was read.

The deploy ledger was opened and committed at `e552d33bb0e056760bc8aba0192d35d7e4269b47` before the first write. The signed files are:

- ADD SHA-256 `8f1ea95a3522034f75b5f526058fc49e7b20db6df9ca0a94e2eece02eb96f349`
- BEFORE SHA-256 `0207127228ff08a4390d29cfd8b53b7946460d87d977f427c0984c9e6925a633`

Two initial ADD attempts reached a matching ADD readback but stopped before any principal simulation because the simulator invocation itself was malformed. Each attempt automatically restored the signed BEFORE policy and proved set-rule equality before the next attempt:

1. The first evidence file carried a UTF-8 BOM rejected by the simulator. BEFORE was restored by `2026-10-09T09:07:35.2840147Z`.
2. The second invocation supplied the account number instead of the account-root ARN as `--resource-owner`. BEFORE was restored by `2026-10-09T09:08:10.9010606Z`.

The simulator invocation was then validated against the restored BEFORE policy for all three principals. The final signed ADD put ran from `2026-10-09T09:09:07.8429027Z` through `2026-10-09T09:09:10.4758656Z` with `--block-public-policy`. The live readback matches ADD under the set rule. Exact-resource simulations returned:

- `cloudops-dell2-agent-user`: `allowed`
- `cloudops-dell1-agent-user`: `explicitDeny`
- `Andrew_Berman`: `allowed`

The put time was sent immediately to COO~C and relayed through MSTR to Dell2 COO~G2. The mandatory REMOVE deadline is `2026-10-09T13:09:10.4758656Z`, or Dell2 X1 if earlier. The REMOVE leg remains open.

Evidence includes `before.json`, `start-verdict.json`, both automatic rollback records and readbacks, `after-final.json`, `put-final.json`, `put-final-timing.json`, `put-final-verdict.json`, and `live-simulations-final.json`. No `GetSecretValue` call was made.
