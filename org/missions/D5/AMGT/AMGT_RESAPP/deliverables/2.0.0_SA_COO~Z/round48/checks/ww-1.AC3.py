"""AMGT_RESAPP round 48, AMGT-ww-1 AC3 -- ON THE SERVED PLANE: ww-2's names and ww-4's words are what the DEPLOYED function answers.

Read-only invokes of `opal-amgt-scoped-api`:
 (a) GET /lead-panel/rankings/trending/chatter: every row carries `name`, `classification` and `name_state`; at least one row reads
     name_state SERVED; no row names a company by its ticker;
 (b) GET /security/AMD_US_Equity/thesis: `model.line_names` equals the page's LINE_NAMES (modelSheet.ts, parsed now), and the
     served Base case carries `formula_words` with no ABC_DEF mnemonic token.
usage: python <this>   (from the repo root)"""
import importlib.util
import re
import sys

import boto3

CAPTURE_LIB = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~158/capture_lib.py"
PAGE = "portal/src/pages/SecurityAnalysis/modelSheet.ts"
MNEMONIC = re.compile(r"\b[A-Z][A-Z0-9]*_[A-Z0-9_]+\b")


def page_line_names():
    src = open(PAGE, encoding="utf-8").read()
    body = re.search(r"export const LINE_NAMES[^{]*\{(.*?)\n\}", src, re.S).group(1)
    return dict(re.findall(r"^\s*([A-Z0-9_]+):\s*'([^']*)'", body, re.M))


def main():
    spec = importlib.util.spec_from_file_location("capture_lib", CAPTURE_LIB)
    cl = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cl)
    client = boto3.client("lambda", region_name=cl.REGION)
    print("deployed CodeSha256 %s" % client.get_function_configuration(FunctionName=cl.FUNCTION)["CodeSha256"])
    bad = []
    obj, meta = cl._invoke(client, "%s/lead-panel/rankings/trending/chatter" % cl.ROUTE_PREFIX)
    rows = (obj or {}).get("rows") or []
    served = 0
    for r in rows:
        if not all(k in r for k in ("name", "classification", "name_state")):
            bad.append("(a) row %s lacks name/classification/name_state" % r.get("ticker"))
            continue
        served += r.get("name_state") == "SERVED"
        if r.get("name") and r.get("name") == str(r.get("ticker") or "").split(" ")[0]:
            bad.append("(a) row %s named by its ticker" % r.get("ticker"))
    if not rows or not served:
        bad.append("(a) rankings rows %d, name SERVED %d (%s)" % (len(rows), served, str(meta)[:120]))
    print("(a) rankings rows %d, name SERVED %d" % (len(rows), served))
    obj, meta = cl._invoke(client, "%s/security/AMD_US_Equity/thesis" % cl.ROUTE_PREFIX)
    model = (obj or {}).get("model") or {}
    if model.get("line_names") != page_line_names():
        bad.append("(b) model.line_names %s the page's LINE_NAMES" % ("absent from" if "line_names" not in model else "differs from"))
    base = (model.get("cases") or {}).get("base") or {}
    words = base.get("formula_words")
    if base.get("status") == "SERVED" and (not words or MNEMONIC.search(words)):
        bad.append("(b) base formula_words %r" % words)
    print("(b) line_names %d, base %s, formula_words %r" % (len(model.get("line_names") or {}), base.get("status"), words))
    for b in bad:
        print("  BAD", b)
    ok = not bad
    print("THE DEPLOYED FUNCTION SERVES THE NAMES AND THE WORDS: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
