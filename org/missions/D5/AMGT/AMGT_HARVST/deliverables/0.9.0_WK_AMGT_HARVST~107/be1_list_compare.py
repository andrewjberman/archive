"""HVST-be-1 list comparison. `universe_securities.build()` as left by this cell, against the served list
(round33) and against the list as it stood (round57). READ-ONLY: no gold build, no silver read, no S3 write.

The pool universe is the snapshot `be1_pool_universe.json` (ONE read-only S3 GET of universe/v1/2026-10-06.json
through `universe_securities._read_universe()`, saved beside this script). `--live` re-reads the pool instead.
Run from the repo root:  python <this file> [--live]
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, *[".."] * 7))
sys.path.insert(0, ROOT)

from lib.research.harvest import universe_securities as us  # noqa: E402

COO = os.path.join(ROOT, "org", "missions", "D5", "AMGT", "AMGT_HARVST", "deliverables", "2.0.0_SA_COO_H")
SERVED = os.path.join(COO, "round33", "securities.universe.r33.json")
BEFORE = os.path.join(COO, "round57", "securities.universe.r57.json")
SNAPSHOT = os.path.join(HERE, "be1_pool_universe.json")
SIX = ["UNVGY_US_Equity", "SHOP_CN_Equity", "AMD_US_Equity", "BZLFY_US_Equity", "MER_PM_Equity", "BP_US_Equity"]

# The closed set of reasons a served alias may still be missing after, with the test for each.
REASONS = (
    "slash tail stripped",                       # served alias carries a /tail; the list carries it without the tail
    "receipt tail",                              # served alias ends in ADR/ADS/GDR; the list carries it without
    "legal name cut in the identity record",     # served alias is a longer form of a name the record cut at 30
    "legal name shorter than served alias",      # the record's name is the served alias minus a corporate/form word
    "whole brand refused by limb (a)",           # a hand-listed whole brand the build now refuses (summary whole_brand_refused)
    "hand alias with no source",                 # no source in the pool name or identity record
)


def load(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def folded(items):
    return {str(a).casefold() for a in items}


def reason_for(alias, security, legal_names, brand_refused=()):
    """ONE reason from REASONS for a served alias the list does not carry."""
    mine = folded(security["aliases"])
    if (security["security_key"], alias) in brand_refused:
        return "whole brand refused by limb (a)"
    cleaned = us.clean_legal_name(alias)[0]
    if cleaned != alias and cleaned.casefold() in mine:
        return "slash tail stripped"
    tokens = alias.split()
    if tokens and tokens[-1].upper() in ("ADR", "ADS", "GDR") and " ".join(tokens[:-1]).casefold() in mine:
        return "receipt tail"
    raw = legal_names.get(security["security_key"])
    if raw and len(raw) == us.LEGAL_NAME_EXACT_LENGTH and alias.casefold().startswith(raw.casefold()):
        return "legal name cut in the identity record"
    if raw and alias.casefold().startswith(us.clean_legal_name(raw)[0].casefold()):
        return "legal name shorter than served alias"
    return "hand alias with no source"


def main():
    live = "--live" in sys.argv
    legal_names, _info = us.load_legal_names()
    after, summary = us.build(universe_path=None if live else SNAPSHOT)
    served = load(SERVED)
    before = load(BEFORE)
    by = lambda rows: {s["security_key"]: s for s in rows}  # noqa: E731
    served_by, before_by, after_by = by(served), by(before), by(after)
    common = sorted(set(served_by) & set(after_by))
    lines = []
    out = lines.append
    fail = []

    out("UNIVERSE: %s  as_of %s" % (summary["universe"].get("source"), summary["universe"].get("as_of")))
    out("DENOMINATOR: served %d, before %d, after %d; common with served %d"
        % (len(served), len(before), len(after), len(common)))
    if len(after) != len(before):
        fail.append("after != before in security count: %d vs %d" % (len(after), len(before)))

    def missing(listed_by, key):
        have = folded(listed_by[key]["aliases"]) if key in listed_by else set()
        return [a for a in served_by[key]["aliases"] if a.casefold() not in have]

    common_before = [k for k in common if k in before_by]
    b_missing = [k for k in common_before if missing(before_by, k)]
    a_missing = [k for k in common if missing(after_by, k)]
    out("SERVED ALIAS MISSING: before %d of %d securities, after %d of %d"
        % (len(b_missing), len(common_before), len(a_missing), len(common)))
    reasons_after = {}
    brand_refused = {(r["security_key"], r["brand"]) for r in summary["whole_brand_refused"]}
    for key in a_missing:
        for alias in missing(after_by, key):
            why = reason_for(alias, after_by[key], legal_names, brand_refused)
            reasons_after[(key, alias)] = why
            out("  STILL MISSING %s: %r  reason: %s  (served %s | after %s)"
                % (key, alias, why, served_by[key]["aliases"], after_by[key]["aliases"]))
    out("  closed set of reasons: %s" % "; ".join(REASONS))

    out("THE SIX:")
    for key in SIX:
        miss = missing(after_by, key) if key in served_by and key in after_by else ["<absent>"]
        out("  %s: served %s | after %s | missing %s"
            % (key, served_by.get(key, {}).get("aliases"), after_by.get(key, {}).get("aliases"), miss))
        for alias in miss:
            if alias == "<absent>" or (key, alias) not in reasons_after:
                fail.append("THE SIX %s misses %r with no printed reason" % (key, alias))

    refused = summary["pool_name_refused_decorated"]
    out("POOL NAMES REFUSED AS DECORATED: %d" % refused["count"])
    for item in refused["items"]:
        out("  {security_key: %s, pool_name: %r}  reason: %s" % (item["security_key"], item["pool_name"], item["reason"]))
    pool_entries = {e["security_key"]: e for e in load(SNAPSHOT)["names"] if e.get("name") and e.get("security_key")}
    refused_keys = {i["security_key"] for i in refused["items"]}
    kept_beside = [k for k, e in pool_entries.items() if k in after_by and k not in refused_keys
                   and k in legal_names]
    kept_sole = [k for k in pool_entries if k in after_by and k not in refused_keys and k not in legal_names]
    out("POOL NAMES KEPT: %d (beside the legal name %d, sole name with no identity record %d); summary "
        "pool_name_kept_as_alias %d"
        % (len(kept_beside) + len(kept_sole), len(kept_beside), len(kept_sole), summary["pool_name_kept_as_alias"]))
    for key in kept_beside:
        out("  KEPT beside legal: {security_key: %s, pool_name: %r, legal: %r}"
            % (key, pool_entries[key]["name"], legal_names[key]))
    for key in kept_sole:
        out("  KEPT sole (no identity record): {security_key: %s, pool_name: %r}" % (key, pool_entries[key]["name"]))
    out("DECORATED BUT NO IDENTITY RECORD: %s" % summary["decorated_but_no_identity_record"])

    def new_forms(listed_by, keys):
        found = []
        for key in keys:
            have = set(served_by.get(key, {}).get("ticker_aliases") or [])
            for form in listed_by[key].get("ticker_aliases") or []:
                if form not in have:
                    found.append((key, form))
        return found

    # over EVERY security of the list (a security the served file lacks counts as having no served form): the order's 43
    forms_before = new_forms(before_by, sorted(before_by))
    forms_after = new_forms(after_by, sorted(after_by))
    out("NEW EXACT-CASE TICKER FORMS vs served: before %d after %d" % (len(forms_before), len(forms_after)))
    out("  after: %s" % ", ".join("%s=%s" % (k.split("_")[0], f) for k, f in forms_after))
    out("  removed vs before: %s" % ", ".join("%s=%s" % (k, f) for k, f in forms_before if (k, f) not in forms_after))
    out("  of which on the %d securities common with served: before %d after %d"
        % (len(common), len([1 for k, _f in forms_before if k in served_by]),
           len([1 for k, _f in forms_after if k in served_by])))

    changed = [k for k in after_by if k in before_by and after_by[k]["aliases"] != before_by[k]["aliases"]]
    out("ALIAS SETS CHANGED vs before: %d of %d" % (len(changed), len(after_by)))
    for key in changed:
        out("  %s: before %s -> after %s" % (key, before_by[key]["aliases"], after_by[key]["aliases"]))
    company_changed = [k for k in after_by if k in before_by and after_by[k]["company"] != before_by[k]["company"]]
    out("COMPANY NAMES CHANGED vs before: %d of %d" % (len(company_changed), len(after_by)))

    out("SUMMARY: company_name_from_pool %d, company_name_from_identity %d, pool_name_kept_as_alias %d, "
        "pool_name_refused_decorated %d, decorated_but_no_identity_record %d, ticker_aliases_added %d, "
        "ticker_forms_refused_by_reason %s"
        % (summary["company_name_from_pool"], summary["company_name_from_identity"],
           summary["pool_name_kept_as_alias"], refused["count"],
           summary["decorated_but_no_identity_record"]["count"], summary["ticker_aliases_added"],
           summary["ticker_forms_refused_by_reason"]))

    # --- the LIST OK conditions -------------------------------------------------------------------------------
    for key in SIX:
        for alias in (missing(after_by, key) if key in served_by and key in after_by else []):
            if reasons_after.get((key, alias)) not in REASONS:
                fail.append("THE SIX %s: %r reason not in the closed set" % (key, alias))
    exempt_hits = []
    for key, security in after_by.items():
        legal_forms = set()
        if key in legal_names:
            company = us.strip_ticker_tail(us.clean_legal_name(legal_names[key])[0], security["ticker"])
            legal_forms = folded(us._entry_aliases(company, security["ticker"])[0])
        for alias in security["aliases"]:
            why = us.pool_name_decoration(alias, security["ticker"], key)
            if why and alias.casefold() in legal_forms:
                exempt_hits.append((key, alias, why))  # a form of the LEGAL name: R1 carries it whatever it reads like
            elif why:
                fail.append("after alias %r of %s matches the decorated rule (%s)" % (alias, key, why))
    out("AFTER ALIASES THAT READ AS DECORATED BUT ARE FORMS OF THE LEGAL NAME (kept by R1): %d" % len(exempt_hits))
    for key, alias, why in exempt_hits:
        out("  %s: %r (%s)" % (key, alias, why))
    out("WHOLE BRANDS: refused before %d after %d; admitted before %d after %d; refused after: %s"
        % (len(load(os.path.join(COO, "round57", "securities.universe.r57.summary.json"))["whole_brand_refused"]),
           len(summary["whole_brand_refused"]),
           len(load(os.path.join(COO, "round57", "securities.universe.r57.summary.json"))["whole_brand_admitted"]),
           len(summary["whole_brand_admitted"]), sorted(brand_refused)))
    for key, security in after_by.items():
        if "AI" in (security.get("ticker_aliases") or []):
            fail.append("%s carries the ticker form AI" % key)
    no_name = []
    for key, raw in legal_names.items():
        if key not in after_by:
            continue
        cleaned = us.clean_legal_name(raw)[0]
        if cleaned.casefold() not in folded(after_by[key]["aliases"]):
            no_name.append((key, cleaned))
    out("IDENTITY NAME NOT AMONG ALIASES: %d  %s" % (len(no_name), no_name))
    for key, cleaned in no_name:
        fail.append("%s: identity name %r is not among its aliases" % (key, cleaned))

    if fail:
        for item in fail:
            out("FAIL LINE: %s" % item)
        out("LIST FAIL")
    else:
        out("LIST OK")

    text = "\n".join(lines) + "\n"
    with open(os.path.join(HERE, "be1_list_compare.out"), "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    with open(os.path.join(HERE, "securities.universe.r58.json"), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(after, handle, indent=1, sort_keys=True)
    sys.stdout.write(text)
    return 0 if not fail else 1


if __name__ == "__main__":
    raise SystemExit(main())
