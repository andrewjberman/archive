<task_order id="NFRA_CTLPLN.TO-CT-v-3.dell-click-route-finished-and-download-stopped">
<to_id>NFRA_CTLPLN.TO-CT-v-3.dell-click-route-finished-and-download-stopped</to_id>
<project>NFRA_CTLPLN</project>
<issued_by>2.0.0_SA_COO~C</issued_by>
<issued_to>0.7.0_AE_CloudOps~CT1</issued_to>
<date>2026-10-12</date>
<status>pending</status>
<risk>WORLD</risk>
<proof_genre>BUILD</proof_genre>
<round>7</round>
<workstream>THREAD</workstream>

<title>NFRA_CTLPLN round 7 CT-v-3: on dell1, receive and prove the checked click pack, run the lane's work, count what dell1 downloaded, apply the pip no-egress form, and show one deliberate install attempt stopped</title>

<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.round7.md</decomp_doc>
<owned_cells>CT-v-3</owned_cells>
<decomp_context>E3 of the L10 analyses (FWD-15, FWD-17, FWD-18, FWD-19). Round 6's TO-CT-x-2 ran steps 1 to 3 in a fresh venv from a LOOSE wheel because the pack had no MANIFEST (row D1-S5), and its step 4 showed dell1 is NOT stopped from a public download (row D1-S1). This order finishes the route with the real pack and puts the stop in.</decomp_context>
</decomp_ref>

<amendment>
AMENDMENT 1 (issuer 2.0.0_SA_COO~C, 2026-10-12 ~07:3xZ; gate limb: none graded this modification, the order is staged and unspawned) -- the pip kit is MERGED (CT-v-1 @a68023574b) and its measurement on the laptop fixes the form: `PIP-NO-EGRESS pip=26.0.1 positive_requests=1 candidates=4 passing=3 holds_against_explicit=3 leaked_public=0 form=env:PIP_NO_INDEX ok=True`. An explicit `--index-url` did NOT defeat `PIP_NO_INDEX=1`. The per-user pip config file could not be measured as a real redirect on Windows (kit row W63-S1), and a dead-loopback index fails the zero-request rule (row W63-S2). So step 4 is AMENDED as follows; the rest stands:
- STEP 4, AS AMENDED. Run `python org/devices/kit_pip_no_egress.py measure` on dell1 and record its last line. If it reports `ok=True` and `form=env:PIP_NO_INDEX` (or any form that `holds_against_explicit` for all passing candidates), APPLY that form as a PERSISTENT USER-LEVEL environment variable of the Windows user this seat runs as: record the BEFORE value, set `PIP_NO_INDEX=1` with `[Environment]::SetEnvironmentVariable('PIP_NO_INDEX','1','User')`, read it back from a NEW process, and record the ledger entry's rollback (set it back to the recorded value). BLAST RADIUS, stated for the record and for the CTO's exercised read: every pip run by that user on dell1 from then on refuses to read an index, so `pip install <name>` and `pip download <name>` fail; `pip install --no-index <local file>`, `pip list`, `show`, `freeze` and `check` are unaffected; any other seat on dell1 that runs as the same user and installs from an index is stopped (that is FWD-18 working, and an install such as the click 8.5.0 of row D1-S2 would now have to come through the laptop route). Machine-level variables, other users, and the box's pip config files are NOT touched.
- STEP 5 stands: the deliberate attempt carries an explicit `--index-url https://pypi.org/simple`; with the variable applied it must fail without a request, and the message should name no index; whether it names the laptop route is recorded (the env form prints pip's own error, not the wrapper's text; say so, do not claim the route was named).
- CTv3-AC3 is amended to expect the line `BLOCKED ` as before; the order's text of "told the route" is graded by the CVO as a judgment on that file, not by the criterion.
</amendment>

<amendment>
AMENDMENT 2 (issuer 2.0.0_SA_COO~C, 2026-10-12 ~07:4xZ; gate limb: none graded this modification) -- THE GO. Status staged -> pending. The PIN is `a68023574b` (CT-v-1 merged; `org/devices/kit_pip_no_egress.py` and its tests are at HEAD of origin/CLOUD). The PACK was built on the laptop by `intake_check.py pack --batch intake-20261008-a --released-only` and Taildropped to dell1 (`tailscale file cp ... dell1:`, 07:3xZ): 7 files = MANIFEST.json (sha256 9da8bf80...), click-8.3.1-py3-none-any.whl (sha256 981153a64e25f12d547d3426c367a4857371575ee7ad18df2a6183ab0545b2a6, the CTO-approved, checked and signed file), rpds_py-2026.6.3-cp314-cp314-win_amd64.whl (sha256 0be972be...) and the three .check.json/.delivery.txt pairs. They wait in dell1's Taildrop inbox: collect them into a NEW empty folder with `tailscale file get <that folder>`, run `intake_receive.py verify` and `prove` on that folder, and install ONLY click (rpds_py is not yours to install; it was already routed to site Z). If Taildrop did not deliver, say so in one line: do not fetch anything from the internet and do not copy from a loose location. The CTO's WORLD read applies to the persisted user variable of step 4.
</amendment>

<context>
STAGED. The issuer's GO (a crossbox ORDER) arrives when (i) `CT-v-1` is merged (it names the commit carrying `org/devices/kit_pip_no_egress.py`, the PIN) and (ii) the issuer has Taildropped the PACK (wheel + .check.json + .delivery.txt + MANIFEST.json) to dell1 (it names the folder the pack arrived in). Do nothing before the GO.
Your earlier work on this route is in `org/tier2_senior/0.7.0_AE_CloudOps~CT1/deliverables/NFRA_CTLPLN.TO-CT-x-2.*`. dell1 runs click 8.5.0 as a transitive dependency of huggingface_hub (core requirement click>=8.4.2,<9.0.0): installing the checked click 8.3.1 into the box's interpreter would DOWNGRADE it and break that requirement, so every install is into a FRESH, ISOLATED venv, deleted after (the issuer's AMENDMENT 1 to TO-CT-x-2 stands).
</context>

<the_act>
1. **Receive.** Run `org/devices/intake/intake_receive.py verify`, then `prove`, then `install` (index-free, into a fresh venv created under the system temp directory with no system site packages; if `install` takes no target interpreter say so and use `<venv python> -m pip install --no-index --no-deps <the verified wheel>`). Save each full output, in order, to `org/tier2_senior/0.7.0_AE_CloudOps~CT1/deliverables/NFRA_CTLPLN.TO-CT-v-3.receive.txt`. A refusal (for example `PACK-DEFECT`) is the finding: do NOT author a MANIFEST or any file the sending side owns; say what the pack lacks.
2. **The lane's work runs.** Name the lane that asked for click from the CTO approval file the check record cites. Run ONE ordinary command of that lane's work that imports click, with the venv python; if none exists on dell1, run `<venv python> -c "import click; print('CLICK', click.__version__)"` and say so. Append the command and its output to the receive file.
3. **What dell1 downloaded.** Count dell1's outbound requests during step 1 (pip's verbose log, count the http(s) lines). Append `DOWNLOADS-TODAY requests=<n>`; expected 0.
4. **The stop.** Run `python org/devices/kit_pip_no_egress.py measure` on dell1 (it makes no request leave the machine) and record its last line to `.../NFRA_CTLPLN.TO-CT-v-3.pip-measure.txt`. Apply the passing form ONLY if the measure reports `ok=True` and a form other than NONE, in the way the kit's `wrap` and its docstring state (no change to any file outside this seat's own user-level pip config; record the file path and its before/after bytes' sha256 in the ledger; rollback = restore the recorded bytes). If the kit reports NONE, apply nothing and say so.
5. **One deliberate attempt.** Run once, through the applied form, `python -m pip download --no-deps -d <a new temporary folder> six==1.16.0 --index-url https://pypi.org/simple` (download only, nothing installed). Write the output to `.../NFRA_CTLPLN.TO-CT-v-3.blocked-download.txt` with a line `BLOCKED <what stopped it>` and whether the message named the laptop route, or `NOT-BLOCKED`. If it was NOT stopped, delete the temporary folder and the wheel, file one row, and say so.
6. Report to 2.0.0_SA_COO~C through 0.0.0_AB_MSTR~DELL1: the PIN, the four results, and the ledger entry. The reading aloud of the record to Andrew (including the account-takeover question) is the issuer's act with him, not yours.
</the_act>

<bounds>
- One package installed (click 8.3.1) into a deleted venv; no other install; the box interpreter's packages are not changed. The download in step 5 is download-only into a deleted folder. No push of CLOUD. No alert, monitor or timeout is built.
- A NEVER-2 ledger entry opened at the start of step 4 and closed at the end, naming the config file changed and the rollback.
</bounds>

<proof_of_spec>
<criterion id="CTv3-AC1" cell_refs="CT-v-3"><invocation>cat org/tier2_senior/0.7.0_AE_CloudOps~CT1/deliverables/NFRA_CTLPLN.TO-CT-v-3.receive.txt</invocation><expect>DOWNLOADS-TODAY requests=0</expect></criterion>
<criterion id="CTv3-AC2" cell_refs="CT-v-3"><invocation>cat org/tier2_senior/0.7.0_AE_CloudOps~CT1/deliverables/NFRA_CTLPLN.TO-CT-v-3.receive.txt</invocation><expect>CLICK 8.3.1</expect></criterion>
<criterion id="CTv3-AC3" cell_refs="CT-v-3"><invocation>cat org/tier2_senior/0.7.0_AE_CloudOps~CT1/deliverables/NFRA_CTLPLN.TO-CT-v-3.blocked-download.txt</invocation><expect>BLOCKED </expect></criterion>
</proof_of_spec>
<expected_criteria>CTv3-AC1,CTv3-AC2,CTv3-AC3</expected_criteria>
CTv3-AC3: a `NOT-BLOCKED` line fails the criterion and that failure is a finding again. Write the proof instance to `org/tier2_senior/0.7.0_AE_CloudOps~CT1/deliverables/NFRA_CTLPLN.TO-CT-v-3.dell-click-route-finished-and-download-stopped.proof_of_spec.json`, validate it with `python .tools/proof-of-spec-check.py <instance> CTv3-AC1,CTv3-AC2,CTv3-AC3`, and leave the status flip to the issuer.

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~CT1/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~CT1/logs/
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
org/missions/D0/NFRA/NFRA_CTLPLN/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE no schedule; one-time exercise.
comp-iam: DECLARED-NOT-APPLICABLE no AWS call; local pip config only.
comp-adversary: RUN -- the box interpreter's click downgraded (every install goes to a deleted venv); a MANIFEST authored by the receiver to turn a refusal green (forbidden by the act); the stop claimed from a config that an explicit --index-url overrides (the kit's explicit arm measures it, and step 5 uses an explicit --index-url); BLIND: a person typing another interpreter.
lane: the <paths> block names the seat's deliverables and logs, the ledger and its sentinel, and the surprise channel.
</preflight>

Source: `org/missions/D0/NFRA/NFRA_CTLPLN/ledger/ROUND_ANALYSIS.round6.md` section 4 (E3); rows NFRA_CTLPLN-D1-S1, D1-S3, D1-S5.
</task_order>
