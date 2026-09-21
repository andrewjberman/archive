# AMGT_RESAPP rk-72 (R18-C) -- session log, `0.9.0_WK_AMGT_RESAPP~72`

Worktree `C:/tmp/wk-amgt-18-72`, branch `wk-amgt-18-72`, spawned at HEAD `154cb8e5c4`.

1. Bar: `git rev-parse --abbrev-ref HEAD` -> `wk-amgt-18-72`; `org/`, `.tools/` present -> TREE-OK.
2. Read the task order top-down to the RECORD FACE marker. Read the never-widen pair
   (`ledger/NEVER_WIDEN_ROUND18_R18C_CSL_POOL_HALVES.md`) -- both halves signed (COO at issuance, CTO
   @154cb8e5c4, ruling the RESOLVED branch's delete-only rollback ACCEPTED with no added gate).
3. Re-measured the section-1 baseline live: `git diff 4a2f054389 HEAD -- lib/research/filings` empty;
   `battery.py` 1256 lines; `test_battery.py` 295 lines; suite baselines 16 (test_battery.py) / 73 (whole
   `lib/research/filings/tests`) -- both reproduced exactly before any edit.
4. Measured the ASX listing-page template live: `GET https://www.asx.com.au/markets/company/CSL` -> HTTP
   200, 137427 bytes (via `fetch.http_get`, no UA/TLS variation). No link on that page's own HTML names
   `csl.com.au` or `investors.csl.com` (checked before coding, so the crawl's own host-allow rule --
   unchanged by this cell -- is what would ever reach the issuer from an ASX-discovered link, not a
   hand-typed seed).
5. Built `EXCHANGE_LISTING_PAGES` (`{"AU": "https://www.asx.com.au/markets/company/{ticker_root}"}`) and
   `_exchange_listing_seed(keys)` in `battery.py`; extended `_step4_company_site` to append the exchange
   seed after `web_address` and `prior_seeds`, de-duplicated, with a `seed_sources` list (url + source
   label) carried on every step-4 `_attempt`; `main()` now prints `seeds=[...]` on the step-4 line when
   `seed_sources` is non-empty. `verified_site` is now computed against
   `_exchange_listing_registrable_domains()` -- a win on an exchange-registrable host sets `verified_site`
   to `None` with a named reason instead of `winning-document-host`.
6. Wrote six new stubbed arms in `test_battery.py` (`TheExchangeListingSeedRuleArm`,
   `TheExchangeSeedOrderArm`, `TheHeadCopyDiscriminatorArm`, `TheUnreachableBloombergSeedArm`,
   `TheExchangeHostedWinArm`, `TheBothSeedsFailArm`) -- 22 of 22 passing in `test_battery.py`, 79 of 79
   across `lib/research/filings/tests`.
7. Correction mid-build: the first draft of the `TheUnreachableBloombergSeedArm`/`TheExchangeHostedWinArm`
   fixture used a literal `U+2019` glyph in a source string instead of the `\u2019` ASCII escape
   `document.py` itself uses for the same character -- caught by AC6 (`test_battery.py` non_ascii_bytes 2
   vs base 0), fixed by building the character with `chr(0x2019)` at runtime instead of any escape text in
   the file (avoids a tool-layer JSON-unescape quirk that converts a literal `\uXXXX` in a parameter into
   the real glyph on write). Re-verified AC6 at 0/0 for both files after the fix.
8. Committed the code (`battery.py`, `test_battery.py`) alone: `a486c3854b39cd4c4b8afbacb5d9779612fb9650`.
9. Ran AC1-AC6 literally (see the proof-of-spec instance for every invocation and output verbatim).
   AC4/AC5 ran live against the ASX and (AC5 only) `www.csl.com.au`; the web_address seed failed with a
   connection reset matching `AMGT_RESAPP-Z-W40-S1`'s own symptom, the exchange seed answered (200) but the
   crawl's 40-page bound was reached on ASX's own generic investor-education pages before any candidate
   document was found -- UNRESOLVED-SOURCE BY DESIGN, both seeds logged with their source labels, steps
   1-3 matching the committed rk-38 record verbatim.
10. Filed surprise row `AMGT_RESAPP-Z-W72-S1`: AC3's own literal derivation script (order section 5) never
    extracts a `domicile` key, so AC4's step 5 prints "no adapter for jurisdiction UNKNOWN" rather than
    matching the rk-38 record's "...for AU" verbatim -- confined to step 5's free-text reason, no test
    outcome changes.
11. Mutant control: `_exchange_listing_seed` mutated to always return `(None, "MUTANT-AC-CONTROL...")` ->
    5 of the 6 new tests FAIL as expected (the 6th, the HEAD-copy discriminator, is independent of live
    code by design and correctly does not fire). Reverted; `git diff --stat` on `battery.py` empty after
    revert; full suite re-run at 79 passed.
12. Determinism control: two independent live battery runs against fresh cache directories
    (`.scratch/r72/battery` and `.scratch/r72/battery_det2`) -- the only differing field between the two
    resulting source objects is `retrieved_at`; every other field, including the full `battery.attempts`
    block and `verified_site`/`verified_site_reason`, is identical.
13. AC5: ran `--write-pool` from AC4's step cache (confirmed via step-file mtimes, unchanged by the
    `--write-pool` run) -- one upload, `filings/v1/CSL_AU_Equity/UNRESOLVED-SOURCE.source.json`, sha256
    `c9224976d64e1dce695ca28a8970436d7d0b6e0ddfd1339398252566dbe091f4`, ContentLength 4488 (overwriting the
    pre-act placeholder named in the never-widen pair's before-state, per the UNRESOLVED branch).
14. Wrote this deliverable and the proof-of-spec instance; graded it with this worktree's own
    `.tools/proof-of-spec-check.py`; flipped the task order's `<status>` to `complete`; committed
    deliverable + investigation row + status flip together.
