# MX-c-1 -- catalog writer, confirmed by census and exercised once; docstring corrected

`0.9.0_WK_NFRA_MCPINDEX~1`, task order `NFRA_MCPINDEX.TO-MX-c-1`, cut `4a475fe055` (base commit for every diff
check below). Read: PRD `org/missions/D9/NFRA/NFRA_MCPINDEX/prd/NFRA_MCPINDEX_PRD.md` @b7dc80e2cc (ENDPOINT +
C1-C8); decomposition `org/missions/D9/NFRA/NFRA_MCPINDEX/decompositions/NFRA_MCPINDEX_DECOMP.md` @f506f63a8b
s.1 falsifier 2, s.3 `MX-c-1` acceptance, s.6 gates, s.8 bounds, s.11 finding 1. Probe:
`org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~1/probes/mx_c_1.py`.

## MXC1-AC1 -- census of files opening the live catalog for writing

**Instrument:** `git ls-files` (tracked-file census) + a per-file regex scan (no docstring/header read).
**Invocation:** `py -3.12 probes/mx_c_1.py AC1`. **UTC:** 2026-09-21T05:12:52Z.
**Denominator:** 39,054 tracked files scanned; 5 of 39,054 `.py` files contain the literal `DATA_CATALOG.yaml`;
1 write-call found among those 5.

Candidates (5): `infra/aws/ec2/opal-gateway/app/graphql_plumbing/exercise_catalog_gate.py`,
`infra/aws/ec2/opal-gateway/app/query_v0.py`, `workflows/atom_decomposition/battery_catalog_v02.py`,
`workflows/atom_decomposition/emit_catalog_v02.py`, `workflows/atom_decomposition/validate_catalog_v02.py`.

Write-call (1): `workflows/atom_decomposition/emit_catalog_v02.py:735  var=OUT  with io.open(OUT, "w",
encoding="ascii") as f:` -- `OUT` was assigned at `:43` from `os.path.join(OUT_DIR, "DATA_CATALOG.yaml")`, the
only line among the 5 candidates whose right-hand side names the literal AND is later opened with a `"w"` mode.
`VERDICT: PASS-MXC1-AC1`.

## MXC1-AC2 -- each candidate writer's own bytes, and any disclaiming line

**Instrument:** same census, re-run; prints the write-call's source line and any line in that file matching a
catalog-scoped disclaim pattern (`never touch|writ` AND `DATA_CATALOG`, case-insensitive -- narrowed after a
first pass over-matched an unrelated `:709` comment about a different served key).
**UTC:** 2026-09-21T05:12:55Z.

```
WRITE-CALL BYTES -- workflows/atom_decomposition/emit_catalog_v02.py:735:     with io.open(OUT, "w", encoding="ascii") as f:
```

Post-AC5-fix, no line in the file currently matches the catalog-scoped disclaim pattern; the module docstring's
line 5 (previously the disclaimer) now reads the corrected statement (see AC5 below). `VERDICT: PASS-MXC1-AC2`.

## MXC1-AC3 -- exactly one writer, targeting the live path

**Instrument:** same census; the sole writer's target resolved by importing `emit_catalog_v02` (side-effect-free:
`main()` is guarded by `if __name__ == "__main__"`) and reading its `OUT` attribute directly, compared
(`os.path.normpath`) to the live path. **UTC:** 2026-09-21T05:12:57Z.

```
WRITERS FOUND: 1
RESOLVED TARGET (module attribute workflows/atom_decomposition/emit_catalog_v02.py.OUT): C:\tmp\wk-mcpindex-1\infra\aws\ec2\opal-gateway\app\refs\DATA_CATALOG.yaml
LIVE PATH (this cell's grain): C:\tmp\wk-mcpindex-1\infra\aws\ec2\opal-gateway\app\refs\DATA_CATALOG.yaml
MATCH: resolved target == live path
```

Exactly one writer, targeting the live path. `VERDICT: PASS-MXC1-AC3`.

## MXC1-AC4 -- REFUSED (grant conflict), filed as BLOCKING row `NFRA_MCPINDEX-W1-S1`

**UTC:** 2026-09-21T05:12:59Z. This criterion requires running the named writer once, with one reversible change
to an emitter input, observing the **served file** (`infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml`)
change by exactly that row, then reverting -- "the run and its revert both in the cell's command log".

This cell's `<paths>` grant is exactly two entries: `workflows/atom_decomposition/emit_catalog_v02.py` (and,
by the cell's own writes line, only its module docstring lines 1-10) and this project's investigation file.
Exercising AC4 as written needs write access to (a) the served file itself, and (b) an emitter input under
`workflows/atom_decomposition/runs/<unit>/<stamp>/rectangle.final.certified.json` (`lift_catalog_v02.py:308-313`
`resolve_substrates()`/`scan_unit()` -- the only lever for a "reversible change to an emitter input" that does
not edit the emitter's own non-docstring code, itself out of grant). Neither path is named.

Per the worker face BOUNDS (top-level and this TO's own): "A path you need that is not named is a BLOCKING
surprise row on that criterion -- never an override." Per decomposition bound 9: "A criterion that cannot be
satisfied as written is REFUSED and reported with its measurement, never repaired, widened or met by another
route" -- redirecting `OUT` to a scratch path would not exercise the NAMED writer against the NAMED live path
(the exact thing AC3 confirms and AC4 extends), so that is not a route taken.

**Filed:** `NFRA_MCPINDEX-W1-S1` (class BLOCKING, hazard_standing INERT) in
`org/missions/D9/NFRA/NFRA_MCPINDEX/surprise-channel/investigations/INVESTIGATION_v1.md`.
`VERDICT: FAIL-MXC1-AC4 REFUSED -- exercising the named writer against the live path requires writing
infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml and a workflows/atom_decomposition/runs/ input file,
neither granted by this cell's <paths>; filed as BLOCKING row NFRA_MCPINDEX-W1-S1, not overridden.`

## MXC1-AC5 -- docstring disclaimer corrected, single-hunk diff

**Instrument:** `git diff --stat|-U0 4a475fe055 -- workflows/atom_decomposition/emit_catalog_v02.py` (fixed cut
base, reproducible pre- or post-commit) + a direct read of the current bytes. **UTC:** 2026-09-21T05:13:04Z
(re-verified after the ruff rename below; unchanged).

```
git diff --stat 4a475fe055 -- workflows/atom_decomposition/emit_catalog_v02.py:
workflows/atom_decomposition/emit_catalog_v02.py | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)

@@ -5 +5 @@ catalog_v02/DATA_CATALOG.v0.2.staged.yaml (the STAGED port artifact).
-THE LIVE refs/DATA_CATALOG.yaml IS NEVER TOUCHED BY THIS SCRIPT. The staged file becomes
+THIS SCRIPT WRITES THE LIVE refs/DATA_CATALOG.yaml DIRECTLY (V03-2; see :38-43 below: query_v0 loads it, catalog_gate enforces it, the EC2 deploy tree ships it, and this emitter WRITES it -- no staged copy, no second output). Historically the staged file became
```

One file, one hunk, lines 1-10 only (line 5), and the new text agrees with `:38-43` ("this emitter WRITES...
no staged copy, no second output"). `VERDICT: PASS-MXC1-AC5`.

## MXC1-AC6 -- catalog header line 3 still names the writer

**Instrument:** direct read of `infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml:3`.
**UTC:** 2026-09-21T05:13:01Z.

```
infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml:3: # BUILT BY: workflows/atom_decomposition/emit_catalog_v02.py at git HEAD a4f1686a28
```

Unchanged (this cell never writes `CAT`, per bound 10). `VERDICT: PASS-MXC1-AC6`.

## MXC1-AC7 -- judgment, no verdict here

`org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~1/probes/mx_c_1.py AC7` prints the
record for `3.0.0_SA_CVO` at L9 and emits no PASS/FAIL line, per PROOF_OF_SPEC.schema.json `judgment`. Recorded
in the proof-of-spec instance as `UNVERIFIABLE-BY-INSTRUMENT`, status_reason naming the CVO as the oracle.

## Summary

| criterion | verdict | denominator |
|---|---|---|
| MXC1-AC1 | PASS | 39,054 tracked files; 5 candidates; 1 write-call |
| MXC1-AC2 | PASS | 1 writer's bytes printed; 0 catalog-scoped disclaim lines remain |
| MXC1-AC3 | PASS | 1 of 1 writers targets the live path |
| MXC1-AC4 | FAIL (REFUSED, grant conflict) | filed `NFRA_MCPINDEX-W1-S1` |
| MXC1-AC5 | PASS | 1 file, 1 hunk, line 5 only |
| MXC1-AC6 | PASS | header line 3, unchanged |
| MXC1-AC7 | judgment | no verdict; record left for the CVO |
