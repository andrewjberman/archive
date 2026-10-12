"""~117 step 1: reproduce ~108's naive 59/31 from its table90.pkl (class90.py line 90 test). Counts only."""
import pickle
P = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~108/"
rows = pickle.load(open(P + "table90.pkl", "rb"))


def tie(p, q):
    return abs(p - q) <= max(1.0, 0.001 * max(abs(p), abs(q)))


t = sum(1 for r in rows if tie(r["t"]["flow"], r["b"]["nadd"]))
print("segments", len(rows), "naive tie", t, "do_not_tie", len(rows) - t)
