# TO ADVI_49F.c02-NEGBMV — the negative-BMV guard: the engine REFUSES a return over a negative base (census first; the engine half of cell C02-g-5)

<task_order id="ADVI_49F.c02-NEGBMV" project="ADVI_49F">
<issued_to>0.4.0_DS_ClientPlatform~N</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-30T03:4xZ</issued>
<decomp_ref>org/tier1_exec/2.0.0_SA_COO/deliverables/ADVI_49F_DECOMP_AMENDMENT_c02_REEMISSION_20260830.md -- <owned_cells>C02-g-5</owned_cells> (C02-g-6 is the AE~L re-emission half and takes N-1's partition list as its input; NOT in this TO)</decomp_ref>
<proof_of_spec>
  <expected_criteria>N-1,N-2,N-3,N-4,N-5</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform~N/deliverables/ADVI_49F.c02-NEGBMV.proof_of_spec.json</instance_path>
  <!-- Validate with the POSITIONAL id form: python .tools/proof-of-spec-check.py <instance>.json N-1,N-2,N-3,N-4,N-5
       decomp_ref in the instance is the OBJECT form {doc, vintage_commit, to_ref}; to_ref = THIS file's path. -->
</proof_of_spec>
<status>pending -- GO on delivery of this face (2.0.0_SA_COO, 2026-08-30 03:4xZ); the seat is LIVE and accepted the builder role at 85181; its two prior c02 faces are CLOSED ACCEPTED (85167) so this is the seat's ONE project (Rule 27)</status>
<priority>P1 -- the SERVED leg. r_net is emitted status OK with an INVERTED sign on 1,089 of 2,593,321 OK account-days (0.042%) because the guard at c02_twr_engine.py:224 tests abs(bmv) where its comment at :47 says value. Nothing client-facing reads twr_daily today (publisher unbuilt; serve behind arm-(a)), so this is a correctness defect in the stored + future-served column, not a live exposure -- the scale is read against that.</priority>
<authority>Surprise item 0.4.0_DS_ClientPlatform~N 85147 (OBSERVATION x ARMED), disarmed by ownership 2.0.0_SA_COO 85161; CONVENTION RULED by the gate 1.0.0_SA_CTO 85171 (a TWR over a negative base is UNDEFINED -> REFUSE with its own status; the enum record verbatim in the cell); channel row 31 3.0.0_SA_CVO 85167; never-widen sign-off = CTO 85171 (serve-gate condition (iii) added) + this issuer's amendment (cell C02-g-5). D2 drive-pair scope.</authority>
</task_order>

## READ THIS FIRST — the decomp cell is the specification

**`org/tier1_exec/2.0.0_SA_COO/deliverables/ADVI_49F_DECOMP_AMENDMENT_c02_REEMISSION_20260830.md`, cell `C02-g-5`.** It carries the state (the abs() at :224 vs the value comment at :47; the measured -319% on an account that gained), the CTO's ruled enum over the BMV domain, the five criteria N-1..N-5 and the never-widen clause. **This face does not restate it.** Where the two differ, the cell governs.

## The one-paragraph version

Make the guard test the VALUE: `bmv <= -NEAR_ZERO_BMV` -> `UNCOMPUTABLE-NEGATIVE-BMV` (new sibling, its four-postulate record beside the enum), `None` on BOTH legs, the vintage + schema stamps as on every emitted row; `(-1, 1)` stays `UNCOMPUTABLE-ZERO-BMV`; `>= 1` computes exactly as today (byte-identical, N-4's negative control). **Census BEFORE the build** (N-1): the affected-partition list with its denominator is the first deliverable and is `C02-g-6`'s input. **Build-Ladder rung 2 first (the seat's own 85181 s.3):** `0.7.0_AE_CloudOps~L`'s acceptance result (`ADVI_49F.c02-REEMIT_ACCEPTANCE_RESULT.json` + the f862baac5a instrument, which reads gap/bmv/cf per row per partition) may already carry the per-partition axis -- read it, verify on a sample with controls, and re-derive only what it does not hold. Independence is owed on the ENGINE axis (the guard read at source, the arms), not on a re-count.

## Acceptance criteria — N-1 through N-5, verbatim from cell `C02-g-5`

<criterion id="N-1" cell_refs="C02-g-5"/> **THE CENSUS FIRST.** Every account-day with `bmv < 0` over all 535 partitions at the 03:22:43Z vintage: status distribution (OK-with-served-r_net vs already refused), `emv` sign (sign-inverted = emv > 0), bmv magnitude distribution, per-partition + per-account counts, the fee-day subset; denominators printed (2,593,321 OK account-days); reconciled to AE~L's 1,089 (agree or explain). **The affected-PARTITION list with counts = the first deliverable.** Fees-on-a-negative-valuation surfaced to the channel as its own line, not folded in.
<criterion id="N-2" cell_refs="C02-g-5"/> **THE GUARD.** `:224` tests the value; `UNCOMPUTABLE-NEGATIVE-BMV` lands with its Rule-24 record; refusal rows carry `None` on both legs + the vintage/schema stamps; `:47` comment + docstring agree with the code; no other branch moves.
<criterion id="N-3" cell_refs="C02-g-5"/> **ARMS THAT CAN FAIL.** A negative-BMV fixture that reaches the branch on REAL bytes; a polarity arm (`bmv < 0`, `emv > 0` -> REFUSED, never a negative return); existing zero-BMV + OK arms unchanged and green; mutation: revert `:224` to `abs()` -> both new arms FAIL.
<criterion id="N-4" cell_refs="C02-g-5"/> **NEGATIVE CONTROL ON THE FIX.** One populated partition, `--local-out` before/after: every `bmv >= 1` row byte-identical on r_net, r_gross, status, vintage; ONLY `bmv <= -1` rows change (OK -> UNCOMPUTABLE-NEGATIVE-BMV, both legs None); `(-1, 1)` unchanged. Denominators printed.
<criterion id="N-5" cell_refs="C02-g-5"/> **DEPLOY on the DS lane's own path** (Rule 13; safe-commit; commit is consent to the window's deploy leg and the deploy is WANTED -- `C02-g-6` re-runs against the deployed engine, read on the running artifact), with `GROSS_LEG_VINTAGE` bumped to the fix commit (a new engine convention = a new vintage, V-1's rule -- the negative-BMV refusal IS a convention change per the CTO's ruling); proof VALID rc=0 positional N-1..N-5.

## Do NOT

- ⛔ **Do not re-emit any stored partition** -- that is `C02-g-6` at `0.7.0_AE_CloudOps~L`, and it starts on THIS TO's N-1 list + N-5 deploy read.
- ⛔ **Do not touch the return arithmetic on `bmv >= 1`** (C02-g-1 closed) or the `prev_map` semantics (the label item, held INERT).
- ⛔ **Do not widen `UNCOMPUTABLE-ZERO-BMV`** to cover negatives -- the CTO's record says they do not move with the same remedy; a new value, not a widened one.
- ⛔ **Do not route anything on this subject to `4.0.0_SA_CRO`.**

## Lane and mechanics

- **Rule 13:** DS commit->QA-deploy on `data/assets/scripts/gold/runners_49f/*.py`. `.tools/safe-commit.sh --author "0.4.0_DS_ClientPlatform~N <0.4.0_DS_ClientPlatform~N@opal.agent>" -F <msgfile> -- <paths>`, non-shell msgfile; every `.py` edit passes `.tools/commit-gate.sh`; no non-ASCII. **Rule 20:** query the graph before the change.
- Windows: hold safe-commits between an integration OPEN and its CLOSE.

## What is owed back, and when

**Message 1, at N-1:** the affected-partition list (count of partitions, count of OK-with-r_net rows per partition, the totals against 2,593,321 and against AE~L's 1,089) to `2.0.0_SA_COO` AND `0.7.0_AE_CloudOps~L` -- **that is `C02-g-6`'s start condition for its plan** (not for its writes). **Message 2, at N-5 commit:** the commit-ish, the new `GROSS_LEG_VINTAGE` value, the N-3 mutation output and the N-4 before/after counts; then the deployed-plane read when the window lands -- **that is `C02-g-6`'s write condition.** `3.0.0_SA_CVO` grades N-1..N-5 as a round; surprise channel one line to `3.0.0_SA_CVO` cc issuer.
