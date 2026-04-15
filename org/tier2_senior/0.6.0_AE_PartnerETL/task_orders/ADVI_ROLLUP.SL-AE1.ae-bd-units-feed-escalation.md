<task_order>
  <metadata>
    <id>ADVI_ROLLUP.SL-AE1</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-04-15</date>
    <status>staged</status><!-- Independent of in-flight work; Andrew GO when AE has bandwidth post-W7 + DH series -->
    <project_code>ADVI_ROLLUP</project_code>
    <wave>4 (Structural convergence — sleeve quantity-source primary path)</wave>
    <priority>P2 (Path 1 primary; Path 3 cost-basis apportionment is fallback in flight via SL-P0)</priority>
  </metadata>

  <references>
    <ref type="trigger">SL-P0 base DS decision memo 2026-04-15 — Path 3 cost-basis chosen for cohort, parallel Path 1 escalation to AE preferred</ref>
    <ref type="related">SL-P0 sleeve discovery (base DS, in flight)</ref>
    <ref type="prd">docs/architecture/ADVI_SLEEVE_PLAN.md</ref>
  </references>

  <objective>
    Escalate to BD (Black Diamond partner) for a daily Units feed in `Fees_OpalCapital_Daily` xlsx export OR a new dedicated export. This is the cleaner quantity-source path for sleeve member identification — DS chose Path 3 cost-basis apportionment as fallback because Units is not currently in our data feed.

    **Tasks:**

    1. **Identify the BD contact** (account manager, integrations contact, partner support email). Search prior emails/threads/Slack for the BD relationship contact. Document the route.

    2. **Draft the request** — short, technical, evidence-based:
       - What we have today (Fees_OpalCapital_Daily columns enumerated)
       - What we need (Units column per security per account per date)
       - Why it matters (sleeve member identification, currently using cost-basis apportionment as proxy)
       - Format ask (extend existing xlsx with new column? new daily csv? S3 drop?)

    3. **Send the request** via the established channel. Cc relevant Opal stakeholders (Andrew + COO).

    4. **Track the response** — open a GitHub issue or org tracking entry. Report back to COO + CTO when BD responds.

    **Out of scope:** building the ingestion path. That's a follow-on TO once BD agrees to the feed and provides a sample.

    **Deliverable:** a session log entry documenting the contact, the request sent (full text), and the channel used. No code changes in this TO.
  </objective>

  <scope>
    <files>
      <file action="create_optional">org/tier2_senior/0.6.0_AE_PartnerETL/correspondence/2026-04-{XX}_bd_units_feed_request.md (the drafted request)</file>
    </files>
  </scope>

  <wire_contract>
    No code change. No S3 write. External communication only.
  </wire_contract>

  <acceptance_criteria>
    1. BD contact identified and documented.
    2. Request drafted and sent.
    3. Response tracked (open ticket / thread / log entry).
    4. MCP COMPLETE to COO + CTO with: contact name, channel used, request text, expected response timeline.
    5. Session log entry with the correspondence trail.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before contact">
      <step>
        <run>head -3 data/black_diamond/source/Fees_OpalCapital_Daily*.xlsx 2>/dev/null || aws s3 ls s3://opal-data-bd/source/Fees_OpalCapital_Daily/ | tail -3</run>
        <expect>Locate a recent xlsx; confirm what columns exist today.</expect>
        <if_mismatch>If file not found, surface to COO before drafting request (cannot describe "what we have" without it).</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="after contact sent">
      <step>
        <run>cat org/tier2_senior/0.6.0_AE_PartnerETL/correspondence/2026-04-{XX}_bd_units_feed_request.md</run>
        <expect>Request text on disk, committed.</expect>
        <if_mismatch>Re-commit.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    <none/>
  </dependencies>

  <next>
    BD response → if YES: follow-on TO to ingest the new feed into silver/units/. If NO/delay: SL-P0 Path 3 cost-basis remains primary indefinitely; document in SLEEVE plan.
  </next>
</task_order>
