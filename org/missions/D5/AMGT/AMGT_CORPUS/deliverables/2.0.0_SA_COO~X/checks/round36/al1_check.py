"""AMGT_CORPUS round 36, CRPS-al-1 -- the Model slice serves the block's fiscal-scope unresolved entries. Issuer's file.

Reads the live newest blocks of 1299_HK_Equity (non-December FYE: many fiscal unresolved entries) and BA_US_Equity, and calls
the REAL `scoped_amgt.read_model` on each. Prints one line per arm, then `al1 build <p>/1 control <q>/1`.
  b1 build:   read_model(...) carries `fiscal_unresolved`, a list equal (as a multiset of (mnemonic, fiscal_year, reason)) to
              the block's `unresolved` entries whose scope is fiscal_year_line_item -- over both names, with 1299 HK non-empty.
  c1 control: `fiscal_year_figures` is unchanged: its length equals the block's fiscal-scope figure count on both names.
"""
import collections
import subprocess
import sys

TOP = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
sys.path.insert(0, TOP)
from lib.research.api import scoped_amgt  # noqa: E402
from lib.research.checkface.scopes import SCOPE_FISCAL_YEAR_LINE_ITEM  # noqa: E402

KEYS = ("1299_HK_Equity", "BA_US_Equity")
b1_ok, c1_ok = True, True
b1_notes, c1_notes = [], []
for key in KEYS:
    block = scoped_amgt.read_model_block(key)
    model = scoped_amgt.read_model(key, model_block=block)
    want = collections.Counter(
        (u.get("mnemonic"), str(u.get("fiscal_year")), u.get("reason"))
        for u in block.get("unresolved", []) if u.get("scope") == SCOPE_FISCAL_YEAR_LINE_ITEM
    )
    served = model.get("fiscal_unresolved")
    if not isinstance(served, list):
        b1_ok = False
        b1_notes.append("%s fiscal_unresolved absent" % key)
    else:
        got = collections.Counter((u.get("mnemonic"), str(u.get("fiscal_year")), u.get("reason")) for u in served)
        if got != want:
            b1_ok = False
        b1_notes.append("%s served %d block %d" % (key, sum(got.values()), sum(want.values())))
        if key == "1299_HK_Equity" and not want:
            b1_ok = False
            b1_notes.append("1299_HK block has 0 fiscal unresolved -- arm cannot discriminate")
    fiscal_block = sum(1 for f in block.get("figures", []) if f.get("scope") == SCOPE_FISCAL_YEAR_LINE_ITEM)
    fiscal_served = len(model.get("fiscal_year_figures") or [])
    if fiscal_block != fiscal_served:
        c1_ok = False
    c1_notes.append("%s fiscal_year_figures %d block %d" % (key, fiscal_served, fiscal_block))

print("ARM b1 %s %s" % ("PASS" if b1_ok else "FAIL", b1_notes))
print("ARM c1 %s %s" % ("PASS" if c1_ok else "FAIL", c1_notes))
print("al1 build %d/1 control %d/1" % (int(b1_ok), int(c1_ok)))
