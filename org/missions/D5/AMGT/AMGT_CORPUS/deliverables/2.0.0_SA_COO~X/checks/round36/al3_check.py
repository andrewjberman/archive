"""AMGT_CORPUS round 36, CRPS-al-3 -- the units judgment read is complete in shape. Issuer's file.

Reads deliverables/0.9.0_WK_AMGT_CORPUS~2/R36_UNITS_JUDGMENT_READ.md (path relative to the repo root of the cwd).
Grades SHAPE only; whether each verdict is right is the CVO's judgment at L9.
  b1 the FAMILY table: a row per (family, name) for the 8 families x 3 names = 24 rows, each a markdown table line
     `| <family> | <security_key> | <MNEMONIC> | <served unit> | <served value> | <basis words> | <verdict> |`
     with family in FAMILIES, security_key in NAMES, verdict in RIGHT / WRONG / CANNOT-TELL, and the served block key it
     read named once in the file (`derived/model_block/<key>/<stamp>/model_block.json`) for each of the 3 names.
  b2 the CURRENCY section: a line `CURRENCY TSM_US_Equity figures <n> labelled <k> right <r> wrong <w> cannot-tell <c>` with
     n > 0 and r + w + c == k, and k == n.
Prints one line per arm, then `al3 build <p>/2`.
"""
import os
import re
import subprocess

TOP = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
PATH = os.path.join(TOP, "org", "missions", "D5", "AMGT", "AMGT_CORPUS", "deliverables", "0.9.0_WK_AMGT_CORPUS~2",
                    "R36_UNITS_JUDGMENT_READ.md")
FAMILIES = {"TEXT", "DATE", "YEAR", "PERCENT", "ABSOLUTE_OR_MILLIONS", "SHARE_COUNT_MILLIONS", "PER_SHARE", "RATIO"}
NAMES = {"BA_US_Equity", "TSM_US_Equity", "SAP_GY_Equity"}
VERDICTS = {"RIGHT", "WRONG", "CANNOT-TELL"}

text = open(PATH, encoding="utf-8").read() if os.path.exists(PATH) else ""
cells = set()
for line in text.splitlines():
    parts = [p.strip().strip("`") for p in line.strip().strip("|").split("|")]
    if len(parts) == 7 and parts[0] in FAMILIES and parts[1] in NAMES and parts[6] in VERDICTS and parts[2]:
        cells.add((parts[0], parts[1]))
keys_named = {n for n in NAMES if re.search(r"derived/model_block/%s/\d{8}T\d{6}Z/model_block\.json" % re.escape(n), text)}
b1 = len(cells) == len(FAMILIES) * len(NAMES) and keys_named == NAMES
print("ARM b1 %s family_rows %d/%d block_keys_named %d/3" % ("PASS" if b1 else "FAIL", len(cells),
                                                             len(FAMILIES) * len(NAMES), len(keys_named)))
m = re.search(r"(?m)^CURRENCY TSM_US_Equity figures (\d+) labelled (\d+) right (\d+) wrong (\d+) cannot-tell (\d+)\s*$", text)
b2 = False
if m:
    n, k, r, w, c = (int(x) for x in m.groups())
    b2 = n > 0 and k == n and r + w + c == k
print("ARM b2 %s %s" % ("PASS" if b2 else "FAIL", m.group(0) if m else "no CURRENCY line" if text else "file absent"))
print("al3 build %d/2" % (int(b1) + int(b2)))
