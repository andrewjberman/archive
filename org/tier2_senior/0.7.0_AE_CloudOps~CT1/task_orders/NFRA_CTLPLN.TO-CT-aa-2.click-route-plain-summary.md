<task_order id="NFRA_CTLPLN.TO-CT-aa-2.click-route-plain-summary">
<to_id>NFRA_CTLPLN.TO-CT-aa-2.click-route-plain-summary</to_id>
<project>NFRA_CTLPLN</project>
<issued_by>2.0.0_SA_COO~C</issued_by>
<issued_to>0.7.0_AE_CloudOps~CT1</issued_to>
<date>2026-10-12</date>
<status>complete</status>
<status_reason>Closed by the issuer 2.0.0_SA_COO~C after reading the record in-tree and on origin (commit 98e48fcbb2, integrated at 4899c05b9a): proof instance VALID (CTaa2-AC1 WORDS-OK, 220 words, no margin; CTaa2-AC2 judgment, recorded UNVERIFIABLE-BY-INSTRUMENT for 3.0.0_SA_CVO~L, ask sent 14:08Z). The text has three parts and states every limit of row D1-S11. The seat left two small facts out for the word bound (the receiving tool's install step was not used; the pack was read from Downloads under TO-CT-v-3 Amendment 3). This is the dell1 hop of the round-11 thread; HOP 5 GRADE reads ABSENT until the CVO's adjudication row lands.</status_reason>
<risk>LOCAL</risk>
<proof_genre>BUILD</proof_genre>
<round>11</round>
<workstream>THREAD</workstream>

<title>NFRA_CTLPLN round 11 CT-aa-2 (E1, the grade hop): on dell1, write a plain-language summary of what the dell1 click-route records prove and do not prove, for Andrew to hear read aloud; one judgment criterion the CVO grades</title>

<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.round11.md</decomp_doc>
<owned_cells>CT-aa-2</owned_cells>
<decomp_context>E1 of the L10 analyses (FWD-1 re-based, FWD-4): one real round is planned on the laptop, worked and committed by a Dell on its box branch, integrated into CLOUD by the integrator, and GRADED on the laptop, each hop read from git by `.tools/thread-trace.py`. Round 9's dell1 order carried no judgment criterion, so the trace read 4 of 5 hops (HOP 5 GRADE absent). This order carries one, so the fifth hop has a grade to read. The content is also the one part of E3 not yet done: Andrew has not heard the dell1 click-route record in plain words.</decomp_context>
</decomp_ref>

<context>
This order is a WRITE of one text file from three records you already wrote. It changes nothing on dell1 except that file, runs nothing, mints nothing. The three records are in your deliverables folder: `NFRA_CTLPLN.TO-CT-v-3.receive.txt`, `NFRA_CTLPLN.TO-CT-v-3.blocked-download.txt` and `NFRA_CTLPLN.TO-CT-y-2.fresh-process-record.txt` (read them whole). The limits you stated yourself (row D1-S11: the fresh environment the system builds lacks SystemRoot and USERPROFILE, so it is not a faithful logon session; pip download ran twice) are part of what the summary must say.
</context>

<the_act>
1. Read the three records whole.
2. Write ONE file, `org/tier2_senior/0.7.0_AE_CloudOps~CT1/deliverables/NFRA_CTLPLN.TO-CT-aa-2.click-route-plain-summary.md`, at most 220 words including headings, in plain English a non-engineer can follow when it is read aloud: three short headed parts in this order, `What was set up` (what you did on dell1 and what the variable PIP_NO_INDEX does), `What was shown` (each thing the records show happened, with the date), `What was not shown` (each limit the records state, in your own words and without softening). Use only facts in the three records; run nothing new; no command lines, hashes or paths inside the text; expand any acronym on first use.
3. COMMIT the file on `box/dell1` through `.tools/safe-commit.sh` as your serial. Do NOT push `CLOUD`; dell1's box-sync publishes `box/dell1` and the integrator takes it. Report to 2.0.0_SA_COO~C through 0.0.0_AB_MSTR~DELL1 with the commit hash.
</the_act>

<bounds>
- One new file; no change to any variable, config file, interpreter package or service on dell1. No run of pip, python or any network call. No push of CLOUD. No alert, monitor or timeout is built.
</bounds>

<proof_of_spec>
<criterion id="CTaa2-AC1" cell_refs="CT-aa-2"><invocation>python -c "import sys; t = open(sys.argv[1], encoding='utf-8').read(); print('WORDS-OK' if 0 < len(t.split()) <= 220 else 'WORDS-BAD')" org/tier2_senior/0.7.0_AE_CloudOps~CT1/deliverables/NFRA_CTLPLN.TO-CT-aa-2.click-route-plain-summary.md</invocation><expect>WORDS-OK</expect></criterion>
<criterion id="CTaa2-AC2" cell_refs="CT-aa-2" judgment="true"/>
</proof_of_spec>
<expected_criteria>CTaa2-AC1,CTaa2-AC2</expected_criteria>
`CTaa2-AC1` -- the file exists and holds 1 to 220 words. `CTaa2-AC2` (JUDGMENT, graded by `3.0.0_SA_CVO~L` and never self-graded; the instance records it UNVERIFIABLE-BY-INSTRUMENT with a `status_reason` naming the CVO): read aloud to a listener who is not an engineer, does the text say what the three records show and what they do not, with each stated limit present and none softened or invented? Write the proof instance to `org/tier2_senior/0.7.0_AE_CloudOps~CT1/deliverables/NFRA_CTLPLN.TO-CT-aa-2.click-route-plain-summary.proof_of_spec.json`, validate it with `python .tools/proof-of-spec-check.py <instance> CTaa2-AC1,CTaa2-AC2`, and leave the status flip to the issuer.

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~CT1/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~CT1/logs/
org/missions/D0/NFRA/NFRA_CTLPLN/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE no schedule; one file.
comp-iam: DECLARED-NOT-APPLICABLE no AWS call.
comp-adversary: RUN -- a summary that claims more than the records show (the judgment criterion grades exactly that); a softened or dropped limit; a number or date not in the records; BLIND: a listener who needs the command lines (this text is for hearing, the records stay the reference).
lane: the <paths> block names the seat's deliverables and logs and the surprise channel.
</preflight>

Source: ROUND_ANALYSIS.round10.md section 3 (E1; E3 read-aloud); TO-CT-y-2 and TO-CT-v-3 records.
</task_order>
