import json
import sys
from pathlib import Path
root = Path(sys.argv[1])
old = json.loads((root / ".scratch/old_contract.json").read_bytes().decode("utf-8"))
new_raw = (root / "org/standards/IRPT_DASHBD_PERFORMANCE_REPORT_CONTRACT.json").read_bytes()
new = json.loads(new_raw.decode("utf-8"))
print("new keys:", list(new.keys()))
print("top-level differing keys:", sorted(k for k in set(old) | set(new) if old.get(k) != new.get(k)))
print("lineage:", json.dumps(new["lineage"], ensure_ascii=False)[:300])
ob = {m["id"]: m for m in old["members"]}
nb = {m["id"]: m for m in new["members"]}
print("member ids equal and in order:", [m["id"] for m in old["members"]] == [m["id"] for m in new["members"]], len(nb))
diff = [i for i in ob if ob[i] != nb[i]]
print("members differing:", len(diff))
bad = [i for i in diff if set(ob[i]) != set(nb[i]) or any(ob[i][k] != nb[i][k] for k in ob[i] if k != "source")]
print("differing members with any non-source change:", bad)
same_src_fields = all(ob[i]["source"]["contract"] == nb[i]["source"]["contract"] for i in diff)
print("all differing members now source from return table:", all(nb[i]["source"]["contract"].endswith("ACCOUNT_RETURN_DAILY_CONTRACT.json") for i in diff))
print("ABSENT members unchanged:", sum(1 for m in new["members"] if m["source"] == "ABSENT"), sum(1 for m in old["members"] if m["source"] == "ABSENT"))
print("pvs return_cumulative still ABSENT:", all(nb["pvs.%s.return_cumulative" % w]["source"] == "ABSENT" for w in ("qtd","ytd","last_12_months","since_inception")))
print("act unchanged:", all(ob[i] == nb[i] for i in ob if i.startswith("act.")))
print("sections/document unchanged:", old["sections"] == new["sections"], old["document"] == new["document"])
print("rest of top-level unchanged:", all(old[k] == new[k] for k in old if k not in ("contract_version", "members")))
print("members diff by section counts:", {s: sum(1 for i in diff if ob[i]["section"] == s) for s in sorted(set(ob[i]["section"] for i in diff))})
print("folds unique:", len(set(nb[i]["source"]["fold"] for i in diff)), "of", len(diff))
print("fold lengths min/max:", min(len(nb[i]["source"]["fold"]) for i in diff), max(len(nb[i]["source"]["fold"]) for i in diff))
print("sample old source:", json.dumps(ob["avs.qtd.net_gain"]["source"])[:200])
print("sample new source:", json.dumps(nb["avs.qtd.net_gain"]["source"])[:200])
print("ascii-only new file:", all(ord(ch) < 128 for ch in new_raw.decode("utf-8")))
print("vendor/custodian name hits in new text:", [w for w in ("black diamond","orion","schwab","commonwealth","bloomberg","ycharts","fidelity","custodian") if w in new_raw.decode("utf-8").lower()])
