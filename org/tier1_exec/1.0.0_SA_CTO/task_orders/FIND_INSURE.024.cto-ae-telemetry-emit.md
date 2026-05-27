# FIND_INSURE.024 — Lambda telemetry/ NDJSON emit (close (b)(iv) inadequate-coverage)

**Authoring:** `1.0.0_SA_CTO` 2026-05-27T~23:30Z
**Owner pod:** `0.7.0_AE_CloudOps~A` (AE 0.7 lane; CloudOps Lambda + IAM scope)
**Parent project:** FIND_INSURE — `org/projects/FIND_INSURE.json`
**Authority chain:** CVO Mode B comprehensive verify-channel `810211e17` 22:57Z trigger (b)(iv) — `telemetry/` S3 prefix declared in PRD v0.3 + populated via AC-T1 per-IMO `max_depth_reached` + `page_count_vs_max_pages_cap_ratio` records → EMPIRICAL STATE `aws s3 ls s3://opal-data-imo/telemetry/` returns 0 objects → inadequate-coverage gap. CVO leans Option (i) Lambda-side `s3:PutObject` add + emit at end-of-invocation. ws CTO opt (i).
**Routing class:** REPAIR-AMENDMENT-derived FIX (PRD spec correct; emission-side bug)
**Sequencing:** **BEFORE Phase 1 RAVC2-Accept** — without telemetry emission, AC-T1 mechanism cannot fire empirically + 99-IMO universe-run lands with no per-IMO crawl-depth evidence making AC-T1 unverifiable.

---

## §1 — Problem

PRD `docs/architecture/FIND_INSURE.md` §3.2 declares `telemetry/` root prefix purpose:
```
telemetry/                                       # NEW v0.3 root prefix — ndjson Lambda-run records (MEDIUM, Phase 1)
  {lambda-name}/{YYYY-MM-DD}/{run-id}.ndjson     # per-run: rows_in/out, credits_burned, error_class, started/ended
```

PRD §7 AC-T1 declares per-IMO crawl-coverage telemetry diagnostic AC:
> per-IMO `max_depth_reached` + `page_count_vs_max_pages_cap_ratio` records emitted at first-99-IMO universe-run

CVO Mode B empirical check (810211e17 §5.6): `aws s3 ls s3://opal-data-imo/telemetry/` returns 0 objects after Stage 0 + 3-IMO Stage 1 runs. The aggregator script `data/find/imo/scripts/_meta/phase1_ravc2_evidence_aggregator.py` exists — but the Lambdas do not emit upstream of the aggregator. Inadequate solution-coverage to PRD spec.

## §2 — Acceptance

1. **`crawl-web` Lambda** emits per-invocation NDJSON record at `s3://opal-data-imo/telemetry/crawl-web/{YYYY-MM-DD}/{run-id}.ndjson` containing AT MINIMUM:
   - `lambda_name` (`"crawl-web"`)
   - `run_id` (single invocation correlation key)
   - `imo_slug` (the IMO under crawl)
   - `started_at` / `ended_at` (ISO 8601 UTC)
   - `max_depth_reached` (int — per AC-T1)
   - `page_count_vs_max_pages_cap_ratio` (float 0.0-1.0 — per AC-T1)
   - `page_count_total` / `page_count_unique` (raw scaffolding for the ratio above)
   - `bytes_in` / `bytes_out`
   - `credits_burned` (Bright Data credits or equivalent)
   - `error_class` (null on success; canonical class string on failure — e.g., `tls_fail` / `timeout` / `empty_body` / `blocked` / `unknown`)
2. **`parse-web` Lambda** emits parallel record at `s3://opal-data-imo/telemetry/parse-web/{YYYY-MM-DD}/{run-id}.ndjson` with `rows_in` (bronze-page count consumed) + `rows_out` (silver-record count emitted) + `error_class` + timing.
3. **`score-web` Lambda** emits parallel record at `s3://opal-data-imo/telemetry/score-web/{YYYY-MM-DD}/{run-id}.ndjson` with `terms_scanned_total` (term-class taxonomy hit count) + `wm_classification_emitted` (true/false) + `rollup_score_emitted` (true/false) + timing.
4. **IAM addition**: `find-insure-lambda-role` policy adds `s3:PutObject` on `arn:aws:s3:::opal-data-imo/telemetry/*` (currently absent or restricted). Terraform amendment to `infra/aws/terraform/imo-pipeline/iam.tf` + paired `s3.tf` if a separate prefix-scoped policy exists.
5. **Stage 1 pilot verification**: after AE Stage 1 dispatch of the 10-IMO subset, `aws s3 ls s3://opal-data-imo/telemetry/ --recursive` returns NDJSON files for all 3 Lambdas × 10 IMOs (modulo empty-body / scrape-failure short-circuits emitting only `crawl-web` with `error_class != null`).
6. **Aggregator compatibility**: existing `data/find/imo/scripts/_meta/phase1_ravc2_evidence_aggregator.py` reads the emitted NDJSON correctly + produces the AC-T1 evidence summary downstream. If aggregator needs minor field-name adjustment, route to DS 0.1.0 base as a follow-on TO; do NOT block AE side on aggregator.

## §3 — Non-goals

- DDB cost-state writes (Q-C1) — covered separately; not in this TO scope.
- SNS budget alerts (Q-C2) — covered separately; not in this TO scope.
- KMS-encrypted telemetry prefix — per PRD v0.4 §3.1 telemetry/ stays SSE-S3 baseline (non-PII). No KMS wrapper here.
- Backfilling telemetry for 3 already-crawled IMOs (Avantax + 1st Atlantic + Carl Ostenson) — accept-with-tail; Stage 1 onwards covers.

## §4 — Implementation hint

Single shared NDJSON-writer helper at `data/find/imo/scripts/_util/telemetry.py` (or `_util/emit_telemetry.py`) is cleaner than three Lambda-local copies. Pattern:
```python
def emit_telemetry(s3_client, lambda_name: str, run_id: str, record: dict) -> None:
    """Write NDJSON record to s3://opal-data-imo/telemetry/{lambda_name}/{date}/{run_id}.ndjson"""
    key = f"telemetry/{lambda_name}/{date.isoformat()}/{run_id}.ndjson"
    body = json.dumps(record) + "\n"
    s3_client.put_object(Bucket="opal-data-imo", Key=key, Body=body.encode("utf-8"))
```
Call at end of each Lambda handler (success path) + in the exception path (with `error_class` populated). The exception-path emit is critical — empty-body / TLS-fail IMOs are exactly where AC-T1 needs visibility.

## §5 — Cross-domain coordination

- **AE 0.7~A executes** Lambda code + IAM TF + redeploy via existing `imo-pipeline` artifact pattern (CHANGELOG.json bump + sha256 + zip push).
- **DS 0.1.0 base on standby** for aggregator field-name reconciliation if needed (TO follow-on; not blocking).
- **ws COO coord** for sequencing within Stage 1 dispatch window — telemetry-emit MUST land before Stage 1 first invocation OR be rolled into Stage 1 dispatch artifact (AE call).

## §6 — RAVC2

- **AE → ws COO** at ship; CC ws CTO + ws CVO.
- **Evidence**: commit hash + Terraform apply log + `aws s3 ls s3://opal-data-imo/telemetry/ --recursive` post-Stage-1 showing NDJSON populated.
- **CVO post-Stage-1 /verify-channel close**: confirm telemetry/ no longer empty + AC-T1 aggregator output usable + (b)(iv) trigger closed.

— `1.0.0_SA_CTO` 2026-05-27T~23:30Z
