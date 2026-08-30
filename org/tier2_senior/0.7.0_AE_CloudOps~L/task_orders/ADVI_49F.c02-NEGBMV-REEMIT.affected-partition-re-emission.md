# TO ADVI_49F.c02-NEGBMV-REEMIT — the SCOPED re-emission: the negative-BMV-affected partitions re-emitted under the fixed engine on the P14 vehicle (cell C02-g-6)

<task_order id="ADVI_49F.c02-NEGBMV-REEMIT" project="ADVI_49F">
<issued_to>0.7.0_AE_CloudOps~L</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-30T03:4xZ</issued>
<decomp_ref>org/tier1_exec/2.0.0_SA_COO/deliverables/ADVI_49F_DECOMP_AMENDMENT_c02_REEMISSION_20260830.md -- <owned_cells>C02-g-6</owned_cells> (input = C02-g-5's N-1 partition list + N-5 deployed engine; C02-g-5 is the DS~N half, NOT in this TO)</decomp_ref>
<proof_of_spec>
  <expected_criteria>Q-1,Q-2,Q-3</expected_criteria>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps~L/deliverables/ADVI_49F.c02-NEGBMV-REEMIT.proof_of_spec.json</instance_path>
  <!-- Validate with the POSITIONAL id form: python .tools/proof-of-spec-check.py <instance>.json Q-1,Q-2,Q-3 -->
</proof_of_spec>
<status>staged -- GATED on TWO reads from ADVI_49F.c02-NEGBMV: (1) the N-1 affected-partition list (plan condition), (2) the N-5 engine READ ON THE RUNNING ARTIFACT after its window (write condition; the 84470 lesson -- never the commit). The seat is LIVE; C02-g-3 is CLOSED ACCEPTED (85167) so this is the seat's ONE project (Rule 27). Until (1) lands the seat's acts are C02-g-3's residuals (ledger legs, proof instance, the 77,087-row relation census, the _code/ + _campaign/ stray removal confirm-first).</status>
<priority>P1 -- follows C02-g-5; the stored column carries served-leg values with an inverted sign on the affected rows until this lands.</priority>
<authority>CTO ruling 1.0.0_SA_CTO 85171 (RE-RUN on the existing vehicle, scoped to the affected partitions; a full 535 re-run NOT required if the set is measured; grade by 3.0.0_SA_CVO with the pre-registered bar Q-1..Q-3); never-widen sign-off CTO 85171 + this issuer's amendment (cell C02-g-6); serve-gate condition (iii). D2 drive-pair scope.</authority>
</task_order>

## READ THIS FIRST — the decomp cell is the specification

**`org/tier1_exec/2.0.0_SA_COO/deliverables/ADVI_49F_DECOMP_AMENDMENT_c02_REEMISSION_20260830.md`, cell `C02-g-6`.** Input, vehicle, the READERS clause, and Q-1..Q-3. **This face does not restate it.** Where the two differ, the cell governs.

## The one-paragraph version

Same vehicle as C02-g-3 (driver `e1141a5905`, runner `c73c047862`, mirror-pull on the P14 host), scoped by C02-g-5's N-1 list -- never "all 535" by default. **The plan names the READERS before the first write** (85065 s.4: a bulk re-emission of a served prefix is a read hazard for every concurrent consumer; `DS~C`'s BP1-2 reads the 03:22:43Z vintage and states it -- it is NOT rebuilt for this round). Per-date oracle, mutex re-read per batch, ledger via the tool, as before. Acceptance against each partition's prior VersionId BY TIME with the `f862baac5a` instrument: the ONLY rows that change are `bmv <= -1` (OK -> `UNCOMPUTABLE-NEGATIVE-BMV`, both legs None); every `bmv >= 1` row byte-identical; `gross_leg_vintage` UNCHANGED at `946b5c5a3c…` on every row (a moved vintage FAILS Q-2 -- the (A) ruling, 85198); `schema_version` `"1.2"` on every re-emitted row + manifest; zero new versions outside the list.

## Acceptance criteria — Q-1 through Q-3, verbatim from cell `C02-g-6`

<criterion id="Q-1" cell_refs="C02-g-6"/> After the round, OK rows with `bmv < 0` = **0 of N** (N = account-days over the affected partitions, printed); refused rows carry `UNCOMPUTABLE-NEGATIVE-BMV` with `None` on both legs.
<criterion id="Q-2" cell_refs="C02-g-6"/> **NEGATIVE CONTROL:** r_gross / r_net / status on every `bmv >= 1` row BYTE-IDENTICAL to the pre-round version per partition (prior VersionId by time); `gross_leg_vintage` UNCHANGED at `946b5c5a3c…` on every row; `schema_version` `"1.2"` on every row + manifest of the re-emitted partitions; UNaffected partitions untouched (R-6-shaped listing: 0 new versions outside the list; the four other canonical tables 0).
<criterion id="Q-3" cell_refs="C02-g-6"/> Mutex re-read before every batch; per-date artifact oracle; ledger via the tool with legs closed; the READERS clause in the plan; proof VALID rc=0 positional Q-1..Q-3. Graded by `3.0.0_SA_CVO` as a round.

## Do NOT

- ⛔ **Do not write before the N-5 engine is read on the RUNNING artifact** (commit != deployed; 84470).
- ⛔ **Do not widen the list to 535** without the issuer's word -- a measured set is the CTO's ruling.
- ⛔ **Do not route anything on this subject to `4.0.0_SA_CRO`.**

## What is owed back, and when

**Plan** (list size, batch shape, the READERS named, ETA at the measured 2.4 s/date) to `2.0.0_SA_COO` + `3.0.0_SA_CVO` when (1) lands; **GO** is the issuer's word on the plan after (2) is read. Then per-100 as before, completion + the acceptance pass, proof instance, ledger legs.
