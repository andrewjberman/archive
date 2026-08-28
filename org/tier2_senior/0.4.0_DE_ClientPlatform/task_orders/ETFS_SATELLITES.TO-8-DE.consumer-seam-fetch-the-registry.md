# TO ETFS_SATELLITES.TO-8-DE — the CONSUMER SEAM: pass the FETCHED registry, and tell a fetch failure from an empty one

<decomp_ref>workflows/atom_decomposition/runs/etfs-satellites/20260827T160438Z/DECOMP.md — `SAT-a-4` (delivery form, CONSUMER half; the serving half is `TO-7-AE`) and `SAT-d-1` / `SAT-d-2` (the panels that consume the registry). **NO new cell.**</decomp_ref>
<certification>Decomp CERTIFIED (`3.0.0_SA_CVO~Z`). No cell added.</certification>
<issued_to>0.4.0_DE_ClientPlatform~S</issued_to>
<executor_class>DE-class (portal, `portal/**` on DEV)</executor_class>
<seating_trigger>⛔ **NEW LANE — letter measured free** (`0.4.0_DE_ClientPlatform~S`: 0 of 388 spawn-audit lines; only `~Y` and `~Z` exist, positive control fires on the two lanes spawned tonight). **Rule 27: `0.4.0_DE_ClientPlatform~Z` is on `ETFS_INGEST` (condition (ii) render) and CANNOT take this** — `ETFS_SATELLITES` is a different project.</seating_trigger>
<placement>SITE Z (Rule 26). ⛔ `portal/` is a WORK-SITE, never a base — address it explicitly and return to the workspace root. **Main tree stays on DEV (Rule 19).**</placement>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-28T01:4xZ</issued>
<status>complete -- ⭐ **CERTIFIED. THE CERTIFICATE EXISTS AND IS ON ORIGIN.** `cvoZ_ETFS_SATELLITES_TO8DE_TO9DE_CERTIFICATION_20260828.md` @`3f16f616f5`, verdict **CERTIFIED -- 5 of 5, INSTANCE VALID**. Located 15:1xZ by `3.0.0_SA_CVO~Z`; VERIFIED at this seat by containment against `origin/SITEZ` with a SOUND negative control (`origin/CLOUD` tip NOT contained, so the test demonstrably returns NO). ⛔ **THIS FACE PREVIOUSLY READ 'awaiting certification' AND WAS STALE -- the certificate POSTDATES it and nobody updated the face.** ROOT: the face and the certificate are TWO DURABLE RECORDS OF ONE FACT WITH NO NAMED PRIMARY -- the certifier writes one and cannot write the other, the issuer owns the face and has no trigger to return, so they diverge from minute one in the direction of 'outstanding'. Corrected by `2.0.0_SA_COO~Z` as ISSUER. ⚠ **BOUND, STATED BY ITS MEASURER AND NOT PAPERED OVER: this establishes A CERTIFICATE EXISTS for the criteria as they read AT CERTIFICATION TIME. It does NOT establish that no criterion was ADDED to this face afterwards -- that needs a per-face criterion-set diff, NOT RUN.**

⚠ **THE ORIGINAL `<status>` CONTENT FOLLOWS, RESTORED VERBATIM.** `2.0.0_SA_COO~Z` replaced it wholesale at @4253643625 instead of appending, destroying evidence on seven faces (142 lines on one of them). Recovered from `4253643625^` and re-attached. **NOTHING BELOW THIS LINE IS NEW; NOTHING ABOVE IT WAS IN THE ORIGINAL.**

complete — SELF-MARKED by the assignee `0.4.0_DE_ClientPlatform~S` 2026-08-28T02:2xZ per `org/XXX.md` ("`complete` = done (self-marked)"). **5 of 5 AC met.** Portal `d04c1599` on DEV; deliverable + 5 read renders + the served registry banked at `509f458cde` (`deliverables/deS_ETFS_SATELLITES_TO8_consumer_seam_20260828/`). **PUSH STATE: both LOCAL** — `origin/DEV = f1180aad`, `origin/SITEZ = c65ed351a7`, read by `ls-remote` + `is-ancestor` with a positive control; push is the integrator's act. ⚠ **`complete` ≠ SHIPPED:** the route is committed but NOT DEPLOYED (router pinned v24; 0 of 26 behaviors mention satellites), so against the live plane this seam correctly renders **fetch-failed** today. The deploy is `POSN_TENANCY.TO-4-AE`, currently under `2.0.0_SA_COO~Z`'s 11910 `[STOP]` — **not this lane's, and not a condition of this TO.** Awaiting `3.0.0_SA_CVO~Z` certification.</status>

## ⛔⛔ STALE BLOCKER RETIRED — MEASURED AT THE **APPLIED** PLANE 2026-08-28 15:0xZ

**Measured by `3.0.0_SA_CVO~Z` (msg 13264) on the DEPLOYED edge artifact, not the desired plane.
Recorded here by `2.0.0_SA_COO~Z` (the COO office issued this TO, so the face is this office's to
correct). `3.0.0_SA_CVO~Z` deliberately did NOT edit it.**

```
THIS FACE SAID           a router/deploy blocker was outstanding
MEASURED 15:0xZ          distribution EVTSA9VEHNZVH, Status Deployed, 27 behaviors
  /api/scoped/satellites/*  IS behavior #27; shared-advisor-router pinned :25, NOT :24
  public-data-router:7 DEPLOYED BYTES (pin resolved BY CONTENT -- downloaded + unzipped,
  never inferred from a version number, per Rule 22a):
      else if (b.uri.startsWith("/api/general/etfs/")) -> "/platinum/etfs/"
      else if (b.uri.startsWith("/api/general/"))      -> "/json/"
  >> THE etfs BRANCH IS ORDERED BEFORE THE CATCH-ALL, so the described fall-through CANNOT occur.
  CONTROLS: etfs 3 / json-tiered 3 / general 10 POSITIVE; satellites 0 / positioning 0 NEGATIVE
            -- the probe DISCRIMINATES; it is not matching everything.
  qualified_arn pin drop: all five routers read DYNAMIC qualified_arn [OK].
```
⭐ **THE ONE-APPLIER HAZARD THIS FACE RAISED IS MOOT:** `list-distributions` returns **EXACTLY ONE**
distribution, so the two router changes necessarily shared it. **The hazard was real when written and
is now settled by measurement.**

⚠ **DIRECTION, STATED: THIS FACE WAS *PESSIMISTIC*, WHICH IS THE SAFE DIRECTION.** It over-stated a
blocker rather than under-stating one, **and a pessimistic face announces itself the moment anyone
measures.** It was TRUE WHEN WRITTEN. ⛔ **The general fault is not this face's author: a `<status>`
block is a SNAPSHOT WITH NO FORWARD REFERENCE TO ITS OWN SUPERSESSION.** Two of them were read as live
state inside one hour today.

⛔ **THE RUNG REACHED IS *APPLIED*, NOT *EXERCISED*.** Deployed bytes and live distribution config were
read; **no authenticated request was issued through the route.** `auth-validator-edge:18` sits on both
behaviors, so an unauthenticated curl would 401 and produce a FALSE NEGATIVE. **"A real user is served"
remains unexercised by this measurement.**

⚠ **INSTRUMENT TRAP FOUND WHILE MEASURING, RECORDED BECAUSE IT WILL BITE THE NEXT PIN RESOLUTION:**
```
public-data-router     v7  2026-08-21T21:03:51   v6  2026-08-21T21:20:23
shared-advisor-router  v25 2026-08-28T02:29:53   v24 2026-08-28T02:46:27
```
**On BOTH routers the LOWER-numbered version is NEWER by wall clock.** ⛔ **"version number ascending ==
chronological" is FALSE on this estate, twice, on two different functions.** Cause NOT diagnosed and
none claimed. **Resolve a pin BY CONTENT, never by comparing version numbers.**


<priority>⛔ **P0 — with `TO-7-AE`, the END-TO-END BLOCKER on Andrew's item 2.**</priority>
<authority>**ANDREW-DIRECT 2026-08-28 ~01:3xZ:** *"End to end full 'Satellites' view mode on 'Positioning' page, including all backend and api work"*. Shape ruled by `1.0.0_SA_CTO~Z` (11617). Wire shape from the binding-now table, `ctoZ_SAT_TO2_PROMOTION_AND_VACUOUS_CORPUS_20260827.md`.</authority>

---

## 1. THE MEASURED STATE YOU ARE FIXING

`0.4.0_DE_ClientPlatform~Z` censused this (11540) — **carried as THEIR measurement, not re-derived:**

```
SATELLITE_REGISTRY appears in exactly 2 files, and EVERY use is a DEFAULT PARAMETER
  satelliteAdapter.ts:100 · satelliteSet.ts:106/112/173
Positioning.tsx:225  satellitesToPositioningShape(positioningData)   <- ONE ARGUMENT
POSITIVE CONTROL  positioning_data.json -> 8 files   <- the census instrument fires
```

⛔ **The second parameter always falls back to the compile-time constant, which `satelliteSet.ts:6-13`
ships EMPTY ON PURPOSE.** Nothing supplies a fetched one.

## 2. ⛔ THE SEAM ALREADY EXISTS. USE IT — DO NOT ADD ONE.

`satellitesToPositioningShape`'s second parameter **is** the registry, already defaulted. **The change
at `Positioning.tsx:225` is to PASS THE FETCHED VALUE.**

⛔ **Do NOT add a branch. Do NOT add a mode arm. Do NOT touch the Models or ETFs paths** — the adapter
was built so those stay **literally untouched**. ⭐ *If your diff grows a conditional, you have left the
ruled shape.*

## 3. ACCEPTANCE CRITERIA

| id | criterion | cell | status |
|---|---|---|---|
| `T8DE-AC1` | **The fetched registry reaches the adapter.** `Positioning.tsx:225` passes it; cite `file:line @ <commit-ish>`. ⛔ **The MODELS and ETFS paths are BYTE-UNCHANGED** — show the diff touches neither. | `SAT-a-4` | **MET** — `Positioning.tsx:280 @d04c1599`. Models/ETFS did-not-move at TWO layers: every removed diff line is satellites-only, AND a models render matched 1 of 2 fixtures (registry never requested; `enabled: isSatellites`). |
| `T8DE-AC2` | ⛔ **A FETCH FAILURE IS NOT AN EMPTY REGISTRY — DISTINGUISH THEM AT THE SEAM.** *"Rendering 'no satellites' because a route 404'd is the plausible-wrong-state twin of the plausible-wrong-number this page has already banked twice."* Three states must be separable and each must be exhibited: **served-empty** (a valid 200, renders "no satellites") · **fetch failed** (renders an error/unknown state, NEVER "no satellites") · **served-populated**. | `SAT-a-4` | **MET, EXHIBITED** — `T8DE_render_{populated,empty,failed}.png`. Separated at the READ SEAM; the render selects on QUERY STATUS, never on emptiness. |
| `T8DE-AC3` | **PUBLISH EMPTY, NEVER DELETE — honoured on the consumer side.** An empty `books` array is a **VALID SERVED STATE** meaning *"no satellites today"*, **not an error and NOT a reason to fall back to anything.** ⛔ **There is no fallback beneath the producer since @`24a8435642`; do not add one in the client.** | `SAT-a-4` | **MET** — no fallback beneath the read. `?? []` is 'nothing fetched yet'; an UNEXPLAINED absence fails toward *could not load*, never toward *no satellites*. |
| `T8DE-AC4` | **`as_of` NON-NULL ALWAYS, including on the empty set — a null RAISES.** The adapter unwraps `.books` from `{ books: SatelliteBook[], as_of }`; `SatelliteBook.code` is the **CANONICAL NAME verbatim**. | `SAT-d-1` | **MET, EXERCISED** — a null `as_of` carrying all NINE VALID BOOKS renders BYTE-IDENTICAL to a transport failure (sha256 `92225d65f302069f`), and distinct from `empty`/`populated`. Without the raise it would be indistinguishable from `populated`. |
| `T8DE-AC5` | ⛔ **RENDERED, NOT GREPPED.** Verify with a **read screenshot** (`/frontend-dev`), not a static check. ⚠ **The canvas is SILVER: light text or ghost-white buttons outside a dark Panel are the #1 recurring portal defect, and a grep cannot see contrast.** Show the satellites mode rendering real books. | `SAT-d-1` `SAT-d-2` | **MET** — 5 screenshots READ via `ui-smoke.mjs`. Canvas law holds: dark-on-light-tint notices, content inside dark Panels, no light text on the silver canvas. |

## 4. ⚠ WHAT THE REGISTRY CONTAINS TODAY — so you are not surprised

The producer publishes weights as **PERCENTAGE** (9 of 9 books sum to 100.000) after
`0.4.0_DS_ClientPlatform~L`'s unit fix @`48c6a7700f`, per `1.0.0_SA_CTO~Z`'s ruling *"the PRODUCER
converts, the consumer does not move."* ⛔ **Do NOT add a client-side conversion** — the contract at
`satelliteSet.ts:46-50` names the producer's seam as the conversion site in writing. ⭐ Before the fix
the consumer **refused all nine books** on its sum check; **that refusal was correct and must keep
working.**

## 5. NOT YOURS

⛔ **The route** — `ETFS_SATELLITES.TO-7-AE` (`0.7.0_AE_CloudOps~S`). ⚠ **Cross-gated deliberately:**
bundled, *you get a route with nothing reading it or a reader with no route, and neither failure
announces itself.* **Coordinate the wire shape; do not build the route.**
⛔ The PROD promote (**DT lane**, Rule 19 / `SAT-f-3`) · the producer · `D1_CATVIEWS` · `ETFS_INGEST`'s
condition-(ii) render, which is **`0.4.0_DE_ClientPlatform~Z`'s** — ⚠ **that lane is a DIFFERENT
INSTANCE ON A DIFFERENT PROJECT; do not coordinate your way into its diff.**

## 6. REPORTING

Deliverable + proof in this lane's `deliverables/` via `.tools/safe-commit.sh --author
"0.4.0_DE_ClientPlatform~S <0.4.0_DE_ClientPlatform~S@opal.agent>" -F <msgfile>` (non-shell writer).
Report to `2.0.0_SA_COO~Z`; `3.0.0_SA_CVO~Z` certifies. **ACK on receipt.**

<proof_of_spec>
  <criterion id="T8DE-AC1" cell_refs="SAT-a-4"/>
  <criterion id="T8DE-AC2" cell_refs="SAT-a-4"/>
  <criterion id="T8DE-AC3" cell_refs="SAT-a-4"/>
  <criterion id="T8DE-AC4" cell_refs="SAT-d-1"/>
  <criterion id="T8DE-AC5" cell_refs="SAT-d-1,SAT-d-2"/>
  <expected_criteria>T8DE-AC1,T8DE-AC2,T8DE-AC3,T8DE-AC4,T8DE-AC5</expected_criteria>
  <alignment_denominators>cells declared: 3 (SAT-a-4, SAT-d-1, SAT-d-2); criteria: 5. FORWARD — 5 of 5 carry >=1 cell_ref. BACKWARD — 3 of 3 reachable (SAT-a-4 from AC1/AC2/AC3, SAT-d-1 from AC4/AC5, SAT-d-2 from AC5). Unmapped 0; untraceable 0. NOTE: `SAT-a-4` is shared with `TO-7-AE` BY DESIGN — that TO closes its SERVING half, this one its CONSUMER half, and the cell is not discharged until both land. That shared-cell split IS the cross-gate.</alignment_denominators>
</proof_of_spec>
