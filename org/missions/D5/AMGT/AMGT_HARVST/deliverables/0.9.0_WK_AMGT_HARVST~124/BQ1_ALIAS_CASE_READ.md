TODAY: YES -- a lower-case common word ("target") pairs with a security (TGT_US_Equity) whose alias list holds "Target"; nothing was repaired.
Arm (i) lower-case "target", title + 3 blocks, no "Target"/"TGT": mention_count=4, match_forms=['Target'], blocks_hit=3 (pair made).
Arm (ii) lower-case "tgt" only: mention_count=0, match_forms=[] (ticker form is stored-case, not paired).
Arm (iii) capitalised "Target": mention_count=4, match_forms=['Target'] (fixture live).
Deciding code, lib/research/harvest/publication_gold.py:
- _alias_pattern L127 (re.I) and _span_pattern L131 (alias alternatives wrapped in scoped (?i:), exact/ticker forms unflagged).
- _match_counts L152 (counts spans from that pattern).
- _security_exact_aliases L178 (ticker_aliases -> case-sensitive forms).
- _security_mentions L213: the stored-case branch `if not security.get("aliases")` applies only to a security with NO alias list; this one has aliases, so it keeps the case-insensitive path.
Test: lib/research/harvest/tests/test_bq1_alias_case_read.py (asserts the observed outcomes of (i), (ii), (iii)).
