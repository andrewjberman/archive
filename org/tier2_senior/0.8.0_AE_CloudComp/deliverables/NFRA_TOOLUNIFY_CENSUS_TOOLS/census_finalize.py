#!/usr/bin/env python3
"""Merge classifier + annotator output into the final NFRA_TOOLUNIFY register
(brief Sec3 schema, restricted to the fields Sec2.D's MUST-CLOSE list asks
for: reads[]/writes[]/binding/evaluation/failure_mode, + closure/entry as
supporting evidence). Applies documented manual overrides for tools I
source-verified directly (the 4 gate cases + spot-checks) rather than trusting
the mechanical candidate blindly everywhere."""
import json
from pathlib import Path

WS = Path(r"C:\Users\AndrewBerman\Desktop\ajb_workspace")
OUTDIR = WS / "org/tier1_exec/1.0.0_SA_CTO/deliverables/NFRA_TOOLUNIFY_CENSUS"

classifier = json.loads((OUTDIR / "_classifier_raw_output.json").read_text(encoding="utf-8"))
annotated = json.loads((OUTDIR / "_annotated_candidates.json").read_text(encoding="utf-8"))

# ---------------------------------------------------------------------------
# MANUAL OVERRIDES -- every entry here was source-read directly by me (not
# just the mechanical candidate), cited to file:line. This is the set of
# tools where I have HIGH confidence, vs the remainder which carry the
# annotator's rule-derived candidate at MEDIUM/LOW confidence (labeled).
# ---------------------------------------------------------------------------
OVERRIDES = {
    "comp-manifest-check": {
        "binding": "GUARD",
        "binding_note": "manifest_check_cli.py: every typed read (graph-call-manifest.yaml, "
                         "comp-coverage-map.yaml, comp-output-contracts.yaml, NFRA_ONTOLOGY_RULE_BANK.yaml, "
                         "the changed-files text) feeds a PASS/BLOCK verdict via the invariant functions "
                         "(_routable_invariant, _placement_invariant, _existence_invariant, "
                         "_registration_invariant, _output_contract_invariant, _stage2_vocab_invariant, "
                         "_retired_alias_invariant) -- none of it is reported as content, all of it decides "
                         "whether a commit proceeds. binding=GUARD confirmed at source (:438-1098).",
        "evaluation": "RUNTIME", "failure_mode": "LOUD",
        "failure_mode_note": "every invariant explicitly fail-closed: 'except Exception as e: print BLOCKED...; "
                              "return 1' at 7 separate call sites (:479,590,643,736,900,983,1088). An "
                              "unevaluable gate blocks, never silently passes -- source-verified.",
        "role_flags": ["GATE-BLOCKING"],
        "confidence": "HIGH -- full source read (manifest_check_cli.py, 1540 lines), FP gate case #1",
        "false_positive_reproduced": "CONFIRMED NEGATIVE: predecessor tagged this tool as touching live "
            "kuzu/graph.json content (string-presence match on the ADHOC_PATTERNS regex LITERALS at "
            ":184-228, which contain the substrings 'kuzu.Connection'/'graph.json' as TEXT BEING SEARCHED "
            "FOR in other files, not code this tool executes). My AST call-site pass shows zero "
            "KUZU-CANONICAL / graph-content hits -- every read is CONFIG (its own registries) or "
            "SOURCE-SCAN-DYNAMIC (the text of files being committed, scanned for the regex patterns). "
            "The regex pattern DEFINITIONS are re.compile() call arguments (string literals), never "
            "kuzu.Connection()/open(graph.json) call sites themselves.",
    },
    "comp-graph": {
        "binding": "LABEL",
        "binding_note": "graph_status_cli.py: every hit is .exists()/.stat()/a 512-byte read_bytes() header "
                         "peek (:74-239) -- reports FRESHNESS LABELS (FRESH/STALE/MISSING/UNVERIFIABLE) about "
                         "OTHER artifacts. Never opens graph.json/kuzu_db/stitch_graph.json for content. "
                         "Delegates the one real verdict it needs (trace-graph freshness) to the enforcer via "
                         "cli.trace_freshness() (:111-117) rather than re-modeling the predicate itself.",
        "evaluation": "DERIVED",
        "evaluation_note": "reports on the AGE/PRESENCE of derived artifacts it does not itself compute; "
                            "the graphs it labels are the derived things, this tool is a thin status layer "
                            "over them (metadata-only, per binding note).",
        "failure_mode": "LOUD",
        "failure_mode_note": "_trace_freshness() (:111-117): 'except Exception as e: return UNVERIFIABLE, "
                              "cannot reach the enforcer...' -- fail-closed to a labeled UNVERIFIABLE state, "
                              "never a silent FRESH. Also has a WRITE role via `comp-graph clear` (:314-335, "
                              ".unlink() on platinum caches + graph.json) -- a cache-invalidation mutation, "
                              "distinct from its read-only `status` mode.",
        "role_flags": ["ADVISORY", "PRODUCER-CANDIDATE(clear-mode-only, local-cache-delete)"],
        "confidence": "HIGH -- full source read (graph_status_cli.py, 361 lines), FP gate case #2",
        "false_positive_reproduced": "CONFIRMED NEGATIVE: predecessor's method would see the strings "
            "'kuzu_db'/'stitch_graph.json'/'graph.json' in this file's source and tag it a content reader of "
            "all three. Every actual call-site hit is meta_only=true (.exists/.stat) or a 512-byte bounded "
            "header peek -- zero full-content reads, zero kuzu.Connection() calls, confirmed by my AST pass.",
    },
    "comp-stitch-refresh": {
        "binding": "ANSWER-BEARING (as a producer -- see role_flags)",
        "binding_note": "the artifact IT WRITES (stitch_graph.json/stitch_marker.json) is the answer it "
                         "produces for every downstream consumer; its own reads (S3 AWS-snapshot fetch, "
                         "local repo scan via derive_stitch.py) feed that output directly, not a gate.",
        "evaluation": "RUNTIME", "failure_mode": "LOUD",
        "failure_mode_note": "wrapper (.tools/comp-stitch-refresh:47-57): rc=2 from derive_stitch.py "
                              "(grain-sentinel FAIL) -> 'ERROR: refusing to publish' + exit 2, hard abort, "
                              "NO artifact written. Empty artifact -> exit 1. Marker upload failure after "
                              "artifact upload succeeded is explicitly called out as SAFE-NOT-HALF-PUBLISHED "
                              "(:83-85) -- deliberate two-phase publish discipline (artifact first, marker "
                              "= the atomic commit point, last).",
        "role_flags": ["PRODUCER"],
        "confidence": "HIGH -- full source read (comp-stitch-refresh wrapper + derive_stitch.py header), "
                       "FP gate case #3",
        "false_positive_reproduced": "CONFIRMED NEGATIVE, AND A REAL BUG FOUND+FIXED IN MY OWN CLASSIFIER "
            "ALONG THE WAY: my first pass mis-classified the two `aws s3 cp \"$ART\" \"s3://...\" --quiet || "
            "{ ...error handling... }` lines as READS, because the bash write-direction check inspected the "
            "LAST TOKEN OF THE WHOLE LINE (which was inside the `|| { }` error-handler clause, not the s3:// "
            "destination) -- then, after isolating just the command portion, failed AGAIN because the token "
            "was quoted (`\"s3://...\"` does not literally start with `s3://`, it starts with a quote mark). "
            "Both fixed (isolate the command before `||`/`&&`/`;`; strip quote chars before the prefix check). "
            "Confirmed post-fix: writes_typed.LIVE-AWS now correctly shows both S3 uploads; reads_typed shows "
            "only the boto3 AWS-snapshot FETCH. This is the exact producer-vs-consumer class the gate exists "
            "to catch, and it caught it in my own tool before I could ship it wrong.",
    },
    "comp-blast": {
        "reads_add_note": "TRANSITIVE closure (30 modules via cli.py) includes org/modules/graph/"
            "nerves_resolve.py -- the KNOWN-MISSED FN CASE. Reachable via cli.py:376-392 "
            "(_print_risk_by_ref), a FUNCTION-LOCAL deferred import (`from nerves_resolve import resolve as "
            "_resolve` at :383, inside a try/except, itself inside a function only called on the NOT-FOUND "
            "path of a node lookup) -- invisible to any depth-1 or module-top-level-only import scan. "
            "nerves_resolve.py:73-74 (_trace_graph()) does `TraceGraph.load(cache) if cache.exists() else "
            "None` -- existence-guarded but NOT vintage/freshness-guarded (no SHA-drift check, unlike cli.py's "
            "own primary _get_graph() path) -- vintage_discipline=SILENT for this specific read path, "
            "distinct from cli.py's own GUARDED-REBUILD primary path. Same graph.json, two different "
            "discipline levels depending on which internal path reaches it -- itself a finding.",
        "false_negative_found": "CONFIRMED: nerves_resolve.py IS in the closure (verified via "
            "closure_modules), reachable only through a function-local deferred import 2+ hops deep -- "
            "exactly the shape a depth-1 scanner (the predecessor method) would miss. FN gate case, closed.",
    },
    "comp-trace": {"reads_add_note": "same nerves_resolve.py transitive reachability as comp-blast (shared cli.py backing)."},
    "comp-diff": {"reads_add_note": "same nerves_resolve.py transitive reachability as comp-blast (shared cli.py backing)."},
    "comp-xref": {"reads_add_note": "same nerves_resolve.py transitive reachability as comp-blast (shared cli.py backing)."},
    "comp-to": {
        "reads": {}, "writes": {"CONFIG": [{"detail": "org/mcp/sessions/<session>.to_id -- session-scoped "
                    "race-free TO_ID file (bash printf redirect, not python -- outside AST scan scope by "
                    "construction)"}]},
        "binding": "CONFIG", "evaluation": "RUNTIME", "failure_mode": "FAIL-OPEN",
        "failure_mode_note": "no CLAUDE_CODE_SESSION_ID -> prints a WARN + fallback instructions and exits "
                              "0 (not a hard failure) -- degrades to the legacy shared-file mechanism rather "
                              "than blocking. Genuinely minimal tool: pure bash, no Python backing at all "
                              "(confirmed by direct read, 26 lines total).",
        "role_flags": ["CONFIG"], "confidence": "HIGH -- full source read (26-line bash script, no python)",
    },
}

FIELD_KEYS = ("tool", "entry", "closure", "reads", "writes", "binding", "evaluation", "refresh",
              "vintage_discipline", "denominator", "failure_mode", "role_flags", "registry_state", "owner")


def main():
    rows = {}
    for tool, c in classifier.items():
        a = annotated.get(tool, {})
        ov = OVERRIDES.get(tool, {})
        confidence = ov.get("confidence", "MEDIUM -- AST/call-site grounded reads+writes+closure; "
                                           "binding/evaluation/failure_mode rule-derived + spot-checked, "
                                           "not individually source-read")
        row = {
            "tool": tool,
            "entry": c.get("entry_modules"),
            "closure_size": c.get("closure_size"),
            "closure": c.get("closure_modules"),
            "reads": ov.get("reads", c.get("reads_typed", {})),
            "writes": ov.get("writes", c.get("writes_typed", {})),
            "unresolved_call_sites_count": len(c.get("unresolved_call_sites", [])),
            "binding": ov.get("binding", a.get("binding_candidate", "UNKNOWN")),
            "binding_note": ov.get("binding_note", a.get("binding_note", "")),
            "evaluation": ov.get("evaluation", a.get("evaluation_candidate", "UNKNOWN")),
            "evaluation_note": ov.get("evaluation_note", a.get("evaluation_note", "")),
            "failure_mode": ov.get("failure_mode", a.get("failure_mode_candidate", "UNKNOWN")),
            "failure_mode_note": ov.get("failure_mode_note", a.get("failure_mode_note", "")),
            "role_flags": ov.get("role_flags", a.get("role_flags_candidate", [])),
            "confidence": confidence,
        }
        if "reads_add_note" in ov:
            row["reads_note"] = ov["reads_add_note"]
        if "false_positive_reproduced" in ov:
            row["false_positive_reproduced"] = ov["false_positive_reproduced"]
        if "false_negative_found" in ov:
            row["false_negative_found"] = ov["false_negative_found"]

        # ZERO UNKNOWN WITHOUT A NAMED REASON (plan Sec2.D acceptance). A
        # remaining UNKNOWN failure_mode means the quick text-scan found no
        # dominant sys.exit/raise/except-swallow pattern -- almost always
        # because the tool uses the codebase's `def main() -> int: ...
        # sys.exit(main())` indirect-return idiom, which routes its actual
        # exit code through a return statement my regex doesn't trace. Rather
        # than ship a bare "UNKNOWN", apply this codebase's OWN documented,
        # repeatedly-observed convention (CLAUDE.md's own governing language:
        # "AN INSTRUMENT THAT CANNOT FAIL IS NOT AN INSTRUMENT"; verified
        # directly in comp-manifest-check, comp-graph, comp-secrets,
        # comp-deadgrant, nerves_resolve.py) as a NAMED, LOW-confidence
        # default -- honest about being a convention, not a per-tool proof.
        if row["failure_mode"] == "UNKNOWN":
            row["failure_mode"] = "LOUD (default)"
            row["failure_mode_note"] = ("quick text-scan found no direct sys.exit(1|2)/raise literal -- "
                "likely the codebase's `def main() -> int: ...; sys.exit(main())` indirect-return idiom, "
                "which routes the real exit code through a return the scan doesn't trace. Defaulted to LOUD "
                "per this codebase's repeatedly-verified house convention (fail-closed, explicit ERROR/"
                "BLOCKED messaging) rather than left UNKNOWN -- NOT individually source-verified for this "
                "specific tool. LOW CONFIDENCE, named reason.")
            row["confidence"] = "LOW -- failure_mode is a named-reason convention default, not source-verified for this tool"
        rows[tool] = row

    outpath = OUTDIR / "D.sidecar.json"
    outpath.write_text(json.dumps({
        "census": "NFRA_TOOLUNIFY_CENSUS Sec2.D -- tool-to-source map",
        "lane": "0.8.0_AE_CloudComp~D", "date": "2026-07-24",
        "denominator": {
            "raw_comp_star_files": 91,
            "plus_pipescript_nonprefixed": 1,
            "total_rowed": len(rows),
            "reconciliation": "91 raw .tools/comp-* files (any extension) + 1 non-comp-prefixed sibling "
                "(pipescript) = 92 rowed. Of the 91: 5 are .py BACKING IMPLEMENTATIONS whose extensionless "
                "wrapper is ALSO in the 91 (comp-deadgrant/.py, comp-denytest/.py, comp-firmsep-sweep/.py, "
                "comp-tagauthz/.py, comp-whoread/.py -- same tool, invoking the wrapper runs the .py, so "
                "excluding the .py dup from a TOOL count is correct); 2 are genuinely unrepresented test "
                "harnesses with no wrapper counterpart (comp-which-routing-test.py, "
                "comp-v5-composite-test.sh). 91 - 7 = 84 (matches comp-manifest-check's own "
                "registration-invariant universe count, which globs comp-* only, post-dedup); 84 + "
                "pipescript = 85 (matches the predecessor brief's ~85 figure). Re-derived independently via "
                "`find .tools -maxdepth 1 -iname comp-*` + manual classification, not quoted from CTO~Z/"
                "CVO~Z's steer (which stated the same reconciliation).",
        },
        "rows": rows,
    }, indent=2), encoding="utf-8")
    print(f"Wrote {outpath} -- {len(rows)} rows")

    # quick coverage stats for the deliverable
    unknown_binding = [t for t, r in rows.items() if r["binding"] == "UNKNOWN"]
    unknown_eval = [t for t, r in rows.items() if r["evaluation"] == "UNKNOWN"]
    unknown_fm = [t for t, r in rows.items() if r["failure_mode"] == "UNKNOWN"]
    print(f"UNKNOWN binding: {len(unknown_binding)} {unknown_binding}")
    print(f"UNKNOWN evaluation: {len(unknown_eval)} {unknown_eval}")
    print(f"UNKNOWN failure_mode: {len(unknown_fm)} {unknown_fm}")


if __name__ == "__main__":
    main()
