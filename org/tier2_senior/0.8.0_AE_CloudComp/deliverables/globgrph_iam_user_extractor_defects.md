# DEFECT REPORT — globgrph `IAM_USER` extractor: 4 real users missing, 2 non-users admitted

**Raised by:** `0.8.0_AE_CloudComp` (base) · 2026-07-25 · at `1.0.0_SA_CTO~Z`'s instruction (183918Z,
reaffirmed 185814Z as *"unaffected and still wanted — accuracy defects, not governance"*).
**Filed here pending CTO~Z's answer on where it belongs**; move it freely, nothing depends on this path.

Surfaced while re-deriving the grain baseline. **These are accuracy defects and explicitly NOT governance**
— unaffected by the 2026-07-25 Andrew-direct ruling that no comp-tool may carry a governance predicate.

## SYMPTOM — fully grounded against live, 2026-07-25

```
graph IAM_USER (4):  Andrew_Berman, github-actions-portal, root, token.actions.githubusercontent.com
live  IAM_USER (6):  Andrew_Berman, Andrew_Berman_1, github-actions-portal, opal-portal-dashboard,
                     Opal_Terminal, patricia@thewhitelabelcreative.com

OVERLAP                            2
DEFECT (a) real users MISSING      4   Andrew_Berman_1, Opal_Terminal, opal-portal-dashboard,
                                       patricia@thewhitelabelcreative.com
DEFECT (b) NON-USERS admitted      2   root, token.actions.githubusercontent.com
```

Both non-users verified live, not inferred:

| node | probe | result |
|---|---|---|
| `root` | `aws iam get-user --user-name root` | **`NoSuchEntity`** — the account root is not an IAM user |
| `token.actions.githubusercontent.com` | `aws iam list-open-id-connect-providers` | **`arn:aws:iam::313476888478:oidc-provider/token.actions.githubusercontent.com`** — an OIDC **provider** |

Live denominator: `aws iam list-users` (us-east-1), 6 users. Graph side: `comp-kuzu` `node_type='IAM_USER'`,
and independently confirmed at 4 in the published `stitch_graph.json` (2026-07-25T18:44:34Z).

**4 is NOT 6-minus-2.** It is 2 right things plus 2 wrong-*kind* things. CTO~Z withdrew their original
"under-count" characterization on this evidence: *"a count comparison cannot detect a population
mismatch — and the arithmetic looked plausible the whole way."*

## SEVERITY — (b) is the worse one, per CTO~Z

*"A type confusion means the extractor's `IAM_USER` predicate is admitting non-users, which likely
affects more than this one class."* Concur: an under-count is a coverage gap, but a predicate admitting
the wrong **kind** of entity is a correctness fault that can repeat wherever that predicate's shape is
reused.

## MECHANISM — ⚠ **NOT LOCATED. HYPOTHESIS ONLY. THIS CANNOT AUTHORIZE A FIX.**

**Single-cause hypothesis that would explain BOTH defects at once:** the extractor may derive `IAM_USER`
from **principals appearing in IAM policy documents / trust relationships**, rather than from
`iam:ListUsers`.

- It would explain **(b)**: `root` and an OIDC provider are exactly the things that appear as
  *principals* in trust policies but are not users.
- It would explain **(a)**: a real user who never appears as a principal in any policy would simply
  never be seen.

One cause, both symptoms, no coincidence required — which is what makes it attractive and therefore
what makes it worth distrusting until confirmed.

**THE DISCRIMINATING TEST** (cheap, and it kills the hypothesis if wrong): check whether the 4 missing
users appear as principals in any trust/resource policy. If none do, the hypothesis survives; if some
do, it is dead and the cause is elsewhere.

**Search denominators, so the next person does not repeat them:**

| search | scope | result |
|---|---|---|
| `comp-grep "IAM_USER"` | `infra/aws/globgrph` (76 files) | **1 hit** — `derive_runner.py:1729`, a class→source *mapping table only*, not an emission site |
| `comp-grep "iam_user"` | `infra/aws/globgrph` (76 files) | **0 hits** — despite `iam_user` being a real key in the produced artifact |
| `comp-grep "iam_user"` | `infra/aws/lambda/globgrph` (2 files) | **0 hits** |
| `comp-grep "list_users"` | `infra/aws` (6,170 files) | 3 hits, **all security scanners** (`access-anomaly-scanner`, `security-sweep-comprehensive`, `security-sweep-daily`) — none is the graph extractor |

**Why it is not locatable from here:** `derive_stitch` consumes a pre-built AWS snapshot
(`snapshots/20260725/graph-20260725.tar.gz`), so the node data is produced **upstream of this repo's
searched surfaces**. The emitter is somewhere I did not reach. I am not guessing at it.

## WHAT I DID NOT DO

Did not fix, did not touch the extractor, did not edit `sovereign_held.py` (hard prohibition, 185814Z —
and note this report is the *accuracy* class, which that prohibition does not cover). Did not adjudicate
severity beyond agreeing with CTO~Z's ordering.

## STATUS OF THE RELATED BASELINE

`IAM_USER` was **provisionally baselined at 4** (landed by CTO~Z `@fc8b81ec0`), with the
`verified_reason` naming the composition explicitly and never the phrase "under-read." Provisional
because it does not obstruct this repair: when the extractor is corrected to emit the true 6, that is
**6/4 = 1.50x**, inside `[0.4, 2.5]`, so the sentinel will not trip on the fix. **This entry should be
superseded when (a) and (b) close.**
