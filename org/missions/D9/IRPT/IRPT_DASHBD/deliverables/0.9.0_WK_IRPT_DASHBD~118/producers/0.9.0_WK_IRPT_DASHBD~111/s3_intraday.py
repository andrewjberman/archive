"""~111 step 3: does the custodian's daily value series + flow amount show intraday timing? Counts/medians only (private pickles, no AWS).
Entry day test (d-1 / d / d+1) and implied-day-return plausibility under START/MID/END against the account's own non-flow daily moves.
"""
import collections
import math
import pickle
import statistics

P = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~108/"
OUT = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~111/"
mem = pickle.load(open(P + "members90.pkl", "rb"))
D = pickle.load(open(P + "read90.pkl", "rb"))
rows = pickle.load(open(P + "table90.pkl", "rb"))
M51 = set(mem["FLOW_TIMING_CONVENTION_DOLLARS_TIE"])


def imp(conv, v0, v1, F):
    if conv == "START":
        return v1 / (v0 + F) - 1.0
    if conv == "MID":
        return (v1 - F / 2.0) / (v0 + F / 2.0) - 1.0
    return (v1 - F) / v0 - 1.0


C = collections.Counter()
pooled = {c: [] for c in ("START", "MID", "END")}
pooled_big = {c: [] for c in ("START", "MID", "END")}
segres = {}
for r in rows:
    if r["idx"] not in M51:
        continue
    a, seg = r["a"], r["seg"]
    g = D["gold"][a]
    ds = sorted(g)
    prev = [d for d in ds if d < seg["start"]]
    ser = [(d, g[d]["mv"], g[d]["flow"] or 0.0) for d in ds if (not prev or d >= prev[-1]) and d <= seg["end"] and g[d]["mv"] is not None]
    noise = [abs(ser[i][1] - ser[i - 1][1]) / ser[i - 1][1] for i in range(1, len(ser)) if ser[i][2] == 0.0 and ser[i - 1][1] and ser[i - 1][2] == 0.0]
    nz = statistics.median(noise) if len(noise) >= 5 else None
    ent = collections.Counter()
    nbig = 0
    for i in range(1, len(ser)):
        d, v1, F = ser[i]
        if F == 0.0 or not ser[i - 1][1] or nz is None or nz <= 0:
            continue
        v0 = ser[i - 1][1]
        rel = abs(F) / v0
        if rel < 5 * nz or rel < 0.01:
            ent["not_readable"] += 1
            continue
        dm1 = (v0 - ser[i - 2][1]) if i >= 2 else None
        dd = v1 - v0
        dn = (ser[i + 1][1] - v1) if i + 1 < len(ser) else None
        h = abs(F) / 2.0
        cand = []
        if dm1 is not None and abs(dm1 - F) <= h:
            cand.append("d-1")
        if abs(dd - F) <= h:
            cand.append("d")
        if dn is not None and abs(dn - F) <= h:
            cand.append("d+1")
        if dn is None:
            ent["no_next_day"] += 1 if cand == ["d"] else 0
        ent[",".join(cand) if cand else "none"] += 1
        # implied returns plausibility (only where day d-1 and d are clean and v0 > 0)
        if v0 > 0 and v0 + F > 0:
            for c in pooled:
                x = abs(imp(c, v0, v1, F)) / nz
                pooled[c].append(math.log(max(x, 1e-3)))
                if rel >= 0.5:
                    pooled_big[c].append(math.log(max(x, 1e-3)))
            if rel >= 0.5:
                nbig += 1
    segres[r["idx"]] = (dict(ent), nbig, nz is not None)
    for k, v in ent.items():
        C[("entry", k)] += v
for k, v in sorted(C.items(), key=lambda z: str(z[0])):
    print(k, v)
for name, pp in (("rel>=5noise&1%", pooled), ("rel>=0.5", pooled_big)):
    print(name, "n_flow_days", len(pp["START"]), {c: round(statistics.median(pp[c]), 2) if pp[c] else None for c in pp})
S = collections.Counter()
for idx, (ent, nbig, has) in segres.items():
    det = [k for k in ent if k not in ("not_readable", "no_next_day")]
    S[("seg_has_noise_scale", has)] += 1
    S[("seg_entry_set", tuple(sorted(det)))] += 1
    S[("seg_has_big_flow(rel>=0.5)", nbig > 0)] += 1
for k, v in sorted(S.items(), key=lambda z: str(z[0])):
    print(k, v)
