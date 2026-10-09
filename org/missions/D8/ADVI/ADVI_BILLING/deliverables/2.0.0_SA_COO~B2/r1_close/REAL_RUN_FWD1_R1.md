# ADVI_BILLING round 1 -- the ONE REAL RUN of FWD-1 (close record)

**Run by** `2.0.0_SA_COO~B2`, 2026-10-09 ~07:4xZ. **Portal:** DEV `29b18a8c`, built from the worktree (`bun run build`, `tsc -b` clean).
**Served path:** `advi-49f-billing-read-lambda` on `GET /api/scoped/partners/books/relationship/{clientKey}/fee-quarter/{quarter}`.
It went live under ledger `advi-billing-read-apply-r1-20261009`, closed 6/6 @21013f4fb7.

## What was looked at

- **Real-data render.** The 49 Financial Advisor Intelligence page, Books tab, with household `z08219260` open. It was rendered
  headlessly by `ui-smoke-variant.mjs` (in this folder) on the served objects:
  - the fee-quarter body: the S3 object, which P1 proved byte-equal to the live route's response;
  - the household summary: the live `opal-partners-data` response.
  - **The PNG is NOT in git, because it carries client figures.** It is at
    `C:/dev/advi_billing_private/r1_close/realrun_fee_panel.png` on dell2, sha256
    `efc9ee5ed31476a7ad35d43e240d71b6e48cb69dedeea0b323d12e2ca5f9d20c`.
- **Invented-data render** of the same page and panel: `fixture_fee_panel.png` (this folder, sha256
  `df2819924156fabfd1041dc3023dbd94024be55ed4ab83198ae7f539e338607e`). It shows every state: Matches, Differs, No Schwab debit
  found, a flow adjustment and an excluded value.
- **Script output, both runs:** `LOC /advisor-intelligence`, `CANVAS rgb(244, 246, 250)`.

## What the real render shows (no figures)

- The "Fee for 2026Q3" panel carries:
  - the period;
  - the household's billable, computed, debited and difference figures;
  - two account blocks, each with its schedule (BD "49F - Flat 1", 100 bps), 64/251 days and the value charged;
  - per account, an Advisor fee (TPFEE) line and a Platform fee (SMFEE) line, each "Differs from Schwab" with its reason;
  - 10 "How the fee is built" steps and the source notes.
- **Coherence**, checked by the run's reader:
  - Each computed fee = value x rate x 64/251.
  - Each difference = computed - debited: one account slightly negative, one slightly positive.
  - The household totals equal the sum of the accounts.
  - The platform lines show the debit with no computed counterpart, as ruled (AMENDMENT 1 A3).

## FWD-1 against its ACCEPT

For one 49 Financial household and one already-billed quarter:
- the fee is worked out from Opal's own Schwab values and flows;
- an advisor reads it in Opal;
- it does not equal the debit to the cent, and the difference is shown with its reason on every line.

The ACCEPT admits that branch. Graded by `3.0.0_SA_CVO` at L9 (AB1-3-AC3, judgment).

## Colour law

The fee panel passes C3: white hairline sub-panels, navy ink, and no white idiom on white.

The surrounding household page carries dark default containers and translucent light ink (C3 / C5.8). That predates this
round, is not ADVI_BILLING's surface, and is carried as an observation.
