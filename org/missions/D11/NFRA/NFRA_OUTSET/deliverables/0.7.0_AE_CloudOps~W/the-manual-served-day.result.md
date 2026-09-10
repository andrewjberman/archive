# NFRA_OUTSET.TO-OS-s-24 -- THE MANUAL SERVED DAY: result

**Assignee:** `0.7.0_AE_CloudOps~W` · **Issuer:** `2.0.0_SA_COO` · **Cell:** `OS-s-24` ·
**Written:** 2026-09-10T14:5xZ. **O24-AC2 carries NO verdict.**

---

## THE ONE-LINE ANSWER

The manual served day was produced, its NEVER-2 entry was opened before the invoke and closed RED
with a verified rollback, and the run is told apart from every other by its own carrier rather than
by a clock. `O24-AC1` **PASSES**: `OS24-MANUAL-SERVED-DAY`, **rc=0 unpiped**, 7 arms, 7 evaluated,
**25 OK, 0 FAIL**.

## THE THING WORTH READING FIRST: THREE OF TONIGHT'S FOUR FAILURES WERE MINE

When this battery was re-run at 14:2xZ it reported **four** failures. **Three were defects in the
battery, not in the estate**, and they are recorded as row `NFRA_OUTSET-S44`:

| arm | what it read | why it went wrong |
|---|---|---|
| (b) | `head_object` on the seam keys at **`latest`** | the 12:30Z build re-published two of them, so it compared **today's** vintage to a run that started 00:30:30Z |
| (c) | the token key at **`latest`** | that key is overwritten by every invoke; the 13:00Z fire replaced the manual token |
| (d) | the fedobs artifact at **`latest`** | printed 39,008 rows at 12:31:13Z beside a run that could only have read **38,872** rows at 00:18:58Z |

⛔ **ALL THREE PASSED WHEN WRITTEN.** On 2026-09-09 the manual token *was* latest and the seam keys
had not been re-published. **THE ARMS DID NOT BREAK; THE WORLD MOVED PAST THEM.** That is the
time-bomb form of the `latest`-versus-VersionId trap: an arm reading a mutable key at `latest` is
correct only on the day it is authored, and its later failure is indistinguishable from broken work.

**The fix is not a pinned VersionId** -- a pin goes stale one round later in the same way. Each arm
now **SELECTS**: (b) and (d) take the latest version whose LastModified **precedes the run start**,
which is by construction the version that run read; (c) reads every version of the token key and
picks the one whose `run_id` **equals the report's**, identifying it by the carrier rather than by
recency. Both print their denominators, so a reader sees the choice rather than trusting it.

## THE ARMS

### (a) THE NEVER-2 ENTRY, OPENED BEFORE THE INVOKE

Entry `20260910T0020Z_estate-report-manual-served-day-09-10.md`, opened **00:20Z** against an
invoke at **00:29:57Z**, with both never-widen halves quoted: the COO's by face hash
(`26f1cd8b82`, later `584003bcae`) and the CTO's by message id (`94764`, superseded by `94820`).

### (b) THE SEAM VINTAGES PRECEDE THE RUN

| key | versions | predating the run | the version THIS RUN read |
|---|---|---|---|
| `outset/comp_heat_freshness_tools.json` | 4 | 3 | `wPjEwsCY4Fg2o84Wp3bG..` 2026-09-10T00:18:59Z |
| `outset/comp_fedobs_coevolution.json` | 3 | 2 | `PX68UJFO3pcBlpUn.P8r..` 2026-09-10T00:19:02Z |
| `outset/laptop/comp_heat_drift.json` | 4 | 4 | `3AE8of7Q44VkfbsNNpwW..` 2026-09-09T23:58:14Z |

The build that produced them is named with its **initiator**: `Andrew_Berman`, SUCCEEDED. The hand
start and the rule start are the same call -- `Target.Input` is NULL on the rule.

### (c) PROVENANCE ON THE ARTIFACT, NEVER THE CLOCK

`run_bundle.trigger` = `manual`; `run_bundle.run_id` = `a588a7ea-8ad2-4f03-a814-4f02668a66d6`. Of
the **2** versions of the token key, the arm selects the one whose `run_id` equals the report's --
`QRHqSjmNPdImTp_rmka.gCcoK1MLWfDR`, `invoked_at` 2026-09-10T00:30:05Z.

⛔ **AND BOTH READINGS OF THE SAME KEY ARE PRINTED**, which is what makes the carrier legible rather
than merely present: the run's version says `manual`, the key's `latest` is the restored pin and
says `scheduled`. One key, two versions, two provenances, neither inferred from a clock.

### (d) THE FIVE ACCEPTS -- **RE-POINTED, WITH THE BEFORE STATE PRESERVED**

⛔ **Arm (d) only was RE-POINTED onto the 13:00Z SCHEDULED run by the issuer at 2026-09-10T14:37Z
(msg 95241)**, on this seat's pitch. Every other arm stays on the manual served day.

**WHY:** group B is `INSTRUMENT_FAILED` on the manual served day under row `NFRA_OUTSET-S36`. The
S36 grant landed `@a9972bf008` at **02:43Z**, *after* the 00:29:57Z run, whose artifact is
**immutable**. The criterion was pointed at a day that predates its own subject.

**AND THE BEFORE STATE IS NOT ERASED** -- the issuer made that the condition of the re-point:

| | group B |
|---|---|
| **BEFORE** -- manual served day, 00:29:57Z | **`INSTRUMENT_FAILED`**, unmeasured=True |
| **AFTER** -- 13:00Z scheduled run | **`OK`**, unmeasured=False, candidates_raw 5, candidates_kept 5 |
| **What separates them** | the S36 exact-key `s3:ListBucket` grant, applied `@a9972bf008` at 02:43Z |

So the failure the re-point walks away from becomes the **negative arm of a difference control
across the fix**, which is stronger evidence than either reading alone.

Group A on the manual served day: `laptop` present by name carrying OS-s-25's own vintage
(23:58:09Z), with a non-reporting device reading UNREAD/SILENT beside it, so the green
discriminates. The independent read of the fedobs artifact is of the version the **re-pointed** run
read (`DVHXrLRp0Qlq2w5pU8jU..`, 12:31:17Z): `answer_state=OK`, **39,008 rows**, grain `FILE-PAIR,
not resource-pair`.

### (e) THE PROTECTED RECORD -- read as BYTES, not VersionIds

The four pins are **two keys x two versions**, so "IsLatest true on the pinned id" cannot hold for
the two that are by construction the SUPERSEDED version. Restoring a pin is a `copy-object`, which
mints a NEW VersionId carrying the pinned CONTENT -- so after 00:58Z the pinned **content** is
latest while the pinned **id** is not. A check on "IsLatest == the pinned id" would FAIL on a
correctly-restored record; one on "IsLatest is unchanged" would PASS on any copy whatever it copied.
**The sha256 of the served bytes is the only form that says what the arm means.**

### (f) / (g) THE CONFIRMATION

The 13:00Z fire reads `trigger='scheduled'` with `run_id` byte-equal to the rule's own token
(`77904431-4b72-4033-8f68-4eaba9704b1e`) -- the carrier's other half, and the one a hand invoke
cannot forge, since only the ABSENCE of a trigger key yields `scheduled`.

---

## O24-AC2 -- JUDGMENT, EVIDENCE ONLY, NO VERDICT

**The five accepts as re-read on this run**, each by its own battery's output and never restated
here as a verdict: OS-s-19 (`the-deploy-of-the-served-runner`, terminal), OS-s-20
(`OS20-SEAM-READ-ON-SERVED-DAY`, rc=0), OS-s-21 (freshness half `OS21-CADENCE-FRESH` on the 13:00Z
run; drift half by OS-s-25, terminal `@520503aa98`), OS-s-22 and OS-s-23 (open -- see below).

**What the 13:00Z confirmation added, beyond confirming:** it is the run on which the S36 grant is
first **EXERCISED**, and group B's move to `OK` is the behavioural proof that the runner's own
identity received a 404 -- because the source chain advances only on `absent=True`, which only the
`FileNotFoundError` arm sets, which only a 404 reaches.

**The entry's status line LEADS with ROLLBACK naming S34**, because the manual run wrote the
PROTECTED 09-09 keys and the rollback was executed and verified.

---

## WHAT THIS RESULT DOES NOT CLAIM

- **That arm (d) passed on the manual served day.** It did not and cannot; it was re-pointed, and
  the before-state is printed above rather than dropped.
- **OS-s-22 and OS-s-23.** Both are open, each with exactly one clause that cannot be read until
  2026-09-11 13:00Z -- the first served artifact carrying `stratum_denominator` and
  `stratum_vintage` (TO-OS-s-27, terminal and deployed, bound to backfill nothing).
- **That the three corrected arms were ever right about the world.** They were wrong about the
  world for hours while reporting failures, and row `NFRA_OUTSET-S44` records that rather than
  letting a now-passing battery absorb it.
