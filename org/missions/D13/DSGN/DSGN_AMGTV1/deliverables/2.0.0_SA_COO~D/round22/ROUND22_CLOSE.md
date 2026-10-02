# DSGN_AMGTV1 -- ROUND 22 CLOSE (issuer `2.0.0_SA_COO~D`, 2026-10-02 ~07:4xZ)

**Input:** `1.0.0_SA_CTO~Z`'s `ledger/ROUND_ANALYSIS.round21.md` @e14de1769c, section 3A (msg 28252). Decomposition v22 and the
issuance are @3db1b9957f, over PRD v0.7 @9ef3af2bee (ADMITTED). Deadline 11:30Z: all three orders were drained by ~07:3xZ.

## 1. ORDERS (3 of 3 terminal, all drained)

| order | cell | worker | portal | instance | drain |
|---|---|---|---|---|---|
| `AV-z-1` | A1 no code-shaped token on Exec, Posture, Peers (FWD-11) | ~69 | bcc95f4b | VALID (AC1 3/3; AC2 tsc 0 + 14/14) | CLOUD b15312132e (needed 5, dropped 0, foreign 0) |
| `AV-z-2` | A2 Peers subject Price/EV from the header (FWD-8) | ~69 (fresh session, same slot) | a195f51f | VALID (AC1 3/3; AC2 3/3 + tsc 0 + 14/14) | same merge |
| `AV-z-4` | A4 errorEmpty starred claims (Z-W56-S4) | ~70 | aa3cc82a | VALID (AC1 3/3; AC2 14/14) | CLOUD c81376fdf2 (needed 2, dropped 0, foreign 0) |

`AV-z-3` (A3) takes no order (decomposition v22 placement a). Portal: the local DEV was fast-forwarded 24646bca -> 3ca6c53a (origin DEV
at the cut), then two `--no-ff` drains: 8c250e5d (~70), **a730d8ce (~69)**. LOCAL; origin DEV is 3ca6c53a.

## 2. DRAIN CHECKS ON THE MERGED DEV a730d8ce

codeface 3/3; subjectrow 3/3; starredclaims 3/3; round15 bound ALL 14 of 14; round21 tipface 3/3; round20 namecard 3/3; `tsc -b
--noEmit` rc 0.

## 3. THE REAL RUN -- signed-in walk `tmp/ui-walk/20261002T072805Z` (site Z only, not committed)

5174 served the main portal tree at DEV a730d8ce (`bun run dev:live --port 5174`). The walker was ARMED and DISARMED with notices to
0.0.0_AB_MSTR~Z (28281 ARM; DISARMED 07:34:30Z, the login after the disarm was REFUSED). 147 shots, walk void no, 0 API issues.
PNGs read by the issuer:

| face | shot | read |
|---|---|---|
| VLO Exec | 067 | "Contact enrichment was skipped for this company." (was "Lusha enrichment: SKIPPED -- no declared domain for VLO_US_Equity in domains.json"); no code token. Still served: officer "Senior Vice" and roles ending in an age ("... President 60") = RESAPP B3 |
| BA Peers | 025 | subject row Price **196.80**, EV **187,188** (header USD 196.80 / USD 187B); absent columns read "not in the comparison map -- <reason>", no ABSENT, no field code |
| VLO Peers | 073 | subject Price **382.86**, EV **116,978** (header USD 382.86 / USD 117B); P/E (trailing) "--" (no P/E header figure served) |
| AMD Peers | 119 | subject Price **630.63**, EV **1,020,653** (header USD 630.63 / USD 1.02T) |
| BA Posture | 052 | reason 2 reads the plain fallback "The reason for this claim is held in the record; its cites follow." (served "ABSENT" claim held in `data-posture-claim-served`, until RESAPP B4) |

Not read as PNGs: BA Exec, AMD Exec, VLO Posture, AMD Posture (the fixture census graded the same code paths).

**Walk findings (12):** raw-code 1 is the Lead Panel's GenerationCaption machine line ("generation ... | coverage vintage
bloomberg-dapi-boxsid ...") inside its collapsed `<details>` (`GenerationCaption.tsx:49-51`, kept there by design). It is outside
A1's sites. CTO~Z RULED 3a (msg 28286): a finding inside a closed, provenance-labelled details block is "raw-code (folded
provenance)" and is not graded against FWD-11; the walk's visible faces carry 0 raw-code hits. The rest: colour-law and
truncation pointers and the two `FWD-6` timeline labels, which are the walker's older numbering (ADJUDICATION_v19 section 4).

## 4. A3 (FWD-2) -- BASELINE BEFORE RESAPP B1

`lead-lists.json` of this walk: 94 price bars; **24 labelled by the ticker** (label == the security key's ticker): RMS FP, HAL US,
KMB US, ICICIBC IN, ENEL IM, RKT LN, ST SP, BABA US, ZURN SW, ULVR LN, KPN NA, IMB LN, COST US, SSE LN, BBSE3 BZ, SAP GY, NOVN SW,
HSBA LN, WALMEX* MM, NG/ LN, BP/ LN, RWE GR, 9433 JP, 2317 TT. These are the 24 the analysis names. The page prints the served name
wherever one is served (70 of 94). A3 is read again on the first walk after RESAPP round 61 B1 deploys: it is REALIZED at 0 of 94.

## 5. OPEN AFTER THIS ROUND

- **The PROD promote of a730d8ce** (with origin DEV's own commits since b3a1d8a6): Andrew's word. The DEV push is
  `0.0.0_AB_MSTR~Z`'s on Andrew's word. Rollback `b3a1d8a6`.
- **A3:** waits on RESAPP B1. **FWD-7** (officer titles, trailing ages): RESAPP B3. **Posture claim wording:** RESAPP B4.
- **Row Z-W69-S1** (INERT): `posture.harness.cjs` throws `useCollectedChatter is not a function`. The issuer re-ran it on DEV
  8c250e5d, which has no z-1 change: the same TypeError, so it pre-exists this round. It is a stale hook stub outside the 14-bound.
- Worktrees `C:/tmp/wk-dsgn-amgtv1-{69,70}` are kept; a teardown is a recursive delete.
