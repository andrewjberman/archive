# cottonwood_sources_entry -- ADVI_COTBKF CB-aq-1 (0.9.0_WK_ADVI_COTBKF~70)

Rule commit (entry + adapter, before the first rebuild): d41d82a633. NO S3 write, no deploy.

## The entry as added (data/assets/scripts/gold/irpt_reporting/sources.json, ONE object appended; nothing else in the file changed)

```json
"_commonwealth_delivery": {
  "registry_key": "z09",
  "valuation_source": "positions_x_as_traded_close",
  "fee_treatment": "net_of_fees",
  "price_basis": "as_traded",
  "entry_comment": "METHOD-FIELDS-ONLY ENTRY ... (comment string)"
}
```

No firm token (naming gate PASS); registry_key z09 resolves via lookup() to firm cottonwood (ard.firm_scope(entry) = cottonwood).
Values: the producer's method_fields() admits any non-empty string and has no closed vocabulary; its own test
(test_returns_method_fields.py::test_manifest_for_a_non_custodian_source_does_not_state_the_custodian_method) reads this exact triple.

## How the compute path skips it

The structural switch is the one declared_sources() already honours: a top-level key starting with "_" is not a custody source
(`not k.startswith("_")`). Printed: declared_sources = ['schwab_08335338']; source_entry(doc, '_commonwealth_delivery') REFUSES
("is not declared ... (declared: schwab_08335338)"); the producer's CLI default source and the reporting-gold handler
(`len(declared_sources) != 1` guard, then sources[0]) therefore see exactly one source as before. The adapter reads the entry
directly (doc["_commonwealth_delivery"]), refuses if declared_sources lists it, and passes it as emit_day(src=...).

## Tests

- producer: data/assets/scripts/gold/irpt_reporting/tests -> 102 passed, 2 warnings (before the rule commit and inside the run)
- reporting-gold handler: infra/aws/lambda/investor-reporting/reporting-gold/tests -> 86 passed

## One built manifest (.scratch/advi_cotbkf/ard_cottonwood_r43/date=2026-06-22/manifest.json, read back from disk)

valuation_source=positions_x_as_traded_close  fee_treatment=net_of_fees  price_basis=as_traded
method: r_t = (V_t - F_t) / V_(t-1) - 1; the valuation source, fee treatment and price basis are the declared fields ..., and no further method is stated for this source; daily returns link geometrically. GIPS-ALIGNED, not GIPS-compliant.
return_basis_census {"NOT_MEASURABLE": 9, "TWR": 3}. All 3,325 day manifests were read back: 0 of 9,975 method fields absent.
Per-file sha256 (data.parquet and manifest.json) and content hash: ard_cottonwood_manifest.json beside this file.
Note: that manifest's method_version is 2 (producer constant) while the rows carry NULL -- surprise row ADVI_COTBKF-D2-W70-S1.

ARD-COTTONWOOD-R43 days=3325 rows=1691729 return_basis_twr=107316 manifest_fields_absent=0 producer_tests=102
