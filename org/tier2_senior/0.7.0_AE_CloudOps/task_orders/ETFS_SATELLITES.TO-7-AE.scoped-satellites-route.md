# TO ETFS_SATELLITES.TO-7-AE — the SCOPED satellites route (the API leg Andrew named)

<decomp_ref>workflows/atom_decomposition/runs/etfs-satellites/20260827T160438Z/DECOMP.md — `SAT-a-4` (DELIVERY FORM — *"an OPEN CUT and is mine to make: served block vs portal-fetched vs build-time constant"*; this TO closes it as **portal-fetched via a scoped route**) and `SAT-c-2` (firm resolution is server-derived, never client-asserted). **NO new cell.**</decomp_ref>
<certification>Decomp CERTIFIED (`3.0.0_SA_CVO~Z`). No cell added; `SAT-a-4` was left explicitly open for the issuer to close and this TO closes it.</certification>
<issued_to>0.7.0_AE_CloudOps~S</issued_to>
<executor_class>AE-class (route / serving plane / IAM)</executor_class>
<seating_trigger>SEATED — **same project (`ETFS_SATELLITES`), same instance, Rule 27 satisfied.** ⭐ This lane declined the `etfs-positioning` apply on Rule 27 grounds (11565) and was right; **this is in-project and is the work its idle AC3 window should take.** Begin now.</seating_trigger>
<placement>SITE Z (Rule 26).</placement>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-28T01:4xZ</issued>
<status>complete — 7 of 7 criteria PASS, CERTIFIED by `3.0.0_SA_CVO~Z` @`fce6aaaa4c` (coverage step-zero run: the TO's declared set and the instance's filed set are identical, set-for-set). Self-marked by the assignee `0.7.0_AE_CloudOps~S` 2026-08-28 ~03:3xZ per `org/XXX.md`, on `2.0.0_SA_COO~Z`'s dispatch 12427. THE ROUTE IS LIVE: `/api/scoped/satellites/*` at `shared-advisor-router:25`, applied 02:29:53Z (0 added / 2 changed / 0 destroyed, re-plan clean), tag `portal-auth-v1.24.0`, deploy ledger CLOSED @`40781748c1`. AC3's authenticated half was discharged by `0.4.0_DE_ClientPlatform~S` @`80f42be356` (served bytes sha256-identical to the object at the key) and is CREDITED to them in the proof instance rather than absorbed. ⚠ **COMPLETE DOES NOT MEAN THE SATELLITES VIEW WORKS** — two rungs remain and neither is this TO's: the consumer seam (`ETFS_SATELLITES.TO-8-DE`) and `Z-S16`, where internal `opal-capital` viewers see the pill and the fetch behind it 400s (ruled by `1.0.0_SA_CTO~Z` a UI-selection gap, not a router defect — an internal viewer is not a firm, so there is no default bucket to resolve). ⚠ The COTTONWOOD path is INFERRED FROM SOURCE ONLY and was never exercised: no cottonwood credential exists on this device, and a forged firm claim was ruled out because it would test the boundary by circumventing it. ⛔ The leading token is bare `complete` ON PURPOSE — `to-check.py:_classify_status` reads the FIRST TOKEN ONLY, so `**COMPLETE**` or an emoji prefix indexes as ACTIVE. HISTORY, kept rather than overwritten: this face read "ACTIVE — BUT THE FIRST ACT IS A TEST, NOT A BUILD" (amended ~01:4xZ, before the seat could act). That amendment is why the TO collapsed to a verification plus a rebuild instead of a build — `T7AE-AC0` found the route already existed in source at `/api/scoped/satellites/`, a DIFFERENT prefix than the relay named.</status>
<priority>⛔ **P0 — THE END-TO-END BLOCKER.** With `TO-8-DE` this is the ONLY thing between a correct published artifact and a rendered page. **The producer could run correctly on a schedule forever and the view would still render empty** without these two.</priority>
<authority>**ANDREW-DIRECT 2026-08-28 ~01:3xZ, VERBATIM:** *"End to end full 'Satellites' view mode on 'Positioning' page, **including all backend and api work**"* — he named this leg himself. Shape ruled by `1.0.0_SA_CTO~Z` (11617). Firm-boundary law: CLAUDE.md NEVER (BUCKET *or* KEY-PREFIX).</authority>

---

## 1. WHY THIS EXISTS — measured, and it is the finding of the night

`0.4.0_DE_ClientPlatform~Z` censused the portal (11540), carried here as **theirs**:

```
satellites/registry  0 files · registry.json 0 files · satelliteRegistry 0 files
satellites.json      0 files · getSatellite  0 files · apiRequest mentioning "satel"  NONE
POSITIVE CONTROL  positioning_data.json -> 8 files          <- the instrument fires
SATELLITE_REGISTRY appears in exactly 2 files and EVERY use is a DEFAULT PARAMETER
Positioning.tsx:225 calls satellitesToPositioningShape(positioningData) with ONE ARGUMENT
```

⛔ **THERE IS NO FETCH PATH. The registry parameter always falls back to the compile-time constant,
which ships EMPTY on purpose.** Every other satellites cell is upstream of a disconnect.

## 2. THE SHAPE — RULED, not open for redesign

**ANDREW ~22:1xZ 2026-08-27, VERBATIM — and this is the SELECTION CRITERION, not a nicety:**
> *"I think it is better to just do a scoped api path for the satellites, that way we dont have to mess
> with the rest of the plumbing of the page and it is inobtrusive + if we decide later that it makes
> more sense to just handle this elsewhere, then doing so is not a massive effort."*

⭐ **HE PRICED REVERSIBILITY OVER CORRECTNESS-TODAY.** Build the cheap-to-unpick thing.

- **(a) SCOPED ROUTE, SATELLITES ONLY.** ⛔ **Do NOT fold the registry into `positioning_data.json`.
  Do NOT generalise the serving plumbing.** `MODELS` and `ETFS` payloads stay untouched and general.
- **(b) FIRM RESOLUTION IS THE BUCKET, NEVER A KEY SEGMENT.** `platinum/satellites/registry.json`
  carries **no firm segment ON PURPOSE** — the bucket **IS** the boundary. Resolve firm → bucket
  exactly as `shared-advisor-router` already does (`FIRM_BUCKET_MAP`, cottonwood → `opal-data-cot`).
  ⛔ **A route that builds a firm-segmented KEY re-introduces "a second, forgeable expression of the
  same boundary"** — the router's own words, and the defect `0.4.0_DS_ClientPlatform~L` just fixed on
  the producer side. **Do not re-introduce it on the serving side.**

## 3. ACCEPTANCE CRITERIA

| id | criterion | cell | status |
|---|---|---|---|
| `T7AE-AC0` | ⛔⛔ **EXERCISE THE EXISTING ROUTE BEFORE BUILDING ANYTHING. BUILD ONLY WHAT THIS TEST PROVES ABSENT.** Call `/api/scoped/advisor-intelligence/platinum/satellites/registry.json` against the live plane and report the status and body. **TWO BOUNDS MAKE THIS NON-OPTIONAL, both from `comp-routes`' own coverage notes:** (1) ⛔ **that tool reads the DESIRED plane ONLY** — it parses committed `.tf` and router source and *"a drifted distribution or a pinned stale Lambda@Edge version reads identical here"*, so **presence in the rewrite table is NOT evidence the route is live**; (2) ⛔ **a 401 REFUSAL exists on the SAME PREFIX** (*"Platinum summary files must be accessed through the API, not S3-direct"*), reportedly scoped to `platinum/**/summary.json` — **CONFIRM `registry.json` is not caught by it. A refusal yields REFUSED WITH NO KEY, and a prefix-only reading renders that as a resolved key** — a false-secure read that looks like success. **If the route serves the object: AC1 and AC2 are discharged by EXHIBITING it, and this TO is a verification. If it does not: build, and §2's shape binds.** | `SAT-a-4` | |
| `T7AE-AC0b` | ⛔⛔ **AC0's ANSWER CAME BACK "ROUTE CODE EXISTS, ARTIFACT IS STALE" — SO THE REMAINING WORK IS A REBUILD, AND IT IS THIS TO's. ADDED 2026-08-28 ~02:2xZ.** ⛔ **THE `[STOP]` ON ANY `portal-auth` APPLY (msg 11906) IS LIFTED ONLY BY THIS CRITERION.** Applying first would wire `/api/scoped/satellites/*` to `shared-advisor-router:24`, **which does not contain the satellites code** — the route goes live **DEAD** while the apply succeeds, the behavior exists for any census, and `comp-routes` shows it. **Only the request fails, as a 403/404 indistinguishable from a refusal.** <br>**THE TOOL EXISTS — Build Ladder rung 2, write nothing:** `infra/aws/lambda/ci/build-nodejs-lambda.sh portal-auth shared-advisor-router` — it bundles (`:243`/`:256`), makes a **deterministic zip** (`:307`), uploads to the artifact bucket (`:60`/`:79`) and **updates `lambda-source-map.json`** (`:192`). <br>**REQUIRED:** (1) rebuild + upload from `@40697fe79d`; (2) ⛔ **CONTENT-VERIFY THE NEW ARTIFACT WITH LITERALS ONLY** — `bun build --format=esm` inlines deps and **minification destroys IDENTIFIERS while preserving STRING LITERALS**, so an identifier probe returns a false absence; show `'/api/scoped/satellites/'` and `'platinum/satellites/registry.json'` PRESENT with a **negative control**; (3) **read the CI gate's COUNTS, not its rc** — it has a recorded history of failing CLOSED (`ReferenceError: require is not defined` before reading a single spec). ⭐ **The suite DOES cover satellites** — `test/satellites-registry.spec.mjs`, 10 cases incl. a two-firm negative arm — **measured, correcting an earlier unmeasured caution.** ⚠ **But a passing suite does not put bytes in S3: the CONTENT check is the precondition, not the gate.** | `SAT-a-4` | |
| `T7AE-AC1` | **The route EXISTS and is SCOPED to satellites.** Cite `file:line @ <commit-ish>`. ⛔ **Show `positioning_data.json`'s payload and the MODELS/ETFS paths are BYTE-UNCHANGED** — a did-not-move control, not an assertion. | `SAT-a-4` | |
| `T7AE-AC2` | ⛔ **FIRM → BUCKET, AND THE KEY CARRIES NO FIRM SEGMENT.** Show the resolved key for cottonwood is exactly `platinum/satellites/registry.json` in `opal-data-cot`. **NEGATIVE CONTROL: a request for a firm the caller is not entitled to must not return another firm's object** — exhibit the refusal, do not assert it. | `SAT-c-2` | |
| `T7AE-AC3` | **APPLIED and EXERCISED, not just declared.** `safe-apply` (never bare); read back from the live plane; then **actually call the route** and show the served bytes match the object at the key (size/ETag). `DESIRED ≠ APPLIED ≠ EXERCISED`. | `SAT-a-4` | |
| `T7AE-AC4` | ⛔ **THE EMPTY SET IS A VALID 200, NOT AN ERROR.** `{ books: [], as_of: <non-null> }` must serve as a normal success. ⚠ **And a MISSING key must NOT be synthesised into an empty set** — the edge synthesis was REMOVED @`24a8435642` precisely because it converted **both 403 and 404** into `200 {books: []}`, reporting a **refusal** as *"this firm has no satellites."* **Do not re-create it.** | `SAT-a-4` | |
| `T7AE-AC5` | **`as_of` IS NON-NULL ALWAYS, INCLUDING ON THE EMPTY SET — a null RAISES.** The route must not strip, default, or synthesise it. | `SAT-a-4` | |

## 4. NOT YOURS

⛔ **The consumer seam** — `Positioning.tsx:225` and `satellitesToPositioningShape`'s second parameter
belong to **`ETFS_SATELLITES.TO-8-DE`** (`0.4.0_DE_ClientPlatform~S`). ⚠ **Cross-gated on purpose:**
bundled into one lane you get *a route with nothing reading it, or a reader with no route, and neither
failure announces itself.* **Coordinate the wire shape; do not implement the other half.**
⛔ The producer (`0.4.0_DS_ClientPlatform~L`) · `ETFS_SATELLITES.TO-6-AE` is **also yours** and is
unchanged — this TO does not displace it · the PROD promote (Andrew's word) · `ETFS_INGEST` anything.

## 5. REPORTING

Deliverable + proof in this lane's `deliverables/` via `.tools/safe-commit.sh --author
"0.7.0_AE_CloudOps~S <0.7.0_AE_CloudOps~S@opal.agent>" -F <msgfile>` (non-shell writer). Report to
`2.0.0_SA_COO~Z`; `3.0.0_SA_CVO~Z` certifies. **ACK on receipt.** ⛔ Ledger entry for any apply.

<proof_of_spec>
  <criterion id="T7AE-AC0" cell_refs="SAT-a-4"/>
  <criterion id="T7AE-AC0b" cell_refs="SAT-a-4"/>
  <criterion id="T7AE-AC1" cell_refs="SAT-a-4"/>
  <criterion id="T7AE-AC2" cell_refs="SAT-c-2"/>
  <criterion id="T7AE-AC3" cell_refs="SAT-a-4"/>
  <criterion id="T7AE-AC4" cell_refs="SAT-a-4"/>
  <criterion id="T7AE-AC5" cell_refs="SAT-a-4"/>
  <expected_criteria>T7AE-AC0,T7AE-AC0b,T7AE-AC1,T7AE-AC2,T7AE-AC3,T7AE-AC4,T7AE-AC5</expected_criteria>
  <alignment_denominators>cells declared: 2 (SAT-a-4, SAT-c-2); criteria: 7. FORWARD — 7 of 7 carry >=1 cell_ref. BACKWARD — 2 of 2 reachable (SAT-a-4 from AC1/AC3/AC4/AC5, SAT-c-2 from AC2). Unmapped 0; untraceable 0. NOTE: this TO CLOSES `SAT-a-4`, which the decomp left as an explicitly OPEN issuer cut ("served block vs portal-fetched vs build-time constant"); the answer is portal-fetched via a scoped route, per Andrew's ~22:1xZ reversibility ruling. No cell is added.</alignment_denominators>
</proof_of_spec>
