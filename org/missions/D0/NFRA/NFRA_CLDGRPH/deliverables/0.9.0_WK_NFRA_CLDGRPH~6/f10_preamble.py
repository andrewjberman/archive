"""F10-AC1 -- THE PREAMBLE, THEN EXACTLY THE OLD BEHAVIOUR.

Three READ-ONLY subcommands through the WRAPPER (`classes`, `dual-managed`, `metrics --graph
<fixture>`). derive / snapshot / iceberg-commit are NEVER run: the shared plane is not touched.

WHAT IS MEASURED, AND WHY EACH LINE CAN FAIL:
  PREAMBLE_FIRST   the preamble is the FIRST thing on stderr (first non-empty line matches), so it
                   is read before whatever the subcommand says.
  PREAMBLE_NAMES   the seven things the notice must name, each by a literal probe.
  STDOUT_UNCHANGED byte-identical stdout vs f10_baseline.json, captured BEFORE the edit. This is
                   the control that must be able to fail -- and it did: a first run of the baseline
                   through a python-spawned bare `bash` hit the System32 WSL stub and recorded three
                   IDENTICAL 504-byte hashes. Distinct hashes per subcommand are printed below so a
                   reader can see the baseline discriminates.
  RC_UNCHANGED     rc equal to the pre-change rc.
  WRAPPER_PREAMBLE_COUNT  the wrapper+CLI pair prints it ONCE. The wrapper prints and exports
                   COMP_AWS_PREAMBLE_PRINTED=1; the CLI honours it. Counted on the wrapper run, with
                   a NEGATIVE CONTROL beside it (the CLI called directly prints it once itself, so
                   the 1 is not a constant produced by a silent CLI).
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import f10_lib as L  # noqa: E402

BASE = json.load(open(L.BASELINE, encoding="utf-8"))

# the SEVEN things the preamble must name -> (label, literal probe)
NAMES = [
    ("served-graph", "SERVED"),
    ("comp-kuzu", "comp-kuzu"),
    ("cloud.read.served_vintage", "cloud.read.served_vintage"),
    ("nightly-derive-runner", "nightly Fargate derive-runner"),
    ("incremental-updater", "incremental updater"),
    ("comp-which", "comp-which"),
    ("andrew-2026-09-09", "2026-09-09"),
]

print("F10-AC1 -- preamble first, then exactly the old behaviour")
print("baseline: %s" % L.BASELINE)
print("")

first_ok = 0
stdout_ok = 0
rc_ok = 0
names_found = []
rows = []

for argv in L.SUBCOMMANDS:
    key = " ".join(argv[:2])
    b = BASE["subcommands"][key]
    rc, out, err = L.run_wrapper(argv)
    lines = [ln for ln in err.splitlines() if ln.strip()]
    first = lines[0] if lines else ""
    is_first = first.startswith("comp-aws: DEPRECATED FOR AGENT USE")
    same_out = (L.sha256_of(out) == b["stdout_sha256"])
    same_rc = (rc == b["rc"])
    first_ok += 1 if is_first else 0
    stdout_ok += 1 if same_out else 0
    rc_ok += 1 if same_rc else 0
    if not names_found:
        names_found = [lab for lab, probe in NAMES if probe in err]
    rows.append((key, is_first, same_out, same_rc, rc, b["rc"],
                 L.sha256_of(out)[:16], b["stdout_sha256"][:16], first[:72]))

print("  %-26s first?  stdout==base?  rc==base?   rc  base_rc  sha16(now)      sha16(base)"
      % "subcommand")
for key, isf, so, sr, rc, brc, sn, sb, first in rows:
    print("  comp-aws %-17s %-7s %-14s %-11s %-3d %-8d %-15s %-15s"
          % (key, "YES" if isf else "NO", "YES" if so else "NO", "YES" if sr else "NO",
             rc, brc, sn, sb))
print("")
for key, isf, so, sr, rc, brc, sn, sb, first in rows:
    print("    first stderr line [%s]: %s" % (key, first))
print("")

print("PREAMBLE_FIRST=%d of %d subcommands" % (first_ok, len(L.SUBCOMMANDS)))
print("PREAMBLE_NAMES=%s" % ",".join(lab for lab, _ in NAMES if lab in names_found))
print("  (%d of %d named; missing: %s)"
      % (len(names_found), len(NAMES),
         [lab for lab, _ in NAMES if lab not in names_found] or "none"))
print("STDOUT_UNCHANGED=%d of %d" % (stdout_ok, len(L.SUBCOMMANDS)))
print("RC_UNCHANGED=%d of %d" % (rc_ok, len(L.SUBCOMMANDS)))

# ---- ONE PRINT PER INVOCATION ------------------------------------------------------------------
rc_w, out_w, err_w = L.run_wrapper(["classes"])
n_wrapper = err_w.count("comp-aws: DEPRECATED FOR AGENT USE")
rc_c, out_c, err_c = L.run_cli(["classes"])
n_cli = err_c.count("comp-aws: DEPRECATED FOR AGENT USE")
print("WRAPPER_PREAMBLE_COUNT=%d" % n_wrapper)
print("  NEGATIVE CONTROL -- the CLI invoked DIRECTLY (no wrapper, no COMP_AWS_PREAMBLE_PRINTED)")
print("  prints it itself: DIRECT_CLI_PREAMBLE_COUNT=%d. So the 1 above is the wrapper's print"
      % n_cli)
print("  being HONOURED by the CLI, not a CLI that never prints.")

# ---- the baseline's own discrimination ---------------------------------------------------------
shas = {k: v["stdout_sha256"] for k, v in BASE["subcommands"].items()}
print("BASELINE_DISCRIMINATES=%s (%d distinct stdout sha256 across %d subcommands)"
      % ("YES" if len(set(shas.values())) == len(shas) else "NO",
         len(set(shas.values())), len(shas)))

ok = (first_ok == len(L.SUBCOMMANDS) and stdout_ok == len(L.SUBCOMMANDS)
      and rc_ok == len(L.SUBCOMMANDS) and len(names_found) == len(NAMES) and n_wrapper == 1)
print("RC=%d" % (0 if ok else 1))
sys.exit(0 if ok else 1)
