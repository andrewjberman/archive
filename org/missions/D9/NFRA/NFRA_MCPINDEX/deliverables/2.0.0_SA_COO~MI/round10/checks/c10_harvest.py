"""c10_harvest.py -- MX-c-8 AC2 instrument (FWD-21): the catalog's harvest rows against the servable-prefix list v3.

Usage: python c10_harvest.py <servable-prefix list .md> <catalog yaml>

THE LIST SIDE is parsed from the list's "The 24 prefixes" table: a row is SERVE-NOW when its V1 cell starts with
"**SERVE" (row 3's "WITHHOLD until the view exists" is not). Its prefixes are the backticked tokens of its prefix cell;
row 8's are its six table names under amgt/harvest/gold/ (never the whole gold prefix); every other row's is its FIRST
backticked token (row 22 also names its sub-folders `model_block/`, `model_block_fye/`, which `derived/` covers). The parse is checked against
the list's own count line (11 SERVE now) and against the 16 prefixes written out in its grant section.

THE CATALOG SIDE is the `harvest_datasets:` section: one mapping per prefix with `bucket: opal-data-harvest`, `prefix`,
and either a non-empty `read_tool` or a non-empty `gap_owner`.
Read-only; no network.
"""
import re
import sys

lst, cat_path = sys.argv[1], sys.argv[2]
text = open(lst, encoding="utf-8").read()
GRANT16 = ["packs/", "filings/v1/", "posture/v1/", "publication-links/v1/", "identity/v1/", "crosswalk/v1/",
           "universe/v1/", "scores/v1/", "peers/v1/", "derived/"]
GOLD6 = ["article_security_mention", "article_sentiment", "chatter_daily", "chatter_event", "chatter_window",
         "candidate_universe"]
GRANT16 += ["amgt/harvest/gold/%s/" % t for t in GOLD6]

serve_rows, want = 0, set()
for line in text.splitlines():
    cells = [c.strip() for c in line.split("|")]
    if len(cells) < 7 or not re.fullmatch(r"\d+b?", cells[1] or ""):
        continue
    if not cells[5].startswith("**SERVE"):
        continue
    serve_rows += 1
    if cells[2].startswith("`amgt/harvest/gold/`"):
        want |= {"amgt/harvest/gold/%s/" % t for t in re.findall(r"`([a-z_]+)`", cells[2])}
    else:
        want |= set(re.findall(r"`([^`]+/)`", cells[2])[:1])   # the row's prefix; later tokens (row 22) are its sub-folders
parse_ok = serve_rows == 11 and want == set(GRANT16)
print("LIST SERVE-NOW rows %d (list says 11); prefixes %d (grant section names %d); parse agrees with grant section: %s"
      % (serve_rows, len(want), len(GRANT16), parse_ok))

import yaml  # noqa: E402

doc = yaml.safe_load(open(cat_path, encoding="ascii"))
rows = [r for r in (doc.get("harvest_datasets") or []) if isinstance(r, dict)]
got, bad_bucket, no_reader, whole_gold, extra = {}, 0, 0, 0, []
for r in rows:
    p = str(r.get("prefix") or "")
    if str(r.get("bucket") or "") != "opal-data-harvest":
        bad_bucket += 1
    if not (str(r.get("read_tool") or "").strip() or str(r.get("gap_owner") or "").strip()):
        no_reader += 1
    if p.rstrip("/") == "amgt/harvest/gold":
        whole_gold += 1
    if p in want:
        got[p] = got.get(p, 0) + 1
    else:
        extra.append(p or "<none>")
covered = len(got)
dups = sum(1 for v in got.values() if v > 1)
print("CATALOG harvest rows %d; SERVE prefixes rowed %d of %d; rows on a prefix not SERVE-NOW %d %s; whole gold prefix %d; "
      "duplicate prefixes %d; rows with neither read_tool nor gap_owner %d; rows not on opal-data-harvest %d"
      % (len(rows), covered, len(want), len(extra), extra[:6], whole_gold, dups, no_reader, bad_bucket))
for p in sorted(want - set(got)):
    print("  UNROWED %s" % p)
ok = parse_ok and covered == len(want) and not extra and not whole_gold and not dups and not no_reader and not bad_bucket
sys.exit(0 if ok else 1)
