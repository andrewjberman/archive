"""AMGT_RESAPP round 78 -- AMGT-bb-7: name search by company name (row AMGT_RESAPP-Z-W275-S1; CTO round-77 ruling 14).

  --crit AC1|AC2|AC3 --where local
  --crit READ --where local|deployed      (the measure alone; always exit 0)

`lib.research.api.name_search.resolve_query(q)` lists a company only when the stored record carries a name. The legal
names AMGT_HARVST joined live in ITS identity record (the path is `symbol_resolution_source` in
lib/opal_data_harvest/config.json, read by lib.research.harvest.universe_securities.load_legal_names). This check reads
that record only to COUNT what a join would reach; the build must not read it at run time.

A record "carries a readable name" when the name search returns it, asked by its own key, with a `name` that is not just
its ticker's first word.

AC1 (build; FAILS at the base):
    C1 "apple" lists AAPL_US_Equity and "microsoft" lists MSFT_US_Equity, status "candidates", each candidate with a
       non-empty name and ticker, and the listed name is a company name, not the ticker;
    C2 the denominator: 238 or more of the stored records carry a readable name (the base reads 100 of 243), and the
       records still without one are printed;
    C3 lib.research.api._company_names imports, holds 230 or more names, every one of them equal to the cleaned legal
       name AMGT_HARVST's record holds for that key (a copy, nothing typed by hand).
AC2 (build; FAILS at the base): lib/research/api/tests/test_name_search.py holds a test named
    test_a_legal_name_lists_its_company and the whole file passes.
AC3 (bound; PASSES at the base and after):
    C1 every stored record's own key still passes through as "exact" (N of N);
    C2 a typed company name is never answered as "exact": "apple", "microsoft", "lenovo" and "airbnb" are not;
    C3 "lenovo" still lists 992_HK_Equity and "airbnb" still lists ABNB_US_Equity; "zzqx no such company 7781" and ""
       still read "none" with a plain reason.
Verdict: R78 BB7 <CRIT> SERVED: YES|NO (exit 0|1). READ prints R78 BB7 READ: DONE.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

TEST = "lib/research/api/tests/test_name_search.py"
TEST_NAME = "test_a_legal_name_lists_its_company"
QUERIES = ("apple", "microsoft", "airbnb")
FN = "opal-amgt-scoped-api"


def _root(record_ticker):
    return str(record_ticker or "").split(" ")[0].strip().lower()


def _readable(fn, keys):
    have, lack = [], []
    for key in keys:
        cands = fn(key).get("candidates") or []
        cand = cands[0] if cands else {}
        name = str(cand.get("name") or "").strip()
        (have if name and name.lower() != _root(cand.get("ticker")) else lack).append(key)
    return have, lack


def _show(q, r):
    print("   %r: status %s candidates %s reason %r" % (
        q, r.get("status"), [(c.get("security_key"), c.get("name")) for c in (r.get("candidates") or [])][:5],
        r.get("reason")))


def _legal():
    from lib.research.harvest import universe_securities as us

    names, info = us.load_legal_names()
    return {k: us.clean_legal_name(v)[0] for k, v in names.items()}, info


def measure(where):
    from lib.research.api import name_search
    from lib.research.identity import crosswalk

    document = crosswalk.load_crosswalk()[0]
    keys = sorted({r["security_key"] for r in document["records"] if r.get("security_key")})
    print("   stored name list as_of %s; records %d" % (document.get("as_of"), len(keys)))
    have, lack = _readable(name_search.resolve_query, keys)
    print("   records carrying a readable name %d of %d; without %d" % (len(have), len(keys), len(lack)))
    legal, info = _legal()
    print("   AMGT_HARVST legal names: %d loaded from %s" % (len(legal), os.path.relpath(info["path"]).replace("\\", "/")))
    reach = [k for k in lack if k in legal]
    print("   of the %d without a name, the legal names hold %d; still without %d %s" % (
        len(lack), len(reach), len(lack) - len(reach), sorted(set(lack) - set(legal))))
    print("   legal names not ASCII: %d" % sum(1 for v in legal.values() if any(ord(ch) > 127 for ch in v)))
    if where == "deployed":
        import boto3

        lam = boto3.client("lambda", region_name="us-east-1")
        for q in QUERIES:
            event = {"rawPath": "/api/scoped/amgt/resolve", "requestContext": {"http": {"method": "GET"}},
                     "headers": {"x-firm-id": "opal"}, "queryStringParameters": {"q": q}}
            raw = json.loads(lam.invoke(FunctionName=FN, Payload=json.dumps(event).encode())["Payload"].read())
            print("   deployed, status code %s:" % raw.get("statusCode"))
            _show(q, json.loads(raw.get("body") or "{}"))
    else:
        for q in QUERIES:
            _show(q, name_search.resolve_query(q))
    return keys, have, lack


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", choices=("AC1", "AC2", "AC3", "READ"), required=True)
    ap.add_argument("--where", choices=("local", "deployed"), default="local")
    a = ap.parse_args()
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print("%s %s %s" % ("PASS" if cond else "FAIL", name, detail))

    if a.crit == "READ":
        measure(a.where)
        print("R78 BB7 READ: DONE")
        return 0

    if a.crit == "AC2":
        text = open(TEST, encoding="utf-8").read() if os.path.isfile(TEST) else ""
        clause("C1 the test file holds %s" % TEST_NAME, ("def %s(" % TEST_NAME) in text)
        p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", TEST], capture_output=True,
                           timeout=600)
        tail = (p.stdout + p.stderr).decode("utf-8", errors="replace").strip().split("\n")[-1]
        print("   " + tail)
        clause("C2 every case in the file passes", p.returncode == 0 and " passed" in tail and "failed" not in tail,
               "rc=%d" % p.returncode)
        return verdict(a, ok)

    from lib.research.api import name_search

    fn = name_search.resolve_query
    if a.crit == "AC3":
        from lib.research.identity import crosswalk

        document = crosswalk.load_crosswalk()[0]
        keys = sorted({r["security_key"] for r in document["records"] if r.get("security_key")})
        miss = [k for k in keys if not (fn(k).get("status") == "exact" and fn(k).get("security_key") == k)]
        clause("C1 every stored key passes through as exact", keys and not miss,
               "%d of %d" % (len(keys) - len(miss), len(keys)))
        typed = {q: fn(q) for q in ("apple", "microsoft", "lenovo", "airbnb")}
        clause("C2 a typed company name is never answered as exact",
               all(r.get("status") != "exact" and not r.get("security_key") for r in typed.values()),
               str({q: r.get("status") for q, r in typed.items()}))
        lists = {"lenovo": "992_HK_Equity", "airbnb": "ABNB_US_Equity"}
        kept = all(any(c.get("security_key") == want for c in (typed[q].get("candidates") or []))
                   for q, want in lists.items())
        nones = [fn("zzqx no such company 7781"), fn("")]
        clause("C3 the names that listed before still list, and no match still reads a plain reason",
               kept and all(r.get("status") == "none" and not r.get("candidates") and str(r.get("reason") or "").strip()
                            for r in nones))
        return verdict(a, ok)

    keys, have, lack = measure("local")
    good = []
    for q, want in (("apple", "AAPL_US_Equity"), ("microsoft", "MSFT_US_Equity")):
        r = fn(q)
        cands = r.get("candidates") or []
        hit = next((c for c in cands if c.get("security_key") == want), None)
        good.append(r.get("status") == "candidates" and hit is not None
                    and all(c.get("name") and c.get("ticker") for c in cands)
                    and q in str((hit or {}).get("name") or "").lower())
    clause("C1 apple and microsoft list their companies by company name", all(good))
    clause("C2 238 or more records carry a readable name", len(have) >= 238,
           "%d of %d; without %s" % (len(have), len(keys), lack[:12]))
    try:
        from lib.research.api import _company_names
    except ImportError as err:
        clause("C3 lib.research.api._company_names imports", False, str(err))
        return verdict(a, ok)
    packaged = getattr(_company_names, "NAMES", None)
    legal, _info = _legal()
    differ = [k for k, v in (packaged or {}).items() if legal.get(k) != v]
    clause("C3 the packaged names are a copy of the legal names", isinstance(packaged, dict) and len(packaged) >= 230
           and not differ, "%d packaged; %d differ %s" % (len(packaged or {}), len(differ), differ[:5]))
    return verdict(a, ok)


def verdict(a, ok):
    yes = bool(ok) and all(ok)
    print("R78 BB7 %s SERVED: %s" % (a.crit, "YES" if yes else "NO"))
    return 0 if yes else 1


if __name__ == "__main__":
    sys.exit(main())
