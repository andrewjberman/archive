"""AMGT_CORPUS round 25, CRPS-aa-1 -- the per-field denomination census of the header money figures on the mixed-currency names,
checked against a population this checker measures itself, and the derive's label rule read through the producer's own function.
Read-only on S3. The issuer's file.

The population: the newest served model block of every key EXCEPT the slash-bearing keys (EXCLUDED, Z-S64) whose `currencies.mixed`
is true, and on it every `scope: header` figure labelled with basis 'reporting (EQY_FUND_CRNCY)'.

  -> 'aa1 population P securities S census_covered C classes_valid V reader_matches M tsm_mkt_cap X control_reporting Y
      unmeasured_labelled U callers N unwired W'
"""
import ast
import importlib.util
import json
import os
import subprocess

import boto3

TOP = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
RES = os.path.join(TOP, "integrations", "bloomberg", "research")
CENSUS = os.path.join(TOP, "org/missions/D5/AMGT/AMGT_CORPUS/deliverables/0.9.0_WK_AMGT_CORPUS~1/DENOMINATION_CENSUS_ROUND25.json")
# AMENDMENT 1 (row Z-W1-S21): RESAPP round-53 ac-3 copies the slash keys to their encoded form; an identity is EXCLUDED in
# either form (raw `BP/_LN_Equity` or encoded `BP-SLASH-_LN_Equity`).
EXCLUDED = {"BP/_LN_Equity", "NG/_LN_Equity", "BP-SLASH-_LN_Equity", "NG-SLASH-_LN_Equity"}
B = "opal-data-harvest"
CLASSES = {"quote", "reporting", "UNRESOLVED"}

spec = importlib.util.spec_from_file_location("mbp_aa1", os.path.join(RES, "model_block_pull.py"))
mbp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mbp)


def reader(mnemonic, quote, reporting, security):
    try:
        return mbp._figure_currency(mnemonic, quote, reporting, security=security)[0]
    except TypeError:
        return mbp._figure_currency(mnemonic, quote, reporting)[0]


s3 = boto3.client("s3")
latest = {}
for pg in s3.get_paginator("list_objects_v2").paginate(Bucket=B, Prefix="derived/model_block/"):
    for o in pg.get("Contents", []):
        rest = o["Key"][len("derived/model_block/"):]
        if rest.endswith("/model_block.json"):
            key = rest.rsplit("/", 2)[0]
            if key not in EXCLUDED and (key not in latest or o["Key"] > latest[key]):
                latest[key] = o["Key"]
population = {}
for key in sorted(latest):
    blk = json.loads(s3.get_object(Bucket=B, Key=latest[key])["Body"].read())
    cur = blk.get("currencies") or {}
    if not cur.get("mixed"):
        continue
    for f in blk.get("figures", []):
        if f.get("scope") == "header" and f.get("currency_basis") == "reporting (EQY_FUND_CRNCY)":
            population[(key, f["mnemonic"])] = (blk.get("security"), cur.get("quote"), cur.get("reporting"))

try:
    census = json.load(open(CENSUS, encoding="utf-8"))
except (OSError, ValueError):
    census = {"figures": []}
figs = census.get("figures") or []
by_key = {(r.get("security_key"), r.get("mnemonic")): r for r in figs}
valid = bool(figs) and all(
    r.get("class") in CLASSES and str(r.get("measurement") or "").strip() and (r.get("security_key"), r.get("mnemonic")) in population
    for r in figs) and len(by_key) == len(figs)
covered = sum(1 for k in population if k in by_key and by_key[k].get("class") in CLASSES and str(by_key[k].get("measurement") or "").strip())
matches = unmeasured_labelled = 0
for k, r in by_key.items():
    if k not in population:
        continue
    security, quote, reporting = population[k]
    got = reader(k[1], quote, reporting, security)
    want = {"quote": quote, "reporting": reporting, "UNRESOLVED": None}.get(r.get("class"), "?")
    matches += int(got == want)
    unmeasured_labelled += int(r.get("class") == "UNRESOLVED" and got is not None)
# AMENDMENT 1 (row Z-W1-S22): the rule reaches the served block only if the derive's own call sites pass the security. Every
# call of `_figure_currency` in model_block_pull.py is read by AST; a call without a `security` keyword is UNWIRED.
tree = ast.parse(open(os.path.join(RES, "model_block_pull.py"), encoding="utf-8").read())
calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call)
         and getattr(n.func, "id", getattr(n.func, "attr", None)) == "_figure_currency"]
unwired = sum(1 for n in calls if not any(k.arg == "security" for k in n.keywords))
tsm = reader("CUR_MKT_CAP", "USD", "TWD", "TSM US Equity")
control = reader("SALES_REV_TURN", "USD", "TWD", "TSM US Equity")
print("aa1 population %d securities %d census_covered %d classes_valid %s reader_matches %d tsm_mkt_cap %s control_reporting %s "
      "unmeasured_labelled %d callers %d unwired %d" % (len(population), len({k for k, _ in population}), covered, valid, matches, tsm, control,
                                  unmeasured_labelled, len(calls), unwired))
