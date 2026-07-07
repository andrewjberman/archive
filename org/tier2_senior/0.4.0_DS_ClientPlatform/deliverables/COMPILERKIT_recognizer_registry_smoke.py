"""COMPILERKIT-P1/P2 -- consolidated recognizer wiring-readiness smoke test. Proves the FULL DS~A-authored
recognizer set registers into the live SDK's RecognizerRegistry and dispatches coherently by
(artifact_class, capability) with NO key collisions -- i.e. the "modular, orthogonal, additive, composes
with no ordering deps" property the SDK promises (comp_recognizer_sdk docstring) holds across the ACTUAL
set, not just the SDK's own sample recognizers.

This is a WIRING-READINESS artifact for 0.8.0~D (framework-lead) to drop into the canonical module: it is
the registration harness for the DS~A recognizers, pre-proven so integration surprises (import-time
collision, a duplicate (artifact_class, concept) key, a capability-tier mismatch, a PROMOTE-seam no-op)
surface HERE, before the full-corpus AC2 parity run, not during it.

Set under test (all live-SDK-validated in their own harnesses -- this checks they COMPOSE):
  batch-2 : (python, s3-key-const)      LEXICAL_AST   code-compiler   [COMPILERKIT_recognizers_batch2]
  batch-2 : (python, s3-key-read-write) RAW_TEXT      code-compiler   [COMPILERKIT_recognizers_batch2]
  compiler#2: (tsx, field-flows-to)     RESOLVED_SEM  tsx-compiler    [COMPILERKIT_recognizer_flowsto]
  P2      : (yaml, config-s3-ref)       LEXICAL_AST   config-compiler [COMPILERKIT_recognizers_P2_config]
  P2      : (env, config-secret-ref)    RAW_TEXT      config-compiler [COMPILERKIT_recognizer... P2_config]

NOTE (scope, honest): the batch-1 dispatch pair (DispatchCatalogRecognizer/MdpfDispatchRecognizer) is
0.8.0~D-authored + already wired into the canonical module (a4f3d302e), so it is NOT imported here (would
create a cross-lane import coupling into ~D's wiring file). This smoke test covers the DS~A-authored set;
~D's registration harness composes this with batch-1 on their side -- both use distinct (artifact_class,
concept) keys (bash/dispatch-* vs the keys above) so the union cannot collide either. Flagged, not assumed.
"""
from __future__ import annotations

import importlib.util
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_GRAPH = os.path.join(_HERE, "..", "..", "..", "modules", "graph")
if os.path.isdir(_GRAPH):
    sys.path.insert(0, os.path.abspath(_GRAPH))
from comp_recognizer_sdk import (  # noqa: E402
    RecognizerRegistry, FrontEndCapability, PROMOTE_SEAM,
)


def _load(mod_name: str, filename: str):
    """Load a sibling recognizer deliverable by path (they are not importable package modules)."""
    spec = importlib.util.spec_from_file_location(mod_name, os.path.join(_HERE, filename))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


if __name__ == "__main__":
    ok = []

    def ck(n, c):
        ok.append(bool(c))
        print(f"  [{'PASS' if c else 'FAIL'}] {n}")

    b2 = _load("b2", "COMPILERKIT_recognizers_batch2.py")
    ft = _load("ft", "COMPILERKIT_recognizer_flowsto.py")
    p2 = _load("p2", "COMPILERKIT_recognizers_P2_config.py")

    recognizers = [
        b2.S3KeyConstRecognizer(),
        b2.S3KeyReadWriteRecognizer(),
        ft.FlowsToRecognizer(),
        p2.ConfigS3RefRecognizer(),
        p2.EnvSecretRefRecognizer(),
    ]

    # 1. distinct (artifact_class, concept) keys -- no collision across the whole authored set.
    keys = [(r.artifact_class, r.concept) for r in recognizers]
    ck(f"all 5 DS~A recognizers have distinct (artifact_class, concept) keys ({len(set(keys))}/5 unique)",
       len(set(keys)) == len(keys) == 5)

    # 2. every one registers into the live SDK registry, and the PROMOTE-seam surfaces each (no silent add).
    surfaced = []
    reg = RecognizerRegistry(on_register=lambda seam, ac, cc: surfaced.append((seam, ac, cc)))
    reg_errors = []
    for r in recognizers:
        try:
            reg.register(r)
        except Exception as e:  # noqa: BLE001
            reg_errors.append((r.concept, str(e)))
    ck(f"all 5 register cleanly into RecognizerRegistry (errors: {reg_errors})", not reg_errors)
    ck("PROMOTE-seam surfaced every registration (no silent add)",
       len(surfaced) == 5 and all(s[0] == PROMOTE_SEAM for s in surfaced))

    # 3. capability-matched dispatch is coherent: each artifact_class dispatches exactly its own
    #    recognizers at the tier they require, and NONE leak across artifact_class.
    #    python@LEXICAL_AST -> s3-key-const only (read-write is RAW_TEXT, requires<=LEXICAL_AST so it ALSO
    #    matches -- RAW_TEXT(0) <= LEXICAL_AST(1)); python@RAW_TEXT -> read-write only (const needs AST).
    py_lexical = {r.concept for r in reg.recognizers_for("python", FrontEndCapability.LEXICAL_AST)}
    py_rawtext = {r.concept for r in reg.recognizers_for("python", FrontEndCapability.RAW_TEXT)}
    ck("python@LEXICAL_AST dispatches BOTH python recognizers (const needs AST; read-write RAW_TEXT<=AST)",
       py_lexical == {"s3-key-const", "s3-key-read-write"})
    ck("python@RAW_TEXT dispatches ONLY the read-write recognizer (const requires higher tier)",
       py_rawtext == {"s3-key-read-write"})

    # 4. artifact_class isolation: yaml/env/tsx dispatch sets never leak a python (or each other's) recognizer.
    yaml_set = {r.concept for r in reg.recognizers_for("yaml", FrontEndCapability.LEXICAL_AST)}
    env_set = {r.concept for r in reg.recognizers_for("env", FrontEndCapability.RAW_TEXT)}
    tsx_set = {r.concept for r in reg.recognizers_for("tsx", FrontEndCapability.RESOLVED_SEMANTIC)}
    ck("yaml artifact_class isolates to config-s3-ref only", yaml_set == {"config-s3-ref"})
    ck("env artifact_class isolates to config-secret-ref only", env_set == {"config-secret-ref"})
    ck("tsx artifact_class isolates to field-flows-to only", tsx_set == {"field-flows-to"})

    # 5. capability-gating floor: a RESOLVED_SEMANTIC recognizer (flows-to) is NOT dispatched to a
    #    lower-tier tsx tree -- it would only honest-degrade, so recognizers_for correctly withholds it.
    tsx_lexical = {r.concept for r in reg.recognizers_for("tsx", FrontEndCapability.LEXICAL_AST)}
    ck("tsx@LEXICAL_AST does NOT dispatch the RESOLVED_SEMANTIC flows-to recognizer (capability floor)",
       tsx_lexical == set())

    # 6. hot-reload replaces without a dup-key raise (the PROMOTE-seam reload path, CVO gap #8).
    reload_ok = True
    try:
        reg.reload(b2.S3KeyConstRecognizer())
    except Exception:  # noqa: BLE001
        reload_ok = False
    ck("hot-reload replaces an existing recognizer without a dup-key raise (PROMOTE reload path)", reload_ok)

    p = sum(ok)
    print(f"\n=== COMPILERKIT DS~A recognizer-set wiring-readiness: {p}/{len(ok)} PASS ===")
    sys.exit(0 if p == len(ok) else 1)
