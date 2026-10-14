"""Member comparison of two Lambda zips by member sha256 (IB-pr-525, worker 0.9.0_WK_IRPT_BCKEND~372).

Usage: python -I ib188_cmp_members.py <built.zip> <live.zip>
Reads the zip bytes only; no network, no AWS call. Prints the member counts, the members only in one zip, and the
members whose bytes differ, each with both sha256 values.
"""
import hashlib
import sys
import zipfile

BUILT = sys.argv[1]
LIVE = sys.argv[2]


def members(path):
    out = {}
    with zipfile.ZipFile(path) as z:
        for info in z.infolist():
            if info.is_dir():
                continue
            out[info.filename] = hashlib.sha256(z.read(info.filename)).hexdigest()
    return out


built = members(BUILT)
live = members(LIVE)
only_built = sorted(set(built) - set(live))
only_live = sorted(set(live) - set(built))
diff = sorted(k for k in set(built) & set(live) if built[k] != live[k])
equal = sorted(k for k in set(built) & set(live) if built[k] == live[k])
print("built_members", len(built), "live_members", len(live))
print("only_in_built", only_built)
print("only_in_live", only_live)
print("differing", diff)
print("equal_count", len(equal))
for k in diff:
    print("DIFF", k, "built=", built[k], "live=", live[k])
