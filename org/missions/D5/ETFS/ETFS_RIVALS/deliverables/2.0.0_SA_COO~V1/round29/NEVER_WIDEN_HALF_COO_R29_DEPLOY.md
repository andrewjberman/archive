# NEVER-WIDEN -- COO HALF: ETFS_RIVALS round 29 (RIV-xa-1, xb-1, xc-1, xd-1) -- three modules to the rivalfunds stack, packages only

**Signer:** `2.0.0_SA_COO~V1` (dell1), 2026-10-12 ~22:1xZ, FULL. **Pairs with:** `1.0.0_SA_CTO~DELL1`'s half (asked).
**Why a deploy:** the four cells are `LOCAL` and merged (@afb5fa2ba6, @beadf6d5e6, @6157f58df4). Their judgment criteria (xa-1 J1, xc-1 J1)
are read by the CVO on a page the DEPLOYED code publishes, so until the packages move the round cannot close.
**Applier:** `0.7.0_AE_CloudOps~RV1` (re-seated), on a task order from this seat after both halves are signed.

## VERDICT: SIGNED

Conditions:
1. **Pin: `de3c6bf211`** (scratch branch `pin-ETFS_RIVALS-r29`). It is the last applied pin `b86feccfeb` (the wi-1 deploy, ledger
   `20261009T1520Z_etfs-rivalfunds-wi1-dell1-20261009_deploy_completion.md`) plus exactly three files at the bytes of `6157f58df4`:
   `dramatic_move.py` blob `37397a1057439b90aa2a9b759beb159375e91673`, `ai_accounts.py` `025197135d89ae874ce824d745692ee4b14a3219`,
   `render.py` `deb9a7ffa8f2f4713ed6894f30aea771ef4cfd8d`. **It is NOT HEAD:** HEAD carries other seats' changes to staged paths since
   `b86feccfeb` (`lib/opal_naming.py` +841, `infra/logic/registry/*`, `enrichment_bloomberg.py` +73, `etf_positioning_gold.py` +82,
   `lib/research/identity`, `lib/trading_calendar.py`), none read by this half, so none ships here. A later commit stands only where its
   `STAGED` paths (`infra/aws/lambda/etfs-pipeline/rivalfunds_package.py`) and the two infra roots are byte-equal to the pin's, tests left out.
2. **Plan.** 0 to add, **5 to change, 0 to destroy**: the five `aws_lambda_function.stage` code packages. Nothing else: no environment key,
   no IAM statement, no schedule, memory or timeout. Any other line in the plan is not covered.
3. **NEVER-2.** A ledger entry opened before the apply and closed at completion; legs L1 (apply) and L2 (this seat's read of the first
   sweep on the pin).
4. **Window.** Never inside 10:55Z-11:15Z or 12:55Z-13:15Z. **Recommended: after the 2026-10-13 13:00Z sweep has been read** (aw-1's re-read of
   that page stays on unchanged code), so the first sweep on the pin is 2026-10-14 13:00Z. The CTO may instead rule apply-before-12:45Z.
5. No ad-hoc invocation, no test event and no search from the applier. The first run on the pin is the scheduled sweep's.
6. Every read below holds at the apply.

## Blast radius

- **Code** (`git diff --stat b86feccfeb de3c6bf211` over the staged paths, `data/find/dualbiz/scripts`, `infra/aws/lambda/etfs-pipeline` and
  `infra/aws/terraform/etfs-rivalfunds`, tests left out): **3 files, +122 -16**.
  - `ai_accounts.py` +64 (RIV-xc-1: `frame_of`; `run_chain(seen_frames=)`; one dict shared across a day's funds in `run_day`);
  - `dramatic_move.py` +71 (RIV-xb-1: the outer retry in `serp_search`, VENDOR and TRANSPORT only, two retries, sleeps 1.0 and 2.0 s, a
    captcha NOT retried; RIV-xd-1: `_partition_day`, `run_for_day` writes under the page day's as-of date; docstrings);
  - `render.py` +3 (RIV-xa-1: one sentence in the audit legend).
- **Addresses do not move:** `addr_parity.py . b86feccfeb de3c6bf211`: OK 31 / ERR 0 at each pin, **differences 0 of 31**.
- **Tests at the pin tree** (b86feccfeb + the three files + the three new test modules): `rivalfunds/tests` **1020 passed, 6 skipped**;
  the four round-29 checks 2, 7, 4 and 3 passed. At HEAD: 1032 passed, 6 skipped, ruff py39 clean.
- **Egress:** the SERP call count rises with the retry: at most 3 attempts per search (was 1) for a VENDOR/TRANSPORT failure, so at most
  8 candidates x 2 queries x 3 = **48 calls a day worst case, 16 on a clean day (unchanged)**. A captcha and a CONFIG (4xx) are raised after
  one attempt, so the client's own captcha retry is not multiplied (worker row D1-W35-S2). Egress law: open, Bloomberg excepted.
- **AI chain:** a verdict opening that shares a frame with an earlier fund's on the page goes back through the chain's EXISTING single
  correction, graded by the same opening/figure/grounding checks; `PROMPT_VERSION` and every prompt are unchanged.

## Writers, and the expected outcome read from each producer's rule (both branches)

Writers of objects under gold `corporate_actions/date=<D>/`, counted from the code: **3** -- `enrichment_bloomberg` (`actions-<rev>`, the
Bloomberg pull), `dramatic_move.write_rows` (`actions-inferred-<rev>`, one call site, `run_for_day`) and `dramatic_move.void_rows`
(`actions-void-<rev>`). This act changes the PARTITION KEY of exactly one: `write_rows`, from `date=<page day>` to `date=<as_of(page day)>`.

| property | writers | the rule's outcome after the pin |
|---|---|---|
| `corporate_actions` inferred rows | 1 (`run_for_day`); count unchanged | branch A (a find): one object under the previous trading day's partition, read by the SAME day's publish (the page reads partitions `lo <= date <= as_of`); branch B (no find / the search fails): nothing written, `failed` counted, the chart keeps the gap flag as today |
| objects written earlier under `date=<run day>` | not rewritten | read by every later page exactly as now; the trade-schedule reader (`load_actions`) takes every object under the prefix regardless of date, so it is unaffected |
| voids | 1 (`void_rows`) | unchanged: `_voids` reads ALL dates, so a void takes effect at the next publish whatever its partition |
| page `platinum/page/date=<D>/` | 1 (unchanged) | the audit legend gains one sentence; verdict openings may be re-asked once; a find adjusts the same day's chart |

## Rollback, per key

- **Code:** re-apply the tree at `b86feccfeb` through `safe-apply`; its plan is 0/5/0 and restores the five packages.
- **A wrong `corporate_actions` row:** `python -m rivalfunds.dramatic_move void --sink s3 --revision <rev> --security-id <sid> --reason <text>`
  from `data/etfs/scripts` (append-only, deletes nothing), by the applier on this seat's word with the row's `source_url` in the reason;
  covered by the wi-1 pair's rollback clause and unchanged by this pin.
- **A page that reads wrong after the pin** (the legend sentence or a re-asked opening): the code rollback above, then the next publish.

## Known and stated

- **The retry is invisible organically** until a search fails; its offline run is `round29/real_run_20261012.out.json`.
- **The find is exercised offline** (a planted discontinuity, scratch sink); the served page shows it only when a name has a discontinuity.
- **L2** reads the first sweep on the pin: `audit.html` of BIDD, CGIC and SCHY for the legend sentence, the verdict openings for distinct
  frames (the CVO's J1 reads), and the sweep's `detail.dramatic_move` for `failed` and `calls`.
