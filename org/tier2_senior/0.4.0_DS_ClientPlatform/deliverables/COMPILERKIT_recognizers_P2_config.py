"""NFRA_COMPILERKIT.P2 -- the config-artifact compiler (YAML/TOML/env/tf-vars), authored against the
live SDK per the P2 split (me = recognizer authoring, 0.8.0~D = framework/wiring; TO:
org/tier1_exec/2.0.0_SA_COO/task_orders/NFRA_COMPILERKIT.P2.config-compiler.md).

SCOPE (per 0.8.0~D's framework review, ac72b0399, 2026-07-07): cse_schema.Entity has NO config-specific
type (no EnvVar/ConfigKey/TfVar) -- a config recognizer only resolves to a TYPED entity when a config
VALUE cross-references something already modeled (an S3 URI, a secret ARN/id, an IAM role ARN, an
endpoint URL). Everything else correctly honest-degrades to Concept(untyped)+low per req #3 -- that's
LAW 1, not a gap. This file builds the two highest-value, REAL-source-grounded cross-reference
recognizers: S3-URI-in-YAML (LEXICAL_AST, PyYAML compose()) and secret-id-in-env (RAW_TEXT). No live
graph exists to diff against (no existing yaml/toml/env/tfvars extractor anywhere in extract_pipeline.py
/ trace_graph.py per ~D) -- so the acceptance bar is fidelity_check + honest-degrade, not a structural
parity diff (~D flagged this framing to COO/CTO).

Firm/scope collision note (CTO ruling, applied from the start per ~D's ask): config artifact BASENAMES
collide the same way gold-script basenames did -- gold_freshness_config.yaml is byte-identical across
data/{black_diamond,inf,cot}/scripts/gold/, and secret-ids.env is byte-identical across
infra/aws/ec2/{bd-49f,bd-cot}-auto-login/. A pipeline-dir firm label (PIPELINE_MAP) covers the data/
tree; outside it (infra/aws/ec2/{service}/), the immediate parent directory IS the deterministic
service-scope token (still derived from provenance.source, never guessed) -- _scope_from_source()
generalizes batch-2's _firm_from_source() to cover both.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

import yaml

# Live SDK (0.8.0~D). Path-robust import (sibling in org/modules/graph), mirroring batch-1/2's bootstrap.
_GRAPH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "modules", "graph")
if os.path.isdir(_GRAPH):
    sys.path.insert(0, os.path.abspath(_GRAPH))
from comp_recognizer_sdk import (  # noqa: E402
    Recognizer, emit_cse, Site, EnrichedTree, EntityRef, RelationshipDelta, Provenance,
    Entity, Relationship, Transformation, FrontEndCapability,
)

_TOOLS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", ".tools")
if os.path.isdir(_TOOLS):
    sys.path.insert(0, os.path.abspath(_TOOLS))
from safe_deploy_core import PIPELINE_MAP  # noqa: E402


def _scope_from_source(source: str) -> str:
    """Deterministic scope token from provenance.source -- PIPELINE_MAP firm label under data/{pipeline}/,
    else the immediate parent directory (the service identity for infra/aws/ec2/{service}/ configs).
    Never guessed; a generalization of COMPILERKIT_recognizers_batch2._firm_from_source for non-data/
    sources (config artifacts live outside the 3-pipeline data/ tree, unlike gold scripts + s3_layout.py)."""
    norm = source.replace("\\", "/")
    for data_dir, (_bucket, label) in PIPELINE_MAP.items():
        if norm.startswith(f"data/{data_dir}/"):
            return label
    parts = [p for p in norm.split("/") if p]
    if len(parts) >= 2:
        return parts[-2]
    return "unscoped"


_S3_URI_RE = re.compile(r"^s3://([a-z0-9.-]+)(/.*)?$")


class ConfigS3RefRecognizer(Recognizer):
    """YAML config values that are literal s3:// URIs (e.g. gold_freshness_config.yaml's
    s3_key_prefix). LEXICAL_AST tier -- walks a PyYAML compose() node tree (not safe_load: compose()
    keeps per-node start_mark.line for real file:line provenance, safe_load discards it). The S3 URI
    itself already embeds the bucket name, so the TARGET ref is inherently firm-disambiguated (no
    s3://opal-data-bd/... vs s3://opal-data-cot/... collision is possible); only the config-artifact
    SUBJECT ref needs the scope token (gold_freshness_config.yaml is byte-identical across firms)."""
    artifact_class = "yaml"
    concept = "config-s3-ref"
    requires = FrontEndCapability.LEXICAL_AST
    compiler_id = "config-compiler"

    def iter_sites(self, tree: EnrichedTree):
        root = tree.root if tree.root is not None else yaml.compose(tree.text)
        if root is None:
            return
        stack = [root]
        while stack:
            node = stack.pop()
            if isinstance(node, yaml.ScalarNode):
                m = _S3_URI_RE.match(node.value)
                if m:
                    yield Site(source=tree.source, locus=f"L{node.start_mark.line + 1}",
                               evidence=node.value, payload={"uri": node.value})
            elif isinstance(node, yaml.MappingNode):
                for k, v in node.value:
                    stack.append(k)
                    stack.append(v)
            elif isinstance(node, yaml.SequenceNode):
                stack.extend(node.value)

    def emit(self, site: Site, tree: EnrichedTree, *, marker_head: str):
        scope = _scope_from_source(site.source)
        artifact = f"config:{scope}:{Path(tree.source).stem}"
        target = f"s3:{site.payload['uri'][len('s3://'):]}"
        prov = Provenance(source=site.source, locus=site.locus, recognizer=self.concept, evidence=site.evidence)
        return [emit_cse(
            verb=Transformation.CREATE.value,
            subject=EntityRef(Entity.ARTIFACT.value, artifact),
            edges=[RelationshipDelta(Relationship.REFERENCES.value, EntityRef(Entity.S3BUCKET.value, target))],
            provenance=prov, confidence=1.0, marker_head=marker_head,
            producer_kind=self.producer_kind, compiler_id=self.compiler_id, artifact_class=self.artifact_class,
        )]


# a SECRET-named key whose value doesn't look like a clean secret-id/path token (spaces, empty after
# trim, obviously not a bare identifier) is genuinely UNTYPABLE -- LAW 1 says degrade, never guess a ref.
_CLEAN_TOKEN_RE = re.compile(r"^[A-Za-z0-9_./-]+$")
_ENV_KV_RE = re.compile(r"^([A-Z][A-Z0-9_]*)\s*=\s*(.*)$")


class EnvSecretRefRecognizer(Recognizer):
    """env-file KEY=VALUE lines where KEY names a secret (per repo convention, *_SECRET_ID / *SECRET*)
    and VALUE is a secret-id POINTER (a Secrets Manager name/path, never a secret VALUE per the files'
    own header contracts -- e.g. infra/aws/ec2/bd-cot-auto-login/secret-ids.env:3 'These are secret-id
    POINTERS ... NEVER secret VALUES'). RAW_TEXT tier -- line-scoped, same shape as batch-2's
    S3KeyReadWriteRecognizer. A SECRET-named key whose value fails the clean-token shape check (rare,
    but a placeholder/malformed value is a real possibility in a .env.example) HONEST-DEGRADES rather
    than emitting a guessed SecretRef -- LAW 1 exercised here, not just at the SDK's capability gate."""
    artifact_class = "env"
    concept = "config-secret-ref"
    requires = FrontEndCapability.RAW_TEXT
    compiler_id = "config-compiler"

    def iter_sites(self, tree: EnrichedTree):
        for lineno, line in enumerate(tree.text.splitlines(), start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            m = _ENV_KV_RE.match(stripped)
            if not m:
                continue
            key, value = m.group(1), m.group(2).strip()
            if "SECRET" not in key or not value:
                continue
            yield Site(source=tree.source, locus=f"L{lineno}", evidence=stripped,
                       payload={"key": key, "value": value})

    def emit(self, site: Site, tree: EnrichedTree, *, marker_head: str):
        value = site.payload["value"]
        if not _CLEAN_TOKEN_RE.match(value):
            return [self.degrade(site, marker_head=marker_head)]
        scope = _scope_from_source(site.source)
        artifact = f"config:{scope}:{Path(tree.source).stem}"
        prov = Provenance(source=site.source, locus=site.locus, recognizer=self.concept, evidence=site.evidence)
        return [emit_cse(
            verb=Transformation.CREATE.value,
            subject=EntityRef(Entity.ARTIFACT.value, artifact),
            edges=[RelationshipDelta(Relationship.REFERENCES.value,
                                     EntityRef(Entity.SECRETREF.value, f"secret:{value}"))],
            provenance=prov, confidence=1.0, marker_head=marker_head,
            producer_kind=self.producer_kind, compiler_id=self.compiler_id, artifact_class=self.artifact_class,
        )]


if __name__ == "__main__":
    import cse_schema as cse
    ok = []

    def ck(n, c):
        ok.append(bool(c))
        print(f"  [{'PASS' if c else 'FAIL'}] {n}")

    # --- ConfigS3RefRecognizer vs REAL gold_freshness_config.yaml (bd + cot, byte-identical basenames) ---
    ws_root = Path(_GRAPH).resolve().parent.parent.parent  # org/modules/graph -> org -> workspace root
    bd_yaml_path = ws_root / "data" / "black_diamond" / "scripts" / "gold" / "gold_freshness_config.yaml"
    bd_yaml_text = bd_yaml_path.read_text(encoding="utf-8")
    t_bd_yaml = EnrichedTree(source="data/black_diamond/scripts/gold/gold_freshness_config.yaml",
                             capability=FrontEndCapability.LEXICAL_AST, text=bd_yaml_text,
                             root=yaml.compose(bd_yaml_text), meta={"marker_head": "h1"})
    cses_bd_yaml, cov_bd_yaml = ConfigS3RefRecognizer().recognize(t_bd_yaml, marker_head="h1")
    # parity-scan excludes comment lines (a '#   s3_key_prefix: s3://bucket/prefix/' doc example at L8 is
    # NOT a real config value -- PyYAML correctly never sees it; a naive regex would, so exclude to match).
    regex_count = sum(1 for ln in bd_yaml_text.splitlines() if not ln.strip().startswith("#")
                      and re.search(r"s3://[a-z0-9.\-/]+", ln))
    ck(f"config-s3-ref: bd yaml resolves every REAL s3:// value, correctly skips the L8 comment example "
       f"(recognizer={len(cses_bd_yaml)}, regex-scan={regex_count})",
       len(cses_bd_yaml) == regex_count and len(cses_bd_yaml) > 0)
    ck("config-s3-ref: bd yaml subject is scope-tagged (config:bd:gold_freshness_config)",
       all(c.transformation["subject"].ref == "config:bd:gold_freshness_config" for c in cses_bd_yaml))
    ck("config-s3-ref: bd yaml targets opal-data-bd bucket (URI-embedded, inherently disambiguated)",
       all(c.transformation["edges"][0].target.ref.startswith("s3:opal-data-bd/") for c in cses_bd_yaml))
    ck("config-s3-ref: every CSE AC6-fidelity-ok", all(cse.cse_fidelity_ok(c)[0] for c in cses_bd_yaml))
    ck("config-s3-ref: coverage clean (no silent drop)", cov_bd_yaml.resolved == cov_bd_yaml.attempted
       and not cov_bd_yaml.unresolved)

    cot_yaml_path = ws_root / "data" / "cot" / "scripts" / "gold" / "gold_freshness_config.yaml"
    cot_yaml_text = cot_yaml_path.read_text(encoding="utf-8")
    t_cot_yaml = EnrichedTree(source="data/cot/scripts/gold/gold_freshness_config.yaml",
                              capability=FrontEndCapability.LEXICAL_AST, text=cot_yaml_text,
                              root=yaml.compose(cot_yaml_text), meta={"marker_head": "h1"})
    cses_cot_yaml, _cov = ConfigS3RefRecognizer().recognize(t_cot_yaml, marker_head="h1")
    bd_subjects = {c.transformation["subject"].ref for c in cses_bd_yaml}
    cot_subjects = {c.transformation["subject"].ref for c in cses_cot_yaml}
    ck("config-s3-ref: bd + cot gold_freshness_config.yaml (identical basename) get DISTINCT scoped subjects",
       bd_subjects == {"config:bd:gold_freshness_config"} and cot_subjects == {"config:cot:gold_freshness_config"})

    # --- EnvSecretRefRecognizer vs REAL secret-ids.env (bd-cot-auto-login + bd-49f-auto-login, same basename) ---
    cot_env_path = ws_root / "infra" / "aws" / "ec2" / "bd-cot-auto-login" / "secret-ids.env"
    cot_env_text = cot_env_path.read_text(encoding="utf-8")
    t_cot_env = EnrichedTree(source="infra/aws/ec2/bd-cot-auto-login/secret-ids.env",
                             capability=FrontEndCapability.RAW_TEXT, text=cot_env_text,
                             meta={"marker_head": "h1"})
    cses_cot_env, cov_cot_env = EnvSecretRefRecognizer().recognize(t_cot_env, marker_head="h1")
    secret_refs = {c.transformation["edges"][0].target.ref for c in cses_cot_env
                   if c.transformation["edges"]}
    ck("config-secret-ref: cot-auto-login secret-ids.env resolves the 3 real *_SECRET_ID pointers",
       secret_refs == {"secret:blackdiamond/cot/otp-gateway-token", "secret:blackdiamond/cot/otp-relay",
                        "secret:astn/kimi/api-key"})
    ck("config-secret-ref: subject is service-scoped (config:bd-cot-auto-login:secret-ids)",
       all(c.transformation["subject"].ref == "config:bd-cot-auto-login:secret-ids" for c in cses_cot_env))
    ck("config-secret-ref: every CSE AC6-fidelity-ok", all(cse.cse_fidelity_ok(c)[0] for c in cses_cot_env))

    m365_env_path = ws_root / "infra" / "aws" / "ec2" / "m365-mcp-gateway" / ".env.example"
    m365_env_text = m365_env_path.read_text(encoding="utf-8")
    t_m365 = EnrichedTree(source="infra/aws/ec2/m365-mcp-gateway/.env.example",
                          capability=FrontEndCapability.RAW_TEXT, text=m365_env_text, meta={"marker_head": "h1"})
    cses_m365, _cov_m365 = EnvSecretRefRecognizer().recognize(t_m365, marker_head="h1")
    ck("config-secret-ref: blank CLIENT_SECRET= (no value) is correctly NOT attempted (nothing to recognize)",
       len(cses_m365) == 0)

    # --- LAW-1 honest-degrade proof: a SECRET-named key with a malformed value (synthetic -- no real repo
    # example exercises this path; same precedent as the SDK's own self-test using synthetic text to
    # prove the capability-gating degrade path) must NOT guess a SecretRef, must degrade to Concept+low. ---
    synth_text = "API_SECRET_TOKEN = not a clean id (placeholder, spaces)\n"
    t_synth = EnrichedTree(source="infra/aws/ec2/synthetic-svc/config.env",
                           capability=FrontEndCapability.RAW_TEXT, text=synth_text, meta={"marker_head": "h1"})
    cses_synth, cov_synth = EnvSecretRefRecognizer().recognize(t_synth, marker_head="h1")
    degraded_ok = (len(cses_synth) == 1
                   and cses_synth[0].transformation["subject"].etype == Entity.CONCEPT.value
                   and float(cses_synth[0].qualifiers.get("confidence", 1.0)) <= cse.LOW_CONFIDENCE_MAX)
    ck("config-secret-ref: malformed SECRET value honest-degrades to Concept(untyped)+low (LAW 1)",
       degraded_ok)

    p = sum(ok)
    print(f"\n=== COMPILERKIT-P2 config recognizers vs REAL source (bd+cot+infra): {p}/{len(ok)} PASS ===")
    sys.exit(0 if p == len(ok) else 1)
