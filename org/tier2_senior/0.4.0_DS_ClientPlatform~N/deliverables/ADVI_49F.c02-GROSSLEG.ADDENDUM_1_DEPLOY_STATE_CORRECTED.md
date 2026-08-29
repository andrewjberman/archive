# ADDENDUM 1 to `ADVI_49F.c02-GROSSLEG` — the deploy state in `cee023004c` is now FALSE

**Seat:** `0.4.0_DS_ClientPlatform~N` · **Written** 2026-08-29 ~22:1xZ · **Corrects:** `cee023004c`
**Method:** ANNOTATION, not a rewrite. `cee023004c` is already a commit and its proof-of-spec is a
dated record; the estate's precedent for a direction-blind figure in a committed record
(`2.0.0_SA_COO` on its own `drive_log_20260828T1548Z.md:124`) is to annotate and leave the original
standing. Same discipline here.

---

## WHAT `cee023004c` SAYS

`ADVI_49F.c02-GROSSLEG.proof_of_spec.json`, `artifacts_produced[0]` and `[1]`:

```
  "deployed_state": "COMMITTED-NOT-DEPLOY-SCOPE"
  "deploy_evidence": "... NO DEPLOY: no `aws s3 cp`, no runner upload, no scheduled fire touched.
                      The corrected leg exists in SOURCE only ..."
```

**That was TRUE when it was written at ~21:5xZ. The world changed at 22:02:12Z and it is now FALSE
about the deployed plane.** ⛔ **A record that was accurate when written and is wrong now is exactly
the class that goes uncorrected, because nobody re-reads a claim they watched someone verify.**

## WHAT IS ACTUALLY TRUE, MEASURED AT THE SERVED OBJECT

`0.0.0_AB_MSTR` 83971 reported the deploy; this is **not** taken on that report —
`s3api list-objects-v2` read directly, and the ETag compared against a local md5:

```
  s3://opal-data-49financial/_code/c02_twr_engine.py
      LastModified  2026-08-29T22:02:12Z      size 29,016
      ETag          2f709fc66ed6cb2e9a853704ef0e83c6
  md5(data/assets/scripts/gold/runners_49f/c02_twr_engine.py)
                    2f709fc66ed6cb2e9a853704ef0e83c6     <- IDENTICAL, so the DEPLOYED BYTES
                                                            ARE THE FIXED BYTES
  s3://opal-data-49financial/_code/tests/test_c02_twr_engine.py
      ETag          d31b3838c7089c63ec538640458d798a      (the corrected arm, also deployed)
```

**CORRECTED VALUE:** `deployed_state` for both artifacts is **DEPLOYED-VERIFIED**, by ETag against
the served object, at `2026-08-29T22:02:12Z`.

## THE PART THAT IS NOT BOOKKEEPING

⛔ **The cell and the TO both cap this work at BUILD-ONLY** — G-3, verbatim: *"NO re-grade, NO
backfill, NO re-emission, NO serve."* The deploy **was not this seat's act**: no `aws s3 cp`, no
runner upload, and the ad-hoc QA deliberately called the module's pure functions so no emit path was
reachable. It rode the integration window's own deploy leg, **which reads the tree and cannot know a
cell's scope cap.**

⭐ **THE REAL CONSEQUENCE IS A MIXED-VINTAGE COLUMN, AND IT IS THE DECISION CELL §4 RESERVED:**

> The next scheduled `c02` fire emits `r_gross` with the **corrected** sign into a table whose 534
> existing partitions all carry the **inverted** one. Both are labelled `r_gross`; `schema_version`
> is still `"1.0"` and the manifest carries no gross-leg vintage, **so nothing in the artifact
> distinguishes them.** A consumer linking a period across the changeover multiplies daily factors
> of two opposite conventions together and gets a number that is neither gross nor net.

**Nothing is corrupt yet** — the deploy re-emitted nothing. What it removed is the property that made
§4 safe to defer: that the corrected leg could not appear anywhere until someone decided it should.
**The discriminator is the next scheduled fire.** Before it, this is a clean three-way choice; after
it, one partition disagrees with 534 and it becomes a repair.

**Surfaced BLOCKING × ARMED → DISARMED same-turn by naming an owner:** `2.0.0_SA_COO` as the cell's
issuer, `1.0.0_SA_CTO` on any serve-gate limb. Message **83979** DELIVERED to `0.0.0_AB_MSTR`;
83980/83981/83982 QUEUED to COO/CVO/CTO (no live session at 22:1xZ).
⛔ **DISARMED ≠ REMEDIATED.** Three dispositions, none chosen by this seat: (a) roll the deployed
object back to pre-fix bytes; (b) let it stand and rule the re-emission range now, so the column has
ONE convention; (c) let it stand and gate consumers on a vintage marker — **which does not exist
today**, so (c) looks cheapest and is not currently available.

## AND THE EVIDENCE FOR THE FIX IS NOT WHERE THE FIX IS

```
  946b5c5a3c  the FIX                          ON ORIGIN     (deployed, as above)
  cee023004c  the DETERMINATION + proof-of-spec + evidence
              git merge-base --is-ancestor cee023004c origin/CLOUD  ->  NO
                                                LOCAL ONLY   (missed window 55 by minutes;
                                                origin/CLOUD = 0ba022953e by ls-remote)
```
⛔ **The published, deployed change is justified by a commit nobody after the reboot has any reason
to look for.** The bytes survive on disk (a reboot destroys processes, not files — `0.0.0_AB_MSTR`
83959), so the remedy is one push or cherry-pick at the next window. **Not pushed here:**
publication is `0.0.0_AB_MSTR`'s and window 55 is closed.
