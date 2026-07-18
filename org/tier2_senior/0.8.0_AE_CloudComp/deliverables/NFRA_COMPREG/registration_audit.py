#!/usr/bin/env python3
"""NFRA_COMPREG registration-gap audit -- per-tool verdict + printed denominator.

Reports, per tracked .tools/comp-* executable, its registration disposition across the
same registries comp-manifest-check's registration-invariant (member 5) reads:
  - tools_index (graph-call-manifest.yaml)      -> routable routing target
  - entries[].tool (graph-call-manifest.yaml)   -> has an agent-phrasing use_case row
  - excluded_not_graph_use_cases (same file)    -> sanctioned escape hatch (with a reason)
  - comp-coverage-map.yaml union(tools[], meta_tools[]) -> ledgered (posterior router)

This is a REPORT, not the gate. It reproduces the gate's denominators exactly (so a match
proves it reads the same fields) and prints a per-tool row so a gap-closure sweep can name
what it covered -- the anti-silent-truncation discipline (CTO gate point 3, 2026-07-18).

Run from workspace root:  python org/tier2_senior/0.8.0_AE_CloudComp/deliverables/NFRA_COMPREG/registration_audit.py
NOT the gate -- the gate is `comp-manifest-check completeness`. This is its legible per-tool view.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import yaml

WS = Path(__file__).resolve().parents[5]
MAN = WS / "org/modules/graph/graph-call-manifest.yaml"
COV = WS / "org/modules/graph/comp-coverage-map.yaml"


def main() -> int:
    raw = yaml.safe_load(MAN.read_text(encoding="utf-8")) or {}
    ti = set((raw.get("tools_index") or {}).keys())
    exc = set(raw.get("excluded_not_graph_use_cases") or [])
    ent = {str(e.get("tool", "")).split()[0] for e in (raw.get("entries") or []) if isinstance(e, dict)}
    led = yaml.safe_load(COV.read_text(encoding="utf-8")) or {}
    cov_tools = {t.get("tool") for t in (led.get("tools") or []) if isinstance(t, dict)}
    cov_meta = {t.get("tool") for t in (led.get("meta_tools") or []) if isinstance(t, dict)}
    ledger = cov_tools | cov_meta

    r = subprocess.run(["git", "ls-files", ".tools/"], capture_output=True, text=True, cwd=str(WS))
    universe = sorted({Path(p).name for p in r.stdout.split()
                       if Path(p).name.startswith("comp-") and "." not in Path(p).name})

    print(f"DENOMINATOR: universe={len(universe)} tracked comp-* | tools_index={len(ti)} "
          f"excluded={len(exc)} entries-tools={len(ent)} coverage-map={len(ledger)} "
          f"(tools[]={len(cov_tools)} meta_tools[]={len(cov_meta)})\n")
    print(f"{'TOOL':<24} {'TI':<3}{'CM':<7}{'EXC':<4}{'ENT':<4} VERDICT")
    print("-" * 70)
    unaccounted, unledgered = [], []
    for t in universe:
        in_ti, in_exc, in_ent = t in ti, t in exc, t in ent
        home = "tools" if t in cov_tools else ("meta" if t in cov_meta else "-")
        accounted, ledgered = (in_ti or in_exc or in_ent), (t in ledger)
        if not accounted:
            unaccounted.append(t)
        if not ledgered:
            unledgered.append(t)
        verdict = ("EXCLUDED" if in_exc and not in_ti
                   else "REGISTERED" if accounted and ledgered else "** GAP **")
        print(f"{t:<24} {'Y' if in_ti else '.':<3}{home:<7}"
              f"{'Y' if in_exc else '.':<4}{'Y' if in_ent else '.':<4} {verdict}")
    print("-" * 70)
    print(f"GAPS: unaccounted={unaccounted or 'NONE'} | unledgered={unledgered or 'NONE'}")
    clean = not unaccounted and not unledgered
    print(f"RESULT: {'CLEAN -- 0 registration gaps across ' + str(len(universe)) + ' tools' if clean else 'GAPS PRESENT'}")
    return 0 if clean else 1


if __name__ == "__main__":
    raise SystemExit(main())
