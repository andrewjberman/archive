"""AC4 (JUDGMENT -- PRESENTED, NOT GRADED) -- are the listing rows that reached silver actually
about the security they are filed under?

SAMPLE, and how it was chosen: EVERY sa `listing_hit` row now in silver -- n = the full population
of sa rows this cell landed (20 from the held LNVGY page drained by AC1, 20 from the ASML page
captured by AC2). A census, not a convenience sample, so there is no selection to argue about; the
denominator is printed and the two source pages are labelled per row.

WHAT "FILED UNDER" MEANS HERE, measured rather than assumed: a listing_hit row carries NO
security_key column. The file-under decision is made downstream by
`publication_gold._listing_hit_security_match`, which word-bounds each security's ALIASES against
the row's `search_query`. So this script prints, per row: the vendor symbol the row came from
(`search_query`, plus the symbol in the row's own content href as an independent read), the article
title, and the security_key(s) the matcher files the row under -- for both populations AC3 measured.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.path.join(
    os.getcwd(), "org", "missions", "D5", "AMGT", "AMGT_HARVST", "deliverables",
    "0.9.0_WK_AMGT_HARVST~22", "scripts"))

from _census import client, listing_hit_rows
from lib.opal_data_harvest.__main__ import universe
from lib.research.harvest.publication_gold import _listing_hit_security_match, _security_aliases

OUT_DIR = os.path.join("org", "missions", "D5", "AMGT", "AMGT_HARVST", "deliverables",
                       "0.9.0_WK_AMGT_HARVST~22")
SYMBOL_HREF = re.compile(r"seekingalpha\.com/symbol/([A-Za-z0-9._-]+)")

with open(os.path.join("org", "missions", "D5", "AMGT", "AMGT_HARVST", "deliverables",
                       "0.9.0_WK_AMGT_HARVST~4", "securities.json"), encoding="utf-8") as fh:
    pop_a = json.load(fh)
config = json.loads(open(os.path.join("lib", "opal_data_harvest", "config.json"),
                         encoding="utf-8").read())
pop_b = [dict(s, security_key=s["key"]) for s in universe(config)]

rows = [r for r in listing_hit_rows(client()) if r.get("publisher") == "sa"]
rows.sort(key=lambda r: (str(r.get("run_stamp")), int(r.get("search_page") or 0),
                         int(r.get("search_rank") or 0)))

print("AC4 EVIDENCE -- PRESENTED FOR L9, NOT GRADED HERE")
print("sample = EVERY sa listing_hit row in silver. n = %d (denominator = %d)" % (len(rows), len(rows)))
print("populations the matcher is run against: A = 6 gold-builder securities, "
      "B = %d --all-securities universe rows" % len(pop_b))
print("")

by_query = {}
for r in rows:
    by_query.setdefault(r.get("search_query"), []).append(r)
print("rows per source listing page (search_query = the vendor symbol queried):")
for q in sorted(by_query):
    print("  %-8s %d rows  run_stamp=%s  bronze_key=%s"
          % (q, len(by_query[q]), by_query[q][0].get("run_stamp"), by_query[q][0].get("bronze_key")))
print("")

records = []
for r in rows:
    content = r.get("content") or ""
    href_symbols = sorted(set(SYMBOL_HREF.findall(content)))
    a_keys = [s["security_key"] for s in pop_a if _listing_hit_security_match(r, s)]
    b_keys = [s["security_key"] for s in pop_b if _listing_hit_security_match(r, s)]
    b_names = [s.get("company") for s in pop_b if _listing_hit_security_match(r, s)]
    records.append({
        "search_query_vendor_symbol": r.get("search_query"),
        "search_page": r.get("search_page"),
        "search_rank": r.get("search_rank"),
        "article_id": r.get("article_id"),
        "title": r.get("title"),
        "symbols_in_row_content_href": href_symbols,
        "query_symbol_present_in_content": r.get("search_query") in href_symbols,
        "filed_under_population_A": a_keys,
        "filed_under_population_B": b_keys,
        "filed_under_population_B_companies": b_names,
        "fetched_at": str(r.get("fetched_at")),
    })

print("PER-ROW EVIDENCE (vendor symbol | rank | filed-under A | filed-under B | title)")
for rec in records:
    print("  %-6s r%-3s A=%-16s B=%-26s %s"
          % (rec["search_query_vendor_symbol"], rec["search_rank"],
             (",".join(rec["filed_under_population_A"]) or "-"),
             (",".join(rec["filed_under_population_B"]) or "-"),
             (rec["title"] or "")[:72]))
print("")

print("PER-ROW SYMBOL CORROBORATION (does the row's own content link the symbol that was queried?)")
for rec in records:
    print("  %-6s r%-3s content symbols=%-34s query symbol present: %s"
          % (rec["search_query_vendor_symbol"], rec["search_rank"],
             (",".join(rec["symbols_in_row_content_href"])[:34] or "-"),
             rec["query_symbol_present_in_content"]))
print("")

for pop_label, field in (("A", "filed_under_population_A"), ("B", "filed_under_population_B")):
    zero = sum(1 for rec in records if len(rec[field]) == 0)
    one = sum(1 for rec in records if len(rec[field]) == 1)
    many = sum(1 for rec in records if len(rec[field]) > 1)
    print("population %s file-under counts over %d rows: 0 keys %d | exactly 1 key %d | >1 key %d"
          % (pop_label, len(records), zero, one, many))
print("")
print("ALIAS SETS THE MATCHER USED (the reason a row files under a key or under nothing):")
for s in pop_a:
    print("  A %-16s aliases=%r sa_symbol=%r" % (s["security_key"], _security_aliases(s), s.get("sa_symbol")))
for s in pop_b:
    if s.get("sa_symbol") in {"LNVGY", "ASML"}:
        print("  B %-26s company=%-14s aliases=%r sa_symbol=%r"
              % (s["security_key"], s.get("company"), _security_aliases(s), s.get("sa_symbol")))

path = os.path.join(OUT_DIR, "ac4_evidence.json")
with open(path, "w", encoding="utf-8", newline="\n") as fh:
    json.dump({"sample_size": len(records), "denominator": len(records),
               "sample_rule": "every sa listing_hit row in silver (census)",
               "rows": records}, fh, indent=2, sort_keys=True)
print("")
print("wrote %s" % path)
print("NOT GRADED HERE -- AC4 is graded at L9 by 3.0.0_SA_CVO.")
