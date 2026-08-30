# TO OPAL_ADVIPOINTERS.INF-ONEWRITER — inf-silver-chain: ONE PRODUCER PER SERVED KEY (all 7 SILVER_BUILDERS) + the billing consumer leg

<task_order id="OPAL_ADVIPOINTERS.INF-ONEWRITER" project="OPAL_ADVIPOINTERS">
<issued_to>RE-ROUTED 2026-08-30T03:4xZ by the issuer 2.0.0_SA_COO: the 03:1xZ re-address to 0.4.0_DS_ClientPlatform~N is SUPERSEDED before it activated -- that seat stays on ADVI_49F for cell C02-g-5 (the negative-BMV guard, surprise item 85147 / CTO ruling 85171), so its activation trigger (release from ADVI_49F) no longer arrives this sitting. NEW TARGET: the NEXT FREED DS LANE -- 0.4.0_DS_ClientPlatform~V at its NFRA_SUBSTRATECARDING.TO-CARD-R-DS card boundary (one card, ~1 h, borrowed by 2.0.0_SA_COO~X at 85109/85137) is the nearest; the issuer names the instance by message at that boundary and edits this field then. UNTIL THEN NO SEAT HOLDS THIS FACE. (Step 1 + consumer leg -> that lane; Step 2 -> 0.7.0_AE_CloudOps base queue position 4, unchanged.) PRIOR: <issued_to>SPLIT BY LANE 2026-08-30T03:1xZ (issuer 2.0.0_SA_COO, per the project owner's 84916): Step 1 (ATTRIBUTE the ~11:5xZ second writer of s3://opal-data-inf/silver/api_dims/billing/ -- a READ, Rule 22 before any edit) + the consumer leg -> 0.4.0_DS_ClientPlatform~N [ACTIVATES at the CVO acceptance of ~N's two ADVI_49F c02 faces; barred until then -- see issuer_record]; Step 2 (remove billing from SILVER_BUILDERS at infra/aws/lambda/inf-pipeline/inf-silver-chain/lambda_function.py:83 + Terraform redeploy of inf-silver-chain, consumers-first) -> 0.7.0_AE_CloudOps base, queue position 4, BEHIND the M-2 deploy plan, TO-S1-AE and the stitch-nightly item; not before Step 1's attribution is read. (was: 0.4.0_DS_ClientPlatform (base; INF plane, steps 1-2 + consumer leg) + 0.7.0_AE_CloudOps (inf-silver-chain TF redeploy; joint))</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issuer_record date="2026-08-30T03:1xZ" by="2.0.0_SA_COO">LIVENESS CALL by the project owner 1.0.0_SA_CTO (84916, measured live 03:05-03:09Z): INF-ONEWRITER is LIVE: list-object-versions on the billing dim shows TWO versions per date on 3 of 3 recent dates (08-27 11:18:26Z 34,051 B + 11:55:39Z 45,489 B latest; 08-28 11:18:09Z + 11:51:58Z; 08-29 11:19:22Z + 11:56:59Z) and billing is STILL in SILVER_BUILDERS :83 (repo); the P1-shaped leg (which writer the SERVED headline reads) NOT re-measured by the CTO. RE-ADDRESSED by the issuer under Rule 27: every live DS lane holds ONE other project (~C ADVI_BDPARITY, ~N ADVI_49F x2 pending grade, ~R ADVI_INSURE TO-R1-DS, ~V NFRA_SUBSTRATECARDING.TO-CARD-R-DS, ~E D3_MODELOVERLAY), the marker cap reads 19 of 20 and the project owner ruled a NEW seat not warranted for a listing-per-turn read -- so the face goes to 0.4.0_DS_ClientPlatform~N as that seat's NEXT project, ACTIVATING at 3.0.0_SA_CVO's acceptance of ADVI_49F.c02-VINTAGE + ADVI_49F.c02-GROSSLEG (expected 2026-08-30 within the hour). UNTIL THAT ACCEPTANCE THIS FACE IS NOT HELD BY ~N AND ~N IS BARRED FROM ACTING ON IT (the /mstr-spawn 1d class: a serial-keyed row must not read as owned before it is). CTO ruling 145259Z (structural remedy (b), widen to all 7 builders) stands as this face records it.</issuer_record>
<issued>2026-08-18T14:58Z</issued>
<dated>THIS WEEK, sequenced at the DS seat BEHIND ADVI_BDPLAT_RESTORE.TO-1 (today) and MDPF_PROVENANCE.T-B (08-19); target 08-20/21. Not tonight. Owner named; a dated TO awaiting its turn, not a staged one.</dated>
<status>staged -- DATED this week (08-20/21), owners named</status>
<priority>P2 with a P1-shaped leg: the two-writer window is small and self-correcting (34 min/day) BUT if step 1 confirms the mechanism, the SERVED billing headline is wrong ALL DAY (fee_earning_aua=0 beside 114.5 bps) -- the 08-12 open served defect. Does NOT displace bd platinum or the provenance TOs.</priority>
<authority>CTO RULING 145259Z (structural remedy (b) + widen to all 7 builders + the 08-12 defect link, INFERRED pending step 1); MSTR 145245Z (the THIRD instance of Rule 22a's two-homes class this week -- route as a class, bank the class); DS finding 145045Z (banked inside ADVI_BDPLAT_RESTORE, correctly not chased); COO verification 1450Z. Governing invariant: OPAL_ADVIPOINTERS -- ONE PRODUCER AND ONE BASIS PER QUANTITY. Andrew's is_fee_earning retirement is the ratified spec (CRO); this TO enforces it structurally.</authority>
</task_order>

## The finding (verified three ways: DS, COO, MSTR)

`s3://opal-data-inf/silver/api_dims/billing/snapshot_date={D}/data.parquet` receives TWO writes daily
(list-object-versions, 08-17 + 08-18 identical shape): **~11:18Z, 34,0xx B, by `inf-silver-chain`'s
BUNDLED `build_billing_dim` (PRE-retirement signature, `is_fee_earning` x9; `lambda_function.py:70` import,
`:83` SILVER_BUILDERS entry, executed from /var/task; `:170`'s own comment admits it writes the same artifact;
SYNC.md last sync 05-11, function LastModified 08-05)** then **~11:50Z, 45,5xx B, by a SECOND writer with
the RETIRED signature (identity NOT yet read)**. Last-writer-wins. Rule 22a's "one logical producer, two
independently-editable homes" -- THE defect that reads clean while the copies diverge. Third live instance
this week (mdpf json/mdpf-vs-platinum; bd legacy-rps-vs-08335338; this).

## Step 1 — ATTRIBUTE the 11:52Z writer (Rule 22, before ANY edit)
One CloudWatch/log read: identify the second writer (hypothesis: the canonical DS
`data/inf/scripts/silver/build_billing_dim.py --upload` from the inf runner / redispatch). Print BOTH
writers' log lines beside the two object versions (timestamps + sizes). The write must be ATTRIBUTED,
not assumed. If the hypothesis is FALSE, STOP and report -- the remedy below assumes the canonical
scheduled run is the retired-signature writer.

## Step 2 — REMEDY (b), STRUCTURAL (CTO ruled): the canonical scheduled DS run is the ONE producer
- REMOVE `billing` from `inf-silver-chain`'s `SILVER_BUILDERS` (`lambda_function.py:83`). Consumers-first:
  the SILVER_BUILDERS entry is the consumer edge -- remove it, AE TF-redeploys `inf-silver-chain` (Rule 1/2:
  commit -> TF -> source-map -> plan -> apply -> 0-diff -> tag), THEN the bundled `build_billing_dim.py` is
  dead code -- delete it in the same commit or the next. **NOT (a) resync**: resync is the discipline-
  dependent form of the same fix and re-manufactures the two-homes class the day the next edit lands in
  one copy. Do NOT delete the bundled file first.
- Verify APPLIED: next day's `snapshot_date` shows ONE object version (list-object-versions), retired
  signature, written by the canonical run; the Lambda's CW stream shows no `[billing]` line.

## Step 3 — WIDEN: one-writer sweep of ALL SEVEN SILVER_BUILDERS (denominator 7, printed)
For each builder in `inf-silver-chain`'s SILVER_BUILDERS: which served silver key it writes; is it the
ONE producer of that key or a SECOND HOME (canonical DS file vs bundled copy: sha, signature diff,
list-object-versions on today's partition -- one version or two?); disposition ∈ {SOLE-WRITER-KEEP,
SECOND-HOME-REMOVE, DEAD, BROKEN-SOLE-PRODUCER}. **The 3 of 7 that fail every day** (household + activity
`NoSuchKey` on bronze `geo_verify` / `unified_account_dim`; `accounts_v2` missing local `rep_map`) get
classified in the same table -- a builder that fails daily is DEAD (remove) or a BROKEN sole producer
(fix), never left as noise. Table = the P5-shaped one-writer census on one Lambda, done once. CTO reads it.

## Step 4 — the CONSUMER LEG (DS INF plane), GATED on step 1 confirming the mechanism
CTO's INFERRED link: `DEFECT_INF_ADVISOR_FEE_SPLIT_IS_FEE_EARNING_DROPPED_20260812` (@97e2cadc14) recorded
"the deployed builder derives is_fee_earning, yet the partition it should have written lacks it" with four
unverified candidates. Two writers 34 min apart with OPPOSITE signatures resolves that contradiction
exactly: the served consumer (`inf advisor lambda_function.py:737`, silent `.get(is_fee_earning, 0.0)`)
reads the SECOND write -> `fee_earning_aua = 0` beside 114.5 bps -- **the served headline is wrong for
the ENTIRE DAY after the second write, not for 34 minutes.** IF step 1 confirms: the defect's root cause
is CLOSED-BY-MECHANISM, and the consumer fix is a CONTRACT act under the retirement's ratified spec (CRO):
the consumer reads the RETIRED signature (`ending_mv_*` / the ratified fee-earning source) and its `.get`
default becomes a REFUSAL (the b01-swallow-FATAL pattern @0205eef992), never a silent 0.0. Served verify:
the advisor headline's fee_earning_aua is non-zero and ties to the ratified source. IF step 1 refutes:
report; the consumer leg re-scopes.

## Acceptance
- OW-1: step 1 -- both writers ATTRIBUTED with log lines + object versions side by side.
- OW-2: `billing` removed from SILVER_BUILDERS; inf-silver-chain TF-redeployed 0-diff + tagged; bundled
  file removed; next-day partition = ONE version, retired signature, canonical writer; CW stream clean.
- OW-3: the 7-row builder table (key / sole-or-second-home / disposition / evidence), denominator 7 printed;
  the 3 daily-failers classified DEAD or BROKEN-SOLE with the fix-or-remove named.
- OW-4: consumer leg -- `.get(is_fee_earning, 0.0)` replaced by the retired-signature read + refusal
  default; served advisor headline fee_earning_aua non-zero + ties (or step-1-refuted, stated).
- OW-5: 08-12 defect record updated: CLOSED-BY-MECHANISM (or NOT, with the refutation) citing OW-1.
- OW-6: MSTR's class note carried: this is instance 3 of the two-homes class; the "how many more / cheap
  detector" question is PROPOSED to Andrew via CTO's residual bank -- not built here.

<proof_of_spec>
  <expected_criteria>OW-1,OW-2,OW-3,OW-4,OW-5,OW-6</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/OPAL_ADVIPOINTERS.INF-ONEWRITER_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>
DS fills OW-1/3/4/5/6; AE fills OW-2. ONE instance (joint, primary DS). Positional-id validation, check the rc.

## Discipline
Terraform is the only Lambda deploy (Rule 1); `safe-apply`; source-map row updated (Rule 4); no alarm/monitor
(moratorium -- the finding + the structural fix ARE the remedy); no shadow, no resync-as-fix. `comp-iam
service inf-silver-chain` after the builder-list change (necessary, not sufficient). CTO arch-gates the
SILVER_BUILDERS change + reads the 7-row table.

## reporting
COO (cc CTO, CRO for the retirement spec, MSTR) at step 1 (BEFORE any edit), at the redeploy, at the table,
at the consumer leg. IMMEDIATELY if step 1 refutes the hypothesis.
