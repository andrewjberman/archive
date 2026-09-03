# comp-blast — NFRA_COMPEFFICACY T-6 result (PRD v0.6 s.4)

Schema: `NFRA_COMPEFFICACY_PRD` v0.6 @`7138c4a176`, s.4. Row T-6. Cell CE-t-6
(decomp v0.2.5 @`e2b6c1fc96`). Measured by `0.8.0_AE_CloudComp~G` on
2026-09-03 after GO Msg-ID 93784. The engine was blob
`abac8d92b2bba70eec8e1982a6a651b2c9e427c9` before this change and
`85c35d0567eab3aca743ebe2e83cb7e0100f706a` after the working-tree edit.

```json
{
  "schema": "NFRA_COMPEFFICACY_PRD v0.6 s.4",
  "row": "T-6",
  "cell": "CE-t-6",
  "measured_by": "0.8.0_AE_CloudComp~G",
  "measured_at_utc": "2026-09-03",
  "read_vintage": "HEAD @327217feba5b749b14d775363cdacce103536959",
  "surprises": [],
  "identity": {
    "tool": "comp-blast",
    "shim_path": ".tools/comp-blast (bash forwarding shim)",
    "engine_path": "org/modules/graph/cli.py (blast subcommand; calls comp_blast_universe and TraceGraph)",
    "graph": "canonical Kuzu resource graph, read-only; 27206 nodes and 58550 edges at AC-7 measured read",
    "built_vintage": "built: 2026-09-03T17:13:01.645625+00:00; Nessie pin 8525533673192182741 (behind current HEAD, explicitly warned)",
    "called_resolver": "org/modules/graph/comp_blast_universe.py::resolve_subject",
    "node_denominator": "27206 canonical Kuzu nodes; real subject arn:aws:s3:::opal-data-bd yielded 158 depth-1 downstream results",
    "called_components": ["TraceGraph.downstream", "TraceGraph.upstream", "comp_blast_universe.load_kuzu_universe", "comp_blast_universe.derive_overlay"]
  },
  "disclosure": {
    "help": "--exact, --all, --direction up|upstream|down|downstream|both, --budget, --cursor, and rc vocabulary 0 clean / 1 tool-failed / 2 stale / 3 NOT-FOUND / 4 phantom-consumer / 5 ambiguous / 6 partial-budget.",
    "real_subject_run": "comp-blast --force arn:aws:s3:::opal-data-bd --direction down --depth 1 --budget 0 -> rc 0, BLAST RADIUS, 158 downstream results, graph built vintage and denominator printed, WITHIN BUDGET scanned 158 of 158 traversal.",
    "absent_subject_run": "comp-blast --force --exact T6-no-such-node -> rc 3, canonical provenance built line, denominator 27206, ANSWER-STATE SUBJECT_ABSENT_FROM_CORPUS, and no radius claim.",
    "grain": "One answer is one canonical Kuzu node subject plus the requested directional traversal; every answer states graph vintage and node denominator.",
    "vintage": "The Kuzu built line and Nessie pin are emitted by the existing provenance formatter; no graph rebuild or comp-trace mutation was performed by this cell."
  },
  "answer_state": {
    "enum": ["SUBJECT_ABSENT_FROM_CORPUS", "PRESENT_WITH_ZERO_RESULTS", "PARTIAL_OR_BLIND", "NOT_APPLICABLE"],
    "SUBJECT_ABSENT_FROM_CORPUS": {"planted": "--exact T6-no-such-node", "printed": "ANSWER-STATE: SUBJECT_ABSENT_FROM_CORPUS", "rc": 3, "radius": "ABSENT"},
    "PRESENT_WITH_ZERO_RESULTS": {"planted": "real node arn:aws:s3:::opal-313476888478-globgrph --direction down", "printed": "ANSWER-STATE: PRESENT_WITH_ZERO_RESULTS", "rc": 0, "radius": "0 downstream results with node named"},
    "PARTIAL_OR_BLIND": {"planted": "accounts_dimension fuzzy subject and --budget 0.001 traversal", "printed": "ANSWER-STATE: PARTIAL_OR_BLIND; AMBIGUOUS-SUBJECT names 27 nodes; BUDGET REACHED scanned 1 of 158", "rc": "5 ambiguous or 6 partial-budget"},
    "NOT_APPLICABLE": {"planted": "--overlap-sweep --population nonexistent:", "printed": "ANSWER-STATE: NOT_APPLICABLE (no producer population selected)", "rc": 0},
    "distinctness": "One --self-test invocation printed all four exact tokens and answer_state.four_distinct_tokens PASS."
  },
  "carry": {
    "table": [
      ["--exact", "exact node-id resolution; fuzzy miss is NOT-FOUND", "real exact subject rc 0; absent exact rc 3"],
      ["--all", "direction=both in blast's universe", "real node rc 0; both-direction traversal accepted"],
      ["--direction up/upstream", "blast direction=up", "accepted; alias maps to upstream"],
      ["--direction down/downstream", "blast direction=down", "accepted; alias maps to downstream"],
      ["--direction both", "blast direction=both", "accepted; both lists rendered"]
    ],
    "trace_sha_before_after": "comp-trace blob 9bcf128cf6ff4b7e95f6ed2e6869526b9588fd2d before and after; byte-identical",
    "trace_evidence": "S17 @a140eed779 and comp-trace --help enumerate --exact, --all, and up/upstream/down/downstream/both; no caller was redirected."
  },
  "rule_t": {
    "carrier": ".tools/_compbudget.py; precedence --budget > COMP_BUDGET_S > default 90s; --budget 0 unbounded",
    "expiry": "EXIT_PARTIAL_BUDGET=6, distinct from clean 0, tool-failed 1, stale 2, NOT-FOUND 3, phantom 4, and ambiguous 5",
    "cut_capture": "--budget 0.001: rc 6, BUDGET REACHED, scanned 1 of 158 traversal, cursor down:<first-node>, ANSWER-STATE PARTIAL_OR_BLIND",
    "resume_capture": "--budget 0 --cursor down:<first-node>: rc 0, WITHIN BUDGET, remaining 157 traversal units; true radius verdict restored",
    "consumer_census": "167 comp-blast runs / 30 days in the TO; blast's ordinary rc is execution/reporting except --check-consumers rc 4, so the verdict-bearing row applies to --check-consumers and budget expiry remains non-clean.",
    "distinct_seat_fwd9": "2.0.0_SA_COO at 16:45:06Z, HEAD 9879a8d5ab: --force --exact arn:aws:s3:::opal-313476888478-globgrph --all --budget 0 -> rc 0, WITHIN BUDGET scanned 507 of 507 traversal; Kuzu 27134 nodes / 58432 edges, Nessie snapshot 7140819680255399272.",
    "unbounded_convention": "The distinct-seat run proves --budget 0 is explicitly UNBOUNDED; it does not exercise expiry. The positive 0.001-second local arm is the expiry control.",
    "ac7_whole_call": "Positive --budget 60 starts one Rule-T clock before Kuzu load; stale served graph returned rc 0 in 8.5 s with BUDGETED CALL: SERVING EXISTING GRAPH STALE (age 0.5h), reason BEHIND Nessie HEAD, and no kuzu_nessie_load.py child or rebuild launch. --budget 0/--force print UNBUDGETED CALL disclosure.",
    "cursor": "Stable direction:node-id key; totals are measured after cursor filtering."
  },
  "overlap": {
    "recording": "BY NAME ONLY",
    "comp_blast": "canonical Kuzu graph blast-radius question: what nodes are reached from a change subject?",
    "comp_similar": "parallel comp-similar corpus/relatedness question over its own similarity joins; no shared graph semantics",
    "boundary": "No comp-similar code, corpus, edges, or callers were imported, merged, or re-scoped."
  },
  "battery": {
    "path": ".tools/tests/test_comp_blast_battery.py",
    "tests": 7,
    "direct": "7/7 PASS",
    "pytest": "7 passed at file grain",
    "red_mutants": "5/5 source-mutant arms: NOT-FOUND radius, exact fuzzy selection, wrong direction alias, partial returning clean, and budgeted refresh ambush",
    "commit_gate": "PASS: commit-gate clean for cli.py, comp_blast_universe.py, and test_comp_blast_battery.py"
  },
  "acceptance": {
    "T6-AC1": "PASS — identity, shim, Kuzu graph built vintage, denominator, and called components recorded.",
    "T6-AC2": "PASS — one self-test invocation emits four distinct tokens; absent and ambiguous paths retain denominator/vintage and never claim a zero radius.",
    "T6-AC3": "PASS — exact/all/upstream/downstream/both carry accepted; comp-trace blob unchanged.",
    "T6-AC4": "PASS — shared carrier/help, rc 6 expiry, cursor, cursor resume, and 167-run consumer census recorded.",
    "T6-AC5": "PASS — battery direct and pytest green; four red mutants; commit gate clean.",
    "T6-AC6": "PASS — proof validates before complete flip; COO distinct-seat FWD-9 is measured and recorded; commits are LOCAL and no push was performed.",
    "T6-AC7": "PASS — budgeted comp-blast serves the existing stale graph immediately with age/reason disclosure and no refresh child; --budget 0/--force disclose the unbudgeted path; the battery includes a RED-first refresh-ambush mutant."
  },
  "push_state": {
    "before": "engine blob abac8d92b2bba70eec8e1982a6a651b2c9e427c9; comp-trace blob 9bcf128cf6ff4b7e95f6ed2e6869526b9588fd2d",
    "after_local": "commit 6df07696eac80fb5322e498d6b121bd9a56d0d02; engine blob 85c35d0567eab3aca743ebe2e83cb7e0100f706a; battery blob c02223250bacccb1434f1f2679eebe130477da4c",
    "origin": "MEASURED ABSENT: origin/CLOUD 351f309e0a6ded1a5a5bdf3aacec18a5f9f8dbee; git merge-base --is-ancestor returned rc=1; no push performed"
  }
}
```

## Captured commands

```text
bash .tools/comp-blast --help
bash .tools/comp-blast --self-test
bash .tools/comp-blast --force --exact T6-no-such-node
bash .tools/comp-blast --force arn:aws:s3:::opal-data-bd --direction down --depth 1 --budget 0.001
bash .tools/comp-blast --force arn:aws:s3:::opal-data-bd --direction down --depth 1 --budget 0 --cursor down:<first-node>
bash .tools/comp-blast --force --overlap-sweep --population nonexistent:
```

## Lift verdict

**PASS pending commit** — comp-blast now carries comp-trace's flags into the canonical Kuzu
universe, distinguishes all four answer states, and makes a partial traversal mechanically
non-clean and resumable without touching comp-trace.
