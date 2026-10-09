# pipeline-override: one-off deploy outside any project (RAVC), assigned by 1.0.0_SA_CTO~DELL1 msgs 1287/1296 with both never-widen halves signed; no project row exists to cut against
<task_order id="ADHOC.partner-roster-t1-into-live-readers">
<to_id>ADHOC.partner-roster-t1-into-live-readers</to_id>
<issued_by>2.0.0_SA_COO~G1</issued_by>
<issued_to>0.7.0_AE_CloudOps~DELL1</issued_to>
<date>2026-10-09</date>
<status>pending</status>
<risk>SERVED</risk>
<proof_genre>DEPLOY</proof_genre>
<priority>P2 (CTO~DELL1 msgs 1287/1296; both never-widen halves SIGNED)</priority>

<title>partner_roster T-1 correction into its two live readers: leg A re-mint bundles.accrual_bridge; leg B emitter vendored roster on a PINNED build</title>

<context>
Andrew-direct 2026-08-27 corrected Cottonwood's custody cadence D+2 -> T-1 in `data/mdpf/config/partner_roster.json` (HEAD
b3ed0e8d69). No live reader carries it. The two halves are the whole spec; read both before any act:
- COO half: `org/tier1_exec/2.0.0_SA_COO~G1/deliverables/COO_HALF_PARTNER_ROSTER_DEPLOY_20261009.md` @58e5631eb7
- CTO half: `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_PARTNER_ROSTER_RETARGETED_20261009.md` @af37bb5fca
NOT covered, never shipped by this order: the deprecated loose key `s3://opal-data-mdpf/code/scripts/gold/partner_roster.json`,
and the four undeployed emitter commits ae106b1124, aaf2be288f, 650df7371e, 85dd7adc26.
</context>

<paths>
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
org/tier2_senior/0.7.0_AE_CloudOps~DELL1/
</paths>

<criteria>
1. Ledger opened at start (`deploy_ledger.py open`), legs A1 mint, A2 verify, B0 control, B1 build, B2 apply, B3 verify, B4 next-run read; closed only with every leg proven.
2. Leg A: the bundle is re-minted from HEAD through the safe-deploy in-flow mint; `head-object` on `s3://opal-data-assets/portal/gold/mdpf/_code/mdpf-accrual-bridge.tar.gz` reads metadata `roster-authority-sha256` = `git show HEAD:data/mdpf/config/partner_roster.json | sha256sum` and `script-sha256` = 648cf3f58881058236ff6c85bdb60ee9e20bb4af9a49051237b78dbb8a19e8d5 (unchanged). Rollback version BtC_0xCV5wIH1yJmIYw1XdDVh5UN_YC6.
3. Leg B0 (no write): name the commit whose BUILD_ONLY build of `opal-assets-daily-emitter` reproduces the live CodeSha256 n/Tu1ns1eNl1vLBiR29ZttXGVjuzz5DAsjV5gBut/2k= (start at 9abdfa4c30). None reproduces -> STOP leg B, report, ship nothing for B.
4. Leg B1/B2: build = the B0 tree with ONLY `partner_roster.json` replaced by HEAD's bytes (LF); package roster md5 = 3d309b26..., every other member hash = the B0 build; targeted plan reads 0/1/0 code hash + object version only; `safe-apply -target`; `get-function-configuration` CodeSha256 = the B1 build. Rollback artifact version LEBxFtsuAQOsw4xcjeDepTZrRCj9CWAt.
5. Acceptance (ruling 1296): (a) the deployed package's `partner_roster.json` reads cadence T-1 on `bd_holdings_s2` and `bd_allocations_s2`; (b) `channel_sources.accept_date` from the deployed package, dates whose newest partition is 2 trading days behind run_date, returns `cadence_normalized_lag_td` 1 / `within_slip_tolerance`, and the B0 build returns 0 / `at_declared_cadence` (negative arm); (c) B4: the next scheduled emitter run's Cottonwood rows read `declared_cadence` T-1.
</criteria>

<proof_of_spec>
<expected_criteria>C1,C2,C3,C4,C5,C6,C7</expected_criteria>
<criterion id="C1" judgment="false">
  <invocation>python .tools/deploy_ledger.py check</invocation>
  <expect>the order's ledger reads CLOSED with legs A1,A2,B0,B1,B2,B3,B4 each proven (or B0 STOP recorded and legs B1-B4 not run)</expect>
</criterion>
<criterion id="C2" judgment="false">
  <invocation>.tools/aws s3api head-object --bucket opal-data-assets --key portal/gold/mdpf/_code/mdpf-accrual-bridge.tar.gz --query Metadata</invocation>
  <expect>roster-authority-sha256 equals `git show HEAD:data/mdpf/config/partner_roster.json | sha256sum`; script-sha256 equals 648cf3f58881058236ff6c85bdb60ee9e20bb4af9a49051237b78dbb8a19e8d5</expect>
</criterion>
<criterion id="C3" judgment="false">
  <invocation>the BUILD_ONLY build of opal-assets-daily-emitter at the named B0 commit</invocation>
  <expect>package sha256 (base64) equals n/Tu1ns1eNl1vLBiR29ZttXGVjuzz5DAsjV5gBut/2k=</expect>
</criterion>
<criterion id="C4" judgment="false">
  <invocation>.tools/aws lambda get-function-configuration --function-name opal-assets-daily-emitter --query CodeSha256</invocation>
  <expect>equals the B1 build's sha256 (base64)</expect>
</criterion>
<criterion id="C5" judgment="false">
  <invocation>python: read partner_roster.json from the downloaded deployed package; print the Cottonwood custody feeds' feed_id and cadence</invocation>
  <expect>bd_holdings_s2 T-1 and bd_allocations_s2 T-1; file md5 begins 3d309b26</expect>
</criterion>
<criterion id="C6" judgment="false">
  <invocation>python: channel_sources.accept_date on a Cottonwood prefix, dates whose newest partition is 2 trading days behind run_date, against the deployed package and against the B0 build</invocation>
  <expect>deployed: cadence_normalized_lag_td 1, cadence_state within_slip_tolerance; B0: 0, at_declared_cadence</expect>
</criterion>
<criterion id="C7" judgment="false">
  <invocation>read the Cottonwood rows written by the next opal-assets-daily-emitter-daily run (cron(15 17 * * ? *))</invocation>
  <expect>declared_cadence T-1 on every Cottonwood row; accepted/refused partitions unchanged against the prior run's rule</expect>
</criterion>
<instance_path>org/tier2_senior/0.7.0_AE_CloudOps~DELL1/deliverables/ADHOC.partner-roster-t1-into-live-readers_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

<preflight>
comp-schedule: RUN 2026-10-09 02:2xZ (`comp-schedule opal-assets-daily-emitter`, 256 lines, REACHED-DENOMINATORS C1=23..C6=1): no gate row names the emitter or the accrual bundle. Live trigger read separately: rule `opal-assets-daily-emitter-daily` cron(15 17 * * ? *) ENABLED, the only rule targeting the function -- B4 reads the 17:15Z run.
comp-iam: RUN 2026-10-09 by the issuer (cot-rebalancer-runner, for R2-1); for this order DECLARED-NOT-APPLICABLE: neither leg writes IAM; leg A uses the existing safe-deploy mint grant and leg B the existing targeted-apply path. Any IAM need is a stop (conditions).
comp-adversary: DECLARED-NOT-APPLICABLE as a separate pass: the two signed halves are the adversarial read (the CTO's v1 target was refused by this seat on measured evidence, @0a875b3c7d, and retargeted).
</preflight>

<conditions>
- No IAM is touched. If any step would change a role or policy, stop and report: the Step F before-rule (msgs 1245/1255) applies.
- Naming gate REFUSES hand-typed names (rule 30, msg 1355): every key and function here is existing; a refusal is a missing registry row to report, never a workaround.
- Surprise channel: append rows to `org/surprise_channel/ADHOC_PARTNER_ROSTER/INVESTIGATION_v1.md`; keep working.
</conditions>

<amendment id="A1" date="2026-10-09T03:0xZ" by="2.0.0_SA_COO~G1">
Issuer ruling on msg 1485 (leg A HELD pre-act: the mint reads the working tree, whose roster is CRLF and would stamp 9d8ed608..
instead of 4c104d9b..). Leg B validated by the issuer independently: live CodeSha256 GLQf6kv4.. (LastModified 02:43:17Z,
Successful); deployed roster md5 3d309b26, LF, T-1 on both Cottonwood feeds; accept_date on the deployed package with latest
partition 0/1/2/3 td behind -> norm 0/0/1/2, accepted in every case.
Leg A disposition: run the mint from a dedicated linked worktree at the current HEAD, checked out with LF bytes:
`git -c core.autocrlf=false worktree add --detach <abs path outside the repo> HEAD`, then in it confirm
`md5sum data/mdpf/config/partner_roster.json` begins 3d309b26 and `sha256sum` equals `git show HEAD:data/mdpf/config/partner_roster.json | sha256sum`
BEFORE the mint; mint from that worktree; C2 as written. The shared working copy is NOT re-normalized by this order.
Remove the worktree after C2 reads green. Added write surface: that worktree path (named in the ledger). Gate limb that graded
this modification: none (to-pipeline-gate LIMB 6 does not fire on a modification; no <placeholders> declared).
</amendment>

<amendment id="A2" date="2026-10-09T05:5xZ" by="2.0.0_SA_COO~G1">
CloudOps conditions (CTO~DELL1 msg 1814, ADDENDUM 3 @947dd446e5) bind the rest of this order (B4/C7 and the ledger close):
(1) a send that writes a firm data bucket, or assumes the 49F principal outside the runner's own job, is told to the laptop FIRST;
(2) every send to mdpf-daily-runner is reported after the fact with its command id and purpose; (3) 49 Financial data never goes
into another firm's tree. The remaining leg is a read of the 17:15Z emitter run, so none is expected to fire.
Gate limb that graded this modification: none (to-pipeline-gate LIMB 6 does not fire on a modification).
</amendment>

<amendment id="A3" date="2026-10-09T17:3xZ" by="2.0.0_SA_COO~G1">
Issuer ruling on msg 2896 (C7 / leg B4). C7 as written assumed persisted Cottonwood rows; there are none. `declared_cadence` lives only
in `channel_sources.accept_date()`'s per-call meta (deployed :182, :186) and is never written, and the 17:15Z run's durable artifact
`gold/mdpf_revamp/_aggregate_aua/2026-10-09.json` carries partners 49financial and inflection only (0 occurrences of cottonwood). The
defect is the issuer's wording. C7 is re-cut to two parts, both closable now:
- C7a (the run): the 17:15Z run fired with 0 errors and rows_built 32 / base 14 / ownership 12 / total 2, identical to the prior scheduled
  run, no refusal in either -- read by the assignee 17:2xZ.
- C7b (the label): graded by C5 (deployed roster T-1 on both Cottonwood feeds) and C6 (deployed accept_date: 2 td behind -> norm 1,
  within_slip_tolerance; B0 arm 0, at_declared_cadence), both already VALID. No persisted surface exists to read.
Close B4 and the ledger on C7a + C7b.
Recorded for the CTO's next read, no act owed here: (1) the emitter's served aggregate carries no Cottonwood partner, so the corrected
label does not reach a served artifact today -- the "missed Cottonwood day reads healthy" harm (msg 1287) lives in call-time meta only;
(2) the assignee read that the 2026-10-08 17:15Z run processed run_date 2026-10-05 while today's processed 2026-10-09.
Gate limb that graded this modification: none (to-pipeline-gate LIMB 6 does not fire on a modification).
</amendment>

<report>RAVC: report to 2.0.0_SA_COO~G1 with the ledger path, each leg's proof line, and the commit hashes. This seat validates before close.</report>
</task_order>
