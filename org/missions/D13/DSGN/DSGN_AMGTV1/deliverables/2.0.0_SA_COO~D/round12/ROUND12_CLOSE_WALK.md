# DSGN_AMGTV1 round 12 -- the close (the COO's one real run)

**Seat:** 2.0.0_SA_COO~D (site Z). **Round:** 12 (decomposition v12, issuance @ec9aa557bc; AV-m-1..5 complete; AV-m-4 AMENDMENT 1
@415f31fda6).

**Build walked:** 5174 @a7dd4ccb, which contains site-Z DEV 2c01af6a (a 0-line diff).
- This seat re-read it: `--is-ancestor` true, `/` 200 (CTO~Z msg 27137, acked).
- The final DEV ba62e945 adds only AV-m-1's `portal/scripts` over 2c01af6a (0 page-source lines).

**Instruments:**
- walk.mjs at CLOUD;
- AV-m-1's `ui-contract-check.mjs --dist`, run by this seat on a vite build of DEV ba62e945 (scratch worktree
  `C:/tmp/cood-r12final-root`, build rc=0).

| run | what | window | artifact (gitignored or scratch, site Z only) | verdict on the instrument |
|---|---|---|---|---|
| control | `round12/checks/walkvoid.sh`, signed OUT, before the walk | 12:27Z | (the check's own run) | YES. Walker rc=3, 1 WALK VOID line, 0 account lines. Afterwards `status` read disabled and SSM ABSENT. |
| L | thread Valero; `--day "992 HK=2026-08-13"` and `--day "BA US=2026-09-08"`; VLO, INTU, SAP GY, 992 HK, IMB LN, AZN LN, TSM US, 6501 JP, BA US; the four routes | 12:28:07Z-12:40:44Z | `tmp/ui-walk/20260930T122807Z/` (433 shots) | VALID, disarm proven (HTTP 401 REFUSED; `status` disabled, SSM ABSENT). 0 guard aborts, 0 API issues. load-states 54 of 54 `loaded`, the longest wait 2,366 ms. |
| render | AV-m-1's instrument, `--dist` of DEV ba62e945, six states | ~12:45Z | `C:/tmp/dsgn-r12-close-render/` (grades.json + 6 PNGs + JSON) | grades.json: PASS 61 / FAIL 2 / NOT_EXERCISED 0 (rc=1). Harnesses drafting 8/8, tabs 20/20, posture 32/32. |

## Each order on the running page (JUDGMENT criteria are the CVO's; this is what the shots show)

- **m-2 (AC4, RESAPP FWD-6), BA's Model tab (walk L shot 394):**
  - 15 versions are listed, each with its UTC time. September 10th reads 22:44, 22:54, 23:14 and 23:20 UTC: four distinct
    labels where round 11 read one label four times.
  - The pickers read "September 10th, 2026, 22:44 UTC" and "September 30th, 2026, 09:37 UTC".
  - The sentence reads "What moved from the earlier version of September 10th, 2026, 22:44 UTC to the version of September 30th,
    2026, 09:37 UTC".
  - The walker's duplicate-options check, which hit 4 names in walk K, hits 0.
- **m-3 (AC4, FWD-13), the same shot:**
  - The what-moved lines read:
    - "Enterprise value: USD 194B to USD 187B"
    - "Market cap: USD 162B to USD 156B"
    - "Beta: 1.35 to 1.36"
    - "Share price (last close): USD 204.80 to USD 196.80"
    - "Short interest ratio (days-to-cover): 2.9039 to 3.036" (named from the served definition)
    - "Short interest: 2.0% to 1.8%"
    - "Average volume: 5.52M to 6.04M"
  - Opal's rule line reads "-0.828".
  - The walker's raw-code check hit "Enterprise value (CURR_ENTP_VAL)" once: the new figure tooltip, whose mnemonic FWD-13
    requires one hover away.
- **m-4 (AC4, FWD-11, HARVST FWD-5):**
  - BA's September 8th rows (shots 383/394) name Barron's, Seeking Alpha and Bloomberg; the news list names The Wall Street
    Journal.
  - 992 HK's August 13th day (shot 163) reads "Searched: Bloomberg, The Wall Street Journal. 2 articles are served for this day;
    the day's search record does not say how they were found." The tooltip reads the same.
    - The served searched set gained WSJ after the cut: HARVST aa-2, CTO~Z msg 27124.
    - The route does not yet serve `publishers_found_codes` until AMGT_RESAPP's round-53 build carries 91b74a9047, so the ABSENT
      wording is the correct face today. The found branch is proven only by the check's planted arm.
  - 6501 JP (shot 334) reads "No articles have been collected for this company yet -- this is not the same as a quiet company
    with no articles."
- **m-5 (AC4, FWD-11), IMB's Posture tab (shot 249):**
  - "The research team has not identified a comparable yet, so there is no comparable filing evidence to show."
  - The footer reads "No citation is drafted for this call yet".
- **m-1 (AC3, FWD-20):** the six PNGs of the render run on DEV ba62e945 were read by this seat. The FWD-20 person-read is the
  CVO's; this seat's read follows.
  - **Security states (thesis, exec, peers, model, posture):** one dark band, which is the identity header; white hairline tab
    panels; four header cards. The JSON grades them PASS on all ten clauses, and the PNGs agree.
  - **list (JSON: darkContainers FAIL, band 1 + strip 1):** the "strip" is the Lead Panel's own navy header bar sitting on its
    band. To a person the Lead Panel reads as one dark block. This is either an instrument rule (a strip adjoining or inside the
    band is part of it) or a page change (the header bar in the band's colour). It is the CTO's call and is not graded here.
  - **fourStates FAIL:** loading 2, error 5, empty 1, no-permission 0. No plain run renders no-permission (FWD-19's levers).
  - **The fixture set (`uiContractFixtures.json`) is stale against today's page.** The PNGs show:
    - a raw description reason ("Description: ABSENT -- no description header scalar ['CIE_DES', 'CIE_DES_BULK'] ...") where the
      live page shows the Bloomberg description;
    - "2023: 528 -- PASSAGE P0278" on the Thesis chart;
    - the timeline in its error state;
    - the Model tab's versions / compare / ledger sections as loading skeletons, which account for fourStates' "loading 2".
  - So the instrument's PNGs under-represent the live page: a fixture refresh is a round-13 input for FWD-14..19's grading.
- **Earlier rounds' outcomes, as far as the shots this seat opened show:**
  - BA's input ledger still reads "1 of 6 inputs have run" (shot 394);
  - 6501's header and timeline opened loaded (shot 334; load-states 54 of 54).
  - TSM's and 6501's Thesis shots were not opened this close.

## Seen on the walk, not in round 12's rectangle (inputs for the round-12 analysis)

1. **FWD-11, machine words still on the live face:**
   - BA Exec Management (shot 383): "CEO public profile (Robert K. Ortberg): unreadable object -- status=ABSENT query=set
     absence_class=None."
   - BA Peers (shot 388): "as of 2026-09-24T2252Z" (a raw ISO stamp); "5 present / 12 absent of 17 declared CSC column(s), as
     R-1's map says; 5 column(s) carry a per-member value on R-1"; the subject row reads "BOEING CO/THE".
2. **FWD-20 on DEV:** the list-state darkContainers reading (above) and fourStates' no-permission (FWD-19); the stale instrument
   fixtures (above).
3. **Minor, m-3:** the short interest ratio's two sides print with different decimal counts ("2.9039 to 3.036", a trimmed
   trailing zero).
4. **Other walker hits:**
   - the page-wide classes seen before: 11 contrast, 3 bands, 2 truncated, 1 tinted status, 1 money format;
   - 7 `timeline:no-event-element` and 1 `timeline:no-day-bar` (AZN and 6501, with no collected timeline);
   - 1 `occluded-popover`, new this walk.
5. **Carried:**
   - FWD-2 names on 7 of 22 rows and the driver series (AMGT_RESAPP);
   - `publishers_found_codes` served after RESAPP round 53;
   - Andrew-direct via COO~H msg 26928: a mention counter.

## Channel

- Round 12 added 4 rows:
  - Z-W47-S1 (BLOCKING, INERT): m-4's AC2 harness, ruled by AMENDMENT 1;
  - Z-W47-S2: resolves S1. Its surfaced_at 12:05Z is the worker's estimate; its commit landed 11:49Z;
  - Z-W45-S1 and Z-W45-S2 (OBSERVATION, INERT): m-1's cell wording names ui-smoke.mjs where ui-contract-check.mjs writes
    grades.json, and the tabPanelsWhite reading the worker chose (which does not discriminate old from new).
- The two slots appended at one offset. The outer merge of ~45 stopped on that conflict and was resolved as a text union:
  - CLOUD's rows kept verbatim, the two W45 rows added after them;
  - 0 lines removed, the result valid JSON;
  - finished through `safe-merge --continue` @55a4f05b8c (0 unresolved, 0 foreign, row gate clean).
