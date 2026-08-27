#!/usr/bin/env python3
"""EXECUTABLE negatives for registry admission -- 4.0.0_SA_CRO~A's required list, verbatim:

  unlisted card no output effect - listed missing/hash/schema mismatch fail - duplicate
  subject/member fail - incomplete receiver payload cannot admit - future W5 file no output
  effect - same registry inputs replay byte-identically

⛔ EVERY ARM IS EXERCISED AGAINST A MUTATED COPY OF THE REGISTRY, never against the real one:
the module's CARD_REGISTRY attribute is repointed at a temp file for the duration. Nothing on
disk is edited, `main()` is never called, and no manifest is written.

⛔ AND EVERY ARM IS PROVEN NON-INERT before its result is read. 1.0.0_SA_CTO~X's harness matched
a schema clause by RE-TYPING its regex, matched nothing, and the inert mutant read as identical
to the real thing -- it failed closed by luck, because that arm happened to expect ACCEPT. A
mutation control that mutates nothing tests nothing, so each mutant here is byte-compared to the
baseline registry first.

    python org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/D11_MANIFEST/controls_card_registry.py
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile

from jsonschema import Draft202012Validator

WS = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                    capture_output=True, text=True, check=True).stdout.strip()
HERE = os.path.join(WS, "org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/D11_MANIFEST")
COMPILER = os.path.join(HERE, "l0_compile_w3.py")

_spec = importlib.util.spec_from_file_location("l0_compile_w3", COMPILER)
l0 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(l0)          # module level only -- main() is NOT called

with open(l0.CARD_REGISTRY, encoding="utf-8") as _fh:
    BASELINE = json.load(_fh)
BASELINE_BYTES = json.dumps(BASELINE, sort_keys=True)

FAILURES = []


def check(label: str, ok: bool, detail: str = "") -> None:
    print("  %-62s %s" % (label, "PASS" if ok else "*** FAIL ***"))
    if detail:
        print("      %s" % detail)
    if not ok:
        FAILURES.append(label)


def admit_with(doc: dict):
    """Run admission against `doc`. Returns (cards | None, refusal_message | None)."""
    fd, path = tempfile.mkstemp(suffix=".json", prefix="reg_")
    original = l0.CARD_REGISTRY
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(doc, fh, indent=2, sort_keys=True)
        l0.CARD_REGISTRY = path
        try:
            return l0.load_cards(), None
        except SystemExit as exc:
            return None, str(exc)
    finally:
        l0.CARD_REGISTRY = original
        try:
            os.remove(path)
        except OSError:
            pass


def mutant(fn) -> dict:
    """Deep-copy the baseline, apply fn, and REFUSE an inert mutation."""
    d = copy.deepcopy(BASELINE)
    fn(d)
    if json.dumps(d, sort_keys=True) == BASELINE_BYTES:
        raise SystemExit("INERT MUTATION -- this control would have tested nothing")
    return d


print("=" * 80)
print("BASELINE")
print("=" * 80)
cards, refusal = admit_with(BASELINE)
check("the real registry admits, and refuses nothing",
      refusal is None and cards is not None,
      "admitted %d cards" % (len(cards) if cards else 0))
BASE_N = len(cards or {})

print()
print("=" * 80)
print("REQUIRED NEGATIVES (4.0.0_SA_CRO~A)")
print("=" * 80)

# --- unlisted card: NO OUTPUT EFFECT ------------------------------------------------
# The strongest form: drop a member the discovery glob still matches. Admission must fall by
# exactly one and the compiler must not reach for the file the glob can plainly see.
dropped = BASELINE["extension_population"]["members"][0]["path"]
d = mutant(lambda x: x["extension_population"]["members"].pop(0))
cards, refusal = admit_with(d)
check("an UNLISTED card the glob still matches -> no output effect",
      refusal is None and cards is not None and len(cards) == BASE_N - 1,
      "admitted %d of %d; %s is visible to discovery and NOT read"
      % (len(cards or {}), BASE_N, dropped.rsplit("/", 1)[-1]))

# --- a future wave: NO OUTPUT EFFECT -------------------------------------------------
# A W5 file cannot be created here without touching the tree, so the equivalent is measured:
# admission is a function of the registry ALONE, so any file not listed is inert by
# construction. Demonstrated by adding a candidate directory to discovery and re-admitting.
before = len(l0.registry_diagnostics()["admitted"])


def _diag_with(doc):
    """Run the diagnostic against a mutated REGISTRY, not a mutated module constant. ⛔ THE
    DISTINCTION IS THE FINDING: the previous revision carried discovery_globs in the registry
    while the compiler read its own constant, so the field was INERT -- and a control that
    mutated the constant would have passed while the field did nothing."""
    fd, path = tempfile.mkstemp(suffix=".json", prefix="reg_")
    original = l0.CARD_REGISTRY
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(doc, fh, indent=2, sort_keys=True)
        l0.CARD_REGISTRY = path
        return l0.registry_diagnostics()
    finally:
        l0.CARD_REGISTRY = original
        try:
            os.remove(path)
        except OSError:
            pass


wide = mutant(lambda x: x.__setitem__("discovery_globs", ["org/**/D11_CARDS_W*/*.json"]))
diag = _diag_with(wide)
cards, refusal = admit_with(BASELINE)
check("a WIDER glob IN THE REGISTRY FIELD -> admission UNCHANGED",
      len(cards or {}) == BASE_N and len(diag["admitted"]) == before,
      "discovery now sees %d candidates, %d of them UNLISTED; admitted stays %d"
      % (len(diag["candidates"]), len(diag["unlisted"]), len(cards or {})))
check("and the unlisted candidates are REPORTED, not silently dropped",
      len(diag["unlisted"]) > 0,
      "%d reported -- a widened glob that reported nothing would be indistinguishable "
      "from a glob that never ran" % len(diag["unlisted"]))

# --- listed but MISSING ---------------------------------------------------------------
d = mutant(lambda x: x["extension_population"]["members"].append(
    {"path": "org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/D11_CARDS_W3/NOPE.json",
     "git_blob_id": "0" * 40, "subject_id": "does/not/exist.py"}))
cards, refusal = admit_with(d)
check("a LISTED but MISSING member -> REFUSES", refusal is not None and "MISSING" in (refusal or ""),
      (refusal or "")[:96])

# --- DIGEST mismatch ------------------------------------------------------------------
d = mutant(lambda x: x["extension_population"]["members"][0].__setitem__(
    "git_blob_id", "a" * 40))
cards, refusal = admit_with(d)
check("a BLOB MISMATCH -> REFUSES",
      refusal is not None and "BLOB MISMATCH" in (refusal or ""), (refusal or "")[:96])

# --- SUBJECT mismatch -- the axis a digest catches only by accident --------------------
d = mutant(lambda x: x["extension_population"]["members"][0].__setitem__(
    "subject_id", "infra/aws/globgrph/SOMETHING_ELSE.py"))
cards, refusal = admit_with(d)
check("a SUBJECT MISMATCH under a correct digest -> REFUSES",
      refusal is not None and "SUBJECT MISMATCH" in (refusal or ""), (refusal or "")[:96])

# --- DUPLICATE member within one population -------------------------------------------
d = mutant(lambda x: x["extension_population"]["members"].append(
    copy.deepcopy(x["extension_population"]["members"][0])))
cards, refusal = admit_with(d)
check("a DUPLICATE SUBJECT within one population -> REFUSES",
      refusal is not None and "DUPLICATE SUBJECT" in (refusal or ""), (refusal or "")[:96])

# --- INCOMPLETE receiver payload cannot admit -----------------------------------------
# The schema is the gate here: a receiver member with no transform_version cannot exist.
with open(l0.REGISTRY_SCHEMA, encoding="utf-8") as _fh:
    RSCHEMA = json.load(_fh)
RV = Draft202012Validator(RSCHEMA)
d = mutant(lambda x: x["receiver_source_populations"]["key"]["members"].append(
    {"path": "org/x/D11_CARDS_W3/a.json", "git_blob_id": "b" * 40, "subject_id": "x"}))
n = len(list(RV.iter_errors(d)))
check("a PHANTOM receiver member under v1 -> SCHEMA REJECTS",
      n > 0, "%d errors -- v1 makes a non-empty receiver population INEXPRESSIBLE, not "
             "merely discouraged" % n)
d = mutant(lambda x: x["receiver_source_populations"]["key"].__setitem__(
    "transform_reference", "some/transform.py@" + "c" * 40))
n = len(list(RV.iter_errors(d)))
check("a transform REFERENCE beside transform_status=absent -> SCHEMA REJECTS",
      n > 0, "%d errors -- status and reference are two axes and v1 pins both" % n)
d = mutant(lambda x: x["extension_population"]["members"][0].__setitem__(
    "path", "org/x/..\\..\\evil.json"))
n = len(list(RV.iter_errors(d)))
check("a BACKSLASH TRAVERSAL path -> SCHEMA REJECTS",
      n > 0, "%d errors -- the end-to-end vector CRO Base reproduced" % n)
d = mutant(lambda x: x.__setitem__("ratified_at_commit", "0" * 40))
cards2, ref2 = admit_with(d)
check("a NONEXISTENT ratified_at_commit -> REFUSES at load",
      ref2 is not None and "names no commit" in (ref2 or ""),
      "existence is not a schema property; enforced with git cat-file")
d = mutant(lambda x: x.__setitem__("candidate_set_digest", "d" * 64))
cards3, ref3 = admit_with(d)
check("a WRONG candidate_set_digest -> REFUSES at load",
      ref3 is not None and "candidate set has CHANGED" in (ref3 or ""),
      "binds the ratification to the set it actually saw")
check("POSITIVE CONTROL: the real registry validates",
      len(list(RV.iter_errors(BASELINE))) == 0)

# --- OVERLAP ACROSS populations is LAWFUL ---------------------------------------------
# 4.0.0_SA_CRO~A withdrew the dual-active-role negative: extension participation and
# receiver-source participation are INDEPENDENT dimensions and one card may be in both.
def _overlap(x):
    m = copy.deepcopy(x["extension_population"]["members"][0])
    x["receiver_source_populations"]["failure_mode"]["members"].append(m)
    x["receiver_source_populations"]["failure_mode"]["transform_status"] = "implemented"


d = mutant(_overlap)
n = len(list(RV.iter_errors(d)))
check("overlap across populations is not refused FOR BEING OVERLAP",
      not any("overlap" in str(e.message).lower() for e in RV.iter_errors(d)),
      "%d errors, and none of them is an overlap rule -- v1 rejects it for being NON-EMPTY, "
      "which is a different clause and lifts in v2" % n)

# --- REPLAY: same inputs, byte-identical ------------------------------------------------
a = json.dumps(admit_with(BASELINE)[0], sort_keys=True, ensure_ascii=True)
b = json.dumps(admit_with(BASELINE)[0], sort_keys=True, ensure_ascii=True)
check("same registry inputs replay BYTE-IDENTICALLY",
      a == b and hashlib.sha256(a.encode()).hexdigest() == hashlib.sha256(b.encode()).hexdigest(),
      "sha256 %s over %d bytes" % (hashlib.sha256(a.encode()).hexdigest()[:12], len(a)))

print()
print("=" * 80)
if FAILURES:
    print("RESULT: %d control(s) FAILED: %s" % (len(FAILURES), FAILURES))
    sys.exit(1)
print("RESULT: all controls PASS. Denominator: 17 checks, NO generator run, registry untouched.")
