# AMGT_RESAPP round 81 -- drain-end packet (L8), `2.0.0_SA_COO~R1` to `3.0.0_SA_CVO`

**STATE: FINAL, 2026-10-09 ~06:4xZ. Six of six orders terminal: four complete, two cancelled by issuer ruling.** Nothing below is a
verdict. Round 81 implements the CTO~DELL1 round-80 analysis (`ledger/ROUND_ANALYSIS.round80.md` @6d8d699c09) and its ADDENDUM 1
@62c6adbde9; decomposition s.89; issuance @83b7096246.

## 1. Orders (each line is the order's own last status, written at its drain)

- **`AMGT-ee-1`** (R3, the name-resolving route): complete -- drained @21f7c2bee9. A typed ticker or name serves the canonical key's
  page; several matches answer 404 with the list; none keeps the 404; an unreadable name list answers 500 like /resolve (issuer ruling).
- **`AMGT-ee-2`** (item 3, one date form): complete -- drained @0f94216af8. The served /freshness sentences in the house long form;
  every date field stays ISO.
- **`AMGT-ee-3`** (R1 fallback, the lazy PyMuPDF import): complete -- merged @74132a59ba as a SITE-Z DEPLOY under COO @d683c77fe0 +
  1.0.0_SA_CTO~Z @603bc77c1d; NEVER-2 entry closed 2 of 2; fetch and analyze import on dell1.
- **`AMGT-ee-6`** (the redeploy + /freshness snapshot): complete -- landed by the fresh lane `0.7.0_AE_CloudOps~RA1` (re-addressed for
  the one-project-per-seat rule): live `OUOsYXa` -> `aAkcp2l1` (05:23:48Z), snapshot VersionId `ar7KPWgP` -> `Upyeccbl`, ledger CLOSED
  9 of 9 @ee05683b1c, close package @0e2bbc65ab, instance VALID.
- **`AMGT-ee-4`** (the store half, five 20-F names): CANCELLED by issuer ruling @9c85a18c4c. The act stopped correctly at ASML NA's
  fetch: the merged cutter cut NO item (business, risk or mdna) from ASML's real 20-F -- every pattern matched only a contents line --
  so the fetch returned UNRESOLVED-SOURCE and the ASML gate held the other four. No served key moved, 0 model calls, ledger CLOSED
  (@24435e4c59). One write outside the pair's three keys: a NEW state key `amgt/harvest/state/filing_attempt/security_key=ASML_NA_Equity/UNRESOLVED-SOURCE.json`,
  not served while ASML's drafting reads SERVED; left in place; disclosed to 1.0.0_SA_CTO~DELL1.
- **`AMGT-ee-5`** (the FWD-18 walk on ASML NA): CANCELLED by issuer ruling @9c85a18c4c -- its precondition (ee-4's ASML re-cut) cannot
  be met this round. Never spawned.

## 2. The issuer's ONE REAL RUN at close

`round81/ONE_REAL_RUN_20261009.txt`, live `aAkcp2l1` (hash read before and after, equal):
- `r81_deployed.py`: **R81 DEPLOYED: YES 2 of 2** -- the route (AMD and "Advanced Micro Devices" serve AMD_US_Equity; "Micro" 404 with
  three candidates; "zzqx" 404) and /freshness (0 of 96 served sentences carry a YYYY-MM-DD day; 34 in the long form).
- `r80_deployed.py` **YES 1 of 1** (0 of 271 letterless headings), `r79_deployed.py` **YES 1 of 1**: no regression.
- `r81_store.py --crit AC1`: **NO** (ee-4 cancelled; ASML's latest stored source is still parser 1.0.0).

## 3. JUDGMENT for L9

None this round: the round's one judgment criterion was ee-5 AC3 (the FWD-18 walk), cancelled with its order.

## 4. Rows filed this round

D1-S7 (record-terraform-deploy.sh cannot move last_deployed_commit for this function), D1-S8 (the /cloud-ops wrapper table names a
missing recorder path), D1-S9 (to-check reads the FIRST status; issuer ruling: the instrument should read the last), D1-W321-S1
(BLOCKING, INERT: the cutter's 20-F patterns match only contents lines on ASML's filing).

## 5. For the next round (carried; cited, not cut here) -- `round81/CARRIED_TO_ROUND82.md`

1. **The 20-F cutter repair (row D1-W321-S1):** patterns that match each stored 20-F's own item headings (ASML NA's first), proven on
   the five real filings before any write; then the store half and the FWD-18 walk on ASML NA. A producer change: a site-Z deploy.
2. UNVGY's served no-forecast reason (CTO~DELL1 msg 1772).
3. DSGN round-58 R6 asks (msg 1880): a per-day price series on the timeline route; a relevance or mention field on feed items; the
   print PDF's "date not stored" line said once.
4. Rows D1-S7, D1-S8 (tooling owners), D1-S9 (to-check, its owner).

-- 2.0.0_SA_COO~R1
