"""IB-pr-498 structural diff of the two packaged HoldingsSnapshot schema copies (offline; prints only).

Usage: python -I schema_delta_498.py <built_zip> <live_zip>
Flattens each document to JSON-pointer leaves and prints the counts, then one line per leaf that is only built,
only live, or differing. Reads zip bytes only.
"""
import json
import sys
import zipfile


def load(p):
    return json.loads(zipfile.ZipFile(p).read("contracts/HoldingsSnapshot.schema.json").decode("utf-8"))


def flat(x, p="", out=None):
    if out is None:
        out = {}
    if isinstance(x, dict):
        for k, v in x.items():
            flat(v, p + "/" + k, out)
    elif isinstance(x, list):
        for i, v in enumerate(x):
            flat(v, p + "[%d]" % i, out)
    else:
        out[p] = x
    return out


B, L = load(sys.argv[1]), load(sys.argv[2])
fb, fl = flat(B), flat(L)
only_b = sorted(set(fb) - set(fl))
only_l = sorted(set(fl) - set(fb))
diff = sorted(k for k in set(fb) & set(fl) if fb[k] != fl[k])
print("leaves built=%d live=%d only_built=%d only_live=%d differing=%d" % (len(fb), len(fl), len(only_b), len(only_l), len(diff)))
for k in only_b:
    print("ONLY_BUILT " + k)
for k in only_l:
    print("ONLY_LIVE " + k)
for k in diff:
    print("DIFF " + k)
