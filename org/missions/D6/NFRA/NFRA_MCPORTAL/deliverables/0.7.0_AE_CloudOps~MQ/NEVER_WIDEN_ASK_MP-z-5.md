# NEVER-WIDEN ASK -- NFRA_MCPORTAL `MP-z-5`, the gateway release (FWD-20)

- **Asked by:** `0.7.0_AE_CloudOps~MQ`
- **Halves asked of:** `1.0.0_SA_CTO~Z` (CTO half) and `2.0.0_SA_COO~MP` (COO half)
- **Order:** `org/missions/D6/NFRA/NFRA_MCPORTAL/task-orders/NFRA_MCPORTAL.TO-MP-z-5.gw-gateway-release.md`
  (Amendment 2 @`2627c1905f`), `<risk>WORLD</risk>`
- **Release branch:** `rel-nfra-mcportal-gw` @`233440afaf`, cut from the LIVE base
  `185dc048881da2030efa11f4d0bfb8704b500c66`
- **Live base, read at the act from the record, never assumed:** `EC2_MANIFEST.json`
  `services.opal-gateway.deployed_commit` = `185dc048881da2030efa11f4d0bfb8704b500c66` on `box/sitez`
- **mcportal bundle:** `0e02a1f` (`0e02a1f1ab56dae65b9df29bd78f1eab319ce6a2`), descends from `bc37107`

## 1. BLAST RADIUS -- what this act may touch

| # | thing it touches | what moves |
|---|---|---|
| 1 | `app/admin_gateway_breakdown.py` | NEW file (377 lines), the breakdown handler |
| 2 | `app/admin_api.py` | +2 lines: one import, one `Route` |
| 3 | `app/server.py` | +29/-1: the deep-link handler, its route line + comment, and one import token |
| 4 | `tests/test_admin_gateway_breakdown.py` | NEW (427 lines) -- source only, ships nowhere |
| 5 | `tests/test_dashboard_deep_links.py` | NEW (178 lines) -- source only, ships nowhere |
| 6 | ONE new admin route | `GET /api/admin/gateway/breakdown`, owner-gated |
| 7 | ONE new catch-all route | `GET/HEAD/POST/PUT/PATCH/DELETE/OPTIONS /{path:path}`, LAST in the table; answers ONLY paths listed in the served bundle's `routes.json`, everything else 404 (or the replayed 307 slash-redirect) |
| 8 | the dashboard bundle | `dashboard/` swapped from mcportal `bc37107` to `0e02a1f` |
| 9 | `EC2_MANIFEST.json` `services.opal-gateway` | `mcportal_commit` pre-act; `deployed_commit`, `previous_deployed_commit`, `release_note` post-act |
| 10 | the running service | one `systemctl restart opal-gateway` on `i-07dccb1615503ac99` |
| 11 | two S3 keys | `ec2/opal-gateway/opal-gateway-<release sha>.tar.gz` (new) and `opal-gateway-latest.tar.gz` (overwritten) |

**BOTH BRANCHES of item 7 are named deliberately.** The catch-all matches EVERY path nothing above it
matches. Its answer is read from the producer's own rule (`server.py` `dashboard_deep_link`), not predicted
from the input shape: a LISTED path is handed to `dashboard_root`, which applies the owner gate first; an
UNLISTED path, any non-GET/HEAD method, and `/` itself fall to the slash-redirect replay and then a plain
404. A missing or malformed `routes.json` lists `/` only -- fail closed. There is exactly ONE writer of the
served `routes.json`: the mcportal bundle, swapped as item 8.

## 2. WHAT IT MAY NEVER TOUCH

1. **The MCP tool surface.** No tool added, removed or renamed. Read before and after; the difference must
   be EMPTY, and the count is re-read on THIS base both times, never carried from an earlier release.
2. **Any IAM.** No role, policy, trust or condition. `MP-z-4` applied the one read grant before `G-REL3`;
   this cell applies none.
3. **Any store write.** The gateway adds no store call kind; `grant_store` stays `read`.
4. **Any Terraform, ALB, listener, security group, instance, secret or schedule.**
5. **Any other service in `EC2_MANIFEST.json`.** 27 services in the file; exactly 1 (`opal-gateway`)
   differs between the release tree and `box/sitez`, and only that entry is written.
6. **`safe-ec2-deploy.sh` and `deploy-to-ec2.sh`** -- read, never edited.

## 3. CENSUS -- measured on the release branch

`git diff --name-only 185dc04888 233440afaf` over the WHOLE repo, not just the gateway dir:

```
infra/aws/ec2/EC2_MANIFEST.json                                   (1 line: mcportal_commit)
infra/aws/ec2/opal-gateway/app/admin_api.py                       (+2)
infra/aws/ec2/opal-gateway/app/admin_gateway_breakdown.py         (+377, new)
infra/aws/ec2/opal-gateway/app/server.py                          (+29 -1)
infra/aws/ec2/opal-gateway/tests/test_admin_gateway_breakdown.py  (+427, new)
infra/aws/ec2/opal-gateway/tests/test_dashboard_deep_links.py     (+178, new)
```

The gateway app/tests subset is the allowed FIVE, `outside GW's set = 0`. The sixth path is
`EC2_MANIFEST.json`, which step 1 and step 4 both require and which `<paths>` names; it is outside the
gateway dir and therefore outside AC1's `allow` regex by construction.

The GO's commits were picked in the GO's order (`0de6cfb834`, `28a7ff1904`, `e42d2c35c3`, `2da54c1d72`,
`fff1ec605a`) plus the step-0 hookup `cfb8b48bbb`. **Every pick was re-authored to this lane** -- the
owned-paths hook grants a path by the COMMITTING serial's live task order, and `0.9.0_WK_NFRA_MCPORTAL~13`
and `~15` hold none at HEAD, so `cherry-pick --continue` was refused with a lane violation on the two
`MP-z-1` files. Each source commit is named in its release-pick message. The source commits' `org/` hunks
were dropped, per Amendment 2. **Zero conflicts occurred under `infra/aws/ec2/opal-gateway/`**; the three
that did occur were all under `org/` and were resolved to the release base's side.

### 3a. ONE DECLARED DEPARTURE -- `server.py` carries THREE hunks, not two

The order says a `server.py` hunk outside *the deep-link handler, its route line and its comment* STOPS the
act. There are three hunks:

1. the `dashboard_deep_link` handler (+26);
2. its `Route(...)` line and its two-line comment (+2);
3. **one token added to one import line:** `PlainTextResponse` in the
   `from starlette.responses import ...` line.

Hunk 3 exists only because the handler's own 404 branch calls `PlainTextResponse`; without it the handler
raises `NameError` on every unlisted path. It is inside `MP-z-3`'s own graded, drained commit
`e42d2c35c3`. **This seat is not repairing the criterion and is not deciding this.** It is declared here so
each half signs with it in view, or refuses. AC1 does not read hunks, so the grading instrument is silent
on it.

## 4. ROLLBACK -- proven BEFORE the act, per key

**Key 1 -- the versioned artifact.**
`s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/opal-gateway-185dc04888.tar.gz` is present and
PRE-ACT: 543,554 B, ETag `b486e614fc122cf854f0d063bd198e4e`, metadata `git-ref` =
`185dc048881da2030efa11f4d0bfb8704b500c66`, LastModified `2026-10-12T12:51:35Z`. This key is NOT written by
this act, which writes `opal-gateway-<new sha>.tar.gz` and `opal-gateway-latest.tar.gz`. It is re-read
immediately pre-act.

**Key 2 -- `opal-gateway-latest.tar.gz`** IS overwritten by this act. Its rollback is the same redeploy,
which rewrites it from the base tree.

**The rebuild, run and measured, with nothing uploaded.** A clean detached worktree at the live base
(`C:/tmp/mp-z5-rb`, 0 local changes, with `admin_gateway_breakdown.py` ABSENT -- the control that it really
is the pre-release base) and mcportal detached at the base's own bundle `bc37107`:

- bun cache pre-check against `bc37107`'s own lockfile: **77 of 77, rc=0** -- no package fetched;
  `bun install --frozen-lockfile && bun run build` then ran fully offline, rc=0, `dist/index.html` present.
- the artifact was re-tarred with `deploy-to-ec2.sh`'s exact member list and exclude set.
- **Rebuilt vs the live artifact downloaded from S3: 543,554 B vs 543,554 B; 132 members vs 132, member-list
  diff 0; 109 files compared by md5, 109 EQUAL, 0 DIFFERENT, 0 only-in-either.**
- **NEGATIVE CONTROL, so the comparison is known to discriminate:** the same md5 walk against the RELEASE
  tree's `app/` reads 98 EQUAL, **2 DIFFERENT (`admin_api.py`, `server.py`) and 1 only-in-release
  (`admin_gateway_breakdown.py`)** -- exactly this release's payload, and nothing else.

**The command that would re-deploy it** (named, not run; from the clean base tree, with the then-live ref
declared so the stale-base guard can pass):

```
cd /c/tmp/mp-z5-rb && DEPLOY_BASE_REF=<the release commit then live> \
  bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh
```

No Terraform, no ALB, no host, role or secret change is involved in either direction.

## 5. READ-BACKS -- each independent of the deploy's rc

- `/health` polled immediately after the restart; **not 200 within 90 s means the rollback above runs AT
  ONCE**, the ledger entry closes as rolled back, and the act stops.
- **AC1** (`checks/z5.AC1.sh`): the `nfra-mcportal-gw-release` entry committed at HEAD, its sentinel gone,
  `deploy_ledger.py list` not listing it with its SCAN DENOMINATOR printed; `deployed_commit` descends from
  `previous_deployed_commit`; the gateway app/tests files between them are ONLY the five; the
  `mcportal_commit` tree holds `src/pages/gateway/` and `public/routes.json` -- both already verified
  present at `0e02a1f`.
- **AC2** (`checks/z5.AC2.sh`, on the host over SSM): `/health` 200; with NO identity the breakdown route and
  `/control-plane`, `/open-calls`, `/gateway` each 401 or 403 -- **not 404**; an unlisted path 404; and the
  served module's own `_compute`, under the instance role, returning at least 2 channels, at least 1 tool,
  0 duplicate tools, at least 1 held channel and `grant_store=read`, in 30 s or less.
- **MCP tool surface:** the registered tool names listed on the host before and after, both counts recorded,
  the difference EMPTY.

## 6. THE ONE THING THIS SEAT CANNOT SATISFY AS WRITTEN -- step 1's "0 failed"

Row **`NFRA_MCPORTAL-Z-S45`** carries the full measurement. In short: on the release tree the named test set
reads **67 passed, 7 failed**; the SAME payload bytes on `box/sitez` HEAD read **87 passed, 0 failed**.
Payload held constant, base varied, outcome flipped -- so the 7 are a property of the RELEASE BASE's
non-payload tree, not of this release.

- **Five** read repo data files that **do not exist in the base commit at all** --
  `org/devices/DEVICES.json` and the `cp2` capture fixture both read `ls-tree` = 0 at the base and 1 at
  `box/sitez` -- and they sit in four test files this release does not modify.
- **Two** are `MP-z-1`'s own tests encoding the post-`OG-tg-1` world: `app/identity_scope.py` on the base
  still carries the `_SEED` grant for `opalbloomberg@opalinvest.com` (including `whoami`) that the trunk
  removed on 2026-10-09, so that principal really IS an m365 holder on the live base and the handler
  reports it truthfully. A control that swapped only `identity_tool_allowlist.txt` to the trunk's version
  did NOT fix them, which is what located the cause in `identity_scope.py` rather than the allowlist file.

**This seat is not repairing the criterion and is not waiving it.** The act is held until each half says
which it signs:

- **(a)** accept the 7 with their causes named, because none is reachable by this payload; or
- **(b)** grade "0 failed" where the tests' inputs exist -- `box/sitez` HEAD, already measured at
  87 passed / 0 failed -- and on the release tree require only that no test NEWLY fails relative to the
  base's own pre-release run; or
- **(c)** something else, including refusing the act.

## 7. WHAT IS ASKED

Each half, citing this ASK by path and commit:

- `1.0.0_SA_CTO~Z` -- the CTO half, at
  `org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/1.0.0_SA_CTO~Z/NEVER_WIDEN_HALF_CTO_MP-z-5_20261013.md`
- `2.0.0_SA_COO~MP` -- the COO half, at
  `org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/2.0.0_SA_COO~MP/NEVER_WIDEN_HALF_COO_MP-z-5_20261013.md`

Each half please also state its disposition of **section 3a** (the `server.py` import hunk) and
**section 6** (step 1's "0 failed"). A refused half STOPS the act.
