"""AMGT_RESAPP round-92 PREP -- the census the CTO's round-91 analysis names (`amgt_minor_unit_census`): no minor-unit currency label beside a
major-unit price anywhere on the live peers routes, no served currency beside a stale reason, and the correct major-unit codes kept.

  PYTHONPATH=<repo root> python r92_minor_unit_census.py [--where deployed|local] [--limit N]

Every member of every keyed subject's peers route (243 subjects, about 2,230 members) is read (Lambda invoke, GET only; `--where local`
calls the repo's own handler on the same live pool):
    M1 member rows serving a currency whose code is a minor-unit code (a lower-case last letter, or GBX, ILA): must be 0.
    M2 member rows serving BOTH a `price_currency` and a `price_currency_reason`: must be 0.
    M3 control: member rows serving a major-unit currency: reported, and must be at least the base's 149 (USD 125, CHF 9, EUR 8,
       JPY 6, HKD 1) less any that a legitimate refusal removes; this floor guards a guard that serves nothing.
    M4 (CTO~DELL1 added condition, round-92 qq-5 pair): the census prints its DENOMINATOR (every served `price_currency` code, by
       code) beside the record currencies of the held index (the `CRNCY` header figure of every crosswalk record, by code, read by
       the function's own `_record_trading_currency`). A record currency that is neither a plain three-capital-letter major code
       nor one the guard classifies as minor, or a known minor spelling the guard does not classify (`ZAC`), reads as a FINDING
       and fails M4: an unlisted minor-unit spelling is a finding, never a pass.
Verdict: R92 MINOR-UNIT CENSUS: YES|NO (exit 0|1). At the base (2026-10-11, live l8egBo/rf..) M1 reads 12 and M2 reads 156: NO.
"""
import argparse
import collections
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor

import boto3

from lib.research.api import scoped_amgt
from lib.research.identity import crosswalk

FN = "opal-amgt-scoped-api"
PREFIX = "/api/scoped/amgt"
MAJOR_FLOOR = 149
_LAM = boto3.client("lambda", region_name="us-east-1")


def peers(where, key):
    event = {"rawPath": "%s/security/%s/peers" % (PREFIX, key), "queryStringParameters": None,
             "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"}}
    if where == "deployed":
        r = json.loads(_LAM.invoke(FunctionName=FN, Payload=json.dumps(event).encode())["Payload"].read())
    else:
        r = scoped_amgt.handler(event)
    return json.loads(r.get("body") or "{}")


KNOWN_MINOR_SPELLINGS = ("GBX", "GBp", "ILA", "ILs", "ZAc", "ZAC")


def held_index_currencies(keys):
    """{code or None: [keys]} from the function's own record read for every held record key."""
    out = collections.defaultdict(list)
    with ThreadPoolExecutor(max_workers=8) as pool:
        for key, (status, value) in zip(keys, pool.map(scoped_amgt._record_trading_currency, keys)):
            out[value if status == "OK" else "<%s>" % status].append(key)
    return out


def is_minor(code):
    return isinstance(code, str) and (code in ("GBX", "ILA") or (len(code) == 3 and code[-1].islower()))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--where", default="deployed", choices=["deployed", "local"])
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()
    doc, _i, _a = crosswalk.load_crosswalk()
    keys = [r["security_key"] for r in doc["records"] if r.get("resolution") == "MEASURED" and r.get("security_key")]
    if args.limit:
        keys = keys[: args.limit]
    rows = minor = both = major = 0
    examples = []
    served_codes = collections.Counter()
    for key in keys:
        for m in peers(args.where, key).get("members") or []:
            if not isinstance(m, dict):
                continue
            rows += 1
            cur, reason = m.get("price_currency"), m.get("price_currency_reason")
            if cur and is_minor(cur):
                minor += 1
                if len(examples) < 4:
                    examples.append((key, m.get("ticker"), m.get("price"), cur))
            elif cur:
                major += 1
            if cur:
                served_codes[cur] += 1
            if cur and reason:
                both += 1
    print("   where=%s subjects=%d | member rows %d | major-unit currencies served %d | minor-unit labels %d | currency AND reason %d" % (
        args.where, len(keys), rows, major, minor, both))
    for e in examples:
        print("   minor-unit e.g. %s %s price=%s currency=%s" % e)
    print("   served price_currency codes (denominator %d rows): %s" % (
        sum(served_codes.values()), ", ".join("%s %d" % kv for kv in sorted(served_codes.items(), key=lambda kv: (-kv[1], kv[0]))) or "none"))
    held = held_index_currencies(sorted({r["security_key"] for r in doc["records"] if r.get("security_key")}))
    print("   record currencies in the held index (denominator %d records):" % sum(len(v) for v in held.values()))
    findings = []
    for code, ks in sorted(held.items(), key=lambda kv: (-len(kv[1]), str(kv[0]))):
        plain = isinstance(code, str) and re.fullmatch(r"[A-Z]{3}", code) is not None
        guard_minor = is_minor(code)
        spelled = isinstance(code, str) and code in KNOWN_MINOR_SPELLINGS
        if code is None or (isinstance(code, str) and code.startswith("<")):
            kind = "no figure (record %s)" % ("without a CRNCY" if code is None else code.strip("<>").lower())
        elif guard_minor:
            kind = "MINOR (guard refuses)"
        elif spelled:
            kind = "FINDING: known minor spelling the guard does not classify"
            findings.append(code)
        elif plain:
            kind = "major"
        elif isinstance(code, str):
            kind = "FINDING: neither a plain major code nor a classified minor"
            findings.append(code)
        else:
            kind = "FINDING: not a string"
            findings.append(code)
        print("     %-12s %4d record(s)  %s" % (code, len(ks), kind))
    m1, m2 = minor == 0, both == 0
    m3 = major >= MAJOR_FLOOR or args.limit is not None
    m4 = not findings
    for ok, label in ((m1, "M1 no minor-unit label beside a scanner price"), (m2, "M2 no served currency beside a stale reason"),
                      (m3, "M3 control: the major-unit codes are kept (floor %d)" % MAJOR_FLOOR),
                      (m4, "M4 every record currency in the held index is a plain major code or a classified minor unit")):
        print("%s %s" % ("PASS" if ok else "FAIL", label))
    ok = m1 and m2 and m3 and m4
    print("R92 MINOR-UNIT CENSUS: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
