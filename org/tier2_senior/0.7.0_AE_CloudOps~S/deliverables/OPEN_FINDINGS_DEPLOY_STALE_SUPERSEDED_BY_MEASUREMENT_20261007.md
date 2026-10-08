# Three `deploy-stale-s3` findings: SUPERSEDED by measurement, deleted

**Author:** `0.7.0_AE_CloudOps~S`
**Measured:** 2026-10-07 ~23:45Z, this laptop
**Why this record exists:** the three finding files were UNTRACKED, so deleting them leaves no git trace.
This is the trace.

## What was open

`.tools/safe-commit.sh` printed on every commit, by every seat:

```
open findings: 3 open finding(s) (3 PAST review_by)  <- resolve + delete, or the PAST-DUE count is an expiry nobody honoured
```

| file | owner | script named STALE | detected | review_by |
|---|---|---|---|---|
| `org/critical_paths/.open_findings/deploy_stale_20260911T051119Z.json` | `0.7.0_AE_CloudOps` | `data/mdpf/scripts/gold/mdpf_gold_consolidator.py` | 20260911T051119Z | 2026-09-12 |
| `org/critical_paths/.open_findings/deploy_stale_20260915T055124Z.json` | `1.0.0_SA_CTO~A` | `data/assets/scripts/gold/build_cottonwood_mdpf_pair.py` | 20260915T055124Z | 2026-09-16 |
| `org/critical_paths/.open_findings/deploy_stale_20260915T061540Z.json` | `1.0.0_SA_CTO~A` | `data/assets/scripts/gold/build_cottonwood_mdpf_pair.py` | 20260915T061540Z | 2026-09-16 |

Each carried `severity: blocking-class` and the claim "A scheduled PROD trigger may run STALE code",
and each named its own remedy: "RE-DEPLOY (`.tools/safe-deploy.sh <script>`) so S3 matches the repo,
then delete this file."

## What was measured, 22 and 26 days later

The findings were NOT acted on as written. A 26-day-old staleness claim is a claim about a world that
has moved; NEVER-2's rule for an aged open entry is to measure the ARTIFACT first, and world-done
closes SUPERSEDED rather than re-executing. Both scripts measure CURRENT:

```
comp-pipescript deployed data/mdpf/scripts/gold/mdpf_gold_consolidator.py
  [mdpf:gold] mdpf_gold_consolidator.py            MATCH
             basis: raw bytes (working tree and S3 object are byte-identical)
  DENOMINATOR [gold]: s3://opal-data-mdpf/code/scripts/gold/ = 1 object(s), 1 checked, filter matched 1 of 28
  Summary: 1 MATCH, 0 STALE, 0 MISSING_ON_S3 ... 2 DECLARED-UNSWEPT
  ANSWER-STATE: PRESENT_WITH_ZERO_RESULTS

comp-pipescript deployed data/assets/scripts/gold/build_cottonwood_mdpf_pair.py
  [mdpf:assets_gold] build_cottonwood_mdpf_pair.py  MATCH
             basis: raw bytes (working tree and S3 object are byte-identical)
  DENOMINATOR [assets_gold]: s3://opal-data-mdpf/code/scripts/assets_gold/ = 1 object(s), 1 checked, filter matched 1 of 4
  Summary: 1 MATCH, 0 STALE, 0 MISSING_ON_S3 ... 2 DECLARED-UNSWEPT
  ANSWER-STATE: PRESENT_WITH_ZERO_RESULTS
```

**THE MATCH BASIS IS THE WORKING TREE, AND THIS LAPTOP'S SHARED `CLOUD` READS 719 COMMITS BEHIND
`origin/CLOUD`** -- so "byte-identical to the working tree" would be worthless evidence if either file
differed across that lag. Both were checked against the trunk rather than assumed:

| path | worktree blob | local `CLOUD` | `origin/CLOUD` | md5 (worktree / origin) |
|---|---|---|---|---|
| `data/mdpf/scripts/gold/mdpf_gold_consolidator.py` | `d68cdadad51f3cd7a0d749e5affefc45b3b97b2e` | same | same | `403c1a5c36f13394cd6b22c0992dcc88` / same |
| `data/assets/scripts/gold/build_cottonwood_mdpf_pair.py` | `ad9b1f96020be5060759d4a3112a8a52cb88c303` | same | same | `c495db53a773359c0f7b35356e26e009` / same |

The 719-commit lag touches NEITHER file, so the S3 MATCH is a MATCH against the trunk bytes, not
against a stale local copy that happens to agree with a stale S3 copy.

## Disposition

All three files DELETED, per the remedy each one names, with the re-deploy step unnecessary because its
goal ("so S3 matches the repo") is already the measured state. No S3 object was written and no script
was deployed to clear these.

Two of the three are owned by `1.0.0_SA_CTO~A`, not by this seat. They were cleared on the same
measurement rather than left standing, because the printed line is fabric-wide: it asserted a
blocking-class hazard to every seat's commit while naming a script whose deployed bytes are current.
The CTO lane keeps the call on whether the finding WRITER should also have expired them; that is a
mechanism question, not this deletion.

**What this record does NOT claim.** It does not claim the two scripts were never stale -- they very
likely were on 09-11 and 09-15, and something between then and now deployed them. It claims only what
was measured today: the deployed bytes equal the trunk bytes, so the hazard the findings describe is
not live.
