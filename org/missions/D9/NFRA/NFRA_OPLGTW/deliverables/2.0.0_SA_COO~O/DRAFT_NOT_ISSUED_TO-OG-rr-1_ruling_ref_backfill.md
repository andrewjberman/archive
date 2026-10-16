# DRAFT, NOT ISSUED -- NFRA_OPLGTW task order `OG-rr-1` -- backfill `ruling_ref` on every name_rulings.json row (CTO ruling @8b9adcbd8d section 3, cell 1; CVO verdict 6495)

Status: held until `OG-ap-23` has released (the CTO's order: "off the 22:00Z critical path (after OG-ap-23)"). Cutting it earlier would change `name_rulings.json` under the release's commit. Then cut it as `TO-OG-rr-1` for worker slot `~111` (the worker that landed the rows), with the check `r37/checks/rr1.AC1.sh` (written, dry-run at the base: FAIL as expected) and `risk WORLD`.

## What it says (for the worker face)

`infra/logic/registry/name_rulings.json` rows carry `name`, `type`, one of `canonical` / `none_owed`, `evidence`, `owner`. The CVO verdict (verbatim): "the gate should check that ruling_ref names a record that exists at a commit, and refuse the row if it does not, not just print the field. A free-text field that only gets printed becomes a lift by assertion." Cell 1 adds the field; cell 2 (`OG-rr-2`) makes the gate check it.

1. Add `ruling_ref` to EVERY row: a string `<repo-relative path>@<commit sha>` naming a committed record that the row's own `evidence` cites (the evidence text names the ruling file or the order; read it; resolve the commit with `git log -1 --format=%H -- <path>` at the commit that carried the record, or the commit the evidence names). Rows from the CTO ruling @d97ea3ae82 cite `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_OPLGTW_CL7_NAMING_GATE_AND_MCPINDEX_AI_CLASSIFIED_20261016_Z.md` (its commit as `git log` resolves it locally).
2. A row whose ruling cannot be found in this repository (its evidence cites nothing, or a record not present locally) is NOT given an invented ref. List it by `(name, type)` in `W/RULING_REF_UNRESOLVED.json` = `{"unresolved": [{"name": ..., "type": ..., "evidence_cites": "<what it cites>", "why": "<one line>"}]}` so the CRO can rule it.
3. Criterion (`rr1.AC1.sh`): every row either has a `ruling_ref` that resolves by `git cat-file -e <commit>:<path>` or is listed unresolved; no row is in both; no row is in neither. Change no other field of any row; keep the file's formatting.

Bounds: `name_rulings.json` and the files under `W/` only; the gate is NOT touched in this cell (the gate check is cell 2, only after this merges).
