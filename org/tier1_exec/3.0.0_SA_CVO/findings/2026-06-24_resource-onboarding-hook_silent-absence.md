# CVO Finding -- Resource-Onboarding Hook + the Silent-Absence invariant

**From:** 3.0.0_SA_CVO · **To:** 1.0.0_SA_CTO (architecture/PRD) + 2.0.0_SA_COO (decompose) · **cc:** 0.0.0_AB_MSTR
**Origin:** Andrew-direct 2026-06-24 ("there should be hooks ... + some kind of comp-{function} which brings [new resources] into the oracle/graph"). GO to route: Andrew 2026-06-24.
**Priority:** P2 -- a systemic rigor/automation investment (retires recurring manual toil + a class of silent gaps); NOT a live-defect fix (every anchor instance is benign/handled). Leverage, not incident.
**Type:** advisory finding -- I recommend the shape; CTO authors the PRD, COO decomposes. I do not draft either.

---

## The gap (one line)

The estate has resource **detection** but no resource **onboarding/action**: a new resource is either **hand-folded** into the graph/oracle (error-prone) or left as **silent drift**. Detection != action.

## Evidence -- 4 live instances surfaced this session (all grounded)

1. **s3-oracle hand-fold (manual + orphan-risk).** A real new bucket (`opal-infrastructure-snapshots`) had to be HAND-added to the s3 cert oracle (`org/modules/graph/aws-shapes/s3-hand-audit-fixture-v1.1.yaml`); it arrived with `tf_managed: null` + provenance `TO-VERIFY`, and rode UNCOMMITTED in the shared tree until base-AE tripped over it on OPLMCP.07 AC2 and had to partial-hunk-isolate around it. Manual fold -> unverified provenance + orphaned WIP. (Resolved: AE commit-through 4189d5a9b, provenance ground-truthed to tf_managed=True/DECLARED; score_s3 node_f1=1.0.)
2. **route53 console-drift (detected, never onboarded).** `opalinvest.dev` A + AAAA are `LIVE-no-DECLARED` (console-created -> portal CloudFront). `comp-aws derive` *detects* the drift every run -- but nothing ever *acts* on it; it sits as permanent drift.
3. **Manual .07 gateway graph-onboarding.** The entire m365-mcp-gateway ALB stack (lb/listener/TG/route53 + EC2 + role) was hand-modeled into comp-iam/comp-aws (OPLMCP.07 AC1-2) + a manual CVO coverage-verify AC (AC4), *because* there is no hook that auto-onboards a new EC2/ALB service when it comes up. (Closed: .07 CLOSED, gateway now graph-native.)
4. **trn_nna silent-absence (the OTHER facet -- absent-but-consumed).** A producer (`convert_schwab_trn_to_nna_silver.py` -> `schwab/silver/trn_nna/`) EXISTS but is never INVOKED by the recurring ingest -> the artifact is live-absent -> the active terminal gold consumer `C_01.canonical_nna` reads it via `lib/schwab_flows.load_schwab_flows_by_date`, which SILENTLY returns `{}` on absence (no error). (Disposition: P2 dormant, served-confirmed uniformly `source_system='bd'`. CTO banked this as the "absent input silently consumed as zero" class, same family as the boto3-silent-no-op catch.)

Instances 1-3 = the **resource-onboarding** facet (Andrew's ask). Instance 4 = the related **silent-absence-consumption** facet -- distinct mechanism, same root theme (something expected is absent; the layer that should act treats absent as benign).

## What exists vs. the gap

- **Exists:** the canonical Nessie/Kuzu graph auto-refreshes on HEAD-advance (marker oracle); `comp-aws derive` flags `LIVE-no-DECLARED`; `EC2_MANIFEST.json` requires manual EC2 registration (Rule 8); the COO's .07 charter made "a permanent estate service is done only when comp-* resolves it" a **manual per-resource AC** (1112012c8).
- **Missing:** a hook at resource-CREATION that proactively brings a new resource INTO the graph AND the per-class cert oracle (with provenance) + emits a CVO-cert; and the inverse -- a presence/freshness assertion so an absent-but-consumed artifact ALARMS instead of silent-zeros.

## For CTO (architecture / PRD)

Recommend a PRD for a **`comp-onboard`-class function + two creation chokepoints**:
- **TF-created -> `safe-apply.sh` post-hook.** Every TF apply already funnels through `safe-apply`; a post-apply step diffs the plan's ADDS and fires `comp-onboard` to auto-derive the new node into the graph + the per-class aws-shapes cert oracle, pulling provenance from TF state, then emits a CVO-cert task. Makes "graph/oracle resolves it" an automatic property of the apply -- retiring the manual per-resource AC (the COO .07 definition-of-done) into a systemic gate.
- **Console-created -> a `LIVE-no-DECLARED` sweep.** `comp-aws derive` already surfaces these; the hook auto-stubs them as PROVISIONAL nodes + flags for TF-import, so drift gets closed instead of accumulating (instance 2).
- Most naturally an extension of **NFRA_GLOBGRPH** (the versioned graph + HEAD-oracle) + **comp-aws** (the derive/score machinery already exists -- `comp-onboard` is the write-side it lacks).
- Recommend the PRD also address the **silent-absence invariant** (below) -- the producer/consumer facet (instance 4) is the same root and worth unifying.

## For COO (decompose, once CTO frames it)

- The `comp-onboard` tool build + the safe-apply post-hook + the per-class oracle-onboard wiring (lane: AE/cloud-ops for comp-aws + safe-apply; CVO co-verifies the auto-cert path).
- Fold the **silent-absence presence-gate** as a sibling: a producer-presence/freshness assertion so an absent-but-consumed artifact alarms (instance 4 + the boto3-no-op class) rather than silent-zeros. (The immediate trn_nna fix -- AE wires the Layer-B converter into /49-schwab-conv -- is a separate tracked P2; this is the GENERAL gate.)

## Unknown-unknown (what to ask that wasn't asked)

The deeper pattern across all 4 instances + the boto3-no-op catch is **SILENT ABSENCE**: something expected is absent (an undeclared resource, an unrun producer, an un-onboarded graph node, an ungranted IAM perm -- cf. the SS4c CW-metric `cloudwatch:PutMetricData` gap caught the same day: `_emit()` denied, `main()` swallows it, metric silently blind), and the layer that should act treats absent as benign (skip / zero / drift-but-no-action). Andrew's ask addresses the resource-onboarding facet. The unasked question: does the estate need a **general "absent-but-expected -> LOUD, not silent-zero" invariant** -- a presence-assertion discipline spanning producers, consumers, graph nodes, and IAM grants? The onboarding hook is one materialization; the unifying defense is making absence *fail loud* by default. That is the higher-leverage frame: not just "auto-onboard new resources," but "the estate never silently tolerates an absent-but-expected thing."

-- 3.0.0_SA_CVO
