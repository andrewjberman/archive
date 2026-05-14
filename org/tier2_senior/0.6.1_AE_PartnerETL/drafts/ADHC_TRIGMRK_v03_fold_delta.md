# ADHC_TRIGMRK v0.3 Fold Delta — AE 0.6.1 → CTO for canonical apply

**Purpose:** v0.3 fold content for CTO to apply to `docs/architecture/ADHC_TRIGMRK.md` per CTO 18:50Z instruction "AE 0.6.1 folds T1-T8 into canonical doc within ~30min, BEFORE TO-001 authoring proceeds."

**Rationale for delta routing:** ADHC_OWNPTH owned-paths hook blocks AE writes to `docs/architecture/`. AE drafts the v0.3 fold content here; CTO applies via canonical-doc edit + project JSON status flip in a single canonicalize-style commit.

**Routing:** MCP to 1.0.0_SA_CTO with this path. Expected CTO apply wall: ~10-15min.

---

## Edit 1 (T1) — §3.2 Path 2 cons reframe

**Find:**
```
- Requires `wait_for_ssm_agent_online` polling in cold-start path (current: marker write is instant; SSM agent boot adds ~30-60s but is required either way for Path 1's daemon-on-boot)
```

**Replace with:**
```
- Requires `wait_for_ssm_agent_online` polling in cold-start path. SSM agent boot adds ~30-60s of new wall-time in cold-start path; this latency is unavoidable and Path 1 has equivalent surface (daemon-on-boot). The "instant marker write" from v1 was only instant because it was silently broken (race-surface-#2) — fast writes to a phantom consumer are structurally worse than slower writes to a real consumer (T1)
```

---

## Edit 2 (T6) — §3.3 Decision-rights

**Find:**
```
**Decision-rights:** CTO architectural ratify on dispatch per LEDGEH precedent. Andrew countermand possible during ratify window; framing-decision documented here so Andrew can override at any phase.
```

**Replace with:**
```
**Decision-rights:** CTO architectural ratify on dispatch per LEDGEH precedent. COO surfaces ratify-decision summary to Andrew via MCP during ratify window (within ~30min of CTO ratify). Default-go after ~30min silence. Andrew countermand via direct MCP to CTO or COO. Default-go pattern matches LEDGEH + FECACHE_COHERENCE + BPMVH precedent — Andrew ratified those explicitly because Cottonwood adjacency / product-strategy surface; routine ADHC architecture defaults to silent-go post-CTO-ratify (T6).
```

---

## Edit 3 (T3 + T4) — AC10 + AC11 + AC12 reflow + new AC13 + AC14

**Find the existing AC10/11/12 rows in the AC table** and **replace with extended rows + 2 new ACs:**

```
| AC10 | Backward-compat deploy boundary — markers swept pre-deploy + SSM Parameter semantics | `aws s3 ls s3://opal-data-inf/gold/trigger-*.json` returns empty post-deploy; no stale audit artifacts. SSM Parameter `/inf/gold/last-trigger-mode` reflects **most recent successfully dispatched mode** (writes AFTER lock acquire + AFTER SSM SendCommand returns CommandId); rejected invocations (409 Conflict / 503 transitional) do NOT update parameter (T4) |
| AC11 | Empirical regression test against today's incident #3 | Re-fire scenario `EC2 hot, prior chain chain_gold-d_* complete >10min ago, no gold/dispatch-lock.json present, mode=gold-d` (formalized per T3; the original incident #3 had ~4h gap between 14:32Z terminal and 18:14Z invoke) → chain TERMINAL within ≤300s wall (matches DS~D SSM-direct precedent 279s); no manual SSM-direct workaround needed |
| AC12 | SSM CommandId audit trail | `aws ssm list-commands --instance-id i-0ed5afded2ebd4ed4 --filters "key=Status,value=Success"` returns Lambda-dispatched commands tagged with mode + invocation_source + lock_run_id |
| AC13 | EventBridge retry policy on 409 Conflict response (T2 NEW) | EventBridge rule property `dead-letter-config` set; `retry-policy.maximum-event-age=60s`; `retry-policy.maximum-retry-attempts=0`. Verify: invoke Lambda twice in <5s with same mode → second invoke returns 409 immediately → EventBridge does NOT retry → no double-fire observed in CloudWatch + SSM list-commands. Default EventBridge retry-on-failure semantics would treat 409 as transient and retry; explicit retry-attempts=0 prevents the retry-storm class |
| AC14 | `comp-iam service inf-gold-trigger` post-deploy gate (T5 NEW) | Post-deploy `comp-iam service inf-gold-trigger` exits 0; no missing IAM permissions; `ssm:SendCommand` scoped to single instance ARN `arn:aws:ec2:us-east-1:*:instance/i-0ed5afded2ebd4ed4`, no wildcard; S3 conditional-put on `gold/dispatch-lock.json` IAM permission present; `ssm:PutParameter` on `/inf/gold/last-trigger-mode` present |
```

---

## Edit 4 (T4) — §3.5 Boot-script update SSM Parameter semantics

**Find:**
```
2. **Boot-script update:** `infra/aws/ec2/inf-gold-layer-runner/scripts/inf-boot-dispatch.sh` shipped in same `safe-ec2-deploy.sh` commit removes marker-read code path; replaced with `aws ssm get-parameter --name /inf/gold/last-trigger-mode` fallback for cold-start mode lookup. (Lambda writes the SSM Parameter on every invoke for cold-start replay.)
```

**Replace with:**
```
2. **Boot-script update:** `infra/aws/ec2/inf-gold-layer-runner/scripts/inf-boot-dispatch.sh` shipped in same `safe-ec2-deploy.sh` commit removes marker-read code path; replaced with `aws ssm get-parameter --name /inf/gold/last-trigger-mode` fallback for cold-start mode lookup. **Lambda writes the SSM Parameter as the LAST step of a successful dispatch (T4):** AFTER lock acquire + AFTER SSM SendCommand returns CommandId. Parameter reflects "most recent **successfully dispatched** mode," NOT "most recent invocation-attempt mode." Rejected invocations (409 Conflict / 503 transitional) do NOT update the parameter, so a cold-start replay always resumes the last actually-dispatched mode.
```

---

## Edit 5 (T8) — §3.4 attribution + §6 cross-references

**§3.4 Find:**
```
**Banking:** Memory entry `feedback_phantom_consumer_marker_pattern.md` will be authored by AE 0.6.1 post-canonicalize, cross-linked to this PRD + `[[feedback_lambda_pending_marker_no_daemon]]` (DS~D-attributed empirical contrast) + `[[reference_inf_ssm_direct_single_script_runbook]]` (canonical workaround).
```

**Replace with:**
```
**Banking:** Memory entry `feedback_phantom_consumer_marker_pattern.md` will be authored by **COO 2.0.0_SA_COO** as part of an 11-entry memory batch (CTO clarification per T8; AE 0.6.1 provides empirical content for the entry but does not separately author; reduces duplication across the 16-entry session corpus). Cross-linked to this PRD + `[[feedback_lambda_pending_marker_no_daemon]]` (DS~D-attributed empirical contrast) + `[[reference_inf_ssm_direct_single_script_runbook]]` (canonical workaround).
```

**§6 Find:**
```
- **`[[feedback_phantom_consumer_marker_pattern]]`** — NEW memory entry to author by AE 0.6.1 post-canonicalize (§3.4); generalizes today's anchor as "before emitting a marker, verify the consumer exists." Distinct from `[[feedback_smoking_gun_field_shape_sanity]]` (wire-protocol shape) and ADVI_SHARED.006 wire-protocol divergence
```

**Replace with:**
```
- **`[[feedback_phantom_consumer_marker_pattern]]`** — NEW memory entry **authored by COO 2.0.0_SA_COO** as part of 11-entry memory batch (T8 attribution-correction; AE 0.6.1 provides empirical content but does not separately author); generalizes today's anchor as "before emitting a marker, verify the consumer exists." Distinct from `[[feedback_smoking_gun_field_shape_sanity]]` (wire-protocol shape) and ADVI_SHARED.006 wire-protocol divergence
```

---

## Edit 6 — §3.7 status stamp + v0.3 changelog block at top of doc

**At top of doc**, replace the title block to add v0.3 changelog above the v0.2 CANONICAL block:

```markdown
# ADHC_TRIGMRK — Trigger-Marker Race-Surface Mitigation (Inflection Gold Pipeline)
**PRD v0.3 — 0.6.1_AE_PartnerETL folds CTO §3.7 T1-T8 ratchet — 2026-05-14 ~19:00Z** (AC1-AC14)

> **v0.3 changelog (T1-T8 folded into canonical doc per CTO 18:50Z instruction "AE 0.6.1 folds T1-T8 within ~30min, BEFORE TO-001 authoring proceeds"):** All 8 T-items absorbed —
> - **T1** §3.2 cons reframed: "instant marker write was silently broken" framing made explicit; SSM agent boot ~30-60s documented as Path 1-equivalent surface
> - **T2** AC13 NEW: EventBridge `retry-policy.maximum-retry-attempts=0` + `dead-letter-config` to prevent 409 retry-storm
> - **T3** AC11 scenario formalized: "EC2 hot, prior chain complete >10min ago, no dispatch-lock present, mode=gold-d"
> - **T4** AC10 + §3.5: SSM Parameter `/inf/gold/last-trigger-mode` semantics = "most recent successfully dispatched mode" (post-CommandId-return); rejected invocations do NOT update
> - **T5** AC14 NEW: `comp-iam service inf-gold-trigger` post-deploy gate (exit 0 + scoped IAM verification)
> - **T6** §3.3 Decision-rights: COO surfaces ratify-decision to Andrew within ~30min; default-go after silence; LEDGEH/FECACHE/BPMVH precedent cited
> - **T7** CROSS-PROJECT: `comp-trace --check-consumer` v0.6 candidate routed to ADHC_COMPIL_V4 corpus via COO; NOT in TRIGMRK TO-001 scope (no in-doc edit)
> - **T8** §3.4 + §6 attribution corrected: `feedback_phantom_consumer_marker_pattern.md` authored by COO (11-entry batch); AE provides empirical content
>
> Architecture (Path 2 + phantom-consumer banking + DRAIN backwards-compat + mode-aware lock TTL) LOCKED per CTO 18:50Z ratify. v0.3 dispatch-ready for TO-001 authoring.
```

**§3.7 header replace:**
```
### §3.7 — v0.3 Ratchet TODO List (CTO-authored 2026-05-14 ~18:50Z; AE 0.6.1 FOLDED 2026-05-14 ~19:00Z)

**STATUS: ALL 8 T-ITEMS FOLDED into v0.3 canonical content as of 2026-05-14 ~19:00Z (AE 0.6.1).** Cross-reference markers (T1/T2/T3/T4/T5/T6/T8) embedded in §3.2 cons (T1), §3.3 Decision-rights (T6), §3.4 + §6 (T8), §3.5 Boot-script update (T4), AC table (T2+T3+T4+T5). T7 cross-project routed to COO for ADHC_COMPIL_V4 v0.6 corpus (no in-doc edit). v0.3 dispatch-ready for TO-001 authoring.

**Original ratchet list (preserved for decision-record auditability):**
```

---

## Edit 7 — §7 Phase 3 AC count update

**Find:**
```
| Phase 3 — Acceptance regression sweep | AE 0.6.1 | ~2h | AC1-AC12 empirical PASS on QA non-prod Lambda alias + QA EC2 sample; includes today's incident #3 re-fire as AC11 |
```

**Replace with:**
```
| Phase 3 — Acceptance regression sweep | AE 0.6.1 | ~2.5h | AC1-AC14 empirical PASS on QA non-prod Lambda alias + QA EC2 sample; includes today's incident #3 re-fire as AC11 (per T3 formalized scenario); AC13 EventBridge no-retry verification; AC14 `comp-iam service` post-deploy gate |
```

---

## Edit 8 — Authoring chain at bottom of doc

**Find:**
```
- v0.2 CANONICAL — 1.0.0_SA_CTO architecturally ratified + canonicalized via git mv to `docs/architecture/ADHC_TRIGMRK.md` — 2026-05-14 ~18:50Z (Path 2 RATIFIED; §3.7 v0.3 ratchet TODO list T1-T8 added)
- v0.3 → AE 0.6.1 folds T1-T8 refinements into canonical doc within ~30min; THEN TO-001 authoring proceeds
```

**Replace with:**
```
- v0.2 CANONICAL — 1.0.0_SA_CTO architecturally ratified + canonicalized via git mv to `docs/architecture/ADHC_TRIGMRK.md` — 2026-05-14 ~18:50Z (Path 2 RATIFIED; §3.7 v0.3 ratchet TODO list T1-T8 added)
- v0.3 — 0.6.1_AE_PartnerETL — 2026-05-14 ~19:00Z (T1-T8 ratchet content authored as AE drafts/ delta; CTO applied to canonical; AC1-AC14; TO-001 authoring proceeds against v0.3 ACs)
- v0.4+ → TO-001 implementation tracking + post-deploy resolution markers (post-Path-2-ship, `[[feedback_lambda_pending_marker_no_daemon]]` flips to RESOLVED; `[[reference_inf_ssm_direct_single_script_runbook]]` updated to note Lambda-canonical-with-SSM-fallback)
```

---

## Project JSON updates (CTO to also apply)

`org/projects/ADHC_TRIGMRK.json`:

**Find:** `"label": "ADHC_TRIGMRK PRD v0.2 CANONICAL (...)"`
**Replace with:** `"label": "ADHC_TRIGMRK PRD v0.3 CANONICAL (Path 2 CTO-ratified; §3.7 T1-T8 FOLDED into v0.3 by AE 0.6.1 delta + CTO canonical apply; AC1-AC14; TO-001 authoring proceeds)"`

**Find:** `"status": "phase1_prd_v02_canonical_cto_ratified"`
**Replace with:** `"status": "phase1_prd_v03_folded_to001_authoring_ready"`

**Find** the `"phase":` field with the v0.2 narrative and **replace** with:
```
Phase 1 PRD v0.3 FOLDED 2026-05-14 ~19:00Z (AE drafts delta + CTO canonical apply). All 8 T-items from CTO §3.7 ratchet folded: T1 §3.2 cons reframed / T2 AC13 EventBridge no-retry / T3 AC11 scenario formalized / T4 AC10+§3.5 SSM Parameter post-CommandId-return semantics / T5 AC14 comp-iam gate / T6 §3.3 COO-surfaces-Andrew + default-go pattern / T7 CROSS-PROJECT comp-trace --check-consumer v0.6 candidate routed via COO / T8 phantom-consumer memory attribution to COO 11-entry batch. Architecture LOCKED per CTO 18:50Z ratify. v0.3 dispatch-ready for TO-001 authoring against AC1-AC14.
```

**Find** the `"blocking":` field with the v0.2 narrative and **replace** with:
```
(1) TO-001 authoring (AE 0.6.1) against v0.3 AC1-AC14 — Path 2 Lambda full rewrite (~120 LOC) + IAM extension (ssm:SendCommand scoped to single instance ARN + s3 conditional-put on dispatch-lock + ssm:PutParameter on /inf/gold/last-trigger-mode) + Terraform updates + EventBridge retry-policy.maximum-retry-attempts=0 + dead-letter-config + pre-deploy marker sweep + boot-script update + EC2_MANIFEST entry. (2) AC1-AC14 empirical regression sweep gates Phase 3 deploy (~2.5h wall per §7 Phase 3 update). (3) Andrew default-go on CTO Path 2 ratify per T6 (within ~30min ratify window; COO surfaces summary).
```

---

## REGISTRY.md row update (CTO to also apply)

Find the ADHC_TRIGMRK row in Active Projects and update phase prefix from `**Phase 1 PRD v0.2 SHIPPED 2026-05-14 ~18:45Z (0.6.1_AE_PartnerETL).**` to `**Phase 1 PRD v0.3 FOLDED 2026-05-14 ~19:00Z (CTO canonical apply via AE drafts/ delta).**` Update the blocking list to match the new JSON `"blocking"` field (TO-001 authoring against AC1-AC14, AC1-AC14 sweep, Andrew default-go).

---

**End of delta.** AE 0.6.1 standing by post-CTO-apply to commence TO-001 authoring against v0.3 AC1-AC14.
