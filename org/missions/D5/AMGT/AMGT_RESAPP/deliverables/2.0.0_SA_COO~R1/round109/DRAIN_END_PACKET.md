# AMGT_RESAPP round 109 -- drain-end packet (L8), `2.0.0_SA_COO~R1` to `3.0.0_SA_CVO`

**STATE: FILLED, 2026-10-17 ~13:1xZ; the four cut orders are terminal. AC2 of `AMGT-bp-2` (the walk's screenshot read) awaits the CVO's grade.** Round 109 is the CTO's round-108 analysis (`ledger/ROUND_ANALYSIS.round108.md`, msg 7490), issued at `46c09f960f` under this seat's keys (decomposition s.118). All commits named here are LOCAL on `box/dell1` (push state not measured here). `bp-5` (the G4 positive-arm read, Mon 2026-10-19) and `bp-6` (the CloudOps redeploy carrying `bp-3`) are PLACED, not cut, and are NOT in this packet's verdict.

## 1. Orders, cells and the issuer acts

| cell | what | state | evidence |
|---|---|---|---|
| `AMGT-bp-1` | W477-S1: a changed figure whose value is a list never crashes the Model tab (one Opal-internal portal candidate) | complete @20c3075bff, merged @7704efe890 | worker ~488; candidate `cand/dell1/amgt-sa-changed-list-value` @d060d119 on PROD 15bc21b3, `WhatChangedPanel.tsx` only; harness 11 of 11 (issuer re-run); AC2 25 of 28 under AMENDMENT 1 (the issuer's expected line was measured in a plain worktree, an instrument error: no harness regresses); AC3 7 of 7 on the page; approval row `dell1-20261017T124336Z-af5c` closed approved by the CTO (msg 7513) |
| `AMGT-bp-2` | the grid-opened walk of VLO US, RIO LN and WALMEX* MM on a local build of PROD plus the bp-1 candidate (the re-run of bo-3 AC5) | complete @03fcef2774, merged @a83367f57e | worker ~491, instance VALID rc=0; one walk, 3 of 3 `OPEN-FIRST "All figures": opened` (151, 145, 144 rows), `OK: DISARMED`, post-disarm login HTTP 401 REFUSED, `walk void: no`; build = candidate d060d119 on port 5174 (torn down, walker `armed=no`); shots outside the repository at `C:/dev/ui-walk-evidence/bp-2/A/20261017T124617Z/`; **AC2 is JUDGMENT** (yours); rows W491-S1, S2 |
| `AMGT-bp-3` | the served label of an unresolved segment column (`lib/research/api`) | complete @f1949f63ff, merged @1514402a12 | worker ~489 after AMENDMENT 1 (`period_note` sentences); 48 passed across the four segment test files (issuer re-run); the stored source holds no period name, so a figure-bearing untied column is served `Year not stated (column n)`; NOT deployed (placed cell `bp-6`) |
| `AMGT-bp-4` | money display: a foreign-currency code and the sign first (one Opal-internal portal candidate) | complete @dc285dca3c, merged @c90915b235 | worker ~490; candidate `cand/dell1/amgt-sa-money-display` @aba098da, `StatTile.tsx` and `HeaderCards.tsx`; harness 24 of 24 (issuer re-run), difference control 14 tiles compared, exactly two differ (GOOGL US NET DEBT `$-63.90B` to `-$63.90B`, ICT PM ENTERPRISE VALUE `$33.11B` to `USD 33.11B`); approval row `dell1-20261017T123830Z-d775` closed approved |

## 2. The issuer's real runs

- **The walk** (bp-2) is the real run of the bo-3 re-run: three names, the grid opened on all three, the Model tab of RIO LN rendered (round 108's walk D read the page error screen there). `walk_A.txt` read by the issuer: OPEN-FIRST opened 3 of 3, DISARMED, REFUSED, `walk void: no`.
- **Root cause of W477-S1, read by the issuer from the served RIO LN compare:** one changed header figure `ERN_ANN_DT_AND_PER` carried a list of records in `from` and `to`; `numeric()` in `WhatChangedPanel.tsx` called `.trim()` on it. The list grew by one OLDER entry (135 to 136, the added entry `2025-07-15 (2025:Q2)`), which is why the earnings row prints its newest entry AND its length.
- **Landing on DEV is BLOCKED, not done:** `portal-merge-forward.sh cand/dell1/amgt-sa-changed-list-value --push` returned `REFUSED reason=conflict` (dev_before = dev_after = 539b1ee7, nothing pushed) on `src/api/endpoints/tickets.ts` and `src/pages/TicketCenter/TicketCenter.tsx`: PROD holds 23 commits DEV lacks (the TicketCenter ones are dell2's), DEV 102 that PROD lacks. The CTO ruled (msg 7523): reconcile PROD into DEV first (the portal manager, dell2 resolves), no `--waive-overlap`; the approvals stand and the issuer reruns both merge-forwards unchanged after the DEV hash is reported.
- **Not read by the issuer:** the G4 positive arm (Mon 2026-10-19 07:30 ET); the read instrument `round109_prep/checks/r109_g4_positive_arm_read.py` @7bec5b4251 is ready (negative and positive controls run).

## 3. WHAT THE READINGS SAY

**The worker's per-name lines (bp-2, no verdict):**
- **VLO US:** Model renders; All-figures open with rows; What Changed 25 changed, 0 added, no `[object Object]` or `undefined`; AI-fill Exec first line "Management frames its approach around a capital allocation framework prioritizing balance sheet strength ..."; no section blank.
- **RIO LN:** (a) Model renders, no error screen; (b) All-figures open with rows (145); (c) the earnings row reads `2026-10-13 (2026:Q3), 135 entries` before and `2026-10-13 (2026:Q3), 136 entries` after, change `--`, change % `--`, no `[object Object]` or `undefined`; (d) tile `47 changed`, 0 added, 47 rows. AI-fill Exec first line "Simon Trott, chief executive since 25 August 2025, spent 25 years at Rio Tinto ..."; no section blank.
- **WALMEX* MM:** Model renders; All-figures open with rows (144); What Changed 41 changed, 0 added, no `[object Object]` or `undefined`; AI-fill Exec first line "Cristian Barrientos Pozo was named chief executive in October 2025 ..."; no section blank.

**Findings for your judgment (not graded by the issuer):**
- **W491-S2:** the walker's `raw-code` findings (UIW-20261017T124617Z-014, -016, -017) report the raw JSON of the earnings-date list (`[{"announcement_date":"2026-10-13","period":"2026:Q3"}, ...`) in a `tbody > tr > td > details > p` on RIO LN's Model tab (What Changed): the row's expandable full-value detail prints `JSON.stringify` of the list, which `AMGT-bp-1`'s `full()` helper does for any non-scalar value. The collapsed row shows none. Issuer's reading: a raw-code class defect in a detail line, introduced by the bp-1 candidate; it is carried (a fix is a new candidate commit and so a new approval at a new head), not patched this round.
- **W491-S1:** the entry-count suffix beyond the order's `<date> (<period>)` form is the issuer's AMENDMENT 1 reading, not a defect of the worker.
- Round 108's two money reads (a `$` beside a non-USD currency, the minus sign after the `$`) are what `bp-4` and `bp-1`'s sign fix change. Neither candidate is on DEV or PROD yet, so a walk of PROD still prints them where the data has them; bp-2's build carried only the bp-1 candidate.

**Not verified by the issuer:** the worker's AI-fill lines and the per-name sections beyond RIO LN's earnings row and tile counts (the issuer read `walk_A.txt`, not the shots); `bp-4`'s ICT PM and GOOGL US tiles were read through the harness, not on a running page.

I propose no verdict on AC2.

## 4. Open and carried

- **Landing on DEV** of `cand/dell1/amgt-sa-changed-list-value` and `cand/dell1/amgt-sa-money-display` waits on the portal PROD-into-DEV reconcile (owner: the portal manager and dell2; carried by `0.0.0_AB_MSTR~DELL1`). PROD stays Andrew's or the CTO's word: the CTO's msg 7513 corrects its round-108 reading to "Security Analysis is Opal-internal, so its PROD promote is approved by this seat".
- **`AMGT-bp-5`** (Mon 2026-10-19, after the 11:30Z fire): `r109_g4_positive_arm_read.py --since 2026-10-19T11:29:00Z`.
- **`AMGT-bp-6`** (the redeploy of `opal-amgt-scoped-api` carrying `bp-3`): placed; waits on a never-widen pair (COO half, CTO half) and the one AMGT CloudOps lane (CLAUDE.md rule 34).
- **A4 step 1** not before Tue 2026-10-20; **the Lusha plan tier** (Andrew).
- **Row `AMGT_RESAPP-D1-S55`** (the status-enum gap) is filed against the gate's lane; `round-close-check --round 109` reads `verdict=REFUSED` on the one ungraded judgment (bp-2 AC2) and reads MAY-CLOSE on your grade, when the L10 slug to the CTO follows.
