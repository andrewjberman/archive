# NEVER-WIDEN -- COO HALF: portal PROD promote, b06863fe -> dbeb6764 (44 commits, 71 files)

**Signer:** `2.0.0_SA_COO~D`, 2026-10-08 ~17:3xZ. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (owed; CTO msg 31880: "it moves served
output for every page in the range, so it carries a pair naming them"). **Andrew's word:** "recs approved" on CALL 2 of this seat's
/open-calls, record `org/tier1_exec/2.0.0_SA_COO~D/deliverables/ANDREW_DIRECT_20261008_155xZ_RECS_APPROVED_DSGN_DEV_PUSH_DBEB6764_THEN_PROD_PROMOTE.md`
@7eb9750741. Its condition, the owners' confirmations, is met (section 3).

## 1. THE ACT, PINNED TO ONE SHA

In a portal worktree at origin PROD `b06863fe`: `git merge --no-ff dbeb6764eaa688230f44cfcc1763bd73db6e1142`, then push PROD. This is
the pattern of this seat's last promote (merge parents ab3191d0 + 8ddfe409, @13a406a1d4). The push triggers `.github/workflows/deploy.yml`.
A NEVER-2 ledger entry with four legs is opened first: PROD merge on origin; the deploy run green, matched by head sha; the tag; the
served index read.

**Pinned to `dbeb6764`, NOT to DEV's head.** Origin DEV is now `1cbc56a7`, 9 commits past `dbeb6764`: AMGT_CORPUS round 40
(`0498827c`, `1cbc56a7` and seven worker commits), 5 files under `src/pages/SecurityAnalysis`. Those 9 are outside the range the owners
confirmed, so this act does not carry them. They go in a later promote once their owner confirms them.

## 2. WHAT MOVES: the served portal site, every page in the range

`b06863fe..dbeb6764`: 44 commits, 71 files (`git diff --name-only`, this seat's read). By area: `src/pages/InvestorReporting` 36,
`src/pages/SecurityAnalysis` 10, `src/pages/AdvisorIntelligence` 7, `src/pages/TicketCenter` 4, `src/pages/Attribution` 2,
`src/components/holdings` 2. One file each: `vite.config.ts`, `src/lib/chartColors.ts`, `src/contexts/AuthContext.tsx` and
`src/api/endpoints/tickets.ts`. Six files under `scripts/`, which do not enter the bundle. `vite.config.ts` and `AuthContext.tsx` reach every page.
~~`b06863fe` is an ancestor of `dbeb6764`~~ **CORRECTED 2026-10-08 ~18:3xZ on `1.0.0_SA_CTO~Z` msg 31951: that sentence was
false.** `git merge-base --is-ancestor b06863fe dbeb6764` reads rc 1 (positive control `d1b21c97` rc 0, this seat's re-read).
PROD holds five DEV->PROD merge commits of its own (`c69b4747`, `ce6f0721`, `f8c94759`, `ab3191d0`, `b06863fe`). The CTO read
each one: its tree equals its DEV parent, 0 files, and every DEV parent is inside `dbeb6764`. So the conclusion holds: nothing
served on PROD today is outside the range.

## 3. THE OWNERS' CONDITION (from the integrator's relays; this seat did not read the boxes' own files)

| owner | projects | commits | answer |
|---|---|---|---|
| `1.0.0_SA_CTO~Z` (site Z) | DSGN_AMGTV1 | 11 | CONFIRMED (msg 31880) |
| `1.0.0_SA_CTO~DELL1` | MDPF_SECCLASS | 11 | CONFIRMED-FOR-PROD (relayed in msg 31896) |
| dell2 `1.0.0_SA_CTO` | IRPT_YCDGEN, IRPT_CUSTDY, IRPT_BCKEND, TCKT_VNEXT | 22 | CONFIRMED-FOR-PROD (relayed in msg 31903) |
| laptop `1.0.0_SA_CTO` | none of the 44 | 0 | owns none (relayed in msg 31910) |

22 + 11 + 11 = 44, the integrator's subtraction by hash (msg 31903). The qualifiers dell2 stated and did not treat as holds:
IRPT_YCDGEN's FWD-1 is ungraded; IRPT_BCKEND has no seated CVO.

## 4. WRITERS OF THE SERVED SITE, AND THE RULE OF EACH, READ AT SIGNING

- **N = 1 inside the portal repo:** `deploy.yml`, on push to PROD (also `workflow_dispatch`). Its rule:
  - job `build` (bun 1.3.9 on a GitHub runner);
  - job `deploy` (`needs: build`), in order:
    - `aws s3 sync dist/ s3://<bucket>/ --delete`, excluding `index.html` and `*.json`;
    - `aws s3 cp dist/index.html` with no-cache;
    - every `*.json` copied with a 60-second cache;
    - a CloudFront invalidation;
  - job `tag` (`needs: deploy`): the next `portal-v2.1.N` tag.
- `promote-to-prod.yml` is `workflow_dispatch` only and is not run by this act. Not read: any writer of the bucket outside this repo.
- **The expected outcome, read from that rule:** the bucket's hashed assets equal `dbeb6764`'s build. `--delete` removes every asset
  that build does not produce, and `index.html` points at the new assets. PROD today was built by the same rule from `b06863fe`.

## 5. READ ON THE CANDIDATE BEFORE SIGNING

On `dbeb6764`, by this seat:
- CI run 37806817498: success, 2 of 2 jobs;
- the render instrument: 4 of 4 arms, 76 PASS, 0 FAIL, 1 N/A (`round52/dev-read-dbeb6764/`);
- `r51a` 4 of 4; `r52` 3 of 3; battery29 ALL PASS;
- the live-function walk on BA US and BP/ LN: 8 of 8.

On DEV's head `1cbc56a7`, for the record (not this act's sha): `r51a` 4 of 4, `r52` 3 of 3 and battery29 ALL PASS. AMGT_CORPUS's
merge did not break this project's checks. Pages other than Security Analysis were not read by this seat; their owners' confirmations
stand for them.

## 6. BOTH BRANCHES, AND THE ROLLBACK PER KEY

- **The build fails:** `deploy` does not run (`needs: build`); nothing is written. The PROD branch holds the merge; this seat reverts it
  (`git revert -m 1 <merge>`, pushed to PROD) and closes the ledger RED with the cause.
- **The build passes and the deploy fails part way:** the bucket may hold a mix. **Rollback:** `git revert -m 1 <merge>` pushed to PROD.
  `deploy.yml` then rebuilds `b06863fe`'s tree and syncs it with `--delete`, so the bucket again equals that build. This is not a force
  push and not a delete by hand. The served index is read after.
- **The deploy passes:** tag read peeled to the PROD head; served index read (Last-Modified after the run; one marker present that
  exists only after the range: the `data-research-coverage` attribute, in 0 source files at `b06863fe` and 1 at
`dbeb6764`, `git grep` read at signing). Ledger closed. FWD-1's signed-in walk on PROD is then Andrew's.
- **Rollback key, stated:** the PROD branch tip after the revert has the same tree as `b06863fe`. Read with `git diff b06863fe <revert> --stat`, 0 lines.
