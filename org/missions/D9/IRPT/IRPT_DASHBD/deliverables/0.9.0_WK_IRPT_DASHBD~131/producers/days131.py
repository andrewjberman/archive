"""~131: build the (account, day) list of the 234 flow-bearing days from the ~108 private pickles, as ~127 did (members list of 51)."""
import os
import pickle
ROOT = os.environ["IRPT_PRIV_ROOT"].rstrip("/")
P = ROOT + "/0.9.0_WK_IRPT_DASHBD~108/"
OUT = os.environ["IRPT_RERUN_DIR"].rstrip("/") + "/"
mem = pickle.load(open(P + "members90.pkl", "rb"))
D = pickle.load(open(P + "read90.pkl", "rb"))
rows = pickle.load(open(P + "table90.pkl", "rb"))
M51 = set(mem["FLOW_TIMING_CONVENTION_DOLLARS_TIE"])
days = {}
nseg = 0
for r in rows:
    if r["idx"] not in M51:
        continue
    nseg += 1
    a, seg = r["a"], r["seg"]
    g = D["gold"][a]
    for d in g:
        if seg["start"] <= d <= seg["end"] and g[d]["r"] is not None and g[d]["flow"]:
            days.setdefault((a, d), []).append((seg["end"], g[d]["flow"]))
out = [{"a": a, "d": d, "end": v[0][0], "flow": v[0][1], "nseg": len(v)} for (a, d), v in sorted(days.items())]
pickle.dump(out, open(OUT + "days234.pkl", "wb"))
print("segments", nseg, "days", len(out), "accounts", len({x["a"] for x in out}), "days in >1 segment", sum(1 for x in out if x["nseg"] > 1))
print("flow sign counts pos/neg:", sum(1 for x in out if x["flow"] > 0), sum(1 for x in out if x["flow"] < 0))
print("min day, max day, max end (years only):", min(x["d"] for x in out)[:4], max(x["d"] for x in out)[:4], max(x["end"] for x in out)[:4])
