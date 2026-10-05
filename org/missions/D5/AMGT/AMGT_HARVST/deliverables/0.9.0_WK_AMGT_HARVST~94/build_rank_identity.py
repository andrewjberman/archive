"""HVST-as-1: snapshot the rank universe and resolve each name's search identities, with NO vendor call.

Step 1 (one pool read, skipped when the snapshot exists unless --refresh): `chatter_axis.read_universe_names()` ->
`rank_universe_20260916.json`.
Step 2 (local only): per name, company / ticker / aliases / sa_symbol, each carrying status + evidence ->
`rank_universe_identity_20260916.json`.

sa_symbol rules, in order (the first that fires wins; nothing is guessed silently):
  R0 the pool `name` IS a folder of the 89-name resolution file -> that file's symbol, its own status carried.
  R1 the cleaned pool name equals (case/punctuation-folded) the cleaned company of one 89-file folder -> that symbol.
  R2 the pool ticker is a US listing (`<SYMBOL> US` / `<SYMBOL> US Equity`, SYMBOL = 1-5 capital letters) -> the
     SYMBOL is its own SA symbol, status DERIVED (not probed against Seeking Alpha).
  R2b an ISSUER ruling for a named key (ISSUER_RULED below), status ISSUER, its ruling quoted as evidence.
  R3 otherwise UNRESOLVED (value null).
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, *([os.pardir] * 7)))
sys.path.insert(0, ROOT)

from lib.opal_data_harvest.publishers import legacy  # noqa: E402
from lib.opal_data_harvest.storage import content_hash  # noqa: E402

SNAPSHOT = os.path.join(HERE, "rank_universe_20260916.json")
IDENTITY = os.path.join(HERE, "rank_universe_identity_20260916.json")
CONFIG = os.path.join(ROOT, "lib", "opal_data_harvest", "config.json")
RESOLVED = os.path.join(ROOT, "org", "tier1_exec", "2.0.0_SA_COO", "deliverables", "AMGT_HARVST",
                        "SA_SYMBOLS_MERGED_89_20260927.json")
US_TICKER = re.compile(r"^([A-Z]{1,5}) US( Equity)?$")
# Issuer ruling on row AMGT_HARVST-Z-W94-S1 (2.0.0_SA_COO~H, 2026-10-05): TPG Inc trades on Nasdaq as TPG; the pool's Bloomberg
# ticker '2602335D US Equity' is a placeholder. Not probed: the run's own sa job confirms or refutes it.
ISSUER_RULED = {"2602335D_US_Equity": "TPG"}


def fold(text):
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def write_json(path, value):
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(value, indent=2, ensure_ascii=True) + "\n")


def snapshot(refresh):
    if os.path.exists(SNAPSHOT) and not refresh:
        return json.load(open(SNAPSHOT, encoding="utf-8"))
    from lib.research.metrics import chatter_axis
    entries, meta = chatter_axis.read_universe_names()
    doc = {"source_key": (meta.get("source") or "").replace("pool:", ""), "bucket": "opal-data-harvest",
           "names_read": meta.get("names_read"), "names_considered": meta.get("names_considered"),
           "denominators": meta.get("denominators"), "meta": meta, "entries": entries}
    write_json(SNAPSHOT, doc)
    return doc


def clean_company(name, ticker):
    """Strip a trailing ticker (the folder-style `Boeing BA`) from a pool name; a Bloomberg-style name is left."""
    root = re.sub(r"\s+(US|Equity)\b", "", ticker or "").strip()
    cut = name
    for suffix in filter(None, {root, (ticker or "").strip()}):
        if cut.endswith(" " + suffix):
            cut = cut[: -len(suffix) - 1].strip()
    return cut


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()
    snap = snapshot(args.refresh)
    names_mod = legacy("ir_domain_bulk_pass")
    config = json.load(open(CONFIG, encoding="utf-8"))
    pilots = {s["company"].lower(): s for s in config["pilot_securities"]}
    resolved = json.load(open(RESOLVED, encoding="utf-8"))
    folders = {r["folder"]: r for r in resolved["records"] if (r.get("sa_symbol") or {}).get("value")}
    by_company = {}
    for folder in folders:
        by_company.setdefault(fold(names_mod.company_name(folder)), []).append(folder)

    records = []
    for entry in snap["entries"]:
        pool_name, ticker = entry["name"], entry["ticker"]
        rec = {"security_key": entry["security_key"], "pool_name": pool_name}
        folder = pool_name if pool_name in folders else None
        company_status = "MEASURED"
        if folder:
            company = names_mod.company_name(folder)
            company_status, company_ev = "DERIVED", "89-file folder %r cleaned by ir_domain_bulk_pass.company_name" % folder
        else:
            company = clean_company(pool_name, ticker)
            company_ev = "pool name as read" if company == pool_name else "pool name %r with its trailing ticker removed" % pool_name
            if company != pool_name:
                company_status = "DERIVED"
        pilot = None
        if folder:
            pilot = next((v for k, v in pilots.items() if k in company.lower()
                          or (folder == "Haliburton HAL" and v["ticker"] == "HAL")), None)
        if pilot:
            rec["key"] = pilot["key"]
            rec["company"] = {"value": pilot["company"], "status": "MEASURED", "evidence": "config.json pilot_securities %s" % pilot["key"]}
            rec["ticker"] = {"value": pilot["ticker"], "status": "MEASURED", "evidence": "config.json pilot_securities %s" % pilot["key"]}
            rec["aliases"] = {"value": list(pilot["aliases"]), "status": "MEASURED", "evidence": "config.json pilot_securities %s" % pilot["key"]}
            rec["sa_symbol"] = {"value": pilot["sa_symbol"], "status": "MEASURED", "evidence": "config.json pilot_securities %s" % pilot["key"]}
            records.append(rec)
            continue
        rec["key"] = "security-" + content_hash(entry["security_key"])[:16]
        rec["company"] = {"value": company, "status": company_status, "evidence": company_ev}
        rec["ticker"] = {"value": ticker, "status": entry.get("identity_status") or "MEASURED", "evidence": "pool universe entry ticker"}
        rec["aliases"] = {"value": [company], "status": "DERIVED", "evidence": "the cleaned company name alone"}
        cell = None
        if folder:
            src = folders[folder]["sa_symbol"]
            cell = {"value": src["value"], "status": src["status"], "evidence": "R0: pool name is 89-file folder %r (%s)" % (folder, src["status"])}
        else:
            hits = by_company.get(fold(company), [])
            if len(hits) == 1:
                src = folders[hits[0]]["sa_symbol"]
                cell = {"value": src["value"], "status": src["status"], "evidence": "R1: cleaned name equals 89-file folder %r company (%s)" % (hits[0], src["status"])}
        if cell is None:
            m = US_TICKER.match(ticker or "")
            if entry["security_key"] in ISSUER_RULED:
                cell = {"value": ISSUER_RULED[entry["security_key"]], "status": "ISSUER",
                        "evidence": "R2b: issuer ruling on row Z-W94-S1 (TPG Inc trades on Nasdaq as TPG; %r is a Bloomberg "
                                    "placeholder); not probed, the run's sa job confirms it" % ticker}
            elif m:
                cell = {"value": m.group(1), "status": "DERIVED",
                        "evidence": "R2: US-listed Bloomberg ticker %r used as its own SA symbol; not probed against Seeking Alpha" % ticker}
            else:
                cell = {"value": None, "status": "UNRESOLVED",
                        "evidence": "R3: no 89-file match and %r is not a US-listed ticker" % ticker}
        rec["sa_symbol"] = cell
        records.append(rec)

    keys = [r["key"] for r in records]
    if len(records) != len(snap["entries"]) or len(set(keys)) != len(keys):
        raise SystemExit("ERROR: identity records %d vs entries %d, distinct keys %d" % (len(records), len(snap["entries"]), len(set(keys))))
    doc = {"artifact": "rank universe search identities (HVST-as-1)", "author": "0.9.0_WK_AMGT_HARVST~94",
           "rules": __doc__.strip().splitlines(), "snapshot": os.path.basename(SNAPSHOT),
           "denominator": {"names": len(records)}, "records": records}
    write_json(IDENTITY, doc)
    print("snapshot entries: %d (source %s)" % (len(snap["entries"]), snap["source_key"]))
    for field in ("company", "ticker", "aliases", "sa_symbol"):
        tally = {}
        for r in records:
            cell = r[field]
            tag = cell["status"] if (cell["value"] or cell["value"] == []) and cell["value"] != [] else "UNRESOLVED"
            tally[tag] = tally.get(tag, 0) + 1
        print("coverage %-9s %s of %d  %s" % (field, len(records) - tally.get("UNRESOLVED", 0), len(records), tally))
    for r in records:
        if r["sa_symbol"]["status"] == "UNRESOLVED":
            print("UNRESOLVED sa_symbol: %s | %s | %s" % (r["security_key"], r["ticker"]["value"], r["pool_name"]))


if __name__ == "__main__":
    main()
