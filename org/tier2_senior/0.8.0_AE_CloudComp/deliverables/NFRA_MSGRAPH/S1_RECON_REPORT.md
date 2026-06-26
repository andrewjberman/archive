# NFRA_MSGRAPH.S1 — RECON REPORT (MS doc-cloud node-count + activity surface)

**TO:** NFRA_MSGRAPH.S1 (recon-and-schema) | **Lane:** 0.8.0_AE_CloudComp | **Date:** 2026-06-26
**Source:** LIVE m365 MCP gateway, delegated Graph API, signed in as `Andrew@opalinvest.com` (`whoami` confirmed)
**Method:** order-of-magnitude enumeration via `find_sharepoint_site` / `list_site_files` / `list_onedrive`, using `folder.childCount` as the fan-out estimator (recon = magnitude + distribution, NOT a full ingest — per TO invariant #4, no substrate gold-plating).

> **archetype:** EXPLORE

---

## 1. Activity surface (AC #2) — SOURCE-GROUNDED, not inferred

Grounded in `infra/aws/ec2/m365-mcp-gateway/app/tools.py` (the gateway's actual tool surface + Graph `$select` params), per CLAUDE.md Rule 22 (a mechanism claim requires source grounding). The gateway exposes **exactly** these document-storage read surfaces:

| Tool | Graph endpoint | `$select` fields | Allowlist class |
|---|---|---|---|
| `list_onedrive` | `GET /me/drive/root[:/{path}:]/children` | name, id, size, **lastModifiedDateTime**, folder, file | `/drives` ✓ |
| `list_site_files` | `GET /sites/{id}/drive/root[:/{path}:]/children` | name, id, size, **lastModifiedDateTime**, folder, file | `/sites`,`/drives` ✓ |
| `search_files` | `GET /me/drive/root/search(q=...)` | name, id, size, **lastModifiedDateTime**, webUrl | `/drives` ✓ |
| `find_sharepoint_site` | `GET /sites?search=` | (default) id, name, displayName, webUrl, **createdDateTime**, **lastModifiedDateTime**, siteCollection | `/sites` ✓ |
| `read_file` | `GET /me/drive/items/{id}/content` | — (raw bytes) | **CONTENT — OFF-LIMITS to ingestion** |

| Surface | Reachable via current gateway? | Grounding | Consequence |
|---|---|---|---|
| **`lastModifiedDateTime` (write-heat)** | **YES — day-one** | in `$select` on all 3 driveItem tools (`tools.py:177,216,185`); empirically present on 100% of sampled items | write-heat heat-map ships in S2/S3 with **no gateway change** |
| **`createdDateTime` per driveItem** | partial | present on `/sites` objects; **NOT** in the driveItem `$select` | trivial S2 ask: add `createdDateTime` to the two `list_*` `$select` strings |
| **`/delta` (incremental change-tracking)** | **NO** | no tool calls `/delta`; only full `/children` listing exists | incremental hourly sync needs **S5**; until then, bounded hourly re-pull of the hot set (PRD §3.3-Q1) |
| **`/insights` · `lastAccessed` (read-heat)** | **NO** | no tool calls `/me/insights` or `/drive/.../analytics` | read-heat depth needs **S5**; write-heat alone is a sound first signal (never-modified ⇒ cold) |
| **`/permissions` (has-access / shared-with edges)** | **NO** | no tool calls `/driveItem/{id}/permissions`; no `/sites/{id}/permissions` | **access-edge density is NOT measurable today** (sharp could-not-verify — see §4). The `has-access`/`shared-with`/`member-of` edge classes in the schema are **defined-but-unpopulatable** until S5 adds a `/permissions` surface |
| **Non-default doc libraries / lists per site** | **NO** | `list_site_files` hits `/sites/{id}/drive` (the DEFAULT drive) only | multi-library sites under-count through current gateway (finding below) |

**Net:** write-heat + nightly-full are GO with today's gateway. `/delta`, `/insights`, **and `/permissions`** are the S5 gateway-extension scope. The PRD named `/delta`+`/insights`; **this recon adds `/permissions` to the S5 list** — without it the access-topology edge classes (a stated PRD capability: audit / least-priv / over-share) cannot be derived.

---

## 2. SharePoint surface — by-site distribution (AC #1)

`find_sharepoint_site("opal")` returned **6 sites**, all under `opalinvest.sharepoint.com` (single tenant). Default document library (`/drive/root`) sampled per site:

| # | Site (displayName) | siteId (host,siteColl,web) | Default-library root | Active? |
|---|---|---|---|---|
| 1 | Opal Capital | `...,7370ba1f-...,18b7f31c-...` | `General` (childCount **0**) | near-empty shell |
| 2 | Opal OCIO | `...,71180614-...,9907f449-...` | `General`(2) + `Sales and Marketing`(0) + `Subscription Models`(0) | light |
| 3 | Opal Consulting | `...,9bbf440e-...,9907f449-...` | (not drilled; assume light) | unknown-light |
| 4 | Opal Trade Submissions & Approvals | `...,5c821ec6-...,d363ce64-...` | **empty `[]`** | empty |
| 5 | **Opal CIO Office for 49 Financial** | `...,291b70c5-...,664d073e-...` | `General` (childCount **10**) — benchmark PDFs, market-update decks, investment packets | **the active one** |
| 6 | 49 Financial Internal Channel | `...,ba3fb192-...,9907f449-...` | (not drilled; assume light) | unknown-light |

**Caveats:** (a) `find_sharepoint_site` is a NAME SEARCH (`/sites?search=opal`), not a full tenant site enumeration — sites not matching "opal" are not surfaced; a complete site list needs `/sites?$select=...&search=*` or admin enumeration (note for S2). (b) only the DEFAULT drive per site is reachable; Teams-connected sites can carry multiple libraries.

**SharePoint magnitude:** **low hundreds of nodes total**, heavily concentrated — 4 of 6 sites are empty/near-empty shells; `Opal CIO Office for 49 Financial` holds essentially all active SP content (FINRA-reviewed benchmark reports, Opal market updates, investment packets — exactly the "findability" target Andrew named). Nesting observed: `site → drive → General → file` = depth 3–4. SP file types: `.pptx`, `.pdf`, `.png` (decks/reports/marketing).

---

## 3. OneDrive surface — Andrew's personal drive (AC #1)

Root = **10 top-level items**. Recursive magnitude estimated via `childCount`:

| Top-level | childCount | size | Node character |
|---|---|---|---|
| Documents | 7 | 72.4 GB | dominated by `Schwab Data Delivery` (1 item, **72.4 GB** — few nodes, huge bytes) + `afterSentDocuments` (**synthetic corpus**, see below) |
| Desktop | 29 | 11.2 GB | dominated by **`ajb_workspace` (childCount 34 → recursively thousands — a full git-repo MIRROR, 11 GB)** + ~20 loose files |
| Attachments | 9 | 0.98 GB | mail/chat attachments |
| **Microsoft Teams Chat Files** | 151 | 0.27 GB | **comms-attachment storage** (Teams-shared files landed in OneDrive) — see §5 |
| Microsoft Copilot Chat Files | 0 | 0 | empty |
| Andrew @ Opal Capital | 2 | small | org docs |
| Apps / Pictures / Meetings / Recordings | 1/2/0/0 | mixed | low |

**Two non-organic subtrees dominate raw node-count:**
- **`Desktop/ajb_workspace`** — a synced copy of THIS git repo. Recursing it yields thousands of files that (a) explode the node budget and (b) **duplicate the AWS repo graph already in globgrph**. Major S2 scoping flag.
- **`Documents/afterSentDocuments`** — `docs0`…`docs14`: **15 identical folders, each childCount 30, each size 711075 bytes** → an obvious generated/test corpus (~450+ duplicate nodes, zero findability value).

**OneDrive magnitude:**
- **Organic, business-relevant nodes** (excluding repo mirror + synthetic corpora + comms-attachment dumps): **low thousands (~10³).**
- **Naive full recursion** (everything): **tens of thousands (~10⁴), almost entirely non-organic** (repo mirror + test fixtures).

---

## 4. Access-edge density (AC #1) — COULD-NOT-VERIFY (sharp finding)

The TO asks for an access-edge-density sample. **This is not measurable through the current gateway.** No tool exposes `/driveItem/{id}/permissions` or `/sites/{id}/permissions` (`tools.py` confirmed — §1). Therefore `has-access` / `shared-with` / `member-of` edge counts are **0-observable today**, not 0-actual. Populating + measuring access topology is gated on the **S5 `/permissions` extension** (added to S5 scope by this recon). Reporting the gap rather than a fabricated density is the correct recon outcome.

---

## 5. Guardrail observations for the schema/cert (AC #4 input)

- **Comms-adjacent OneDrive folders** surface as ordinary driveItems: `Microsoft Teams Chat Files` (151), `Microsoft Copilot Chat Files`, `Documents/Copilot`. These are **structurally `/drives` items** (folder/file metadata — allowlist-legal) but **semantically comms-attachment storage.** They are NOT the `/chats` or `/messages` comms surfaces (those are separate gateway tools that ingestion must never call). **Schema/cert stance:** metadata of these folders is ingestible under the allowlist; their FILE CONTENT is excluded like all content. Flag them for the S6 access/privacy review as a likely **exclusion-by-default subtree** (low findability value, comms-adjacent).
- **The gateway co-exposes the full comms surface** (`list_recent_email`/`search_email`/`read_email`, `list_chats`/`read_chat_messages`, `list_teams`/`read_channel_messages`, `list_calendar`) — `tools.py:74-334`. The S2 ingestion CLOSE-leg cert must assert the extractor calls ONLY `find_sharepoint_site`/`list_site_files`/`list_onedrive` (+ future `/delta`,`/insights`,`/permissions`) and **never** any `/me/messages`, `/me/chats`, `/chats`, `/teams`, `/me/calendarView`, or `read_file` content endpoint.

---

## 6. Budget recommendation (gates S2)

1. **The node budget is set by the EXCLUSION POLICY, not raw counts.** Recommend S2 ingest:
   - **ALL SharePoint sites + default libraries** (low hundreds — cheap, high findability value).
   - **OneDrive organic business subtrees** (low thousands), with **default-exclude** for: `Desktop/ajb_workspace` (repo mirror — already in AWS graph), `Documents/afterSentDocuments` + any synthetic/identical-size corpus, and (S6-review) the comms-attachment dumps.
2. **Order-of-magnitude derive cost target:** ~**10³ organic nodes** (not 10⁴). Page the derive; set a per-site/per-subtree node ceiling; structure-derive nightly only (PRD §3.3-Q1).
3. **Heat half-life:** insufficient signal this pass to tune (docs span 2022–2026; SP active content clusters 2024). Recommend default 30d → tune post-S3 on real `lastModifiedDateTime` distribution (PRD open-Q3).

---

## 7. Compiler Tools

| Tool | Result |
|---|---|
| `comp-which "how do I enumerate SharePoint sites and OneDrive drives via the m365 gateway"` | **Backstop only — no MS-gateway route exists in the manifest.** Expected: the MS doc-cloud is net-new; comp-which has no MS surface until S4 registers `comp-ms-*` + extends routing. **Coverage gap logged** (this IS the S4 deliverable). Live enumeration done via the m365 MCP gateway tools directly. |
| `comp-to NFRA_MSGRAPH.S1` | OK — TO context set (race-free per-session). |
| (planned) `comp-kuzu`/`comp-xref` on existing globgrph schema | grounding the MS node/edge taxonomy against existing globgrph conventions — done in the SCHEMA deliverable (`S1_MS_GRAPH_SCHEMA.md` §2). |

**Gap finding:** `comp-which` has no m365-gateway route. This is not a defect to fix now — it is precisely the S4 findability layer (`comp-ms-find` + comp-which MS routing). Logged for S4.
