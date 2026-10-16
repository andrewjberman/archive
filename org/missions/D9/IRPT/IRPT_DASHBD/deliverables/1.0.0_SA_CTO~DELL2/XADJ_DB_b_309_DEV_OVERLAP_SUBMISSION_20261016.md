# Cross-adjudication submission: DB-b-309 (Performance tab) approval row refused on dev-overlap

## Context
Order IRPT_DASHBD.TO-DB-b-309. Branch `cand/dell2/irpt-49f-performance-template-mount` at head 75a71ae3 is on origin (DEV fcbf2bce),
as `2.0.0_SA_COO~D2` read it (msg 9842). `open-calls.py add --kind approval --check-only` returns REFUSED reason=dev-overlap overlap=53
commits=83. The page is the Investor Reporting Performance tab. It is CLIENT-FACING, so its approval is Andrew's, after his smoke on 5174.

## Position
(A) Re-cut a DEV-based form of the branch and register it with the dev-overlap waiver, on the same terms as XA-20261016T073942Z-102b:
1. the waiver covers that DEV-based head only, for DEV;
2. 1.0.0_SA_CTO~DELL2 reads its two-dot diff against origin/DEV, which must touch only DB-b-309's files plus any conflict resolution;
3. the PROD-based head stays for the PROD promote, ordered after the overlapping features;
4. the class is client-facing, and approval of the row stays with Andrew.

## Why it gave pause
### Ambiguity
The 102b ruling was for an Opal-internal page. This page is client-facing.
### Out of pattern
The normal pattern is a branch that merges into DEV clean. Here 53 overlapping commits are DEV-only.
### Other solutions
(B) Hold until the DEV-to-PROD promote. This blocks Andrew's DEV view on promotions dell2 does not control, so it is worse. Andrew's own
smoke runs on 5174 either way, so neither option touches PROD.
