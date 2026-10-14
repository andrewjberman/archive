"""c11_harvest.py -- MX-c-9 AC2 / MX-r-12 instrument (FWD-21 re-pinned to list v4, PRD v0.10 item 1).

Usage: python c11_harvest.py <servable-prefix list .md at its v4 pin> <catalog yaml>

THE LIST SIDE: v4's table row "the 24 top-level prefixes" (every backticked `<name>/` on that line, checked to be 24),
plus `amgt/`'s sub-prefixes listed EXPLICITLY (the CVO's carried note, CTO msg 33847): row 12b's seven
`amgt/harvest/gold/` research tables AND `amgt/harvest/bronze/`, `amgt/harvest/silver/`, `amgt/harvest/state/`
(rows 12 and 13), each with its own row. AMENDED A1 at the issuer's cut, before the drain.
THE CATALOG SIDE: the `harvest_datasets:` section. A top-level prefix is COVERED when at least one row's `prefix` starts
with it. Each row carries `bucket: opal-data-harvest`, a `prefix`, and a non-empty `read_tool` or `gap_owner`. The grain
rule from round 10 stands: no row on the whole `amgt/harvest/gold/` prefix, no duplicate prefix, and the six round-10
gold tables are kept.
Read-only; no network.
"""
import re
import sys

lst, cat_path = sys.argv[1], sys.argv[2]
text = open(lst, encoding="utf-8").read()
top = []
for line in text.splitlines():
    if line.startswith("| the 24 top-level prefixes"):
        top = re.findall(r"`([a-z0-9-]+/)`", line)
        break
r12b = []
for line in text.splitlines():
    cells = [c.strip() for c in line.split("|")]
    if len(cells) > 3 and cells[1] == "12b":
        r12b = ["amgt/harvest/gold/%s/" % t for t in re.findall(r"`([a-z_-]+)`", cells[2]) if t not in ("amgt",)]
        break
r12b = [p for p in r12b if not p.endswith("/gold/amgt/")]
AMGT3 = ["amgt/harvest/bronze/", "amgt/harvest/silver/", "amgt/harvest/state/"]
GOLD6 = ["amgt/harvest/gold/%s/" % t for t in ("article_security_mention", "article_sentiment", "chatter_daily",
                                               "chatter_event", "chatter_window", "candidate_universe")]
print("LIST v4 top-level prefixes %d (expect 24); row 12b research tables %d (expect 7)" % (len(top), len(r12b)))

import yaml  # noqa: E402

doc = yaml.safe_load(open(cat_path, encoding="ascii"))
rows = [r for r in (doc.get("harvest_datasets") or []) if isinstance(r, dict)]
prefixes = [str(r.get("prefix") or "") for r in rows]
covered = [t for t in top if any(p.startswith(t) for p in prefixes)]
r12b_rowed = [p for p in r12b if p in prefixes]
gold6_kept = [p for p in GOLD6 if p in prefixes]
amgt3_rowed = [p for p in AMGT3 if p in prefixes]
bad_bucket = sum(1 for r in rows if str(r.get("bucket") or "") != "opal-data-harvest")
no_reader = sum(1 for r in rows if not (str(r.get("read_tool") or "").strip() or str(r.get("gap_owner") or "").strip()))
whole_gold = sum(1 for p in prefixes if p.rstrip("/") == "amgt/harvest/gold")
dups = len(prefixes) - len(set(prefixes))
outside = [p for p in prefixes if not any(p.startswith(t) for t in top)]
print("CATALOG harvest rows %d; top-level prefixes covered %d of %d; research tables rowed %d of %d; "
      "round-10 gold tables kept %d of 6; amgt bronze/silver/state rowed %d of 3; whole gold prefix %d; "
      "duplicate prefixes %d; rows outside the 24 %d; rows with neither read_tool nor gap_owner %d; "
      "rows not on opal-data-harvest %d"
      % (len(rows), len(covered), len(top), len(r12b_rowed), len(r12b), len(gold6_kept), len(amgt3_rowed),
         whole_gold, dups, len(outside), no_reader, bad_bucket))
for t in top:
    if t not in covered:
        print("  UNCOVERED %s" % t)
for p in r12b + AMGT3:
    if p not in prefixes:
        print("  UNROWED %s" % p)
ok = (len(top) == 24 and len(r12b) == 7 and len(covered) == 24 and len(r12b_rowed) == 7 and len(gold6_kept) == 6
      and len(amgt3_rowed) == 3
      and not whole_gold and not dups and not outside and not no_reader and not bad_bucket)
sys.exit(0 if ok else 1)
