<task_order id="NFRA_CTLPLN.TO-CT-u-4.dell1-ssh-tailnet-enable">
<to_id>NFRA_CTLPLN.TO-CT-u-4.dell1-ssh-tailnet-enable</to_id>
<project>NFRA_CTLPLN</project>
<issued_by>2.0.0_SA_COO~C</issued_by>
<issued_to>0.7.0_AE_CloudOps~CT1</issued_to>
<date>2026-10-12</date>
<status>withdrawn</status>
<status_reason>WITHDRAWN by the issuer 2.0.0_SA_COO~C as round 8's first act, per org/missions/D0/NFRA/NFRA_CTLPLN/ledger/ROUND_ANALYSIS.round7.md section 1 (1.0.0_SA_CTO msg 108494), so the row gate reads no staged order and the CVO can graduate D1-S8 and D1-S10. Nothing was done under this order. The FWD-27 per-box cell is NOT dropped: it is re-cut as an ACTIVE (pending, never staged) order in the same commit as its GO when Andrew's public keys land; the text of this order is the template. FWD-27 stays gated on Andrew's keys and his elevated line per box (a qualified essential wait, decomposition NFRA_CTLPLN_DECOMP.remote1.md).</status_reason>
<risk>WORLD</risk>
<proof_genre>BUILD</proof_genre>
<round>1</round>
<workstream>REMOTE</workstream>

<title>NFRA_CTLPLN workstream REMOTE CT-u-4: SSH over the tailnet on dell1 -- place the checked script, print Andrew's elevated lines, record the receipt</title>

<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.remote1.md</decomp_doc>
<owned_cells>CT-u-4</owned_cells>
<decomp_context>FWD-27 (PRD v0.23): every box on the tailnet answers an SSH login from the laptop by key, and nothing else. Elevation is the one person step: no agent session is elevated and none can answer a UAC prompt, so Andrew runs the enable lines in an elevated PowerShell over the RDP that already works (his word 2026-10-12 ~01:5xZ, record org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261012_015xZ_SSH_OVER_TAILNET_EXECUTE_COO_C.md). That wait is expressly qualified; everything around it is an act you take on demand.</decomp_context>
</decomp_ref>

<context>
STAGED. The issuer's GO (a crossbox file, not a broker message) arrives when `CT-u-1` and `CT-u-2` are merged. It names the merge commit (the PIN) that carries `.tools/ssh-tailnet-enable.ps1` and `.tools/ssh-tailnet-verify.py`, and the path of the committed PUBLIC key file(s) under `org/devices/ssh_public_keys/`. Do nothing before the GO.
Plan: `org/tier1_exec/1.0.0_SA_CTO/deliverables/LD0644_ROLLOUT_PLAN_CLUSTER_REMOTE_ACCESS_TAILNET_20261011.md` sections 3 and 7. Wave 1 measured this box: `elevated=False`, no sshd, no :22 rule, RDP tailnet-scoped.
</context>

<the_act>
1. At the GO, confirm the PIN is an ancestor of your branch (`git merge-base --is-ancestor <pin> HEAD`) and read the script's header. If not, pull the box's trunk the normal way; do not copy the file by hand.
2. Run the script UNELEVATED with `-Plan` on this box (it changes nothing) and keep its receipt: `org/devices/state/dell1/ssh_enable_<stamp>.json` with `"mode":"plan"`.
3. Print for Andrew, in your report to 0.0.0_AB_MSTR~DELL1 (who relays it), exactly two PowerShell lines, with absolute paths for this box:
   - LINE 1 (enable): `powershell -NoProfile -ExecutionPolicy Bypass -File <abs>\.tools\ssh-tailnet-enable.ps1 -PublicKey <abs>\org\devices\ssh_public_keys\<file>` -- installs the service, the tailnet-only rule, the shell and the key; leaves password auth ON.
   - LINE 2 (after the laptop proves a key login to this box): the same with `-DisablePassword`.
   Tell Andrew where each is run: an elevated PowerShell on this box ("Run as administrator").
4. When told the run is done, copy the apply receipt to the stable name `org/devices/state/dell1/ssh_enable_receipt.json` (`"mode":"apply"`) and commit it. Do NOT run the enable lines yourself; you are unelevated, and an elevated path you find (a scheduled task registered as SYSTEM) is NOT used without Andrew's express word.
5. Report to 0.0.0_AB_MSTR~DELL1: the PIN, the two lines, the receipt path. The key-login proof from the laptop is the issuer's act (it must come from the laptop); do not claim it.
</the_act>

<bounds>
- No change to RDP, to any firewall rule other than through the script, or to any other service. No private key is read, written or sent. No password is typed or stored.
- No push of CLOUD. No alert, monitor or timeout is built.
</bounds>

<proof_of_spec>
<criterion id="CTU4-AC1" cell_refs="CT-u-4"><invocation>cat org/devices/state/dell1/ssh_enable_receipt.json</invocation><expect>"mode":"apply"</expect></criterion>
<criterion id="CTU4-AC2" cell_refs="CT-u-4"><invocation>cat org/devices/state/dell1/ssh_enable_receipt.json</invocation><expect>"tailnet_rule_remote_address":"100.64.0.0/10"</expect></criterion>
</proof_of_spec>
<expected_criteria>CTU4-AC1,CTU4-AC2</expected_criteria>
Write the proof instance to `org/tier2_senior/0.7.0_AE_CloudOps~CT1/deliverables/NFRA_CTLPLN.TO-CT-u-4.dell1-ssh-tailnet-enable.proof_of_spec.json`, validate it with `python .tools/proof-of-spec-check.py <instance> CTU4-AC1,CTU4-AC2`, and leave the status flip to the issuer.

<paths>
org/devices/state/dell1/
org/tier2_senior/0.7.0_AE_CloudOps~CT1/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~CT1/logs/
org/missions/D0/NFRA/NFRA_CTLPLN/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE no schedule; one-time enable.
comp-iam: DECLARED-NOT-APPLICABLE no AWS call; local Windows service and firewall only, by Andrew's elevated run.
comp-adversary: RUN -- password auth turned off before a key login is proven (the script refuses without a key present before the run, and LINE 2 is held until the laptop proves it); the capability's default any-address rule left enabled (the script disables it; the receipt shows default_rule_enabled); an agent using an elevated path it found (forbidden by the act); a receipt claimed as the key-login proof (not the receipt's job); BLIND: whether a non-tailnet source is refused in practice (the rule's scope is the only evidence).
lane: the <paths> block names the receipt dir, the seat's deliverables and logs, and the surprise channel.
</preflight>

Source: PRD `prd/NFRA_CTLPLN_PRD.md` v0.23 FWD-27; CTO msg 108406.
</task_order>
