<task_order>
  <metadata>
    <id>2.0.0_SA_COO~Z-2026-08-07-canplat-v3</id>
    <issued_by>2.0.0_SA_COO~Z</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~Z</issued_to>
    <date>2026-08-07</date>
    <status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project MDPF_CANPLAT, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: pending</status>
    <project_code>MDPF_CANPLAT</project_code>
    <governing>VALIDATION PRD @2dedd8f6a §2 V-3 (rubric rows V9/V10/V11 — V12 is NOT in this TO, it needs R3's cutover + the deployed edge) · PRD §0 binds · V-series MEASURES ONLY</governing>
    <capability_basis>portal repo now LOCAL at ajb_workspace/portal/ @DEV 604101df, 403 src files, clean tree (Andrew-direct via MSTR~Z 005808Z). The V-PRD's "cannot be done from here" limit was measured BEFORE this clone and is CLOSED. ⛔ portal/ is READ-ONLY REFERENCE — Rule 19 (main tree stays on DEV), no portal-write scope exists on this program.</capability_basis>
  </metadata>

  <standing_instruction>
    ⛔ PRD §0 BINDS, VERBATIM FORCE (full text in your P1-1 TO @f123fbf6e): VALIDATE WHAT IS DESCRIBED,
    DO NOT HUNT ERRORS. **V-series MEASURES ONLY — a component that would break is a NAMED VERDICT in
    your deliverable and a SURPRISE-CHANNEL line to 2.0.0_SA_COO~Z, never a frontend fix** (portal is
    DT/portal-lane; you have no write scope there and need none). Two stale-comment nits MSTR~Z already
    recorded (portal-proxy.ts:421 backing-key comment; :417 DEMO-MODE TODO) are KNOWN — cite, don't
    re-derive, don't chase.
  </standing_instruction>

  <objective>
    V-3, the program's real residual risk (CTO~Z: "key stability is not component compatibility"):
    census the portal components consuming the three MDPF artifact types and deliver a NAMED CONSUMER
    VERDICT for every added or newly-nullable §B field — the one way this build can break a working
    portal without moving a single key.
  </objective>

  <requirements>
    <requirement id="V9">CENSUS, DENOMINATOR PRINTED: every portal component reading the three artifact
    types (aggregate-aua-timeseries, aum-metrics, account-distribution), per scope, from
    portal/src @604101df. Print files-scanned as the denominator (403 src files is the baseline count).
    Use the comp rail now that it resolves on this device: comp-routes frontend bindings,
    comp-transform fields for each consuming component, comp-cache for the queryKey layer; comp-grep
    for the residue. MSTR~Z's source pass (005808Z: portal-proxy.ts constructs the scoped hyphen paths
    ONLY; zero fetches of archived keys or underscore twins) is ADOPTED as prior evidence — verify by
    citation, extend to the COMPONENT layer (who consumes what the proxy returns).</requirement>
    <requirement id="V10">PER-FIELD VERDICTS: for every added or newly-nullable field in CONTRACT §B
    (as amended @9c36d33bf + the no-carve-outs ruling @6c50710af), a named verdict — SAFE / BREAKS /
    NO-CONSUMER — with the consuming component + line cited. The enumerated field set: `basis` + `source`
    newly NULL at global (the sharpest case: any `data.basis.<method>()` on null); `firm_id`/`firm_name`
    newly present at global; `meta` + `meta.account_count_by_model_key` newly present at 49financial;
    `total.account_units` folded into account-distribution on ALL FOUR scopes; non-model detail folded
    into aum-metrics AND aggregate-aua-timeseries (real at global, honest-null at firms); W-1's three
    fields newly present at cottonwood (`account_count_total`, `count_provenance`, `source_vintage_last`);
    the five §B3 fields per DS's own ruled classification (canonical-for-all, honest absence at firm
    scope). A verdict of NO-CONSUMER is a real verdict and carries its denominator.</requirement>
    <requirement id="V11">LEGACY BELL UNAFFECTED: the unscoped legacy consumer reads `json/mdpf/`
    (untouched by the R-series, D9) — confirm from source which component that is and that its read
    path carries no §B-changed field. MSTR~Z's fact 2 (the non-model display fetches the LEGACY
    json/portfolios family at portal-proxy.ts:417, NOT the platinum standalone) is adopted as input —
    fold it into the verdict table; it is the surface that actually feeds that component today, and the
    eventual extras-retirement TO will need it stated.</requirement>
  </requirements>

  <do_not>
    <rule>⛔ portal/ is READ-ONLY. No edits, no checkouts off DEV, no branch changes, no bun installs.
    A lingering CWD in portal/ is itself a defect (XXX.md Step 1a) — address it as `git -C portal` /
    scoped reads and return to the workspace root.</rule>
    <rule>NO frontend fixes, however small — incl. the two known stale comments. Verdicts, not patches.</rule>
    <rule>V12 (edge rewrite on the DEPLOYED edge version, post-cutover) is NOT yours and NOT now.</rule>
    <rule>NO error-hunting (§0). SURPRISE: line to COO~Z, then continue. Lane commits only; push is
    MSTR~Z's; scratchpad for working files.</rule>
  </do_not>

  <deliverables>
    <deliverable type="document">V9 census (components x artifact-types x scopes, denominator printed) + V10 per-field verdict table (field → consumer → SAFE/BREAKS/NO-CONSUMER, cited to file:line @604101df) + V11 legacy-bell verdict</deliverable>
    <deliverable type="document">Session log with a Compiler Tools section</deliverable>
  </deliverables>
</task_order>
