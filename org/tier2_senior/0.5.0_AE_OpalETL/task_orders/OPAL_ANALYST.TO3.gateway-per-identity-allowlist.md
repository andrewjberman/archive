# OPAL_ANALYST.TO3 — Server-side per-identity tool allowlist at m365-mcp-gateway

<task_order>
<id>OPAL_ANALYST.TO3</id>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued_to>0.5.0_AE_OpalETL~Z</issued_to>
<date>2026-08-10</date>
<status>staged</status>
<priority>P1</priority>

<references>
  <ref type="prd">docs/architecture/OPAL_ANALYST_PRD.md §4.3, §6 TO-3, §7 Q3 (v1.0 @d179643ca)</ref>
  <ref type="posture">opal-bloomberg key = WRITE_CAPABLE/STANDARD_EMPLOYEE @798cff68b — catalog + client fence are today the entire fence</ref>
</references>

<scope>
Extend the `m365-mcp-gateway` tier/entitlement layer (`infra/aws/ec2/m365-mcp-gateway/app/`) so the
SERVER enforces per-identity tool scope for the `opal-bloomberg` identity: allow exactly the
concierge's needed set (Teams read/send on its own account; portal read path only once PRD §7 Q1
activates), deny the rest server-side with a structured refusal the agent can quote (the 08-07
tier-guard denial is the model). This is MECHANICAL enforcement of an existing entitlement
boundary — NOT a new approval gate on work (no-gates law untouched). Andrew's key is a control:
unaffected.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>Enumerate the concierge's actual tool needs from refs/REQUEST_CATALOG.md + /bbg-teams-assist SKILL.md; .tools/comp-find "tier" infra/aws/ec2/m365-mcp-gateway/app (tier-check call sites)</run>
      <expect>A finite named tool list, each row justified by a catalog/skill line; all tier-check call sites located.</expect>
      <if_mismatch>STOP. An allowlist you cannot derive from the catalog is a guess; surface to CTO~Z.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="deploy">
    <step>
      <run>Deploy per EC2 standard: local → S3 artifact → safe-ec2-deploy.sh (never write code on the VM, never inline in SSM)</run>
      <expect>Deploy path per docs/deployment/EC2_CODE_DEPLOYMENT_STANDARD.md; EC2_MANIFEST.json entry current.</expect>
      <if_mismatch>STOP. Non-standard EC2 deploy path is a NEVER-rule adjacency; do not improvise.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after deploy">
    <step>
      <run>EXERCISE (separate invocations, Rule 22a): (a) a DENIED tool from the opal-bloomberg key; (b) an ALLOWED tool from the same key; (c) control — same denied tool from Andrew's key</run>
      <expect>(a) structured refusal naming the policy; (b) passes; (c) Andrew's key unaffected.</expect>
      <if_mismatch>Surface to COO~Z + CTO~Z. A config-read is not a behavioral claim — only the exercised path counts.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
Gateway app/ is shared with every gateway consumer (opal-gateway + opal-gateway-bbg on multiple
devices). The tier check must key on IDENTITY, not on tool globally — a global tool disable would
hit Andrew's own key (the Phase-3 control exists for exactly this). No other open TO touches
the gateway tree on this fabric.
</cross_domain_coordination>

<acceptance_criteria>
1. Denied-tool call from `opal-bloomberg` returns a structured, quotable refusal (exercised, output
   in log).
2. Allowed set passes (exercised).
3. Andrew's key control unaffected (exercised, separate invocation).
4. Allowlist CONTENT carries CTO~Z plan-review sign-off before deploy (gate below).
5. Session log Compiler Tools section reproduces each <run> with observed output vs <expect>.
</acceptance_criteria>

<notes>
STAGED — gate state as of 2026-08-10 1644Z:
(a) CTO~Z plan review: **CLEARED** (delivered 20260810T164421Z, broker msg on record). The
    APPROVED FRAME is binding on Phase 1's derived list:
    (i) deny-by-default: an ALLOWLIST of named tools, never a denylist;
    (ii) allowed now: whoami + Teams own-account serve set (poll_addressed_teams_messages,
    chat list/read/send; channel list/read/send ONLY if the REQUEST_CATALOG derivation
    justifies a channel row — if the catalog is chat-only, channels stay denied);
    (iii) denied explicitly regardless of derivation: email send/reply/draft,
    site/OneDrive/SharePoint writes + upload_text_to_site + save_email_attachment_to_site,
    opal_data_refresh_upload, ALL ycharts_* (vendor egress needs Andrew per-use word
    independently), any Bloomberg download-class surface;
    (iv) post-Q1 only: portal read path added later as a second reviewed row-set, NOT
    pre-wired dormant;
    (v) Andrew's key (opal-gateway identity) untouched — the Phase-3 control proves it.
    ONE-PASS DISPOSITION: a derived list fitting frame (i)-(v) is APPROVED AS DERIVED
    (attach the derivation as evidence, no second review round); only a row OUTSIDE the
    frame returns to CTO~Z, and only that row.
(b) PRD §7 Q3 at Andrew: **CLEARED** — Andrew-direct 2026-08-10 ~1653Z at the CTO~Z terminal,
    "All recs approved, proceed" (record @bc7eb60de): Q3 RATIFIED AS PROPOSED (Teams read/send
    own-account + post-Q1 portal read, all else denied).
Q1 RULING FOLDED IN (same record): portal-bucket READ entitlement on `opal-gateway-bbg` is
ACTIVATED by his word — it lands mechanically via THIS TO's deploy as the frame's clause-(iv)
second row-set (its own derivation evidence attached, same one-pass disposition). YCHARTS
STAYS HELD — per-use egress regime unchanged; all ycharts_* remain in the explicit-deny rows.
ALL GATES CLEAR — GO sent 2026-08-10 (see broker record). Effort: medium.
</notes>
</task_order>
