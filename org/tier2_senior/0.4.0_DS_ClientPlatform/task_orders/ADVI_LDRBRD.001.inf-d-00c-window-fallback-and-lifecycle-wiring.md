<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_LDRBRD.001</id>
    <project>ADVI_LDRBRD</project>
    <title>INF_D_00c MAX window fallback (Bug A) + accounts_v2_dim lifecycle wiring (Bug C) — surfaced post AUDIT-003a chain re-fire</title>
    <issued_to>0.4.0_DS_ClientPlatform~D</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-05</issued_date>
    <status>complete</status><!-- CLOSED 20260506T~1340Z by COO session 59. D5 artifact generated_at 2026-05-06T13:37:08Z (SSM on 6e49f2694). Commits: 0755a2330 (LDRBRD.001 original fix) + 46d55bc51 (Bug C2 dtype) + 6e49f2694 (Bug A2 0.0 psa_map default + Bug C2b). AC1 PASS: individual advisors peter_lee/patrick_scanlan/joe_brandenburg all 0.0 in YTD+MAX (pre-onboarding); firm aggregate inflection_wealth_management period_start_aua=None is expected (firm path constructed separately at L867; not in all_advisors set). AC2 PASS: lifecycle_aua non-zero for all 4 entries across QTD/YTD/MAX. AC3/AC4/AC5/AC6 PASS. DS~C RAVC5 CLOSE 20260506T133750Z. Dashboard v10 patch (advisor_count=4 + $182.5M discrepancy investigation) ongoing separately as DS~D follow-on — NOT gating this close. Bug A2 follow-on TO (psa 0.0 for firm aggregate) is low-priority future scope. -->
    <priority>high</priority>
    <estimated_effort>~30-45 min total (pre-authored already + ship cycle + D4 chain re-fire); already 80% complete</estimated_effort>
  </metadata>

  <references>
    <ref type="audit_evidence">DS~D Phase 0 audit MCP 20260505T203035Z — full 3-bug trace (A: MAX window, B: YTD data gap, C: lifecycle wiring) + QTD% expected-distortion analysis</ref>
    <ref type="empirical_trigger">DS~C RAVC5 PARTIAL FAIL on RPBKTPI.001 AC4: leaderboard.json post D2d showed MAX/YTD all None + lifecycle_aua zeros. Mechanical RPBKTPI.001 fix correct; persisting nulls = ADVI_LDRBRD scope.</ref>
    <ref type="cascade">Gates on D3 chain-full --from INF_B_00 RAVC5'' (~21:20-21:35Z). After this TO ships: D4 --from INF_D_00c (~10-15min wall) closes empirical AC4 + lifecycle_aua decomposition.</ref>
  </references>

  <context>
    DS~D's Phase 0 audit identified 3 distinct issues in `data/orion/scripts/gold/INF_D_00c.portal_leaderboard.py` causing leaderboard.json AC4 failures post AUDIT-003a fix:

    **Bug A (MAX period_start_aua always None):** `_aua_at_start()` iterates `reversed(holdings_*.parquet)` looking for latest date `<= window_start`. MAX window_start = pd.Timestamp('2000-01-01'). Holdings files start 2019-09-17. No file satisfies `d <= 2000-01-01` → `best_key = None` → returns empty DataFrame → all None.

    **Bug B (YTD period_start_aua always None):** Same function. YTD window_start = 2026-01-01. holdings_2025-12-31.parquet exists but Inflection was onboarded AFTER 2025-12-31 — no Inflection rows. Same fallback as Bug A would give "earliest-available AUA" semantic. **DS~C semantic ratify needed before fixing — DEFERRED to follow-on TO.**

    **Bug C (lifecycle_aua all zeros):** `_compute_hh_lifecycle()` guard requires `accounts_v2_dim` with `first_trade_date` column. Currently:
    - Not loaded in main() (~L892-897)
    - Not passed to `compute_leaderboard_entries()` (no accounts_v2_dim param)
    - Not forwarded to `_compute_hh_lifecycle()` calls (L727 + L806)
    Result: `use_v2=False` + `'first_trade_date' not in accounts_dim.columns` → returns empty DataFrame → lifecycle_aua stays {nmnc:0, nmec:0, existing:0}.

    **QTD absurd %** (peter +4213%, patrick +7638%): EXPECTED data distortion (mid-onboarding period; Inflection accounts coming online during Q2 2026). Not a code bug. UI guard candidate — DE/RD scope, separate.

    Pre-authoring already complete in DS~D's working tree per RAVC 20260505T203620Z. ds-commit-gate clean. Sprint ship-ready on D3 trigger.
  </context>

  <phase id="1" when="before commit (already mostly complete per pre-authoring)">
    <step>
      <run>Verify pre-authored fixes in working tree: `git diff data/orion/scripts/gold/INF_D_00c.portal_leaderboard.py | head -100`</run>
      <expect>7 surgical edits visible:
- L101: `SILVER_API_ACCOUNTS_V2_PREFIX` constant
- L281-296: `load_accounts_v2_dim()` function
- L346-351: Bug A fallback (`best_key = keys[0]` when None + log WARN)
- compute_leaderboard_entries() signature: `accounts_v2_dim=None` param
- L727 + L806: forward `accounts_v2_dim` to `_compute_hh_lifecycle()`
- main() L897: `accounts_v2_dim = load_accounts_v2_dim()`
- main() call site: `accounts_v2_dim=accounts_v2_dim` passed</expect>
      <if_mismatch>If pre-authoring drifted: re-apply per audit doc; re-run gate.</if_mismatch>
    </step>
    <step>
      <run>.tools/ds-commit-gate.sh data/orion/scripts/gold/INF_D_00c.portal_leaderboard.py</run>
      <expect>Exit 0 — all checks passed (already verified clean per RAVC 20260505T203620Z)</expect>
      <if_mismatch>Re-run gate after addressing surfaced issue.</if_mismatch>
    </step>
  </phase>

  <phase id="2" when="ship sequence on D3 RAVC5'' trigger">
    <step>
      <run>.tools/safe-commit.sh --author "0.4.0_DS_ClientPlatform_D &lt;0.4.0_DS_ClientPlatform_D@opal.agent&gt;" -m "feat(ADVI_LDRBRD.001): INF_D_00c MAX window fallback (Bug A) + accounts_v2_dim lifecycle wiring (Bug C)" -- data/orion/scripts/gold/INF_D_00c.portal_leaderboard.py</run>
      <expect>safe-commit PASS; pathspec scoped + index clean; commit hash returned</expect>
      <if_mismatch>safe-commit abort: clean staged extras with `git reset HEAD -- &lt;path&gt;`; re-run.</if_mismatch>
    </step>
    <step>
      <run>git push origin CLOUD</run>
      <expect>Push succeeds; commit on origin/CLOUD</expect>
      <if_mismatch>If push fails: `git pull --rebase origin CLOUD` + retry.</if_mismatch>
    </step>
    <step>
      <run>aws s3 cp data/orion/scripts/gold/INF_D_00c.portal_leaderboard.py s3://opal-data-inf/code/gold/</run>
      <expect>S3 upload successful; new ETag</expect>
      <if_mismatch>Re-run S3 cp.</if_mismatch>
    </step>
    <step>
      <run>comp-pipescript deployed INF_D_00c</run>
      <expect>MATCH — runner has updated script</expect>
      <if_mismatch>STALE → re-upload until MATCH.</if_mismatch>
    </step>
  </phase>

  <phase id="3" when="after ship — RAVC3 to COO + AE 0.7 D4 dispatch trigger">
    <step>
      <run>RAVC3 MCP to 2.0.0_SA_COO + 0.7.0_AE_CloudOps with: commit hash + push confirmation + S3 ETag + comp-pipescript MATCH evidence</run>
      <expect>AE 0.7 reads RAVC3 → fires D4 --from INF_D_00c on inf-gold-layer-runner with heartbeat + auto-shutdown suppression per their 7th ops finding</expect>
      <if_mismatch>If AE 0.7 unresponsive within 10 min of RAVC3: ping COO; pinch-hit path remains available.</if_mismatch>
    </step>
  </phase>

  <phase id="4" when="post D4 — empirical verification + RAVC5 close">
    <step>
      <run>aws s3 cp s3://opal-data-inf/platinum/firm/leaderboard.json - | jq '.windows | to_entries[] | {window: .key, advisors: (.value.entries | map({advisor_id, period_start_aua, aua_growth_pct, lifecycle_aua}))}'</run>
      <expect>
- All 4 advisors in QTD/YTD/MAX windows
- Bug A verifier: MAX window period_start_aua non-null per advisor (using earliest-available holdings as fallback baseline)
- Bug C verifier: lifecycle_aua decomposition non-zero where expected
- joe_brandenburg appears in all 3 windows
- (Bug B may still show YTD nulls — DS~C semantic call deferred)
      </expect>
      <if_mismatch>Empirical mismatch: investigate deeper; surface to COO.</if_mismatch>
    </step>
    <step>
      <run>RAVC5 close MCP to 2.0.0_SA_COO with: commit hash + S3 verify + D4 SSM CommandId + leaderboard.json empirical evidence (per-window per-advisor table)</run>
      <expect>RAVC5 delivered. ADVI_LDRBRD.001 ready for COO close.</expect>
      <if_mismatch>If empirical PARTIAL (e.g., Bug A passes but Bug C still zero): document + escalate semantic question to COO.</if_mismatch>
    </step>
  </phase>

  <cross_domain_coordination>
    <coord>**Gates on D3 chain-full --from INF_B_00 RAVC5''** (AE 0.7; ETA ~21:20-21:35Z). Don't ship before D3 RAVC; chain re-fire requires fresh canonical_holdings + performance silver from D3.</coord>
    <coord>**AE 0.7 fires D4 --from INF_D_00c** post DS~D RAVC3. ~10-15 min wall. AE 0.7's auto-shutdown suppression workaround required (heartbeat + `shutdown -c` post-fire OR guard file pattern).</coord>
    <coord>**DS~A v10 patch routing** opens post D4 RAVC5 (~22:00-22:15Z). DS~A holds v10 in working tree; routes to CTO + DT same-turn.</coord>
    <coord>**DS~C semantic ratify on Bug B (YTD fallback)** — separate follow-on TO if Bug B still empirically nulls post-D4. NOT this TO's scope.</coord>
    <coord>**RD comprehensive Playwright sweep** fires post v10 patch land + DT submodule bump. Final empirical close ~22:15-22:30Z.</coord>
  </cross_domain_coordination>

  <data_reprocess_scope>
    <reprocess_required>
      <reason>Bug A + Bug C are gold-tier compute logic fixes. INF_D_00c re-emits leaderboard.json + dependent platinum/firm/ + platinum/advisors/ artifacts when D4 fires. Gold/canonical/ not affected (already correct from D3).</reason>
      <s3_prefix_globs>
        <glob>s3://opal-data-inf/platinum/firm/leaderboard.json (re-emit by INF_D_00c)</glob>
        <glob>s3://opal-data-inf/platinum/advisors/*/summary.json (downstream consumers via D-chain)</glob>
        <glob>s3://opal-data-inf/platinum/firm/dashboard.json (INF_09 re-run; downstream of leaderboard updates)</glob>
      </s3_prefix_globs>
      <verification>aws s3 ls each prefix post-D4; LastModified > D4 fire timestamp; leaderboard.json window per-advisor empirical pass per Phase 4 Step 1.</verification>
      <downstream_consumer_freshness_gate>Portal FE reads platinum/firm/leaderboard.json + platinum/firm/dashboard.json directly; no Lambda layer in path (per DE state-of-affairs doc §2). Fresh artifacts visible to RD sweep immediately on chain re-fire RAVC.</downstream_consumer_freshness_gate>
    </reprocess_required>
  </data_reprocess_scope>

  <compiler_tools_mandate>
    <phase id="1" when="before commit">
      <step>
        <run>.tools/ds-commit-gate.sh data/orion/scripts/gold/INF_D_00c.portal_leaderboard.py</run>
        <expect>Exit 0 (already verified per pre-authoring RAVC)</expect>
        <if_mismatch>Fix per gate output</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="post S3 upload">
      <step>
        <run>comp-pipescript deployed INF_D_00c</run>
        <expect>MATCH</expect>
        <if_mismatch>STALE → re-upload</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="post D4 chain">
      <step>
        <run>aws s3 ls s3://opal-data-inf/platinum/firm/leaderboard.json + jq query per Phase 4 Step 1</run>
        <expect>Empirical verifier per Bug A + Bug C expected outputs</expect>
        <if_mismatch>Per Phase 4 if_mismatch</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <criterion id="AC1">Bug A fix: leaderboard.json MAX window period_start_aua non-null per advisor (using earliest-available holdings as fallback baseline; values may be small but non-None).</criterion>
    <criterion id="AC2">Bug C fix: leaderboard.json lifecycle_aua decomposition non-zero per advisor where expected (joe_brandenburg + peter_lee + patrick_scanlan have first_trade_date in accounts_v2; lifecycle_aua splits should populate).</criterion>
    <criterion id="AC3">comp-pipescript deployed INF_D_00c MATCH post-S3-upload.</criterion>
    <criterion id="AC4">D4 chain --from INF_D_00c completes cleanly; leaderboard.json LastModified > D4 fire timestamp.</criterion>
    <criterion id="AC5">RAVC5 close package: commit hash + S3 verify + D4 SSM CommandId + per-window per-advisor leaderboard empirical table.</criterion>
    <criterion id="AC6">Bug B (YTD nulls) status: documented as still-pending per DS~C semantic ratify; NOT a blocker for this TO close.</criterion>
  </acceptance_criteria>

  <go_signal>
    <issued_at>2026-05-05T20:36:00Z (sprint dispatch per Andrew override)</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>GO. Pre-authoring complete + ds-commit-gate clean per RAVC 20260505T203620Z. Ship on D3 RAVC5'' trigger (~21:20-21:35Z). Phase 4 empirical AC1+AC2 verifier post D4 chain.</message>
  </go_signal>
</task_order>
