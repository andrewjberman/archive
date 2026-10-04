"""AMGT_RESAPP round 67 -- the CTO's round-66 analysis @d76db3486c, section 4 (rulings 1, 2, 4, 5, 6).

  --cell c23|c24|c25|c26 --where local|deployed

c23 (FWD-39 list repair, rulings 1-2), over EVERY served timeline payload: each name of the collected/chatter universe, on BOTH the
    route's default range (the store floor to the latest day, the population 3.0.0_SA_CVO~Z read in ADJUDICATION_v79) and
    2026-09-01..today:
    C1  0 clouds carry their own ticker root or a word of the served short name (display_name); long-name words are the plant test's;
    C2  0 clouds carry a word on the extended list (the CTO's measured boilerplate: among, top, quant, focus, big, notable, higher);
    C3  BA over an inverted window (from 2025-06-01, before the store floor) serves `terms: []` with a reason, and does not print an
        inverted from/to pair.
c24 (FWD-36 tone, ruling 4): for ?days=30/90/365, every chatter row's served `tone` and `voters` equal the latest `chatter_window`
    part's row for (security_key, window_days); a name with 0 voters serves `tone` null with `tone_reason` "no clear tone"; the
    "not served on this route yet" reason is gone.
c25 (FWD-38 (d) provenance, ruling 5), on BA, AMD, VLO, the `/ledger` route:
    C1  every class names a `source` or a non-empty `source_reason`;
    C2  the `news` class carries a run whose stamp equals the overlay provenance's harvested_news `last_run` (the page agrees with
        itself);
    C3  `denominators.classes_with_a_run` equals the number of classes with a served run.
c26 (Z-S86, ruling 6): DE_US_Equity's thesis and peers answer 200 with a plain reason (no 404); the control key ZZZZ_US_Equity still
    answers 404.
Verdict: R67 <CELL> SERVED: YES|NO.
"""
from __future__ import annotations

import argparse
import datetime
import importlib.util
import json
import re
import sys

ROOT = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables"
CAPTURE_LIB = ROOT + "/0.9.0_WK_AMGT_RESAPP~158/capture_lib.py"
PREFIX = "/api/scoped/amgt"
NAMES = ("BA_US_Equity", "AMD_US_Equity", "VLO_US_Equity")
EXTENDED = ("among", "top", "quant", "focus", "big", "notable", "higher")
WORD = re.compile(r"[a-z0-9']+")


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _stamp(value):
    return re.sub(r"[^0-9]", "", str(value or ""))[:14]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cell", choices=("c23", "c24", "c25", "c26"), required=True)
    ap.add_argument("--where", choices=("local", "deployed"), required=True)
    a = ap.parse_args()
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")

    from lib.research.api import scoped_amgt

    if a.where == "deployed":
        import boto3

        cl = _load("capture_lib", CAPTURE_LIB)
        lam = boto3.client("lambda", region_name=cl.REGION)

        def call(path, query=None):
            body, meta = cl._invoke(lam, path, query)
            return (200, body) if body is not None else (meta.get("status"), None)
    else:
        def call(path, query=None):
            r = scoped_amgt.handler({"rawPath": path, "requestContext": {"http": {"method": "GET"}},
                                     "headers": {"x-firm-id": "opal"}, "queryStringParameters": query})
            try:
                return r.get("statusCode"), json.loads(r.get("body") or "null")
            except ValueError:
                return r.get("statusCode"), None

    today = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    if a.cell == "c23":
        st, ch = call(PREFIX + "/lead-panel/timeseries/collected/chatter")
        rows = (ch or {}).get("rows") or []
        name_hits, list_hits, nonempty = [], [], 0
        payloads = 0
        for r in rows:
            key = r.get("security_key")
            words = set(WORD.findall(str(r.get("display_name") or "").lower()))
            root = str(r.get("ticker") or "").strip().split(" ")[0].lower()
            own = {w for w in words if len(w) >= 3} | ({root} if root else set())
            for label, q in (("default", None), ("0901", {"from": "2026-09-01", "to": today})):
                st_t, tl = call(f"{PREFIX}/security/{key}/timeline", q)
                payloads += 1
                terms = [str(t.get("term")).lower() for t in (((tl or {}).get("word_cloud") or {}).get("terms") or [])]
                if terms:
                    nonempty += 1
                hit = sorted(set(terms) & own)
                if hit:
                    name_hits.append(f"{key}/{label}:{','.join(hit[:3])}")
                lh = sorted(set(terms) & set(EXTENDED))
                if lh:
                    list_hits.append(f"{key}/{label}:{','.join(lh[:3])}")
        clause("C1 0 clouds carry their own ticker root or a served short-name word", st == 200 and rows and not name_hits,
               f"names {len(rows)} payloads {payloads} non-empty {nonempty} offenders {len(name_hits)} e.g. {name_hits[:6]}")
        clause("C2 0 clouds carry a word on the extended list", st == 200 and rows and not list_hits,
               f"payloads {payloads} offenders {len(list_hits)} e.g. {list_hits[:5]}")
        st, tl = call(f"{PREFIX}/security/BA_US_Equity/timeline", {"from": "2025-06-01", "to": "2025-06-30"})
        wc = (tl or {}).get("word_cloud") or {}
        win = wc.get("window") or {}
        inverted = bool(win.get("from") and win.get("to") and str(win["from"]) > str(win["to"]))
        clause("C3 an inverted window serves its reason and no inverted from/to pair",
               st == 200 and wc.get("terms") == [] and bool(str(wc.get("reason") or "").strip()) and not inverted,
               f"status {st} window {win} reason {str(wc.get('reason'))[:80]!r}")
    elif a.cell == "c24":
        from lib.research.harvest import publication_gold

        table = publication_gold._latest_gold_snapshot_rows("chatter_window")
        idx = {(t.get("security_key"), int(t.get("window_days"))): t for t in table}
        print(f"   chatter_window rows read: {len(table)}")
        for d in (30, 90, 365):
            st, b = call(PREFIX + "/lead-panel/timeseries/collected/chatter", {"days": str(d)})
            rows = (b or {}).get("rows") or []
            bad, old, missing = [], 0, 0
            for r in rows:
                if "not served on this route yet" in str(r.get("tone_reason") or ""):
                    old += 1
                t = idx.get((r.get("security_key"), d))
                if t is None:
                    missing += 1
                    continue
                voters = int(t.get("voters") or 0)
                if voters == 0:
                    good = r.get("tone") is None and str(r.get("tone_reason") or "") == "no clear tone"
                else:
                    good = r.get("tone") is not None and abs(float(r["tone"]) - float(t["tone"])) < 1e-9
                if not good or int(r.get("voters") or 0) != voters:
                    bad.append(f"{r.get('security_key')}:{r.get('tone')}/{r.get('voters')} vs {t.get('tone')}/{voters}")
            clause(f"C1 days={d} every row's tone and voters equal chatter_window, 0 voters read 'no clear tone'",
                   st == 200 and rows and not bad and old == 0 and missing == 0,
                   f"status {st} rows {len(rows)} mismatches {len(bad)} e.g. {bad[:3]} old-reason {old} no-table-row {missing}")
            # aq-6 (row Z-S346): C1 skips a row the CHECK's index lacks, so a function that cannot read the table is
            # invisible on those rows. C2 counts the unreadable-table reason over EVERY served row.
            unreadable = [r.get("security_key") for r in rows if "could not be read" in str(r.get("tone_reason") or "")]
            clause(f"C2 days={d} 0 rows serve the unreadable-table reason",
                   st == 200 and bool(rows) and not unreadable,
                   f"status {st} rows {len(rows)} unreadable {len(unreadable)} e.g. {unreadable[:3]}")
    elif a.cell == "c25":
        for key in NAMES:
            st_l, led = call(f"{PREFIX}/security/{key}/ledger")
            st_o, ov = call(f"{PREFIX}/security/{key}/overlay")
            led = led or {}
            classes = led.get("classes") or {}
            runs = led.get("latest_by_class") or {}
            unsourced = [c for c, v in classes.items() if not (v or {}).get("source") and not str((v or {}).get("source_reason") or "").strip()]
            news_ov = next((i for i in ((ov or {}).get("provenance") or {}).get("inputs") or [] if i.get("input") == "harvested_news"), {})
            news_run = runs.get("news") or {}
            agree = bool(news_ov.get("last_run")) and _stamp(news_run.get("stamp")) == _stamp(news_ov.get("last_run"))
            denom = (led.get("denominators") or {}).get("classes_with_a_run")
            clause(f"C1 {key} every class names a source or a source_reason", st_l == 200 and classes and not unsourced,
                   f"status {st_l} classes {len(classes)} unsourced {unsourced}")
            clause(f"C2 {key} the news class's run equals the overlay's harvested_news last_run", agree,
                   f"ledger news stamp {news_run.get('stamp')} overlay last_run {news_ov.get('last_run')}")
            clause(f"C3 {key} classes_with_a_run equals the served runs", denom is not None and denom == len(runs),
                   f"classes_with_a_run {denom} served runs {len(runs)}")
    else:
        for route in ("thesis", "peers"):
            st, b = call(f"{PREFIX}/security/DE_US_Equity/{route}")
            text = " ".join(str(v) for k, v in (b or {}).items() if "reason" in str(k).lower())
            clause(f"C1 DE_US_Equity {route} answers 200 with a plain reason", st == 200 and bool(text.strip()),
                   f"status {st} reason {text[:100]!r}")
        st, b = call(f"{PREFIX}/security/ZZZZ_US_Equity/thesis")
        clause("C2 the control ZZZZ_US_Equity thesis still answers 404", st == 404, f"status {st}")
    print(f"R67 {a.cell.upper()} SERVED: {'YES' if all(ok) else 'NO'}")
    return 0 if all(ok) else 1


if __name__ == "__main__":
    sys.exit(main())
