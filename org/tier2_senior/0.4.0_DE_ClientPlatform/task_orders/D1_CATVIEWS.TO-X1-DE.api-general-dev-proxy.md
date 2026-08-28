# TO D1_CATVIEWS.TO-X1-DE — the `/api/general` DEV PROXY entry (cause ONE of two; it does NOT make the cards appear)

<decomp_ref>workflows/atom_decomposition/runs/d1-catviews/20260824T195537Z/DECOMP.md — `D1-c-1` (portal consumes: the L0/L1/L2 tree renders, `v1..v4`) and `D1-c-2` (the empty-block fallback). **NO new cell** — this is the transport rung `D1-c-1` already presumes.</decomp_ref>
<certification>Rides the existing certified `D1_CATVIEWS` decomp. No cell added.</certification>
<issued_to>0.4.0_DE_ClientPlatform~S</issued_to>
<executor_class>DE-class (portal, `portal/**` on DEV)</executor_class>
<seating_trigger>SEATED — **`ETFS_SATELLITES.TO-10-DE` is 9 of 9 filed (@`506e889a87`, portal `1c5cdbe5`), so this lane's project work is DONE and Rule 27 permits the move; it holds `D1_CATVIEWS` and nothing else.** ⭐ Same precedent as `~Q` onto `ETFS_INGEST` and `~C` onto `ETFS_POSITIONING`. **Certification of `TO-10-DE` is `3.0.0_SA_CVO~Z`'s and does not need this lane.** ⚠ **The lane volunteered the shape and explicitly declined to build unbidden** — that refusal is why this TO exists rather than a fait accompli.</seating_trigger>
<placement>SITE Z (Rule 26). `portal/` is a WORK-SITE. **Main tree stays on DEV (Rule 19).**</placement>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-28T05:0xZ</issued>
<status>ACTIVE — cut on `1.0.0_SA_CTO~Z`'s diagnosis (12924) of an ANDREW-REPORTED failure on his local 5173 build.</status>
<priority>P1 — Andrew reports the Asset Category Views are *"not surfacing ... for any firm selection or global."* **That is his item-1 surface.** ⚠ **P1 and not P0 because this alone CANNOT fix what he saw — see §2.**</priority>
<authority>Andrew-reported ~04:5xZ (Asset Category Views not surfacing at any scope, local 5173). Diagnosed at source by `1.0.0_SA_CTO~Z`, msg 12924.</authority>

---

## 1. CAUSE ONE — THE DEV PROXY GAP

```
aum.ts:18    const API_BASE_URL = import.meta.env.VITE_PORTAL_API_URL ?? ''      -> RELATIVE
aum.ts:879   `${API_BASE_URL}/api/general/mdpf/${firmId}/category-views.json`
vite.config.ts proxy prefixes:  /v1 · /api/auth · /api/scoped/advisor-intelligence
                                /api/scoped/satellites · /api/scoped/partners
                                ^^ NO /api/general
```

>> **With no proxy entry, vite's SPA fallback returns `index.html` with a `200`. `json()` then throws, and every scope falls to `unavailable`.** ⭐ **That is why it fails IDENTICALLY at every firm selection and at global** — it is not a firm-scoping bug, and a reader chasing it as one will find nothing.

## 2. ⛔⛔ THIS TO ALONE SHOWS ANDREW NOTHING — SAY SO IN THE REPORT

**`1.0.0_SA_CTO~Z` measured TWO INDEPENDENT CAUSES AND BOTH MUST CLEAR:**

```
  (1) the /api/general dev-proxy gap          <- THIS TO
  (2) THE ARTIFACT DOES NOT EXIST YET         <- NOT this TO
```

>> ⛔ **FIXING (1) ALONE STILL SHOWS HIM NO CARDS.** Cause (2) clears when `category_views` reaches the served plane on the **~13:30Z scheduled mdpf floor fire** — that is `D1_CATVIEWS.TO-P1-AE`'s `TP1AE-AC1`, currently undischarged, owned elsewhere and **NOT yours**.

⛔ **THEREFORE: DO NOT REPORT THIS AS "THE CARDS ARE FIXED", AND DO NOT ASK ANDREW TO RE-TEST ON THE STRENGTH OF IT.** ⚠ **If he re-tests after this lands and still sees nothing, the correct conclusion is "cause (2) is still open", NOT "the fix failed"** — and a report that omits this invites exactly that misreading.
⭐ **What this TO buys is that the transport is READY when the artifact appears**, so 13:30Z produces cards rather than a second investigation.

## 3. ⛔ WHAT YOU MUST NOT DO

- ⛔ **Do NOT create the artifact, seed a fixture at the served key, or stub the response to make cards appear.** That manufactures a green that Andrew's own eye would then be testing against nothing real.
- ⛔ **Do NOT run an ad-hoc `mdpf` gold run to make cause (2) clear.** It writes a REAL artifact at the REAL key and **DESTROYS the time-of-day discriminator `TP1AE-AC1` exists to produce.** Standing prohibition, unchanged.
- ⛔ **Do NOT change `API_BASE_URL` or the call site in `aum.ts`.** The relative URL is correct; the proxy is what is missing.
- ⛔ **`ETFS_SATELLITES` / `ETFS_POSITIONING` / `ETFS_INGEST`** — other projects. **Rule 27.**

## 4. ACCEPTANCE CRITERIA

| id | criterion | cell | status |
|---|---|---|---|
| `TX1DE-AC1` | **`/api/general` IS PROXIED IN `vite.config.ts`** — one entry, the **same CloudFront target as the `advisor-intelligence` rule**, with `changeOrigin`, `secure`, and the `proxyReq` hook that forwards `Authorization`. **Cite `file:line`.** | `D1-c-1` | |
| `TX1DE-AC2` | **THE SPA-FALLBACK FAILURE IS GONE, DEMONSTRATED BY WHAT COMES BACK.** Before: a request to `/api/general/...` returns `index.html` with a `200`. After: it must NOT. **Exhibit the response -- a status AND a content-type, not a claim.** **AMENDED ~05:0xZ by `2.0.0_SA_COO~Z` (issuer) on `3.0.0_SA_CVO~Z`'s pre-build finding (12940): MY ORIGINAL PASS SET ADMITTED A HALF-BUILT PROXY.** I wrote *"a 404 or 403 from the real origin is a PASS"*. ⛔ **A `401` ALSO PROVES "not the SPA fallback" AND IS NOT A PASS.** `api-client.ts:186`: ***ALL `api/general/*` PATHS NOW REQUIRE JWT.*** The proxy entries come in TWO SHAPES -- `/v1` and `/api/auth` have **NO `configure` block**, while `/api/scoped/advisor-intelligence` and `/api/scoped/satellites` **DO** and forward `Authorization`. **A `/v1`-shaped entry yields `401`, which would have passed AC2 while the Authorization forwarding -- the thing `AC1` requires -- was missing entirely.** >> **PASS = a status showing the request REACHED the origin AND was AUTHORIZED: a `404` or `403` for a genuinely absent artifact.** ⛔ **`401` = FAIL, and it names its own remedy: the `configure`/`proxyReq` block is absent.** ⛔ **`200` with `text/html` = FAIL (the original defect).** | `D1-c-1` | |
| `TX1DE-AC3` | ⛔ **THE `unavailable` STATE IS NOW HONEST, NOT MANUFACTURED.** With the artifact still absent, the page must reach `unavailable`/empty-block **by a real failed fetch**, not by a parse error on an HTML body. **`D1-c-2`'s empty-block fallback must still render.** | `D1-c-2` | |
| `TX1DE-AC4` | **EVERY PRE-EXISTING PROXY PREFIX STILL RESOLVES.** **AMENDED ~05:0xZ by `2.0.0_SA_COO~Z` (issuer): I WROTE "THE OTHER FIVE" AND ENUMERATED FIVE. `3.0.0_SA_CVO~Z`'s source read finds SIX** -- `/v1`, `/api/auth`, `/api/scoped/advisor-intelligence`, `/api/scoped/satellites`, `/api/scoped/partners`, **and `/api/partners`**, which my list dropped. ⛔ **AN ENUMERATED LIST THAT UNDER-COUNTS PASSES ITS OWN CHECK WHILE LEAVING THE MISSING MEMBER UNGUARDED** -- the same shape as a ban list that lapses when a name is added. >> **SO THE CRITERION IS NOW A DENOMINATOR, NOT A LIST: count the proxy keys in `vite.config.ts` BEFORE and AFTER, PRINT BOTH, and show `after == before + 1`.** **Name the six by reading them, do not trust this TO's enumeration -- it was already wrong once.** **A one-entry addition must not reorder or shadow an existing rule.** | `D1-c-1` | |
| `TX1DE-AC5` | **RENDERED, NOT GREPPED.** A read screenshot of the Model Portfolios view after the change. ⚠ **It will most likely still show no cards — that is the EXPECTED result while cause (2) is open, and the report must say so rather than presenting it as a failure.** **THE CANVAS IS SILVER.** | `D1-c-1` | |

## 5. REPORTING

Deliverable + read render + proof instance in this lane's `deliverables/`, via `.tools/safe-commit.sh --author "0.4.0_DE_ClientPlatform~S <0.4.0_DE_ClientPlatform~S@opal.agent>" -F <msgfile>` (message file by a **non-shell** writer). Report to `2.0.0_SA_COO~Z`; `3.0.0_SA_CVO~Z` certifies. **ACK on receipt, then report.**

⭐ **State plainly in the report that cause (2) remains open and names `TP1AE-AC1` / the ~13:30Z fire** — his item-1 bar is his eye, and a report that lets him expect cards costs him a wasted look.

<proof_of_spec>
  <criterion id="TX1DE-AC1" cell_refs="D1-c-1"/>
  <criterion id="TX1DE-AC2" cell_refs="D1-c-1"/>
  <criterion id="TX1DE-AC3" cell_refs="D1-c-2"/>
  <criterion id="TX1DE-AC4" cell_refs="D1-c-1"/>
  <criterion id="TX1DE-AC5" cell_refs="D1-c-1"/>
  <expected_criteria>TX1DE-AC1,TX1DE-AC2,TX1DE-AC3,TX1DE-AC4,TX1DE-AC5</expected_criteria>
  <alignment_denominators>cells declared: 2 (D1-c-1, D1-c-2); criteria: 5. FORWARD — 5 of 5 carry >=1 cell_ref. BACKWARD — 2 of 2 reachable (D1-c-1 from AC1/AC2/AC4/AC5, D1-c-2 from AC3). Unmapped 0; untraceable 0. NOTE: no cell is added — this is the TRANSPORT rung `D1-c-1` already presumes when it says the portal consumes the served views. AC2 is deliberately written so that a 404 or 403 from the real origin PASSES: the defect is an HTML-200 that makes `json()` throw, and a criterion demanding DATA would conflate this TO's cause with cause (2), which is a different owner's undischarged criterion (`TP1AE-AC1`, the ~13:30Z fire).</alignment_denominators>
</proof_of_spec>
