<task_order>
  <metadata>
    <id>ADHC_CRYPCT.001</id>
    <slug>ds-comprehensive-crypto-removal-news-pipeline</slug>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.1.0_DS_MarketIntelligence</issued_to>
    <date>2026-05-19</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <!-- COMPLETE -- status flip 2026-05-22 by 0.1.0_DS_MarketIntelligence, CTO-authorized (1.0.0_SA_CTO). Work delivered 2026-05-19: 4-layer comprehensive crypto removal + the 5th surface (backfill_from_layer2) caught in verification and hotfixed; v2.9.8/2.9.9/2.9.10 deployed; +1h end-to-end verification PASS; CTO RAVC ratified. The pending flag was stale (un-flipped since delivery). Ship-attestation re-confirmed per CTO belt-and-suspenders step: git tag news-v2.9.10 EXISTS; Lambda opal-news-layer3-curation LastModified 2026-05-19T17:01:56Z (runtime agrees with the v2.9.10 deploy log). ADHC_CRYPCT.002 stays cancelled (Andrew vetoed v2.9.11; +24h residual ruled acceptable). -->

    <dispatch_unblock_condition>DISPATCHED via Andrew-direct CTO authorization 2026-05-19 ~14:35Z (verbatim: "we need to get rid of any and all crypto news sources from the news scanner process. i thought i already fixed this with 0.1.0_DS [...] but we're still seeing crypto news dominating. Please investigate and write a TO to 0.1.0_DS under ADHC"). No upstream gates -- start on receipt.</dispatch_unblock_condition>
    <project_code>ADHC_CRYPCT</project_code>
    <priority>P1 -- Andrew-direct: crypto news still dominating despite the 2026-05-12 fix `c72c9368a`. Defense-in-depth gap: prior fix cut INGESTION + added SOURCE BLOCKLIST + RECENCY FLOOR, but DID NOT remove crypto from the RANKING / NORMALIZATION / PROMPTING layers. Non-blocked sources (TechCrunch, Bloomberg, Reuters, Yahoo Finance, MarketWatch, CNBC) all cover crypto stories which still flow through Layer 2 -> Layer 3, get normalized into `crypto`/`bitcoin` keyword buckets, and are explicitly prompted as preferred portal keywords. Comprehensive removal at all 4 layers required.</priority>
    <sla>~3-4h wall -- enumerated edits across 2-3 Lambdas + GPT prompt refactor + post-deploy monitor + brief. No new resources, no IAM changes.</sla>
  </metadata>

  <references>
    <prior_fix>2026-05-12 commit `c72c9368a` "fix(news): recency-dominant trending + cut crypto sources" (DS author). Session log `org/tier2_senior/0.1.0_DS_MarketIntelligence/logs/2026-05-12/mkov_trends_recency_crypto_cut.md`. DevOps brief `docs/briefs/devops-brief-mkov-trending-recency-crypto-cut.md`. That fix succeeded at the source-ingestion layer but the structural enablement of crypto in the ranking + GPT prompt layers was explicitly out-of-scope.</prior_fix>
    <ingestion_lambda>infra/aws/lambda/news_ingestion_scheduler/lambda_function.py -- `RSS_FEEDS` (line 37). 5 crypto feeds REMOVED 2026-05-12 (line 65-68 comment). VERIFIED still clean. No action needed at this Lambda unless audit surfaces a new crypto-prefixed feed snuck in.</ingestion_lambda>
    <layer3_lambda>infra/aws/lambda/news_layer3_curation/lambda_function.py -- the primary target. Surviving crypto-enablement vectors per CTO audit 2026-05-19:
      - `TOP_20_KEYWORDS` (line 164): includes `'bitcoin', 'crypto'` -- portal word cloud explicitly features these
      - `KEYWORD_NORMALIZATION` (line 196-201): MAPS `'btc' -> 'bitcoin'`, `'cryptocurrency' -> 'crypto'`, `'coinbase' -> 'crypto'`, `'ethereum' -> 'crypto'` -- actively LIFTS crypto signal from broader inputs into the prescribed bucket
      - `BLOCKED_SOURCES` (line 420): only 6 crypto-only publications; only fires at >50% threshold (`BLOCKED_SOURCE_THRESHOLD`)
      - GPT prompt "PORTAL KEYWORD PREFERENCE" (~line 1373): includes `bitcoin, crypto` in the preferred-keyword list shown to the model
      - GPT prompt "Topics about stocks, crypto, Fed policy..." (~line 1467): explicitly invites crypto coverage
      - `CRYPTO_KEYWORDS = {'bitcoin', 'crypto'}` (line 1936): drives the CRYPTO_CAP rule that allows ONE crypto in top-3 (cap, not ban)
      - "ANTI-CONCENTRATION RULE" guidance in GPT prompt (~line 1265-1268): assumes multiple crypto topics in pool, just caps at one</layer3_lambda>
    <layer2_lambda>infra/aws/lambda/news_trending_analysis/lambda_function.py -- surviving crypto vector at line 207-208: example sectors/assets list still includes "crypto", "bitcoin" as a category. May also need clustering-level filter; investigation step.</layer2_lambda>
  </references>

  <context>
    Andrew's 2026-05-12 directive (verbatim, from prior session log): "let's get rid of all these crypto publications, we're all tired of the crypto news nobody gives a fuck we're a large cap macro firm." The 2026-05-12 fix delivered the SOURCE-LEVEL cut (RSS feeds removed) plus a 50%-source-dominance blocklist and a recency floor. That worked for ELIMINATING crypto-only-publication-dominated clusters. It did NOT eliminate crypto as a topic class because:
    (a) Non-crypto-publication sources (TechCrunch, Bloomberg, Reuters, Yahoo Finance, MarketWatch, CNBC, BBC, Financial Times) all cover crypto news -- those stories pass the source blocklist (under 50% from blocked-only sources)
    (b) The KEYWORD_NORMALIZATION map ACTIVELY routes 'btc' / 'cryptocurrency' / 'coinbase' / 'ethereum' INTO the `crypto`/`bitcoin` original_keyword bucket -- LIFTING signal, not suppressing
    (c) TOP_20_KEYWORDS prescribes bitcoin + crypto as portal-preferred keywords, and the GPT prompt features them explicitly
    (d) The CRYPTO_CAP allows one crypto topic in top-3 by design

    Andrew's 2026-05-19 directive (verbatim): "we need to get rid of any and all crypto news sources from the news scanner process [...] we're still seeing crypto news dominating." The plain reading: ZERO crypto in the trending output. Not "minimize crypto exposure" -- zero. This TO tears out crypto presence at all layers, replacing the cap-at-one CRYPTO_CAP semantics with a hard-drop-at-prefilter pattern.
  </context>

  <scope>
    <in_scope>
      **Layer 3 (news_layer3_curation) -- primary surface, comprehensive crypto removal:**
      - Remove `'bitcoin'` and `'crypto'` from `TOP_20_KEYWORDS` (line 164). Portal word cloud loses two entries; cosmetic side effect acceptable. (Coordinate w/ DE 0.1.0_DE_MarketIntelligence on the word-cloud rendering if any consumer assumes exactly 20 entries.)
      - Remove crypto entries from `KEYWORD_NORMALIZATION` (line 196-201): drop the entire `# Crypto variants` block. Letting `'btc'`, `'cryptocurrency'`, `'coinbase'`, `'ethereum'` pass through as raw means they hit no `original_keyword` bucket and are treated as low-priority topics -- no lift into crypto categorization.
      - Extend `BLOCKED_SOURCES` (line 420) materially. Add (at minimum): `'bloomberg crypto'`, `'yahoo crypto'`, `'marketwatch crypto'`, `'cnbc crypto'`, `'forbes crypto'`, `'fortune crypto'`, `'reuters crypto'`, `'ft crypto'`, `'ft alphaville crypto'`, `'wsj crypto'`. Empirical extension: DS scan the last 7 days of `opal-news-trending-daily` DynamoDB for crypto-tagged articles and add any source publishing 3+ crypto stories in that window. Lower `BLOCKED_SOURCE_THRESHOLD` from 0.5 to 0.3 (any meaningful crypto-source presence drops the topic).
      - **Replace CRYPTO_CAP with CRYPTO_BAN.** The existing `CRYPTO_KEYWORDS = {'bitcoin', 'crypto'}` cap rule (line 1936) caps at 1; change to a HARD-DROP filter at prefilter (same shape as `PREFILTER_RECENCY_FLOOR`): if `original_keyword in CRYPTO_KEYWORDS` -> drop entirely, never reach GPT. Rename constant to `BANNED_KEYWORDS` for semantic clarity. Add a positive content-level filter: drop topics where >X% of sample-article headlines match a CRYPTO_RAW_PATTERN regex (bitcoin|btc|crypto|cryptocurrency|coinbase|ethereum|eth|stablecoin|defi|nft|web3|altcoin|memecoin|coin\b) even if `original_keyword` differs. Threshold suggestion: X=40% -- DS final-tunes against the 7-day DynamoDB scan.
      - **GPT prompt scrub:** strip ALL crypto references from the prompt. Specifically:
        * "PORTAL KEYWORD PREFERENCE (for original_keyword): ai, war, tech, ~~bitcoin, crypto,~~ trump, fed, nvidia, china, energy, jobs, euro, retail, oil, inflation, google, consumer, nasdaq" -- remove the two crypto entries.
        * "Topics about stocks, ~~crypto,~~ Fed policy, trade, companies, commodities, economic data, geopolitics with market impact - SELECT THEM ALL" -- remove `crypto`.
        * "ANTI-CONCENTRATION RULE" guidance referencing "two crypto topics" or "two bitcoin topics" -- rewrite generically without crypto exemplars.
        * Add an explicit instruction line: "EXCLUSION: ignore all topics about cryptocurrency, bitcoin, ethereum, stablecoins, DeFi, NFTs, web3, or crypto exchanges. These are out-of-scope for this large-cap macro firm. If a topic is cryptocurrency-related, do not select it for either direction."

      **Layer 2 (news_trending_analysis) -- defense in depth:**
      - Audit for any clustering-level crypto bias. The line 207-208 comment lists "crypto", "bitcoin", "tech stocks" as example sectors/assets; rewrite to remove crypto example. Confirm no clustering-step crypto-keyword PREFERENCE (e.g., a `tfidf` boost on crypto terms) -- if found, rip out.
      - Optional reinforcement: in `calculate_quality_score`'s quality_map, add an ANTI-quality entry for any source consistently publishing crypto-dominated content (negative quality_score effectively suppresses the cluster). Discretionary; only if needed to deal with the residual non-blocklisted-source crypto leak.

      **Empirical 7-day audit BEFORE editing code:**
      - Pull `opal-news-trending-daily` DynamoDB scan for the last 7 days
      - Identify every cluster where `original_keyword` was bitcoin/crypto OR where >40% of article headlines match the CRYPTO_RAW_PATTERN
      - Enumerate the source distribution: which sources are still pushing crypto into the pipeline despite the May 12 blocklist
      - This drives the BLOCKED_SOURCES extension list (empirical, not speculative)
      - Document in the brief as Phase 0 evidence

      **Deploy + verify:**
      - Coordinate with 0.1.0_DT_MarketIntelligence for `news-pipeline` deploy as `news-v2.9.9` (or whatever next-version per MEMORY.md tag-versioning rule: `git tag -l "news-v*" | sort -V | tail -5`)
      - Post-deploy: monitor `opal-news-layer3-curation` CloudWatch for the next 3 invocation cycles. Confirm:
        * New `BLOCKED: CRYPTO:` log lines fire (or whatever the new banned-keyword log line is named)
        * Zero crypto-tagged topics in `bullish_top_3` or `bearish_top_3` outputs
        * Portal word-cloud renders cleanly (DE 0.1.0_DE coordination on the 18-instead-of-20 keyword consequence)
      - 24-hour follow-up: re-check live portal +trending output, screenshot evidence for the brief

      **Brief:**
      - `docs/briefs/adhc-crypct-comprehensive-crypto-removal-20260519.md` with:
        * Phase 0 7-day DynamoDB audit findings (source distribution + bullish/bearish examples that survived May 12)
        * Per-Lambda edit summary with line citations
        * BLOCKED_SOURCES additions list (with the empirical 7-day audit anchors)
        * GPT prompt diff (before/after)
        * Post-deploy 3-cycle log verification + 24h portal screenshot
        * Verdict: "ZERO crypto-tagged topics observed in trending output over verification window"
    </in_scope>
    <out_of_scope>
      - Modifying Layer 1 ingestion to add new RSS feeds. The May 12 cut held; no re-adding.
      - Touching the FinBERT scoring model itself.
      - Touching `data_contract.xml` for shapes already published (consumer-side change OK only if word cloud renders break).
      - Touching `semantic-news-layer3-curation` (inactive per May 12 log; defer to its reactivation).
      - Rate-limiting or quota-changing any AWS resources.
      - Modifying the portal frontend rendering. If word-cloud needs adjustment for 18 vs 20 keywords, coordinate with DE 0.1.0_DE_MarketIntelligence via MCP, do not edit portal directly.
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
    <phase id="0" when="empirical 7-day audit before edits">
      <step>
        <run>aws dynamodb scan --table-name opal-news-trending-daily --filter-expression "begins_with(date, :prefix)" --expression-attribute-values '{":prefix":{"S":"2026-05-1"}}' --projection-expression "topic_keyword,sample_articles,#d,trending_score" --expression-attribute-names '{"#d":"date"}' --max-items 1000</run>
        <expect>The last ~7-10 days of trending output. Identify crypto-tagged clusters by `topic_keyword` OR by article headlines matching crypto patterns. Report source distribution + count of crypto-leaking-sources NOT yet in BLOCKED_SOURCES.</expect>
        <if_mismatch>If the table/filter shape differs from prior session's queries, adjust + document. If scan-permission denied, surface to AE 0.5/0.6 for IAM check.</if_mismatch>
      </step>
      <step>
        <run>aws s3 cp s3://opal-data-news/news_trending_results/LATEST/result.json - | jq '.bullish_top_3[].sample_articles[].source, .bearish_top_3[].sample_articles[].source' | sort -u</run>
        <expect>The current set of sources represented in the live top-3 output. Cross-reference vs the May 12 BLOCKED_SOURCES to identify new offenders.</expect>
        <if_mismatch>If S3 key path has shifted (news-v2.x deploy may have renamed), grep `infra/aws/lambda/news_layer3_curation/lambda_function.py` for the OUTPUT_KEY constant and use that.</if_mismatch>
      </step>
    </phase>
    <phase id="1" when="before commit">
      <step>
        <run>python -m py_compile infra/aws/lambda/news_layer3_curation/lambda_function.py infra/aws/lambda/news_trending_analysis/lambda_function.py</run>
        <expect>Both Lambdas compile clean.</expect>
        <if_mismatch>Fix syntax before commit.</if_mismatch>
      </step>
      <step>
        <run>.tools/ds-precommit-check.py infra/aws/lambda/news_layer3_curation/lambda_function.py</run>
        <expect>Exit 0 (Class-A pre-commit gate per CLAUDE.md Rule 14).</expect>
        <if_mismatch>Fix surfaced issue before commit.</if_mismatch>
      </step>
      <step>
        <run>ruff check --target-version py39 infra/aws/lambda/news_layer3_curation/lambda_function.py infra/aws/lambda/news_trending_analysis/lambda_function.py</run>
        <expect>"All checks passed".</expect>
        <if_mismatch>Fix the linter issue. Use ruff 0.15.11.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="after deploy">
      <step>
        <run>aws logs tail /aws/lambda/opal-news-layer3-curation --since 30m --filter-pattern "BLOCKED:"</run>
        <expect>New `BLOCKED: CRYPTO:` or `BLOCKED: BANNED_KEYWORD:` log lines fire on the next invocation cycle. If invocation cycle hasn't fired yet, wait for next cron + re-run.</expect>
        <if_mismatch>If no BLOCKED-CRYPTO lines fire AND crypto topics still appear in output, the filter logic is not landing -- debug the prefilter flow before declaring done.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>The Lambda fix affects only future invocations. Historical `opal-news-trending-daily` entries may still carry crypto-tagged topics (acceptable: they're aged-out by the recency floor + the curation step only consumes recent). The S3 `news_trending_results/LATEST` is overwritten by the next cron fire -- post-deploy verification waits one cycle. No silver/bronze touched. No backfill required.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    - 0.1.0_DT_MarketIntelligence: deploy coordination via DevOps brief, same pattern as the May 12 `c72c9368a` -> `news-v2.9.8` cycle. New tag `news-v2.9.9` or per memory tag-versioning rule.
    - 0.1.0_DE_MarketIntelligence: portal word-cloud renders 20 keywords; this TO drops to 18. Coordinate via MCP whether word-cloud accepts the shorter list or needs a default-keyword substitution. If they need replacement keywords, suggest two from the existing `KEYWORD_NORMALIZATION` map (e.g., add `'apple', 'tesla'` as direct mappings to fill the slots) -- DE makes the call, not DS.
    - No AE involvement (no IAM, no resource changes, no terraform). Standard Lambda code-only deploy via the news-pipeline DevOps flow.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">7-day DynamoDB + S3 audit Phase 0 evidence in the brief: source distribution table of crypto-leaking sources (those publishing crypto stories that survived the May 12 BLOCKED_SOURCES + RECENCY_FLOOR filters); 5+ specific bullish_top_3 or bearish_top_3 examples from the last 7 days demonstrating the leak; BLOCKED_SOURCES extension list anchored to this empirical evidence.</ac>
    <ac id="AC2">`news_layer3_curation/lambda_function.py` edits: TOP_20_KEYWORDS no longer contains bitcoin/crypto; KEYWORD_NORMALIZATION no longer maps anything to crypto/bitcoin; BLOCKED_SOURCES extended per AC1 with BLOCKED_SOURCE_THRESHOLD reduced to 0.3; CRYPTO_KEYWORDS renamed to BANNED_KEYWORDS and converted from CAP to hard-drop-at-prefilter; new CRYPTO_RAW_PATTERN regex + content-level filter implemented.</ac>
    <ac id="AC3">GPT prompt scrub: zero references to bitcoin, crypto, cryptocurrency, ethereum, defi, nft, web3 anywhere in the prompt text. New explicit EXCLUSION instruction line added per scope §in_scope. Prompt diff in the brief.</ac>
    <ac id="AC4">`news_trending_analysis/lambda_function.py` audit: any clustering-level crypto bias removed (line 207-208 sector example + any tfidf/keyword boost on crypto terms). Diff in the brief.</ac>
    <ac id="AC5">Pre-commit gates (py_compile + ds-precommit + ruff py39) all exit 0. CLAUDE.md Rule 14 compliance.</ac>
    <ac id="AC6">DevOps brief authored at `docs/briefs/devops-brief-adhc-crypct-deploy-20260519.md` mirroring the May 12 pattern. DT 0.1.0_DT_MarketIntelligence deploys to `news-v{next}` per memory tag-versioning rule (`git tag -l "news-v*" | sort -V | tail -5` BEFORE picking the next tag).</ac>
    <ac id="AC7">Post-deploy verification: 3-invocation-cycle CloudWatch log inspection showing new BLOCKED: CRYPTO lines firing + zero crypto topics in bullish_top_3/bearish_top_3 outputs. 24-hour follow-up confirming portal trending display carries zero crypto stories. Both pieces of evidence in the brief with screenshots and log snippets.</ac>
    <ac id="AC8">Finding brief committed at `docs/briefs/adhc-crypct-comprehensive-crypto-removal-20260519.md` containing AC1 audit, AC2-AC4 edit diffs, AC5 gate evidence, AC6 deploy evidence, AC7 verification evidence, and the verdict statement: "ZERO crypto-tagged topics observed in trending output over the verification window."</ac>
    <ac id="AC9">Session log under `org/tier2_senior/0.1.0_DS_MarketIntelligence/logs/2026-05-19/` with Compiler Tools section. RAVC2 to 1.0.0_SA_CTO (Andrew-direct routing).</ac>
  </acceptance_criteria>

  <deliverables>
    - `docs/briefs/adhc-crypct-comprehensive-crypto-removal-20260519.md` -- the audit + edits + verification finding brief.
    - `docs/briefs/devops-brief-adhc-crypct-deploy-20260519.md` -- DT deploy instructions (mirror the May 12 DevOps-brief shape).
    - Lambda edits committed: `news_layer3_curation/lambda_function.py`, `news_trending_analysis/lambda_function.py` (and `news_ingestion_scheduler/lambda_function.py` only if Phase 0 audit surfaces a new crypto feed snuck in since May 12).
    - Tag `news-v{next}` after deploy per memory rule (DT-driven).
    - Session log under org/tier2_senior/0.1.0_DS_MarketIntelligence/logs/2026-05-19/ with Compiler Tools section.
    - RAVC2 to 1.0.0_SA_CTO (Andrew-direct).
  </deliverables>
</task_order>
