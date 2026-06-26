# NFRA_MSGRAPH.S1 — MS doc-cloud node/edge/activity SCHEMA (CTO arch-gate pending)

**TO:** NFRA_MSGRAPH.S1 | **Lane:** 0.8.0_AE_CloudComp | **Date:** 2026-06-26
**Status:** DRAFT — routed to 1.0.0_SA_CTO for the S1 arch-gate (gates S2 ingestion cut).
**Grounded against:** `docs/architecture/NFRA_COMPAWS_SCHEMA.md` (the canonical globgrph schema) + live `comp-kuzu` introspection of the deployed graph (12,644 nodes, single `CloudNode` label, property-typed). This schema **merges into that single graph** — it does NOT stand up a parallel schema (PRD §3.4: one Nessie estate, one UNCATEGORIZED cert).

> **archetype:** IMPLEMENT (schema authoring)

---

## §0 — Binding design decisions (mirror the canonical conventions)

1. **Single label, property-typed.** Live globgrph uses ONE Kuzu label `CloudNode`; the class is the `node_type` PROPERTY (`S3_BUCKET`, `ReactComponent`, `Field`, …), with `layer` ∈ {`aws`, `frontend`/portal, pipeline}. **MS nodes are `CloudNode` with `layer='ms'`** and MS `node_type` values below. No new node LABEL.
2. **CLOSED vocabulary.** Per NFRA_COMPAWS_SCHEMA §4: every node gets a §1/§2 type; every edge gets a typed verb; **`UNCATEGORIZED=0` is an absolute cert-fail**; there is **no `OTHER`/`UNKNOWN`/`RELATES_TO` escape hatch.** The MS node/edge sets below are TOTAL over the MS allowlist surface.
3. **No Terraform "declared" side for MS** → the §1.3 `DECLARED`/`LIVE-no-DECLARED` drift axis does not apply (there is no IaC for the MS doc-cloud). MS uses its own provenance axis `ms_state` (§3), exactly as the portal/pipeline layer uses `coherence_class` instead of the TF drift axis (NFRA_COMPAWS_SCHEMA §6.1).
4. **New edge verbs = vocabulary-adds requiring this CTO gate.** `CONTAINS`, `OWNED_BY`, `HAS_ACCESS`, `SHARED_WITH`, `MEMBER_OF` are proposed additions to the §1.2 CLOSED edge vocabulary. A new label is a schema change, not a per-class detail (NFRA_COMPAWS_SCHEMA §0 consumption note) — hence the gate.
5. **Lean (TO invariant #4).** Enough to unblock S2 + interface-ready for S5; no substrate gold-plating.

---

## §1 — MS node classes (`layer='ms'`)

Universal CloudNode props every MS node carries: `node_id` (canonical MS URN — see §1.1), `node_type`, `name`, `layer='ms'`, `ms_state` (§3), `source` (e.g. `ms-full-derive`), `snapshot_ts` (epoch-ms, same convention as AWS), `props` (JSON blob of MS-specific attrs).

| `node_type` | Represents | Graph source | `props` (MS-specific) |
|---|---|---|---|
| `MS_SITE` | a SharePoint site | `find_sharepoint_site` → `/sites` | `site_id`, `web_url`, `display_name`, `created_dt`, `last_modified_dt`, `host` (`opalinvest.sharepoint.com`), `description` |
| `MS_LIBRARY` | a document library (a site `drive`) | `/sites/{id}/drive` (root of `list_site_files`) | `drive_id`, `library_name` (e.g. `Documents`), `web_url`. **NOTE:** current gateway reaches only the DEFAULT drive per site (recon finding) — multi-library sites under-modeled until S2/S5 adds `/sites/{id}/drives` enumeration |
| `MS_FOLDER` | a folder (driveItem with `folder` facet) | `list_site_files` / `list_onedrive` children where `folder` present | `item_id`, `drive_id`, `web_url`, `child_count`, `created_dt`, `last_modified_dt`, `path` |
| `MS_FILE` | a file (driveItem with `file` facet) | children where `file` present | `item_id`, `drive_id`, `web_url`, `file_type` (`.pdf`/`.pptx`/…), `mime_type`, `size`, `created_dt`, `last_modified_dt`, `quick_xor_hash`. **CONTENT (bytes) NEVER stored — `read_file` off-limits.** |
| `MS_DRIVE_ONEDRIVE` | a user's OneDrive root drive | `list_onedrive` root (`/me/drive`) | `drive_id`, `owner_upn`, `web_url`. (A OneDrive is a personal `drive`; modeled as its own root so OneDrive trees and SP libraries share the `MS_FOLDER`/`MS_FILE` child model.) |
| `MS_USER` | a user principal (owner / access-grantee) | from `owned-by` / `/permissions` (S5) | `upn`, `display_name`, `user_id`. **Mirrors AWS `IAM_USER` typed-principal pattern (§3.2a) — never wildcard-exempt.** |
| `MS_GROUP` | an M365 group / SP group | from `shared-with` / `/permissions` (S5) | `group_id`, `display_name`, `group_type` |

**Reuse of existing `MS_USER` vs AWS `IAM_USER`:** distinct node_types (different identity namespace — UPN vs ARN), distinct `layer`. A future cross-domain "same human" link is out of P1 scope (PRD open-Q5).

**Activity metadata (the heat substrate)** lives in `props` on `MS_FILE`/`MS_FOLDER`:
- `last_modified_dt` — **write-heat, day-one, CONFIRMED present** (recon AC#2). Primary heat signal.
- `last_accessed_dt` — **read-heat, S5-additive** (gateway `/insights` not exposed today). Field RESERVED in the schema now (additive, no refactor) — populated when S5 lands.

---

## §2 — MS edge classes (proposed §1.2 vocabulary-adds — CTO-gate)

An edge is `SOURCE -[VERB]-> TARGET`; fan-out = source out-degree (N edges), per the §1.2 D4 rule. Every MS edge carries `edge_type`, `layer='ms'`, and its own `ms_state`.

| `edge_type` | From → To | Derivation | S5-gated? |
|---|---|---|---|
| `CONTAINS` | `MS_SITE` → `MS_LIBRARY` → `MS_FOLDER`/`MS_FILE`; `MS_DRIVE_ONEDRIVE` → `MS_FOLDER`/`MS_FILE`; `MS_FOLDER` → `MS_FOLDER`/`MS_FILE` | the structural hierarchy from `list_*` children (parent→child, one edge per child) | NO — day-one |
| `OWNED_BY` | `MS_FILE`/`MS_FOLDER` → `MS_USER` | driveItem `createdBy`/`lastModifiedBy` (add to `$select` in S2 — trivial gateway change) | partial (needs `$select` add) |
| `HAS_ACCESS` | `MS_USER` → `MS_FILE`/`MS_FOLDER`/`MS_SITE` | `/driveItem/{id}/permissions` + `/sites/{id}/permissions` | **YES — S5** (`/permissions` not exposed; recon AC#4 could-not-verify) |
| `SHARED_WITH` | `MS_FILE`/`MS_FOLDER` → `MS_USER`/`MS_GROUP` | explicit-share grants in `/permissions` (the over-share / external-share audit class) | **YES — S5** |
| `MEMBER_OF` | `MS_USER` → `MS_GROUP` | group membership (`/groups/{id}/members`) | **YES — S5** |

**Day-one (S2) populatable:** `CONTAINS` (full structural tree) + `OWNED_BY` (with the `$select` add). **S5-gated:** `HAS_ACCESS`/`SHARED_WITH`/`MEMBER_OF` — the access-topology family the PRD names for audit/least-priv/over-share. They are **defined now, populated at S5** (interface-ready, additive — invariant #3): the edge_type vocabulary + node targets exist so the S5 `/permissions` feed lands as data, not a schema refactor.

**0-dangling preserved:** every MS edge terminates on a typed MS node (or, for `OWNED_BY`/`SHARED_WITH`, an `MS_USER`/`MS_GROUP` created on first reference — same pattern as AWS typed-principal admission, §3.2a).

---

## §3 — MS provenance axis: `ms_state` (replaces the TF drift axis)

Like the portal layer's `coherence_class`, MS nodes/edges carry `ms_state` (NOT `DECLARED`/`LIVE-no-DECLARED` — there is no IaC for the doc-cloud):

| `ms_state` | Meaning | Detector |
|---|---|---|
| `LIVE` | present in the latest Graph derive pull | observed this cycle |
| `STALE` | in the graph, NOT seen in the latest pull (not yet confirmed deleted) | absent from current full-derive, present in prior tag |
| `REMOVED` | confirmed deleted from the source (the delete signal) | **S5-gated** — needs `/delta` (a full-derive cannot distinguish "deleted" from "moved out of the enumerated scope" without delta tokens). Until S5: a node missing for ≥N nightly derives → `STALE`, never asserted `REMOVED` |

CVO scores `ms_state`-accuracy as the MS provenance sub-F1 (the analog of provenance-F1 / coherence-F1). The UNCATEGORIZED-class still applies: an MS resource matching no §1 node_type = cert-fail (no escape hatch).

---

## §4 — STRUCTURAL CERT / ALLOWLIST (the catastrophic-floor — gate-impossible, NOT policy) — locked_invariant #1

The S2 ingestion carries an **emit-time cert** that makes a content/comms leak **gate-impossible**, not merely discouraged. Two enforcement layers:

### 4.1 Source-call allowlist (extractor input gate)
The `extract_ms_cloud()` step may call ONLY these gateway tools (the document-storage surface):
`find_sharepoint_site`, `list_site_files`, `list_onedrive`, `search_files` — and the S5-additive `/delta`, `/insights`, `/permissions`. **HARD-DENY** (the extractor must not import or invoke): `list_recent_email`, `search_email`, `read_email`, `create_draft`, `send_email`, `reply_email`, `list_calendar`, `list_chats`, `read_chat_messages`, `send_chat_message`, `list_teams`, `list_channels`, `read_channel_messages`, `send_channel_message`, `poll_addressed_teams_messages`, **and `read_file`** (the content surface). Grounded in `infra/aws/ec2/m365-mcp-gateway/app/tools.py` — the comms + content surfaces are physically separate tools; the allowlist is a closed set of 4 (+3 S5).

### 4.2 Emitted-node content/comms cert (the gate-impossible leg)
Before the MS subgraph merges into the derive, a cert scans EVERY emitted MS node/edge and **FAILS the derive** (does not warn) if any of:
- a node carries a CONTENT field (file body / `content` / `bodyPreview` / mail-body / message-text) — only structural metadata fields in §1 are permitted; an unknown content-bearing field = FAIL;
- a node's `node_type` is a comms class (any email/message/chat/calendar-derived type) — the MS node_type set is the closed §1 list; a comms-class type = FAIL (it could only arrive via a forbidden source call);
- `web_url`/`path` resolves to a comms surface (`/me/messages`, `/chats`, `/calendar`).
This is the S2 CLOSE-leg: a content/comms node is **cert-impossible to merge**, mirroring the globgrph UNCATEGORIZED cert-fail mechanism (PRD §3.4 — an unmapped/forbidden class fails the combined-graph derive). **Access-topology (`HAS_ACCESS`/`SHARED_WITH` with `MS_USER`/`MS_GROUP`) is EXPLICITLY RETAINED** (locked_invariant: org-internal access = security-valid, Andrew-direct) — the cert excludes content + comms, NOT access edges.

---

## §5 — S5 interface-readiness (locked_invariant #3 — additive, no refactor)

The schema ACCEPTS the S5 feeds as pure additions:
- **`/delta`** → enables `ms_state='REMOVED'` (§3) + hourly incremental activity refresh (no structural re-derive). No node/edge change — only the `ms_state` detector upgrades.
- **`/insights`** → populates the RESERVED `last_accessed_dt` field on `MS_FILE`/`MS_FOLDER` (§1). Field exists now; S5 fills it. Read-heat joins write-heat in the heat engine additively.
- **`/permissions`** → populates the already-defined `HAS_ACCESS`/`SHARED_WITH`/`MEMBER_OF` edges (§2) + `MS_USER`/`MS_GROUP` nodes. Edge vocabulary + node targets exist now; S5 supplies the data.
None of the three is a schema refactor — each is a feed into a slot the S1 schema already defines.

---

## §6 — CTO arch-gate checklist (what this gate decides)

1. **APPROVE** the single-label/property-typed merge (`layer='ms'`, no new Kuzu label) into the existing globgrph.
2. **APPROVE** the 7 MS node_types (§1) + the `ms_state` provenance axis (§3) as the closed MS vocabulary.
3. **APPROVE** the 5 new edge verbs (§2) as §1.2 CLOSED-vocabulary additions (`CONTAINS`/`OWNED_BY`/`HAS_ACCESS`/`SHARED_WITH`/`MEMBER_OF`).
4. **CONFIRM** the §4 structural cert shape (allowlist + emit-time content/comms-fail) is concrete enough for S2 to implement as a gate-impossible CLOSE leg.
5. **RULING NEEDED:** add `/permissions` to the S5 gateway-extension scope (recon found it absent — the access-topology edges are unpopulatable without it; the PRD §3.2 named only `/delta`+`/insights`).

On PASS, S2 ingestion (`extract_ms_cloud` in `derive_runner.py`) is cut against this schema.
