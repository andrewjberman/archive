"""HVST-p-2 AC3: base (b635dadc66) vs after pass sets, from the two recorded pytest -rA outputs.

Run: python org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~67/scripts/p2_ac3_compare.py
"""

from pathlib import Path
import re

OUT = Path(__file__).resolve().parent.parent


def outcomes(name):
    text = (OUT / name).read_text(encoding="utf-8", errors="replace")
    text = re.sub(r"\x1b\[[0-9;]*m", "", text)
    return {kind: set(re.findall(r"^%s (\S+)" % kind, text, re.M)) for kind in ("PASSED", "FAILED", "ERROR", "SKIPPED")}


base, after = outcomes("p2_base_pytest.txt"), outcomes("p2_ac3_after_pytest.txt")
print("base (b635dadc66): passed=%d failed=%d error=%d" % (len(base["PASSED"]), len(base["FAILED"]), len(base["ERROR"])))
print("after            : passed=%d failed=%d error=%d" % (len(after["PASSED"]), len(after["FAILED"]), len(after["ERROR"])))
lost = sorted(base["PASSED"] - after["PASSED"])
added = sorted(after["PASSED"] - base["PASSED"])
print("passed at base and not passing after: %d of %d %s" % (len(lost), len(base["PASSED"]), lost))
print("newly passing after: %d, all in test_p2_fetched_and_stored_keys.py: %s" % (
    len(added), all("test_p2_fetched_and_stored_keys.py" in name for name in added)))
assert not lost and not after["FAILED"] and not after["ERROR"]
