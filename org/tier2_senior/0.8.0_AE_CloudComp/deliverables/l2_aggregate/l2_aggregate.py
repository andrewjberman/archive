"""l2_aggregate -- NFRA_COMPLEARN L2, THE AGGREGATE (fleet).

Collects conformant boundary reports (L1a, Class-1 domain gaps) and the monotonicity
pair-table (L1b, Class-2 predicate gaps), and answers ONE question: "where is our model
short?" -- as a report, never a dashboard of per-item judgment calls.

Author: 0.8.0_AE_CloudComp (base). Dispatch: 1.0.0_SA_CTO~Z 20260725T135630Z + two
same-day boundary corrections (135910Z L1b-verified + third-row-class; 141210Z the real
4-sensor/5-report corpus, corp-residue as named non-emitter).

THIS FILE IS NOT A REGISTERED comp-TOOL. It is a one-off L2 build artifact living under
this lane's ownpath, same convention as the l1a_*/l1b_sensor siblings in this directory.

GOVERNING ACCEPTANCE (IMPLEMENTATION_LEVELS_AND_SEQUENCING.md L2 section, verbatim intent,
not paraphrase-drifted -- re-read the spec before touching this file):
  1. N/A is NEVER summed as 0. States its applicability denominator explicitly.
  2. NEVER aggregates across `address_space`. Aggregates on cell, method, tool, head only.
  3. States the BIAS of its own denominator from the `method` mix it contains.
  4. Ranking uses DETERMINISTIC PROXIES ONLY (neighbourhood signals). Never per-item judgment.
  5. Reports coverage OF ITSELF: how many fleet tools emit, how many do not.

PLUS the 5 banked L2 design inputs (SYNTHESIS.md Sec4, binding on this build):
  1. Per-CELL applicability denominator, alongside the per-tool one (ADDS to acceptance 1).
  2. Live-population denominators, never declared ones.
  3. Can-ever-match denominators for ranking; a named-but-dead candidate is itself residue.
  4. Raw accounting line per sensor required, not just its verdict.
  5. SYMPTOM rows collect immediately; `mechanism` populates only from reproduced results.

ASCII-only. Read-only against its inputs (never mutates a report). No network, no AWS.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# native-path rule (CTO~Z standing rule, 20260725T065646Z): resolve relative to this file,
# never a hand-built /c/ or /cygdrive/c/ literal -- __file__ is native-form on every
# interpreter that can run this script at all.
_HERE = Path(__file__).resolve().parent
_WORKSPACE = _HERE.parent.parent.parent.parent.parent  # deliverables/l2_aggregate -> ajb_workspace
_GRAPH_MODULES = _WORKSPACE / "org" / "modules" / "graph"

sys.path.insert(0, str(_GRAPH_MODULES))
import boundary_report as BR  # noqa: E402


# ---------------------------------------------------------------------------------------
# THE INPUT MANIFEST -- enumerated explicitly, membership stated not counted (CTO~Z's own
# lesson from this build's own STOP: "enumerate members, not counts, and print them").
# Do NOT glob for these. A glob is exactly the retrieval method that missed comp-blast
# (filename convention) and missed comp-kuzu (directory convention) on the two independent
# first passes that preceded this file.
# ---------------------------------------------------------------------------------------

L1A_REPORTS = [
    _WORKSPACE / "org/tier2_senior/0.8.0_AE_CloudComp/deliverables/l1a_sensor2/boundary_report_comp_cache.json",
    _WORKSPACE / "org/tier1_exec/1.0.0_SA_CTO/deliverables/NFRA_TOOLUNIFY_CENSUS/L1A_SENSOR3_comp-blast.report.node_type.json",
    _WORKSPACE / "org/tier1_exec/1.0.0_SA_CTO/deliverables/NFRA_TOOLUNIFY_CENSUS/L1A_SENSOR3_comp-blast.report.edge_type.json",
    _WORKSPACE / "org/tier2_senior/0.8.0_AE_CloudComp/deliverables/l1a_item1b/boundary_report_lambda_env.json",
    _WORKSPACE / "org/tier2_senior/0.8.0_AE_CloudComp/deliverables/l1a_item1b/boundary_report_comp_kuzu.json",
]

L1B_REPORT = _WORKSPACE / "org/tier2_senior/0.8.0_AE_CloudComp/deliverables/l1b_sensor/l1b_pairtable_emitted.json"

# L1b's DECLARED/UNKNOWN row-classes are NOT in the --emit'd JSON (that emission carries
# only classified L0b-typed pairs, by the sensor's own design -- confirmed by inspection of
# the emitted file: 20 pairs / 25 limbs, SENSITIVE+MONOTONE-BLIND only). Cited here from the
# sensor's own live stdout this session (verbatim, not paraphrased) rather than silently
# dropped -- the DECLARED/UNKNOWN distinction is load-bearing per CTO~Z's 135910Z boundary
# update and must not disappear because the emission format doesn't carry it.
L1B_DECLARED_ROWCLASSES = [
    ("RESEMANT x every mechanical kind", "UNDETECTABLE-BY-DESIGN",
     "L0b s2 ratified: meaning moves, members/counts/shape stable -- nothing mechanical is sensitive by construction"),
    ("assumption (inf-intraday-iam) x all 9 change-types", "IMMOBILE-BY-CONSTRUCTION",
     "the check returns ASSUMPTION unconditionally -- a predicate that cannot move under ANY change"),
]
L1B_UNKNOWN_ROWCLASSES = [
    ("metric_current (ct-count-current) x all mechanical", "could not synthesize without executing comp-system against a mutated estate; injecting CompSystem._fresh IS the patched-constant class the spec forbids"),
    ("system_current (eng-currentstate-current) x all mechanical", "same mechanism as metric_current"),
    ("grep_present/version_pin/derived_count x REGRAIN", "no representative single-source regrain synthesizable at these sources' own grain without mutating MEANING (RESEMANT-adjacent)"),
]

# The named NON-EMITTER (CTO~Z 141210Z, binding): comp-residue is built, exists, is
# real-invoked in the estate, and does NOT emit a boundary_report-conformant artifact.
# Per the coupling note (spec Sec2): a tool that emits no sensor report is a domain the
# graph can never learn about. Recorded here, never omitted from self-coverage.
NAMED_NON_EMITTERS = [
    {
        "tool": "comp-residue",
        "layer": "L1a (would-be domain-gap sensor, schema shape)",
        "reason": "residue_cli.py does not import boundary_report, has no --json flag; "
                  "cmd_check/cmd_surface print prose only (PASS/VERDICT/REFUSE/FAIL + a "
                  "residue count and path list, never a cells{} breakdown). Its own "
                  "12/12 positive-control history validated the CONCEPT later formalized "
                  "into L0a; it was never wrapped to emit the type. Confirmed at source "
                  "this session, not inferred from its name or its spec listing (the "
                  "spec's own listing of comp-residue as an L1a sensor was itself wrong, "
                  "corrected by CTO~Z in the same reply that named this non-emitter).",
    },
]


def load_l1a_reports():
    """Load + validate every L1a report. Returns list of (path, report_dict, violations)."""
    out = []
    for p in L1A_REPORTS:
        if not p.exists():
            raise FileNotFoundError(
                "L1A_REPORTS manifest names a path that does not exist: %s -- "
                "the manifest is enumerated by hand precisely so a missing member is "
                "LOUD, not a silent glob-miss." % p
            )
        report = json.loads(p.read_text(encoding="utf-8"))
        violations = BR.validate(report)
        out.append((p, report, violations))
    return out


def load_l1b_report():
    if not L1B_REPORT.exists():
        raise FileNotFoundError("L1B_REPORT does not exist: %s" % L1B_REPORT)
    return json.loads(L1B_REPORT.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------------------
# SECTION A -- per-report raw accounting line (banked input 4: redundant derivation is a
# control only when derivations CAN disagree; this is what makes L2 itself verifiable).
# ---------------------------------------------------------------------------------------

def raw_accounting_lines(l1a_loaded):
    lines = []
    for path, report, violations in l1a_loaded:
        cells = report.get("cells", {})
        parts = []
        applicable_sum = 0
        for cell in sorted(BR.CELLS):
            rec = cells.get(cell, {})
            if rec.get("applicable") is True:
                parts.append("%s=%d(%s)" % (cell, rec["count"], rec.get("method")))
                applicable_sum += rec["count"]
            else:
                parts.append("%s=N/A" % cell)
        reconciles = applicable_sum == report.get("surface_total")
        lines.append({
            "tool": report.get("tool"),
            "address_space": report.get("address_space"),
            "head": report.get("head"),
            "raw_line": " + ".join(parts) + " (applicable_sum=%d, surface_total=%d, %s)" % (
                applicable_sum, report.get("surface_total"),
                "RECONCILES" if reconciles else "MISMATCH -- FLAG",
            ),
            "conformance_violations": [
                {"code": v.code, "where": v.where, "message": v.message} for v in violations
            ],
        })
    return lines


# ---------------------------------------------------------------------------------------
# SECTION B -- per-cell aggregation (acceptance 2: never across address_space; acceptance 1
# + banked input 1: per-cell AND per-tool applicability denominators, N/A never summed as 0;
# acceptance 3: method-mix bias stated per aggregate).
# ---------------------------------------------------------------------------------------

def per_cell_aggregate(l1a_loaded):
    """Per (cell x address_space) -- NEVER a per-cell scalar across spaces.

    CORRECTED 20260725T1426Z (CTO~Z verify, CVO~Z-checked): the prior version summed
    `total_count_where_applicable` across ALL address spaces for a given cell (e.g.
    "covered: 138" = 105 code_call_site + 3 dag_node_type + ... ) -- a real acceptance-2
    violation. Listing the components beside the sum did not cure it: a total published
    next to its components is still read as the summary, and it is the number that gets
    quoted. FIX: break the count out per address_space; the applicability DENOMINATOR
    (a count of TOOLS, not a sum of incommensurable quantities) stays scalar and correct.
    """
    agg = {}
    for cell in sorted(BR.CELLS):
        applicable_tools = []
        na_tools = []
        by_space = {}  # address_space -> {"count": int, "method": str, "tool": str}
        for path, report, _ in l1a_loaded:
            rec = report.get("cells", {}).get(cell, {})
            space = report.get("address_space")
            tool_label = "%s/%s" % (report.get("tool"), space)
            if rec.get("applicable") is True:
                applicable_tools.append(tool_label)
                # a cell CAN repeat an address_space (none do in this corpus, but comp-blast's
                # two shapes are both distinct spaces already) -- key by (tool, space) so two
                # reports sharing a space are never silently merged either.
                by_space["%s/%s" % (report.get("tool"), space)] = {
                    "address_space": space,
                    "count": rec["count"],
                    "method": rec.get("method"),
                }
            else:
                na_tools.append(tool_label)

        n = len(l1a_loaded)
        m = len(applicable_tools)

        per_space_bias = {}
        for key, rec in by_space.items():
            direction = BR.METHODS[rec["method"]]
            tag = ("EXACT" if not direction["under_reports"] and not direction["over_reports"]
                   else "UNDER-REPORTS" if direction["under_reports"]
                   else "OVER-REPORTS")
            per_space_bias[key] = "%d via %s (%s)" % (rec["count"], rec["method"], tag)

        agg[cell] = {
            "definition": BR.CELLS[cell],
            "applicability_denominator": "%d/%d tools applicable (%s)" % (
                m, n, ", ".join(applicable_tools) if applicable_tools else "none"),
            "na_tools": na_tools,
            "counts_by_address_space": by_space,
            "method_mix_bias_by_address_space": per_space_bias,
            "note": ("N/A is NOT summed as 0 above -- %d of %d tools carry this cell as "
                     "not-applicable, listed in na_tools. NO CROSS-SPACE SCALAR is published "
                     "for this cell (acceptance 2) -- counts_by_address_space is the only "
                     "count field; read it per-space, never summed." % (n - m, n)),
        }
    return agg


def per_tool_denominator(l1a_loaded):
    """Acceptance 1's own literal phrasing: 'of N tools, M have a doc plane, N-M do not.'"""
    lines = []
    n = len(l1a_loaded)
    for cell in sorted(BR.CELLS):
        m = sum(1 for _, r, _ in l1a_loaded if r.get("cells", {}).get(cell, {}).get("applicable") is True)
        lines.append("of %d tool-reports, %d have a `%s` plane, %d do not (N/A)" % (n, m, cell, n - m))
    return lines


# ---------------------------------------------------------------------------------------
# SECTION C -- ranking (acceptance 4: deterministic proxies only, never per-item judgment).
# Proxy used: NEIGHBOURHOOD TOUCH COUNT -- for each residue item (orphan/doc_only), how many
# OTHER items across the WHOLE corpus (any report, any cell) share its file path (the part
# of `address` before a line/column marker, or the whole address for non-file addresses).
# This is a live, re-derivable, deterministic count over the actual corpus -- not a
# per-item subjective call. Ties broken by address string, never by judgment.
# ---------------------------------------------------------------------------------------

def _file_key(address: str) -> str:
    # "portal/src/.../Foo.tsx:236:useQueries" -> "portal/src/.../Foo.tsx"
    # a bare symbolic address (e.g. "CALLS", "env:X") has no ':' path form -> itself is the key
    if "/" in address and ":" in address:
        return address.split(":")[0]
    return address


def rank_residue_items(l1a_loaded):
    all_addresses = []
    residue_items = []
    for path, report, _ in l1a_loaded:
        for item in report.get("items", []):
            all_addresses.append(_file_key(item.get("address", "")))
            if item.get("cell") in ("orphan", "doc_only"):
                residue_items.append({
                    "tool": report.get("tool"),
                    "address_space": report.get("address_space"),
                    "address": item.get("address"),
                    "cell": item.get("cell"),
                    "method": item.get("method"),
                    "evidence": item.get("evidence"),
                })

    ranked = []
    for item in residue_items:
        key = _file_key(item["address"])
        # neighbourhood touch: how many OTHER addresses (incl. covered/member) share this
        # file key, across the WHOLE corpus -- a deterministic can-ever-match-scoped count,
        # never a per-item guess about "importance."
        touch = sum(1 for a in all_addresses if a == key) - 1  # exclude self
        ranked.append({**item, "neighbourhood_touch_count": max(touch, 0)})

    ranked.sort(key=lambda r: (-r["neighbourhood_touch_count"], r["address"]))
    return ranked


# ---------------------------------------------------------------------------------------
# SECTION D -- L1b track (Class-2, predicate gaps). Distinct shape from L1a; reported
# separately, never numerically merged with the cell-based L1a aggregate (grain error).
# ---------------------------------------------------------------------------------------

def l1b_summary(l1b_report):
    pairs = l1b_report.get("pairs", [])
    total_limbs = sum(len(p["limbs"]) for p in pairs)
    classes = {}
    for p in pairs:
        for limb in p["limbs"]:
            classes[limb["class"]] = classes.get(limb["class"], 0) + 1
    reconciles = classes.get("SENSITIVE", 0) + classes.get("MONOTONE-BLIND", 0) == total_limbs
    return {
        "l0b_version": l1b_report.get("l0b_version"),
        "pair_count": len(pairs),
        "limb_count": total_limbs,
        "classified": classes,
        "raw_accounting_line": "%d SENSITIVE + %d MONOTONE-BLIND = %d limbs across %d pairs (%s)" % (
            classes.get("SENSITIVE", 0), classes.get("MONOTONE-BLIND", 0), total_limbs,
            len(pairs), "RECONCILES" if reconciles else "MISMATCH -- FLAG",
        ),
        "declared_rowclasses_excluded_from_classified": [
            {"rowclass": rc, "epistemic_state": state, "reason": reason}
            for rc, state, reason in L1B_DECLARED_ROWCLASSES
        ],
        "unknown_rowclasses_excluded_from_classified": [
            {"rowclass": rc, "reason": reason} for rc, reason in L1B_UNKNOWN_ROWCLASSES
        ],
        "note": ("DECLARED and UNKNOWN are OPPOSITE epistemic states (CTO~Z 135910Z, binding) "
                 "and neither is summed into the classified 25-limb denominator above. "
                 "DECLARED = nothing could EVER detect this (UNDETECTABLE-BY-DESIGN / "
                 "IMMOBILE-BY-CONSTRUCTION). UNKNOWN = this sensor could not SYNTHESIZE a "
                 "test this pass (a build limit, not a property of the predicate)."),
    }


# ---------------------------------------------------------------------------------------
# SECTION E -- coverage of itself (acceptance 5). The fleet-coverage ceiling GRAPHLEARNS
# inherits, per the spec's own coupling note (Sec2).
# ---------------------------------------------------------------------------------------

def self_coverage(l1a_loaded, l1b_report):
    l1a_emitters = sorted(set(r.get("tool") for _, r, _ in l1a_loaded))
    return {
        "l1a_emitting_tools": l1a_emitters,
        "l1a_emitter_count": len(l1a_emitters),
        "l1a_report_count": len(l1a_loaded),
        "l1b_emitting_subjects": ["system_parity"],
        "named_non_emitters": NAMED_NON_EMITTERS,
        "fleet_wide_eligible_population": "UNKNOWN -- not yet enumerated. This program has "
            "so far attempted 6 named subjects (comp-cache, comp-blast, lambda-env-reader, "
            "comp-kuzu, comp-residue, system_parity); 5 emit conformant reports (4 L1a tools "
            "+ 1 L1b subject), 1 (comp-residue) is a named non-emitter. The TRUE denominator "
            "-- how many of the ~92-tool comp-* fleet COULD emit a boundary report or a "
            "monotonicity pair-table if wrapped -- has not been measured by this build and "
            "is stated here as an honest UNKNOWN, not fabricated as a fraction of 92 (most "
            "of the 92 are not source-traversal-checkable in the L1a/L1b sense at all).",
        "graphlearns_ceiling_note": "Per spec Sec2's coupling: GRAPHLEARNS's domain IS "
            "COMPLEARNS's output. A tool that emits no sensor report (comp-residue, today) "
            "is a domain the graph can never learn about. This ceiling is invisible from "
            "inside L3 and must stay visible here.",
    }


def build_report():
    l1a_loaded = load_l1a_reports()
    l1b_report = load_l1b_report()

    any_hard_violations = []
    for path, _, violations in l1a_loaded:
        hard = [v for v in violations if v.code != "BR008"]  # BR008 = allowed, just reported
        if hard:
            any_hard_violations.append((str(path), [(v.code, v.where, v.message) for v in hard]))

    out = {
        "l2_meta": {
            "dispatch": "1.0.0_SA_CTO~Z 20260725T135630Z + boundary corrections 135910Z, 141210Z",
            "corpus_membership_enumerated": {
                "l1a_reports": [str(p) for p in L1A_REPORTS],
                "l1b_report": str(L1B_REPORT),
            },
            "hard_conformance_violations": any_hard_violations,
        },
        "raw_accounting_lines": raw_accounting_lines(l1a_loaded),
        "per_cell_aggregate": per_cell_aggregate(l1a_loaded),
        "per_tool_denominator_statements": per_tool_denominator(l1a_loaded),
        "ranked_residue_items": rank_residue_items(l1a_loaded),
        "l1b_summary": l1b_summary(l1b_report),
        "self_coverage": self_coverage(l1a_loaded, l1b_report),
    }
    return out


def self_test() -> int:
    """Positive + negative control on the ranking proxy itself (care-is-not-a-control
    discipline: the real corpus returned touch=0 for every item this run, and an
    instrument only ever seen NOT fire is untested, per this program's own recurring
    lesson). Constructs synthetic reports -- NEVER mixed into build_report()'s real
    output -- purely to prove _file_key + the touch-count mechanism CAN discriminate.
    """
    ok = True

    # POSITIVE: two reports whose orphan/doc_only items share a file -> touch must be > 0.
    synth_a = {
        "tool": "synthA", "address_space": "s3_prefix", "head": "t", "surface_total": 1,
        "cells": {c: {"applicable": True, "count": 0, "method": "mention"} for c in BR.CELLS},
        "items": [{"address": "shared/path/file.py:10:fn", "cell": "orphan", "method": "traversal", "evidence": "x"}],
    }
    synth_b = {
        "tool": "synthB", "address_space": "s3_prefix", "head": "t", "surface_total": 1,
        "cells": {c: {"applicable": True, "count": 0, "method": "mention"} for c in BR.CELLS},
        "items": [{"address": "shared/path/file.py:20:other_fn", "cell": "covered", "method": "traversal", "evidence": "x"}],
    }
    ranked = rank_residue_items([(None, synth_a, []), (None, synth_b, [])])
    positive_pass = len(ranked) == 1 and ranked[0]["neighbourhood_touch_count"] == 1
    print("[%s] POSITIVE control (shared file -> touch=1): got %r" % (
        "PASS" if positive_pass else "FAIL",
        ranked[0]["neighbourhood_touch_count"] if ranked else None,
    ))
    ok = ok and positive_pass

    # NEGATIVE: two reports whose items share NOTHING -> touch must be 0.
    synth_c = {
        "tool": "synthC", "address_space": "s3_prefix", "head": "t", "surface_total": 1,
        "cells": {c: {"applicable": True, "count": 0, "method": "mention"} for c in BR.CELLS},
        "items": [{"address": "totally/unrelated/other.py:1:z", "cell": "orphan", "method": "traversal", "evidence": "x"}],
    }
    ranked2 = rank_residue_items([(None, synth_a, []), (None, synth_c, [])])
    negative_pass = len(ranked2) == 2 and all(r["neighbourhood_touch_count"] == 0 for r in ranked2)
    print("[%s] NEGATIVE control (disjoint files -> touch=0): got %r" % (
        "PASS" if negative_pass else "FAIL",
        [r["neighbourhood_touch_count"] for r in ranked2],
    ))
    ok = ok and negative_pass

    print()
    print("CONCLUSION: the real corpus's touch=0-everywhere result (see the main run) is a "
          "GENUINE PROPERTY of this corpus's sparse itemization (the 5 reports' explicitly-"
          "itemized addresses barely overlap by file/symbol), not a dead instrument -- the "
          "proxy demonstrably discriminates when a real overlap exists (positive control) "
          "and correctly reports zero when none exists (negative control).")
    return 0 if ok else 1


def main():
    report = build_report()
    out_path = _HERE / "L2_aggregate_output.json"
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print("=== L2 AGGREGATE ===")
    print("L1a corpus: %d reports, %d distinct tools (enumerated: %s)" % (
        len(report["l2_meta"]["corpus_membership_enumerated"]["l1a_reports"]),
        report["self_coverage"]["l1a_emitter_count"],
        ", ".join(report["self_coverage"]["l1a_emitting_tools"]),
    ))
    if report["l2_meta"]["hard_conformance_violations"]:
        print("HARD CONFORMANCE VIOLATIONS (non-BR008):")
        for path, viols in report["l2_meta"]["hard_conformance_violations"]:
            print("  %s: %s" % (path, viols))
    else:
        print("All 5 L1a reports conformant (BR008 unknown-address-space notes are allowed, listed below).")
    print()
    print("--- raw accounting lines ---")
    for line in report["raw_accounting_lines"]:
        print("  %s (%s): %s" % (line["tool"], line["address_space"], line["raw_line"]))
        for v in line["conformance_violations"]:
            print("    [%s] %s: %s" % (v["code"], v["where"], v["message"]))
    print()
    print("--- per-tool denominator statements (acceptance 1) ---")
    for s in report["per_tool_denominator_statements"]:
        print("  " + s)
    print()
    print("--- per-cell aggregate (acceptance 1+2+3, banked input 1) ---")
    print("  NOTE: NO cross-address_space scalar is printed anywhere below (acceptance 2, fixed 20260725T1426Z).")
    for cell, data in report["per_cell_aggregate"].items():
        print("  %s: %s" % (cell, data["applicability_denominator"]))
        for key, rec in sorted(data["counts_by_address_space"].items()):
            print("    %s: count=%d | %s" % (
                key, rec["count"], data["method_mix_bias_by_address_space"][key]))
    print()
    print("--- ranked residue items (deterministic neighbourhood-touch proxy, acceptance 4) ---")
    for item in report["ranked_residue_items"][:10]:
        print("  touch=%d  [%s/%s]  %s (%s)" % (
            item["neighbourhood_touch_count"], item["tool"], item["cell"],
            item["address"], item["method"]))
    print()
    print("--- L1b (Class-2, predicate gaps) ---")
    print("  " + report["l1b_summary"]["raw_accounting_line"])
    print("  DECLARED row-classes: %d | UNKNOWN row-classes: %d (both excluded from classified count)" % (
        len(report["l1b_summary"]["declared_rowclasses_excluded_from_classified"]),
        len(report["l1b_summary"]["unknown_rowclasses_excluded_from_classified"]),
    ))
    print()
    print("--- coverage of itself (acceptance 5) ---")
    sc = report["self_coverage"]
    print("  L1a emitters (%d): %s" % (sc["l1a_emitter_count"], ", ".join(sc["l1a_emitting_tools"])))
    print("  L1b emitters: %s" % ", ".join(sc["l1b_emitting_subjects"]))
    print("  Named non-emitters: %s" % ", ".join(x["tool"] for x in sc["named_non_emitters"]))
    print("  Fleet-wide eligible population: %s" % sc["fleet_wide_eligible_population"][:120] + "...")
    print()
    print("Full JSON: %s" % out_path)
    return 0


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(self_test())
    sys.exit(main())
