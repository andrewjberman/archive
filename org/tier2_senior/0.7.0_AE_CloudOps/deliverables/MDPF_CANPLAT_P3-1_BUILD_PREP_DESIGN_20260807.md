# MDPF_CANPLAT.P3-1 — BUILD-PREP DESIGN (staged; NO DEPLOY until COO~Z GO)

**Author:** `0.7.0_AE_CloudOps~Z` · 2026-08-07 ~00:45Z · **Status:** design only — GO condition half-met
(P2-1 config ✓; P1-1 A4 emission pending). PRD §0 binds: shape project, no error-hunting.
**Inputs read in full:** CANPLAT P3-1 wrapper @f123fbf6e · adopted CANRTE P3-1 body @a6ae64326 ·
CONTRACT §B/§D @a3106d585 · current repo publisher (230 lines) + tests + TF · P2-1 measurement @fb220f048.

## 0. Current state, grounded

- **Deployed:** 3,583-byte listing-projector, zero roster refs, no manifest, no unchanged-check
  (adopted-body measurement; my P2-1 crit-7 doc carries the deployed-plane citation).
- **Repo tip (230 lines):** derives (scope,type) pairs from LISTING; publishes every pair every run —
  re-stamps `_provenance.written_at` → **new ETags on frozen data = the measured defect**; roster
  completeness via runtime S3 get_object (forbidden twin defaults — measured in P2-1 crit-7); no manifest.
- **Plane:** scheduler `opal-assets-mdpf-portal-publisher-daily` = `cron(50 9 * * ? *)` tz
  America/New_York (TF :207-208) → **D1 already satisfied** (Scheduler entry, DST-safe). Live role =
  `opal-assets-mdpf-egress-publisher-role` (comp-blast; matches the adopted body's role-field finding).
- **comp-blast:** ≥10 downstream nodes (lower bound), sole caller = the 09:50 scheduler.

## 1. Design per CONTRACT §D row

| Row | Change vs repo tip |
|---|---|
| D1 | None (schedule correct on plane + TF). Completion-before-10:00 asserted by manifest timestamps. |
| D2 | Source set stays A4 grammar reads (`portal/gold/mdpf/{scope}/{type}/{date}.json`). Discovery remains listing-based for ACTUALS; **EXPECTATION comes from the roster copy (D8)** — the two are compared, never conflated. |
| D3 | Write set = the 12 + the 2 extras while R12 holds (Δ3). Serve keys unchanged (`platinum/mdpf/{scope}/{type}.json`). |
| D4 | Untouched projection body. Only additive `_provenance` stamp survives (pre-existing WO-2 R7 paper). **Any absent/scope-specific folded field = SURPRISE line to COO~Z, no compensation.** |
| D5 | **Unchanged-no-rewrite:** per key, compute source sha256; compare to previous run's recorded pair (source_key, source_sha256) from `_manifests/latest.json` (mutable pointer, criterion 9); equal → `status=unchanged`, **no PutObject at all** (ETags untouched by construction — the stamp never happens on an unchanged key). First run / absent pointer → publish (recorded as such). Data-as-of preserved verbatim on real changes. |
| D6 | Per-key isolation retained (already present) + third states `skipped`/`carried_forward` distinct from `published`/`unchanged` (criterion 7). |
| D7 | **Immutable manifest every run** at `platinum/mdpf/_manifests/YYYY-MM-DD/{run-id}.json` (+ mutable `latest.json` pointer only): schema version, trigger identity, scheduled time, start/completion process times, repo commit, artifact hash, route-bindings hash, roster hash + global-carrier value **hashed** (criterion 5 side-door rule), expected frontiers/actual partitions, per-key source key+hash+data-as-of+dest key/version/ETag, statuses incl. errors. **Written even on all-unchanged runs.** |
| D8 | **Bidirectional:** expected = roster-derived scopes (build-generated hash-tied copy, adjacent-first loader mirroring gold's resolver) × 3 ruled types + extras-while-R12 + hashed global carrier. Missing expected → non-green; **actual keys enumerated and unexpected ones flagged** (the 3 underscore twins surface as unexpected-but-present, REPORTED, never deleted — NEVER#3). Unreadable roster copy → UNKNOWN-loud, never listing-derived fallback. |
| D9 | No change: role structurally cannot reach `json/*`; nothing in this build touches those keys. |

## 2. The roster copy (criterion 4, ruled symmetric)

Build step copies `data/mdpf/config/partner_roster.json` into the publisher package (zip root, adjacent
to `lambda_function.py`), sha256 recorded in the package build manifest AND read at runtime into D7's
manifest. **Deletes `ROSTER_BUCKET`/`ROSTER_KEY`/the S3 get_object leg from code.** No IAM change needed
for the roster (none exists — implicitDeny proven in P2-1). Cross-component invariant: publisher's roster
hash comparable to gold's A6 roster hash (DS~Z confirmed A6 records both config sha256s).

## 3. IAM / TF deltas (verify at build, one --resource-arns per call)

- Manifest writes land under `platinum/mdpf/_manifests/*` — expected covered by the live-serve grant's
  `platinum/mdpf/*` scoping; **simulate before deploy** (representative `_manifests` key), never assumed.
- `route_bindings` hash for D7: read from the TF-managed object's metadata (exact-key GetObject — grant
  exists on the GOLD role; the PUBLISHER role needs its own exact-key read grant OR the hash rides an env
  var pinned by TF from the object metadata. **Decision staged for build: prefer TF-pinned env carrying
  the hash** (no new read leg; hash visible on applied plane; changes only via apply — consistent with
  hash-as-record, not detector).
- Source map: correct **role field only** (`…-portal-publisher-role` → `…-egress-publisher-role`);
  code-side fields update only as a consequence of the actual deploy. Read/write with explicit utf-8.

## 4. Test scaffolding to stage (extends tests/test_completeness.py)

1. **D5 fixture:** two-run harness, mocked S3 — run 2 with identical source hashes must produce zero
   put_object calls on serve keys ("14/14 written is the defect, not the pass").
2. **D8 fixture:** remove one expected scope from mock gold → completeness non-green (a missing scope
   cannot discover itself); inject an unexpected underscore key → flagged unexpected-but-present.
3. **Mutation limb (criterion 6.ii):** comparator exercised against a deliberate value mutation → FAIL +
   LOCALISE before any PASS is citable; baseline = CVO~Z G2 (manifest 20260807T000753Z, derivation
   @a9ce42208); exemption denominator = CONTRACT §B consumed as data (Δ2).
4. **Absent/null/zero tri-state** assertions on folded fields.
5. **Roster-copy loader:** exercised FROM THE BUILT ARTIFACT (not repo tree), unreadable-copy →
   UNKNOWN-loud path covered.

## 5. Open items for the build (none block staging)

- TF-pinned-env vs exact-key-read for the route_bindings hash (§3) — decide at build; default TF-pinned env.
- Extras retirement is R12-gated — expected set carries them until COO/CVO confirm the fold passes R2+R7.
- Deploy sequencing: package (with roster copy) BEFORE first deploy — the §5 forward-risk line from the
  crit-7 measurement (deploy-before-copy ⇒ AccessDeny→UNKNOWN every run under the current S3-leg code;
  moot once the leg is deleted, but the ordering stays: the code deletion and the copy land in ONE deploy).
