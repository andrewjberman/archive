# Task Order: ADVI_INFLEC SCOPEFIX-2 — Inflection-Only Advisor Filter

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-20260427-advi-inflec-scopefix-2</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-27</date>
    <status>open</status>
    <priority>CRITICAL — higher than F1-F3 schema work; wrong data outranks wrong shape</priority>
  </metadata>

  <objective>
    Andrew identified a fundamental data scoping error: the Inflection portal currently
    shows $429M total AUA but Inflection's actual AUA is ~$191M. Root cause: the
    Inflection user account in Orion has view access to all affiliate firms (Keil Partners
    + others), so the current export includes non-Inflection advisors and their AUM.

    SCOPEFIX-1 (complete, silver-layer firm filter) catches the firm-level tag but does
    NOT filter advisor-level affiliate mixing. SCOPEFIX-2 adds an advisor-identity filter
    so only the ~4 actual Inflection employees survive into silver and downstream.

    This is a temporary bridge measure. The inf-bronze-runner (BRONZERUN_V2 PRD,
    W3.B TOs) will eventually apply upstream filtering at the Orion export step.
    SCOPEFIX-2 holds until that lands.
  </objective>

  <scope>
    <phase id="0" label="Audit">
      Inspect the Orion silver data to identify which column(s) carry advisor firm
      identity. Candidates: firm_id, office_id, parent_firm, affiliate_firm, rep_id,
      advisor_code, or any string column that could distinguish Inflection employees
      from Keil Partners or other affiliates.

      Deliverable: a short audit note (inline comment or MCP message) that identifies:
        (a) the exact column(s) that carry firm identity for each advisor row
        (b) the value(s) that identify Inflection-proper employees
        (c) the value(s) present for non-Inflection advisors (Keil Partners etc.)
        (d) whether the filter can be cleanly applied at silver layer or requires
            gold dimension layer injection
    </phase>

    <phase id="1" label="Implement filter">
      Apply an Inflection-only advisor filter at the silver layer (preferred) or at
      the gold advisor dimension layer (fallback if no clean silver-layer column).

      Silver-layer preferred approach:
        In convert_orion_to_silver.py (or its equivalent), after loading the raw
        export, apply:
          df = df[df[FIRM_ID_COL].isin(INFLECTION_ADVISOR_IDS)]
        where INFLECTION_ADVISOR_IDS is the set of rep_ids / advisor_codes identified
        in Phase 0.

      Gold dimension fallback (if silver column is unavailable):
        In the gold advisor dimension script (I_00 or equivalent), inject an
        advisor allowlist filter keyed on the same INFLECTION_ADVISOR_IDS set.

      Whichever layer is chosen, the filter must be:
        - Explicit (constant set, not a regex or inference rule)
        - Commented with the SCOPEFIX-2 reference and the temp-measure note
        - Gate-safe (pre-commit gate .tools/ds-commit-gate.sh must pass)
    </phase>

    <phase id="2" label="Re-run chain">
      After filter is in place and committed, dispatch the full Inflection gold chain
      re-run via AE 0.6.1 (same pattern as SCOPEFIX-1 chain re-run).

      Chain sequence: silver rebuild → I_00 → ... → I_09 → publisher → platinum S3.
      AE 0.6.1 owns the SSM dispatch and chain coordination.

      DS signals AE when the filter commit is live on CLOUD with a RAVC message
      that includes: commit hash, filter column, and filtered advisor ID set.
    </phase>
  </scope>

  <acceptance_criteria>
    <criterion id="1">
      header_metrics.json total_aua is approximately $191M (within reasonable
      market-movement tolerance from Andrew's stated figure). NOT $429M.
    </criterion>
    <criterion id="2">
      Advisor count in leaderboard.json drops from 9 to ~4 (the actual Inflection
      headcount). Non-Inflection advisors (Keil Partners etc.) are absent.
    </criterion>
    <criterion id="3">
      comp-validate exit 0 on the re-run platinum artifacts.
    </criterion>
    <criterion id="4">
      The filter implementation passes .tools/ds-commit-gate.sh (py_compile +
      ds-precommit-check.py + ruff check --target-version py39).
    </criterion>
    <criterion id="5">
      Commit uses --only pathspec (CLAUDE.md Rule 14a). No COMP_LEARNS or unrelated
      files swept. Author attributed to 0.4.0_DS_ClientPlatform serial.
    </criterion>
    <criterion id="6">
      DS sends RAVC to COO (2.0.0_SA_COO) + AE 0.6.1 on filter commit.
      AE 0.6.1 sends RAVC to COO on chain re-run + platinum S3 confirm.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Filter must be applied to advisor rows only (do not filter client/account
    rows by firm independently — the client-advisor join handles that downstream).</constraint>
    <constraint>No emojis in code, logs, or print statements (CloudWatch ASCII rule).</constraint>
    <constraint>from __future__ import annotations must remain first import in all
    modified .py files (CLAUDE.md Rule 15).</constraint>
    <constraint>This is a TEMP measure. Add a comment in the filter block:
    # SCOPEFIX-2: Inflection-only advisor allowlist — temp until BRONZERUN_V2 upstream filter
    </constraint>
    <constraint>Do NOT modify F1-F3 platinum schema shape (leaderboard, partner_analytics,
    header_metrics structures). SCOPEFIX-2 re-runs the chain with the same schema;
    only the data values change (AUA, advisor count).</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.6.1_AE_PartnerETL"
                task="chain-rerun-post-scopefix2"
                status="pending"
                note="AE 0.6.1 must dispatch the silver-rebuild → gold chain → platinum
                publisher SSM sequence after DS delivers the filter commit. Same
                pattern as SCOPEFIX-1 chain re-run. Gate: DS RAVC on filter commit."/>
    <dependency agent="0.4.2_RD_AdvisorIntelligence"
                task="integrated-re-smoke"
                status="HOLD"
                note="RD Option C re-smoke is HELD pending SCOPEFIX-2 chain completion.
                RD will smoke the post-SCOPEFIX-2 platinum (correct ~$191M data)
                not the current $429M artifacts. Andrew sign-off (step 8) likewise
                held."/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">Filter implementation commit on CLOUD with --only pathspec,
    pre-commit gate passing, SCOPEFIX-2 comment block present.</deliverable>
    <deliverable type="mcp">RAVC message to 2.0.0_SA_COO + 0.6.1_AE_PartnerETL with
    commit hash, filter column, and Inflection advisor ID set.</deliverable>
  </deliverables>

  <references>
    <ref type="project">org/projects/ADVI_INFLEC.json</ref>
    <ref type="prd">docs/architecture/ADVI_INFLEC.md</ref>
    <ref type="prior_fix">SCOPEFIX-1 — silver-layer firm filter (complete, commit in CLOUD)</ref>
    <ref type="future">BRONZERUN_V2 PRD — upstream Orion export filtering (W3.B, replaces this temp fix)</ref>
  </references>
</task_order>
```
