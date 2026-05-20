<task_order>
  <metadata>
    <id>SSCN_DIVDEF.011</id>
    <slug>de-equal-weight-remainder-spread-fix</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.3.0_DE_TradingOperations</issued_to>
    <implementation_lane>0.3.4_RD (optional -- 2-line fix; DE may implement directly or hand to RD)</implementation_lane>
    <date>2026-05-20</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>DISPATCHED 2026-05-20 -- Andrew ruled HOLD .006 for this fix (he brought 0.3.0_DE online specifically to do it). COO flipped staged->pending + fired GO. The fix is fully specified below. Post-close sequence: .011 commit -> DT DEV push origin/DEV + :5175 refresh -> Andrew re-smoke of the Equal Weight fix -> .006 PROD GO.</dispatch_unblock_condition>
    <project_code>SSCN_DIVDEF</project_code>
    <priority>P1 -- bug surfaced by Andrew's 2026-05-20 DEV smoke of the SSCN bundle. Trivial fix; joins the .006 PROD bundle.</priority>
    <sla>~10-15min wall once GO lands.</sla>
    <deadline>None -- ship at DE/RD pace once GO lands.</deadline>
  </metadata>

  <references>
    <directive>Andrew DEV smoke 2026-05-20 surfaced one bug -- the Equal Weight button produces a visibly broken weight distribution. CTO 1.0.0_SA_CTO root-caused it + fully specified the 2-line fix; this TO is the decomposition of that.</directive>
    <prd>docs/architecture/SSCN_DIVDEF.md -- SSCN_DIVDEF project. This fix is a smoke-surfaced defect in the existing useScannerState.ts equal-weight helper; not a v0.x amendment scope item. CTO may note it in the v0.6 closeout.</directive>
  </references>

  <context>
    `portal/src/pages/SecurityScanner/hooks/useScannerState.ts` -> `buildEqualWeights()`. With the 13-factor DIVZ preset it floors 100/13 to base=7% each (13 x 7 = 91), then dumps the entire 9-point remainder onto factors[0] (Dividend Yield NTM, first in preset order) -> 16%. The total sums to 100 but the distribution is visibly broken: one outlier at 16%, twelve at 7%. The fix spreads the remainder one point each across the first `remainder` factors so every factor lands within 1 point of every other.
  </context>

  <scope>
    <step>Phase 1 -- the fix is fully specified by CTO; apply it to `portal/src/pages/SecurityScanner/hooks/useScannerState.ts` `buildEqualWeights()`:
      - Line ~40, REPLACE:  `result[f.code] = i === 0 ? base + remainder : base`
        WITH:               `result[f.code] = i < remainder ? base + 1 : base`
      - Line ~32 docstring, REPLACE the "remainder to first" phrasing WITH: "remainder spread one point each across the first `remainder` factors".
      Verify the line numbers against the live file before editing (they are approximate). Touch ONLY buildEqualWeights() -- no other function, no other file.
      Arithmetic check: 13 factors -> base = floor(100/13) = 7, remainder = 100 - 91 = 9 -> factors 0-8 get 8, factors 9-12 get 7 -> 9x8 + 4x7 = 100, every factor within 1 point.
    </step>
    <step>Phase 2 -- run the compiler mandate (tsc + lint + /frontend-dev smoke). Commit via `.tools/safe-commit.sh` (DE author, or RD serial if RD implements). Portal DEV push is a DT lane action -- DT 0.3.0 folds this commit into the .006 PROD bundle (do NOT do a separate PROD push).</step>
    <step>Phase 3 (RAVC2) -- to 2.0.0_SA_COO + CC 1.0.0_SA_CTO with AC1-AC4 evidence + the commit SHA. TO status -> complete on RAVC2 send. CC DT 0.3.0 so the commit joins the .006 bundle.</step>
  </scope>

  <acceptance_criteria>
    <ac id="AC1">Clicking Equal Weight on the 13-factor DIVZ preset yields nine factors at 8% and four factors at 7%, summing to exactly 100. Observed in DEV (or asserted via the function's output for 13 inputs).</ac>
    <ac id="AC2">No factor's equal-weight value is more than 1 point off any other factor's (max - min &lt;= 1).</ac>
    <ac id="AC3">`/frontend-dev` smoke green.</ac>
    <ac id="AC4">`bun run typecheck` (tsc) clean and `bun run lint` clean.</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>(none -- pure-logic helper function; comp-transform schema-check not applicable, no rendered-field change)</run>
        <expect>N/A -- documented per CTO: this is a 2-line logic fix, no schema surface.</expect>
        <if_mismatch>N/A</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>bun run typecheck</run>
        <expect>tsc exits clean (0 errors).</expect>
        <if_mismatch>Fix before commit.</if_mismatch>
      </step>
      <step>
        <run>bun run lint</run>
        <expect>lint exits clean.</expect>
        <if_mismatch>Fix before commit.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>/frontend-dev smoke</run>
        <expect>Smoke green; Equal Weight on the DIVZ preset shows the spread distribution (nine 8s + four 7s).</expect>
        <if_mismatch>Iterate until AC1/AC2 hold.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    The commit joins the SSCN_DIVDEF.006 PROD bundle (.007 + .008 + .010 + .011). DT 0.3.0 folds it in -- this TO does NOT trigger its own PROD push. No file overlap with .009 (Lambda/registry) or any other in-flight TO -- touches only useScannerState.ts buildEqualWeights(). Sequencing: CTO gates the GO on Andrew's hold-vs-ship ruling.
  </cross_domain_coordination>

  <deliverables>
    - The 2-line buildEqualWeights() fix on portal DEV.
    - Session log under org/tier2_senior/0.3.0_DE_TradingOperations/logs/YYYY-MM-DD/ with AC1-AC4 evidence + commit SHA + Compiler Tools section.
    - RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO + CC 0.3.0_DT_TradingOperations on close; TO status -> complete on RAVC2 send.
  </deliverables>

  <do_not>
    <rule>Do NOT touch any function other than buildEqualWeights(), and no file other than useScannerState.ts.</rule>
    <rule>Do NOT do a separate PROD push -- the commit folds into the .006 bundle (DT lane).</rule>
    <rule>Do NOT start before CTO's GO -- the sequencing awaits Andrew's hold-vs-ship ruling on .006.</rule>
    <rule>No emojis in code, commit messages, or the session log (CLAUDE.md ASCII-only rule).</rule>
  </do_not>
</task_order>
