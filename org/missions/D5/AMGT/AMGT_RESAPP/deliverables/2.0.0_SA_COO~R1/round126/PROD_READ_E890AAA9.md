# AMGT_RESAPP round 126 -- the page read on the PROD head `e890aaa94f` under a REAL staff login (`AMGT-ch-4` read), `2.0.0_SA_COO~R1`, 2026-10-20 ~02:44Z to 02:48Z

Push state of every commit named: LOCAL on box/dell1 unless stated; the PROD head is on origin (`git ls-remote origin refs/heads/PROD` read `e890aaa94fea`, 2026-10-20 ~02:43Z). Evidence (gitignored, local, client data; nothing is pasted from a screenshot except the page's plain sentences): `tmp/ui-walk/20261020T024405Z/` (63 screenshots, `summary.md`), `C:/dev/ui-walk-evidence/r126-walk-prod.txt`, crop `r126-prod-ba-posture.png`.

## 1. What was read, and what it is not

- **The promote (H2's report, msg 8589, and my own reads):** PROD `ba2c3412` -> `e890aaa94f` (tag `portal-v2.1.246`); `git merge-base --is-ancestor` reads both `c8cd2da0eb` (`cg-2`) and `ebd7b44720` (`ch-1`) IN-PROD; the CI run on that sha reads `completed` / `success` (`gh run list --branch PROD --limit 1`); H2's `AC1` read 19 of 19 paths byte-equal between the two branches and PROD.
- **The read is of the PROD head's SOURCE, not of the deployed bundle.** The walker refuses any base URL that is not `localhost` (the `/ui-walk` safety model), so I ran a scratch worktree at `e890aaa94f` under `bun run dev:live --port 5174`: the page code is PROD's, the login and the data are the live ones through CloudFront. Nothing is stubbed and nothing is forced on this walk. The deployed bundle in a browser at the production host was NOT looked at; the byte tie (AC1) and the CI success are what tie the two.
- Login: the walker armed the account under its one-walk lease and disarmed it (`OK: DISARMED at 02:47:45Z`, post-disarm login refused, 0 guard aborts, the account reads `status=disabled armed=no` at the end); the dev server stopped (port 5174 free) and the scratch worktree removed.

## 2. What the page printed (plain sentences only)

| wording | name | what the PROD-head page printed |
|---|---|---|
| the Peers tab's read suffix (`cg-2`), the `W532-S1` gap | `ICICIBC IN` (step `010-ICICIBC-IN-Peers`) | the peers sentence ends `... and this page says so rather than showing one (read served)`: the plain word `served`, no uppercase state word |
| the Posture tab's cite words | `BA US` (step `063-BA-US-Posture-expanded`) | `Citation not resolved -- a filing passage the analysis built for this name cites, which no drafted sentence on this name's thesis quotes, so this page does not carry its text`; fit-score lines in words (`No fit score for this name ... none of its 13 factors has a value`); figures in words (`Revenue, FY2025: 89,463 million`) |

The failure states (`read failed`, the failed print and export, the two `ch-1` management and model cite words) are not producible on a served name; they were read FORCED on the DEV build (`LIVE_READ_DEV_5552E219.md`), and `AC1` shows PROD carries the same bytes as the two branches DEV carried.

## 3. Disposition

Row `AMGT_RESAPP-D1-W532-S1` (the PROD-only Peers gap) is disarmed by row `AMGT_RESAPP-D1-S66` in the same commit as this record. The `ch-4` fold-back (step 8) is with H2; the `ch-4` order's status flip, the round-126 packet and the L10 slug follow its landing.
