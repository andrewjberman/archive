# REPRO_NOTES -- AR-y-436 (0.9.0_WK_IRPT_ANLREQ~316), HEAD b8e0e961034

Script: `repro_composition.py` (this folder). Run: `python -I org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~316/repro_composition.py`.

## Output (two runs, identical)

    REPRO-A step=none class=none
    REPRO-B step=none class=none detail=-
    REPRO-C step=2 class=ValidationError

## Diagnosis

1. Offline, neither (A) nor (B) is refused. CompositionAdmission.validate admits the three-row KEPT_BY_HISTORY
   composition and the four-row composition with one UNRESOLVED/KEPT_AS_TYPED row. The refusal seen in run 5B is
   NOT reproduced by the HEAD code path. Its cause stays unmeasured here.
2. Step 5 is live, so the admission is not a pass-through. A probe in `.scratch/` (not committed) tampers the
   frozen document: `analysis_dollars` of a kept row, the `history.rows` of a kept row, and the `resolution` of the
   UNRESOLVED row each refuse at step 5 (PortfolioRefused via verify_frozen_portfolio).
3. For 5C: validate admits the three-row composition on this replica. That does not prove 5C passes, because
   the live refusal cause is still unknown.

## (A) three KEPT_BY_HISTORY rows (SPY, AGG, TIMXX)

- Built: freeze_template_portfolio (intake/portfolio.py:416) over checks from security_resolution.SecurityResolver
  with a synthetic checker (KEPT, reason HISTORY_ROWS) and an empty provider. Result NORMALIZED, 3 rows, method
  KEPT_BY_HISTORY, finding TICKER_KEPT_BY_HISTORY NOTICE x3.
- Steps 1-4: admitted. Step 2: resolved.document is a bare object (RequestComposition.schema.json:766).
- Step 5: admitted. verify_frozen_portfolio (portfolio.py:336-357) rebuilds the template and compares it byte for
  byte (portfolio.py:347-348). Refusal sites that would fire: composition_admission.py:63-64 (log + raise),
  portfolio.py:341 FROZEN_INPUT_CHANGED, portfolio.py:348 TEMPLATE_REPLAY_MISMATCH.

## (B) (A) plus ZQXWVK, resolution UNRESOLVED, method KEPT_AS_TYPED

- Built: same freeze with the equal Keep pair (ZQXWVK, ZQXWVK, finding TICKER_NOT_FOUND). The row is built at
  portfolio.py:591-594: resolution UNRESOLVED, method KEPT_AS_TYPED, provider_receipt_sha256 None, price None,
  price_source None, outside holdings.
- Steps 1-5: admitted; the rebuild reproduces the UNRESOLVED row (tamper probe: removing `resolution` refuses at step 5).
- No field of the UNRESOLVED row is rejected by the contract, so there is no field to name.

## Why a kept row fits the composition contract

The schema does not read the rows: resolved.document is typed as a bare object and deferred to verify_frozen_portfolio
(RequestComposition.schema.json:766). validate_bindings (reports/request_composition.py:26-264) reads owner, sources,
input_ref and browser, never the rows. The rows are accepted because freeze_template_portfolio itself emits them
(KEPT at portfolio.py:600-608, UNRESOLVED at 591-594), so the step-5 rebuild reproduces them.

## Proposal (NOT applied)

No change is needed to admit (A) or (B) on HEAD. The next measurement is the live resident journal line
`COMPOSITION-REFUSED step=<n> error_class=<Class>` (printed at composition_admission.py:63) for the 5C request id.
The 5B log did not match it. Only measured fact: the five composition-relevant files are identical at pin C
2a3aaa2815 and HEAD (`git diff --quiet`, rc 0), so the live code path is the one replicated, unless the deployed
release predates pin C (not measured; no AWS).

## Limits

- Owner: the test world's FIRM_ADVISOR fixture (firm 49financial, advisor "one"). The 5B receipt shows a 49financial
  advisor principal ("A2 advisor ok"), the same class, not compared field by field.
- The baseline artifact_ref.artifact_id and retention_ref.retention_id still name the baseline artifact; validate
  does not read them. input_ref.sha256, content_sha256, input_id, byte_length and browser.input_id are re-derived.
- The product's test world is reached through pytest's FixtureFunctionDefinition._get_wrapped_function (a pytest
  internal). Filed as surprise IRPT_ANLREQ-D2-W316-S2.
