<task_order>
  <metadata>
    <id>0.4.0_DE_ClientPlatform-2026-04-14-profau-007</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-14</date>
    <status>complete</status>
    <project_code>ADVI_PROFAU</project_code>
  </metadata>

  <references>
    <ref type="audit">docs/audits/advisor-profile-book-input-mapping-2026-04-13.md</ref>
    <ref type="ds_prep">DS PROFAU.007 prep message 20260414T160556Z — is_fee_paying confirmed live</ref>
  </references>

  <dependencies>
    <dependency agent="0.4.0_DT_ClientPlatform"
                task="ADVI_OFFICE.W4.dt-portal-deploy + ADVI_PROFAU.006 follow-on push"
                status="pending"
                description="Complete the W4 + .006 deploy sequence before starting .007. No data dependency — is_fee_paying is live in platinum now."/>
  </dependencies>

  <objective>
    Add is_fee_paying to the AdvisorClient TypeScript type and wire a fee-paying / non-fee-paying
    client count split display at L2 in AdvisorBookView. Data is already live — this is a pure
    portal type + render change.
  </objective>

  <context>
    DS investigation confirmed: `is_fee_paying: bool` is emitted on every entry in
    `book.clients[]` inside `platinum/advisors/{slug}/summary.json`. Delivered in
    PROFAU.002 (f2507121), NaN bug fixed (b0ad9811). No gold re-run needed.

    Verified against Sydney Cobb summary.json:
      book.clients.length = 241
      is_fee_paying true  = 28
      is_fee_paying false = 213

    comp-transform shows `clients: AdvisorClient[]` is currently UNUSED in AdvisorBookView
    (declared in PlatinumAdvisorSummary but never rendered). This TO wires it.

    Blast radius (comp-blast AdvisorBookView): 3 endpoints + opal-partners-data Lambda.
    4 nodes — same baseline as PROFAU.004/.005. Isolated, no cross-pod impact.
  </context>

  <scope>
    <change id="1">
      <file>portal/src/pages/AdvisorIntelligence/types.ts</file>
      <action>Add is_fee_paying field to AdvisorClient interface</action>
      <detail>
        Current: AdvisorClient = { client_key: string; client_name: string; aua: number; ... }
        Add: is_fee_paying?: boolean
        (Optional to guard against any older cached artifacts missing the field)
      </detail>
    </change>

    <change id="2">
      <file>portal/src/pages/AdvisorIntelligence/AdvisorBookView.tsx</file>
      <action>Wire L2 client count split — fee-paying vs non-fee-paying</action>
      <detail>
        Source: advisorSummary.book.clients (PlatinumAdvisorSummary.book.clients: AdvisorClient[])
        Derive at render time:
          const feePayingCount = book.clients.filter(c => c.is_fee_paying).length
          const nonFeePayingCount = book.clients.length - feePayingCount
        Display at L2 book header alongside existing client_count:
          "28 fee-paying / 213 non-fee-paying" (or similar format — check existing L2 layout)
        Null-safe: guard on book.clients?.length > 0 before rendering split.
      </detail>
    </change>
  </scope>

  <compiler_tools_mandate>
    <phase name="before_write">
      Set context: printf "SERIAL=0.4.0_DE_ClientPlatform\nTO_ID=ADVI_PROFAU.007\n" > .comp-graph/.agent_context
      <run>comp-transform schema-check AdvisorBookView</run>
      <expect>clients: AdvisorClient[] UNUSED — confirms field not yet rendered. AdvisorClient type visible.</expect>
      <run>comp-blast AdvisorBookView</run>
      <expect>4 downstream nodes: 3 endpoints + opal-partners-data Lambda. Unchanged from .004/.005 baseline.</expect>
    </phase>

    <phase name="before_commit">
      <run>bun run build (or bunx tsc -b)</run>
      <expect>0 TypeScript errors. is_fee_paying: boolean? accepted on AdvisorClient.</expect>
      <run>comp-transform schema-check AdvisorBookView</run>
      <expect>clients: AdvisorClient[] moves from UNUSED to rendered (or at minimum is_fee_paying consumed).</expect>
    </phase>

    <phase name="after_commit">
      <run>comp-blast AdvisorBookView</run>
      <expect>Still 4 downstream nodes — no new dependencies introduced.</expect>
      Append row to org/compiler-tools-log.md.
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <none/>
    No shared S3 keys or artifacts modified. Data is read-only from existing platinum path.
    No other active TOs touch AdvisorBookView or AdvisorClient type.
  </cross_domain_coordination>

  <acceptance_criteria>
    1. AdvisorClient type declares is_fee_paying?: boolean in types.ts.
    2. AdvisorBookView L2 renders fee-paying count and non-fee-paying count from book.clients.
    3. Spot-check Sydney Cobb on PROD (after DT push): fee-paying = 28, non-fee-paying = 213.
    4. TypeScript build clean (0 errors).
    5. comp-blast AdvisorBookView: 4 nodes unchanged.
    6. MCP message to 2.0.0_SA_COO on completion.
    7. Session log with compiler tools section.
  </acceptance_criteria>

  <deliverables>
    - types.ts: AdvisorClient.is_fee_paying added.
    - AdvisorBookView.tsx: L2 client fee-paying split rendered.
    - Portal DEV commit.
    - Session log with compiler tools section.
    - MCP to COO.
  </deliverables>
</task_order>
