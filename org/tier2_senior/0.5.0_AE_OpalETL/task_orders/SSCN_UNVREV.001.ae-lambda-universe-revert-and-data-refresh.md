<task_order>
  <metadata>
    <id>SSCN_UNVREV.001</id>
    <slug>ae-lambda-universe-revert-and-data-refresh</slug>
    <issued_by>0.3.0_DE_TradingOperations</issued_by>
    <issued_to>0.5.0_AE_OpalETL</issued_to>
    <date>2026-05-21</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>DISPATCHED 2026-05-21. Andrew-direct: Andrew brought 0.5.0_AE_OpalETL online "to assist as needed in the cloud" for this Security Scanner update and ruled (AskUserQuestion 2026-05-21) to REVERT the SSCN_DIVDEF v0.2 universe migration. The GO is this dispatch — begin immediately. COO/CTO are CC'd for project-state + doc coherence (the SSCN_DIVDEF v0.2 universe contract is being reversed); that notification does not gate your start.</dispatch_unblock_condition>
    <project_code>SSCN_UNVREV</project_code>
    <priority>P1 — Yang feedback on the live Security Scanner page; the portal-side universe revert (DE lane) lands in parallel and the PROD push bundles both.</priority>
  </metadata>

  <background>
Yang sent a refreshed FactSet screening export for the Security Scanner:
`Screening_DIVZ_IDVZ_20260519.xlsx` (on Andrew's machine at
`C:\Users\AndrewBerman\Downloads\Screening_DIVZ_IDVZ_20260519.xlsx`).

DE validated the file against the Lambda contract (pandas `read_excel(header=4)`,
2,707 rows x 335 cols, headers clean — the "dated columns" defect Yang apologised
for is fixed). **However the file carries the LEGACY 6-set universe-weight columns,
not the v0.2 5-set:**

| In the file | NOT in the file |
|-------------|-----------------|
| `wt_ivv`, `wt_iwb`, `wt_iwd`, `wt_acwx`, `wt_efa`, `wt_efv` | `wt_iwr`, `wt_ijh`, `wt_csus` |

SSCN_DIVDEF v0.2 (2026-05-19, Andrew-ratified) had migrated the page + Lambda to a
5 US-equity set (`sp500/r1000/rmidcap/sp400/msciusa`) on the strength of the
2026-05-18 export. The current ongoing feed (this 2026-05-19 file) empirically
carries the legacy mixed US/international/value columns. **New empirical state =>
Andrew ruled 2026-05-21: revert to the legacy 6-universe set.** This is the
post-revert contract:

| Portal ID | Source column | Label              | Country col |
|-----------|---------------|--------------------|-------------|
| `sp500`   | `wt_ivv`      | S&P 500            | hidden (US) |
| `r1000`   | `wt_iwb`      | Russell 1000       | hidden (US) |
| `r1000v`  | `wt_iwd`      | Russell 1000 Value | hidden (US) |
| `acwx`    | `wt_acwx`     | MSCI ACWI ex-US    | shown (intl)|
| `eafe`    | `wt_efa`      | MSCI EAFE          | shown (intl)|
| `eafev`   | `wt_efv`      | MSCI EAFE Value    | shown (intl)|

You already own this Lambda — `sscn_divdef_009_registry_regen_lambda_redeploy.md`
deployed `security-scanner-v1.1.3`. This TO reverses the `UNIVERSE_MAP` portion of
the v0.2 change and refreshes the data.
  </background>

  <scope>
Two deliverables, STRICTLY SEQUENCED (Part B must not run before Part A is live).

### Part A — Lambda UNIVERSE_MAP revert + redeploy

File: `infra/aws/lambda/opal_security_scanner_processor/lambda_function.py`

Revert `UNIVERSE_MAP` (currently lines ~46-53, the v0.2 5-set) to the legacy 6-set:

```python
UNIVERSE_MAP = {
    "sp500":  "wt_ivv",
    "r1000":  "wt_iwb",
    "r1000v": "wt_iwd",
    "acwx":   "wt_acwx",
    "eafe":   "wt_efa",
    "eafev":  "wt_efv",
}
```

- `NON_SCORING_COLS` already contains all six of `wt_ivv/wt_iwb/wt_iwd/wt_acwx/wt_efa/wt_efv`
  AND `wt_iwr/wt_ijh/wt_csus` — leave it unchanged (forward-compat; the three unused
  weight columns staying in the exclusion set is harmless and correct).
- Update any "5 universe" docstring/comment wording back to "6" (module docstring,
  `lambda_handler` docstring, the `NON_SCORING_COLS` "v0.2: new 5 + legacy 4" comment).
  Doc-only — no logic.
- Deploy via Terraform per CLAUDE.md Rules 1-2 + 6 + 18: build-and-upload.sh ->
  source-map update -> commit -> `.tools/safe-apply.sh` -> 0-diff verify -> tag.
- Tag: latest is `security-scanner-v1.1.3`. This is a universe-set contract change
  (a minor bump) — `security-scanner-v1.2.0`. Confirm with `git tag -l "security-scanner-v*" | sort -V | tail`.

### Part B — Data refresh (ONLY after Part A Lambda is live)

Upload Yang's file to the S3 prefix that triggers the processor:

```
aws s3 cp "/c/Users/AndrewBerman/Downloads/Screening_DIVZ_IDVZ_20260519.xlsx" \
  "s3://opal-data-portal-v2/security_scanner/uploads/20260519/Screening_DIVZ_IDVZ_20260519.xlsx"
```

Key shape is mandatory: the Lambda's `_KEY_RE` extracts `asOf` from
`security_scanner/uploads/{asOf}/...` — the `{asOf}` directory must be `20260519`
and the filename `Screening_DIVZ_IDVZ_20260519.xlsx`.

The ObjectCreated event fires `opal-security-scanner-processor`, which writes the
JSON artifacts to `s3://opal-data-portal-v2/json/security_scanner/latest/`.

Watch the Lambda CloudWatch logs for the run; confirm it loaded 2,707 rows and
emitted all six universes (it logs per-universe member counts).
  </scope>

  <sequencing>
A before B is non-negotiable. The S3 upload triggers whatever Lambda code is
currently deployed. If B runs while the v0.2 5-set `UNIVERSE_MAP` is still live,
the processor silently skips `r1000v/acwx/eafe/eafev` (no matching column) and
emits only `sp500/r1000` — a wasted run on a stale contract. Deploy Part A to a
verified 0-diff state, THEN upload in Part B.
  </sequencing>

  <acceptance_criteria>
- AC1: `UNIVERSE_MAP` in the deployed Lambda is the 6-entry legacy dict above.
- AC2: `terraform plan` shows 0-diff after apply; `security-scanner-v1.2.0` tagged
  and pushed with `--follow-tags`; `lambda-source-map.json` updated.
- AC3: The xlsx is present at
  `s3://opal-data-portal-v2/security_scanner/uploads/20260519/Screening_DIVZ_IDVZ_20260519.xlsx`.
- AC4: After the trigger run, all SIX of these exist and are freshly timestamped
  (today) — `aws s3 ls`:
  `s3://opal-data-portal-v2/json/security_scanner/latest/universes/{sp500,r1000,r1000v,acwx,eafe,eafev}/universe_data.json`
  and `.../scanner_data.json`, plus `.../latest/factor_metadata.json`.
- AC5: Spot-check one US universe (`sp500`) and one international (`acwx`)
  `universe_data.json`: non-empty `securities[]`, plausible counts (sp500 ~502 per
  the file's `wt_ivv` member count), and `acwx` rows carry a non-empty `country`.
- AC6: `scanner_data.json` rows include BOTH `values` and `pctls` objects populated
  (DE depends on `values` for the Universe Scanner "Percentiles + Raw" column toggle).
  </acceptance_criteria>

  <compiler_tools_mandate>
- Before edit: `comp-pipescript io` is gold-script-oriented and N/A for a Lambda;
  instead run `comp-iam service opal-security-scanner-processor` to confirm no IAM
  gap (no new boto3 call is added, so this should be clean — one sentence in the log).
- Before commit: `comp-iam gaps` only if `iam.tf` is touched (it should not be).
- After deploy: confirm `comp-pipescript deployed` N/A (Lambda, not a gold runner) —
  the 0-diff `terraform plan` is the deployed-state check. Note this in the log.
  </compiler_tools_mandate>

  <cross_domain_coordination>
- DE (`0.3.0_DE_TradingOperations`) lands the portal-side universe revert in parallel
  (`security-scanner.ts` `UNIVERSE_IDS`, `types.ts` `UniverseId`, `constants.ts`
  `US_ONLY_UNIVERSES`) on portal DEV. No shared files — portal vs Lambda are disjoint
  trees. The only ordering coupling is at PROD: the portal must not reach PROD before
  AC4 (the 6 universes exist in S3) or 4 universes render empty/404. DT bundles the
  portal PROD push after this TO's AC4 + Andrew's DEV smoke.
- RAVC: report back to DE (`0.3.0_DE_TradingOperations`) with evidence — tag,
  0-diff plan output, `aws s3 ls` of the 6 universes, and the per-universe member
  counts from the Lambda log. CC `2.0.0_SA_COO`.
  </cross_domain_coordination>

  <deliverables>
1. Reverted + redeployed Lambda (`security-scanner-v1.2.0`).
2. Refreshed S3 JSON artifacts for all 6 universes.
3. Session log with the Compiler Tools section.
4. RAVC2 to DE (CC COO) with AC1-AC6 evidence.
  </deliverables>
</task_order>
