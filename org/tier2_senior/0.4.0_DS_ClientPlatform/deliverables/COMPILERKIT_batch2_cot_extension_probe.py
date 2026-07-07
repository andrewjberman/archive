"""COMPILERKIT-P1 batch-2 cot firm-EXTENSION probe -- NFRA recognizer-COVERAGE proof (DS~A).

WHY: batch-2 (S3-key const + read/write) landed BD-only (canonical comp_recognizers_code.py:310, scope_note
"cot/inf extension not yet run -- flagged, not silent"). COO~B + 0.8.0~D BOTH ruled 2026-07-07: EXTEND to cot
(APPROVED -- purely additive 3rd-firm coverage on cot's bd-identical central s3_layout.py; firm-scope keeps
refs distinct; does NOT touch the bd AC2 baseline; strengthens the parity-oracle from 1->2 firms). inf
read/write is DEFERRED (accept-parity: deployed extract_pipeline has 0 inf read/write coverage, so 0-vs-0 IS
parity; ~D ruling #3) -- this probe deliberately does NOT extend inf read/write.

SCOPE DISCIPLINE (COO~B guard): this is NFRA recognizer-coverage -- it runs the LANDED NFRA recognizers over
cot source as recognizer INPUT. It is NOT cot-pipeline firm work; nothing under data/cot/ is modified.

This probe imports the recognizers from the CANONICAL landed module (comp_recognizers_code.py), so it exercises
the REAL wired code -- not a staging copy. It proves cot coverage fires GREEN + (the load-bearing safety check)
that cot's byte-identical-basename gold scripts stay firm-scope-DISTINCT from bd (no collision, no baseline
perturbation). The 2-line scope-dict patch this validates is handed to 0.8.0~D to fold into the canonical
module's parity_run_batch2 (their wiring/closeout lane).

Run: python COMPILERKIT_batch2_cot_extension_probe.py   (exit 0 = all PASS)
"""

from __future__ import annotations

import ast
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_WS = os.path.abspath(os.path.join(_HERE, "..", "..", "..", ".."))  # deliverables -> ...-> ajb_workspace
_GRAPH = os.path.join(_WS, "org", "modules", "graph")
for _p in (_GRAPH,):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import cse_schema as cse  # noqa: E402
from comp_recognizer_sdk import EnrichedTree, FrontEndCapability  # noqa: E402
from comp_recognizers_code import (  # noqa: E402  -- the CANONICAL landed recognizers
    S3KeyConstRecognizer, S3KeyReadWriteRecognizer, _firm_from_source,
)

# The exact scope-dict addition proposed for parity_run_batch2 (bd already present; this adds cot).
COT_LAYOUT_SRC = "data/cot/scripts/gold/lib/s3_layout.py"
COT_GOLD_SCRIPTS = [
    "data/cot/scripts/gold/A_00.accounts_dimension.py",
    "data/cot/scripts/gold/A_01.advisor_assignments.py",
]
BD_LAYOUT_SRC = "data/black_diamond/scripts/gold/lib/s3_layout.py"
BD_GOLD_SCRIPTS = [
    "data/black_diamond/scripts/gold/A_00.accounts_dimension.py",
    "data/black_diamond/scripts/gold/A_01.advisor_assignments.py",
]


def _run_firm(firm_expect: str, layout_src: str, gold_scripts: list, marker_head: str = "cot-ext") -> dict:
    """Mirror parity_run_batch2 for one firm: const over s3_layout.py -> map -> read/write over gold scripts."""
    const_rec = S3KeyConstRecognizer()
    rw_rec = S3KeyReadWriteRecognizer()
    ap = os.path.join(_WS, layout_src)
    with open(ap, encoding="utf-8", errors="replace") as fh:
        layout_text = fh.read()
    t_layout = EnrichedTree(source=layout_src, capability=FrontEndCapability.LEXICAL_AST,
                            text=layout_text, root=ast.parse(layout_text))
    const_cses, _cov = const_rec.recognize(t_layout, marker_head=marker_head)
    s3_constants = {s.payload["name"]: s.payload["value"] for s in const_rec.iter_sites(t_layout)}
    const_ok = all(cse.cse_fidelity_ok(c)[0] for c in const_cses)
    const_subjects = [c.transformation["subject"].ref for c in const_cses]

    rw_edges = []
    rw_ok = True
    for script_src in gold_scripts:
        sp = os.path.join(_WS, script_src)
        with open(sp, encoding="utf-8", errors="replace") as fh:
            script_text = fh.read()
        t_script = EnrichedTree(source=script_src, capability=FrontEndCapability.RAW_TEXT,
                                text=script_text, meta={"s3_constants": s3_constants})
        rw_cses, _rwcov = rw_rec.recognize(t_script, marker_head=marker_head)
        rw_ok = rw_ok and all(cse.cse_fidelity_ok(c)[0] for c in rw_cses)
        for c in rw_cses:
            rw_edges.append((c.transformation["subject"].ref, c.transformation["edges"][0].rtype,
                             c.transformation["edges"][0].target.ref, c.provenance.locus))
    return {"firm_expect": firm_expect, "const_n": len(const_cses), "const_ok": const_ok,
            "const_subjects": const_subjects, "rw_n": len(rw_edges), "rw_ok": rw_ok, "rw_edges": rw_edges}


def main() -> int:
    checks = []

    def chk(name: str, cond: bool, detail: str = "") -> None:
        checks.append((name, bool(cond), detail))

    # Ground the firm resolution FIRST (verify-don't-assume): the whole firm-scoping rests on
    # _firm_from_source deriving 'cot' from a cot path via PIPELINE_MAP -- never guessed.
    cot_firm = _firm_from_source(COT_LAYOUT_SRC)
    bd_firm = _firm_from_source(BD_LAYOUT_SRC)
    chk("firm-resolve: cot s3_layout.py -> 'cot' via PIPELINE_MAP", cot_firm == "cot",
        f"got '{cot_firm}'")
    chk("firm-resolve: bd s3_layout.py -> 'bd' via PIPELINE_MAP", bd_firm == "bd", f"got '{bd_firm}'")

    cot = _run_firm("cot", COT_LAYOUT_SRC, COT_GOLD_SCRIPTS)
    bd = _run_firm("bd", BD_LAYOUT_SRC, BD_GOLD_SCRIPTS)

    # --- cot coverage FIRES ---
    chk("cot: S3KeyConst fires over cot s3_layout.py (const edges > 0)", cot["const_n"] > 0,
        f"const_n={cot['const_n']}")
    chk("cot: every const CSE AC6-fidelity-ok", cot["const_ok"])
    chk("cot: S3KeyReadWrite fires over cot gold scripts (rw edges > 0)", cot["rw_n"] > 0,
        f"rw_n={cot['rw_n']}")
    chk("cot: every read/write CSE AC6-fidelity-ok", cot["rw_ok"])

    # --- FIRM-SCOPE DISTINCTNESS (the load-bearing safety proof: additive, no bd collision) ---
    cot_subjs = set(cot["const_subjects"]) | {e[0] for e in cot["rw_edges"]}
    bd_subjs = set(bd["const_subjects"]) | {e[0] for e in bd["rw_edges"]}
    # every cot subject ref is cot-scoped; every bd subject ref is bd-scoped; NO overlap despite
    # byte-identical basenames (A_00/A_01 exist in both firms).
    cot_all_scoped = all((":cot:" in s) for s in cot_subjs)
    bd_all_scoped = all((":bd:" in s) for s in bd_subjs)
    overlap = cot_subjs & bd_subjs
    chk("scope: every cot ref is :cot:-scoped", cot_all_scoped,
        f"unscoped={[s for s in cot_subjs if ':cot:' not in s][:3]}")
    chk("scope: every bd ref is :bd:-scoped", bd_all_scoped,
        f"unscoped={[s for s in bd_subjs if ':bd:' not in s][:3]}")
    chk("scope: ZERO cot/bd ref overlap despite byte-identical A_00/A_01 basenames", not overlap,
        f"overlap={list(overlap)[:3]}")
    # cot read/write targets are cot-bucket keys, bd are bd-bucket keys -> byte-identical relative
    # paths stay distinct s3key refs (the confirmed-live collision batch-2 was built to defeat).
    cot_tgts = {e[2] for e in cot["rw_edges"]}
    bd_tgts = {e[2] for e in bd["rw_edges"]}
    chk("scope: ZERO cot/bd read-write TARGET (s3key) overlap", not (cot_tgts & bd_tgts),
        f"overlap={list(cot_tgts & bd_tgts)[:3]}")

    # --- report ---
    print("=== COMPILERKIT batch-2 cot firm-EXTENSION probe (NFRA recognizer-coverage) ===\n")
    print(f"cot: const={cot['const_n']} (ok={cot['const_ok']}) | read/write={cot['rw_n']} (ok={cot['rw_ok']})")
    for subj, rel, tgt, loc in cot["rw_edges"][:8]:
        print(f"    {subj} --{rel}--> {tgt}  @{loc}")
    if cot["rw_n"] > 8:
        print(f"    ... +{cot['rw_n'] - 8} more")
    print(f"\nbd  (baseline, unchanged): const={bd['const_n']} | read/write={bd['rw_n']}")
    print()
    n_pass = sum(1 for _n, ok, _d in checks if ok)
    for name, ok, detail in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({detail})" if (detail and not ok) else ""))
    all_ok = n_pass == len(checks)
    print(f"\n=== cot extension: {n_pass}/{len(checks)} {'PASS' if all_ok else 'FAIL'} "
          f"(cot additive + firm-scope-distinct from bd, no baseline perturbation) ===")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
