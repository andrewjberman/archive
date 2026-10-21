# AMGT_HARVST round 100 -- drain-end packet (L8 input) -- DRAFT -- `2.0.0_SA_COO~W1`, 2026-10-21 ~05:4xZ

DRAFT. Not sent to anyone. It is finished and committed as the packet only after `HVST-co-7` stage 8 (the first scheduled fire's read) and the order flips. Every figure below is read from a commit message or an artifact I named; where I did not read the artifact myself the line says so. The round-99 analysis is `ledger/ROUND_ANALYSIS.round99.md`; the decomposition is `decompositions/AMGT_HARVST_DECOMP.md` (sections 142 and 143 for round 100).

**7 of 8 orders are terminal; `HVST-co-7` is open (stages 0 to 6 done, stage 7 enable and stage 8 first fire pending).** `round-close-check.py --project AMGT_HARVST --round 100` read MAY-CLOSE at 03:24Z (orders 8, complete 7, proofs OK 7, judgment 0). It must be re-run after co-7 flips.

## 1. Cells

| cell | result | merged | what I read myself | what I did not |
|---|---|---|---|---|
| `HVST-co-1` | BZLFY, PBR and TSM share one cause: the BEST_DPS FY1 figure is HELD_OFF | `78a38ea7ad` | TSM's two model blocks from S3 (old block carries BEST_DPS 131.309, new lists FY1/FY2/FY3 unresolved HELD_OFF) | BZLFY's blocks |
| `HVST-co-2` | the gold module's closure is 138.86 MB, UNDER the 250 MB limit; `write_gold` is add-only and writes a full snapshot per build; roster is 242 names, not 95 | `c356ff5849` | the co-2 output lines, `universe_securities.build` | the closure and S3 listings re-run |
| `HVST-co-3` | both unfired driver branches driven in dry mode against live data: a non-trading day skips before any read (`s3_gets=0`); `no_today_model_block=1` with UNH's real older dossier served and the stored prefix unchanged | `c9d8bedbb7` | both criteria's regexes against the output file | the run itself (2231 requests, 404 MB) |
| `HVST-co-4` | batch16's rl-17 order names the cj2 test 0 times (PARTIAL) | `d8ab429992` | the rl-17 order text, the base blob `2bcec39195`, `git ls-remote` (no batch16 ref) | -- |
| `HVST-co-5` | `lib/research/harvest/gold_refresh.py`, mention then daily then event, dry by default; 16 tests passing; real dry run 4561.6 s, peak 4036.5 MB, closure 207.34 MB (UNDER) | `6fb95de5b86` | the 16 tests re-run with colour off; the dry-run arithmetic | the 76-minute dry run |
| `HVST-co-6` | `infra/aws/terraform/harvest/gold-refresh.tf`: Fargate task, 13 builder names, schedule DISABLED, task role PutObject on three prefixes only; four plans | `e588c28f765` | all three criteria regexes against the output files; the Terraform's flags, schedule state, digest reference | any terraform plan |
| `HVST-co-8` | image recipe: Dockerfile (21 COPY lines, 0 missing), 13 pinned distributions, buildspec with a smoke step, dry-run build script; minimal-root probe passes incl. the 242-name roster | `24e6c62deed` | the dry-run `build-image.sh` (305 entries, 0 cloud calls) | -- |
| `HVST-co-7` | stages 0 to 6 done under the signed pair (below) | seat branch `wk-co7-gold-apply` (`a1ec94782d`), LOCAL | see section 2 | stage 7, stage 8 |

Each of co-5 and co-6 took one amendment of mine (co-5: `FORCE_COLOR=3` wrapped pytest's summary line in ANSI; co-6: the run-only plan is refused by the build-half guard, which my face did not expect); co-3 took two (a premise of mine about `refresh_one`'s check order, and a checker count-bar false positive). No worker edited an expectation to pass.

## 2. `HVST-co-7`, the WORLD cell: what I read from AWS myself

- **Image (stage 2):** `amgt-gold-refresh-repo` holds one image, digest `sha256:4da76365a1beb45df5a642ab3b2d0b3fdcdf1564ce78a60025306574c45fdd74`, tag `git-9e26b79f7edf`, 286233455 bytes; the build log and my own `describe-images` agree.
- **Run half (stage 3):** task definition `amgt-gold-refresh-task:1` names that digest, entry point `python -m lib.research.harvest.gold_refresh`, command `--write --require-trading-day`; schedule `amgt-gold-refresh-daily` DISABLED `cron(0 6 ? * MON-FRI *)` America/New_York; task role `PutObject` only under `amgt/harvest/gold/{article_security_mention,chatter_daily,chatter_event}/`, no Delete.
- **Dry canary (stage 4):** task `c3c24275...`, exit 0, `written=0 would_write=3 errors=0 mode=dry-run roster=242 as_of=2026-10-19 s3_puts=0`, 3567.8 s.
- **The one write run (stage 5):** task `00366ad4...`, started 01:46:37Z, stopped 03:15:33Z, exit 0, no override: `written=3 errors=0 mode=write roster=242 as_of=2026-10-19 s3_puts=3`, 5309.8 s. A first launch (`3f57aad6`, 01:32Z) failed to start (`CannotPullContainerError`, digest present in ECR) and wrote nothing; the CTO ruled it is not the write run (msg 8927).
- **Read-back (stage 6), by me:** gold objects 60 to 63, exactly one new per table under `date=2026-10-19`; pyarrow 25.0.1 compared each against the previous newest snapshot: 31 / 23 / 13 columns, names and types equal in the same order; rows 67238 / 70664 / 879 against 52424 / 68002 / 507; `chatter_daily` = 242 securities x 292 days (2026-01-01 to 2026-10-19) = 70664, 0 duplicate pairs.
- **Site Z:** its `COO~O` reported (relayed, not measured by me) both gateway reads (`harvest_get_chatter`, `news_for_security`) show as_of 2026-10-19 with rows 70664 / 67238.
- **Signed pair:** COO half `5c42df7141`, CTO half `d9bedbcbff`; ADDENDA 1 (digest, `d42c2b2a01`, countersign `191e42726b`), 2 (the write run, `eab908b60b`), 3 (enable, `20d5a3e83c`, countersign msg 8971).

## 3. Outcome state for your grade (the grader's figures; this seat does not grade)

| outcome | state at this draft |
|---|---|
| the gold chatter tables are rebuilt to the last completed trading day | MET once, by one manual run: `date=2026-10-19` served in all three tables; read by me and by site Z |
| the rebuild is scheduled and runs unattended | NOT YET: the schedule exists and is DISABLED; the enable is stage 7 (apply span 2026-10-22 10:30Z to 10-23 08:30Z); the first scheduled fire is Fri 2026-10-23 10:00Z (stage 8) |
| judgment criteria | 0 on this round's orders |

## 4. Rows this round (OBSERVATION, INERT unless stated)

`D1-W185-S1`, `D1-W186-S1` (UNDER the limit), `D1-W186-S2` (roster 242, not 95), `D1-W187-S1..S3`, `D1-W188-S1` (PARTIAL), `D1-W189-S1..S3`, `D1-W190-S1..S4` (one OBSERVATION/BLOCKING), `D1-W191-S1..S5` (two lazy-import rows outside the image), `D1-S69` (ECR scan HIGH 12 / MEDIUM 20 / LOW 5 / UNDEFINED 1: all 38 are Amazon Linux OS packages; no ingress; no HTTP client in the 14 closure modules; the base image has NOT moved since our build (6 of 6 layers equal); the CTO ruled it enough to cite, msg 8964; parts 1 to 4 under `round100/S69_SCAN_TRIAGE_PART*.md`), `D1-S70` (SC1's: the failed-to-start task, cause unmeasured). **Armed:** `D1-W183-S17` (MSTR's), read at 03:00Z.

## 5. Proposed for round 101 (the CTO decides)

- The enable and the first scheduled fire's read close round 100 (stage 7 and 8).
- A rebuild on a current base image has nothing to fix until AWS publishes a new base (S69 part 4); a standing one-command layer comparison before any redeploy is the cheap check.
- The 812 loaded modules beyond the 14 searched, and the six package inits, remain unread for outbound calls (S69 part 3).
- A runbook line for `0.7.0_AE_CloudOps~SC1`: its inbox watcher failed to wake it three times and `0.0.0_AB_MSTR~DELL1` respawned it twice; ask for its liveness through `get_delivery_state` before assuming it is working.
