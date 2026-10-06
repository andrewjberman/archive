"""AMGT_RESAPP round 73 -- the CTO's round-72 analysis @bb75b180ab, section 4 (PRD v0.39).

  --cell c48|c49|c50|c51|c52 --where local|deployed

c48 (FWD-5, the print as a document, ruling 2): the PDF of /security/<key>/print?format=pdf for BA, AMD and ASML_NA carries
    C1 0 unit-code tokens (whole upper-case words MILLIONS, BILLIONS, THOUSANDS, PERCENT, RATIO, TEXT, and the phrases
       "(string field)", "(dimensionless");
    C2 0 figures with more than 4 decimals (\\d+\\.\\d{5,});
    C3 0 Python reprs (None, True, False as words; "{'"; "[]");
    C4 0 text spans whose right edge passes the page edge (pymupdf span bbox x1 > page width - 1).
c49 (FWD-7, the pack clock, ruling 3): over every covered /freshness row, `pack` is a date, never "NEVER".
c50 (Z-W243-S2, plain names): no name served in capitals (5+ letters, all upper case) in the rankings rows
    (/lead-panel/rankings/{trending,breakout}/price `name`), the collected chatter rows (`name` / `display_name`), the overlay
    subject (`name` / `display_name` of BA, AMD, ASML_NA, BP_LN, SAP_GY), and the covered /freshness rows (`name`).
c51 (cold start, ruling 1; local plane): in a FRESH process per route, the first `read_rankings('trending','price')` and the first
    `read_monthly_chatter(30)` read 0 objects under `derived/model_block/` just to name a row (GetObject Key prefix counted).
c52 (Z-W243-S1, keep-prior, ruling 7; local): `build_universe --as-of <today> --dry-run` names all 95 covered keys, and every name
    whose `filing_identity.form_expected` in the prior pool object (rows under `names`) `universe/v1/2026-09-16.json` is not "none" keeps that value (0 regressions).
Verdict: R73 <CELL> SERVED: YES|NO.
"""
from __future__ import annotations

import argparse
import base64
import datetime
import json
import re
import subprocess
import sys

FN = "opal-amgt-scoped-api"
PREFIX = "/api/scoped/amgt"
PRINT_NAMES = ("BA_US_Equity", "AMD_US_Equity", "ASML_NA_Equity")
UNIT_CODE = re.compile(r"\b(MILLIONS|BILLIONS|THOUSANDS|PERCENT|RATIO|TEXT)\b|\(string field\)|\(dimensionless")
LONG_DECIMAL = re.compile(r"\d+\.\d{5,}")
REPR = re.compile(r"\bNone\b|\bTrue\b|\bFalse\b|\{'|\[\]")
CAPS_MIN = 5


def _event(path, query):
    return {"rawPath": path, "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"},
            "queryStringParameters": query}


def _all_caps(name):
    letters = re.sub(r"[^A-Za-z]", "", str(name or ""))
    return len(letters) >= CAPS_MIN and letters.isupper()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cell", choices=("c48", "c49", "c50", "c51", "c52"), required=True)
    ap.add_argument("--where", choices=("local", "deployed"), required=True)
    ap.add_argument("--c51-route", choices=("rankings", "chatter"), default="")
    a = ap.parse_args()
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")

    if a.cell == "c51":
        import botocore.client

        reads = {"n": 0}
        orig = botocore.client.BaseClient._make_api_call

        def counted(self, op, params):
            if op == "GetObject" and str(params.get("Key", "")).startswith("derived/model_block/"):
                reads["n"] += 1
            return orig(self, op, params)

        botocore.client.BaseClient._make_api_call = counted
        from lib.research.api import monthly_chatter, scoped_amgt

        routes = {"rankings": lambda: scoped_amgt.read_rankings("trending", "price"),
                  "chatter": lambda: monthly_chatter.read_monthly_chatter(30)}
        if a.c51_route:
            routes[a.c51_route]()
            print(f"C51READS {reads['n']}")
            return 0
        res = {}
        for label in routes:
            p = subprocess.run([sys.executable, __file__, "--cell", "c51", "--where", a.where, "--c51-route", label],
                               capture_output=True, timeout=900)
            m = re.search(r"C51READS (\d+)", p.stdout.decode("utf-8", errors="replace"))
            res[label] = int(m.group(1)) if m else 10**9
        print(f"   model-block GetObjects on the first request (one fresh process per route): {res}")
        clause("C1 no first request reads a model block to name a row", all(v == 0 for v in res.values()), str(res))
    elif a.cell == "c52":
        import boto3

        from lib.research.coverage import covered_universe

        today = datetime.date.today().isoformat()
        p = subprocess.run([sys.executable, "-m", "lib.research.identity.build_universe", "--as-of", today, "--dry-run"],
                           capture_output=True, timeout=900)
        out = p.stdout.decode("utf-8", errors="replace")
        keys = sorted(covered_universe.covered_security_keys())
        named = [k for k in keys if k in out]
        s3 = boto3.client("s3", region_name="us-east-1")
        prior = json.loads(s3.get_object(Bucket="opal-data-harvest", Key="universe/v1/2026-09-16.json")["Body"].read())
        # the pool object's rows sit under "names"; form_expected sits inside each row's filing_identity
        def _forms(rows):
            return {r.get("security_key"): (r.get("filing_identity") or {}).get("form_expected")
                    for r in rows or [] if isinstance(r, dict)}

        prior_form = _forms(prior.get("names") if isinstance(prior, dict) else prior)
        try:
            new = json.loads(out)
            new_rows = new.get("names") if isinstance(new, dict) else new
        except ValueError:
            new_rows = []
        new_form = _forms(new_rows)
        decided = {k: v for k, v in prior_form.items() if v and v != "none"}
        regress = [f"{k}:{v}->{new_form.get(k)}" for k, v in decided.items() if k in new_form and new_form.get(k) != v]
        print(f"   dry-run rc {p.returncode}; covered named {len(named)} of {len(keys)}; prior decided forms {len(decided)}; "
              f"rows parsed {len(new_rows or [])}")
        clause("C1 the dry-run succeeds and names every covered key", p.returncode == 0 and keys and len(named) == len(keys),
               f"missing {len(keys) - len(named)}")
        clause("C2 no prior decided form_expected regresses", decided and new_rows and not regress,
               f"regressions {len(regress)} e.g. {regress[:4]}")
    else:
        from lib.research.api import scoped_amgt

        if a.where == "deployed":
            import boto3

            lam = boto3.client("lambda", region_name="us-east-1")

            def raw(path, query=None):
                r = lam.invoke(FunctionName=FN, Payload=json.dumps(_event(path, query)).encode())
                return json.loads(r["Payload"].read())
        else:
            def raw(path, query=None):
                return scoped_amgt.handler(_event(path, query))

        def call(path, query=None):
            r = raw(path, query)
            try:
                return r.get("statusCode"), json.loads(r.get("body") or "null")
            except ValueError:
                return r.get("statusCode"), None

        if a.cell == "c48":
            import pymupdf

            tot = {"unit": 0, "dec": 0, "repr": 0, "clip": 0}
            seen = 0
            for key in PRINT_NAMES:
                r = raw(f"{PREFIX}/security/{key}/print", {"format": "pdf"})
                body = r.get("body") or ""
                pdf = base64.b64decode(body) if r.get("isBase64Encoded") else body.encode("latin-1", errors="replace")
                if r.get("statusCode") != 200 or not pdf.startswith(b"%PDF"):
                    print(f"   {key}: status {r.get('statusCode')} not a PDF")
                    continue
                seen += 1
                doc = pymupdf.open(stream=pdf, filetype="pdf")
                text = "\n".join(pg.get_text() for pg in doc)
                clip = sum(1 for pg in doc for b in pg.get_text("dict")["blocks"] for ln in b.get("lines", [])
                           for sp in ln["spans"] if sp["bbox"][2] > pg.rect.width - 1)
                n = {"unit": len(UNIT_CODE.findall(text)), "dec": len(LONG_DECIMAL.findall(text)),
                     "repr": len(REPR.findall(text)), "clip": clip}
                for k in tot:
                    tot[k] += n[k]
                print(f"   {key}: pages {len(doc)} unit-codes {n['unit']} long-decimals {n['dec']} reprs {n['repr']} "
                      f"clipped-spans {n['clip']}")
            clause("C1 0 unit-code tokens", seen == 3 and tot["unit"] == 0, f"{tot['unit']}")
            clause("C2 0 figures past 4 decimals", seen == 3 and tot["dec"] == 0, f"{tot['dec']}")
            clause("C3 0 Python reprs", seen == 3 and tot["repr"] == 0, f"{tot['repr']}")
            clause("C4 0 spans past the page edge", seen == 3 and tot["clip"] == 0, f"{tot['clip']}")
        elif a.cell == "c49":
            st, fr = call(f"{PREFIX}/freshness")
            rows = [r for r in (fr or {}).get("rows") or [] if isinstance(r, dict) and r.get("covered")]
            never = [r.get("security_key") for r in rows if str(r.get("pack") or "NEVER").upper() == "NEVER"]
            print(f"   population: covered rows {len(rows)} status {st}")
            clause("C1 every covered row's pack clock is a date", st == 200 and rows and not never,
                   f"NEVER {len(never)} e.g. {never[:5]}")
        elif a.cell == "c50":
            bad, seen = [], 0
            for mv in ("trending", "breakout"):
                st, b = call(f"{PREFIX}/lead-panel/rankings/{mv}/price")
                for r in (b or {}).get("rows") or []:
                    seen += 1
                    if _all_caps(r.get("name")):
                        bad.append(f"rank/{mv}:{r.get('name')}")
            st, b = call(f"{PREFIX}/lead-panel/timeseries/collected/chatter", {"days": "30"})
            for r in (b or {}).get("rows") or (b or {}).get("securities") or []:
                if isinstance(r, dict):
                    seen += 1
                    nm = r.get("display_name") or r.get("name")
                    if _all_caps(nm):
                        bad.append(f"chatter:{nm}")
            for key in ("BA_US_Equity", "AMD_US_Equity", "ASML_NA_Equity", "BP_LN_Equity", "SAP_GY_Equity"):
                st, ov = call(f"{PREFIX}/security/{key}/overlay")
                subj = (ov or {}).get("subject") or {}
                nm = subj.get("display_name") or subj.get("name") or (ov or {}).get("display_name") or (ov or {}).get("name")
                seen += 1
                if _all_caps(nm):
                    bad.append(f"overlay/{key}:{nm}")
            st, fr = call(f"{PREFIX}/freshness")
            for r in (fr or {}).get("rows") or []:
                if isinstance(r, dict) and r.get("covered"):
                    seen += 1
                    if _all_caps(r.get("name")):
                        bad.append(f"freshness:{r.get('name')}")
            print(f"   population: names read {seen}")
            clause("C1 no served name is all capitals", seen and not bad, f"failing {len(bad)} e.g. {bad[:6]}")

    verdict = "YES" if ok and all(ok) else "NO"
    print(f"R73 {a.cell.upper()} SERVED: {verdict}")
    return 0 if verdict == "YES" else 1


if __name__ == "__main__":
    raise SystemExit(main())
