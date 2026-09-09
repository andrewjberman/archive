# CG-s-30 -- comp-aws DEPRECATED FOR AGENT USE AND PULLED OUT OF `comp-which` SELECTION, WITH NO GATE

**Worker:** `0.9.0_WK_NFRA_CLDGRPH~6` (spine-v3 L7 subagent of `2.0.0_SA_COO~A`)
**Order:** `NFRA_CLDGRPH.TO-CG-F-10` · **Cell:** CG-s-30 (decomposition v0.8) · **PRD:** v0.9 row S30
**Branch:** `wk-cldgrph-6-6` · **Worktree:** `C:/tmp/wk-cldgrph-6-6` · **Base HEAD:** `973a20aff9`
**Push state:** LOCAL -- never pushed, never merged, never rebased, not measured against a remote.

```json
{
  "andrews_words_this_implements": [
    "there should be no need for the laptop (or any other user) to be running manual refreshes",
    "effectively deprecate it and pull it off from being surfaced via comp-which. We do not need to gate it, merely need to pull it out of comp-which selection, that will be enough."
  ],

  "THE_PREAMBLE_VERBATIM": "comp-aws: DEPRECATED FOR AGENT USE since 2026-09-09 (Andrew-direct; recorded in org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20260909_191xZ_NO_LAPTOP_GRAPH_REFRESH_COMP_AWS_WRITE_PATHS_RETIRED.md).\n  The cloud graph is SERVED: read it with `comp-kuzu \"<Cypher>\"` -- manifest entry cloud.read.served_vintage, which states how old its answer is on every call.\n  It is REFRESHED estate-side by the nightly Fargate derive-runner (full reconcile) and by the incremental updater. There is no refresh for you to run and no question is ever the cause of a rebuild.\n  This CLI is NO LONGER ROUTED BY comp-which. It is NOT gated: nothing here refuses, and every subcommand's exit code is unchanged.\n  -- running <subcommand> as before.",

  "where_the_preamble_lives_and_who_prints_it": {
    "cli": "org/modules/graph/comp_aws_cli.py -- DEPRECATION_PREAMBLE + print_deprecation_preamble(cmd), called from main() BEFORE ap.parse_args(). Placing it before parse_args (not between parse_args and args.fn) is deliberate: argparse exits INSIDE parse_args for --help and for a usage error, so a hook after it would miss both. sys.argv[1:] is read only to NAME the subcommand in the last line; argparse still owns every parsing decision.",
    "wrapper": ".tools/comp-aws -- prints the same text, then `export COMP_AWS_PREAMBLE_PRINTED=1` before invoking the CLI.",
    "one_print_per_invocation": "THE WRAPPER PRINTS AND THE CLI HONOURS THE FLAG. Measured both ways: through the wrapper WRAPPER_PREAMBLE_COUNT=1; the CLI invoked directly (no wrapper, flag unset) DIRECT_CLI_PREAMBLE_COUNT=1. So the 1 is a suppression that works, not a CLI that never prints.",
    "channel": "STDERR ONLY. stdout is the subcommands' data channel (`metrics` and `contract-diff --json` emit JSON a consumer parses). A stderr preamble changes no stdout byte -- which is exactly how 'then behaves exactly as before' is measured.",
    "help_case": "--help CARRIES THE PREAMBLE, MEASURED BOTH WAYS: `bash .tools/comp-aws --help` prints the notice on stderr and argparse's usage on stdout, rc=0; `python comp_aws_cli.py --help` prints it too (the CLI-side hook fires because the flag is unset). This is why the hook sits BEFORE parse_args() -- argparse exits INSIDE parse_args for --help, so a hook placed between parse_args and args.fn would miss it entirely."
  },

  "no_gate_anywhere": "No refusal, no sys.exit, no rc change, no branch on the subcommand name. print_deprecation_preamble returns a bool nobody acts on. The three write subcommands (derive, snapshot, the versioned-store commit) are byte-unchanged and callable by name. NONE of them was run during this order -- the preamble was exercised on classes, dual-managed and metrics --graph <fixture> only, and the fixture is two synthetic nodes in this deliverables folder, not a census.",

  "before_and_after_rank_counts_per_phrasing": {
    "instrument": "the SPILLED RANK FILE .comp-graph/which/rank-<pid>.yaml, never page 1 of stdout -- the terminal shows 3 of ~79, so a stdout read would certify nothing. Same instrument before and after.",
    "What AWS resources exist + how are they typed/connected?": {"before": "1 comp-aws row at rank 4 of 79", "after": "0 comp-aws rows of 78"},
    "What's the drift / blast radius / unmanaged surface?":      {"before": "1 comp-aws row at rank 42 of 79", "after": "0 comp-aws rows of 78"},
    "Is any resource dual-managed across TF states?":            {"before": "1 comp-aws row at rank 23 of 79", "after": "0 comp-aws rows of 78"},
    "Cloud-shape snapshot + diff over time":                     {"before": "1 comp-aws row at RANK 1 of 79", "after": "0 comp-aws rows of 78"},
    "CONTROL -- list all s3 buckets":                            {"before": "rank 1 = comp-kuzu (comp-aws at rank 17)", "after": "rank 1 = comp-kuzu"},
    "tools_ranked": "79 before, 78 after, in every list -- exactly one tool left the pool and the pool did not otherwise move."
  },

  "stdout_sha256_equality_and_rc_per_read_only_subcommand": {
    "baseline_captured": "BEFORE any edit, by f10_before.py -> f10_baseline.json, through the same wrapper.",
    "comp-aws classes":              {"rc_before": 0, "rc_after": 0, "stdout_sha256": "c55fa1b400bb34305a4e694610dcddc0ccc3544a19c237b4bc45e90b7fb86e93", "equal": true},
    "comp-aws dual-managed":         {"rc_before": 0, "rc_after": 0, "stdout_sha256": "13ffd2bbba32058c88aa023cd709683896a2b77271f4398eeb8e62988579b59b", "equal": true},
    "comp-aws metrics --graph FIX":  {"rc_before": 0, "rc_after": 0, "stdout_sha256": "f23d37cfd2a8b1729841570738a45c5c37968285e8f178de6e7a2139f3c9151f", "equal": true},
    "the_baseline_discriminates": "3 DISTINCT stdout sha256 across the 3 subcommands. This is not decoration: the FIRST baseline run recorded three IDENTICAL 504-byte hashes with rc=1, because a python-spawned bare `bash` Windows-resolves to the System32 WSL stub. Had that baseline been kept, STDOUT_UNCHANGED would have compared three copies of a stub's error message and passed. f10_lib.git_bash() now resolves the absolute Git-for-Windows bash and REFUSES to fall back."
  },

  "regeneration_numbers": {
    "carriers": 3,
    "regen_commands_MEASURED": 2,
    "why_2_not_3": "each carrier was asked which generator it DECLARES in its own header; .tools/gen_tool_registry.py writes BOTH org/modules/graph/TOOL_MASTER.yaml and .tools/tool_index.py in ONE invocation. The count is measured, not padded to the carrier count (F-8's W4-S2 finding, reused).",
    "population_parity": "99 of 99 -- a deprecated tool STAYS in the population. Membership is unchanged; only routing and description moved.",
    "SECOND_REGEN_DIFF_LINES": 0,
    "HAND_EDITED_CARRIERS": "0 of 3",
    "lf_normalised": "every comparison is on LF-normalised bytes -- this is an autocrlf checkout where a byte-identical tool_index.py reads MODIFIED against HEAD.",
    "master_row": "TOOL_MASTER.yaml tools['comp-aws'].status == 'deprecated'; .tools/tool_index.py TOOLS['comp-aws']['status'] == 'deprecated'; LEDGER_DOC (the embedded map) carries the same, and surfaces[AWS-CLOUD].high_level_tool == 'comp-kuzu'."
  },

  "phrase_census_by_domain": {
    "domain_DECLARED_by_the_issuer": ["-> .comp-graph", "snapshot tarballs -> opal-<acct>-globgrph", "--commit-to-nessie", "iceberg-commit", "writes the derive", "run comp-aws derive", "full derive"],
    "files": ["org/modules/graph/comp-tools.yaml", "org/modules/graph/comp-aws-agent-usage.yaml"],
    "before_scoped": {"-> .comp-graph": 1, "snapshot tarballs -> opal-<acct>-globgrph": 1, "full derive": 1, "others": 0, "total": 3},
    "before_unscoped": {"total": 4},
    "after_scoped": {"total": 0},
    "after_unscoped": {"total": 0},
    "COMP_AWS_KEYS_IN_COMP_TOOLS": 1,
    "YAML_LOADS": "2 of 2",
    "PHRASE_PROBE_CONTROL": "FIRED -- a laptop-producer `output:` line appended to an in-memory copy of each file is caught in 2 of 2."
  },

  "criterion_results": {
    "F10-AC1": "PASS-by-output -- PREAMBLE_FIRST=3 of 3 subcommands; PREAMBLE_NAMES=served-graph,comp-kuzu,cloud.read.served_vintage,nightly-derive-runner,incremental-updater,comp-which,andrew-2026-09-09; STDOUT_UNCHANGED=3 of 3; RC_UNCHANGED=3 of 3; WRAPPER_PREAMBLE_COUNT=1",
    "F10-AC2": "PASS-by-output -- COMP_AWS_ROWS=0 of 4 phrasings; RANKED_LISTS_READ=4 of 4; CONTROL_PHRASING_ROUTES_TO=comp-kuzu; CURATED_TUPLES_NAMING_COMP_AWS=0 of 90",
    "F10-AC3": "PASS-by-output -- MAP_STATUS_FIELD=deprecated (declared in schema); MASTER_ROW_STATUS=deprecated; PARITY=99 of 99; SECOND_REGEN_DIFF_LINES=0; HAND_EDITED_CARRIERS=0 of 3",
    "F10-AC4": "PASS-by-output -- PHRASE_DOMAIN=7 phrases; LAPTOP_PRODUCER_PHRASINGS=0 of 7; COMP_AWS_KEYS_IN_COMP_TOOLS=1; YAML_LOADS=2 of 2; PHRASE_PROBE_CONTROL=FIRED",
    "F10-AC5": "PASS-by-output -- CMD_DERIVE_BYTES_UNCHANGED=true; HANDLERS_UNCHANGED=3 of 3; DERIVE_RUNNER_CALLSITE=infra/aws/globgrph/derive_runner.py:101",
    "F10-AC6": "RECORDED (judgment=true) -- UNVERIFIABLE-BY-INSTRUMENT, graded by 3.0.0_SA_CVO at L9. The reading is below."
  },

  "F10-AC6_the_reading_no_verdict": {
    "what_stops_a_seat_running_snapshot_tomorrow": "THREE THINGS, AND NOTHING ELSE, BY ANDREW'S WORD. (1) A PREAMBLE IT READS -- but only if it reads stderr, and only if it already decided to type the command. This control acts AFTER the decision, not before it. (2) AN ABSENT ROUTE -- the strongest of the three, because comp-which is where a seat's cloud question actually STARTS. comp-aws is now absent from 78-of-79 ranked lists, absent from every curated tuple, and absent from the AWS-CLOUD surface drill-down; a seat that asks rather than remembers will never be handed the name. (3) A REGISTRY THAT SAYS SO -- comp-tools.yaml and comp-aws-agent-usage.yaml now lead with the deprecation and describe derive/snapshot/the versioned-store commit as estate paths. What is NOT here: no refusal, no rc change, no allowlist, no env guard, no confirmation prompt. A seat with the name in its context window -- from an older transcript, a doc outside these two files, or its own memory -- runs it exactly as before and succeeds. That is not a defect of the implementation; it is the specification. The residual risk is therefore a MEMORY risk, not a CAPABILITY one, and the honest statement of it is: this order removes comp-aws from the surfaces a seat CONSULTS, and does nothing about the surfaces a seat CARRIES.",
    "what_the_nightlys_next_SUCCEEDED_derive_proves": "It proves the ENGINE is intact ACROSS THE SEAM THIS ORDER TOUCHED -- and it is a strong proof precisely because the derive-runner does NOT go through the CLI. It calls comp_aws_cli.cmd_derive IN-PROCESS at infra/aws/globgrph/derive_runner.py:101, so it never executes main(), never sees the preamble, and never reads argparse. The three engine functions are byte-identical to the hand-off commit (measured by ast-sliced git show, with main() as the positive control returning UNEQUAL), so the nightly's success is EXPECTED rather than informative about the diff. What it DOES discriminate is the class of failure this order could plausibly have caused and did not: an import-time break in comp_aws_cli.py. The new module-level DEPRECATION_PREAMBLE constant and function execute at import, in the runner's process, before cmd_derive is reached -- a syntax error, a NameError (one WAS hit and fixed here: this module has no module-level `import os`), or an unguarded stderr write would take the nightly down at import. A SUCCEEDED derive with its tarball published is therefore a genuine control on the import path, and the CVO reading it the morning after is reading the right thing. What it does NOT prove: anything about the read-only subcommands, the routing change, or the registry text -- none of which the nightly exercises.",
    "FWD_2_no_question_is_ever_the_cause_of_a_rebuild": "READS DIFFERENTLY, AND MORE STRONGLY, BUT NOT COMPLETELY. Before this order the sentence was true of the SERVED READ (comp-kuzu has no refresh) and false of the ROUTER: a seat asking 'what's the drift / blast radius' was handed comp-aws at rank 42, and asking 'cloud-shape snapshot + diff over time' was handed it at RANK 1 -- the single strongest routing signal the fabric emits, pointing at a subcommand whose whole job is to rebuild. That path is now gone in 4 of 4 measured phrasings. What remains between FWD-2 and 'realized' is not a route but a HABIT: the capability is unchanged by design, so the claim can only ever be that no question ROUTES to a rebuild, never that no question CAUSES one. L10 should read FWD-2 at that grain and say which it means.",
    "FWD_6_no_refresh_choice_on_the_client": "READS DIFFERENTLY IN KIND. FWD-6 was previously satisfiable only by describing a choice a seat SHOULD NOT make; the choice was present in the router, in the registry text, and in the surface's own high_level_tool. After this order the AWS-CLOUD surface's high_level_tool IS the served read (comp-kuzu), the map's refresh_mechanism states the estate-side cadence in words that name no laptop, and both registry files carry a `who_refreshes: the estate ... Not you` fact. The client-side refresh choice is no longer PRESENTED anywhere this order can reach. It is still EXECUTABLE, and the two are different claims -- L10 should not let the first stand in for the second.",
    "one_thing_the_CVO_should_weigh_against_this_order": "The deprecated-skip is implemented in .tools/comp-which, reading `status:` out of the ledger. It is therefore a ROUTER-side exclusion, not a POPULATION-side one, and a SECOND router (or a consumer of TOOL_MASTER/tool_index that ranks on its own) would not inherit it automatically. The status field IS carried on every generated row precisely so a second consumer CAN honour it, but only comp-which does today. That is a deliberate scope, not an oversight -- widening it would have meant editing comp_capability_provider.py, which is outside this order's <paths>."
  },

  "what_this_order_did_NOT_do": [
    "did not gate, refuse, or change an exit code anywhere",
    "did not edit cmd_derive, cmd_snapshot or cmd_iceberg_commit (byte-identical, measured)",
    "did not run derive, snapshot or iceberg-commit against anything",
    "did not change the population authority's MEMBERSHIP -- comp-aws stays homed, parity 99 = 99",
    "did not hand-edit a generated carrier -- all three regenerated, HAND_EDITED_CARRIERS=0 of 3",
    "did not touch graph-call-manifest.yaml",
    "did not repair .tools/tool_overrides.yaml (out of grant -- row NFRA_CLDGRPH-W6-S1)"
  ]
}
```

## The three surfaces the route left by, and why all three were needed

`comp-which` reaches a tool by three independent paths, and closing two of them would have left a
measurement that read clean while the route survived.

1. **The curated vocabulary tuples** (`.tools/comp-which:288` and `:373`). The router "ranks TOOLS
   off THIS curated vocabulary, and never reads tools_index" -- the file says so at `:293`. Both
   tuples now call the served surface (`comp-kuzu`, `comp-find --corpus aws`); `comp-iam` and
   `comp-estate` keep their places. The description string at `:1190` that named
   "comp-aws classes/derive is the live census" was rewritten in place. **0 of 90 tuples name
   comp-aws** where 2 did before, and 0 non-comment code lines do where 3 did.
2. **The ledger's `high_level_tool`** (`comp-coverage-map.yaml:397`, read by `_surface_index`).
   The AWS-CLOUD surface's high-level tool is now `comp-kuzu` -- which is simply true: the served
   read is the surface's agent-facing entry and comp-aws is the engine beneath it.
3. **The scored posterior**, which walks the map's `tools[]` through
   `comp_capability_provider._build_capabilities` and would have surfaced comp-aws by concern-token
   overlap regardless of 1 and 2. This is what the `status: deprecated` field closes: the router
   filters the WHOLE ranking (not the printed top-3) before it spills the rank file, so the
   measurement surface carries no deprecated row either. Filtering only the terminal menu would
   have left the tool one `open` away and made "0 rows" a claim about page 1.

The surface drill-down (`_surface_index`) skips a deprecated tool for the same reason.

## What the field is, and what it deliberately is not

`status` is declared in the map's own `schema.node_fields` with `values: [active, deprecated,
retired]` and `default: active`, mirroring `graph-call-manifest.yaml`'s per-entry `status: retired`
but at TOOL grain rather than route grain. The doc block states what one remedy does **not** move
(TAXONOMY LAW iv): un-deprecating is a one-line edit plus a regeneration, and it does **not**
restore curated vocabulary tuples repointed elsewhere, nor re-describe the tool in
`comp-tools.yaml`. Those are separate acts on separate files.

`deprecated` is explicitly a **routing and description state, not an execution state**. It changes
what a seat is OFFERED; it changes nothing about what a seat can RUN. `retired` is left declared
but unenforced by this field on purpose -- a retirement is a MEMBERSHIP act on the map, and this
order was forbidden from touching membership.

The field has a CONSUMER on both sides, which is the whole mechanism: `gen_tool_registry.py`
projects it onto every generated master and index row (so the value cannot drift to unpopulated),
and `.tools/comp-which` rejects on it.

## Two things worth the next reader's attention

**The baseline nearly certified a stub.** The first `f10_before.py` run recorded `rc=1` and
`504 bytes` of identical stdout for all three subcommands. That is the System32 WSL stub: a
python-spawned bare `bash` Windows-resolves to it, and it returns UTF-16LE on stdout. Had that
baseline been kept, `STDOUT_UNCHANGED=3 of 3` would have compared three copies of an error message
and passed cleanly. The tell was the *identical* hashes, not the rc -- which is why
`BASELINE_DISCRIMINATES` is printed beside the criterion: three distinct hashes are what make the
equality a measurement. `f10_lib.git_bash()` resolves the absolute Git-for-Windows binary through
`.tools/git_bash_resolver.py` and raises rather than falling back.

**My own rewrite re-armed the phrase census.** After rewriting both registry files, `F10-AC4` read
`LAPTOP_PRODUCER_PHRASINGS=1 of 7`: the new text SPELLED one of the declared phrases while saying
it was not for agent use. A tombstone that repeats a literal keeps it in every future census
(E-1's W2-S38 convention). The three sites now CITE the subcommand instead of spelling it, and the
scoped and unscoped reads both go to 0. The failure was caught because the probe was written before
the criterion was claimed, not after.

## One finding filed and not fixed

`NFRA_CLDGRPH-W6-S1` (OBSERVATION / ARMED, owner `2.0.0_SA_COO~A`): the map's `concern` reword does
NOT reach `TOOL_MASTER.yaml` or `tool_index.py`. `gen_tool_registry.main()` sources a tool's
`concern` **and** `canonical_call` from `.tools/tool_overrides.yaml` -- bootstrapped from the map
once, when the overrides file was absent, and frozen since. Both generated carriers therefore still
carry `canonical_call: "comp-aws derive --out <path>"`, an agent-facing string describing exactly
the act this order deprecates. `tool_overrides.yaml` is not in this order's `<paths>`, so the repair
is out of grant and was not attempted. Note the shape: `comp_capability_provider` reads the map
DIRECTLY, so the ROUTER shows the new concern -- a check scoped to comp-which cannot see this at
all.

## TERMINAL STATUS: OPEN -- BLOCKING, row NFRA_CLDGRPH-W6-S2

**The work is done and measured; it cannot be committed.** `bash .tools/safe-commit.sh` on the ten
source and carrier paths is REFUSED by a pre-existing mechanical gate:

```
BLOCKED: 1 catalogued tool(s) do NOT surface for their own use_case:
  - comp-aws               comp-which returns nothing naming it
  A tool the mandated router cannot return is undiscoverable, however well it is
  catalogued. FIX: give it distinctive curated vocabulary in .tools/comp-which, and do
  NOT let its catalog text name a sibling tool -- a description is routing input, and
  naming a sibling hands it your intent. Then: python .tools/comp-which-routing-test.py
BLOCKED: comp-manifest-check completeness family (registered-implies-reachable / one-map-home / self-routes)
```

`comp-which returns nothing naming it` **is the deliverable.** The gate is measuring the world
correctly and reading the intent backwards: it enforces registered-implies-reachable over
`graph-call-manifest.yaml`'s `tools_index`, where comp-aws is registered (78 entries, **0** of which
carry any `status` key), and it fires on any commit touching
`manifest_check_cli._SELFROUTE_CORPUS` -- `comp-coverage-map.yaml`,
`comp_capability_provider.py`, `.tools/comp-which`. This order necessarily edits two of those
three, so **no commit carrying its substance can pass**.

**Both remedies are outside `<paths>`.** The manifest is forbidden by the order's own NEVER clause
("a `status: retired` entry is R14's, not yours; if a manifest entry names comp-aws as a route,
that is a ROW"), and the invariant's exclusion set is a hardcoded literal at
`.tools/comp-which-routing-test.py:273` -- `EXCLUDE = {"comp-grep", "comp-glob", "comp-which"}` --
in a file this order does not grant.

**The one in-grant workaround was refused.** The gate's own message says: give comp-aws distinctive
curated vocabulary in `.tools/comp-which`. That is inside the grant and would land the commit. It
also restores exactly the comp-which surfacing Andrew ordered removed, so taking it would be the
order widening itself to satisfy a gate. `--force` is not a route either: the gate's text says so.

There IS a design that satisfies both -- the **prohibition tuple** already in this file (the
`pipescript` tuple, whose comment reads "Never delete the phrasings: an agent asking 'pipescript'
must be TOLD it is retired, not dropped into a no-match"). A comp-aws prohibition tuple would make
the tool self-route to a message that says *do not run this, read comp-kuzu instead*, satisfying the
gate and arguably serving Andrew's intent better than silence. But it changes what `F10-AC2`
measures -- "0 comp-aws rows in 4 of 4 ranked lists" would need re-cutting against a tuple that
deliberately returns one. That is the issuer's call, not the worker's, and it is stated in row
W6-S2 rather than taken.

**What landed and what did not.** The deliverables folder (this record, the before-census, the
baseline, the fixture, the five probes and the shared instrument) and the two channel rows ARE
committed -- none of those paths is in the self-route corpus. The ten source and carrier edits are
**UNCOMMITTED IN THE WORKTREE** `C:/tmp/wk-cldgrph-6-6` on branch `wk-cldgrph-6-6`:
`org/modules/graph/comp_aws_cli.py`, `.tools/comp-aws`, `org/modules/graph/comp-coverage-map.yaml`,
`.tools/gen_tool_registry.py`, `.tools/comp-which`, `org/modules/graph/comp-tools.yaml`,
`org/modules/graph/comp-aws-agent-usage.yaml`, `org/modules/graph/TOOL_MASTER.yaml`,
`.tools/tool_index.py` (`.tools/TOOL_CLASSIFICATION.yaml` regenerated byte-identical, so it does not
appear in `git status`). Every criterion output recorded above was measured against those worktree
bytes, and the record says so rather than implying a landed state.

**The task order's `<status>` is NOT flipped.** All five mechanical criteria read PASS by output;
a VALID instance is not a met order, and neither is a measured criterion on an uncommitted tree.
