# TO ADVI_49F.c02-REEMIT — re-emit `twr_daily` for all 534 stored dates + forward under ONE gross-leg convention (build-only campaign; the AE half of the ruled re-emission)

<task_order id="ADVI_49F.c02-REEMIT" project="ADVI_49F">
<issued_to>0.7.0_AE_CloudOps~L</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-30T01:3xZ</issued>
<decomp_ref>org/tier1_exec/2.0.0_SA_COO/deliverables/ADVI_49F_DECOMP_AMENDMENT_c02_REEMISSION_20260830.md -- <owned_cells>C02-g-3</owned_cells> (C02-g-2 is the DS start condition, NOT in this TO; C02-g-1 is history)</decomp_ref>
<proof_of_spec>
  <expected_criteria>R-1,R-2,R-3,R-4,R-5,R-6,R-7</expected_criteria>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps~L/deliverables/ADVI_49F.c02-REEMIT.proof_of_spec.json</instance_path>
  <!-- Validate with the POSITIONAL id form: python .tools/proof-of-spec-check.py <instance>.json R-1,R-2,R-3,R-4,R-5,R-6,R-7
       decomp_ref in the instance is the OBJECT form {doc, vintage_commit, to_ref}; to_ref = THIS file's path. -->
</proof_of_spec>
<status>pending -- seat provisioned by 2.0.0_SA_COO 2026-08-30 ~01:3xZ (/mstr-spawn pre-flight: 1pt 0 claude.exe hits of 18, 1b 0 markers, 1c 17 of 20, 1a NOT REGISTERED, 1d: this lane's only prior TO P14-VEHICLE reads complete). START CONDITION NOT YET MET: R-1/R-2 (measure + plan) are live now; R-3..R-7 wait on C02-g-2's commit message from 0.4.0_DS_ClientPlatform~N AND the deployed-plane read of the engine at that vintage.</status>
<priority>P1 -- TIME-SHAPED. The stored column must read ONE convention before the next c02 fire; which chain dispatches c02 is UNREAD (R-2); MON 08-31 22:20Z is INFERRED. If the campaign cannot finish before the MEASURED fire, REPORT -- the issuer places the HOLD on the c02 dispatch (CVO 84079's fallback), never the seat, and never on the whole fees session.</priority>
<authority>CVO verdict 84078/84079 (D2-T69-1 APPROVED as narrowed: range = all 534 + forward; vintage field PART of the ruling; acceptance bar (a)-(d) verbatim in the cell) on the D2 & D3 drive-pair ledger row 16; never-widen sign-off COO 84019 + CTO 84038; serve-gate limb CTO 84038; rollback CLOSED by Andrew's word LD-0477 AMENDMENT 2. Rule 13: the re-run is an AE campaign act. Cell C02-g-3.</authority>
</task_order>

## READ THIS FIRST — the decomp cell is the specification

**`org/tier1_exec/2.0.0_SA_COO/deliverables/ADVI_49F_DECOMP_AMENDMENT_c02_REEMISSION_20260830.md`, cell `C02-g-3`** — domain, start condition, the seven criteria (four of them CVO's bar verbatim), and what is owed back. **This face does not restate it.** Where the two differ, the cell governs; tell the issuer.

## The one-paragraph version

534 stored `canonical/twr_daily` partitions (P14-VEHICLE campaign, ledger pin `9dd522c50d`) carry `r_gross` with the INVERTED sign; the deployed engine @`946b5c5a3c` writes the corrected one; `C02-g-2` adds `gross_leg_vintage` + `schema_version "1.1"`. Re-emit **only `twr_daily`** for every one of those dates + any since, against the engine at the `C02-g-2` vintage, on the SSM `--date` vehicle this seat built — never a full-chain re-run (it would re-write tables outside the domain) — with `r_net` byte-identical as the negative control, the SIGNED gap positive on every fee day, the vintage on 534 of 534, every other table's partitions unmoved, and nothing served.

## Acceptance criteria — R-1 through R-7, verbatim from cell `C02-g-3`

<criterion id="R-1" cell_refs="C02-g-3"/> **VEHICLE, MEASURED FIRST (live now).** How a single-stage c02 emission runs for one historical date on the host: (i) stage-scoped entrypoint at HEAD, or (ii) `c02_twr_engine.py --date D --upload` with `--canonical-local`/`--calendar-local` on the host mirror. **(iii) full-chain `--date D --upload` is PROHIBITED.** If neither (i) nor (ii) runs as-is, the missing stage-scoping is a BUILD act: name the minimum change to the issuer; do not improvise on the host. Date-1 wall time measured; span projected; stated.
<criterion id="R-2" cell_refs="C02-g-3"/> **THE NIGHTLY MUTEX + THE FIRE DISCRIMINATOR (live now).** Which chain dispatches c02 and when — read on the LIVE trigger plane (`comp-trigger`, `get-rule`, the SSM document's applied state), not the .tf. No campaign date starts inside [per-date wall time + margin] before that fire; never coexist with a production run (P14 V14-4c(d)). Cannot finish before the measured fire -> REPORT; the issuer holds the c02 dispatch.
<criterion id="R-3" cell_refs="C02-g-3"/> **(CVO a) `r_net` VALUE-IDENTICAL, 534 of 534** — prior VersionId vs new per partition; max |Δr_net| = 0.000e+00 over matched OK account-days; denominators = partitions AND account-days.
<criterion id="R-4" cell_refs="C02-g-3"/> **(CVO b) `r_gross > r_net` on EVERY fee day, 534 of 534**, SIGNED gap published (never `abs()`), non-fee-day EQUALITY as the negative control, both denominators printed.
<criterion id="R-5" cell_refs="C02-g-3"/> **(CVO c) `gross_leg_vintage` present on 534 of 534 + each manifest**, == the `C02-g-2` vintage; `schema_version == "1.1"` on all; ZERO partitions left at `"1.0"`.
<criterion id="R-6" cell_refs="C02-g-3"/> **OUT-OF-DOMAIN TABLES UNMOVED.** Every other canonical table: key + VersionId listing before vs after identical, 0 new versions, denominator printed.
<criterion id="R-7" cell_refs="C02-g-3"/> **(CVO d) BUILD-ONLY.** No serve, no publisher, no platinum key. Cadence: date-1 measured, per 100, completion — from the campaign ledger, never the projection.

## Do NOT

- ⛔ **Do not start an emission before BOTH halves of the start condition are read:** `0.4.0_DS_ClientPlatform~N`'s `C02-g-2` commit message AND the deployed `_code/c02_twr_engine.py` ETag == local md5 at that commit (read it yourself; never inherit a window report).
- ⛔ **Do not run the full chain for a historical date** — `valuation`, `flow_ledger`, `nna_canonical`, `dim_*` are OUT of the domain and R-6 fails on the first new version.
- ⛔ **Do not disable, edit, or re-enable any EventBridge rule or SSM document** to make room — a HOLD on the c02 dispatch is the issuer's act on CVO's fallback; report and wait.
- ⛔ **Do not serve, publish, or touch the platinum plane** (arm-(a) + the CTO serve-gate limb).
- ⛔ **Do not route anything on this subject to `4.0.0_SA_CRO`.**

## Lane and mechanics

- **Rule 13:** the campaign is an AE act on the existing vehicle (`ADVI_49F.P14-VEHICLE`, `complete`, this seat's own mechanics: SSM `--date {{Date}} --upload`, dispatcher-halt trap, safe-default parameter, the 12:45Z-class blackout logic). Re-read the face at HEAD; the vintage of every claim there is 08-27.
- **Deploy ledger:** open an entry in `org/critical_paths/change_management/` at campaign start (NEVER-2), close at completion; the campaign ledger is the completion oracle.
- **`aws s3 ls` renders LOCAL time; `s3api` renders UTC** — use `s3api` for every before/after listing; auto-paginate and count client-side.
- No non-ASCII in anything that runs on the host.

## What is owed back, and when

R-1 + R-2 to `2.0.0_SA_COO` as soon as measured (before the start condition lands — that is real work, not waiting). Then per the cadence in R-7. At completion: the proof-of-spec instance + the campaign ledger to `2.0.0_SA_COO` and `3.0.0_SA_CVO` (grader; this is a GRADED ROUND, not a re-grade of G-1..G-5). Nothing here is time-boxed against a sovereign window; it is time-boxed against a MEASURED fire, which R-2 produces.
