<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFREL.003</id>
    <project>ADVI_INFREL</project>
    <title>clients_tab.json regen wiring (gates on TO-1 silver-chain fix)</title>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <secondary>0.6.1_AE_PartnerETL</secondary>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-05</issued_date>
    <status>staged</status><!-- Authored sprint mode 2026-05-05T~21:15Z. Gates on TO-1 silver-chain fix RAVC5 — if silver propagation is fixed, clients_tab.json may regenerate automatically (TO-3 closes without code change). Default receiver: DS lane (gold script authoring); AE 0.6.1 secondary if dispatch issue. -->
    <priority>medium</priority>
    <estimated_effort>~0.25d (small wiring fix OR auto-close if TO-1 fix propagates)</estimated_effort>
  </metadata>

  <references>
    <ref type="prd_canonical">docs/architecture/ADVI_INFREL.md v0.1; §4.3 + §6 TO-3</ref>
    <ref type="evidence_baseline">`gold/artifacts/clients_tab.json` LastModified 2026-04-29 (~6 days stale); other gold artifacts (dashboard.json, leaderboard.json, header_metrics.json) regenerate daily as part of chain</ref>
  </references>

  <context>
    `gold/artifacts/clients_tab.json` last regenerated 2026-04-29 (per S3 LastModified). Other artifacts in same prefix regenerate daily as part of standard chain runs. Three competing diagnoses:

    - **(a) Producer exists in chain but is being skipped** — chain script that writes `clients_tab.json` has a guard (e.g., conditional on a missing dim) that's been false since 2026-04-29.
    - **(b) Producer exists outside daily chain** — separate script/cadence; hasn't been triggered since 2026-04-29.
    - **(c) No producer in current chain** — artifact was hand-published one-off; no automated producer exists.

    Diagnosis path: post TO-1 silver-chain fix, observe whether clients_tab.json regenerates automatically. If yes → (a); diagnosis self-resolves. If no → identify producer; class (b) or (c); scope fix.
  </context>

  <phase id="0" when="Phase 0 — observe post TO-1 ship">
    <step>
      <run>Wait for TO-1 silver-chain fix RAVC5 + 24-48h empirical. Then poll `aws s3 ls s3://opal-data-inf/gold/artifacts/clients_tab.json` — does LastModified update post TO-1?</run>
      <expect>If LastModified updates → class (a); diagnosis self-resolves; TO-3 closes without code change. If LastModified stays stale → proceed to Phase 1 investigation.</expect>
      <if_mismatch>If TO-1 fix doesn't ship within 48h: re-poll cadence; do NOT block on TO-3 indefinitely.</if_mismatch>
    </step>
  </phase>

  <phase id="1" when="Phase 1 investigation — gates on Phase 0 (b)/(c) classification">
    <step>
      <run>Identify producer: `comp-pipescript` search for any gold script that writes `clients_tab.json`. Likely candidates: INF_D_*, INF_C_*, or one-off in tier2_senior.</run>
      <expect>Producer found OR confirmed absent</expect>
      <if_mismatch>If multiple candidates: investigate each; document which is intended primary.</if_mismatch>
    </step>
    <step>
      <run>If producer found (class b): why hasn't it run since 2026-04-29? Cron config? Manual-only? Wire into daily chain.</run>
      <expect>Producer wired into daily chain (D-chain entry OR separate cron)</expect>
      <if_mismatch>If wiring requires architectural change: surface to me + CTO before authoring</if_mismatch>
    </step>
    <step>
      <run>If no producer found (class c): author one. Source of canonical data: `silver/api_dims/accounts_v2/` (post TO-1 fix). Output schema: match existing clients_tab.json (LastModified 2026-04-29 partition). Wire into D-chain.</run>
      <expect>New producer authored + wired into D-chain</expect>
      <if_mismatch>If schema not derivable from existing artifact: surface to RD lane (frontend consumer of clients_tab.json) for canonical schema definition.</if_mismatch>
    </step>
  </phase>

  <phase id="2" when="Phase 2 — commit + ship">
    <step>
      <run>safe-commit.sh — gold script edit OR chain wiring change. ds-commit-gate.sh per CLAUDE.md rule 14.</run>
      <expect>Clean commit + push CLOUD</expect>
      <if_mismatch>Per safe-commit / ds-commit-gate protocol</if_mismatch>
    </step>
    <step>
      <run>If new gold script: aws s3 cp to s3://opal-data-bd/code/gold/ (DS owns upload per CLAUDE.md rule 13); comp-pipescript deployed verify MATCH.</run>
      <expect>Deployed runner has fresh code</expect>
      <if_mismatch>Per CLAUDE.md rule 13 protocol</if_mismatch>
    </step>
  </phase>

  <phase id="3" when="Phase 3 empirical">
    <step>
      <run>Next chain run: `gold/artifacts/clients_tab.json` LastModified updates within 26h.</run>
      <expect>AC1 satisfied</expect>
      <if_mismatch>If artifact still stale post-fix: re-investigate same TO</if_mismatch>
    </step>
  </phase>

  <cross_domain_coordination>
    <coord>**Gates on TO-1 silver-chain fix RAVC5.** Phase 0 observes whether TO-1 fix auto-resolves; if yes, TO-3 closes without code change.</coord>
    <coord>**DS lane lead** (gold script authoring) per project JSON lane_note. AE 0.6.1 secondary if root cause is dispatch issue, not gold script.</coord>
    <coord>**Frontend consumer** — RD 0.4.2 owns clients_tab.json portal-side rendering; if schema change needed, coordinate via RD lane.</coord>
  </cross_domain_coordination>

  <compiler_tools_mandate>
    <phase id="1" when="before writing">comp-pipescript io <candidate gold script> + comp-pipescript deployed</phase>
    <phase id="2" when="before commit">ds-commit-gate.sh + safe-commit.sh</phase>
    <phase id="3" when="after deploy">Next chain run empirical</phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <criterion id="AC1">`gold/artifacts/clients_tab.json` LastModified < 26h on any nightly poll.</criterion>
    <criterion id="AC2">Producer documented in TO `<phase_0_findings>` (class a/b/c).</criterion>
    <criterion id="AC3">RAVC5 close: commit hash (if code change) + 7-day empirical no-stale.</criterion>
  </acceptance_criteria>

  <go_signal>
    <issued_at>STAGED — gates on TO-1 RAVC5 + Phase 0 observation</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>Status `staged`. Gates on TO-1 silver-chain fix; Phase 0 observation determines if code change needed.</message>
  </go_signal>
</task_order>
