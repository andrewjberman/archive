# `battery_ib_s_9.result.md` -- S9-AC1, eleven arms, 11 of 11

**TO:** `IRPT_BCKEND.TO-IB-s-9` | **cell:** `IB-s-9` (PRD cell B9) | **assignee:** `0.9.0_WK_IRPT_BCKEND~3`
**Branch:** `wk-irpt_bckend-1-3` | **worktree:** `/c/tmp/wk-irpt-1-3` | **base:** `1f795d1f71`

**Invocation (the one the task order names):**
```
timeout 600 python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~3/battery_ib_s_9.py
```
**rc 0. Last line: `IBS9-GENERATION-CHAIN`. Full verbatim output (162 lines):
`org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~3/IB-s-9_S9-AC1_battery_output.txt`.**

The face grades seven lettered arms `(a)`-`(h)` plus `(v0.8)` and `(amend)`; the issuer supplement
(channel row `IRPT_BCKEND-S14`, PRD v0.10 @`3624e60def`) adds work that is graded inside a further
arm `(v0.10)` rather than by changing any arm the face wrote. **Eleven arms, `11 of 11`.**

---

## The arms

### (a) SEVEN OF SEVEN -- each recipe step against the replay -- `8 of 8`

Seven declared steps (`identity, template, upload, create, validate, generate, download`) plus the
`read_back`, which is a step the recipe performs and the face grades separately under `(d)`; the
battery runs and prints **8**. Every step `ok=True` with the captured status: `identity 200`,
`template 200`, `upload 200`, `create 201`, `validate 200`, `generate 201`, `download 200`,
`read_back 200`.

Identity is not "a 200 came back": all four legs must hold --
`{"authenticated": true, "email_match": true, "no_impersonation": true, "stable_user_id_match": true}` --
and the **wrong-user-id CONTROL is rejected (`True`)**, so the four legs are load-bearing rather than
decorative.

The multipart names are the MEASURED ones and are cited as such: upload field `'holdings'`, create
fields `['portfolio', 'items']`, PRD v0.8 SUPP VI.5 @`d67e9813b5`. The bound against INVENTION stands
for every other field; these were measured live by the estate and the issuer amendment names them.

A saved Overview template legitimately returning an **empty `sections` array** is accepted
(`True`) -- it is a measured vendor behaviour, not a parse failure.

### (b) SUBMITTING BEFORE THE SIDE EFFECT -- THE DIFFERENCE CONTROL

A kill (`InjectedKill`, a `BaseException` so no `except Exception` can swallow it) is injected
**after `submitting_before_create` and before the create response is recorded**.

| | correct build | broken build (`ResubmittingJob`) |
|---|---|---|
| state read on restart | `SUBMITTING` | `SUBMITTING` |
| intent claimed BEFORE the POST | `True` | `True` |
| resumed | `True` | -- |
| **re-submitted** | **`False`** | `True` |
| **create POSTs after restart** | **`0`** | **`1`** |
| adopted | `2332060` by `OWNED_BY_NAME` | -- |

The broken build is in the battery, not described by it: it is a subclass that re-POSTs the create on
restart, and the arm prints it FAILING. Without that half, "0 create POSTs" is a number with no scale.

### (c) NEVER THE NEWEST ROW

The replay's collection carries a newer FOREIGN portfolio: `id=2332999
created_at=2026-09-11T04:00:30Z name='Advisor B working copy'`, created after the owned one.
Reconciliation adopts **`2332060` by `OWNED_BY_NAME`**; `newest adopted: False`.

The owned name is **deterministic and derived BEFORE the submit** (`True`) -- which is what makes
reconciliation-by-identity possible at all. A name minted after the fact could only be matched by
recency, which is the bound this arm exists to hold.

Mutant **M1** replaces `reconcile_owned` with a recency rule and the arm's predicate goes
`true -> false`, adopting `2332999`. See `IB-s-9_mutant_control_output.json`.

### (d) SETTINGS READ BACK -- `7 of 7`

| setting | expected (`settings.json`, IB-s-7) | actual (read back) |
|---|---|---|
| `rebalance_frequency` | `quarterly` | `quarterly` |
| `reinvest_dividends` | `false` | `false` |
| `start_of_series` | `oldest` | `oldest` |
| `level_as_of_type` | `prior_close` | `prior_close` |
| `tax_status` | `non_qualified` | `non_qualified` |
| `benchmark_symbol` | `^SPXTR` | `^SPXTR` |
| `management_fee` | `0.003` | `0.003` |

**DRIFT CONTROL:** a replay that returns a drifted setting is DETECTED -- `6 of 7 matched,
drifted=['management_fee'], job outcome=SETTINGS_DRIFTED, job state=ATTENTION`. The job does not
"fix" the drift and does not proceed to READY: a vendor whose effective settings disagree with what
the request asked for is an ATTENTION state for a person, because the number's meaning changed.

### (e) BODIES PER S8

- **34-key August vs 33-key July**, root keys `34 / 33`, modal fields `34 / 32`. The July body is
  derived from August **by SUBTRACTION**, never written as a second forward list: the ONLY
  August-extra root key is `['branding_client_group_id']` and the only modal extras are
  `['brandingClientGroupId', 'requestedSectionOrder']`. A forward list could silently omit a field;
  a subtraction cannot lose one without the count disagreeing.
- **single `secondarySecurity` vs the Multi array:**
  `secondarySecurity.securityId` = `{"COMPARISON": "S:SPY", "MULTI": null, "OVERVIEW": null}` and
  `comparisonSecurities` length = `{"COMPARISON": 0, "MULTI": 2, "OVERVIEW": 0}`. The two carriers
  are mutually exclusive by variant, exactly as captured.
- **asymmetric null/empty fields**, printed with the TYPE per field rather than as "empty":
  `custom_security_labels list`, `custom_texts dict`, `dollar_conversion_levels list`,
  `reportState NoneType`, `risk_profile NoneType`, `saved_hypothetical_id NoneType`, `sections list`,
  `serialized_transition_analyses dict`, `talking_points dict`. `null` and `[]` and `{}` are not
  interchangeable to this vendor and the fixture records which is which.
- **duplicate cover fields agree: `True` across 7 pairs.**
- **cardinality is REFUSED when wrong:** `template 14141847 (MULTI) takes 2..5 comparison securities
  and 1 were supplied`.
- **templates read from `templates.json`** as CAPTURED CONFIGURATION, not constants in code:
  `['14141822', '14141824', '14141847']`.
- **`0` PUTs of global preferences**, censused over the whole run:
  `{"global_preference_writes": 0, "offending_routes": [], "requests_recorded": 7}` -- the
  denominator (7 requests) is printed beside the zero, because a zero over an unstated denominator is
  not a measurement.

### (f) THE 201 IS WRAPPED -- the job id is OPAL'S

- Opal attempt id `ATT-9fef11e014433c6027050eac` -- minted by Opal, deterministic per attempt.
- **vendor-job-id census over the attempt row:** `fields_walked 41`, `by_shape []`, `by_token []`,
  `vendor_job_id_fields []`. The census walks every field of the row by SHAPE and by TOKEN; there is
  nothing to invent because the vendor's measured 201 carries only `['report_url', 'zip_url']` --
  **no vendor background-job id exists in the response at all**, which is the fact the bound rests on.
- artifact key `firms/49financial/generations/2332060/attempts/0/vendor/report.pdf`, under the bound
  firm's generations prefix (`True`).
- PDF `sha256=cef3b030a93763cb bytes=193`, **credential headers sent `[]`, header names sent `[]`** --
  the separate unauthenticated client sends `[[]]` headers per request.
- **SIGNED-PARAM CENSUS over every log line:** `{"log_lines": 18, "occurrences": 0, "params_found":
  [], "signed_params_looked_for": 4}`. Four signed parameter names looked for across 18 log lines,
  zero occurrences.
- job states in order: `['CLAIMED', 'SUBMITTING', 'SUBMITTING', 'SUBMITTED', 'SUBMITTING',
  'DOWNLOADING', 'READY']` -- `SUBMITTING` is persisted before the side effect and again on the
  resumed leg.

### (g) SCHEMA-VALID -- the `AnalysisReport` attempt row

`validated=True` against `AnalysisReport.schema.json`; required members
`['request_ref', 'vendor_artifact', 'effective_inputs', 'sections', 'disclosures',
'extraction_validation', 'release']`.

`extraction_validation.status` is recorded **`UNCERTIFIED`**, not `CERTIFIED`: the four checks this
cell runs are STRUCTURAL (the PDF parses, its hash matches, its byte count matches, the artifact key
is under the bound prefix). Certification against a paired PDF is cell IB-s-10's, and claiming it
here would be a green this cell did not earn.

### (v0.8) THE MEASURED CONTRACTS AND THE DECISION TABLE, ON THE REPLAY

- upload field `'holdings'`; save fields `['portfolio', 'items']` -- PRD v0.8 SUPP VI.5 @`d67e9813b5`,
  MEASURED LIVE, not invented.
- full payload (34 keys) -> **201**; minimal payload -> **404, classified `CONTRACT_FAILURE`**, never
  session expiry and never `INVALID_RESPONSE`. This is the branch that matters most in practice: a
  404 that reads as "logged out" sends an operator to re-authenticate against a payload defect.
- fee `0` -> **422 `invalid_management_fee`**; the captured `0.003` annual recipe succeeds.
- empty `sections` accepted: `True`.
- **PDF client separate and unauthenticated: `True`; session-cookie headers on that request: `0`.**
- **JOB BUDGET: `26.76 s`** measured for the live Overview invocation against a `900 s` Lambda budget
  -- `33.6x` headroom, so a durable worker is NOT selected. Printed beside the measurement, not
  asserted: *a timeout NEVER licenses regeneration -- it marks the outcome UNCERTAIN and reconciles
  the owned object.*
- **DECISION TABLE -- `10 of 10` branches classified as declared:**

| fixture | status | classified |
|---|---|---|
| `HEALTHY` | 200 | `HEALTHY` |
| `ARTIFACT_FETCH_PENDING` | 201 | `ARTIFACT_FETCH_PENDING` |
| `REFRESH_401` | 401 | `REFRESH` |
| `REFRESH_EVICTION` | 403 | `REFRESH` |
| `INVALID_RESPONSE_HTML` | 200 | `INVALID_RESPONSE` |
| `BROWSER_CHALLENGE` | 405 | `BROWSER_CHALLENGE` |
| `WAF_REFRESH_REQUIRED` | 202 | `WAF_REFRESH_REQUIRED` |
| `DENIED` | 403 | `DENIED` |
| `BACKOFF_429` | 429 | `BACKOFF` |
| `RECONCILE_UNCERTAIN` | `None` | `RECONCILE` |

Note the two 403s and the two 200s: the same status classifies to DIFFERENT branches, which is the
whole point of a decision table rather than a status map. `ONE refresh allowed: True | repeat
eviction refused: True`.

### (v0.10) THREE RECIPES IN ONE HANDLER -- the issuer supplement

The packet `docs/research/investor_reporting_ycharts_variants_20260911/` @`72acd16e66` is **NOT in
this branch's ancestry** and was read **by object reference**; measured and filed as row
`IRPT_BCKEND-W3-S7`, with the reachability printed in arm `(h)` rather than left as a silence.

- **VARIANT FROM THE COMPARISON COUNT -- `3 of 3` correct.** `0 -> OVERVIEW/14141822`,
  `1 -> COMPARISON/14141824`, `2 -> MULTI/14141847`. **6 comparisons selects NO recipe** and is
  refused against the declared cardinalities `[(0,0,'OVERVIEW'), (1,1,'COMPARISON'), (2,5,'MULTI')]`.
  A DECLARED variant that disagrees with the count is refused:
  `VARIANT_CARDINALITY_MISMATCH: the caller asked for 'MULTI' and 1 comparison(s) derives
  'COMPARISON'`. The count is the authority; a caller's label is checked against it, never trusted.
- **PRE-ACCESS CONTROLS -- each with the vendor-request count AT THE REFUSAL:**

| control | refusal code | vendor requests |
|---|---|---|
| `account_scope_mismatch` | `CLIENT_ACCOUNT_SCOPE_MISMATCH` | **0** |
| `changed_inputs_same_request_id` | `CHANGED_INPUTS_SAME_REQUEST_ID` | **0** |
| `outside_catalog` | `COMPARISON_OUTSIDE_AUTHORIZED_CATALOG` | **0** |
| `server_controlled_field` | `SERVER_CONTROLLED_FIELD` | **0** |
| **total across all refusals** | | **0** |

  "Rejected BEFORE vendor access" is a claim about ORDER, so it is measured as a COUNT at the moment
  of refusal, not asserted by reading the code.
- **DUPLICATE RE-DELIVERY:** first run `READY` with **7** vendor requests; the duplicate ->
  **`EXISTING_ARTIFACT_REUSED` with 0** vendor requests, keyed on the committed receipt
  `firms/49financial/generations/REQ-abababababababababababab/attempts/0/receipt.json`. The
  7-versus-0 pair is the measurement; either number alone is not. Mutant **M2** removes the receipt
  check and the duplicate costs **7** requests again.
- **WAF:** the same 202 **WITH** the `x-amzn-waf-action` header -> `WAF_REFRESH_REQUIRED`;
  **WITHOUT** it -> `INVALID_RESPONSE`. The measured case is a 202 during calculation polling whose
  ONLY signal was that response header. The carried `recovery_contract.decision()` reads the BODY and
  cannot see it -- row `IRPT_BCKEND-W3-S8`. Mutant **M3** strips the header rule and the verdict
  reverts to `INVALID_RESPONSE`, so the new rule is load-bearing.
- **COMPARISON CATALOG:** 4 entries, 4 typed `model_portfolio`, 3 live-proven:
  `['P:1728413', 'P:1728415', 'P:1728315', 'P:1728420']`.
- **MEASURED VARIANT OUTPUTS (the CRO's live run, not this cell's):** `14141822` 23 pages portrait
  573677 bytes; `14141824` 31 pages portrait 820984 bytes; `14141847` 35 pages landscape 854115
  bytes. Recorded as measurements with their owner named, because they are not this cell's to claim.
- **UPLOAD RECONCILED (not merely parsed): `True`** -- 2 rows sent, 2 echoed, unit `'Dollars'`.

### (amend) GUARDED, BOUND, AND SILENT ON THE REFUSED VALUE

**This cell ships NO route handler.** The generation job is a QUEUE CONSUMER woken by
`irpt-generation`, not a handler the edge reaches. So:

- `unguarded_routes(job.ROUTES) -> 0 of 0 unguarded`, and **the census is declared VACUOUS
  (`True`)** rather than reported as a pass. `routes.json` is IB-s-15's deliverable at
  `infra/aws/terraform/investor-reporting/api/routes.json` and does not exist before that cell lands
  (channel row `S13`, adopted from this worker's `W3-S5`).
- **The two CONTROLS carry the arm instead:** an UNGUARDED handler wired to a route censuses
  `1 of 1 unguarded`; the SAME handler wrapped by `guard()` censuses `0 of 1`. The censor is proven,
  not an empty set.
- public callables added by this cell: **17**, route-reachable: **0**.
- **FIRM BINDING:** a non-reconciling binding -> `ok=False code=FIRM_BINDING`, **opaque id echoed:
  `False`**. The refusal says the binding does not reconcile *"rather than returning an empty result,
  which a caller cannot tell apart from a revocation"* -- row W2-S9's exact failure mode.
- **`_keys` SILENCE:** `code=KEY_REFUSED`, audit entries `1`, envelope `809 bytes`,
  **OCCURRENCES OF THE REFUSED VALUE: `0`** over the WHOLE envelope (body + reason + audit trail),
  not over the census alone. The reason carries parameter NAMES only:
  `1 of 2 key parameter(s) were refused by the key grammar: ['client']`.

### (h) NOTHING LEFT THE MACHINE; THE LEDGER CLOSED

- **netguard:** `0 external of 0 connection attempt(s)`. The battery states plainly why that is weak
  on its own -- *"a 0-of-0 refusal count is vacuous on its own"* -- and carries the arm on a
  **POSITIVE CONTROL: attempted `ycharts.com:443` -> `refused=True`, guard external `0 -> 1`**. A
  guard that cannot go non-zero is a constant wearing a measurement's clothes.
- replay requests made by the chain: **7**, over the 7 captured routes.
- **served bytes:** `CodeSha256 S9C9ibDNI8D77ZUefrAQSq2OgwO1206wySuzfolxUhI=` ==
  **rebuilt zip** (81065 bytes, 25 members) == **source-map registration**. Verified against the
  BUILD INPUT, never by filename. `Layers: None | Timeout: 900s`. (This is the artifact's SECOND
  revision -- see the manifest repair below.)
- the IB-s-8 host `i-0167fd745ad906a66` after this cell's apply: **`stopped` (untouched)**.
- ledger `20260911T0417Z_irpt-bckend-s9_deploy_completion.md`: `CLOSED=True, legs=5, open markers=0,
  sentinel on disk=False`, with **BOTH of the sentinel's commits printed** -- `9e40afcf4a` (OPEN,
  before the upload and the apply) and `a0e05b957d` (close). That ordering is this worker's own
  IB-s-6 finding (row `IRPT_BCKEND-W3-S4`) applied as the rule it asked for: the open window now
  exists in git, not only in the entry's header.
- **THE VARIANTS PACKET IS NOT IN THIS BRANCH (row W3-S7):** `{"present_in_worktree": false,
  "files_at_72acd16e66": 26, "commit_is_ancestor_of_head": false,
  "positive_control_known_ancestor": true}`. The positive control is there because an
  `is-ancestor` that answers NO to everything answers nothing.
- **FIXTURE MANIFEST RE-DERIVED FROM DISK (row W3-S9): `13 of 13` rows match, 13 files on disk,
  `0` unlisted; declared `{"decision_branches": 10, "files": 13}` vs counted
  `{"decision_branches": 10, "files": 13}` -- disagreeing: `none`.** Added at report time. See
  the repair below.

### The manifest repair, and why there was a second deploy

`FIXTURE_MANIFEST.json` is the artifact that says which fixtures are MEASURED and which are
EXTENDED -- it is the carrier the `S9-AC3` judgment record points the CVO at for exactly that
split -- and **it had gone stale in this cell's own package.** The supplement commit `88c97c1529`
changed two of the fixtures it describes and did not regenerate it. Found at report time by
RE-DERIVING every row from disk rather than reading the manifest:

| | declared | actual |
|---|---|---|
| `decision_branches.json` | `ab7c405441..` / 1621 B | `e55589ccba..` / 2545 B |
| `upload_ok.json` | `18263ec209..` / 463 B | `5249e5b855..` / 753 B |
| `_meta.denominators.decision_branches` | `9` | `10` |
| `_meta.denominators.templates_with_live_proof` | `1` | `3` |

plus prose still reading *"NO LIVE PROOF EXISTS for templates 14141824 and 14141847"*, which the
issuer supplement contradicts (all three proven live by `4.0.0_SA_CRO` on Andrew's word -- the
CRO's measurement, cited with its owner, never this cell's).

**A stale hash in a provenance record is worse than no hash,** because it reads as MEASURED: a
reader checking a fixture against it gets a false MISMATCH on a good file and cannot tell that
from a tampered one. This is Rule 22's shared-dependency blindness in a new place -- every
fixture verified fine individually; what was broken was the one artifact they have in COMMON, and
no per-fixture check could see it.

Repaired BY RECOMPUTATION, never by hand, with the file list taken from the DIRECTORY BY
SUBTRACTION so a fixture added without a manifest row cannot hide. **The manifest is a packaged
zip member (12 of 25), so the repair required a redeploy** -- leaving it repaired-but-not-served
would have broken the `served == rebuilt` equality this very arm grades. Second change-management
entry `irpt-bckend-s9-manifest`, five legs, sentinel committed OPEN at `a2c335b99e` before the act
and removed at `2146d82bd2`. Artifact
`gYMxOLN8XndUFeK54aP/A5HsxhOsTSrY62GijStzmH4=` -> `S9C9ibDNI8D77ZUefrAQSq2OgwO1206wySuzfolxUhI=`.
Filed as row `IRPT_BCKEND-W3-S9`. The estate-wide gate this finding suggests was **not** built --
that would widen this order.

---

## Controls

**MUTANTS -- four, all FIRED** (`IB-s-9_mutant_control.py`, output
`IB-s-9_mutant_control_output.json`, `mutants_fired_as_expected: true`):

| | mutation | baseline | mutant |
|---|---|---|---|
| **M1** | `reconcile_owned` adopts the NEWEST row | adopts `2332060`, newest `False` | adopts `2332999`, newest `True` -- arm (c) predicate FALSE |
| **M2** | the duplicate receipt check removed (`MemoryBlobs.head -> None`) | duplicate `EXISTING_ARTIFACT_REUSED`, **0** vendor requests | duplicate `READY`, **7** vendor requests -- arm (v0.10) predicate FALSE |
| **M3** | the WAF header rule removed from `decision()` | `WAF_REFRESH_REQUIRED` | `INVALID_RESPONSE` -- arm (v0.10) predicate FALSE |
| **M4** | ONE BYTE appended to a described fixture, on a COPY, without touching its manifest row | `13 of 13` rows match, `fresh true` | `12 of 13`, `stale_rows ['upload_ok.json']`, `fresh false` -- arm (h) predicate FALSE |

M4 exists because the check it controls was ADDED at report time in response to row `W3-S9`, and
**a freshness check that has only ever seen a fresh manifest is a constant wearing a
measurement's clothes.** It is exercised on a copy in `.scratch/`; no packaged fixture is touched.

A fifth mutant is not in that file because it **ships inside the battery**: arm (b)'s
`ResubmittingJob` is a deliberately broken build that re-POSTs the create, and the arm prints it
failing.

**DETERMINISM:** two full runs of the battery compared line by line -- `lines 162 162 | identical:
True | differing: 0`, and the GRADED run is byte-identical to both (`graded run identical to run
A: True`), so the recorded output is not a third, luckier run. Every arm verdict, every count and
every denominator is stable, and all three printed `IBS9-GENERATION-CHAIN` at rc 0. Nothing in
this battery binds an ephemeral port or stamps a wall-clock time into a deciding line.

---

## What this arm set does NOT show

Stated here rather than left for a reader to discover; the fuller version is the `S9-AC3` judgment
record, which is graded by `3.0.0_SA_CVO` at L9 and carries no verdict of mine.

1. **No live YCharts call was made, by construction.** Every response is a recorded or extended
   fixture. The three variants' live proof is the CRO's, on Andrew's word, recorded in the packet at
   `72acd16e66` -- it is cited as a MEASUREMENT WITH AN OWNER, never restated as this cell's.
2. **Two captured responses had to be EXTENDED** -- the upload body and the two-comparison-only Multi
   example. Both are separated from the measured ones in
   `fixtures/har/FIXTURE_MANIFEST.json` (`MEASURED` vs `EXTENDED`), so no reader has to trust the
   battery's framing to tell them apart.
3. **The replay cannot produce a genuinely ambiguous create.** It can inject a kill and it can return
   a `None` status; it cannot produce the case where the vendor's write landed and the response was
   lost on a network the test does not own.
4. **`extraction_validation` is `UNCERTIFIED`,** deliberately. See arm (g).
