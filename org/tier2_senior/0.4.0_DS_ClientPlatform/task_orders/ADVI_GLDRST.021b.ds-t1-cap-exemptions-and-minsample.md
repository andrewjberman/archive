<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-10-v2-cap-exemptions-minsample</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-10</date>
    <status>complete</status>
    <project_code>ADVI_GLDRST</project_code>
  </metadata>

  <objective>
    Stop the T1 outlier cap in `build_canonical_prices_v2.py` from silently rewriting legitimate prices. Add two narrowly-scoped exclusions to the cap logic so the 8 genuine 2024-08-07 BD corruption cases remain caught while the 6 currently-false-positive assets (2 regime shifts + 4 thinly-traded collective-trust-style assets) are left alone. Exclusions: (1) an explicit `_T1_CAP_EXEMPTIONS` frozenset for named regime-shift assets, and (2) a `MIN_OBSERVATIONS_FOR_CAP = 15` sample-size threshold below which the cap does not apply. Verified via a re-run of the diff-before-ship harness from .021, which must show exactly 23 rows newly un-capped (13 regime-shift + 10 sparse-pollution) and exactly 8 rows still capped (all 2024-08-07 corruption), with zero other changes.
  </objective>

  <context>
    ADVI_GLDRST.021 shipped a `transaction_observed_capped` source tag on any row the 50x lifetime-median cap rewrites. The diff-before-ship harness (`data/analysis/v2_cap_tag_diff.py`) surfaced 31 capped rows across 14 assets. An audit of all 14 assets was then requested via `docs/briefs/data-scientist-t1-cap-audit.md` and delivered as `docs/briefs/data-scientist-t1-cap-audit-findings.md`. Read the findings doc in full before starting — every classification in this TO depends on its evidence lines.

    **Audit result summary:**

    | Classification | Assets | Rows | Keep capped? |
    |---|---|---:|---|
    | LEGITIMATE — regime shift (stock split / reverse split) | CHIPOTLE MEXICAN GRILL INC COM (50:1 split 2024-06-26), PRAXIS PRECISION MEDICINES INC COM NEW (1:15 reverse split 2023-11-29 + late-2025 runup) | 13 | **No** — explicit exemption |
    | LEGITIMATE — sparse history polluted by synthetic $1.00 entries | VANGUARD INSTL 500 IDX TRST GM, VANGUARD INSTL TOTAL BD ID GM, RED ROCK RESORTS INC CL A, VANGUARD EXPLORER FUND GM | 10 | **No** — auto-exempt via min-observation guard |
    | CORRUPTION — 2024-08-07 BD file error | INVESCO STABLE VALUE RET CL 1, DODGE & COX INCOME X, NORTHERN TRST COLL EAFE IDX T3, NORTHERN TRUST S&P 500 TIER 3, NT AGG BOND INDEX DC NL TIER 3, PGIM JENNISON SMALL COMPANY R6, VANGUARD BALANCED INDEX I, VANGUARD EMERGING MKTS STOCK IDX INSTL | 8 | **Yes** — cap working as intended |
    | **Total** | 14 | 31 |  |

    **Why two mechanisms and not one:**

    The regime-shift cases (CMG, PRAX) have **plenty of observations** — CMG has 36 daily T1 dates, PRAX has ~78. They trip the cap because the asset's historical median is legitimately the post-shift value and pre-shift observations look like outliers. A sample-size guard would not catch them; only an explicit exemption does.

    The sparse-pollution cases (Vanguard GM trusts, RRR, Explorer) have **very few observations** — 3, 5, 9, and 9 daily T1 dates respectively. The problem is that BD records some transaction types (dividend reinvestments, income distributions, lot disposals) with `price = units × $1.00` synthetic pricing, and when those synthetic rows dominate a thinly-traded asset's history, the lifetime median collapses to $1.00. A sample-size guard of 15 catches all four of these cases cleanly without requiring anyone to name them individually, and it catches any future thinly-traded asset that hits the same pattern.

    **Why 15 specifically:**

    | Group | Observation counts | Min | Max |
    |---|---|---:|---:|
    | Sparse-pollution (auto-exempt target) | RRR=3, Explorer=5, Vanguard 500 GM=9, Vanguard Bond GM=9 | 3 | 9 |
    | Corruption (must stay capped) | EAFE=30, Northern S&P=31, NT Bond=31, PJSQX=33, DOXIX=34, VBAIX=34, INVESCO=41, VEMIX=51 | **30** | 51 |
    | Regime-shift (explicit exemption) | CMG=36, PRAX~78 | 36 | ~78 |

    Any threshold between 10 and 29 cleanly separates sparse-pollution from corruption. 15 sits in the middle with comfortable margin on both sides (6-point cushion above the largest sparse case, 15-point cushion below the smallest corruption case). Do not parameterize this as a configurable knob — the threshold choice is data-driven and justified by the audit; keeping it as a module constant makes the rationale discoverable in the code.

    **Expected diff result:**

    Before 021b: 31 rows carry `source='transaction_observed_capped'` across 14 assets.
    After 021b:  8 rows carry `source='transaction_observed_capped'` across 8 assets (all on 2024-08-07).
    Delta: 23 rows drop from the capped set, 0 rows added, 0 price values changed on the remaining 8.

    If the diff shows any other number, stop and investigate before committing.

    **Andrew's decision (2026-04-10):** ship the combined fix (exemption list + min-observation guard) in a single commit. The VANGUARD EXPLORER FUND GM ambiguous case from the audit resolves automatically via the min-observation guard (5 observations < 15), so no individual judgment call is needed. Scoring the four follow-ups the audit recommended: #1 (min-observation guard) ships in this TO; #2 (filter synthetic $1.00 entries from the median) defers as a better-but-riskier long-term root-cause fix; #3 (PRAX "NEW"-suffix history truncation) defers because the exemption handles the immediate symptom; #4 (audit the 2024-08-07 BD file at source) is a separate open item not in DS scope, flagged for Andrew to decide whether to request BD to resend the extract.
  </context>

  <compiler_tools_mandate>
    Phase 1 (before writing):
    - `comp-blast data/black_diamond/scripts/silver/build_canonical_prices_v2.py` — confirm the blast radius hasn't changed since .021 (same consumers: A_03, B_01, E_00, E_05, E_06, E_14, bd-price-update).
    - Re-read `build_canonical_prices_v2.py:182-210` (the T1 build block including .021's source-tag additions) to confirm you understand exactly where the cap is applied and how `source` gets set.
    - Read `docs/briefs/data-scientist-t1-cap-audit-findings.md` per-asset sections for CMG, PRAX, and the 4 sparse-pollution cases. Verify the exact BD `asset_name` strings you will use in the exemption set (case and spacing must match BD's raw values — the findings doc used the audit output directly so the strings there are authoritative).

    Phase 2 (before committing):
    - Dry-run the modified v2 against current silver/transactions using the existing diff harness at `data/analysis/v2_cap_tag_diff.py` (extend it or copy-adapt it — whatever is cleanest). The harness must be able to compare "021 shipped state" vs "021b candidate state" and report row-level deltas.
    - `python -m py_compile data/black_diamond/scripts/silver/build_canonical_prices_v2.py` — syntax clean.
    - Verify the diff result matches the expected outcome table in `<acceptance_criteria>` #3 exactly. Any deviation is a STOP-SHIP signal.

    Phase 3 (after committing):
    - `comp-blast data/black_diamond/scripts/silver/build_canonical_prices_v2.py` again — confirm no blast-radius drift vs Phase 1. Same set of consumers expected.
    - Log both Phase 1 and Phase 3 outputs in the session log Compiler Tools section.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <none/>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. **`_T1_CAP_EXEMPTIONS` frozenset added** at module scope in `data/black_diamond/scripts/silver/build_canonical_prices_v2.py`, above the `build_t1_prices` function. Contents, exact:
       ```python
       _T1_CAP_EXEMPTIONS: frozenset[str] = frozenset({
           'CHIPOTLE MEXICAN GRILL INC COM',           # 50:1 split 2024-06-26 (yfinance confirmed)
           'PRAXIS PRECISION MEDICINES INC COM NEW',   # 1:15 reverse split 2023-11-29 + late-2025 runup (yfinance confirmed)
       })
       ```
       Do NOT add any other assets. The four sparse-pollution cases are handled by the min-observation guard, not this list.

    2. **`MIN_OBSERVATIONS_FOR_CAP` constant added** at module scope near `_T1_CAP_EXEMPTIONS`, value `15`, with a comment citing the audit findings doc and the observation-count table from the `<context>` section.

    3. **Cap-application logic modified** at `build_canonical_prices_v2.py:189-210` (the block containing the 50x cap introduced by earlier commits and the `transaction_observed_capped` tag from .021). The new logic must:
       - Compute `asset_n_obs = t1.groupby('asset_name').size()` (count of daily T1 observations per asset)
       - Join `asset_n_obs` onto `t1` as a per-row column
       - Build a `should_cap_mask` that is True ONLY when all three conditions hold:
         (a) the row's price exceeds 50x the asset's historical median (existing 50x check), AND
         (b) the asset is NOT in `_T1_CAP_EXEMPTIONS`, AND
         (c) the asset has >= `MIN_OBSERVATIONS_FOR_CAP` daily T1 observations
       - Apply the rewrite (both the price replacement and the `capped` bool flag from .021) only on rows where `should_cap_mask` is True.
       - The `transaction_observed_capped` source tag from .021 continues to propagate through `resolve_prices_for_asset`. No changes to the resolve function.

    4. **Diff-before-ship re-run.** Run the updated diff harness against current production transactions. Expected outcome **exactly**:

       | Metric | Before 021b | After 021b | Delta |
       |---|---:|---:|---:|
       | Rows tagged `transaction_observed_capped` | 31 | 8 | -23 |
       | Distinct assets with any capped row | 14 | 8 | -6 |
       | CMG rows capped | 4 | 0 | -4 |
       | PRAX rows capped | 9 | 0 | -9 |
       | Vanguard 500 GM rows capped | 4 | 0 | -4 |
       | Vanguard Bond GM rows capped | 4 | 0 | -4 |
       | RRR rows capped | 1 | 0 | -1 |
       | Vanguard Explorer GM rows capped | 1 | 0 | -1 |
       | Rows for the 8 corruption assets | 8 | 8 | 0 |
       | Any price value change on corruption-group rows | N/A | 0 | 0 |

       If any number differs from this table, STOP and investigate before committing. Most likely causes of deviation: BD asset_name string mismatch (check case, whitespace, punctuation), logic error in the min-observation count (check whether you're counting rows in the pre-cap DataFrame or post-cap DataFrame — must be pre-cap), or a join-on-index bug.

    5. **Regression check: 2024-08-07 corruption cases still caught.** All 8 assets listed in the context section's "CORRUPTION" row must still have their 2024-08-07 row tagged `transaction_observed_capped` in the post-021b output. Specifically verify INVESCO STABLE VALUE RET CL 1 (the canonical example Andrew wrote the cap for) is still caught.

    6. **Diff result documented in the session log** with the exact numeric table from #4, a list of the 23 newly-uncapped rows (asset, date, pre-cap price, what source tag they now have — should be plain `transaction_observed`), and confirmation that the 8 corruption rows are unchanged.

    7. **Commit follows the standard DS cycle.** `git status` clean, `--author=0.4.0_DS_ClientPlatform`, push to CLOUD, `aws s3 cp data/black_diamond/scripts/silver/build_canonical_prices_v2.py s3://opal-data-bd/code/silver/build_canonical_prices_v2.py`, verify etag equals local md5. **Do NOT trigger the runner or invoke bd-price-update.** The nightly schedule is still not in place (that's ADVI_GLDRST.022), so this upload is pure staging.

    8. **Session log** at `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-04-{DD}/` with: the commit SHA, the S3 etag, the diff result table, the 23-row drop-out list, the 8-row regression confirmation, the compiler tools Phase 1 and Phase 3 outputs, and a Next Steps block noting that ADVI_GLDRST.022 can now proceed.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/silver/build_canonical_prices_v2.py</file>
      <file action="modify or create">data/analysis/v2_cap_tag_diff.py (extend to compare pre-021b vs post-021b, or create a sibling diff script — your call)</file>
      <file action="reference">docs/briefs/data-scientist-t1-cap-audit-findings.md</file>
      <file action="reference">docs/briefs/data-scientist-t1-cap-audit.md</file>
      <file action="reference">org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-04-10/gold_trigger_chain_trace_and_d00c_role_split_fix.md</file>
      <file action="reference">org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/ADVI_GLDRST.021.ds-v2-source-tag-and-diff.md</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">ADVI_GLDRST.021 MUST be complete (it is — commit 9b4f7a77, source-tag shipped, diff harness in place). Verify the `transaction_observed_capped` tag is already live before starting.</requirement>
    <requirement id="2">Do NOT change the 50x threshold. Do NOT change the cap replacement value (still asset historical median). Do NOT touch the within-day collapse at line 183-184. The only behavioral changes permitted are the two new exclusions (named exemption + min-observation guard).</requirement>
    <requirement id="3">Do NOT parameterize `MIN_OBSERVATIONS_FOR_CAP` as an environment variable, CLI flag, or constructor arg. It's a module constant with a data-driven rationale documented in the code comment. Keep it stable and discoverable.</requirement>
    <requirement id="4">Do NOT add any assets to `_T1_CAP_EXEMPTIONS` beyond CMG and PRAX. The audit explicitly classified the other 4 sparse-pollution assets as auto-exempt via the observation guard. Naming them in the exemption list is redundant and makes the list stale-prone.</requirement>
    <requirement id="5">The diff-before-ship in acceptance criterion #4 is mandatory and the expected numbers are specified exactly. Do NOT ship if any number differs. A deviation indicates either a logic bug or an asset_name string mismatch — both must be investigated and resolved before commit.</requirement>
    <requirement id="6">Do NOT invoke bd-gold-trigger, bd-price-update, or any Lambda. Do NOT start the gold runner. This TO is pure code staging like .021 was.</requirement>
    <requirement id="7">Do NOT implement the audit's follow-up #2 (filter synthetic $1.00 entries from the median). That is a deferred root-cause fix, explicitly out of scope for 021b. If you notice a clean way to implement it while working on 021b, log it as a Next Step in the session log and move on.</requirement>
    <requirement id="8">Do NOT implement the audit's follow-up #3 (PRAX pre-split history truncation). Also deferred. The explicit PRAX exemption handles the immediate symptom.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">One commit on CLOUD modifying `build_canonical_prices_v2.py` with the exemption frozenset, the min-observation constant, and the updated cap-application logic. Optionally includes the diff harness extension. `--author=0.4.0_DS_ClientPlatform`.</deliverable>
    <deliverable type="s3_upload">`s3://opal-data-bd/code/silver/build_canonical_prices_v2.py` with etag matching local md5.</deliverable>
    <deliverable type="document">Diff-before-ship result table in the session log matching the expected outcome in acceptance criterion #4. Must include the 23-row drop-out enumeration.</deliverable>
    <deliverable type="document">Session log with Compiler Tools section (Phase 1 + Phase 3 outputs), the commit SHA, the S3 etag, and the Next Steps block unblocking ADVI_GLDRST.022.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT modify the 50x threshold, the replacement value (asset historical median), or the within-day collapse median at line 183-184. All frozen.</rule>
    <rule>Do NOT add assets to `_T1_CAP_EXEMPTIONS` beyond CMG and PRAX. The other 4 audit-identified legitimate cases are handled by `MIN_OBSERVATIONS_FOR_CAP`.</rule>
    <rule>Do NOT parameterize `MIN_OBSERVATIONS_FOR_CAP`. Keep it as a module constant with inline rationale.</rule>
    <rule>Do NOT ship if the diff-before-ship numbers don't match the expected table exactly. Investigate the deviation first.</rule>
    <rule>Do NOT implement audit follow-ups #2, #3, or #4 in this TO. All deferred.</rule>
    <rule>Do NOT trigger the gold runner or any Lambda. Code staging only.</rule>
    <rule>Do NOT move v2 into code/gold/. That belongs to ADVI_GLDRST.022.</rule>
    <rule>Do NOT mark ADVI_GLDRST.022's status as anything other than `staged` in this TO. .022 unblocks when 021b is complete, but the flip happens there, not here.</rule>
  </do_not>
</task_order>
