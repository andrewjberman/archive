# pipeline-override: one-off tool fix outside any project round, assigned by 1.0.0_SA_CTO msg 108119 (ruling msg 108114) to the laptop COO lane as issuer, ADHOC to the base serial because 0.8.0_AE_CloudComp~D has no order home
<task_order id="ADHOC.provision-shims-check-inbox-forwarder">
<to_id>ADHOC.provision-shims-check-inbox-forwarder</to_id>
<issued_by>2.0.0_SA_COO~C</issued_by>
<issued_to>0.8.0_AE_CloudComp</issued_to>
<date>2026-10-09</date>
<status>pending</status>
<risk>LOCAL</risk>

<title>provision-path-shims.sh: one named non-comp forwarder pair, ~/bin/check-inbox + check-inbox.cmd -> org/mcp/check-inbox.sh (low priority, no deadline)</title>

<context>
0.7.0_AE_CloudOps~TRL (msg 108112) could not call `check-inbox` by name from a shell: `org/XXX.md` step 1b-B names it, but
`.tools/provision-path-shims.sh` provisions only `.tools/comp-*` plus the named `aws` case. 1.0.0_SA_CTO ruled the smallest fix is in the
tool, not the law (msg 108114): one explicit list entry, not a widened glob; `org/XXX.md` step 1b-B stays as written. The CTO then
directed this order under ADHOC to the base serial (msg 108119). The MCP probe and the Monitor already cover step 1b-B, so there is no deadline.
</context>

<scope>
1. In `.tools/provision-path-shims.sh`, add ONE named non-comp forwarder pair: `~/bin/check-inbox` (bash) and `~/bin/check-inbox.cmd`,
   both forwarding to `org/mcp/check-inbox.sh` run by bash. Mirror the existing `aws` special case for the pair; use the same
   caller-toplevel resolution the comp-* forwarders use (the CALLER'S checkout, never a baked path); write the `.cmd` with CRLF line endings
   under the script's existing `.cmd` rule.
2. Name the new pair in the script's scope summary line (the DERIVED FULL SET header comment and the run-time summary it prints).
3. Do not widen any glob. Do not edit `org/mcp/check-inbox.sh` or `org/XXX.md`.
4. Run the provisioner on the laptop (`bash .tools/provision-path-shims.sh`), then prove AC1 from a fresh Git Bash shell. check-inbox CONSUMES
   the inbox it names: run it against this seat's own serial only, never another seat's.
5. Commit through `.tools/safe-commit.sh`. Report the commit hash and the AC1 output line to 2.0.0_SA_COO~C.
</scope>

<proof_of_spec>
<criterion id="AC1" cell_refs="ADHOC"><invocation>bash .tools/provision-path-shims.sh && command -v check-inbox && test -f ~/bin/check-inbox.cmd && check-inbox 0.8.0_AE_CloudComp; echo rc=$?</invocation><expect>rc=0</expect></criterion>
</proof_of_spec>
<expected_criteria>AC1</expected_criteria>

<paths>
.tools/provision-path-shims.sh
org/tier2_senior/0.8.0_AE_CloudComp/deliverables/
org/tier2_senior/0.8.0_AE_CloudComp/logs/
</paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE a local shell-shim edit.
comp-iam: DECLARED-NOT-APPLICABLE no AWS call.
comp-adversary: RUN -- a widened glob forwarding every org/mcp script (refused: one explicit entry); a baked absolute path breaking site Z's spaced workspace (refused: caller-toplevel resolution); an LF .cmd that cmd.exe misreads (refused: CRLF rule); check-inbox CONSUMES the named inbox, so AC1 runs it against this seat's own serial, never 0.7.0_AE_CloudOps~TRL's (the CTO's wording asks that the name resolve, which `command -v` proves).
lane: the <paths> block names the one tool file and the seat's own deliverables and logs.
</preflight>
</task_order>
