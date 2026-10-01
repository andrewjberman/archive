# DSGN_AMGTV1 round 11 -- the close walk (the COO's one real run)

**Seat:** 2.0.0_SA_COO~D (site Z). **Round:** 11 (decomposition v11, issuance @eacffcbd94; AV-n-1..6 complete).

**Build walked:** 5174 @4e4307be, which contains site-Z DEV 846ecc6c with a 0-line diff.
- This seat re-read it: `--is-ancestor` is true and `/` returns 200.
- CTO~Z's message 27052 (acked) reports the same.

**Instrument:** walk.mjs at CLOUD 5f1750bfa6 (AV-n-4). It waits for each load state and writes `load-states.json`.

| walk | what | window | artifact (gitignored, site Z only) | verdict on the instrument |
|---|---|---|---|---|
| control | `round11/checks/walkvoid.sh`, signed OUT, before the walk | 08:56Z | (the check's own run) | YES. Walker rc=3, 1 WALK VOID line, 0 account lines. Afterwards `status` read disabled, SSM ABSENT. |
| K | thread Valero, `--day "992 HK=2026-08-13"`; VLO, INTU, SAP GY, 992 HK, IMB LN, AZN LN, TSM US, 6501 JP, BA US; the four routes | 08:58:22Z-09:11:03Z | `tmp/ui-walk/20260930T085822Z/` (432 shots) | VALID, disarm proven ("HTTP 401 -> REFUSED"; `status` disabled, SSM ABSENT). 0 guard aborts, 0 API issues, 3 console errors. |

**Load states (AV-n-4's record):**
- 54 of 54 waits read `loaded` (0 `error`, 0 `ceiling`), covering every name's overlay and every tab. The longest wait was 3,609 ms.
- 6501 JP opened fully this time: its header, Thesis, Model and Posture were all shot loaded.

## Each order on the running page (JUDGMENT criteria are the CVO's; this is what the shots show)

- **n-1 (AC4, RESAPP FWD-30):**
  - TSM's header card (shot 294) reads "Enterprise value unit not resolved -- raw figure 71,993,494.73 (TWD)". The qualifier
    comes first and the digits are labelled raw.
  - The measured controls are unchanged on the same walk: IMB "Enterprise value GBP 30.13B" (shot 249) and 6501 "JPY 24.15T"
    (shot 336).
- **n-2 (AC4, FWD-11):** IMB's Posture tab (shot 249) reads:
  - the heading "Filing evidence, each side";
  - "IMB LN (subject): no filing evidence is carried for this name yet.";
  - "No reason with a basis is drafted for this name yet." and "Comparable: none named yet.";
  - no "pack", no "on this object" and no raw key in that section;
  - the research team's line is unchanged: "Fund of record: IDVZ; last stated position: Potential ADD in IDVZ (currently
    ~2.5%). Source: Imperial Brands Research Pack 2026 07 17_v1".
- **n-3 (AC4, HARVST FWD-5/11):**
  - The planted day moved under the page. 992 HK 2026-08-13 is now served PARTIAL, not DENIED (shot 163: "Partial day -- not
    the whole story for that day. Searched: a publisher this page has no name for yet -- 2 found"), so it no longer exercises
    the DENIED wording.
  - The wording is exercised organically on BA US, 2026-09-08 (shot 393): "NOT SEARCHED FOR THIS COMPANY DIRECTLY -- 5
    ARTICLES FOUND IN OTHER SEARCHES", followed by the five served rows.
  - Neither page shows "found anyway".
- **n-4 (AC4, CORPUS FWD-10/11/15/16/18):**
  - 6501 JP's header and Thesis tab (shot 336) were shot loaded.
  - The Thesis reads the served reason: "The research team's thesis pillars: no research dossier for this name."
  - `load-states.json` records all 54 steps.
- **n-5 (AC4, RESAPP FWD-11/13):** BA's Model tab (shot 393) shows:
  - "14 versions have landed; a refresh adds a version and never overwrites an earlier one", followed by the list;
  - "What moved from the earlier version of September 10th, 2026 to the version of September 30th, 2026: 212 figures added,
    0 removed, 7 changed, 172 unchanged", followed by the seven changed lines.
- **n-6 (AC4, RESAPP FWD-12):** BA's Model tab (shot 393) reads "Where each input came from", then:
  - "1 of 6 inputs have run.";
  - "Market data: Bloomberg; last ran September 25th, 2026 and worked.";
  - Filings, News, Social and Web: "no source set up yet; has not run yet."; Seeking Alpha: "Seeking Alpha; has not run yet.";
  - "Re-running one input on its own is not available on this page yet."
  - No storage path is visible.

## Seen on the walk, not in round 11's rectangle (inputs for the round-11 analysis)

1. **The versions picker repeats labels.**
   - The walker's duplicate-options check found this on 4 names: on BA, "September 10th, 2026" x4, "25th", "24th" and "19th"
     x2 (UIW-...-011).
   - Several versions landed on one day, and the long date alone cannot tell them apart. The served stamp carries a time
     (e.g. `20260910T224432Z`, `20260910T225428Z`).
2. **What-moved lines print raw numbers:**
   - "Enterprise value: 193510.78009600003 to 187187.819936" and "Beta: 1.350954532623291 to 1.3597170114517212" (float
     noise, ungrouped);
   - "Short interest: 2.016643 to 1.800129";
   - one line reads "a line this page has no name for yet: 2.903939 to 3.036011" (SHORT_INT_RATIO, which is named only in
     postureCites.ts; worker ~44 flagged this).
   - The same float noise appears on Opal's rule line: "forward EPS (FY1) is -0.8280000000000001".
3. **FWD-11, machine words still on the face (carried from round 10):** 6501's timeline reads "No chatter_daily rows exist for
   this security_key yet".
4. **IMB Posture:** the comparable side reads "a comparable the research team has not identified (comparable): no filing evidence
   ...". The footer reads "0 of the 0 citations can be shown on this page; 0 of 0 were checked", which is correct but reads
   poorly at zero.
5. **The publisher name map:** 992 HK's partial day names its searched publisher "a publisher this page has no name for yet"
   (carried from round 10, item 3).
6. **Other walker hits:**
   - page-wide classes seen before: 11 contrast, 3 bands, 2 truncated, 1 tinted status, and 1 money format ("USD 1,234" beside
     "$1,234" on the thread);
   - 7 `timeline:no-event-element` and 1 `timeline:no-day-bar` (AZN and 6501, which have no collected timeline).
7. **Carried:**
   - FWD-2 names on 7 of 22 rows and the driver series (AMGT_RESAPP r51);
   - the `/timeline/day` latency (HARVST n-6);
   - Andrew-direct via COO~H msg 26928: a mention counter.

## Channel

- Round 11 added no rows (0 worker rows W40-W44).
- The channel holds 23 investigation rows and 13 adjudication rows.
- Every ARMED-standing or BLOCKING row's latest disposition is terminal.
- 5 OBSERVATION/INERT rows remain UNDER_INVESTIGATION (see the drain-end read, section 3).
