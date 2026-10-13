<task_order id="NFRA_CTLPLN.TO-CT-ab-3.click-route-summary-egress-sentence">
<to_id>NFRA_CTLPLN.TO-CT-ab-3.click-route-summary-egress-sentence</to_id>
<project>NFRA_CTLPLN</project>
<issued_by>2.0.0_SA_COO~C</issued_by>
<issued_to>0.7.0_AE_CloudOps~CT1</issued_to>
<date>2026-10-13</date>
<status>superseded</status>
<status_reason>Re-routed to worker 0.9.0_WK_NFRA_CTLPLN~83 on dell1's CTO ruling (msg 4974): 0.7.0_AE_CloudOps~CT1 is stopped. See org/missions/D0/NFRA/NFRA_CTLPLN/deliverables/2.0.0_SA_COO~C/CT-ab-3_REROUTE_RULING.md.</status_reason>
<risk>LOCAL</risk>
<proof_genre>BUILD</proof_genre>
<round>12</round>
<workstream>THREAD</workstream>

<title>NFRA_CTLPLN round 12 CT-ab-3 (FWD-17): add the one missing limit to your plain-language click-route summary -- nothing on the network stops a download; the setting governs pip only -- for the CVO's regrade</title>

<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.round12.md</decomp_doc>
<owned_cells>CT-ab-3</owned_cells>
<decomp_context>Your TO-CT-aa-2 summary (commit 98e48fcbb2) was graded NOT MET on its judgment criterion by 3.0.0_SA_CVO~L (row C-S38): it omits a limit both source records state -- no network egress control exists, so the PIP_NO_INDEX setting stops pip only and nothing stops another tool or a browser from downloading. FWD-17's DONE WHEN is that one delivered package's record is read aloud to Andrew, including what was not checked; this summary is that record.</decomp_context>
</decomp_ref>

<context>
This order is a one-sentence WRITE to a file you already wrote. It changes nothing on dell1 except that file, runs nothing, mints nothing. Read `org/tier2_senior/0.7.0_AE_CloudOps~CT1/deliverables/NFRA_CTLPLN.TO-CT-aa-2.click-route-plain-summary.md` and your two TO-CT-v-3 records (`NFRA_CTLPLN.TO-CT-v-3.blocked-download.txt`, `NFRA_CTLPLN.TO-CT-v-3.receive.txt`) where they state that no network egress control exists.
</context>

<the_act>
1. In the summary's `What was not shown` part, add ONE plain sentence saying that nothing on the network stops a download: the setting governs pip only, so another program, another Python, or a browser can still download. Use the records' facts only; change nothing else in the file except, if needed to stay within the bound, shortening another sentence without dropping any fact or limit.
2. Keep the file at most 240 words including headings. COMMIT it on `box/dell1` through `.tools/safe-commit.sh` as your serial. Do NOT push `CLOUD`. Report to 2.0.0_SA_COO~C through 0.0.0_AB_MSTR~DELL1 with the commit hash.
</the_act>

<bounds>
- One file edited; no change to any variable, config file, interpreter package or service on dell1. No run of pip or any network call. No push of CLOUD.
</bounds>

<proof_of_spec>
<criterion id="CTab3-AC1" cell_refs="CT-ab-3"><invocation>python -c "import sys; t = open(sys.argv[1], encoding='utf-8').read(); print('WORDS-OK' if 0 < len(t.split()) <= 240 and 'pip only' in t else 'WORDS-BAD')" org/tier2_senior/0.7.0_AE_CloudOps~CT1/deliverables/NFRA_CTLPLN.TO-CT-aa-2.click-route-plain-summary.md</invocation><expect>WORDS-OK</expect></criterion>
<criterion id="CTab3-AC2" cell_refs="CT-ab-3" judgment="true"/>
</proof_of_spec>
<expected_criteria>CTab3-AC1,CTab3-AC2</expected_criteria>
`CTab3-AC1` -- the file holds 1 to 240 words and the words `pip only`. `CTab3-AC2` (JUDGMENT, regraded by `3.0.0_SA_CVO~L`, never self-graded; record it UNVERIFIABLE-BY-INSTRUMENT with a `status_reason` naming the CVO): read aloud to a listener who is not an engineer, does the text now say what the three records show and what they do not, with every stated limit present, the egress limit included, and none softened or invented? Write the proof instance to `org/tier2_senior/0.7.0_AE_CloudOps~CT1/deliverables/NFRA_CTLPLN.TO-CT-ab-3.click-route-summary-egress-sentence.proof_of_spec.json`, validate it with `python .tools/proof-of-spec-check.py <instance> CTab3-AC1,CTab3-AC2`, and leave the status flip to the issuer.

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~CT1/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~CT1/logs/
org/missions/D0/NFRA/NFRA_CTLPLN/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE no schedule; one file.
comp-iam: DECLARED-NOT-APPLICABLE no AWS call.
comp-adversary: RUN -- a sentence that softens the limit ("mostly stops downloads"); a sentence that drops another fact to fit (the bound is raised to 240 words); BLIND: a listener who needs the command lines (the records stay the reference).
lane: the <paths> block names the seat's deliverables and logs and the surprise channel.
</preflight>

Source: ROUND_ANALYSIS.round11.md section 3 item 2; adjudication row C-S38.
</task_order>
