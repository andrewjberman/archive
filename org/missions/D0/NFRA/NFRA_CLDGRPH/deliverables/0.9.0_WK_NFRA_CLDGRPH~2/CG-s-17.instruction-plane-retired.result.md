# CG-s-17 -- THE INSTRUCTION PLANE'S ROUTE BACK, RETIRED (TO-CG-E-1, round 5)

**Worker:** `0.9.0_WK_NFRA_CLDGRPH~2` · **Branch:** `wk-cldgrph-5-2` · **HEAD at pass-2 spawn:** `91d62f2ee6`
(pass 1 ran from `de466829e0`) · **Order:** `NFRA_CLDGRPH.TO-CG-E-1` · **Cell:** CG-s-17 ·
**PASS 2, on the issuer's amendment @`facc7241a5`.** **Status of the order: COMPLETE** -- six mechanical
criteria PASS by output, the seventh is recorded and graded by `3.0.0_SA_CVO` at L9.

```json
{
  "to_id": "NFRA_CLDGRPH.TO-CG-E-1",
  "cell": "CG-s-17",
  "worker": "0.9.0_WK_NFRA_CLDGRPH~2",
  "branch": "wk-cldgrph-5-2",
  "pass": 2,
  "head_at_pass1_spawn": "de466829e0",
  "head_at_pass2_spawn": "91d62f2ee6",
  "pass1_work_commits": ["97b461da9f", "629fa87b36"],
  "premises_reground_at_handoff": [
    {
      "premise": "infra/aws/globgrph/kuzu_cli.py REFUSES --mode",
      "holds": true,
      "measured": "python infra/aws/globgrph/kuzu_cli.py --mode full 'MATCH (n) RETURN n LIMIT 1' -> 'usage: kuzu_cli.py [-h] [--json] [--limit LIMIT] [--schema] [query]' / 'kuzu_cli.py: error: unrecognized arguments: --mode ...'",
      "note": "the usage line carries a --schema flag the order's paraphrase does not name; the tools_index subcommand row was set from the MEASURED surface, not the paraphrase"
    },
    {
      "premise": "graph-call-manifest.yaml carries cloud.refresh.full and cloud.refresh.incremental with status: canonical",
      "holds": true,
      "measured": "yaml.safe_load -> 127 entries, Counter({'canonical': 126, None: 1}); both refresh ids present, status canonical, mode rebuild, tool comp-kuzu"
    },
    {
      "premise": "bash .tools/comp-manifest-check completeness prints PASS at HEAD",
      "holds": true,
      "measured": "'PASS: routable + placement + self-routes + existence, over 78 registered tool(s).' and 'retired-alias invariant PASS: 9 retired name(s) declared'"
    }
  ],
  "what_pass2_owed_and_did": [
    {
      "owed": "(1) gen_tool_classification.py takes its POPULATION from the authority, the exclusions printed",
      "did": "Population moved from org/tier1_exec/3.0.0_SA_CVO/deliverables/tool_profile.json to org/modules/graph/comp-coverage-map.yaml. THE AUTHORITY IS READ THROUGH gen_tool_registry.population_from_map(), IMPORTED, NEVER COPIED -- a second implementation here would be a second reader of one population, the defect being fixed one file over. Fails CLOSED and loud on an unimportable reader OR an empty authority (an empty authority would exclude every row and write a vacuous clean file). PROFILE stays the ATTRIBUTE source. The split is printed BEFORE anything is written.",
      "measured": "POPULATION AUTHORITY: org/modules/graph/comp-coverage-map.yaml -- 99 tool(s) | PROFILE (attributes only) -- 93 row(s) | EXCLUDED_NOT_IN_AUTHORITY=5 of 93 | of those DECLARED RETIRED ALIASES (expected)=4 of 5 | NOT DECLARED RETIRED -- A FINDING, NOT AN EXCLUSION=1 of 5: comp-v5-composite-test.sh | AUTHORITY_WITHOUT_A_PROFILE_ROW=16 of 99"
    },
    {
      "owed": "(2) regenerate classification -> registry -> TOOL_MASTER.yaml + tool_index.py",
      "did": "python .tools/gen_tool_classification.py, then python .tools/gen_tool_registry.py. BOTH ARTIFACTS ARE REGENERATED, NEVER HAND-EDITED. The registry generator, which REFUSED at pass 1 with PopulationDivergence, now runs.",
      "measured": "'WROTE .tools/TOOL_CLASSIFICATION.yaml / classified 85 / unclassified 3' then 'WROTE org/modules/graph/TOOL_MASTER.yaml  (99 tools)' / 'WROTE .tools/tool_index.py (card = 8 fields + MANIFEST_DOC + LEDGER_DOC, import-verified pre-replace)'. TOOL_MASTER counts: tools 99, population_authority_count 99 (was 91/91 and stale against a 99-tool authority)."
    },
    {
      "owed": "(3) the capture repoint in summary_corpus.py (W2-S32)",
      "did": "_capture_kuzu_vintage now parses the SERVED disclosure line and ONLY that line; the retired local header's `built:`/`DB:` regexes are gone, because a second limb for a store retired at CG-s-8 is a reader kept alive for a surface that no longer exists. built = the service's own VINTAGE stamp; age = the service's plain-words sentence VERBATIM; db = the SERVED SURFACE (the artifact prefix, or the literal `served`). The client renders an absent bracket field as the literal string `None`, which is treated as the ABSENCE it is.",
      "measured": "Exercised in-process on five shapes: served+vintage -> {'built': '2026-09-09T11:02:44+00:00', 'age': 'built 2026-09-09T11:02:44+00:00, 0.4h ago', 'db': 's3://opal-globgrph-projection/served/', 'claim': 'measured'}; service unreachable -> {}; served with vintage=None -> {}; served with prefix=None -> db 'served'; the RETIRED local header -> {}."
    },
    {
      "owed": "(4) the probe rename + D-7's probe restored (W2-S34)",
      "did": "E1-AC6's probe is now e1_commit_gate_all.sh; every probe this order writes carries the e1_ prefix from here. D-7's commit_gate_all.sh restored from de466829e0 by `git show` and verified BYTE-IDENTICAL.",
      "measured": "D-7 blob @de466829e0 sha256 54df937de6cf2fad6f4e76a6c3278c32d71459e4353e1221618a6925a3c7ae34, 3251 bytes; restored worktree file sha256 54df937de6cf2fad6f4e76a6c3278c32d71459e4353e1221618a6925a3c7ae34, 3251 bytes; BYTE-IDENTICAL: True"
    },
    {
      "owed": "(5) every criterion re-run at HEAD",
      "did": "All six mechanical criteria run under `timeout`, each rc read UNPIPED; no rc 124 anywhere. E1-AC1..AC6 PASS by output; E1-AC7 recorded, not graded.",
      "measured": "see `criteria` below"
    },
    {
      "owed": "(6) the instance updated, validated, and the flip ONLY on rc 0 with every mechanical row PASS",
      "did": "Instance rebuilt with pass-2 outputs and pass-2 artifact pins; validated with the seven ids; the <status> flipped to complete in the same commit as the instance, the deliverables and every touched carrier.",
      "measured": "proof-of-spec-check rc=0"
    },
    {
      "owed": "the comp-system two-phase override is EXPECTED; do not attempt phase two",
      "did": "The audited `system-current-override: STRUCTURAL-TWOPHASE/rule-bank` trailer is taken as the gate directs and cites W2-S36. infra/system/ is untouched; the discharge is the issuer's at the drain.",
      "measured": "the gate's own text: 'Land-then-recompile is TWO-PHASE BY NECESSITY and the override IS the legal path, not a lapse'"
    }
  ],
  "census": {
    "instrument": "python .tools/comp-find 'cloud\\.refresh\\.(full|incremental)|\\-\\-mode (auto|inc|full)|\\-\\-db-path' org/modules/graph .tools docs org/ref .claude CLAUDE.md --files",
    "denominator_line_before": "DENOMINATOR: 165 hit(s) across 2054 file(s) scanned in scope [corpus=all] | 15 EPHEMERAL-FLOOR, NOT searched (--corpus raw reads these) | 7 BINARY, NOT searched",
    "bands_before": "SURFACED=57 CONFIG=99 TEST=2 DOC=7 ; PAGE 1 of 1 (showing 18 of 18)",
    "reproduces_issuer": "yes -- 18 files / 165 hits, identical to the issuer's cut figure",
    "denominator_line_after_pass1": "DENOMINATOR: 101 hit(s) across 2054 file(s) scanned in scope [corpus=all] -- 11 file(s)",
    "denominator_line_after_pass2": "DENOMINATOR: 22 hit(s) across 2055 file(s) scanned in scope [corpus=all] | 46 EPHEMERAL-FLOOR, NOT searched (--corpus raw reads these) | 7 BINARY, NOT searched",
    "bands_after_pass2": "SURFACED=7 CONFIG=6 TEST=2 DOC=7 ; PAGE 1 of 1 (showing 10 of 10)",
    "files": "18 -> 11 (pass 1) -> 10 (pass 2)",
    "hits": "165 -> 101 (pass 1) -> 22 (pass 2)",
    "table": [
      {"file": ".tools/comp-which", "band": "SURFACED", "occ_before": 5, "occ_after": 0, "disposition": "REPOINTED", "what": "the two curated LOCAL-REFRESH routes (:631-642) merged into ONE curated route to the served read; all 30 refresh phrasings KEPT and repointed, 3 vintage phrasings added"},
      {"file": ".tools/comp-describe", "band": "SURFACED", "occ_before": 1, "occ_after": 0, "disposition": "REPOINTED", "what": "the 0-matches hint no longer names --mode inc; the surface line now says SERVED (no local store, no db path)"},
      {"file": ".tools/comp-cluster", "band": "SURFACED", "occ_before": 1, "occ_after": 0, "disposition": "REPOINTED", "what": "the `--db-path PATH ... frozen-vintage DB` usage line replaced with a note that comp_cluster_cli.py REFUSES a local path at runtime (exercised: 'REFUSE: local database paths are retired (NFRA_CLDGRPH R7)')"},
      {"file": ".tools/gen_tool_classification.py", "band": "SURFACED", "occ_before": 1, "occ_after": 0, "disposition": "REPOINTED (pass 1) + POPULATION MOVED TO THE AUTHORITY (pass 2)", "what": "pass 1 repointed PRIM_MAP['GRAPH-DB'] excludes AT SOURCE; pass 2 moved the file's POPULATION from the CVO's tool_profile.json to comp-coverage-map.yaml, read through gen_tool_registry.population_from_map() rather than a second copy, with the exclusions printed and a not-declared-retired exclusion reported as a finding"},
      {"file": ".tools/comp-find", "band": "SURFACED", "occ_before": 1, "occ_after": 1, "disposition": "HISTORY-NOT-ROUTING", "what": "one DOCSTRING line at :133 recording that no --mode inc is left on the aws path -- prose about the retirement, band-excluded by E1-AC3's own rule"},
      {"file": ".tools/tool_index.py", "band": "SURFACED", "occ_before": 48, "occ_after": 7, "disposition": "REGENERATED (never hand-edited)", "what": "GENERATED by gen_tool_registry.py, whose header forbids hand edits. Pass 1 could not regenerate it (the compiler REFUSED); pass 2 fixed the compiler's input and regenerated. The 7 remaining occurrences: 3 inside the DECLARED retired-alias records for comp-kuzu-full/comp-kuzu-inc (:3353, :3375, :3379 -- exempt by E1-AC3's own clause) and 4 that are the entry IDS `cloud.refresh.full|incremental` (:1150, :1175, :1220), a token E1-AC3 does not score at all. E1-AC3's own walk reads 0 counted hits"},
      {"file": ".tools/TOOL_CLASSIFICATION.yaml", "band": "CONFIG", "occ_before": 34, "occ_after": 0, "disposition": "REGENERATED (never hand-edited)", "what": "regenerated twice -- pass 1 for the repointed excludes string, pass 2 for the authority-sourced population"},
      {"file": "org/modules/graph/TOOL_MASTER.yaml", "band": "CONFIG", "occ_before": 33, "occ_after": 0, "disposition": "REGENERATED (never hand-edited)", "what": "GENERATED by gen_tool_registry.py ('DO NOT HAND-EDIT'). Blocked at pass 1, regenerated at pass 2: 91 -> 99 tools, population_authority_count 99, and the 33 copies of the repointed excludes string carried through"},
      {"file": "org/modules/graph/comp-tools.yaml", "band": "CONFIG", "occ_before": 12, "occ_after": 0, "disposition": "REPOINTED", "what": "comp-kuzu command/when/cost/freshness/rebuild_trigger rewritten to the served read; comp-describe's rebuild_trigger hint repointed"},
      {"file": "org/modules/graph/comp-output-contracts.yaml", "band": "CONFIG", "occ_before": 7, "occ_after": 0, "disposition": "REPOINTED", "what": "comp-kuzu coverage/blind_spots/vintage/exit_codes rewritten to the served client's real contract; comp-blast address_space repointed"},
      {"file": "org/modules/graph/graph-call-manifest.yaml", "band": "CONFIG", "occ_before": 27, "occ_after": 7, "disposition": "REPOINTED + RETIRED-RECORD", "what": "two entries retired under the convention, successor added, three freshness texts and one rebuild_trigger rewritten, tools_index comp-kuzu and comp-cluster rows corrected. Pass 2 reworded the two retired records to CITE the literal historical call form where retired_aliases already records it, rather than repeating it (row W2-S38). The 7 remaining are RECORDS: 3 in the pre-existing retired_aliases block, 2 the retired entry IDS, 2 in the successor's notes naming what it succeeds"},
      {"file": "org/modules/graph/comp_aws_cli.py", "band": "SURFACED (outside the flags census -- kuzu_nessie_db only)", "occ_before": 2, "occ_after": 0, "disposition": "REPOINTED", "what": ":2857 comment and :2866 print now name the SERVED projection and its pointer"},
      {"file": "org/modules/graph/debtscan/comp_similar.py", "band": "SURFACED (outside the flags census -- kuzu_nessie_db only)", "occ_before": 3, "occ_after": 1, "disposition": "REPOINTED", "what": "the C3c leg rewritten TWICE: pass 1 removed the fabricated header; pass 2 made both arms the SERVED shape (served+vintage -> measured on the served surface; served without a vintage -> absent + DISCLOSED) and added a retired-shape control. The 1 remaining hit is a COMMENT recording what was removed"},
      {"file": "org/modules/graph/debtscan/summary_corpus.py", "band": "SURFACED (added to <paths> by the amendment)", "occ_before": 0, "occ_after": 0, "disposition": "REPOINTED (the CAPTURE, W2-S32)", "what": "_capture_kuzu_vintage repointed from the retired local header to the SERVED disclosure line; the retired regexes removed rather than kept as a second limb"},
      {"file": ".tools/tests/test_cg6_thin_client_battery.py", "band": "TEST", "occ_before": 2, "occ_after": 2, "disposition": "TEST-ASSERTS-REFUSAL", "what": "FORBIDDEN_FLAGS asserts the flags are REFUSED. Not a carrier; not edited; run and PASS 7/7"},
      {"file": "docs/architecture/EC2_TELEMETRY_DESIGN.md", "band": "DOC", "occ_before": null, "occ_after": null, "disposition": "HISTORY-NOT-ROUTING", "what": "declared, not edited"},
      {"file": "docs/architecture/NFRA_DEBTSCAN_PRD.md", "band": "DOC", "occ_before": null, "occ_after": null, "disposition": "HISTORY-NOT-ROUTING", "what": "declared, not edited"},
      {"file": "docs/architecture/NFRA_KUZUSPLIT_PRD.md", "band": "DOC", "occ_before": null, "occ_after": null, "disposition": "HISTORY-NOT-ROUTING", "what": "declared, not edited -- it is the PRD that LANDED the two refresh modes; its account of what was built stays true"},
      {"file": "docs/briefs/nfra-tsgraph-p0-spike-report-20260617.md", "band": "DOC", "occ_before": null, "occ_after": null, "disposition": "HISTORY-NOT-ROUTING", "what": "declared, not edited"},
      {"file": "docs/doctrine/CLAUDE_ANNEX.md", "band": "DOC", "occ_before": null, "occ_after": null, "disposition": "HISTORY-NOT-ROUTING", "what": "declared, not edited"},
      {"file": "org/modules/graph/COMPTOOL_REGISTRATION_FLOW.md", "band": "DOC", "occ_before": null, "occ_after": null, "disposition": "HISTORY-NOT-ROUTING", "what": "declared, not edited"}
    ]
  },
  "successor_entry": {
    "id": "cloud.read.served_vintage",
    "tool": "comp-kuzu",
    "mode": "query",
    "write_path": false,
    "status": "canonical",
    "canonical_call": "comp-kuzu \"<Cypher>\" [--json] [--limit N]   # the answer on stdout, then a VINTAGE line on stderr saying in plain words how old it is",
    "is_a_read_not_a_refresh": true,
    "names_how_old_its_answer_is": true,
    "source_of_the_vintage_claim": "infra/aws/globgrph/kuzu_cli.py:46-61 _disclosure; :64-66 _unavailable_disclosure names the ABSENCE",
    "documents_no_db_path_and_no_parameter_dict": "projection_client.query(statement, timeout_s) -> {rows, vintage, age_line, manifest_sha256, artifact_prefix} (:194-201), quoted in the entry's notes"
  },
  "retired_records": [
    {"id": "cloud.refresh.full", "status": "retired", "superseded_by": "cloud.read.served_vintage", "resolves_to_live_entry": true, "has_retired_prose": true, "has_why_prose": true, "deleted": false},
    {"id": "cloud.refresh.incremental", "status": "retired", "superseded_by": "cloud.read.served_vintage", "resolves_to_live_entry": true, "has_retired_prose": true, "has_why_prose": true, "deleted": false}
  ],
  "status_value_chosen": {
    "value": "retired",
    "declared_where": "graph-call-manifest.yaml per-entry schema -- the enum widened to 'canonical | deprecated | planned | retired' with the entry-grain convention and the reason written in",
    "why_not_deprecated": "manifest_check_cli.deprecated_signatures():355-380 builds its detection signature from the entry's `tool:` NAME alone, so applying it to a mode-variant of the still-live comp-kuzu flags every code line naming that tool. MEASURED in-process before choosing: 168 ERROR-class A_deprecated_call findings over 5 files. Row NFRA_CLDGRPH-W2-S31",
    "how_the_entry_actually_leaves_the_candidate_set": "NOT by the status field -- no consumer filters on it. It leaves because its `use_case:` no longer carries routing vocabulary, and the vocabulary itself was REPOINTED in comp-which's curated table rather than deleted"
  },
  "comp_which_answers": {
    "instrument_caveat": "comp-which prints 'ALARM: POTION semantic embedder unavailable -> falling back to lexical relevance (POTION hash-mismatch on tokenizer.json ... FAIL-CLOSED)' on every call in this worktree -- pre-existing at HEAD, untouched here. All four routings are LEXICAL, not semantic",
    "my graph is behind": "rank 1: comp-kuzu \"MATCH ...\" -- no cloud.refresh, no --mode, no --db-path, no kuzu_nessie_db",
    "full rebuild / ground-truth reset of the local projection": "rank 1: comp-kuzu \"MATCH ...\" -- clean",
    "MSTR startup graph warm": "rank 1: comp-kuzu \"MATCH ...\" -- clean",
    "control (what breaks if I change this bucket)": "rank 1: comp-blast <fn-or-artifact> -> tools_index['comp-blast'].entries = ['trace.blast.what_breaks'], status canonical"
  },
  "instrument_lines": {
    "gen_tool_classification": "POPULATION AUTHORITY: org/modules/graph/comp-coverage-map.yaml -- 99 tool(s) (read via gen_tool_registry.population_from_map) | EXCLUDED_NOT_IN_AUTHORITY=5 of 93 | NOT DECLARED RETIRED -- A FINDING, NOT AN EXCLUSION=1 of 5: comp-v5-composite-test.sh | AUTHORITY_WITHOUT_A_PROFILE_ROW=16 of 99 | WROTE .tools/TOOL_CLASSIFICATION.yaml, classified 85 / unclassified 3",
    "gen_tool_registry": "WROTE org/modules/graph/TOOL_MASTER.yaml (99 tools) | WROTE .tools/tool_index.py (card = 8 fields + MANIFEST_DOC + LEDGER_DOC, import-verified pre-replace) | master sha256 6bde9aa2bce785f8 | master bytes 89738 | index bytes 543627",
    "comp_manifest_check_completeness": "PASS: routable + placement + self-routes + existence, over 78 registered tool(s). | retired-alias invariant PASS: 9 retired name(s) declared, all disjoint from live+excluded (99 live), successors valid",
    "comp_coverage_view_verify": "OK: all 78 manifest tools_index entries present in the ledger union (99 tools); regeneration is non-breaking.",
    "thin_client_battery": "BATTERY: 7 of 7 arm(s) PASS -- ARM v 'CLI surface: no refresh/db-path choice 5 of 5 checks PASS'",
    "comp_similar_self_test": "=== comp_similar self-test: PASS (11/11) === with 'C3c vintage-CAPTURE (served+vintage -> measured on the SERVED surface; served without a vintage -> absent + DISCLOSED; the retired local header -> unreadable): served=ok neg-control=ok retired-shape-control=ok PASS'",
    "commit_gate": "pre-commit gate clean (8 of 8 file(s): commit-gate rc=0, comp-which compile rc=0, bash -n rc=0; thin-client battery PASS; comp-similar self-test PASS)",
    "d7_probe_restore": "D-7 blob @de466829e0 sha256 54df937de6cf2fad6f4e76a6c3278c32d71459e4353e1221618a6925a3c7ae34 (3251 bytes) == restored worktree file sha256 54df937de6cf2fad6f4e76a6c3278c32d71459e4353e1221618a6925a3c7ae34 (3251 bytes) -- BYTE-IDENTICAL"
  },
  "criteria": {
    "E1-AC1": {"verdict": "PASS-by-output", "deciding": "LIVE_ROUTES_BACK=0 of 126 ; RETIRED_RECORDS=2 of 2 ; TOOLS_INDEX_FLAGS=0 of 9 ; TOOLS_INDEX_FLAGS_UNSCOPED=0 of 78 row(s) ; ROUTE_PROBE_CONTROL=FIRED ; ROUTE_NEGATIVE_CONTROL=FIRED", "rc": 0},
    "E1-AC2": {"verdict": "PASS-by-output", "deciding": "RETIRED_ROUTES=0 of 3 ; WHICH_PROBE_CONTROL=FIRED (comp-blast -> trace.blast.what_breaks, status canonical)", "rc": 0},
    "E1-AC3": {"verdict": "PASS-by-output", "deciding": "HELP_ROUTES_BACK=0 of 8 ; HELP_COUNTED_HITS_TOTAL=0 ; HELP_EXCLUDED_AS_RECORD_OR_PROSE=2 ; HELP_PROBE_CONTROL=FIRED ; HELP_BAND_CONTROL=FIRED", "rc": 0, "pass1_was": "HELP_ROUTES_BACK=1 of 8, rc 1 -- the probe is BYTE-UNCHANGED between the two passes; what changed is the world it measures"},
    "E1-AC4": {"verdict": "PASS-by-output", "deciding": "retired-alias invariant PASS ... PASS: routable + placement + self-routes + existence, over 78 registered tool(s).", "rc": 0},
    "E1-AC5": {"verdict": "PASS-by-output", "deciding": "OK: all 78 manifest tools_index entries present in the ledger union (99 tools); regeneration is non-breaking.", "rc": 0},
    "E1-AC6": {"verdict": "PASS-by-output", "deciding": "pre-commit gate clean (8 of 8 file(s): commit-gate rc=0, comp-which compile rc=0, bash -n rc=0; thin-client battery PASS; comp-similar self-test PASS)", "rc": 0},
    "E1-AC7": {"verdict": "RECORDED (judgment) -- graded by 3.0.0_SA_CVO at L9, no verdict here", "rc": null}
  },
  "E1-AC7_person_half_and_successor_shape": {
    "a_what_would_exercise_the_accept_clause_2": "A seat ON SITE Z asks D-8's FIXED QUESTION through the PUBLIC GATEWAY, inside D-8's WINDOW, and its answer matches the laptop's BYTE-FOR-BYTE under ONE VINTAGE. Four conjuncts, and this order satisfies none of them: it ran on the laptop fabric only, opened no gateway session, asked no fixed question and compared no two machines. FWD-7's PERSON half is MODELLED -- the model being D-8's one worker on two machines -- and stays modelled until the roadmap's site-Z allocation puts a second seat on a second fabric. This order closes FWD-7's INSTRUCTION half.",
    "b_is_the_successor_a_read_that_names_how_old_its_answer_is": "Yes. cloud.read.served_vintage carries mode: query, write_path: false, and a bare Cypher canonical_call. Its freshness QUOTES the client's own disclosure from source (kuzu_cli.py:46-61) rather than paraphrasing it, and carries BOTH failure directions verbatim -- 'AGE NOT STATED BY THE SERVICE -- no age was inferred' and 'VINTAGE: unavailable -- the projection service did not answer; no age was inferred and no local copy was read'. Its rebuild_trigger is the word 'none' WITH the reason, not an empty field.",
    "b_did_any_repoint_re_create_a_rebuild_path": "No. No entry, help text, curated route, registry row or code site added by either pass names a refresh, a rebuild, a loader or a store to open. The two retired entries keep mode: rebuild as part of the historical record and are excluded from the LIVE candidate set; E1-AC1 counts that live set and reads 0 of 126 with a planted-positive proving the predicate would catch one and a planted-negative proving it does not convict a plain read. Pass 2 went further in the same direction: summary_corpus.py's parser for the RETIRED header was REMOVED rather than kept as a fallback limb, because a reader kept alive for a retired surface is the same defect one layer down.",
    "b_did_any_repoint_document_a_db_path_or_a_parameter_dict": "No, and the W2-S27 bound was APPLIED at four sites rather than assumed: the successor entry's notes quote projection_client.query's real signature and return keys; comp-tools.yaml's comp-kuzu `when:` says in terms that the tool takes no database path and no Cypher parameter dict; comp-output-contracts.yaml's third blind_spot says the same and adds that a caller must substitute literals before running; and summary_corpus.py's repointed capture reads only the fields the served answer actually carries. The tools_index subcommand list was set from the MEASURED usage line, which carries a --schema derivation the order's paraphrase omitted.",
    "b_two_reservations_for_the_grader": "(i) E1-AC2's four comp-which answers were produced with the POTION embedder unavailable (fail-closed, pre-existing at HEAD, untouched here), so the routing measured is LEXICAL, not semantic; the curated-route table this criterion is about is matched lexically in both modes, so the reading holds, but a semantic re-run is not offered and is not claimed. (ii) E1-AC3's RETIRED-RECORD exemption is NAME-grained while this order's retirement is ENTRY-grained, so two record fields and one test fixture were written to discriminate WITHOUT carrying the retired token rather than widening the probe -- the probe at HEAD is byte-identical to the one that FAILED at pass 1, which is the evidence that the bar did not move. Row NFRA_CLDGRPH-W2-S38 states the choice for grading."
  },
  "surprises": [
    "NFRA_CLDGRPH-W2-S30",
    "NFRA_CLDGRPH-W2-S31",
    "NFRA_CLDGRPH-W2-S32",
    "NFRA_CLDGRPH-W2-S33",
    "NFRA_CLDGRPH-W2-S34",
    "NFRA_CLDGRPH-W2-S35",
    "NFRA_CLDGRPH-W2-S36",
    "NFRA_CLDGRPH-W2-S37",
    "NFRA_CLDGRPH-W2-S38"
  ]
}
```

## What the two passes did, and what the second one actually fixed

The cell's test is the CTO's: *a retirement has three planes, and a manifest that places only the
EXECUTABLE one passes every cell while leaving a live instruction to re-create the path.* The
executable plane went at CG-s-8. This order is the instruction plane, and the census measures how
much of it moved: **18 files / 165 hits -> 10 files / 22 hits**, with every reachable carrier at 0
and the remainder being records, history, and a battery that asserts the refusal.

**Pass 1 landed six of seven and named its own block.** The manifest's two refresh entries are
retired under the file's own convention applied one grain down, with a READ successor;
`comp-which`'s curated table keeps all thirty refresh phrasings and lands them on that read, because
a deleted rule is a fall-through and not a retirement; every registry carrier was repointed. E1-AC3
failed on one file, `.tools/tool_index.py`, which is not a help surface but a compiled artifact
whose generator refused.

**Pass 2 fixed the refusal at its cause, which was one file over and inside the grant.**
`gen_tool_registry.py` builds its master from `TOOL_CLASSIFICATION.yaml` and refuses on any
divergence from `comp-coverage-map.yaml`, the sole population authority. But
`TOOL_CLASSIFICATION.yaml` is generated by `gen_tool_classification.py` from the CVO's
`tool_profile.json` — so the classification generator was itself *"a peer file that enumerates its
own tool list"*, the exact thing the CTO's ruling 212335Z forbids, and the four retired names still
in the profile made the compiler refuse outright. The fix moves that generator's **population** to
the authority and keeps the profile as the **attribute** source it always was. Two choices in the
implementation are worth the grader's eye:

- **The authority is read through `gen_tool_registry.population_from_map()`, imported, never
  copied.** Writing a second `population_from_map()` here would have created a second reader of one
  population — the defect being removed, one file over. The import **fails closed and loud**, and so
  does an empty authority: an empty authority would exclude every profile row and write a
  clean-looking empty classification, which is a vacuous pass wearing a green tick.
- **The exclusions are printed with their denominator and split by kind.** `EXCLUDED_NOT_IN_AUTHORITY=5
  of 93`, of which four are declared retired aliases (expected bookkeeping) and **one is not** —
  `comp-v5-composite-test.sh`, which is not a missing tool but one tool spelled two ways, because
  the shared normaliser strips `.py` and not `.sh`. That is printed under its own heading so it can
  never read as a retirement, and it is row `NFRA_CLDGRPH-W2-S37`. The reverse direction is printed
  too (`AUTHORITY_WITHOUT_A_PROFILE_ROW=16 of 99`), and those are not dropped: the registry
  generator emits each with an explicit UNCLASSIFIED marker.

With that, both generated artifacts regenerated — never hand-edited — and E1-AC3 went from
`HELP_ROUTES_BACK=1 of 8` to `0 of 8` **with the probe byte-unchanged from the pass that failed**.

**The capture finally moved with the comparison.** The amendment widened `<paths>` by
`summary_corpus.py`, so `_capture_kuzu_vintage` now parses the served disclosure line and *only*
that line: the retired header's `built:`/`DB:` regexes were removed rather than kept as a fallback,
because a reader kept alive for a retired surface is this cell's own defect one layer down. Every
`comp-similar` coverage line over the served graph now carries a measured vintage naming the served
surface, where before it carried a permanent UNKNOWN.

**Two things this pass had to do that the order did not say, both rows.** `W2-S37` is above.
`W2-S38` is the one a grader should read closely: E1-AC3 exempts *"a string inside a declared
RETIRED-ALIAS record"*, and `retired_aliases:` is a closed set of **names**, while this order's
retirement is at the **entry** grain — so the two retired entries' own `canonical_call` and `why:`
prose scored as instructions. Widening the probe's exemption would have been the worker grading its
own criterion. The probe was left alone and the prose was changed instead: the records now **cite**
the literal historical call form where the convention already keeps it — this file's
`retired_aliases` entries for `comp-kuzu-full` and `comp-kuzu-inc` — rather than repeating it. The
record loses nothing and the instrument was not touched.

**One thing this pass deliberately did not do.** The `comp-system` gate makes any commit touching
`org/modules/graph/` a two-phase act, and phase two writes `infra/system/`. The issuer's amendment
says that is expected and the discharge is the issuer's at the drain, so the audited
`STRUCTURAL-TWOPHASE/rule-bank` override is taken as the gate directs, cites `NFRA_CLDGRPH-W2-S36`,
and `infra/system/` is untouched.
