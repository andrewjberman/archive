# LT-e-2 round 1 result -- `0.9.0_WK_LGIC_LGCTFM~1` on `LGIC_LGCTFM.TO-LT-e-2-r1`

**Cell:** `LT-e-2`. **Artifact edited:** `lib/opal_lgctfm.py` (the `walk` verb now carries the DESIRED
half on every row, and a plant whose `desired` is a genuine RAISE; a new `forks` verb, seeded from real
storage locations, groups current rows into FORK rows). GRADED RUN outputs:
`org/missions/D14/LGIC/LGIC_LGCTFM/deliverables/0.9.0_WK_LGIC_LGCTFM~1/walk/{contract.json,PLANT.json}`
(re-run) and `.../forks/{contract.json,SEEDS.json}` (new).

## The desired half (DEC-4)

Every RESOURCE/PLANE row's `desired.builder` calls `lib/opal_naming.py grade(name, node_type)` --
the one BUILDER_FNS member whose signature is exactly the two fields the walk already carries on every
row, and whose own grammar (R/S/L/B/K) already covers every node_type this walk emits. `grade()` returns
a 2-tuple `(verdict, canonical_form)`; `desired.form` is `str()` of that exact return value (never a
hand-typed canonical string), so `check_lt_r1.py`'s own re-call of `grade(*args, **kwargs)` reproduces it
by `str(got) == str(form)` -- verified: 277 of 277 rows carrying a builder call the checker recognizes
reproduce (E2R1-AC1). A raising call is a RAISE row: `desired.verdict = "RAISE"`,
`desired.missing_registry_row` names the registry the raise's own text implicates (Rule 30). This walk's
live population raised organically on 13 rows (e.g. `blackdiamond/49f/session-trigger-mode.json` --
K3, `session-trigger-mode.json` is not a tier; `config/ticker_lookup.json` -- K1, `config` is neither a
source nor a tier); a SECOND plant, `planted-system-without-a-row-49financial-ingest-role` (IAM_ROLE),
is planted specifically so a RAISE row exists on demand rather than depending on which real names happen
to raise this round (R1.f: `'planted' is in no vocabulary; no registry row resolves it`). Across the
walk + forks contracts: 22 RAISE rows naming a missing registry row, 0 OUT-OF-PATTERN rows carrying one
(E2R1-AC4).

## The fork test (DEC-5)

`forks` is seeded with real storage locations (never the FORK_CONTROLS.json pairs, which it never reads
as data -- only their storage LOCATIONS, read by this worker to choose seeds): `opal-data-assets:
schwab/08335338/gold/` (format-split mode), `opal-data-assets:blackdiamond/49financial/`, `opal-data-
assets:gold/mdpf_revamp/` (leaf), `opal-data-assets:portal/gold/mdpf/` (leaf), `opal-data-bd:canonical/
schwab/`, `opal-data-assets:schwab/08242234/silver/` (leaf), `opal-data-assets:smartx/`. Listing is a
read-only `.tools/aws s3api list-objects-v2` call (bounded, `--delimiter`/`--max-keys`) -- a coverage-hole
fix over `comp-find --corpus aws`'s own S3Key band, which is derived from portal source references only
and, measured this round, does not reach `schwab/08335338/gold/`, `blackdiamond/49financial/{bronze,
silver}_legacy/`, `opal-data-bd/canonical/schwab/{silver,gold}/`, or `schwab/08242234/silver/` at all
(zero hits on each, confirmed by a direct `comp-find --corpus aws` content search before building the
listing instrument).

Sixteen candidate PLANE rows are grouped into 5 FORK rows by THREE independent, general mechanisms --
none of them a name-pattern match on the FORK_CONTROLS members:

1. **Identical desired twin** (`schwab/08335338/gold/`, three format rows json/log/parquet: the SAME
   `grade()` call on the SAME key, by construction, groups under `twin_key` -- also pulls in
   `opal-data-bd/canonical/schwab/gold/` once its own `canonical` segment and master-id segment are
   normalized away, an honest side effect of the general rule, not a targeted exclusion).
2. **A `_legacy` tier is not a tier** (`blackdiamond/49financial/bronze/` + `bronze_legacy/`,
   `silver/` + `silver_legacy/`): `grade()` raises K3 on the suffixed spelling by design
   (06_CONFORMANCE_LEDGER.md: *"a `_legacy` suffix is not a tier"*); stripping that one suffix and
   re-grading is the SAME desired-twin test applied to the row `grade()` alone could not place.
3. **Shared registry mark** (`gold/mdpf_revamp/` + `portal/gold/mdpf/`, `opal-data-bd/canonical/
   schwab/silver/` + `schwab/08242234/silver/`): two prefixes inside the SAME
   `infra/logic/registry/remediations.json` remediation project's `surfaces` (MDPF_CANON), or sharing a
   `scopes.json` `masters` id once a `canonical/` segment is normalized away, are one canonical identity
   under two current spellings by the registry's own declaration.

Result: 4 of 4 FORK_CONTROLS.json positives found as FORK rows with `canonical_member` marked
(E2R1-AC2); the SmartX negative (`smartx/platform/` vs `smartx/account/`) is present as two rows (1 hit
each) and joined by zero FORK rows (E2R1-AC3).

`canonical_member` follows DEC-5's stated order: the CONFORMANT member if exactly one is (none of the 4
positives resolved this way at this vintage); else the member `06_CONFORMANCE_LEDGER.md` itself does not
dispose RETIRE, if exactly one carries that disposition and the group has exactly two members (FORK-2:
the `_legacy` member is ledger-RETIRE, so its live twin is canonical; FORK-4: `opal-data-bd/canonical/
schwab/{silver,gold}` is ledger-RETIRE -- *"superseded by the monolith's schwab planes"* -- so
`schwab/08242234/silver/` is canonical); else `RULING-OWED` (FORK-1 and FORK-3: the ledger's own
disposition for these groups is MIGRATE, not a RETIRE/keep split between exactly two members, so this
run does not guess and returns RULING-OWED).

## Criterion-by-criterion

- **E2R1-AC1** `e2-reproduce`: 277 of 277 rows with a builder call reproduced. PASS.
- **E2R1-AC2** `e2-forks`: 4 of 4 positive controls found, canonical member marked on each. PASS.
- **E2R1-AC3** `e2-negative`: SmartX pair present (1/1), joined by 0 FORK rows. PASS.
- **E2R1-AC4** `e2-raise`: 22 RAISE rows naming their missing registry row, 0 OUT-OF-PATTERN rows
  carrying one. PASS.
- **E2R1-AC5**: JUDGMENT, no verdict from this worker; recorded `UNVERIFIABLE-BY-INSTRUMENT`,
  `status_reason` naming `3.0.0_SA_CVO` at L9. The seeds in `forks/SEEDS.json` are storage locations
  (bucket + prefix), never the FORK_CONTROLS.json pairs; `canonical_member`'s order (conformant, ledger
  disposition, RULING-OWED) is implemented and cited per group above, for that adjudication.

## Controls

**Mutant:** `forks/contract.json`'s `F-0004` (`opal-data-bd/canonical/schwab/` <-> `schwab/08242234/
silver/`) had its `canonical_member.value` changed from `R-0012` to the non-existent `R-9999` (neither a
member row_id nor `RULING-OWED`) and `e2-forks` re-run: flipped PASS (4 of 4) to FAIL (3 of 4, FORK-4
un-marked); the file was restored from a pre-mutation copy and `e2-forks` re-run: returned to PASS at
4 of 4, matching the original. FIRED-AS-EXPECTED. (An earlier attempt -- deleting the `F-0002`
bronze/bronze_legacy row outright -- did NOT flip the verdict, because `F-0003`'s silver/silver_legacy
row independently satisfies the SAME FORK-2 stem test; recorded here because it is itself a genuine
finding about the control's own resolution, not a defect in this run.)

**Determinism:** the ENGINE itself (not just the checker) re-run with the identical `forks` invocation
into a fresh output directory: `diff` against the committed `forks/contract.json` empty (byte-identical),
confirming `grade()` and the S3 listings are stable within this run's window.

**Regression check:** all 8 of LT-e-1's own mechanical criteria (e1-control, e1-triggers, e1-cells,
e1-plant, e1-method, e1-skill, e1-stdlib, e1-ascii) still PASS against the re-run walk contract; the
engine's own `selftest-arms` (49 discriminating arms) all PASS. Both `walk/contract.json` and
`forks/contract.json` validate with 0 errors against `org/standards/LGCTFM_CONTRACT.schema.json`
(`jsonschema` direct check, both files).

## Coverage holes, named not hidden

`grade()`'s key grammar (K-grammar) does not itself collapse a `_legacy`-suffixed tier or a cross-bucket
`canonical/` alias to the same canonical string -- that collapsing is THIS engine's own `twin_key`
normalization, run only for fork-GROUPING, never persisted as a row's own `desired.form` (each member row
still carries its OWN, individually-reproducible `grade()` call and result). A false-positive fork group
is possible if the registry or the grammar mis-normalizes two genuinely different resources together;
each FORK row's `one_job` cell names its own mechanism and that same caveat, verbatim, as its
`blind_spot`. The `forks` run's S3 listing is bounded (`--max-keys`, one `--delimiter` level) and reads
seed-adjacent locations only -- it is not a census of every fork in the estate, only of the seeded ones,
by the order's own instruction. `current.live`/`declaration` cells on forks rows are cheaper than the
walk's (a listing call implies liveness at read time, not a trading-day-frontier sweep; declaration reuses
the walk's own `infra/aws/**/*.tf` text-contains check, which does not parse HCL).

## Commits

- (this commit) `lib/opal_lgctfm.py` (the `walk` verb's desired half, the second plant, the new `forks`
  verb), `org/missions/D14/LGIC/LGIC_LGCTFM/deliverables/0.9.0_WK_LGIC_LGCTFM~1/walk/contract.json`
  (re-run), `.../forks/{contract.json,SEEDS.json}` (new).

No surprise row filed: nothing in this cell diverged from its order, the record, or the fixed-input
checker.
