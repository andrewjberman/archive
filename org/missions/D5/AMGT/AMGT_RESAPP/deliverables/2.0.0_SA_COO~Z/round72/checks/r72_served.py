"""AMGT_RESAPP round 72 -- the CTO's round-71 analysis @be50c0d724, section 4 (PRD v0.39).

  --cell c39|c41|c42|c43|c44|c45|c46|c47 --where local|deployed

c39 (DSGN FWD-4, blockless names): over every /freshness row with covered=false and a key (138 at the cut), /security/<key>/overlay
    answers 200 and its `header_figures` carries >= 7 entries, each with a value or a non-empty plain `reason`.
c41 (FWD-5, the print in plain words): the PDF of /security/<key>/print?format=pdf for BA, AMD, ASML_NA carries 0 raw field-code
    tokens (UPPER_UNDERSCORE words, e.g. CUR_MKT_CAP) in its text layer. Denominator: pages and tokens per name print.
c42 (FWD-18, driver-chart passages): every point of /security/<key>/thesis `thesis_driver_chart.points` that carries a `passage_id`
    also serves a non-empty `passage_text`, for BA and ASML_NA (6 points at the cut).
c43 (FWD-1, segments): every covered name's /thesis serves `segment_breakdown` with non-empty `rows` (each row a `segment`, `text`
    and `cite`), or empty rows and a non-empty plain `reason`. C2: at least 12 names serve rows.
c44 (DSGN FWD-8, numeric member tickers): every /security/<key>/peers member whose `ticker` is all digits carries a non-empty
    `security_key`, or a non-empty plain `ticker_reason`. Over the 95 covered names.
c45 (DSGN FWD-27, plain names): every /peers `subject` and member serves `display_name`, and none of them is all capitals (a name
    with 5+ letters, all upper case). Over the 95 covered names.
c46 (cold start, local plane only): each in its OWN fresh process, the first `read_rankings('trending','price')` and the first
    `monthly_chatter.read_monthly_chatter(30)` each make <= 15 AWS API calls (botocore `_make_api_call` counted).
c47 (the pool universe): `python -m lib.research.identity.build_universe --as-of <today> --dry-run` exits 0, and its stdout names
    every covered security key (95 of 95).
Verdict: R72 <CELL> SERVED: YES|NO.
"""
from __future__ import annotations

import argparse
import base64
import datetime
import importlib.util
import io
import json
import re
import subprocess
import sys

ROOT = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables"
CAPTURE_LIB = ROOT + "/0.9.0_WK_AMGT_RESAPP~158/capture_lib.py"
PREFIX = "/api/scoped/amgt"
FN = "opal-amgt-scoped-api"
PRINT_NAMES = ("BA_US_Equity", "AMD_US_Equity", "ASML_NA_Equity")
CODE_TOKEN = re.compile(r"\b[A-Z][A-Z0-9]*_[A-Z0-9_]*[A-Z0-9]\b")


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _event(path, query):
    return {"rawPath": path, "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"},
            "queryStringParameters": query}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cell", choices=("c39", "c41", "c42", "c43", "c44", "c45", "c46", "c47"), required=True)
    ap.add_argument("--where", choices=("local", "deployed"), required=True)
    ap.add_argument("--c46-route", choices=("rankings", "chatter"), default="")
    a = ap.parse_args()
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")

    if a.cell == "c46":
        import botocore.client

        calls = {"n": 0}
        orig = botocore.client.BaseClient._make_api_call

        def counted(self, op, params):
            calls["n"] += 1
            return orig(self, op, params)

        botocore.client.BaseClient._make_api_call = counted
        from lib.research.api import monthly_chatter, scoped_amgt

        routes = {"rankings": lambda: scoped_amgt.read_rankings("trending", "price"),
                  "chatter": lambda: monthly_chatter.read_monthly_chatter(30)}
        if a.c46_route:
            routes[a.c46_route]()
            print(f"C46CALLS {calls['n']}")
            return 0
        res = {}
        for label in routes:
            # each route in its OWN fresh process, so one route's reads never warm the other's
            p = subprocess.run([sys.executable, __file__, "--cell", "c46", "--where", a.where, "--c46-route", label],
                               capture_output=True, timeout=900)
            m = re.search(r"C46CALLS (\d+)", p.stdout.decode("utf-8", errors="replace"))
            res[label] = int(m.group(1)) if m else 10**9
        print(f"   first-request AWS calls (one fresh process per route): {res}")
        clause("C1 each first read makes <= 15 AWS calls", all(v <= 15 for v in res.values()), str(res))
    elif a.cell == "c47":
        today = datetime.date.today().isoformat()
        p = subprocess.run([sys.executable, "-m", "lib.research.identity.build_universe", "--as-of", today, "--dry-run"],
                           capture_output=True, timeout=900)
        out = p.stdout.decode("utf-8", errors="replace")
        from lib.research.coverage import covered_universe

        keys = sorted(covered_universe.covered_security_keys())
        named = [k for k in keys if k in out]
        err = p.stderr.decode("utf-8", errors="replace").strip().splitlines()[-1:] if p.returncode else []
        print(f"   build_universe --dry-run rc {p.returncode}; covered named {len(named)} of {len(keys)} {err}")
        clause("C1 the union universe dry-run succeeds and names every covered key",
               p.returncode == 0 and keys and len(named) == len(keys), f"missing {len(keys) - len(named)}")
    else:
        from lib.research.api import scoped_amgt

        if a.where == "deployed":
            import boto3

            cl = _load("capture_lib", CAPTURE_LIB)
            lam = boto3.client("lambda", region_name=cl.REGION)

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

        non200 = []
        if a.cell == "c39":
            st, fr = call(f"{PREFIX}/freshness")
            keys = sorted({r.get("security_key") for r in (fr or {}).get("rows") or []
                           if isinstance(r, dict) and r.get("covered") is False and r.get("security_key")})
            bad = []
            for key in keys:
                st, ov = call(f"{PREFIX}/security/{key}/overlay")
                if st != 200:
                    bad.append(f"{key}:{st}")
                    continue
                figs = (ov or {}).get("header_figures") or []
                good = [f for f in figs if isinstance(f, dict)
                        and (f.get("value") is not None or str(f.get("reason") or "").strip())]
                if len(good) < 7:
                    bad.append(f"{key}:{len(good)}")
            print(f"   population: uncovered names with a key {len(keys)}")
            clause("C1 every uncovered name's overlay serves 7 figures, each a value or a plain reason", keys and not bad,
                   f"failing {len(bad)} e.g. {bad[:5]}")
        elif a.cell == "c41":
            import pypdf

            total, detail = 0, []
            for key in PRINT_NAMES:
                r = raw(f"{PREFIX}/security/{key}/print", {"format": "pdf"})
                body = r.get("body") or ""
                pdf = base64.b64decode(body) if r.get("isBase64Encoded") else body.encode("latin-1", errors="replace")
                if r.get("statusCode") != 200 or not pdf.startswith(b"%PDF"):
                    non200.append(f"{key}:{r.get('statusCode')}")
                    continue
                reader = pypdf.PdfReader(io.BytesIO(pdf))
                text = "\n".join((pg.extract_text() or "") for pg in reader.pages)
                toks = CODE_TOKEN.findall(text)
                total += len(toks)
                detail.append(f"{key}: pages {len(reader.pages)} tokens {len(toks)} distinct {len(set(toks))} e.g. {sorted(set(toks))[:3]}")
            for d in detail:
                print(f"   {d}")
            clause("C1 the three prints carry 0 raw field-code tokens", len(detail) == 3 and total == 0 and not non200,
                   f"tokens {total} non-200 {non200}")
        elif a.cell == "c42":
            pts_n, bad = 0, []
            for key in ("BA_US_Equity", "ASML_NA_Equity"):
                st, th = call(f"{PREFIX}/security/{key}/thesis")
                if st != 200:
                    non200.append(f"{key}:{st}")
                    continue
                for p in (((th or {}).get("thesis_driver_chart") or {}).get("points") or []):
                    if p.get("passage_id"):
                        pts_n += 1
                        if not str(p.get("passage_text") or "").strip():
                            bad.append(f"{key}/{p.get('passage_id')}")
            print(f"   population: points with a passage_id {pts_n}")
            clause("C1 every driver-chart point with a passage_id serves its passage_text", pts_n and not bad and not non200,
                   f"failing {len(bad)} e.g. {bad[:6]} non-200 {non200}")
        else:
            from lib.research.coverage import covered_universe

            keys = sorted(covered_universe.covered_security_keys())
            if a.cell == "c43":
                bad, with_rows = [], 0
                for key in keys:
                    st, th = call(f"{PREFIX}/security/{key}/thesis")
                    if st != 200:
                        non200.append(f"{key}:{st}")
                        continue
                    sb = (th or {}).get("segment_breakdown")
                    rows = (sb or {}).get("rows") if isinstance(sb, dict) else None
                    if rows and all(isinstance(r, dict) and r.get("segment") and r.get("text") and r.get("cite") for r in rows):
                        with_rows += 1
                    elif not (isinstance(sb, dict) and not rows and str(sb.get("reason") or "").strip()):
                        bad.append(key)
                print(f"   population: names {len(keys)} with segment rows {with_rows} non-200 {len(non200)}")
                clause("C1 every name serves segment rows or a plain reason", keys and not bad and not non200,
                       f"failing {len(bad)} e.g. {bad[:5]}")
                clause("C2 at least 12 names serve segment rows", with_rows >= 12, f"with rows {with_rows}")
            elif a.cell in ("c44", "c45"):
                bad, seen = [], 0
                for key in keys:
                    st, pe = call(f"{PREFIX}/security/{key}/peers")
                    if st != 200:
                        non200.append(f"{key}:{st}")
                        continue
                    subject = (pe or {}).get("subject") or {}
                    members = (pe or {}).get("members") or []
                    if a.cell == "c44":
                        for m in members:
                            if str(m.get("ticker") or "").strip().isdigit():
                                seen += 1
                                if not (str(m.get("security_key") or "").strip() or str(m.get("ticker_reason") or "").strip()):
                                    bad.append(f"{key}/{m.get('ticker')}")
                    else:
                        for who, obj in [("subject", subject)] + [("member", m) for m in members]:
                            if not obj:
                                continue
                            seen += 1
                            dn = str(obj.get("display_name") or "").strip()
                            letters = re.sub(r"[^A-Za-z]", "", dn)
                            if not dn or (len(letters) >= 5 and letters.isupper()):
                                bad.append(f"{key}/{who}:{dn or '<none>'}")
                print(f"   population: names {len(keys)} objects read {seen} non-200 {len(non200)}")
                name = ("C1 every numeric-ticker member resolves or carries a plain ticker_reason" if a.cell == "c44"
                        else "C1 every peers subject and member serves a display_name that is not all capitals")
                clause(name, keys and seen and not bad and not non200, f"failing {len(bad)} e.g. {bad[:5]}")

    verdict = "YES" if ok and all(ok) else "NO"
    print(f"R72 {a.cell.upper()} SERVED: {verdict}")
    return 0 if verdict == "YES" else 1


if __name__ == "__main__":
    raise SystemExit(main())
