# CG-s-17 -- THE INSTRUCTION PLANE'S ROUTE BACK, RETIRED (TO-CG-E-1, round 5)

**Worker:** `0.9.0_WK_NFRA_CLDGRPH~2` · **Branch:** `wk-cldgrph-5-2` · **HEAD at spawn:** `de466829e0` ·
**Order:** `NFRA_CLDGRPH.TO-CG-E-1` · **Cell:** CG-s-17 · **Status of the order: OPEN** -- E1-AC3 FAILs by
output on one carrier that this grant cannot repair (row `NFRA_CLDGRPH-W2-S30`). Six of seven criteria pass;
the seventh is recorded, not graded.

```json
{
  "to_id": "NFRA_CLDGRPH.TO-CG-E-1",
  "cell": "CG-s-17",
  "worker": "0.9.0_WK_NFRA_CLDGRPH~2",
  "branch": "wk-cldgrph-5-2",
  "head_at_spawn": "de466829e0",
  "premises_reground_at_handoff": [
    {
      "premise": "infra/aws/globgrph/kuzu_cli.py REFUSES --mode",
      "holds": true,
      "measured": "python infra/aws/globgrph/kuzu_cli.py --mode full 'MATCH (n) RETURN n LIMIT 1' -> 'usage: kuzu_cli.py [-h] [--json] [--limit LIMIT] [--schema] [query]' / 'kuzu_cli.py: error: unrecognized arguments: --mode ...'",
      "note": "the usage line carries a --schema flag the order's paraphrase does not name; the tools_index subcommand row was corrected to the MEASURED surface, not the paraphrased one"
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
  "census": {
    "instrument": "python .tools/comp-find 'cloud\\.refresh\\.(full|incremental)|\\-\\-mode (auto|inc|full)|\\-\\-db-path' org/modules/graph .tools docs org/ref .claude CLAUDE.md --files",
    "denominator_line_before": "DENOMINATOR: 165 hit(s) across 2054 file(s) scanned in scope [corpus=all] | 15 EPHEMERAL-FLOOR, NOT searched (--corpus raw reads these) | 7 BINARY, NOT searched",
    "bands_before": "SURFACED=57 CONFIG=99 TEST=2 DOC=7 ; PAGE 1 of 1 (showing 18 of 18)",
    "reproduces_issuer": "yes -- 18 files / 165 hits, identical to the issuer's cut figure",
    "denominator_line_after": "DENOMINATOR: 101 hit(s) across 2054 file(s) scanned in scope [corpus=all] | 28 EPHEMERAL-FLOOR, NOT searched (--corpus raw reads these) | 7 BINARY, NOT searched",
    "bands_after": "SURFACED=49 CONFIG=43 TEST=2 DOC=7 ; PAGE 1 of 1 (showing 11 of 11)",
    "files_before": 18,
    "files_after": 11,
    "hits_before": 165,
    "hits_after": 101,
    "table": [
      {"file": ".tools/comp-which", "band": "SURFACED", "occ_before": 5, "occ_after": 0, "disposition": "REPOINTED", "what": "the two curated LOCAL-REFRESH routes (:631-642) merged into ONE curated route to the served read; all 30 refresh phrasings KEPT and repointed, 3 vintage phrasings added"},
      {"file": ".tools/comp-describe", "band": "SURFACED", "occ_before": 1, "occ_after": 0, "disposition": "REPOINTED", "what": "the 0-matches hint no longer names --mode inc; the surface line now says SERVED (no local store, no db path)"},
      {"file": ".tools/comp-cluster", "band": "SURFACED", "occ_before": 1, "occ_after": 0, "disposition": "REPOINTED", "what": "the `--db-path PATH ... frozen-vintage DB` usage line replaced with a note that comp_cluster_cli.py REFUSES a local path at runtime (exercised: 'REFUSE: local database paths are retired (NFRA_CLDGRPH R7)')"},
      {"file": ".tools/gen_tool_classification.py", "band": "SURFACED", "occ_before": 1, "occ_after": 0, "disposition": "REPOINTED", "what": "PRIM_MAP['GRAPH-DB'] excludes: 'a scratch --db-path is a frozen vintage' -> 'anything the SERVED projection has not picked up yet -- read the VINTAGE line'. THE SOURCE, not the output"},
      {"file": ".tools/comp-find", "band": "SURFACED", "occ_before": 1, "occ_after": 1, "disposition": "HISTORY-NOT-ROUTING", "what": "one DOCSTRING line at :133 recording that no --mode inc is left on the aws path -- prose about the retirement, band-excluded by E1-AC3's own rule"},
      {"file": ".tools/tool_index.py", "band": "SURFACED", "occ_before": 48, "occ_after": 57, "disposition": "BLOCKING-ROW", "what": "GENERATED artifact (DO-NOT-EDIT). Its two sources were repointed; its compiler gen_tool_registry.py REFUSES on a PRE-EXISTING population divergence and the repairing inputs are outside <paths>. Row NFRA_CLDGRPH-W2-S30. Count RISES because the after-figure adds the kuzu_nessie_db/ENGINE-INTERNALLY tokens E1-AC3 scores, which the census pattern did not carry"},
      {"file": ".tools/TOOL_CLASSIFICATION.yaml", "band": "CONFIG", "occ_before": 34, "occ_after": 0, "disposition": "REPOINTED", "what": "REGENERATED from the edited generator (python .tools/gen_tool_classification.py -> 'WROTE .tools/TOOL_CLASSIFICATION.yaml, classified 89 / unclassified 4'); 34 insertions / 34 deletions, no other field moved"},
      {"file": "org/modules/graph/TOOL_MASTER.yaml", "band": "CONFIG", "occ_before": 33, "occ_after": 33, "disposition": "BLOCKING-ROW", "what": "GENERATED by the same refusing compiler; the 33 are the SAME excludes string, fanned out. Row NFRA_CLDGRPH-W2-S30"},
      {"file": "org/modules/graph/comp-tools.yaml", "band": "CONFIG", "occ_before": 12, "occ_after": 0, "disposition": "REPOINTED", "what": "comp-kuzu command/when/cost/freshness/rebuild_trigger rewritten to the served read; comp-describe's rebuild_trigger hint repointed"},
      {"file": "org/modules/graph/comp-output-contracts.yaml", "band": "CONFIG", "occ_before": 7, "occ_after": 0, "disposition": "REPOINTED", "what": "comp-kuzu coverage/blind_spots/vintage/exit_codes rewritten to the served client's real contract; comp-blast address_space repointed"},
      {"file": "org/modules/graph/graph-call-manifest.yaml", "band": "CONFIG", "occ_before": 27, "occ_after": 9, "disposition": "REPOINTED + RETIRED-RECORD", "what": "two entries retired under the convention, successor added, three freshness texts and one rebuild_trigger rewritten, tools_index comp-kuzu and comp-cluster rows corrected. The 9 remaining are RECORDS: 3 in the retired_aliases block (pre-existing), 2 in the retired entries' ids, 2 in their `why:` prose quoting the historical call form, 2 in the successor's notes naming what it succeeds"},
      {"file": ".tools/tests/test_cg6_thin_client_battery.py", "band": "TEST", "occ_before": 2, "occ_after": 2, "disposition": "TEST-ASSERTS-REFUSAL", "what": "FORBIDDEN_FLAGS = ('--mode', '--db-path', ...) -- the battery asserts the flags are REFUSED. Not a carrier; not edited; run and PASS 7/7"},
      {"file": "docs/architecture/EC2_TELEMETRY_DESIGN.md", "band": "DOC", "occ_before": null, "occ_after": null, "disposition": "HISTORY-NOT-ROUTING", "what": "declared, not edited"},
      {"file": "docs/architecture/NFRA_DEBTSCAN_PRD.md", "band": "DOC", "occ_before": null, "occ_after": null, "disposition": "HISTORY-NOT-ROUTING", "what": "declared, not edited"},
      {"file": "docs/architecture/NFRA_KUZUSPLIT_PRD.md", "band": "DOC", "occ_before": null, "occ_after": null, "disposition": "HISTORY-NOT-ROUTING", "what": "declared, not edited -- it is the PRD that LANDED the two refresh modes; its account of what was built stays true"},
      {"file": "docs/briefs/nfra-tsgraph-p0-spike-report-20260617.md", "band": "DOC", "occ_before": null, "occ_after": null, "disposition": "HISTORY-NOT-ROUTING", "what": "declared, not edited"},
      {"file": "docs/doctrine/CLAUDE_ANNEX.md", "band": "DOC", "occ_before": null, "occ_after": null, "disposition": "HISTORY-NOT-ROUTING", "what": "declared, not edited"},
      {"file": "org/modules/graph/COMPTOOL_REGISTRATION_FLOW.md", "band": "DOC", "occ_before": null, "occ_after": null, "disposition": "HISTORY-NOT-ROUTING", "what": "declared, not edited"},
      {"file": "org/modules/graph/comp_aws_cli.py", "band": "SURFACED (outside the flags census -- carries kuzu_nessie_db only)", "occ_before": 2, "occ_after": 0, "disposition": "REPOINTED", "what": ":2857 comment and :2866 print now name the SERVED projection and its pointer; the derive-not-published message no longer names a store comp-kuzu no longer opens"},
      {"file": "org/modules/graph/debtscan/comp_similar.py", "band": "SURFACED (outside the flags census -- carries kuzu_nessie_db only)", "occ_before": 3, "occ_after": 1, "disposition": "REPOINTED (comparison) + BLOCKING-ROW (capture)", "what": "the C3c fixture no longer feeds a header the tool never emits; the one remaining hit is a COMMENT recording what was removed. The PARSER it feeds is outside <paths> -- row NFRA_CLDGRPH-W2-S32"}
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
    "source_of_the_vintage_claim": "infra/aws/globgrph/kuzu_cli.py:46-61 _disclosure -- 'VINTAGE: %s  [vintage=%s manifest=%s prefix=%s]'; :64-66 _unavailable_disclosure names the ABSENCE",
    "documents_no_db_path_and_no_parameter_dict": "projection_client.query(statement, timeout_s) -> {rows, vintage, age_line, manifest_sha256, artifact_prefix} (:194-201) -- quoted in the entry's notes"
  },
  "retired_records": [
    {"id": "cloud.refresh.full", "status": "retired", "superseded_by": "cloud.read.served_vintage", "resolves_to_live_entry": true, "has_retired_prose": true, "has_why_prose": true, "deleted": false},
    {"id": "cloud.refresh.incremental", "status": "retired", "superseded_by": "cloud.read.served_vintage", "resolves_to_live_entry": true, "has_retired_prose": true, "has_why_prose": true, "deleted": false}
  ],
  "status_value_chosen": {
    "value": "retired",
    "declared_where": "graph-call-manifest.yaml per-entry schema, lines 23-38 -- the enum widened to 'canonical | deprecated | planned | retired' with the entry-grain convention and the reason written in",
    "why_not_deprecated": "manifest_check_cli.deprecated_signatures():355-380 builds its detection signature from the entry's `tool:` NAME alone, so a deprecated entry on the still-live comp-kuzu flags every code line naming that tool. MEASURED in-process before choosing: 168 ERROR-class A_deprecated_call findings over 5 files. Row NFRA_CLDGRPH-W2-S31",
    "how_the_entry_actually_leaves_the_candidate_set": "NOT by the status field -- no consumer filters on it (comp-which's _manifest_matches:1346-1369 iterates every entries: row regardless; comp_coverage_view.py never reads it). It leaves by its `use_case:` being rewritten to a RETIRED-RECORD sentence carrying no routing vocabulary, because the fuzzy backstop scores on use_case tokens; and the vocabulary itself was REPOINTED in comp-which's curated table rather than deleted, so an agent who still types it lands on the read"
  },
  "comp_which_answers": {
    "instrument_caveat": "comp-which prints 'ALARM: POTION semantic embedder unavailable -> falling back to lexical relevance (POTION hash-mismatch on tokenizer.json ... FAIL-CLOSED)' on every call in this worktree -- pre-existing at HEAD, untouched here. All four routings below are LEXICAL, not semantic",
    "my graph is behind": "rank 1: comp-kuzu \"MATCH ...\" (score 2.00 of 79) -- no cloud.refresh, no --mode, no --db-path, no kuzu_nessie_db",
    "full rebuild / ground-truth reset of the local projection": "rank 1: comp-kuzu \"MATCH ...\" (score 1.50 of 80) -- clean",
    "MSTR startup graph warm": "rank 1: comp-kuzu \"MATCH ...\" (score 1.50 of 79) -- clean",
    "control (what breaks if I change this bucket)": "rank 1: comp-blast <fn-or-artifact> (score 1.83) -> tools_index['comp-blast'].entries = ['trace.blast.what_breaks'], status canonical -- the router ran and can answer"
  },
  "instrument_lines": {
    "comp_manifest_check_completeness": "PASS: routable + placement + self-routes + existence, over 78 registered tool(s). | [manifest-check] retired-alias invariant PASS: 9 retired name(s) declared, all disjoint from live+excluded (99 live), successors valid; citation check (C) DID NOT RUN -- no routing surface in scope.",
    "comp_coverage_view_verify": "OK: all 78 manifest tools_index entries present in the ledger union (99 tools); regeneration is non-breaking.",
    "thin_client_battery": "BATTERY: 7 of 7 arm(s) PASS / PASS (rc 0) -- ARM v 'CLI surface: no refresh/db-path choice 5 of 5 checks PASS'",
    "comp_similar_self_test": "=== comp_similar self-test: PASS (11/11) === with 'C3c vintage-CAPTURE (SERVED header -> absent + DISCLOSED; readable header -> measured, so the parser is not a constant): served=ok live-parser-control=ok PASS'",
    "commit_gate": "OK: pre-commit gate clean for 3 of 3 file(s) ; pre-commit gate clean (6 of 6 file(s): commit-gate rc=0, comp-which compile rc=0, bash -n rc=0; thin-client battery PASS)"
  },
  "criteria": {
    "E1-AC1": {"verdict": "PASS-by-output", "deciding": "LIVE_ROUTES_BACK=0 of 126 ; RETIRED_RECORDS=2 of 2 ; TOOLS_INDEX_FLAGS=0 of 9 ; TOOLS_INDEX_FLAGS_UNSCOPED=0 of 78 row(s) ; ROUTE_PROBE_CONTROL=FIRED ; ROUTE_NEGATIVE_CONTROL=FIRED", "rc": 0},
    "E1-AC2": {"verdict": "PASS-by-output", "deciding": "RETIRED_ROUTES=0 of 3 ; WHICH_PROBE_CONTROL=FIRED (comp-blast -> trace.blast.what_breaks, status canonical)", "rc": 0},
    "E1-AC3": {"verdict": "FAIL", "deciding": "HELP_ROUTES_BACK=1 of 8 (the one carrier is .tools/tool_index.py, 38 counted CODE-band hits) ; HELP_PROBE_CONTROL=FIRED ; HELP_BAND_CONTROL=FIRED ; HELP_EXCLUDED_AS_RECORD_OR_PROSE=4", "rc": 1, "blocking_row": "NFRA_CLDGRPH-W2-S30"},
    "E1-AC4": {"verdict": "PASS-by-output", "deciding": "retired-alias invariant PASS ... PASS: routable + placement + self-routes + existence, over 78 registered tool(s).", "rc": 0},
    "E1-AC5": {"verdict": "PASS-by-output", "deciding": "OK: all 78 manifest tools_index entries present in the ledger union (99 tools); regeneration is non-breaking.", "rc": 0},
    "E1-AC6": {"verdict": "PASS-by-output", "deciding": "pre-commit gate clean (6 of 6 file(s): commit-gate rc=0, comp-which compile rc=0, bash -n rc=0; thin-client battery PASS)", "rc": 0},
    "E1-AC7": {"verdict": "RECORDED (judgment) -- graded by 3.0.0_SA_CVO at L9, no verdict here", "rc": null}
  },
  "E1-AC7_person_half_and_successor_shape": {
    "a_what_would_exercise_the_accept_clause_2": "A seat ON SITE Z asks D-8's FIXED QUESTION through the PUBLIC GATEWAY, inside D-8's WINDOW, and its answer matches the laptop's BYTE-FOR-BYTE under ONE VINTAGE. Four conjuncts, and none of them is exercised by this order: this order ran on the laptop fabric only, opened no gateway session, asked no fixed question, and compared no two machines. FWD-7's PERSON half is therefore MODELLED, not realized -- the model being D-8's one worker on two machines -- and it stays modelled until the roadmap's site-Z allocation puts a second seat on a second fabric. This order closes FWD-7's INSTRUCTION half only, and only in part (E1-AC3).",
    "b_is_the_successor_a_read_that_names_how_old_its_answer_is": "Yes. cloud.read.served_vintage has mode: query and write_path: false; its canonical_call is a bare Cypher read; its freshness field quotes the client's own disclosure line from source (kuzu_cli.py:46-61) rather than paraphrasing it, including BOTH failure directions -- the service stating no age ('AGE NOT STATED BY THE SERVICE -- no age was inferred') and the service not answering ('VINTAGE: unavailable ... no local copy was read'). Its rebuild_trigger is the word 'none' with the reason, not an empty field.",
    "b_did_any_repoint_re_create_a_rebuild_path": "No. No entry, help text, curated route, registry row or code site added in this order names a refresh, a rebuild, a loader or a store to open. The two retired entries keep mode: rebuild as part of the historical record and are excluded from the live candidate set; E1-AC1's LIVE_ROUTES_BACK counts the live set and reads 0 of 126, and its planted-positive control proves the predicate would have caught one.",
    "b_did_any_repoint_document_a_db_path_or_a_parameter_dict": "No, and the W2-S27 bound was applied at three sites rather than assumed: the successor entry's notes quote projection_client.query's real signature and return keys; comp-tools.yaml's comp-kuzu `when:` says in terms that the tool takes no database path and no Cypher parameter dict; comp-output-contracts.yaml's third blind_spot says the same and adds that a caller must substitute literals before running. The tools_index subcommand list was set from the MEASURED usage line (--json, --limit, --schema, <cypher>), not from the order's paraphrase, which omitted --schema.",
    "b_one_reservation_for_the_grader": "comp-which's answers in E1-AC2 were produced with the POTION embedder unavailable (fail-closed, pre-existing), so the routing measured is LEXICAL. The curated-route table this criterion is about is matched lexically in both modes, so the reading holds; a semantic re-run is not offered and is not claimed."
  },
  "surprises": [
    "NFRA_CLDGRPH-W2-S30",
    "NFRA_CLDGRPH-W2-S31",
    "NFRA_CLDGRPH-W2-S32",
    "NFRA_CLDGRPH-W2-S33",
    "NFRA_CLDGRPH-W2-S34",
    "NFRA_CLDGRPH-W2-S35",
    "NFRA_CLDGRPH-W2-S36"
  ]
}
```

## What was done, and the one thing that could not be

The cell's test is the CTO's: *a retirement has three planes, and a manifest that places only the
EXECUTABLE one passes every cell while leaving a live instruction to re-create the path.* The executable
plane went at CG-s-8. This order is the instruction plane, and the census says how much of it moved:
**18 files / 165 hits -> 11 files / 101 hits**, with every carrier the grant can reach reading **0**
except by design.

**The manifest.** The two refresh entries are retired *under the file's own convention, applied one grain
down* -- `superseded_by` a live entry, `retired:` prose carrying the consumers-first order, `why:` prose
carrying what the entry used to say and why the guarantee it held is not lost. They are KEPT. The successor
`cloud.read.served_vintage` is a **read**: it answers "my graph is behind" by telling the reader how old the
answer is, because FWD-2 and FWD-3 are what make a refresh route unnecessary. Choosing the status VALUE was
the one place where the file's own convention and its own enforcement disagreed, and the disagreement is
measured rather than argued: `deprecated` is TOOL-grained in `manifest_check_cli.deprecated_signatures()`,
so applying it to a mode-variant of a live tool produced **168 ERROR-class findings over 5 files** in a
dry run before anything was committed. `retired` was chosen and *declared in the schema* with that reason
written beside it. Separately, and more importantly for the next such retirement: **no consumer filters the
routing candidate set on `status` at all**, so the field alone would have retired nothing -- the entry
leaves the candidate set because its `use_case:` no longer carries routing vocabulary, and the vocabulary
itself was moved, not deleted.

**The route back that agents actually travel** was `comp-which`'s own curated table, not the manifest. Both
rules were merged into one that keeps every one of the 30 refresh phrasings and lands them on the read --
because an agent who types "ground-truth reset" must arrive somewhere that answers, and a deleted rule is a
fall-through, not a retirement.

**What could not be done.** `.tools/tool_index.py` is not a help surface; it is a compiled artifact of
`.tools/gen_tool_registry.py`, which refuses in this worktree on a population divergence that predates this
order (measured on unedited HEAD bytes: authority 99, classification 85, four names in the classification
absent from the authority). Its two sources are in `<paths>` and both were repointed; the compiler that
would carry those edits into the artifact cannot run, and the two inputs that would repair it are not in
`<paths>`. Hand-editing it would break its own DO-NOT-EDIT contract, would be reverted by the first
successful regeneration, and would require hand-editing `TOOL_MASTER.yaml` too, since 34 of the 38 counted
hits arrive through that file. So **E1-AC3 reads FAIL by output, the order stays OPEN, and the widening is
`2.0.0_SA_COO~A`'s call** (row `NFRA_CLDGRPH-W2-S30`). One measurement worth carrying with that row: the
artifact was **already** out of use for the manifest corpus before this edit -- its `MANIFEST_SHA256` pin
matches neither the HEAD manifest nor the edited one, so every reader already falls back to parsing the
live YAML. The strings are dead bytes in a superseded compilation. They are still readable by an agent,
which is exactly why the criterion counts them and why this is a finding rather than a shrug.

**One more finding arrived from the COMMIT and not from the work.** `safe-commit`'s `comp-system`
gate blocked the first attempt -- any commit touching `org/modules/graph/` is a two-phase act, and
its second phase is a recompile commit under `infra/system/`, which this order's `<paths>` does not
name. The audited override was taken with the gate's own reserved `STRUCTURAL-TWOPHASE/rule-bank`
prefix, exactly as the gate directs, and the discharge is named for the drain seat in row
`NFRA_CLDGRPH-W2-S36`. Recorded here because a worker face that touches the rule bank needs either
`infra/system/` in its grant or a line at the cut saying the override is expected.
