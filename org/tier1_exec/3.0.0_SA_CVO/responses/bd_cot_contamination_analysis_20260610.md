# CVO finding — bd / cot pipeline contamination surface + Andrew full-separation directive
**archetype:** DIAGNOSE
**Author:** 3.0.0_SA_CVO
**Date:** 2026-06-10 (Andrew-direct investigation, started 2026-06-09 evening)
**Trigger:** Andrew-direct (CVO session) — "look into these systems and make sure they don't contaminate each other," followed by sovereign decision "completely separate the scripts for bd and cot ... no conceivable connection where contamination could occur" + "tell CTO, roll it into the DTAFLP project."

---

## Bottom line

The two Black-Diamond-derived pipelines are firewalled on **two of three planes** and **wide open on the third**:

| Plane | State | Evidence |
|---|---|---|
| **Serving / routing** (Lambda@Edge) | **PROTECTED** | `infra/aws/lambda-edge/_shared/firm-config.mjs` — frozen SSOT, `cottonwood→opal-data-cot`, `49financial→opal-data-bd`; CI sentinel `shared-advisor-router/test/firm-routing.spec.mjs` catches missed onboarding at deploy gate. |
| **Data** (S3 + IAM) | **PROTECTED (strong)** | `infra/aws/terraform/cot-pipeline/iam.tf:7` "no cot-* role is granted access to opal-data-bd"; cot_gold_layer + cot_exporter roles scoped to `opal-data-cot` only (`:162-163`, `:233-234`); secrets scoped `blackdiamond/cot/*`. Neither firm's runtime can physically write the other's bucket. |
| **Code** (gold script bodies) | **WIDE OPEN — the contamination surface** | cot runs the **same** `data/black_diamond/scripts/gold/*.py` files as 49F, differentiated only by env vars (`D_00.py:77 FIRM_ID = os.environ.get('FIRM_ID','49financial')`; SSM sets `FIRM_ID=cottonwood BD_S3_BUCKET=opal-data-cot`, `cot-pipeline/ssm.tf:237-238`). Every edit to a bd gold script **is** an edit to cot's gold logic. |

**The IAM firewall is the load-bearing protection** — it bounds all contamination to the *code* plane. Worst case is a shared-code edit makes cot serve wrong data **in cot's own bucket**; it can never cross-write 49F's data. That is a genuine, verified strength. But the code plane is real exposure, and Andrew's call to fully separate the scripts is the correct structural fix.

---

## The code-plane contamination vectors (what Andrew's directive severs)

### Vector 1 — Shared script bodies (structural / permanent)
cot and bd execute identical gold files. The intended mitigation (CTO ruling `89e1e4573`) was `FIRM_CAPABILITIES` config — firm-conditional branches, FIRM_ID-gated, NO-OP for non-applicable firms. **It does not exist yet** (grep for `FIRM_CAPABILITIES` across `data/black_diamond/scripts/gold/` = 0 hits). So today the divergent cot behavior is unguarded at the code layer.

### Vector 2 — Mirror-patch state + re-mirror clobber (acute / transitional)
The ~20 cot-specific fixes from the 2026-06-09 AUA re-architecture (B_00 holdings-snapshot branch → $373.2M vs the FIFO $44M undercount; D_02/D_03 skip; Schwab-disconnect graceful; pandas 2.2.3 pin; etc., per `0.6.2_AE_PartnerETL/logs/2026-06-09/work_2235Z.md:21-22`) live **only on the `opal-data-cot/code/gold/` mirror — NOT in git.**
- Nightly cot run is **safe**: SSM syncs gold from `s3://opal-data-cot/code/gold/` (`ssm.tf:254-255`), not from bd.
- But the documented Rule-13 deploy step on any 49F gold change is `aws s3 sync s3://opal-data-bd/code/gold/ → s3://opal-data-cot/code/gold/` (`ssm.tf:198`). Because the cot patches are mirror-only, **that sync silently overwrites them with un-patched bd code — reverting the entire $373.2M re-architecture.** This is a live footgun until the divergence is resolved.

### Vector 3 — "Fix cot by making it like bd" (correctness contamination)
Because the bodies are shared and bd is the mature reference, the natural-but-wrong instinct when debugging cot is to apply bd's positions-FIFO valuation — which re-breaks cot to the $44M undercount. Captured in memory `project_cot_gold_positions_fifo_undercounts_use_allocations_aua`. Only memory protects this today; no code-level invariant.

### Lower-risk / already-separate
- **Bronze + silver:** cot has its OWN bodies (`data/cot/scripts/bronze/cot_bronze_ingest.py`, `silver/cot_silver_merge.py`) — firm-native, not shared. Silver is firm-agnostic by Rule 17 (correct). Risk here is only conceptual cross-application of shared BD-mechanics knowledge, not a shared edit.
- **`lib/` modules:** the bd gold scripts import shared `data/black_diamond/scripts/gold/lib/*` (gold_utils, nna_flows, s3_layout…). **A full fork must copy lib/ into cot's tree too** — else lib bodies remain shared = residual contamination. Flag for the separation scope.

### Process gap
`.tools/safe-deploy.sh` covers **only** `data/black_diamond/scripts/{gold,silver,bronze} → opal-data-bd` (`:28`). cot deploys to `opal-data-cot` are manual `aws s3 cp`/`sync`, **outside the structural deploy gate** — no commit→MATCH→dispatch cycle, no drift detection. This is *why* the undetected mirror-patch state was able to form.

---

## Andrew's sovereign decision (2026-06-10)

> "completely separate the scripts for bd and cot. they should be stored separately in s3, they should not be connected in any conceivable way where contamination could occur, we need clear separation."

This **supersedes CTO ruling `89e1e4573`** (FIRM_CAPABILITIES shared-body config). Implication for in-flight work:

**⚠ The pending DS FIRM_CAPABILITIES fold-in handoff (per `work_2235Z.md:33`) is now counter-productive** — it would fold cot patches *into* the shared bd scripts, deepening exactly the coupling Andrew wants severed. **Recommend HOLD on that handoff** pending CTO re-scope under the separation directive.

### What "complete separation" entails (mechanism-specific, for CTO scoping)
1. **Fork the gold tree:** `data/black_diamond/scripts/gold/*.py` → independent `data/cot/scripts/gold/*.py` (own copies incl. `lib/`); the two diverge freely thereafter.
2. **Sever the S3 mirror:** `opal-data-cot/code/gold/` becomes an **independent deploy target** fed from `data/cot/scripts/gold/` — never `aws s3 sync`'d from `opal-data-bd`. Rewrite the `ssm.tf:194-208` mirror comments + the gold-run sync source accordingly.
3. **First-class cot deploy path:** extend `safe-deploy.sh` (or a cot analog) so `data/cot/scripts/{gold,silver,bronze} → opal-data-cot` is gated with `comp-pipescript deployed` MATCH + drift detection.
4. **Drop the FIRM_ID env-switch indirection for cot gold** once forked — cot scripts are firm-native; no `os.environ.get('FIRM_ID','49financial')` shared-default ambiguity.

### Honest tradeoff to name (CVO doctrine — not just endorse)
Full separation means **cot no longer auto-inherits bd gold bugfixes/improvements.** That is the explicit, correct cost here: the two pipelines are at "very different levels of sophistication" (Andrew), and shared bodies were *forcing* cot to carry bd's assumptions — the FIFO undercount being the exact symptom. Recommend CTO document a deliberate "cherry-pick bd fixes into cot when applicable" policy so divergence is managed, not accidental.

---

## Routing (this finding)

- **CTO (1.0.0_SA_CTO)** — P0: absorb Andrew's full-separation directive into **NFRA_DTAFLP** scope (the project already restructures `data/black_diamond→data/bd` with the right owner set + 0-residual cert; cot-gold-fork is a natural co-scope). Re-scope or retire the `89e1e4573` FIRM_CAPABILITIES ruling. Author the separation into the DTAFLP PRD.
- **COO (2.0.0_SA_COO)** — P0: **HOLD the in-flight DS FIRM_CAPABILITIES fold-in handoff** (now conflicts with separation). Sequence: until separation lands, treat any 49F gold re-mirror to cot as **unsafe** (would clobber the cot mirror patches).
- **DS (0.4.0) / AE (0.6.2, 0.7.0)** — execution owners of the fork under NFRA_DTAFLP once CTO re-scopes; no action until the re-scoped TOs issue.

## Verifier-not-fixer note
CVO surfaced the contamination model + routed Andrew's decision; CVO does not author the PRD/TOs or fork the scripts. Independent verification of the eventual separation (0-residual: no cot runtime path resolves to bd code/data) is a CVO close-gate when NFRA_DTAFLP ships.

— 3.0.0_SA_CVO
