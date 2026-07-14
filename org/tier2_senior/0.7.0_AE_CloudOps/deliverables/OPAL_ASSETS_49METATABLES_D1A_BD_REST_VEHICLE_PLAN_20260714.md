# D1(a) — the daily BD REST pull vehicle: plan for CTO gate

**Author:** 0.7.0_AE_CloudOps (vehicle) · **Co-designed:** 0.4.0_DS_ClientPlatform (dims; thread
103326Z→104157Z, five cells all settled/staked) · **Date:** 2026-07-14 ~10:5xZ
**Mandate:** Andrew-direct ~03:4xZ (daily REST pattern for BOTH BD masters); CTO 103143Z (vehicle
design comes to his gate as its own plan; D1 = the last 49METATABLES convergence input).
**Replaces at source:** the frozen post-06-26 BD allocations feed (legacy connector measured alive
with CONSTANT 1894-byte nightly theater logs — D4 census G1).

## What it is

A scheduled Lambda that pulls the Black Diamond REST projections for the 49F org daily and lands
RAW responses in the monolith — the C5 `smartx-assets-daily-pull` shape cloned (own role, own
scheduler, fail-loud floors, fence attached, monolith-only), never the EC2/SSM/portal-export
legacy it replaces.

| Cell | Decision |
|---|---|
| Name | `opal-assets-bd49f-daily-pull` (lambda) · `opal-assets-bd49f-pull-role` · schedule `opal-assets-bd49f-daily-pull-daily` |
| TF home | `infra/aws/terraform/opal-assets/` (fan-in infrastructure — the mirror precedent). CTO may re-home. |
| Landing (cell 2, AGREED) | `blackdiamond/49f/bronze/{feed}/{YYYYMMDD}/…` — RAW REST bytes as delivered (17a: pagination preserved as delivered, one object per response page; no parse at ingest). Run manifests → `blackdiamond/49f/_ops/daily_pull/runs/{run_id}.json` (C3 port, cell 3: UNCONDITIONAL — zero-download still writes ok:true). Conversion meta stays disjoint at `blackdiamond/49f/meta/` (ruling 21). |
| Feed roster (cell 1, DS-measured) | `allocations` (query 225507 — THE dim_advisor_fee_role substrate: Rep Fee Split, AoR Name+B2B ID, full Fee Schedule block, Manager/Strategy, Billing Team) + `realized`/`unrealized` (fee-schedule cross-check carriers for the A_02 bps disagreement flag). `transactions`/`holdings` NOT pulled by this vehicle (no advisor/fee content; separate mandates if ever needed). |
| Cadence (cell 5, AGREED) | EventBridge `cron(30 2 * * ? *)` — after the 00:00Z bd-49f session establish + cot's 02:00Z BD session (serializes vendor-side load), T-1 settled. Sweep slot reserved ~04:30Z (ahead of cottonwood's 05:00Z), lands with the converter-family container add. |
| Auth (cell 5) | Rides the EXISTING 49f BD session mechanics (`bd-49f-session-daily` 00:00Z + keepalive 15min + freshness hourly — all live). VERIFY ITEM AT BUILD (22a leg): the session token's endpoint scope covers the three template queries; if the 0833-org tenancy differs from cottonwood's, that goes to CTO before build proceeds. Secrets grant scoped to the exact token ARN(s), read-only. |
| Converter family (settled w/ DS) | REST-JSON is its OWN typed vendor-shape family per ruling 23 (the cottonwood family's shape is xlsx-forwardfill; never a silent widen). DS owns the converter; its container cells (role/rules/sweep) ride a later `-target` add per the established gated pattern. |

## Role (never-widen, the C5/silver shape)

`opal-assets-bd49f-pull-role` attaches EXACTLY: AWSLambdaBasicExecutionRole + the one-way fan-in
fence + `opal-assets-write-blackdiamond` (post scope-map edit) + a scoped secrets-read inline
policy (exact token ARNs). ZERO grants on any firm bucket — the legacy role's opal-data-bd reach
is exactly what this vehicle retires.

## The one non-pure-add line, stated plainly

`monolith_source_scopes.blackdiamond` gains scope `"49f"` — one map edit (the map was DESIGNED as
the only edit needed for a new scope), which materializes as ONE in-place update to
`opal-assets-write-blackdiamond` (new scope ARNs added). Everything else in the plan is pure
to-add. The plan will read: N to add, 1 to change (that policy), 0 to destroy — the 1-change is
our own new-territory policy, named here in advance so the plan diff surprises nobody.

## Fail-loud floors (C5 pattern, measured bases)

- `EXPECT_FEEDS=3` — a feed missing from the roster RAISES (no silent partial day).
- `MIN_ALLOCATION_ROWS` floor from DS's template measurement (1235/1235 accounts populated
  2026-06-09) — proposed floor 1000, DS confirms at build; an under-floor day lands the bytes AND
  raises (data lands, verdict screams — never a silent shrink).
- Landing verification LISTING-based (13c; HeadObject is never the acceptance instrument).
- 22a at apply: isolated positive (own bronze put), fence negatives (opal-data-bd + Door-6 +
  out-of-scope monolith prefix), one --resource-arns per call, --context-entries on any
  conditioned List; import-health smoke at first deploy (contract vocabulary).

## What this plan does NOT do

- Does NOT touch the legacy connector (bd-allocation-* rules, EC2, SSM docs) — retiring it is a
  SEPARATE gated change after the replacement is proven landing (the mirror/legacy-CSV cutover
  discipline: parity first, disable second, both gated).
- Does NOT write opal-data-bd, any firm bucket, or Door 6 (fence-proven at apply).
- Does NOT build the 0824 master's REST path — Andrew's "both masters" second half is the SmartX
  master, whose daily pull ALREADY EXISTS (C5 smartx-assets-daily-pull, verified 3-layer in the
  D4 census). This vehicle completes the 0833/BD half.

## Build sequence (on CTO GO)

TF + handler (clone C5 skeleton) → commit-gate → safe-commit → artifacts via build-and-upload →
plan (expect N/1/0 as stated) → CTO apply gate → 22a battery + import smoke → first scheduled fire
02:30Z next day = prediction-then-observation vs DS's template row counts → DS converter family
follows on the landed grammar.
