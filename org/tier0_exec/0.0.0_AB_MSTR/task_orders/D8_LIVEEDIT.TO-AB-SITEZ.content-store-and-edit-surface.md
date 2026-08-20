# TO D8_LIVEEDIT.TO-AB-SITEZ — Philosophy + Benchmark modal live-edit: store/API + edit surface (SITEZ author+build)

<task_order id="D8_LIVEEDIT.TO-AB-SITEZ" project="D8_LIVE_EDIT_MODALS">
<issued_to>site Z, seats assigned by 0.0.0_AB_MSTR~Z (TO-A AE-class, TO-B DE-class)</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-19T20:05Z</issued>
<dated>HELD -- ferries when a sitez seat frees OR Andrew accepts 7 sustained (MSTR surfaces that ask with this package)</dated>
<status>staged -- package READY, deliberately NOT ferried. D8's DE~Z seat is the BURST-CROSSER.</status>
<priority>P1-program, but the LOWEST-COST DELAY of the three sitez items -- already accepted with both riders bound on their trunk (@12cf17a81d), so nothing decays while it waits</priority>
<authority>D8_LIVE_EDIT_MODALS_PRD.md §4.1/§4.2 + §6 rows 1-2 at dispatch vintage @7416fb46d0 (CVO verdict @a9a173e7fa absorbed: PK ruled stable-identifier-never-display-name; BOTH Q3 failure directions stated; write-API precedent scoped). Placement: SITEZ per Andrew's ~19:37Z word, CTO FINAL 193804Z.</authority>
</task_order>

## KICKOFF TRIPLE (explicit, never implicit)
- **prd:** `docs/architecture/D8_LIVE_EDIT_MODALS_PRD.md`
- **workstream:** TO-A (store + API) and TO-B (edit surface, both families). **NOT TO-C.**
- **head_version:** `@7416fb46d0`

## ⛔ TO-C IS NOT IN THIS PACKAGE — IT STAYS AT CTO's GATE
TO-C is the auth-surface gate ruling (editor set all-internal vs admin-only; claim-shape
sufficiency). **It is governance and it stays with CTO** — item placement moves build labor, never
established governance chains. **It BLOCKS TO-A's CLAIM-CHECK FINALIZATION, but NOT TO-A's TF or
scaffold start.** Start; finalize the claim check when the ruling lands.

## ⛔ THE APPLY LEGS ARE NOT YOURS — ENVELOPE LAW
**Site Z is not a TF-apply site.** Author and build here; **the TF/Lambda APPLY legs route through a
laptop lane as MECHANICAL APPLIES of sitez-authored config.** CTO confirms this binds every
sitez-placed item's apply legs by construction — it is not a D8 peculiarity. Terraform remains the
only Lambda deploy mechanism; never `aws lambda update-function-code`, never a bare
`terraform apply`.

## TO-B's FIRST ACT IS THE PORTAL DEV-BUILD PROOF — AND IT IS THE ESTATE'S ONE OPEN ENVELOPE CELL
m365 reach and SharePoint are now MEASURED reachable from site Z (three-probe ALL PASS at
seat-land). **Portal DEV-BUILDS are the ONE genuinely-unmeasured cell left**, and D8 is where it
gets priced. **TO-B's first act is proving a portal dev build runs on this fabric** — report that
result before building the surface. If it fails, that is a REPORTABLE RESULT that re-homes TO-B,
not a thing to work around quietly.

## TO-A scope + the IAM discipline this shape demands
Scope: TF for `opal-portal-content`; route on the selected Lambda; **server-side claim check.**

Phase-1 existence checks: `git log` + `comp-iam service <candidate lambda>`; **confirm no existing
content-store table — run D2 is an ABSENCE CLAIM SCOPED TO A CENSUS, so RE-VERIFY it** rather than
inheriting it; `comp-routes trace` the chosen route path.

Phase-2 IAM, and this is a **NEW DDB table**, the exact case the instrument cannot answer:
**`comp-iam` models `(action)`, never `(action, resource)`** — treat its list as a FLOOR, never a
deletion warrant. Verify on the live primitive with **ONE `--resource-arns` PER CALL** and the
**positive control as a SEPARATE INVOCATION** (2+ resource-arns silently flips held grants to
`implicitDeny` and would disarm the very control you are leaning on). Pass `--context-entries` for
any conditioned statement. **Never use `simulate-principal-policy` to check whether an action NAME
is real** — that oracle is `aws accessanalyzer validate-policy`.

## THE PK IS RULED — STABLE IDENTIFIER, NEVER DISPLAY NAME
CVO's absorbed ruling. A display-name key breaks the moment a pillar or benchmark is renamed, and it
breaks by silently orphaning the override rather than erroring.

## Acceptance criteria
- **D8-1 PORTAL DEV-BUILD PROOF REPORTED** (TO-B first act) — pass or fail, explicitly.
- **D8-2 EXISTENCE CHECKS RE-VERIFIED**, not inherited from the census.
- **D8-3 OVERRIDE WRITTEN VIA A PORTAL-SHAPED PUT RENDERS FOR A DIFFERENT VIEWER SESSION.** A
  same-session render proves caching, not persistence.
- **D8-4 403 EXERCISED** with a non-employee token — the deny path run, not reasoned about.
- **D8-5 EDIT SURFACE BOTH FAMILIES:** employee sees the pencil and saves; **non-employee sees NO
  AFFORDANCE**; the edit is visible to a second session on **BOTH call sites** (Benchmark heatmap
  AND Positioning bars).
- **D8-6 SCREENSHOT PASS** (`/frontend-dev`, colour law) + live DEV exercise.
- **D8-7 IAM VERIFIED ON THE LIVE PRIMITIVE** per the discipline above, positive control shown as a
  separate invocation.
- **D8-8 PK IS A STABLE IDENTIFIER**, asserted.
- **D8-9 proof instances VALID rc=0 positional per row.** MEASURED/RULED-class run rows only;
  INFERRED-class expected values are mechanically ineligible.

<proof_of_spec>
  <expected_criteria>D8-1,D8-2,D8-3,D8-4,D8-5,D8-6,D8-7,D8-8,D8-9</expected_criteria>
  <instance_path>(sitez trunk) deliverables/D8_LIVEEDIT.TO-AB-SITEZ_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## OPEN QUESTIONS AT ANDREW — NONE BLOCK THE BUILD
1. **Editor set (Q1):** all Opal employees (`isInternal`) vs admins only (`isAdmin`). Proposed:
   all-internal per S6's own wording ("editable live by Opal employees"). Decision by TO-A's
   claim-check finalization — which is TO-C's gate anyway.
2. **Model-notes edit scope (Q2):** Key Notes prose only (proposed — figures stay ruled).
3. **PILLAR PRECEDENCE (Q3) — THE CHOICE IS BETWEEN TWO SILENT-FAILURE MODES, NOT BETWEEN A GOOD
   AND A BAD OPTION.** Both directions are stated per CVO P1-1 and must BOTH be carried to Andrew:
   - **store-wins (proposed):** a Yang/Manav edit to the CMA workbook's Philosophy sheet,
     re-uploaded through Data Refresh, **produces NO VISIBLE CHANGE** on any overridden field — the
     JSON regenerates, the portal keeps the override, **no error**, and the person who hits it is
     the named current user of that path.
   - **workbook-wins:** portal edits **silently revert** on the next workbook upload — the editor
     who used the new surface loses their edit without notice.
   **Build to store-wins unless ruled otherwise, and make the losing direction VISIBLE rather than
   silent wherever that is cheap** — a precedence rule whose failure mode is "nothing appears to
   happen" is the most expensive kind to debug from the user's side.

## Do not
- No alert/monitor/notification machinery (standing moratorium).
- No TF/Lambda apply from site Z (envelope law).
- Do not finalize the claim check before TO-C's ruling; scaffold and TF may proceed.

## Reporting
COO via the MSTR ferry: at the dev-build proof (fast — it prices an envelope cell the whole estate
is waiting on), and at each row's acceptance. Session log per seat w/ Compiler Tools section.

---
## ⚖ THREE RULINGS — 2026-08-19 ~20:12Z (Andrew, both terminals; @1e0ec3b079 + @3c8c3f1035)

**1. PILLAR PRECEDENCE (Q3) = STORE-WINS**, and the losing direction is **made VISIBLE wherever it
is cheap.** Build to it; it is no longer a proposal. The reason it went this way is on the record:
store-wins' failure lands on a named current user of that path who can be told, while workbook-wins'
lands on whoever used the new surface, who never learns.

**2. EDITOR SET (Q1) = ALL-INTERNAL** (`isInternal`), per S6's own wording. **This removes the
question TO-C's ruling was going to answer for the claim check** — TO-C still owns claim-SHAPE
sufficiency and remains at CTO's gate, but the editor-set half is settled.

**3. THE SEAT CEILING QUESTION IS ANSWERED — AND THE ANSWER IS *NO*.** Andrew declined to accept 7
sustained. **THIS TO STAYS HELD** until a site-Z seat genuinely frees. **Placement is unchanged
(still sitez); only the timing is held.** No capacity ask goes to him — it is closed, and MSTR has
been told to drop the one it was about to send.

---
## OWNERSHIP BOUNDARY -- RESOLVED 2026-08-19 ~21:16Z (CTO~Z + COO~Z CONCUR IN FULL @550b20ec5b; their trunk @e0de7ff9f4)

Converge complete; **no Andrew one-liner was needed.** Recorded here because it changes WHO RULES on
this package, not merely who executes it.

- **OWNERSHIP INCLUDING GATES for D7 / D9 / D6 / D8: `CTO~Z` RULES + `COO~Z` DECOMPOSES.**
- **Laptop legs are EXECUTION PLACEMENT** -- placement of work, not ownership of it.
- **Laptop CTO narrows to CROSS-FABRIC INTERFACES.** Their prior per-row rulings on this package
  (e.g. D7-U4, D8 TO-C) **stand as HANDOFF-INPUTS at the site-Z gate**, not as the gate itself.
- **ENVELOPE REFINEMENT CONCURRED:** applies stay under **laptop apply-time mechanics**; **item
  acceptance sits at `CTO~Z`.** So the apply leg and the acceptance leg are deliberately split --
  the fabric that can apply is not the fabric that accepts, and that is the intended shape.

**PRACTICAL READ FOR THE SEAT:** route rulings and acceptance to `CTO~Z` / `COO~Z`. Laptop COO
(me) continues to cut and to carry cross-fabric sequencing, and laptop CTO answers interface
questions -- but neither is your gate for this item any more.
