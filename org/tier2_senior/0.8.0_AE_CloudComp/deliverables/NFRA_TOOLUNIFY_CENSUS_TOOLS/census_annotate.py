#!/usr/bin/env python3
"""
Second pass: derive evaluation / failure_mode / binding / role_flags from the
classifier's grounded reads_typed/writes_typed/closure output, via EXPLICIT,
GENERAL rules (never a per-tool special case -- CVO~Z's held-back-case gate
is specifically testing that this generalizes past the 4 published examples).

Confidence is tracked per field per tool so the deliverable can say, honestly,
which rows got a full source read vs a rule-derived default -- "could not
verify to full confidence" is a valid, printed finding, not something to
paper over.
"""
from __future__ import annotations
import json
import re
from pathlib import Path

WS = Path(r"C:\Users\AndrewBerman\Desktop\ajb_workspace")
RAW = WS / "org/tier1_exec/1.0.0_SA_CTO/deliverables/NFRA_TOOLUNIFY_CENSUS/_classifier_raw_output.json"

DERIVED_KINDS = {"FROZEN-SNAPSHOT", "DERIVED-CACHE", "KUZU-CANONICAL", "ICEBERG-DIRECT"}
RUNTIME_KINDS = {"LIVE-AWS", "SOURCE-SCAN", "SOURCE-SCAN-DYNAMIC", "CONFIG"}

GATE_NAME_MARKERS = ("check", "gate", "validate", "denytest", "routable-check", "surface-check")


# auto-attached to ~55/92 closures (every tool's comp_log_auto.py trailer +
# comp_output_contract.py declaration) -- pure shared infrastructure, never
# distinctive of any ONE tool's own failure-handling style. Included them in
# a first pass and the failure_mode distribution came back ~49% FAIL-OPEN,
# implausibly high; comp_log_auto.py alone carries 16 `except` blocks (its
# OWN best-effort logging discipline) that were drowning out each tool's
# actual primary logic. Excluded from the TEXT SCAN only -- still correctly
# counted in reads[]/writes[]/closure_size, which is real.
_SHARED_INFRA_MODULES = {
    "org/modules/graph/comp_log_auto.py",
    "org/modules/graph/comp_output_contract.py",
}


def read_source_text(closure_modules):
    text = ""
    for m in closure_modules:
        if m in _SHARED_INFRA_MODULES:
            continue
        p = WS / m
        if p.is_file():
            try:
                text += "\n" + p.read_text(encoding="utf-8", errors="replace")
            except Exception:
                pass
    return text


def derive_evaluation(reads_typed: dict, tool: str) -> tuple[str, str]:
    kinds = set(reads_typed.keys())
    derived_hit = kinds & DERIVED_KINDS
    if derived_hit:
        return "DERIVED", f"reads[] includes {sorted(derived_hit)} -- depends on a pre-built artifact, not computed fresh at invocation"
    if kinds:
        return "RUNTIME", f"reads[] limited to {sorted(kinds)} -- live/fresh at invocation, no pre-built-artifact dependency"
    return "RUNTIME", "no typed reads detected -- treated as RUNTIME by default (nothing to derive from); verify manually"


def derive_failure_mode(source_text: str) -> tuple[str, str, dict]:
    if not source_text.strip():
        return "UNKNOWN", "no source text available to scan", {}
    loud_hits = len(re.findall(r"sys\.exit\(\s*[12]\s*\)|raise\s+\w|sys\.exit\(f?[\"']ERROR", source_text))
    blocked_hits = len(re.findall(r"BLOCKED|print\([^)]*ERROR", source_text))
    failopen_hits = len(re.findall(r"except[^:]*:\s*\n\s*(pass|return None|return \{\}|return \[\])", source_text))
    silent_empty_hits = len(re.findall(r"return \[\]\s*$|return \{\}\s*$", source_text, re.M))
    counts = {"loud": loud_hits + blocked_hits, "fail_open": failopen_hits, "silent_empty_candidates": silent_empty_hits}
    if counts["loud"] >= 2 and counts["loud"] >= counts["fail_open"]:
        note = f"LOUD signals dominate (sys.exit/raise/BLOCKED count={counts['loud']} vs fail-open count={counts['fail_open']})"
        return "LOUD", note, counts
    if counts["fail_open"] > 0 and counts["fail_open"] >= counts["loud"]:
        return "FAIL-OPEN", f"except-swallow pattern(s) found (count={counts['fail_open']}) >= loud signals ({counts['loud']})", counts
    if counts["loud"] == 1:
        return "LOUD", "single explicit sys.exit/raise found -- weak signal, verify manually", counts
    return "UNKNOWN", "no dominant pattern found in a quick scan -- needs a manual read", counts


def derive_binding(tool: str, reads_typed: dict, role_flags: list) -> tuple[str, str]:
    kinds = set(reads_typed.keys())
    is_gate_named = any(m in tool for m in GATE_NAME_MARKERS)
    if "GATE-BLOCKING" in role_flags or is_gate_named:
        return ("GUARD", "name/role signals an enforcement gate -- its typed reads decide a PASS/BLOCK "
                          "verdict rather than being reported as the tool's primary content answer "
                          "(though specific findings printed alongside the verdict ARE answer-bearing "
                          "for 'what was found' -- see notes; this is the mixed case CVO~Z's binding "
                          "warning targets, verify per-tool)")
    if kinds & {"CONFIG"} and len(kinds) == 1:
        return "CONFIG", "only typed read is CONFIG -- driving behavior/settings, not reported content"
    return "ANSWER-BEARING", "typed reads feed the tool's reported output (default for a non-gate query/report tool; verify manually for tools with a routing/dispatch role)"


def main():
    report = json.loads(RAW.read_text(encoding="utf-8"))
    out = {}
    for tool, r in report.items():
        if "error" in r:
            out[tool] = {"tool": tool, "SKIPPED": r["error"]}
            continue
        closure_mods = r.get("closure_modules", [])
        src = read_source_text(closure_mods) if closure_mods else ""
        reads_typed = r.get("reads_typed", {})
        writes_typed = r.get("writes_typed", {})

        role_flags = []
        if any(m in tool for m in GATE_NAME_MARKERS):
            role_flags.append("GATE-BLOCKING-CANDIDATE")  # confirm manually
        if writes_typed:
            role_flags.append("PRODUCER-CANDIDATE")
        if not role_flags:
            role_flags.append("ADVISORY")

        ev, ev_note = derive_evaluation(reads_typed, tool)
        fm, fm_note, fm_counts = derive_failure_mode(src)
        bd, bd_note = derive_binding(tool, reads_typed, role_flags)

        out[tool] = {
            "tool": tool,
            "reads_typed": reads_typed,
            "writes_typed": writes_typed,
            "closure_size": r.get("closure_size"),
            "entry_modules": r.get("entry_modules"),
            "unresolved_call_sites": r.get("unresolved_call_sites", []),
            "role_flags_candidate": role_flags,
            "evaluation_candidate": ev, "evaluation_note": ev_note,
            "failure_mode_candidate": fm, "failure_mode_note": fm_note, "failure_mode_counts": fm_counts,
            "binding_candidate": bd, "binding_note": bd_note,
        }

    outpath = WS / "org/tier1_exec/1.0.0_SA_CTO/deliverables/NFRA_TOOLUNIFY_CENSUS/_annotated_candidates.json"
    outpath.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"Wrote {outpath}")

    # summary
    from collections import Counter
    ev_counts = Counter(v.get("evaluation_candidate") for v in out.values() if "evaluation_candidate" in v)
    fm_counts_all = Counter(v.get("failure_mode_candidate") for v in out.values() if "failure_mode_candidate" in v)
    bd_counts = Counter(v.get("binding_candidate") for v in out.values() if "binding_candidate" in v)
    print("evaluation distribution:", dict(ev_counts))
    print("failure_mode distribution:", dict(fm_counts_all))
    print("binding distribution:", dict(bd_counts))
    unknown_fm = [t for t, v in out.items() if v.get("failure_mode_candidate") == "UNKNOWN"]
    print(f"UNKNOWN failure_mode ({len(unknown_fm)}):", unknown_fm)


if __name__ == "__main__":
    main()
