<task_order>
<id>OPAL_KIMIPIPELINE.DEP2</id>
<title>Deploy f023857ab -- DELIVER the corpus to the model (it was never handed over) + kill the silent mid-string truncation. Same act as DEP1, new vintage.</title>
<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-05</issued>
<status>staged</status>
<priority>P0-class defect, P1 window</priority>

<references>
  <ref type="commit">f023857ab3 -- THE DEPLOY VINTAGE (1.0.0_SA_CTO~B, 1133Z). Supersedes a254104b34 (deployed 14:56:59Z, correct as far as it went).</ref>
  <ref type="acceptance">3.0.0_SA_CVO @155105Z -- EXERCISED SPECIFICALLY AT f023857ab. Their PRIOR acceptances (@95d6a8d3d, @72a187048) DO NOT COVER THIS VINTAGE; they ran new limbs and returned SHIP IT.</ref>
  <ref type="source-of-truth">infra/aws/ec2/EC2_MANIFEST.json:571 -- re-upload IS the deploy; verify head-object ETag vs local md5, never rc=0.</ref>
  <ref type="predecessor">OPAL_KIMIPIPELINE.DEP1 -- complete 145659Z. Same act, same key, same verification.</ref>
</references>

<context>
THE DEFECT (CVO found ~1530Z, CTO~B re-derived independently): the corpus was COMPUTED, LOGGED,
WRITTEN INTO THE ARTIFACT AND COUNTED INTO THE MANIFEST -- and never passed to `build_prompt`, which
had no corpus parameter. Kimi has been reasoning from the git appendix alone and has NEVER seen the
human-ruling half that Andrew's ruling 6 calls the entire point.
Compounding: the git half it did receive was `json.dumps(...)[:60000]` -- a silent mid-string cut. On
today's 69,495-char payload that dropped 9,495 chars and THE RESULT DID NOT PARSE AS JSON. The model
received invalid input with no way to know.

WHAT THIS IS NOT: DEP1 improved the FRESHNESS REPORTING of a payload the model never read. That was
still the right fix -- humans and CVO read that artifact, and the honest reporting is what made THIS
defect findable (a blanket `degraded_sources []` all-clear would have kept "counted but never
delivered" invisible, since presence was the only predicate and the corpus WAS present). But DEP1 on
its own did not put the corpus in front of the model. DEP2 does.
</context>

<the_deploy_act>
  <what>A SINGLE S3 PutObject. Identical act to DEP1.</what>
  <target>s3://opal-estate-report/code/estate_report_runner.py</target>
  <source>infra/aws/ec2/estate-report-runner/estate_report_runner.py @f023857ab3</source>
  <NOT>NOT safe-ec2-deploy.sh. NOT SSM. Transient box; systemd oneshot pulls on boot.</NOT>
  <window>Before the 2026-08-06 13:00Z BOOT.</window>
</the_deploy_act>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>aws s3api head-object --bucket opal-estate-report --key code/estate_report_runner.py</run>
      <expect>Records the CURRENT served state -- which is DEP1's artifact, ETag a110981492b461e19fb9be7848b9ad09, 62875 B. Record all three values before overwriting.</expect>
      <if_mismatch>If the ETag is NOT a110981492b461e19fb9be7848b9ad09, someone deployed between DEP1 and now -- STOP and surface to COO.</if_mismatch>
    </step>
    <step>
      <run>git log -3 --oneline -- infra/aws/ec2/estate-report-runner/estate_report_runner.py</run>
      <expect>f023857ab3 IS THE TIP. *** RE-DERIVE THIS YOURSELF; DO NOT INHERIT THE PIN. *** Two deploys in three hours on one file is exactly when a pin must not be trusted -- DEP1's original pin went stale in 22 minutes.</expect>
      <if_mismatch>Anything above f023857ab3 -> STOP, surface to COO. Vintage is CTO~B's call, acceptance is CVO's. Do NOT pick a commit yourself in either direction.</if_mismatch>
    </step>
    <step>
      <run>git diff f023857ab3 -- infra/aws/ec2/estate-report-runner/estate_report_runner.py</run>
      <expect>EMPTY. The bytes you hash ARE the bytes CVO exercised, by construction.</expect>
      <if_mismatch>STOP. A non-empty diff means you would ship something nobody verified.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>md5sum infra/aws/ec2/estate-report-runner/estate_report_runner.py</run>
      <expect>Local md5 RECORDED. It MUST differ from DEP1's a110981492b461e19fb9be7848b9ad09 -- an identical hash would mean you are re-uploading DEP1's artifact.</expect>
      <if_mismatch>Equal to DEP1's md5 -> you are on the wrong vintage. STOP.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>aws s3api head-object --bucket opal-estate-report --key code/estate_report_runner.py</run>
      <expect>ETag == Phase-2 md5, LastModified newer than Phase-1, ContentLength changed. A `-N` suffix = multipart = INVALID comparison, say so explicitly rather than calling it a mismatch.</expect>
      <if_mismatch>*** DID NOT LAND. DO NOT REPORT SUCCESS. *** rc=0 from put-object is NOT evidence -- record it, never rely on it.</if_mismatch>
    </step>
    <step>
      <run>aws s3 cp s3://opal-estate-report/code/estate_report_runner.py - | md5sum   (round-trip)</run>
      <expect>Served bytes hash to the Phase-2 md5. YOU ADDED THIS CONTROL ON DEP1 UNPROMPTED AND IT IS NOW MANDATED: ETag proves S3 stored what you sent; only a read-back proves a booting instance gets it.</expect>
      <if_mismatch>STOP and surface. Stored-correctly and readable-correctly are different claims.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<risk_adjudicated>
  <risk name="61378-vs-60000-prompt-size" verdict="CLEARED -- SHIP AS BUILT, do NOT retune">
    CTO~B flagged the new prompt at ~61,378 chars vs 60,000 as "2% over on the exact dimension
    KIMI_EMPTY sat on," and offered to retune CORPUS_PROMPT_BUDGET 25000 -> 20000.
    REFUTED BY TWO SEATS ON DIFFERENT DERIVATIONS (which is what makes the tie meaningful):
      AE (grounded): MISATTRIBUTION -- two different budgets. KIMI_EMPTY was OUTPUT (`max_tokens`
        4000->32000, literally the 95e1f0283f diff; PRD:38 says starvation occurred "on the ~60KB
        production prompt", i.e. that INPUT size was already fine). f023857ab keeps max_tokens 32000
        at :965. Adding ~350 input tokens consumes zero max_tokens. Also: 60,000 was NEVER a tested
        boundary -- at a254104b34:826 it is a hand-picked `[:60000]` slice on ONE half, the same class
        of magic number this patch removes.
      CVO (independent): risk LOW -- 8x margin on the output budget, input grew 2-3%; the mechanism
        that bit us is not meaningfully re-armed.
    DO NOT RETUNE: dropping to 20000 sacrifices 5,000 chars of the corpus -- the thing the patch
    exists to deliver -- to buy back 2% on an axis that is not the failure mode.
    HONEST RESIDUAL, both seats state it: this remains a JUDGEMENT, not a MEASUREMENT. The only
    instrument that settles it is a live Kimi call = VENDOR EGRESS = needs Andrew's explicit per-use
    word. Kimi is NOT on the standing lift list and the 08-04 1745Z word does NOT cover a fresh call
    today. Absent that authorisation, tomorrow's 13:00Z fire is the first exercise -- acceptable
    because the failure mode is now LOUD (KIMI_LENGTH_STARVED is a discriminated record, not a silent
    empty) and the day is recoverable. AE's K3 context-window read is an ESTIMATE, not a measurement.
  </risk>
</risk_adjudicated>

<acceptance_criteria>
  <criterion>Phase-3 ETag == Phase-2 md5, both quoted VERBATIM. A claim of equality without both printed values is NOT accepted.</criterion>
  <criterion>Phase-2 md5 DIFFERS from DEP1's a110981492b461e19fb9be7848b9ad09 (proves a new vintage actually shipped).</criterion>
  <criterion>Round-trip read-back hash matches. Stored != readable.</criterion>
  <criterion>Tip re-derived at GO time by YOU, not inherited.</criterion>
  <criterion>Upload before 2026-08-06 13:00Z. A missed window is REPORTED before it closes, never a silent slip.</criterion>
  <criterion>Session log Compiler Tools section reproduces every run with observed output and pass/fail. Missing rows = REWORK.</criterion>
  <criterion>NO alert/alarm/SNS/SES/checker/monitor built (standing moratorium).</criterion>
</acceptance_criteria>

<known_not_closed_by_this_to>
  CVO measured that only 69 of 153 nuggets reach the prompt. Ranked SOVEREIGN-first with 105 SOVEREIGN
  nuggets, that means ~36 of Andrew's own verbatim rulings still do not reach the model, and ZERO
  delegated/unclassified rows do. NOT a ship-blocker -- 69 is transformatively better than the 0 the
  model has had since day one, and the omission is DECLARED in-prompt ("69 of 153 shown, omitted for
  prompt budget, not filtered"), which is the contract. But "the corpus is wired in" and "the model
  sees the corpus" are different claims and only the first is true after this deploy. The budget split
  (25000 corpus / 35000 git appendix -- 42% vs 58%) is a live tuning question for CTO~B, surfaced to
  Andrew, and is NOT this TO's scope.
  Post-deploy CVO owes: SERVED-artifact verification vs f023857ab, then after the 13:00Z fire,
  verification that the EMITTED REPORT carries the corpus block + coverage line. Deployed code and
  emitted artifact are two different claims.
</known_not_closed_by_this_to>
</task_order>
