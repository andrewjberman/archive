<to_id>NFRA_COT_RULE15</to_id>
<project>NFRA_DTAFLP (Rule-15 compliance; same Rule-13 deploy pattern)</project>
<title>Rule-15 backfill — insert `from __future__ import annotations` in the 20 cot gold scripts missing it</title>
<assigned_to>0.4.0_DS_ClientPlatform</assigned_to>
<issued_by>2.0.0_SA_COO (CTO gap-sizing 141911Z; COT-FIX b9754025b exposed gap — cot gold escaped the 71-script backfill)</issued_by>
<issued_date>2026-06-12</issued_date>
<status>pending</status>
<priority>Low — fully latent (0 live PEP-604 syntax in the 20 missing scripts, nothing crashes today); GO at capacity; can ride same allocation pass as NFRA_COT_TOOLING or cot fee-ingestion timeline</priority>

<references>
  <ref type="gap-sizing">CTO 141911Z: 20 of 47 cot scripts missing future-import, ALL in gold (silver/bronze covered); 0 of the 20 contain live PEP-604 union syntax = FULLY LATENT; list available from CTO on request</ref>
  <ref type="rule">CLAUDE.md Rule 15: every data/*/scripts/gold/*.py MUST begin with `from __future__ import annotations` as its first import statement</ref>
  <ref type="gate">ds-precommit-check.py enforces ADHC_DSFLOW.004; the edit-time gate already catches future touches — this TO closes the pre-existing gap</ref>
  <ref type="precedent">71-script bd+cot backfill sweep (prior session) missed the cot gold tree; b9754025b fixed A_01+A_04 as incidental; this TO covers the remaining 20</ref>
</references>

<scope>
Mechanical backfill: insert `from __future__ import annotations` as the FIRST import statement in all 20 cot gold scripts currently missing it.

**Step 1 — Enumerate:** Request the exact 20-script list from CTO (141911Z MCP, he has it from his direct sweep). Alternatively: `grep -rL "from __future__ import annotations" data/cot/scripts/gold/*.py` to derive it independently.

**Step 2 — Verify pre-condition:** confirm each missing script has 0 live PEP-604 union syntax (`str | None`, `X | Y`, `X | None`) before touching — CTO's sizing says 0, but confirm per-file before the batch commit.

**Step 3 — Insert:** for each script, add `from __future__ import annotations` as the first line after the module docstring (if any) or as the very first line (if no docstring), before all other imports. Do NOT reorder existing imports or change any logic.

**Step 4 — Gate + deploy:** run `.tools/ds-commit-gate.sh` on all 20 files (py_compile + ruff pass required); then Rule-13 deploy cycle to opal-data-cot/code/gold/ for all 20 in one batch.

**Firm separation:** cot gold only. No changes to bd or inf scripts. Deploy to opal-data-cot ONLY.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before change">
    <step>
      <run>grep -rL "from __future__ import annotations" data/cot/scripts/gold/*.py</run>
      <expect>~20 scripts (matches CTO's count). Enumerate the exact list before touching any file.</expect>
      <if_mismatch>If count differs significantly from 20, surface to CTO before proceeding (may indicate tree drift since CTO's sweep).</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>.tools/ds-commit-gate.sh data/cot/scripts/gold/*.py (the 20 modified scripts)</run>
      <expect>All checks exit 0 (py_compile + ds-precommit-check + ruff). Rule-15 check now passes on all 20.</expect>
      <if_mismatch>Fix before commit — a compile error means the insertion was malformed.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after deploy">
    <step>
      <run>comp-pipescript deployed data/cot/scripts/gold/[spot-check 2-3 scripts from the batch]</run>
      <expect>MATCH (if NFRA_COT_TOOLING has landed by then) OR md5-verify manually against opal-data-cot/code/gold/ (if tooling TO not yet complete).</expect>
      <if_mismatch>STALE = deploy cycle incomplete. Re-run safe-deploy before RAVC2.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- **NFRA_COT_TOOLING (AE 0.6.0, same allocation pass):** if that TO lands before this one, use comp-pipescript deployed for the Phase-3 MATCH check. If it hasn't landed yet, use md5-verify manually.
- No coordination with AE required for the code change itself — this is a standalone compliance sweep.
</cross_domain_coordination>

<acceptance_criteria>
- grep confirms 0 cot gold scripts missing `from __future__ import annotations` after the batch.
- ds-commit-gate.sh exits 0 on all 20 modified scripts.
- Rule-13 deploy to opal-data-cot/code/gold/ MATCH-verified (all 20).
- RAVC2 to COO: commit hash + grep-0 confirmation + deploy MATCH spot-check.
</acceptance_criteria>

<data_reprocess_scope><no_reprocess_needed>Compliance-only insertion; no logic change; no data-path changes. No served output movement expected or possible.</no_reprocess_needed></data_reprocess_scope>
