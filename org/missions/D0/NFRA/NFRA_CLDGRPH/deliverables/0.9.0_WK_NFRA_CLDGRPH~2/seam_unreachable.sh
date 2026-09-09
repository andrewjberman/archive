#!/bin/bash
# D7-AC1, AS AMENDED @e27c871ccf -- IS THE RETIRED SEAM REACHABLE? A BEHAVIOUR PROBE, NOT A COUNT.
#
# The criterion this replaces counted TEXT ('comp-find' over the retired symbol names) while the
# property R7 asserts is BEHAVIOUR: that no caller can obtain the rebuild seam. Those are different
# questions, and on this population they are ANTI-CORRELATED -- the text count rose 29 -> 36 across
# the pass that REMOVED the seam, because a tombstone must NAME what it retires, a battery must
# NAME what it asserts refuses, and an unanchored pattern collides with two unrelated freshness
# families ('tool_probe.ensure_fresh', '_ensure_fresh_danger_map'). This probe asks the question
# the property actually poses: import the module a caller would import, reach for the three seam
# symbols a caller would reach for, and count how many HAND BACK AN OBJECT.
#
# REACHABLE is defined as "getattr returned without raising". A symbol that raises is unreachable
# NO MATTER WHICH exception it raises -- but the KIND is printed anyway, because an AttributeError
# would mean the tombstone had degraded to a SILENT refusal that a `getattr(m, n, None)` caller
# reads as "older build, skip the refresh" and carries on past. That degradation is invisible to
# the count and visible in the kind line.
#
# THE CONTROL EXISTS BECAUSE A ZERO HAS TWO CAUSES. A module that failed to import, or a module
# object with no live attribute access at all, would print a PERFECT zero on the three seam names
# while proving nothing about the retirement. SEAM_PROBE_CONTROL reaches for a constant the
# tombstone DOES define (`_RETIRED_BY`) through the SAME verb, on the SAME module object, in the
# SAME process: if that returns a non-empty value, attribute access is live and the zero above it
# is a REFUSAL rather than a dead import. Import failure never reaches the count -- it exits 2 as
# BLOCKED, so this script cannot report an absence it did not measure.
#
# Exit: 0 = seam unreachable and control fired; 1 = a seam symbol was reachable, or the control is
# dead; 2 = BLOCKED (the module could not be read or imported at all).
set -u
cd "$(git rev-parse --show-toplevel)" || exit 2

python - <<'PY'
import os
import sys

GLOBGRPH = os.path.join("infra", "aws", "globgrph")
MODULE = "_canonical"
SEAM = ("ensure_fresh", "_full_rebuild_only", "_append_fallback_sink")
CONTROL = "_RETIRED_BY"

target = os.path.join(GLOBGRPH, MODULE + ".py")
if not os.path.isfile(target):
    print("BLOCKED: %s is absent -- a probe cannot certify a module it never read" % target)
    sys.exit(2)

sys.path.insert(0, GLOBGRPH)
try:
    import _canonical
except BaseException as exc:                       # noqa: BLE001 - a failed import is a BLOCK
    print("BLOCKED: import of %s FAILED (%s: %s)" % (MODULE, type(exc).__name__, exc))
    print("BLOCKED: this is NOT a zero -- an unimportable module refuses every name for the")
    print("BLOCKED: wrong reason, which is exactly the false absence the control guards against")
    sys.exit(2)

print("SEAM_PROBE_TARGET=%s" % _canonical.__file__)
print("SEAM_PROBE_VERB=getattr(module, name) in-process; REACHABLE = returned without raising")

reachable = []
kinds = []
for name in SEAM:
    try:
        obj = getattr(_canonical, name)
    except BaseException as exc:                   # noqa: BLE001 - any raise is a refusal
        kinds.append(type(exc).__name__)
        print("  %-22s REFUSED  %s" % (name, type(exc).__name__))
        continue
    reachable.append(name)
    print("  %-22s REACHED  %r" % (name, obj))

print("SEAM_REACHABLE=%d of %d" % (len(reachable), len(SEAM)))
if reachable:
    print("SEAM_REACHABLE_NAMES=%s" % ",".join(reachable))
print("SEAM_REFUSAL_KIND_RUNTIMEERROR=%d of %d  (an AttributeError here would be a SILENT refusal"
      " a hasattr() caller carries on past)" % (kinds.count("RuntimeError"), len(SEAM)))

try:
    value = getattr(_canonical, CONTROL)
except BaseException as exc:                       # noqa: BLE001
    print("SEAM_PROBE_CONTROL=DEAD -- %s raised %s; the zero above measures a dead module, not a"
          " retirement" % (CONTROL, type(exc).__name__))
    sys.exit(1)
if not isinstance(value, str) or not value.strip():
    print("SEAM_PROBE_CONTROL=DEAD -- %s resolved to %r, which certifies nothing" % (CONTROL, value))
    sys.exit(1)
print("SEAM_PROBE_CONTROL=FIRED -- %s -> %r returned through the SAME verb on the SAME module"
      " object, so attribute access is LIVE and the count above is a refusal" % (CONTROL, value))

sys.exit(1 if reachable else 0)
PY
