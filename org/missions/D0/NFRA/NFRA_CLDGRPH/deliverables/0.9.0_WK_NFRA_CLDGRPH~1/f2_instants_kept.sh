#!/usr/bin/env bash
# F2-AC1 -- EVERY ASK BEGAN WITHIN 5 s OF ITS INSTANT.
#
# Reads the three capture files f2_ask_T0.txt / T1 / T2 written by f2_ask_at.sh,
# each of which prints LAPTOP_OFFSET_S_T<n> = T_START - instant on ONE clock
# (the laptop's), so the number never depends on agreement with any other
# machine. KEPT means offset in [0, 5): a NEGATIVE offset is refused too, because
# an ask fired before its instant is not the same ask site Z made.
#
# A MISSED instant is printed BY NAME and excluded from the numerator AND the
# denominator, never silently -- that is the face's own instruction, and it is
# why the expectation is <n> of <n> rather than 3 of 3.
#
# CONTROL: f2_plant/planted_late_ask.txt is a capture in the same format whose
# offset is 12.345 s. It goes through the SAME parser and must come back NOT
# kept; a checker that cannot fail on it is grading nothing.
set -u
cd "$(git rev-parse --show-toplevel)" || exit 3
D=org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~1
PY=${PYTHON:-python}

echo "=== f2_instants_kept.sh -- $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "HEAD=$(git rev-parse HEAD)  BRANCH=$(git rev-parse --abbrev-ref HEAD)"
echo

"$PY" - "$D" <<'PY'
import io
import os
import re
import sys

D = sys.argv[1]
LABELS = ["T0", "T1", "T2"]
INSTANTS = {"T0": "2026-09-09T19:00:00Z",
            "T1": "2026-09-09T20:00:00Z",
            "T2": "2026-09-09T21:00:00Z"}


def read(path):
    if not os.path.exists(path):
        return None
    return io.open(path, encoding="utf-8", errors="replace").read()


def grade(text, label):
    """(state, offset) -- state in ASKED / MISSED / NO-CAPTURE."""
    if text is None:
        return "NO-CAPTURE", None
    if re.search(r"^LAPTOP_STATUS_%s=MISSED" % label, text, re.M):
        return "MISSED", None
    m = re.search(r"^LAPTOP_OFFSET_S_%s=(-?[0-9.]+)" % label, text, re.M)
    if not m:
        return "NO-CAPTURE", None
    return "ASKED", float(m.group(1))


print("--- THE THREE INSTANTS ---")
attempted, kept, missed = 0, 0, []
for lb in LABELS:
    st, off = grade(read(os.path.join(D, "f2_ask_%s.txt" % lb)), lb)
    if st == "ASKED":
        attempted += 1
        ok = (off is not None and 0.0 <= off < 5.0)
        kept += 1 if ok else 0
        print("  %s instant=%s START_OFFSET_S=%.3f KEPT=%s"
              % (lb, INSTANTS[lb], off, str(ok).lower()))
    else:
        missed.append("%s (%s, %s)" % (lb, INSTANTS[lb], st))
        print("  %s instant=%s %s -- excluded from BOTH numerator and denominator"
              % (lb, INSTANTS[lb], st))

print()
print("MISSED_INSTANTS=%s" % ("; ".join(missed) if missed else "NONE"))
print("ATTEMPTED=%d of 3 declared instants" % attempted)
print()

print("--- CONTROL: a planted capture whose ask started 12.345 s late ---")
ctrl_txt = read(os.path.join(D, "f2_plant", "planted_late_ask.txt"))
cst, coff = grade(ctrl_txt, "T0")
cok = (coff is not None and 0.0 <= coff < 5.0)
print("  planted state=%s offset=%s KEPT=%s" % (cst, coff, str(cok).lower()))
print()

print("--- F2-AC1 VERDICT LINES ---")
print("INSTANTS_KEPT=%d of %d within 5s" % (kept, attempted))
if cst == "ASKED" and not cok:
    print("INSTANT_PROBE_CONTROL=FIRED  (the planted 12.345 s late start was READ and scored NOT KEPT, so the numerator above can move)")
else:
    print("INSTANT_PROBE_CONTROL=DEAD  (the planted late start was not caught: state=%s kept=%s)" % (cst, str(cok).lower()))
PY
echo "=== f2_instants_kept.sh END ==="
