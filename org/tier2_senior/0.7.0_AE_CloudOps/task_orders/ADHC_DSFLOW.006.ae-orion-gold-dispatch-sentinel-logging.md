<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADHC_DSFLOW.006</id>
    <project>ADHC_DSFLOW</project>
    <title>orion-gold-dispatch.sh sentinel-write error visibility — remove `2>/dev/null` suppression at line 786; pipe stderr; non-silent error logging on pipeline-complete.json write failure</title>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-11</issued_date>
    <status>pending</status>
    <priority>medium</priority>
    <estimated_effort>~10 min (script edit + S3 deploy + test dispatch)</estimated_effort>
    <authorized_by>1.0.0_SA_CTO ratified 2026-05-11 — silent-failure on production sentinel write is operational gap</authorized_by>
  </metadata>

  <references>
    <ref type="empirical_incident">2026-05-11 Gate 4 investigation — `gold/meta/pipeline-complete.json` absent post-cascade. CTO root-cause analysis identified `orion-gold-dispatch.sh:786` `aws s3 cp ... 2>/dev/null` suppressing potential write failures silently.</ref>
    <ref type="affected_script">orion-gold-dispatch.sh (lives at `s3://opal-data-inf/code/gold/orion-gold-dispatch.sh`, NOT in repo per AE 0.7 audit `feedback_gold_runner_pull_mechanism_s3.md`)</ref>
    <ref type="related_to">ADHC_INFRUNNERPARITY (`35ffe221b`) — out-of-band-installed boot dispatcher remediation. This TO is the sentinel-write logging hardening; sequenced separately.</ref>
    <ref type="cto_root_cause">CTO 2026-05-11: "Sentinel writes REGARDLESS of chain_exit code — failures don't block it (verified lines 758-789: no early-exit between chain_exit capture and sentinel write). `aws s3 cp` error is suppressed via `2>/dev/null` (line 786) — silent failure path."</ref>
  </references>

  <context>
    `orion-gold-dispatch.sh` is the production boot dispatcher for the inf-gold-layer-runner. Line 774 writes `pipeline-complete.json` as the INFETL.011 production safety-net sentinel. Today's gate 4 investigation revealed that line 786's `aws s3 cp ... 2>/dev/null` suppresses ALL stderr including legitimate write failures.

    Silent failure of this sentinel write is a serious operational gap:
    - Aggregator Lambda + downstream consumers depend on `pipeline-complete.json` as the chain-done signal
    - INFETL.011 production safety net presumes the marker reliably appears
    - If S3 cp fails (transient throttle, IAM glitch, regional outage), the chain appears "incomplete" to all downstream consumers but the operator gets no signal
    - Operators have NO log evidence of the failure to investigate

    **The fix is small but operational-discipline-load-bearing:** remove `2>/dev/null`, pipe stderr to stdout or to journalctl, add explicit success/failure log line.

    Today's local cascade `b9967954` did NOT exercise this code path (local cascade bypasses dispatch.sh entirely — per CTO scenario-2 analysis), so this TO doesn't unblock anything today. But the NEXT PROD chain trigger will hit this code path. Hardening today prevents the silent-failure class from biting in production.

    Coordination with `ADHC_INFRUNNERPARITY` — that TO codifies the dispatch.sh into repo. Order options:
    - **Option A (preferred):** AE 0.7 does this hardening as a one-line edit to the live S3 dispatch.sh + update internal change tracking. Doesn't depend on INFRUNNERPARITY shipping first.
    - **Option B:** Sequence after INFRUNNERPARITY ships dispatch.sh into repo; then both files are repo-edited atomically.

    Recommend A — small surgical fix, high-value safety net, urgent enough to not wait on INFRUNNERPARITY's larger surface.
  </context>

  <scope>
    <step>
      **Pull current `orion-gold-dispatch.sh` from S3** to a local working copy:
      `aws s3 cp s3://opal-data-inf/code/gold/orion-gold-dispatch.sh /tmp/orion-gold-dispatch.sh`

      Verify SHA256 + read line 786 + surrounding context (lines 770-795).
    </step>

    <step>
      **Apply the hardening edit at line 786.** Change from:
      ```bash
      aws s3 cp "$SENTINEL_FILE" "s3://${BUCKET}/gold/meta/pipeline-complete.json" 2>/dev/null
      ```
      to:
      ```bash
      if aws s3 cp "$SENTINEL_FILE" "s3://${BUCKET}/gold/meta/pipeline-complete.json"; then
          echo "[$(date -u +%FT%TZ)] [dispatch] Sentinel OK: gold/meta/pipeline-complete.json"
      else
          echo "[$(date -u +%FT%TZ)] [dispatch] WARN: sentinel write FAILED with exit=$? — chain completion signal not delivered" >&2
      fi
      ```
      Logs to stdout on success (visible in systemd journal); to stderr on failure (escalates to operator visibility).
    </step>

    <step>
      **Verify lines 770-795 holistic.** Confirm no other silent-fail patterns in the sentinel-write block. If similar suppression appears at adjacent steps (e.g., `git_sha` capture, instance metadata fetch), surface in RAVC but DO NOT auto-fix in this TO (scope-creep boundary).
    </step>

    <step>
      **Upload hardened script back to S3:**
      `aws s3 cp /tmp/orion-gold-dispatch.sh s3://opal-data-inf/code/gold/orion-gold-dispatch.sh`

      Verify SHA256 local vs S3 MATCH.
    </step>

    <step>
      **Test dispatch (low-risk option):** trigger a manual `inf-gold-trigger` Lambda invocation with `--dry-run` or test-only mode IF available. Otherwise, schedule next chain run + capture journalctl to confirm new logging fires correctly.

      If no dry-run path exists: document this as a follow-up "dry-run mode for dispatch.sh" TO candidate; for now, validate the script via `bash -n orion-gold-dispatch.sh` syntax check + ruff/shellcheck if available.
    </step>

    <step>
      **Author followup memory entry** (or fold into existing `feedback_gold_runner_pull_mechanism_s3.md` as an annotation): document the sentinel-write logging convention.
    </step>

    <step>
      **Commit + push** (the in-repo copy doesn't exist yet per INFRUNNERPARITY context; this TO updates the live S3 copy + tracks via session log). When INFRUNNERPARITY ships the script into repo, the hardened version becomes the canonical commit.
      
      Author: `0.7.0_AE_CloudOps`.
    </step>

    <step>
      **RAVC2 to COO** with:
      - Before/after diff of line 786
      - SHA256 MATCH on S3 deploy
      - Test outcome (journalctl evidence preferred; syntax-check only if no test path)
      - Any adjacent silent-fail patterns flagged for follow-on
    </step>
  </scope>

  <acceptance_criteria>
    1. **Line 786 hardening applied** — success/failure logging visible to operator.
    2. **No new silent-fail patterns introduced.** Adjacent suppression cleaned up OR flagged as separate follow-on.
    3. **S3 deploy SHA256 MATCH.**
    4. **Syntax-check PASS** (`bash -n` minimum; shellcheck preferred).
    5. **Next chain dispatch produces** "Sentinel OK" or "WARN: sentinel write FAILED" log line — capture journalctl evidence.
    6. **RAVC2 delivered** with diff + test outcome.
  </acceptance_criteria>

  <blocking>
    None. Independent of `ADHC_INFRUNNERPARITY` per the Option A path in `<context>`. Cascade close already accepted; this TO is post-close hardening, not blocker.

    Note: when `ADHC_INFRUNNERPARITY` ships, the hardened version of dispatch.sh ships with it into repo. Coordinate with AE 0.7 on which TO ships first; either order works.
  </blocking>

  <notes>
    **DSFLOW family continuation:** .001-.004 established gate + backfill; .005 = safe-deploy wrapper; **.006 = this dispatch.sh sentinel logging**. Workspace-wide concern (operational visibility on production safety-net writes).

    **Why medium not high priority:** silent failure didn't bite today (cascade was local, not production). But IT WILL bite when production has a transient S3 issue. The "no operator signal" failure mode is worse than the underlying transient — operators need the WARN logged so they investigate.

    **Cross-reference for memory entry:** "sentinel-write silent-failure is one instance of the broader pattern: `2>/dev/null` on critical operational ops is anti-pattern; pipe to logger or stderr always." Worth a DSFLOW operational-pattern memory entry candidate.

    **Relationship to ADHC_DSFLOW.005 (safe-deploy gate):** different surface (deploy vs runtime dispatch) but same family — operational discipline on workspace infrastructure scripts. Both AE 0.7 lane.
  </notes>
</task_order>
