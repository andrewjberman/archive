# AMGT_HARVST ROUND 12 -- DRAIN-END PACKET, `2.0.0_SA_COO~H`, 2026-09-29 ~03:1xZ

**Issuance:** `a51c02d159` (seven orders over `ROUND_ANALYSIS.round11.md` @`91276ffa94`; decomp section 24).
**L8-L10 route:** `3.0.0_SA_CVO~Z`. **Close run:** `round12/CLOSE_RUN_ROUND12_TRACE.txt` (deployed plane, OK).

## 1. SEVEN ORDERS, SEVEN TERMINAL, SEVEN VALID

| order | seat | class | close | result |
|---|---|---|---|---|
| `a-1` declare the mount | `~35` | WORLD (floor) | `180989c8a8` | tf list + precondition + route table 16 -> 18; api suite 256/256 after AMENDMENT 1 (two RESAPP tests pinned 16) |
| `a-2` package + deploy | `0.7.0_AE_CloudOps~A` | WORLD | `0d54b880cf` / close `ada97990df` | ONE combined act with RESAPP `uu-4` under both pairs; issuer re-measured AC1 + AC2 on the served plane |
| `a-3` the plurality lead | `~36` | LOCAL | `2751f0be77` | story grouping in `event_rows`; 1 of 8 leads moves; ids/spans/members unchanged |
| `a-4` the served rebuild | `~36` | SERVED | `8e3e28e696` | one added part `date=2026-09-29/part-20260929T002311Z`; 4 prior parts intact (issuer re-read) |
| `w-5` bbg diagnostic | `~37` | WORLD | `2dd09b20b9` | one call pair (user-info 200, search 403 PerimeterX); vendor-side regime SUPPORTED; capture not plannable |
| `w-4` ft/barrons diagnostic | `~38` | LOCAL | `09230f554a` | no vendor call; the ft duplicate never double-counts; the barrons flake is the z-3 patch class |
| `w-2` capped sa capture | `~37` | WORLD | `7c1c04b844` | three guards PASS; ONE request, account check HTTP 402, 0 articles |

## 2. THE OUTCOME, ON THE DEPLOYED PLANE

**The timeline is reachable for the first time.** API `7k3ed8px20` mounts 18 scoped-AMGT routes; the deployed function
(CodeSha256 `CtIvirv...`, 01:58:24Z) answers `/timeline` and `/timeline/day/<date>` HTTP 200 with data. The close run
invokes the deployed function for `BA_US_Equity` and `992_HK_Equity` and finds what it serves EQUAL, span and lead, to the
newest landed `chatter_event` rows -- including the rebuilt lead "Boeing Delivers 51 Jets in August, Lowest in Four
Months" on 2026-09-08. In-region timing: range 2.0-2.4 s, day route 8.5-8.9 s, against the 29 s ceiling.

**Not claimed:** FWD-5 / FWD-6 are graded at L9/L10, not here. The portal DEV push of `92a2576254` (Andrew's ruling 3)
now has its route condition met on the served backend; its measurement is `0.0.0_AB_MSTR~Z`'s, and that seat has no
live session.

## 3. JUDGMENTS FOR L9 (presented, not graded)

- `a-4` AC4: every multi-story event (8 of 8 under the grouping), same-event vs unrelated stories printed. Both halves
  card the rule as THIN: 1 of 8 leads moves, the single-token link was tuned on the one judged case (over-merge risk,
  BA 09-08), and NVDA 06-01 UNDER-merges (one story read as three). `BA_US_Equity` 2026-08-26 is a 1-1 tie
  (row `Z-W36-S1`); "is a multi-story day one event?" stays open.
- `w-2` AC4: 0 `--new-only` skips (no listing page was fetched), so nothing to grade.

## 4. THE INCIDENT, AND WHAT IS STILL AN ACCOUNT-HOLDER ITEM

At 00:21Z a `w-2` guard test misfired and ran the producer's real Seeking Alpha re-authentication (headed Chrome,
stored credential submitted, bot wall, 3 Kimi calls). Row `Z-W37-S3`. The CTO ruled the resume behind three guards
(record @`74e1eea534`, msgs 26391/26396); all three PASS. The spend is ledgered as ESTIMATE-UPPER-BOUND (<= 12,000 out
+ 13,788 in tokens; rate UNMEASURED; the provider figure NOT MEASURED). **Then the capture's one request met HTTP 402
on the sa account check** (200 on 09-26), row `Z-W37-S4`, cause unmeasured. **For the account holder, not a seat:** is
the Seeking Alpha subscription active, and does the account show the 00:21Z sign-in? The worktree
`C:/Users/Opal Bloomberg/Desktop/wk-hvst-r12-37` is KEPT: its untracked `.scratch/auth/` holds the only raw incident
evidence (login-form screenshots, never committed); it is removed on that owner's word.

## 5. ROWS -- the gate's own fold: 88 ids, GRADUATED 46, DISMISSED_WITH_REASON 25, UNDER_INVESTIGATION 17 (24 files)

Remedy EXERCISED this round (the CVO writes the clock): `Z-S34` (the mount spec), `Z-S35` (pyarrow), `Z-S36` + `Z-S39`
(the grant, GET then LIST), `Z-S38` (the pin), `Z-W31-S1` (unmounted), `Z-W35-S1` (the pinned-16 tests), `Z-W37-S3`
(the three guards). `Z-W31-S2` (latency) is answered by in-region timing (8.9 s worst of 29 s).
Open with a named owner: `Z-S37` (the `safe-merge --continue` window; tool fix proposed to the script's authoring lane),
`Z-W37-S4` (the 402; account holder). INERT / informational: `Z-W34-S1`, `Z-W35-S2`, `Z-W36-S1`, `Z-W37-S1`, `-S2`, `-S5`.
**Armed rows with an owner this seat could not seat: NONE.**

## 6. WHAT I GOT WRONG THIS ROUND -- three, all grants and censuses

1. The cut said the role "already reads harvest gold" -- an inference (`Z-S36`, caught by `4.0.0_SA_CRO~Z`).
2. The grant then covered GET, not LIST (`Z-S39`, caught by `0.7.0_AE_CloudOps~A`); and my section 9 claimed the pool list
   held none of the eight prefixes after reading only its head (5 of 8 were already covered; half s.10).
3. `a-1`'s `<paths>` missed two tests that pin the table length (`Z-W35-S1`, caught by the worker).
**One shape:** a permission or a reader population asserted from a partial read. COST of the fix: enumerate the WHOLE
object (every S3 call a loader makes; every reader of a changed value; the whole list) before writing the grant.
And one more that is mine and not a grant: my `a-3` drain swept `~A`'s NEVER-2 entry (`Z-S37`), found by my own audit.

## 7. FOR THE ROUND-13 CUT (the CTO decides)

1. The timeline in the portal: Andrew's ruling-3 DEV push, now unblocked on the route side.
2. FWD-5 / FWD-6 walks on the served page.
3. The lead rule's thinness and the open "one event?" question -- decided on L9's evidence.
4. bbg: `w-5` names ONE further observation (an article-API GET) that would split host-wide from search-scoped; it
   needs its own word.
5. sa: nothing plannable until the 402 is explained by the account holder.

## 8. WHAT THIS PACKET DOES NOT DO

It grades no judgment, claims no FWD REALIZED, pushes nothing (every commit is LOCAL), and cuts no round-13 cell.
