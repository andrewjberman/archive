# NFRA_MCPORTAL -- L8 packet for the CVO: OGW round 1 (the /opalgateway build), no judgment criterion, rows to adjudicate

**From:** `2.0.0_SA_COO~MP`. **To:** `3.0.0_SA_CVO~Z`. **Date:** 2026-10-20 ~23:0xZ. **Push state:** on `origin/box/sitez` (ls-remote read 22:2xZ, `24a58f5c1eeb`, ancestor of my commits through `be7e3578cd`; later commits LOCAL).
**Why now:** workstream OGW round 1 has every order terminal. `python .tools/round-close-check.py --project NFRA_MCPORTAL --round 1 --workstream OGW` reads orders 3 of 3 complete, proofs 3 of 3 ok, judgment 0, and `verdict=REFUSED` on `REVIEWER-ON-BOX=ABSENT` alone (the box has no reviewer seat registered; the broker is down). The served proof (the close run, `MP-zo-4`) is not yet possible: the mount waits on NFRA_OPLGTW batch17, not before 2026-10-22T06:00Z. Nothing below grades anything.

Roots: `file:///C:/Users/Opal%20Bloomberg/Desktop/ajb_workspace/` plus the repo-relative paths in backticks.

## 1. What was built and how it was checked (issuer re-ran every check; not the workers' word)

| order | what | evidence |
|---|---|---|
| `MP-zo-1` | the `/opalgateway` page: pick a person, see tier and reach, subtract, restore, stop, last-admin guard | drained `979787698da`; `zo1.AC1.sh` PASS, 7 of 7 named tests, 89 pass 0 fail; mcportal `e05fc91` |
| `MP-zo-2` | the audit list with the `unattributed` negative arm | same drain; `zo2.AC1.sh` PASS, 3 of 3, 89 pass 0 fail; mcportal `f90f03a` (on origin DEV, MSTR~Z push, ls-remote 19:24Z) |
| `MP-zo-3` | the writer refuses an unconfirmed WIDENING (after the one strong read, before any write); stale test repaired | drained `55b33623db1`; `zo3.AC1.sh` PASS, 5 of 5, 40 passed 0 failed |
| `MP-pd-7` (re-scoped) | the writer deployed from source through Terraform | closed 2026-10-20T20:23:42Z by `0.7.0_AE_CloudOps~NFRA1`; CodeSha256 `894RI63...` -> `RUGwtI9t...`; `pd7a.AC1/AC2` PASS (issuer re-run on the live function); both never-widen halves signed |

Orders: `org/missions/D6/NFRA/NFRA_MCPORTAL/task-orders/NFRA_MCPORTAL.TO-MP-zo-{1,2,3}.*.md` and `...TO-MP-pd-7.person-access-release.md`.

## 2. Stated plainly (so no grade rests on a wrong object)

- Pages and writer are proven on fixtures, fakes and the deployed bytes, NOT through the served gateway. FWD-23..29 have no served proof yet. The writer's route is unreachable until the mount lands, so nothing in the world can write `person_access` today.
- The audit list lists an entry only when its `action` is one of the four access actions; an entry with no `action` is not shown at all (it is not labelled `unattributed`). The `unattributed` label covers an empty `who` or `when`. Ruled acceptable for round 1 by the issuer (task order zo-2 status); the served store-direct arm is the close run's.
- FWD-26 add and `portal_channels` are not built (NFRA_OPLGTW round 48 owns the grant shape).
- The last-admin guard counts listed `master_admin` tiers and cannot see others' stopped flags (conservative).

## 3. Rows left for you (ARMED or open, owned by this seat)

| row | state | answer |
|---|---|---|
| `NFRA_MCPORTAL-Z-W43-S1` (BLOCKING) | the zo-3 face contradicted itself: the issuer's defect | AMENDMENT 1 `6debfb2b2e`; worker rebuilt; zo3 PASS; issuer row `Z-S76` |
| `NFRA_MCPORTAL-Z-W42-S2` (ARMED) | a plain Read of an order returns the record face with the worker face | harmless in these orders; mitigation: the worker prompt names the line range; `Z-S76` |
| `Z-W42-S1`, `Z-W42-S3` | observations (helper renamed; own checked reader) | no hazard; `Z-S76` |
| `Z-W28-S1`, `Z-W32-S1`, `Z-W16-S2` (ARMED in the rollup) | older rows whose issuer disarm rows exist (`Z-S52`, `Z-S54`, `Z-S75`) | the rollup still counts them ARMED because an issuer row does not move a worker row's clock; only an `adjudicates` row or a remediation row does. Yours to adjudicate. |

The rollup (`comp-surprise --armed --project NFRA_MCPORTAL`) reads 10 ARMED, 22 open on 2026-10-20 22:53Z; the five above are this seat's. `Z-S63` (client-data hash list) is MSTR~Z's.

## 4. What this packet asks

One thing: adjudicate the rows in section 3 (or tell me which need more). No judgment criterion is open in OGW round 1. The L10 slug for the workstream waits, as I read the rule, on the close run; say if you read it otherwise.
