# CG-s-28 -- THE LAST TWO DESCRIPTIONS OF THE DEAD ENGINE, AND THE NORMALISER (TO-CG-F-8, round 6)

**Worker:** `0.9.0_WK_NFRA_CLDGRPH~4`, a spine-v3 L7 subagent of `2.0.0_SA_COO~A`, branch
`wk-cldgrph-6-4`, worktree `C:/tmp/wk-cldgrph-6-4`, base HEAD `c6b16d8f04`. **PUSH STATE: LOCAL** --
never pushed, never merged, never rebased, not measured against a remote and not claimed.

**PASS 2, ON THE ISSUER AMENDMENT @`c722bf8bdc` (2026-09-09 18:5xZ). THE ORDER IS COMPLETE.** All
four mechanical criteria PASS by output at the amended cut; `F8-AC5` is recorded and never
self-graded. What changed is in the section *PASS 2* below -- the pass-1 paragraph is kept UNEDITED
beneath it, because the reasoning that left the order open is the reasoning the amendment acted on,
and deleting it would leave the amendment unexplained.

**PASS 1 LEFT THE ORDER OPEN, AND THAT IS WHAT THE AMENDMENT ANSWERED.** Three source edits landed
and both substantive criteria PASSED by output (`F8-AC1`, `F8-AC2`). `F8-AC3` and `F8-AC4` FAILED,
and neither failure was in the work: each named an instrument the world does not carry -- a
`REGEN_COMMANDS=3` against a tree with two generator scripts, and a `--check` flag on a script with
no argv parsing at all. Both were rows (`NFRA_CLDGRPH-W4-S2`, `NFRA_CLDGRPH-W4-S3`), both carried
the measured substance beside the failure, and neither was papered over by choosing a denominator
that fits. **THE `F8-AC3` PROBE IS BYTE-UNCHANGED BETWEEN THE TWO PASSES**: what changed is the
expect the issuer cut, not the number the probe measured -- `REGEN_COMMANDS=2` is the same 2 it
printed when the criterion read FAIL.

## PASS 2 -- what the amendment ordered, and what it measured

```json
{
  "amendment": "org/missions/D0/NFRA/NFRA_CLDGRPH/task-orders/NFRA_CLDGRPH.TO-CG-F-8.dead-engine-descriptions-and-normaliser.md, section 'ISSUER AMENDMENT 2026-09-09 18:5xZ' @c722bf8bdc, standing authority @9f4a57262f",

  "1_the_two_recut_criteria": {
    "F8-AC3": "expect was 'REGEN_COMMANDS=3', now 'REGEN_CARRIERS=3 ... REGEN_COMMANDS=[1-9] ... SECOND_REGEN_DIFF_LINES=0 ... HAND_EDITED_CARRIERS=0 of 3'. RE-RUN at this HEAD, not re-quoted: REGEN_CARRIERS=3, REGEN_COMMANDS=2, SECOND_REGEN_DIFF_LINES=0, HAND_EDITED_CARRIERS=0 of 3, HAND_EDIT_CONTROL=FIRED, rc 0. MATCHES.",
    "F8-AC4": "invocation was 'python .tools/gen_tool_registry.py --check', now 'timeout 120 python .tools/gen_tool_registry.py' with expect on the two WROTE lines. RE-RUN at this HEAD: both WROTE lines, rc 0 -- and REACHING them IS the parity pass, because assert_population_parity() at :138 is called at :219 and is raise-only. MATCHES. The two controls stand from pass 1 and were re-exercised this pass: positive assert_population_parity(pop,pop) -> 99; negative assert_population_parity({'a'},{'b'}) -> PopulationDivergence FIRED."
  },

  "2_the_widened_grant_one_file_one_string": {
    "edited": "org/modules/graph/graph-call-manifest.yaml:1500 -- the freshness: field of entry cloud.cluster.page_panel_drilldown, and NOTHING else in the file (git diff --numstat reads 1 1 on one file: one line changed).",
    "before": "live canonical Nessie->Kuzu graph (NFRA_TSGRAPH P2-1 extractor emit, P2-2 materialized); prints the comp-kuzu provenance header to stderr (current/BEHIND/UNKNOWN VINTAGE); auto-refreshes on HEAD-advance; Rule 20 QUERY-default -- never rebuilds",
    "after": "the SERVED graph projection, cluster layer included (NFRA_TSGRAPH P2-1 extractor emit, P2-2 materialized; served since NFRA_CLDGRPH CG-s-8). Every call ends with a VINTAGE line on stderr stating in plain words how old the answer is. There is NO agent-runnable refresh and no HEAD-advance trigger: the projection is advanced by the marker-driven cloud worker (NFRA_CLDGRPH CG-s-2/3) on the estate's own schedule, never by a call. Rule 20 QUERY-default -- never rebuilds. See cloud.read.served_vintage.",
    "house_style_not_invented": "the wording follows the entry's own siblings rather than a new form -- cloud.lookup.nodes_by_type:156 already reads 'the SERVED projection; every call ends with a VINTAGE line ... There is NO agent-runnable refresh and no database path'. 'never rebuilds' stays, as the amendment directs, and the successor pointer cloud.read.served_vintage is added because that is where E-1 put freshness for this graph.",
    "CRLF_TRAP_HIT_AND_HANDLED": "graph-call-manifest.yaml is CRLF in this worktree (1899 CRLF of 1899 LF). A text-mode read-modify-write matched ZERO on the anchor and, if forced through, would have rewritten every line ending in the file -- a one-string grant turned into a 1899-line diff. The edit was done on BYTES with an assertion that the CRLF count is identical before and after. That is why the diff is one line.",
    "manifest_invariants_after_the_edit": {
      "manifest_check_cli selfcheck": "PASS: 3 finding(s) (B + C present, 2 ERROR-class), 0 false-positive -- and its own output prints this order's reworded raw_cypher note VERBATIM, which is an independent exercise of edit 3 through the checker's own fixture",
      "manifest_check_cli completeness": "PASS: routable + placement + self-routes + existence, over 78 registered tool(s).",
      "manifest_check_cli retired-alias": "retired-alias invariant PASS: 9 retired name(s) declared, all disjoint from live+excluded (99 live), successors valid; none cited across the 129 routing surface(s) in scope (1 tombstoned mention(s) exempted). / PASS: retired-alias.",
      "comp-coverage-check": "PASS: comp-coverage-map.yaml is internally consistent -- every tool one home, every overlap declared, no phantom seam, inventory complete, projection current, grain stable. swept: 99 homed tool(s) (35 tools[] + 64 meta_tools[]) | 12 gate_contract rule(s), 0 unverifiable",
      "yaml_parse": "128 entries parse; the entry's status, tool, canonical_call, cost, rebuild_trigger and anti_pattern are byte-unchanged"
    },
    "F8-AC1_after": "GENERATOR_SOURCED_HITS=0 of 0 hits ; CHECKER_HITS=0 ; MANIFEST_SOURCED_HITS=0 (NONE) ; OTHER_SOURCED_HITS=0 ; PHRASE_PROBE_CONTROL=FIRED. The last hit in the compiled index is gone AT ITS SOURCE, not at the carrier -- which is the only place it could be fixed, since tool_index.py reproduces the manifest verbatim as MANIFEST_DOC.",
    "index_bytes": "543627 -> 543977 after regeneration; master sha256 3d2deb234dc29a28 unchanged, because the manifest is embedded in the INDEX and not in the master"
  },

  "3_the_scoped_census_across_the_two_passes": "python .tools/comp-find 'auto-refresh on HEAD-advance|auto-refreshes on HEAD-advance|canonical persisted Kuzu DB' .tools org/modules/graph --all: 21 hit(s) / 799 file(s) at the cut -> 7 / 799 after pass 1 -> 5 / 800 after pass 2. The remaining 5 are exactly W4-S4's out-of-grant set less the manifest entry, carried NAMED to L10 by the amendment (S74): comp_ws4_crosswalk.py:14, comp_debt/grounding_lib.py:205, comp_legacywriter.py:237, estate-coverage-resolver.json:1356, estate_census/pass1_inventory.json:1858.",

  "4_the_new_row": "NFRA_CLDGRPH-W4-S6 -- the amendment opened ONE STRING and the entry it opened carries THREE substrate descriptions. cost: (:1498, 'reads the materialized cluster layer off the canonical Kuzu graph') and rebuild_trigger: (:1501, 'queries the live graph; the cluster layer re-derives with the graph refresh') were NOT touched, are outside the one-string grant, and -- the part worth carrying -- match NONE of the three censused phrases, so the entry can read 0 hits while still describing a dead engine in two fields. The same row carries the count correction W4-S4 cannot take in place (six out-of-grant residues became five).",

  "5_rows_at_the_close": {
    "W4-S1": "DISARMED by the amendment's grant widening (issuer ack S73 on CLOUD, not in this worktree's index) -- the string is fixed at source and F8-AC1 reads MANIFEST_SOURCED_HITS=0 (NONE)",
    "W4-S2": "DISARMED by the F8-AC3 re-cut (issuer ack S72) -- the probe is byte-unchanged and still prints REGEN_COMMANDS=2",
    "W4-S3": "DISARMED by the F8-AC4 re-cut (issuer ack S72) -- the generator itself is now the named instrument",
    "W4-S4": "CARRIED NAMED to L10 by the amendment (S74); five members remain, per W4-S6",
    "W4-S5": "INERT, no disarm owed -- the population-counter side effect, recorded so a repair is not read as a regression",
    "W4-S6": "NEW this pass, OBSERVATION / ARMED to 2.0.0_SA_COO~A"
  },

  "6_what_this_pass_did_NOT_do": "no row was edited (W4-S1..W4-S5 stand as written, including W4-S4's six); no disarm was self-recorded (the acks are the issuer's and live on CLOUD); no manifest entry other than the one named was touched; no generated carrier was hand-edited; infra/system/ is still untouched and the comp-system phase-two discharge is still the drain's."
}
```

```json
{
  "to_id": "NFRA_CLDGRPH.TO-CG-F-8",
  "cell": "CG-s-28",
  "terminal_status": "COMPLETE at PASS 2 on the issuer amendment @c722bf8bdc -- F8-AC1..F8-AC4 all PASS-by-output at the amended cut, F8-AC5 recorded and never self-graded. EVERYTHING BELOW THIS FIELD IN THIS BLOCK IS THE PASS-1 RECORD AND IS LEFT AS WRITTEN: it was true when written, the amendment acted on it, and the PASS 2 section above carries the deltas. Read the two together, not one instead of the other. PASS 1 read: OPEN -- F8-AC3 and F8-AC4 FAIL against their literal expects; F8-AC1 and F8-AC2 PASS-by-output.",

  "the_three_edits_by_line_at_this_HEAD": [
    {
      "file": ".tools/gen_tool_registry.py",
      "lines": "36 (new SUFFIXES_STRIPPED constant), 109-133 (def norm_tool)",
      "before": "n = name.strip(); return n[:-3] if n.endswith('.py') else n",
      "after": "SUFFIXES_STRIPPED = ('.py', '.sh') at module scope beside MASTER/INDEX; norm_tool iterates it and returns n[:-len(suffix)] on the first match, else n",
      "why": "W2-S37: stripping .py alone made comp-v5-composite-test.sh read as a FIFTH exclusion beside four real retirements -- one tool spelled two ways, not a missing tool. The docstring now carries the CENSUS, not an assumption, so the next suffix is a re-census rather than a silent pass-through.",
      "call_sites_censused": "3, all in these two generators: gen_tool_registry.py:105 (population_from_map), :165 (the master key), and gen_tool_classification.py:61 which returns reg.norm_tool as NORM. comp-find 'norm_tool' over the repo: 20 hits / 29102 files, 1 DEF + 4 SURFACED (those three plus the docstring line) + 15 records/docs."
    },
    {
      "file": ".tools/gen_tool_classification.py",
      "lines": "132-141 (the tombstone comment), 142-146 (REFRESH['GRAPH-DB'])",
      "before": "'refresh_mechanism': 'auto-refresh on HEAD-advance; provenance header printed per call', 'refresh_is_incremental': True",
      "after": "'refresh_mechanism': 'served projection; refreshed by the marker-driven cloud worker (NFRA_CLDGRPH CG-s-2/3), never by a call; provenance header (VINTAGE) printed per call', 'refresh_is_incremental': True",
      "why": "The string described the LOCAL Kuzu projection retired at CG-s-8 (@173a1d8c90). Nothing refreshes on a HEAD-advance any more and no CALL refreshes anything: the served projection is refreshed by the marker-driven cloud worker and every seat READS it through the thin client.",
      "why_refresh_is_incremental_stays_True": "MEASURED against what the worker actually does, not carried forward: infra/aws/globgrph/kuzu_incremental_refresh.py is incremental-first with a FULL-RELOAD FALLBACK on a large delta (:53-56, FALLBACK_MIN_ABS=4000 / FALLBACK_FRACTION=0.25, both env-tunable; the docstring at :21-22 states the fallback is for delta ~= the whole table). Incremental is the mechanism; the full reload is the exception. True stands.",
      "tombstone_convention": "the comment CITES the retired phrase instead of repeating it (E-1's W2-S38 convention), which is why the repo census of the phrase drops to 7 rather than 8: a tombstone that carries the literal is one more hit for the next seat to triage.",
      "fan_out_measured": "6 of 99 tools in org/modules/graph/TOOL_MASTER.yaml now carry the new refresh_mechanism (comp-axes, comp-canon-motif, comp-fedobs, and three more -- the GRAPH-DB class), matching the 6 CONFIG hits the old string had in each carrier."
    },
    {
      "file": "org/modules/graph/manifest_check_cli.py",
      "lines": "207-215 (the raw_cypher finding's note)",
      "before": "\"embeds raw Cypher outside comp-kuzu. Route graph queries through comp-kuzu so they hit the canonical persisted Kuzu DB (manifest cloud.* / xlayer.*).\"",
      "after": "\"embeds raw Cypher outside comp-kuzu. Route graph queries through comp-kuzu so they hit the SERVED graph projection through the thin client (manifest cloud.lookup.nodes_by_type / cloud.read.served_vintage / xlayer.fullstack.firm_component_to_bucket); the local persisted Kuzu DB is RETIRED (NFRA_CLDGRPH CG-s-8).\"",
      "manifest_ids_verified_at_this_HEAD": "the three named ids are REAL, read out of the manifest and not composed: comp-read --enumerate 'id: (cloud|xlayer)\\.[a-z_.]+' returns 38 entry ids -- cloud.lookup.nodes_by_type:147, cloud.read.served_vintage:232, xlayer.fullstack.firm_component_to_bucket:1227. cloud.read.served_vintage is E-1's successor for both retired refresh entries (superseded_by at :263 and :280). The old note's 'cloud.*' glob also matched cloud.refresh.full / cloud.refresh.incremental, the two entries CG-s-17 RETIRED, which is why the glob was replaced with named live ids."
    }
  ],

  "the_suffix_census_the_order_asked_for": {
    "instrument": "python over both population sides, regex (\\.[A-Za-z0-9]+)$ on every tool name -- a suffix set is a DECLARED DOMAIN, so both sides are enumerated before the stripped set is chosen",
    "authority": "org/modules/graph/comp-coverage-map.yaml (tools[] + meta_tools[]) -- 99 names, suffixes present: {'(none)': 99}. The AUTHORITY CARRIES NO SUFFIX AT ALL.",
    "profile": "org/tier1_exec/3.0.0_SA_CVO/deliverables/tool_profile.json -- 93 names, suffixes present: {'(none)': 86, '.py': 6, '.sh': 1}. The seven: comp-deadgrant.py, comp-denytest.py, comp-firmsep-sweep.py, comp-tagauthz.py, comp-v5-composite-test.sh, comp-which-routing-test.py, comp-whoread.py",
    "cmd_ps1_asked_about_explicitly": "ABSENT. No .cmd, no .ps1, no other suffix on either side -- the order asked whether shim suffixes appear in the map and the measured answer is no.",
    "stripped": "('.py', '.sh') -- SUFFIX_DOMAIN_MECE=true, unstripped=none",
    "control": "NORM_CONTROL=FIRED -- norm_tool('comp-v5-composite-test.sh')=='comp-v5-composite-test', norm_tool('comp-whoread.py')=='comp-whoread', norm_tool('comp-find')=='comp-find' (the no-suffix name must survive unchanged)"
  },

  "EXCLUDED_NOT_IN_AUTHORITY_before_and_after": {
    "before": "EXCLUDED_NOT_IN_AUTHORITY=5 of 93: comp-adapter-audit, comp-kuzu-full, comp-kuzu-inc, comp-surface-check, comp-v5-composite-test.sh | of those, DECLARED RETIRED ALIASES (expected)=4 of 5 | NOT DECLARED RETIRED -- A FINDING, NOT AN EXCLUSION=1 of 5: comp-v5-composite-test.sh | AUTHORITY_WITHOUT_A_PROFILE_ROW=16 of 99 | classified 85 / unclassified 3",
    "after": "EXCLUDED_NOT_IN_AUTHORITY=4 of 93: comp-adapter-audit, comp-kuzu-full, comp-kuzu-inc, comp-surface-check | of those, DECLARED RETIRED ALIASES (expected)=4 of 4 | NOT DECLARED RETIRED -- A FINDING, NOT AN EXCLUSION=0 of 4: none | AUTHORITY_WITHOUT_A_PROFILE_ROW=15 of 99 | classified 85 / unclassified 4",
    "re_derived_independently": "f8_excluded.sh does NOT parse the generator's prose for the verdict: it re-computes the exclusion set from population_from_map() and checks each name against graph-call-manifest.yaml's retired_aliases directly -- RE_DERIVED_EXCLUDED=4 of 93, all four declared_retired=True, UNDECLARED_EXCLUSIONS=0. A generator asserting its own exclusions are benign is the producer self-reporting.",
    "the_entry_grain_too": "the order's clause cites R14 `status: retired` on the ENTRY. At this HEAD exactly 2 manifest entries carry it -- cloud.refresh.full and cloud.refresh.incremental -- and they are ENTRY ids, not tool names, so the NAME-grain declaration surface for these four is retired_aliases (9 names). Both are printed; the grains are not conflated.",
    "the_side_effect": "row NFRA_CLDGRPH-W4-S5 -- the same change carries comp-v5-composite-test.sh into the KEPT set, where its profile row has \"primitives\": [], so unclassified rises 3 -> 4 and AUTHORITY_WITHOUT_A_PROFILE_ROW falls 16 -> 15. No tool is added, lost or reclassified (TOOL_MASTER stays 99 tools, counts.population_authority_count 99, parity holds). It was unclassified BEFORE by absence and is unclassified AFTER by empty primitives -- same end state, except its attributes are now reachable and it carries the explicit UNCLASSIFIED marker CTO ruling 212335Z requires instead of sitting in the orphan list."
  },

  "the_phrase_census_by_source": {
    "why_by_source": "three of the four scanned files are GENERATED. A raw hit count over a generated file cannot say WHICH upstream literal put the string there, and this order owns exactly one of the two upstreams.",
    "scanned": ".tools/tool_index.py, .tools/TOOL_CLASSIFICATION.yaml, org/modules/graph/TOOL_MASTER.yaml, org/modules/graph/manifest_check_cli.py -- 3 carriers + 1 checker",
    "phrases": "3, fragment-built in the probe so the probe itself never adds a hit to a future census",
    "GENERATOR_SOURCED_HITS": "0 of 1 hits",
    "CHECKER_HITS": "0",
    "MANIFEST_SOURCED_HITS": "1 -- .tools/tool_index.py:2936, inside the MANIFEST_DOC literal, attributed by parsing graph-call-manifest.yaml and walking each string to its nearest enclosing entry id: cloud.cluster.page_panel_drilldown (manifest :1489 id, :1500 freshness). Carried by row NFRA_CLDGRPH-W4-S1; the manifest is outside <paths> and tool_index.py reproduces it verbatim, so no regeneration this order can run removes it.",
    "OTHER_SOURCED_HITS": "0",
    "control": "PHRASE_PROBE_CONTROL=FIRED -- the phrase planted into a COPY of gen_tool_classification.py AND of TOOL_CLASSIFICATION.yaml drives GENERATOR_SOURCED_HITS to 1 through the SAME scan function. Nothing under the repo is written by the control.",
    "unscoped_repo_census_beside_it": "python .tools/comp-find 'auto-refresh on HEAD-advance|auto-refreshes on HEAD-advance|canonical persisted Kuzu DB' .tools org/modules/graph --all -- 21 hits / 799 files BEFORE (SURFACED=6 CONFIG=15), 7 hits / 799 files AFTER (SURFACED=4 CONFIG=3). The 7 are the one manifest-sourced carrier hit plus the six out-of-grant residues in row NFRA_CLDGRPH-W4-S4. The issuer's cut-time figure of 16 / 854 is a DIFFERENT pathspec and the two denominators are not comparable."
  },

  "the_regeneration": {
    "commands_MEASURED_not_assumed": "each carrier was asked which generator it declares in its OWN header: .tools/TOOL_CLASSIFICATION.yaml:3 'generated_by: .tools/gen_tool_classification.py'; org/modules/graph/TOOL_MASTER.yaml:3 'generated_by: .tools/gen_tool_registry.py -- DO NOT HAND-EDIT'; .tools/tool_index.py:1 'GENERATED by .tools/gen_tool_registry.py -- DO NOT EDIT'.",
    "REGEN_CARRIERS": 3,
    "REGEN_COMMANDS": 2,
    "why_not_3": "row NFRA_CLDGRPH-W4-S2. gen_tool_registry.py writes BOTH TOOL_MASTER.yaml and tool_index.py in one main() (:309-311, two WROTE prints). E-1's record says the same. A repo census of 'gen_tool_registry|gen_tool_classification' turns up no third generator. Printing 3 would be a fabricated denominator, and a summary field is not repaired by prose beside it.",
    "idempotence": "SECOND_REGEN_DIFF_LINES=0 -- both generators run twice; all three carriers byte-identical across the two passes (TOOL_CLASSIFICATION.yaml 657e0577f162a002, TOOL_MASTER.yaml 762f9d33c811a3ca, tool_index.py 6ae9c5e5aa77e542, LF-normalised sha256 prefixes).",
    "hand_edits": "HAND_EDITED_CARRIERS=0 of 3, with HAND_EDIT_CONTROL=FIRED (an in-memory mutated copy compares UNEQUAL, so the 0 is a measurement).",
    "the_CRLF_trap_this_probe_avoids": "this is an autocrlf checkout. .tools/tool_index.py is 543627 bytes in the worktree and 536980 at HEAD with IDENTICAL content -- `git status --porcelain` reports it MODIFIED after a no-op regeneration while `git diff` returns 0 lines. Every comparison in f8_regen_idempotent.sh is on LF-normalised bytes, so a phantom edit cannot read as a hand edit and a real one cannot hide behind the warning.",
    "the_baseline_this_establishes": "the three carriers at base HEAD c6b16d8f04 ALREADY equalled their generators' output: regenerating before any edit produced a 0-line git diff. So every byte of carrier change in this order is attributable to the two source edits, not to a pre-existing drift."
  },

  "F8-AC4_the_named_flag_does_not_exist": {
    "row": "NFRA_CLDGRPH-W4-S3",
    "measured": "'argparse' and 'sys.argv' are BOTH absent from .tools/gen_tool_registry.py. Python discards the unknown argument and main() runs, so `python .tools/gen_tool_registry.py --check` REGENERATES both carriers and exits 0 -- a check-shaped invocation with a WRITE side effect. Its five output lines contain ZERO occurrences of PARITY or OK.",
    "the_real_parity_check": "assert_population_parity() at :138-151, called at :219 inside main(). It is RAISE-ONLY: PopulationDivergence on any divergence in either direction, silence on success, with the count landing in the master as counts.population_authority_count. There is no CLI surface for it and no invocation of this generator can emit the token the expect requires.",
    "and_it_passes_with_both_controls": "positive -- assert_population_parity(population_from_map(), population_from_map()) returns 99; negative -- assert_population_parity({'a'},{'b'}) raises PopulationDivergence('POPULATION DIVERGENCE vs org/modules/graph/comp-coverage-map.yaml (the SOLE population authority)...'). TOOL_MASTER.yaml counts = {'tools': 99, 'population_authority_count': 99} after the normaliser change. So the criterion's SUBSTANCE holds and is controlled; only its instrument and its expect token do not exist.",
    "what_was_deliberately_not_done": "no --check flag was added. BOUNDS caps this order at three source edits; a fourth would widen the order, and the clause's own remedy is a row, not a build."
  },

  "F8-AC5_the_instruction_plane_read_one_last_time": {
    "grading": "3.0.0_SA_CVO at L9. NO VERDICT IS OFFERED HERE.",
    "instrument_caveat_stated_first": "comp-which prints 'ALARM: POTION semantic embedder unavailable -> falling back to lexical relevance (POTION hash-mismatch on tokenizer.json ... FAIL-CLOSED)' on every call in this worktree -- pre-existing at HEAD, untouched here, and identically present in E-1's record. All three routings below are LEXICAL, not semantic.",
    "three_phrasings_and_their_routes": [
      "'how do I refresh the graph' -> near-tie, top 3 of 80: (1) comp-aws derive --out <path> (the live-AWS cloud-graph WRITE-PATH), (2) comp-build [--check] (rebuilds the TRACE-graph cache), (3) comp-kuzu \"<Cypher>\" ... 'the answer on stdout, then a VINTAGE line on stderr saying in plain words how old it is'. NO route names a refresh of the retired local Kuzu projection; the two write-paths that do surface are a different graph each (the AWS cloud graph, the trace cache).",
      "'my graph is behind, what refreshes it' -> top 3 of 79: (1) comp-kuzu \"MATCH ...\" score 2.00 -- 'cross-surface federated READ ... the FAST default read-path', (2) comp-drift, (3) comp-aws. The rank-1 answer to a staleness question is a READ tool whose card states the served projection and its VINTAGE line. This is E-1's E1-AC2 phrasing and it answers the same way at this HEAD.",
      "'what refreshes the served graph projection' -> near-tie, top 3 of 79: (1) comp-drift, (2) comp-kuzu \"<Cypher>\" with the VINTAGE-line description, (3) comp-describe. Again no refresh command for the projection."
    ],
    "what_the_manifest_sourced_residue_means": "one entry, cloud.cluster.page_panel_drilldown, still tells a reading seat three things about the retired engine in one freshness: string -- 'live canonical Nessie->Kuzu graph', 'prints the comp-kuzu provenance header', 'auto-refreshes on HEAD-advance'. It is NOT a route back (no call, no flag), so it does not fire E1-AC1's predicate; it is a DESCRIPTION, which is exactly what FWD-7 covers and exactly what a route-shaped probe cannot see. Whose row: the manifest is graph-call-manifest.yaml, E-1/CG-s-17's surface and outside this order's <paths>; the row is NFRA_CLDGRPH-W4-S1 with disarm_owner 2.0.0_SA_COO~A, and the fix is one string plus a regeneration of tool_index.py. Note the shape for the grader: this residue reaches the compiled index through MANIFEST_DOC, so 'regenerate the index' can NEVER clear it -- only editing the manifest can.",
    "is_the_normaliser_MECE_now": "over the names that EXIST today, yes and it is measured: suffixes present across both sides = {.py, .sh}, stripped = {.py, .sh}, unstripped = none, and the no-suffix name survives unchanged (NORM_CONTROL). What it is NOT is MECE over a declared domain of possible suffixes -- there is no such declaration anywhere, and a new .cmd or .ps1 name in either registry would pass through unstripped and reappear as a false exclusion by exactly the W2-S37 mechanism. The docstring now says so in the file, so the next seat re-censuses instead of assuming; whether that is sufficient, or whether the suffix set belongs in the coverage map as declared data, is a question for the grader, not a claim here.",
    "one_more_thing_the_reading_turned_up": "the six out-of-grant residues in row NFRA_CLDGRPH-W4-S4 are not all of one kind. Two are LIVE INSTRUCTION in module prose a reader is shown (comp_debt/grounding_lib.py:205 tells a debt-grounding reader that 'comp-kuzu auto-refreshes on HEAD-advance, so a healthy call reads current' -- a falsifiable claim about behaviour); one is a comment justifying a defensive branch (comp_legacywriter.py:237); one is a module docstring (comp_ws4_crosswalk.py:14); two are estate-census DATA carriers with their own producers (estate-coverage-resolver.json:1356, estate_census/pass1_inventory.json:1858), which will re-emit the string on their next build unless their SOURCE moves."
  },

  "bounds_honoured": {
    "source_edits": "3 (plus one same-file rewrite of the tombstone comment in gen_tool_classification.py so it CITES rather than repeats the retired phrase -- same edit, same criterion, not a fourth surface)",
    "generated_carriers": "REGENERATED, never hand-edited -- HAND_EDITED_CARRIERS=0 of 3",
    "manifest": "NOT edited. graph-call-manifest.yaml was READ only (comp-read --enumerate x2, plus a parse in the probe).",
    "population_authority": "NOT changed. comp-coverage-map.yaml READ only; gen_tool_classification still reads the population through gen_tool_registry.population_from_map(), imported, never copied.",
    "tools": "none retired, none added -- TOOL_MASTER 99 tools before and after, population parity 99/99",
    "graph-call-manifest.yaml / infra/system/": "untouched. The comp-system two-phase gate fires on org/modules/graph/ edits and its phase-two discharge (comp-system regenerating infra/system/06_current_state.*) belongs to the DRAIN seat 2.0.0_SA_COO~A, per this face and W2-S36.",
    "outside_paths": "nothing written outside <paths> plus this deliverables folder. The six residues in W4-S4 are rows, not edits -- a path a grant lacks is a row, never an override."
  },

  "rows_filed": [
    "NFRA_CLDGRPH-W4-S1 -- OBSERVATION / ARMED (2.0.0_SA_COO~A) -- the surviving carrier hit is manifest-sourced (cloud.cluster.page_panel_drilldown freshness), unreachable by any regeneration this order can run",
    "NFRA_CLDGRPH-W4-S2 -- BLOCKING / ARMED (2.0.0_SA_COO~A) -- F8-AC3 expects REGEN_COMMANDS=3; two generator scripts write three carriers",
    "NFRA_CLDGRPH-W4-S3 -- BLOCKING / ARMED (2.0.0_SA_COO~A) -- F8-AC4's --check flag does not exist and is silently ignored; the real parity check is silent-on-success",
    "NFRA_CLDGRPH-W4-S4 -- OBSERVATION / ARMED (2.0.0_SA_COO~A) -- six out-of-grant descriptions of the dead engine remain, enumerated with lines",
    "NFRA_CLDGRPH-W4-S5 -- OBSERVATION / INERT -- the .sh fix moves a second counter (unclassified 3 -> 4, AUTHORITY_WITHOUT_A_PROFILE_ROW 16 -> 15) and the cause is measured"
  ],

  "channel_denominator": "152 rows in 124 blocks before this append, 157 in 125 after -- COUNTED BY PARSING every fenced json block and summing their lengths, never by an id grep (which matches the header line itself). No row edited, no id renumbered; W4-S1..W4-S5 are this slot's first rows in this channel."
}
```

## What this order fixed, and what it could not

*(The prose below is the PASS 1 narrative, unedited. Two of its claims were overtaken by the
issuer amendment and are corrected here rather than rewritten there, because the reasoning is
what the amendment acted on: (i) "the one hit that survives is not the carrier's to fix" was
true under the pass-1 grant -- the amendment widened the grant by that one string and the hit
is now fixed AT SOURCE, so F8-AC1 reads `MANIFEST_SOURCED_HITS=0 (NONE)`; (ii) "two criteria
could not be satisfied" was true against the original expects -- both were re-cut and both now
PASS, with the F8-AC3 probe BYTE-UNCHANGED. What did not change: the measured numbers.)*

**Two descriptions of a dead engine, in the two places that fan out.** `REFRESH['GRAPH-DB']` in
`gen_tool_classification.py` is not one string: it is the value that lands on every GRAPH-DB tool in
both generated registries, which is why the phrase read six times in `TOOL_CLASSIFICATION.yaml` and
six times in `TOOL_MASTER.yaml`. Changing the generator and regenerating took all twelve to zero in
one act -- and the same act would have been undone by any hand edit of a carrier, which is why the
idempotence check is the criterion rather than a diff. The checker's `raw_cypher` note is the second:
it told every seat that tripped the finding to route back to "the canonical persisted Kuzu DB", a
store retired at CG-s-8, and its `cloud.*` glob also matched the two entries CG-s-17 retired. It now
names three live ids that were read out of the manifest, not composed.

**The normaliser was one suffix, and the suffix set was the thing worth measuring.** The repair is a
line; the work is the census that says which suffixes exist on each side, so the constant is a
declared domain with a printed denominator instead of a second guess. The authority carries no
suffix at all (99 of 99); the profile carries `.py` six times and `.sh` once. `EXCLUDED_NOT_IN_AUTHORITY`
goes 5 of 93 to 4 of 93 and the "NOT DECLARED RETIRED -- A FINDING" line goes to `0 of 4: none`,
which is the whole point: the four names that remain are four real retirements and nothing else is
hiding among them.

**The one hit that survives is not the carrier's to fix.** `tool_index.py:2936` still reads the
retired phrase because `tool_index.py` embeds `graph-call-manifest.yaml` verbatim as `MANIFEST_DOC`,
and the manifest entry `cloud.cluster.page_panel_drilldown` still describes the local engine in its
`freshness:` field. This is exactly why `F8-AC1` counts by SOURCE: a raw hit count over a generated
file would have made this look like a failure of the generator this order owns, and a worker chasing
that number would have hand-edited a generated carrier -- the W2-S30 defect -- or edited a manifest
outside its grant. It is row `NFRA_CLDGRPH-W4-S1` instead, with the entry id and the line.

**Two criteria could not be satisfied because their instruments do not exist, and neither was
papered over.** `F8-AC3` wants `REGEN_COMMANDS=3`; the tree has three generated carriers and *two*
generator scripts, because `gen_tool_registry.py` writes `TOOL_MASTER.yaml` and `tool_index.py` in
one invocation -- measured by asking each carrier which generator it declares in its own header,
not inferred. Every substantive limb of that criterion holds (`SECOND_REGEN_DIFF_LINES=0`,
`HAND_EDITED_CARRIERS=0 of 3`, both with controls). Printing `3` to clear a regex would have been
this worker choosing its own denominator. `F8-AC4` names `--check`, and `gen_tool_registry.py` has
no argv parsing at all -- so the "check" silently regenerates both carriers and returns 0, and the
real parity assertion is raise-only and prints nothing on success. The order's own clause anticipated
this and directs a row rather than a silent substitution; the row carries the real instrument, the
positive control (99) and the negative control (`PopulationDivergence` FIRED), so a re-cut has
everything it needs to decide whether the criterion should read on `rc 0 + no PopulationDivergence +
counts.population_authority_count == the authority size`, or whether the generator should grow a real
check mode in a later order. Adding that flag here would have been a fourth source edit against a
BOUNDS block that caps this order at three.

**One thing deliberately not done.** The `comp-system` gate makes any commit touching
`org/modules/graph/` a two-phase act, and phase two writes `infra/system/`. This face says that is
expected and the discharge is the drain's, so the audited `STRUCTURAL-TWOPHASE`/rule-bank override is
taken as the gate directs, citing `NFRA_CLDGRPH-W2-S36` and this face, and `infra/system/` is
untouched by this worker.
