# comp-estate -- NFRA_COMPEFFICACY per-tool result (PRD v0.5 s.4)

Row T-17, measured by `0.8.0_AE_CloudComp~H` on 2026-09-03. The audited engine
change is `be15852e764df27c631c9d410eea0a51cd442264`; the naming snapshot was read,
not regenerated. Every field is measured unless marked ABSENT, PRESENT-BUT-WRONG, or CARRIED.

```json
{
  "schema": "NFRA_COMPEFFICACY_PRD v0.5 s.4 @5bbdab5ec7",
  "row": "T-17",
  "measured_by": "0.8.0_AE_CloudComp~H",
  "measured_at_utc": "2026-09-03T14:39Z..15:48Z",
  "read_vintage": "engine commit be15852e764df27c631c9d410eea0a51cd442264",
  "identity": {
    "tool": "comp-estate",
    "shim_path": ".tools/comp-estate (62 lines)",
    "engine_path": "org/modules/graph/opal_estate_infrastructure.py (1444 lines after T17; 1011 before)",
    "engine_vintage": "be15852e764df27c631c9d410eea0a51cd442264 (2026-09-03T11:46:16-04:00)",
    "aliases": [],
    "purpose_1line": "First-contact named-thread traversal returning every resource and traversal pointer for a requested business-semantic Estate thread (engine header, lines 3-7).",
    "self_identifies": {
      "grade": "PARTIAL",
      "default_run": "line 1 names ENGINE org/modules/graph/opal_estate_infrastructure.py and NAMING ONTOLOGY org/modules/graph/estate-coverage-resolver.json",
      "help": "names comp-estate and its flags but prints no engine vintage or version",
      "version_flag": "ABSENT"
    }
  },
  "disclosure": {
    "subject": {
      "grade": "PRESENT",
      "quoted": "--list: '29 C3.ii semantic verticals / 135 chains'; named default: comp-estate C3.ii vertical 'cma' - 1 chains"
    },
    "corpus_or_backend": {
      "grade": "PRESENT",
      "quoted": "NAMING ONTOLOGY: org/modules/graph/estate-coverage-resolver.json; generated C3.ii naming snapshot"
    },
    "vintage": {
      "grade": "PRESENT-BUT-STALE",
      "quoted": "last_review 2026-07-30",
      "measured_age": "35 days on the 2026-09-03 run"
    },
    "denominator": {
      "grade": "PRESENT",
      "quoted": "--list: 29 verticals / TOTAL 135 chains; cma: scanned 1 of 1 chain"
    },
    "resolved_unresolved": {
      "grade": "PRESENT",
      "quoted": "--list prints IN-SCOPE/OUT/UNREV per vertical; cma prints in-scope 1 / explicit-out 0 / unreviewed 0"
    },
    "blind_spots": {
      "grade": "PRESENT",
      "quoted": "snapshot is not locked C(N); C(N) is RELIES-ON NFRA_C3MATERIALIZE; C0 facts are NOT exhaustive; freshness adjectives are CENSUS-VINTAGE claims"
    },
    "pagination": {
      "grade": "PRESENT-BUT-WRONG",
      "quoted": "--head declares '[TRUNCATED --head: showing 0 of 10 body lines; verdict/denominator follow]' and preserves the terminal denominator",
      "wrong_part": "no --page/--limit/--all or PAGE i of N; --head does not meet Rule P"
    },
    "timeout": {
      "grade": "PRESENT for audited traversal; PRESENT-BUT-WRONG engine-wide",
      "quoted": "default named run: WITHIN BUDGET: scanned 1 of 1 chain; budget: 90 s (default)",
      "wrong_part": "--verify-served retains timeout=15, aws census-drift timeout=120, and --refresh has no timeout; these non-audited calls do not derive from remaining()"
    }
  },
  "answer_state": {
    "SUBJECT_ABSENT_FROM_CORPUS": {
      "planted": "comp-estate ZZZ_CE_T17_NO_SUCH_VERTICAL --budget 0",
      "printed": "ANSWER-STATE: SUBJECT_ABSENT_FROM_CORPUS / 0 matches across 29 declared C3.ii vertical name(s)",
      "rc": 2
    },
    "PRESENT_WITH_ZERO_RESULTS": {
      "planted": "comp-estate ceo-digest --budget 0; snapshot independently shows name present, 0 chains, separate 1-item C0 roster",
      "printed": "ANSWER-STATE: PRESENT_WITH_ZERO_RESULTS / measured result is 0 chain(s) across 135 / scanned 0 of 0 chain",
      "rc": 0
    },
    "PARTIAL_OR_BLIND": {
      "planted": "comp-estate 'C(N)' --budget 0",
      "printed": "ANSWER-STATE: PARTIAL_OR_BLIND / TOOL-VOICE: NOT-DECIDABLE / CARRIED to RELIES-ON NFRA_C3MATERIALIZE / no answer guessed",
      "rc": 0
    },
    "NOT_APPLICABLE": {
      "planted": "production _list_run invoked once with empty named_threads; fixture changes population only",
      "printed": "ANSWER-STATE: NOT_APPLICABLE / --list has no C3.ii vertical population; mode-level empty domain",
      "rc": 0
    }
  },
  "answer_state_assessment": {
    "grain": "Each case is one invocation's answer about one subject/mode and contains exactly one ratified ANSWER-STATE token; rc is not used to distinguish the rc-0 states.",
    "verdict": "PASS: four planted cases, four distinct ratified state tokens."
  },
  "bounds": {
    "subprocess_timeouts": [
      {
        "file_line": "opal_estate_infrastructure.py:337 @be15852e76",
        "value_s": 15,
        "wraps": "aws s3api head-object under opt-in --verify-served"
      },
      {
        "file_line": "opal_estate_infrastructure.py:858 @be15852e76",
        "value_s": "ABSENT",
        "wraps": "gen-estate-resolver.py under --refresh"
      },
      {
        "file_line": "opal_estate_infrastructure.py:1158 @be15852e76",
        "value_s": 120,
        "wraps": "aws lambda list-functions under --census-drift --plane aws"
      }
    ],
    "ceiling_behaviour": {
      "exercised": true,
      "expiry": "cma --budget 0.00001 -> BUDGET REACHED 1e-05 s (flag), scanned 0 of 1, PREFIX, rc 0",
      "clean": "cma --budget 0 -> WITHIN BUDGET scanned 1 of 1, unbounded, rc 0",
      "env": "COMP_BUDGET_S=0.00001 cma -> expiry source '(env COMP_BUDGET_S)', rc 0",
      "cursor": "advi-bd --cursor bd-allocation-file-watchdog --budget 0 resumes after the unit; battery asserts 18 of 18 and no replay"
    },
    "page_contract": {
      "page_flag": false,
      "limit_flag": false,
      "all_flag": false,
      "head_flag": true,
      "true_total_preserved": true,
      "rule_P": "NOT MET: --head is disclosed but is not PAGE i of N"
    },
    "size_invariance": {
      "audited_traversals": "MET: shared 90 s default, deterministic chain boundary, n<N expiry, resumable thread_id cursor, n=N completion",
      "list": "DECLARED NON-APPLICATION for early-abort because snapshot load is atomic; 29/135 still prints",
      "verdict_rc": "execution-only non-gate: Rule T expiry rc 0",
      "residual": "NOT MET engine-wide for refresh, verify-served, and aws census-drift"
    }
  },
  "passcraft": {
    "moves_1_to_8": [
      {
        "move": 1,
        "status": "DONE",
        "falsifier_answer": "read 62-line runpy shim and 1444-line engine; recon's self-contained label is false"
      },
      {
        "move": 2,
        "status": "DONE",
        "falsifier_answer": "wrapper appends telemetry; --refresh writes the shared snapshot; default/list/name/resource traversal is estate-read-only"
      },
      {
        "move": 3,
        "status": "DONE",
        "falsifier_answer": "oracle is shared generated snapshot, last_review 2026-07-30; run now names stale vintage and C(N) boundary"
      },
      {
        "move": 4,
        "status": "DONE",
        "falsifier_answer": "source JSON independently enumerates 29 names, 135 chains, 27 resource-roster keys; tool prints 29/135"
      },
      {
        "move": 5,
        "status": "DONE",
        "falsifier_answer": "source proves cma=1 chain, ceo-digest=name+0 chains+1 C0, C(N) absent; fixture proves empty N/A population"
      },
      {
        "move": 6,
        "status": "DONE",
        "falsifier_answer": "mutants are disposable sibling copies deleted in finally; snapshot/estate never mutated"
      },
      {
        "move": 7,
        "status": "DONE",
        "falsifier_answer": "ground truth from direct JSON, git blobs, and typed Observation_Record wrapper; wrapper parses positive and zero-chain headings"
      },
      {
        "move": 8,
        "status": "DONE",
        "falsifier_answer": "read-only inventory/router; hunted guard asymmetry, aging, terminal honesty, control-flow label, resource blindness, vacuity, and wiring"
      }
    ],
    "archetype": "read-only business-semantic inventory/router over a generated naming snapshot, with optional live key/AWS branches",
    "findings": [
      {
        "id": "F1",
        "shape": "aging-oracle",
        "cite": "estate-coverage-resolver.json last_review 2026-07-30",
        "text": "naming oracle is 35 days old; now disclosed and never presented as locked C(N)"
      },
      {
        "id": "F2",
        "shape": "resource-blind",
        "cite": "opal_estate_infrastructure.py:563-572 @be15852e76",
        "text": "C(N) is unavailable and is carried to NFRA_C3MATERIALIZE; zero ontology entries guessed"
      },
      {
        "id": "F3",
        "shape": "terminal-honest/artifact-lies",
        "cite": "--head help/output @be15852e76",
        "text": "true denominator survives --head, but Rule P PAGE i of N is absent"
      },
      {
        "id": "F4",
        "shape": "mislabelled-control-flow",
        "cite": "comp-passcraft recon versus .tools/comp-estate:38-58",
        "text": "recon says self-contained although shim runpy-executes engine+telemetry; repeats detector class already recorded as S25"
      },
      {
        "id": "F5",
        "shape": "correct-but-unwired",
        "cite": "CLAUDE.md:162-165; comp-tool-hud.sh:288-300",
        "text": "Build Ladder/HUD advise but do not invoke or read rc; typed Observation_Record is the only located external rc reader"
      },
      {
        "id": "F6",
        "shape": "vacuous-that-can-block",
        "cite": ".tools/tests/test_fabric_check_classify.py:76",
        "text": "directory pytest aborts collection on module-scope sys.exit(0), known PRD/T16 lane defect; T17 file is import-inert and passes alone"
      },
      {
        "id": "F7",
        "shape": "correct-but-unwired",
        "cite": "NFRA_COMPEFFICACY-S28 @718767b608be1d8b44b5168a2c4909dcc477f538",
        "text": "Codex seats share CLAUDE_CODE_SESSION_ID, corrupting supposedly per-session to_id; tool+serial counts remain usable"
      }
    ]
  },
  "usage": {
    "runs_30d": {
      "snapshot_utc": "2026-09-03T15:48:19Z",
      "runs_jsonl": {
        "count": 316,
        "by_mode": {
          "<name>": 106,
          "--resource": 47,
          "--list": 42,
          "--definitions": 72,
          "--layers": 13,
          "--matrix": 11,
          "--segments": 11,
          "--help": 6,
          "--census-drift": 3,
          "--self-test": 2,
          "--refresh": 1,
          "--gate-b": 1,
          "default/no-arg": 1
        },
        "by_caller": {
          "4.0.0_SA_CRO": 68,
          "3.0.0_SA_CVO": 68,
          "0.8.0_AE_CloudComp~H": 53,
          "1.0.0_SA_CTO": 23,
          "3.0.0_SA_CVO~A": 10,
          "1.0.0_SA_CTO~B": 10,
          "1.0.0_SA_CTO~C": 9,
          "1.0.0_SA_CTO~X": 8,
          "0.0.0_AB_MSTR": 7,
          "2.0.0_SA_COO": 7,
          "0.4.0_DS_ClientPlatform": 7,
          "0.7.0_AE_CloudOps": 6,
          "3.0.0_SA_CVO~C": 6,
          "4.0.0_SA_CRO~A": 6,
          "4.0.0_SA_CRO~B": 5,
          "0.4.0_DS_ClientPlatform~O": 4,
          "4.0.0_SA_CRO~C": 3,
          "0.4.0_DT_ClientPlatform~X": 3,
          "4.0.0_SA_CRO~X": 3,
          "1.0.0_SA_CTO~A": 2,
          "0.8.0_AE_CloudComp~X": 2,
          "0.8.0_AE_CloudComp": 2,
          "0.4.0_DS_ClientPlatform~A": 1,
          "1.0.0_SA_CTO~D": 1,
          "0.4.0_DS_ClientPlatform~B": 1,
          "0.8.0_AE_CloudComp~Y": 1
        },
        "rc": {
          "0": 258,
          "1": 6,
          "2": 52
        },
        "note": "PRD cut said 281; sink grew during audit. Count uses tool+serial+rc, not corrupt to_id (S28)."
      },
      "rail_log": {
        "invocation_rows": 0,
        "mention_rows": 2080,
        "note": "matches are routing/search intent; none has tool=comp-estate"
      }
    },
    "hook_driven": {
      "fraction": "0 of 316 (0%)",
      "basis": "executable-body census finds only advisory HUD strings; no hook executes comp-estate. Sink has no origin field, so this is wiring-derived."
    },
    "battery": {
      "path": ".tools/tests/test_comp_estate_battery.py @be15852e76",
      "arms": "7/7 direct PASS; each disposable mutant makes its arm red",
      "file_grain": "direct 7/7 rc 0; pytest file 1 passed rc 0",
      "directory_grain": "pytest .tools/tests rc 3 INTERNALERROR at test_fabric_check_classify.py:76; no tests ran in 2.08 s; pre-existing lane defect",
      "mutants": [
        "absent token",
        "zero token",
        "C(N) GUESSED-ONTOLOGY injection",
        "N/A token",
        "ignored deadline",
        "replayed cursor",
        "hidden carrier help"
      ]
    },
    "overlap": "No alias entrypoint. estate_infrastructure_cli is delegated renderer; comp-api is same-engine facade; comp-pipescript is a per-pipeline drill and comp-kuzu the graph destination, not duplicates.",
    "proposed": "CARRIED: landed answer-state and audited traversal-budget improvements; locked C(N) remains RELIES-ON NFRA_C3MATERIALIZE. Rule P and non-audited refresh/verify/census Rule T residuals also require disposition before CLEARED."
  },
  "cn_dependency": {
    "relationship": "RELIES-ON",
    "project": "NFRA_C3MATERIALIZE",
    "state_read": "active/incomplete",
    "answers_found_wrong_or_empty_because_unlocked": [
      "literal C(N) -> PARTIAL_OR_BLIND / NOT-DECIDABLE / CARRIED",
      "literal NFRA_C3MATERIALIZE -> same carried branch"
    ],
    "ontology_entries_invented_or_widened": 0
  },
  "production_identity": {
    "engine_blob_before": "1f646d7c26d95dff3af19b5eee74e81385709ff7",
    "engine_blob_after": "8feb1bb38cb35fb202399341ae358de9ac9fc471",
    "shim_blob_before_after": "e0bd92509e2ea16d494dbe1bf6262336cb95c00c (unchanged)",
    "code_commit": "be15852e764df27c631c9d410eea0a51cd442264",
    "surprise_commit": "718767b608be1d8b44b5168a2c4909dcc477f538"
  }
}
```

## Quoted live-run evidence

Default `comp-estate --list`, rc 0:

```text
comp-estate | ENGINE: org/modules/graph/opal_estate_infrastructure.py | NAMING ONTOLOGY: org/modules/graph/estate-coverage-resolver.json -- last_review 2026-07-30
  ONTOLOGY BOUNDARY: this is a generated C3.ii naming snapshot, not locked C(N). C(N) is RELIES-ON NFRA_C3MATERIALIZE; unresolved C(N) names are CARRIED there, never guessed here.
RULE T: budget: 90 s (default)
  DECLARED NON-APPLICATION for --list early-abort/resume: the generated naming snapshot is one atomic read before this mode begins.
comp-estate - 29 C3.ii semantic verticals / 135 chains (D2 = C2-motif instances) (estate census 2026-07-30)
...
TOTAL                    135
```

Default `comp-estate cma`, rc 0:

```text
comp-estate C3.ii vertical 'cma' - 1 chains (D2 = C2-motif instances) (in-scope 1 / explicit-out 0 / unreviewed 0)
...
C0 facts (1) - the CENSUS-TAXONOMY roster for 'cma'. NOT exhaustive:
...
WITHIN BUDGET: scanned 1 of 1 chain; budget: 90 s (default), used 0.046000000002095476 s
```

Expiry, `comp-estate cma --budget 0.00001`, rc 0:

```text
PREFIX ONLY: 0 of 1 chain unit(s) rendered. Whole-traversal tool census and C0 roster are DEFERRED until the resumed union completes.
ANSWER-STATE: PARTIAL_OR_BLIND
TOOL-VOICE: NOT-DECIDABLE
BUDGET REACHED: 1e-05 s (flag); scanned 0 of 1 chain(s); results are a PREFIX, not the answer; NO CURSOR YET.
```

## Consumer census and rc conclusion

`CLAUDE.md:162-165` and the HUD advise humans; neither invokes the tool or reads rc.
`comp_api.run()` catches and discards `SystemExit`. One real consumer was found:
`NFRA_EPISTEMY.C1-ENVELOPE/src/observation_envelope.py:266-300` executes the shim,
maps nonzero rc to UNKNOWN, and parses the established `comp-estate ... - N chains`
heading. Both `cma` and `ceo-digest` were exercised through it and returned all stages
SUCCEEDED. Named/resource traversal is execution-only, so Rule T expiry correctly stays rc 0;
an absent subject remains rc 2 and becomes UNKNOWN to the typed wrapper.

## C(N) boundary

Only the literal contract probes `C(N)` and `NFRA_C3MATERIALIZE` are attributed to unlocked
C(N); both are carried, not answered. Ordinary unknown names remain measured snapshot absences.
No member, alias, or structure was inferred, and `org/projects/NFRA_C3MATERIALIZE.json` was read
but not modified.
