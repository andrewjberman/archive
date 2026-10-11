"""~111 step 1: reproduce the 51 flow-class members from ~108's pickles; peek at txn row shape. Prints counts only."""
import collections
import pickle

P = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~108/"
mem = pickle.load(open(P + "members90.pkl", "rb"))
print({k: len(v) for k, v in mem.items()})
D = pickle.load(open(P + "read90.pkl", "rb"))
print("reads", D["reads"])
print("txn rows", len(D["txn"]))
print("txn cols", sorted(D["txn"][0].keys()))
c = collections.Counter((t.get("external_flow"), t.get("action"), t.get("transaction_type")) for t in D["txn"])
for k, v in c.most_common(25):
    print(k, v)
print("gold day keys sample type", type(next(iter(next(iter(D["gold"].values()))))))
print("ratio of txn with settle != trade:", sum(1 for t in D["txn"] if t.get("settle_date") != t.get("trade_date")), "of", len(D["txn"]))
print("return_date vs trade_date differ:", sum(1 for t in D["txn"] if str(t.get("return_date"))[:10] != str(t.get("trade_date"))[:10]))
print("sample dtype", repr(D["txn"][0].get("return_date")), repr(D["txn"][0].get("trade_date")), repr(D["txn"][0].get("settle_date")))
