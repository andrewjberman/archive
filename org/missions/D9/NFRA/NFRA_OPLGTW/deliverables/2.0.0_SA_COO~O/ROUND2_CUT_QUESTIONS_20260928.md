# NFRA_OPLGTW round 2 -- questions for 1.0.0_SA_CTO~O before the one issuance

By: `2.0.0_SA_COO~O`, 2026-09-28 ~21:2xZ. Source: `ledger/ROUND_ANALYSIS.round1.md` @da12a0c091.

All 11 enrichment cells are drafted as 14 orders under `round2_drafts/` in this folder. The drafts are LOCAL,
uncommitted and not issued. Six questions below would change a cell's text. Each carries this seat's
recommendation. A question with no answer at the cut is issued on the recommendation, and the order records that it
was.

| # | Cell | Question | Recommendation |
|---|---|---|---|
| Q1 | E7 (R-3 b) | Callers that carry no `tid`/`oid` fall to the lowest tier. `MASTER_ADMIN_EMAILS` is documented as "andrew@ + systems allowlist" (`app/tier.py:74`). The MS-ingest bearer path acts as `MS_INGEST_IDENTITY` by email (`app/ms_ingest.py:114,207`) and `token_broker.py:192` also takes an email. Are machine/bearer callers inside R-3's scope, or named out of scope under R-3(f)? | Name them out of scope in t-1's first criterion. They do not pass through `resolve_tier` as a person. t-2's pre-read then covers every identity in the 14-day audit (the draft already does this) and must show 0 tier deltas for them too. |
| Q2 | E7 (R-3 f) | `identity_scope.py` and `query_v0.py` stay keyed on email. W3-S9 is then only partly disarmed. | Name both in t-1's out-of-scope list. The row stays ARMED on those two, owner this seat, with a round-3 enrichment. |
| Q3 | E8 (R-2) | `lib/opal_naming.py` refuses the kind `eip`. Rule 30 treats that as a missing registry row, never a hand-typed workaround. The gateway root also cannot plan on a fresh tree: it needs NFRA_MCPORTAL's grant-writer layer zip and two owner-key variables. | Add the `eip` kind row to `infra/logic/registry/` (whose seat?) before n-1 is cut. n-1 applies TARGETED to the EIP and its association, so MCPORTAL's unapplied resources are not created as a rider. n-1 is cut after MP-a-1's build. |
| Q4 | E4 / E1 | The analysis puts FWD-2's live run in E4's close run. A worker holds no user sign-in to the live gateway. | Keep E4 as the seal plus the offline grade. FWD-2's live exercise is this seat's one real run at close (rule 22) through the E1 walkthrough identity. It is not a worker criterion. |
| Q5 | E6 (R-6) | The regrade window 09-11..09-17 predates every OPLGTW release, so it cannot measure the served build for FWD-7. | Keep 09-11..09-17 as R-OG-23A's baseline and add one post-release window of equal length ending at the cut, both printed with their request counts. |
| Q6 | E10 | Site Z has no `moto` and no `.venv-og`, so 12 gateway test files cannot run here. | E10's suite runs in a fresh venv built from the gateway's own requirements file at the cut. The cell installs nothing else. |

Other things the drafts found, stated so the analysis's numbers are read correctly:
- R-3's `config.py:233-235` roster is now `app/config.py:243-260`. The other four sites match.
- Row Z-S8 @b6727f8cee: the export path cannot return a CSV today. It folds into E5 (x-2 wires the real `run_export`).
- E5 splits into x-2 (build) and x-3 (the narrow release). E7 splits into t-1 (build) and t-2 (the release E9 rides).
  E9 splits into u-1 (W3-S11, W3-S18) and u-2 (the DCR lifetime, R-5 now signed).

Gates still open at the cut: the switchover sitting (Part D value for t-1), and G-C (a CloudOps seat, seated when E1
is next).
