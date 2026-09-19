# Session log -- `0.9.0_WK_AMGT_RESAPP~49` on `AMGT_RESAPP.TO-AMGT-rk-48.ceo-serp-organizing-agent`

Continuation of slot `~49` after `AMGT-rk-47` (complete, drained @0452b0d140). Worktree
`/c/tmp/wk-amgt-14-49`, branch `wk-amgt-14-49`, fast-forwarded to SITEZ HEAD `bdaf6431a2`
(confirmed with `git rev-parse --short=10 HEAD` as the first act, matching the issuer's note).

## Preflight

- Never-widen pair confirmed on file: `NEVER_WIDEN_ROUND14_CHAIN_E_COO_HALVES.md` (`AMGT-rk-48`
  section at `:110-141`) and `NEVER_WIDEN_ROUND14_CHAIN_E_CTO_HALVES.md` (`AMGT-rk-48` section
  at `:385-393`, withheld `:553-556`, re-signed `:574-578`) both carry `AMGT-rk-48` sections;
  both agree AC1-AC3 are offline (no pair needed) and AC4-AC6 are live ONLY under Andrew's
  Bright Data per-use word.
- Issuer notes on this spawn state that per-use word is NOT on file. Per the order's own closing
  bound ("if the spawn prompt does not state the per-use word ... AC4-AC6 are REFUSED with a row
  and the order is terminal on AC1-AC3 plus that refusal"), AC4-AC6 were REFUSED without any
  Bright Data or other vendor call being made. Row `AMGT_RESAPP-Z-W49-S2` files this.
- No change-management ledger entry was opened: this order's live/write arm (AC4-AC6, the
  served-output rewrite) never ran, so no `--write-pool` act occurred and NEVER-2's "open before
  the first write act" duty never became live.

## What was built (AC1-AC3, offline)

1. **`data/find/dualbiz/scripts/serp.py`**: added the pure classifier `classify_serp_attempt`
   (FAILED/EMPTY/OK per design s.1.5's four measured shapes), `serp_brightdata_records` (the
   structured records primitive with injectable `transport`, retry-only-on-captcha-or-5xx,
   never-on-4xx), a local `_scrub_body` (contact-key scrub with `general.mobile` exempt), and
   `_resolve_wrapper` (one un-followed GET on a `google.com/goto?url=` link). `serp_brightdata`
   is now a thin wrapper delegating to `serp_brightdata_records`, keeping `list[str]` for
   FIND_DUALBIZ's two other callers (`serp_search`, `casec.py:80`) and printing one `WARN:` line
   on FAILED. Lane note: `serp.py` is FIND_DUALBIZ's file; this order's `<paths>` grant covers
   the edit (order text, section 1 step 1).
2. **`lib/research/management/ceo_search.py`** (new): `ceo_profile()` -- the full pipeline
   (query, records, broker-drop, Call A triage, LinkedIn link-only, fetch, contact-scrub, the
   500-character deterministic anchor, Call B extraction, `passages.Locator` verification, dedupe,
   status/reason_code assignment) plus `classify_source_kind`, `identity_anchor`,
   `company_short_name`, `contact_scrub_text`, `dedupe_facts`, `verify_quote`, and
   `project_ceo_public_profile` (the legacy-shape projection). `require_verified_domain=True` is
   the default: no `verified_site` means `NOT_SEARCHED` / `NO_VERIFIED_SITE`, never a guessed
   domain (issuer bind, msg 23833; row `AMGT_RESAPP-Z-W49-S4` records the reading this worker took
   where the order's own step 7 and the issuer bind are in tension).
3. **`lib/research/management/management.schema.json`**: added `ceo_profile` (REQUIRED, new
   closed `ceo_profile_block` definition, the five-state enum, `ceo_fact`/`ceo_search_item`/
   `ceo_search_found_not_read` sub-definitions, the six fact topics with no `other`); kept
   `ceo_public_profile` REQUIRED, renamed its definition to `ceo_public_profile_block` and
   corrected the stale "opaque redirect" claim.
4. **`lib/research/management/enrich.py`**: added `company_display_name()` (prefers the filings
   battery's `entity_name`, falls back to `domains.json`'s declared entity, then the Bloomberg
   yellow-key form) and `verified_domain_for()` (reads `source_object.verified_site.host` ONLY --
   never `domains.json` -- per the issuer bind). `build_document` now calls
   `ceo_search.ceo_profile()` and projects the result onto `ceo_public_profile`; the old
   `ceo_public_profile()` function is retired from the call site (left defined, since
   `test_management.py`'s `CeoProfileTest` class calls it directly and this order does not name
   that class as in scope to rewrite). The `SERP:` print line now prints `ceo_profile`'s status,
   reason_code, name_source, query and cost.
5. **Tests**: `lib/research/management/tests/test_ceo_search.py` (new, 19 tests, all offline/
   stubbed) covers every AC1-named case: the four classify shapes, captcha-retried-exactly-twice
   (3 attempts) / bad-zone-never-retried (1 attempt), EMPTY-with-9-records-flagged, OK-with-title-
   and-snippet, the old-wrapper-matches-records-call check, the MUTANT classifier (captcha ->
   EMPTY) refused by its own discriminating assertion, the namesake/positive-control anchor pair,
   the verbatim control (every kept quote relocates; every drop/swap/splice mutant of it is
   refused, "mutants refused 9 of 9" printed), `official_bio` only on the verified host, the
   planted-contact-string-never-reaches-the-block check, and the `NO_VERIFIED_SITE` gate.
   `test_management.py` and `test_bloomberg_fallback.py` needed one fixture line each (a
   schema-valid minimal `ceo_profile` block via `ceo_search.ceo_profile(None, ...)`) to keep
   passing now that `ceo_profile` is schema-required; both files are back to fully green
   (47 and 7 tests respectively).

## Collateral checked, not fixed (outside `<paths>`)

`lib/research/api/tests/test_generation_and_pool_routes.py` (a WALL) carries 2 pre-existing
failing assertions against `scoped_amgt.ceo_profile_reading`, traced to a stale test fixture
missing the `query` key against the adapter's own already-renamed enum (`AMGT-rk-43` retired
`NOT_CONFIRMED_NOTHING_FOUND` before this order); `scoped_amgt.py` imports neither `enrich.py`
nor `ceo_search.py`, so this is unrelated to this order's edits. Row `AMGT_RESAPP-Z-W49-S3`
records it; not fixed here (`lib/research/api/` is a named WALL).

## AC1-AC3 results (verbatim, this session)

- **AC1**: `python -m unittest lib.research.management.tests.test_ceo_search -v` -- 19 tests,
  ends `OK`, every named case present and passing; `mutants refused 9 of 9`.
- **AC2**: the same classifier through `enrich._serp_module()` -- all 4 measured shapes PASS,
  denominator 4 of 4.
- **AC3**: schema check -- `ceo_profile` required True, `ceo_public_profile` kept required True,
  five-state enum, six fact topics (no `other`), stale redirect claim False, 8 definitions.

## AC4-AC6

REFUSED. No Bright Data or other external vendor API call was made. See row
`AMGT_RESAPP-Z-W49-S2`.

## Commits

See the WORKER REPORT (final message) for hashes; `proof_of_spec.json`'s `artifacts_produced`
rows are pinned to the carrying commit on the follow-up commit per the issuer's instruction.
