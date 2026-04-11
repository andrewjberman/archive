<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-10-v2-source-tag</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-10</date>
    <status>staged</status>
    <project_code>ADVI_GLDRST</project_code>
  </metadata>

  <objective>
    Make the T1 outlier cap in build_canonical_prices_v2.py auditable without changing its behavior. Add a `transaction_observed_capped` source tag on any row the 50x lifetime-median cap rewrites, document the known tradeoff inline, and run a production diff-before-ship to confirm the tag correctly marks the same rows the cap has historically been rewriting silently. This TO is scoped narrowly to v2 itself; the gold-runner integration and scheduling work is in a separate TO (ADVI_GLDRST.022).
  </objective>

  <context>
    The T1 price aggregation in `data/black_diamond/scripts/silver/build_canonical_prices_v2.py:182-204` has two medians doing different jobs:

    1. **Within-day collapse** (line 183-184): `groupby(['asset_name', 'trade_date'])['obs_price'].median()`. Collapses multiple same-day observations of the same asset into a single daily T1 price. This is an unavoidable aggregation primitive — needs *some* function, median is a robust default for the rare cases where same-day observations disagree. **Stays as-is.**

    2. **Lifetime asset-median outlier cap** (lines 189-204): computes each asset's historical median across all dates, then caps any day's T1 price that exceeds 50x that asset's historical median by rewriting it to the historical median. The in-line comment cites the 2024-08-07 collective trust incident (price=$60K / MV=-$3.6B for a $1.00 stable value fund) as the motivating case. **Stays as-is for defensive purposes.**

    The problem we're solving: the cap is currently **silent**. It writes a print statement listing the first 10 capped rows per run, then overwrites every capped row in the output parquet with `source='transaction_observed'` indistinguishable from clean observations. Downstream consumers have no way to tell a capped row from an observed row. If a future regime shift (legitimate stock split, IPO pop, structured-product denomination change) trips the cap, the real price is silently rewritten and we only find out when something breaks downstream.

    Prior discussion: this session's log file `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-04-10/gold_trigger_chain_trace_and_d00c_role_split_fix.md` documents the full event chain upstream of the gold runner and the canonical_prices deprecation history. Andrew confirmed on 2026-04-10 that the 50x cap stays in place as a defensive safety net, but that the silent-rewrite property must be fixed. Source-tag approach is the minimal-change path that addresses the audit problem without altering cap behavior.

    Known tradeoff being accepted: legitimate 50x+ regime shifts will still be silently smoothed in the numeric output. The source tag makes them detectable by any downstream consumer that filters on source, but does not automatically protect them. If this bites us later, the fix is to add a per-asset exception rather than loosening the global threshold.
  </context>

  <compiler_tools_mandate>
    Phase 1 (before writing): `comp-blast data/black_diamond/scripts/silver/build_canonical_prices_v2.py` to surface every consumer of canonical_prices.parquet and flag any script that filters on `source`. Expected blast targets include A_03.positions_cube, B_00.canonical_holdings, B_01.holdings_lots, and the E-series pricing diagnostics. Confirm none of them will break if a new `transaction_observed_capped` value appears in the `source` column (i.e. they treat it as "not T1" or as a pass-through rather than raising on unexpected values).

    Phase 2 (before committing): re-read the resolve_prices_for_asset logic at lines 310-356 and confirm that rows tagged `transaction_observed_capped` still participate correctly in the T2/T3/T4 resolution (they should — the tag is additive, not a type change). Also run `python -m py_compile data/black_diamond/scripts/silver/build_canonical_prices_v2.py` before committing.

    Phase 3 (after committing): `comp-blast data/black_diamond/scripts/silver/build_canonical_prices_v2.py` again and diff against the Phase 1 output to confirm the blast radius has not expanded. Log both outputs in the session log Compiler Tools section.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <none/>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. `data/black_diamond/scripts/silver/build_canonical_prices_v2.py` at lines 189-204 includes a new `transaction_observed_capped` source-tag assignment on every row the outlier cap rewrites. The tag must propagate through the T2/T3/T4 resolution logic at lines 310-356 so the final `canonical_prices.parquet` `source` column carries the tag on exactly the capped rows.

    2. An inline comment above the cap block explicitly documents the tradeoff: "Known tradeoff: legitimate 50x+ regime shifts are silently rewritten. Flag with source='transaction_observed_capped' and review if downstream consumers surface unexpected smoothing."

    3. A diff-before-ship has been run against current production transactions:
       - Run 1: checkout current main / CLOUD, run `python data/black_diamond/scripts/silver/build_canonical_prices_v2.py --dry-run` and capture the output DataFrame (or write to a temp location and download).
       - Run 2: apply the source-tag change, run again against the same inputs, capture the output.
       - Compare the two outputs row-by-row. **Expected delta:** the only columns that should differ are `source` — rows that were previously `transaction_observed` but exceeded the 50x cap should now be `transaction_observed_capped`. **Every price value should be identical between the two runs.** If any price value differs, investigate before shipping.

    4. The diff result is documented in the session log with: total count of rows newly tagged `transaction_observed_capped`, count of distinct assets affected, the first 10 (asset_name, date, pre-cap implied price, post-cap written price) tuples, and confirmation that no price values changed between runs.

    5. The 2024-08-07 collective trust incident is verified to still be handled: grep the Run 2 output for rows where `date == '2024-08-07'` AND `asset_name` matches stable-value / collective-trust patterns, and confirm those rows are tagged `transaction_observed_capped`. This is the regression check — the original incident the cap was written for must still be caught.

    6. Commit follows the standard DS cycle: `git status` clean, `--author` set, push to CLOUD, `aws s3 cp` to `s3://opal-data-bd/code/silver/build_canonical_prices_v2.py`, verify etag matches local md5. **Do NOT trigger the gold runner or invoke bd-price-update.** v2 is not yet on the runner's sync path; the upload is just staging for ADVI_GLDRST.022.

    7. Session log written under `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-04-{DD}/` with the diff result table, the inline comment text, the commit SHA, the S3 etag, and the Compiler Tools section.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/silver/build_canonical_prices_v2.py</file>
      <file action="reference">data/black_diamond/scripts/gold/lib/exclusions.py</file>
      <file action="reference">infra/aws/lambda/bd-pipeline/bd-price-update/lambda_function.py</file>
      <file action="reference">org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-04-10/gold_trigger_chain_trace_and_d00c_role_split_fix.md</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Do NOT change the 50x threshold. Do NOT change the cap replacement value (still asset historical median). Do NOT touch the within-day collapse at line 183-184. The only behavioral change permitted is the source tag assignment.</requirement>
    <requirement id="2">The source tag must be written BEFORE the T2/T3/T4 resolution at line 310-356 runs, so downstream resolution can see the tag. Check that the resolve_prices_for_asset function does not overwrite source values when T1 is the winning tier — if it does, that's a separate bug to flag in the session log, and the tag should be preserved via a small modification.</requirement>
    <requirement id="3">The diff-before-ship in acceptance criterion #3 is mandatory. Do NOT commit without it. If the diff surfaces any price-value changes (not just source-column changes), stop and escalate to Andrew before committing — that would indicate the source-tag change accidentally altered cap behavior.</requirement>
    <requirement id="4">Upload to `s3://opal-data-bd/code/silver/` (NOT code/gold/). v2 lives in silver for now; ADVI_GLDRST.022 handles the code/gold/ relocation as part of the boot-integration work.</requirement>
    <requirement id="5">Do NOT invoke bd-gold-trigger, bd-price-update, or any Lambda. Do NOT start the gold runner. This TO is pure code staging.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">One commit on CLOUD modifying `build_canonical_prices_v2.py` with source tag + inline tradeoff comment, pushed with `--author=0.4.0_DS_ClientPlatform`.</deliverable>
    <deliverable type="s3_upload">`s3://opal-data-bd/code/silver/build_canonical_prices_v2.py` with etag matching local md5.</deliverable>
    <deliverable type="document">Diff-before-ship result table in session log: total capped rows, distinct assets, first 10 capped (asset, date, price) tuples, 2024-08-07 regression check result.</deliverable>
    <deliverable type="document">Session log with Compiler Tools section (before / after comp-blast outputs).</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT delete, loosen, or tighten the 50x threshold.</rule>
    <rule>Do NOT replace the cap with a row-exclusion list. Andrew explicitly decided to keep the cap as-is on 2026-04-10.</rule>
    <rule>Do NOT touch the within-day collapse median at line 183-184.</rule>
    <rule>Do NOT skip the diff-before-ship. Any price value change between runs is a STOP-SHIP signal.</rule>
    <rule>Do NOT trigger the gold runner or any Lambda in this TO.</rule>
    <rule>Do NOT move v2 to code/gold/ in this TO. That belongs to ADVI_GLDRST.022.</rule>
  </do_not>
</task_order>
