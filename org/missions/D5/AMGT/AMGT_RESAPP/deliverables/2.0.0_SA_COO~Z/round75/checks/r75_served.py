"""AMGT_RESAPP round 75 -- the CTO's round-74 analysis @0967e3d9c5, section 4 (PRD v0.40).

  --cell c57|c58|c59|c60|c61 --where local|deployed [--bar N] [--burst N]

c57 (FWD-5, ruling 1): for the PDF prints of BA, AMD and ASML_NA, C1 no line under a "Fiscal year YYYY" heading is stamped with the
    run date (today, UTC); C2 the run date appears exactly ONCE in each print, on page 1 (the header).
c58 (FWD-5, ruling 2): C1 the BA print carries every sentence /security/BA_US_Equity/thesis serves in `drafted_sections` (17 at the
    cut), compared with whitespace and line-break hyphens removed; C2 on all 3 prints, no "No <section> has been written" line for a
    section whose served sentences are non-empty.
c59 (FWD-7, ruling 3): local -- C1 `lib.research.freshness.snapshot.build_freshness_snapshot()` returns rows EQUAL to
    `scoped_amgt.read_coverage_freshness()` rows (every row, every field). deployed -- C1 the snapshot object the route reads exists
    and its rows EQUAL a locally computed view; C2 a burst of --burst concurrent /freshness invokes (default 40, wide enough to
    exceed the warm pool; row Z-S361, issuer ruling 2026-10-06): every COLD one (a REPORT with Init Duration) answers 200 within the
    bar (init + duration, default 2,000 ms). An EMPTY cold list is UNMEASURED, never a FAIL: the verdict then reads
    `R75 C59 SERVED: UNMEASURED` with exit 2 (a slow or failed cold invoke stays NO, exit 1); C3 one invoke
    after 65 s idle (the in-process hold expired) answers 200 within the bar.
c60 (ruling 5): in a FRESH process, `read_monthly_chatter(30)` logs `AMGT_PHASE route=chatter phase=names ms=<n>` with n within the
    bar (default 300 ms).
c61 (ruling 6): over every covered name's /thesis, C1 no segment_breakdown row is headed by a filing section ("ITEM ..."), a figure
    (a digit or '$'), and BA's headings are one segment name each: at most 3 distinct, each in {Commercial Airplanes; Defense, Space &
    Security; Global Services}; C2 every driver-chart point whose passage_text is a table run (half or more of its tokens numeric)
    serves `passage_table` with non-empty `columns` and `rows`, each row a non-empty `label`.
Verdict: R75 <CELL> SERVED: YES|NO (exit 0|1); c59 deployed may also read UNMEASURED (exit 2).
"""
from __future__ import annotations

import argparse
import base64
import concurrent.futures
import datetime
import json
import re
import subprocess
import sys
import time

FN = "opal-amgt-scoped-api"
PREFIX = "/api/scoped/amgt"
PRINT_NAMES = ("BA_US_Equity", "AMD_US_Equity", "ASML_NA_Equity")
BA_SEGMENTS = {"Commercial Airplanes", "Defense, Space & Security", "Global Services"}
FY_HEADING = re.compile(r"^\s*Fiscal year (\d{4})\s*$")
PLACEHOLDER = re.compile(r"(?i)^\s*No ([a-z ,&]+?) (?:has|have) been written")
NUMERIC = re.compile(r"^[\$\(\)\-,.%\d*]+$")


def _event(path, query=None):
    return {"rawPath": path, "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"},
            "queryStringParameters": query}


def _norm(text):
    return re.sub(r"\s+", "", re.sub(r"-\n", "", str(text or ""))).lower()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cell", choices=("c57", "c58", "c59", "c60", "c61"), required=True)
    ap.add_argument("--where", choices=("local", "deployed"), required=True)
    ap.add_argument("--bar", type=float, default=0.0)
    ap.add_argument("--burst", type=int, default=40)
    a = ap.parse_args()
    ok = []
    unmeasured = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")

    if a.cell == "c60":
        bar = a.bar or 300.0
        code = ("import logging, io\nbuf = io.StringIO(); h = logging.StreamHandler(buf)\n"
                "logging.getLogger().addHandler(h); logging.getLogger().setLevel(logging.INFO)\n"
                "from lib.research.api import monthly_chatter\nmonthly_chatter.read_monthly_chatter(30)\nprint(buf.getvalue())\n")
        p = subprocess.run([sys.executable, "-c", code], capture_output=True, timeout=900)
        out = (p.stdout + p.stderr).decode("utf-8", errors="replace")
        m = re.search(r"AMGT_PHASE route=chatter phase=names ms=(\d+)", out)
        ms = int(m.group(1)) if m else None
        print(f"   fresh-process names phase: {ms} ms (bar {bar:.0f})")
        clause("C1 the first chatter request resolves names within the bar", ms is not None and ms <= bar, f"{ms}")
        return _verdict(a, ok)

    from lib.research.api import scoped_amgt

    if a.where == "deployed":
        import boto3

        from botocore.config import Config

        lam = boto3.client("lambda", region_name="us-east-1",
                           config=Config(max_pool_connections=max(10, a.burst + 4), read_timeout=120))

        def invoke(path, query=None, tail=False):
            r = lam.invoke(FunctionName=FN, Payload=json.dumps(_event(path, query)).encode(),
                           **({"LogType": "Tail"} if tail else {}))
            body = json.loads(r["Payload"].read())
            return (body, base64.b64decode(r["LogResult"]).decode("utf-8", "replace")) if tail else body

        def raw(path, query=None):
            return invoke(path, query)
    else:
        def raw(path, query=None):
            return scoped_amgt.handler(_event(path, query))

    def body(path, query=None):
        r = raw(path, query)
        try:
            return r.get("statusCode"), json.loads(r.get("body") or "{}")
        except ValueError:
            return r.get("statusCode"), {}

    if a.cell in ("c57", "c58"):
        import pymupdf

        run_date = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
        texts, first_pages = {}, {}
        for key in PRINT_NAMES:
            r = raw(f"{PREFIX}/security/{key}/print", {"format": "pdf"})
            b = r.get("body") or ""
            pdf = base64.b64decode(b) if r.get("isBase64Encoded") else b.encode("latin-1", errors="replace")
            if r.get("statusCode") != 200 or not pdf.startswith(b"%PDF"):
                texts[key] = None
                continue
            doc = pymupdf.open(stream=pdf, filetype="pdf")
            texts[key] = "\n".join(pg.get_text() for pg in doc)
            first_pages[key] = doc[0].get_text()
        if a.cell == "c57":
            fy_bad, once_bad = {}, {}
            for key, text in texts.items():
                if text is None:
                    fy_bad[key] = once_bad[key] = "not a PDF"
                    continue
                in_fy, n = False, 0
                for line in text.split("\n"):
                    if FY_HEADING.match(line):
                        in_fy = True
                        continue
                    if in_fy and re.match(r"^\s*[A-Z][A-Za-z ]+$", line) and "as of" not in line and len(line.split()) <= 4 \
                            and not line.strip().endswith(("-", ":")):
                        in_fy = False
                    if in_fy and run_date in line:
                        n += 1
                fy_bad[key] = n
                total = text.count(run_date)
                once_bad[key] = (total, run_date in first_pages.get(key, ""))
                print(f"   {key}: fiscal-year lines stamped {run_date}: {n}; run date occurrences {total}; on page 1 "
                      f"{run_date in first_pages.get(key, '')}")
            clause("C1 no fiscal-year figure is stamped with the run date", all(v == 0 for v in fy_bad.values()), f"{fy_bad}")
            clause("C2 the run date appears once, on page 1", all(isinstance(v, tuple) and v == (1, True) for v in once_bad.values()),
                   f"{once_bad}")
        else:
            missing_total, served_total = 0, 0
            placeholder_bad = []
            for key, text in texts.items():
                code, th = body(f"{PREFIX}/security/{key}/thesis")
                sections = th.get("drafted_sections") or []
                nt = _norm(text)
                if text is None:
                    placeholder_bad.append(f"{key}:not a PDF")
                    continue
                if key == "BA_US_Equity":
                    sents = [s.get("text") for sec in sections for s in (sec.get("sentences") or []) if s.get("text")]
                    served_total = len(sents)
                    missing = [s for s in sents if _norm(s) not in nt]
                    missing_total = len(missing)
                    print(f"   BA: served sentences {served_total}; in the print {served_total - missing_total}; "
                          f"e.g. missing {[m[:60] for m in missing[:2]]}")
                served_labels = {str(sec.get("label") or "").lower() for sec in sections if sec.get("sentences")}
                for line in text.split("\n"):
                    m = PLACEHOLDER.match(line)
                    if m:
                        word = m.group(1).lower()
                        if any(word.split()[0] in lab or lab.split()[0] in word for lab in served_labels if lab):
                            placeholder_bad.append(f"{key}:{line.strip()[:60]}")
            clause("C1 the BA print carries every served thesis sentence", served_total and missing_total == 0,
                   f"{served_total - missing_total} of {served_total}")
            clause("C2 no 'not written' line for a section the route serves", not placeholder_bad, f"{placeholder_bad[:4]}")
    elif a.cell == "c59":
        bar = a.bar or 2000.0
        computed = scoped_amgt.read_coverage_freshness()
        crow = {r.get("security_key") or r.get("name"): r for r in computed.get("rows") or []}

        def equal(rows):
            served = {r.get("security_key") or r.get("name"): r for r in rows or []}
            diff = [k for k in crow if served.get(k) != crow[k]] + [k for k in served if k not in crow]
            return len(crow) - len([k for k in diff if k in crow]), len(crow), diff[:4]

        if a.where == "local":
            try:
                from lib.research.freshness import snapshot

                built = snapshot.build_freshness_snapshot()
            except Exception as err:  # noqa: BLE001 -- the base has no builder
                print(f"   builder: {type(err).__name__}: {err}")
                built = None
            same, n, diff = equal((built or {}).get("rows")) if built else (0, len(crow), ["no snapshot builder"])
            print(f"   snapshot rows EQUAL {same} of {n}; e.g. differing {diff}")
            clause("C1 the snapshot builder's rows equal the computed view", built and same == n and n > 0, f"{same} of {n}")
        else:
            code, served = body(f"{PREFIX}/freshness")
            src = served.get("snapshot") or {}
            # ISSUER AMENDMENT (row Z-S359, AE~A STOP 30010): `rot` is rendered from the list register, which the Lambda
            # package carries and a local tree does not, so a local baseline cannot judge it. Rows are compared on every
            # OTHER field against the local view; `rot` is compared within ONE environment, against the deployed /lists.
            for r in list(crow.values()):
                r.pop("rot", None)
            rows_wo = [{k: v for k, v in (r or {}).items() if k != "rot"} for r in served.get("rows") or []]
            same, n, diff = equal(rows_wo)
            print(f"   served from snapshot: {bool(src)} {json.dumps(src)[:160]}; rows EQUAL (all fields but rot) {same} of {n}; "
                  f"e.g. {diff}")
            from lib.research.freshness.build_view import render_rot_signal

            lcode, lists = body(f"{PREFIX}/lists")
            want_rot = render_rot_signal({"lists": lists.get("lists")} if lists.get("lists") else None)
            rots = {json.dumps(r.get("rot")) for r in served.get("rows") or []}
            print(f"   rot: served {sorted(rots)[:1]}; rendered from the deployed /lists {json.dumps(want_rot)[:120]}")
            clause("C1 the route serves the snapshot; rows equal the computed view, rot equal to the deployed register's",
                   bool(src) and same == n and n > 0 and rots == {json.dumps(want_rot)}, f"{same} of {n}")
            with concurrent.futures.ThreadPoolExecutor(a.burst) as ex:
                res = list(ex.map(lambda _: invoke(f"{PREFIX}/freshness", tail=True), range(a.burst)))
            cold = []
            for (b, log) in res:
                rep = next((ln for ln in log.split("\n") if ln.startswith("REPORT")), "")
                init = re.search(r"Init Duration: ([\d.]+) ms", rep)
                dur = re.search(r"\tDuration: ([\d.]+) ms", rep)
                if init and dur:
                    cold.append((b.get("statusCode"), float(init.group(1)) + float(dur.group(1))))
            print(f"   burst of {a.burst}: cold invokes {len(cold)} {sorted((c, round(t)) for c, t in cold)}")
            if cold:
                clause("C2 every cold invoke answers within the bar", all(c == 200 and t <= bar for c, t in cold),
                       f"bar {bar:.0f}; {len(cold)} cold of {a.burst}")
            else:
                unmeasured.append("C2")
                print(f"UNMEASURED C2 no cold invoke was observed in a burst of {a.burst}; widen --burst (this is not a FAIL)")
            time.sleep(65)
            t0 = time.time()
            b, log = invoke(f"{PREFIX}/freshness", tail=True)
            ms = (time.time() - t0) * 1000.0
            rep = next((ln for ln in log.split("\n") if ln.startswith("REPORT")), "")
            print(f"   after 65 s idle: {ms:.0f} ms end to end, status {b.get('statusCode')}; {rep[:120]}")
            clause("C3 a read after the hold expires answers within the bar", b.get("statusCode") == 200 and ms <= bar,
                   f"{ms:.0f} ms")
    elif a.cell == "c61":
        from lib.research.coverage.covered_universe import covered_security_keys

        keys = sorted(covered_security_keys())
        bad_heads, ba_heads, table_bad, tables = [], set(), [], 0
        for key in keys:
            code, th = body(f"{PREFIX}/security/{key}/thesis")
            for row in ((th.get("segment_breakdown") or {}).get("rows") or []):
                head = str(row.get("segment") or "")
                if re.match(r"(?i)^\s*item\s+\d", head) or re.search(r"[\d$]", head):
                    bad_heads.append(f"{key}:{head[:40]}")
                if key == "BA_US_Equity":
                    ba_heads.add(head)
            for p in ((th.get("thesis_driver_chart") or {}).get("points") or []):
                toks = str(p.get("passage_text") or "").split()
                if toks and sum(1 for t in toks if NUMERIC.match(t)) / len(toks) >= 0.5:
                    tables += 1
                    pt = p.get("passage_table") or {}
                    rows = pt.get("rows") or []
                    if not (pt.get("columns") and rows and all(isinstance(r, dict) and str(r.get("label") or "").strip()
                                                                for r in rows)):
                        table_bad.append(f"{key}/{p.get('passage_id')}")
        ba_ok = 0 < len(ba_heads) <= 3 and ba_heads <= BA_SEGMENTS
        print(f"   names {len(keys)}; bad segment headings {len(bad_heads)} e.g. {bad_heads[:3]}; BA headings {sorted(ba_heads)}")
        print(f"   table passages {tables}; without labels {len(table_bad)} e.g. {table_bad[:3]}")
        clause("C1 every segment row is headed by one segment name", not bad_heads and ba_ok,
               f"bad {len(bad_heads)}; BA {len(ba_heads)} headings")
        clause("C2 every table passage serves its row and column labels", not table_bad, f"{len(table_bad)} of {tables}")
    return _verdict(a, ok, unmeasured)


def _verdict(a, ok, unmeasured=()):
    verdict = "YES" if ok and all(ok) else "NO"
    if verdict == "YES" and unmeasured:
        print(f"R75 {a.cell.upper()} SERVED: UNMEASURED ({', '.join(unmeasured)} observed nothing to grade)")
        return 2
    print(f"R75 {a.cell.upper()} SERVED: {verdict}")
    return 0 if verdict == "YES" else 1


if __name__ == "__main__":
    raise SystemExit(main())
