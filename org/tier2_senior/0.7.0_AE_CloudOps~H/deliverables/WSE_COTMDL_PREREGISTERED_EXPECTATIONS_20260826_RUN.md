# WSE_COTMDL TO-R1-AE / TO-R2-AE -- PRE-REGISTERED EXPECTATIONS FOR THE 2026-08-26 06:00Z RUN

**author:** `0.7.0_AE_CloudOps~H` -- **written 2026-08-25, BEFORE the run it predicts.**
**why pre-registered:** a prediction recorded before the exercise cannot be rationalised after it.
Both TOs' EXERCISED criteria (R1 AC3/AC4, R2 AC2/AC3) land on the next SCHEDULED fire --
`cot-rebalancer-runner-daily`, `cron(0 6 * * ? *)`, ENABLED. **An ad-hoc run is a QA
instrument and is NEVER production evidence**, so the 19.5h wait is the correct cost of a
real answer, not a delay to be engineered around.

## DEPLOYED STATE BEING TESTED (both landed 2026-08-25, ledgers CLOSED)

| layer | value | ref |
|---|---|---|
| env | `MODEL_DETAIL_SCOPE=all` | applied `2026-08-25T09:50:45.000+0000`, TF @`27a3a98cdc` |
| code | `all` UNIONs roster with child descent (`:316` guard removed) | applied `2026-08-25T10:38:32.000+0000`, @`b56ec0e8ce` |
| package | `CodeSha256 gdW/oQJlKLIaREk8DhEBOv7/kPxIcHuguJhk4KmGE8Y=` | deployed bytes == build input, byte-identical |

## THE BEFORE-STATE, MEASURED (2026-08-25 06:00Z scheduled run)

Source: `s3://opal-data-assets/blackdiamond/cottonwood/meta/2026-08-25-complete.json`
(LastModified `Tue, 25 Aug 2026 06:00:49 GMT`, s3api UTC).

```
manifest rebalancer_model_detail = {"count": 30, "scope": "opal_closure"}

TWO POPULATIONS, NEVER FUSED:
  roster denominator ................ 64
  roster models WITH detail ......... 22   <- TRUE coverage. NOT 30.
  roster models MISSED .............. 42   <- the real gap. NOT 34.
  non-roster transitive children .... 8
  22 + 8 = 30 detail files          RECONCILES
```

> The TO and decomp said **"30 of 64"**. That fraction counts TWO POPULATIONS -- 30 is
> detail FILES (22 roster + 8 non-roster children), 64 is ROSTER MODELS. Corrected by COO
> @`ea6f3f4f7c` and by CTO to Andrew directly. **True coverage was 22 of 64; the gap was 42.**

## PREDICTIONS -- score these against the 2026-08-26 stamp

**P1** `rebalancer_model_detail.scope == "all"`.

**P2 ROSTER POPULATION: every roster id present.** Report as `N of <tomorrow's own
totalResultCount>` -- **re-read the denominator, do not carry 64 forward.** The roster is
vendor-side and can change overnight; a stale denominator is the defect this whole TO chain
exists to correct.

**P3 NON-ROSTER POPULATION: >= 8 children present**, and the 8 known ones by id:

  - `0e632e04-9881-4ed7-97af-00e3356e2fbc`
  - `267376fd-31d9-4770-9ce3-1826b80ee158`
  - `58ea3200-6715-4944-9fbd-694f7647d637`
  - `623b1942-4057-4add-ba61-bb36c76e44d1`
  - `67010675-ea84-4f1c-a402-30aac2b25420`
  - `ac3b8211-77f4-49dc-8a3f-47ec77ca05b1`
  - `ae9ef8d2-c12e-4447-9170-2dbf8c5b03c2`
  - `b25ed964-29fc-4523-955d-d5f59f026b95`

⛔ **P3 IS A LOWER BOUND, NOT AN EQUALITY.** Today's 8 were discovered by descending from
only the **22 Opal-named** seeds. Tomorrow descends from **all 64**, and the 42 roster models
never pulled before may hold children nobody has ever seen. **A count above 8 is the expected
case, not an anomaly.** Their details have never been landed, so the exact number is
**unmeasurable from here** -- bounding it needs the vendor API, which this seat is not
authorized to call.

**P4 THE FALSIFYING CASE -- both Anna models present:**

  - `1ae61190-70fb-4d6c-a259-cee9019ed125`  name=`'Anna *9237'`
  - `6ae9e540-9b27-474c-8ad9-3dfc5131c530`  name=`' Anna *9238'`

⛔ **The second name carries a LEADING SPACE. Do not normalise it away** -- match on id.
They are why the defect was found; **their absence falsifies the fix whatever the count says.**

**P5 COUNT:** `count == P2 + P3` and `count > 30`. **Report the two populations SEPARATELY.**
A fused delta is precisely what hid the original defect: *"30 -> 64, +34"* is arithmetically
true and describes something that did not happen.

**P6 RUNTIME:** last 5 scheduled runs 6751-7322 ms against a **300000 ms** timeout (max 2.44%,
41x headroom; max memory 107 MB of 512 MB). Tomorrow does more GETs -- **>= 64 + children vs 30
today.** Even 3x lands near 1% of budget. **If it times out, that is a finding, not a retry.**

## WHAT WOULD FALSIFY THE WHOLE CHAIN

- **P4 fails** -> the fix did not fix the thing it was authorized for. Report and STOP.
- **P3 returns 0 children** -> the `:316` union is not operative in the deployed path, despite
  the deployed bytes carrying it and the build-level mutant firing. Report and STOP -- **do not
  reach for a second knob until the first is understood.**
- **count unchanged at 30** -> `MODEL_DETAIL_SCOPE` is not the operative control and the
  coverage gap has another cause entirely. Report and STOP.

## STILL OPEN, NOT MINE

- **The 08-21 backfill** (`COT-e-1`) -- excluded by determination, an open call at Andrew.
  Forward-only means **every partition through 2026-08-25 inclusive carries 22-of-64 roster
  coverage**; today joined that set three hours before the fix landed.
- **3 foreign committed-but-unapplied changes in `opal-assets`** -- STILL ARMED. Both my
  applies were `-target`ed, which disarmed **those two acts only, not the workspace.**
  CTO owns naming disarm owners.
