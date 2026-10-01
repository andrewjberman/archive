"""AMGT_CORPUS round 26, CRPS-ab-5 -- the header-currency census extended to BP/ LN and NG/ LN (the Z-S69 class on the two names
aa-1 excluded). The population is measured here: the newest block at each ENCODED key whose `currencies.mixed` is true, and on it
every `scope: header` figure labelled with basis 'reporting (EQY_FUND_CRNCY)'. The derive's own `_figure_currency(...,
security=)` must return the currency the worker's class implies. Read-only. The issuer's file.

  -> 'ab5 population P securities S census_covered C classes_valid V reader_matches M unmeasured_labelled U'
"""
import importlib.util
import json
import os
import subprocess

import boto3

TOP = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
RES = os.path.join(TOP, "integrations", "bloomberg", "research")
CENSUS = os.path.join(TOP, "org/missions/D5/AMGT/AMGT_CORPUS/deliverables/0.9.0_WK_AMGT_CORPUS~5/DENOMINATION_CENSUS_ROUND26.json")
KEYS = ("BP-SLASH-_LN_Equity", "NG-SLASH-_LN_Equity")
B = "opal-data-harvest"
CLASSES = {"quote", "reporting", "UNRESOLVED"}

spec = importlib.util.spec_from_file_location("mbp_ab5", os.path.join(RES, "model_block_pull.py"))
mbp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mbp)
s3 = boto3.client("s3")
population = {}
for k in KEYS:
    st = sorted(o["Key"] for o in s3.list_objects_v2(Bucket=B, Prefix="derived/model_block/%s/" % k).get("Contents", [])
                if o["Key"].endswith("/model_block.json"))
    blk = json.loads(s3.get_object(Bucket=B, Key=st[-1])["Body"].read())
    cur = blk.get("currencies") or {}
    if not cur.get("mixed"):
        continue
    for f in blk.get("figures", []):
        if f.get("scope") == "header" and f.get("currency_basis") == "reporting (EQY_FUND_CRNCY)":
            population[(k, f["mnemonic"])] = (blk.get("security"), cur.get("quote"), cur.get("reporting"))
try:
    figs = json.load(open(CENSUS, encoding="utf-8")).get("figures") or []
except (OSError, ValueError):
    figs = []
by = {(r.get("security_key"), r.get("mnemonic")): r for r in figs}
valid = bool(figs) and len(by) == len(figs) and all(
    r.get("class") in CLASSES and str(r.get("measurement") or "").strip() and (r.get("security_key"), r.get("mnemonic")) in population
    for r in figs)
covered = sum(1 for k in population if k in by and by[k].get("class") in CLASSES and str(by[k].get("measurement") or "").strip())
matches = unmeasured = 0
for k, r in by.items():
    if k not in population:
        continue
    sec, q, rep = population[k]
    got = mbp._figure_currency(k[1], q, rep, security=sec)[0]
    want = {"quote": q, "reporting": rep, "UNRESOLVED": None}.get(r.get("class"), "?")
    matches += int(got == want)
    unmeasured += int(r.get("class") == "UNRESOLVED" and got is not None)
print("ab5 population %d securities %d census_covered %d classes_valid %s reader_matches %d unmeasured_labelled %d" % (
    len(population), len({k for k, _ in population}), covered, valid, matches, unmeasured))
