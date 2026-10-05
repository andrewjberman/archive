# DSGN_AMGTV1 -- ROUND 38 CLOSE (issuer `2.0.0_SA_COO~D`, 2026-10-05 ~13:1xZ) -- THE SHARED FOOTERS, THE END LINE, WHAT CHANGED'S STATES

**Input:** decomposition v38 and the issuance @c528ed0107, over PRD v0.15. Rectangle: the CTO's list @0a865d7e8f. Base: portal 85e24287
(the CTO-approved round-37 candidate).

## 1. THE CELL (1 of 1 terminal, drained)

| order | cell | worker | portal | AC1 / AC2 (issuer re-run on the worker tree) | outer drain |
|---|---|---|---|---|---|
| `AV-zp-1` | shared footers, end line, What changed's states (FWD-11, FWD-19) | ~100 (re-seated once) | 788d54a8 + 75f9f477 | repairs38 5/5; battery29 ALL PASS 14/14 | 48d8c081d7 |

**Amendment 1** (@237bf4df8d, on row Z-W100-S1): the first pass read AC2 at 3 of 14, because the page's own harness loaders had fixed
import lists and one asserted the retired caption. The amendment granted the 11 loaders and ruled S2: no invented clock on a bare served
day. The original worker could not be resumed, so a fresh worker continued on slot ~100 from its commits. Rows S1 and S2 were
addressed. **S3 is open:** the shared `PageEnd` (outside the cell's paths) still prints "5:00p ET" after a bare served day.

## 2. THE CANDIDATE -- portal `5fe58e89` = DEV 0edab95f + rounds 37 and 38 (LOCAL)

- battery29 ALL PASS (0 skipped).
- Nine checks, rounds 34-38, at full marks. repairs36 first printed an empty line: an interim tail read while it ran. Re-run alone it
  reads 5/5.
- FWD-20 instrument (C:/tmp/r38-scratch-close): 4 of 4 arms, 76 PASS / 0 FAIL. The shared footers on the light ground keep
  lightOnDark at 0.

**CTO review @2e225582da: APPROVED pending ONE fix.** `CardFooter.tsx:95`'s last fallback prints a de-punctuated raw code, which FWD-11
forbids. It must return `UNNAMED_SOURCE_WORDS`, and repairs38 gains one arm with an unknown long source. The fix is cut as round 39 (a
direct act). Andrew's word (record 121b7b016e, msg 29560): "3.) Yes, recommendation approved." -- the round 37+38 DEV push, once the fix
lands and the CTO confirms it.

## 3. THE REAL RUNS (walker slot 29542 after site Z's Modern Standby 09:14Z-12:32Z; ARMED 12:45:09Z, DISARMED 13:05:20Z, login after REFUSED)

**Close walk** `round35/walk/read-20261005T124508Z` (closewalk35.mjs, names BA/VLO/AMD/MSFT): **27 reads, 26 PASS, 1 FAIL, 0 ERROR.** The FAIL
is the known BA dividends-per-share real move to zero.

**Reads** `round37/walk/reads37.mjs`, read-20261005T125739Z: **8 reads, 5 PASS, 2 FAIL, 1 ERROR.**
- fwd5-markers BA: PASS (marker -> HeroDialog). AMD: ERROR, because AMD serves no events or markers (a served-data fact).
- **fwd5-own-first BA and AMD: PASS "by served origin: own rows lead".** The day route now serves an origin field (RESAPP r68 item 6),
  so the round-37 "vacuous" reading is retired.
- **fwd19-panels BA and AMD: graded PASS on reading -- the instrument is stale, not the page.** The timeline and the header render the
  DESIGNED PanelLoading and PanelError. What changed's loading renders the DESIGNED PanelLoading. For What changed's error the walk
  reports NONE because its probe scope selector no longer finds the panel: round 38 moved the error into the probe's own component.
  The page PNG (`fwd19-BA-US-what-changed-error-page.png`) shows the designed error in place: "What changed could not be loaded. Try
  again; if it keeps failing, the feed is down." with a "Try again" button. **Issuer instrument fix owed:** reads37's What-changed
  scope selector.
- fwd19-no-permission: PASS.
- **fwd11-side-by-side (the person's read, issuer):**
  - every served card now ends in the shared footer: key figures "October 4th, 2026, 3:56p ET | Source: Bloomberg."; recent news
    "October 1st, 2026, 1:03a ET | Source: Seeking Alpha, Barron's, Bloomberg and The Wall Street Journal."; the Model tab "October
    5th, 2026, 9:03a ET | Source: Bloomberg.";
  - the page ends "End of Security Analysis. Data as of October 2nd, 2026, 5:00p ET.", in the reference pages' form.
  - **The one defect seen: the end line's "5:00p ET" is not served (row S3).** The timeline shows no footer, correctly, since it
    serves no source.

## 4. OPEN -> ROUND 39

1. **The CTO-required fix:** `CardFooter.tsx` unknown source -> `UNNAMED_SOURCE_WORDS`, plus the repairs38 arm (being authored).
2. **Row S3:** the end line prints no clock after a bare served day (the shared PageEnd: one optional prop, default unchanged, or a
   pre-formatted date from SecurityAnalysis.tsx).
3. **Issuer instrument:** reads37's What-changed scope selector follows the probe component.
**Then:** the round 37+38(+39) DEV push on Andrew's word, held at MSTR~Z.
