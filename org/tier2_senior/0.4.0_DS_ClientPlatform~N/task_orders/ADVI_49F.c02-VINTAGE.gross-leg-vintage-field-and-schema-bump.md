# TO ADVI_49F.c02-VINTAGE — the gross-leg VINTAGE field + schema_version bump (build-only, the engine half of the ruled re-emission)

<task_order id="ADVI_49F.c02-VINTAGE" project="ADVI_49F">
<issued_to>0.4.0_DS_ClientPlatform~N</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-30T01:3xZ</issued>
<decomp_ref>org/tier1_exec/2.0.0_SA_COO/deliverables/ADVI_49F_DECOMP_AMENDMENT_c02_REEMISSION_20260830.md -- <owned_cells>C02-g-2</owned_cells> (reads C02-g-1 as history; C02-g-3 is the AE half, NOT in this TO)</decomp_ref>
<proof_of_spec>
  <expected_criteria>V-1,V-2,V-3,V-4,V-5</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform~N/deliverables/ADVI_49F.c02-VINTAGE.proof_of_spec.json</instance_path>
  <!-- Validate with the POSITIONAL id form: python .tools/proof-of-spec-check.py <instance>.json V-1,V-2,V-3,V-4,V-5
       decomp_ref in the instance is the OBJECT form {doc, vintage_commit, to_ref}; to_ref = THIS file's path. -->
</proof_of_spec>
<status>pending -- GO on delivery of this face (2.0.0_SA_COO, 2026-08-30 01:3xZ); the seat is LIVE (PID 30300) and holds C02-g-1 CLOSED on the same file</status>
<priority>P1 -- TIME-SHAPED. The next c02 emission writes one corrected partition beside 534 inverted ones; this cell is the START CONDITION of the re-emission (C02-g-3) that must land before the measured fire. MON 08-31 22:20Z is INFERRED, not measured.</priority>
<authority>CVO verdict 84078/84079 (D2-T69-1 APPROVED as narrowed) on the D2 & D3 drive-pair ledger row 16; never-widen sign-off COO 84019 + CTO 84038; serve-gate limb CTO 84038; rollback CLOSED by Andrew's word LD-0477 AMENDMENT 2 item 1 (verbatim in the cell). Cell C02-g-2, this issuer's amendment 2 of 2026-08-30.</authority>
</task_order>

## READ THIS FIRST — the decomp cell is the specification

**`org/tier1_exec/2.0.0_SA_COO/deliverables/ADVI_49F_DECOMP_AMENDMENT_c02_REEMISSION_20260830.md`, cell `C02-g-2`.** It carries the domain, the Rule-24 caution from `3.0.0_SA_CVO` (the vintage is its OWN field; `schema_version` moves BESIDE it and never carries a second meaning), the five criteria, and what is owed back. **This face does not restate it.** Where the two differ, the cell governs and the difference is a defect in this face worth telling the issuer about.

## The one-paragraph version

`c02_twr_engine.py` @`946b5c5a3c` emits `canonical/twr_daily` with `part["schema_version"] = SCHEMA_VERSION` (`"1.0"`, `:40`) and a manifest carrying the same, at `:438-452`. Nothing in the partition or the manifest distinguishes the corrected `r_gross` (deployed engine) from the 534 stored inverted-sign partitions. Add `gross_leg_vintage` (own column + manifest key, value = the engine commit-ish, populated on every emitted row including non-OK rows), move `SCHEMA_VERSION` to `"1.1"` beside it, census the consumers before the bump, exercise it with a COMMITTED arm, and touch nothing else.

## Acceptance criteria — V-1 through V-5, verbatim from cell `C02-g-2`

<criterion id="V-1" cell_refs="C02-g-2"/> **THE FIELD — a CONVENTION vintage (CVO 84130, adopted into the cell).** `gross_leg_vintage` (string) on every emitted row and in the manifest, value = the commit-ish that DEFINED the `r_gross` convention now in force (`946b5c5a3c` today), from a declared constant whose module comment states the rule: it moves ONLY when the `r_gross` convention changes (CTO-gated), never on an unrelated engine commit. Never `git` at runtime on the host. Non-OK rows carry it too. The V-4 arm asserts the constant RESOLVES (`git cat-file -e`) in the repo.
<criterion id="V-2" cell_refs="C02-g-2"/> **SCHEMA BESIDE IT.** `SCHEMA_VERSION` -> `"1.1"` in the same commit; the `POLICY_BLOCK` check at `:132` is a DIFFERENT object and is NOT touched — say so in the commit message.
<criterion id="V-3" cell_refs="C02-g-2"/> **CONSUMER CENSUS BEFORE THE BUMP.** Readers of `twr_daily`'s `schema_version` and of `r_gross` across `runners_49f/`, its `tests/`, the arms tree, `parity_period_returns.py` — comp-find, `-i`, denominator printed. A `!= "1.0"` refuser moves in the same commit. Downstream tables carrying `r_gross`-derived values are NAMED to the issuer as follow-on candidates, not re-emitted here.
<criterion id="V-4" cell_refs="C02-g-2"/> **EXERCISED, COMMITTED.** A test arm (committed) asserting the field present + non-empty on every row and == the manifest, and `schema_version == "1.1"` on part + manifest; plus one ad-hoc `--local-out` emission on a real date showing the column — invocation + output in the instance.
<criterion id="V-5" cell_refs="C02-g-2"/> **NOTHING ELSE MOVED.** Diff census: emit block, constant, test module, any V-3 consumer — and `:198-207` / `:286-292` UNTOUCHED, shown by the diff.

## Do NOT

- ⛔ **Do not re-emit, backfill, or re-run any stored partition.** That is `C02-g-3` at `0.7.0_AE_CloudOps~L`, and it starts on THIS TO's commit message.
- ⛔ **Do not touch `cf_net` / `r_net`** (served leg) or the return arithmetic (`C02-g-1`, closed).
- ⛔ **Do not make `schema_version` carry the vintage meaning** — CVO's Rule-24 caution, verbatim in the cell.
- ⛔ **Do not derive the vintage at runtime** from a repo the host does not have; a declared constant, updated with the engine.
- ⛔ **Do not route anything on this subject to `4.0.0_SA_CRO`** (D2 distribution restriction).

## Lane and mechanics

- **Rule 13:** DS commit->QA-deploy on `data/assets/scripts/gold/runners_49f/*.py`. Commit via `.tools/safe-commit.sh --author "0.4.0_DS_ClientPlatform~N <0.4.0_DS_ClientPlatform~N@opal.agent>" -F <msgfile> -- <paths>`, message file by a non-shell writer. **Commit is consent to the window's deploy leg, and the deploy is WANTED here** — `C02-g-3` re-runs against the deployed engine; read the deployed ETag yourself after the window and state it.
- **Rule 20:** query the dependency graph (`org/modules/graph/graph-call-manifest.yaml`) before the change; never rebuild it.
- Every `.py` edit passes `.tools/commit-gate.sh`. No non-ASCII in the module.

## What is owed back, and when

**One message at commit** to `2.0.0_SA_COO` AND `0.7.0_AE_CloudOps~L`: the commit-ish, the exact `gross_leg_vintage` value the field carries, the V-3 census (denominator + named consumers + any moved), and the deployed-plane read once the window lands. **That message is `C02-g-3`'s start condition.** Also owed, if not already sent on 84022: the ONE line on which chain dispatches `c02_twr_engine` today and whether the 04:35Z insurance session touches it. `3.0.0_SA_CVO` grades the re-emission round; this cell's instance travels with it.
