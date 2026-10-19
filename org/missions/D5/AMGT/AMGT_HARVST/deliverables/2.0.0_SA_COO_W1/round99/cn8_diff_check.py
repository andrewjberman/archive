"""HVST-cn-8 diff check (issuer-written, 2026-10-19).

Compares dossier-refresh.tf in the working tree with the pinned base blob and proves two things:
  (1) the default of variable dossier_refresh_schedule_state is "ENABLED";
  (2) every changed line is either a comment line or inside that one variable block.
A planted change to a resource line must be detected first (the negative control).

Usage (repo root of the worktree): python <this file>
Prints DIFF-CONTROL ..., then DIFF-CHECK ...; exit 1 if either fails.
"""
import difflib
import re
import subprocess
import sys

BASE_REF = "8f7d3651c3"
TF = "infra/aws/terraform/harvest/dossier-refresh.tf"
BLOCK_START = re.compile(r'^variable "dossier_refresh_schedule_state" \{')
DEFAULT_RE = re.compile(r'^\s*default\s*=\s*"([A-Z]+)"\s*$')


def block_lines(lines):
    """Indexes of the lines inside the schedule_state variable block (start..closing brace)."""
    inside = set()
    start = None
    for i, ln in enumerate(lines):
        if start is None and BLOCK_START.match(ln):
            start = i
        if start is not None:
            inside.add(i)
            if ln.startswith("}"):
                break
    return inside


def schedule_default(lines):
    inside = sorted(block_lines(lines))
    for i in inside:
        m = DEFAULT_RE.match(lines[i])
        if m:
            return m.group(1)
    return "NONE"


def outside_allowed(base_lines, new_lines):
    """Count changed lines that are neither comments nor inside the schedule_state variable block."""
    base_in = block_lines(base_lines)
    new_in = block_lines(new_lines)
    changed = 0
    bad = 0
    sm = difflib.SequenceMatcher(a=base_lines, b=new_lines, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        for i in range(i1, i2):
            changed += 1
            if not (base_lines[i].strip().startswith("#") or i in base_in):
                bad += 1
        for j in range(j1, j2):
            changed += 1
            if not (new_lines[j].strip().startswith("#") or j in new_in):
                bad += 1
    return changed, bad


def main():
    base = subprocess.run(["git", "show", BASE_REF + ":" + TF], capture_output=True, check=True).stdout.decode("utf-8")
    with open(TF, "rb") as fh:
        new = fh.read().decode("utf-8")
    base_lines = base.splitlines()
    new_lines = new.splitlines()

    # negative control: plant a change to a resource line in memory
    planted = list(new_lines)
    for k, ln in enumerate(planted):
        if ln.startswith("resource "):
            planted[k] = ln + " # planted"
            planted[k + 1] = planted[k + 1] + "x"
            break
    _, planted_bad = outside_allowed(base_lines, planted)
    control = "yes" if planted_bad > 0 else "no"
    print("DIFF-CONTROL planted_resource_change_detected=%s" % control)

    changed, bad = outside_allowed(base_lines, new_lines)
    default = schedule_default(new_lines)
    print("DIFF-CHECK schedule_default=%s changed_lines=%d outside_allowed=%d" % (default, changed, bad))
    if control != "yes" or default != "ENABLED" or bad > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
