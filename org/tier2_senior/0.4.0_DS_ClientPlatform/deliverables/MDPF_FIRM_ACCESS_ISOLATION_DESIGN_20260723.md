# MDPF Firm-Level PHYSICAL Access Isolation — Design Exploration

**Dispatch:** Andrew-direct via COO 193228Z (*"how to parse out access so that firms physically
only get the information transferred for their firm over, except opal employees get the aggregate
and all the firm level items"*). Design + options, not a build. Author: 0.4.0_DS_ClientPlatform.

## 1. Current state, grounded (comp-routes behaviors, 2026-07-23)

The MDPF JSONs (`opal-data-portal-v2/json/mdpf/*`, `json/portfolios/*`) serve through **one
shared path**: CloudFront behavior `/api/general/*` → `auth-validator-edge` (viewer-request) →
`public-data-router` (origin-request, path→key rewrite) → the S3 origin. **Every authenticated
portal user can fetch EVERY key** — the per-firm JSONs and the Global aggregate are equally
reachable by anyone who passes auth; isolation today is UI-only (the frontend just doesn't link
other firms' views). The aggregate IS a published JSON (`json/mdpf/aggregate-aua-timeseries.json`),
not client-composed — so Opal-only-aggregate is enforceable at the serving layer (good).

**Two grounded facts that shape the options:**
- **Precedent in-estate:** behaviors 2–15 (`/api/scoped/advisor-intelligence/*`) already run a
  **scoping origin-request router** (`shared-advisor-router`) that maps the caller to allowed S3
  keys before the origin fetch — the firm-scoping problem is the same shape one level up.
- **FLAG for CTO~B / PORTAL_AUTHHARD:** behavior 17 (`/json-tiered/*`) hits the same S3 origin
  with **no edge Lambda at all**. Whether any mdpf-relevant key is reachable through it needs
  verification in the AUTHHARD sweep — a no-auth path to the origin would undercut every option
  below. (Flagged, not asserted; the path-prefix mapping may already exclude `json/`.)

## 2. The entitlement model (two tiers, one source of truth)

| Tier | Sees |
|---|---|
| firm-user (49F / INF / COT) | their own firm's keys ONLY — never another firm's bytes, never the aggregate |
| Opal-internal | the Global aggregate + ALL firm-level items |

The tier must ride an **auth claim evaluated at the edge/serving layer** (never the client), and
there must be exactly ONE entitlement model shared with PORTAL_AUTHHARD — not a parallel one.

## 3. Options

### A. Firm-scoped origin-request router (the shared-advisor-router pattern, one level up) — RECOMMENDED FIRST STEP
Extend/clone the existing scoped-router pattern for the mdpf paths: the edge Lambda reads the
validated token's firm claim and **denies any key outside the caller's prefix allowlist**
(`json/mdpf/{their-firm}/*` for firm-users; everything incl. the aggregate for Opal-internal)
*before* the origin fetch. S3 stays locked to CloudFront (OAC), so the router is the only path
to the bytes — key-guessing returns 403 at the edge, which satisfies "physical" in the sense
that no request a firm can make will ever transfer another firm's bytes.
- **Pros:** smallest churn; proven pattern in this exact estate; single distribution; naturally
  merges into PORTAL_AUTHHARD's validator (one entitlement model); per-firm prefixes already exist.
- **Cons:** isolation lives in Lambda logic + bucket policy, not in separate storage — a router
  bug is the failure mode (mitigate: deny-by-default + the mutant tests below).

### B. CDN-native scoping: per-firm path behaviors + signed cookies (CloudFront key groups)
Firm login issues signed cookies whose policy covers only `json/mdpf/{firm}/*`; Opal-internal
cookies cover all. CloudFront rejects out-of-scope paths cryptographically.
- **Pros:** enforcement is CDN-native (no custom code on the request path).
- **Cons:** cookie issuance/rotation machinery at login; coarser than claims; still one origin —
  and it must coexist with auth-validator-edge (two mechanisms unless AUTHHARD adopts it wholesale).

### C. Per-firm physical storage: separate buckets (± separate distributions)
`opal-portal-49f`, `opal-portal-inf`, `opal-portal-cot`, `opal-portal-internal` — bucket policy +
IAM Deny per firm, the same firm-separation class already law for bd↔cot. The publish step
fans out per-firm (a small extension of the stage/publish script).
- **Pros:** the strongest honest reading of "physically only get their firm's data" — different
  bytes live behind different doors; misconfiguration of one firm's door cannot expose another's.
- **Cons:** highest ops surface (buckets, OACs, possibly distributions/domains per firm); the
  publish fan-out and freshness verification multiply by firm count.

### D. Push delivery to firm-owned destinations
If firms should *receive* their data (Andrew's word "transferred over") rather than browse the
portal: per-firm export — S3 cross-account replication to a firm-owned bucket, SFTP drop, or a
signed per-firm export bundle. Nothing to reach into; the aggregate never leaves Opal.
- **Pros:** literal physical transfer of only their data; zero shared serving surface.
- **Cons:** a delivery product, not an access-control change; only right if firms consume
  outside the portal. Composable with A–C (portal for Opal, delivery for firms).

## 4. Recommendation + sequencing

**A now, C as the hard-isolation upgrade, D if the requirement is delivery.** A gives real
serving-layer isolation this quarter using a pattern the estate already runs, and its entitlement
claim work is exactly the work PORTAL_AUTHHARD needs anyway (do it once, together — CTO~B
coordination is a precondition, not an afterthought). C becomes right if/when firms get direct
programmatic access or audit requirements demand storage-level separation. B is dominated by A
in this estate (A reuses the existing router+validator machinery; B adds a second mechanism).

**Mutant battery for whichever lands (the physical-isolation proof):** (1) firm-A token requests
firm-B key → 403 with zero bytes; (2) firm token requests the aggregate → 403; (3) Opal token
requests every firm + aggregate → 200 each; (4) unauthenticated request on every mdpf behavior
incl. `/json-tiered/*` → denied; (5) key-guessing sweep (enumerate real keys under a foreign
firm token) → all denied. Run as an exercised battery per Rule 22a — behavior claims need the
path exercised, not config reads.

## 5. Needs Andrew's ruling (flagged per the dispatch)

1. **Identity source for the two tiers:** how is "Opal employee" vs "firm user" established —
   Entra/m365 group membership, the portal user table role, or the auth provider's claim? (This
   decides where the entitlement lives and who administers it.)
2. **Do firm users use the portal at all**, or is the real requirement per-firm *delivery* (D)?
   The options differ materially on this.
3. **Confirm the aggregate is strictly Opal-only** (his statement implies yes — recorded as the
   default here).
