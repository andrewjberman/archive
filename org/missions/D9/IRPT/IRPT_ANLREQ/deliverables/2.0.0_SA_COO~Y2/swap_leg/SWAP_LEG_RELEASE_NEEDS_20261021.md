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
An Overview with a real-but-unregistered name from the PRD (BREIT, SREIT or KPEC), not ZQXWVK (a nonsense ticker the model correctly cannot classify, which stays NOT_ANALYSED). The issuer cuts that order (7M) when r34t is live.
