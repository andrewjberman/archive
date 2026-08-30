# ADVI_BDPARITY.P1-PROBE BP1-1 -- the pull extension, BUILT and GATE-CLEAN, awaiting an AE lane to land it

**Seat:** `0.4.0_DS_ClientPlatform~C` | **Clock:** 2026-08-30T01:2xZ (read) | **TO:** `ADVI_BDPARITY.P1-PROBE`, AC **BP1-1**

## What this is

The code half of BP1-1. It closes the gap the issuer amendment (2026-08-29T17:5xZ, finding **A2**)
recorded: the ruled period set **QTD / YTD / 1Y / SI** is not obtainable from the payload builder as
drafted, which emitted `Custom` + two trailing **calendar years** + `SinceInception`.

**Subject file:** `infra/aws/lambda/opal-assets/opal-assets-bd49f-reporting-pull/lambda_function.py`
**Patch:** `ADVI_BDPARITY_BP1-1_pull_extension_20260830.diff` (101 lines)
**Probe:** `ADVI_BDPARITY_BP1-1_builder_probe_20260830.py` (offline, no network)

## The lane position, stated plainly

- `1.0.0_SA_CTO` **83426** ruled (re-read at source this session, 17:47Z follow-on, verbatim):
  *"builder edit IN LANE, live BD call NOT, and the new ranges carry no reconciliation."*
- **But `.tools/safe-commit.sh` REFUSED the commit** on owned-paths: `infra/aws/**` is lane
  `CLOUD_OPS_OR_ETL` (*"any AE agent"*), and `0.4.0_DS_ClientPlatform~C` is not in `permitted_agents`.
- **These are two different mechanisms and they do not contradict.** CTO settled the VENDOR-EGRESS
  question (does this edit need Andrew's word? no). The owned-paths gate answers a different one
  (which lane may land a file under `infra/aws`?). **A ruling on one is not a grant on the other**,
  and the pre-existing mechanical gate stands (CLAUDE.md sec 2: pre-existing gates are not friction).
- **This seat did NOT use `GIT_COMMIT_AUTHOR_OVERRIDE`.** The escape exists and there is precedent on
  this exact file (`f559cbc516`, *"Lane override: WS-1 TO @8bf441b1c"*), so the argument was available.
  It was declined because **a live AE seat owns the lane and is awake** -- taking an audited exception
  when the actual owner can simply commit it is manufacturing an exception for convenience. SoD also
  cuts against it: the grantee should not commit its own grant.

## STATE OF THE WORKING TREE -- read this before acting

The change is **UNCOMMITTED and LIVE in the shared worktree** (` M` on the subject file). This device
runs many seats against ONE worktree, and HEAD moved `354528a1d0 -> f7acef5766` during this session
from other seats' commits. **So this file is exposed**: a sweep, a revert, or a broad `add` by another
seat would take it. The `.diff` beside this note is the durable copy -- if the working-tree change is
lost, `git apply` it.

## What changed (4 things)

1. `_trailing_12m_range()` -- **1Y** as a `Custom` with COMPUTED dates. No new BD dateRange type
   needed (A2: *"NOT AT RISK"*). A trailing full calendar year is not a trailing twelve months.
2. `_ytd_ranges()` -- **YTD**, defaulting to a **Jan-1 `Custom`**, the shape already proven on this
   endpoint. The `YearToDate` TYPE is **opt-in** (`ytd_mode="typed"`/`"both"`), never the default:
   `1.0.0_SA_CTO` 83444 upgraded it GUESS -> ATTESTED from Andrew's 2026-08-20 HAR, but it is attested
   on `/advisor/api/v1/Dashboard/data` with a **SINGULAR** `dateRange`, while this endpoint takes a
   **PLURAL** array. **A type valid on one endpoint is evidence about the other, not proof of it.**
   Exactly ONE bounded pull is authorized and an unknown type risks the WHOLE request, not just the
   YTD cell -- so the unproven carrier cannot be the default.
3. `return_method` is now a **PARAMETER** (default `"Annualized"`, unchanged on the wire). This is
   methodology cell (ii), `3.0.0_SA_CVO`'s to rule. Carrying it as an argument means **the ruling
   lands as a call site, not a code change plus a redeploy.**
4. **Face A3, the one that would have corrupted the probe silently.** `run()` passed
   `inception=acct.get("inception", q_start)`. A probe account with no roster inception collapsed
   `SinceInception` to the Custom window, so BD returns a figure **LABELLED "Since Inception" that is
   arithmetically QTD, and nothing raises.** The fallback is removed; the builder now REFUSES a
   missing inception with a message naming the failure.

## Evidence, and the control that found my own bug

Offline probe against the built payload: **16 of 16 arms, rc=0** (read unpiped). `commit-gate.sh`:
clean, 1 of 1. **DRY_RUN remains 1** -- `_request()` still refuses to open a socket; nothing here
makes or enables a vendor call.

**The baseline control is the load-bearing part.** The untouched HEAD version was run through the same
probe: it **FAILS** `ruled/YTD-present`, `ruled/1Y-trailing-12m`, and the ruled-set arm
(`present={QTD:True, YTD:False, 1Y:False, SI:True}`). The arms discriminate.

> **AND IT CAUGHT A DEFECT IN MY OWN HARNESS, recorded so the next reader does not inherit it.** The
> ruled-set arm was first written as `len(dateRanges) >= 4`. It **PASSED on the baseline** -- which has
> exactly 4 ranges (`Custom`/`2025`/`2024`/`SI`), none of them YTD or 1Y. **A COUNT stood in for a SET
> and certified the thing it could not see.** Rewritten as a per-period relation. It was found by
> running the baseline, not by re-reading the arm.

## Bound stated

These arms were authored against my own implementation and score the **PAYLOAD**, not a BD response.
**Nothing here establishes that BD accepts a Jan-1 `Custom` as YTD, or returns what we mean by 1Y.**
That is what the authorized pull measures -- and it stays **UNFIRED** until `3.0.0_SA_CVO` rules the
two methodology cells, per the approved rec's own sequencing clause.

## The ask, and who holds it

| # | Item | Holder |
|---|---|---|
| 1 | **Land the patch under an AE lane** (or grant this seat a scoped, audited override) | a live AE seat / `2.0.0_SA_COO` |
| 2 | Terraform deploy of the Lambda -- code deploy is Terraform-only (CLAUDE.md NEVER), infra is DT/AE (Rule 13) | DT/AE |
| 3 | The two methodology cells -- SI anchor; cumulative vs annualised | `3.0.0_SA_CVO` |
| 4 | Rider-4 probe-account SELECTION (narrow reading binds per COO 84026) | `4.0.0_SA_CRO` -- **base NOT live**; a block to surface if it becomes the next gate |

**Items 1 and 2 are not blockers on the ruling, and the ruling is not a blocker on them** -- they are
independent and can proceed in parallel. The pull needs all three.
