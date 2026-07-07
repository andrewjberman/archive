"""COMPILERKIT-P1 recognizer batch-2 -- built against the LIVE SDK (comp_recognizer_sdk, 7af2db209) +
cse_schema 0.2 (9e2605898, no breaking changes to the SDK -- confirmed by 0.8.0~D 2026-07-07). The S3-key
pair: S3KeyConstRecognizer (compiler #1's ast mechanism -- lib/s3_layout.py constant + key-function
catalog) + S3KeyReadWriteRecognizer (compiler #1's callee-co-occurrence mechanism -- per-script READS/
WRITES classification). Lexical-only (CTO #3), file:line provenance throughout.

Author-DS/commit-AE: ~D commits into the SDK + runs the AC2 parity-oracle (same split as batch-1).

REUSE-NOT-REBUILD: both recognizers import their core vocabulary/helpers directly from the DEPLOYED
extractor (org/modules/graph/extract_pipeline.py -- zero-API-call, deterministic, already AC2-parity-
authoritative) rather than re-deriving them, so the recognizer's classification decision is byte-identical
to today's production extractor, not a parallel reimplementation that can drift. Only the emission (CSE
wrapping) is new.

Front-end contract (hard-part #2, "per-artifact + authoritative-map assembly", flagged in
COMPILERKIT_P1_recognizer_prestage.md): S3KeyReadWriteRecognizer needs the FULL constant->s3_path map
BEFORE it can classify any one script's usage (a script only ever imports a subset of s3_layout.py's
names). The front-end assembles that map once (by running S3KeyConstRecognizer's own iter_sites over
s3_layout.py, or equivalently extract_pipeline._parse_s3_layout) and threads it via
EnrichedTree.meta["s3_constants"] = {const_name: s3_path, ...} into every gold-script tree. This mirrors
extract_pipeline.py's own Step-1-then-Step-3 flow (parse the registry once, classify each script against
it) -- the SDK just wraps step 3 in Recognizer.emit().
"""
from __future__ import annotations

import ast
import os
import re
import sys
from pathlib import Path

# Live SDK (0.8.0~D). Path-robust import (sibling in org/modules/graph), mirroring batch-1's bootstrap.
_GRAPH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "modules", "graph")
if os.path.isdir(_GRAPH):
    sys.path.insert(0, os.path.abspath(_GRAPH))
from comp_recognizer_sdk import (  # noqa: E402
    Recognizer, emit_cse, Site, EnrichedTree, EntityRef, RelationshipDelta, Provenance,
    Entity, Relationship, Transformation, FrontEndCapability,
)
# REUSE the deployed extractor's vocabulary + helpers (zero-API-call, deterministic per its own docstring)
# so the recognizer's read/write verdict is the SAME decision as today's production DAG, not a parallel one.
from extract_pipeline import (  # noqa: E402
    _extract_fstring_template, _find_aliases, _WRITE_CALLEES, _READ_CALLEES,
)


class S3KeyConstRecognizer(Recognizer):
    """Compiler #1's ast mechanism -- lib/s3_layout.py's constant assignments (ACCOUNTS_DIMENSION = '...')
    AND key-generating functions (def advisor_fee_detail_key(...) -> f'...{}...'). Mirrors
    extract_pipeline._parse_s3_layout's two ast.walk branches (Assign + FunctionDef) exactly -- same
    uppercase-name + '/'-in-value gate, same legacy_/private-function skip, same f-string template
    extraction. Emits a C0 S3Bucket entity per key (matches the SDK's own _SampleS3KeyConstRecognizer
    shape) -- no edges; the read/write EDGES are S3KeyReadWriteRecognizer's job."""
    artifact_class = "python"
    concept = "s3-key-const"
    requires = FrontEndCapability.LEXICAL_AST
    compiler_id = "code-compiler"

    def iter_sites(self, tree: EnrichedTree):
        mod = tree.root if isinstance(tree.root, ast.Module) else ast.parse(tree.text)
        for node in ast.walk(mod):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and isinstance(node.value, ast.Constant):
                        name, value = target.id, node.value.value
                        if isinstance(value, str) and "/" in value and name.isupper():
                            yield Site(source=tree.source, locus=f"L{node.lineno}",
                                       evidence=f"{name} = {value!r}",
                                       payload={"name": name, "value": value, "kind": "const"})
            if isinstance(node, ast.FunctionDef):
                if node.name.startswith("legacy_") or node.name.startswith("_"):
                    continue
                for child in ast.walk(node):
                    if isinstance(child, ast.Return) and child.value:
                        template = _extract_fstring_template(child.value)
                        if template and "/" in template:
                            yield Site(source=tree.source, locus=f"L{node.lineno}",
                                       evidence=f"def {node.name}(...): return {template!r}",
                                       payload={"name": node.name, "value": template, "kind": "func"})
                            break

    def emit(self, site: Site, tree: EnrichedTree, *, marker_head: str):
        prov = Provenance(source=site.source, locus=site.locus, recognizer=self.concept, evidence=site.evidence)
        return [emit_cse(
            verb=Transformation.CREATE.value,
            subject=EntityRef(Entity.S3BUCKET.value, f"s3key:{site.payload['value']}"),
            edges=[], provenance=prov, confidence=1.0, marker_head=marker_head,
            producer_kind=self.producer_kind, compiler_id=self.compiler_id, artifact_class=self.artifact_class,
        )]


class S3KeyReadWriteRecognizer(Recognizer):
    """Compiler #1's callee-co-occurrence mechanism -- per-script classification of each imported S3-key
    constant as a READ or WRITE. Line-scoped (not extract_pipeline._classify_constant's file-level
    aggregate-then-collapse-multiline-calls): each site is exactly one line where a known constant's alias
    co-occurs with a write- or read-side callee name, so provenance decompresses to a real, single file:line
    (AC6) rather than a synthesized cross-line aggregate. A constant used BOTH ways (e.g. A_00 reads via
    get_object then writes via upload_file under a local alias) naturally yields two independent sites/CSEs
    -- one READS, one WRITES -- which is the honest lexical decomposition of extract_pipeline's 'both'
    verdict, not a re-aggregation of it.

    KNOWN GAP (logged, not silent): does not port extract_pipeline's multi-line-call collapse or the
    Key=/Prefix=/f-string special-case matchers (lines 400-421) -- those cover calls split across lines and
    a handful of argument-shape variants. The base callee-name+alias-on-one-line co-occurrence check (the
    dominant case; verified against both single-line real examples this batch was validated on) is what's
    implemented. Coverage.unresolved does not (yet) enumerate the specific multi-line calls this misses --
    a genuine limitation of this recognizer, not a coverage-channel bug; flagged to ~D for the wiring pass
    (compare against extract_pipeline's aggregate to size the residual before AC2 parity-sign)."""
    artifact_class = "python"
    concept = "s3-key-read-write"
    requires = FrontEndCapability.RAW_TEXT
    compiler_id = "code-compiler"

    def iter_sites(self, tree: EnrichedTree):
        consts = tree.meta.get("s3_constants", {})
        if not consts:
            return
        alias_map = {name: _find_aliases(name, tree.text) | {name} for name in consts}
        for lineno, line in enumerate(tree.text.splitlines(), start=1):
            stripped = line.strip()
            if stripped.startswith(("#", "from ", "import ")):
                continue
            for name, s3_path in consts.items():
                if not any(a in line for a in alias_map[name]):
                    continue
                kind = None
                for callee in _WRITE_CALLEES:
                    if callee in line and re.search(rf"{re.escape(callee)}\s*\(", line):
                        kind = "write"
                        break
                if kind is None:
                    for callee in _READ_CALLEES:
                        if callee in line and re.search(rf"{re.escape(callee)}\s*\(", line):
                            kind = "read"
                            break
                if kind:
                    yield Site(source=tree.source, locus=f"L{lineno}", evidence=stripped,
                               payload={"const": name, "s3_path": s3_path, "kind": kind})

    def emit(self, site: Site, tree: EnrichedTree, *, marker_head: str):
        rel = Relationship.WRITES.value if site.payload["kind"] == "write" else Relationship.READS.value
        script = Path(tree.source).stem
        prov = Provenance(source=site.source, locus=site.locus, recognizer=self.concept, evidence=site.evidence)
        return [emit_cse(
            verb=Transformation.CREATE.value,
            subject=EntityRef(Entity.MODULE.value, f"gold:{script}"),
            edges=[RelationshipDelta(rel, EntityRef(Entity.S3BUCKET.value, f"s3key:{site.payload['s3_path']}"))],
            provenance=prov, confidence=1.0, marker_head=marker_head,
            producer_kind=self.producer_kind, compiler_id=self.compiler_id, artifact_class=self.artifact_class,
        )]


if __name__ == "__main__":
    import cse_schema as cse
    from extract_pipeline import _classify_constant  # AC2-parity cross-check only, not used by the recognizer
    ok = []

    def ck(n, c):
        ok.append(bool(c))
        print(f"  [{'PASS' if c else 'FAIL'}] {n}")

    # --- S3KeyConstRecognizer vs the REAL lib/s3_layout.py (BD) -----------------------------------------
    layout_path = Path(_GRAPH) / ".." / ".." / ".." / "data" / "black_diamond" / "scripts" / "gold" / "lib" / "s3_layout.py"
    layout_path = layout_path.resolve()
    layout_text = layout_path.read_text(encoding="utf-8")
    t_layout = EnrichedTree(source="data/black_diamond/scripts/gold/lib/s3_layout.py",
                            capability=FrontEndCapability.LEXICAL_AST, text=layout_text,
                            root=ast.parse(layout_text), meta={"marker_head": "h1"})
    cses_layout, cov_layout = S3KeyConstRecognizer().recognize(t_layout, marker_head="h1")
    names_found = {c.transformation["subject"].ref for c in cses_layout}
    ck("s3-key-const: real s3_layout.py resolves >=10 keys", len(cses_layout) >= 10)
    ck("s3-key-const: ACCOUNTS_DIMENSION const captured",
       "s3key:gold/dimensions/accounts_dimension_latest.parquet" in names_found)
    ck("s3-key-const: advisor_fee_detail_key() function captured (f-string template)",
       any(r.startswith("s3key:gold/canonical/advisor_fee_detail/") for r in names_found))
    ck("s3-key-const: every CSE AC6-fidelity-ok", all(cse.cse_fidelity_ok(c)[0] for c in cses_layout))
    ck("s3-key-const: coverage clean (no silent drop)", cov_layout.resolved == cov_layout.attempted
       and not cov_layout.unresolved)

    # --- S3KeyReadWriteRecognizer vs REAL gold scripts, cross-checked against the DEPLOYED classifier -----
    s3_constants = {
        "ACCOUNTS_DIMENSION": "gold/dimensions/accounts_dimension_latest.parquet",
        "ADVISOR_ASSIGNMENTS": "gold/dimensions/advisor_assignments_history.parquet",
    }
    gold_dir = layout_path.parent.parent

    a00_path = gold_dir / "A_00.accounts_dimension.py"
    a00_text = a00_path.read_text(encoding="utf-8", errors="replace")
    t_a00 = EnrichedTree(source="data/black_diamond/scripts/gold/A_00.accounts_dimension.py",
                         capability=FrontEndCapability.RAW_TEXT, text=a00_text,
                         meta={"marker_head": "h1", "s3_constants": s3_constants})
    cses_a00, cov_a00 = S3KeyReadWriteRecognizer().recognize(t_a00, marker_head="h1")
    kinds_a00 = {(c.transformation["edges"][0].rtype) for c in cses_a00
                 if c.transformation["subject"].ref == "gold:A_00.accounts_dimension"}
    deployed_verdict_a00 = _classify_constant("ACCOUNTS_DIMENSION", a00_text)
    ck("s3-read-write: A_00 emits >=2 CSEs (read + write sites)", len(cses_a00) >= 2)
    ck("s3-read-write: A_00 READS ACCOUNTS_DIMENSION (get_object)", "reads" in kinds_a00)
    ck("s3-read-write: A_00 WRITES ACCOUNTS_DIMENSION (upload_file)", "writes" in kinds_a00)
    ck(f"s3-read-write: A_00 matches deployed extractor's 'both' verdict (got {deployed_verdict_a00!r})",
       deployed_verdict_a00 == "both" and {"reads", "writes"} <= kinds_a00)
    ck("s3-read-write: A_00 every CSE AC6-fidelity-ok", all(cse.cse_fidelity_ok(c)[0] for c in cses_a00))

    a01_path = gold_dir / "A_01.advisor_assignments.py"
    a01_text = a01_path.read_text(encoding="utf-8", errors="replace")
    t_a01 = EnrichedTree(source="data/black_diamond/scripts/gold/A_01.advisor_assignments.py",
                         capability=FrontEndCapability.RAW_TEXT, text=a01_text,
                         meta={"marker_head": "h1", "s3_constants": s3_constants})
    cses_a01, cov_a01 = S3KeyReadWriteRecognizer().recognize(t_a01, marker_head="h1")
    kinds_a01 = {c.transformation["edges"][0].rtype for c in cses_a01
                 if c.transformation["subject"].ref == "gold:A_01.advisor_assignments"
                 and c.transformation["edges"][0].target.ref.endswith("accounts_dimension_latest.parquet")}
    deployed_verdict_a01 = _classify_constant("ACCOUNTS_DIMENSION", a01_text)
    ck("s3-read-write: A_01 READS ACCOUNTS_DIMENSION only (_read_s3), no WRITES",
       kinds_a01 == {"reads"})
    ck(f"s3-read-write: A_01 matches deployed extractor's 'read' verdict (got {deployed_verdict_a01!r})",
       deployed_verdict_a01 == "read")

    p = sum(ok)
    print(f"\n=== COMPILERKIT batch-2 vs LIVE SDK + REAL source (AC2 cross-check): {p}/{len(ok)} PASS ===")
    sys.exit(0 if p == len(ok) else 1)
