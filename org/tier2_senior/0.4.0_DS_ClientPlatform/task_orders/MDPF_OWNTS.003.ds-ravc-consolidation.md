<task_order>
<metadata>
  <to_id>MDPF_OWNTS.003</to_id>
  <project>MDPF_OWNTS</project>
  <title>DS RAVC consolidation: end-to-end live-run verification + AC1-AC7 evidence packet + project-close RAVC2</title>
  <assigned_to>0.4.0_DS_ClientPlatform</assigned_to>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-05-26</issued_date>
  <status>pending — dispatch_held (gates on MDPF_OWNTS.002 RAVC2-ACCEPT + first live chain fire post-Stage-4-wire)</status>
  <dispatch_held>true</dispatch_held>
  <priority>HIGH (project-close gate; Andrew sovereign chain final validation)</priority>
  <references>
    <ref type="prd">docs/architecture/MDPF_OWNTS.md v0.1 (commit `8a125c682`)</ref>
    <ref type="prd_section">§6 TO decomposition (MDPF_OWNTS.003); §8.2 AC1-AC7 project-close ACs</ref>
    <ref type="depends_on">MDPF_OWNTS.001 (DS author) + MDPF_OWNTS.002 (AE chain wire) RAVC2-ACCEPTED</ref>
    <ref type="live_fire">First mdpf-daily-dispatch chain run post-.002 deploy (EventBridge cron 15:00 UTC OR ad-hoc SSM dispatch for fast-path validation)</ref>
  </references>
  <dependencies>
    <dependency>**HARD GATE:** MDPF_OWNTS.002 RAVC2-ACCEPTED + AE chain wire deployed + first live chain fire post-Stage-4 emission</dependency>
  </dependencies>
</metadata>

<scope>
**End-to-end live-run validation** of the MDPF_OWNTS chain Stage 4 emission per PRD v0.1 §8.2 project-close ACs.

**Substrate (4 deliverables):**

1. **Verify first-live-emission of augmented aggregate-AUA platinum** carries `ownership_pct` field per `held_by_partner` entry inside `etf_decomposition`; reconciliation invariants UNAFFECTED (PRD AC1).

2. **Verify per-ticker time-series artifact** at `s3://opal-data-portal-v2/platinum/mdpf/etf_ownership_timeseries/{ticker}.json` for all 4 Opal ETFs (DIVZ + IDVZ + PFDE + PFOE) emits cleanly on first chain fire (PRD AC2).

3. **Verify MTD + YTD rollups arithmetically** against DS brief findings (PRD AC3):
   - Post-onboard window n=6 PFOE 6.520% + PFDE 7.413% present-only
   - Pre-onboard-zero full-window PFOE ~2.30% + PFDE ~2.61%
   - DIVZ/IDVZ 0.000% per Inflection's Eclipse v1 zero-target

4. **Verify reconciliation gates** PASS on first live emit (PRD AC6 self-consistency ratio-recompute gate); verify DoD anomaly soft-flag fires correctly when historical PFOE 5/21-5/22 trajectory is rebuilt (PRD AC5).

**RAVC2 packet to ws COO** citing:
- Concrete S3 object paths + sha256 hashes for the augmented aggregate-AUA platinum + per-ticker time-series artifacts
- Reconciliation block from first-live-emit chain manifest
- AC1-AC7 evidence inline (AC7 RUNBOOK update is verified by AE in .002 but cross-checked here)
- comp-validate exit-0 confirmation
- chain manifest run-id for first-live-fire-post-deploy
</scope>

<acceptance_criteria>
- AC1-AC7: per PRD §8.2 — each AC empirically verified by inspection of live-emit S3 artifacts + chain manifest + comp-validate outputs (NOT just code-inspection per [[feedback_verification_class_taxonomy_for_b_extension_rulings]] empirical-smoke-class).

**Pass requires all 7 PRD ACs MET via empirical-smoke verification on live emissions (NOT fixture runs alone).**
</acceptance_criteria>

<compiler_tools_mandate>
- `comp-validate [script] --artifact <S3-object-path>` on first-live-emit artifacts (NOT fixtures)
- `comp-pipescript deployed` on `mdpf_aggregate_aua.py` + `build_mdpf_etf_ownership_timeseries.py` (verify runner has the chain-deployed code MATCH)
- `comp-trace [ownership_pct] --direction both` cross-layer validation if any downstream consumer surfaces (none expected v1)
</compiler_tools_mandate>

<cross_domain_coordination>
- **MDPF_OWNTS.002 (AE) HARD GATE** — your TO does NOT fire until AE RAVC2-ACCEPTED + first live chain fire post-Stage-4-wire emits artifacts.
- **Project close on this RAVC2-ACCEPT** — ws COO 3-step atomic project-close (JSON + REGISTRY + PRD status COMPLETE bundle); CC CTO + MSTR per PRD §6 ratification chain.
</cross_domain_coordination>

<deliverable_disposition>
**Submit RAVC2-Request to ws COO** at completion. ~30min wall per PRD §6 (live-run validation + evidence packet).

**Project closes** on ws COO RAVC2-ACCEPT of this TO.
</deliverable_disposition>

<notes>
- Empirical-smoke-class validation MANDATORY per [[feedback_verification_class_taxonomy_for_b_extension_rulings]] LD-0095 doctrine; code-inspection alone insufficient for a live-chain-fire AC.
- Fast wall-time (~30min) reflects evidence-packet-only scope; assumes .002's first live chain fire already emitted clean artifacts.
- If first chain fire post-.002 emits errors (Stage 4 failure, missing S3 keys, reconciliation gate fail), this TO surfaces blocker → AE 0.7 hotfix loop → re-run chain → re-validate. Worst-case +1d.
</notes>
</task_order>
