<task_order>
  <metadata>
    <id>YALP_MDSRC.V1A</id>
    <slug>ds-4-bond-representative-ycharts-index</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.1.0_DS_MarketIntelligence</issued_to>
    <date>2026-05-21</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <!-- COMPLETE 2026-05-22 by 0.1.0_DS_MarketIntelligence. 1 of 4 bands resolved (0-1Yr Treasury -> Bloomberg US Treasury Bills 1-3 Month ^BBUTB13MTR, depth-confirmed); 3 escalated to COO -- YCharts carries no Bloomberg maturity-band index for HY-short / TIPS-short / 20+yr-Treasury-pure (maturity-band coverage there is ICE-vendored). Deliverable: docs/briefs/mdsrc-v1a-4-bond-representative-index-20260522.md. C2 pull-spec 4 rows corrected. RAVC2 to COO CC CTO. -->

    <dispatch_unblock_condition>GO ON PICKUP — a small V1 addendum. Andrew re-ruled the 4 Bloomberg maturity-band bonds (2026-05-21, via CTO): NEITHER the ETF-proxy NOR manual-Bloomberg — instead find a representative Bloomberg bond index that YCharts carries. This SUPERSEDES the ETF-proxy resolution 0.1.0_DS folded into the C2 pull-spec; V1A produces the corrected resolution. Small/bounded — runs alongside or right after M2 (your primary).</dispatch_unblock_condition>
    <project_code>YALP_MDSRC</project_code>
    <priority>P1 — corrects 4 rows of the C2 pull-spec that currently carry the Andrew-rejected ETF-proxy resolution. Small task, but the pull-spec is wrong until it lands.</priority>
    <sla>~0.5 effort-day — 4 representative-index lookups on the YCharts entity surface.</sla>
  </metadata>

  <references>
    <ruling>Andrew 2026-05-21 (via CTO), verbatim: "we find a bloomberg index that is representative of those or very similar that ycharts does have, which ycharts surely can oblige." Andrew explicitly REJECTED both the ETF-proxy and the manual-Bloomberg options.</ruling>
    <v1>YALP_MDSRC.V1 — the completed 76-entity history-verification + the C2 pull-spec (docs/briefs/mdsrc-c2-pull-spec-prestage-20260521.csv). V1A corrects the 4 maturity-band-bond rows.</v1>
    <prior_finding>V1 established YCharts carries NO index for any of the 4 EXACT maturity bands. V1A's task is the next step Andrew directed — the closest REPRESENTATIVE index, not an exact-band match.</prior_finding>
  </references>

  <context>
    The 4 Bloomberg maturity-band bonds — Bloomberg 0-1 Year Treasury, 0-5 Year High Yield, 0-5 Year TIPS, 20+ Year Treasury — were the only entities of the 76 not directly YCharts-replaceable. The interim ETF-proxy resolution (SHV/SHYG/STIP/TLT) is now SUPERSEDED — Andrew rejected it. His ruling: for each, find the closest REPRESENTATIVE Bloomberg bond index that YCharts DOES carry — same or very similar maturity band + credit quality. YCharts carries many Bloomberg fixed-income indices; the exact 4 bands aren't among them, but a representative neighbor should be.
  </context>

  <scope>
    <in_scope>
      - For EACH of the 4 maturity-band bonds: search the YCharts entity surface (/search/suggest/main + the index taxonomy) for the closest REPRESENTATIVE Bloomberg bond index YCharts carries — closest maturity band + matching credit quality (Treasury / High Yield / TIPS).
      - Per band, document the REPRESENTATIVENESS BASIS: the maturity-band overlap (e.g. "Bloomberg 1-3yr Treasury vs the 0-1yr target — adjacent short band"), the credit-quality match, and the residual basis difference.
      - Depth-confirm the chosen representative index on YCharts (clean daily series, adequate history) — verification-scope, mchm login.
      - Output: the corrected C2 pull-spec rows for the 4 (replacing the ETF-proxy resolution) + a short brief documenting each representative-index choice + basis.
      - If a band genuinely has NO reasonable representative Bloomberg index on YCharts — do NOT force a bad match; ESCALATE that band back to COO with the finding (Andrew's expectation is one exists, but verify per-band).
    </in_scope>
    <out_of_scope>
      - The ETF-proxy approach (SHV/SHYG/STIP/TLT) — Andrew rejected it; do not use it.
      - Manual-Bloomberg — Andrew rejected it.
      - The other 72 entities — V1 closed them.
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
    <note>V1A is a small YCharts-entity sourcing task — no gold/portal/route/IAM/schema change; no comp-* graph tool applies. The assertions are empirical self-checks.</note>
    <phase id="1" when="per representative-index candidate">
      <step>
        <run>For each of the 4: pull the candidate representative index live on YCharts and confirm it returns a clean daily series with adequate history.</run>
        <expect>Each chosen representative index returns HTTP 200, daily cadence, history depth past the ~6yr backbone — measured, not assumed.</expect>
        <if_mismatch>If a candidate doesn't return a usable series, it is not a valid representative — pick the next-closest or escalate the band.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before declaring complete">
      <step>
        <run>Verify each of the 4 representative choices has a documented representativeness basis (maturity-band overlap + credit-quality match + residual basis).</run>
        <expect>4 documented choices, OR fewer-than-4 with the remainder explicitly escalated as no-representative-found.</expect>
        <if_mismatch>An undocumented "representative" choice is not acceptable — the basis is what makes it defensible.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - Corrects 4 rows of the C2 pull-spec (docs/briefs/mdsrc-c2-pull-spec-prestage-20260521.csv) — the ETF-proxy resolution + the etf_proxy_disclosure field on those 4 rows are removed, replaced by the representative-Bloomberg-index resolution. Honest labeling still applies — the portal series should note it's a representative index, not the exact requested band.
    - F1 single YCharts seat — verification-scope, mchm login; coordinate seat use if M2 or other YCharts work overlaps.
  </cross_domain_coordination>

  <acceptance_criteria>
    - AC1 — each of the 4 maturity-band bonds resolved to a representative Bloomberg bond index that YCharts carries (or explicitly escalated as no-representative-found).
    - AC2 — per band: the representativeness basis documented (maturity-band overlap, credit-quality match, residual basis difference).
    - AC3 — each chosen representative index depth-confirmed live (Phase-1: HTTP 200, daily, adequate history).
    - AC4 — the C2 pull-spec's 4 maturity-band-bond rows corrected (ETF-proxy resolution removed); short brief committed; RAVC2 to COO + CC CTO.
  </acceptance_criteria>
</task_order>
