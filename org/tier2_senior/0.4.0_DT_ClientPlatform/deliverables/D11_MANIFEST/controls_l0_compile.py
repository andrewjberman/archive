#!/usr/bin/env python3
"""EXECUTABLE controls for the two compiler obligations 4.0.0_SA_CRO~A assigned to this lane.

Their rework was exact and both halves of it are the point:
  "Add executable invalid-first/valid-last duplicate-key negative. MECHANISM ALONE DOES NOT
   PROVE FAIL-CLOSED BEHAVIOR."
  "Add reversed-insertion byte-equality control for canonical emission. sort_keys=True ALONE IS
   AN UNTESTED PROMISE."

Both were true of what I had shipped. My duplicate-key exercise ran VALID-FIRST, which is the
arm the parser's last-wins rule makes harmless -- the dangerous ordering is INVALID-FIRST,
because there the discarded value is the bad one and the survivor validates. An exercise that
only runs the harmless arm reads as a proof and is not one.

⛔ RUNS NOTHING. This imports l0_compile_w3 for its loader and its dump settings; `main()` is
never called and no manifest is written. Module import is constants + function definitions.

    python org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/D11_MANIFEST/controls_l0_compile.py
"""
from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile

WS = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                    capture_output=True, text=True, check=True).stdout.strip()
COMPILER = os.path.join(
    WS, "org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/D11_MANIFEST/l0_compile_w3.py")

_spec = importlib.util.spec_from_file_location("l0_compile_w3", COMPILER)
l0 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(l0)          # module level only -- main() is NOT called

FAILURES = []


def check(label: str, ok: bool, detail: str = "") -> None:
    print("  %-64s %s" % (label, "PASS" if ok else "*** FAIL ***"))
    if detail:
        print("      %s" % detail)
    if not ok:
        FAILURES.append(label)


# ---------------------------------------------------------------------------------------
# CONTROL 1 -- DUPLICATE RAW OBJECT KEYS, INVALID FIRST AND VALID LAST
# ---------------------------------------------------------------------------------------
# The suffix-keyed object was chosen because "duplicate keys are impossible". That is a
# property of the parsed dict, NOT of the bytes. Python keeps the LAST duplicate, so
# invalid-first/valid-last is the ordering where the document validates and the rejected value
# is the one a reviewer would have caught.
DUP_INVALID_FIRST = (
    '{"variant_suffixes": {'
    '".wal": {"mint": "banana", "note": ""}, '
    '".wal": {"mint": "conditional", "note": "write-ahead log"}}}')
DUP_VALID_FIRST = (
    '{"variant_suffixes": {'
    '".wal": {"mint": "conditional", "note": "write-ahead log"}, '
    '".wal": {"mint": "banana", "note": ""}}}')
CLEAN = (
    '{"variant_suffixes": {'
    '".wal": {"mint": "conditional", "note": "write-ahead log"}, '
    '".lock": {"mint": "unknown", "note": "lock side-artifact"}}}')


def _write(text: str) -> str:
    fd, path = tempfile.mkstemp(suffix=".json", prefix="l0ctl_")
    with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    return path


def _strict_refuses(path: str):
    try:
        l0.load_json_strict(path)
    except SystemExit as exc:
        return str(exc)
    return None


print("=" * 84)
print("CONTROL 1 -- DUPLICATE RAW OBJECT KEYS (4.0.0_SA_CRO~A rework 2)")
print("=" * 84)
_paths = []
try:
    p_bad_first = _write(DUP_INVALID_FIRST)
    p_bad_last = _write(DUP_VALID_FIRST)
    p_clean = _write(CLEAN)
    _paths = [p_bad_first, p_bad_last, p_clean]

    # THE HAZARD, DEMONSTRATED rather than described.
    survivor = json.load(open(p_bad_first, encoding="utf-8"))["variant_suffixes"][".wal"]
    check("HAZARD: plain json.load on invalid-first keeps the VALID last value",
          survivor == {"mint": "conditional", "note": "write-ahead log"},
          "plain parser returned %r -- the INVALID value is gone and no validator can see it"
          % (survivor,))

    check("invalid-first / valid-last  -> strict loader REFUSES",
          _strict_refuses(p_bad_first) is not None,
          (_strict_refuses(p_bad_first) or "")[:100])
    check("valid-first / invalid-last  -> strict loader REFUSES",
          _strict_refuses(p_bad_last) is not None,
          "the harmless ordering must refuse too, or the guard is order-dependent")

    # POSITIVE CONTROL: the guard must not simply refuse everything.
    parsed = l0.load_json_strict(p_clean)
    check("POSITIVE CONTROL: a clean two-key object parses",
          set(parsed["variant_suffixes"]) == {".wal", ".lock"},
          "keys parsed: %s" % sorted(parsed["variant_suffixes"]))

    # AND THE GUARD MUST REACH NESTED OBJECTS, not only the top level.
    p_nested = _write('{"a": {"b": {"k": 1, "k": 2}}}')
    _paths.append(p_nested)
    check("a duplicate NESTED three levels down -> strict loader REFUSES",
          _strict_refuses(p_nested) is not None,
          "object_pairs_hook fires per object, so depth must not matter")
finally:
    for _p in _paths:
        try:
            os.remove(_p)
        except OSError:
            pass

# ---------------------------------------------------------------------------------------
# CONTROL 2 -- CANONICAL EMISSION, REVERSED INSERTION ORDER
# ---------------------------------------------------------------------------------------
# sort_keys=True is a promise about bytes. Two dicts holding identical data in opposite
# insertion order must serialise IDENTICALLY, or every digest comparison downstream reports
# drift that does not exist.
print()
print("=" * 84)
print("CONTROL 2 -- CANONICAL EMISSION UNDER REVERSED INSERTION (4.0.0_SA_CRO~A rework 3)")
print("=" * 84)

FORWARD = {"member_set": {"enumerable": False,
                          "variant_suffixes": {".lock": {"mint": "unknown", "note": "l"},
                                               ".wal": {"mint": "conditional", "note": "w"}},
                          "basis": "measured"},
           "id": "kuzu_nessie_db.rebuild.tmp.SET"}
REVERSED = {"id": "kuzu_nessie_db.rebuild.tmp.SET",
            "member_set": {"basis": "measured",
                           "variant_suffixes": {".wal": {"note": "w", "mint": "conditional"},
                                                ".lock": {"note": "l", "mint": "unknown"}},
                           "enumerable": False}}

# THE COMPILER'S OWN DUMP SETTINGS, not a retyped guess at them.
KW = {"indent": 2, "ensure_ascii": True, "sort_keys": True}
a = json.dumps(FORWARD, **KW)
b = json.dumps(REVERSED, **KW)
check("reversed insertion order -> BYTE-IDENTICAL under the emission settings",
      a == b,
      "%d vs %d bytes" % (len(a.encode()), len(b.encode())))

# THE ARM THAT PROVES THE CONTROL CAN DISTINGUISH. Without it, byte-equality would also
# "pass" for a comparison that never looked -- a control that cannot fail tests nothing.
KW_NOSORT = {"indent": 2, "ensure_ascii": True}
check("NEGATIVE ARM: the same pair WITHOUT sort_keys is byte-DIFFERENT",
      json.dumps(FORWARD, **KW_NOSORT) != json.dumps(REVERSED, **KW_NOSORT),
      "so the equality above is the sorting, not an insensitive comparison")

# AND THE PROMISE MUST BE READ OFF THE COMPILER, not restated here.
src = open(COMPILER, encoding="utf-8").read()
check("the compiler's own dump carries sort_keys=True",
      "json.dump(out, f, indent=2, ensure_ascii=True, sort_keys=True)" in src,
      "read from %s" % os.path.relpath(COMPILER, WS).replace(os.sep, "/"))

print()
print("=" * 84)
if FAILURES:
    print("RESULT: %d of the controls FAILED: %s" % (len(FAILURES), FAILURES))
    sys.exit(1)
print("RESULT: all controls PASS. Denominator: 8 checks, and NO generator was run.")
