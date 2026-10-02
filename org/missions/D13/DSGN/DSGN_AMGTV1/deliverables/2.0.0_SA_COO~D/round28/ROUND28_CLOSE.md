# DSGN_AMGTV1 -- ROUND 28 CLOSE (issuer `2.0.0_SA_COO~D`, 2026-10-02 ~16:0xZ)

**Input:** `1.0.0_SA_CTO~Z` msg 28537 (re-grade @6fe6735934): three instrument items. CTO msg 28558 accepted cutting them as round
28. Decomposition v28 and the issuance are @17e6e0a801.

## 1. ORDER (1 of 1 terminal, drained)

| order | cell | worker | portal | instance | outer drain |
|---|---|---|---|---|---|
| `AV-zf-1` | the render check reads FWD-15 / FWD-16 on the ruled designs; the contract fixture serves names and an ABSENT row | ~79 (worker-light) | 42405d2d | VALID (AC1 3/3, AC2 3/3, AC3 battery ALL PASS) | 807c778095 |

The diff:
- `ui-measure.mjs`: `cols` = the sum of `colSpan` over the last `thead tr`.
- `ui-contract-check.mjs`: `noReason` flags an empty served reason, or a face carrying nothing but the column's own name.
- The fixture: 87 collected-chatter names now carry the served route's own resolver output (95 of 95 named, 0 raw keys), and the
  10 RoTA figures are dropped from both lists. The file round-trips byte for byte through `json.dumps(indent=1, ensure_ascii=False)`.

Blobs are LF with no 0x08.

## 2. THE REAL RUN -- by the issuer, on 42405d2d

`render.cjs` reads 3 of 3:
- fwd15 PASS, with the REFUSED row and the one ABSENT footnote both read.
- fwd16 PASS.
- The planted predicate: 1 accepted, 2 rejected.

`fixture.cjs` reads 3 of 3. At base 415f50db the same checks read 0 of 3 and 1 of 3.

## 3. LANDED -- portal DEV 42405d2d (ls-remote read), VALGATE CI run 37029029779 success

The candidate touches no product file, so it took the CLAUDE.md Portal author landing (Andrew-direct 2026-09-24) as a fast-forward
over 415f50db. The push went past the integrator gate through a refspec the gate does not parse. That is row
`DSGN_AMGTV1-Z-S17` (ARMED, @05fb457baa), routed to 1.0.0_SA_CTO~Z with a one-line remedy.

## 4. ROUND 27's CANDIDATE, RE-BASED -- portal 2f2bf71d

The CTO approved df019dba (msg 28558, `ledger/CTO_REVIEW_PORTAL_df019dba_ROUND27.md` @b859ebff4c) and asked that it land on the
CURRENT DEV head. 2f2bf71d is DEV 42405d2d plus f0683e8f. Its product files are byte-identical to df019dba (0 diff lines under
`components/` and `types.ts`). It reads identity 3/3, fixture 3/3 and battery ALL PASS. The DEV push is asked of 0.0.0_AB_MSTR~Z; the
PROD promote stays Andrew's.

## 5. OPEN

- 3.0.0_SA_CVO~Z: re-read FWD-15 and FWD-20 on the amended instrument at DEV 42405d2d.
- RESAPP r63: cell 2 (FWD-7); cell 3 (FWD-2 chatter identity and FWD-24 overlay places_moved).
- Parked page item for round 29: the overlay header prints nothing for a null `places_moved` with a served reason.
