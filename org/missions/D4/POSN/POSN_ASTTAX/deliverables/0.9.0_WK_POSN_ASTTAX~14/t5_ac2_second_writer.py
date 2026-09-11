"""T5-AC2/AC7 -- does the SECOND writer of etf-classifications carry any retag-set member?

seed_canonical_securities.py --upload --yang does update_item SET asset_class on the SAME table
the retag writes. AT3-s-4's durability fix covered seed-etf-classifications.py only.
"""
import ast
import subprocess

PIN = "3ce0c0e372"
PATH = "data/black_diamond/scripts/classification/seed_canonical_securities.py"
MEMBERS = ["DBC", "GLD", "GSG", "IAU", "SLV", "USO", "VIXY", "VXX", "UVXY", "QBER", "PDBC"]

src = subprocess.run(["git", "show", "%s:%s" % (PIN, PATH)], capture_output=True).stdout.decode("utf-8", "replace")
tree = ast.parse(src)
canon = None
for node in tree.body:
    if isinstance(node, ast.Assign):
        for t in node.targets:
            if isinstance(t, ast.Name) and t.id == "CANONICAL_SECURITIES":
                canon = ast.literal_eval(node.value)
print("CANONICAL_SECURITIES: %d rows in %s@%s" % (len(canon), PATH, PIN))
by = {r["ticker"]: r for r in canon}
print("\nDENOMINATOR: %d retag-set members checked against %d canonical rows" % (len(MEMBERS), len(canon)))
hit = 0
for m in MEMBERS:
    r = by.get(m)
    if r:
        hit += 1
        print("  IN THE SECOND WRITER: %-6s asset_class=%-12r sub=%r" % (m, r.get("asset_class"), r.get("sub_asset_class")))
    else:
        print("  absent            : %-6s" % m)
print("\n%d of %d retag-set members are written by the SECOND writer." % (hit, len(MEMBERS)))

print("\n== asset_class VOCABULARY this second writer uses (its own enum) ==")
vals = {}
for r in canon:
    vals[r.get("asset_class")] = vals.get(r.get("asset_class"), 0) + 1
for v, n in sorted(vals.items(), key=lambda kv: -kv[1]):
    print("   %-16r %3d" % (v, n))
