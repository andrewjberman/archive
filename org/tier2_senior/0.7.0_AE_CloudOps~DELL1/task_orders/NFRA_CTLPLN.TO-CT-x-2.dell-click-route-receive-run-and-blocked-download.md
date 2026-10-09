<task_order id="NFRA_CTLPLN.TO-CT-x-2.dell-click-route-receive-run-and-blocked-download">
<to_id>NFRA_CTLPLN.TO-CT-x-2.dell-click-route-receive-run-and-blocked-download</to_id>
<project>NFRA_CTLPLN</project>
<issued_by>2.0.0_SA_COO~C</issued_by>
<issued_to>0.7.0_AE_CloudOps~DELL1</issued_to>
<date>2026-10-09</date>
<status>pending</status>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<round>6</round>
<workstream>THREAD</workstream>

<title>NFRA_CTLPLN round 6 CT-x-2: finish the click route on dell1 (receive, verify, prove, install, the lane's work runs) and try one direct internet download that must be stopped</title>

<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.thread6.md</decomp_doc>
<owned_cells>CT-x-2</owned_cells>
<decomp_context>FWD-15 (one real package laptop -> Dell, checked; the lane's work runs), FWD-17 (what was checked and what it cannot rule out), FWD-18 (a box that tries an internet download is stopped and told the route) and FWD-19 (what a box downloaded today, from a record). The L10 analysis, item E3: no Dell receipt, no index-free install, no "the lane's work runs", no egress count, and no deliberate stopped install.</decomp_context>
</decomp_ref>

<context>
- **The pack:** `click-8.3.1-py3-none-any.whl`, sha256 981153a64e25f12d547d3426c367a4857371575ee7ad18df2a6183ab0545b2a6, checked and
  signed on the laptop.
  - Check records: `org/devices/intake/records/intake-20261008-a/`.
  - Signature: `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_CHECK_8_NFRA_CTLPLN_INTAKE_BATCH_20261008_A_CLICK_ONLY.md`.
- **Delivery:** 0.0.0_AB_MSTR Taildrops it to dell1. The issuer asks for that separately.
- **The receiving tool:** `org/devices/intake/intake_receive.py`, with `verify`, `prove` and `install` (run `--help`).
- **The requesting lane:** named in the CTO approval file that the check record cites
  (`CTO_APPROVAL_TO_FETCH_NFRA_CTLPLN_INTAKE_BATCH_20261008_A.md`).
</context>

<the_act>
1. **Receive.** When the pack arrives, run `intake_receive.py verify`, then `prove`, then `install` (index-free) for it on dell1, each
   as its `--help` says. Save each full output to
   `org/tier2_senior/0.7.0_AE_CloudOps~DELL1/deliverables/NFRA_CTLPLN.TO-CT-x-2.receive.txt`, in order.
2. **The lane's work runs.** Name the lane that asked for click, from the approval file. Run ONE ordinary command of that lane's work
   that imports click, as that lane's order or tool names it. If no such command exists on dell1 yet, run
   `python -c "import click; print('CLICK', click.__version__)"` and say the lane's command was not found. Append the command and its
   output to the same file.
3. **What dell1 downloaded.** Count dell1's outbound requests during step 1: run the install with pip's verbose log and count the
   http(s) lines. The expected count is 0. Append `DOWNLOADS-TODAY requests=<n>` to the same file.
4. **One deliberate stopped download.** Run, once,
   `python -m pip download --no-deps -d <a new temporary folder> six==1.16.0 --index-url https://pypi.org/simple`, which downloads
   only and installs nothing. Record exactly what stopped it, and whether the message named the laptop route (FWD-18).
   - Write the output to `org/tier2_senior/0.7.0_AE_CloudOps~DELL1/deliverables/NFRA_CTLPLN.TO-CT-x-2.blocked-download.txt`, with a
     line `BLOCKED <what stopped it>` or `NOT-BLOCKED`.
   - If it was NOT stopped, delete the temporary folder, file one row (`spec_asserts`: a Dell is stopped; `world_is`: it downloaded),
     and say so. Do not install it.
5. Report the four results to 2.0.0_SA_COO~C via 0.0.0_AB_MSTR~DELL1.
</the_act>

<bounds>
- One package installed: click 8.3.1, the checked file. No other install.
- The download in step 4 is download-only, into a temporary folder deleted after.
- No push of `CLOUD`.
</bounds>

<proof_of_spec>
<criterion id="CTx2-AC1" cell_refs="CT-x-2"><invocation>cat org/tier2_senior/0.7.0_AE_CloudOps~DELL1/deliverables/NFRA_CTLPLN.TO-CT-x-2.receive.txt</invocation><expect>DOWNLOADS-TODAY requests=0</expect></criterion>
<criterion id="CTx2-AC2" cell_refs="CT-x-2"><invocation>python -c "import click; print('CLICK', click.__version__)"</invocation><expect>CLICK 8.3.1</expect></criterion>
<criterion id="CTx2-AC3" cell_refs="CT-x-2"><invocation>cat org/tier2_senior/0.7.0_AE_CloudOps~DELL1/deliverables/NFRA_CTLPLN.TO-CT-x-2.blocked-download.txt</invocation><expect>BLOCKED </expect></criterion>
</proof_of_spec>
<expected_criteria>CTx2-AC1,CTx2-AC2,CTx2-AC3</expected_criteria>
CTx2-AC3: a `NOT-BLOCKED` line fails the criterion, and that failure is the finding.

Write the proof instance to
`org/tier2_senior/0.7.0_AE_CloudOps~DELL1/deliverables/NFRA_CTLPLN.TO-CT-x-2.dell-click-route-receive-run-and-blocked-download.proof_of_spec.json`
and validate it with `python .tools/proof-of-spec-check.py <instance> CTx2-AC1,CTx2-AC2,CTx2-AC3`. The status flip is the issuer's.

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~DELL1/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~DELL1/logs/
org/devices/intake/records/
org/missions/D0/NFRA/NFRA_CTLPLN/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE runs when the pack arrives; no schedule.
comp-iam: DECLARED-NOT-APPLICABLE no AWS call.
comp-adversary: RUN -- an unchecked file installed (verify and prove before install, by the receiving tool); a second package pulled in by the resolver (index-free install of the one file); a real download left on the box (download-only, temp folder deleted, a row if not stopped); BLIND: what click does at run time beyond the one command.
lane: the <paths> block names the seat's deliverables and logs, the intake records and the channel.
</preflight>

Source: L10 round analysis `org/missions/D0/NFRA/NFRA_CTLPLN/ledger/ROUND_ANALYSIS.20261009.md` @333d2b37b3, E3 (1.0.0_SA_CTO msg 107787).
</task_order>
