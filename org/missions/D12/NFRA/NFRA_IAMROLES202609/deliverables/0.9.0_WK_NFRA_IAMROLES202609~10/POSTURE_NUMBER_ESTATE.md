# POSTURE NUMBER -- the estate, 219 roles (TO-IAM-u-1)

POSTURE: only 1858 of 5494 granted permissions (33.8 percent) could be observed at all, and of those 421 (22.7 percent) were used in the 90-day lookback; 3636 (66.2 percent) are unobservable -- denominator = 5494 permission grants across 219 roles at Path "/", as of 2026-09-10 (lookback 90 days), excluding the 10 service-linked roles at Path "/aws-service-role/".
POSTURE-EXCL-CODEBUILD: without opal-drift-producer-codebuild-role, 1113 of 2576 granted permissions (43.2 percent) could be observed and 418 of those (37.6 percent) were used; 1463 (56.8 percent) are unobservable -- denominator = 2576 grants across 218 roles at Path "/", as of 2026-09-10, excluding the 10 service-linked roles.

Read the EXCL-CODEBUILD line first: one role carries 2918 of the 5494 grants off a single AWS-managed ReadOnlyAccess attachment, and dominates every all-role aggregate.

## The answer to "are we following least privilege?"

Not shown either way for two-thirds of the grants. Figures (recomputed by `posture-rollup.py` from the committed bundle `permission-cold-raw-bundle.json`, no cloud call):

| | roles | granted | used | never-used | unobservable |
|---|---|---|---|---|---|
| all | 219 | 5494 | 421 | 1437 | 3636 |
| excl. codebuild | 218 | 2576 | 418 | 695 | 1463 |

Three numbers are kept in view together (C-COVERAGE-OVER-COUNT):
1. Observable share of all grants: 1858 of 5494 (33.8 percent); excluding codebuild 1113 of 2576 (43.2 percent).
2. Used share of the observable grants: 421 of 1858 (22.7 percent); excluding codebuild 418 of 1113 (37.6 percent).
3. Unobservable share: 3636 of 5494 (66.2 percent); excluding codebuild 1463 of 2576 (56.8 percent).

Why this figure: used-of-observable alone would read as a verdict on the whole estate, but it speaks for a third of it. Observable-share alone says nothing about use. So the headline gives both and the unobservable share. The ratio never-used/granted (1437 of 5494) is deliberately NOT the posture: it counts the unobservable grants as if they were clean, which the instrument did not show.

Per role (all 219): 27 roles have no observable grant at all, 21 have observable grants that were all used, 171 have at least one observable grant never used in the lookback.

This document recommends nothing and changes nothing (C-NO-ACCESSDENIED); it speaks to the permissions axis only. The round-1 one-role posture (opal-data-refresh-lambda-role) is a different object and is not cited as an estate figure.

## Population qualifier

219 is every live role at Path "/": 229 roles in the account (313476888478) at 2026-09-10 minus the 10 service-linked roles at Path "/aws-service-role/", which are excluded and named in the bundle's population_rule. The figure carries that qualifier wherever it is quoted.

## Since then

The figure is as of 2026-09-10. The live role graph read 283 IAM_ROLE nodes at 2026-10-09 03:31 UTC. That is a different instrument and it counts service-linked roles too, so 283 against 219 is not a like-for-like delta; but the population has moved. This document does not recompute against AWS; a fresh run is a separate cell (IAM-u-2). Until then, treat the figures above as a 2026-09-10 reading only.
