"""~113 step 8: where do the k copies of a differing day's rows sit in the landed tree? Counts only."""
import collections
import pickle

OUT = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~113/"
R = pickle.load(open(OUT + "a1_days.pkl", "rb"))
B = pickle.load(open(OUT + "b2_rows.pkl", "rb"))["rows"]
by = collections.defaultdict(list)
for t in B:
    by[(str(t["account_number"]).strip().lstrip("0"), str(t["return_date"])[:10])].append(t)
print("example extra keys (names only):", sorted(B[0]["_extra"].keys()))
C = collections.Counter()
for d in R["days50"]:
    L = [t for t in by[(d["a"].lstrip("0"), d["day"])] if t.get("external_flow") in ("Contribution", "Withdrawal")]
    parts = collections.Counter(t["_part"] for t in L)
    srcs = collections.Counter(str(t["_extra"].get("_source_file")) for t in L)
    ing = collections.Counter(str(t["_extra"].get("_ingested_at")) for t in L)
    asof = collections.Counter(str(t["_extra"].get("as_of_date"))[:10] for t in L)
    C[("rows_match_prior_read", len(L) == len(d["rows"]))] += 1
    C[("n_partitions_holding_the_day", len(parts))] += 1
    C[("n_source_files", len(srcs))] += 1
    C[("n_ingested_at", len(ing))] += 1
    C[("n_as_of", len(asof))] += 1
    k = len(L) // max(1, len({(t["action"], t["market_value"], t["trade_date"], t["settle_date"]) for t in L})) if L else 0
    C[("copies_per_partition_equal", len(set(parts.values())) == 1)] += 1
    C[("partition_date_equals_return_date", all(p == d["day"] for p in parts))] += 1
    C[("partition_after_return_date", all(p > d["day"] for p in parts))] += 1
    C[("partition_before_return_date", all(p < d["day"] for p in parts))] += 1
for k, v in sorted(C.items(), key=str):
    print(k, v)
# distinct-k vs partitions
M = collections.Counter()
for d in R["days50"]:
    L = [t for t in by[(d["a"].lstrip("0"), d["day"])] if t.get("external_flow") in ("Contribution", "Withdrawal")]
    parts = collections.Counter(t["_part"] for t in L)
    cnt = collections.Counter((t["action"], t["market_value"], t["trade_date"], t["settle_date"]) for t in L)
    kk = set(cnt.values())
    M[(tuple(sorted(kk)), len(parts))] += 1
print("(k, n_partitions) pairs:", sorted(M.items()))
