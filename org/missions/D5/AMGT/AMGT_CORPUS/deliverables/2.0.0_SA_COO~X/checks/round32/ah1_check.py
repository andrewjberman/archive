"""AMGT_CORPUS round 32, CRPS-ah-1 (row Z-S74) -- the provenance validator and print renderer read a unit or sign as
NOT measured when it is empty, the retired pointer "SEE field_map.json ...", an "UNRESOLVED-ON-<security>: ..." text, or a
"ZERO-DOMINATED: ..." text. Offline (no network). The issuer's file.

  BUILD arms (FAIL at the base, PASS after): b1 unit UNRESOLVED-ON-, b2 unit ZERO-DOMINATED, b3 sign UNRESOLVED-ON-,
    b4 render_figure_line prints the unresolved marker for an UNRESOLVED-ON- unit.
  CONTROL arms (PASS at the base and after): c1 PERCENT is MEASURED, c2 the retired pointer is UNRESOLVED, c3 an empty unit is
    UNRESOLVED, c4 a POSITIVE sign is MEASURED, c5 render_figure_line prints a measured unit as itself.
  -> one 'ARM <id> PASS|FAIL <got>' line per arm, then 'ah1 build <p>/4 control <q>/5'
"""
import subprocess
import sys

TOP = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
sys.path.insert(0, TOP)

from lib.research.provenance import validate as v  # noqa: E402
from lib.research.provenance import render_print as rp  # noqa: E402

UNRES = "UNRESOLVED-ON-BBSE3 BZ Equity: no value returned for this mnemonic (absent value)"
ZDOM = "ZERO-DOMINATED: no magnitude: 6 of 10 fiscal years are zero"


def line(unit):
    return rp.render_figure_line({"unit": unit, "mnemonic": "CAPITAL_EXPEND", "value": 0.0, "vintage": "x",
                                  "basis": {"mnemonic": "CAPITAL_EXPEND", "definition": "d"}})


ARMS = [
    ("b1", "build", lambda: v.derive_unit_status({"unit": UNRES}), "UNRESOLVED"),
    ("b2", "build", lambda: v.derive_unit_status({"unit": ZDOM}), "UNRESOLVED"),
    ("b3", "build", lambda: v.derive_sign_status({"sign": UNRES}), "UNRESOLVED"),
    ("b4", "build", lambda: rp.UNRESOLVED_MARKER in line(UNRES) and UNRES not in line(UNRES), True),
    ("c1", "control", lambda: v.derive_unit_status({"unit": "PERCENT"}), "MEASURED"),
    ("c2", "control", lambda: v.derive_unit_status({"unit": "SEE field_map.json: a MEASURED unit is not yet built"}),
     "UNRESOLVED"),
    ("c3", "control", lambda: v.derive_unit_status({"unit": ""}), "UNRESOLVED"),
    ("c4", "control", lambda: v.derive_sign_status({"sign": "POSITIVE"}), "MEASURED"),
    ("c5", "control", lambda: "PERCENT" in line("PERCENT") and rp.UNRESOLVED_MARKER not in line("PERCENT"), True),
]

score = {"build": 0, "control": 0}
for aid, kind, fn, want in ARMS:
    try:
        got = fn()
    except Exception as e:  # an arm that raises is a FAIL with its cause printed
        got = "RAISED %s: %s" % (type(e).__name__, e)
    ok = got == want
    score[kind] += ok
    print("ARM %s %s %r" % (aid, "PASS" if ok else "FAIL", got))
print("ah1 build %d/4 control %d/5" % (score["build"], score["control"]))
