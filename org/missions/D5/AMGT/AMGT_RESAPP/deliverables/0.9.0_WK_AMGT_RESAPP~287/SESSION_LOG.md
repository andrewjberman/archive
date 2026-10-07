# 0.9.0_WK_AMGT_RESAPP~287 -- AMGT-ba-25 session log

- Built research_pulls.py, research_pull_fields.json, test_research_pulls.py; added "segments" to BRONZE_REQUESTS.
- Code commit b18a66387672b0661dfc943467785b50c0323336. 20 tests on fakes pass; AC1-AC3 PASS.
- Live store reads (no Bloomberg call): plan officers = 86 names / 86 calls; plan segments = 83 names / 83 calls.
- Rows: AMGT_RESAPP-Z-W287-S1 (86 vs the order's 84), AMGT_RESAPP-Z-W287-S2 (no segment mnemonic in the repo).
- No Bloomberg call, no session to 127.0.0.1:8194, no schtasks read, no AWS write.
