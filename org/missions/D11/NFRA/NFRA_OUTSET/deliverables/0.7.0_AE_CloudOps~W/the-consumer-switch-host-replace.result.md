# NFRA_OUTSET.TO-OS-s-20 -- THE CONSUMER SWITCH: result

**Assignee:** `0.7.0_AE_CloudOps~W` · **Issuer:** `2.0.0_SA_COO` · **Cell:** `OS-s-20` ·
**outcome_ref:** FWD-3 · **PRD** v0.9 · face AMENDED 2026-09-09 ~22:2xZ and RE-POINTED
2026-09-10 ~02:2xZ on row `NFRA_OUTSET-S34`.
**Written:** 2026-09-10T13:1xZ. **Both criteria are reported here; O20-AC2 carries NO verdict.**

---

## THE ONE-LINE ANSWER

`ESTATE_OUTSET_SEAM_PREFIX` is set on the replaced host, and **the served report proves the
consumer used it**: group A's stratum reads `OK` on the manual served day and
`INSTRUMENT_UNAVAILABLE` on the un-switched host's own real day, through the same reader at the
same JSON path. `O20-AC1` **PASSES** by its own output.

## O20-AC1 -- MECHANICAL, PASSES

**Invocation, exactly as the face names it:**

```
timeout 300 python org/missions/D11/NFRA/NFRA_OUTSET/deliverables/0.7.0_AE_CloudOps~W/test_os20_served_day_reads_seam.py
```

**Expect:** `OS20-SEAM-READ-ON-SERVED-DAY` · **Observed:** `OS20-SEAM-READ-ON-SERVED-DAY`, **rc=0**.

⛔ **rc WAS CAPTURED UNPIPED.** A pipeline's exit status is its LAST stage's, so `python ... | tail`
would have reported `tail`'s 0 whatever the battery did. The run was redirected to a file and `$?`
read from the python process itself.

**DENOMINATOR: 6 arms, all 6 evaluated, 0 NOT-EVALUATED, 8 OK verdicts, 0 FAIL.**

### (a) THE SERVED DAY -- the deciding arm

| | |
|---|---|
| Object | `daily/2026/09/09/estate-report-2026-09-09.json` |
| VersionId | `F3CLuHhwgcRKo7OdbCdLbexIO6BUo3Mw` (**not `latest`**) |
| Size / LastModified | 206,144 B / 2026-09-10T00:52:49Z |
| Identified ON THE ARTIFACT | `run_bundle.trigger` = `manual`, `run_bundle.run_id` = `a588a7ea-8ad2-4f03-a814-4f02668a66d6` |
| `/ai/groups/A/stratum_status` | **`OK`** |

⛔ **THE VERSION IS IDENTIFIED BY THE CARRIER, NOT THE CLOCK.** The battery refuses the version
unless `run_id` matches, so a different run wearing the same key cannot be graded as this one. That
is OS-s-26's carrier doing the work it was built for, inside another order's accept.

⛔ **AND `latest` IS NOT READ ANYWHERE.** `latest` on this key is the PIN restored by content after
the manual run (row `NFRA_OUTSET-S34`); reading it would have graded the 13:11Z run of the
*un-switched* host while looking like a clean read.

### (b) THE SEAM ARTIFACT'S VINTAGE, DISCLOSED ON THE SERVED OBJECT

11 proposals carry a `tool_row_cited`; **2 of them name `A_propagation@`**, and both carry a
parseable produced-instant and an age. Verbatim, truncated at 200 chars by the battery:

```
A_propagation@laptop: comp-heat drift produced 2026-09-09T23:58:09Z (tool vintage: none reported),
age 0.6 h | site-z: UNREAD (s3://opal-estate-report/outset/site-z/comp_heat_drift.json) | _os22_probe...
```

The vintage is read out of **what a reader of the report actually meets**, not out of the runner's
source. Proving it from the source would have proved the code, not the day.

### (c) THE NEGATIVE ARM -- A REAL DAY, NOT A MUTANT

| | |
|---|---|
| Object | the same key at VersionId `8SP4fGAuhE8twzBpucMPsYbotD6Tddty` |
| Size / LastModified | 162,172 B / 2026-09-09T13:11:02Z |
| Written by | `i-0512bd3cbaf602b7f`, the RETIRED host, before the variable existed |
| `/ai/groups/A/stratum_status` | **`INSTRUMENT_UNAVAILABLE`** |
| `run_bundle.trigger` | `None` -- the carrier did not exist yet |

**THE SAME READER AND THE SAME JSON PATH ON BOTH DAYS.** One function, `get_version` + `dig`, is
used for every served read in the battery, so a difference between the arms is a difference in the
OBJECT and never in the instrument. The comparator is therefore proven able to return
`INSTRUMENT_UNAVAILABLE` -- without arm (c), arm (a)'s `OK` would be a constant.

### (d) THE ORCHESTRATOR'S TARGET, LIVE, WITH A PLANTED-STALE CONTROL

| read | result |
|---|---|
| `estate-report-orchestrator` env `ESTATE_INSTANCE_ID` | `i-0584e17d283fa7ef4` |
| `describe-instances` on it | exists, state **`running`** (the 13:00Z fire had started it) |
| equals the switched host | **yes** |
| PLANTED STALE ID `i-0512bd3cbaf602b7f` | `exists=False`, `no-reservation`, equals-switched-host **False** |

The control matters because "equal ids" is otherwise a claim no arm can fail. Note the shape the
control also exercised: **a stale instance id RAISES `InvalidInstanceID.NotFound` rather than
returning an empty set**, so the resolver handles both branches; a bare `len()==0` test would have
missed the raising branch and reported the control as a pass.

### (e) CONTROL ARM -- RECORDED, DECIDES NOTHING

Live `user_data` on `i-0584e17d283fa7ef4`, 11,153 B, **1 line** naming the variable:

```
ESTATE_OUTSET_SEAM_PREFIX=s3://opal-estate-report/outset
```

⛔ **THIS ARM CANNOT FAIL THE BATTERY, BY CONSTRUCTION** -- it appends to no failure list. The face
is explicit that the env line is "a CONTROL arm, never the deciding line": a variable being SET
proves the DESIRED plane; only arm (a) proves the CONSUMER used it.

It is read from `describe-instance-attribute` (the APPLIED plane) rather than SSM **because the host
is stopped between runs**: an SSM read would be UNAVAILABLE for a reason with nothing to do with the
variable, and an arm that cannot run is not the same as an arm that failed.

### (f) CONFIRMATION, NEVER A GATE

At the graded run (13:04:52Z) `daily/2026/09/10/` held **0 objects** and the arm printed
`NOT-YET-FIRED`. The verdict comes from (a)-(e). The face: "The 13:00Z fire on the same day's keys
is CONFIRMATION, read if present, never a gate."

---

## O20-AC2 -- JUDGMENT, EVIDENCE ONLY, NO VERDICT

`3.0.0_SA_CVO` grades this at L9. Recorded here with vintage:

| item | value |
|---|---|
| Ledger entry | `org/critical_paths/change_management/20260909T1510Z_estate-report-host-replace-seam-prefix_deploy_completion.md` |
| Opened-before | committed OPEN at `4c173cddbc` |
| Closed-after | `2686fc81d6` |
| Old / new instance | `i-0512bd3cbaf602b7f` -> `i-0584e17d283fa7ef4` |
| Orchestrator target after the apply | `ESTATE_INSTANCE_ID` = `i-0584e17d283fa7ef4`, read LIVE (re-read again at this grading, still equal) |
| Andrew's authority | GO in principle for this host replacement @`e1b44ba4cc`; "All recs approved" 2026-09-09 ~14:2xZ |
| Which of the two shapes | **OFF-HOST cadence.** The ONE-REPLACE-NOT-TWO clause was decided off-host at `4c173cddbc`, so OS-s-21's cadence needed no second `user_data` change and no second replacement. |

**Rows filed at the act, not after it:** `NFRA_OUTSET-S21` (the one-replace decision) and
`NFRA_OUTSET-S22` (the creation-boot run rewrites the day's served report at the same key -- which
is why the negative arm above is pinned by VersionId and survived).

---

## WHAT THIS RESULT DOES NOT CLAIM

- **It does not claim the 13:00Z fire.** That run was in flight when this was graded and is
  confirmation, not the accept.
- **It does not claim group B.** Group B reads `INSTRUMENT_FAILED` on the manual served day. That is
  row `NFRA_OUTSET-S36` and it belongs to `TO-OS-s-23`, whose exact-key grant landed at
  `a9972bf008` and is **APPLIED, NOT EXERCISED** until the runner's own identity reads a 404.
- **It does not claim anything from a linked worktree.** Every census in this order ran on the MAIN
  tree, so the comp-rail worktree-corpus defect the COO relayed at 95126 (a well-formed zero from
  the wrong tree) cannot have touched it.
