# SESSION LOG -- AMGT_RESAPP.TO-AMGT-rk-36 (0.9.0_WK_AMGT_RESAPP~39)

1. Confirmed the continuation: `git rev-parse --short=10 HEAD` -> `7e3baf2b04`; AMGT-rk-35's
   `<status>` read `complete` and its change-management entry read CLOSED
   (`20260919T0953Z_amgt-rk35-rolling-window-validation-names-20260918_deploy_completion.md`).

2. Read both never-widen halves (`NEVER_WIDEN_ROUND14_CHAIN_M_{COO,CTO}_HALVES.md`) -- both carry
   an `AMGT-rk-36` section; the CTO half's WITHHOLDING on the rollback shape was LIFTED -- SIGNED at
   `541d395e0d` (re-cut as `s3api copy-object` from the pre-act VersionId, never a Terraform
   `version_id` re-point). sha256: COO `594ba746e3...`, CTO `db0e1bbaffe...`.

3. Confirmed `bloomberg_health` -> `ok: True`. Ran the dry-run pull (AC1's discipline before any
   live act) -- printed 3 override requests per name, 0 written.

4. Opened the change-management entry `amgt-rk36-forecasts-adapter-20260918` (3 legs) BEFORE any
   live act; committed the sentinel + entry (`0e390d887a`); pasted the never-widen pair sha256, the
   PRE-ACT `CodeSha256` (`3TXiCLy8w3Le2z9hiKzW3eqqhKQT4ALaKGCeCECv3rM=`), the artifact's pre-act
   `VersionId` (`gg65p2Qo.KibhsWzkZmsvaSdavPreFoF`, the rollback target) and bucket versioning
   `Enabled` (re-measured).

5. Built the producer/adapter code: `model_block_pull.py` (three `ReferenceDataRequest`s per
   security, explicit `BEST_FPERIOD_OVERRIDE`, `bestdata.json` landing, the quarter-trap guard,
   the forecast-scope derive), `sa_forecast_fallback.py` (new module: ported entity test, the SA
   field map with the one measured mapping `pe_nongaap_fy{n}` and four candidates, the fallback
   sequence), `build_unit_map.py` (BEST_ mnemonics joined to their unit families),
   `scopes.py` (`SCOPE_FORECAST`, `MODEL_BLOCK_SCOPES_MANDATORY` keeping the landed-artifact
   completeness test honest against the un-re-derived BABA fixture),
   `test_fiscal_scope_contract.py` (the one changed assertion), and the new
   `test_forecast_fallback.py` (13 offline planted cases). Committed `1de3fb108c`.

6. Ran the live pull + derive on the three validation names (`CAT US Equity`, `CSL AU Equity`,
   `6861 JP Equity`) -- 15 requests total, all with the explicit override. AC1/AC2/AC3 measured
   PASS: all three names' Bloomberg BEST_ pulls were FULLY populated (no gap on any of the 15
   cells per name), so the Seeking Alpha fallback's honest "no Bloomberg gap" branch fired for all
   three -- zero Seeking Alpha network calls were made this session (a legitimate exercise of the
   gap rule, per AC3's own closing line; the fill/no-value/not-meaningful/quarter-trap/entity-test
   branches are proven by the AC4 fixture instead).

7. AC4: `pytest integrations/bloomberg/research/tests/test_forecast_fallback.py
   lib/research/api/tests/test_fiscal_scope_contract.py` -> 22 passed, 0 failed, 0 errors.

8. Discovered, while proving AC5, that `read_thesis_bundle` never nested a `model` key (only
   flattened three of `read_model()`'s keys out by name), so AC5's own grading script (reading
   `inner['model']`) could not reach `forecast_figures`/etc at all -- a pre-existing gap, not
   introduced by rk-34/rk-35. Filed row `AMGT_RESAPP-Z-W39-S3`. Fixed additively (`bundle["model"]
   = model`, every existing flattened key unchanged); re-verified 22/22 offline tests plus 16/16
   `lib/research/api/tests/` thesis/model/fiscal tests. Committed `5c701edc4c`.

9. Re-ran the stale-bytes check (EMPTY, licensed) and rebuilt/re-uploaded the artifact (VersionId
   `6Kr.kKS6nCiPwLaCJkz1vMLnexahBGcg`, sha256 `7lAqBNEGJWmYGt87UpxFYobyA6jevkFxM5yoIIjB+WY=`).
   Pre-deploy 13-route census: 13 of 13 200 (movement=trending, subject=chatter). Targeted plan: 0
   add / 1 change (`source_code_hash`/`s3_object_version`/`last_modified` only) / 0 destroy.

10. `HALT_ACK=1 bash .tools/safe-apply.sh -chdir=infra/aws/terraform/harvest apply
    -target=module.scoped_amgt_api.aws_lambda_function.this -auto-approve -no-color` -> `Apply
    complete! Resources: 0 added, 1 changed, 0 destroyed.` No HALT-GATE surfaced this run.
    Post-act `CodeSha256` = uploaded sha; targeted replan `No changes`.

11. Post-deploy 13-route census: 13 of 13 200, `LOST=[]` `GAINED=[]`. Ran AC5's literal
    invocation: BA_US_Equity SERVED/has_forecast_keys True/forecast_figures 0/forecast_reason
    naming the missing `bestdata.json`; `check_face_len` 179 and `fiscal_row_count` 165, both
    independently confirmed unmoved (`_figures(model_block, 'fiscal_year_line_item')` direct read,
    unaffected by this order's additive change). `HOLLOW_NONEXISTENT_KEY_Equity` ABSENT/
    has_forecast_keys True/forecast_figures 0.

12. Closed all 3 change-management legs and the entry (`528200fb02`).

13. Wrote and validated the proof-of-spec instance; flipped `<status>` to `complete`.
