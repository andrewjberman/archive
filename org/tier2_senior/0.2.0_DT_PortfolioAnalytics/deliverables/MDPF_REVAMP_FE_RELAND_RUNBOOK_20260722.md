# MDPF_REVAMP FE re-land — DT runbook + hard-gate battery

**Owner:** `0.2.0_DT_PortfolioAnalytics` (executes the promote) · **Gate owner:** `1.0.0_SA_CTO` (issues the go)
**Status:** OPEN — held. Created 2026-07-22 ~0420Z after the P0 rollback.
**Why this file exists:** the gate sequence below was assembled across ~10 MCP messages during a live P0.
A session ends; this does not. A successor DT should reinstantiate with the gate list rather than
re-derive it, and item 5's follow-up must still be visible after the P0 heat dies down.

## Situation

The MDPF FE (`aa8c0420`) is stranded on portal `DEV`. The forward flip was **rolled back** by CTO after a
P0: live Global's `opal_aggregate_aua` != `model_aua + non_model_aua`. The re-land is **FE-FIRST**, after
the data is corrected and a **FRESH** never-widen co-sign is issued.

- portal main tree stays on **DEV**, always (CLAUDE.md Rule 19).
- `origin/DEV` = `aa8c0420` · `origin/PROD` = `99fed48f` · **DEV is 4 commits ahead.**
- The re-land is a **4-commit forward merge**, not one: `aa8c0420`, `1508d183`, `5b1e44dc`, `2f603319`.
  "Promote @aa8c0420" reads like a single commit and is not — do not let that phrasing shrink the diff
  in anyone's head.

> **⛔ THE 0159Z ANDREW CO-SIGN IS VOID FOR THIS RE-LAND.** It pinned the ORIGINAL (buggy) coherent-9
> ETags. The fix changes the data → new ETags → new pin → **a FRESH co-sign is required.** A "go" citing
> 0159Z is **NOT A GO**; route it back rather than acting on it. This is the single most likely way a
> wrong promote happens, which is why it is at the top.

## LANE ACTIVE — FE-FIRST sequence (COO 055650Z; data-gate PASSED, COO-verified)

The data-gate is **PASSED** — COO independently re-ran CVO's Layer-3 live against the new coherent-9
(`c27e1f37` set): PASS, B-basis consistent, 421/421 mutant-proven. The re-land is **FE-FIRST**, the
deliberate inverse of the flip that half-landed:

```
1. DE   folds 2x + content-A/B into the revamp FE  ->  DEV surface-check GREEN   (DE's leg, CTO-tasked)
2. DT   promotes FE-FIRST (/prod-deploy, ephemeral worktree, main tree stays DEV) -> opalinvest.dev
3. AE   re-populates the publisher (9 keys from the c27e1f37 fixed data) + re-applies routing
```
**FE leads, data follows.**

> ### ⚠ THE WINDOW BETWEEN STEP 2 AND STEP 3 IS REAL
> Between my push and AE's re-populate, **the new FE is live against the OLD published data.** If the
> revamp FE reads a key or shape the currently-published set does not carry, opalinvest.dev renders
> wrong or empty for the duration — and it is Andrew-visible.
> This is **not** an argument against FE-first (half-landed proved the other order is worse). It is an
> argument for answering *"what does the new FE do against the old data?"* **before** the push, not
> after. **That answer is DE's to give.** Degrades clean (empty states, no crash) -> the window is
> cosmetic. Hard-fails or shows misleading numbers -> compress the gap deliberately, AE staged to fire
> immediately behind me. Raised to COO + DE 0557Z so it costs a question rather than an incident.

## Hard-gate battery — ALL SIX before `/prod-deploy`

| # | Gate | Owner | How it is satisfied (evidence, not assertion) |
|---|---|---|---|
| 1 | Global `opal_aggregate_aua` **composition** fix landed + re-staged | DS | new staged ETags; **not** the firm-sum — that was always correct (CROSSFIRM_PASS both sides) |
| 2 | **Consistency gate rc=0** on the corrected set | DT | `mdpf_parity_check.py --consistency --published-prefix <stage>` → rc=0. Plus re-run the date-joined **parity** leg on the new ETags. Both legs (COO scope). |
| 3 | 3 inflection `PARTIAL_NULL` dates dispositioned | DS (+CVO) | 2026-05-21 / 06-01 / 07-01: `partner_custody_total` populated, BOTH components None. Honest → a NAMED exemption I add **and CVO rules whether that exemption can hide a real defect**; else fixed. **Do not soften the gate to reach green.** |
| 4 | Re-land DEV commit carries `SURFACE_ACK: <reason>` | DE/DS (FE author) | CTO ruling 041852Z (a). The SEV1 touch is *justified* (the revamp IS model-portfolios work) but **justification != ack**. The `^`-anchor is load-bearing: the token must **START** the line. |
| 5 | **Surface-Check Gate GREEN on the EXACT promoted sha** | DT verifies, CTO confirms | Interim manual control for the PROD-path gap (below). Quote run id + head sha + conclusion. Not "a green run on DEV" — *the sha*. |
| 6 | **FRESH** never-widen co-sign (CTO+COO+Andrew) + Andrew re-eyeball + CTO go | CTO/COO/Andrew | pinned to the **corrected** ETags — **the NEW `c27e1f37` set** |

### Gate status as of 2026-07-22 ~0558Z

| # | Status |
|---|---|
| 1 | **DONE** — composition fix landed; `opal_aggregate_aua` == model + non_model exactly |
| 2 | **DONE** — DT consistency `rc=0` all 3 firms + `CROSSFIRM_PASS` regime B, ETag-pinned; parity all aggregates `NAMED_DELTA_PASS`, 0 unexplainable windows, fitted-signature 0/8 |
| 3 | **DONE** — 6 dates declared honest-None via `meta.honest_none`, CVO lineage-verified truthful; DT marker consumer @`41cbd7220` (11 mutants, CTO's seeded case RED) |
| 4 | **PENDING DE** — the revamp FE commit must carry a `^`-anchored `SURFACE_ACK:` line |
| 5 | **PENDING DE** — DEV surface-check GREEN **on that exact sha**; DT verifies + quotes run id/headSha/conclusion, CTO confirms |
| 6 | **PENDING** — COO co-sign **STAGED, NOT ISSUED**; Andrew's sovereign limb follows. **STAGED != ISSUED — hold.** |

**COO's data-gate verification (055650Z): PASSED**, independently re-ran CVO's Layer-3 live on the
`c27e1f37` set. The remaining gates are all FE-side + the co-sign, not data.

### The frozen 9 (every leg must cite THIS set — cross-vintage expiry control, CTO-adopted)
```
49f agg    aa5c5b85066109c9bdb557e51b0d8ffd    inf agg    cec5a0d6fe749aae77735f9297edbb71
global agg c27e1f370f9c08de6489cb11bf885e13    A4         8a195549c6f80257f188d91a6423d547
A2         f2c034760b44c4bd7338be0fd6c75c58    A1         529b7c211b268f6cb72fa4a92941727d
dist 49f   865919f2be40c6c44a58fdb15dbefe23    dist inf   afb964c4d67f2a3e3682c50269dc69e8
dist glb   b946d8364ca35dc258d90919d68fb771
```
**A multi-leg gate assembled across a moving vintage risks "four greens each true of a different
object."** This stage moved three times on 2026-07-22. Before gating, HeadObject all 9 and confirm every
leg cites the same live set; any leg citing a superseded set re-runs first.

> **LEDGER: open a NEW one at deploy-start. Do NOT re-close the old exact-9 ledger** — AE already closed
> it as *rolled-back* @040519Z (COO 060024Z). Re-closing someone else's closed ledger would overwrite a
> rollback record with a deploy record, which is worse than leaving it alone.

> **CO-SIGN: `STAGED` IS NOT `ISSUED`.** COO's limb is staged and will fire with CTO's and Andrew's,
> pinned to `c27e1f37`. COO will say plainly and unambiguously when the fresh co-sign has FIRED. Until
> that sentence exists, **there is no go** — and a go citing the 0159Z co-sign is not a go either.

Then: `/prod-deploy` — 4-commit `DEV→PROD` forward merge in an **ephemeral worktree**, `bun install` in it
first (else the pre-push `tsc` gate fails "tsc: command not found"), main tree never leaves DEV, verify CI
conclusion via `gh run view --json`, update the workspace submodule pointer on CLOUD, tear down the
worktree, confirm `portal/` back on DEV, end at the workspace root.

## ⚠ OPEN FOLLOW-UP — the PROD-path surface gate gap (do not let this drift)

**Measured 2026-07-22** (`portal/.github/workflows/`, read at DEV `aa8c0420`):

```
surface-check.yml    on: push -> branches: [DEV]      <- the SEV1 gate. DEV ONLY.
ci.yml               on: push -> branches: [DEV]
deploy.yml           on: push -> branches: [PROD]     <- zero "surface" references
promote-to-prod.yml  workflow_dispatch only           <- zero "surface" references
```

**DEV is gated; PROD is not.** That is backwards for a client-facing surface: a promote pushes to PROD,
which does **not** re-check, so an un-acked SEV1 change can reach production past a gate that already
returned `BLOCKED` on a branch nobody re-reads. **That is a red gate being laundered by a branch change,
not a gate being satisfied.**

- **Interim control (this re-land only):** gate #5 above — manual, two-person. **CTO ruling 041852Z (b).**
- **Durable fix:** add the surface gate (or an ack-verification step) to `promote-to-prod.yml` /
  `deploy.yml`. **Route as a TO to the portal-CI owner POST-re-land** (CTO's sequencing).
- **Honest limit, stated so "interim" does not quietly become "resolved":** gate #5 depends on a human
  remembering to run it. That is the weakest kind of control — it is exactly the class this whole
  incident is about. The CI fix is the real one.

Live evidence of the gate firing (so a future reader knows it is real, not theoretical):
run `29888356628`, head `aa8c0420`, **FAILURE exit 2** —
`CRITICAL: change touches model_portfolios.benchmark (SEV1)` and `model_portfolios.headline (SEV1)`
`[firms: bd/inf/cot] via portal/src/pages/ModelPortfolios.tsx` → `BLOCKED (SEV1, block-with-ack)`.
`CI - Build & Validate` was **GREEN** on the same sha — which is why this stayed invisible: the green one
is the one people look at.

## Standing facts worth not re-deriving

- **PARITY IS NOT CONSISTENCY.** The 3/3 gate (CTO S3 re-verify + CVO re-derive + DT date-joined parity)
  was honestly CLEAN while the data was internally wrong, because all three compare served-vs-published
  and the defect was present on **both** sides. Three independent methods, one shared axis, one blind
  spot. The consistency gate (`--consistency`) is the axis that was missing; CTO adopted it as the
  standing pre-serve gate (041443Z / 040932Z).
- **The rollback did NOT fix the data.** Served (legacy live) global fails **429/429** dates with the
  same hole, back to **2024-11-01**. The revamp *revealed* it; it did not introduce it. Rollback cleared
  the visible defect + the half-landed state only. (CTO corrected his Andrew brief on this.)
- **The hole moves:** $64,478,099.34 (frontier 2026-07-20) → $203,203,649.06 (max), median
  $163,093,838.09 across 421 staged dates. The circulating "~$153M" is early history (~2024-11 to
  mid-2025), not the frontier. **Quote a number with the date it is OF.**
- **The revamp fixes a legacy defect:** served 49financial fails 2025-12-26 (−$43,157,544.80); staged 49f
  is clean 427/427.
- **Gate design note for anyone extending it:** the total field resolves **by presence** —
  `opal_aggregate_aua` is **global-only**; partners carry `partner_custody_total`. A gate hard-coded to
  the obvious field name no-ops on 2 of 3 firms **and reports a clean sweep**. If a fix renames or adds a
  total field, extend `TOTAL_FIELD_CANDIDATES` rather than let it read `TOTAL_FIELD_ABSENT` (which fails
  deliberately — **uncheckable is not a pass**).

## Instruments

- `deliverables/mdpf_parity_check.py` @`3e557741e` (CLOUD) — self-test PASS, 13 mutant clauses,
  measured sensitivity floor **$1.01** printed by the test. `--consistency [--published-prefix ...]
  [--served]`, rc=1 on any violation. `--all` now also returns 1 on a consistency failure (CTO: keep it).
- CVO's independent Layer-3 gate @`f3c202256` — same axis, separately built. Two independent gates on the
  axis we were all blind on.

## Provenance

CTO rulings 040932Z (gate adopted, 5 corrections accepted) + 041852Z (surface-check: do not launder;
ack required; PROD-path gap real; Rule 20 correction is CTO's). COO 034403Z (corrected mission), 034839Z
(gate routed), 041443Z (corrections independently confirmed). MSTR 034450Z (spawn-hint correction).
CVO 040643Z (adversarial refutation in flight).

**CLAUDE.md Rule 20 is STALE for the portal DEV-push path** — LD-0273 Stage-1 HALF-2 landed and
`surface-check.yml` IS a non-bypassable DEV gate. Still true for workspace `safe-commit` and the PROD
path. **CTO owns that law edit** (confirmed his, deliberate, not mid-P0). Do not edit CLAUDE.md for it.
