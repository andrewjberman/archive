# TO ETFS_SATELLITES.TO-4 — the FIRM GATE (`modesFor(firm)`). **DE + AE. THE CLIENT-FACING EXPOSURE LIVES HERE.**

**Project:** `ETFS_SATELLITES` · **Directive:** D4 (SITEZ) · **Round:** 1
**Issued by:** `1.0.0_SA_CTO~Z` · 2026-08-27 ~17:4xZ
**Issued to:** **DE-class + AE-class, JOINTLY.** ⛔ **SEATS NOT ASSIGNED.** ⚠ **There is no AE seat on
this fabric** — `0.7.0_AE_CloudOps~Z` was closed out by Andrew. Seating is `0.0.0_AB_MSTR~Z`'s.
**Status:** ACTIVE · **Cells:** `SAT-c-1` `SAT-c-2` `SAT-c-3` · **Invariant:** `SAT-inv-4`

---

## 0. ⛔ WHY THIS IS ITS OWN TO — THE FINDING THAT SURVIVED EVERY REVIEW

The mode (`TO-3`) rides machinery that already exists. **This does not.** `SAT-c-1` measured **ZERO
firm-id references in the entire Positioning directory** — there is nothing to read from yet.

>> **A SINGLE TO READING "ADD THE SATELLITES MODE" COVERS THE FIRST AND SILENTLY NOT THE SECOND. THE
   FAILURE IS QUIET IN BOTH DIRECTIONS — either the pill renders for EVERY FIRM, or the gate exists
   with nothing behind it. On a multi-tenant surface the first is a CLIENT-FACING EXPOSURE THAT SHIPS
   GREEN.** <<

⛔ **DO NOT cite Rule 24 postulate (iv) as the reason for this split.** The decomp's v1 (iv)=FAIL was
**WITHDRAWN as an over-application** (Andrew caught it); **(iv) PASSES**. The split is a
**DECOMPOSITION point**. Citing the withdrawn verdict lets a certifier correctly reject the citation
and **the real finding dies with it.**

---

## 1. `SAT-c-1` — THE VIEWER-FIRM SOURCE IS **ALREADY NAMED**. DO NOT RE-DERIVE IT.

`SAT-c-1`'s prerequisite — *"the viewer-firm source is named with its `file:line @ commit`; a gate
written against an unnamed source is INFERRED and non-actionable"* — is **DISCHARGED** at
`org/tier1_exec/1.0.0_SA_CTO/deliverables/ctoZ_SAT_C2_MODESFOR_FIRM_FOUR_POSTULATE_RECORD_20260827.md` §1.

**All citations at portal `origin/DEV 4ac152f8`:**

```
AuthContext.tsx:196-201, :348-354   claims = parseClaims(meData.user)  <- GET /auth/me + bearer
                                    => THE FIRM IS SERVER-DERIVED. The client does not assert it.
AuthContext.tsx:354                 FALLBACK on /auth/me FAILURE:  claims = { firmId: null, ... }
AuthContext.tsx:583-588             canAccessFirm: 'opal-capital' -> true; else EXACT match
firmAccess.ts:18                    INTERNAL_FIRM_ID = 'opal-capital'
firmAccess.ts:65,:73                'cottonwood' allowlist CONTAINS '/positioning'
firmAccess.ts:99-106                isPathAllowedForFirm: ... ?? false     <- DENY-ALL DEFAULT
AuthContext.tsx:499-545             devBypass -- DEV-ONLY (import.meta.env.DEV), window.__devBypass.
                                    NOT the production path. Named so you do not mistake it for a hole.
```

⚠ **VINTAGE:** the local portal submodule read `eaa094e6`, **2 behind**, and **`src/lib/firmAccess.ts`
is one of the 5 files those commits touched.** Read from `origin/DEV`, not the working tree.

## 2. ⛔ `SAT-c-2` — `modesFor(firm)`. THE FOUR-POSTULATE RECORD IS AUTHORED; **(i) FAILS AS NAIVELY STATED.**

Rule 24 binds — *"predicates ARE schemas"* — and CVO's **F2 (P1)** required the record **before this
TO was cut**. It is authored (link above). **Its finding changes what you build:**

The decomp reads *"Cottonwood + Opal see three pills; every other firm sees two."*

>> ⛔ **`null` IS NOT A FIRM, SO IT IS NOT COVERED BY "EVERY OTHER FIRM."** `AuthContext.tsx:354`
   produces `firmId: null` when `/auth/me` **FAILS** — an authenticated session whose firm is
   **UNKNOWN**, not absent. **The domain is `firms ∪ {null}` and the naive statement has an uncovered
   member. CE FAILS until `null` is covered.** <<

**THE REMEDY IS ONE LINE, AND THE EXISTING CODE ALREADY MODELS IT:** declare the mapping **TOTAL**
over `firms ∪ {null}`, with **`null` → the TWO-pill set**, mirroring `isPathAllowedForFirm`'s
`?? false` deny-default. ⛔ **Fail CLOSED. A `null` firm must never see the satellites pill** — that
is the identity service being down handing out a third firm's view.

**(ii) SAME GRAIN, (iii) INTENT COHERENCE, (iv) STATE COHERENCE all PASS** — see the record. **Token
census: `modesFor` = 0 hits / 407 files, `satellites` = 0 hits. Both NET-NEW, colliding with nothing.**

**ORACLE — and the NEGATIVE CONTROL IS THE LOAD-BEARING ONE:**
- a non-Cottonwood viewer gets **two** pills, **AND**
- ⛔ **cannot reach the satellites mode BY HAND-EDITING THE PERSISTED TOGGLE.** The mode is
  session-persisted; the persistence layer validates a stored value. **Exercise the tamper.**
- **AND the `null`-firm case**: `/auth/me` failure → two pills, never three.

## 3. `SAT-c-3` — THIS IS A **VISIBILITY** GATE, NOT AN **AUTHORIZATION** BOUNDARY, AND YOU MUST SAY SO

The underlying models payload **is already served to this viewer**; satellites are **arithmetic over
it**. **State that on the artifact's face.**

⛔ **IF IT IS MEANT TO BE AN AUTHORIZATION BOUNDARY, THAT IS A DIFFERENT DESIGN AND A DIFFERENT
REVIEW** — and a client-side decision in `bookSet.ts` would not be adequate for it. **Say which, and
do not let the answer drift by default.** The four-postulate record §2.2 states the constraint; this
criterion is where it is discharged.

## 4. `SAT-inv-4` — OTHER FIRMS UNCHANGED

**Two pills, byte-identical behaviour.** This is a **REGRESSION assertion, exercised rather than
assumed.**

<decomp_ref>workflows/atom_decomposition/runs/etfs-satellites/20260827T160438Z/DECOMP.md @936b9ae1e9 — cells `SAT-c-1` `SAT-c-2` `SAT-c-3`, invariant `SAT-inv-4`. Four-postulate record for `modesFor`: `org/tier1_exec/1.0.0_SA_CTO/deliverables/ctoZ_SAT_C2_MODESFOR_FIRM_FOUR_POSTULATE_RECORD_20260827.md`.</decomp_ref>
<certification>**CERTIFIED WITH FINDINGS** @`205546c65c`, amended @`a025e2be91`. **CVO F2 (P1) is discharged by the four-postulate record linked above and is submitted for certification like any other artifact** — the issuer authoring it is not the issuer certifying it.</certification>
<issued_by>1.0.0_SA_CTO~Z</issued_by>
<issued>2026-08-27T17:4xZ</issued>
<status>ACTIVE — unblocked on its merits; waiting on TWO SEATS (DE + AE), and there is no AE seat on this fabric today.</status>

<proof_of_spec>
  <!-- ISSUANCE half (1.0.0_SA_CTO~Z). POSITIONAL:
         python .tools/proof-of-spec-check.py <instance>.json SAT-TO4-AC1,SAT-TO4-AC2,SAT-TO4-AC3,SAT-TO4-AC4,SAT-TO4-AC5
       CHECK THE RC, NEVER THE OUTPUT STRING; WITHOUT A PIPE. Coverage diff is BIDIRECTIONAL. -->
  <criterion id="SAT-TO4-AC1" cell_refs="SAT-c-1"/>
  <criterion id="SAT-TO4-AC2" cell_refs="SAT-c-2"/>
  <criterion id="SAT-TO4-AC3" cell_refs="SAT-c-2"/>
  <criterion id="SAT-TO4-AC4" cell_refs="SAT-c-3"/>
  <criterion id="SAT-TO4-AC5" cell_refs="SAT-inv-4"/>
  <expected_criteria>SAT-TO4-AC1,SAT-TO4-AC2,SAT-TO4-AC3,SAT-TO4-AC4,SAT-TO4-AC5</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/ETFS_SATELLITES.TO-4_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Acceptance criteria

| id | criterion | cell_refs | grounding layer |
|---|---|---|---|
| **`SAT-TO4-AC1`** | The gate reads the **NAMED** viewer-firm source (`AuthContext` claims via `/auth/me`), cited `file:line @ commit-ish` in the delivered code's own comment. ⛔ **Do NOT read `window.__devBypass` or any client-settable value as the firm** | `SAT-c-1` | **SOURCE** |
| **`SAT-TO4-AC2`** | `modesFor(firm)` is **TOTAL over `firms ∪ {null}`**. ⛔ **`null` → TWO pills. Fail CLOSED**, mirroring `isPathAllowedForFirm`'s `?? false`. **Exercise the `/auth/me`-failure path** and assert the satellites pill is absent — an identity outage must never hand out a third firm's view | `SAT-c-2` | **EXERCISED (null arm)** |
| **`SAT-TO4-AC3`** | ⛔ **THE NEGATIVE CONTROL IS THE LOAD-BEARING ONE:** a non-Cottonwood viewer gets two pills **AND CANNOT REACH the satellites mode by HAND-EDITING THE PERSISTED TOGGLE.** Exercise the tamper and show the refusal. A positive-only test proves the gate runs, not that it gates | `SAT-c-2` | **EXERCISED, both arms** |
| **`SAT-TO4-AC4`** | The artifact **STATES ON ITS FACE** that this is a **VISIBILITY** gate, not an authorization boundary, with the reason (the models payload is already served; satellites are arithmetic over it). ⛔ If the intent is authorization, **say so and STOP** — different design, different review, not a client-side decision | `SAT-c-3` | **ARTIFACT (declaration)** |
| **`SAT-TO4-AC5`** | `SAT-inv-4`: **other firms byte-identical**, two pills, exercised **not assumed**. Byte-diff a non-Cottonwood viewer's rendered payload pre- and post-change | `SAT-inv-4` | **EXERCISED + diff** |

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step><run>comp-blast on the auth/claims accessor you intend to call</run><expect>Auto-Rule 6 -- every call site of a shared predicate surfaced before patching</expect></step>
    <step><run>comp-routes trace /positioning</run><expect>the full serving path incl. the auth leg -- the AE half of this TO lives here</expect></step>
    <step><run>comp-iam service &lt;lambda&gt;</run><expect>Auto-Rule 3 IF the AE half touches a boto3 call, CF behavior, SSM target or a new S3 prefix; comp-iam gaps at Phase 2 if iam.tf changed</expect></step>
  </phase>
  <phase id="2" when="before commit">
    <step><run>bunx tsc -b (portal)</run><expect>ZERO typescript errors</expect></step>
    <step><run>/frontend-dev render as BOTH a Cottonwood and a non-Cottonwood viewer</run><expect>three pills vs two; silver-canvas colour law clean</expect></step>
  </phase>
  <phase id="3" when="after commit"><step><run>comp-routes trace /positioning (re-run)</run><expect>no new unauthenticated path to the satellites data</expect></step></phase>
</compiler_tools_mandate>

## Standing constraints

**DE commits portal; DT pushes and promotes** (Rule 19: main worktree stays on DEV). **AE owns
infra/IAM** — `1.0.0_SA_CTO~Z` cannot commit `infra/aws/**` (measured this session: lane
`CLOUD_OPS_OR_ETL` refused it). **No alarm/SNS/SES/monitor.** Report **"LOCAL @hash"**. Surprise
channel `org/surprise_channel/ETFS_SATELLITES/` opens on first item, **filed by `3.0.0_SA_CVO~Z`**.
**Mid-round the spec is FROZEN: route, do not adjudicate.**

-- `1.0.0_SA_CTO~Z`, issuer
