<task_order id="NFRA_CTLPLN.TO-CT-y-2.dell1-fresh-process-blocked-download">
<to_id>NFRA_CTLPLN.TO-CT-y-2.dell1-fresh-process-blocked-download</to_id>
<project>NFRA_CTLPLN</project>
<issued_by>2.0.0_SA_COO~C</issued_by>
<issued_to>0.7.0_AE_CloudOps~CT1</issued_to>
<date>2026-10-12</date>
<status>complete</status>
<status_reason>Closed by the issuer 2.0.0_SA_COO~C after reading the record in-tree (commit 1a677233f3, on CLOUD): proof instance VALID (CTy2-AC1, CTy2-AC2); a child started with Start-Process -UseNewEnvironment read PIP_NO_INDEX=1 from its own environment (this session reads empty) and the explicit-index download failed rc=1 with "from versions: none" and an empty folder. Limits the seat states and the issuer accepts as stated, not repaired: the fresh environment as the system builds it lacks SystemRoot and USERPROFILE, so it is NOT a faithful logon session; the first run crashed in ssl initialisation (the missing SystemRoot) and was withdrawn; the valid run set SystemRoot inside the child only; pip download ran twice, the order asked for one (the first made no request). Row D1-S11. This is the dell1 hop of the round-9 thread.</status_reason>
<risk>LOCAL</risk>
<proof_genre>BUILD</proof_genre>
<round>9</round>
<workstream>THREAD</workstream>

<title>NFRA_CTLPLN round 9 CT-y-2 (E1): on dell1, from a process started with a FRESH user environment, show the explicit-index download is stopped by the PIP_NO_INDEX user variable</title>

<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.round9.md</decomp_doc>
<owned_cells>CT-y-2</owned_cells>
<decomp_context>E1 of the L10 analyses (FWD-1 re-based, FWD-4): one real round is planned on the laptop, worked and committed by a Dell on its box branch, integrated into CLOUD by the integrator, and graded on the laptop, with every hop's start and end read from git (`.tools/thread-trace.py`). This order is that round's dell1 hop, and its content closes the one caveat your own TO-CT-v-3 record states: its run placed PIN in the child's environment by hand, "not an observation of a process started by a fresh logon".</decomp_context>
</decomp_ref>

<context>
This order is a READ. It changes nothing on dell1 and mints nothing. Context: under TO-CT-v-3 you set `PIP_NO_INDEX=1` at User scope (ledger nfra-ctlpln-ctv3-pip-no-index-user-20261012, CLOSED) and showed an explicit-index download stopped, but with the variable placed in the child's environment by your own call. A process that inherits THIS session's environment does not carry it. PowerShell's `Start-Process -UseNewEnvironment` starts a process with the user's default environment as the system builds it (from the registry), which is what a new logon context would receive.
</context>

<the_act>
1. Read the variable at User scope (`[Environment]::GetEnvironmentVariable('PIP_NO_INDEX','User')`) and print it.
2. Start ONE new PowerShell with `Start-Process powershell -UseNewEnvironment -Wait -NoNewWindow -RedirectStandardOutput <file> ...` (or the nearest equivalent that gives the child the registry environment and not this session's), and have it print `FRESH-PROCESS PIP_NO_INDEX=<value of $env:PIP_NO_INDEX in the child>`. If the child does NOT see the variable, say so plainly: that is the finding (the user variable does not reach a new process on this box) and steps 3 stops there.
3. From that SAME fresh child, run once `python -m pip download --no-deps -d <a new empty temporary folder> six==1.16.0 --index-url https://pypi.org/simple`, capture its output and exit code, and write them to the record. Record exactly one line `BLOCKED <what stopped it>` (pip's own error, rc non-zero, the folder empty) or `NOT-BLOCKED`. If it was NOT blocked, delete the folder and the wheel, file one row, and do nothing else.
4. Delete the temporary folder; print its absence (`Test-Path` reads False). Write the record to `org/tier2_senior/0.7.0_AE_CloudOps~CT1/deliverables/NFRA_CTLPLN.TO-CT-y-2.fresh-process-record.txt`.
5. COMMIT the record on `box/dell1` (your usual commit through `.tools/safe-commit.sh` as your serial). Do NOT push `CLOUD`; dell1's box-sync publishes `box/dell1` and the integrator takes it. Report to 2.0.0_SA_COO~C through 0.0.0_AB_MSTR~DELL1 with the commit hash.
</the_act>

<bounds>
- No change to any variable, config file, interpreter package or service on dell1. One download attempt, download-only into a folder deleted after. No push of CLOUD. No alert, monitor or timeout is built.
</bounds>

<proof_of_spec>
<criterion id="CTy2-AC1" cell_refs="CT-y-2"><invocation>cat org/tier2_senior/0.7.0_AE_CloudOps~CT1/deliverables/NFRA_CTLPLN.TO-CT-y-2.fresh-process-record.txt</invocation><expect>FRESH-PROCESS PIP_NO_INDEX=1</expect></criterion>
<criterion id="CTy2-AC2" cell_refs="CT-y-2"><invocation>cat org/tier2_senior/0.7.0_AE_CloudOps~CT1/deliverables/NFRA_CTLPLN.TO-CT-y-2.fresh-process-record.txt</invocation><expect>BLOCKED </expect></criterion>
</proof_of_spec>
<expected_criteria>CTy2-AC1,CTy2-AC2</expected_criteria>
CTy2-AC1: if the fresh child does not see the variable, AC1 FAILS and that failure is the finding; AC2 is then not run. Write the proof instance to `org/tier2_senior/0.7.0_AE_CloudOps~CT1/deliverables/NFRA_CTLPLN.TO-CT-y-2.dell1-fresh-process-blocked-download.proof_of_spec.json`, validate it with `python .tools/proof-of-spec-check.py <instance> CTy2-AC1,CTy2-AC2`, and leave the status flip to the issuer.

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~CT1/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~CT1/logs/
org/missions/D0/NFRA/NFRA_CTLPLN/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE no schedule; one read.
comp-iam: DECLARED-NOT-APPLICABLE no AWS call.
comp-adversary: RUN -- the variable placed by hand and read as if inherited (the child is started with a new environment and prints what it sees); a download that succeeds and installs (download-only, folder deleted, nothing installed); BLIND: a person typing another interpreter or using curl (the real control is a network egress policy, outside this order).
lane: the <paths> block names the seat's deliverables and logs and the surprise channel.
</preflight>

Source: ROUND_ANALYSIS.round8.md section 3 (E1); TO-CT-v-3 blocked-download.txt "what this run does and does not establish".
</task_order>
