"""tools_compare.py <live.json> <cut.json>: compare two tool censuses by name, with a negative control."""

import json
import sys

a = json.load(open(sys.argv[1]))
b = json.load(open(sys.argv[2]))
la, lb = set(a["all"]), set(b["all"])
print("live: native %d integration %d total %d" % (a["native"], a["integration"], a["total"]))
print("cut : native %d integration %d total %d" % (b["native"], b["integration"], b["total"]))
print("added", sorted(lb - la), "removed", sorted(la - lb), "-- NAMES EQUAL", la == lb)
dropped = sorted(lb)[0]
print("NEGATIVE CONTROL (drop one cut name %r): EQUAL reads %s" % (dropped, (lb - {dropped}) == la))
