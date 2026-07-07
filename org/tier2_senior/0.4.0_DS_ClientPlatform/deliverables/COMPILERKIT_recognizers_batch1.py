"""COMPILERKIT-P1 recognizer batch-1 (DS-authored draft) -- built against 0.8.0~D's framework interface
(design 4a7e739dd). LEXICAL-ONLY per CTO's #3 ruling. Author-DS/commit-AE: ~D commits into the SDK +
runs the AC2 parity-oracle. Built against the STABLE a-c signatures (the SDK skeleton lands on CTO ACK);
the recognizer LOGIC is the deliverable. LAW-2 provenance uplift (file:line) baked into every Site via
the extract_iam template `content[:pos].count("\\n")+1`.

This batch = the parity-critical DISPATCH pair (compiler #1's #2 dispatch-catalog = my D1-class + the
MDPF EC2 dispatch = the DEBTSCAN root-fix). They CONVERGE: one recognizer body closes the DEBTSCAN
reachability FP-block AND is compiler #1's dispatch recognizer in COMPILERKIT.
"""
from __future__ import annotations

import re
from pathlib import Path

# Framework symbols (0.8.0~D SDK; skeleton pending CTO ACK -- these signatures are stable for the lexical
# set per the interface handoff). ~D resolves these imports when committing into the SDK:
#   from compilerkit import Recognizer, Site, FrontEndCapability, emit_cse, EntityRef, RelationshipDelta, Provenance
#   from cse_schema import Entity, Relationship, Transformation


class DispatchCatalogRecognizer(Recognizer):  # noqa: F821 (framework symbol, ~D-provided)
    """Compiler #1 recognizer #2 -- the gold-dispatch CATALOG heredoc (the D1-class). A dispatch runner
    TRIGGERS each catalog-listed gold script. artifact_class=bash, requires=RAW_TEXT (regex over shell).
    AC2 parity target: reproduces today's dispatcher-[TRIGGERS]->script C1 edges (the 84bb8377b D1 fix)."""
    artifact_class = "bash"
    concept = "gold-dispatch-catalog"
    requires = FrontEndCapability.RAW_TEXT  # noqa: F821

    _CATALOG = re.compile(r"read -r -d '' CATALOG << 'CATALOG_END'(.*?)CATALOG_END", re.DOTALL)
    _ROW = re.compile(r"^\s*(\S+)\|(\S+\.py)\|", re.MULTILINE)  # ID|filename|flags

    def iter_sites(self, tree):
        content = tree.text
        cat = self._CATALOG.search(content)
        if not cat:
            return
        body, base = cat.group(1), cat.start(1)
        for m in self._ROW.finditer(body):
            pos = base + m.start()
            line = content[:pos].count("\n") + 1  # LAW-2 uplift: capture the match line
            yield Site(  # noqa: F821
                source=tree.source, locus=f"L{line}", evidence=m.group(0).strip(),
                payload={"script_id": m.group(1), "filename": m.group(2)},
            )

    def emit(self, site, tree):
        script = Path(site.payload["filename"]).stem
        return [emit_cse(  # noqa: F821
            verb=Transformation.CREATE,  # noqa: F821 -- asserting the trigger relationship
            subject=EntityRef(Entity.SERVICE, ref=f"dispatch:{Path(site.source).stem}"),  # noqa: F821
            edges=[RelationshipDelta(  # noqa: F821
                Relationship.TRIGGERS, target=EntityRef(Entity.MODULE, ref=f"gold:{script}"))],  # noqa: F821
            provenance=Provenance(  # noqa: F821
                source=site.source, locus=site.locus, recognizer=self.concept, evidence=site.evidence),
            confidence=1.0, marker_head=tree.marker_head,
        )]


class MdpfDispatchRecognizer(Recognizer):  # noqa: F821
    """DEBTSCAN root-fix + COMPILERKIT #1 -- the MDPF EC2 stage-runner. Distinct front-end shape from the
    CATALOG heredoc: `run_step LABEL <relpath>.py args...` + a few `X_SCRIPT="${SCRIPTS_DIR}/<relpath>.py"`
    vars. Source-verified 2026-07-07 (edges the build_mdpf_*/aggregate/wsb/wsd/wse/rollup/ownts block +
    validate_schwab_native_custody + pull_orion_model_composition -- the DEBTSCAN reachability FP-block)."""
    artifact_class = "bash"
    concept = "mdpf-ec2-dispatch"
    requires = FrontEndCapability.RAW_TEXT  # noqa: F821

    _RUN_STEP = re.compile(r"run_step\s+\S+\s+(\S+\.py)\b")
    _VAR = re.compile(r'\w+_SCRIPT="\$\{SCRIPTS_DIR\}/(\S+\.py)"')

    def iter_sites(self, tree):
        content = tree.text
        for pat in (self._RUN_STEP, self._VAR):
            for m in pat.finditer(content):
                line = content[:m.start()].count("\n") + 1
                yield Site(  # noqa: F821
                    source=tree.source, locus=f"L{line}", evidence=m.group(0).strip(),
                    payload={"relpath": m.group(1)},
                )

    def emit(self, site, tree):
        script = Path(site.payload["relpath"]).stem
        return [emit_cse(  # noqa: F821
            verb=Transformation.CREATE,  # noqa: F821
            subject=EntityRef(Entity.SERVICE, ref="mdpf-daily-runner"),  # noqa: F821
            edges=[RelationshipDelta(  # noqa: F821
                Relationship.TRIGGERS, target=EntityRef(Entity.MODULE, ref=f"gold:{script}"))],  # noqa: F821
            provenance=Provenance(  # noqa: F821
                source=site.source, locus=site.locus, recognizer=self.concept, evidence=site.evidence),
            confidence=1.0, marker_head=tree.marker_head,
        )]

# NEXT in batch (authoring against the same interface): S3KeyConstRecognizer (#1, ast, requires=LEXICAL_AST
# -> Entity.S3BUCKET/DATASET + a key ref); read/write-classifier (#3, READS/WRITES); then compiler #2's
# TSX passes (FLOWS_TO HELD pending CTO's KIND+condition schema-bump decision-1). Each AC2 parity-oracle.
