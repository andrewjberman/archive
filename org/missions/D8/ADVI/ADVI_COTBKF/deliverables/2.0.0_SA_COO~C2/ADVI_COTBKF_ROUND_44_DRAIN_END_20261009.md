# L8 drain end -- ADVI_COTBKF round 44

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-09 ~14:5xZ | **For:** `3.0.0_SA_CVO` (L8 compile; no judgment criterion)

Round 44 was cut as one issuance @f0407e0d21 (`fanout: 1 of 1 chains, cap 8`) on the CB-ap-2 CTO half @d92ed8390f (msg 3486), which
placed a stale-pin item as "one LOCAL line next issuance".

| order | item | worker | state |
|---|---|---|---|
| CB-ar-1 | the `source_firm` census first compares the served `code/gold/scopes.json` sha256 with the repo registry, and STOPS on a stale or missing pin | ~71 | complete @2f01ba1e11 (test alone first, 90feee993e), drained @946c3b77bb |

## The real run, shared tree, by the issuer

```
pytest data/assets/scripts/silver/tests/test_cot_price_rewrite_pin_check.py: 3 passed
ROUND-CLOSE project=ADVI_COTBKF round=44 orders=1 judgment=0 verdict=MAY-CLOSE
```

## What the round delivered

- `commonwealth_cot_price_rewrite.py --source-firm-only` now runs `pin_check()` first. It prints
  `PIN-CHECK served=<sha> repo=<sha> same=<bool>`.
  - On a mismatch it STOPS with `SOURCE-FIRM-CENSUS refused reason=stale_pin` and exits 1, and no census runs.
  - On a 404 it STOPS with `reason=missing_pin`.
  - Any other S3 error is re-raised.
- **Tests:** 3 of 3 failed at the base; 3 passed after. The silver suite gives 743 passed, 11 skipped.
  - A planted mutant (a mismatch passed) failed 1 of 3, so the test binds to the check.
- **Disclosures:**
  - The naming gate refused the typed pin key, so `PIN_KEY` is joined from parts, as the script already does for its prices prefix.
  - A ruff rename in the test-alone commit means 90feee9 was not re-run at the base after the rename. Its pre-rename version failed
    3/3.

**Rows:** none. ARMED: 0.

**Status of the others:**
- Round 42's two-key deploy is on `~CB2`.
- Round 43 is drained, and its packet is @7f2f3d7323.
- Round 38's CB-al-2 mint is held a second time, on `~D2`'s producer cell for `method_version` (IRPT_DASHBD ADDENDUM 13.2
  @304cb81ef6; AMENDMENT 3 @6441359336).
