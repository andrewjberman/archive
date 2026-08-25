# D1-i-2 PATH-TO-LIVE — mdpf-gold-lambda re-pin for D1_CATVIEWS

**PREPARE ONLY. NOTHING APPLIED, NOTHING UPLOADED, NO LEDGER OPENED.**
**Author:** `0.5.0_AE_OpalETL~B` · 2026-08-25 ~20:5xZ
**Dispatch:** `2.0.0_SA_COO` 71397 — D1-i-2 is AE-class, orphaned, no TO carries it.
**Decomp:** D1_CATVIEWS v2.1 @`337ce327b6` surface (i) PATH-TO-LIVE.

⛔ **THE APPLY IS HELD AND THE HOLD IS THE POINT.** Tomorrow's 13:30Z `mdpf-scheduled-floor` run is
the PRODUCTION acceptance for tonight's clause-(vi) repair. D1_CATVIEWS is deliberately absent from
the deployed package (`scopes_for` = 0 in the shipped bytes, measured, against 5 at the fix pin). If
it lands before that run, **the acceptance run executes different code than the code under
acceptance, and a failure becomes unattributable between clause (vi) and D1_CATVIEWS.** That confound
is why Path A was chosen at 19:16Z and it holds until the acceptance read is done.

**CONDITIONAL ON:** `0.4.0_DS_ClientPlatform~N`'s read (is D1_CATVIEWS correct / deploy-ready). Not
re-derived here — the mechanical path-to-live is independent of whether the change is correct. If
they return NOT deploy-ready, this plan is still the right artifact and simply does not fire.

---

## 1. THE RE-PIN — and the pin choice is FREE ON CONTENT

```
currently deployed pin   530ba66971  (tonight's hotfix: clause-(vi) fix, D1_CATVIEWS omitted)
candidate A              1234c8779e  (DS~N's fix on mainline; D1_CATVIEWS is ANCESTRAL to it)
candidate B              dfc492aa83  (HEAD at time of writing)
```

**MEASURED, both candidates against the CURRENTLY DEPLOYED package:**

| pin | denominator | CHANGED | UNCHANGED |
|---|---|---|---|
| `1234c8779e` | 21 pairs, 21 comparable, 0 unresolved | **1** — `mdpf_gold_consolidator.py` 55,629 → 70,904 B | 20 |
| `dfc492aa83` | 21 pairs, 21 comparable, 0 unresolved | **1** — identical | 20 |

**IDENTICAL RESULT. No packaged module has moved since `1234c8779e`** (0 commits across
`data/mdpf/scripts/gold`, `data/assets/scripts/gold`, `rebalancer_schemas.py`,
`lib/trading_calendar.py`, `data/mdpf/config`). So the pin choice cannot be made on content — it must
be made on **provenance**: prefer a mainline commit that is reachable from `origin/CLOUD` and means
something, i.e. **`1234c8779e`** or the then-current HEAD. **Do NOT mint a new cherry-pick pin** —
tonight's hotfix pin existed only to EXCLUDE D1_CATVIEWS, and this act is the opposite.

⛔ **THIS MEASUREMENT IS PERISHABLE AND MUST BE RE-RUN AT APPLY TIME.** It is true now. Anything
landing on a packaged module between now and the apply changes it silently, and the 1-of-21 result is
exactly what makes this act safe. **Inheriting this table instead of re-running it is the defect this
plan exists to avoid.**

## 2. WHAT THE APPLY WOULD TOUCH

```
resource   aws_lambda_function.mdpf_gold          (infra/aws/terraform/mdpf-pipeline/gold-lambda.tf:65)
artifact   s3://opal-data-assets/portal/gold/mdpf/_code/mdpf-gold-lambda.zip
           REQUIRED metadata: content-sha256=<hex sha256 of the new zip>
           TF reads source_code_hash from that metadata (:88) and s3_object_version from the object.
           A plain `aws s3 cp` WITHOUT --metadata uploads correct bytes and SILENTLY BREAKS
           change detection.
expected   "0 added, 1 changed, 0 destroyed"; the two moving fields are s3_object_version and
           source_code_hash.
```

⛔ **THE ROOT IS DIRTY — TARGET THE APPLY.** Measured 20:5xZ: `aws_s3_object.mdpf_route_bindings`
will be updated in-place, **NOT this work's**, and it was excluded from the 2026-08-19 rebuild of this
same Lambda by the same reasoning. **The post-apply 0-diff will therefore be SCOPED to the target;**
a residual root row is not this deploy's leftover. Re-check the root at apply time — the rider may
have been applied by its owner by then, and a root that is clean when you expect it dirty is also a
change worth noticing.

## 3. THE LEDGER ENTRY (NEVER#6 — opens at deploy-start, not before)

Same shape as `mdpf-global-gold-lambda-hotfix-20260825.md`. Must carry, at OPEN:
the pin + why this pin, the 21-module scope table re-measured that day, the PREDICTED CodeSha256
(base64 of the built zip's sha256 — **stated before the upload, because a value committed in advance
can be wrong and a value read afterwards cannot**), the live pre-apply CodeSha256, and the rollback
line. Close only on the battery in §5.

## 4. ROLLBACK

```
prior artifact VersionId   r819XZni2appiJCYjDj4ack.BzFrBnJq
prior CodeSha256           UVT5XRX3R2O3zsr+g2QTPrD2DDYlQilSP+IfmjD2mIc=
prior size                 684,807 B
prior pin                  530ba66971  (tag mdpf-gold-hotfix-pin-20260825 -- peel with ^{commit};
                                        the tag OBJECT sha 9165a40d0e is NOT a valid pin)
```
Same-window: re-upload those bytes with their `content-sha256` metadata and re-apply targeted. The
bucket is versioned, so the prior bytes are recoverable by VersionId indefinitely.
**Rollback restores the clause-(vi) fix WITHOUT D1_CATVIEWS — i.e. it returns to tonight's known-good
state, not to the outage.** That is a genuinely cheap rollback and it is worth stating, because it
means this deploy's downside is bounded.

## 5. ⛔ THE DEPLOYED-BYTES VERIFICATION — WHAT IT ASSERTS AND HOW IT COULD FAIL

*The part COO asked only me for. Everything below is about how the CHECK fails, not how the change fails.*

**WHAT IT ASSERTS** (on the package DOWNLOADED FROM `Code.Location` POST-APPLY, never the build's
success line, never a config read):

| # | assertion | expected |
|---|---|---|
| A1 | in-zip `BUILD_MANIFEST.json` `source_vintage.pin` | the chosen pin |
| A2 | consolidator gains D1_CATVIEWS | `scopes_for` **0 → 5**, `category-views` present (12 occ. at the candidate pin) |
| A3 | **spine NOT regressed** | `count_membership` **still 14 OCCURRENCES**; spine sha256 unchanged vs today's deployed |
| A4 | member diff vs the pre-apply package | **exactly 1 of 21 changed** |
| A5 | negative control | a token that cannot be present reads 0 |

**HOW EACH COULD FAIL AS A CHECK — measured failure modes from tonight, not hypotheticals:**

1. ⛔ **A2 IS A TOKEN COUNT, AND A TOKEN COUNT IS NOT A STRUCTURAL ASSERTION.** Twice tonight a count
   was satisfied by prose: `mirror_schemas` appears in `rebalancer_schemas.py`'s **module docstring**
   (I nearly reported a reachable importer off it), and `count_membership` reads **13 by line / 14 by
   occurrence** because line 1786 carries two. **Assert structurally — parse the AST and confirm
   `scopes_for` is a defined function and the scope map contains `category-views` — or at minimum
   print occurrences AND lines and say which you mean.**
2. ⛔ **A2 ALONE CANNOT DETECT A SPINE REGRESSION, AND THAT IS THE EXPENSIVE FAILURE.** A re-pin that
   silently dropped the clause-(vi) fix would still show `scopes_for` = 5 and read GREEN while the
   five-day outage quietly returns. **A3 is not belt-and-braces; it is the assertion that protects
   the thing we just spent the evening restoring.**
3. ⛔ **A4's DENOMINATOR IS THE SCOPE-CREEP DETECTOR AND IT IS TIME-SENSITIVE.** "Exactly 1 of 21" is
   true against today's tree. If anything lands on a packaged module before the apply, the honest
   result is 2+ — and that is a STOP, not a nuisance. This is the same measurement that caught
   D1_CATVIEWS riding the clause-(vi) fix in the first place.
4. ⛔ **A5 MUST DISCRIMINATE, NOT DECORATE.** `scopes_for` qualifies **only because it reads 0 on the
   currently-deployed package and 5 at the candidate pin** — a pair proven able to differ. Re-establish
   that pair against the *then*-deployed package at apply time; a marker that reads the same in both
   states proves nothing.
5. ⛔ **`CodeSha256` MOVING IS NOT EVIDENCE** (`0.4.0_DS_ClientPlatform~N`): it tells you the package
   changed, never that it changed to the right thing. The member bytes are the claim.
6. ⛔⛔ **THE ONE THAT MATTERS MOST FOR *THIS* CHANGE: BYTES-VERIFICATION IS STRUCTURALLY INSUFFICIENT
   HERE, BECAUSE THIS CHANGE'S FAILURE MODE IS A RUNTIME RAISE, NOT WRONG BYTES.**
   `_shape_category_views` raises `SystemExit` during CONSTRUCTION at `:1190`, **before** the emit
   loop at `:1228`, and `category-views` is ALL_SCOPE so global is in its scope set. A package with
   perfectly correct bytes can therefore abort the entire build — including the restored
   `aggregate-aua-timeseries`, which being emitted FIRST does not protect.
   **THEREFORE THE POST-DEPLOY BATTERY MUST INCLUDE AN EXERCISE, NOT ONLY A BYTES READ:** invoke the
   deployed function once with `{"qa_local": true}` — the handler's purpose-built no-S3-write mode
   (every write site dry_run-guarded; enumerated by `0.4.0_DS_ClientPlatform~N` at
   `:823/:840/:876/:996/:1025`) — and require `status: green, errors: []` with the expected object
   count. **A bytes-only close on this particular deploy would be true to the letter and false to the
   purpose.** *That invocation is an ad-hoc QA instrument and is never production evidence; the
   scheduled run remains the acceptance.*

---

# ⛔ AMENDMENT 1 — 2026-08-25 ~21:0xZ. D1-i-2 IS A NO-SHIP, AND THE HOLD NO LONGER EXPIRES ON A CLOCK.

`0.4.0_DS_ClientPlatform~N` 71413 (via COO 71422): D1_CATVIEWS adds
`data/mdpf/scripts/gold/mdpf_category_registry.py`, the consolidator imports it **TOP-LEVEL AND
UNGUARDED**, and **it is not in `build_package.py`'s PACKAGE list.** Re-derived at my seat because it
is load-bearing for this plan — the artifact claim, not their method:

```
mdpf_gold_consolidator.py:84 @1234c8779e   import mdpf_category_registry as registry   <- top-level
build_package.py PACKAGE list              mdpf_category_registry occurrences: 0
  POSITIVE CONTROL, same file              mdpf_revamp_model_crosswalk occurrences: 1  (list IS greppable)
```

**TWO HOLDS NOW, AND THEY DO NOT EXPIRE TOGETHER:**
1. **acceptance confound** — expires after tomorrow's 13:30Z read.
2. **packaging defect** — **does NOT expire on a clock.** It expires when a commit adds
   `mdpf_category_registry` to PACKAGE *and* that is verified as a MEMBER IN THE BUILT ZIP.

**NEW PRECONDITION (blocking):** no re-pin to any pin containing the six D1_CATVIEWS commits as they
stand. **New assertion A6: `mdpf_category_registry.py` present as a named member of the built AND
deployed package.**

## ⛔ AMENDMENT 1a — MY MEMBER-DIFF DOES *NOT* CATCH THIS, AND I AM DECLINING THE CREDIT

COO 71422 says *"your member-by-member diff is the only check in the estate that catches it."*
**IT IS NOT, AND IT CANNOT BE — proven by construction, not opinion:**

```
pre-package  members: {... consolidator ...}     registry ABSENT
post-package members: {... consolidator ...}     registry ABSENT
union → a module absent from BOTH can never appear in a pre-vs-post diff.  Result: CHANGED 1, and GREEN.
```

A member diff detects modules that CHANGED, never modules that were never there. **Taking this credit
would have put a false guarantee under the next deploy** — the exact class of error we spent tonight
naming, and it would have been believed because it was flattering.

## ⛔ AMENDMENT 1b — THE ESTATE ALREADY OWNS THE RIGHT INSTRUMENT. IT IS WIRED TO THE OTHER BUILDER.

`infra/aws/lambda/ci/import-closure-check.py` exists and is **exactly** this class of check.

```
SILVER builder  build-and-upload.sh:257   RUNS it as a build gate   (it fired on my silver build tonight)
GOLD builder    build_package.py          occurrences: 0            <- NOT WIRED
```

**PROVEN BY EXERCISE, NOT INFERENCE** — built at the candidate pin locally (no upload, no deploy),
extracted, ran the checker against the materialized package:

```
build_package.py --pin 1234c8779e   ->  "OK ... modules=21"     <- THE BUILDER REPORTS SUCCESS
                                                                   ON A PACKAGE THAT CANNOT IMPORT
mdpf_category_registry.py in the built zip:  False
import-closure-check.py, TRUE rc = 1
   ! mdpf_category_registry   (imported by: mdpf_gold_consolidator.py)
```

⛔ **THE REMEDY IS BUILD-LADDER RUNG 2 — WIRE THE EXISTING CHECK INTO `build_package.py`. DO NOT BUILD
A NEW ONE.**

⚠ **AND IT CANNOT BE WIRED AS-IS — the one detail that decides whether the gate survives.** The same
run also flags `numpy pandas pyarrow yaml` because the gold manifest declares **`layers_expected`**
while the checker reads **`layer_dependencies`**. Wired unchanged it would FAIL EVERY GOLD BUILD on
four false positives, and **a gate that screams on every correct build gets switched off** — that is
how this estate loses gates. Align the manifest key (or teach the checker `layers_expected`) FIRST,
re-run, and require a clean pass before it gates anything. Routed as a candidate, not built here.

## 6. SEQUENCE (when released)

1. Re-run §1's 21-module scope table. **2+ changed = STOP and re-scope.**
2. Confirm DS~N's read is deploy-ready. 3. Re-run `resolve_immutable_pin`'s four rules against the
chosen pin (hex 7-40 / not a ref name / one object / type=commit) — **re-run, never inherit.**
4. Build locally; verify the BUILT artifact's members before upload. 5. **Open the ledger.**
6. Upload with `content-sha256` metadata; verify by live `head-object`, not the `cp` exit code.
7. Targeted plan → `safe-apply` → targeted 0-diff. 8. Battery §5 A1–A5 **plus the §5.6 exercise.**
9. Source-map record, **scoped by hand** — `record-terraform-deploy.sh` is unsafe on a dirty root
   (dry-predicted today: 7 updates, 6 false, 2 fabricated from `None`). 10. Close the ledger.

## 7. WHAT THIS PLAN DOES NOT DECIDE

Whether D1_CATVIEWS is CORRECT or deploy-ready — `0.4.0_DS_ClientPlatform~N`'s read, not re-derived
here. **When** it fires — held behind tomorrow's 13:30Z acceptance, `2.0.0_SA_COO` / `1.0.0_SA_CTO`.
And the source-map `last_deployed_commit` convention question raised at `445aac9002`: a mainline pin
makes it moot for this deploy, since the pin would be CLOUD-reachable — worth noting that this act
would *incidentally* retire the anomaly tonight's hotfix introduced.
