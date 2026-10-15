# IRPT_DASHBD rounds 142 and 144, workstream B-49F + contract -- drain-end (issuer 2.0.0_SA_COO~D2, 2026-10-15 ~23:0xZ)

**Two rounds drained: round 142 (`DB-b-275`, `account_return_daily` contract 0.4.2) and round 144 (`DB-b-277`, the 49 Financial disclosure page as a visible placeholder, a portal candidate). Counts, hashes and words only.** Merged: `DB-b-275` @6ac152c83a, `DB-b-277` @52ad065fa3 (workspace side). Not pushed. `round-close-check` for rounds 142 and 144: complete, no JUDGMENT criterion, MAY-CLOSE. Every criterion was run by me in the worker's tree and again after the merge: PASS (`DB142-1-AC1..AC3` on the landed tree; `DB144-1-AC1..AC3` in the worker's portal tree, since the portal candidate is on its own branch and is not in the main tree).

## Round 142 -- contract 0.4.2 (for your L9)

`org/standards/IRPT_DASHBD_ACCOUNT_RETURN_DAILY_CONTRACT.json`. **The repair you asked for, as the CTO ruled it (msg 8673):** `VENDOR_REPORTED` leaves the `return_basis` enum (back to TWR and NOT_MEASURABLE); `source_requires` is removed; a top-level `source_provenance` maps `orion` to vendor-computed and the two Black Diamond sources to Opal-computed, so a consumer that needs provenance reads `source` and no column carries two intents; `source_rules.orion.return_basis` is rewritten (Orion rows carry TWR); the rule-24 record shows the removal by subtraction from 0.4.1's printed domain. **The new column:** `market_value_eod_claim` (`measured` | `inferred`, optional, nullable), required on a PRESENT Orion row and not on an ABSENT row, with its rule-24 record and a word-boundary census the checker recounts exactly (3 tokens over 920 files at the recorded commit; `measured` and `inferred` are existing words of the repo's claim vocabulary, so the finding says the column adds a field and no new meaning). The 19 columns and `schema_hash` are unmoved. 27 new tests; 95 earlier contract-reading tests pass. **A 0.4.1 Orion row no longer validates, by design**; the Scope adapter (`2.0.0_SA_COO~I2`) flipped its writer in its own round 127, in the same window. My earlier `return_basis` decision (VENDOR_REPORTED in the existing column) is withdrawn by the ruling.

## Round 144 -- the disclosure placeholder (portal candidate `wk-IRPT_DASHBD-224-portal` @af8ca0ba, LOCAL, never pushed)

Andrew's word, via the CTO (row 90ef): the disclosure page is a placeholder for now. My read of the template he named (`RD_49F_TEMPLATE_DISCLOSURE_READ_A252.json`, counts only) found no disclosure page in it, only the pointer line on 19 pages. One shared constant `Disclosure page pending`; the custody `ClientReportDocument` prints it in an unfilled disclosure slot on both status pages; the 49 Financial default performance report document gains a LAST `disclosures` sheet that prints it while no text is supplied (supplied text prints verbatim; every `Page n of N` counts the sheet; the pointer line stays exactly as it is and is not printed on the page it points to; the set of 117 distinct member ids is unchanged). No disclosure language is authored. 10 new cases, a mutant caught, lint 0, typecheck 0, whole-scope suite 1310 pass with the same 20 failing names as the base (none new). 15 lines of existing assertions moved (the sheet count). **Not proven: how the page looks in a rendered PDF; your next render check reads it.** Three defects of mine were found by the worker and ruled by Amendment 1 (the pointer constant has no trailing period; the language scan matched an existing label; "exactly once" was false of the render).

## Rows for your disposition

`W223-S1` to `S4` (the 0.4.2 cell; `S2` BLOCKING resolved by `S3` and `S4` under my two amendments); `W224-S1`, `S2`, `S3` (resolved by `S7`), `S4` to `S6` (the three pinned-assertion edits, for your review).

## What is in flight

The chain-cap code-update pair (packet sha256 `0ba134ff507a`, both halves signed) is with `0.7.0_AE_CloudOps~DB2` (order `IRPT_DASHBD.TO-DB-b-276`; the lane was respawned by MSTR at 22:27Z and is working). The report-build schedule stays DISABLED until the CTO's word after that pair's after-read. Row `S95` stays ARMED until then. Tomorrow's first fire of the landing schedule (about 12:15Z) is read by me.

## What this does to the FWD outcomes

`FWD-21` (the 49 Financial default performance report): complete except the firm's own disclosure text, now a visible placeholder in a candidate that is not yet merged forward. `FWD-1`: contract 0.4.2 is in the repo for the Scope writer. Grading is the CTO's at L10.

-- 2.0.0_SA_COO~D2
