# TO OPAL_MDPFCLEANUP.TO-2 — RE-HOME THE COT DIM (unblocks every K3 kill) ⛔ STAGED

<task_order id="OPAL_MDPFCLEANUP.TO-2" project="OPAL_MDPFCLEANUP">
<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-14T17:2xZ</issued>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project OPAL_MDPFCLEANUP, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: staged — gate: TO-1 ratification (Andrew may dispute rows); lane allocation may add a DS hand (MSTR handshake, CTO 172234Z note); CTO holds the arch gate + apply GOs</status>
<priority>Strict sequence position 3 (PRD §4); gates all K3 kills</priority>
</task_order>

**PRD:** `docs/architecture/OPAL_MDPFCLEANUP_PRD.md` v1.1 @9f75dcb996 §4 TO-2 + §1 conditional row, verbatim.

## Objective

Port `build_dim_model_portfolio` into the canonical scheduled path. **It already ships inside
mdpf-gold-lambda's package — the build ladder says WIRE THE EXISTING MODULE, build nothing new.**
Correctly-first-time + direct port; **NO shadow/parallel emission, no standing comparator**
(Andrew's complete veto, standing). The `mdpf-daily-*` EC2 chain (§1: the ONLY producer of
`blackdiamond/cottonwood/gold/dim_model_portfolio`, source-pinned in TRGALN proof_TO-0) stays KEEP
until this TO's acceptance.

## Acceptance

The dim builds on the canonical schedule, **exercised on one full cycle** (dim written by the
canonical path, values tie against the prior producer's last artifact — run-and-read, nothing
standing) BEFORE any K3 kill. Rule 13 lane split honored if gold-script edits arise (DS owns
data/*/scripts/gold content; AE owns infra/TF/trigger wiring). Deploy per law: commit → TF → plan
→ apply → 0-diff → tag.

<proof_of_spec>
<expected_criteria>dim-wired-into-canonical-scheduled-path-no-new-build; no-shadow-no-comparator; full-cycle-exercised-dim-written-by-canonical-path; values-tie-against-prior-producer-run-and-read; zero-diff-apply-tagged</expected_criteria>
<instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/OPAL_MDPFCLEANUP/proof_TO-2.json</instance_path>
</proof_of_spec>
