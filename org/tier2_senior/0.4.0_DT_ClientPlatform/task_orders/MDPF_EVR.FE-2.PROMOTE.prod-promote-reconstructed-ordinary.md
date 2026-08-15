# TO MDPF_EVR.FE-2.PROMOTE — portal DEV -> PROD promote of the reconstructed-as-ordinary render (3-commit payload)

<task_order id="MDPF_EVR.FE-2.PROMOTE" project="MDPF_EVR">
<issued_to>0.4.0_DT_ClientPlatform</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-15T21:12Z</issued>
<status>pending</status>
<priority>P2 — Andrew-direct GO, spawn-triggered (MSTR spawned DT for this)</priority>
<authority>Andrew-direct at the MSTR terminal 2026-08-15 ~2100Z, VERBATIM: "yes, do both" — (b) spawn DT for the PROD promote (MSTR 210435Z). Underlying ruling being shipped: Andrew-direct 2026-08-15 "yes they should render as ordinary points" (LD-0417; MDPF_EVR.FE-2 @9f074450a4 validated + closed by COO).</authority>
</task_order>

## The payload — stated as FACT, verified twice (MSTR pre-ask; COO 2110Z own fetch)

`origin/PROD..origin/DEV` is **EXACTLY 3 commits**, in order:
1. `684e67de` feat(OPAL_INVPHL): pillar copy reads served overrides with a per-field repo fallback
   (DT's own follow-on to the Philosophy page already on PROD v2.1.161)
2. `778ea780` feat(MDPF_EVR.FE-2): `reconstructed` = own render-enum member, measured-identical
   pixels, label preserved (Implementation B)
3. `e8b1fb07` feat(MDPF_EVR.FE-2 AC-8): per-firm read prefers a date-aligned `point_class[]` when
   the cohort channel cannot carry classes

Nothing unexpected rides along. Current PROD tag: `portal-v2.1.161` @fbbb9b39. **A promote ships
whatever is on DEV, not just the change that prompted it** — if `origin/PROD..origin/DEV` reads
anything OTHER than these 3 at your Step 0, STOP and report before merging.

## Why the promote is needed — what success LOOKS like on PROD

On PROD today the PER-FIRM views already render the 7 reconstructed inflection points ordinary —
accidentally, via the date-less-cohort fail-safe — and labelled `measured`. It is the **GLOBAL view
that still renders 2 dates as estimate-class** (visually distinct, live), which is exactly what
Andrew ruled against. **The user-visible deliverable of this promote is those 2 Global dates going
ordinary**; everything else is label correctness underneath (per-firm 7 points now LABELLED
`reconstructed`, not relabelled `measured` — no pixel change there by design).

## Procedure — `/prod-deploy`, every step, in order (DT lane; the skill IS the procedure)

Run the `/prod-deploy` skill. Do not re-derive it. Non-negotiables restated because each has bitten
a promote before:
- **The portal MAIN TREE NEVER LEAVES DEV** (Rule 19). The merge-forward runs in an EPHEMERAL
  WORKTREE. Confirm the main tree is back on DEV at the end and end at the workspace root.
- **Step 3 (re-assert local PROD from origin) is mandatory** — kills the dry-run-pollution class.
- **Verify the CI conclusion with `gh run view --json`, NEVER `gh run watch`** (hangs on benign
  warnings). Annotated tags need peeling for verification.
- **Hold DEV pushes during the window** — DEV is not a frozen snapshot; a re-merge window exists.
  Announce the freeze (Step 0) and release it (Step 8).
- **No `MSYS_NO_PATHCONV` on `git push`** — it breaks the VALGATE pre-push gate.
- **`bun install` in the worktree only, foreground.**
- After CI lands: update the workspace submodule pointer on CLOUD (Step 6), tear the worktree down
  (Step 7). **The workspace-side PUSH is MSTR's as integrator** — commit the pointer under your
  author line, tell MSTR.

## Acceptance — a RENDERED read, not a CI-green read

- AC-P1: `origin/PROD..origin/DEV` = exactly the 3 commits above at Step 0 (cite the log).
- AC-P2: CI conclusion `success` via `gh run view --json` (cite run id + conclusion); new
  annotated tag `portal-v2.1.162` (or the CI-minted next) peeled and cited; PROD HEAD = the merge.
- AC-P3: **RENDERED on the deployed PROD instance:** the Model Portfolios GLOBAL view shows the 2
  formerly-estimate-class dates as ordinary points — no band, no dash, no "Interpolated" legend
  entry for them. Evidence = a screenshot of PROD (`/frontend-dev` against the PROD origin, or
  Playwright) with the PNG path cited and READ. **CI green says the bytes shipped; it does not say
  the pixels are right.**
- AC-P4: workspace submodule pointer on CLOUD updated to the PROD merge commit (cite the workspace
  commit); main portal tree confirmed on DEV; worktree removed; freeze released.
- AC-P5: rollback pointer recorded in the merge commit message per the skill's form
  (`Base <sha>. Rollback: <sha>.`) — cite it.

<proof_of_spec>
  <expected_criteria>AC-P1,AC-P2,AC-P3,AC-P4,AC-P5</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/MDPF_EVR.FE-2.PROMOTE_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

Fill the instance from your OWN efforts (schema `org/standards/PROOF_OF_SPEC.schema.json`); validate
BEFORE the `complete` flip with the POSITIONAL id form and CHECK THE RC (a flagged form exits rc=2;
the 2-arg fallback prints VALID with coverage unchecked):
`python .tools/proof-of-spec-check.py org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/MDPF_EVR.FE-2.PROMOTE_PROOF_OF_SPEC.json AC-P1,AC-P2,AC-P3,AC-P4,AC-P5`

## compiler_tools_mandate

BEFORE: `comp-routes behaviors` (CF/serving path sanity for /portfolios — the skill's own pre-step);
`git -C portal rev-list --count origin/PROD..origin/DEV` = 3. DURING: none beyond the skill's
gates. AFTER: the PROD render (AC-P3).

## cross_domain_coordination

`0.0.0_AB_MSTR` — integrator push of the workspace pointer commit; spawned you. `2.0.0_SA_COO` —
issuer; validate + close on your report. `0.4.0_DE_ClientPlatform` — being stood down by MSTR after
their last TO reconciles; not needed for the promote. No other seat touches DEV during the freeze.

## reporting

Report to `2.0.0_SA_COO` (cc `0.0.0_AB_MSTR`) at completion with the proof-of-spec instance + PROD
PNG path, or IMMEDIATELY on: a payload mismatch at Step 0, a CI failure, a rendered read that does
NOT show the 2 Global dates ordinary (that is the abort path — the skill has one). Surprise channel:
one line to COO, no action, keep working.
