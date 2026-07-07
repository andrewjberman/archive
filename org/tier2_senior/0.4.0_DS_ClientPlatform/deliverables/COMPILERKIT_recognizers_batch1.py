"""COMPILERKIT-P1 recognizer batch-1 -- REFINED against the LIVE SDK (comp_recognizer_sdk, e49e54bf1).
The parity-critical DISPATCH pair: DispatchCatalogRecognizer (compiler #1 #2 = the D1-class) +
MdpfDispatchRecognizer (the DEBTSCAN root-fix, live-proven parse). Lexical (RAW_TEXT), CTO-#3-clean.
Author-DS/commit-AE: ~D commits into the SDK + runs the AC2 parity-oracle. VALIDATED against the live SDK
(the __main__ block: import + recognize() + CSE-shape + AC6-fidelity + coverage -- verify-don't-trust).

They CONVERGE: one recognizer body closes the DEBTSCAN reachability FP-block AND is compiler #1's dispatch
recognizer in COMPILERKIT.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

# Live SDK (0.8.0~D). Path-robust import (sibling in org/modules/graph), mirroring cse_schema's bootstrap.
_GRAPH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "modules", "graph")
if os.path.isdir(_GRAPH):
    sys.path.insert(0, os.path.abspath(_GRAPH))
from comp_recognizer_sdk import (  # noqa: E402
    Recognizer, emit_cse, Site, EnrichedTree, EntityRef, RelationshipDelta, Provenance,
    Entity, Relationship, Transformation, FrontEndCapability, locus_at,
)


def _marker(tree) -> str:
    """marker_head for the CSE. NOTE(DS->~D verify-don't-trust finding): emit(site,tree) has NO marker_head
    param (recognize() passes it only to degrade()), so a real recognizer can't reach it. Reading tree.meta
    is the clean path IF the front-end sets it."""  # SUPERSEDED below.
    return (getattr(tree, "meta", None) or {}).get("marker_head", "")


# marker_head: ~D RULED (b) 2026-07-07 (SDK 7af2db209) -- recognize() threads marker_head into emit()
# (emit(self, site, tree, *, marker_head)). The _marker/tree.meta workaround above is retired; emit takes it.


class DispatchCatalogRecognizer(Recognizer):
    """Compiler #1 recognizer #2 -- the gold-dispatch CATALOG heredoc (the D1-class). A dispatch runner
    TRIGGERS each catalog-listed gold script. AC2 parity target = today's dispatcher-TRIGGERS-script C1."""
    artifact_class = "bash"
    concept = "gold-dispatch-catalog"
    requires = FrontEndCapability.RAW_TEXT
    compiler_id = "code-compiler"

    _CATALOG = re.compile(r"read -r -d '' CATALOG << 'CATALOG_END'(.*?)CATALOG_END", re.DOTALL)
    _ROW = re.compile(r"^\s*(\S+)\|(\S+\.py)\|", re.MULTILINE)  # ID|filename|flags

    def iter_sites(self, tree):
        cat = self._CATALOG.search(tree.text)
        if not cat:
            return
        body, base = cat.group(1), cat.start(1)
        for m in self._ROW.finditer(body):
            # locus at the ROW CONTENT (group-1 start), not m.start() -- the `\s*` eats the leading
            # newline, so m.start() would point at the prior line (off-by-one). Verify-don't-trust catch.
            yield Site(source=tree.source, locus=locus_at(tree.text, base + m.start(1)),
                       evidence=m.group(0).strip(),
                       payload={"script_id": m.group(1), "filename": m.group(2)})

    def emit(self, site, tree, *, marker_head):
        script = Path(site.payload["filename"]).stem
        prov = Provenance(source=site.source, locus=site.locus, recognizer=self.concept, evidence=site.evidence)
        return [emit_cse(
            verb=Transformation.CREATE.value,
            subject=EntityRef(Entity.SERVICE.value, f"dispatch:{Path(site.source).stem}"),
            edges=[RelationshipDelta(Relationship.TRIGGERS.value,
                                     EntityRef(Entity.MODULE.value, f"gold:{script}"))],
            provenance=prov, confidence=1.0, marker_head=marker_head,
            producer_kind=self.producer_kind, compiler_id=self.compiler_id, artifact_class=self.artifact_class,
        )]


class MdpfDispatchRecognizer(Recognizer):
    """DEBTSCAN root-fix + COMPILERKIT #1 -- the MDPF EC2 stage-runner. `run_step LABEL <relpath>.py` + a few
    `X_SCRIPT="${SCRIPTS_DIR}/<relpath>.py"` vars. Live-proven (0.8.0 wired the parse e4eca6c36, 7 edged)."""
    artifact_class = "bash"
    concept = "mdpf-ec2-dispatch"
    requires = FrontEndCapability.RAW_TEXT
    compiler_id = "code-compiler"

    _RUN_STEP = re.compile(r"run_step\s+\S+\s+(\S+\.py)\b")
    _VAR = re.compile(r'\w+_SCRIPT="\$\{SCRIPTS_DIR\}/(\S+\.py)"')

    def iter_sites(self, tree):
        for pat in (self._RUN_STEP, self._VAR):
            for m in pat.finditer(tree.text):
                yield Site(source=tree.source, locus=locus_at(tree.text, m.start()),
                           evidence=m.group(0).strip(), payload={"relpath": m.group(1)})

    def emit(self, site, tree, *, marker_head):
        script = Path(site.payload["relpath"]).stem
        prov = Provenance(source=site.source, locus=site.locus, recognizer=self.concept, evidence=site.evidence)
        return [emit_cse(
            verb=Transformation.CREATE.value,
            subject=EntityRef(Entity.SERVICE.value, "mdpf-daily-runner"),
            edges=[RelationshipDelta(Relationship.TRIGGERS.value,
                                     EntityRef(Entity.MODULE.value, f"gold:{script}"))],
            provenance=prov, confidence=1.0, marker_head=marker_head,
            producer_kind=self.producer_kind, compiler_id=self.compiler_id, artifact_class=self.artifact_class,
        )]


if __name__ == "__main__":
    import cse_schema as cse
    ok = []

    def ck(n, c):
        ok.append(bool(c))
        print(f"  [{'PASS' if c else 'FAIL'}] {n}")

    catalog_text = (
        "#!/usr/bin/env bash\n"
        "read -r -d '' CATALOG << 'CATALOG_END'\n"
        "INF_A_00|A_00.build_accounts_dimension.py|--upload\n"
        "INF_A_02|A_02.fee_rate_history.py|--upload\n"
        "CATALOG_END\n"
    )
    t1 = EnrichedTree(source="data/inf/scripts/gold/orion-gold-dispatch.sh",
                      capability=FrontEndCapability.RAW_TEXT, text=catalog_text, meta={"marker_head": "h1"})
    cses1, cov1 = DispatchCatalogRecognizer().recognize(t1, marker_head="h1")
    ck("catalog: 2 CSEs", len(cses1) == 2)
    ck("catalog: subject=SERVICE", all(c.transformation["subject"].etype == Entity.SERVICE.value for c in cses1))
    ck("catalog: edge=TRIGGERS->MODULE gold:X", all(
        c.transformation["edges"][0].rtype == Relationship.TRIGGERS.value
        and c.transformation["edges"][0].target.etype == Entity.MODULE.value
        and c.transformation["edges"][0].target.ref.startswith("gold:") for c in cses1))
    ck("catalog: provenance file:line", {c.provenance.locus for c in cses1} == {"L3", "L4"})
    ck("catalog: every CSE AC6-fidelity-ok", all(cse.cse_fidelity_ok(c)[0] for c in cses1))
    ck("catalog: coverage clean (no silent drop)", cov1.resolved == 2 and not cov1.unresolved)

    mdpf_text = (
        "run_step WS-C   gold/build_mdpf_wsc_inflection_feeder.py --date x --upload\n"
        "run_step WS-A   gold/mdpf_aggregate_aua.py --date x --upload\n"
        'S0_SCRIPT="${SCRIPTS_DIR}/bronze/pull_orion_model_composition.py"\n'
    )
    t2 = EnrichedTree(source="infra/aws/ec2/mdpf-daily-runner/mdpf-daily-dispatch.sh",
                      capability=FrontEndCapability.RAW_TEXT, text=mdpf_text, meta={"marker_head": "h1"})
    cses2, cov2 = MdpfDispatchRecognizer().recognize(t2, marker_head="h1")
    ck("mdpf: 3 CSEs (2 run_step + 1 X_SCRIPT)", len(cses2) == 3)
    ck("mdpf: subject=mdpf-daily-runner", all(c.transformation["subject"].ref == "mdpf-daily-runner" for c in cses2))
    ck("mdpf: targets the mdpf scripts", {c.transformation["edges"][0].target.ref for c in cses2} == {
        "gold:build_mdpf_wsc_inflection_feeder", "gold:mdpf_aggregate_aua", "gold:pull_orion_model_composition"})
    ck("mdpf: every CSE AC6-fidelity-ok", all(cse.cse_fidelity_ok(c)[0] for c in cses2))

    p = sum(ok)
    print(f"\n=== COMPILERKIT batch-1 vs LIVE SDK: {p}/{len(ok)} PASS ===")
    sys.exit(0 if p == len(ok) else 1)
