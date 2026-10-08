"""Read-only: what is ICT_US_Equity and which source carries it. S3 GET only (pool universe).
Run from repo root: PYTHONPATH=. python <this file>"""
import json
import re

from lib.research.metrics import chatter_axis as ca

LIST = "org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_H/round60/securities.universe.r60.json"
REG = "lib/research/identity/registrations.json"
CFG = "lib/opal_data_harvest/config.json"
KEY = "ICT_US_Equity"
TOK = re.compile(r"(?<![A-Za-z0-9])ICT(?![A-Za-z0-9])")
ID_FIELDS = re.compile(r"key|ticker|name|company|bloomberg|folder|value|cik|lei|figi|isin|sedol", re.I)


def load(path):
    with open(path, encoding="utf-8") as h:
        return json.load(h)


def flat(obj, prefix=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            for x in flat(v, prefix + "." + k if prefix else k):
                yield x
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            for x in flat(v, "%s[%d]" % (prefix, i)):
                yield x
    elif isinstance(obj, str):
        yield prefix, obj


def scan(records):
    hits = []
    for r in records:
        fields = [(p, v) for p, v in flat(r) if ID_FIELDS.search(p) and TOK.search(v)]
        if fields:
            hits.append((r, fields))
    return hits


def block(label, where, records, carriers):
    print("SOURCE %s: %s" % (label, where))
    print("  record count (denominator): %d" % len(records))
    hits = scan(records)
    print("  records carrying ICT as a whole token: %d" % len(hits))
    for r, fields in hits:
        idf = {p: v for p, v in flat(r) if re.search(r"(^|\.)(key|security_key|bloomberg|bloomberg_security|ticker|name|company|company\.value|pool_name|folder|ticker\.value)$", p)}
        print("  - " + json.dumps(idf)[:300])
        print("    ICT in: " + json.dumps([p for p, _v in fields])[:300])
        if any(KEY in v or KEY == v for _p, v in flat(r)):
            carriers.add(label)
    return len(records)


def main():
    carriers = set()
    counts = {}
    names = {}
    gold = load(LIST)
    counts["a"] = block("a (gold list)", LIST, gold, carriers)
    for s in gold:
        if s.get("security_key") == KEY:
            names["a"] = s.get("company")
    reg = load(REG)["registrations"]
    counts["b"] = block("b (identity registry registrations)", REG, reg, carriers)
    for s in reg:
        if s.get("security_key") == KEY:
            names["b"] = (s.get("identity") or {}).get("name")
    cfg = load(CFG)["symbol_resolution_source"]
    recs = load(cfg)["records"]
    counts["c"] = block("c (collector identity record)", cfg, recs, carriers)
    for s in recs:
        if s.get("security_key") == KEY:
            names["c"] = (s.get("company") or {}).get("value")
    doc, src = ca._read_pool_universe()
    print("POOL UNIVERSE FETCHED FROM: s3://%s/%s (S3 GET, no put)" % (ca.pool_reader.POOL_BUCKET, src.replace("pool:", "")))
    pool = doc.get("names") or []
    counts["d"] = block("d (pool universe, build() default read)", src, pool, carriers)
    for s in pool:
        if s.get("security_key") == KEY or (s.get("ticker") or "").replace(" ", "_") == KEY[:-7] + "_US":
            names["d"] = s.get("name")
    print("  pool entry keys: %s" % sorted({k for s in pool for k in s}))
    landed = load(ca.DEFAULT_UNIVERSE_PATH)
    lrec = landed.get("names") or []
    counts["e"] = block("e (landed fallback universe build() reads when the pool fails; research_names and sa_symbols are caller-named options with no default path)", ca.DEFAULT_UNIVERSE_PATH, lrec, carriers)
    print("SOURCES READ: %d of 5" % len([k for k in counts if counts[k] is not None]))
    order = sorted(carriers)
    print("SOURCES CARRYING ICT_US_Equity: %s" % (order or "NONE"))
    print("COMPANY NAMES ON THAT EXACT KEY: %s" % json.dumps(names))
    distinct = {v.strip().lower() for v in names.values() if v}
    if names and distinct:
        if len(distinct) > 1:
            print("SOURCES DISAGREE: %s" % json.dumps(names))
        first = sorted(names)[0]
        print("ICT_US_Equity IS: %s -- per source %s" % (names[first], first))
    else:
        print("NO SOURCE NAMES ICT_US_Equity")
    pm = [s for s in reg if s.get("security_key") == "ICT_PM_Equity"]
    pmc = [s for s in recs if s.get("security_key") == "ICT_PM_Equity"]
    print("ICT_PM_Equity registry: %s" % json.dumps([(s.get("identity") or {}).get("name") for s in pm]))
    print("ICT_PM_Equity collector record: %s" % json.dumps([(s.get("company") or {}).get("value") for s in pmc]))
    us = [s for s in reg if s.get("security_key") == KEY]
    shared = []
    for a in us:
        for b in pm:
            for f in ("lei", "cik", "sec_id", "isin", "figi", "name"):
                av, bv = (a.get("identity") or {}).get(f), (b.get("identity") or {}).get(f)
                if av and av == bv:
                    shared.append(f)
    print("ICT_US_Equity and ICT_PM_Equity: %s" % (("SHARED FIELDS " + ",".join(shared)) if shared else "NOT SHOWN BY ANY FIELD"))
    ok = all(counts[k] > 0 for k in "abcd")
    print("RECORD OK" if ok else "RECORD FAIL")


main()
