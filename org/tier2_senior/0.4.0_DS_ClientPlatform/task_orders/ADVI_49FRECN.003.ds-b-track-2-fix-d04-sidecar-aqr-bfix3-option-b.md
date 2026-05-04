<task_order>
  <metadata>
    <id>ADVI_49FRECN.003</id>
    <project>ADVI_49FRECN</project>
    <title>Track 2 Fix — D_04 AQR Filter Removal + c1_recovered_accounts.json Sidecar + B_00/A_03 Ratification + Standing-Backlog</title>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-04</issued_date>
    <status>pending</status>
    <priority>P0 — completes 49FRECN Track 2 fix scope; recovers $60.4M of the $64.8M C1 bucket (93.3%)</priority>
    <estimated_effort>0.5d (most fixes already shipped opportunistically; this TO formalizes acceptance + adds AQR removal + sidecar emit + standing-backlog file)</estimated_effort>
  </metadata>

  <context>
    Phase 1.5 sub-investigation `.002.5` closed 2026-05-01 with C1 recalibrated to 64 accts/$64.8M
    (all C1b — zero genuinely closed) and 3 root-cause mechanisms identified:

      - B_00 RECONCILE_DROP: $38.5M (accounts dropped due to N-day stale window)
      - A_03 ingestion gap: $22.1M (RPS coverage lag at onboarding)
      - Genuinely-new (C1c): $4.1M (accounts in Schwab RPS feed without prior BD coverage)

    Recommended fix: Option D+B+A hybrid. Recovers $60.4M = 93.3% of C1.

    DS~B (you) shipped two fixes opportunistically before formal TO authoring:
      - `9fde23538` BFIX3 — B_00 rescue all-stale alive accounts from Schwab RPS cycle lag (Option D)
      - `e09cb806b` Option B — A_03 narrow rps_covered to accounts with actual RPS events

    This TO formalizes those + adds AQR filter removal (Andrew Q2 answer) + adds the
    `c1_recovered_accounts.json` sidecar (Andrew approved on `b4d8b121a` — FE forensic visibility
    on the $60.4M AUA shift) + creates a standing-backlog file documenting the two bandaids
    (N-day stale window per Q1; 7-day TXN_LAG tolerance per Q4 recommendation).

    Andrew Q answers (locked 2026-05-04):
      Q1 (N-day stale window): KEEP current bandaid; defer proper closure-detection rule to backlog
      Q2 (AQR scope): INCLUDE AQR-managed accounts in 49F AUA (remove D_04 AQR filter; +11 accts)
      Q3 (first-seen Schwab RPS attribution): DS~B/CTO design call for C1c $4.1M genuinely-new
      Q4 (TXN_LAG tolerance): COO recommendation = 7-day RPS lag tolerance, no SLA hold,
          flag rps_lag_days in sidecar, do NOT exclude from AUA. Andrew confirmed via "OK send GO."
  </context>

  <objective>
    Ship Track 2 fix end-to-end: AQR removal + sidecar emit + ratification of already-shipped
    BFIX3 and Option B fixes + standing-backlog file. After this TO closes, ADVI_49FRECN Phase 1
    is complete and project closes with the $60.4M recovery + the $4.1M C1c bucket parked as
    Option A wave (ship-or-park decision in this TO).
  </objective>

  <acceptance_criteria>
    <ac id="1">
      <title>D_04 AQR filter removal</title>
      <detail>
        Locate the line in `D_04.client_portal_summary.py` that filters out AQR-managed accounts
        (likely a string-match or flag-check excluding accounts with strategy/manager containing
        "AQR"). Remove it. Re-run on a recent gold partition. Verify:
        - 11 AQR accounts now appear in firm AUA roll-up (count match against .002.5 finding)
        - Firm-level AUA shifts upward by ~$11M
        - No regression on advisor/client roll-ups (AQR accounts attribute correctly to their assigned advisor)
        Document the filter location (file:line) and the exact line removed in the session log.
      </detail>
    </ac>
    <ac id="2">
      <title>c1_recovered_accounts.json sidecar emit</title>
      <detail>
        D_04 emits a parallel sidecar to `out_of_scope_accounts.json`:
        Path: `s3://opal-data-bd/gold/artifacts/49f/c1_recovered_accounts.json`
        Schema (per Andrew approval `b4d8b121a` + COO Q4 ruling):
        ```
        {
          "snapshot_date": "YYYY-MM-DD",
          "total_recovered_aua": <float>,
          "total_recovered_count": <int>,
          "accounts": [
            {
              "account_id": "...",
              "advisor_id": "...",
              "advisor_name": "...",
              "household_id": "...",
              "recovery_mechanism": "B_00_BFIX3" | "A_03_OPTION_B" | "GENUINELY_NEW_C1C" | "AQR_INCLUDED",
              "aua": <float>,
              "first_seen_rps": "YYYY-MM-DD",
              "first_txn_posted": "YYYY-MM-DD" | null,
              "rps_lag_days": <int>,
              "rps_lag_flag": <bool> // true if rps_lag_days > 7
            }
          ]
        }
        ```
        Sidecar parallels `out_of_scope_accounts.json` ETag-equivalent verification.
        Initial expected count: 64 + 11 AQR = 75 accounts; total_recovered_aua ~$60.4M + ~$11M = ~$71.4M.
      </detail>
    </ac>
    <ac id="3">
      <title>B_00 BFIX3 ratification</title>
      <detail>
        `9fde23538` (B_00 rescue all-stale alive accounts from Schwab RPS cycle lag) ratifies as-is
        per Andrew Q1. Document in session log:
        - Pre-fix B_00 RECONCILE_DROP bucket size (was $38.5M per .002.5)
        - Post-fix RECONCILE_DROP bucket size (expected near-zero, OR stable smaller residual)
        - N-day threshold value used (current bandaid number — document for backlog)
        No code change in this TO for B_00; this AC is an evidence audit on the already-shipped fix.
      </detail>
    </ac>
    <ac id="4">
      <title>A_03 Option B ratification</title>
      <detail>
        `e09cb806b` (A_03 narrow rps_covered to accounts with actual RPS events) ratifies as-is
        per Andrew Q3 first-seen attribution. Document in session log:
        - Pre-fix A_03 ingestion-gap bucket size (was $22.1M per .002.5)
        - Post-fix ingestion-gap bucket size (expected near-zero, OR stable smaller residual)
        - The narrowing predicate (the "actual RPS events" definition — for backlog)
        No code change in this TO for A_03; evidence audit only.
      </detail>
    </ac>
    <ac id="5">
      <title>C1c genuinely-new bucket — Option A ship-or-park decision</title>
      <detail>
        $4.1M / ~10 accounts genuinely new (Schwab RPS feed appearance without prior BD coverage).
        Andrew Q3 deferred to DS~B/CTO design call. Two paths:

        - **SHIP (Option A wave):** First-seen Schwab RPS attribution rule — emit account in C1c
          bucket of sidecar with `recovery_mechanism: "GENUINELY_NEW_C1C"` + flag for FE forensic
          review. Same first-seen logic as A_03 Option B.
        - **PARK:** $4.1M / 6.3% of C1 is small enough that residual is acceptable.
          Document in standing-backlog as deferred.

        DS~B recommendation (with empirical reasoning) lands in session log. CTO acks before commit
        (one MCP exchange). Default position if CTO unresponsive: SHIP the sidecar emit but do NOT
        add to AUA roll-up (forensic-only). Reversible.
      </detail>
    </ac>
    <ac id="6">
      <title>Standing-backlog file</title>
      <detail>
        Create `docs/architecture/49FRECN_STANDING_BACKLOG.md` documenting the two bandaids that
        survived this fix:

        1. **N-day stale window for B_00 RECONCILE_DROP** (Q1) — current threshold is X days
           (you fill in actual value), source: `9fde23538` BFIX3. Proper rule should be RPS-feed-driven
           (account is closed when it stops appearing in RPS feed for 2+ consecutive cycles), not
           time-driven. Research project — Andrew flagged "can't hold up everything else."

        2. **7-day TXN_LAG tolerance** (Q4) — accounts with >7 days between first RPS appearance
           and first transaction posting flagged in sidecar via `rps_lag_flag: true` but NOT
           excluded from AUA. Bandaid pending proper SLA definition.

        File should be short (~1 page), include:
        - Problem statement
        - Current bandaid
        - Why proper rule is needed
        - Estimated effort to design proper rule
        - Trigger conditions for activating the research project
      </detail>
    </ac>
    <ac id="7">
      <title>Session log + Compiler Tools section + RAVC4</title>
      <detail>
        Standard. Session log under
        `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-05-04/ADVI_49FRECN_003_track2_fix.md`.
        Compiler Tools section reproduces every `<run>` in this TO's mandate with observed result
        + pass/fail vs `<expect>`. RAVC4 to COO with sidecar S3 path + ETag + commit hashes.
      </detail>
    </ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before_writing_code">
      <step>
        <run>comp-pipescript io D_04</run>
        <expect>D_04 reads 24 sources + writes 22 platinum keys; AQR filter location identifiable in source via grep</expect>
        <if_mismatch>If comp output diverges materially from this baseline (which COO ran 2026-05-04), flag a structural change since `eb929bf45`/`0ae9068aa` to COO before proceeding</if_mismatch>
      </step>
      <step>
        <run>comp-platinum reverse c1_recovered_accounts.json</run>
        <expect>Zero downstream consumers (sidecar is forensic — initial release)</expect>
        <if_mismatch>If FE component already wired to read this path, verify schema compatibility before emit; flag DE coordination need to COO</if_mismatch>
      </step>
      <step>
        <run>comp-platinum reverse out_of_scope_accounts.json</run>
        <expect>Enumerate FE consumers if any (sister artifact from .002); ensure new sidecar follows same conventions</expect>
        <if_mismatch>If sister artifact is already FE-rendered, mirror its conventions; if not, document as backlog for FE wiring</if_mismatch>
      </step>
      <step>
        <run>grep -n "AQR" data/black_diamond/scripts/gold/D_04.client_portal_summary.py</run>
        <expect>One or more lines matching AQR filter logic (string-match exclusion or flag check)</expect>
        <if_mismatch>If zero matches, the filter may live upstream in A_00 or C_03 — chase the chain; document the actual filter location</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before_commit">
      <step>
        <run>.tools/ds-commit-gate.sh data/black_diamond/scripts/gold/D_04.client_portal_summary.py</run>
        <expect>py_compile + ds-precommit-check + ruff all exit 0</expect>
        <if_mismatch>Fix the underlying issue per CLAUDE.md Rule 14; do NOT bypass with --force</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript deployed D_04</run>
        <expect>S3 runner state shows MATCH after upload (DS-owned upload per CLAUDE.md Rule 13)</expect>
        <if_mismatch>STALE = re-upload via aws s3 cp; MISSING = investigate</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after_commit">
      <step>
        <run>aws s3 ls s3://opal-data-bd/gold/artifacts/49f/c1_recovered_accounts.json</run>
        <expect>Sidecar object present after gold run; mtime &gt; commit time</expect>
        <if_mismatch>Gold run failed to emit sidecar; debug D_04 emit logic</if_mismatch>
      </step>
      <step>
        <run>aws s3api head-object --bucket opal-data-bd --key gold/artifacts/49f/c1_recovered_accounts.json --query "ETag"</run>
        <expect>ETag captured for RAVC4 evidence (mirrors .002 RAVC4 pattern)</expect>
        <if_mismatch>Object missing or unreadable; investigate IAM or emit path</if_mismatch>
      </step>
      <step>
        <run>jq '.total_recovered_count, .total_recovered_aua' &lt; sidecar.json</run>
        <expect>count ≈ 75 (64 C1 + 11 AQR), AUA ≈ $71.4M (60.4M C1 + 11M AQR), tolerance ±5% for partition drift</expect>
        <if_mismatch>Numbers materially off — verify mechanism counts and AQR removal landed correctly</if_mismatch>
      </step>
      <step>
        <run>comp-validate D_04 --artifact /tmp/c1_recovered_accounts.json</run>
        <expect>If validate config exists for D_04, exit 0 all-pass; else "no config" exit is acceptable per COMP_VALIDATE_PROTOCOL</expect>
        <if_mismatch>Per COMP_VALIDATE_PROTOCOL.md retry/escalation; ERROR-class fail blocks RAVC4</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <resource>
      <path>data/black_diamond/scripts/gold/D_04.client_portal_summary.py</path>
      <owners>0.4.0_DS_ClientPlatform~B (this TO); no concurrent active TO touches D_04</owners>
      <coordination>None required — DS~A standing down; DS~C on E_25 unrelated; DS~D on HISTBF unrelated. Sole-owner edit window.</coordination>
    </resource>
    <resource>
      <path>s3://opal-data-bd/gold/artifacts/49f/c1_recovered_accounts.json</path>
      <owners>0.4.0_DS_ClientPlatform~B (producer); FE downstream TBD post-RAVC</owners>
      <coordination>If FE wants to render the sidecar, separate DE TO post-this-TO ship. Forensic-only acceptable initial state.</coordination>
    </resource>
    <resource>
      <path>docs/architecture/49FRECN_STANDING_BACKLOG.md</path>
      <owners>0.4.0_DS_ClientPlatform~B (author); CTO architectural sponsor for future research project trigger</owners>
      <coordination>None for this TO. Future project authoring is CTO scope.</coordination>
    </resource>
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>
      Reasoning: All changes are gold-tier (D_04 is bd-gold). No silver/bronze script touched.
      Historical data semantically unchanged — only this gold-run-forward emits the corrected
      AUA roll-up + sidecar. Downstream platinum consumers (FE) read latest snapshot only;
      no historical replay needed. AQR-included AUA shift visible immediately on next gold run.
    </no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    <item>D_04 AQR filter removal — 1 commit (DS~B author)</item>
    <item>D_04 c1_recovered_accounts.json sidecar emit logic — same commit OR follow-up commit</item>
    <item>docs/architecture/49FRECN_STANDING_BACKLOG.md — separate commit (architectural doc)</item>
    <item>Session log with Compiler Tools section + B_00/A_03 ratification evidence + AC#5 SHIP-or-PARK decision</item>
    <item>RAVC4 MCP to COO with sidecar S3 path + ETag + commit hashes + total_recovered_count + total_recovered_aua</item>
  </deliverables>
</task_order>
