<task_order>
  <metadata>
    <id>SSCN_UNVREV.002</id>
    <slug>ae-lambda-weight-fields-and-20260521-refresh</slug>
    <issued_by>0.3.0_DE_TradingOperations</issued_by>
    <issued_to>0.5.0_AE_OpalETL</issued_to>
    <date>2026-05-22</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <!-- GO 2026-05-22 (2.0.0_SA_COO -- exec commit+dispatch mechanics only). DE 0.3.0 authored; base COO committed into the 0.5.0_AE lane + GO'd because COO~B (the SSCN exec lane) is offline. Origin: Andrew-direct 2026-05-22 (Yang feedback). SSCN project-state + doc canonicalization remain COO~B's lane. -->
    <dispatch_unblock_condition>GO ON PICKUP -- committed + dispatched 2026-05-22 by 2.0.0_SA_COO (Andrew-direct origin). Execute Part A (Lambda change + deploy) -> verify 0-diff -> THEN Part B (data refresh upload). A-before-B is non-negotiable.</dispatch_unblock_condition>
    <project_code>SSCN_UNVREV</project_code>
    <priority>P1 — Yang feedback on the live Security Scanner; the portal-side column work (DE lane) is already on portal DEV (47330865 + 6f66c67f + 7786eef9) and renders the two new weight columns empty until this TO ships the data.</priority>
  </metadata>

  <background>
Yang asked (via Andrew, 2026-05-22) for two column additions to the Security
Scanner page:
- Universe Data tab: weight-of-universe + weight-of-DIVZ columns.
- Security Scanner tab: sector, industry group, weight-of-universe, weight-of-DIVZ.

DE has shipped the portal side to portal DEV (`7786eef9`): `UniverseDataRow`
gains `divzWeight`; `ScannerRow` gains `universeWeight` + `divzWeight`; the
columns render in both tabs. Sector / industry group / the Universe-Data-tab
universe weight already exist in the JSON contract and render now. **But
`divzWeight` (both tabs) and the Security-Scanner-tab `universeWeight` are NOT
emitted by `opal-security-scanner-processor`** — those columns render blank
until this TO ships.

Yang also supplied a new source file with the DIVZ weight column:
`Screening_DIVZ_IDVZ_20260521 (1).xlsx` (on Andrew's machine at
`C:\Users\AndrewBerman\Downloads\Screening_DIVZ_IDVZ_20260521 (1).xlsx`).

DE verified the file: 2,707 rows x 339 columns (the current 20260519 file is
335 cols). It carries **four new model-weight columns** the 20260519 file did
not: `wt_divz`, `wt_idvz`, `wt_pfde`, `wt_pfoe`. The legacy 6 universe-weight
columns and `sector_name` / `indgrp_name` / `dy_ntm` are all present.

Weight scale (DE check, sentinel-42 replaced with NaN): `wt_iwb` 1,002 members,
0.0001-7.57, sum ~100. `wt_divz` 25 members, 1.01-5.92 — DIVZ is a ~25-name
model, so `wt_divz` is null for the vast majority of securities (expected).
  </background>

  <scope>
Two deliverables, STRICTLY SEQUENCED (Part B must not run before Part A is live).

### Part A — Lambda: exclude the new weight columns + emit the weight fields

File: `infra/aws/lambda/opal_security_scanner_processor/lambda_function.py`

1. **`NON_SCORING_COLS`** — add the four new model-weight columns. Without this
   they fall through to `scoring_cols` (anything NOT in the set) and get
   percentile-ranked as if they were factors, AND pollute the factor list /
   `factor_metadata.json`. Add to the existing "Universe weight columns" block:

   ```python
   "wt_divz",  # DIVZ model weight  (Yang feedback SSCN_UNVREV.002)
   "wt_idvz",  # IDVZ model weight
   "wt_pfde",  # PFDE model weight
   "wt_pfoe",  # PFOE model weight
   ```

2. **`_build_universe_rows`** — add a `divzWeight` field to each emitted row:

   ```python
   "divzWeight": _to_json_value(row.get("wt_divz")),
   ```
   (place it immediately after the existing `"universeWeight"` line.)

3. **`_build_scanner_rows`** — currently emits no weight field. Add BOTH
   `universeWeight` (the selected-universe weight) and `divzWeight`. This
   requires threading `universe_col` into the function:
   - change the signature to `_build_scanner_rows(df_universe, scoring_cols, universe_col)`;
   - update the call site in `lambda_handler` to pass `universe_col`;
   - add to each emitted row (after `"industryGroup"`):
     ```python
     "universeWeight": _to_json_value(row.get(universe_col)),
     "divzWeight": _to_json_value(row.get("wt_divz")),
     ```

   Rationale for `universeWeight` = selected-universe weight (NOT a fixed
   `wt_iwb`): Andrew ruling 2026-05-22 — the column tracks whichever universe
   the dropdown has selected, matching the existing `UniverseDataRow.universeWeight`.

4. Deploy via Terraform per CLAUDE.md Rules 1-2 + 6 + 18: build-and-upload.sh ->
   commit -> `.tools/safe-apply.sh` -> 0-diff verify -> tag. No new boto3 call,
   no `iam.tf` change, no source-map change (existing function).
5. Tag: latest is `security-scanner-v1.2.0` (SSCN_UNVREV.001). This is a
   data-contract change (rows gain fields) — minor bump `security-scanner-v1.3.0`.
   Confirm with `git tag -l "security-scanner-v*" | sort -V | tail`.

### Part B — Data refresh with the new 20260521 file (ONLY after Part A is live)

Upload Yang's new file. **Rename on upload** — drop the browser " (1)" suffix;
the Lambda's `_KEY_RE` + filename convention require `Screening_DIVZ_IDVZ_{asOf}.xlsx`:

```
aws s3 cp "/c/Users/AndrewBerman/Downloads/Screening_DIVZ_IDVZ_20260521 (1).xlsx" \
  "s3://opal-data-portal-v2/security_scanner/uploads/20260521/Screening_DIVZ_IDVZ_20260521.xlsx"
```

The `{asOf}` directory must be `20260521` and the filename
`Screening_DIVZ_IDVZ_20260521.xlsx`. The ObjectCreated event fires the
processor, which regenerates the 6-universe JSON artifacts under
`s3://opal-data-portal-v2/json/security_scanner/latest/`.

Watch CloudWatch: confirm 2,707 rows x 339 cols loaded, 6 universes processed,
0 errors.
  </scope>

  <sequencing>
A before B is non-negotiable. Part B's upload triggers whatever Lambda code is
deployed. If B runs while the old v1.2.0 code is live, `wt_divz/wt_idvz/wt_pfde/
wt_pfoe` are treated as scoring factors — they get percentile-ranked and appear
in `factor_metadata.json` as bogus factors, and the new weight fields are not
emitted. Deploy Part A to verified 0-diff, THEN upload in Part B.
  </sequencing>

  <acceptance_criteria>
- AC1: Deployed Lambda `NON_SCORING_COLS` contains `wt_divz`, `wt_idvz`,
  `wt_pfde`, `wt_pfoe` (CodeSha256 byte-identical to the v1.3.0 artifact).
- AC2: `terraform plan` 0-diff after apply; `security-scanner-v1.3.0` tagged and
  pushed `--follow-tags`.
- AC3: xlsx present at
  `s3://opal-data-portal-v2/security_scanner/uploads/20260521/Screening_DIVZ_IDVZ_20260521.xlsx`.
- AC4: After the trigger run, every `universes/{id}/universe_data.json` row
  carries a `divzWeight` key, and every `scanner_data.json` row carries both
  `universeWeight` and `divzWeight` keys.
- AC5: Spot-check `r1000`: `scanner_data.json` rows have `universeWeight` > 0
  (members are weight-filtered). `divzWeight` is a number for the ~25 DIVZ
  holdings and `null` for the rest — confirm both a populated and a null case.
- AC6: `wt_divz/wt_idvz/wt_pfde/wt_pfoe` do NOT appear as factor codes in
  `factor_metadata.json` and are NOT keys in any row's `values`/`pctls` objects
  (confirms they were excluded from `scoring_cols`).
  </acceptance_criteria>

  <compiler_tools_mandate>
- Before edit: `comp-iam service opal-security-scanner-processor` — confirm no
  IAM gap (no new boto3 call; should be clean — one sentence in the log).
- Before commit: `comp-iam gaps` only if `iam.tf` is touched (it should not be).
- After deploy: `comp-pipescript deployed` N/A (Lambda, not a gold runner) — the
  0-diff `terraform plan` is the deployed-state check. Note this in the log.
  </compiler_tools_mandate>

  <cross_domain_coordination>
- DE (`0.3.0_DE_TradingOperations`) shipped the portal side to portal DEV
  (`7786eef9`): `UniverseDataRow.divzWeight`, `ScannerRow.universeWeight` +
  `ScannerRow.divzWeight`, and the columns in both tabs. No shared files —
  portal vs Lambda are disjoint trees. PROD coupling: the portal must not reach
  PROD before this TO's AC4 or the two weight columns render blank in PROD. DT
  bundles the portal PROD push after AC4 + Andrew's DEV smoke.
- `SSCN_DATA_CONTRACT.md` Section 5 (`UniverseDataRow` / `ScannerRow`) should
  gain the new fields. SSCN doc canonicalization is `2.0.0_SA_COO~B`'s lane —
  flag the contract delta to COO~B; do not block the deploy on the doc edit.
- RAVC: report back to DE (`0.3.0_DE_TradingOperations`) with evidence — tag,
  0-diff plan, `aws s3 ls` of the refreshed artifacts, and a divzWeight /
  universeWeight spot-check from one universe's JSON. CC `2.0.0_SA_COO`.
  </cross_domain_coordination>

  <deliverables>
1. Reverted-contract Lambda redeployed (`security-scanner-v1.3.0`).
2. Refreshed S3 JSON artifacts for all 6 universes from the 20260521 file.
3. Session log with the Compiler Tools section.
4. RAVC2 to DE (CC COO) with AC1-AC6 evidence.
  </deliverables>
</task_order>
