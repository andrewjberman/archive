<to_id>NFRA_WRKFLW.P1</to_id>
<project>NFRA_WRKFLW</project>
<title>NFRA_WRKFLW P1 -- L0 FOUNDATION (privacy-critical): de-identify the scoping-lake to ZERO-identity + two-zone hot/cold + semantic-signature distill + sessionID-stitch + separate least-priv READ role</title>
<assigned_to>0.7.0_AE_CloudOps (hot-zone infra / de-id / read-role / two-zone -- owns the .05 audit-lake) + 0.4.0_DS_ClientPlatform (consult: the token-level semantic-signature distill)</assigned_to>
<verify>3.0.0_SA_CVO (PRIVACY-VERIFY: the scoping-lake holds ZERO identity -- no user:email / no identity reconstructable)</verify>
<arch_gate>1.0.0_SA_CTO -- the TWO-ZONE PRIVACY DESIGN is the FIRST mandatory arch-gate; NOTHING mines until the scoping-lake holds zero identity (CTO + CVO confirm)</arch_gate>
<issued_by>2.0.0_SA_COO (Andrew-direct via CTO 160626Z; PRD docs/architecture/NFRA_WRKFLW_PRD.md S6; MSTR scoping-owner, brief docs/briefs/oplmcp-workflow-scoping-20260624.md)</issued_by>
<issued_date>2026-06-24</issued_date>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project NFRA_WRKFLW, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: queued</status>
<!-- PACED: substrate (.05/R8 audit-lake) is READY, but P1 build PACES BEHIND the DATA_PLATFORM deep-expansion + OPLMCP-completion hot-priorities (capacity). Authored now for coverage; executes when capacity frees. P2-P5 queued behind P1. -->

<objective>
The privacy-critical L0 foundation for workflow-mining over the OPLMCP M365-MCP traffic: de-identify AT distillation so the scoping-lake holds ZERO identity (the .05 audit-lake persists user:email for the AUDIT; the MINING-lake must be identity-free -- you mine PATTERNS, not who-did-what). The gate the whole project rests on -- NOTHING mines until zero-identity is verified.
</objective>

<the_work>
- Close the DE-IDENTIFICATION gap: the .05 lake persists user:email -> de-identify AT distillation -> a separate SCOPING-LAKE with ZERO identity.
- TWO-ZONE hot/cold split (the privacy boundary -- CTO arch-gates this design first).
- TOKEN-LEVEL SEMANTIC-SIGNATURE distill (the workflow-pattern signature, identity-stripped) + RESULT-SHAPE-capture + sessionID-STITCH (a workflow = a session's tool-sequence).
- A SEPARATE LEAST-PRIVILEGE READ role (reads the .05 lake for distillation; NOT the gateway write-role).
- Infra via Terraform -> safe-apply + deploy-completion ledger.
</the_work>

<acceptance_criteria>
1. The scoping-lake holds ZERO identity -- CVO privacy-verifies no user:email / no identity reconstructable (the hard gate).
2. Two-zone hot/cold + the semantic-signature distill + result-shape-capture + sessionID-stitch built.
3. A separate least-privilege READ role (distinct from the gateway write-role).
4. CTO two-zone-privacy arch-gate PASS BEFORE any mining (P2+); infra via safe-apply + ledger.
5. RAVC2 COO + CTO. (P2-P5 gated on P1 privacy-PASS.)
</acceptance_criteria>
