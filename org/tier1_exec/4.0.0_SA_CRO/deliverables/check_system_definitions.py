#!/usr/bin/env python3
"""check_system_definitions -- the SYSTEM_DEFINITIONS.yaml schema gate (F-C1).

Andrew-direct 2026-08-10: "build the definitions checker" -- the explicit ask the no-new-gates
law requires. Spec is CVO's census remedy verbatim (@abfe77a537 row 5): the 4 required fields +
the status enum + the underscore-key rule, as a commit-time lint or a fail-loud in the serving
tool. This is the standalone engine; WIRING it (pre-commit vs serving-tool fail-loud) is CVO's
call as file owner.

Why it exists: 51/51 entries conform TODAY by discipline alone while a live tool
(comp-estate --definitions) compiles from the file. This makes tomorrow's nonconforming entry
LOUD instead of silently served to every agent.

Exit 0 = PASS (denominator printed). Exit 1 = named violations. Exit 2 = the file itself is
unreadable/unparseable (fail-closed: an unreadable registry is never a PASS).
Scope note (CVO's own precision, carried): this gate binds the PRESENT state of a versioned
registry; if the file ever grows an append-only history section, that section takes the
declaration pattern, not this lint.

Usage:
  python check_system_definitions.py [path/to/SYSTEM_DEFINITIONS.yaml]
  python check_system_definitions.py --self-test
"""
from __future__ import annotations

import io
import re
import sys

DEFAULT_PATH = "infra/system/ontology/SYSTEM_DEFINITIONS.yaml"
REQUIRED_FIELDS = ("definition", "authority", "sits_at", "status")
# ⚠ ENUM-FREEZE, documented rather than hidden (the predicate-not-roster class): these three are
# the OBSERVED values at 2026-08-10, frozen here because the file declares no status vocabulary of
# its own. A NEW lawful status will FIRE this gate (loud, not silent) until either (a) CVO declares
# the vocabulary IN SYSTEM_DEFINITIONS (preferred -- then this reads it from the file) or (b) this
# set is amended with the ratifying record cited. Routed to CVO at wiring.
STATUS_ENUM = {"reserved_ratified", "deprecated", "contested_unresolved"}
# keys are identifier-shaped: letters/digits/underscore, no spaces/hyphens. C0..C4/D1..D3 legal.
# NARROW RATIFIED EXCEPTION (measured on first live run, 2026-08-10): the dotted C-sublayer form
# C3.i / C3.ii is RATIFIED vocabulary -- the dot IS the name. Admitted as ^C\d+\.(i|ii)$ ONLY;
# a general dot-allowance would loosen the gate, and renaming ratified terms to satisfy a lint
# would be the lint outranking the vocabulary it guards. Flagged to CVO (file owner) at wiring.
KEY_RE = re.compile(r"^(?:[A-Za-z][A-Za-z0-9_]*|C\d+\.(?:i|ii))$")


def check(doc: dict) -> tuple[int, int, list[str]]:
    """Return (entries_checked, violation_count, messages). Pure -- no I/O."""
    msgs: list[str] = []
    terms = doc.get("terms")
    if not isinstance(terms, dict) or not terms:
        return 0, 1, ["FATAL: no 'terms' mapping -- the vocabulary section is absent or empty"]
    n = 0
    bad = 0
    for key, entry in terms.items():
        n += 1
        if not KEY_RE.match(str(key)):
            bad += 1
            msgs.append(f"KEY-RULE: '{key}' is not identifier-shaped (letters/digits/underscore)")
        if not isinstance(entry, dict):
            bad += 1
            msgs.append(f"SHAPE: '{key}' entry is {type(entry).__name__}, not a mapping")
            continue
        missing = [f for f in REQUIRED_FIELDS
                   if f not in entry or entry[f] is None
                   or (isinstance(entry[f], str) and not entry[f].strip())]
        if missing:
            bad += 1
            msgs.append(f"MISSING: '{key}' lacks required field(s): {', '.join(missing)}")
        status = entry.get("status")
        if status is not None and status not in STATUS_ENUM:
            bad += 1
            msgs.append(f"STATUS-ENUM: '{key}' status '{status}' not in {sorted(STATUS_ENUM)}")
    return n, bad, msgs


def self_test() -> int:
    """The gate must FIRE on each violation class and PASS a conforming doc. A gate never
    exercised on its failure limbs is a gate that cannot fail."""
    good_entry = {"definition": "d", "authority": "a", "sits_at": "s", "status": "reserved_ratified"}
    cases = [
        ("conforming doc PASSES", {"terms": {"alpha_one": dict(good_entry)}}, 0),
        ("missing required field FIRES", {"terms": {"alpha": {k: v for k, v in good_entry.items() if k != "authority"}}}, 1),
        ("bad status enum FIRES", {"terms": {"alpha": {**good_entry, "status": "vibes"}}}, 1),
        ("non-identifier key FIRES", {"terms": {"bad-key name": dict(good_entry)}}, 1),
        ("non-mapping entry FIRES", {"terms": {"alpha": "just prose"}}, 1),
        ("empty terms FIRES", {"terms": {}}, 1),
        ("extra fields are LAWFUL (annex precedent)", {"terms": {"alpha": {**good_entry, "describes": "x"}}}, 0),
        ("ratified dotted sublayer key (C3.i) is LAWFUL", {"terms": {"C3.i": dict(good_entry)}}, 0),
        ("general dotted key still FIRES (X.y)", {"terms": {"X.y": dict(good_entry)}}, 1),
        ("whitespace-only required value FIRES", {"terms": {"alpha": {**good_entry, "definition": "   "}}}, 1),
    ]
    failures = 0
    for label, doc, want_bad in cases:
        _, bad, _ = check(doc)
        ok = (bad == 0) == (want_bad == 0)
        print(f"  {'PASS' if ok else '*** FAIL ***'}  {label}")
        failures += 0 if ok else 1
    print(f"self-test: {failures} failure(s)")
    return 0 if failures == 0 else 1


def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        return self_test()
    path = argv[0] if argv else DEFAULT_PATH
    try:
        import yaml  # PyYAML is a standing dependency of the ontology tooling

        # DUPLICATE-KEY DETECTION (exercised breakpoint, 2026-08-10): yaml.safe_load silently
        # keeps the LAST duplicate mapping key -- so a vocabulary FORK (two entries for one term)
        # would be collapsed BEFORE any field check runs, and the checker would bless the survivor.
        # A loader-level hook sees every key as parsed; duplicates are fail-closed (exit 2 --
        # a forked registry is unreadable-in-the-sense-that-matters, never a PASS).
        class _DupSafeLoader(yaml.SafeLoader):
            pass

        def _no_dupes(loader, node, deep=False):
            seen = set()
            for k_node, _ in node.value:
                k = loader.construct_object(k_node, deep=deep)
                if k in seen:
                    raise yaml.YAMLError(f"DUPLICATE KEY '{k}' -- a vocabulary fork, collapsed silently by a plain load")
                seen.add(k)
            return yaml.SafeLoader.construct_mapping(loader, node, deep)

        _DupSafeLoader.add_constructor(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _no_dupes)
        doc = yaml.load(io.open(path, encoding="utf-8"), Loader=_DupSafeLoader)
    except Exception as e:  # noqa: BLE001 -- unreadable registry is fail-closed, never PASS
        print(f"UNREADABLE ({type(e).__name__}: {e}) -- an unreadable registry is NOT a pass")
        return 2
    n, bad, msgs = check(doc if isinstance(doc, dict) else {})
    for m in msgs:
        print(f"  {m}")
    print(f"check_system_definitions: {n} entries checked, {bad} violation(s) "
          f"[required={','.join(REQUIRED_FIELDS)}; status-enum={len(STATUS_ENUM)} values; key-rule=identifier]")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
