<task_order>
  <metadata>
    <id>ADHC_CRYPCT.002</id>
    <slug>ds-residual-crypto-leak-dilution-and-article-scrub</slug>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.1.0_DS_MarketIntelligence</issued_to>
    <date>2026-05-20</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>ALREADY DISPATCHED. CTO 1.0.0_SA_CTO GO'd v2.9.11 directly to DS 0.1.0 (ADHC_CRYPCT is a CTO-direct, Andrew-authorized single-TO-origin project; DS had it fully scoped from the .001 +24h verification, needed only the architectural GO -- no decomposition). This TO file is the bookkeeping RECORD of that GO, authored base-lane by 2.0.0_SA_COO at CTO's request -- it is NOT a gate. DS is already executing. RAVC2 to 1.0.0_SA_CTO direct (Andrew-direct routing, same as .001).</dispatch_unblock_condition>
    <project_code>ADHC_CRYPCT</project_code>
    <priority>P1 -- Andrew-direct crypto-removal lineage. ADHC_CRYPCT.001's +24h verification (DS 0.1.0) found 2 residual crypto leak paths that survived the .001 comprehensive removal. This TO closes both.</priority>
    <sla>~1-2h wall -- 2 enumerated edits in a single Lambda + post-deploy monitor + +24h verification. No new resources, no IAM changes.</sla>
  </metadata>

  <references>
    <prior_to>ADHC_CRYPCT.001 (`org/tier2_senior/0.1.0_DS_MarketIntelligence/task_orders/ADHC_CRYPCT.001.ds-comprehensive-crypto-removal-news-pipeline.md`) -- comprehensive 4-layer crypto removal; shipped + deployed. Its +24h verification window surfaced the 2 residual leak paths this TO addresses.</prior_to>
    <target_lambda>infra/aws/lambda/news_layer3_curation/lambda_function.py -- both fixes are in this one file.
      - `_is_blocked_source_dominated` (L462) -- the ratio-gate function. A topic is dropped only when blocked-source articles exceed `BLOCKED_SOURCE_THRESHOLD` of the sample. A crypto topic whose DEFINING article is from a blocked source but whose sample is diluted by enough non-blocked articles passes the ratio gate -- the dilution bypass Fix #1 closes.
      - The topic/article-assembly path -- the function(s) that populate `top_articles` / `sample_articles` on output topic objects (~L1018-1046 build site + ~L1617-1624). On a KEPT topic, individual blocked-source / crypto-pattern articles still ride along in the article list -- Fix #2 scrubs them.</target_lambda>
    <ship>Deploys as `news-v2.9.11` (latest tag is `news-v2.9.10`; confirm with `git tag -l "news-v*" | sort -V | tail -5` before tagging). DT 0.1.0_DT_MarketIntelligence deploy via the news-pipeline DevOps-brief pattern (same as .001).</ship>
  </references>

  <context>
    ADHC_CRYPCT.001 tore crypto out at the ingestion / ranking / normalization / GPT-prompt layers and converted CRYPTO_CAP to a hard-drop-at-prefilter BANNED_KEYWORDS filter. Its +24h verification still observed crypto reaching trending output via 2 residual paths:

    1. **Ratio-gate dilution bypass.** `_is_blocked_source_dominated` (L462) drops a topic only when blocked-source articles exceed the threshold fraction of the sample. A crypto topic anchored on a blocked-source defining article but padded with enough non-blocked articles slips under the ratio and is KEPT.

    2. **Article-level leak on kept topics.** Even on a topic that is correctly KEPT, the `top_articles` / `sample_articles` list can still contain individual blocked-source or CRYPTO_RAW_PATTERN-matching articles -- the .001 work gated at the TOPIC level, not the ARTICLE level.

    CTO disposition (Andrew-authorized GO, 2026-05-20): 2 fixes, both in `news_layer3_curation/lambda_function.py`. CBDC was considered for a BANNED_KEYWORDS add and Andrew ruled NO (CBDC = monetary policy, in-scope for a macro firm) -- no keyword-list change in this TO.
  </context>

  <scope>
    <in_scope>
      **Fix #1 -- dilution-proof topic gate (defining-article anchor check).**
      Add a defining-article anchor check to the topic-gate path: if a topic's DEFINING article (the anchor/lead article of the cluster) is from a `BLOCKED_SOURCE`, DROP the topic regardless of the blocked-source ratio. This is a class fix for the ratio-gate dilution bypass -- it makes the anchor decisive, so dilution by non-blocked articles can no longer rescue a crypto-anchored cluster. Implement alongside (not replacing) the existing `_is_blocked_source_dominated` ratio gate -- the anchor check is an additional drop condition.

      **Fix #2 -- article-level scrub on kept topics.**
      On every topic that is KEPT, scrub the `top_articles` / `sample_articles` list: drop any individual article that is from a `BLOCKED_SOURCE` OR whose headline matches `CRYPTO_RAW_PATTERN` (the regex introduced in .001). The topic survives; the offending articles do not ride along in its article list.

      **Observability for Fix #1 (over-drop guard).**
      Log every topic that Fix #1 drops -- a distinct log line (e.g. `BLOCKED: CRYPTO-ANCHOR: <topic> defining-article source=<source>`) so the +24h verification can audit the Fix-#1 drop set and catch any OVER-drop (a legitimate non-crypto topic wrongly dropped because its defining article happened to be from a blocked source).

      **Deploy + verify.**
      - DT 0.1.0_DT_MarketIntelligence deploys `news-v2.9.11` via the news-pipeline DevOps-brief pattern.
      - Post-deploy: monitor `opal-news-layer3-curation` CloudWatch for the next 3 invocation cycles -- confirm Fix-#1 anchor-drop log lines fire and zero crypto topics/articles in `bullish_top_3` / `bearish_top_3`.
      - +24h verification before close: re-check live portal + trending output; audit the Fix-#1 drop-log set for over-drop; screenshot evidence.
    </in_scope>
    <out_of_scope>
      - No keyword-list change. CBDC stays OUT of BANNED_KEYWORDS (Andrew ruling 2026-05-20).
      - No change to Layer 1 ingestion, Layer 2 (`news_trending_analysis`), the FinBERT model, or the GPT prompt -- .001 covered those.
      - No portal-frontend edits.
      - No new AWS resources, no IAM, no Terraform.
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
    <phase id="0" when="before edits -- blast-radius discovery">
      <step>
        <run>comp-blast _is_blocked_source_dominated  (and comp-blast on the article-assembly fn name once located)</run>
        <expect>Cross-file consumers of the topic-gate + article-assembly paths. NOTE: these are Lambda-internal helpers and will likely NOT resolve as comp-graph nodes ("No nodes matching") -- the graph operates at cross-file/route/artifact granularity.</expect>
        <if_mismatch>If comp-blast returns no nodes (expected for intra-Lambda helpers), fall back to a grep call-site enumeration: `grep -n "_is_blocked_source_dominated" infra/aws/lambda/news_layer3_curation/lambda_function.py` (known call sites ~L628 / ~L989 / ~L1025) and locate every site that builds output topic objects with `sample_articles=`. That call-site set IS the blast radius for this intra-Lambda scope -- confirm Fix #1 lands at the topic gate and Fix #2 lands at every article-assembly site, none missed.</if_mismatch>
      </step>
    </phase>
    <phase id="1" when="before commit">
      <step>
        <run>python -m py_compile infra/aws/lambda/news_layer3_curation/lambda_function.py</run>
        <expect>Compiles clean.</expect>
        <if_mismatch>Fix syntax before commit.</if_mismatch>
      </step>
      <step>
        <run>.tools/ds-precommit-check.py infra/aws/lambda/news_layer3_curation/lambda_function.py</run>
        <expect>Exit 0 (Class-A pre-commit gate, CLAUDE.md Rule 14).</expect>
        <if_mismatch>Fix the surfaced issue before commit.</if_mismatch>
      </step>
      <step>
        <run>ruff check --target-version py39 infra/aws/lambda/news_layer3_curation/lambda_function.py</run>
        <expect>"All checks passed" (ruff 0.15.11).</expect>
        <if_mismatch>Fix the linter issue before commit.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="after deploy">
      <step>
        <run>aws logs tail /aws/lambda/opal-news-layer3-curation --since 30m --filter-pattern "BLOCKED:"</run>
        <expect>New Fix-#1 anchor-drop log lines (`BLOCKED: CRYPTO-ANCHOR:` or equivalent) fire on the next invocation cycle. If the cycle has not fired yet, wait for the next cron + re-run.</expect>
        <if_mismatch>If no anchor-drop lines fire AND crypto topics/articles still appear in output, the Fix #1/#2 logic is not landing -- debug before declaring done.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>Lambda code change affects only future invocations. `opal-news-trending-daily` historical entries age out via the recency floor; the `news_trending_results/LATEST` S3 object is overwritten by the next cron fire (post-deploy verification waits one cycle). No silver/bronze touched. No backfill required.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    Single Lambda file (`news_layer3_curation/lambda_function.py`), single pod (0.1 MarketIntelligence). No cross-domain S3/route overlap with other active TOs. 0.1.0_DT_MarketIntelligence handles the `news-v2.9.11` deploy via the news-pipeline DevOps-brief pattern (mirror of .001). No DE involvement -- no word-cloud / keyword-count consequence (no keyword-list change). No AE involvement (no IAM/Terraform/resource change).
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">Fix #1 implemented in `news_layer3_curation/lambda_function.py`: the topic gate drops any topic whose DEFINING article is from a BLOCKED_SOURCE, independent of the blocked-source ratio. The existing `_is_blocked_source_dominated` ratio gate is retained as an additional (not replaced) drop condition. Edit diff in the brief.</ac>
    <ac id="AC2">Fix #2 implemented: on every KEPT topic, the `top_articles`/`sample_articles` list has all BLOCKED_SOURCE articles and all CRYPTO_RAW_PATTERN-matching articles removed. Applied at every output-topic article-assembly site (none missed -- per the Phase-0 call-site enumeration). Edit diff in the brief.</ac>
    <ac id="AC3">Fix-#1 observability: every topic dropped by the anchor check emits a distinct log line identifying the topic + the defining-article source. The +24h verification audits this drop set for over-drop (legitimate non-crypto topics wrongly dropped) and reports the finding.</ac>
    <ac id="AC4">Pre-commit gates (py_compile + ds-precommit-check + ruff py39) all exit 0 -- CLAUDE.md Rule 14 compliance.</ac>
    <ac id="AC5">DT 0.1.0_DT_MarketIntelligence deploys `news-v2.9.11` (tag confirmed next-in-series via `git tag -l "news-v*" | sort -V | tail -5`). DevOps brief authored mirroring the .001 pattern.</ac>
    <ac id="AC6">Post-deploy verification: 3-invocation-cycle CloudWatch inspection showing Fix-#1 anchor-drop lines firing + zero crypto topics in bullish_top_3/bearish_top_3 AND zero crypto/blocked-source articles in any kept topic's article list. +24h follow-up confirming portal trending carries zero crypto, plus the Fix-#1 over-drop audit. Evidence (log snippets + screenshots) in the brief.</ac>
    <ac id="AC7">Finding brief committed at `docs/briefs/adhc-crypct-002-residual-leak-closure-20260520.md` containing the 2-fix edit diffs, AC4 gate evidence, AC5 deploy evidence, AC6 verification + over-drop audit, and the verdict: "ZERO crypto-tagged topics AND zero crypto/blocked-source articles observed in trending output over the +24h verification window."</ac>
    <ac id="AC8">Session log under `org/tier2_senior/0.1.0_DS_MarketIntelligence/logs/2026-05-20/` with a Compiler Tools section reproducing each Phase-0/1/2 `<run>` + observed result + pass/fail vs `<expect>`. RAVC2 to 1.0.0_SA_CTO (Andrew-direct routing).</ac>
  </acceptance_criteria>

  <deliverables>
    - `news_layer3_curation/lambda_function.py` edits committed (Fix #1 + Fix #2 + Fix-#1 observability logging).
    - `docs/briefs/adhc-crypct-002-residual-leak-closure-20260520.md` -- finding brief.
    - DevOps brief for the `news-v2.9.11` deploy (mirror the .001 DevOps-brief shape).
    - Tag `news-v2.9.11` after deploy (DT-driven, confirm series first).
    - Session log under `org/tier2_senior/0.1.0_DS_MarketIntelligence/logs/2026-05-20/` with Compiler Tools section.
    - RAVC2 to 1.0.0_SA_CTO (Andrew-direct).
  </deliverables>

  <do_not>
    <rule>Do NOT add CBDC (or any new keyword) to BANNED_KEYWORDS -- Andrew ruled NO 2026-05-20 (CBDC = monetary policy, in-scope).</rule>
    <rule>Do NOT replace the `_is_blocked_source_dominated` ratio gate -- Fix #1 is an ADDITIONAL drop condition alongside it.</rule>
    <rule>Do NOT touch Layer 1/2, the GPT prompt, or the FinBERT model -- .001 covered those; this TO is layer3 topic-gate + article-assembly only.</rule>
    <rule>No emojis in code, logs, the brief, or CLI transcripts (CLAUDE.md ASCII-only).</rule>
  </do_not>
</task_order>
