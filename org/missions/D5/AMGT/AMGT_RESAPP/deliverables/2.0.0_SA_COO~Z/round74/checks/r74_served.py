"""AMGT_RESAPP round 74 -- the CTO's round-73 analysis @cf0d03deb2, section 4 (PRD v0.40).

  --cell c53|c54|c55|c56 --where local|deployed [--bar N]

c53 (FWD-7, /freshness speed, ruling 3a): after one priming call, 3 timed calls of /api/scoped/amgt/freshness each answer 200 within
    the bar (2,000 ms default), with covered rows 95. Prints min/max ms.
c54 (cold cut, ruling 5; local plane): in a FRESH process, the first `read_monthly_chatter(30)` logs an `AMGT_PHASE route=chatter
    phase=mentions decode ms=<n>` line with n within the bar (500 ms default). Base local 1,132 ms.
c55 (Z-W251-S4, the slash keys, ruling 4): C1 the APPLIED gateway `opal-portal-data-proxy-api` (7k3ed8px20) carries, for each of
    overlay, thesis, peers and print, a GET route that matches a key containing '/' (a greedy `{...+}` path parameter under
    /api/scoped/amgt/security/); C2 on the deployed function, BP/_LN_Equity and NG/_LN_Equity (raw and %2F) answer 200 on all 4
    routes (16 reads).
c56 (FWD-5, Opal Brand form, ruling 2): the PDF of /security/<key>/print?format=pdf for BA, AMD and ASML_NA
    C1 embeds the brand font (a font whose name contains "Lato") and uses it for most of the text (>= 80% of spans);
    C2 one company-description heading at most, one CURRENT market-cap line at most (the per-year fiscal-year-end history is
       not a duplicate), and 0 raw internal markers ("[MACHINE-...");
    C3 the c48 floor holds: 0 unit codes, 0 long decimals, 0 reprs, 0 spans past the page edge.
Verdict: R74 <CELL> SERVED: YES|NO.
"""
from __future__ import annotations

import argparse
import base64
import json
import re
import subprocess
import sys
import time

FN = "opal-amgt-scoped-api"
API_ID = "7k3ed8px20"
PREFIX = "/api/scoped/amgt"
PRINT_NAMES = ("BA_US_Equity", "AMD_US_Equity", "ASML_NA_Equity")
SLASH_KEYS = ("BP/_LN_Equity", "NG/_LN_Equity")
LEAVES = (("overlay", None), ("thesis", None), ("peers", None), ("print", {"format": "rich"}))
UNIT_CODE = re.compile(r"\b(MILLIONS|BILLIONS|THOUSANDS|PERCENT|RATIO|TEXT)\b|\(string field\)|\(dimensionless")
LONG_DECIMAL = re.compile(r"\d+\.\d{5,}")
REPR = re.compile(r"\bNone\b|\bTrue\b|\bFalse\b|\{'|\[\]")
# the CURRENT market-cap line ("Market cap:" / "Market capitalisation:"), never the per-year "... at the fiscal year end:" history
MCAP = re.compile(r"(?im)^\s*market cap(?:italisation|italization)?\s*:")
# a company-description heading in any of its forms ("Company description:", "... (full text):", "COMPANY DESCRIPTION:")
DESC = re.compile(r"(?im)^\s*company description\b")
INTERNAL = re.compile(r"\[MACHINE-[A-Z]+")


def _event(path, query):
    return {"rawPath": path, "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"},
            "queryStringParameters": query}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cell", choices=("c53", "c54", "c55", "c56"), required=True)
    ap.add_argument("--where", choices=("local", "deployed"), required=True)
    ap.add_argument("--bar", type=float, default=0.0)
    a = ap.parse_args()
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")

    if a.cell == "c54":
        bar = a.bar or 500.0
        code = ("import logging, io\nbuf = io.StringIO(); h = logging.StreamHandler(buf)\n"
                "logging.getLogger().addHandler(h); logging.getLogger().setLevel(logging.INFO)\n"
                "from lib.research.api import monthly_chatter\nmonthly_chatter.read_monthly_chatter(30)\nprint(buf.getvalue())\n")
        p = subprocess.run([sys.executable, "-c", code], capture_output=True, timeout=900)
        out = (p.stdout + p.stderr).decode("utf-8", errors="replace")
        m = re.search(r"AMGT_PHASE route=chatter phase=mentions decode ms=(\d+)", out)
        ms = int(m.group(1)) if m else None
        print(f"   fresh-process mentions decode: {ms} ms (bar {bar:.0f})")
        clause("C1 the first chatter request decodes mentions within the bar", ms is not None and ms <= bar, f"{ms}")
    elif a.cell == "c55":
        p = subprocess.run(["aws", "apigatewayv2", "get-routes", "--api-id", API_ID, "--output", "json"],
                           capture_output=True, timeout=120)
        try:
            keys = [r["RouteKey"] for r in json.loads(p.stdout.decode("utf-8", errors="replace")).get("Items", [])]
        except ValueError:
            keys = []
        sec = [k for k in keys if k.startswith(f"GET {PREFIX}/security/")]
        greedy = [k for k in sec if re.search(r"\{[A-Za-z_]+\+\}", k)]
        missing = []
        for leaf, _ in LEAVES:
            if not any(("+}" in k) and (k.endswith("+}") or k.endswith("/" + leaf)) for k in greedy):
                missing.append(leaf)
        print(f"   gateway routes read {len(keys)}; security GET routes {len(sec)}; greedy {greedy[:4]}")
        clause("C1 the applied gateway carries a slash-capable route for overlay/thesis/peers/print", keys and not missing,
               f"missing {missing}")
        import boto3

        lam = boto3.client("lambda", region_name="us-east-1")
        bad = []
        for key in SLASH_KEYS:
            for enc in (key, key.replace("/", "%2F")):
                for leaf, q in LEAVES:
                    r = json.loads(lam.invoke(FunctionName=FN, Payload=json.dumps(
                        _event(f"{PREFIX}/security/{enc}/{leaf}", q)).encode())["Payload"].read())
                    if r.get("statusCode") != 200:
                        bad.append(f"{enc}/{leaf}:{r.get('statusCode')}")
        clause("C2 the function answers 200 for both slash keys on all 4 routes, raw and %2F", not bad, f"failing {bad[:6]}")
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

        if a.cell == "c53":
            bar = a.bar or 2000.0
            raw(f"{PREFIX}/freshness")
            times, codes, covered = [], [], 0
            for _ in range(3):
                t0 = time.time()
                r = raw(f"{PREFIX}/freshness")
                times.append((time.time() - t0) * 1000.0)
                codes.append(r.get("statusCode"))
                try:
                    covered = sum(1 for x in json.loads(r.get("body") or "{}").get("rows") or [] if x.get("covered"))
                except ValueError:
                    covered = 0
            print(f"   /freshness warm: min {min(times):.0f} ms max {max(times):.0f} ms status {sorted(set(codes))} covered rows {covered}")
            clause("C1 /freshness answers warm within the bar", all(c == 200 for c in codes) and max(times) <= bar and covered == 95,
                   f"worst {max(times):.0f} ms bar {bar:.0f}")
        elif a.cell == "c56":
            import pymupdf

            seen, fails = 0, []
            tot = {"unit": 0, "dec": 0, "repr": 0, "clip": 0}
            for key in PRINT_NAMES:
                r = raw(f"{PREFIX}/security/{key}/print", {"format": "pdf"})
                body = r.get("body") or ""
                pdf = base64.b64decode(body) if r.get("isBase64Encoded") else body.encode("latin-1", errors="replace")
                if r.get("statusCode") != 200 or not pdf.startswith(b"%PDF"):
                    fails.append(f"{key}:not a PDF")
                    continue
                seen += 1
                doc = pymupdf.open(stream=pdf, filetype="pdf")
                spans = [sp for pg in doc for b in pg.get_text("dict")["blocks"] for ln in b.get("lines", []) for sp in ln["spans"]]
                lato = sum(1 for sp in spans if "lato" in str(sp.get("font", "")).lower())
                share = lato / len(spans) if spans else 0.0
                text = "\n".join(pg.get_text() for pg in doc)
                desc = len(DESC.findall(text))
                mcap = len(MCAP.findall(text))
                internal = len(INTERNAL.findall(text))
                clip = sum(1 for pg in doc for b in pg.get_text("dict")["blocks"] for ln in b.get("lines", [])
                           for sp in ln["spans"] if sp["bbox"][2] > pg.rect.width - 1)
                n = {"unit": len(UNIT_CODE.findall(text)), "dec": len(LONG_DECIMAL.findall(text)),
                     "repr": len(REPR.findall(text)), "clip": clip}
                for k in tot:
                    tot[k] += n[k]
                print(f"   {key}: pages {len(doc)} lato-share {share:.2f} description-headings x{desc} current-market-cap lines x{mcap} "
                      f"internal-markers x{internal} {n}")
                if share < 0.8:
                    fails.append(f"{key}:lato {share:.2f}")
                if desc > 1 or mcap > 1 or internal:
                    fails.append(f"{key}:dup desc {desc} mcap {mcap} internal {internal}")
            clause("C1 the brand font carries the text", seen == 3 and not [f for f in fails if "lato" in f or "PDF" in f],
                   f"{[f for f in fails if 'lato' in f]}")
            clause("C2 no duplicated description or market-cap line", seen == 3 and not [f for f in fails if "dup" in f],
                   f"{[f for f in fails if 'dup' in f]}")
            clause("C3 the c48 floor holds", seen == 3 and not any(tot.values()), f"{tot}")

    verdict = "YES" if ok and all(ok) else "NO"
    print(f"R74 {a.cell.upper()} SERVED: {verdict}")
    return 0 if verdict == "YES" else 1


if __name__ == "__main__":
    raise SystemExit(main())
