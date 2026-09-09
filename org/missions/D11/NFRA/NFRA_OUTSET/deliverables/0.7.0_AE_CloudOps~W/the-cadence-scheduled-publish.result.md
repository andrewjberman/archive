# NFRA_OUTSET.TO-OS-s-21 -- THE CADENCE: result

**Assignee:** `0.7.0_AE_CloudOps~W` · **Issuer:** `2.0.0_SA_COO` · **Issuance:** `e4dbe0448e`
**Face vintage:** `eb2d27b6e4` (AMENDED on the CTO's ruling `054353ac5e`, row `NFRA_OUTSET-S25`,
shape **(d)**) · **Worked:** 2026-09-09 15:20Z -> 17:05Z
**Order status:** `pending`. **The ACT is complete on both halves; the ACCEPT reads on a served day.**

---

## THE ANSWER IN ONE PARAGRAPH

The seam has a cadence. Its two artifacts turned out to need **two different homes**, and finding
that out was most of the work: `comp-heat freshness` reads commit timestamps and is identical on
every clone, so it belongs on a cloud schedule; `comp-heat drift` is `git status --porcelain` and
its subject is a working tree, so on any clean host it would publish **n=0 forever** with a healthy
answer state and a correct denominator. Freshness runs in CodeBuild at 12:30Z. Drift runs on this
laptop at 11:30Z under a role scoped to one key. Both fired today.

---

## THE FRESHNESS HALF -- cloud-side

| | |
|---|---|
| Home | CodeBuild `estate-report-seam-freshness-publisher`, `NO_SOURCE` + inline buildspec, blobless clone |
| Identity | `estate-report-seam-freshness-publisher`, `s3:PutObject` on ONE EXACT KEY |
| Trigger | `estate-report-seam-freshness-0830et`, ENABLED, `cron(30 8 * * ? *)` `America/New_York` |
| First fire | 2026-09-10 12:30Z |
| Exercised | 2026-09-09 16:54:39Z -- `outset/comp_heat_freshness_tools.json`, 63,964 B, `answer_state OK`, scanned 399 of 399 under `.tools` |

**WHY CODEBUILD.** Build-ladder rung 2 was measured FALSE, not assumed: `EC2_MANIFEST.json` holds 27
service entries and **zero** carry a workspace checkout, and all four existing CodeBuild projects
build from an **S3 source zip**, which carries no `.git` and therefore no commit timestamps -- so
none was reusable for a measurement that reads them. Rung 4 is what this uses: `NO_SOURCE` with an
inline buildspec is the native primitive for clone-and-run-on-a-schedule, and it needs no instance to
patch, no self-stop lifecycle, no dead-man's switch and no Lambda git layer.

**THE IDENTITY IS NEW BECAUSE NOTHING COULD DO IT.** An applied-plane sweep before cutting it found
**0 holders** of `s3:PutObject` reaching `outset/*` across 224 roles. Coverage qualifier: 174
attached-managed statements were UNRESOLVED and are therefore uncovered, never absent.

## THE DRIFT HALF -- device-side, shape (d)

| | |
|---|---|
| Home | this laptop, `infra/aws/ec2/outset-drift-device/publish_drift.py` |
| Identity | `outset-drift-publisher-laptop`, assumed under the pinned session name `outset-drift-laptop` |
| Grant | ONE statement, `s3:PutObject`, ONE exact key `outset/laptop/comp_heat_drift.json` |
| Trigger | Windows task `OpalOutsetDriftLaptop`, daily 07:30 local |
| Exercised | `publisher_arn = arn:aws:sts::313476888478:assumed-role/outset-drift-publisher-laptop/outset-drift-laptop`, n=156, tracked_total=30,835, git_head `2befa0e9ff10` |

### The install, the read-back, and the removal

**INSTALL** (PowerShell -- `schtasks` through Git Bash is mangled by MSYS path conversion, which
rewrote `/Query` into `C:/Program Files/Git/Query` when measured):

    schtasks.exe /Create /TN "OpalOutsetDriftLaptop" /SC DAILY /ST 07:30 /F /TR "cmd /c cd /d C:\Users\AndrewBerman\Desktop\ajb_workspace && C:\Users\AndrewBerman\AppData\Local\Programs\Python\Python312\python.exe infra\aws\ec2\outset-drift-device\publish_drift.py --out-prefix s3://opal-estate-report/outset"

**REMOVAL, one line:**

    schtasks.exe /Delete /TN "OpalOutsetDriftLaptop" /F

**READ-BACK, after creation:**

    State               : Ready
    NextRunTime (local) : 09/10/2026 07:30:00
    NextRunTime (UTC)   : 09/10/2026 11:30:00
    LogonType           : Interactive
    RunLevel            : Limited
    UserId              : AndrewBerman
    StartWhenAvailable  : (unset)
    WakeToRun           : (unset)

The task did **not** exist before this (`Get-ScheduledTask` -> ABSENT, checked first), so nothing was
installed over blind. The next fire was verified **in UTC**, not trusted in local time, because the
ordering against the 13:00Z report is the thing `O21-AC1` grades.

### TWO PROPERTIES STATED, NOT FIXED

**(i) THIS TIMER ONLY FIRES WHEN THE MACHINE IS AWAKE AND LOGGED ON, AND IT DOES NOT CATCH UP.**
Measured rather than inferred from the absent `/RU`: `LogonType: Interactive`, so a laptop asleep,
locked out or logged off at 07:30 local does not run it. And two settings read UNSET, which sharpens
it further -- `WakeToRun` is not enabled, so the task will not wake the machine, and
`StartWhenAvailable` is not enabled, so a **missed fire is not run late**. A reader who assumed
either would be wrong.
**That is not a defect to paper over: it is the local failure mode, and the seam already renders it
honestly.** With no publish, the artifact ages past `OUTSET_SEAM_MAX_AGE_HOURS` (26 h, default,
unset in `runtime.env`) and group A renders that device **SILENT** for that day while the other
devices still render. The consumer's ceiling and this timer's logon dependency are the same fact seen
from two ends, and "the laptop was closed" and "the publisher is broken" are correctly the same
observation to a reader who is told the ceiling -- which is why the ceiling is named beside it here.

**(ii) `/ST 07:30` IS LOCAL TIME AND MOVES WITH THE CLOCK, AND IT IS BEFORE 13:00Z BOTH WAYS.**
Today (EDT, UTC-4) it is **11:30Z**; after the November change (EST, UTC-5) it is **12:30Z**. Both
precede the 13:00Z report, so the ordering `O21-AC1` grades survives the transition. Stated so a
later reader does not read 12:30Z as a late timer. The cloud half's schedule is DST-native for the
same reason, by a different mechanism (`aws_scheduler_schedule` with an IANA zone).

---

## O21-AC2 evidence -- THE TRIGGER'S SHAPE AND HOME. Recorded, NO VERDICT.

**Where the producers run and why, in one line each.** Freshness: cloud, because it reads commit
timestamps and those are identical on every clone. Drift: this device, because it reads
`git status --porcelain` and a clean clone has nothing uncommitted **by construction** -- a scheduled
cloud publisher would emit n=0 forever with `answer_state OK`, a correct denominator and a fresh
vintage (row `NFRA_OUTSET-S23`).

**The publishing identities, named, with applied-plane reach.** Cloud:
`estate-report-seam-freshness-publisher`, `s3:PutObject` on exactly two keys plus one exact-object
`s3:GetObject` (census 16:38:06Z). Device: `outset-drift-publisher-laptop`, one statement, one key,
trust by ARN with `sts:RoleSessionName` pinned (census 16:52:15Z, 229 roles). DESIRED == APPLIED on
both.

⛔ **THE DESIGN FACT WORTH CARRYING PAST THIS CELL: `boto3` FALLS BACK TO AMBIENT CREDENTIALS IN
SILENCE.** A device script that merely built a default client would publish successfully as the
admin user, every check would go green, and the named identity would have done nothing -- the role
would be decoration and no test would say so. So the publish client is constructed **only** from the
assumed session, `publish_artifact(..., s3_client=<that client>)` is what writes, and a failed assume
is a hard exit rather than a fall-back.

**The trigger is the producer's own schedule**, never success-of-upstream and never a watcher on a
consumer. Nothing new is stored on the device: no key minted, written or cached; the assume uses the
credential source already present and the session lives in memory for one publish.

**What a FAILED producer publishes:** a FAILED artifact, never nothing -- and the exit code says so
separately. Both publishers return **4**, not 2, for "published a FAILED artifact", because the
interpreter uses 2 for "cannot open file" and those are opposite states. That is measured, not
anticipated: a CodeBuild run hit exactly the interpreter's 2 earlier today when its entrypoint was
absent from the cloned branch.

**The QA hand publish, distinguished from the exercise.** The device artifact was first published by
hand at 15:55:16Z and again under the named role at 16:52:31Z; the cloud pair was fired by hand at
16:54:39Z / 16:54:42Z. **All of these are QA and none is the accept.** The accept is the scheduled
fire, and an ad-hoc artifact is never production evidence.

**The moratorium boundary as I read it:** a pipeline trigger is not a monitor (CTO `e18317d0e0`), so
the two schedules are in bounds. No alarm, alert, SNS or freshness checker was built, and nothing is
armed to watch either fire. The freshness *question* is already answered by the consumer's own 26 h
ceiling, which convicts a stale artifact with nothing watching it.

---

## O21-AC1 -- NOT YET READABLE, AND THAT IS CORRECT

The battery reads a SERVED DAY. The freshness arm can first read **2026-09-10 13:00Z**; the drift arm
needs the TIMER's own fire, so **2026-09-11 13:00Z** at the earliest, on three planes: `get-role-policy`
DESIRED == APPLIED, a CloudTrail `PutObject` on the key by the `outset-drift-laptop` session at the
11:30Z fire, and served group A naming `laptop` with n equal to the device's porcelain count at
`git_head`.

## ROWS FILED UNDER THIS ORDER

| Row | Class | What |
|---|---|---|
| `NFRA_OUTSET-S23` | BLOCKING | `comp_heat_drift` is `git status --porcelain`, so a scheduled clean host publishes n=0 forever and `O21-AC1` would have passed on it |
| `NFRA_OUTSET-S25` | BLOCKING | the device timer had no identity it could honestly use; three shapes offered, all refused, and the CTO ruled a fourth |
| `NFRA_OUTSET-S26` | OBSERVATION | the seam's row roster is hand-enumerated and a second producer defeats it -- 38,872 rows would have published as a clean zero |

## WHAT I DID NOT DO

- **Did not build a drift publisher of any shape in the cloud**, before or after the ruling.
- **Did not mint, write or cache a credential** on this device.
- **Did not edit `org/modules/heatmap/outset_seam.py`** -- read only, and refused by the lane
  resolver as my negative control.
- **Did not build the S3-sourced entrypoint** that would have removed the push gate. It works around
  a gate that exists on purpose and would ship the repository's history into an artifact bucket.
- **Did not push.** Refused under this order's BOUNDS.
