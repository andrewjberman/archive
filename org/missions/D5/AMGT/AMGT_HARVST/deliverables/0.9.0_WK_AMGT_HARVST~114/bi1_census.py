"""HVST-bi-1 census. BEFORE = build() of the base commit's universe_securities (loaded from `git show`);
AFTER = build() as it stands. Read-only (S3 GET), no put, no gold."""
import collections
import importlib.util
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *[".."] * 7))
sys.path.insert(0, REPO)
BASE = "47297a5a82"
REL = "lib/research/harvest/universe_securities.py"
PREFIX = "one name is a prefix of the other; a cut name is not evidence of one issuer"

from lib.research.harvest import universe_securities as after_mod  # noqa: E402


def load_base():
    src = subprocess.run(["git", "-C", REPO, "show", "%s:%s" % (BASE, REL)], capture_output=True, check=True).stdout
    path = os.path.join(REPO, "lib", "research", "harvest", "_us_base_census_tmp.py")  # beside the real module: it resolves paths from __file__
    with open(path, "wb") as fh:
        fh.write(src)
    spec = importlib.util.spec_from_file_location("lib.research.harvest._us_base_census_tmp", path)
    mod = importlib.util.module_from_spec(spec)
    mod.__package__ = "lib.research.harvest"
    try:
        spec.loader.exec_module(mod)
    finally:
        os.remove(path)
    return mod


def verdicts(secs, summ):
    roots = collections.defaultdict(list)
    for s in secs:
        roots[s["security_key"].split("_")[0]].append(s["security_key"])
    multi = {r: sorted(k) for r, k in roots.items() if len(k) > 1}
    limb = {}
    for g in summ["issuer_groups"]:
        for k in g["keys"]:
            limb[k] = (tuple(g["keys"]), g["limb"])
    ng = summ["listings_sharing_a_root_not_grouped"]
    out = {}
    for r, ks in sorted(multi.items()):
        if all(k in limb for k in ks) and len({limb[k][0] for k in ks}) == 1:
            out[r] = ("G", "GROUPED by limb %s" % limb[ks[0]][1])
        else:
            rs = [i.get("reason", "(no reason field)") for i in ng if set(i["keys"]) <= set(ks)]
            out[r] = ("N", "NOT GROUPED: %s" % "; ".join(rs))
    return out


def main():
    base = load_base()
    b_secs, b_sum = base.build()
    a_secs, a_sum = after_mod.build()
    b = {s["security_key"]: s for s in b_secs}
    a = {s["security_key"]: s for s in a_secs}
    S = len(a)
    vb, va = verdicts(b_secs, b_sum), verdicts(a_secs, a_sum)
    print("DENOMINATOR: securities %d, ticker roots with two or more listings %d" % (S, len(va)))
    for r, (_k, text) in va.items():
        print("ROOT %s: %s" % (r, text))
    print("GROUPS: before %d after %d" % (len(b_sum["issuer_groups"]), len(a_sum["issuer_groups"])))
    print("BRAND REFUSALS: before %d after %d" % (len(b_sum["whole_brand_refused"]), len(a_sum["whole_brand_refused"])))
    changed = sorted(k for k in a if b.get(k) != a[k])
    print("SECURITIES WHOSE BUILT DICT CHANGED: %d of %d" % (len(changed), S))
    for k in changed:
        print("  changed: %s\n    before aliases %s\n    after  aliases %s" % (
            k, b.get(k, {}).get("aliases"), a[k]["aliases"]))
    fails = []
    if va.get("TTE", ("", ""))[0] != "G":
        fails.append("TTE not grouped")
    if va.get("ICT", ("", ""))[0] != "N" or PREFIX not in va.get("ICT", ("", ""))[1]:
        fails.append("ICT not NOT GROUPED with the prefix sentence")
    for r, (k, _t) in vb.items():
        if k == "G" and va.get(r, ("",))[0] != "G":
            fails.append("%s was grouped before and is not now" % r)
    if changed:
        fails.append("%d built dicts changed" % len(changed))
    print("CENSUS OK" if not fails else "CENSUS FAIL: " + "; ".join(fails))


if __name__ == "__main__":
    main()
