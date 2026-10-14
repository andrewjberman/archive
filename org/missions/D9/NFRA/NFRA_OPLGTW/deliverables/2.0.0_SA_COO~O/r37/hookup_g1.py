# -*- coding: utf-8 -*-
"""The issuer's hookup commit for the ten G1 typed harvest tools (OG-gt-1..gt-4). Usage: python hookup_g1.py <gateway-root> [--check]"""
import sys

GW = sys.argv[1].rstrip("/")
APP, TESTS = GW + "/app/", GW + "/tests/"

# (module alias, module file, tool name, signature, call args, audit args)
TOOLS = [
    ("_hvi", "harvest_resolve_security", "query: str", "query", '{"query": query[:64]}',
     "Resolve a ticker, Bloomberg ticker, security_key, company name, CIK, ISIN or SEDOL to the harvest security_key (status exact | candidates | none | not_held; a CUSIP answers not_held)."),
    ("_hvi", "harvest_security_coverage", "security_key: str", "security_key", '{"security_key": security_key}',
     "What the harvest bucket holds on one resolved security and how fresh each dataset is, in trading days behind T-1."),
    ("_hvp", "harvest_get_chatter", "security_key: str, from_day: str, to_day: str", "security_key, from_day, to_day", '{"security_key": security_key}',
     "Press chatter for one security over a day range: daily rows with data_status (0 articles is not 'no chatter'), 30/90/365-day windows, events. Newest part of the newest date partition only."),
    ("_hvp", "harvest_search_articles",
     "security_key: str, publisher: str = None, from_day: str = None, to_day: str = None, min_tier: str = None, in_title: bool = False, limit: int = 25",
     "security_key, publisher, from_day, to_day, min_tier, in_title, limit", '{"security_key": security_key}',
     "Articles mentioning one security, newest first, with sentiment, title, url and words (limit 25 default, 100 max)."),
    ("_hvp", "harvest_get_article", "article_key: str, publisher: str, include_text: bool = False", "article_key, publisher, include_text",
     '{"article_key": article_key[:128], "publisher": publisher}',
     "One article by key and publisher; the text only when include_text is true."),
    ("_hvf", "harvest_get_fundamentals", "security_key: str, kind: str, mnemonics: list = None, fiscal_years: list = None",
     "security_key, kind, mnemonics, fiscal_years", '{"security_key": security_key, "kind": kind}',
     "Fundamentals for one security: kind is model | consensus | reference | valuation_history | segments | price."),
    ("_hvf", "harvest_query_columns",
     "dataset: str, columns: list, security_keys: list = None, filters: list = None, order_by: str = None, limit: int = 50",
     "dataset, columns, security_keys, filters, order_by, limit", '{"dataset": dataset}',
     "Projected rows of one allow-listed tabular dataset (declared columns only; filters = [{column, op, value}], op in = < > in; limit 50 default, 200 max)."),
    ("_hvr", "harvest_get_research", "security_key: str, as_of: str = None, fields: list = None", "security_key, as_of, fields", '{"security_key": security_key}',
     "Our research on one security: dossier fields with citations, continuation thesis, ai_fill blocks, research reports, management roster."),
    ("_hvr", "harvest_get_filing_analysis", "security_key: str, accession: str = None, include_passages: bool = False", "security_key, accession, include_passages",
     '{"security_key": security_key}', "The analysed latest (or named) filing for one security: guidance, segments, risks, commentary, big bets, big challenges, with citations."),
    ("_hvr", "harvest_get_peers_and_scores", "security_key: str", "security_key", '{"security_key": security_key}',
     "Peers, divergence / peers_v / robustness scores and our posture (verdict, books, weight by book) for one security."),
]
NAMES = [t[1] for t in TOOLS]


def edit(path, old, new, count=1):
    s = open(path, encoding="utf-8").read()
    assert s.count(old) == count, "%s: %r found %d times" % (path, old[:60], s.count(old))
    open(path, "w", encoding="utf-8", newline="").write(s.replace(old, new))


# 1. tools.py: the import and the ten registrations, after harvest_read's
edit(APP + "tools.py",
     "from . import harvest_read as _hv   # NFRA_OPLGTW OG-hv-1: the tool names harvest_list/harvest_read are this module's",
     "from . import harvest_read as _hv   # NFRA_OPLGTW OG-hv-1: the tool names harvest_list/harvest_read are this module's\n"
     "from . import harvest_identity as _hvi, harvest_press as _hvp, harvest_figures as _hvf, harvest_research as _hvr   # NFRA_OPLGTW G1-TYPED (FWD-22)")
blk = ["", "# NFRA_OPLGTW G1-TYPED (round 37, FWD-22): ten typed READ tools over s3://opal-data-harvest, Opal principals only. Each admits through",
       "# app/harvest_typed.admit_typed BEFORE any S3 call and answers with as_of, source_keys, a denominator and absent_reason."]
for mod, name, sig, call, audit, doc in TOOLS:
    blk += ["@mcp.tool()", "def %s(%s) -> dict:" % (name, sig), '    """%s"""' % doc,
            '    return _run("%s", %s, lambda t: %s.%s(%s))' % (name, audit, mod, name, call.replace("from_day", "from_day").replace("to_day", "to_day")), "", ""]
anchor = '    return _run("harvest_read", {"key": key}, lambda t: _hv.harvest_read(key))\n\n\n'
edit(APP + "tools.py", anchor, anchor + "\n".join(blk[1:]).rstrip("\n") + "\n\n\n")
# 2. the two name lists
names_txt = ", ".join('"%s"' % n for n in NAMES)
edit(APP + "data_entitlement.py", '    "harvest_list", "harvest_read",   # OG-hv-1 (round-37 R4), read class, legacy (NOT DATA_GRANT_TOOLS): Opal principals only\n',
     '    "harvest_list", "harvest_read",   # OG-hv-1 (round-37 R4), read class, legacy (NOT DATA_GRANT_TOOLS): Opal principals only\n'
     + "".join('    "%s",\n' % n for n in NAMES).replace('",\n', '",   # NFRA_OPLGTW G1-TYPED (FWD-22), read class, legacy: Opal principals only\n', 1))
edit(APP + "destructive_ops.py", '    "harvest_list", "harvest_read",   # NFRA_OPLGTW OG-hv-1 (round-37 R4): READ-ONLY ListObjectsV2 + one capped GetObject on\n'
     '                                # s3://opal-data-harvest under 24 served prefixes, Opal principals only; no write, no send.\n',
     '    "harvest_list", "harvest_read",   # NFRA_OPLGTW OG-hv-1 (round-37 R4): READ-ONLY ListObjectsV2 + one capped GetObject on\n'
     '                                # s3://opal-data-harvest under 24 served prefixes, Opal principals only; no write, no send.\n'
     + "".join('    "%s",\n' % n for n in NAMES).replace('",\n', '",   # NFRA_OPLGTW G1-TYPED (FWD-22): READ-ONLY typed reads over the harvest bucket, Opal principals only\n', 1))
# 3. the pinned counts
edit(TESTS + "test_entitlement_admin.py", "    assert len(registered_tool_names) == 65", "    assert len(registered_tool_names) == 75")
edit(TESTS + "test_entitlement_admin.py", "+ OG-hv-1's harvest_list and harvest_read (round-37 R4, read class): 65.",
     "+ OG-hv-1's harvest_list and harvest_read (round-37 R4, read class): 65, + the ten G1 typed harvest tools (G1-TYPED, FWD-22): 75.")
edit(TESTS + "test_data_entitlement_family.py", "assert len(non_data) == 56 and", "assert len(non_data) == 66 and")
s = open(TESTS + "test_data_entitlement_family.py", encoding="utf-8").read()
s = s.replace("# discovery: all 56 non-data tools", "# discovery: all 66 non-data tools").replace("the profile denies none of the 56", "the profile denies none of the 66")
open(TESTS + "test_data_entitlement_family.py", "w", encoding="utf-8", newline="").write(s)
print("hookup applied: %d tools" % len(NAMES))
