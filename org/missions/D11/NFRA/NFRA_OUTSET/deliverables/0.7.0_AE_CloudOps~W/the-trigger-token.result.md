# NFRA_OUTSET.TO-OS-s-26 -- THE TRIGGER TOKEN: result

**Assignee:** `0.7.0_AE_CloudOps~W` · **Issuer:** `2.0.0_SA_COO` · **Cell:** `OS-s-26` ·
**Written:** 2026-09-10T13:2xZ. **O26-AC2 carries NO verdict.**

---

## THE ONE-LINE ANSWER

The orchestrator writes a token before `StartInstances`; the runner reads it at boot; the served
report carries the run's `trigger` and `run_id`. **Matched on the ID, never on the clock.**
`O26-AC1` **PASSES**: `OS26-TRIGGER-TOKEN-CARRIED`, **rc=0 captured unpiped**, 5 arms declared,
5 evaluated, 0 NOT-EVALUATED, 10 OK, 0 FAIL.

## THE INSTRUMENT IS THE SERVED FUNCTION, NOT THE REPO'S

Arm (b) imports `_trigger_token_read` **out of the object the host actually pulls**
(`code/estate_report_runner.py` @`Vl2cyFrB8dphstJ8IX2iNt01oDrMt7Sp`, 180,310 B, downloaded at run
time), not out of the worktree. A battery that imported the checkout would grade the code this seat
can see rather than the code the estate runs -- and arm (d), which proves those two are byte-equal,
would then be verifying a premise the battery had already assumed. Testing the served bytes makes
(d) an independent check instead of a circular one.

## (a) THE CARRIER, END TO END

| | value |
|---|---|
| Report | `daily/2026/09/09/estate-report-2026-09-09.json` @`F3CLuHhwgcRKo7OdbCdLbexIO6BUo3Mw` |
| `run_bundle.trigger` / `run_id` | `manual` / `a588a7ea-8ad2-4f03-a814-4f02668a66d6` |
| Token | `config/last-trigger.json` @`QRHqSjmNPdImTp_rmka.gCcoK1MLWfDR`, 117 B, LastModified 2026-09-10T00:30:07Z |
| `token.trigger` / `run_id` / `invoked_at` | `manual` / `a588a7ea-8ad2-4f03-a814-4f02668a66d6` / `2026-09-10T00:30:05Z` |

**The two ids are EQUAL.** The orchestrator wrote it at 00:30:05Z and the runner stamped the same
id into the served artifact.

⛔ **THE TOKEN IS FETCHED BY VersionId AND THAT IS LOAD-BEARING.** The token key is overwritten by
every invoke -- it now holds the 13:00Z scheduled token (`77904431-...`, `invoked_at`
2026-09-10T13:00:44Z). Reading `latest` would compare this run's report against a LATER run's
token, which could only ever fail, or pass by coincidence if ids were ever reused.

`started_at` on the report reads `2026-09-10T00:30:30.554548+00:00` and **is not used by this arm**.
The face is explicit: never inferred from the clock.

## (b) THE TWO NEGATIVE ARMS -- AND NOTHING WAS WRITTEN TO PRODUCE THEM

| sub-arm | how the state was produced | result |
|---|---|---|
| head-object control pair | read-only | `404` on an absent key beside `200` on the present one |
| **ABSENT token** | the real function pointed at a key that does not exist | `('UNKNOWN', None)` |
| **STALE token** | the real, present token with a boot instant 1 s AFTER its `invoked_at` | `('UNKNOWN', None)` |
| **FRESH token (positive control)** | the same token, boot instant 1 s BEFORE `invoked_at` | `('scheduled', '77904431-4b72-4033-8f68-4eaba9704b1e')` |

⛔ **NO put-object, NO delete, NO served-key write of any kind.** Staleness was supplied through the
`boot_instant` PARAMETER -- which is exactly what the runner's own docstring says the caller
supplies -- rather than by mutating the object. PRD R-5 is absolute, and a battery that had to
mutate served state to prove a negative would trade a real artifact for a test result.

⛔ **THE POSITIVE CONTROL IS WHAT MAKES THE NEGATIVES MEASUREMENTS.** A function that returned
`UNKNOWN` unconditionally would pass both negative arms and look identical. It returns `scheduled`
on a fresh token, so it is not a constant.

## (c) THE GRANTS ON THE APPLIED PLANE, WITH A SIBLING-KEY NEGATIVE CONTROL

| role / policy | action | resources | reaches the token key | reaches a sibling under `config/` |
|---|---|---|---|---|
| `estate-report-orchestrator-role` / `estate-report-orchestrator` | `s3:PutObject` | **1**, exactly `.../config/last-trigger.json` | yes | **NONE** |
| `estate-report-runner-role` / `estate-report-runner` | `s3:GetObject` | 6 (`daily/*`, `code/*`, `manifest/*`, `kuzu_nessie_db`, `outset/*`, `config/last-trigger.json`) | yes | **NONE** |

⛔ **`simulate-principal-policy` WAS NOT USED HERE, DELIBERATELY.** It has four independent
false-deny modes -- a conditioned statement with no context entries, a batched multi-ARN call, an
unvalidated action name, and a wrong-grain resource ARN (that last one measured at this seat as row
`NFRA_OUTSET-S3`). Against a narrowly scoped principal, which is exactly what these two roles are,
a false deny reads as a correct negative. The applied `Resource` list was read directly and matched
with a local ARN matcher instead.

⛔ **AND THE MATCHER CARRIES ITS OWN POSITIVE CONTROL.** If `arn_matches` returned `False` for
everything, the sibling `NONE` would pass for the wrong reason. A `config/*` wildcard **does** match
the sibling key, so the `NONE` is a property of the grant and not of the matcher.

## (d) THE SERVED RUNNER == THE BUILD INPUT

| | value |
|---|---|
| Served | 180,310 B, VersionId `Vl2cyFrB8dph...`, ETag `d9b82ec4578251ed3c335e992e2fbe84` |
| `git show HEAD:` | 180,310 B, md5 `d9b82ec4578251ed3c335e992e2fbe84`, sha256 `37579654c920ee7a...` |
| Re-downloaded bytes | sha256 `37579654c920ee7a...` -- agree |
| **NEGATIVE CONTROL** | one bit flipped at offset 100, length held fixed -> **MISMATCH** |

The length is held fixed on purpose, so a length check cannot be what catches the mutant.

## (e) CONFIRMATION, NEVER WAITED FOR

At the graded run (13:17:04Z) `daily/2026/09/10/` held **0 objects** and the arm printed
`NOT-YET-FIRED`. The face: "read as CONFIRMATION and recorded, never waited for." The verdict comes
from (a)-(d).

⛔ **BUT THE SCHEDULED READING IS NOT ABSENT FROM THIS EVIDENCE.** Arm (b)'s positive control read
the **live 13:00Z token** and returned `('scheduled', '77904431-4b72-4033-8f68-4eaba9704b1e')`. So
the `scheduled` value is already proven to travel from the orchestrator into the runner's own
read function; what arm (e) still adds is the last hop -- that value appearing in the published
report. That hop is unproven here and is not claimed.

---

## O26-AC2 -- JUDGMENT, EVIDENCE ONLY, NO VERDICT

**The event-to-trigger mapping as built.** EventBridge Scheduler `estate-report-0900et`
(`cron(0 9 * * ? *)` `America/New_York`) invokes the orchestrator Lambda; the orchestrator writes
ONE object to `config/last-trigger.json` and THEN calls `StartInstances`.

**The token's fields:** `trigger` (declared domain `{scheduled, manual}`), `run_id` (a UUID minted
per invoke), `invoked_at` (UTC, second precision).

**How the runner decides STALE, and why the comparison is not the obvious one.** The token is
written BEFORE `StartInstances`, so its `invoked_at` is ALWAYS earlier than this boot -- a naive
"newer than boot" test would read `UNKNOWN` on every run including the correct ones. The caller
therefore supplies `run start - TRIGGER_TOKEN_MAX_AGE_S` (3600 s) as the boot instant, and the
token is fresh iff `invoked_at >= boot_instant`. The runner reads the boot instant from its own
`started_at`, in `_trigger_for_run`.

**The two grants' applied reach before and after:** before, neither role named the key at all (it
did not exist); after, exactly the table in (c) above -- the orchestrator's Put list is ONE ARN and
nothing else.

**The runner deploy's NEVER-2 entry:**
`org/critical_paths/change_management/20260909T2243Z_estate-report-runner-trigger-token-read_deploy_completion.md`,
opened before the upload at `d1c0fa3c83` and closed at `9b5fed4570`, with the ETag control.

**THE ONE BLINDNESS WORTH STATING.** A token written by a THIRD caller with a forged `trigger`
value is TRUSTED. The runner authenticates nothing about the writer: it checks the shape, the
declared domain and the freshness window, and nothing else. Today only the orchestrator role holds
`s3:PutObject` on that key -- which is what makes the blindness tolerable rather than absent -- so
the control is entirely IAM's, and any future widening of that grant silently widens what the
report will believe about its own provenance. **A value carries its claim only as far as the
identity that may write it.**

---

## WHAT THIS RESULT DOES NOT CLAIM

- **The published `scheduled` reading.** Arm (e) printed `NOT-YET-FIRED`; the run was in flight.
- **That the token proves WHO invoked.** It proves WHAT the caller declared, under an IAM control.
- **Anything from a linked worktree.** Every census here ran on the MAIN tree.
