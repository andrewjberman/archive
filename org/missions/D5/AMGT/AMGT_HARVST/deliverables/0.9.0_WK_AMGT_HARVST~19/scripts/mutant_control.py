"""Mutant control for AC2's delta-measurement logic: feed it a FABRICATED before-state with a
nonzero sa count and confirm the SAME comparison code reports a nonzero delta -- proving the +0
this cell measured is a property of the DATA, not a script that always prints +0."""
import json
import sys
import os

sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.path.join(os.getcwd(), ".scratch", "s1"))
from _common import client, silver_listing_hit_counts

with open(os.path.join(".scratch", "s1", "ac0_before.json"), encoding="utf-8") as f:
    real_before = json.load(f)

mutant_before = dict(real_before)
mutant_before["silver_listing_hit_rows"] = dict(real_before["silver_listing_hit_rows"])
mutant_before["silver_listing_hit_rows"]["sa"] = 3  # fabricated: real value is 0
mutant_before["sa_listing_hit_before"] = 3

c = client()
silver_after = silver_listing_hit_counts(c)
sa_after = silver_after.get("sa", 0)
sa_delta_real = sa_after - real_before["sa_listing_hit_before"]
sa_delta_mutant = sa_after - mutant_before["sa_listing_hit_before"]

print("real before=%d after=%d delta=%+d" % (real_before["sa_listing_hit_before"], sa_after, sa_delta_real))
print("mutant before=%d after=%d delta=%+d" % (mutant_before["sa_listing_hit_before"], sa_after, sa_delta_mutant))
if sa_delta_real == 0 and sa_delta_mutant == -3:
    print("MUTANT FIRED AS EXPECTED: the same delta code reports -3 against a fabricated before, "
          "and +0 only against the real, measured before.")
else:
    print("MUTANT DID NOT FIRE AS EXPECTED")
    sys.exit(1)
