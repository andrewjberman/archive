"""READ-ONLY, offline: does a typed ETF reach _compare_stage as a comparable? Measures the tree modules (r34s = tree at af7e16202a1+)."""
import json
import sys
ROOT = "C:/dev/ajb_workspace/infra/aws/lambda/investor-reporting"
sys.path[:0] = [ROOT + "/_scope", ROOT + "/ycharts/research", ROOT + "/ycharts/generate", ROOT + "/lib", "C:/dev/ajb_workspace/lib", ROOT]
import maintained_sources as ms  # noqa: E402

owner = {"firm_id": "F1", "principal_id": "P1", "principal_class": "OPAL_GLOBAL", "advisor_id": None, "home_firm_id": "F1"}
input_ref = {"content_sha256": "0" * 64}
catalogue = {"maintainer": "2.0.0_SA_COO~Y", "candidate_version": ms.COMPARISON_CANDIDATE_VERSION, "entries": []}
table = {"VNQ": {"name": "Vanguard Real Estate ETF"}}
ms.resolve_prospect_owner = lambda headers: owner
out = ms.resolve_comparison_fields({}, input_ref, ["VNQ"], get_catalogue=lambda: catalogue,
                                   authorize_input=lambda o, i: True, read_classifications=lambda: table)
entry = out["comparison_catalog"]["VNQ"]
print("catalog_entry", json.dumps(entry, sort_keys=True))
print("has_key_field", "key" in entry)
# the exact mapping of resident_worker._opal_comparables (line 547)
prepared = {"comparison_keys": ["VNQ"], "comparisons": [entry]}
comps = [{"key": key, "label": c.get("name"), "ticker": c.get("key") if c.get("security_type") == "etf" else None}
         for key, c in zip(prepared["comparison_keys"], prepared["comparisons"])]
print("opal_comparables", json.dumps(comps))
print("ticker_reaches_compare_stage", bool(comps[0]["ticker"]))
