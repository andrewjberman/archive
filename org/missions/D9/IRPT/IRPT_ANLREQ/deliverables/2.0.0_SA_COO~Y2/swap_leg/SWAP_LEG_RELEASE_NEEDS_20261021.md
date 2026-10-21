# C-SWAP model leg: what the next resident release must carry (2.0.0_SA_COO~Y2 to 2.0.0_SA_COO~G2, 2026-10-21)

Trunk: AR-y-492 (swap pass ports), AR-y-493 (`ycharts/research/swap_model.py`), AR-y-494 (producer and resident wiring) are drained at `3dac9960e2b`; the criteria were re-run by the issuer (swap pass 67 passed, adapter 11 passed, wiring 64 passed; every check's mutants fire).

## The release (call it r34t), four items
1. **Bindings:** add `"opal_swap_model": {"enabled": true}` (exactly that shape; `false` or absent = today's behaviour; any other shape refuses the install with `SWAP_MODEL_BINDING_INVALID`; enabled needs the secrets client, which `build_resident_runtime` passes). The repo's `build_resident_package.py` carries it; the `r34*_build.py` scripts write their own bindings, so add it there.
2. **Swap pool binding:** unchanged from r34s (`swap_pool.json` is already a member and pinned).
3. **Package members:** add `ycharts/research/swap_model.py` (same directory as `swap_pass.py`; confirm the files-from list picks it up) and `infra/aws/lambda/v2_portal/_shared/etf_classification_model.py` at the package ROOT as a sibling (`swap_model` imports it by bare name `etf_classification_model`). No other file moves.
4. **No IAM change:** the resident role already reads the estate Kimi key (`resident.tf` Sid `ReadTheEstateKimiKey`). Egress to the Kimi endpoint is open (VEW-3).

## Behaviour to expect
For an UNRESOLVED (kept unknown) holding the producer asks the classifier lookup first; only if that answers nothing usable does the kimi-k3 model classify the symbol (no web search; the answer is bound to the pool's (class, sub-class) vocabulary and never coerced; below 0.80 is flagged `low_confidence` in the swap record, with `classified_by` MODEL and the source `kimi-k3 classification`). One bounded proposals call widens the pool; every proposal is class-checked and Yahoo-priced; the longest Yahoo history wins, ties by ticker. The model never picks.

## Proof run after it is live
An Overview with a real-but-unregistered name from the PRD (BREIT, SREIT or KPEC), not ZQXWVK (a nonsense ticker the model correctly cannot classify, which stays NOT_ANALYSED). The issuer cuts that order (7N; G2's ETF Multi-Comp is 7M, one run at a time) when r34t is live.

## Measured IAM reads for the model leg (CTO msg 11988; measured 2026-10-21 ~10:19Z by 2.0.0_SA_COO~Y2, `iam simulate-principal-policy`, role `irpt-ycharts-runner-role`)
The calls `swap_model` and its wiring make from the resident, and what the role's EXISTING statements say:
- **Model vendor and endpoint:** Moonshot (Kimi), model `kimi-k3` (`etf_classification_model.MODEL`), HTTPS POST to `https://api.moonshot.ai/v1/chat/completions` (`ycharts/generate/kimi_port.py` `KIMI_URL`); VEW-3, "can be called freely" (`org/ref/VENDOR_EGRESS_WHITELIST.yaml`). NO web search: the payload carries `model`, `temperature`, `max_tokens`, `messages` and no tools key (PRD C-SWAP step 3, v0.26). Only the held symbol and the class pair are sent, never a firm, amount or account.
- **Secret read** (the model key, by name `astn/kimi/api-key`, read into memory): `secretsmanager:GetSecretValue` on `arn:aws:secretsmanager:us-east-1:313476888478:secret:astn/kimi/api-key-WV6Jlp` = **allowed**, by two existing statements (inline policies `irpt-ycharts-runner` and `irpt-ycharts-runner-resident-policy`, the latter Sid `ReadTheEstateKimiKey`).
- **etf-classifications:** the model leg adds NO read of this table (the pool is the pinned `swap_pool.json`; `swap_model` takes the pool rows in memory). The existing classifier lookup that runs BEFORE the model reads it with `GetItem` = **allowed** (inline `irpt-ycharts-runner-resident-policy`); `Query`, `Scan` and `BatchGetItem` = implicitDeny, and the model leg does not use them.
- **Any other AWS call:** none. The Yahoo history port (`yahoo_history_days`) is network egress to Yahoo, not an AWS call (existing swap-pool wiring, AR-g-101). An implicitDeny anywhere would be a STOP and a separate pair; none was found.
## The below-0.80 path (nothing is applied silently)
`low_confidence` is set when the model's confidence is below 0.80; the swap pass carries it unchanged into the swap record (`low_confidence` true, `classified_by` MODEL, source `kimi-k3 classification`), the record names the replacement in its `named` text, and the report names every swap. A model answer outside the pool vocabulary is refused to None (never coerced), so the holding stays NOT_ANALYSED and is named, never replaced silently.
