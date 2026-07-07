"""COMPILERKIT compiler #2 -- the FLOWS_TO recognizer (field-grain lineage with the KIND discriminator),
authored against the LIVE SDK + cse_schema 0.2 (EdgeKind PASSTHROUGH/RENAME/RECOMPUTE_GUARDED +
RelationshipDelta.kind/.condition, landed by CTO exec-commit 9e2605898). This is the recognizer that
preserves TSGRAPH's most valuable capability -- the field-level flow KIND that catches the {...spread}
bug the regex can't see (a recompute/guarded flow that LOOKS like a passthrough at the object-literal
level but actually re-derives or conditionally-guards the field).

GROUNDED against REAL compiler-#2 output: org/modules/graph/tsgraph_spike/out/live_flowsto.json (961 real
FLOWS_TO edges over the live portal, produced by extractor_full.ts PASS-6 via ts-morph
TypeChecker.getSymbol). This recognizer is the MAPPING half of the P1 refactor for compiler #2 ("map its
11 labels to CSE enums, route emission through the framework") -- the ts-morph RESOLUTION stays in
extractor_full.ts (compiler #2's front-end, a RESOLVED_SEMANTIC-tier producer owned by 0.8.0~D); this
recognizer consumes its already-resolved FLOWS_TO edge output and emits the CSE with the correct
EdgeKind + condition, proving the field-grain lineage survives the generalization onto the CSE IR.

THE LOAD-BEARING NORMALIZATION (caught by grounding, not assumed): extractor_full.ts:373 emits the kind
literal "recompute/guarded" (with a SLASH), but cse_schema 0.2 EdgeKind.RECOMPUTE_GUARDED.value is
"recompute_guarded" (UNDERSCORE), and cse_schema.validate:372-373 REJECTS any off-EdgeKind kind
(governed-closed, LAW 1). Over the real 961-edge corpus that is 482 edges (50%!) that would fail-closed
without the slash->underscore normalization here. Grounding against the real output surfaced this exact
impedance mismatch -- the same class of catch as batch-1's locus off-by-one and batch-2's firm-collision.

LAW 1: a kind literal outside the three known compiler-#2 values honest-degrades to Concept(untyped)+low,
NEVER a guessed EdgeKind -- so a future extractor kind (a new discriminator) surfaces as an explicit
unresolved+degrade, not a silent mis-map.

Author-DS/commit-AE: 0.8.0~D wires + runs AC2 parity (the 961-edge FLOWS_TO parity target, CTO-signed
961/961 per the prestage doc). Same split as batch-1/2.
"""
from __future__ import annotations

import json
import os
import re
import sys

_GRAPH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "modules", "graph")
if os.path.isdir(_GRAPH):
    sys.path.insert(0, os.path.abspath(_GRAPH))
from comp_recognizer_sdk import (  # noqa: E402
    Recognizer, emit_cse, Site, EnrichedTree, EntityRef, RelationshipDelta, Provenance,
    Entity, Relationship, Transformation, FrontEndCapability,
)
from cse_schema import EdgeKind  # noqa: E402


# compiler-#2 kind literal -> governed EdgeKind value. The "recompute/guarded"->"recompute_guarded"
# entry is the load-bearing normalization (slash vs underscore; 482/961 real edges depend on it).
_KIND_MAP = {
    "passthrough": EdgeKind.PASSTHROUGH.value,
    "rename": EdgeKind.RENAME.value,
    "recompute/guarded": EdgeKind.RECOMPUTE_GUARDED.value,
}

# "via" carries the mapping-site provenance: e.g. "mapping portal/src/components/Foo.tsx:354".
_VIA_RE = re.compile(r"mapping\s+(?P<file>\S+):(?P<line>\d+)\s*$")


class FlowsToRecognizer(Recognizer):
    """Consumes compiler #2's emitted FLOWS_TO edges (extractor_full.ts PASS-6 output, the live_flowsto.json
    shape) and emits one CSE per edge: subject = source Field, edge = FLOWS_TO -> dst Field carrying the
    governed EdgeKind + the (optional) lexical guard condition. RESOLVED_SEMANTIC tier -- the getSymbol
    cross-file field resolution was done by the ts-morph front-end; this recognizer maps its resolved
    output, it does not re-resolve. A kind literal outside _KIND_MAP honest-degrades (LAW 1)."""
    artifact_class = "tsx"
    concept = "field-flows-to"
    requires = FrontEndCapability.RESOLVED_SEMANTIC
    compiler_id = "tsx-compiler"

    def iter_sites(self, tree: EnrichedTree):
        # front-end delivers the resolved FLOWS_TO edges via meta["flowsto_edges"] (list of the
        # {src, dst, props} dicts) -- the whole-project ts-morph lifecycle (hard-part #2) already ran.
        for edge in tree.meta.get("flowsto_edges", []):
            props = edge.get("props")
            props = json.loads(props) if isinstance(props, str) else (props or {})
            # locus/source from the mapping-site "via" (real file:line); fall back to the tree source.
            m = _VIA_RE.search(props.get("via", "") or "")
            source = m.group("file") if m else tree.source
            locus = f"L{m.group('line')}" if m else "L0"
            yield Site(source=source, locus=locus,
                       evidence=f"{props.get('srcField', edge.get('src'))} "
                                f"-FLOWS_TO({props.get('kind')})-> {props.get('dstField', edge.get('dst'))}",
                       payload={"src": edge.get("src"), "dst": edge.get("dst"),
                                "kind": props.get("kind"), "condition": props.get("condition") or ""})

    def emit(self, site: Site, tree: EnrichedTree, *, marker_head: str):
        mapped = _KIND_MAP.get(site.payload["kind"])
        if mapped is None:
            # unknown compiler-#2 kind literal -> LAW 1 honest-degrade, never a guessed EdgeKind.
            return [self.degrade(site, marker_head=marker_head)]
        prov = Provenance(source=site.source, locus=site.locus, recognizer=self.concept, evidence=site.evidence)
        return [emit_cse(
            verb=Transformation.CREATE.value,
            subject=EntityRef(Entity.FIELD.value, site.payload["src"]),
            edges=[RelationshipDelta(Relationship.FLOWS_TO.value,
                                     EntityRef(Entity.FIELD.value, site.payload["dst"]),
                                     kind=mapped, condition=site.payload["condition"])],
            provenance=prov, confidence=1.0, marker_head=marker_head,
            producer_kind=self.producer_kind, compiler_id=self.compiler_id, artifact_class=self.artifact_class,
        )]


if __name__ == "__main__":
    import collections
    import cse_schema as cse
    from pathlib import Path
    ok = []

    def ck(n, c):
        ok.append(bool(c))
        print(f"  [{'PASS' if c else 'FAIL'}] {n}")

    # --- FlowsToRecognizer vs the REAL 961-edge compiler-#2 output -------------------------------------
    live_path = Path(_GRAPH) / "tsgraph_spike" / "out" / "live_flowsto.json"
    live_edges = json.loads(live_path.read_text(encoding="utf-8"))
    tree = EnrichedTree(source="org/modules/graph/tsgraph_spike/out/live_flowsto.json",
                        capability=FrontEndCapability.RESOLVED_SEMANTIC,
                        meta={"marker_head": "h1", "flowsto_edges": live_edges})
    cses, cov = FlowsToRecognizer().recognize(tree, marker_head="h1")

    # ground-truth the source distribution independently from the raw file
    src_kinds = collections.Counter(json.loads(e["props"])["kind"] for e in live_edges)
    src_conds = sum(1 for e in live_edges if json.loads(e["props"]).get("condition"))

    ck(f"flows-to: all 961 real edges resolve to CSEs (got {len(cses)}, source={len(live_edges)})",
       len(cses) == len(live_edges) == 961)
    ck("flows-to: coverage clean, zero unresolved (no silent drop)",
       cov.resolved == cov.attempted == 961 and not cov.unresolved)

    # the load-bearing proof: every CSE VALIDATES -- i.e. the 482 recompute/guarded edges did NOT
    # fail-closed on the slash-vs-underscore EdgeKind mismatch (they would without the normalization).
    ck("flows-to: every CSE is valid + AC6-fidelity-ok (proves the 482 recompute_guarded normalize, not reject)",
       all(cse.cse_fidelity_ok(c)[0] for c in cses))

    out_kinds = collections.Counter(c.transformation["edges"][0].kind for c in cses)
    ck(f"flows-to: kind distribution maps + normalizes correctly "
       f"(src {dict(src_kinds)} -> out {dict(out_kinds)})",
       out_kinds["passthrough"] == src_kinds["passthrough"] == 337
       and out_kinds["rename"] == src_kinds["rename"] == 142
       and out_kinds["recompute_guarded"] == src_kinds["recompute/guarded"] == 482)
    ck("flows-to: NO edge carries the un-normalized slash form 'recompute/guarded' (would have rejected)",
       "recompute/guarded" not in out_kinds)

    # conditions survive the round-trip (the guard expression = the spread-bug evidence)
    out_conds = sum(1 for c in cses if c.transformation["edges"][0].condition)
    ck(f"flows-to: all 23 lexical guard conditions survive the CSE round-trip (got {out_conds})",
       out_conds == src_conds == 23)
    sample_cond = next((c for c in cses if c.transformation["edges"][0].condition), None)
    ck("flows-to: a real condition is carried verbatim (e.g. \"... === 'HOLD' == false\")",
       sample_cond is not None and "==" in sample_cond.transformation["edges"][0].condition)

    # provenance uplift: locus is a REAL file:line parsed from the 'via' mapping-site, not L0
    real_loci = sum(1 for c in cses if c.provenance.locus != "L0"
                    and c.provenance.source.endswith((".ts", ".tsx")))
    ck(f"flows-to: provenance is real file:line from the mapping-site via ({real_loci}/{len(cses)} uplifted)",
       real_loci == len(cses))

    # LAW-1 honest-degrade: a future/unknown kind literal -> Concept(untyped)+low, never a guessed EdgeKind
    synth = [{"src": "type:x.ts#A#f", "dst": "type:y.ts#B#g",
              "props": json.dumps({"kind": "aggregate/folded", "condition": None, "srcField": "A.f",
                                   "dstField": "g", "via": "mapping x.ts:9"})}]
    t_synth = EnrichedTree(source="x.ts", capability=FrontEndCapability.RESOLVED_SEMANTIC,
                           meta={"marker_head": "h1", "flowsto_edges": synth})
    scses, scov = FlowsToRecognizer().recognize(t_synth, marker_head="h1")
    degraded = (len(scses) == 1 and scses[0].transformation["subject"].etype == Entity.CONCEPT.value
                and float(scses[0].qualifiers.get("confidence", 1.0)) <= cse.LOW_CONFIDENCE_MAX)
    ck("flows-to: an unknown kind literal honest-degrades to Concept(untyped)+low (LAW 1), never a guess",
       degraded)

    p = sum(ok)
    print(f"\n=== COMPILERKIT FLOWS_TO recognizer vs REAL 961-edge compiler-#2 output: {p}/{len(ok)} PASS ===")
    sys.exit(0 if p == len(ok) else 1)
