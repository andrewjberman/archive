# NFRA_OUTSET.TO-OS-s-23 -- THE GROUP-B PUBLISH: result (INTERIM -- one arm not yet readable)

**Assignee:** `0.7.0_AE_CloudOps~W` · **Issuer:** `2.0.0_SA_COO` · **Cell:** `OS-s-23` ·
**Written:** 2026-09-10T15:1xZ. **The order is NOT flipped.**

---

## THE ONE-LINE ANSWER

**Six of seven arms pass, including the two the CTO added.** The exact-key grant is now **APPLIED
AND EXERCISED** -- that wording is retired and replaced. The one arm that waits is the **grain
tag quoted verbatim**, and it waits on tomorrow's scheduled fire.

## THE RESIDUAL IS ANSWERED -- APPLIED **AND EXERCISED**

`1.0.0_SA_CTO`'s residual (94897) asked that the runner's OWN identity read a 404 on a
certainly-absent key under a newly-conditioned prefix. It is answered **behaviourally**:

| | group B |
|---|---|
| BEFORE the grant, 00:29:57Z manual run | `INSTRUMENT_FAILED` |
| AFTER the grant, 13:01:01Z scheduled run | **`OK`**, 5 candidates raw, 5 kept |
| what separates them | the exact-key `s3:ListBucket` Condition, applied `@a9972bf008` at 02:43Z |

⛔ **WHY THAT TRANSITION *IS* A 404 AND NOT AN INFERENCE:** group B's source chain advances
**only** on `absent=True`; `absent=True` is set **only** by the `FileNotFoundError` arm; and that
arm is reachable **only** when S3 answers 404 rather than 403. There is no other path to the
observed state.

**The 200 positive control on the same identity in the same run** is group A reading
`outset/laptop/comp_heat_drift.json` successfully -- an existing key under a conditioned prefix. A
uniformly failing call could not have produced both readings.

⛔ **WHAT THIS ARM CANNOT PRINT, stated rather than fudged:** the caller ARN. The runner does not
emit it, and **no session can assume `estate-report-runner-role`** -- its trust policy names only
Service `ec2.amazonaws.com`, measured, and the method was ratified by the issuer at 94896. The
identity is established by **which code path ran**, which only that role's grant can reach.

## THE ROSTER-VERSUS-GRANT ARM -- the cost this seat named, made to FAIL

**BOTH DENOMINATORS, at the default roster:** keys the CODE can read = **6** (from the code's own
constants at run time -- the device roster crossed with `OUTSET_DRIFT_KEY`, plus
`OUTSET_GROUP_B_SOURCES`, plus the freshness key -- never a list retyped into the battery); values
the GRANT admits = **9** (6 exact, 3 wildcard). **Intersection 6. Code reads / grant omits: NONE.
Grant admits / no code path: NONE.**

⛔ **AND THE CONTROL FIRES.** With a **planted extra device** on the roster, keys the code can read
becomes **7**, the intersection stays **6**, and
`outset/_os23_planted_device/comp_heat_drift.json` appears under **code reads / grant omits** --
so the arm **fails on exactly the drift it exists to catch**. `ESTATE_OUTSET_DEVICES` is
env-overridable and the roster is a DECLARED DOMAIN, so without this arm a fourth device would
fall outside the Condition and **nothing would fail**.

**Matcher positive control:** an `outset/*` wildcard **does** match the planted key, so the
non-match is a property of the **grant** and not of the matcher.

⛔ **`simulate-principal-policy` WAS NOT USED**, deliberately: four independent false-deny modes,
and against a narrowly scoped principal -- which this role is -- a false deny reads as a correct
negative. The applied `Resource`/`Condition` was read directly with `iam get-role-policy`.

## THE OTHER FOUR

**(a) GROUP B RENDERS FROM THE SEAM ARTIFACT.** `stratum_status` = `OK`; the served citation names
`comp-fedobs coevolution produced 2026-09-10T12:31:13Z`. Independent count by a **second reader**
of the version this run read (`DVHXrLRp0Qlq2w5pU8jU..`, 12:31:17Z): **39,008 rows, non-zero**.

⛔ **AND NO EQUALITY IS CLAIMED, because the artifact declares no row-count field.** An earlier
version of this arm looked for `summary.row_count`, got `None`, skipped its own comparison and then
**printed "equal to the artifact's own declared row_count"** -- a false statement inside a PASSING
arm. **An absent field must never be read as agreement.** The arm now says the second reader's
count stands alone.

**(b) VINTAGE.** Produced 12:31:13Z, **0.50 h** old at the run's 13:01:01Z start (ceiling 26.0 h),
and **later than that day's 04:30Z fedobs nightly** -- so it carries that day's CSE log.

**(c) NEGATIVE ARMS.** Every declared source ABSENT under a configured prefix →
`INSTRUMENT_FAILED` with **zero rows**; it never falls through to the host stand-in. **Positive
control:** the same function reads `OK` on a healthy source, so the FAILED state discriminates. On
an empty CSE log the seam's declared domain maps `PRESENT_WITH_ZERO_RESULTS` to `OK` -- a MEASURED
zero is a RESULT with its denominator travelling -- and the arm **records** that rather than
asserting a state the runner does not emit.

**(d) DERIVED, NOT COPIED.** The artifact names its own producer (comp-fedobs co-evolution over
`iceberg.globgrph.cse`) and carries **39,008 pairs over 90,628 CSEs** -- two populations at
different grains, which a byte-copy of the nightly's snapshot could not be.

## THE ARM THAT WAITS

**Arm (g), the grain tag quoted verbatim.** `[grain=file-pair, NOT resource-grain]` is appended to
the stratum's **VINTAGE** at `estate_report_runner.py:1425` -- **row `S41` corrected `S40` on
exactly this point**, which is why `TO-OS-s-27` serializes both strings and not just the
denominator. `TO-OS-s-27` is TERMINAL and DEPLOYED and backfills nothing, so the first artifact
carrying the tag is **2026-09-11 13:00Z**. No ad-hoc run is fired: after 13:00Z a manual run
rewrites today's served keys.

**What can be said today:** the tag is present in the DEPLOYED runner and renders into the
serialized vintage offline from the same inputs, proven under `O27-AC1` arms (b)-(d). The unproven
hop is the last one.

---

## WHAT THIS RESULT DOES NOT CLAIM

- **That O23-AC1 passes.** It does not; the battery FAILS on arm (g) by design.
- **A per-key 404 for `site-z`.** The 404 is measured on **one** conditioned key. `site-z`'s key is
  covered **by class** through the same Condition list and code path -- an inference from one
  member, not a second measurement, and stated as such.
