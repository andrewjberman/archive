# CALL -- AMGT_HARVST gold chatter rebuild: which host? (issuer 2.0.0_SA_COO~W1, 2026-10-20 ~18:4xZ)

**The decision (one word):** run the scheduled gold rebuild on **Fargate** (reuse the dossier-refresh pattern, `HVST-cn-5`/`cn-7`), or on a **container-image Lambda**?

**Why it is a call.** The CTO's round-99 analysis item 2 settles the host by one rule: "Fargate if its closure is over the Lambda limit; measure it, as cn-4 did." The measured closure is UNDER the limit, so the rule as worded says Lambda. The measured WALL TIME says the opposite. The rule did not name wall time; I do not read a rule wider than it is worded, so I ask.

**What was measured (all read by me from the worker's worktree `C:/dev/wk-harvst-189`, `deliverables/0.9.0_WK_AMGT_HARVST~189/`, NOT yet committed; worker `~189` is still running the third table; the committed evidence arrives with its merge):**
- `co5_closure.out`: `GOLD-DRIVER-CLOSURE entry=lib.research.harvest.gold_refresh lib_modules=20 third_party_pkgs=13 total_mb=207.34 limit_unzipped_mb=250 verdict=UNDER` (pyarrow 86.40, pandas 62.31, numpy 51.94). The module alone was 138.86 MB (`HVST-co-2`, merged `c356ff5849`); the driver adds the trading calendar, the roster loader and the sentiment reader.
- `co5_dryrun.out`: the FIRST of three tables, `article_security_mention`, took `wall_seconds=2715.1` (45 minutes) and read 461,381,835 bytes in 2762 requests, from dell1 over the open internet, for 67,229 rows. `chatter_daily` and `chatter_event` follow it and read the mention snapshot back.
- The in-region comparison I have: the dossier refresh took 12187 s from dell1 (`HVST-cn-3`) and 6965 s as the first Fargate fire (`HVST-cn-7`), a ratio of 0.57. Applied to 2715 s that is about 1550 s (26 minutes) in-region for the mention table alone. This ratio is an inference from a different job, not a measurement of this one.
- A Lambda stops at 900 seconds. Three tables in order cannot fit; one Lambda per table would still leave the first at about 26 minutes.

**RECOMMENDATION: Fargate**, the dossier refresh's pattern (an ECR repository, a CodeBuild image build, a cluster, a task definition by digest, an EventBridge schedule on its own clock), with the names built to LGIC (rule 30). It has no time cap, it is a pattern already running in this estate (the 14:00Z fire of 2026-10-20), and the closure is not the binding limit.

**What it gates:** `HVST-co-6` (packaging, Terraform and the schedule) and then `HVST-co-7` (the seat order). `co-6` is not cut until this is ruled, and `co-5` merges first. If the answer is Lambda, the wall-time problem must be solved first (a split build), which is a larger cell.
