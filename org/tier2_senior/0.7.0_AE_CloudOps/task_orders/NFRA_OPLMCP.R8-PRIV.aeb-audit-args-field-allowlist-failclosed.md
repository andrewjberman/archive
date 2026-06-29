# TASK ORDER — NFRA_OPLMCP.R8-PRIV

<issued_to>0.7.0_AE_CloudOps~B</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>complete</status>
<!-- CLOSED 2026-06-29 (0.7.0_AE_CloudOps~B). ALL 4 ACs met. AC1+AC2 unit-proven (5 fail-closed assertions, 838d8790b). AC3 schema CVO-verified. AC4 served-verify CVO-SIGNED (192401Z): base deployed the gateway (on-box md5=440b6f08 == committed); CVO independently ran NEVER#7 on the LIVE gateway -- called list_recent_email (UNDECLARED, content-bearing) which returned a REAL sensitive email (subject "Confirming Allocation", account 3589-3056, allocation), and the Athena mcp_audit row (19:21:23Z) showed args={"_omitted":"args fail-closed (tool not in R8-PRIV allowlist)"} -- ZERO leak (no subject/body/account/sender), metadata-only. Regression: whoami (declared) still logs args {} normally. The fail-closed-by-default works at the SERVED layer, proven against a real content tool. STRUCTURALLY CLOSES the R8 P2 forward-looking privacy gap. GATE LIFTS: the 3-tool scope-hold was the interim; ANY tool is now safe-by-fail-closed -> the OPLMCP audit scope can expand (a new/content tool's args fail-closed-omit until explicitly declared metadata-safe + CVO-schema-verified). -->
<!-- ORIGINAL: active -- BUILT, awaiting base-AE deploy + CVO served-verify (AC4) -->
<!-- PROGRESS 2026-06-29 (0.7.0_AE_CloudOps~B): code BUILT + committed 838d8790b (gateway audit.py _safe_args). AC1 (fail-closed per-tool field allowlist, default-OMIT, no-schema-tool->args-omitted) + AC2 (256-char length-cap backstop) DONE -- 5 unit assertions pass (declared-keep, otp-VALUE-omit, read_email-args-omit, cap, whoami-empty). AC3 current-3-tools schema (ms_site_children:{site_id,folder_path}, otp_fetch:{sender,found}, whoami:{}) CVO-pre-verified in the R8 close; future content-tools (read_email/send_email/read_file) stay fail-closed-OMITTED until declared+CVO-schema-verified at scope-expansion. REMAINING: base-AE gateway DEPLOY (S3->EC2->restart; coordinated) -> AC4 CVO served-verify (NEVER#7: content-tool test -> metadata-only Athena row, no body). -->
<!-- ORIGINAL: pending -->
<priority>MEDIUM — privacy gate before audit-scope-grow (no current leak; the scope-hold prevents one until this lands). ~B-surfaced + CVO-co-found; CTO-ruled the policy (190109Z).</priority>
<date>2026-06-29</date>

## Context

The OPLMCP.05.R8 gateway audit lake (S3/Athena) logs ts/user/tool/ARGS/outcome/detail; args is currently
UNREDACTED. Safe NOW only because the 3 audited tools (ms_site_children/otp_fetch/whoami) carry
request-metadata in args. The no-bodies property is SCOPE-DEPENDENT — if the audit expands to
content-carrying tools (read_email/send_email/read_file), unredacted args = message/document bodies
queryable in Athena (privacy-bar break). CTO ruled the policy (190109Z).

## Objective

Implement a FAIL-CLOSED args-handling control at the gateway audit `_emit` so the audit can safely admit
content-carrying tools (full accountability metadata) while NEVER storing body/content — and so a new tool
or new arg field cannot leak a body by default.

## Scope (CTO ruling 190109Z — implement exactly)

- **Per-tool args-FIELD ALLOWLIST, default-OMIT.** For each tool admitted to the audit, declare an explicit
  set of metadata-safe arg FIELDS to log. EVERY undeclared field is OMITTED. A tool with no declared
  field-schema -> args omitted entirely (log only ts/user/tool/outcome), never raw args. (Field-level
  allowlist at the `_emit` point — fail-closed: the default is omit, not log.)
- **Declared metadata-safe fields (CVO co-verifies per-field; default OMIT when unsure):** e.g.
  read_email -> mailbox/sender/messageId (subject? = CVO call — subject lines can carry content);
  send_email -> to/messageId (subject? = CVO call); read_file -> path/site (NEVER the body/content field).
  The current 3 tools keep their existing metadata fields.
- **DEFENSE-IN-DEPTH BACKSTOP: a hard LENGTH CAP** (truncate every logged arg value to N chars). NOT the
  primary control (a 1-line body slips under a cap) — a backstop that caps blast radius if the allowlist is
  ever mis-configured. Belt + suspenders.

<compiler_tools_mandate>
- It's the m365-gateway audit.py / AC2 redaction surface (base-AE owns the gateway — COORDINATE the _emit edit).
- Verify against the SERVED audit record (NEVER#7): emit a content-carrying tool through the gateway in a test + confirm the Athena row has the metadata fields + NO body field (not just "the code looks right").
- Gateway deploy is the m365-gateway path (base-AE's lane / coordinate).
</compiler_tools_mandate>

<cross_domain_coordination>
- base-AE: owns the m365-gateway (audit.py / _emit / the deploy) — coordinate the edit + deploy.
- 3.0.0_SA_CVO: co-verifies the per-field metadata-vs-content schema (especially the subject? calls; default-OMIT-when-unsure).
- 1.0.0_SA_CTO: ruled the policy (arch owner).
</cross_domain_coordination>

<acceptance_criteria>
1. Field-allowlist implemented at `_emit`: declared metadata-safe fields logged, ALL undeclared fields OMITTED, no-schema-tool -> args omitted entirely. Fail-closed verified (an undeclared/new field does NOT appear in the audit row).
2. Length-cap backstop on every logged arg value.
3. Per-field schema CVO-co-verified (the metadata-vs-content calls, subject? resolved).
4. SERVED-record verify: a content-carrying tool (e.g. read_file with a body-ish arg) emitted through the gateway lands a metadata-only Athena row — NO body. RAVC me + CC CTO + base-AE + CVO.
</acceptance_criteria>

## Note
GATE (CTO-affirmed): until this lands, the OPLMCP audit scope MUST NOT expand beyond the 3 metadata-safe
tools — the scope-hold is the structural prevention (no leak possible meanwhile). This TO is the prereq
that UNLOCKS safe scope-expansion. R8 stays closed accurately at the current metadata-safe scope.
