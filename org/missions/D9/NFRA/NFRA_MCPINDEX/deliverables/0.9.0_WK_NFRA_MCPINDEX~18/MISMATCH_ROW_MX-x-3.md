# MISMATCH_ROW MX-x-3 (live run, read-only, opal-data-portal-v2)

SUMMARY: {"rows": 36, "concrete_ok": 26, "concrete_missing": 0, "family_ok": 9, "family_mismatch_or_error": 1}
ROW: mp.15.json-mdpf-legacy | STATE: FAMILY-EMPTY | CAUSE: DENY row key json/mdpf/** (declared OPEN); list-objects-v2 prefix json/mdpf/ returns 0 keys (measured; json/ top-level prefixes list 20 dirs, none mdpf), so the DENY is about a key tree that does not exist
