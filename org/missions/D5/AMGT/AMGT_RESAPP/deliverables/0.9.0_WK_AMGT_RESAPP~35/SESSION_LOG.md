# AMGT-rk-31 session log -- `0.9.0_WK_AMGT_RESAPP~35`

Worktree `/c/tmp/wk-amgt-14-35`, branch `wk-amgt-14-35`, cut from SITEZ @`047aee5478`.
2026-09-19, round 14, chain I, order 1 of 1 (entry cell).

1. **The bar.** `git rev-parse --abbrev-ref HEAD` -> `wk-amgt-14-35`; `org/`, `.tools/`,
   `lib/research/identity/`, `integrations/bloomberg/mcp/blp_client.py` all present. TREE-OK.
2. **Re-grounded the premises.** Read both never-widen halves
   (`NEVER_WIDEN_ROUND14_CHAIN_I_{COO,CTO}_HALVES.md`); both carry an `AMGT-rk-31` section naming
   `crosswalk/v1/<as_of>.json` and `raw/bloomberg/<KEY>/` as blast radius + rollback; sha256
   recorded. Confirmed `add_security.py` absent, `registrations.json` absent (CTO half's own
   finding). Read `crosswalk.py`, `build_universe.py`, `resolver.py`,
   `integrations/bloomberg/mcp/blp_client.py`, `integrations/bloomberg/research/model_block_pull.py`
   (the raw-landing family), `lib/research/filings/fetch.py:64` (the `CIK%010d` padding rule),
   `crosswalk.schema.json`, `test_crosswalk.py`. Ran AC1: 89 records, 33 MEASURED, 4 unregistered
   (Alphabet GOOGL US, Eli Lilly LLY US, Quanta Services PWR, UnitedHealth Group UNH US) --
   matches the analysis exactly. Confirmed Bloomberg DAPI health `ok: true` before any call.
3. **Built** `crosswalk.py` additions (`registrations_path()`, `load_registrations()`,
   `_record_for_registration()`, `build_crosswalk()`'s second input, registered so the existing
   34-arm fixture suite is unaffected -- registrations default to empty when `coverage_doc` is
   passed explicitly, mirroring the `pilots` convention). Extended `crosswalk.schema.json` with
   OPTIONAL `identity`, nullable `source_row.folder`, `registrations_source`,
   `denominators.registered` -- verified the LIVE `crosswalk/v1/2026-09-15.json` still validates
   against the updated schema before writing any code against it.
4. **Built** `add_security.py`: `--bloomberg`/`--folder`/`--as-of`/`--dry-run`|`--write-pool`.
   Idempotency (match by folder or bloomberg field, no call, no write) and the security_key
   collision refusal (built via `crosswalk.build_crosswalk()` against local disk state, before any
   Bloomberg call) both happen before any vendor call. `--write-pool` refuses any `--as-of` that
   is not today UTC, checked first, before any local or vendor work.
5. **Bug caught by AC2's own literal expectation**: first cut computed `sec_id` as
   `"CIK%010d" % cik` (carrying the literal "CIK" prefix, matching `fetch.py`'s URL-filename
   template); AC2's expected value is `'0000018230'`, no prefix. Fixed `_cik_and_sec_id()` to
   `"%010d" % cik`; re-ran AC2, matched exactly. One extra Bloomberg call spent on the re-run
   (recorded, ceiling unaffected: 6 of 9 used at the cut).
6. **Wrote 12 new unit arms** (`test_add_security.py`): registration record shape with/without a
   folder, the planted vendor error -> UNRESOLVED no key no write, the collision refused before
   any write (no Bloomberg call), idempotent re-registration, and the pre-existing (2026-09-15)
   shape plus a registration-bearing shape both validating against `crosswalk.schema.json`. 41 of
   41 total unit arms pass.
7. **Opened** the change-management ledger (`deploy_ledger.py open`, slug
   `amgt-rk-31-add-security`, 3 legs) BEFORE the first `--write-pool`; pasted both never-widen
   halves' sha256 and the fresh pre-act census (crosswalk/v1/ = 1 key = 2026-09-15.json; all three
   raw prefixes 404) into the entry's log.
8. **Ran AC8 (before AC4):** planted `--as-of 2026-09-15` and `--as-of 2099-01-01` under
   `--write-pool` -- both refuse (rc 3), POST census identical to PRE (etags_unchanged,
   keys_unchanged).
9. **Ran AC2, AC3** (dry runs, CAT US MEASURED / ZZZZQQ US UNRESOLVED, nothing written both times).
10. **Ran AC4:** three `--write-pool` registrations (CAT US, CSL AU, 6861 JP). 6861 JP's
    `CENTRAL_INDEX_KEY_NUMBER` came back `BAD_FLD/NOT_APPLICABLE_TO_REF_DATA` (Keyence has no US
    CIK) -- recorded verbatim in `field_errors`, `cik`/`sec_id` both `None`, never guessed. Newest
    crosswalk `crosswalk/v1/2026-09-19.json`, MEASURED 33+3=36. Every validation-name form resolves
    correctly (`CAT US`, `CSL AU`, `6861 JP`, `CAT US Equity`, `CAT_US_Equity`).
11. **Ran AC5:** all four unregistered folders auto-discovered via `--folder`; none carries a ONE
    PAGER workbook (re-measured, matches AC1), so all four register UNRESOLVED, rc 0, no Bloomberg
    call. `unregistered_after` 0 of 93.
12. **Ran AC6:** base `2026-09-15.json` (89 records) untouched; `base_records_byte_identical_in_newest`
    89 of 89; newest carries 96 records (89 + 7 registrations), MEASURED 36, registered 7.
13. **Ran AC8 (after AC6):** same two planted dates, still refuse (rc 3), POST census identical.
14. **Ran AC7:** unit suite 41/41; crosswalk CLI dry run fixed-point True twice, ascii True.
15. Committed code + tests + schema + registrations.json + ledger-open state (`0add9d26c1`).
    Closed ledger legs L1 (commit hash), L2 (write_pool receipt), L3 (AC6 line); closed the
    entry. Built the mutant control: a MEASURED registration record with `security_key` forced
    `null` -- schema REFUSES it, unmutated document validates (FIRED-AS-EXPECTED).
16. Wrote this proof instance, flipped `<status>` to `complete`, committed.

**Bounds honoured.** Vendor calls: Bloomberg `reference_data` only, 6 calls total against a
ceiling of 9 (AC2 x2 -- one bad cut, one fix re-run -- AC3 x1, AC4 x3, AC5 x0 -- no workbook found
for any of the four folders). No `historical_data`. No web/Seeking Alpha/Lusha. No fleet re-run of
the 33. No downstream stage touched (no model block pull, no battery, no `universe/v1` write).
COLLECTION STAYS OFF; no alarm/monitor/SNS/SES built. Never pushed.
