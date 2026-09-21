# Session log -- `0.9.0_WK_AMGT_RESAPP~71` on `AMGT_RESAPP.TO-AMGT-rk-48.live-ceo-search-validation-names`

Worktree `C:/tmp/wk-amgt-da-71`, branch `wk-amgt-da-71`, based at `71f9a1e027`. Bar check: `git rev-parse
--abbrev-ref HEAD` -> `wk-amgt-da-71`; `test -d org && test -d .tools` -> `TREE-OK`.

## AC1 -- read-only baseline (PASS)
Ran the order's own invocation. `word_record_at_HEAD True` (Andrew's Bright Data per-use word record on
file). All 3 pre-act versions matched the issuer's measurement exactly: CAT `PO0KN5ZWaAmK28_drCI9dXxmmYC5Qx1T`,
CSL `pNV1.QMgs9tdvbuVCa4ifuzP4K.UKKIX`, 6861 `ntH46iAfkv1Je.AMZA0LIXbDeyJCNm80`; `objects_under_prefix 1` for
each. Pre-act bytes saved to `.scratch/rk48_pre/*.json` with sha256 printed (rollback baseline).
`POOL_BASELINE objects 3 newest management/v1/_pool/2026-09-19.json etag "7a1197377a0fff0e4e861ebc5208cf4a"`.
No STOP condition triggered.

## AC2 -- open deploy ledger (PASS)
`python .tools/deploy_ledger.py open --slug amgt-rk48-live-ceo-search ...` before any live write. Entry
opened at `org/critical_paths/change_management/20260921T1623Z_amgt-rk48-live-ceo-search_deploy_completion.md`,
leg `L1` OPEN. Ran strictly after AC1 and before AC3.

## AC3 -- live search (PASS)
Exported `BRIGHT_DATA_API_KEY` and `ANTHROPIC_API_KEY` via `comp-secrets get ... --reveal --value-only`
(bare value, not the four-line descriptor idiom behind row W50-S4); both non-empty, values never printed.
`as_of` pinned to `2026-09-19` (rk-47's dated keys, not a today-dated run). Ran `enrich.main` for the three
validation names, `--write-pool --skip-pool`. RC 0 for all three. All three read `NOT_SEARCHED` (one of the
five PRD-ratified states -- confirmed by direct read of `lib.research.management.ceo_search`:
`STATUS_NOT_SEARCHED == "NOT_SEARCHED"`), each with a `reason_code`: CAT `NO_CEO_ON_ROSTER` (roster resolved,
1 officer, not identified as CEO), CSL `NO_VERIFIED_SITE` (`domains.json` declares no domain for CSL,
consistent with the order's own bind that the domain must come from the filings battery's verified_site,
never `domains.json`), 6861/Keyence `NO_CEO_ON_ROSTER` (roster carries 1 officer, no CEO identified --
explicitly named as an honest allowed outcome by the order's own AC3 text). `TOTALS serp_attempts 0 of cap 9
| model_usd 0.0 of cap 2.00` -- no cap breach, no name outside the three. No secret value appears anywhere
in the captured output (verified by reading `.scratch/rk48_ac3.txt` back -- only the command text and result
fields are present).

**Surprise filed (AMGT_RESAPP-Z-W71-S1):** the signed COO half's EXPECTED OUTCOME text states a name with no
verified_site reads "`NOT_ATTEMPTED` / `NO_VERIFIED_SITE`, nothing searched, **nothing rewritten for it**".
Measured: the literal token `NOT_ATTEMPTED` occurs nowhere in the codebase (`comp-find "NOT_ATTEMPTED"
lib/research/management/` -> 0 hits across 19 files); the real ratified token is `NOT_SEARCHED`
(`ceo_search.STATUS_NOT_SEARCHED == "NOT_SEARCHED"`, matching the PRD's own ratified state list at
`AMGT_RESAPP_PRD.md:748`). And contrary to "nothing rewritten for it", AC4's read-back shows all three
objects WERE rewritten (`rewritten True`) -- because rk-47's pre-act objects carried no `ceo_profile` field
at all, so adding one (even with status `NOT_SEARCHED`) is a genuine non-identical byte change under
`crosswalk.write_pool`'s write-if-changed rule (the CTO half's own gap-3 analysis, section 3). Separately,
the CTO half's section 3 predicted the domain-verification gate (branch 2, `NO_VERIFIED_SITE`) would fire
FIRST on all three names; in practice two of three (CAT, 6861) hit an earlier, unnamed gate
(`NO_CEO_ON_ROSTER` -- no CEO identified on the filed roster at all) before the domain check was ever
reached. None of this changed the mechanical grading of AC3/AC4 (both criteria's literal texts accommodate
either outcome and neither forces a rollback), but the world differs from what the signed pair asserted.

## AC4 -- read-back verification (PASS, no rollback)
Read back all 3 objects via `get_object` + `enrich.validate()`. `dated_objects` EXACTLY
`["2026-09-19.json"]` for each (no `2026-09-21.json` key created -- pinned `as_of` held). `schema_valid True`
with no errors on all 3. `rewritten True` for all 3 (see surprise above -- a genuine, non-identical byte
change, consistent with `crosswalk.write_pool`'s rule). `POOL objects 3 newest
management/v1/_pool/2026-09-19.json etag "7a1197377a0fff0e4e861ebc5208cf4a"` -- EQUAL to AC1's
POOL_BASELINE (`_pool/` untouched, `--skip-pool` held). `facts with quote and char_range 0 of 0` (explicitly
reported, no facts existed since nothing was searched). `contact fields stored 0`. No rollback-branch
condition fired (schema_valid True on all 3, 0 contact fields, no new dated key, pool unmoved, no cap
breach) -- rollback NOT exercised.

## AC5 -- close ledger (PASS)
`deploy_ledger.py close-leg --leg-id L1 --proof "$(cat .scratch/rk48_ac4.txt)"` then `close` then `check`.
Leg L1 closed with AC4's read-back as its proof; entry CLOSED, sentinel removed. `check` output lists no
entry for `amgt-rk48-live-ceo-search` (other listed entries are pre-existing, unrelated open items with
their own owners).

## Rollback
Not fired. No branch required it.

## Summary
AC1-AC5 all PASS-by-output. Zero SERP attempts, $0.00 model spend (all three names resolved NOT_SEARCHED
before any vendor call was needed -- roster/domain gates fired first), zero contact fields stored, `_pool/`
untouched, no new dated key. One surprise row filed (AMGT_RESAPP-Z-W71-S1, OBSERVATION/INERT) on the
signed pair's "nothing rewritten" / `NOT_ATTEMPTED` token mismatch against measured reality.
