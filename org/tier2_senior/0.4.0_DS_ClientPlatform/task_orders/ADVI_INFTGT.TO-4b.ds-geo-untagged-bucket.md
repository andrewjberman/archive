<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFTGT.TO-4b</id>
    <project>ADVI_INFTGT</project>
    <title>[P1] Continuous-GEO-AUA bug investigation — $189M is bogus (always-wrong), not coverage gap; root-cause + fix</title>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-11</issued_date>
    <revised>2026-05-11 — scope flipped post-Andrew correction: $189M has always been wrong, not a coverage subset</revised>
    <status>active</status>
    <priority>P1 — parity gap (RD interim drop-subtotal covers demo; this is the architectural fix)</priority>
    <authorized_by>CTO ruling 2026-05-11 (REVISION post-Andrew direct correction); Andrew direct: "no idea why Continuous-GEO-AUA would surface 189m that number is wrong and has always been wrong"</authorized_by>
  </metadata>

  <context>
    Andrew flagged Continuous Segment Analytics shows "$189M Cumulative AUA by Geography" — should be $203M canonical. Initial COO/CTO hypothesis: coverage gap (state_tagged_aua is strict subset of total_aua, ~$14M untagged). Proposed fix: add synthetic "Untagged" bucket.

    **Andrew correction:** "no idea why Continuous-GEO-AUA would surface 189m that number is wrong and has always been wrong"

    **Implication:** $189M is NOT a partial-set. It's a **computation bug** in INF_D_08 (or whichever script feeds the Continuous-GEO-AUA cumulative sidebar). Adding an "untagged bucket" would paper over the bug without fixing the underlying logic.

    **This is an INVESTIGATION TO** — root-cause before fix. The bucket-add framing is OFF THE TABLE until the underlying computation is verified correct on the accounts it DOES include.
  </context>

  <scope>
    <step>Phase 1 — Locate producer:
      `comp-pipescript io INF_D_08` (or whichever script feeds nna_geo / Continuous-GEO-AUA)
      `comp-trace nna_geo --direction both`
      `comp-platinum reverse nna_geo`
      Confirm: which file produces the $189M value? What columns/filters does it use?
    </step>

    <step>Phase 2 — Hypothesis test (try each, document which is true):
      H1: **Wrong source column** — summing `fee_earning_aua` instead of `total_aua` OR `state_tagged_aua` instead of canonical
      H2: **Filter excluding accounts** — entity-vs-individual filter, or active-only filter, or rep_id filter that drops some
      H3: **Double-counting OR dropping dimensions** — sum-over-grouped result misses accounts present in multiple state rows OR drops accounts in no rows
      H4: **Snapshot/partition mismatch** — reading older silver partition than sibling artifacts
      H5: **Cumulative-calculation logic error** — averaging instead of summing, only-positive filter, period-window misalignment
      
      For each hypothesis, verify against canonical: pull current silver, compute the same metric manually, compare to artifact value.
    </step>

    <step>Phase 3 — Root cause documentation:
      Once H is identified, document in session log:
      - File + function + line range of the bug
      - Which hypothesis confirmed
      - Why it produces $189M specifically
      - Why it has "always been wrong" (when did the bug enter; what's the git history)
    </step>

    <step>Phase 4 — Fix:
      Implement the fix. Could be:
      - Single-line column rename (`fee_earning_aua` → `total_aua`)
      - Filter relaxation
      - Group-by-then-sum logic refactor
      - Snapshot pin alignment
      Test with current silver: cumulative-by-geo sums to canonical total_aua within rounding.
    </step>

    <step>Phase 5 — Coordinate with RD:
      After this ships + coordinated rerun (TO-2b) completes, ping RD to optionally re-add the cumulative subtotal in Continuous Segment Analytics (RD interim drop is still acceptable per partner UX).
    </step>

    <step>Pre-commit gate per CLAUDE.md rule 14.</step>

    <step>Local verify: re-run affected script; confirm cumulative geo-AUA sums to canonical total_aua.</step>

    <step>Commit + push + S3 deploy + manual SHA verify.</step>

    <step>RAVC2 to COO with:
      - Root cause documentation (hypothesis + git history)
      - Before/after computation values
      - Confirmation cumulative = canonical (±rounding)
      - Portal coordination note for optional re-add of subtotal
    </step>
  </scope>

  <acceptance_criteria>
    1. Root cause of $189M identified + documented in session log (file/function/line/hypothesis).
    2. Bug fix implemented + matches root-cause analysis.
    3. Post-fix cumulative-by-geo sums to canonical total_aua within rounding ($1k tolerance).
    4. NOT acceptable to ship "add untagged bucket" without first establishing whether the underlying computation is correct.
    5. Pre-commit gate exits 0.
    6. S3 deploy MATCH.
    7. RAVC2 includes root cause + git history + before/after values.
    8. RD coordination note (subtotal re-add optional).
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      `comp-pipescript io INF_D_08` (or actual producer script)
      `comp-trace nna_geo --direction both`
      `comp-platinum reverse nna_geo`
    </phase>
    <phase id="2" when="before commit">
      `.tools/ds-commit-gate.sh` on edited .py files
      Local manual verify cumulative = canonical
    </phase>
    <phase id="3" when="after commit">
      Manual SHA verify on S3 deploy
      Post-coordinated-rerun (TO-2b): re-verify against fresh artifacts
    </phase>
  </compiler_tools_mandate>

  <notes>
    **CTO ask to Andrew:** Has any historical context for what cut/subset $189M might historically have matched? Would help bound DS's search. CTO will relay if Andrew replies.

    **Investigation effort range:** 1h if root cause obvious from first hypothesis; up to 6h if requires multiple test rounds across silver partitions.

    **Sibling work:** TO-2b coordinated rerun should land first OR concurrent — TO-4b fix needs to verify against fresh artifacts. Coordinate with whoever takes TO-2b.

    **NOT partner-blocking** — RD's drop-subtotal interim covers the demo today.
  </notes>
</task_order>
