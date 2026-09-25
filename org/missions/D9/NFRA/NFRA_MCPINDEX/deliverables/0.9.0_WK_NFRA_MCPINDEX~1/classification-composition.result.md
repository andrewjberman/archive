# MX-c-4 -- classification and registration compose from each integration's own declaration

`0.9.0_WK_NFRA_MCPINDEX~1`, task order `NFRA_MCPINDEX.TO-MX-c-4`, cut `60464dd3f8` (base commit for every
diff/before-reading below). Read: PRD `org/missions/D9/NFRA/NFRA_MCPINDEX/prd/NFRA_MCPINDEX_PRD.md` @b7dc80e2cc
(ENDPOINT + C2); decomposition `org/missions/D9/NFRA/NFRA_MCPINDEX/decompositions/NFRA_MCPINDEX_DECOMP.md`
@f506f63a8b s.1 finding (brief IV.9 / falsifier 6 row `read_teams_attachment`), s.3 `MX-c-4` acceptance, s.6 gates
(N-1), s.8 bounds 9/10/14, s.9 postulate (iv), s.11 findings 11-12. Probe:
`org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~1/probes/mx_c_4.py`; test file:
`infra/aws/ec2/opal-gateway/tests/test_tool_classification_composition.py`.

## Design, in one paragraph

`IntegrationSpec` (`INT/base.py`) gains three new fields, each defaulting to empty: `tools` (the tool-name
manifest an integration DECLARES), `tool_classifications` (name -> a destructive_ops-shaped tag) and
`tool_catalog_refs` (name -> a `DATA_CATALOG.yaml` entity id). `validate_integration_spec` refuses a spec when a
name in `tools` lacks either. `INT/registry.py` tracks which spec currently owns each live tool
(`_ACTIVE_BY_TOOL`) and, after `register()`, refuses (strips from the report, "composed_path_refused") any
ACTUALLY-registered tool that resolves through NEITHER this spec's own declaration NOR
`app/data_entitlement.py`'s existing classification -- the defense-in-depth net MXC4-AC12 names.
`APP/destructive_ops.py.classify()` composes: native tags first (unchanged), then a lazy lookup through the
active spec (`registry.classification_for_tool`), then the fail-closed default (unchanged). None of the four
real integrations (`ycharts`, `opal_portal`, `globgrph`, `schwab`) declare the new fields -- their `integration.py`
files are outside this cell's `<paths>` grant -- so they have nothing checked on the new axis and behave exactly
as before; they are not exempted, they simply never opted in, which is what "an integration that declares no
manifest" means everywhere in this diff.

## MXC4-AC1 -- IntegrationSpec carries a per-tool classification + catalog-entry reference; refused when either
is missing

**Instrument:** `pytest -q -s tests/test_tool_classification_composition.py::test_mxc4_ac1` (planted specs,
`validate_integration_spec` called directly). **Invocation:** `py -3.12 probes/mx_c_4.py AC1`. **UTC:**
2026-09-21T09:20Z.

```
complete spec errs=[]
missing-classification errs=["tool 'mxac1_x' has no classification declared on the integration spec (C2)"]
missing-catalog-ref errs=["tool 'mxac1_x' has no catalog-entry reference declared on the integration spec (C2)"]
```
`VERDICT: PASS-MXC4-AC1`.

## MXC4-AC2 -- destructive_ops.classify(tool) reads through the registered spec; fail-closed for the undeclared

**Instrument:** `pytest -q -s ...::test_mxc4_ac2`. **UTC:** 2026-09-21T09:21Z.

```
declared tool -> class=<OpClass.SAFE: 'safe'> unclassified=None
undeclared tool -> class=<OpClass.IRREVERSIBLE_SEND: 'irreversible_send'> unclassified=True
```
`VERDICT: PASS-MXC4-AC2`.

## MXC4-AC3 (difference) -- planted integration, missing classification refused / present registers

**Instrument:** `pytest -q -s ...::test_mxc4_ac3` (`registry.register_enabled` against a planted factory).
**UTC:** 2026-09-21T09:22Z. Missing: `report[iid] = {'error': 'invalid integration spec...'}`, `mcp.names=[]`
(zero tools added anywhere -- `register()` was never called). Present: `report[iid]['tools'] == ['mxac3_a']`,
`mcp.names == ['mxac3_a']`. `VERDICT: PASS-MXC4-AC3`.

## MXC4-AC4 (difference) -- planted tool, missing catalog ref refused / present registers

**Instrument:** `pytest -q -s ...::test_mxc4_ac4`. **UTC:** 2026-09-21T09:23Z. Same shape as AC3, over the
catalog-ref axis. `VERDICT: PASS-MXC4-AC4`.

## MXC4-AC5 -- the four existing ids register exactly as before, names printed before and after

**Instrument:** a faithful BEFORE snapshot -- the live worktree copied to a temp dir, then exactly the four
files this cell writes (`destructive_ops.py`, `data_entitlement.py`, `integrations/base.py`,
`integrations/registry.py`) reverted to their `HEAD` (this cell's cut, `60464dd3f8`, pre-edit) bytes via
`git show HEAD:<path>`; everything else, INCLUDING the four real integrations' own directories, is untouched.
`register_enabled`'s underlying `factory().register(stub_mcp)` is run in each tree (a zero-side-effect stub
`mcp` that only records `@mcp.tool()` names). **UTC:** 2026-09-21T09:24Z.

```
BEFORE (HEAD 60464dd3f8, pre-edit):           AFTER (this worktree):
  globgrph:     2 names                         globgrph:     2 names  (identical)
  opal_portal:  1 name                          opal_portal:  1 name   (identical)
  schwab:       5 names                         schwab:       5 names  (identical)
  ycharts:      6 names                         ycharts:      6 names  (identical)
```
Byte-identical name sets, both directions. `VERDICT: PASS-MXC4-AC5`.

## MXC4-AC6 -- 49 existing tool names, zero collateral classification differences

**Instrument:** the same BEFORE/AFTER snapshot pair; `destructive_ops.classify(n)` and `data_entitlement.classify(n)`
called for every `n` in the union of `NATIVE_TOOLS | INTEGRATION_TOOLS | SCHWAB_TOOLS`, both trees. **UTC:**
2026-09-21T09:25Z. **DENOMINATOR: 49** (union of before/after name sets, printed).

The only difference across all 49: `read_teams_attachment` (`dop_class` `irreversible_send`->`safe`,
`dop_unclassified` `true`->`false`; `de_class` unchanged, `legacy` both sides) -- exactly the deliberate change
MXC4-AC7/AC8 own and grade. Zero OTHER differences. `VERDICT: PASS-MXC4-AC6`.

## MXC4-AC7 -- read_teams_attachment classified, no longer fail-closed-denied

**Instrument:** direct import, `destructive_ops.classify('read_teams_attachment')` +
`data_entitlement.classify('read_teams_attachment')`. **UTC:** 2026-09-21T09:26Z.

```
destructive_ops.classify -> {'class': SAFE, 'reversible': True, 'irreversible': False, 'native_undo': None, 'blast_dimensions': []}
data_entitlement.classify -> 'legacy'
'read_teams_attachment' in destructive_ops.SAFE_TOOLS -> True
```
`VERDICT: PASS-MXC4-AC7`.

## MXC4-AC8 -- JUDGMENT (CVO, no verdict here)

`read_teams_attachment` was classified SAFE, in `destructive_ops.SAFE_TOOLS`, alongside `read_document`,
`read_site_file`, `read_workbook` and the other content-read tools already there. Reasoning recorded for the
CVO's grade: the tool resolves a Teams-message attachment `contentUrl` (already visible to any caller who can
call the already-SAFE `read_chat_messages`/`read_channel_messages`) and reads bounded text/CSV/markdown, or
returns a structured hint for binary files -- no external mutation, no write-class tag in `TOOL_WRITE_CLASS`
(`APP/destructive_ops.py`), and it does not widen what any tier reaches: the attachment's existence and location
were already exposed by the two SAFE list/read tools that hand this tool its `content_url` argument. Status:
`UNVERIFIABLE-BY-INSTRUMENT`, `status_reason`: "classification correctness is a judgment call over the read
surface it exposes, per the task order's own AC8 label -- graded by 3.0.0_SA_CVO at L9."

## MXC4-AC9 -- pinned count becomes a derived, by-name assertion; fails on an unpinned plant

**Instrument (planted difference):** `pytest -q -s ...::test_mxc4_ac9_diff` (`diff_against_pin`, the factored
comparison both the real check below and `TST/test_entitlement_admin.py:332`'s own assertion now use).
**Instrument (real population):** a subprocess replay of the identical composition `test_entitlement_admin.py:332`
now runs in-file (that file cannot be collected on this box -- see AC10's SCOPE_NOTE; the replay runs the SAME
code path directly so the real population is still measured here). **UTC:** 2026-09-21T09:27Z.

```
planted: with unpinned plant -> [('mxac9plant', ['mxac9_b'], [])]; plant removed -> []
real:    mismatches=[] registered_len=44 derived_len=44
```
`VERDICT: PASS-MXC4-AC9`.

## MXC4-AC10 -- Gateway suite counts, before and after, no new failure

**SCOPE (printed in full by the probe, reproduced here):** the full tracked suite (163 files, decomp s.7) does
not finish inside this criterion's own `timeout 120` budget -- MEASURED: 280s was not enough
(`--continue-on-collection-errors`, terminated by the harness). Two exclusions, both MEASURED and PRE-EXISTING
(present before this cell touched anything):
  (a) 14 collection units (`tests/acceptance/` + 13 `tests/test_*.py` files, `test_entitlement_admin.py` among
      them) fail to COLLECT with `ModuleNotFoundError: No module named 'moto'` on this box -- confirmed via
      `pip show moto` (not found) and `py -0` (only Python 3.12 installed). Bound 14 ("a missing instrument is a
      refusal, never an install") forbids fixing this here. `--collect-only`: 150 tests collected, 14 errors, 1.13s.
  (b) `tests/test_schwab_engine.py` (spawns a child job-runner process) did not terminate within 100s locally;
      excluded per bound 11 ("every invocation terminates").
**Instrument:** `py -3.12 -m pytest -q --color=no <the 10 remaining files> + this cell's own new test file`.
**BEFORE** (captured 2026-09-21, before this cell's first edit, over the 10 pre-existing files only): `1 failed,
130 passed, 55 warnings, 34 subtests passed in 12.99s`; the one failure,
`tests/test_identity_scope.py::test_scoped_deny_by_default`, is in an UNRELATED module (`app/identity_scope.py`)
this cell never touches -- PRE-EXISTING, bound 17 ("a pre-existing failure is not its to fix"). **AFTER** (same
10 files + `test_tool_classification_composition.py`): `1 failed, 137 passed` -- the SAME one pre-existing
failure, plus this cell's own 7 new passing tests. Newly-failing (passed before, fails after): `[]`.
**UTC:** 2026-09-21T09:28Z. `VERDICT: PASS-MXC4-AC10`.

## MXC4-AC11 -- C2's bar, AMENDED (issuer `0bec07601a`, per CTO ruling `@5f3b4a20c6`): two registry limbs only

**Original text (2026-09-21) superseded below.** The catalog-entry limb is struck from AC11 by the amendment; it
is graded on each tool's own shipping cell (`MX-t-1` .. `MX-t-7`). AC11's probe (`mx_c_4.py::ac11`) was conformed
to drop the catalog walk and grade only `destructive_ops.classify` + `data_entitlement.classify`, by name, over
every registered tool -- see the 2026-09-25 re-run section below for the graded measurement.

Original (2026-09-21) measurement, kept for record: direct import; for every name in the 49-tool union,
`destructive_ops.classify`, `data_entitlement.classify` and a parsed-YAML walk of `CAT` for any
`tools`/`tool_ref`/`tool_refs` field anywhere in the document. DENOMINATOR 49.
```
CAT tool-reference fields found across the whole catalog: 0
fails destructive_ops.classify (no declared class): 14 of 49 (the 9 ycharts/opal_portal/globgrph + 5 schwab
  tools -- their owning specs declare no per-tool manifest, since their integration.py files are outside
  this cell's <paths>)
fails data_entitlement.classify: 0 of 49
fails catalog-entry-reference resolution: 49 of 49
```
Filed then: `NFRA_MCPINDEX-W1-S5`.

## MXC4-AC12 (difference) -- composed-path bypass, resolving through neither registry, refused

**Instrument:** `pytest -q -s ...::test_mxc4_ac12` -- a planted spec whose OWN manifest is empty (so
`validate_integration_spec`'s pre-check has nothing to catch) but whose `register()` adds a tool anyway (the
composed-registration-path bypass). **UTC:** 2026-09-21T09:30Z.

```
neither registry:            report['tools']=[] composed_path_refused=['mxac12_orphan'] mcp.names=['mxac12_orphan']
resolves via data_entitlement: report['tools']=['mxac12_orphan'] (no composed_path_refused)
```
`register()` DID run (the tool was reachable); the report/registry-level check refuses it when it resolves
through neither registry, and ships it once it resolves through one. `VERDICT: PASS-MXC4-AC12`.

## RE-RUN 2026-09-25 (post-amendment `0bec07601a`, per CTO ruling `@5f3b4a20c6`) -- `0.9.0_WK_NFRA_MCPINDEX~1`

Every mechanical criterion's own `<invocation>` names `py -3.12` verbatim. On this device today `py -3.12`
returns rc=103 `No suitable Python runtime found` for every one of the 11 mechanical criteria (AC1-AC7,
AC9-AC12), each run as `cd /c/tmp/mx-1 && timeout 120 py -3.12 .../probes/mx_c_4.py AC<n>`; `py -0`/`py -0p` list
only Python 3.11 as launcher-registered, a filesystem sweep finds no Python312 anywhere on the device, and this
cell's own build-commit record (line 137 above) shows the device carried "only Python 3.12 installed" at build
time -- a device-level interpreter-registration drift since the build, not a code or dependency defect (Python
3.11, the only registered interpreter, carries the identical package set: pyyaml 6.0.3, jsonschema 4.26.0,
pytest 9.1.1). Per bound 14 ("a missing instrument is a refusal, never an install") and bound 9 ("a criterion
that cannot be satisfied as written is REFUSED and reported with its measurement"), no substitute interpreter
was used for the graded run. Filed: `NFRA_MCPINDEX-W1-S6` (BLOCKING, `disarm_owner` `2.0.0_SA_COO`).

**Graded verdict, every mechanical criterion, this re-run:** FAIL-by-output -- the named invocation never
printed a `VERDICT:` line (rc=103 instead). Denominator: 11 of 11 mechanical criteria (AC1-AC7, AC9-AC12).

**Informational only (NOT the graded instrument, py -3.11, same unmodified probe code, run to characterize the
code itself independent of the interpreter-registration gap):** AC1 PASS, AC2 PASS, AC3 PASS, AC4 PASS, AC5
PASS, AC6 PASS, AC7 PASS, AC9 PASS, AC10 PASS, AC12 PASS. AC11 (amended, two-limb form) still measures FAIL under
py -3.11: `DENOMINATOR 49 registered tool name(s)`; `fails destructive_ops.classify: 14 of 49` (the same 9
ycharts/opal_portal/globgrph + 5 schwab tools noted in the original AC11 measurement above -- their owning
integrations declare no per-tool manifest, since their `integration.py` files are outside this cell's `<paths>`,
unchanged by the amendment); `fails data_entitlement.classify: 0 of 49`. This is not new: AC6 measured the
identical 49-tool population byte-identical before/after this cell's edit, so these 14 tools were already
fail-closed through `destructive_ops.classify` before this cell touched anything -- the amendment removes only
the catalog axis, and the dop axis it kept still measures a real, pre-existing gap the 4 real integrations'
own directories (out of `<paths>`) would have to close.

## Summary

**As graded by this re-run's own named invocation (py -3.12, unavailable on this device, rc=103):**
FAIL-by-output: AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC9, AC10, AC11, AC12 (11 of 11 mechanical criteria --
none produced a `VERDICT:` line). Judgment, no verdict here: AC8.
Rows filed: `NFRA_MCPINDEX-W1-S5` (build-commit round, AC11 catalog-axis REFUSAL, since amended away) and
`NFRA_MCPINDEX-W1-S6` (this round, py -3.12 unavailable, BLOCKING).
Informational-only (py -3.11, not the graded instrument): 10 of 11 PASS, AC11 FAIL (measured gap unchanged by
the amendment -- see above). `<status>` is NOT flipped to `complete`: not every mechanical criterion passes by
its own named invocation.
