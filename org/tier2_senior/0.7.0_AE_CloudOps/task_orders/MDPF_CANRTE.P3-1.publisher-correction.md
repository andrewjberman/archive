<task_order>
  <metadata>
    <id>2.0.0_SA_COO~Z-2026-08-06-publisher-correction</id>
    <issued_by>2.0.0_SA_COO~Z</issued_by>
    <issued_to>0.7.0_AE_CloudOps~Z</issued_to>
    <date>2026-08-06</date>
    <status>staged</status>
    <project_code>MDPF_CANRTE</project_code>
  </metadata>

  <objective>
    Correct `opal-assets-mdpf-portal-publisher` so it stops republishing frozen gold with a fresh process
    timestamp, derives completeness from EXPECTED scopes rather than listing discovery, and writes an
    immutable publish manifest — **without changing one byte of the served contract.**
  </objective>

  <context>
    ### THE MEASURED DEFECT

    The publisher ran at 09:50 ET on **both** August 5 and 6 and reported **14/14 writes both days**. On
    August 6 it wrote **the exact same source vintages as August 5** (aggregates 08-03; 49F/inflection/global
    account distribution 08-04; cottonwood 08-03). All four served aggregates reported
    `as_of_last=2026-08-03` with `_provenance.written_at=2026-08-06T13:50:48Z`.
    **ETags changed BECAUSE THE PUBLISHER INJECTED A NEW PROCESS TIMESTAMP.**

    ⇒ **NEITHER LastModified NOR ETag PROVES DATA FRESHNESS ON THIS SURFACE.** A green 14/14 is exactly what
    the defect produces.

    ### ⛔ HARD ORDERING — P2-1 LANDS CONFIG BEFORE THIS TO DEPLOYS

    Grounded on both ends, not asserted:
      DEPLOYED artifact (via `get-function`, 3,583 bytes, denominator 1 entry, 173 lines): **ZERO**
      references to `roster` / `ROSTER` / `partner_roster` / `EXTRA_EXPECTED` / `expected_scopes`.
      REPO TIP: 230 lines, **21** roster refs, plus a 98-line `tests/test_completeness.py` with 17.
      `config/mdpf/` **does not exist as a prefix at all** (measured 21:13Z, positive-controlled).
    **A blind rebuild from repo tip reads an object that is not there.** Magnitude of the change: 173 → 230
    lines of behaviour. **This is a 33% behavioural expansion of a live serving component — treat it as new
    behaviour being introduced, not as a patch.**

    ### THE ROSTER: SYMMETRIC, RULED (CTO~Z 220204Z)

    **The publisher takes a BUILD-GENERATED, HASH-TIED copy of the same committed authority.
    NO `ROSTER_BUCKET`, NO `ROSTER_KEY`, NO GetObject leg.** Three reasons, and the third is the decisive one:

    1. Because the deployed publisher has ZERO roster resolution today, **we are not reconciling an
       inherited divergence — we are choosing whether to CREATE one.** Having measured this morning what a
       divergence surface costs (nine days stale on a live threshold, undetected), deliberately building a
       second one would be indefensible. **It is far easier to decline to create a hazard than to remove
       one, and this is the rare moment we get the easy version.**
    2. **The apparent case for S3 does not survive contact.** "Update expectations without a redeploy"
       describes a scenario that does not exist: a roster change means a partner onboards or a cadence
       changes, which requires GOLD to build that firm's artifacts — a roster row plus route bindings plus
       almost certainly code. **THE ROSTER CHANGING IS NEVER A PUBLISHER-ONLY EVENT.** So the "benefit" is a
       hazard: it lets the publisher's expected-scopes drift ahead of or behind what gold produces, **and
       noticing that gap is the publisher's entire job. AN EXPECTATIONS SOURCE THAT CAN MOVE INDEPENDENTLY
       OF THE PRODUCER IS AN EXPECTATIONS SOURCE THAT CAN LIE ABOUT COMPLETENESS.**
    3. **SYMMETRY IS WHAT MAKES THE CROSS-COMPONENT INVARIANT CHECKABLE.** With both components on
       build-generated copies, BOTH record a roster hash in their manifests — so `gold-hash != publisher-hash`
       is a DETECTABLE statement that they were built from different commits. **Put one on S3 and one on a
       build copy and THERE IS NOTHING TO COMPARE: the divergence becomes real and invisible in the same
       move** — the nine-day failure mode rebuilt across components instead of within one.

    ### H8 IS RESOLVED, AND THE PACK'S CHARACTERISATION IS WRONG IN A WAY THAT MATTERS HERE

    Provenance is RECONSTRUCTED AND VERIFIED: source-map `artifact_sha256` == live `CodeSha256`, TIE TRUE,
    negative-controlled (`mdpf-daily-trigger`'s hash → False). `last_deployed_commit` `63eea3814` real with a
    matching subject.

    `01` §10 frames THREE source-map fields as stale. **Only ONE is.** `artifact_sha256` ACCURATE ·
    `last_deployed_commit` ACCURATE · the "build-alongside" note ACCURATE **because the deployed thing IS
    still the build-alongside publisher** · `iam_role` **STALE** (map: `...-portal-publisher-role`; live:
    `...-egress-publisher-role`).

    > **A SOURCE MAP IS NEVER UNIFORMLY FRESH OR STALE. IT IS FRESH PER-FIELD, ACCORDING TO WHAT LAST TOUCHED
    > THAT FIELD'S SUBJECT.** Code-side fields update on a CODE DEPLOY; the role field changes when IAM
    > changes — **which can happen without a code deploy, and did.** Reading it as one artifact with one
    > freshness is the error the pack made.
  </context>

  <compiler_tools_mandate>
    Phase 1 — before writing:
      <run>comp-routes behaviors</run>
      <expect>CloudFront error rules that could mask a JSON error on the served path.</expect>
      <if_mismatch>A CF error rule masking a 4xx/5xx changes what "the portal reads it" means; report to COO~Z.</if_mismatch>

      <run>comp-blast opal-assets-mdpf-portal-publisher</run>
      <expect>Blast radius WITH DENOMINATOR; every served consumer named.</expect>
      <if_mismatch>A ZERO is a LOWER BOUND. Corroborate with a literal-key grep.</if_mismatch>

    Phase 2 — before committing:
      <run>comp-iam service opal-assets-mdpf-portal-publisher</run>
      <expect>DESIRED grants for the corrected function.</expect>
      <if_mismatch>NECESSARY NOT SUFFICIENT — models (action) never (action, resource), and FAILS GREEN.
      Any new key needs `simulate-principal-policy`, ONE `--resource-arns` per call, positive control in a
      SEPARATE invocation.</if_mismatch>

    Phase 3 — after committing:
      <run>comp-pipescript deployed</run>
      <expect>MATCH.</expect>
      <if_mismatch>STALE/MISSING is a blocker.</if_mismatch>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <shared_resource>`config/mdpf/route_bindings.yaml` + the build-generated roster copy</shared_resource>
    <also_in_to>P2-1 (creates the prefix and the objects)</also_in_to>
    <last_write_owner>0.7.0_AE_CloudOps~Z (both TOs)</last_write_owner>
    <required_action>⛔ **P2-1 LANDS FIRST. HARD.** Deploying repo-tip publisher behaviour before the config
    objects exist introduces a read against a missing object.</required_action>

    <shared_resource>`portal/gold/mdpf/{scope}/{type}/{as-of}.json` — the publisher's source</shared_resource>
    <also_in_to>P1-1 (DS~Z produces it) · P4-1 (cutover)</also_in_to>
    <required_action>The publisher must consume the EXACT canonical keys the new gold Lambda writes. MCP
    DS~Z if the artifact grammar shifts.</required_action>

    <shared_resource>The 14 served platinum pairs + `json/mdpf/*`</shared_resource>
    <also_in_to>P0-1 (schema baseline is this TO's verification input) · P6-3</also_in_to>
    <required_action>The P0-1 per-key schema baseline (`@db5f37b11`) is what criterion 6 asserts against.
    It exists BECAUSE doc 04's schema constraint had no input; use it rather than re-deriving.</required_action>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. UNCHANGED SOURCE ⇒ NO REWRITE. Before `PutObject`, compare the destination's recorded immutable
       source key AND source content hash. If unchanged, return `status=unchanged` and **do not rewrite the
       served object.**
       FORBIDDEN SHORTCUT, NAMED: **"14/14 written" IS THE DEFECT, NOT THE PASS.** The measured 08-05/08-06
       runs both reported 14/14 while republishing identical vintages. A run reporting 14 published with 14
       UNCHANGED SOURCE HASHES and 14 new destination ETags has reproduced the bug with a green light on it.

    2. DATA-AS-OF IS PRESERVED, NEVER SUBSTITUTED. On a real change, the artifact's own as-of field carries
       through untouched. **Process time belongs in the manifest/provenance and NOWHERE ELSE.**
       Assertion level is CORRECTNESS: pin the VALUE, not the presence of a field.

    2a. **THE DAILY CONTRACT IS 12 OBJECTS — ANDREW-RULED 2026-08-06 ~2205Z.** VERBATIM: *"3 files times 4
       scopes means that this pipeline needs to generate 12 platinum files into the relevant scope path
       buckets in opal-data-portal-v2/platinum/mdpf/{scope} every single day."*
       `{global, 49financial, inflection, cottonwood}` × `{aggregate-aua-timeseries.json, aum-metrics.json,
       account-distribution.json}`.
       **"EVERY SINGLE DAY" IS PART OF THE RULING. 12 IS A DAILY COMPLETENESS DENOMINATOR — a cycle emitting
       fewer than 12 is INCOMPLETE, not merely quiet.**
       FORBIDDEN SHORTCUT, NAMED: this is the governing outcome-not-intervention criterion applied to the
       daily contract. **ACCEPTANCE ASSERTS THE 12 OBJECTS EXIST FOR THE DAY. It does NOT assert "the
       publisher ran," "the schedule fired," or "12 writes were attempted."**
       ⚠ COMPOSES WITH CRITERION 1, and the two are not in tension: an `unchanged` result still satisfies
       "the object exists for the day" — what fails is an object ABSENT, or one whose data-as-of never
       advances while its source did.
       ✅ **12-vs-14 RESOLVED, Andrew-direct ~2215Z: EXACTLY 12, AND THE EXTRAS' INFORMATION FOLDS IN.**
       `account-units` count → into `account-distribution.json`; non-model assets → into BOTH
       `aum-metrics.json` and `aggregate-aua-timeseries.json`. **So 12 IS THE FINAL EXPECTED DENOMINATOR**
       and criterion 3a's bidirectional check has its complete expected set: **anything else under the
       scope paths is UNEXPECTED and flags.**
       ⚠ **BUT NOT YET — ORDERING IS CORRECTNESS HERE.** `cottonwood/account-units.json` and
       `global/non-model-assets.json` were written by TODAY's live cycle; they are CURRENT output.
       **THEY RETIRE ONLY AFTER THE FOLDED FIELDS ARE VERIFIED IN THE CANONICAL 12** (P1-1's work).
       **NOTHING STOPS BEFORE ITS REPLACEMENT IS PROVEN.** Until then the publisher continues emitting
       them and they are EXPECTED, not unexpected.
       ⚠ **PLATINUM NEVER PATCHES SHAPE.** Vendor divergence dies in GOLD. If the folded fields are absent
       or scope-specific when they reach you, that is a P1-1 defect to report — **do not compensate for it
       in the publisher.** Canonical serve shape comes from an already-canonical gold.
       ⚠ **H6 IS DISCHARGED THROUGH THE FOLD, NOT VIOLATED BY IT** — it is the "separately tested schema
       migration" doc 04 anticipates. That licenses the fold and NOTHING ELSE: every other served field
       stays exactly as the P0-1 baseline recorded it.

    3. COMPLETENESS DERIVES FROM EXPECTED SCOPES, NOT FROM LISTING DISCOVERY.
       FORBIDDEN SHORTCUT, NAMED: **A MISSING SCOPE CANNOT DISCOVER ITSELF.** An expected scope absent from
       gold makes completeness NON-GREEN even when listing discovery otherwise succeeds. Missing
       roster/config is `UNKNOWN`/failed manifest status — **never silent listing-derived success.**
       Unrecognized gold grammar is SURFACED, not skipped.

    3a. ⛔ **THE CHECK IS BIDIRECTIONAL — ENUMERATE ACTUAL KEYS, FLAG UNEXPECTED ONES TOO.**
       Measured live (CVO~Z, s3api UTC, `opal-data-portal-v2` prefix `platinum/mdpf/`, 461 objects /
       **17 non-archive**):
         Andrew's **12** — all present, all written today in one publisher cycle.
         The **2 extras** (`cottonwood/account-units.json`, `global/non-model-assets.json`) — **ALSO written
           today, same cycle. THEY ARE LIVE, NOT VESTIGIAL.** Retiring them removes something CURRENT.
         **THE OTHER 3** — `49financial/`, `global/`, `inflection/` `aggregate_aua_timeseries.json`
           (**UNDERSCORE**), all at `2026-07-31T15:00:01+00:00`. **SIX DAYS STALE, IN THE SERVED BUCKET.**

       **A 12-of-12 PASS AND A 14-of-14 PASS ARE EACH FULLY GREEN WITH THREE STALE FILES ON THE SERVED
       SURFACE.** And this is not a counting oversight: the `(scope, artifact-type)` PAIR MODEL NORMALISES
       `aggregate_aua_timeseries` and `aggregate-aua-timeseries` TO THE SAME TYPE, **so the pack's own
       14-pair denominator STRUCTURALLY CANNOT REPRESENT THEM AS DISTINCT ROWS.** The data model cannot see
       them, so no amount of care with the count would have found them.
       ⇒ **Enumerate ACTUAL KEYS under each scope prefix and compare to the expected set in BOTH
       DIRECTIONS.** An expected-set check that only asks *"are my 12 there"* is ONE-DIRECTIONAL and passes
       on a served surface carrying arbitrary extra stale content.
       ⚠ These look like residue of the underscore/undated→hyphen promotion doc 02 marks the 09:40 bridge
       RETIRE for — **and retiring the bridge does not by itself remove what it left behind.**
       ⛔ DO NOT DELETE THEM. Served keys are NEVER#3 and Andrew's call. Report them.

    3b. ⛔ **EXISTENCE IS NOT THE WHOLE CHECK — AN A PRIORI DENOMINATOR MAKES A PASS CHEAP.**
       12 files at 12 known paths **reads identically whether they are fresh or frozen**, so a 12/12
       EXISTENCE check **WOULD HAVE PASSED ON EVERY FROZEN DAY** — including 08-05 and 08-06, the exact
       defect this TO exists to fix.
       So criterion 2a's daily-contract assertion is NECESSARY AND NOT SUFFICIENT: it must be evaluated
       **together with** criterion 1's source-hash comparison and doc 04 §3's **"read served object BODIES,
       not LastModified alone."**
       FORBIDDEN SHORTCUT, NAMED: **do not let the count getting easy retire the body read.** The freshness
       question is answered by the body and the source hash; the 12 answers only the coverage question.

    4. THE ROSTER IS A BUILD-GENERATED, HASH-TIED COPY. **NO `ROSTER_BUCKET`, NO `ROSTER_KEY`, NO GetObject
       leg** — CTO~Z ruled symmetric with gold.
       FORBIDDEN SHORTCUT, NAMED: do not add an S3 read "so expectations can be updated without a redeploy."
       That scenario does not exist — the roster changing is never a publisher-only event — and it would let
       expected-scopes drift independently of the producer, which is the one thing this component exists to
       detect.

    5. THE MANIFEST FULLY DETERMINES EXPECTED SCOPES. Record the roster hash **AND whatever carries the
       non-partner `global` scope** (doc 02 has it as an explicit config row; an env var is acceptable).
       FORBIDDEN SHORTCUT, NAMED: an unhashed `global` carrier is **a third input to expected-ness arriving
       through the side door**, and it reintroduces exactly the problem criterion 4 closes.
       The manifest must also carry: schema version, trigger identity, scheduled time, start/completion
       process times, repository commit, artifact hash, route-binding hash; expected frontiers by feed and
       actual partitions read; per scope/type source key + source content hash + data-as-of + destination
       key/version/ETag; and `published` / `unchanged` / `skipped` / `carried_forward` / `conflict` / errors.

    6. THE SERVED CONTRACT IS BYTE-COMPATIBLE, VERIFIED PER KEY AGAINST THE P0-1 BASELINE (`@db5f37b11`).
       FORBIDDEN SHORTCUT, NAMED: **DO NOT SAMPLE ONE KEY PER ARTIFACT FAMILY.**
       `global/aggregate-aua-timeseries.json` carries `count_as_of` and its twelve siblings do not — a
       family-level sample that picked a firm key would certify a schema the global key does not have.
       H6 binds: **seven as-of families are FACTS TO PRESERVE.** `as_of_date` appears in 2 of 23 sampled
       objects and is **NOT** a convention to align to.

    7. PER-KEY ISOLATION HOLDS AND OVERALL STATUS IS HONEST. One key's failure does not suppress other keys,
       and the overall manifest remains NON-GREEN. Third state present: `skipped` and `carried_forward` are
       distinct from `published` and from `unchanged`.

    8. THE SOURCE MAP'S **ROLE** FIELD IS CORRECTED AND ITS CODE-SIDE FIELDS ARE LEFT ALONE.
       FORBIDDEN SHORTCUT, NAMED: **DO NOT "FIX" `artifact_sha256`, `last_deployed_commit`, OR THE
       "build-alongside" NOTE — ALL THREE ARE ACCURATE.** The pack's framing invites distrusting them, and a
       well-meant cleanup there would INJECT the drift the map currently does not have.
       Update the code-side fields only as a consequence of THIS deploy actually changing them.

    9. AN IMMUTABLE PUBLISH MANIFEST IS WRITTEN EVERY RUN at
       `platinum/mdpf/_manifests/YYYY-MM-DD/{run-id}.json` — **including on an all-unchanged run.** An
       optional `latest.json` pointer may be mutable; history may not.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="modify">infra/aws/lambda/opal-assets/opal-assets-mdpf-portal-publisher/lambda_function.py</file>
      <file action="modify">infra/aws/lambda/opal-assets/opal-assets-mdpf-portal-publisher/tests/test_completeness.py</file>
      <file action="modify">infra/aws/lambda/ci/lambda-source-map.json</file>
      <file action="modify">infra/aws/terraform/opal-assets/mdpf_portal_publisher.tf</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Unchanged source key+hash never rewrites the served object.</requirement>
    <requirement id="2">Data-as-of preserved; process time only in manifest/provenance.</requirement>
    <requirement id="3">Completeness from expected scopes; a missing scope cannot discover itself.</requirement>
    <requirement id="4">Build-generated hash-tied roster; no S3 read leg.</requirement>
    <requirement id="5">Manifest fully determines expected scopes, including the `global` carrier.</requirement>
    <requirement id="6">Served contract byte-compatible, verified PER KEY against P0-1.</requirement>
    <requirement id="7">Correct only the source map's role field.</requirement>
    <requirement id="8">Deploy only after P2-1 lands the config objects.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">Corrected publisher + tests + source-map role fix + TF, committed to your lane on SITEZ (push is MSTR~Z's, :55-:00)</deliverable>
    <deliverable type="document">Per-key served-contract comparison against the P0-1 baseline</deliverable>
    <deliverable type="document">Session log with a Compiler Tools section</deliverable>
  </deliverables>

  <do_not>
    <rule>DO NOT DEPLOY BEFORE P2-1 LANDS THE CONFIG OBJECTS. Repo tip reads a roster; `config/mdpf/` does
    not exist as a prefix.</rule>
    <rule>DO NOT ADD ROSTER_BUCKET / ROSTER_KEY / A ROSTER GetObject LEG. Ruled symmetric with gold.</rule>
    <rule>DO NOT MOVE, RENAME, OR TEAR DOWN SERVED OUTPUT. `json/mdpf/*` keeps its `period` convention; the
    hyphenated legacy `account-distribution.json` is a LIVE SERVED PORTAL BELL. NEVER#3 binds and the
    `json/mdpf/*` teardown is PARKED.</rule>
    <rule>DO NOT NORMALISE, RENAME, OR RECONCILE ANY SERVED FIELD. Seven as-of families are facts (H6). This
    is an infrastructure cutover, not a schema migration.</rule>
    <rule>DO NOT "CORRECT" THE SOURCE MAP'S ACCURATE FIELDS. Only the role field is stale.</rule>
    <rule>DO NOT ADD NON-ASCII TO `lambda-source-map.json`, and read it with EXPLICIT utf-8 — it already
    carries mojibake and two C1 control characters that crash a cp1252 default. Routed to CTO base; do not
    absorb the cleanup.</rule>
    <rule>DO NOT TREAT LastModified OR ETag AS FRESHNESS EVIDENCE on this surface. Read served object BODIES.</rule>
    <rule>NO NEW GATES. NO SHADOWS — no second publish path, no parity comparator. NO ALARMS, SNS TOPICS,
    SES SENDS, FRESHNESS CHECKERS, OR MONITORS: the manifest is a RECORD, and the three MDPF alarms are
    being RETIRED, not replaced.</rule>
    <rule>NEVER call a feed stale without resolving the TRADING CALENDAR first, in TRADING DAYS. Per-feed
    cadence is NOT one shared date.</rule>
    <rule>DO NOT use the shared dirty checkout as build input. Never rebase on SITEZ. Commit to your lane;
    push is MSTR~Z's. Working files in the scratchpad.</rule>
  </do_not>
</task_order>
