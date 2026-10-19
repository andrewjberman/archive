# HVST-cn-5 buildspec check. Run from the repo root of the worktree:  python -I <this file> > cn5_buildspec.out
#
# CodeBuild reads every phases.*.commands item as a string (YAML_FILE_ERROR otherwise). This program:
# 1. NEGATIVE CONTROL: plants one unquoted `- echo "A: b"` command item in memory and proves the check counts it.
# 2. Loads infra/aws/harvest/dossier-refresh/buildspec.yml with yaml.safe_load and counts every item of every
#    phases.*.commands list, and how many of those items are not str.
# Prints its transcript to stdout only (the caller redirects it). Exit 0 only when the control fires AND k == 0.

import os
import sys

try:
    import yaml
except ImportError:
    sys.exit("ERROR: PyYAML is not importable in this interpreter")

ROOT = os.getcwd()
BUILDSPEC = os.path.join(ROOT, "infra", "aws", "harvest", "dossier-refresh", "buildspec.yml")

if not os.path.isfile(BUILDSPEC):
    sys.exit("ERROR: run from the repo root of the worktree (buildspec not found in the cwd)")

PLANT = 'phases:\n  build:\n    commands:\n      - echo "A: b"\n'


def count_commands(doc):
    """Return (n_items, bad) over every phases.*.commands list in a loaded buildspec.
    bad is a list of (where, type_name) for each item that is not a str, or for each phase lacking a list."""
    n_items = 0
    bad = []
    phases = doc.get("phases") if isinstance(doc, dict) else None
    if not isinstance(phases, dict):
        return 0, [("phases", "not-a-mapping")]
    for phase_name in sorted(phases):
        phase = phases[phase_name]
        commands = phase.get("commands") if isinstance(phase, dict) else None
        if not isinstance(commands, list):
            bad.append(("phases.%s.commands" % phase_name, "not-a-list"))
            continue
        for idx, item in enumerate(commands):
            n_items += 1
            if not isinstance(item, str):
                bad.append(("phases.%s.commands[%d]" % (phase_name, idx), type(item).__name__))
    return n_items, bad


_, planted_bad = count_commands(yaml.safe_load(PLANT))
detected = "yes" if len(planted_bad) == 1 else "no"
print("BUILDSPEC-CONTROL planted_nonstring_detected=%s" % detected)

with open(BUILDSPEC, "r", encoding="utf-8") as fh:
    real_doc = yaml.safe_load(fh.read())
n_cmds, real_bad = count_commands(real_doc)
for where, type_name in real_bad:
    print("BUILDSPEC-NONSTRING %s type=%s" % (where, type_name))
print("BUILDSPEC-CHECK commands=%d non_string=%d" % (n_cmds, len(real_bad)))

if detected != "yes" or real_bad:
    sys.exit(1)
