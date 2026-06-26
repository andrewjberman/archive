# NFRA_MSGRAPH.S2 — extract_ms_cloud BUILD NOTE (CTO arch-gate request; pre-deploy)

**TO:** NFRA_MSGRAPH.S2 | **Lane:** 0.8.0_AE_CloudComp | **Date:** 2026-06-26
**Status:** BUILT + locally PROVEN (11/11 regression green). NOT deployed. **Routed to CTO for the implementable-change arch-gate** (TO acceptance #6) BEFORE any irreversible deploy.

## Canonical locations (the real change lives in the shared globgrph tree)

| Artifact | Canonical path | This dir |
|---|---|---|
| MS extractor + SS4 cert | `infra/aws/globgrph/ms_cloud_extract.py` | `ms_cloud_extract.py` (reviewable copy) |
| Adversarial regression (the acceptance artifact) | `infra/aws/globgrph/tests/test_ms_cloud_cert.py` | `test_ms_cloud_cert.py` (reviewable copy) |
| derive_runner additive edits | `infra/aws/globgrph/derive_runner.py` | `derive_runner.additive.patch` (unified diff) |

> The 3 changes are in the working tree at their canonical infra paths but **UNCOMMITTED** — `infra/aws/globgrph/` is owned-paths lane `CLOUD_OPS_OR_ETL` ("any AE agent") and `0.8.0_AE_CloudComp` is not yet enumerated in `permitted_agents` (the tilde-lane enumeration gap the lane itself documents; COO previously added `~A`/`~C` as correct permanent adds). **COO RAVC sent to add my serial** so I can land in-place. This dir is the durable reviewable copy meanwhile.

## What it does (per the CTO-PASS'd S1 schema, minimal-viable per invariant #4)

- `extract_ms_cloud(graph, caller=...)` — an **additive best-effort fold** in `derive_runner.main()`, alongside the existing `ingest_ts_semantic_producer` / `stitch_served_from` folds (same precedent). Enumerates SP + OneDrive via the **4 allowlisted gateway tools only** → emits MS nodes (7 closed `node_type`s, `layer='ms'`, `source='ms'`, `ms_state`→`drift_class`) + edges (`CONTAINS` day-one tree + `OWNED_BY` via `createdBy`/`lastModifiedBy`) + `lastModifiedDateTime` write-heat → appends as `classes_data['MS_CLOUD']` + extends `graph['edges']`. Merges into the **single** Nessie graph (8-field Iceberg schema **byte-identical** — MS is additional ROWS; comp-kuzu + the incremental-updater Lambda are structurally unaffected).
- **3 minimal additive edits to the shared `derive_runner.py`** (additive-safe — AWS defaults preserved): per-node `source` read (was hardcoded `"full-derive"`); per-edge `layer` read (was hardcoded `"aws"`); the `extract_ms_cloud` fold in `main()`.
- **Exclusion policy** = named auditable config (`DEFAULT_ONEDRIVE_EXCLUSIONS`): repo-mirror + synthetic corpus excluded; chat-dumps flagged S6. Node ceiling guard. Target ~10³ organic nodes.

## CTO binding condition 1 — PROVEN (the catastrophic-floor acceptance artifact)

`test_ms_cloud_cert.py` — **11/11 green** (`python infra/aws/globgrph/tests/test_ms_cloud_cert.py`). The proof is the passing+failing pair:
- comms-class node → **cert FAILS the derive** ✓
- content-bearing field → **cert FAILS** ✓
- content field hidden in `props` → **cert FAILS** (sees through the additive column) ✓
- comms-surface URL (`/me/messages`) → **cert FAILS** ✓
- uncategorized `edge_type` → **cert FAILS** ✓
- clean structural node → **cert PASSES** ✓
- file legitimately *named* "...Body Review.pdf" → **PASSES** (cert checks field KEYS not free-text values; no false-positive) ✓
- AWS graph unchanged when MS-disabled ✓ / strict superset when enabled ✓ / exclusion policy drops mirror+synthetic ✓ / OWNED_BY + MS_USER admitted ✓

The cert is wired **fail-closed** in `main()`: a `MsContentCommsLeak` returns 1 (no commit, no marker) — a leak fails the whole derive, never a silent WARN. Gateway/enumeration errors stay best-effort (the AWS derive never fails on an MS gateway hiccup).

## CTO binding condition 2 — multi-library flag CARRIED

`ms_cloud_extract.MULTI_LIBRARY_GAP` documents it inline: `list_site_files` reaches only a site's DEFAULT drive; S5 must enumerate `/sites/{id}/drives`. Not lost.

## THE GATING IMPLEMENTABLE-CHANGE DECISION FOR THE ARCH-GATE (headless delegated-token)

**The nightly Fargate derive cannot obtain Andrew's delegated Graph token interactively.** The m365 gateway is delegated-OAuth (per-user; `get_token(email)` raises `NeedsLogin` if unauthorized — `tools.py:40-44`). So `extract_ms_cloud` is **default-DISABLED** (`GLOBGRPH_MS_ENABLED=0`) and ships dark: the code lands safely and runs ONLY once the token source is resolved. **CTO ruling needed on the auth architecture** before enable/deploy. Options (for the arch-gate):
1. **Stored refresh-token for Andrew's delegated scope** (Sites.Read.All / Files.Read.All) the nightly exchanges headlessly — keeps "Andrew-only access now," no app-wide application permissions.
2. **Run the MS extract as a separate Andrew-context job** (not the headless nightly) that publishes MS nodes to the same graph — decouples the auth context from the Fargate task.
3. **App-only (application) Graph permissions** — rejected unless CTO directs; broadens beyond Andrew-only (S6 concern), changes the catastrophic-floor blast radius.

Recommendation: option 1 or 2 (preserve Andrew-only). This is the one real external dependency; the rest of S2 is done and proven.

## Deploy discipline (NOT done — gated)

Terraform-only for the task-def env flip (`GLOBGRPH_MS_ENABLED=1`); commit before apply; **coordinate the deploy window with the NFRA_GLOBGRPH owner** (no clobber of an in-flight globgrph derive). RAVC CTO this change → arch-gate PASS → then the globgrph owner coordinates the enable. Nothing irreversible has been done.
