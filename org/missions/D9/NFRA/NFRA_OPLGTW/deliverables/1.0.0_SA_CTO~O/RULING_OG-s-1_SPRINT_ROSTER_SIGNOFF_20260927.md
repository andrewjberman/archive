# OG-s-1 -- never-widen sign-off, CTO half (1.0.0_SA_CTO~O, 2026-09-27 ~21:3xZ)

**Act:** `NFRA_OPLGTW.TO-OG-s-1.sprint-owner-only` (@95e499c916). Release `6a98a0553a` = live `fe94911257` plus one
file, `deploy-to-ec2.sh` (+2/-1). Deployer `0.9.0_WK_NFRA_OPLGTW~9`; issuer `2.0.0_SA_COO~O`. PHASE A:
`deliverables/0.9.0_WK_NFRA_OPLGTW~9/ANNOUNCE_OG-s-1.md`, drained @ce32a3ddef.
**Authority:** Andrew-direct ~19:5xZ, "call 1 yes rec approved" (record @785fc4d71f); the arming term for the halves.
**Second half owed:** `3.0.0_SA_CVO~O`, a non-acting seat.

## What changes (read from `git diff fe94911257 6a98a0553a`)

- One comment line, plus the host `.env` printf, which now emits `SPRINT_VIEW_ALLOWED_EMAILS=andrew@opalinvest.com`.
  That is the only new key: the rendered file goes from 27 to 28 lines. `ENABLED_INTEGRATIONS` and every other line are
  byte-unchanged, per PHASE A's render check.
- No `app/` file changes, so the tool list stays 46 = 46.

## The reader, and every route it guards

- `config.py:103-104` parses the value into a lower-cased frozenset.
- `sprint_view._allowed` (`:173-175`): an empty set admits everyone, a non-empty set admits members only.
- It is called by `sprint_page` (`:182`), which serves `/sprint` and `/sprint/{day}`, and by `sprint_archive`
  (`:222`), which serves `/sprint/archive`.
- `/sprint/` is `sprint_redirect`, a 307 to `/sprint` that serves no content.
- So all 4 routes (`server.py` `Route("/sprint" ...)` x4) are covered.
- The viewer's email is lower-cased at the source (`identity.py:66`, the `alb_oidc` path).

## Writers of the named property (NEVER-1: count them)

The named property is the `/sprint*` answer. **N = 3:**
1. The code: unchanged by this act.
2. The host `.env` roster: written by `deploy-to-ec2.sh` on EVERY deploy (this act, and every later release, which
   is why the line goes in the template), or by a hand edit.
3. The S3 day pages written by `publish_daily_report.py`: unchanged.

## Both branches (from `_allowed`)

- **Andrew (`andrew@opalinvest.com`):** admitted, so today's answer is unchanged.
- **Any other signed-in tenant account:** 403 "Not on the Daily Sprint roster", where today it is served. This is a
  NARROWING, on Andrew's word. Nothing widens.
- **The one bad branch is an owner lockout.** It happens if the ALB claim for Andrew ever differs from
  `andrew@opalinvest.com`. The same literal is already the owner-gate roster and `OTP_MAILBOX`. It is still covered
  below.

## Rollback, per key

- **Code/config:** redeploy `fe94911257`'s artifact (79 of 79 identical to live, per PHASE A).
- **Owner lockout, fastest path:** remove the one `.env` line over SSM and restart. This is an act by this seat's
  fabric on Andrew's report.
- **Data:** none written.

## Guards at GO

- Host md5 of the 4 app files equals `fe94911257` before the act.
- The mcportal HEAD equals the manifest pin.
- The live `ENABLED_INTEGRATIONS` literal is unchanged before the act.
- **The rendered `.env` carries EXACTLY ONE new line, `SPRINT_VIEW_ALLOWED_EMAILS=andrew@opalinvest.com`**: diff the
  on-host `.env` KEY SET before and after; values other than this key are not printed.
- After the act: `/health` 200, md5 equals the release, tool list 46 = 46.
- The NEVER-2 ledger is opened before and closed after.
- Off-hours; announced through `0.0.0_AB_MSTR~Z` and the agentbus.

**CTO half: SIGNED**, for the act above as bounded here, by `1.0.0_SA_CTO~O`.
