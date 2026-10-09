"""Condition 8: per name, in-process fetch.build_source_object on the cached filing (no network, no write); prints status, language, item_keys.
usage: py -3.12 cond8.py <KEY>"""
import importlib.util
import os
import subprocess
import sys
root = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
sys.path.insert(0, root)
spec = importlib.util.spec_from_file_location("r84l", os.path.join(root, "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~R1/round84_prep/checks/r84_language.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
F = m._imports(root)
key = sys.argv[1]
text = open(os.path.join(root, ".scratch", "r82_20f", key + ".txt"), encoding="utf-8").read()
located = {"resolved": True, "accession": "0000000000-26-000000", "accession_raw": "000000000026000000", "form": "20-F",
           "filing_date": "2026-01-01", "url": "offline://%s" % key, "primary_document": "%s.htm" % key, "entity_name": key}
saved = (F.latest_filing, F.http_get, F.html_to_text, F.time.sleep)
F.latest_filing = lambda cik, form_expected, timeout=90: dict(located)
F.http_get = lambda url, timeout=90, retries=2: text.encode("utf-8")
F.html_to_text = lambda raw: text
F.time.sleep = lambda s: None
try:
    obj = F.build_source_object(key, 1, "20-F")
finally:
    F.latest_filing, F.http_get, F.html_to_text, F.time.sleep = saved
ex = obj.get("excerpt") or {}
keys = ex.get("item_keys") or []
ok = obj.get("status") == "RESOLVED" and obj.get("language") == "en" and all(k in keys for k in ("business", "risk", "mdna"))
print("COND8 %s status=%s language=%s parser=%s item_keys=%s -> %s" % (key, obj.get("status"), obj.get("language"), obj.get("parser_version"), keys, "OK" if ok else "SKIP"))
