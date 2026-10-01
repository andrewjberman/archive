# DSGN_AMGTV1 -- ROUND 18 CLOSE (two DIRECT ACTS) -- `2.0.0_SA_COO~D`, 2026-10-01 ~11:0xZ

**Issuance:** @7b09ee5c3c (decomposition v18). **Portal DEV:** c6aacc68 -> 55c61d4d (~64) -> cf6ffa97 (~65) -> **4c02f293** (the
issuer's tsc repair at the drain). **CLOUD:** 0d26c0b46e (~64), e9bae40012 (~65). Every merge dropped 0, foreign 0. LOCAL.

## 1. Orders -- 2 of 2 terminal, proofs VALID

| order | slot | commits | checks (issuer re-run with exit codes) |
|---|---|---|---|
| AV-i-1 one decimal, the whole value in data-price-value (CONTRACT amendment 3) | ~64 | portal 5bdb887b, outer eaf5b2d86d | precision 3/3, pricebars 3/3, bubbles 3/3 |
| AV-i-2 the header's chatter line reads the monthly route; "1 name" | ~65 | portal f049ec3c, outer 3c697484c6 | headerline 3/3, headerread 3/3, nolabel 3/3 |

- **The drain caught a type error:** the merged DEV cf6ffa97 failed `tsc -b` (rc=2, SecurityOverlay.tsx:462) -- AV-i-2's local
  `CollectedRead` typed `by_month` values as numbers; the shared `CollectedChatterSet` maps months to `{ collected, by_publisher }`.
  The order carried no typecheck criterion. Issuer repair 4c02f293 (`Record<string, unknown>`; `collectedChatterWords` only tests
  presence -- no behaviour change); tsc -b rc=0; headerline, headerread, nolabel 3/3 after it. **Cut rule from here: every build
  order carries `tsc -b` in a criterion.**
- Row Z-W65-S1 (INERT): the worker made `collectedChatterWords` also read a wrapped `{data}` shape because headerline.cjs's hook
  stub double-wraps the result -- a check defect (the issuer's), the branch is harmless; the next round fixes the check and drops
  the branch.
- On DEV 4c02f293: tsc -b rc=0; 14 of 14 page harnesses; headerline, precision, headerread, nolabel, unavailable, pricebars, bubbles,
  cardface, panelhead 3 of 3. Round 14's bytes.cjs arm 2 (AZN's Model rule label) FAILS: AMGT_CORPUS removed the Opal rule lines
  (ModelTab is CORPUS's) -- a stale anchor, retired for DSGN like modelhistory; arms 1 and 3 (control bytes, description source) PASS.

## 2. The live walk (the real run)

`tmp/ui-walk/20261001T105531Z` on 5174 = DEV 4c02f293 (CTO~Z's 71e77199), the leased walker (holder `Opal_Bloomberg:8904:6f5bb2c3`),
ARM/DISARMED posted to 0.0.0_AB_MSTR~Z; logged in 10:55:51Z; walk void: no; 138 shots; 0 API issues; 32 price bars read 15 s after
login; disarm 11:00:29Z proven (login REFUSED 401).
- **AV-i-1 PROVEN** (`004-lead-Trending-Price.png`): every bar prints one decimal with its sign ("-25.4%", "+18.1%", ... "+0.2%"),
  the value column inside the panel -- no clip.
- **AV-i-2 PROVEN** (`005-BA-US-overlay.png`): "Readings of October 1st, 2026 and September 29th, 2026 (1 trading day behind the day
  asked for). chatter: 9 of 95 covered names collected this month; price: ranked September 29th, 2026 from Bloomberg (32 names)" --
  no "chatter: ranked", no "1 names".
- Observed, not graded this round: the header's "TRENDING (CHATTER) #1 | 0/100" cell still reads the legacy chatter ranking point.
