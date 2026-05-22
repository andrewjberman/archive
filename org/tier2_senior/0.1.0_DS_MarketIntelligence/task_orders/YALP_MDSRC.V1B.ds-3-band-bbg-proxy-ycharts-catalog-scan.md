<task_order>
  <metadata>
    <id>YALP_MDSRC.V1B</id>
    <slug>ds-3-band-bbg-proxy-ycharts-catalog-scan</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.1.0_DS_MarketIntelligence</issued_to>
    <date>2026-05-22</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <!-- COMPLETE 2026-05-22 by 0.1.0_DS_MarketIntelligence. All 3 bands resolved to a representative Bloomberg-origin YCharts index: 0-5Yr HY -> ^BBUSCOHYTR, 0-5Yr TIPS -> ^BBUTISTR, 20+Yr Treasury -> ^BBUSLGCRTR. All depth-confirmed live. Deliverable: docs/briefs/mdsrc-v1b-3-band-bbg-proxy-20260522.md. C2 pull-spec 3 rows corrected -- pull-spec now 76/76 complete. RAVC2 to COO CC CTO. -->

    <dispatch_unblock_condition>GO ON PICKUP — Andrew ruling 2026-05-22 on the V1A 3-band escalation. V1A resolved 1 of 4 bands and escalated 3 (0-5Yr High Yield, 0-5Yr TIPS, 20+Yr Treasury) because YCharts carries no Bloomberg maturity-BAND index for them. Andrew's ruling: do NOT go ICE cross-vendor and do NOT keep them on the pkl — scan the available Bloomberg indices on YCharts and find a representative BBG-origin proxy per band. Bounded; runs in parallel — does not need C1.</dispatch_unblock_condition>
    <project_code>YALP_MDSRC</project_code>
    <priority>P1 — closes the last 3 open rows of the C2 pull-spec. C2 itself is staged on C1, but the pull-spec must be correct and complete before C2 builds against it.</priority>
    <sla>~0.5 effort-day — a YCharts Bloomberg fixed-income catalog scan + 3 representative picks + pull-spec update.</sla>
  </metadata>

  <references>
    <ruling>Andrew 2026-05-22, verbatim: "Need to scan the available bloomberg indexes that are available on YCharts and find a BBG proxy on the same platform. It is not essential that we have the exact same index, as long as its representative of that duration concept and is BBG in origin."</ruling>
    <v1a>YALP_MDSRC.V1A — complete. Resolved band 1 (Bloomberg 0-1Yr Treasury -> ^BBUTB13MTR). Brief: docs/briefs/mdsrc-v1a-4-bond-representative-index-20260522.md. V1B closes the 3 V1A escalated.</v1a>
    <v1a_finding>V1A established YCharts' Bloomberg maturity-BAND coverage = US Government/Credit family (1-3yr, 1-5yr) + Municipal bands + the 1-3mo T-Bill index. V1B's task is to look BEYOND the maturity-band family — the broad Bloomberg HY / TIPS / long-Treasury indices YCharts carries — for a representative-of-the-duration-concept BBG proxy.</v1a_finding>
  </references>

  <context>
    Three bond bands have no exact Bloomberg maturity-band index on YCharts: 0-5Yr High Yield, 0-5Yr TIPS, 20+Yr Treasury. Andrew has ruled the resolution stays Bloomberg-origin and on YCharts — the exact maturity band is NOT required, only that the chosen index is (a) Bloomberg in origin, (b) representative of the duration/segment concept, (c) carried by YCharts. ICE cross-vendor indices are explicitly OUT (rejected this ruling). The pkl is OUT (Andrew rejected manual). V1A's search was scoped to the maturity-band family and came up empty; V1B widens the scan to the full Bloomberg fixed-income index catalog on YCharts.
  </context>

  <scope>
    <in_scope>
      - Scan the YCharts Bloomberg fixed-income index catalog (/search/suggest/main + the index taxonomy) for ALL Bloomberg-origin indices in the High Yield, TIPS/inflation-linked, and long-Treasury segments — not just maturity-band variants.
      - For EACH of the 3 bands, pick the most representative Bloomberg-origin index YCharts carries: closest on the duration/segment concept (short-duration HY; TIPS/inflation-linked; long-Treasury) and matching credit quality.
      - Per band, document the REPRESENTATIVENESS BASIS: how the chosen index maps to the target duration concept, the credit-quality match, and the residual difference (e.g. "broad Bloomberg US Corporate HY vs the 0-5yr-HY target — full-maturity HY, not short-banded; residual = longer average duration").
      - Depth-confirm each chosen index live on YCharts (HTTP 200, clean daily series, adequate history) — verification scope, mchm login.
      - Update the 3 rows of the C2 pull-spec (docs/briefs/mdsrc-c2-pull-spec-prestage-20260521.csv) with the representative BBG-index resolution + honest representative labeling.
      - Output: a short brief documenting the catalog scan + each of the 3 representative-index choices + basis.
    </in_scope>
    <out_of_scope>
      - ICE cross-vendor indices — Andrew ruled BBG-origin only.
      - The Bloomberg pkl / manual sourcing — Andrew rejected manual.
      - ETF proxies — Andrew rejected proxies.
      - Band 1 (0-1Yr Treasury) — V1A resolved it.
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
    <note>V1B is a YCharts-entity sourcing task — no gold/portal/route/IAM/schema change; no comp-* graph tool applies. Assertions are empirical self-checks.</note>
    <phase id="1" when="per representative-index candidate">
      <step>
        <run>For each of the 3: pull the candidate Bloomberg index live on YCharts and confirm a clean daily series with adequate history.</run>
        <expect>HTTP 200, daily cadence, history depth past the ~6yr backbone — measured, not assumed.</expect>
        <if_mismatch>A candidate that doesn't return a usable series is not valid — pick the next-closest Bloomberg index.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before declaring complete">
      <step>
        <run>Verify each of the 3 choices is Bloomberg-origin, YCharts-carried, and has a documented representativeness basis.</run>
        <expect>3 documented Bloomberg-origin choices.</expect>
        <if_mismatch>If a band genuinely has NO reasonable Bloomberg-origin representative on YCharts even after the full-catalog scan, do NOT force a bad match and do NOT fall back to ICE — escalate that single band back to COO with the catalog evidence.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - Corrects the final 3 rows of the C2 pull-spec (docs/briefs/mdsrc-c2-pull-spec-prestage-20260521.csv). Honest labeling applies — the portal series notes it is a representative Bloomberg index, not the exact requested band.
    - F1 single YCharts seat — verification scope, mchm login; coordinate seat use if other YCharts work overlaps.
    - C2 (staged, gated on C1) consumes the completed pull-spec; V1B does not itself depend on C1.
  </cross_domain_coordination>

  <acceptance_criteria>
    - AC1 — each of the 3 bands (0-5Yr HY, 0-5Yr TIPS, 20+Yr Treasury) resolved to a representative Bloomberg-origin index that YCharts carries.
    - AC2 — per band: representativeness basis documented (duration-concept mapping, credit-quality match, residual difference).
    - AC3 — each chosen index depth-confirmed live (Phase-1: HTTP 200, daily, adequate history).
    - AC4 — the C2 pull-spec's 3 rows corrected; short brief committed; RAVC2 to COO + CC CTO.
  </acceptance_criteria>
</task_order>
